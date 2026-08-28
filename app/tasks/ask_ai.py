"""Phase C — Ask AI question answering.

Reproduces api/app/core/ask.py::generate_answer's LLM contract against a
candidate model:

  * same system template selection (symbol vs general), same
    json.dumps(packet) user-content assembly
  * same TWO-attempt budget (not three — Ask AI is a live path with a
    latency budget, unlike the offline summarizer)
  * same validation: ask_answer_violation(answer, causal_backstop), where
    causal_backstop is derived from the packet exactly as run_ask derives it
  * same "refused" handling: a model refusal is a legitimate, recorded
    outcome, not a failure

DELIBERATELY NOT REPRODUCED
---------------------------
Everything downstream of the LLM call in RedixFi's generate_answer — the
document-not-found substitution, PREDICTION_DECLINE_LINE, the template
fallback text, weight computation, citations. Those are product routing and
billing decisions, not model behaviour, and reproducing them would measure
RedixFi's cascade rather than the candidate model. The evaluation compares
the raw answer the model produced against the raw answer production's model
produced.

Retrieval and fusion are likewise not reproduced: the fixture carries the
fact packet exactly as production assembled it.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..compliance.validators import ask_answer_violation
from ..inference.base import Backend, GenerationRequest, Message
from ..schemas.output_schemas import schema_for_task
from ..prompts.ask_ai import build_user_content, system_prompt
from .base import TaskResult, parse_json_object

TASK_NAME = "ask_ai"

# RedixFi's live path allows at most 2 real LLM calls per question.
MAX_ATTEMPTS = 2


def derive_causal_backstop(fixture: Dict[str, Any]) -> bool:
    """run_ask enables the backstop when the packet has no usable cause.

    The fixture records what production decided in `causal_backstop`; when
    that is absent (an older fixture), fall back to deriving it from the
    packet the same way — a change_explanation whose cause_available is
    not true means any causal language in the answer would be invented.
    """
    if "causal_backstop" in fixture:
        return bool(fixture["causal_backstop"])
    packet = fixture.get("fact_packet") or {}
    change_explanation = packet.get("change_explanation")
    if not isinstance(change_explanation, dict):
        return True
    return not bool(change_explanation.get("cause_available"))


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
    symbol = fixture.get("symbol")
    causal_backstop = derive_causal_backstop(fixture)
    rejections: List[Dict[str, Any]] = []
    corrective_note: Optional[str] = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        result.attempts = attempt
        request = GenerationRequest(
            messages=[
                Message("system", system_prompt(symbol)),
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
            corrective_note = (
                "the previous attempt failed to reach the model — retry the same question"
            )
            continue

        parsed, repaired, parse_error = parse_json_object(generation.text)
        result.json_repair_used = result.json_repair_used or repaired
        if parsed is None:
            rejections.append({"pass": attempt, "reason": f"invalid_json: {parse_error}",
                               "text": generation.text[:500]})
            corrective_note = "the previous attempt was not valid JSON"
            continue

        out = {
            "answer": str(parsed.get("answer", "")).strip(),
            "refused": bool(parsed.get("refused")),
            "refusal_reason": parsed.get("refusal_reason"),
        }

        # A refusal is a real, valid outcome — RedixFi returns immediately
        # on it and never re-prompts. Whether refusing was CORRECT is a
        # judgement for the comparison report, not for this loop.
        if out["refused"]:
            result.ok = True
            result.output = out
            result.output["causal_backstop"] = causal_backstop
            result.rejections = rejections
            return result

        bad = ask_answer_violation(out["answer"], causal_backstop)
        if not bad and out["answer"]:
            result.ok = True
            result.output = out
            result.output["causal_backstop"] = causal_backstop
            result.rejections = rejections
            return result

        rejections.append({"pass": attempt,
                           "reason": f"validation: {bad or 'empty answer'}", "text": out})
        corrective_note = bad or "empty answer"

    result.rejections = rejections
    result.error = f"failed validation after {MAX_ATTEMPTS} attempts (production would template-fallback here)"
    return result
