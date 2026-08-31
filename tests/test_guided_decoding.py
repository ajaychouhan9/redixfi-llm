"""Guided (structured) decoding — offline proofs.

WHAT THESE CAN AND CANNOT ESTABLISH
-----------------------------------
PROVEN HERE (no GPU, no network):
  * every schema is valid JSON Schema and xgrammar-safe for vLLM 0.28.0
  * a schema-shaped payload survives the REAL task parser with every field
    populated — i.e. the schema matches the parser, not just the prompt
  * VLLMInProcessBackend builds `SamplingParams(structured_outputs=
    StructuredOutputsParams(json=<schema>))` — verified against a stub that
    mimics the 0.28.0 signature, since vLLM is not installable here
  * the OpenAI-compatible backend emits `response_format: json_schema`
  * telemetry separates "guided and clean" from "guided but repaired"

NOT PROVEN HERE — needs the real GPU run:
  * that xgrammar actually constrains decoding on T4 / AWQ / TP=2
  * that json_repair_used genuinely drops to 0 on real generations
Only the Kaggle smoke run can establish those. See RUNBOOK_STEP4.md.
"""
from __future__ import annotations

import json
import sys
import types

import pytest

from app.evaluation import compare as compare_mod
from app.inference.base import GenerationRequest, GenerationResult, Message
from app.inference.echo import EchoBackend
from app.inference.openai_compat import OpenAICompatBackend
from app.schemas.output_schemas import (
    STATIC_SCHEMAS,
    red_flag_schema,
    schema_for_task,
    xgrammar_unsupported_features,
)
from app.tasks import annual_report_summary as task_ar
from app.tasks import annual_report_summary_legacy as task_legacy
from app.tasks import ask_ai as task_ask
from app.tasks import concall_summary as task_cc
from app.tasks import red_flag as task_rf

ALL_TASKS = ["annual_report_summary", "annual_report_summary_legacy",
             "concall_summary", "ask_ai", "red_flag"]


def _fixture_for(task):
    if task == "red_flag":
        return {"candidates": ["auditor_qualification", "contingent_liability"]}
    return None


# --------------------------------------------------------------------------
# schema shape + xgrammar safety
# --------------------------------------------------------------------------
@pytest.mark.parametrize("task", ALL_TASKS)
def test_schema_is_serialisable_and_well_formed(task):
    schema = schema_for_task(task, _fixture_for(task))
    assert schema is not None
    json.dumps(schema)                       # must survive the wire
    assert schema["type"] == "object"
    assert schema["required"]
    assert schema["additionalProperties"] is False
    for name in schema["required"]:
        assert name in schema["properties"], f"{task}: required '{name}' not defined"


@pytest.mark.parametrize("task", ALL_TASKS)
def test_schema_is_xgrammar_safe(task):
    """A schema using an unsupported construct silently pushes decoding onto
    a fallback backend on the GPU. Catch that here, not there."""
    bad = xgrammar_unsupported_features(schema_for_task(task, _fixture_for(task)))
    assert not bad, f"{task} uses xgrammar-unsupported constructs: {bad}"


def test_xgrammar_guard_actually_detects_bad_constructs():
    """A guard that cannot fail is worthless."""
    assert xgrammar_unsupported_features(
        {"type": "object", "properties": {"n": {"type": "integer", "multipleOf": 2}}})
    assert xgrammar_unsupported_features(
        {"type": "object", "properties": {"a": {"type": "array", "uniqueItems": True}}})
    assert xgrammar_unsupported_features(
        {"type": "object", "patternProperties": {"^x": {"type": "string"}}})
    assert xgrammar_unsupported_features(
        {"type": "object", "properties": {"s": {"type": "string", "format": "byte"}}})
    # ...and does NOT flag what we actually use
    assert not xgrammar_unsupported_features(
        {"type": "object",
         "properties": {"a": {"type": "array", "items": {"type": "string"},
                              "minItems": 3, "maxItems": 5}}})


