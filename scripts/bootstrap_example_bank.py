#!/usr/bin/env python3
"""Seed (or backfill) the example bank from an existing run's REAL
validated (`ok=True`) outputs.

WHY THIS EXISTS
---------------
The example bank (`app/example_bank.py`) is meant to accumulate
automatically going forward — see `app/evaluation/runner.py`'s call to
`example_bank.record_result()`. But that only starts capturing from the
NEXT run onward. This script backfills from a run that already happened,
so the bank isn't starting from zero the first time it's used.

It reads a saved run JSON (the same files under `evaluation/*/runs/`) and
records every case where `result["ok"] is True` — the SAME gate the live
runner applies, so a backfilled entry is indistinguishable from one
recorded live.

    python scripts/bootstrap_example_bank.py \
        --run evaluation/concall/runs/concall_summary__retries_extended__qwen3-14b-awq-tp2__20260830T041530Z.json \
        --task concall_summary
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import example_bank  # noqa: E402
from app.evaluation import fixtures as fx  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, help="path to a saved run JSON")
    ap.add_argument("--task", required=True,
                    choices=("concall_summary", "annual_report_summary", "red_flag"))
    ap.add_argument("--fixture",
                    help="path to the source fixture (needed for the fields "
                         "retrieval_text_for() reads — the run JSON's own "
                         "case_meta is a subset). Defaults inferred from "
                         "fixtures/<task-family>_benchmark.json")
    args = ap.parse_args()

    run = json.load(open(args.run, encoding="utf-8"))
    fixture_path = args.fixture
    if not fixture_path:
        family = {"concall_summary": "concall", "annual_report_summary": "annual_report",
                  "red_flag": "red_flag"}[args.task]
        fixture_path = f"fixtures/{family}_benchmark.json"
    fs = fx.load(fixture_path)
    by_id = {c.get("benchmark_id") or c.get("fixture_id"): c for c in fs.cases}

    recorded = skipped = 0
    for row in run.get("results") or []:
        if not row.get("ok"):
            skipped += 1
            continue
        bid = (row.get("case_meta") or {}).get("benchmark_id") or row.get("fixture_id")
        fixture = by_id.get(bid)
        if fixture is None:
            print(f"  SKIP {bid}: not found in {fixture_path}")
            skipped += 1
            continue
        example_bank.record_result(
            args.task, fixture, row.get("output") or {},
            attempts_used=row.get("attempts") or 1,
            model=run.get("model", "?"),
            run_id=run.get("run_id", "?"),
        )
        recorded += 1

    bank = example_bank.load_bank(args.task)
    print(f"recorded {recorded} entries ({skipped} skipped — not ok, or fixture not found)")
    print(f"bank now holds {len(bank)} entries for {args.task} "
         f"at {example_bank._bank_path(args.task)}")
    hard = sum(1 for e in bank if e.get("was_hard_case"))
    print(f"  of which {hard} are flagged as hard cases (needed >1 attempt)")


if __name__ == "__main__":
    main()
