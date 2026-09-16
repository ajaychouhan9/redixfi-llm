"""Annual Report Summary task — PRODUCTION (simplified prompt + deterministic
evidence-anchored validation; NO GPT repair layer).

Contract (unchanged externally):
  * one Qwen generation under guided JSON decoding;
  * deterministic validation against the SAME evidence the model was given:
      app/compliance/ar_grounding.validate_annual_report_summary(...)
    covering advisory-language compliance, evidence-anchored figure grounding
    (unsupported number / unit-scale mismatch / unit ambiguity / sign /
    guidance-to-fact), the distortion guard and the two completeness checks;
  * PASS  -> final_status QWEN_PASS, final_source qwen;
  * anything else -> HUMAN_REVIEW_REQUIRED with the reason and findings
    recorded in `rejections`. There is no second LLM layer and no retry.

Removed on 2026-09-16: the GPT-4o-mini rephrase/repair step for annual
reports, the blanket forward-tense ban and the "every figure needs an
attribution phrase" rule.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from ..compliance import ar_grounding
from ..inference.base import Backend, GenerationRequest, Message
from ..schemas.output_schemas import schema_for_task
from ..prompts.annual_report_summary import (
    BULLET_MAX,
    BULLET_MIN,
    SYSTEM_PROMPT,
    build_user_content,
)
from .base import TaskResult, parse_json_object
from .context_budget import plan_context
from .retry_policy import PRODUCTION_POLICY, RetryPolicy

TASK_NAME = "annual_report_summary"


def _normalize(parsed: Dict[str, Any]) -> Dict[str, Any]:
    """Canonical RedixFi current-schema output only (unchanged)."""
    executive_summary = str(
        parsed.get("executive_summary") or parsed.get("summary") or ""
    ).strip()

    key_points_raw = parsed.get("key_points") or parsed.get("bullets") or []
    if not isinstance(key_points_raw, list):
        key_points_raw = []
    key_points = [str(b).strip() for b in key_points_raw if str(b).strip()]

    risks_raw = parsed.get("important_risks") or []
    if not isinstance(risks_raw, list):
        risks_raw = []
    important_risks = [str(r).strip() for r in risks_raw if str(r).strip()]

    key_takeaway = str(parsed.get("key_takeaway", "")).strip()

    return {
        "executive_summary": executive_summary,
        "key_points": key_points,
        "important_risks": important_risks,
        "key_takeaway": key_takeaway,
    }


def validate(fixture: Dict[str, Any], out: Dict[str, Any]) -> Tuple[Optional[str], Dict[str, Any]]:
    """Deterministic, evidence-anchored validation.

    Returns (reason, findings). reason is None only when the summary may be
    published automatically.
    """
    if not (
        BULLET_MIN <= len(out.get("key_points") or []) <= BULLET_MAX
    ):
        findings = {"bullet_count": len(out.get("key_points") or [])}
        return (
            f"key_points count {len(out.get('key_points') or [])} outside "
            f"[{BULLET_MIN}, {BULLET_MAX}]",
            findings,
        )
    return ar_grounding.validate_annual_report_summary(
        fixture.get("evidence_text") or "", out,
    )


def run(
    backend: Backend,
    fixture: Dict[str, Any],
    model: str,
    temperature: float = 0.0,
    max_tokens: int = 1024,
    seed: Optional[int] = 0,
    policy: RetryPolicy = PRODUCTION_POLICY,
    rephrase_backend: Optional[Backend] = None,  # accepted for API compatibility; unused
) -> TaskResult:
    result = TaskResult(task=TASK_NAME, fixture_id=str(fixture.get("fixture_id") or ""), ok=False)

    schema = schema_for_task(TASK_NAME, None)
    rejections: List[Dict[str, Any]] = []

    planned_user, context_log = plan_context(TASK_NAME, fixture, model, max_tokens)
    result.context_log = context_log
    if planned_user is None:
        result.ok = False
        result.error = f"context_overflow: {context_log}"
        result.final_status = "HUMAN_REVIEW_REQUIRED"
        result.human_review_required = True
        result.human_review_reason = result.error
        return result

    # ONE Qwen generation. No validator-driven retry, no GPT edit.
    result.attempts = 1
    attempt_temperature = policy.temperature_for(1, temperature)
    attempt_seed = policy.seed_for(1, seed)
    request = GenerationRequest(
        messages=[
            Message("system", SYSTEM_PROMPT),
            Message("user", planned_user),
        ],
        model=model,
        temperature=attempt_temperature,
        max_tokens=max_tokens,
        seed=attempt_seed,
        json_mode=True,
        json_schema=schema,
    )
    sampling = {"temperature": attempt_temperature, "seed": attempt_seed}
    generation = backend.generate(request)
    result.absorb(generation)

    if not generation.ok:
        result.ok = False
        result.error = f"llm_exception: {generation.error}"
        result.final_source = "failed_human_review"
        result.final_status = "HUMAN_REVIEW_REQUIRED"
        result.human_review_required = True
        result.human_review_reason = result.error
        result.rejections = [{"pass": 1, "sampling": sampling, "reason": result.error}]
        return result

    parsed, repaired, parse_error = parse_json_object(generation.text)
    result.json_repair_used = result.json_repair_used or repaired
    if parsed is None:
        result.ok = False
        result.error = f"invalid_json: {parse_error}"
        result.final_source = "failed_human_review"
        result.final_status = "HUMAN_REVIEW_REQUIRED"
        result.human_review_required = True
        result.human_review_reason = result.error
        result.rejections = [{"pass": 1, "sampling": sampling, "reason": result.error}]
        return result

    out = _normalize(parsed)
    reason, findings = validate(fixture, out)

    rejection = {
        "pass": 1,
        "sampling": sampling,
        "reason": reason,
        "text": out,
        "raw_text": generation.text,
        "grounding": findings,
    }
    result.rejections = [rejection]

    if reason:
        result.ok = False
        result.error = f"deterministic validation failed: {reason}"
        result.final_source = "failed_human_review"
        result.final_status = "HUMAN_REVIEW_REQUIRED"
        result.human_review_required = True
        result.human_review_reason = reason
        return result

    result.ok = True
    result.output = out
    result.rejections = []
    result.final_source = "qwen"
    result.final_status = "QWEN_PASS"
    return result
