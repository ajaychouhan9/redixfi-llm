"""Unit tests for the GPT-4o-mini rephrase layer (2026-08-31 controlled fix).

Covers the ten required behaviors:
  1. validator PASS  -> GPT not called
  2. eligible failure -> GPT called exactly once
  3. GPT receives only Qwen summary + finding + policy instruction
  4. original source/transcript is NOT passed to GPT
  5. GPT output is validated again
  6. successful GPT rephrase becomes final output
  7. failed GPT rephrase -> human-review status
  8. no Qwen retries for eligible validator failures
  9. technical failures do not invoke GPT
  10. Red Flag classification remains unchanged
"""
import json

from app.inference.base import GenerationRequest, GenerationResult
from app.tasks import annual_report_summary as task_ar
from app.tasks import concall_summary as task_cc
from app.tasks import red_flag as task_rf

COMPLIANT_CC = json.dumps({
    "summary": "Management stated the plant is expected to commence production in September 2026.",
    "tone_label": "Neutral",
    "tone_note": "The call highlighted reported results.",
})
BAD_CC = json.dumps({
    "summary": "The plant will commence production in September 2026.",
    "tone_label": "Neutral",
    "tone_note": "The call highlighted reported results.",
})
COMPLIANT_AR = json.dumps({
    "executive_summary": "The report described management's stated priorities.",
    "key_points": ["Management described capacity work",
                   "The report stated a sourcing programme",
                   "Governance practices were reviewed"],
    "important_risks": [],
    "key_takeaway": "The report centred on stated operating priorities.",
})
BAD_AR = json.dumps({
    "executive_summary": "Revenue will expand next year.",
    "key_points": ["a", "b", "c"],
    "important_risks": [],
    "key_takeaway": "Fine.",
})

CC_FIXTURE = {
    "benchmark_id": "CC_TEST_1",
    "company_name": "Test Ltd",
    "symbol": "TEST",
    "input_text": "SUPER_SECRET_TRANSCRIPT_XYZ should never reach GPT.",
}
AR_FIXTURE = {
    "fixture_id": "AR_TEST_1",
    "symbol": "T",
    "company_name": "T Ltd",
    "fiscal_year": "FY2024-25",
    "filing_date": "2025-01-01",
    "page_count": 100,
    "evidence_text": "SUPER_SECRET_EVIDENCE_XYZ should never reach GPT.",
}


class FakeQwen:
    name = "fake-qwen"

    def __init__(self, text):
        self.text = text
        self.calls = 0

    def generate(self, request: GenerationRequest) -> GenerationResult:
        self.calls += 1
        return GenerationResult(text=self.text, model=request.model,
                                backend=self.name, prompt_tokens=10,
                                completion_tokens=5, total_tokens=15)


class FakeRephrase:
    name = "fake-gpt"

    def __init__(self, text, error=None):
        self.text = text
        self.error = error
        self.requests = []
        self.calls = 0

    def generate(self, request: GenerationRequest) -> GenerationResult:
        self.calls += 1
        self.requests.append(request)
        if self.error:
            return GenerationResult(text="", model=request.model, backend=self.name,
                                    error=self.error)
        return GenerationResult(text=self.text, model=request.model, backend=self.name,
                                prompt_tokens=7, completion_tokens=4, total_tokens=11)


class BoomRephrase:
    """Fails the test if GPT is called at all."""

    def generate(self, request):
        raise AssertionError("GPT rephrase should NOT have been called")


def test_validator_pass_does_not_call_gpt():
    q = FakeQwen(COMPLIANT_CC)
    r = task_cc.run(q, CC_FIXTURE, "m", rephrase_backend=BoomRephrase())
    assert r.ok is True
    assert r.final_source == "qwen"
    assert r.rephrase_log is None
    assert q.calls == 1


def test_eligible_failure_calls_gpt_exactly_once():
    q = FakeQwen(BAD_CC)
    rb = FakeRephrase(COMPLIANT_CC)
    r = task_cc.run(q, CC_FIXTURE, "m", rephrase_backend=rb)
    assert r.ok is True
    assert r.final_source == "gpt_rephrase"
    assert r.rephrase_log is not None
    assert rb.calls == 1
    assert q.calls == 1, "no Qwen validator retries"


def test_gpt_receives_only_summary_finding_and_policy():
    q = FakeQwen(BAD_CC)
    rb = FakeRephrase(COMPLIANT_CC)
    task_cc.run(q, CC_FIXTURE, "m", rephrase_backend=rb)
    user = rb.requests[0].messages[-1].content
    assert "Validator finding" in user
    assert "Policy note" in user
    assert "Qwen summary (JSON)" in user


