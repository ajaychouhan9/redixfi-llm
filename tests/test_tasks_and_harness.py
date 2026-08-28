"""Offline harness tests — no GPU, no network, no database."""
from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

from app.compliance.validators import ask_answer_violation, chunk_fails_compliance, violation
from app.evaluation import compare as compare_mod
from app.evaluation import fixtures as fixtures_mod
from app.evaluation import report as report_mod
from app.evaluation.runner import run_evaluation
from app.inference.base import Backend, GenerationRequest, GenerationResult, Message
from app.inference.echo import EchoBackend
from app.models.registry import get_model_spec, list_models
from app.tasks import annual_report_summary as task_ar
from app.tasks import ask_ai as task_ask
from app.tasks import red_flag as task_rf
from app.tasks.base import parse_json_object

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ScriptedBackend(Backend):
    """Returns a fixed sequence of raw strings, so a task's retry loop and
    validation can be driven deterministically."""

    name = "scripted"

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = 0

    def generate(self, request: GenerationRequest) -> GenerationResult:
        text = self.responses[min(self.calls, len(self.responses) - 1)]
        self.calls += 1
        if isinstance(text, Exception):
            return GenerationResult(text="", model=request.model, backend=self.name,
                                    error=str(text))
        return GenerationResult(text=text, model=request.model, backend=self.name,
                                prompt_tokens=10, completion_tokens=5, total_tokens=15)

    def stream(self, request):
        yield self.generate(request).text

    def health(self):
        return {"backend": self.name, "status": "ok"}


# --------------------------------------------------------------------------
# validators
# --------------------------------------------------------------------------
def test_violation_rejects_forward_tense_and_forbidden_words():
    assert violation("Revenue will rise") is not None
    assert violation("Management stated a goal of expanding capacity") is None
    assert violation("Place a buy order") is not None
    assert violation("FII net buy was recorded") is None


def test_financial_figure_check_is_summarizer_only():
    text = "Revenue grew 12% during the year"
    assert violation(text, check_financial_figures=True) is not None
    assert violation(text, check_financial_figures=False) is None
    assert violation("The order book stood at Rs 4,200 crore",
                     check_financial_figures=True) is not None


def test_call_carveout_distinguishes_meeting_from_trading():
    assert chunk_fails_compliance("Discussed on the earnings call") is None
    assert chunk_fails_compliance("Noted on the last call") is None
    assert chunk_fails_compliance("A buy call with a target price") is not None


def test_causal_backstop_only_fires_when_enabled():
    answer = "The score fell because of sector weakness."
    assert ask_answer_violation(answer, causal_backstop=True) is not None
    assert ask_answer_violation(answer, causal_backstop=False) is None


# --------------------------------------------------------------------------
# JSON parsing
# --------------------------------------------------------------------------
def test_parse_json_object_handles_bare_fenced_and_broken():
    parsed, repaired, error = parse_json_object('{"a": 1}')
    assert parsed == {"a": 1} and not repaired and error is None

    parsed, repaired, error = parse_json_object('```json\n{"a": 2}\n```')
    assert parsed == {"a": 2} and repaired and error is None

    parsed, repaired, error = parse_json_object("not json at all")
    assert parsed is None and error


# --------------------------------------------------------------------------
# Phase A
# --------------------------------------------------------------------------
def _ar_fixture():
    return {
        "fixture_id": "T:FY2024-25", "symbol": "T", "company_name": "T Ltd",
        "fiscal_year": "FY2024-25", "filing_date": "2025-01-01", "page_count": 100,
        "evidence_text": "[Evidence chunk 1, page ~2]\nManagement described capacity work.",
    }


def test_annual_report_accepts_compliant_output():
    good = json.dumps({
        "executive_summary": "The report described management's stated priorities.",
        "key_points": ["Management described capacity work",
                       "The report stated a sourcing programme",
                       "Governance practices were reviewed"],
        "important_risks": [],
        "key_takeaway": "The report centred on stated operating priorities.",
    })
    result = task_ar.run(ScriptedBackend([good]), _ar_fixture(), "test-model")
    assert result.ok and result.attempts == 1
    assert len(result.output["key_points"]) == 3
    # Legacy fields RedixFi also writes must be present.
    assert result.output["summary"] == result.output["executive_summary"]
    assert result.output["bullets"] == result.output["key_points"]


