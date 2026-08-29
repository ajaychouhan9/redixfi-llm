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
def _prov():
    return {"pipeline_version": "test", "input_type": "test"}


def test_fixture_validation_catches_real_problems():
    doc = fixtures_mod.build_document("red_flag", [
        {"benchmark_id": "RF_A_1", "chunk_text": "x", "candidates": [],
         "case_polarity": "positive", "reference": {"risk_flag_type": None},
         "provenance": _prov()},
    ], {}, "now")
    problems = fixtures_mod.validate_document(doc)
    assert any("empty candidate list" in p for p in problems)

    doc = fixtures_mod.build_document("concall_summary", [
        {"benchmark_id": "CC_A_1", "symbol": "A", "input_text": "t", "provenance": _prov()},
        {"benchmark_id": "CC_A_1", "symbol": "B", "input_text": "t", "provenance": _prov()},
    ], {}, "now")
    assert any("duplicate benchmark_id" in p for p in fixtures_mod.validate_document(doc))


def test_fixture_validation_requires_provenance():
    doc = fixtures_mod.build_document("concall_summary", [
        {"benchmark_id": "CC_A_1", "symbol": "A", "input_text": "t"},
    ], {}, "now")
    assert any("missing 'provenance'" in p for p in fixtures_mod.validate_document(doc))


def test_fixture_validation_enforces_benchmark_id_prefix():
    doc = fixtures_mod.build_document("concall_summary", [
        {"benchmark_id": "XX_A_1", "symbol": "A", "input_text": "t",
         "provenance": _prov()},
    ], {}, "now")
    assert any("does not start with 'CC_'" in p for p in fixtures_mod.validate_document(doc))


def test_ask_ai_must_be_stamped_partial():
    """A rebuilt packet presented as exact would be the single most
    misleading thing this benchmark could ship."""
    case = {"benchmark_id": "ASK_A_1", "question": "q", "fact_packet": {},
            "provenance": _prov()}
    doc = fixtures_mod.build_document("ask_ai", [case], {}, "now")
    assert any("PACKET_RECONSTRUCTION_PARTIAL" in p
               for p in fixtures_mod.validate_document(doc))

    case["reconstruction_status"] = "PACKET_RECONSTRUCTION_PARTIAL"
    doc = fixtures_mod.build_document("ask_ai", [case], {}, "now")
    assert fixtures_mod.validate_document(doc) == []


def test_annual_report_fixture_requires_both_inputs():
    """Dual-input is the whole point of Phase A — a case with only the
    Evidence Finder side cannot be replayed against the pipeline that
    produced its reference."""
    case = {"benchmark_id": "AR_A_1", "symbol": "A", "evidence_text": "e",
            "provenance": _prov()}
    doc = fixtures_mod.build_document("annual_report_summary", [case], {}, "now")
    assert any("no legacy_input_text" in p for p in fixtures_mod.validate_document(doc))


