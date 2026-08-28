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

from ..compliance.validators import violation
from ..inference.base import Backend, GenerationRequest, Message
from ..prompts.concall_summary import (
    MAX_ATTEMPTS,
    SYSTEM_PROMPT,
    TONE_LABELS,
    build_user_content,
)
from .base import TaskResult, parse_json_object

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
        violation(out["summary"])
        or violation(out["tone_note"])
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
) -> TaskResult:
    result = TaskResult(task=TASK_NAME, fixture_id=str(fixture.get("benchmark_id")
                                                        or fixture.get("fixture_id") or ""),
                        ok=False)
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