def test_annual_report_retries_then_succeeds_on_a_compliance_failure():
    bad = json.dumps({
        "executive_summary": "Revenue will expand next year.",
        "key_points": ["a", "b", "c"], "important_risks": [],
        "key_takeaway": "Fine.",
    })
    good = json.dumps({
        "executive_summary": "The report described management's stated priorities.",
        "key_points": ["Management described capacity work",
                       "The report stated a sourcing programme",
                       "Governance practices were reviewed"],
        "important_risks": [],
        "key_takeaway": "The report centred on stated operating priorities.",
    })
    backend = ScriptedBackend([bad, good])
    result = task_ar.run(backend, _ar_fixture(), "test-model")
    assert result.ok and result.attempts == 2
    assert "forward-tense" in result.rejections[0]["reason"]


def test_annual_report_bullet_count_bound_is_enforced():
    too_many = json.dumps({
        "executive_summary": "The report described stated priorities.",
        "key_points": [f"point {i}" for i in range(9)],
        "important_risks": [], "key_takeaway": "A takeaway.",
    })
    result = task_ar.run(ScriptedBackend([too_many]), _ar_fixture(), "test-model")
    assert not result.ok
    assert "outside [3, 5]" in result.rejections[0]["reason"]


def test_annual_report_writes_no_placeholder_on_total_failure():
    bad = json.dumps({"executive_summary": "Revenue will rise.",
                      "key_points": ["a", "b", "c"], "important_risks": [],
                      "key_takeaway": "It will rise."})
    result = task_ar.run(ScriptedBackend([bad]), _ar_fixture(), "test-model")
    assert not result.ok
    assert result.output == {}          # no placeholder, matching RedixFi
    assert result.attempts == task_ar.MAX_ATTEMPTS == 3


# --------------------------------------------------------------------------
# Phase B
# --------------------------------------------------------------------------
def _rf_fixture(candidates=("related_party_transaction",)):
    return {
        "fixture_id": "c1",
        "chunk_text": "Related party transactions were reviewed by the auditors.",
        "candidates": list(candidates),
    }


def test_red_flag_confirms_and_emits_metadata_contract():
    good = json.dumps({
        "category": "related_party_transaction",
        "summary": "The excerpt states related party transactions were reviewed.",
    })
    result = task_rf.run(ScriptedBackend([good]), _rf_fixture(), "test-model")
    assert result.ok
    assert result.output["risk_flag_type"] == "related_party_transaction"
    assert result.output["risk_classified"] is True


def test_red_flag_omits_keys_rather_than_nulling_them():
    """ChromaDB metadata cannot hold None — the keys must be ABSENT."""
    result = task_rf.run(
        ScriptedBackend([json.dumps({"category": None, "summary": ""})]),
        _rf_fixture(), "test-model",
    )
    assert result.ok
    assert result.output == {"risk_classified": True}
    assert "risk_flag_type" not in result.output
    assert "risk_flag_summary" not in result.output


def test_red_flag_rejects_a_category_outside_the_candidates():
    out_of_set = json.dumps({"category": "promoter_pledge", "summary": "Shares pledged."})
    result = task_rf.run(ScriptedBackend([out_of_set]), _rf_fixture(), "test-model")
    assert "risk_flag_type" not in result.output
    assert "not in candidates" in result.rejections[0]["reason"]


def test_red_flag_drops_a_noncompliant_summary():
    bad = json.dumps({
        "category": "related_party_transaction",
        "summary": "The company will expand related party dealings.",
    })
    result = task_rf.run(ScriptedBackend([bad]), _rf_fixture(), "test-model")
    assert result.output == {"risk_classified": True}
    assert "failed compliance" in result.rejections[0]["reason"]


def test_red_flag_spends_no_call_without_candidates():
    backend = ScriptedBackend(["should never be used"])
    result = task_rf.run(backend, _rf_fixture(candidates=()), "test-model")
    assert result.ok and backend.calls == 0 and result.attempts == 0


# --------------------------------------------------------------------------
# Phase C
# --------------------------------------------------------------------------
def _ask_fixture(cause_available=False):
    return {
        "fixture_id": "q1", "symbol": "T",
        "question": "What did management say about strategy?",
        "fact_packet": {
            "symbol": "T",
            "change_explanation": {"cause_available": cause_available},
            "document_chunks": [{"text": "Management described capacity work."}],
        },
    }