def test_red_flag_requires_polarity_and_reference_key():
    case = {"benchmark_id": "RF_A_1", "chunk_text": "x",
            "candidates": ["auditor_qualification"], "provenance": _prov()}
    problems = fixtures_mod.validate_document(
        fixtures_mod.build_document("red_flag", [case], {}, "now"))
    assert any("case_polarity" in p for p in problems)
    assert any("risk_flag_type" in p for p in problems)


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
    assert "NO MODEL WAS CONSULTED" in rendered
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
        # The rule is "low-bit enough to fit a 16 GB card AND executable on
        # Turing", not "literally AutoAWQ". compressed-tensors int4 qualifies:
        # its W4A16 scheme reports get_min_capability()==75 in vLLM 0.28.0,
        # commented "Turing and up". Anything outside this set (fp8, nvfp4,
        # modelopt) needs Ampere+ and must not reach a T4 run.
        assert spec.quantization in ("awq", "gptq", "compressed-tensors"), (
            f"{name} uses {spec.quantization!r}; must be a low-bit method that "
            "fits 16 GB cards and runs on compute capability 7.5"
        )
        assert spec.max_model_len <= 65536, (
            f"{name} asks for {spec.max_model_len} context; KV cache on two "
            "16 GB cards cannot back that"
        )


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

    from app.prompts.annual_report_summary_legacy import SYSTEM_PROMPT as AR_LEGACY
    from app.prompts.concall_summary import SYSTEM_PROMPT as CC

    backend = EchoBackend()
    for system, expected in (
        (AR, "annual_report_summary"),
        (AR_LEGACY, "annual_report_summary_legacy"),
        (CC, "concall_summary"),
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
    from app.tasks import annual_report_summary_legacy as task_legacy
    from app.tasks import concall_summary as task_cc

    backend = EchoBackend()
    assert task_ar.run(backend, _ar_fixture(), "echo").ok
    assert task_legacy.run(backend, _ar_legacy_fixture(), "echo").ok
    assert task_cc.run(backend, _cc_fixture(), "echo").ok
    assert task_rf.run(backend, _rf_fixture(), "echo").ok
    assert task_ask.run(backend, _ask_fixture(), "echo").ok


@pytest.mark.parametrize("task", ["annual_report_summary", "concall_summary",
                                  "red_flag", "ask_ai"])
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
    # The five sections the founder specified must all be present.
    for section in ("SOURCE / EVIDENCE", "OLD — GPT-4o-mini OUTPUT",
                    "NEW — QWEN OUTPUT", "OBJECTIVE VALIDATION",
                    "HUMAN REVIEW NOTES"):
        assert section in rendered, f"missing review section: {section}"
    # ...and the quality dimensions must be listed but left unfilled.
    for dimension in ("factual quality", "evidence grounding", "completeness",
                      "hallucination", "numerical accuracy", "readability",
                      "compliance"):
        assert dimension in rendered, f"missing review dimension: {dimension}"


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
        assert task in ("annual_report_summary", "annual_report_summary_legacy",
                        "concall_summary", "red_flag", "ask_ai")
        assert get_model_spec(model)
    # Each phase must be pointed at a context that can actually hold it,
    # using the sizes MEASURED against the real exported fixtures.
    needs = {"concall_summary": 19308, "annual_report_summary": 16291,
             "annual_report_summary_legacy": 62456, "red_flag": 944, "ask_ai": 4640}
    for task, required in needs.items():
        spec = get_model_spec(RECOMMENDED_MODEL_BY_TASK[task])
        assert spec.max_model_len >= required, (
            f"{task} needs {required} tokens but {spec.name} offers "
            f"{spec.max_model_len}")


# --------------------------------------------------------------------------
# Phase D — concall (PRIMARY summarization benchmark)
# --------------------------------------------------------------------------
def _cc_fixture():
    return {
        "benchmark_id": "CC_T_1", "symbol": "T", "company_name": "T Ltd",
        "filing_date": "2025-08-02", "doc_kind": "earnings concall transcript",
        "input_text": "Management reported commissioning progress at two facilities.",
    }


def test_concall_accepts_a_valid_tone_label():
    from app.tasks import concall_summary as task_cc
    good = json.dumps({
        "summary": "Management reported commissioning progress at two facilities.",
        "tone_label": "Positive",
        "tone_note": "Management emphasised commissioning progress.",
    })
    result = task_cc.run(ScriptedBackend([good]), _cc_fixture(), "test-model")
    assert result.ok and result.output["tone_label"] == "Positive"


def test_concall_rejects_a_tone_label_outside_the_closed_set():
    """tone_label is a 4-way closed set in production. Anything else is a
    hard failure there, and must be a hard failure here."""
    from app.tasks import concall_summary as task_cc
    bad = json.dumps({
        "summary": "Management reported commissioning progress.",
        "tone_label": "Bullish",          # not in TONE_LABELS
        "tone_note": "Management emphasised progress.",
    })
    result = task_cc.run(ScriptedBackend([bad]), _cc_fixture(), "test-model")
    assert not result.ok
    assert "invalid tone_label" in result.rejections[0]["reason"]


def test_concall_does_not_apply_the_financial_figure_rule():
    """FINANCIAL_FIGURE_RE belongs only to the annual report summarizer.
    Production does not apply it to concalls, so neither may this."""
    from app.tasks import concall_summary as task_cc
    with_figure = json.dumps({
        "summary": "Management reported that volumes rose 12% during the quarter.",
        "tone_label": "Neutral",
        "tone_note": "Management described volume trends.",
    })
    result = task_cc.run(ScriptedBackend([with_figure]), _cc_fixture(), "test-model")
    assert result.ok


def test_concall_comparison_scores_tone_agreement():
    case = {"reference": {"summary": "s", "tone_label": "Positive", "tone_note": "n"}}
    agree = compare_mod.compare("concall_summary", case,
                                {"summary": "s", "tone_label": "Positive", "tone_note": "n"})
    assert agree["tone_label_agrees"] is True and agree["tone_label_valid"] is True

    disagree = compare_mod.compare("concall_summary", case,
                                   {"summary": "s", "tone_label": "Negative", "tone_note": "n"})
    assert disagree["tone_label_agrees"] is False

    invalid = compare_mod.compare("concall_summary", case,
                                  {"summary": "s", "tone_label": "Bullish", "tone_note": "n"})
    assert invalid["tone_label_valid"] is False


# --------------------------------------------------------------------------
# Phase A-legacy — the like-for-like replay
# --------------------------------------------------------------------------
def _ar_legacy_fixture():
    return {
        "benchmark_id": "AR_T_1", "symbol": "T", "company_name": "T Ltd",
        "fiscal_year": "FY2024-25", "filing_date": "2025-01-01", "page_count": 100,
        "legacy_input_text": "Chairman's letter. Management described capacity work.",
    }


def test_legacy_annual_report_uses_the_three_field_contract():
    from app.tasks import annual_report_summary_legacy as task_legacy
    good = json.dumps({
        "summary": "The report described management's stated priorities.",
        "bullets": ["Management described capacity work",
                    "The report stated a sourcing programme",
                    "Governance practices were reviewed"],
        "key_takeaway": "The report centred on stated operating priorities.",
    })
    result = task_legacy.run(ScriptedBackend([good]), _ar_legacy_fixture(), "test-model")
    assert result.ok
    assert "bullets" in result.output
    # important_risks did not exist in the legacy contract.
    assert "important_risks" not in result.output
    assert "key_points" not in result.output


def test_legacy_annual_report_refuses_without_the_legacy_input():
    from app.tasks import annual_report_summary_legacy as task_legacy
    fixture = _ar_legacy_fixture()
    del fixture["legacy_input_text"]
    backend = ScriptedBackend(["{}"])
    result = task_legacy.run(backend, fixture, "test-model")
    assert not result.ok and backend.calls == 0
    assert "legacy_input_text" in result.error


def test_legacy_prompt_differs_from_current_and_asks_for_bullets():
    from app.prompts import annual_report_summary as current
    from app.prompts import annual_report_summary_legacy as legacy
    assert legacy.SYSTEM_PROMPT != current.SYSTEM_PROMPT
    assert '"bullets"' in legacy.SYSTEM_PROMPT
    assert "important_risks" not in legacy.SYSTEM_PROMPT
    assert "important_risks" in current.SYSTEM_PROMPT


def test_annual_report_fixture_replays_both_ways(tmp_path):
    """One exported fixture, two readings — the point of dual-input."""
    subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "make_sample_fixtures.py"),
         "--out-dir", str(tmp_path), "--task", "annual_report_summary"],
        check=True, capture_output=True, cwd=ROOT)
    fs = fixtures_mod.load(str(tmp_path / "sample_annual_report_summary.json"))
    assert set(fs.replayable_as()) == {"annual_report_summary",
                                       "annual_report_summary_legacy"}

    current = run_evaluation(EchoBackend(), fs, "echo-model")
    assert current["replayed_as"] == "annual_report_summary"

    legacy = run_evaluation(EchoBackend(), fs, "echo-model",
                            replay_as="annual_report_summary_legacy")
    assert legacy["replayed_as"] == "annual_report_summary_legacy"
    assert legacy["results"][0]["comparison"]["comparison_is_like_for_like"] is True


