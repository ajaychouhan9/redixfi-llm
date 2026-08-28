"""Human review sheet generator.

Puts the production reference and the candidate output side by side in the
five sections the founder specified, then leaves the quality judgement
BLANK for a human:

    SOURCE / EVIDENCE
    OLD GPT-4o-mini OUTPUT
    NEW QWEN OUTPUT
    OBJECTIVE VALIDATION
    HUMAN REVIEW NOTES

Nothing here scores quality and there is no LLM judge. The OBJECTIVE
VALIDATION block carries only mechanically-checkable facts — did it pass the
same compliance validator production's output had to pass, did it obey the
schema, did the closed-set label agree, what did it cost. Everything a
reader would call "quality" sits in the blank table underneath.
"""
from __future__ import annotations

import os
from typing import Any, Dict, List

# The founder's quality dimensions, reported SEPARATELY and left unfilled.
REVIEW_CRITERIA = [
    ("factual quality", "Are the stated facts correct against the source?"),
    ("evidence grounding", "Is every claim traceable to the supplied evidence?"),
    ("completeness", "Are the important points from the evidence covered?"),
    ("hallucination", "Anything asserted that is NOT in the evidence? (none = good)"),
    ("numerical accuracy", "Any figure stated, and is it right? (AR: figures are forbidden)"),
    ("readability", "Would an investor find it clear and usable?"),
    ("compliance", "Beyond the regex: any forward-looking or advice-like tone?"),
]

VERDICTS = "ACCEPTABLE / NOT ACCEPTABLE / INCONCLUSIVE"


def _block(text: str) -> str:
    text = (text or "").strip()
    return text if text else "_(empty)_"


def _bullets(items: List[str]) -> str:
    if not items:
        return "_(none)_"
    return "\n".join(f"- {i}" for i in items)


def _pass_fail(reason) -> str:
    return "✅ PASS" if not reason else f"❌ FAIL — {reason}"


# --------------------------------------------------------------------------
# Per-task rendering of the three content sections
# --------------------------------------------------------------------------
def _source_section(task: str, case_meta: Dict[str, Any], case: Dict[str, Any]) -> str:
    lines = []
    for label, key in (("Symbol", "symbol"), ("Company", "company_name"),
                       ("Fiscal year", "fiscal_year"), ("Filing id", "filing_id"),
                       ("Doc type", "doc_type"), ("Doc kind", "doc_kind"),
                       ("Chunk id", "chunk_id"), ("Polarity", "case_polarity")):
        if case_meta.get(key):
            lines.append(f"- **{label}:** {case_meta[key]}")
    if case_meta.get("candidates"):
        lines.append(f"- **Keyword candidates:** `{', '.join(case_meta['candidates'])}`")
    if case_meta.get("question"):
        lines.append(f"- **Question:** {case_meta['question']}")
    if case_meta.get("reconstruction_status"):
        lines.append(f"- **Reconstruction:** `{case_meta['reconstruction_status']}`")

    evidence = case.get("evidence_excerpt")
    if evidence:
        lines.append(f"\n<details><summary>Evidence supplied to the model "
                     f"(first 1,500 chars)</summary>\n\n```\n{evidence}\n```\n\n</details>")
    return "\n".join(lines)


def _summary_pair(payload: Dict[str, Any], schema: str) -> str:
    if not payload:
        return "_(no output)_"
    if schema == "current_ar":
        return (f"**executive_summary**\n\n{_block(payload.get('executive_summary'))}\n\n"
                f"**key_points**\n\n{_bullets(payload.get('key_points') or [])}\n\n"
                f"**important_risks**\n\n{_bullets(payload.get('important_risks') or [])}\n\n"
                f"**key_takeaway**\n\n{_block(payload.get('key_takeaway'))}")
    if schema == "legacy_ar":
        return (f"**summary**\n\n{_block(payload.get('summary'))}\n\n"
                f"**bullets**\n\n{_bullets(payload.get('bullets') or [])}\n\n"
                f"**key_takeaway**\n\n{_block(payload.get('key_takeaway'))}")
    if schema == "concall":
        return (f"**tone_label:** `{payload.get('tone_label') or '—'}`\n\n"
                f"**summary**\n\n{_block(payload.get('summary'))}\n\n"
                f"**tone_note**\n\n{_block(payload.get('tone_note'))}")
    if schema == "red_flag":
        return (f"**risk_flag_type:** `{payload.get('risk_flag_type') or '— (no flag)'}`\n\n"
                f"**risk_flag_summary**\n\n{_block(payload.get('risk_flag_summary'))}")
    if schema == "ask_ai":
        return (f"**refused:** `{payload.get('refused')}`\n\n"
                f"{_block(payload.get('answer'))}")
    return _block(str(payload))


SCHEMA_FOR = {
    "annual_report_summary": "current_ar",
    "annual_report_summary_legacy": "legacy_ar",
    "concall_summary": "concall",
    "red_flag": "red_flag",
    "ask_ai": "ask_ai",
}

# The reference is LEGACY-shaped even when the current-schema replay runs.
REFERENCE_SCHEMA_FOR = dict(SCHEMA_FOR)
REFERENCE_SCHEMA_FOR["annual_report_summary"] = "legacy_ar"


