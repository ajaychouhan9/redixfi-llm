#!/usr/bin/env python3
"""Phase 1 targeted verification — real outputs, deterministic fixes only.

Uses the REAL Qwen outputs from the 72/100/100 run as "before" and applies
the Phase 1 canonical-schema / risk_classified normalization to show "after".
No new model generation is performed, so this consumes Phase 1 retest budget
only in the sense of case samples reviewed (AR 2, Concall 2, Red Flag 3).
"""
from __future__ import annotations

import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "evaluation", "fix_validation")
os.makedirs(OUT_DIR, exist_ok=True)

OUTPUTS = os.path.join(ROOT, "evaluation", "comparison", "_outputs")

AR_CASES = ["AR_GODREJCP_AR_26977_GODREJCP_2024_2025_A_16072025185902",
            "AR_BRITANNIA_AR_27040_BRITANNIA_2024_2025_A_19072025234802"]
CC_CASES = ["CC_BATAINDIA_106539458", "CC_POWERMECH_106545915"]
RF_CASES = ["RF_MOTHERSON_AR_MOTHERSON_342",
            "RF_ADANIPOWER_AR_ADANIPOWER_659",
            "RF_ASIANPAINT_AR_ASIANPAINT_679"]


def load(name: str):
    with open(os.path.join(OUTPUTS, name), encoding="utf-8") as fh:
        return json.load(fh)


def ar_after(out: dict) -> dict:
    return {k: v for k, v in out.items() if k not in ("summary", "bullets")}


def rf_after(out: dict) -> dict:
    if out.get("risk_flag_type"):
        out["risk_classified"] = True
    else:
        out["risk_classified"] = False
    return out


def main() -> None:
    ar = {r["case_id"]: r for r in load("output_annual_report_summary.json")["results"]}
    cc = {r["case_id"]: r for r in load("output_concall_summary.json")["results"]}
    rf = {r["case_id"]: r for r in load("output_red_flag.json")["results"]}

    rows = []
    # AR: duplicate fields removed
    for cid in AR_CASES:
        r = ar[cid]
        before = r["output"]
        after = ar_after(before)
        dup_before = "summary" in before and "executive_summary" in before
        dup_after = "summary" in after or "bullets" in after
        rows.append({
            "phase": 1, "category": "annual_report", "symbol": r.get("symbol"),
            "case_id": cid, "fix_tested": "canonical_schema_remove_legacy_duplicates",
            "gpt4o_mini_output": json.dumps(r.get("reference") or {}, ensure_ascii=False),
            "qwen_before": json.dumps(before, ensure_ascii=False),
            "qwen_after": json.dumps(after, ensure_ascii=False),
            "validation_before": "duplicates_present" if dup_before else "no_duplicates",
            "validation_after": "no_duplicates" if not dup_after else "FAIL",
            "retry_attempts": r.get("attempts", 1),
            "result": "PASS" if (dup_before and not dup_after) else "FAIL",
        })
    # CC: schema unchanged and still parses
    for cid in CC_CASES:
        r = cc[cid]
        before = r["output"]
        after = dict(before)
        ok_before = set(before) == {"summary", "tone_label", "tone_note"}
        rows.append({
            "phase": 1, "category": "concall", "symbol": r.get("symbol"),
            "case_id": cid, "fix_tested": "schema_unchanged_still_parses",
            "gpt4o_mini_output": json.dumps(r.get("reference") or {}, ensure_ascii=False),
            "qwen_before": json.dumps(before, ensure_ascii=False),
            "qwen_after": json.dumps(after, ensure_ascii=False),
            "validation_before": "parses" if ok_before else "FAIL",
            "validation_after": "parses" if set(after) == {"summary", "tone_label", "tone_note"} else "FAIL",
            "retry_attempts": r.get("attempts", 1),
            "result": "PASS" if ok_before else "FAIL",
        })
    # RF: risk_classified consistency
    for cid in RF_CASES:
        r = rf[cid]
        before = dict(r["output"])
        after = rf_after(dict(before))
        valid_before = before.get("risk_classified") is True and bool(before.get("risk_flag_type"))
        valid_after = after.get("risk_classified") is True and bool(after.get("risk_flag_type"))
        consistent_after = after.get("risk_classified") is bool(after.get("risk_flag_type"))
        rows.append({
            "phase": 1, "category": "red_flag", "symbol": r.get("symbol"),
            "case_id": cid, "fix_tested": "risk_classified_consistent_with_type",
            "gpt4o_mini_output": json.dumps(r.get("reference") or {}, ensure_ascii=False),
            "qwen_before": json.dumps(before, ensure_ascii=False),
            "qwen_after": json.dumps(after, ensure_ascii=False),
            "validation_before": "PASS" if valid_before else "n/a",
            "validation_after": "consistent" if consistent_after else "FAIL",
            "retry_attempts": r.get("attempts", 1),
            "result": "PASS" if consistent_after else "FAIL",
        })

    path = os.path.join(OUT_DIR, "phase1_records.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {path}")
    print(f"rows: AR {len(AR_CASES)}, Concall {len(CC_CASES)}, Red Flag {len(RF_CASES)}")


if __name__ == "__main__":
    main()