def test_fixture_cannot_be_replayed_as_an_unrelated_task(tmp_path):
    subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "make_sample_fixtures.py"),
         "--out-dir", str(tmp_path), "--task", "concall_summary"],
        check=True, capture_output=True, cwd=ROOT)
    fs = fixtures_mod.load(str(tmp_path / "sample_concall_summary.json"))
    with pytest.raises(ValueError, match="cannot be replayed"):
        run_evaluation(EchoBackend(), fs, "echo-model", replay_as="red_flag")


# --------------------------------------------------------------------------
# validator fidelity — the call carve-out, found by real production data
# --------------------------------------------------------------------------
def test_summarizer_validator_allows_earnings_conference_call():
    """6 of 20 REAL production concall references were flagged non-compliant
    before this split existed. Both RedixFi summarizers carry the
    "call"-means-a-meeting carve-out; risk_flag_classifier does not."""
    from app.compliance.validators import summarizer_violation

    phrase = "The earnings conference call on February 13 highlighted turnover growth."
    assert summarizer_violation(phrase) is None
    # risk_flag_classifier's variant genuinely has no carve-out.
    assert violation(phrase) is not None
    # but a real trading call must still be rejected by both
    assert summarizer_violation("Place a buy call at the target price") is not None


def test_summarizer_validator_financial_figure_split():
    from app.compliance.validators import summarizer_violation
    figure = "Revenue rose 12% during the year."
    assert summarizer_violation(figure, check_financial_figures=True) is not None
    assert summarizer_violation(figure, check_financial_figures=False) is None


