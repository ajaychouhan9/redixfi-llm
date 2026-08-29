#!/usr/bin/env python3
"""Re-render review sheets from saved run JSON — every case, no truncation.

WHY THIS EXISTS
---------------
`report_mod.save()` defaults to `max_cases=25`. That is fine for a 15-case
sample and quietly wrong for an expanded review run: a 60-case red-flag
sheet would show 25 cases and look complete. The launcher now passes the
full case count, but any run produced BEFORE that fix has a truncated
sheet on disk while its JSON still holds every case.

This regenerates the markdown from the JSON, so a truncated sheet can be
repaired without re-spending GPU time. It reads run artifacts only — it
never contacts a model, a database, or Kaggle.

    python scripts/regenerate_review_sheets.py                # all runs
    python scripts/regenerate_review_sheets.py --glob '...'   # a subset
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.evaluation import report as report_mod  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", default="evaluation/*/runs/*.json",
                    help="which run JSON files to re-render")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    paths = sorted(p for p in glob.glob(args.glob)
                   if not os.path.basename(p).startswith("concall_experiments"))
    if not paths:
        print(f"no run JSON matched {args.glob!r}")
        return

    print(f"{'file':<64}{'cases':>7}{'in sheet':>10}  action")
    rewritten = 0
    for path in paths:
        try:
            run = json.load(open(path, encoding="utf-8"))
        except Exception as exc:
            print(f"{os.path.basename(path)[:62]:<64}{'—':>7}{'—':>10}  SKIP ({exc})")
            continue
        results = run.get("results") or []
        md_path = path.replace(".json", ".md")

        shown_before = None
        if os.path.exists(md_path):
            text = open(md_path, encoding="utf-8").read()
            shown_before = text.count("\n### Case ")

        needs = shown_before is None or shown_before < len(results)
        action = "would rewrite" if (needs and args.dry_run) else (
            "REWROTE" if needs else "ok, complete")
        if needs and not args.dry_run:
            report_mod.save(run, md_path, max_cases=len(results))
            rewritten += 1
        print(f"{os.path.basename(path)[:62]:<64}{len(results):>7}"
              f"{str(shown_before):>10}  {action}")

    if not args.dry_run:
        print(f"\nrewrote {rewritten} sheet(s); every case now rendered.")


if __name__ == "__main__":
    main()
