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
from .retry_policy import (PRODUCTION_POLICY, RetryPolicy,
                           build_corrective_note)

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
) -> TaskResult:
    result = TaskResult(task=TASK_NAME, fixture_id=str(fixture.get("benchmark_id")
                                                        or fixture.get("fixture_id") or ""),
                        ok=False)

    # Guided decoding: constrain the shape at DECODE time so valid
    # JSON is produced by construction. parse_json_object stays as a
    # fallback and `json_repair_used` still reports if it was needed.
    schema = schema_for_task(TASK_NAME, None)
    rejections: List[Dict[str, Any]] = []
    corrective_note: Optional[str] = None
    previous_raw: Optional[str] = None

    # Pre-generation context budget: never spend retries on an impossible
    # request (e.g. BAJFINANCE transcript exceeding 32,768 tokens).
    planned_user, context_log = plan_context(TASK_NAME, fixture, model, max_tokens)
    result.context_log = context_log
    if planned_user is None:
        result.ok = False
        result.error = f"context_overflow: {context_log}"
        return result

    for attempt in range(1, MAX_ATTEMPTS + 1):
        result.attempts = attempt
        # Retries sample differently so they can actually differ; attempt 1
        # is untouched. See retry_policy's docstring for the measured
        # repetition this fixes. Both values are recorded on each rejection
        # so "the retry really did differ" stays checkable from the run JSON.
        attempt_temperature = policy.temperature_for(attempt, temperature)
        attempt_seed = policy.seed_for(attempt, seed)
        user_content = planned_user
        if corrective_note:
            user_content += (
                f"\n\n(Your previous attempt was rejected: {corrective_note}. "
                "Rewrite following the rules exactly.)"
            )
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
            rejections.append({"pass": attempt, "sampling": sampling,
                               "reason": f"llm_exception: {generation.error}"})
            corrective_note = "the previous attempt failed to reach the model — retry"
            continue

        parsed, repaired, parse_error = parse_json_object(generation.text)
        result.json_repair_used = result.json_repair_used or repaired
        if parsed is None:
            rejections.append({"pass": attempt, "sampling": sampling,
                               "reason": f"invalid_json: {parse_error}",
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

        output_changed = previous_raw is None or generation.text != previous_raw
        next_note = build_corrective_note(bad, out, ['summary', 'tone_note'],
                                          policy=policy)
        rejections.append({
            "pass": attempt,
            "sampling": sampling,
            "reason": bad,
            "text": out,
            "raw_text": generation.text,
            "corrective_note": corrective_note,   # note that shaped THIS attempt
            "next_corrective_note": next_note,    # directive for the next attempt
            "output_changed": output_changed,
        })
        corrective_note = next_note
        previous_raw = generation.text

    result.rejections = rejections
    result.error = f"failed validation after {MAX_ATTEMPTS} attempts"
    return result