def test_red_flag_schema_is_per_request_and_nullable():
    """category must be one of THIS chunk's candidates, or null — not the
    full category set. Anything else re-opens the rejection path the schema
    exists to close."""
    schema = red_flag_schema(["promoter_pledge"])
    variants = schema["properties"]["category"]["anyOf"]
    enum = next(v for v in variants if "enum" in v)["enum"]
    assert enum == ["promoter_pledge"]
    assert {"type": "null"} in variants

    with pytest.raises(ValueError):
        red_flag_schema([])          # no candidates -> no LLM call in production


def test_annual_report_schema_encodes_the_bullet_bound():
    kp = schema_for_task("annual_report_summary")["properties"]["key_points"]
    assert (kp["minItems"], kp["maxItems"]) == (task_ar.BULLET_MIN, task_ar.BULLET_MAX)
    # important_risks must stay unbounded below — [] is a valid answer.
    assert "minItems" not in schema_for_task(
        "annual_report_summary")["properties"]["important_risks"]


def test_concall_schema_pins_the_closed_tone_set():
    from app.prompts.concall_summary import TONE_LABELS
    assert schema_for_task("concall_summary")["properties"]["tone_label"]["enum"] == list(
        TONE_LABELS)


# --------------------------------------------------------------------------
# schemas match the REAL parsers, not just the prompts
# --------------------------------------------------------------------------
class _Fixed:
    """Backend returning one canned payload."""
    name = "fixed"

    def __init__(self, payload):
        self.payload = payload
        self.requests = []

    def generate(self, request):
        self.requests.append(request)
        return GenerationResult(
            text=json.dumps(self.payload), model=request.model, backend=self.name,
            prompt_tokens=1, completion_tokens=1, total_tokens=2,
            structured_output_used=request.json_schema is not None,
            structured_output_mode="json_schema" if request.json_schema else None)

    def stream(self, request):
        yield self.generate(request).text

    def health(self):
        return {"backend": self.name, "status": "ok"}


SCHEMA_SHAPED = {
    "annual_report_summary": {
        "executive_summary": "The report described stated priorities.",
        "key_points": ["Management described capacity work",
                       "The report stated a sourcing programme",
                       "Governance practices were reviewed"],
        "important_risks": [],
        "key_takeaway": "The report centred on stated priorities.",
    },
    "annual_report_summary_legacy": {
        "summary": "The report described stated priorities.",
        "bullets": ["Management described capacity work",
                    "The report stated a sourcing programme",
                    "Governance practices were reviewed"],
        "key_takeaway": "The report centred on stated priorities.",
    },
    "concall_summary": {
        "summary": "Management reported commissioning progress.",
        "tone_label": "Neutral",
        "tone_note": "Management described activity in even terms.",
    },
    "ask_ai": {"answer": "Management described capacity work.",
               "refused": False, "refusal_reason": None},
    "red_flag": {"category": "auditor_qualification",
                 "summary": "The excerpt states the auditor issued a qualified opinion."},
}

RUNNERS = {
    "annual_report_summary": (task_ar.run, {
        "benchmark_id": "AR_X_1", "symbol": "X", "company_name": "X",
        "fiscal_year": "FY", "filing_date": "d", "page_count": 1,
        "evidence_text": "evidence"}),
    "annual_report_summary_legacy": (task_legacy.run, {
        "benchmark_id": "AR_X_1", "symbol": "X", "company_name": "X",
        "fiscal_year": "FY", "filing_date": "d", "page_count": 1,
        "legacy_input_text": "front slice"}),
    "concall_summary": (task_cc.run, {
        "benchmark_id": "CC_X_1", "symbol": "X", "company_name": "X",
        "filing_date": "d", "doc_kind": "earnings concall transcript",
        "input_text": "transcript"}),
    "ask_ai": (task_ask.run, {
        "benchmark_id": "ASK_X_1", "symbol": "X", "question": "q",
        "fact_packet": {"symbol": "X"}}),
    "red_flag": (task_rf.run, {
        "benchmark_id": "RF_X_1", "chunk_text": "qualified opinion",
        "candidates": ["auditor_qualification"]}),
}