def test_ask_accepts_a_compliant_answer():
    good = json.dumps({"answer": "Management described capacity work.",
                       "refused": False, "refusal_reason": None})
    result = task_ask.run(ScriptedBackend([good]), _ask_fixture(), "test-model")
    assert result.ok and result.output["refused"] is False


def test_ask_refusal_returns_immediately_without_retry():
    refusal = json.dumps({"answer": "I don't have that.", "refused": True,
                          "refusal_reason": "not in packet"})
    backend = ScriptedBackend([refusal, refusal])
    result = task_ask.run(backend, _ask_fixture(), "test-model")
    assert result.ok and result.output["refused"] is True
    assert backend.calls == 1


def test_ask_causal_backstop_derives_from_the_packet():
    assert task_ask.derive_causal_backstop(_ask_fixture(cause_available=False)) is True
    assert task_ask.derive_causal_backstop(_ask_fixture(cause_available=True)) is False


def test_ask_budget_is_two_attempts_not_three():
    bad = json.dumps({"answer": "It will rise.", "refused": False, "refusal_reason": None})
    backend = ScriptedBackend([bad, bad, bad])
    result = task_ask.run(backend, _ask_fixture(), "test-model")
    assert not result.ok
    assert backend.calls == task_ask.MAX_ATTEMPTS == 2


# --------------------------------------------------------------------------
# fixtures / comparison / report
# --------------------------------------------------------------------------
def test_fixture_validation_catches_real_problems():
    doc = fixtures_mod.build_document("red_flag", [
        {"fixture_id": "a", "chunk_text": "x", "candidates": []},
    ], {}, "now")
    problems = fixtures_mod.validate_document(doc)
    assert any("empty candidate list" in p for p in problems)

    doc = fixtures_mod.build_document("annual_report_summary", [
        {"fixture_id": "a", "symbol": "A", "evidence_text": "t"},
        {"fixture_id": "a", "symbol": "B", "evidence_text": "t"},
    ], {}, "now")
    assert any("duplicate fixture_id" in p for p in fixtures_mod.validate_document(doc))


def test_red_flag_comparison_classifies_every_outcome():
    def outcome(ref, cand):
        return compare_mod.compare_red_flag({"reference": ref}, cand)["outcome"]

    flagged = {"risk_flag_type": "auditor_qualification", "risk_flag_summary": "s"}
    none_flag = {"risk_classified": True}
    assert outcome(flagged, flagged) == "agree"
    assert outcome({"risk_flag_type": None}, none_flag) == "agree_no_flag"
    assert outcome(flagged, none_flag) == "false_negative"
    assert outcome({"risk_flag_type": None}, flagged) == "false_positive"
    assert outcome(flagged, {"risk_flag_type": "contingent_liability"}) == "category_mismatch"


def test_aggregate_refuses_to_emit_a_quality_score():
    summary = compare_mod.aggregate("ask_ai", [
        {"ok": True, "comparison": {"reference_present": True, "lexical_overlap": 0.5}},
    ])
    assert summary["quality_verdict"].startswith("NOT COMPUTED")


def test_report_flags_an_echo_run_as_non_evidence():
    run = {
        "task": "ask_ai", "model": "m", "backend": "echo", "run_id": "r",
        "generated_at": "now", "sampling": {}, "fixture": {}, "environment": {},
        "summary": {"cases": 0}, "results": [],
    }
    rendered = report_mod.render(run)
    assert "echo` backend" in rendered
    assert "EXPERIMENTAL / NOT PRODUCTION" in rendered


# --------------------------------------------------------------------------
# registry / echo / end-to-end
# --------------------------------------------------------------------------
def test_registry_never_offers_bfloat16_to_a_t4():
    for name in list_models():
        spec = get_model_spec(name)
        assert spec.dtype == "float16", (
            f"{name} requests {spec.dtype}; T4 (Turing) has no bf16 datapath"
        )
        assert spec.quantization == "awq", f"{name} must be quantized to fit 16 GB cards"


