"""Targeted tests for the 2026-08-31 context-budget and validator fixes."""
from app.compliance.validators import summarizer_violation
from app.tasks.context_budget import plan_context


def test_attributed_management_guidance_is_allowed():
    assert summarizer_violation(
        "Management stated that it expects to reach 1 billion tonnes."
    ) is None
    assert summarizer_violation(
        "Management said it targets 1 billion tonnes of coal production."
    ) is None
    assert summarizer_violation(
        "The report stated an outlook of continued growth."
    ) is None


def test_bare_future_claim_is_still_rejected():
    assert summarizer_violation(
        "The company will achieve 1 billion tonnes."
    ) is not None
    assert summarizer_violation(
        "Coal production will reach 1 billion tonnes."
    ) is not None
    assert summarizer_violation(
        "Targeted growth of 10% next year."
    ) is not None


def test_context_plan_reduces_large_concall_input():
    case = {
        "benchmark_id": "CC_BIG",
        "symbol": "BIG",
        "input_text": "word " * 200_000,   # ~1M chars, far over 32k tokens
    }
    user, log = plan_context("concall_summary", case, "qwen3-14b-awq-tp2", 1024)

    assert log["generation_allowed"] is True
    assert log["selection_action"].startswith("front_slice_reduction")
    assert log["context_limit"] == 32768
    assert log["original_input_tokens"] > log["selected_input_tokens"]
    assert len(user) < len(case["input_text"])
