#!/usr/bin/env python3
"""Build the small, DIVERSE 15-case subset for the first GPU run.

Why a pre-built subset rather than `--limit 3`
----------------------------------------------
`--limit` takes the first N cases, which on a sorted fixture means three
adjacent symbols and (for red_flag) three cases from the same stratum. That
would waste the run. This picks for coverage instead, deterministically, so
the same 15 cases come back on a re-run and results stay comparable.

Selection, per the approved split (~15 cases):
  annual_report   3  distinct symbols, spread across evidence size
  concall         3  one per tone_label present, doc_kind varied
  red_flag        6  one per positive category (4) + 2 negatives
  ask_ai          3  distinct symbols, varied answer length

Writes to fixtures/sample15/. Nothing is generated or scored here — this
only subsets the already-exported production fixtures.
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.evaluation.fixtures import build_document, load, save  # noqa: E402

SRC = {
    "annual_report_summary": "fixtures/annual_report_benchmark.json",
    "concall_summary": "fixtures/concall_benchmark.json",
    "red_flag": "fixtures/red_flag_benchmark.json",
    "ask_ai": "fixtures/ask_ai_benchmark.json",
}
OUT_NAME = {
    "annual_report_summary": "annual_report_sample15.json",
    "concall_summary": "concall_sample15.json",
    "red_flag": "red_flag_sample15.json",
    "ask_ai": "ask_ai_sample15.json",
}


def pick_annual_report(cases, n=3):
    """Distinct symbols, spread across evidence size (small/median/large) so
    a context or truncation problem shows up on the first run."""
    ranked = sorted(cases, key=lambda c: c["evidence_stats"]["evidence_tokens"])
    picks, seen = [], set()
    for idx in (0, len(ranked) // 2, len(ranked) - 1):
        for c in ranked[idx:] + ranked[:idx]:
            if c["symbol"] not in seen:
                picks.append(c)
                seen.add(c["symbol"])
                break
        if len(picks) == n:
            break
    return picks[:n]


def pick_concall(cases, n=3):
    """One per tone_label present — tone_label is the only closed-set,
    objectively-scorable field in any summarization phase, so the first run
    must exercise more than one value of it."""
    by_tone = {}
    for c in cases:
        by_tone.setdefault(c["reference"]["tone_label"], []).append(c)
    picks = []
    # Prefer an earnings transcript over a presentation where both exist.
    for tone in sorted(by_tone):
        pool = sorted(by_tone[tone],
                      key=lambda c: (c["doc_kind"] != "earnings concall transcript",
                                     c["benchmark_id"]))
        picks.append(pool[0])
    return picks[:n]


def pick_red_flag(cases, n_pos_per_cat=1, n_neg=2):
    """One per positive category plus negatives. The negatives matter most:
    they are the chunks that tripped the keyword prefilter and were then
    LLM-REJECTED, so they are the false-positive-resistance test."""
    by_cat, negatives = {}, []
    for c in cases:
        cat = c["reference"]["risk_flag_type"]
        if cat:
            by_cat.setdefault(cat, []).append(c)
        else:
            negatives.append(c)
    picks = []
    for cat in sorted(by_cat):
        picks.extend(sorted(by_cat[cat], key=lambda c: c["benchmark_id"])[:n_pos_per_cat])
    # Spread the negatives across different symbols where possible.
    seen = set()
    for c in sorted(negatives, key=lambda c: c["benchmark_id"]):
        if len([p for p in picks if p["case_polarity"] == "negative"]) >= n_neg:
            break
        if c["symbol"] in seen:
            continue
        seen.add(c["symbol"])
        picks.append(c)
    return picks


def pick_ask_ai(cases, n=3):
    """Distinct symbols, and spread across reference answer length so both a
    terse and a detailed reference are exercised."""
    ranked = sorted(cases, key=lambda c: len(c["reference"]["answer"]))
    picks, seen = [], set()
    for idx in (0, len(ranked) // 2, len(ranked) - 1):
        for c in ranked[idx:] + ranked[:idx]:
            if c["symbol"] not in seen:
                picks.append(c)
                seen.add(c["symbol"])
                break
        if len(picks) == n:
            break
    return picks[:n]


PICKERS = {
    "annual_report_summary": pick_annual_report,
    "concall_summary": pick_concall,
    "red_flag": pick_red_flag,
    "ask_ai": pick_ask_ai,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the 15-case first-run subset")
    parser.add_argument("--out-dir", default="fixtures/sample15")
    args = parser.parse_args()

    now = datetime.now(timezone.utc).isoformat()
    total = 0
    print("=" * 70)
    print("FIRST-RUN SUBSET — diverse, deterministic, ~15 cases")
    print("=" * 70)

    for task, src in SRC.items():
        fs = load(src)
        picks = PICKERS[task](fs.cases)
        total += len(picks)

        source = dict(fs.source)
        source.update({
            "subset_of": os.path.basename(src),
            "subset_reason": "first GPU run — small, diverse sample",
            "parent_case_count": len(fs.cases),
            "selection": PICKERS[task].__doc__.strip().split("\n")[0],
        })
        doc = build_document(task, picks, source, now)
        out = os.path.join(args.out_dir, OUT_NAME[task])
        save(doc, out)

        print(f"\n{task}  ->  {len(picks)} of {len(fs.cases)}")
        for c in picks:
            extra = ""
            if task == "concall_summary":
                extra = f"tone={c['reference']['tone_label']} kind={c['doc_kind'][:20]}"
            elif task == "red_flag":
                extra = f"{c['case_polarity']}/{c['reference']['risk_flag_type'] or 'none'}"
            elif task == "annual_report_summary":
                extra = f"evidence_tokens={c['evidence_stats']['evidence_tokens']}"
            elif task == "ask_ai":
                extra = f"ref_chars={len(c['reference']['answer'])}"
            print(f"    {c['benchmark_id'][:52]:<52} {extra}")
        print(f"  wrote {out}")

    print(f"\nTOTAL: {total} cases across 4 benchmarks")


if __name__ == "__main__":
    main()