def _objective_block(task: str, row: Dict[str, Any]) -> str:
    cmp_ = row.get("comparison") or {}
    lines = ["| Check | Result |", "|---|---|"]

    lines.append(f"| Generation succeeded | {'✅ yes' if row.get('ok') else '❌ no — ' + str(row.get('error'))} |")
    lines.append(f"| Attempts used | {row.get('attempts')} |")
    lines.append(f"| Compliance — **Qwen** | {_pass_fail(cmp_.get('candidate_compliance'))} |")

    if cmp_.get("reference_schema_matches_replay") is False:
        lines.append("| Compliance — reference | ⚠️ not comparable (schema mismatch) |")
    else:
        lines.append(f"| Compliance — reference (gpt-4o-mini) | {_pass_fail(cmp_.get('reference_compliance'))} |")
    if cmp_.get("reference_compliance_backstop_artifact"):
        lines.append("| Reference compliance note | ⚠️ backstop artifact of packet rebuild, not a production failure |")

    if task == "concall_summary":
        agree = cmp_.get("tone_label_agrees")
        lines.append(f"| tone_label — reference | `{cmp_.get('reference_tone_label')}` |")
        lines.append(f"| tone_label — Qwen | `{cmp_.get('candidate_tone_label')}` |")
        lines.append(f"| tone_label valid (closed set) | {'✅' if cmp_.get('tone_label_valid') else '❌'} |")
        lines.append(f"| tone_label agrees | {'✅ yes' if agree else ('❌ no' if agree is False else '—')} |")
    if task == "red_flag":
        lines.append(f"| Category — reference | `{cmp_.get('reference_category') or '— (no flag)'}` |")
        lines.append(f"| Category — Qwen | `{cmp_.get('candidate_category') or '— (no flag)'}` |")
        lines.append(f"| Outcome | **{cmp_.get('outcome')}** |")
    if task == "ask_ai":
        agree = cmp_.get("refusal_agreement")
        lines.append(f"| Refused — reference / Qwen | `{cmp_.get('reference_refused')}` / `{cmp_.get('candidate_refused')}` |")
        lines.append(f"| Refusal agrees | {'✅ yes' if agree else ('❌ no' if agree is False else '—')} |")

    if isinstance(cmp_.get("lexical_overlap"), (int, float)):
        lines.append(f"| Lexical overlap | {cmp_['lexical_overlap']} _(triage aid, NOT a score)_ |")
    guided = row.get("structured_output_used")
    repaired = row.get("json_repair_used")
    if guided and not repaired:
        shape = "✅ guided decoding — valid JSON by construction"
    elif guided and repaired:
        shape = "⚠️ guided decoding ON but repair still needed — investigate"
    elif repaired:
        shape = "❌ unguided, post-hoc repair was required"
    else:
        shape = "unguided, but output parsed cleanly"
    lines.append(f"| Output shape | {shape} |")
    lines.append(f"| Structured mode | `{row.get('structured_output_mode') or 'none'}` |")

    tps = (row.get("completion_tokens") or 0) / row["latency_sec"] if row.get("latency_sec") else 0
    lines.append(f"| Latency | {row.get('latency_sec')} s |")
    lines.append(f"| Input / output tokens | {row.get('prompt_tokens')} / {row.get('completion_tokens')} |")
    lines.append(f"| Tokens/sec (output) | {tps:.1f} |")
    return "\n".join(lines)


def _review_table() -> str:
    header = "| Dimension | What to look for | Qwen | Reference | Notes |\n|---|---|---|---|---|\n"
    rows = "".join(f"| **{name}** | {hint} |  |  |  |\n" for name, hint in REVIEW_CRITERIA)
    return header + rows + f"\n**Case verdict ({VERDICTS}):** ______\n"