@pytest.mark.parametrize("task", ALL_TASKS)
def test_schema_shaped_payload_survives_the_real_parser(task):
    """The failure this guards against: a schema that is valid JSON but the
    wrong SHAPE moves the failure instead of fixing it. A payload built to
    the schema must parse cleanly AND populate every field."""
    runner, fixture = RUNNERS[task]
    backend = _Fixed(SCHEMA_SHAPED[task])
    result = runner(backend, fixture, "test-model")

    assert result.ok, f"{task} rejected a schema-shaped payload: {result.error} {result.rejections}"
    assert not result.json_repair_used, f"{task}: schema-shaped payload needed repair"
    assert result.structured_output_used, f"{task}: schema was not passed to the backend"
    assert result.output, f"{task}: parser produced an empty output"

    if task == "annual_report_summary":
        assert len(result.output["key_points"]) == 3
        assert result.output["executive_summary"]
    if task == "annual_report_summary_legacy":
        assert len(result.output["bullets"]) == 3
        assert "important_risks" not in result.output
    if task == "concall_summary":
        assert result.output["tone_label"] == "Neutral"
    if task == "red_flag":
        assert result.output["risk_flag_type"] == "auditor_qualification"
    if task == "ask_ai":
        assert result.output["refused"] is False


@pytest.mark.parametrize("task", ALL_TASKS)
def test_every_task_passes_a_schema_to_the_backend(task):
    runner, fixture = RUNNERS[task]
    backend = _Fixed(SCHEMA_SHAPED[task])
    runner(backend, fixture, "test-model")
    sent = backend.requests[0]
    assert sent.json_schema is not None, f"{task} sent no json_schema"
    assert sent.json_schema == schema_for_task(task, fixture)


def test_red_flag_null_category_is_expressible():
    """A keyword false positive must be able to answer null — 2 of the 6
    first-run red-flag cases were exactly that."""
    backend = _Fixed({"category": None, "summary": ""})
    runner, fixture = RUNNERS["red_flag"]
    result = runner(backend, fixture, "test-model")
    assert result.ok
    assert result.output == {"risk_classified": False}
    assert "risk_flag_type" not in result.output


# --------------------------------------------------------------------------
# vLLM 0.28.0 call construction, against a stub of the real signature
# --------------------------------------------------------------------------
@pytest.fixture()
def stub_vllm(monkeypatch):
    """Mimics vLLM 0.28.0: SamplingParams(structured_outputs=...) and
    vllm.sampling_params.StructuredOutputsParams(json=...). vLLM cannot be
    installed on this machine, so this proves the CALL SHAPE only."""
    captured = {}

    class StructuredOutputsParams:
        def __init__(self, json=None, json_object=None, **kw):
            if (json is None) == (json_object is None):
                raise ValueError("exactly one constraint must be set")
            self.json = json
            self.json_object = json_object

    class SamplingParams:
        def __init__(self, structured_outputs=None, **kw):
            self.structured_outputs = structured_outputs
            self.kw = kw
            captured["params"] = self

    vllm_mod = types.ModuleType("vllm")
    vllm_mod.SamplingParams = SamplingParams
    sp_mod = types.ModuleType("vllm.sampling_params")
    sp_mod.StructuredOutputsParams = StructuredOutputsParams
    sp_mod.SamplingParams = SamplingParams
    monkeypatch.setitem(sys.modules, "vllm", vllm_mod)
    monkeypatch.setitem(sys.modules, "vllm.sampling_params", sp_mod)
    return captured


def _vllm_backend(monkeypatch):
    from app.inference.vllm_inprocess import VLLMInProcessBackend

    class _Engine:
        def generate(self, prompts, params):
            out = types.SimpleNamespace(
                text='{"answer":"x","refused":false,"refusal_reason":null}',
                token_ids=[1, 2, 3], finish_reason="stop")
            return [types.SimpleNamespace(outputs=[out], prompt_token_ids=[1])]

        def get_tokenizer(self):
            raise RuntimeError("no tokenizer in the stub")

    return VLLMInProcessBackend(_Engine(), "qwen3-14b-awq-tp2")


