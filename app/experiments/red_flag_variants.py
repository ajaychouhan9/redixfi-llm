"""Red Flag prompt experiments — same measurement, only the prompt varies.

CONTEXT
-------
At n=60, red_flag showed 7 false positives (0 false positives had been seen
at the earlier n=6 smoke size — the small-sample warning from that session
validated again: a failure mode invisible at n=6 was the dominant one at
n=60). Checked individually before writing any fix — see
app/prompts/red_flag_instance_check.py's docstring for the breakdown: 4 of
7 share one root cause (accounting-policy boilerplate misread as an actual
disclosed instance), 2 of 7 are a different, harder issue (a genuine Key
Audit Matter that gpt-4o-mini itself sometimes DOES flag elsewhere in this
same set, so no blanket rule is safe), and 1 of 7 is a third pattern
(a category name mentioned in an unrelated list, never elaborated on).

WHAT IS HELD CONSTANT — this is the point
------------------------------------------
Every variant reuses the REAL `red_flag.violation` compliance check, the
real `parse_json_object`, and the real JSON schema (including red_flag's
DYNAMIC per-chunk category enum). Only the SYSTEM PROMPT varies. red_flag
has no retry loop in production (`classify_chunk` makes exactly one call),
so there is no retry-policy axis here the way there is for concall.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..inference.base import Backend, GenerationRequest, Message
from ..prompts import red_flag as prod_prompt
from ..prompts import red_flag_instance_check as instance_check_prompt
from ..prompts import red_flag_stage1_v1 as stage1_v1_prompt
from ..schemas.output_schemas import schema_for_task
from ..tasks.base import TaskResult, parse_json_object
# The REAL judging logic — imported, never reimplemented.
from ..tasks.red_flag import TASK_NAME
from ..compliance.validators import violation


@dataclass
class Variant:
    name: str
    system_prompt: str
    description: str
    # 2026-09-19: when True, `is_red_flag` is added to the request schema's
    # `required` list (production/baseline leaves it optional — see
    # output_schemas.py::red_flag_schema's own note) and run_variant()
    # enforces it as an AND-condition alongside `category`. Only set for a
    # variant whose prompt actually explains the field.
    requires_is_red_flag: bool = False


def production_variant() -> Variant:
    return Variant(
        name="baseline_production",
        system_prompt=prod_prompt.SYSTEM_PROMPT,
        description="Exactly what production/gpt-4o-mini used. The control.",
    )


def instance_check_variant() -> Variant:
    return Variant(
        name=instance_check_prompt.VARIANT_NAME,
        system_prompt=instance_check_prompt.SYSTEM_PROMPT,
        # MEASURED 2026-08-30, n=60 (not the pre-test prediction this
        # description originally carried, which expected 4/7 targeted and
        # was too optimistic in one direction, too pessimistic in another):
        # ALL 7 known false positives were suppressed (7 -> 1; the 1
        # remaining, ASIANPAINT-679, is a NEW false positive at a
        # previously-correct case, not a surviving original one). But
        # false negatives rose from 2 to 28, spread across every category
        # (auditor_qualification 9, related_party_transaction 6,
        # promoter_pledge 6, contingent_liability 5) — including genuine
        # Key Audit Matters gpt-4o-mini itself confirms (ABB-277,
        # HDFCBANK-766). Overall agreement fell 0.85 -> 0.5167. A large net
        # regression: do not adopt as-is. See CONCALL_AND_REDFLAG_TUNING.md.
        description=("Production prompt plus ONE added instruction "
                     "distinguishing a policy DESCRIPTION from an actual "
                     "disclosed INSTANCE, using the real confirmed "
                     "false-positive chunk (BAJFINANCE-488) as the negative "
                     "example. MEASURED: fixed all 7 known false positives, "
                     "but introduced 26 new false negatives (2 -> 28) by "
                     "over-suppressing genuine instances across every "
                     "category, including real Key Audit Matters gpt-4o-mini "
                     "itself confirms elsewhere. Net regression "
                     "(agreement 0.85 -> 0.5167) — NOT a fix as written."),
    )


def stage1_v1_variant() -> Variant:
    return Variant(
        name=stage1_v1_prompt.VARIANT_NAME,
        system_prompt=stage1_v1_prompt.SYSTEM_PROMPT,
        requires_is_red_flag=True,
        description=("Asymmetric follow-up to instance_check_v1's proven "
                     "regression, per that variant's own recommended next "
                     "step: full policy-vs-instance framing for "
                     "contingent_liability and related_party_transaction "
                     "(the near-universal-boilerplate categories), but ONLY "
                     "positive framing for auditor_qualification (what DOES "
                     "count — never names 'Key Audit Matter' or 'unmodified "
                     "opinion' as an exclusion, to avoid the negation-priming "
                     "pattern measured on concall_summary at n=20). Adds an "
                     "explicit is_red_flag field (required in this variant's "
                     "schema, unlike baseline_production's) rather than "
                     "relying solely on category:null."),
    )


def run_variant(
    backend: Backend,
    fixture: Dict[str, Any],
    model: str,
    variant: Variant,
    temperature: float = 0.0,
    max_tokens: int = 512,
    seed: Optional[int] = 0,
) -> TaskResult:
    """Mirrors red_flag.run()'s control flow exactly, with the variant's
    prompt substituted. The candidate-membership check, compliance check
    and metadata contract (never storing null, fail-soft to unflagged) are
    the real ones — reimplementing them here would risk silently judging a
    variant by different rules than production uses."""
    result = TaskResult(
        task=f"{TASK_NAME}[{variant.name}]",
        fixture_id=str(fixture.get("benchmark_id") or fixture.get("fixture_id") or ""),
        ok=False)
    schema = schema_for_task(TASK_NAME, fixture)
    if schema and variant.requires_is_red_flag:
        # Only this variant's own schema gets is_red_flag as REQUIRED —
        # baseline_production's schema (built the same way, via
        # schema_for_task) stays optional-only, since its prompt never
        # asks for the field. See output_schemas.py::red_flag_schema's
        # own note.
        schema = {**schema, "required": [*schema["required"], "is_red_flag"]}
    candidates = list(fixture.get("candidates") or [])

    if not candidates:
        result.ok = True
        result.attempts = 0
        result.output = {"risk_classified": True}
        return result

    request = GenerationRequest(
        messages=[
            Message("system", variant.system_prompt),
            Message("user", prod_prompt.build_user_content(fixture)),
        ],
        model=model, temperature=temperature, max_tokens=max_tokens,
        seed=seed, json_mode=True, json_schema=schema,
    )
    generation = backend.generate(request)
    result.absorb(generation)
    result.attempts = 1

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
            if category else "model returned no category (genuine non-match)")

    # Same backward-compatible AND-condition app/tasks/red_flag.py::run()
    # applies: a missing is_red_flag (baseline_production's prompt never
    # asks for it) defaults to legacy behaviour; a variant that DOES ask
    # for it (requires_is_red_flag=True, enforced above via the schema)
    # gets the stricter check.
    if "is_red_flag" in parsed and not bool(parsed.get("is_red_flag")):
        return unflagged("category matched a topic but is_red_flag=false (no adverse finding)")

    summary = str(parsed.get("summary") or "").strip()
    if not summary:
        return unflagged("confirmed a category but returned an empty summary")

    bad = violation(summary)
    if bad:
        return unflagged(f"summary failed compliance: {bad}")

    result.ok = True
    result.output = {"risk_classified": True, "risk_flag_type": category,
                     "risk_flag_summary": summary}
    return result


def run_variant_evaluation(
    backend: Backend,
    fixtures: Any,
    model: str,
    variant: Variant,
    *,
    temperature: float = 0.0,
    max_tokens: int = 512,
    seed: Optional[int] = 0,
    limit: Optional[int] = None,
    progress: Optional[Any] = None,
    gpu: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Runs a variant over a whole fixture set and emits the same run shape
    `run_evaluation` produces, so it renders through the same review sheet
    and is directly comparable to the baseline. Scored with the real
    imported comparator/aggregator — never a second implementation."""
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
        row["comparison"] = compare_mod.compare(TASK_NAME, case, result.output)
        row["reference"] = case.get("reference")
        row["case_meta"] = {k: case.get(k) for k in
                            ("benchmark_id", "symbol", "candidates",
                             "case_polarity", "chunk_id") if k in case}
        evidence = case.get("chunk_text") or ""
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
            "prompt_is_production": variant.system_prompt == prod_prompt.SYSTEM_PROMPT,
        },
        "model": model,
        "backend": getattr(backend, "name", "unknown"),
        "sampling": {"temperature": temperature, "max_tokens": max_tokens,
                     "seed": seed},
        "gpu": gpu,
        "like_for_like_with_reference": variant.system_prompt == prod_prompt.SYSTEM_PROMPT,
        "fixture": {"path": fixtures.path, "cases_total": len(fixtures.cases),
                    "cases_run": len(cases)},
        "summary": compare_mod.aggregate(TASK_NAME, rows),
        "results": rows,
    }
