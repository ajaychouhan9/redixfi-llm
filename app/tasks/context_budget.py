"""Pre-generation context-budget planning for task runners.

WHY THIS EXISTS
---------------
The eval harness has a context check (app/evaluation/context_check.py), but
the real generation path (task runners used by production_generate.py and
retest_generate.py) did not. A long Concall transcript (e.g. BAJFINANCE)
could therefore produce a prompt larger than the model's 32,768-token
context, and every retry would be rejected by vLLM as an impossible request —
wasting the entire retry budget before generation even happened.

This module runs BEFORE the model call:

  1. count the full prompt (system + user) with tiktoken and a conservative
     Qwen-tokenizer skew;
  2. reserve the completion budget plus a safety margin;
  3. if it fits, generate as-is;
  4. if it does not fit, reduce the INPUT using the same front-slice
     convention RedixFi already uses for these workloads (Concall transcripts
     and Annual Report evidence are both consumed as a front slice), and
     re-check;
  5. if safe reduction cannot fit, return generation_allowed=False with a
     diagnostic so the caller NEVER spends retries on an impossible request.

The reduction is deliberate, bounded, and logged — not a blind arbitrary
truncation.
"""
from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from ..models.registry import get_model_spec
from ..prompts import annual_report_summary as ar_prompt
from ..prompts import concall_summary as cc_prompt

TOKENIZER_SKEW = 1.15
OUTPUT_SAFETY_MARGIN = 256
MIN_INPUT_TOKENS = 2000


def count_tokens(text: str) -> int:
    if not text:
        return 0
    try:
        import tiktoken
        return len(tiktoken.encoding_for_model("gpt-4o-mini").encode(text))
    except Exception:
        return max(1, int(len(text) / 2.5))


def _builders(task: str):
    if task == "concall_summary":
        return cc_prompt.SYSTEM_PROMPT, cc_prompt.build_user_content, "input_text"
    if task == "annual_report_summary":
        return ar_prompt.SYSTEM_PROMPT, ar_prompt.build_user_content, "evidence_text"
    raise ValueError(f"context_budget: unsupported task {task!r}")


def _prompt_tokens(system: str, user: str) -> int:
    return int(count_tokens(system + user) * TOKENIZER_SKEW)


def plan_context(
    task: str,
    fixture: Dict[str, Any],
    model: str,
    max_tokens: int,
    corrective_note: Optional[str] = None,
) -> Tuple[Optional[str], Dict[str, Any]]:
    """Returns (user_content_to_use_or_None, context_log)."""
    system, builder, field = _builders(task)

    def log(case_id, symbol, original_tokens, selected_tokens, final_tokens,
            context_limit, reserved, action, allowed, note=""):
        return {
            "case_id": case_id,
            "symbol": symbol,
            "original_input_tokens": original_tokens,
            "selected_input_tokens": selected_tokens,
            "context_limit": context_limit,
            "reserved_output_tokens": reserved,
            "final_prompt_tokens": final_tokens,
            "selection_action": action,
            "generation_allowed": allowed,
            "note": note,
        }

    case_id = str(fixture.get("benchmark_id") or fixture.get("fixture_id")
                  or fixture.get("chunk_id") or "")
    symbol = str(fixture.get("symbol") or "")

    try:
        spec = get_model_spec(model)
    except KeyError:
        user = builder(fixture, corrective_note)
        return user, log(case_id, symbol, 0, 0, _prompt_tokens(system, user),
                         0, 0, "context_limit_unknown", True,
                         "model not in registry; context not checked")

    context_limit = int(spec.max_model_len or 0)
    if context_limit <= 0:
        user = builder(fixture, corrective_note)
        return user, log(case_id, symbol, 0, 0, _prompt_tokens(system, user),
                         0, 0, "context_limit_unknown", True,
                         "registry spec has no max_model_len; context not checked")

    user = builder(fixture, corrective_note)
    full_prompt_tokens = _prompt_tokens(system, user)
    reserved = max_tokens + OUTPUT_SAFETY_MARGIN
    original_input_tokens = int(count_tokens(str(fixture.get(field) or "")) * TOKENIZER_SKEW)

    if full_prompt_tokens + reserved <= context_limit:
        return user, log(case_id, symbol, original_input_tokens,
                         original_input_tokens, full_prompt_tokens,
                         context_limit, reserved, "no_reduction_needed", True)

    # ---- reduce the input field (front-slice convention) -----------------
    text = str(fixture.get(field) or "")
    if not text:
        return None, log(case_id, symbol, original_input_tokens, 0,
                         full_prompt_tokens, context_limit, reserved,
                         "cannot_reduce_empty_input", False)

    empty_case = dict(fixture)
    empty_case[field] = ""
    overhead_tokens = _prompt_tokens(system, builder(empty_case, corrective_note))
    input_budget_tokens = context_limit - reserved - overhead_tokens
    if input_budget_tokens <= 0:
        return None, log(case_id, symbol, original_input_tokens, 0,
                         full_prompt_tokens, context_limit, reserved,
                         "no_input_budget_available", False)

    input_tokens_now = max(1, int(count_tokens(text) * TOKENIZER_SKEW))
    chars_per_token = len(text) / input_tokens_now
    target_chars = int(input_budget_tokens * chars_per_token)
    reduced_text = text[:target_chars]
    reduced_case = dict(fixture)
    reduced_case[field] = reduced_text
    user = builder(reduced_case, corrective_note)
    final_prompt_tokens = _prompt_tokens(system, user)

    guard = 0
    while final_prompt_tokens + reserved > context_limit and guard < 30:
        reduced_text = reduced_text[:int(len(reduced_text) * 0.9)]
        reduced_case[field] = reduced_text
        user = builder(reduced_case, corrective_note)
        final_prompt_tokens = _prompt_tokens(system, user)
        guard += 1

    selected_input_tokens = int(count_tokens(reduced_text) * TOKENIZER_SKEW)
    allowed = (
        final_prompt_tokens + reserved <= context_limit
        and selected_input_tokens >= MIN_INPUT_TOKENS
    )
    action = (f"front_slice_reduction_{original_input_tokens}_to_"
              f"{selected_input_tokens}_tokens" if allowed
              else "reduction_still_overflows_or_below_minimum")
    return (user if allowed else None), log(
        case_id, symbol, original_input_tokens, selected_input_tokens,
        final_prompt_tokens, context_limit, reserved, action, allowed,
    )
