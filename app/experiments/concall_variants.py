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
from typing import Any, Callable, Dict, List, Optional

from ..compliance.validators import FORWARD_TENSE_RE
from ..inference.base import Backend, GenerationRequest, Message
from ..prompts import concall_summary as prod_prompt
from ..prompts import concall_summary_fewshot_bank as fewshot_bank_prompt
from ..prompts import concall_summary_markdown_fairness as markdown_prompt
from ..prompts import concall_summary_steered as steered_prompt
from ..prompts import concall_summary_variant as variant_prompt
from ..schemas.output_schemas import schema_for_task
from ..tasks.base import TaskResult, parse_json_object
from ..tasks.context_budget import plan_context
from ..tasks.rephrase import (build_rephrase_backend, build_rephrase_request,
                              collect_validator_findings,
                              information_preservation_check,
                              is_eligible_for_rephrase)
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
    # Every prior variant here varied only the SYSTEM prompt, using
    # prod_prompt.build_user_content(fixture, corrective_note) unconditionally
    # for the user message. Retrieved few-shot examples are dynamic PER CASE
    # content, which belongs in the user message, not a static system string
    # — so this is a hook, not a second system-prompt mechanism. None means
    # "use production's user-content builder", so every existing variant's
    # behaviour is unchanged by this field's addition.
    user_content_fn: Optional[Callable[[Dict[str, Any], Optional[str]], str]] = None


def production_variant() -> Variant:
    return Variant(
        name="baseline_production",
        system_prompt=prod_prompt.SYSTEM_PROMPT,
        max_attempts=prod_prompt.MAX_ATTEMPTS,      # 3
        description="Exactly what production/gpt-4o-mini used. The control.",
    )


def retries_variant(max_attempts: int = 6,
                    policy: RetryPolicy = PRODUCTION_POLICY) -> Variant:
    """`policy` defaults to PRODUCTION_POLICY so old callers/tests are
    unaffected. This matters here specifically: the ORIGINAL retries_6
    result (repaired 2/5) was measured under PRODUCTION_POLICY — every
    attempt at temperature=0, so retries 2 through 6 mostly reproduced
    attempt 1's rejected text verbatim. That is a test of "does raising the
    budget help when every retry is identical", not "does raising the
    budget help now that retries genuinely differ" — those are different
    questions, and conflating them would misread which one this answers."""
    tag = policy.name if policy is not PRODUCTION_POLICY else "production"
    return Variant(
        name=f"retries_{max_attempts}_{tag}",
        system_prompt=prod_prompt.SYSTEM_PROMPT,
        max_attempts=max_attempts,
        description=("Production prompt, larger retry budget. Cheapest possible "
                     "fix. Tests whether the model CAN produce a compliant "
                     "answer and simply needs more attempts, versus being "
                     "unable to find one at all."),
        policy=policy,
    )


