"""Phase A-legacy — Annual Report Summary, replayed against the ORIGINAL
pre-Evidence-Finder contract.

WHY THIS EXISTS
---------------
Production's 72 stored annual-report summaries were all written on
2026-08-16, before the Evidence Finder unification (2026-08-24). Running
the CURRENT pipeline against them compares two different things at once —
a different input AND a different output schema.

This task removes both variables. It replays the LEGACY prompt against the
LEGACY input (`raw_text[:150_000]`) so a candidate model is measured on
exactly the job gpt-4o-mini did. The 3-field output contract
(`summary`/`bullets`/`key_takeaway`) is validated, with NO
`important_risks` — that field did not exist yet.

Pair it with app/tasks/annual_report_summary.py (current pipeline,
Evidence Finder input, 4-field schema) to get both readings from one
exported fixture. The fixture carries both inputs; these two runners are
the only thing that differs.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..compliance.validators import violation
from ..inference.base import Backend, GenerationRequest, Message
from ..prompts.annual_report_summary_legacy import (
    BULLET_MAX,
    BULLET_MIN,
    MAX_ATTEMPTS,
    SYSTEM_PROMPT,
    build_user_content,
)
from .base import TaskResult, parse_json_object

TASK_NAME = "annual_report_summary_legacy"


def _normalize(parsed: Dict[str, Any]) -> Dict[str, Any]:
    """The legacy 3-field contract. `bullets`, not `key_points`; no
    `important_risks`."""
    summary = str(parsed.get("summary") or parsed.get("executive_summary") or "").strip()
    bullets_raw = parsed.get("bullets") or parsed.get("key_points") or []
    if not isinstance(bullets_raw, list):
        bullets_raw = []
    bullets = [str(b).strip() for b in bullets_raw if str(b).strip()]
    return {
        "summary": summary,
        "bullets": bullets,
        "key_takeaway": str(parsed.get("key_takeaway", "")).strip(),
    }


def validate(out: Dict[str, Any]) -> Optional[str]:
    """Legacy validation set. Financial-figure checking is ON — rule (4) of
    the legacy prompt is identical to the current one on that point."""
    def check(text: str) -> Optional[str]:
        return violation(text, check_financial_figures=True)

    return (
        check(out["summary"])
        or check(out["key_takeaway"])
        or next((check(b) for b in out["bullets"] if check(b)), None)
        or (None if BULLET_MIN <= len(out["bullets"]) <= BULLET_MAX
            else f"bullets count {len(out['bullets'])} outside [{BULLET_MIN}, {BULLET_MAX}]")
    )


def run(
    backend: Backend,
    fixture: Dict[str, Any],
    model: str,
    temperature: float = 0.0,
    max_tokens: int = 1024,
    seed: Optional[int] = 0,
) -> TaskResult:
    result = TaskResult(task=TASK_NAME, fixture_id=str(fixture.get("benchmark_id")
                                                        or fixture.get("fixture_id") or ""),
                        ok=False)
    if not fixture.get("legacy_input_text"):
        result.error = ("fixture carries no legacy_input_text — this case cannot be "
                        "replayed against the legacy contract")
        return result

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

    result.rejections = rejections
    result.error = f"failed validation after {MAX_ATTEMPTS} attempts"
    return result
