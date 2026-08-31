#!/usr/bin/env python3
"""Build Phase 2-4 retest comparison records.

BEFORE = the real outputs from the previous 72/100/100 run.
AFTER  = the small controlled retest kernel outputs (evaluation/fix_validation/retest_outputs).
References come from the tiny retest fixtures.

No scoring; records are for human review.
"""
from __future__ import annotations

import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "evaluation", "fix_validation")
AFTER_DIR = os.path.join(OUT_DIR, "retest_outputs")
BEFORE_DIR = os.path.join(ROOT, "evaluation", "comparison", "_outputs")
FIXTURES = os.path.join(ROOT, "fixtures")

SPECS = [
    {
        "phase": 2,
        "category": "annual_report",
        "fix_tested": "shared_retry_improved_policy",
        "fixture": "retest_ar_3.json",
        "before": "output_annual_report_summary.json",
        "after": "output_annual_report_summary.json",
        "task": "annual_report_summary",
    },
    {
        "phase": "2+3",
        "category": "concall",
        "fix_tested": "shared_retry+content_selection",
        "fixture": "retest_cc_3.json",
        "before": "output_concall_summary.json",
        "after": "output_concall_summary.json",
        "task": "concall_summary",
    },
    {
        "phase": 4,
        "category": "red_flag",
        "fix_tested": "disclosure_vs_material_red_flag",
        "fixture": "retest_rf_5.json",
        "before": "output_red_flag.json",
        "after": "output_red_flag.json",
        "task": "red_flag",
    },
]


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = []
    for spec in SPECS:
        fixture = load(os.path.join(FIXTURES, spec["fixture"]))
        before_doc = load(os.path.join(BEFORE_DIR, spec["before"]))
        before_map = {r.get("case_id"): r for r in before_doc.get("results", [])}
        after_path = os.path.join(AFTER_DIR, spec["after"])
        after_doc = load(after_path) if os.path.exists(after_path) else {"results": []}
        after_map = {r.get("case_id"): r for r in after_doc.get("results", [])}

        for case in fixture["cases"]:
            cid = case.get("benchmark_id") or case.get("fixture_id") or case.get("chunk_id")
            symbol = case.get("symbol")
            ref = case.get("reference")
            b = before_map.get(cid) or {}
            a = after_map.get(cid) or {}
            before_out = b.get("output") or {}
            after_out = a.get("output") or {}
            before_ok = bool(b.get("ok")) and bool(before_out)
            after_ok = bool(a.get("ok")) and bool(after_out)

            if spec["category"] == "red_flag":
                ref_type = (ref or {}).get("risk_flag_type")
                after_type = after_out.get("risk_flag_type")
                before_type = before_out.get("risk_flag_type")
                # Phase 4 target: KAM/boilerplate should not be flagged.
                if ref_type is None:
                    result = "PASS" if after_type is None else "FAIL"
                else:
                    result = "PASS" if after_type == ref_type else "INCONCLUSIVE"
                validation_before = f"type={before_type}"
                validation_after = f"type={after_type}"
            else:
                result = "PASS" if after_ok else "FAIL"
                validation_before = "ok" if before_ok else f"failed:{b.get('error')}"
                validation_after = "ok" if after_ok else f"failed:{a.get('error')}"

            rows.append({
                "phase": spec["phase"],
                "category": spec["category"],
                "symbol": symbol,
                "case_id": cid,
                "fix_tested": spec["fix_tested"],
                "gpt4o_mini_output": json.dumps(ref, ensure_ascii=False, default=str) if ref else "GPT4O_MINI_REFERENCE_MISSING",
                "qwen_before": json.dumps(before_out, ensure_ascii=False, default=str),
                "qwen_after": json.dumps(after_out, ensure_ascii=False, default=str),
                "validation_before": validation_before,
                "validation_after": validation_after,
                "retry_attempts": a.get("attempts", ""),
                "result": result,
            })

    path = os.path.join(OUT_DIR, "phase234_records.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {path} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
