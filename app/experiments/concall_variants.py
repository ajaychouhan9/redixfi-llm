"""Concall fix experiments — same measurement, only prompt/retries vary.

CONTEXT
-------
Concall is the one category that has not cleared. Annual Report and Red
Flag passed their mechanical/compliance checks on the guided-decoding
re-run; concall was reported as failing 2 of 3 real cases (empty output
after 3 attempts, plus genuine forward-tense violations).

Established offline before spending any GPU on this:

  * All 20 production gpt-4o-mini concall summaries in the benchmark
    fixture PASS the compliance validator — including ones stating explicit
    FY27 revenue guidance. So the validator is NOT miscalibrated for
    concall, and the task is demonstrably achievable under it.
  * The production prompt already prescribes the compliant construction in
    prose ("rephrase as 'management set a goal of X'"), and gpt-4o-mini's
    accepted output uses exactly that pattern.

That narrows the question to instruction-following, which is what these
variants probe.

WHAT IS HELD CONSTANT — this is the point
------------------------------------------
Every variant below reuses the REAL `concall_summary._normalize` and
`concall_summary.validate`, plus the real `parse_json_object` and the real
JSON schema. Nothing about how an answer is judged changes between
variants. Only two things vary, one at a time:

    A  retry budget      3 -> 6      (prompt unchanged)
    B  system prompt     production -> few-shot variant (retries unchanged)

so a difference in outcome is attributable.

WHAT A VARIANT RESULT DOES AND DOES NOT MEAN
--------------------------------------------
gpt-4o-mini achieved its result with the production prompt and a 3-attempt
budget. A variant that beats it on a different prompt or a larger budget
has not matched it like-for-like — it has shown what Qwen needs in order to
get there. Both facts are worth knowing; conflating them is not.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..compliance.validators import FORWARD_TENSE_RE
from ..inference.base import Backend, GenerationRequest, Message
from ..prompts import concall_summary as prod_prompt
from ..prompts import concall_summary_steered as steered_prompt
from ..prompts import concall_summary_variant as variant_prompt
from ..schemas.output_schemas import schema_for_task
from ..tasks.base import TaskResult, parse_json_object
# The REAL judging logic — imported, never reimplemented.
from ..tasks.concall_summary import TASK_NAME, _normalize, validate
from ..tasks.retry_policy import (IMPROVED_POLICY, PRODUCTION_POLICY,
                                  RetryPolicy, build_corrective_note)


@dataclass
class Variant:
    name: str
    system_prompt: str
    max_attempts: int
    description: str
    # Defaults to production so a variant varies ONLY what it names.
    policy: RetryPolicy = PRODUCTION_POLICY


def production_variant() -> Variant:
    return Variant(
        name="baseline_production",
        system_prompt=prod_prompt.SYSTEM_PROMPT,
        max_attempts=prod_prompt.MAX_ATTEMPTS,      # 3
        description="Exactly what production/gpt-4o-mini used. The control.",
    )


def retries_variant(max_attempts: int = 6) -> Variant:
    return Variant(
        name=f"retries_{max_attempts}",
        system_prompt=prod_prompt.SYSTEM_PROMPT,
        max_attempts=max_attempts,
        description=("Production prompt, larger retry budget. Cheapest possible "
                     "fix. Tests whether the model CAN produce a compliant "
                     "answer and simply needs more attempts, versus being "
                     "unable to find one at all."),
    )


def fewshot_variant() -> Variant:
    return Variant(
        name=variant_prompt.VARIANT_NAME,
        system_prompt=variant_prompt.SYSTEM_PROMPT,
        max_attempts=prod_prompt.MAX_ATTEMPTS,      # 3, so only the prompt differs
        description=("Production prompt plus worked examples of compliant "
                     "forward-looking phrasing, harvested verbatim from "
                     "production gpt-4o-mini output that passed this exact "
                     "validator."),
    )


def retry_policy_variant() -> Variant:
    return Variant(
        name="retry_policy_improved",
        system_prompt=prod_prompt.SYSTEM_PROMPT,
        max_attempts=prod_prompt.MAX_ATTEMPTS,      # 3, as production
        description=("Production prompt and production retry budget — only the "
                     "retry MECHANICS change: retries sample at a non-zero "
                     "temperature with a shifted seed, and get a directive note "
                     "quoting the rejected clause. Isolates the retry-loop fix "
                     "from any prompt change."),
        policy=IMPROVED_POLICY,
    )


def steered_variant(policy: RetryPolicy = IMPROVED_POLICY) -> Variant:
    return Variant(
        name=steered_prompt.VARIANT_NAME,
        system_prompt=steered_prompt.SYSTEM_PROMPT,
        max_attempts=prod_prompt.MAX_ATTEMPTS,      # 3, as production
        description=("Content-preference steering: report period results first "
                     "and abstract forward guidance into attributed past-tense "
                     "framings harvested from real gpt-4o-mini output. Layered "
                     "on the improved retry policy, so its delta is measured "
                     "against retry_policy_improved, not against the baseline."),
        policy=policy,
    )


def run_variant(
    backend: Backend,
    fixture: Dict[str, Any],
    model: str,
    variant: Variant,
    temperature: float = 0.0,
    max_tokens: int = 1024,
    seed: Optional[int] = 0,
) -> TaskResult:
    """Mirrors concall_summary.run()'s control flow exactly, with the
    variant's prompt and retry budget substituted. The normalize/validate/
    parse calls are the real ones."""
    result = TaskResult(
        task=f"{TASK_NAME}[{variant.name}]",
        fixture_id=str(fixture.get("benchmark_id") or fixture.get("fixture_id") or ""),
        ok=False)
    schema = schema_for_task(TASK_NAME, None)
    rejections: List[Dict[str, Any]] = []
    corrective_note: Optional[str] = None

    for attempt in range(1, variant.max_attempts + 1):
        result.attempts = attempt
        # Attempt 1 is always the caller's deterministic settings; only
        # retries vary, and only under a policy that says so.
        attempt_temperature = variant.policy.temperature_for(attempt, temperature)
        attempt_seed = variant.policy.seed_for(attempt, seed)
        request = GenerationRequest(
            messages=[
                Message("system", variant.system_prompt),
                Message("user", prod_prompt.build_user_content(fixture, corrective_note)),
            ],
            model=model, temperature=attempt_temperature, max_tokens=max_tokens,
            seed=attempt_seed, json_mode=True, json_schema=schema,
        )
        sampling = {"temperature": attempt_temperature, "seed": attempt_seed}
        generation = backend.generate(request)
        result.absorb(generation)

        if not generation.ok:
            rejections.append({"pass": attempt,
                               "reason": f"llm_exception: {generation.error}"})
            corrective_note = "the previous attempt failed to reach the model — retry"
            continue

        parsed, repaired, parse_error = parse_json_object(generation.text)
        result.json_repair_used = result.json_repair_used or repaired
        if parsed is None:
            rejections.append({"pass": attempt,
                               "reason": f"invalid_json: {parse_error}",
                               "raw_output": generation.text,
                               "raw_output_chars": len(generation.text or "")})
            corrective_note = "the previous attempt was not valid JSON"
            continue

        out = _normalize(parsed)
        bad = validate(out)
        if not bad:
            result.ok = True
            result.output = out
            result.rejections = rejections
            return result

        # Record the FULL output plus the offending span, so a post-mortem
        # can see whether the model repeats one phrase or drifts differently
        # each attempt — the distinction between "needs another try" and
        # "cannot find a compliant formulation at all".
        rejections.append({
            "pass": attempt,
            "sampling": sampling,
            "reason": bad,
            "text": out,
            "raw_text": generation.text,
            "raw_output_chars": len(generation.text or ""),
            "forward_tense_hits": _forward_hits(out),
        })
        corrective_note = build_corrective_note(bad, out, ["summary", "tone_note"],
                                                policy=variant.policy)

    result.rejections = rejections
    result.error = f"failed validation after {variant.max_attempts} attempts"
    return result


def _forward_hits(out: Dict[str, Any]) -> Dict[str, List[str]]:
    """Every forward-tense trigger in the rejected output, with context —
    the raw material for judging whether the model is stuck on one phrase."""
    hits: Dict[str, List[str]] = {}
    for field_name in ("summary", "tone_note"):
        text = out.get(field_name) or ""
        found = []
        for m in FORWARD_TENSE_RE.finditer(text):
            start = max(0, m.start() - 60)
            found.append(f"...{text[start:m.end() + 60]}...")
        if found:
            hits[field_name] = found
    return hits