def retries_extended_variant(max_attempts: int = 8) -> Variant:
    """Larger retry budget UNDER THE IMPROVED POLICY — the test the original
    retries_6 result could not answer, because it ran before temp/seed
    variation existed. Now that a retry demonstrably produces different
    text (measured: similarity 0.04-0.36 vs 1.000 under production), more
    attempts may simply be more genuine chances to land compliant phrasing,
    rather than more repeats of the same rejected text."""
    v = retries_variant(max_attempts, policy=IMPROVED_POLICY)
    return Variant(
        name=v.name,
        system_prompt=v.system_prompt,
        max_attempts=v.max_attempts,
        description=("Production PROMPT (unmodified) + the improved retry "
                     f"policy (varied sampling, directive notes) + a larger "
                     f"budget ({max_attempts} attempts, vs production's 3). "
                     "Isolates budget size as the only additional variable on "
                     "top of the already-committed retry-mechanics fix — no "
                     "steering, no markdown instruction, no other prompt "
                     "change."),
        policy=v.policy,
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


def markdown_fairness_variant() -> Variant:
    """ONE line added to the production prompt, forbidding markdown
    explicitly. PRODUCTION_POLICY, hardcoded — this is deliberately NOT
    combined with the retry-sampling fix or with content steering, so any
    change in outcome is attributable to the one added line alone, applied
    identically to whichever model is running."""
    return Variant(
        name=markdown_prompt.VARIANT_NAME,
        system_prompt=markdown_prompt.SYSTEM_PROMPT,
        max_attempts=prod_prompt.MAX_ATTEMPTS,      # 3, as production
        description=("Production prompt plus ONE explicit line forbidding "
                     "markdown/asterisks/bold. Production retry policy — no "
                     "sampling variation, no directive notes, no content "
                     "steering. Isolates whether a stronger markdown "
                     "instruction alone changes behaviour, and whether "
                     "forbidden-figure violations found inside markdown "
                     "persist once the markdown itself is suppressed."),
        policy=PRODUCTION_POLICY,
    )


def fewshot_bank_variant(
    bank_entries: List[Dict[str, Any]],
    policy: RetryPolicy = IMPROVED_POLICY,
    max_attempts: Optional[int] = None,
    k: int = 2,
) -> Variant:
    """Retrieval-augmented few-shot: the SYSTEM prompt is UNMODIFIED
    production; the user message gets 1-2 REAL prior validated examples,
    retrieved by similarity from `bank_entries`, prepended before the
    current case. No forbidden vocabulary is named anywhere in this
    variant — a deliberate contrast with every other prompt change tried
    this session, all of which named forbidden words or added rules.

    `bank_entries` is passed in (not loaded internally) so the caller
    controls exactly which snapshot of the bank is used — important for a
    leave-one-out test, where the SAME bank is reused per case but the
    current case's own id is excluded at retrieval time inside
    `build_variant_user_content`, not by pre-filtering the bank here.

    Defaults to IMPROVED_POLICY and max_attempts=None (falls back to
    production's 3) so this can be composed with the retry-budget fix if
    desired, or tested against the production retry budget alone — the
    caller decides which comparison this run is meant to isolate."""
    return Variant(
        name=fewshot_bank_prompt.VARIANT_NAME,
        system_prompt=fewshot_bank_prompt.SYSTEM_PROMPT,   # == production, unmodified
        max_attempts=max_attempts or prod_prompt.MAX_ATTEMPTS,
        description=(f"Production SYSTEM prompt, completely unmodified. Only "
                     f"the user message differs: up to {k} REAL validated "
                     "prior successes, retrieved by jaccard similarity from "
                     "the accumulating example bank, prepended before the "
                     "current document. No forbidden vocabulary is named "
                     "anywhere — the examples are positive demonstrations "
                     "only, testing a mechanism different from every other "
                     "prompt change tried this session."),
        policy=policy,
        user_content_fn=lambda fixture, note: fewshot_bank_prompt.build_variant_user_content(
            fixture, bank_entries, note, k=k),
    )


def run_variant(
    backend: Backend,
    fixture: Dict[str, Any],
    model: str,
    variant: Variant,
    temperature: float = 0.0,
    max_tokens: int = 1024,
    seed: Optional[int] = 0,
    rephrase_backend: Optional[Backend] = None,
) -> TaskResult:
    """Mirrors concall_summary.run()'s new control flow: ONE Qwen attempt,
    then a single GPT-4o-mini compliance edit on eligible validator failures.
    The normalize/validate/parse calls are the real ones. Validator-driven
    Qwen retries are gone (2026-08-31)."""
    result = TaskResult(
        task=f"{TASK_NAME}[{variant.name}]",
        fixture_id=str(fixture.get("benchmark_id") or fixture.get("fixture_id") or ""),
        ok=False)
    schema = schema_for_task(TASK_NAME, None)
    rejections: List[Dict[str, Any]] = []

    # Pre-generation context budget (same guard as task_cc.run). Applied to
    # production-prompt variants, which is the path BAJFINANCE actually uses.
    planned_user: Optional[str] = None
    if variant.user_content_fn is None:
        planned_user, context_log = plan_context(TASK_NAME, fixture, model, max_tokens)
        result.context_log = context_log
        if planned_user is None:
            result.ok = False
            result.error = f"context_overflow: {context_log}"
            result.final_status = "HUMAN_REVIEW_REQUIRED"
            result.human_review_required = True
            result.human_review_reason = result.error
            return result

    # ONE Qwen generation.
    result.attempts = 1
    attempt_temperature = variant.policy.temperature_for(1, temperature)
    attempt_seed = variant.policy.seed_for(1, seed)
    if variant.user_content_fn is not None:
        user_content = variant.user_content_fn(fixture, None)
    else:
        user_content = planned_user or ""
    request = GenerationRequest(
        messages=[
            Message("system", variant.system_prompt),
            Message("user", user_content),
        ],
        model=model, temperature=attempt_temperature, max_tokens=max_tokens,
        seed=attempt_seed, json_mode=True, json_schema=schema,
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

    result.rejections = [{
        "pass": 1,
        "sampling": sampling,
        "reason": bad,
        "text": out,
        "raw_text": generation.text,
        "raw_output_chars": len(generation.text or ""),
        "forward_tense_hits": _forward_hits(out),
    }]

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


def run_variant_evaluation(
    backend: Backend,
    fixtures: Any,
    model: str,
    variant: Variant,
    *,
    temperature: float = 0.0,
    max_tokens: int = 1024,
    seed: Optional[int] = 0,
    limit: Optional[int] = None,
    progress: Optional[Any] = None,
    gpu: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Run a variant over a WHOLE fixture set and emit the same run shape
    `run_evaluation` produces, so a variant result renders through the same
    review sheet and is directly comparable to the baseline.

    The comparison and aggregation are the real ones, imported — a variant
    is never scored by anything the baseline was not scored by."""
    from datetime import datetime, timezone

    from ..evaluation import compare as compare_mod

    cases = fixtures.cases[:limit] if limit else fixtures.cases
    rows: List[Dict[str, Any]] = []

    for index, case in enumerate(cases, start=1):
        bid = str(case.get("benchmark_id") or case.get("fixture_id"))
        if progress:
            progress(index, len(cases), bid)
        result = run_variant(backend, case, model, variant,
                             temperature=temperature, max_tokens=max_tokens,
                             seed=seed)
        row = result.to_dict()
        # Scored as concall_summary, not as the variant's decorated task
        # name, so the comparator and aggregator behave identically.
        row["comparison"] = compare_mod.compare(TASK_NAME, case, result.output)
        row["reference"] = case.get("reference")
        row["case_meta"] = {k: case.get(k) for k in
                            ("benchmark_id", "symbol", "company_name",
                             "filing_date", "doc_kind") if k in case}
        evidence = case.get("input_text") or ""
        if evidence:
            row["evidence_excerpt"] = evidence[:1500] + (
                "\n\n… truncated for review; full text is in the fixture …"
                if len(evidence) > 1500 else "")
        rows.append(row)

    return {
        "run_id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task": TASK_NAME,
        "variant": {
            "name": variant.name,
            "description": variant.description,
            "max_attempts": variant.max_attempts,
            "retry_policy": variant.policy.name,
            "prompt_is_production": variant.system_prompt == prod_prompt.SYSTEM_PROMPT,
        },
        "model": model,
        "backend": getattr(backend, "name", "unknown"),
        "sampling": {"temperature": temperature, "max_tokens": max_tokens,
                     "seed": seed},
        "gpu": gpu,
        "like_for_like_with_reference": (
            variant.system_prompt == prod_prompt.SYSTEM_PROMPT
            and variant.policy is PRODUCTION_POLICY
            and variant.max_attempts == prod_prompt.MAX_ATTEMPTS),
        "fixture": {"path": fixtures.path, "cases_total": len(fixtures.cases),
                    "cases_run": len(cases)},
        "summary": compare_mod.aggregate(TASK_NAME, rows),
        "results": rows,
    }


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
