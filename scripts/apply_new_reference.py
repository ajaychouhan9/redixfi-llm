#!/usr/bin/env python3
"""Swap in the regenerated reference and re-score an existing run — ACTION 1.

The annual-report run compared Qwen against a LEGACY-schema reference
produced from different input, so the sheet carried a caveat banner
instead of a verdict. `scripts/regenerate_annual_report_reference.py` has
now produced current-schema gpt-4o-mini output for the same 20 cases.

This replaces ONLY the reference side of an existing run and recomputes
the comparison. Qwen's generations are copied through untouched — no GPU
is spent and no candidate output changes, so the candidate column of the
re-rendered sheet is byte-identical to the one already reviewed.

    python scripts/apply_new_reference.py --run <run.json> \
        --reference fixtures/annual_report_reference_gpt4omini.json
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.evaluation import compare as compare_mod   # noqa: E402
from app.evaluation import report as report_mod     # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", help="run JSON to re-score; default = newest "
                                  "annual_report_summary run")
    ap.add_argument("--reference",
                    default="fixtures/annual_report_reference_gpt4omini.json")
    ap.add_argument("--suffix", default="__refreshed_reference")
    args = ap.parse_args()

    run_path = args.run
    if not run_path:
        # Pick by run_id, NOT by filename: "…awq__" and "…awq-tp2__" do not
        # sort in run order. Echo runs are offline stubs with no real model
        # output and must never be mistaken for a measured run.
        best = None
        for path in glob.glob("evaluation/*/runs/annual_report_summary__*.json"):
            if args.suffix in path:
                continue
            try:
                r = json.load(open(path, encoding="utf-8"))
            except Exception:
                continue
            if r.get("backend") == "echo" or len(r.get("results") or []) < 5:
                continue
            if best is None or r.get("run_id", "") > best[1]:
                best = (path, r.get("run_id", ""))
        if best is None:
            sys.exit("no real annual_report_summary run found")
        run_path = best[0]

    run = json.load(open(run_path, encoding="utf-8"))
    ref_doc = json.load(open(args.reference, encoding="utf-8"))
    refs = {r["fixture_id"]: r["reference"]
            for r in ref_doc["results"] if r.get("ok") and r.get("reference")}

    print(f"run       : {run_path}")
    print(f"reference : {args.reference}  ({len(refs)} usable)")
    print(f"task      : {run.get('task')}\n")

    swapped = missing = 0
    for row in run.get("results") or []:
        fid = row.get("fixture_id") or (row.get("case_meta") or {}).get("benchmark_id")
        new_ref = refs.get(fid)
        if not new_ref:
            missing += 1
            print(f"  MISSING reference for {fid}")
            continue
        row["reference"] = new_ref
        # Re-score against the new reference. The candidate is untouched.
        row["comparison"] = compare_mod.compare(
            run["task"], {"reference": new_ref}, row.get("output") or {})
        swapped += 1

    run["summary"] = compare_mod.aggregate(run["task"], run["results"])
    run["reference_source"] = {
        "replaced_at": ref_doc.get("generated_at"),
        "model": ref_doc.get("model"),
        "file": os.path.basename(args.reference),
        "schema": ref_doc.get("schema"),
        "retry_policy": ref_doc.get("retry_policy"),
        "cost_usd_actual": ref_doc.get("cost_usd_actual"),
        "note": ("Reference REGENERATED for this benchmark, not read from "
                 "production: production holds no current-schema annual-report "
                 "output. Candidate generations are unchanged from the original "
                 "run — only the reference side was replaced."),
    }

    out_path = run_path.replace(".json", f"{args.suffix}.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(run, fh, ensure_ascii=False, indent=2, default=str)
    report_mod.save(run, out_path.replace(".json", ".md"),
                    max_cases=len(run["results"]))

    s = run["summary"]
    print(f"swapped {swapped} reference(s); {missing} missing\n")
    print("re-scored summary:")
    for k in ("cases", "generated_ok", "candidate_compliance_failures",
              "reference_compliance_failures", "mean_lexical_overlap"):
        if k in s:
            print(f"  {k}: {s[k]}")
    print(f"\nwrote {out_path}")
    print(f"wrote {out_path.replace('.json', '.md')}")


if __name__ == "__main__":
    main()