# --------------------------------------------------------------------------
def render(run: Dict[str, Any], max_cases: int = 25) -> str:
    task = run["task"]
    summary = run.get("summary") or {}
    results = run.get("results") or []
    lines: List[str] = []

    lines.append(f"# Review sheet — {task}\n")
    lines.append(
        "> **EXPERIMENTAL / NOT PRODUCTION.** This file is evidence for a human "
        "to review, not a verdict. No quality score is computed anywhere in it, "
        "and no LLM judge was used. The candidate model is NOT declared better "
        "or worse than gpt-4o-mini by this tooling.\n")

    if run.get("backend") == "echo":
        lines.append(
            "> ⚠️ **`echo` backend — NO MODEL WAS CONSULTED.** These results "
            "validate the harness only and are not a model comparison.\n")

    if task == "annual_report_summary":
        lines.append(
            "> ⚠️ **Not a like-for-like comparison.** The stored reference was "
            "produced on 2026-08-16 by the LEGACY pipeline (raw_text front slice, "
            "`summary`/`bullets`/`key_takeaway`). This replay uses the CURRENT "
            "pipeline (Evidence Finder evidence, "
            "`executive_summary`/`key_points`/`important_risks`). Both the input "
            "AND the output schema differ. The like-for-like replay is "
            "`annual_report_summary_legacy`, which needs a 64k context.\n")

    # ---- run configuration ----
    cfg = run.get("model_config") or {}
    sampling = run.get("sampling") or {}
    fixture = run.get("fixture") or {}
    env = run.get("environment") or {}
    lines.append("## Run configuration\n")
    lines.append("| | |\n|---|---|")
    lines.append(f"| Model | `{run.get('model')}` |")
    if cfg.get("hf_repo"):
        lines.append(f"| Weights | `{cfg['hf_repo']}` |")
        lines.append(f"| Quantization / dtype | `{cfg.get('quantization')}` / `{cfg.get('dtype')}` |")
        lines.append(f"| Tensor parallel | {cfg.get('tensor_parallel_size')} |")
        lines.append(f"| Context length | {cfg.get('max_model_len')} |")
    lines.append(f"| Backend | `{run.get('backend')}` |")
    lines.append(f"| Sampling | temperature={sampling.get('temperature')}, "
                 f"max_tokens={sampling.get('max_tokens')}, seed={sampling.get('seed')} |")
    lines.append(f"| Fixture | `{fixture.get('path')}` |")
    lines.append(f"| Cases | {fixture.get('cases_run')} of {fixture.get('cases_total')} |")
    lines.append(f"| Run id | `{run.get('run_id')}` ({run.get('generated_at')}) |")
    lines.append(f"| LLM project commit | `{env.get('llm_project_commit')}` |")
    if run.get("gpu"):
        g = run["gpu"]
        lines.append(f"| GPU | {g.get('count')}x {g.get('name')} ({g.get('total_vram_gb')} GB total) |")
        lines.append(f"| CUDA / torch / vLLM | {g.get('cuda')} / {g.get('torch')} / {g.get('vllm')} |")
    lines.append("")

    # ---- objective roll-up ----
    lines.append("## Objective signals (mechanical only — no judgement)\n")
    lines.append("| Metric | Value |\n|---|---|")
    for key, value in summary.items():
        if isinstance(value, dict):
            value = ", ".join(f"{k}={v}" for k, v in value.items())
        lines.append(f"| {key} | {value} |")
    lines.append("")

    if task == "red_flag":
        lines.append(
            "**Reading the outcomes:** `false_positive` = Qwen flagged where "
            "production did not · `false_negative` = Qwen missed a flag production "
            "confirmed · `category_mismatch` = both flagged, different category.\n")

    # ---- cases ----
    lines.append("## Cases\n")
    shown = results[:max_cases]
    if len(results) > len(shown):
        lines.append(f"_Showing the first {len(shown)} of {len(results)}._\n")

    cand_schema = SCHEMA_FOR.get(task, task)
    ref_schema = REFERENCE_SCHEMA_FOR.get(task, task)

    for i, row in enumerate(shown, start=1):
        meta = row.get("case_meta") or {}
        bid = meta.get("benchmark_id") or row.get("fixture_id")
        lines.append(f"---\n\n### Case {i} — `{bid}`\n")

        lines.append("#### SOURCE / EVIDENCE\n")
        lines.append(_source_section(task, meta, row) or "_(no source metadata)_")
        prov = row.get("provenance") or {}
        if prov:
            lines.append(f"\n- **Reference pipeline:** `{prov.get('pipeline_version')}` "
                         f"· model `{prov.get('reference_model')}` "
                         f"· prompt `{prov.get('reference_prompt_version')}`")
            if prov.get("limitations"):
                lines.append("- **Recorded limitations:**")
                for lim in prov["limitations"]:
                    lines.append(f"  - {lim}")
        lines.append("")

        lines.append("#### OLD — GPT-4o-mini OUTPUT (production reference)\n")
        lines.append(_summary_pair(row.get("reference") or {}, ref_schema))
        lines.append("")

        lines.append(f"#### NEW — QWEN OUTPUT (`{run.get('model')}`)\n")
        lines.append(_summary_pair(row.get("output") or {}, cand_schema))
        if row.get("rejections"):
            lines.append("\n<details><summary>Rejected attempts</summary>\n")
            for r in row["rejections"]:
                lines.append(f"- pass {r.get('pass')}: {r.get('reason')}")
            lines.append("\n</details>")
        lines.append("")

        lines.append("#### OBJECTIVE VALIDATION\n")
        lines.append(_objective_block(task, row))
        lines.append("")

        lines.append("#### HUMAN REVIEW NOTES\n")
        lines.append(_review_table())

    lines.append("\n---\n\n## Overall reviewer verdict\n")
    lines.append(
        "Fill this in only AFTER completing the per-case tables above.\n\n"
        f"- **Verdict ({VERDICTS}):** ______\n"
        "- **If NOT ACCEPTABLE — the specific failure mode:** ______\n"
        "- **If INCONCLUSIVE — what additional cases would settle it:** ______\n"
        "- **Reviewer:** ______   **Date:** ______\n\n"
        "This was a small sample. It cannot establish production-readiness "
        "regardless of how good the outputs look.\n")
    return "\n".join(lines)


def save(run: Dict[str, Any], path: str, max_cases: int = 25) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(render(run, max_cases=max_cases))
    return path