def test_vllm_backend_builds_structured_outputs_from_schema(stub_vllm, monkeypatch):
    backend = _vllm_backend(monkeypatch)
    schema = schema_for_task("ask_ai")
    result = backend.generate(GenerationRequest(
        messages=[Message("user", "hi")], model="m", json_mode=True,
        json_schema=schema, max_tokens=32))

    params = stub_vllm["params"]
    assert params.structured_outputs is not None, "structured_outputs was not passed"
    assert params.structured_outputs.json == schema
    assert params.structured_outputs.json_object is None
    assert result.structured_output_used is True
    assert result.structured_output_mode == "json_schema"


def test_vllm_backend_falls_back_to_json_object_without_a_schema(stub_vllm, monkeypatch):
    backend = _vllm_backend(monkeypatch)
    backend.generate(GenerationRequest(
        messages=[Message("user", "hi")], model="m", json_mode=True, max_tokens=32))
    so = stub_vllm["params"].structured_outputs
    assert so.json is None and so.json_object is True


def test_vllm_backend_sends_nothing_when_not_asked(stub_vllm, monkeypatch):
    backend = _vllm_backend(monkeypatch)
    result = backend.generate(GenerationRequest(
        messages=[Message("user", "hi")], model="m", max_tokens=32))
    assert stub_vllm["params"].structured_outputs is None
    assert result.structured_output_used is False


def test_vllm_backend_reports_honestly_when_vllm_lacks_the_kwarg(monkeypatch):
    """An older vLLM without `structured_outputs` must NOT be reported as
    guided — a silent downgrade would look like success while repair does
    all the work."""
    class SamplingParams:
        def __init__(self, structured_outputs=None, **kw):
            if structured_outputs is not None:
                raise TypeError("unexpected keyword 'structured_outputs'")

    class StructuredOutputsParams:
        def __init__(self, **kw):
            pass

    vllm_mod = types.ModuleType("vllm")
    vllm_mod.SamplingParams = SamplingParams
    sp_mod = types.ModuleType("vllm.sampling_params")
    sp_mod.StructuredOutputsParams = StructuredOutputsParams
    monkeypatch.setitem(sys.modules, "vllm", vllm_mod)
    monkeypatch.setitem(sys.modules, "vllm.sampling_params", sp_mod)

    backend = _vllm_backend(monkeypatch)
    result = backend.generate(GenerationRequest(
        messages=[Message("user", "hi")], model="m",
        json_schema=schema_for_task("ask_ai"), max_tokens=32))
    assert result.ok
    assert result.structured_output_used is False
    assert result.structured_output_mode is None


# --------------------------------------------------------------------------
# OpenAI-compatible surface + telemetry
# --------------------------------------------------------------------------
def test_openai_compat_emits_json_schema_response_format():
    backend = OpenAICompatBackend(base_url="http://x/v1")
    schema = schema_for_task("concall_summary")
    body = backend._body(GenerationRequest(
        messages=[Message("user", "hi")], model="m",
        json_mode=True, json_schema=schema))
    rf = body["response_format"]
    assert rf["type"] == "json_schema"
    assert rf["json_schema"]["schema"] == schema
    assert rf["json_schema"]["strict"] is True

    # json_mode alone still degrades to json_object
    body2 = backend._body(GenerationRequest(
        messages=[Message("user", "hi")], model="m", json_mode=True))
    assert body2["response_format"] == {"type": "json_object"}


def test_echo_reports_structured_output_when_a_schema_is_given():
    backend = EchoBackend()
    from app.prompts.concall_summary import SYSTEM_PROMPT
    req = GenerationRequest(messages=[Message("system", SYSTEM_PROMPT),
                                      Message("user", "x")],
                            model="echo", json_schema=schema_for_task("concall_summary"))
    assert backend.generate(req).structured_output_used is True
    req2 = GenerationRequest(messages=[Message("system", SYSTEM_PROMPT),
                                       Message("user", "x")], model="echo")
    assert backend.generate(req2).structured_output_used is False


