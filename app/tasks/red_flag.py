"""Phase B — Red Flag / risk classification.

Reproduces data-pipeline/risk_flag_classifier.py::classify_chunk against a
candidate model. Faithfully preserved, including the parts that look like
edge cases and are not:

  * ONE call per keyword-matched chunk, candidates passed together (a chunk
    matching two categories still costs one call) — no retry loop, unlike
    Phase A. RedixFi's classifier has no MAX_ATTEMPTS.
  * A returned category NOT in the candidate list is rejected outright.
  * The summary is re-validated with _violation(); a non-compliant summary
    is DROPPED, leaving the chunk classified-but-unflagged. RedixFi never
    stores non-compliant LLM-authored text as metadata.
  * METADATA CONTRACT: `risk_classified` is always True; `risk_flag_type`
    and `risk_flag_summary` are OMITTED entirely (never null) whenever
    nothing was confirmed. ChromaDB metadata cannot hold null, and
    reproducing this exactly is what makes the outputs comparable.
  * Financial-figure checking is OFF here — that check belongs only to the
    annual report summarizer.

NOTE ON SCOPE: api/app/core/red_flag_ask.py (the query-time answer) makes
ZERO LLM calls, so there is no generation to evaluate there. See
app/prompts/red_flag.py's docstring.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from ..compliance.validators import violation
from ..inference.base import Backend, GenerationRequest, Message
from ..schemas.output_schemas import schema_for_task
from ..prompts.red_flag import SYSTEM_PROMPT, build_user_content
from .base import TaskResult, parse_json_object

TASK_NAME = "red_flag"


def run(
    backend: Backend,
    fixture: Dict[str, Any],
    model: str,
    temperature: float = 0.0,
    max_tokens: int = 512,
    seed: Optional[int] = 0,
) -> TaskResult:
    result = TaskResult(task=TASK_NAME, fixture_id=str(fixture.get("fixture_id") or ""), ok=False)

    # Guided decoding: constrain the shape at DECODE time so valid
    # JSON is produced by construction. parse_json_object stays as a
    # fallback and `json_repair_used` still reports if it was needed.
    schema = schema_for_task(TASK_NAME, fixture)
    candidates = list(fixture.get("candidates") or [])

    # classify_chunk's own short-circuit: no keyword candidates means no LLM
    # call at all, and the chunk is marked classified-but-unflagged.
    if not candidates:
        result.ok = True
        result.attempts = 0
        result.output = {"risk_classified": True}
        return result

    request = GenerationRequest(
        messages=[
            Message("system", SYSTEM_PROMPT),
            Message("user", build_user_content(fixture)),
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
    result.attempts = 1

    # Every failure path below is fail-soft to {"risk_classified": True},
    # exactly as classify_chunk is. `ok` stays True because "no flag" is a
    # legitimate outcome, not an error; `rejections` records WHY so the
    # comparison report can distinguish a genuine no-match from a model
    # that could not produce parseable output.
    def unflagged(reason: str) -> TaskResult:
        result.ok = True
        result.output = {"risk_classified": True}
        result.rejections = [{"pass": 1, "reason": reason}]
        return result

    if not generation.ok:
        return unflagged(f"llm_exception: {generation.error}")

    parsed, repaired, parse_error = parse_json_object(generation.text)
    result.json_repair_used = repaired
    if parsed is None:
        return unflagged(f"invalid_json: {parse_error}")

    category = parsed.get("category")
    if category not in candidates:
        return unflagged(
            f"category {category!r} not in candidates {candidates}"
            if category else "model returned no category (genuine non-match)"
        )

    summary = str(parsed.get("summary") or "").strip()
    if not summary:
        return unflagged("confirmed a category but returned an empty summary")

    bad = violation(summary)
    if bad:
        return unflagged(f"summary failed compliance: {bad}")

    result.ok = True
    result.output = {
        "risk_classified": True,
        "risk_flag_type": category,
        "risk_flag_summary": summary,
    }
    return result
