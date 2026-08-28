"""Human review sheet generator.

Produces a markdown document putting the production reference and the
candidate output side by side, followed by an UNFILLED scoring table across
the criteria the founder specified. The scores are blank on purpose: this
project does not auto-score quality, and a report that arrived pre-scored
would quietly become the authority the brief says it must not be.
"""
from __future__ import annotations

from typing import Any, Dict, List

# The founder's criteria list, verbatim in intent.
REVIEW_CRITERIA = [
    "factual correctness",
    "numerical accuracy",
    "financial terminology",
    "evidence grounding",
    "hallucination (none = good)",
    "completeness",
    "relevance",
    "reasoning quality",
    "source/citation correctness",
    "risk identification accuracy",
    "consistency",
    "formatting",
    "usefulness to an investor",
]


def _fence(text: str) -> str:
    return (text or "_(empty)_").strip()


def _bullets(items: List[str]) -> str:
    if not items:
        return "_(none)_"
    return "\n".join(f"- {item}" for item in items)


def _ar_block(payload: Dict[str, Any], label: str) -> str:
    if not payload:
        return f"**{label}:** _(no output)_\n"
    return (
        f"**{label} — executive_summary**\n\n{_fence(payload.get('executive_summary'))}\n\n"
        f"**{label} — key_points**\n\n{_bullets(payload.get('key_points') or [])}\n\n"
        f"**{label} — important_risks**\n\n{_bullets(payload.get('important_risks') or [])}\n\n"
        f"**{label} — key_takeaway**\n\n{_fence(payload.get('key_takeaway'))}\n"
    )


def _scoring_table() -> str:
    header = "| Criterion | Reference (OpenAI) | Candidate | Notes |\n|---|---|---|---|\n"
    rows = "".join(f"| {c} |  |  |  |\n" for c in REVIEW_CRITERIA)
    return header + rows


