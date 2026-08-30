#!/usr/bin/env python3
"""Build the three human-review comparison CSVs from fixtures + Qwen outputs.

Inputs (all defaulted to this project's normal layout):

  fixtures/  annual_report_72.json, concall_100.json, red_flag_100.json
  outputs/   output_annual_report_summary.json, output_concall_summary.json,
             output_red_flag.json

Outputs (evaluation/comparison/):

  ar_comparison_72.csv
  concall_comparison_100.csv
  red_flag_comparison_100.csv
  REDIXFI_LLM_COMPARISON.csv

Columns are exactly what the founder asked for — no quality score, no
truncation, no paraphrase. GPT-4o-mini reference and Qwen output are stored
as full JSON strings so structured outputs survive verbatim. A missing
reference is recorded as GPT4O_MINI_REFERENCE_MISSING; a failed Qwen
generation is recorded as QWEN_GENERATION_FAILED: <reason>.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SPECS = [
    {
        "category": "annual_report",
        "fixture": "annual_report_72.json",
        "output": "output_annual_report_summary.json",
        "csv": "ar_comparison_72.csv",
        "id_field": "benchmark_id",
    },
    {
        "category": "concall",
        "fixture": "concall_100.json",
        "output": "output_concall_summary.json",
        "csv": "concall_comparison_100.csv",
        "id_field": "benchmark_id",
    },
    {
        "category": "red_flag",
        "fixture": "red_flag_100.json",
        "output": "output_red_flag.json",
        "csv": "red_flag_comparison_100.csv",
        "id_field": "benchmark_id",
    },
]


def load_json(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def output_text(row) -> str:
    if not row:
        return "QWEN_GENERATION_FAILED: no output row in Qwen results"
    if row.get("ok"):
        payload = row.get("output") or {}
        return json.dumps(payload, ensure_ascii=False, default=str)
    reason = row.get("error") or row.get("rejections") or "unknown error"
    return f"QWEN_GENERATION_FAILED: {reason}"


def reference_text(case) -> str:
    ref = case.get("reference")
    if ref is None:
        return "GPT4O_MINI_REFERENCE_MISSING"
    return json.dumps(ref, ensure_ascii=False, default=str)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures-dir", default=os.path.join(ROOT, "fixtures"))
    ap.add_argument("--outputs-dir", default=os.path.join(ROOT, "evaluation", "comparison", "_outputs"))
    ap.add_argument("--out-dir", default=os.path.join(ROOT, "evaluation", "comparison"))
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    combined_path = os.path.join(args.out_dir, "REDIXFI_LLM_COMPARISON.csv")

    summary = []
    with open(combined_path, "w", newline="", encoding="utf-8") as combined_fh:
        combined = csv.writer(combined_fh)
        combined.writerow(["category", "symbol", "gpt4o_mini_output", "qwen_output"])

        for spec in SPECS:
            fixture_path = os.path.join(args.fixtures_dir, spec["fixture"])
            output_path = os.path.join(args.outputs_dir, spec["output"])
            csv_path = os.path.join(args.out_dir, spec["csv"])

            fixture = load_json(fixture_path)
            cases = fixture.get("cases", [])
            qwen_doc = load_json(output_path) if os.path.exists(output_path) else {"results": []}
            qwen_rows = {r.get("case_id"): r for r in qwen_doc.get("results", [])}

            missing_refs = 0
            qwen_failures = 0
            written = 0

            with open(csv_path, "w", newline="", encoding="utf-8") as fh:
                writer = csv.writer(fh)
                writer.writerow(["symbol", "gpt4o_mini_output", "qwen_output"])
                for case in cases:
                    cid = case.get(spec["id_field"]) or case.get("fixture_id") or case.get("chunk_id")
                    symbol = case.get("symbol") or "UNKNOWN"
                    gpt = reference_text(case)
                    if gpt == "GPT4O_MINI_REFERENCE_MISSING":
                        missing_refs += 1
                    q = output_text(qwen_rows.get(cid))
                    if q.startswith("QWEN_GENERATION_FAILED"):
                        qwen_failures += 1
                    writer.writerow([symbol, gpt, q])
                    combined.writerow([spec["category"], symbol, gpt, q])
                    written += 1

            summary.append({
                "category": spec["category"],
                "cases": written,
                "missing_gpt4o_mini_references": missing_refs,
                "qwen_failures": qwen_failures,
                "csv": csv_path,
            })
            print(f"{spec['csv']}: {written} rows, "
                  f"{missing_refs} missing GPT-4o-mini refs, {qwen_failures} Qwen failures")

    print(f"combined: {combined_path}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