def test_annual_report_comparator_flags_legacy_schema_mismatch():
    """A legacy-shaped reference read with the current schema must NOT be
    reported as a compliance failure — that would read as production having
    emitted bad text, which is false."""
    legacy_ref = {
        "summary": "The report described management's stated priorities.",
        "bullets": ["a", "b", "c"],
        "key_takeaway": "A takeaway.",
    }
    r = compare_mod.compare("annual_report_summary", {"reference": legacy_ref}, {})
    assert r["reference_schema_matches_replay"] is False
    assert r["reference_compliance"] is None
    assert "like-for-like" in r["schema_mismatch_note"]

    current_ref = {"executive_summary": "The report described priorities.",
                   "key_points": ["a"], "important_risks": [], "key_takeaway": "T."}
    r2 = compare_mod.compare("annual_report_summary", {"reference": current_ref}, {})
    assert r2["reference_schema_matches_replay"] is True
    assert r2["schema_mismatch_note"] is None


@pytest.mark.skipif(not os.path.exists(os.path.join(ROOT, "fixtures",
                                                    "concall_benchmark.json")),
                    reason="real exported fixtures not present")
def test_real_production_references_pass_their_own_validators():
    """Regression guard against vendoring drift: every REAL production
    reference must pass the validator its own pipeline used."""
    from app.compliance.validators import summarizer_violation

    cc = fixtures_mod.load(os.path.join(ROOT, "fixtures", "concall_benchmark.json"))
    bad = [c["symbol"] for c in cc.cases
           if summarizer_violation(c["reference"]["summary"])
           or summarizer_violation(c["reference"]["tone_note"])]
    assert not bad, f"concall references failing their own validator: {bad}"

    ar = fixtures_mod.load(os.path.join(ROOT, "fixtures",
                                        "annual_report_benchmark.json"))
    bad = []
    for c in ar.cases:
        r = c["reference"]
        checks = [summarizer_violation(r.get("summary") or "", check_financial_figures=True),
                  summarizer_violation(r.get("key_takeaway") or "", check_financial_figures=True)]
        checks += [summarizer_violation(b, check_financial_figures=True)
                   for b in (r.get("bullets") or [])]
        if any(checks):
            bad.append(c["symbol"])
    assert not bad, f"annual report references failing their own validator: {bad}"


def test_ask_reference_backstop_artifact_is_separated_not_counted():
    """The causal backstop is derived from a REBUILT packet. An answer that
    was compliant when production wrote it must not be reported as a
    production compliance failure just because the rebuilt packet lost the
    news event that justified its causal language."""
    answer = "The score fell due to the reported order cancellation."
    case = {"reference": {"answer": answer, "refused": False}}

    art = compare_mod.compare("ask_ai", case, {"answer": "x", "refused": False,
                                               "causal_backstop": True})
    assert art["reference_compliance"] is None
    assert art["reference_compliance_backstop_artifact"] is True

    off = compare_mod.compare("ask_ai", case, {"answer": "x", "refused": False,
                                               "causal_backstop": False})
    assert off["reference_compliance"] is None
    assert off["reference_compliance_backstop_artifact"] is False

    # A genuine violation is still reported, backstop or not.
    real = compare_mod.compare(
        "ask_ai", {"reference": {"answer": "Place a buy call.", "refused": False}},
        {"answer": "x", "refused": False, "causal_backstop": True})
    assert real["reference_compliance"] is not None
    assert real["reference_compliance_backstop_artifact"] is False
