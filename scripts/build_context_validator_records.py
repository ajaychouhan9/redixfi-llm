#!/usr/bin/env python3
"""Build context/validator retest comparison records.

BEFORE = Phase 2-4 retest outputs (after Phase 1-4, before this task).
AFTER  = the context/validator retest kernel outputs.
References come from the tiny retest fixtures.
"""
from __future__ import annotations

import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "evaluation", "fix_validation")
AFTER_DIR = os.path.join(OUT_DIR, "context_validator_outputs")
BEFORE_DIR = os.path.join(OUT_DIR, "retest_outputs")
FIXTURES = os.path.join(ROOT, "fixtures")

TARGETS = {
    "annual_report": ["AR_COALINDIA_AR_27257_COALINDIA_2024_2025_A_04082025110141"],
    "concall": ["CC_BAJFINANCE_106604310", "CC_APLLTD_106633638"],
}


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = []
    for category, cids in TARGETS.items():
        fixture_name = {"annual_report": "retest_ar_3.json",
                        "concall": "retest_cc_3.json"}[category]
        before_name = {"annual_report": "output_annual_report_summary.json",
                       "concall": "output_concall_summary.json"}[category]
        after_name = before_name
        fixture = load(os.path.join(FIXTURES, fixture_name))
        before_map = {r.get("case_id"): r for r in load(os.path.join(BEFORE_DIR, before_name)).get("results", [])}
        after_path = os.path.join(AFTER_DIR, after_name)
        after_map = {r.get("case_id"): r for r in load(after_path).get("results", [])} if os.path.exists(after_path) else {}

        for case in fixture["cases"]:
            cid = case.get("benchmark_id")
            if cid not in cids:
                continue
            symbol = case.get("symbol")
            ref = case.get("reference")
            b = before_map.get(cid) or {}
            a = after_map.get(cid) or {}
            problem = "context_overflow" if cid.startswith("CC_BAJFINANCE") else "forward_looking_validator"
            before_out = b.get("output") or {}
            after_out = a.get("output") or {}
            before_ok = bool(b.get("ok")) and bool(before_out)
            after_ok = bool(a.get("ok")) and bool(after_out)

            if problem == "context_overflow":
                clog = a.get("context_log") or {}
                result = "PASS" if clog.get("generation_allowed") is True else "FAIL"
                notes = json.dumps(clog, ensure_ascii=False)
            else:
                result = "PASS" if after_ok else "FAIL"
                notes = f"before_ok={before_ok} after_ok={after_ok}"

            rows.append({
                "category": category,
                "symbol": symbol,
                "case_id": cid,
                "problem_tested": problem,
                "GPT-4o-mini_reference": json.dumps(ref, ensure_ascii=False, default=str) if ref else "MISSING",
                "Qwen_before": json.dumps(before_out, ensure_ascii=False, default=str),
                "Qwen_after": json.dumps(after_out, ensure_ascii=False, default=str),
                "original_prompt_tokens": (a.get("context_log") or {}).get("original_input_tokens", ""),
                "final_prompt_tokens": (a.get("context_log") or {}).get("final_prompt_tokens", ""),
                "context_limit": (a.get("context_log") or {}).get("context_limit", ""),
                "retry_attempts": a.get("attempts", ""),
                "temperatures": json.dumps([r.get("sampling", {}).get("temperature") for r in (a.get("rejections") or [])], ensure_ascii=False),
                "seeds": json.dumps([r.get("sampling", {}).get("seed") for r in (a.get("rejections") or [])], ensure_ascii=False),
                "validation_failures": json.dumps([r.get("reason") for r in (a.get("rejections") or [])], ensure_ascii=False),
                "corrective_notes": json.dumps([r.get("next_corrective_note") for r in (a.get("rejections") or [])], ensure_ascii=False),
                "result": result,
                "notes": notes,
            })

    path = os.path.join(OUT_DIR, "context_validator_records.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {path} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