def test_aggregate_separates_guided_clean_from_guided_repaired():
    rows = [
        {"ok": True, "structured_output_used": True, "json_repair_used": False,
         "comparison": {}},
        {"ok": True, "structured_output_used": True, "json_repair_used": True,
         "comparison": {}},
        {"ok": True, "structured_output_used": False, "json_repair_used": True,
         "comparison": {}},
    ]
    s = compare_mod.aggregate("ask_ai", rows)
    assert s["structured_output_used"] == 2
    assert s["guided_and_clean"] == 1
    assert s["guided_but_repaired"] == 1
    assert s["unguided"] == 1
    assert s["json_repair_used"] == 2


# --------------------------------------------------------------------------
# Concall fix experiments — only prompt/retries may vary
# --------------------------------------------------------------------------
def test_variants_reuse_the_real_judging_logic():
    """The whole value of the experiment is attributability. If a variant
    quietly used its own normalize/validate, a 'fix' could be an artifact of
    looser judging rather than better output."""
    from app.experiments import concall_variants as cv
    from app.tasks import concall_summary as real

    assert cv.validate is real.validate
    assert cv._normalize is real._normalize


def test_variant_definitions_change_exactly_one_thing_each():
    from app.experiments import concall_variants as cv
    from app.prompts import concall_summary as prod

    base = cv.production_variant()
    assert base.system_prompt == prod.SYSTEM_PROMPT
    assert base.max_attempts == prod.MAX_ATTEMPTS

    retries = cv.retries_variant(6)
    assert retries.system_prompt == prod.SYSTEM_PROMPT   # prompt held constant
    assert retries.max_attempts == 6

    fewshot = cv.fewshot_variant()
    assert fewshot.max_attempts == prod.MAX_ATTEMPTS      # budget held constant
    assert fewshot.system_prompt != prod.SYSTEM_PROMPT


def test_variant_prompt_extends_production_verbatim():
    """The variant must be production + additions, never a rewrite — a
    rewrite would change far more than the one thing under test."""
    from app.prompts import concall_summary as prod
    from app.prompts import concall_summary_variant as var
    assert var.SYSTEM_PROMPT.startswith(prod.SYSTEM_PROMPT)


def test_fewshot_examples_themselves_pass_the_validator():
    """Showing the model non-compliant text labelled RIGHT would actively
    teach the failure this variant exists to fix."""
    import re
    from app.compliance.validators import summarizer_violation
    from app.prompts import concall_summary_variant as var

    for line in var._REAL_COMPLIANT_EXAMPLES.split("\n"):
        line = re.sub(r"\s*\[[A-Z]+\]\s*$", "", line).strip()
        if line:
            assert summarizer_violation(line) is None, f"bad exemplar: {line}"


def test_production_prompt_vendored_copy_is_untouched_by_the_variant():
    """The variant module must not mutate the vendored production prompt —
    that copy is drift-guarded against RedixFi's real source."""
    import importlib
    from app.prompts import concall_summary as prod
    before = prod.SYSTEM_PROMPT
    importlib.import_module("app.prompts.concall_summary_variant")
    assert prod.SYSTEM_PROMPT == before


def test_recording_backend_is_transparent_and_captures_raw_text():
    from app.inference.recording import RecordingBackend

    inner = EchoBackend()
    rec = RecordingBackend(inner, tag="t1")
    # Must impersonate the wrapped backend, or runs would be labelled
    # "recording" instead of the real runtime.
    assert rec.name == inner.name

    from app.prompts.concall_summary import SYSTEM_PROMPT
    req = GenerationRequest(messages=[Message("system", SYSTEM_PROMPT),
                                      Message("user", "x" * 3000)],
                            model="echo", json_schema=schema_for_task("concall_summary"))
    result = rec.generate(req)
    assert result.text                      # passthrough unchanged
    assert len(rec.transcript) == 1
    entry = rec.transcript[0]
    assert entry["raw_output"] == result.text          # verbatim, untruncated
    assert entry["json_schema_sent"] is True
    assert entry["user_prompt_chars"] == 3000
    assert len(entry["user_prompt_tail"]) <= 1200