def render(run: Dict[str, Any], max_cases: int = 25) -> str:
    task = run["task"]
    summary = run.get("summary") or {}
    lines: List[str] = []

    lines.append(f"# Evaluation review sheet — {task}\n")
    lines.append(
        "> **EXPERIMENTAL / NOT PRODUCTION.** Nothing here is evidence that the "
        "candidate model is fit for use. The objective columns below are "
        "mechanical checks; every quality judgement is left blank for a human "
        "reviewer, by design.\n"
    )

    lines.append("## Run configuration\n")
    lines.append(f"- **Model:** `{run['model']}`")
    config = run.get("model_config") or {}
    if config.get("hf_repo"):
        lines.append(
            f"- **Weights:** `{config['hf_repo']}` "
            f"(quantization: `{config.get('quantization')}`, dtype: `{config.get('dtype')}`, "
            f"TP: {config.get('tensor_parallel_size')}, max_model_len: {config.get('max_model_len')})"
        )
    lines.append(f"- **Backend:** `{run.get('backend')}`")
    sampling = run.get("sampling") or {}
    lines.append(
        f"- **Sampling:** temperature={sampling.get('temperature')}, "
        f"max_tokens={sampling.get('max_tokens')}, seed={sampling.get('seed')}"
    )
    fixture = run.get("fixture") or {}
    lines.append(f"- **Fixture:** `{fixture.get('path')}` (exported {fixture.get('exported_at')})")
    lines.append(f"- **Cases run:** {fixture.get('cases_run')} of {fixture.get('cases_total')}")
    env = run.get("environment") or {}
    lines.append(f"- **LLM project commit:** `{env.get('llm_project_commit')}`")
    lines.append(f"- **Run id:** `{run.get('run_id')}` ({run.get('generated_at')})\n")

    if run.get("backend") == "echo":
        lines.append(
            "> ⚠️ **This run used the `echo` backend.** No model was consulted. "
            "These results validate the harness only and must never be read as "
            "a model comparison.\n"
        )

    lines.append("## Objective signals (mechanical, no judgement)\n")
    lines.append("| Metric | Value |\n|---|---|")
    for key, value in summary.items():
        if isinstance(value, dict):
            value = ", ".join(f"{k}={v}" for k, v in value.items())
        lines.append(f"| {key} | {value} |")
    lines.append("")

    if task == "red_flag":
        lines.append(
            "**Reading the outcomes:** `false_positive` = candidate flagged where "
            "production did not; `false_negative` = candidate missed a flag "
            "production confirmed; `category_mismatch` = both flagged, different "
            "category. These are the numbers that matter for this task.\n"
        )

    lines.append("## Side-by-side cases\n")
    results = run.get("results") or []
    shown = results[:max_cases]
    if len(results) > len(shown):
        lines.append(f"_Showing the first {len(shown)} of {len(results)} cases._\n")

    for index, row in enumerate(shown, start=1):
        meta = row.get("case_meta") or {}
        label = meta.get("symbol") or meta.get("chunk_id") or row.get("fixture_id")
        lines.append(f"### {index}. `{label}` — fixture `{row.get('fixture_id')}`\n")

        if meta.get("question"):
            lines.append(f"**Question:** {meta['question']}\n")
        if meta.get("fiscal_year"):
            lines.append(f"**Fiscal year:** {meta['fiscal_year']}\n")
        if meta.get("candidates"):
            lines.append(f"**Keyword candidates:** `{', '.join(meta['candidates'])}`\n")

        comparison = row.get("comparison") or {}
        reference = row.get("reference") or {}
        candidate = row.get("output") or {}

        if not row.get("ok"):
            lines.append(f"> **Generation failed:** {row.get('error')}\n")
            for rejection in row.get("rejections") or []:
                lines.append(f"> - pass {rejection.get('pass')}: {rejection.get('reason')}")
            lines.append("")

        if task == "annual_report_summary":
            lines.append(_ar_block(reference, "REFERENCE (production, gpt-4o-mini)"))
            lines.append(_ar_block(candidate, "CANDIDATE"))
        elif task == "red_flag":
            lines.append(
                f"| | Category | Summary |\n|---|---|---|\n"
                f"| **Reference** | `{reference.get('risk_flag_type') or '—'}` | "
                f"{_fence(reference.get('risk_flag_summary')).replace(chr(10), ' ')} |\n"
                f"| **Candidate** | `{candidate.get('risk_flag_type') or '—'}` | "
                f"{_fence(candidate.get('risk_flag_summary')).replace(chr(10), ' ')} |\n"
            )
            lines.append(f"**Outcome:** `{comparison.get('outcome')}`\n")
            chunk_text = (row.get("case_meta") or {}).get("chunk_text")
            if chunk_text:
                lines.append(f"<details><summary>Source excerpt</summary>\n\n{chunk_text}\n\n</details>\n")
        else:  # ask_ai
            lines.append(
                f"**REFERENCE (production, gpt-4o-mini)** "
                f"— refused={reference.get('refused')}\n\n{_fence(reference.get('answer'))}\n"
            )
            lines.append(
                f"**CANDIDATE** — refused={candidate.get('refused')}\n\n"
                f"{_fence(candidate.get('answer'))}\n"
            )

        cand_compliance = comparison.get("candidate_compliance")
        ref_compliance = comparison.get("reference_compliance")
        lines.append(
            f"**Compliance —** candidate: "
            f"{'❌ ' + str(cand_compliance) if cand_compliance else '✅ pass'} · "
            f"reference: {'❌ ' + str(ref_compliance) if ref_compliance else '✅ pass'}\n"
        )
        if isinstance(comparison.get("lexical_overlap"), (int, float)):
            lines.append(
                f"**Lexical overlap:** {comparison['lexical_overlap']} "
                "_(triage aid only — not a quality score)_\n"
            )

        lines.append("**Human review** — fill this in:\n")
        lines.append(_scoring_table())
        lines.append("\n---\n")

    lines.append("## Reviewer verdict\n")
    lines.append(
        "After completing the tables above, record ONE of:\n\n"
        "- **ACCEPTABLE** — quality is close enough to production to justify a "
        "narrow, reversible pilot on one workload.\n"
        "- **NOT ACCEPTABLE** — name the specific failure mode.\n"
        "- **INCONCLUSIVE** — say what additional cases would settle it.\n\n"
        "Verdict: _______   Reviewer: _______   Date: _______\n"
    )
    return "\n".join(lines)


def save(run: Dict[str, Any], path: str, max_cases: int = 25) -> str:
    import os
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(render(run, max_cases=max_cases))
    return path
