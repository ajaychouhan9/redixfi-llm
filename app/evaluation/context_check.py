"""Pre-run context-budget check.

WHY THIS EXISTS — a real defect caught locally, not on Kaggle
------------------------------------------------------------
RedixFi's Evidence Finder builds annual-report evidence under a global
20,000-token budget. Measured against real reports (ABB, TCS), that yields
~20,000 evidence tokens, which becomes a ~96,000-character user message.

`qwen3-14b-awq` is registered with `max_model_len=16384`. A Phase A prompt
therefore does NOT fit, and vLLM would reject every request at generation
time — after the weights had downloaded and the server had started, i.e.
after most of the GPU-hour cost had already been paid.

This module makes that failure visible before a session starts. It is
cheaper to be told locally than to discover it on Kaggle.

Token counting uses tiktoken when available (the same tokenizer RedixFi's
own evidence budgeting uses). Qwen's tokenizer differs, so treat the number
as a close estimate, not an exact count — the conservative headroom factor
below exists for that reason.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..models.registry import ModelSpec
from ..prompts import annual_report_summary as ar_prompt
from ..prompts import ask_ai as ask_prompt
from ..prompts import red_flag as rf_prompt

# Qwen tokenizers typically produce slightly more tokens than o200k_base on
# the same English text. 1.15 is a deliberately conservative allowance so a
# borderline case is reported as at-risk rather than passed.
TOKENIZER_SKEW = 1.15


def count_tokens(text: str) -> int:
    if not text:
        return 0
    try:
        import tiktoken
        return len(tiktoken.encoding_for_model("gpt-4o-mini").encode(text))
    except Exception:
        # Same fallback convention RedixFi uses when tiktoken is absent.
        return max(1, int(len(text) / 2.5))


def _prompt_for(task: str, case: Dict[str, Any]) -> str:
    if task == "annual_report_summary":
        return ar_prompt.SYSTEM_PROMPT + ar_prompt.build_user_content(case)
    if task == "red_flag":
        return rf_prompt.SYSTEM_PROMPT + rf_prompt.build_user_content(case)
    if task == "ask_ai":
        return (ask_prompt.system_prompt(case.get("symbol"))
                + ask_prompt.build_user_content(case))
    return ""


def check(
    task: str,
    cases: List[Dict[str, Any]],
    spec: Optional[ModelSpec],
    max_tokens: int,
) -> Dict[str, Any]:
    """Returns a report: per-case prompt sizes and whether they fit."""
    sizes = []
    for case in cases:
        raw = count_tokens(_prompt_for(task, case))
        sizes.append(int(raw * TOKENIZER_SKEW))

    if not sizes:
        return {"cases": 0, "fits": True}

    result: Dict[str, Any] = {
        "cases": len(sizes),
        "min_prompt_tokens": min(sizes),
        "max_prompt_tokens": max(sizes),
        "mean_prompt_tokens": int(sum(sizes) / len(sizes)),
        "completion_budget": max_tokens,
        "tokenizer_skew_applied": TOKENIZER_SKEW,
    }

    if spec is None or not spec.max_model_len:
        result["fits"] = True
        result["note"] = "no registry spec — context limit unknown, not checked"
        return result

    # A request needs room for BOTH the prompt and the completion.
    required = max(sizes) + max_tokens
    result["model_max_model_len"] = spec.max_model_len
    result["required_context"] = required
    result["fits"] = required <= spec.max_model_len
    result["over_by"] = max(0, required - spec.max_model_len)
    result["cases_that_overflow"] = sum(
        1 for size in sizes if size + max_tokens > spec.max_model_len
    )

    if not result["fits"]:
        options = []
        if spec.tensor_parallel_size == 1:
            options.append(
                f"use a TP=2 variant to buy KV-cache headroom "
                f"(e.g. '{spec.name}-tp2' if registered) and raise --max-model-len"
            )
        options.append(
            f"raise the model's max_model_len to at least {required} "
            "(VRAM permitting — KV cache grows with it)"
        )
        options.append(
            f"lower --max-tokens (currently {max_tokens}); this only helps if the "
            "prompt itself fits"
        )
        options.append(
            "reduce EVIDENCE_MAX_TOKENS at EXPORT time — but note this changes "
            "the evidence RedixFi actually uses, so the comparison would no "
            "longer be like-for-like. Prefer the options above."
        )
        result["options"] = options
    return result


def render(report: Dict[str, Any]) -> str:
    lines = ["Context budget check:"]
    lines.append(f"  cases                  : {report.get('cases')}")
    if not report.get("cases"):
        return "\n".join(lines)
    lines.append(f"  prompt tokens (min/mean/max): "
                 f"{report.get('min_prompt_tokens')} / "
                 f"{report.get('mean_prompt_tokens')} / "
                 f"{report.get('max_prompt_tokens')}")
    lines.append(f"  completion budget      : {report.get('completion_budget')}")
    if "model_max_model_len" in report:
        lines.append(f"  model max_model_len    : {report['model_max_model_len']}")
        lines.append(f"  required context       : {report['required_context']}")
    if report.get("fits"):
        lines.append("  VERDICT                : FITS")
    else:
        lines.append(f"  VERDICT                : DOES NOT FIT — over by "
                     f"{report['over_by']} tokens on the largest case "
                     f"({report['cases_that_overflow']} of {report['cases']} would fail)")
        for option in report.get("options", []):
            lines.append(f"    - {option}")
    return "\n".join(lines)
