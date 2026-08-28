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

TASK_NAME = "annual_report_summary"


def _normalize(parsed: Dict[str, Any]) -> Dict[str, Any]:
    """Mirrors call_llm_summarize's parsing, including its legacy-key
    fallback (`summary`/`bullets`) and the additive legacy output fields."""
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
        # Legacy fields RedixFi also stores (Research page reads these).
        "summary": executive_summary,
        "bullets": key_points,
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
) -> TaskResult:
    result = TaskResult(task=TASK_NAME, fixture_id=str(fixture.get("fixture_id") or ""), ok=False)

    # Guided decoding: constrain the shape at DECODE time so valid
    # JSON is produced by construction. parse_json_object stays as a
    # fallback and `json_repair_used` still reports if it was needed.
    schema = schema_for_task(TASK_NAME, None)
    rejections: List[Dict[str, Any]] = []
    corrective_note: Optional[str] = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        result.attempts = attempt
        request = GenerationRequest(
            messages=[
                Message("system", SYSTEM_PROMPT),
                Message("user", build_user_content(fixture, corrective_note)),
            ],
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            seed=seed,
            json_mode=True,
            json_schema=schema,
        )
        generation = backend.generate(request)
        result.absorb(generation)

        if not generation.ok:
            rejections.append({"pass": attempt, "reason": f"llm_exception: {generation.error}"})
            corrective_note = "the previous attempt failed to reach the model — retry"
            continue

        parsed, repaired, parse_error = parse_json_object(generation.text)
        result.json_repair_used = result.json_repair_used or repaired
        if parsed is None:
            rejections.append({"pass": attempt, "reason": f"invalid_json: {parse_error}",
                               "text": generation.text[:500]})
            corrective_note = "the previous attempt was not valid JSON"
            continue

        out = _normalize(parsed)
        bad = validate(out)
        if not bad:
            result.ok = True
            result.output = out
            result.rejections = rejections
            return result

        rejections.append({"pass": attempt, "reason": bad, "text": out})
        corrective_note = bad

    # Same posture as RedixFi: no placeholder on total failure.
    result.rejections = rejections
    result.error = f"failed validation after {MAX_ATTEMPTS} attempts"
    return result
