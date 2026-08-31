"""Phase A — Annual Report Summary.

Reproduces data-pipeline/annual_report_summarizer.py::generate_summary's
contract against a candidate model:

  * same SYSTEM_PROMPT and user-content shape (app/prompts/annual_report_summary.py)
  * same MAX_ATTEMPTS=3 regenerate-then-validate loop, with the rejection
    reason fed back as the corrective note
  * same validation set: _violation() on executive_summary, key_takeaway,
    every key_point and every important_risk, PLUS the key_points count
    bound — and, unlike the other two tasks, the financial-figure check
  * same failure posture: total failure returns no summary at all rather
    than a placeholder

Evidence comes from the fixture, produced by RedixFi's real
evidence_finder.py. Nothing here selects evidence.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..compliance.validators import summarizer_violation
from ..inference.base import Backend, GenerationRequest, Message
from ..schemas.output_schemas import schema_for_task
from ..prompts.annual_report_summary import (
    BULLET_MAX,
    BULLET_MIN,
    MAX_ATTEMPTS,
    SYSTEM_PROMPT,
    build_user_content,
)
from .base import TaskResult, parse_json_object
from .context_budget import plan_context
from .rephrase import (build_rephrase_backend, build_rephrase_request,
                       collect_validator_findings, information_preservation_check,
                       is_eligible_for_rephrase)
from .retry_policy import PRODUCTION_POLICY, RetryPolicy

TASK_NAME = "annual_report_summary"


def _normalize(parsed: Dict[str, Any]) -> Dict[str, Any]:
    """Canonical RedixFi current-schema output only.

    Phase 1 (2026-08-30 controlled fix): the previous normalization mirrored
    call_llm_summarize's additive legacy fallback and emitted BOTH the current
    keys (`executive_summary`/`key_points`) and the legacy keys
    (`summary`/`bullets`) with duplicated content. Consumers observed the
    duplication. The canonical schema for the current pipeline is
    `executive_summary` / `key_points` / `important_risks` / `key_takeaway`;
    the legacy keys are no longer emitted by this task.
    """
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


def validate(out: Dict[str, Any]) -> Optional[str]:
    """Byte-for-byte the same rejection logic as generate_summary's `bad`
    expression, including check order. Financial-figure checking is ON —
    rule (4) of the system prompt is the summarizer's distinguishing rule.
    """
    def check(text: str) -> Optional[str]:
        return summarizer_violation(text, check_financial_figures=True)

    return (
        check(out["executive_summary"])
        or check(out["key_takeaway"])
        or next((check(b) for b in out["key_points"] if check(b)), None)
        or next((check(r) for r in out["important_risks"] if check(r)), None)
        or (
            None
            if BULLET_MIN <= len(out["key_points"]) <= BULLET_MAX
            else f"key_points count {len(out['key_points'])} outside [{BULLET_MIN}, {BULLET_MAX}]"
        )
    )


def run(
    backend: Backend,
    fixture: Dict[str, Any],
    model: str,
    temperature: float = 0.0,
    max_tokens: int = 1024,
    seed: Optional[int] = 0,
    policy: RetryPolicy = PRODUCTION_POLICY,
    rephrase_backend: Optional[Backend] = None,
) -> TaskResult:
    result = TaskResult(task=TASK_NAME, fixture_id=str(fixture.get("fixture_id") or ""), ok=False)

    # Guided decoding: constrain the shape at DECODE time so valid
    # JSON is produced by construction. parse_json_object stays as a
    # fallback and `json_repair_used` still reports if it was needed.
    schema = schema_for_task(TASK_NAME, None)
    rejections: List[Dict[str, Any]] = []

    # Pre-generation context budget: never spend retries on an impossible
    # request (same protection as Concall; Annual Report evidence normally
    # fits, but the guard is shared).
    planned_user, context_log = plan_context(TASK_NAME, fixture, model, max_tokens)
    result.context_log = context_log
    if planned_user is None:
        result.ok = False
        result.error = f"context_overflow: {context_log}"
        result.final_status = "HUMAN_REVIEW_REQUIRED"
        result.human_review_required = True
        result.human_review_reason = result.error
        return result

    # ONE Qwen generation. Validator-driven Qwen retries were removed
    # (2026-08-31): if the wording fails, a single GPT-4o-mini EDIT is used.
    result.attempts = 1
    attempt_temperature = policy.temperature_for(1, temperature)
    attempt_seed = policy.seed_for(1, seed)
    user_content = planned_user
    request = GenerationRequest(
        messages=[
            Message("system", SYSTEM_PROMPT),
            Message("user", user_content),
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
    bad = validate(out)
    if not bad:
        result.ok = True
        result.output = out
        result.rejections = []
        result.final_source = "qwen"
        result.final_status = "QWEN_PASS"
        return result

    result.rejections = [
        {"pass": 1, "sampling": sampling, "reason": bad, "text": out,
         "raw_text": generation.text},
    ]

    # Only eligible wording/compliance issues go to GPT-4o-mini. Technical
    # failures (context overflow, model unavailable, invalid JSON, missing
    # evidence) must NOT be sent to a rephraser.
    if not is_eligible_for_rephrase(bad):
        result.ok = False
        result.error = f"non-eligible validator failure: {bad}"
        result.final_source = "failed_human_review"
        result.final_status = "HUMAN_REVIEW_REQUIRED"
        result.human_review_required = True
        result.human_review_reason = result.error
        return result

    # ONE GPT-4o-mini edit, max. The source document is never sent.
    findings = collect_validator_findings(TASK_NAME, out)
    rb = rephrase_backend or build_rephrase_backend()
    g = rb.generate(build_rephrase_request(TASK_NAME, out, findings, schema, max_tokens))
    rephrase_log = {
        "gpt_rephrase_called": True,
        "gpt_model": g.model,
        "gpt_input_tokens": g.prompt_tokens,
        "gpt_output_tokens": g.completion_tokens,
        "validator_finding": findings,
    }
    result.rephrase_log = rephrase_log
    if not g.ok:
        rephrase_log["error"] = g.error
        result.ok = False
        result.error = f"gpt rephrase failed: {g.error}"
        result.final_source = "failed_human_review"
        result.final_status = "HUMAN_REVIEW_REQUIRED"
        result.human_review_required = True
        result.human_review_reason = result.error
        return result

    parsed2, repaired2, parse_error2 = parse_json_object(g.text)
    result.json_repair_used = result.json_repair_used or repaired2
    if parsed2 is None:
        rephrase_log["error"] = parse_error2
        rephrase_log["gpt_rephrased_output"] = g.text
        result.ok = False
        result.error = f"gpt rephrase invalid json: {parse_error2}"
        result.final_source = "failed_human_review"
        result.final_status = "HUMAN_REVIEW_REQUIRED"
        result.human_review_required = True
        result.human_review_reason = result.error
        return result

    out2 = _normalize(parsed2)
    bad2 = validate(out2)
    rephrase_log["gpt_rephrased_output"] = out2
    rephrase_log["validator_status_after_rephrase"] = bad2 or "PASS"

    if bad2:
        # One GPT attempt only — do NOT loop back to GPT.
        result.ok = False
        result.error = f"gpt rephrase failed validation: {bad2}"
        result.final_source = "failed_human_review"
        result.final_status = "HUMAN_REVIEW_REQUIRED"
        result.human_review_required = True
        result.human_review_reason = result.error
        result.rejections.append({"pass": 2, "reason": bad2, "text": out2,
                                  "raw_text": g.text})
        return result

    # Deterministic information-preservation guard: never accept a GPT edit
    # that silently removed material numbers/dates/percentages.
    info = information_preservation_check(out, out2)
    result.information_preservation_check = info
    rephrase_log["information_preservation_check"] = info
    if info["status"] != "PASS":
        result.ok = False
        result.error = (f"information loss after rephrase: "
                        f"{info['missing_material_tokens']}")
        result.final_source = "failed_human_review"
        result.final_status = "HUMAN_REVIEW_REQUIRED"
        result.human_review_required = True
        result.human_review_reason = result.error
        return result

    result.ok = True
    result.output = out2
    result.final_source = "gpt_rephrase"
    result.final_status = "GPT_REPHRASE_PASS"
    return result