# --------------------------------------------------------------------------
# chat-native prompt path (Mistral/Tekken) vs rendered-string path (Qwen)
# --------------------------------------------------------------------------
"""Qwen's numbers were all produced by rendering the chat template to a
string and calling llm.generate(). If that path ever silently changed, every
existing Qwen result would stop being comparable. Ministral needs the other
path, because the Ministral preflight logged that
`MistralCommonBackend.apply_chat_template(..., tokenize=False)` is unsafe.

These pin both, and pin that the prompt TEXT is the same either way — the
flag must not become a way to give one model a better prompt."""


class _FakeOut:
    def __init__(self, text="{}"):
        self.outputs = [type("C", (), {"text": text, "token_ids": [1, 2],
                                       "finish_reason": "stop"})()]
        self.prompt_token_ids = [1, 2, 3]


class _RecordingLLM:
    def __init__(self):
        self.generate_calls, self.chat_calls = [], []

    def get_tokenizer(self):
        class T:
            def apply_chat_template(self, messages, tokenize=False,
                                    add_generation_prompt=True):
                return "RENDERED:" + "|".join(m["content"] for m in messages)
        return T()

    def generate(self, prompts, params):
        self.generate_calls.append(prompts)
        return [_FakeOut()]

    def chat(self, messages, params, use_tqdm=True):
        self.chat_calls.append(messages)
        return [_FakeOut()]


def _req():
    from app.inference.base import GenerationRequest, Message
    return GenerationRequest(
        messages=[Message("system", "SYS"), Message("user", "USER")],
        model="m", temperature=0.0, max_tokens=16, seed=0)


def test_default_path_renders_a_string_and_calls_generate(stub_vllm):
    """The path every Qwen number was produced on. Must not drift."""
    from app.inference.vllm_inprocess import VLLMInProcessBackend
    llm = _RecordingLLM()
    backend = VLLMInProcessBackend(llm, "qwen-like")
    assert backend.chat_native is False
    backend.generate(_req())
    assert len(llm.generate_calls) == 1 and not llm.chat_calls
    assert llm.generate_calls[0][0].startswith("RENDERED:")


def test_chat_native_path_calls_chat_and_never_prerenders(stub_vllm):
    from app.inference.vllm_inprocess import VLLMInProcessBackend
    llm = _RecordingLLM()
    backend = VLLMInProcessBackend(llm, "ministral-like", chat_native=True)
    backend.generate(_req())
    assert len(llm.chat_calls) == 1 and not llm.generate_calls
    assert llm.chat_calls[0] == [{"role": "system", "content": "SYS"},
                                 {"role": "user", "content": "USER"}]


def test_both_paths_carry_identical_prompt_text(stub_vllm):
    """The flag changes ENCODING, never content. If it ever changed the text,
    a model comparison would be measuring two different prompts."""
    from app.inference.vllm_inprocess import VLLMInProcessBackend
    a, b = _RecordingLLM(), _RecordingLLM()
    VLLMInProcessBackend(a, "x").generate(_req())
    VLLMInProcessBackend(b, "y", chat_native=True).generate(_req())
    rendered = a.generate_calls[0][0]
    chatted = " ".join(m["content"] for m in b.chat_calls[0])
    for fragment in ("SYS", "USER"):
        assert fragment in rendered and fragment in chatted


def test_structured_outputs_still_applied_on_the_chat_path(stub_vllm):
    """Guided decoding must not be lost by switching paths — the preflight's
    6/6 guided result depends on it reaching the engine either way."""
    from app.inference.vllm_inprocess import VLLMInProcessBackend
    req = _req()
    req.json_schema = {"type": "object", "properties": {}}
    backend = VLLMInProcessBackend(_RecordingLLM(), "z", chat_native=True)
    params, mode = backend._structured_outputs(req)
    assert mode == "json_schema" and params is not None
