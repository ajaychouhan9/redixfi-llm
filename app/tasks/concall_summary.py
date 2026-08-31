"""Phase D (PRIMARY summarization benchmark) — Concall summary.

Reproduces data-pipeline/concall_summarizer.py::generate_summary:

  * same SYSTEM_PROMPT and user-content shape
  * same MAX_ATTEMPTS=3 regenerate-then-validate loop
  * same validation set: _violation() on `summary` AND `tone_note`, plus
    `tone_label` membership in the CLOSED set TONE_LABELS
  * same "return None, store nothing" posture on total failure

`tone_label` is the one genuinely objective, non-judgement quality signal
in any of the summarization phases: it is a 4-way closed-set classification
the production model already committed to, so candidate-vs-reference
agreement is a real accuracy number, not a similarity heuristic.

Financial-figure checking is OFF here. That rule belongs only to the annual
report summarizer — concalls are allowed to restate figures management
stated, and production does not apply FINANCIAL_FIGURE_RE to them.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..compliance.validators import summarizer_violation
from ..inference.base import Backend, GenerationRequest, Message
from ..schemas.output_schemas import schema_for_task
from ..prompts.concall_summary import (
    MAX_ATTEMPTS,
    SYSTEM_PROMPT,
    TONE_LABELS,
    build_user_content,
)
from .base import TaskResult, parse_json_object
from .context_budget import plan_context
from .rephrase import (build_rephrase_backend, build_rephrase_request,
                       collect_validator_findings, information_preservation_check,
                       is_eligible_for_rephrase)
from .retry_policy import PRODUCTION_POLICY, RetryPolicy

TASK_NAME = "concall_summary"


def _normalize(parsed: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "summary": str(parsed.get("summary", "")).strip(),
        "tone_label": str(parsed.get("tone_label", "")).strip(),
        "tone_note": str(parsed.get("tone_note", "")).strip(),
    }


def validate(out: Dict[str, Any]) -> Optional[str]:
    """Mirrors concall_summarizer.py::generate_summary's `bad` expression,
    including order."""
    return (
        summarizer_violation(out["summary"])
        or summarizer_violation(out["tone_note"])
        or (None if out["tone_label"] in TONE_LABELS
            else f"invalid tone_label {out['tone_label']!r}")
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
    result = TaskResult(task=TASK_NAME, fixture_id=str(fixture.get("benchmark_id")
                                                        or fixture.get("fixture_id") or ""),
                        ok=False)

    # Guided decoding: constrain the shape at DECODE time so valid
    # JSON is produced by construction. parse_json_object stays as a
    # fallback and `json_repair_used` still reports if it was needed.
    schema = schema_for_task(TASK_NAME, None)
    rejections: List[Dict[str, Any]] = []

    # Pre-generation context budget: never spend retries on an impossible
    # request (e.g. BAJFINANCE transcript exceeding 32,768 tokens).
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
    # failures must NOT be sent to a rephraser.
    if not is_eligible_for_rephrase(bad):
        result.ok = False
        result.error = f"non-eligible validator failure: {bad}"
        result.final_source = "failed_human_review"
        result.final_status = "HUMAN_REVIEW_REQUIRED"
        result.human_review_required = True
        result.human_review_reason = result.error
        return result

    # ONE GPT-4o-mini edit, max. The source transcript is never sent.
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

    # Deterministic information-preservation guard.
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