def test_registry_serve_args_are_well_formed():
    spec = get_model_spec("qwen3-14b-awq")
    args = spec.to_server_args()
    assert args[0] == spec.hf_repo
    assert "--dtype" in args and "float16" in args
    assert "--quantization" in args


def test_echo_backend_detects_each_task_and_marks_itself_synthetic():
    from app.prompts.annual_report_summary import SYSTEM_PROMPT as AR
    from app.prompts.ask_ai import ASK_SYSTEM_TEMPLATE
    from app.prompts.red_flag import SYSTEM_PROMPT as RF

    backend = EchoBackend()
    for system, expected in (
        (AR, "annual_report_summary"),
        (RF, "red_flag"),
        (ASK_SYSTEM_TEMPLATE.format(symbol="T"), "ask_ai"),
    ):
        result = backend.generate(GenerationRequest(
            messages=[Message("system", system), Message("user", "x")], model="echo",
        ))
        assert result.raw["detected_task"] == expected
        assert result.raw["is_synthetic"] is True
        assert json.loads(result.text)


def test_echo_output_passes_every_task_validator():
    """The echo stubs must be compliance-clean, or a harness run fails for
    reasons that have nothing to do with the harness."""
    backend = EchoBackend()
    assert task_ar.run(backend, _ar_fixture(), "echo").ok
    assert task_rf.run(backend, _rf_fixture(), "echo").ok
    assert task_ask.run(backend, _ask_fixture(), "echo").ok


@pytest.mark.parametrize("task", ["annual_report_summary", "red_flag", "ask_ai"])
def test_end_to_end_sample_fixture_runs_green(tmp_path, task):
    """Generates the synthetic fixture, runs it through the full harness,
    and renders the review sheet — the whole local pipeline, no GPU."""
    subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "make_sample_fixtures.py"),
         "--out-dir", str(tmp_path), "--task", task],
        check=True, capture_output=True, cwd=ROOT,
    )
    path = tmp_path / f"sample_{task}.json"
    assert path.exists()

    fixture_set = fixtures_mod.load(str(path))
    assert fixture_set.source["synthetic"] is True
    run = run_evaluation(EchoBackend(), fixture_set, "echo-model")

    assert run["summary"]["cases"] == len(fixture_set.cases)
    assert run["summary"]["quality_verdict"].startswith("NOT COMPUTED")
    rendered = report_mod.render(run)
    assert "Human review" in rendered


# --------------------------------------------------------------------------
# context budget gate
# --------------------------------------------------------------------------
def test_context_check_catches_a_phase_a_overflow():
    """The real defect this gate exists for: RedixFi's Evidence Finder emits
    a ~20k-token budget, which does not fit qwen3-14b-awq's 16k context."""
    from app.evaluation import context_check

    # Sized to the REAL measurement: Evidence Finder at its 20k-token budget
    # produced ~23.6k prompt tokens on ABB/TCS/RELIANCE. This phrase is ~6
    # tokens, so ~3,300 repeats lands in that range.
    big = {"fixture_id": "big", "symbol": "T", "company_name": "T",
           "fiscal_year": "FY", "filing_date": "d", "page_count": 400,
           "evidence_text": "management described capacity work. " * 3300}

    over = context_check.check(
        "annual_report_summary", [big], get_model_spec("qwen3-14b-awq"), 1024,
    )
    assert over["fits"] is False
    assert over["cases_that_overflow"] == 1
    assert over["options"]

    under = context_check.check(
        "annual_report_summary", [big], get_model_spec("qwen3-14b-awq-tp2"), 1024,
    )
    assert under["fits"] is True


def test_context_check_passes_small_prompts():
    from app.evaluation import context_check
    report = context_check.check(
        "red_flag", [_rf_fixture()], get_model_spec("qwen3-14b-awq"), 512,
    )
    assert report["fits"] is True
    assert report["max_prompt_tokens"] < 2000


def test_recommended_model_per_task_is_registered():
    from app.models.registry import RECOMMENDED_MODEL_BY_TASK
    for task, model in RECOMMENDED_MODEL_BY_TASK.items():
        assert task in ("annual_report_summary", "red_flag", "ask_ai")
        assert get_model_spec(model)
    # Phase A must not be pointed at a context that cannot hold it.
    assert get_model_spec(
        RECOMMENDED_MODEL_BY_TASK["annual_report_summary"]
    ).max_model_len >= 32768
