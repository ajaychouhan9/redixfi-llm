#!/usr/bin/env python3
"""Build the human-review CSV for the GPT-4o-mini rephrase layer tests."""
from __future__ import annotations

import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "evaluation", "fix_validation")
RESULTS = os.path.join(OUT_DIR, "rephrase_retest_outputs", "rephrase_targeted_results.json")
FIXTURES = os.path.join(ROOT, "fixtures")


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main() -> None:
    rows = load(RESULTS)
    refs = {}
    for fixture_name in ("retest_ar_3.json", "retest_cc_3.json"):
        doc = load(os.path.join(FIXTURES, fixture_name))
        for case in doc["cases"]:
            refs[case["benchmark_id"]] = case.get("reference")

    out_path = os.path.join(OUT_DIR, "rephrase_records.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=[
            "category", "symbol", "case_id",
            "gpt4o_mini_original_reference",
            "qwen_output",
            "validator_finding",
            "gpt4o_mini_rephrased_output",
            "final_output",
            "rephrase_used",
            "validator_before",
            "validator_after",
            "information_preservation_check",
            "final_status",
            "human_review_required",
            "human_review_reason",
            "gpt_input_tokens",
            "gpt_output_tokens",
            "result",
        ])
        writer.writeheader()
        for r in rows:
            cid = r["case_id"]
            writer.writerow({
                "category": r["category"],
                "symbol": r["symbol"],
                "case_id": cid,
                "gpt4o_mini_original_reference": json.dumps(refs.get(cid), ensure_ascii=False, default=str) if refs.get(cid) else "MISSING",
                "qwen_output": json.dumps(r["qwen_output"], ensure_ascii=False, default=str),
                "validator_finding": json.dumps(r["validator_finding"], ensure_ascii=False, default=str),
                "gpt4o_mini_rephrased_output": json.dumps(r["gpt_rephrased_output"], ensure_ascii=False, default=str),
                "final_output": json.dumps(r["final_output"], ensure_ascii=False, default=str),
                "rephrase_used": r["gpt_rephrase_called"],
                "validator_before": json.dumps(r["validator_finding"], ensure_ascii=False, default=str),
                "validator_after": r["validator_after"] or "",
                "information_preservation_check": json.dumps(r.get("information_preservation_check"), ensure_ascii=False, default=str),
                "final_status": r.get("final_status", ""),
                "human_review_required": r.get("human_review_required", False),
                "human_review_reason": r.get("human_review_reason") or "",
                "gpt_input_tokens": r["gpt_input_tokens"],
                "gpt_output_tokens": r["gpt_output_tokens"],
                "result": r["result"],
            })
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
