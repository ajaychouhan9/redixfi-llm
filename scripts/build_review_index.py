#!/usr/bin/env python3
"""Build a single entry-point index over the expanded review runs.

WHY
---
The expanded run produces one review sheet per category, each with dozens
of cases. A reviewer opening a 60-case red-flag sheet has no cheap way to
see which cases are worth reading first, or which comparisons are even
valid. This builds the front page: what ran, what the objective signals
say, which cases disagree with gpt-4o-mini, and — importantly — which
comparisons carry a known caveat.

It computes NOTHING about quality. It ranks by disagreement and by
objective flags only, so a reviewer spends their attention where the two
models actually differ. Every quality judgement stays in the blank tables
inside the sheets themselves.

    python scripts/build_review_index.py --out evaluation/REVIEW_INDEX.md
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TASK_LABEL = {
    "annual_report_summary": "Annual Report (current pipeline)",
    "annual_report_summary_legacy": "Annual Report (legacy replay — like-for-like)",
    "concall_summary": "Concall",
    "red_flag": "Red Flag",
    "ask_ai": "Ask AI (out of scope for Qwen migration)",
}


def _latest_runs(pattern: str, min_cases: int):
    """Newest run per task, ignoring tiny smoke runs and echo runs.

    A PROMPT-VARIANT run carries the same `task` as the baseline it is
    compared against, so without separating them the newest variant would
    silently displace the production-prompt result in this index — and the
    headline table would then report a number that was not obtained on the
    production prompt. Variants are keyed separately and labelled."""
    best, variants = {}, {}
    for path in sorted(glob.glob(pattern)):
        if os.path.basename(path).startswith("concall_experiments"):
            continue
        try:
            run = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        if run.get("backend") == "echo":
            continue
        if len(run.get("results") or []) < min_cases:
            continue
        task = run.get("task")
        bucket = variants if run.get("variant") else best
        # Key by MODEL as well as task. Without this, a second model's run is
        # newer and silently displaces the first's row — the headline table
        # would show one model's number under a heading that reads as though
        # it covered the category, and the comparison would vanish.
        model = run.get("model", "?")
        # The variant bucket needs the SAME model-keying fix: two models can
        # run the identical variant (e.g. concall_markdown_fairness_v1), and
        # without ::model the second model's run silently overwrote the
        # first's row here too.
        key = (f"{task}[{run['variant']['name']}]::{model}" if run.get("variant")
               else f"{task}::{model}")
        prev = bucket.get(key)
        # Rank by (run_id, has-regenerated-reference). The re-scored copy of
        # a run shares its run_id, so without the second term the tie breaks
        # by filename and the index would show the SUPERSEDED scoring — the
        # one compared against legacy-schema stubs.
        rank = (run.get("run_id", ""), 1 if run.get("reference_source") else 0)
        prev_rank = ((prev[1].get("run_id", ""),
                      1 if prev[1].get("reference_source") else 0)
                     if prev else None)
        if prev is None or rank > prev_rank:
            bucket[key] = (path, run)
    return best, variants


def _disagreements(task: str, run: dict):
    """Cases where Qwen and gpt-4o-mini differ on an OBJECTIVE, closed-set
    field. Not a quality judgement — a reading-order aid."""
    out = []
    for row in run.get("results") or []:
        c = row.get("comparison") or {}
        meta = row.get("case_meta") or {}
        bid = meta.get("benchmark_id") or row.get("fixture_id")
        if not row.get("ok"):
            out.append((bid, f"GENERATION FAILED — {row.get('error')}"))
        elif task == "red_flag" and c.get("outcome") not in ("agree", "agree_no_flag"):
            out.append((bid, f"category {c.get('outcome')}: "
                             f"ref={c.get('reference_category')} "
                             f"qwen={c.get('candidate_category')}"))
        elif task == "concall_summary" and c.get("tone_label_agrees") is False:
            out.append((bid, f"tone: ref={c.get('reference_tone_label')} "
                             f"qwen={c.get('candidate_tone_label')}"))
        elif c.get("candidate_compliance"):
            out.append((bid, f"compliance: {c.get('candidate_compliance')}"))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", default="evaluation/*/runs/*.json")
    ap.add_argument("--min-cases", type=int, default=5,
                    help="ignore smoke runs below this size")
    ap.add_argument("--out", default="evaluation/REVIEW_INDEX.md")
    args = ap.parse_args()

    runs, variant_runs = _latest_runs(args.glob, args.min_cases)
    if not runs and not variant_runs:
        print("no qualifying runs found")
        return

    L = []
    L.append("# Expanded review — index\n")
    L.append("> **EXPERIMENTAL / NOT PRODUCTION.** Nothing here scores quality. "
             "The tables below carry only mechanically-checkable signals and a "
             "suggested reading order; every quality judgement lives in the "
             "blank HUMAN REVIEW NOTES tables inside the per-case sheets.\n")
    L.append(f"_Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC_\n")
    L.append("> ## ⚠️ Read this before comparing any two runs\n"
             ">\n"
             "> **Generation on this hardware is NOT reproducible run-to-run, "
             "even at `temperature=0` with a fixed seed.** Observed from a SINGLE "
             "before/after comparison (n=2 samples per case, not a repeated-trial "
             "measurement — see `ACTIONS_1_3_FULL_RESULTS.md` for the precise "
             "accounting of what was and wasn't measured): re-running the same "
             "fixtures with identical settings, attempt-1 output differed on "
             "**4 of 20** annual-report cases and **7 of 20** concall cases, and "
             "the attempt-1 pass/fail verdict itself flipped on **1** "
             "annual-report and **3** concall cases. The likely cause is "
             "continuous batching and non-deterministic reduction order across "
             "the two T4s, not the sampling settings.\n"
             ">\n"
             "> **Consequence: at n=20, a difference of ±1–3 cases between runs "
             "is inside this observed range and should not be read as a confirmed "
             "improvement or regression on its own.** A properly measured noise "
             "floor (3-5x repeat, never yet run) could show a tighter or wider "
             "range than this — treat ±1-3 as a lower bound on the uncertainty, "
             "not a precise figure. Larger deltas (roughly 5+ cases) are "
             "unlikely to be pure noise. This applies to every before/after "
             "number in this index.\n"
             ">\n"
             "> **Session documents, in the order the work happened:** "
             "`ACTIONS_1_3_FULL_RESULTS.md` (the noise-floor correction above), "
             "`MINISTRAL_EVAL.md` (head-to-head vs Ministral 3 14B, shelved), "
             "`CONCALL_MARKDOWN_FAIRNESS.md` (one-line markdown ban, both "
             "models), `CONCALL_AND_REDFLAG_TUNING.md` (retry-budget 20/20 for "
             "concall; red_flag instance-check — net regression, not adopted).\n")

    L.append("## What ran\n")
    L.append("| Category | Model | Cases | Generated | Compliance fails | "
             "Guided / repaired | Sheet |")
    L.append("|---|---|---|---|---|---|---|")
    for key, (path, run) in sorted(runs.items()):
        task = run.get("task")
        s = run.get("summary") or {}
        # Forward slashes: markdown links must not carry Windows separators,
        # and these sheets are read on GitHub as often as locally.
        md = os.path.relpath(path.replace(".json", ".md"),
                             os.path.dirname(args.out) or ".").replace(os.sep, "/")
        L.append(f"| {TASK_LABEL.get(task, task)} | `{run.get('model')}` | {s.get('cases')} | "
                 f"{s.get('generated_ok')} | {s.get('candidate_compliance_failures')} | "
                 f"{s.get('guided_and_clean', '—')} / {s.get('json_repair_used', '—')} | "
                 f"[{os.path.basename(md)}]({md}) |")
    L.append("")

    # Per-category objective roll-up + reading order
    for key, (path, run) in sorted(runs.items()):
        task = run.get("task")
        s = run.get("summary") or {}
        # Model in the heading: two models now share every task heading, and
        # an unlabelled section would read as the category's only result.
        L.append(f"## {TASK_LABEL.get(task, task)} — `{run.get('model')}`\n")

        if task == "annual_report_summary":
            src = run.get("reference_source")
            if src:
                L.append("> ✅ **Reference regenerated — the comparison is now "
                         f"schema-matched.** Production holds no current-schema "
                         f"annual-report output, so the reference was regenerated "
                         f"with `{src.get('model')}` on the CURRENT prompt from the "
                         f"SAME evidence block Qwen received, under production retry "
                         f"mechanics (cost ${src.get('cost_usd_actual')}). Both sides "
                         "now differ only by model. The reference is a REPLAY, not "
                         "the text production actually stored — production stored "
                         "nothing in this schema.\n")
            else:
                L.append("> ⚠️ **Known caveat — the comparison is NOT like-for-like.** "
                         "Production holds no current-schema gpt-4o-mini annual-report "
                         "output: all 72 stored summaries are legacy-schema, written "
                         "2026-08-16, and 0 documents carry `evidence_tokens`. So the "
                         "reference differs from this replay in BOTH input and output "
                         "schema. Judge Qwen's output on its own merits against the "
                         "evidence; do not read the side-by-side as a score. See "
                         "`deployment/kaggle/ANNUAL_REPORT_REFERENCE_SCHEMA.md`.\n")

        rp = run.get("retry_policy")
        if rp and not rp.get("like_for_like_with_reference"):
            L.append(f"> ⚠️ **Retry policy `{rp.get('name')}` — NOT like-for-like.** "
                     "gpt-4o-mini was measured under production retry mechanics "
                     "(every attempt deterministic, descriptive corrective note). "
                     "This run varied sampling on retries and sent a directive note. "
                     "The fair remedy, if this is what closes the gap, is adopting "
                     "it in RedixFi for both models — not treating it as a "
                     "Qwen-only crutch.\n")

        cfg = run.get("model_config") or {}
        L.append(f"- Model: `{run.get('model')}` "
                 f"(ctx {cfg.get('max_model_len')}, {cfg.get('quantization')}, "
                 f"TP={cfg.get('tensor_parallel_size')})")
        L.append(f"- Run id: `{run.get('run_id')}`")
        for key in ("cases", "generated_ok", "generation_failures",
                    "candidate_compliance_failures", "reference_compliance_failures",
                    "guided_and_clean", "json_repair_used",
                    "tone_label_agreement_rate", "agreement_rate", "outcomes"):
            if key in s:
                L.append(f"- {key}: **{s[key]}**")
        L.append("")

        dis = _disagreements(task, run)
        L.append(f"### Read these first — {len(dis)} case(s) where the models "
                 f"differ or a check failed\n")
        if not dis:
            L.append("_None. Qwen matched gpt-4o-mini on every objective signal "
                     "in this category. That is not the same as matching on "
                     "quality — the sheets still need reading._\n")
        else:
            L.append("| Case | What differs |")
            L.append("|---|---|")
            for bid, why in dis:
                L.append(f"| `{bid}` | {why} |")
            L.append("")

    # Prompt-variant runs, reported BESIDE the baseline, never instead of it.
    if variant_runs:
        L.append("## Prompt-variant runs (full fixture)\n")
        L.append("> These use a NON-PRODUCTION system prompt. The reference model "
                 "achieved its result on the production prompt, so a variant number "
                 "is not a like-for-like comparison against it — it shows what the "
                 "candidate model needs to get there, or (for a fairness test run "
                 "identically on two candidate models) how they compare to EACH "
                 "OTHER under the same added instruction. Read it against the "
                 "baseline row for the same model above, not against the reference.\n")
        L.append("| Variant | Model | Task | Cases | Generated | Compliance fails | "
                 "Tone agreement | Outcome breakdown | Sheet |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for key, (path, run) in sorted(variant_runs.items()):
            s = run.get("summary") or {}
            v = run.get("variant") or {}
            md = os.path.relpath(path.replace(".json", ".md"),
                                 os.path.dirname(args.out) or ".").replace(os.sep, "/")
            outcomes = s.get("outcomes")
            outcome_str = (", ".join(f"{k}={v}" for k, v in outcomes.items())
                          if outcomes else "—")
            L.append(f"| `{v.get('name')}` | `{run.get('model')}` | "
                     f"{TASK_LABEL.get(run.get('task'), run.get('task'))} | "
                     f"{s.get('cases')} | {s.get('generated_ok')} | "
                     f"{s.get('candidate_compliance_failures')} | "
                     f"{s.get('tone_label_agreement_rate', '—')} | "
                     f"{outcome_str} | "
                     f"[{os.path.basename(md)}]({md}) |")
        L.append("")
        seen_desc = set()
        for key, (path, run) in sorted(variant_runs.items()):
            v = run.get("variant") or {}
            name = v.get("name")
            if name not in seen_desc:
                seen_desc.add(name)
                # red_flag variants have no retry concept (single-shot task);
                # only render attempts/policy when the variant actually has them.
                cfg_bits = []
                if v.get("max_attempts") is not None:
                    cfg_bits.append(f"attempts {v.get('max_attempts')}")
                if v.get("retry_policy") is not None:
                    cfg_bits.append(f"retry policy `{v.get('retry_policy')}`")
                cfg = f" ({', '.join(cfg_bits)})" if cfg_bits else ""
                L.append(f"- **`{name}`**{cfg}: {v.get('description')}")
        L.append("")

    # Concall experiments, if present
    exp_paths = sorted(glob.glob("evaluation/concall/runs/concall_experiments__*.json"))
    if exp_paths:
        exp = json.load(open(exp_paths[-1], encoding="utf-8"))
        L.append("## Concall fix experiments\n")
        L.append(f"Repair targets: {exp.get('targets')}\n")
        L.append("| Variant | Attempts budget | Repaired |")
        L.append("|---|---|---|")
        for name, v in (exp.get("variants") or {}).items():
            L.append(f"| `{name}` | {v.get('attempts_budget')} | "
                     f"{v.get('passed')}/{v.get('of')} |")
        L.append("")
        L.append("> A variant that passes on a **different prompt** or a **larger "
                 "retry budget** has not matched gpt-4o-mini like-for-like — "
                 "gpt-4o-mini achieved its result on the production prompt at 3 "
                 "attempts. If the few-shot variant closes the gap, the fair "
                 "remedy is adopting that prompt in RedixFi for both models, not "
                 "keeping it as a Qwen-only crutch.\n")

    L.append("## How to review\n")
    L.append("1. Start with the *Read these first* lists above — that is where "
             "the two models actually diverge.\n"
             "2. Open the per-category sheet and fill in the HUMAN REVIEW NOTES "
             "table for those cases.\n"
             "3. Then sample a handful of agreeing cases, to check that agreement "
             "reflects genuine quality rather than both models being vague.\n"
             "4. Record a verdict per category. A small sample cannot establish "
             "production-readiness however good the output looks.\n")

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    print(f"wrote {args.out}  ({len(runs)} categories)")


if __name__ == "__main__":
    main()