def test_original_source_not_sent_to_gpt():
    q = FakeQwen(BAD_CC)
    rb = FakeRephrase(COMPLIANT_CC)
    task_cc.run(q, CC_FIXTURE, "m", rephrase_backend=rb)
    for msg in rb.requests[0].messages:
        assert "SUPER_SECRET_TRANSCRIPT_XYZ" not in msg.content

    q2 = FakeQwen(BAD_AR)
    rb2 = FakeRephrase(COMPLIANT_AR)
    task_ar.run(q2, AR_FIXTURE, "m", rephrase_backend=rb2)
    for msg in rb2.requests[0].messages:
        assert "SUPER_SECRET_EVIDENCE_XYZ" not in msg.content


def test_gpt_output_is_validated_again():
    q = FakeQwen(BAD_CC)
    # GPT returns another bare future claim -> must fail after re-validate.
    rb = FakeRephrase(BAD_CC)
    r = task_cc.run(q, CC_FIXTURE, "m", rephrase_backend=rb)
    assert r.ok is False
    assert r.final_source == "failed_human_review"
    assert r.rephrase_log["validator_status_after_rephrase"] != "PASS"


def test_successful_gpt_rephrase_becomes_final_output():
    q = FakeQwen(BAD_AR)
    rb = FakeRephrase(COMPLIANT_AR)
    r = task_ar.run(q, AR_FIXTURE, "m", rephrase_backend=rb)
    assert r.ok is True
    assert r.final_source == "gpt_rephrase"
    assert r.output["executive_summary"] == (
        "The report described management's stated priorities.")


def test_failed_gpt_rephrase_results_in_human_review():
    q = FakeQwen(BAD_AR)
    rb = FakeRephrase(BAD_AR)
    r = task_ar.run(q, AR_FIXTURE, "m", rephrase_backend=rb)
    assert r.ok is False
    assert r.final_source == "failed_human_review"
    assert r.output == {}


def test_no_qwen_retries_for_eligible_validator_failures():
    q = FakeQwen(BAD_CC)
    rb = FakeRephrase(COMPLIANT_CC)
    r = task_cc.run(q, CC_FIXTURE, "m", rephrase_backend=rb)
    assert q.calls == 1
    assert r.attempts == 1
    assert rb.calls == 1


def test_technical_failure_does_not_invoke_gpt():
    q = FakeQwen(BAD_CC)
    q.generate = lambda request: GenerationResult(
        text="", model=request.model, backend=q.name,
        error="VLLMValidationError: context overflow")
    r = task_cc.run(q, CC_FIXTURE, "m", rephrase_backend=BoomRephrase())
    assert r.ok is False
    assert r.final_source == "failed_human_review"
    assert r.rephrase_log is None
    assert "VLLMValidationError" in r.error


def test_information_loss_marks_human_review_required():
    qwen = json.dumps({
        "executive_summary": "Coal India plans expansion to 1 billion tonnes by FY28-29.",
        "key_points": ["a", "b", "c"],
        "important_risks": [],
        "key_takeaway": "Fine.",
    })
    lossy = json.dumps({
        "executive_summary": "Coal India plans significant expansion by FY28-29.",
        "key_points": ["a", "b", "c"],
        "important_risks": [],
        "key_takeaway": "Fine.",
    })
    r = task_ar.run(FakeQwen(qwen), AR_FIXTURE, "m",
                    rephrase_backend=FakeRephrase(lossy))
    assert r.ok is False
    assert r.final_status == "HUMAN_REVIEW_REQUIRED"
    assert r.human_review_required is True
    assert r.information_preservation_check["status"] == "HUMAN_REVIEW_REQUIRED"
    assert "1" in r.information_preservation_check["missing_material_tokens"]


def test_red_flag_classification_unchanged():
    rf_fixture = {
        "fixture_id": "RF_TEST_1",
        "chunk_text": "Related party transactions were reviewed by the auditors.",
        "candidates": ["related_party_transaction"],
    }
    good = json.dumps({
        "category": "related_party_transaction",
        "summary": "Related party transactions were reviewed by the auditors.",
    })
    r = task_rf.run(FakeQwen(good), rf_fixture, "m")
    assert r.ok is True
    assert r.output.get("risk_classified") is True
    assert r.output.get("risk_flag_type") == "related_party_transaction"
    assert r.rephrase_log is None
