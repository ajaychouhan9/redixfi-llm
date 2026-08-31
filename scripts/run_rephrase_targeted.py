#!/usr/bin/env python3
"""Targeted rephrase-layer test using REAL stored Qwen outputs (no Qwen GPU).

Cases:
  * AR COALINDIA   — first eligible validator failure from the Phase 2-4 retest
  * CC APLLTD      — first eligible validator failure from the Phase 2-4 retest
  * AR VEDL        — previously SUCCESSFUL Qwen output (control: no GPT call)

GPT-4o-mini is called only for the two failing cases. The source/transcript
is never sent (only the Qwen summary + validator finding + policy note).
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from app.experiments.concall_variants import retries_extended_variant, run_variant
from app.inference.base import GenerationRequest, GenerationResult
from app.tasks import annual_report_summary as task_ar
from app.tasks import concall_summary as task_cc
from app.tasks.rephrase import build_rephrase_backend


class StaticQwen:
    """Returns one pre-stored Qwen output (raw JSON string)."""

    name = "static-qwen"

    def __init__(self, output_dict):
        self.output_dict = output_dict

    def generate(self, request: GenerationRequest) -> GenerationResult:
        return GenerationResult(
            text=json.dumps(self.output_dict),
            model=request.model,
            backend=self.name,
            prompt_tokens=0,
            completion_tokens=0,
            total_tokens=0,
        )


def find_case(results, cid):
    for r in results:
        if r.get("case_id") == cid:
            return r
    return None


def first_failed_text(result):
    for rej in (result.get("rejections") or []):
        if isinstance(rej.get("text"), dict) and rej.get("text"):
            return rej["text"]
    return None


def main() -> None:
    out_dir = os.path.join(ROOT, "evaluation", "fix_validation", "rephrase_retest_outputs")
    os.makedirs(out_dir, exist_ok=True)

    ar_before = json.load(open(os.path.join(
        ROOT, "evaluation", "fix_validation", "retest_outputs",
        "output_annual_report_summary.json"), encoding="utf-8"))["results"]
    cc_before = json.load(open(os.path.join(
        ROOT, "evaluation", "fix_validation", "retest_outputs",
        "output_concall_summary.json"), encoding="utf-8"))["results"]

    ar_fixtures = json.load(open(os.path.join(
        ROOT, "fixtures", "retest_ar_3.json"), encoding="utf-8"))["cases"]
    cc_fixtures = json.load(open(os.path.join(
        ROOT, "fixtures", "retest_cc_3.json"), encoding="utf-8"))["cases"]

    ar_fix = {c["benchmark_id"]: c for c in ar_fixtures}
    cc_fix = {c["benchmark_id"]: c for c in cc_fixtures}

    gpt = build_rephrase_backend()
    records = []

    # --- AR COALINDIA -----------------------------------------------------
    coal = find_case(ar_before, "AR_COALINDIA_AR_27257_COALINDIA_2024_2025_A_04082025110141")
    qwen_text = first_failed_text(coal)
    fixture = ar_fix["AR_COALINDIA_AR_27257_COALINDIA_2024_2025_A_04082025110141"]
    r = task_ar.run(StaticQwen(qwen_text), fixture, "qwen3-14b-awq-tp2",
                    rephrase_backend=gpt)
    records.append({
        "category": "annual_report",
        "symbol": "COALINDIA",
        "case_id": fixture["benchmark_id"],
        "qwen_output": qwen_text,
        "validator_finding": (r.rejections or [{}])[0].get("reason"),
        "gpt_rephrase_called": r.rephrase_log.get("gpt_rephrase_called") if r.rephrase_log else False,
        "gpt_input_tokens": r.rephrase_log.get("gpt_input_tokens") if r.rephrase_log else 0,
        "gpt_output_tokens": r.rephrase_log.get("gpt_output_tokens") if r.rephrase_log else 0,
        "gpt_rephrased_output": r.rephrase_log.get("gpt_rephrased_output") if r.rephrase_log else None,
        "validator_after": r.rephrase_log.get("validator_status_after_rephrase") if r.rephrase_log else None,
        "final_output": r.output,
        "final_source": r.final_source,
        "result": "PASS" if r.ok else "FAIL",
        "notes": r.error or "",
    })
    print("COALINDIA", json.dumps(records[-1], ensure_ascii=False, default=str)[:800])

    # --- CC APLLTD --------------------------------------------------------
    apl = find_case(cc_before, "CC_APLLTD_106633638")
    qwen_text = first_failed_text(apl)
    fixture = cc_fix["CC_APLLTD_106633638"]
    variant = retries_extended_variant(8)
    r = run_variant(StaticQwen(qwen_text), fixture, "qwen3-14b-awq-tp2", variant,
                    rephrase_backend=gpt)
    records.append({
        "category": "concall",
        "symbol": "APLLTD",
        "case_id": fixture["benchmark_id"],
        "qwen_output": qwen_text,
        "validator_finding": (r.rejections or [{}])[0].get("reason"),
        "gpt_rephrase_called": r.rephrase_log.get("gpt_rephrase_called") if r.rephrase_log else False,
        "gpt_input_tokens": r.rephrase_log.get("gpt_input_tokens") if r.rephrase_log else 0,
        "gpt_output_tokens": r.rephrase_log.get("gpt_output_tokens") if r.rephrase_log else 0,
        "gpt_rephrased_output": r.rephrase_log.get("gpt_rephrased_output") if r.rephrase_log else None,
        "validator_after": r.rephrase_log.get("validator_status_after_rephrase") if r.rephrase_log else None,
        "final_output": r.output,
        "final_source": r.final_source,
        "result": "PASS" if r.ok else "FAIL",
        "notes": r.error or "",
    })
    print("APLLTD", json.dumps(records[-1], ensure_ascii=False, default=str)[:800])

    # --- AR VEDL control (previously successful; GPT must NOT be called) --
    vedl = find_case(ar_before, "AR_VEDL_AR_26570_VEDL_2024_2025_A_18062025151918")
    qwen_text = vedl.get("output") or first_failed_text(vedl)
    fixture = ar_fix["AR_VEDL_AR_26570_VEDL_2024_2025_A_18062025151918"]
    r = task_ar.run(StaticQwen(qwen_text), fixture, "qwen3-14b-awq-tp2",
                    rephrase_backend=gpt)
    records.append({
        "category": "annual_report",
        "symbol": "VEDL",
        "case_id": fixture["benchmark_id"],
        "qwen_output": qwen_text,
        "validator_finding": None,
        "gpt_rephrase_called": bool(r.rephrase_log),
        "gpt_input_tokens": r.rephrase_log.get("gpt_input_tokens") if r.rephrase_log else 0,
        "gpt_output_tokens": r.rephrase_log.get("gpt_output_tokens") if r.rephrase_log else 0,
        "gpt_rephrased_output": r.rephrase_log.get("gpt_rephrased_output") if r.rephrase_log else None,
        "validator_after": r.rephrase_log.get("validator_status_after_rephrase") if r.rephrase_log else None,
        "final_output": r.output,
        "final_source": r.final_source,
        "result": "PASS" if r.ok else "FAIL",
        "notes": r.error or "",
    })
    print("VEDL", json.dumps(records[-1], ensure_ascii=False, default=str)[:400])

    with open(os.path.join(out_dir, "rephrase_targeted_results.json"), "w", encoding="utf-8") as fh:
        json.dump(records, fh, ensure_ascii=False, indent=2, default=str)
    print("WROTE", os.path.join(out_dir, "rephrase_targeted_results.json"))


if __name__ == "__main__":
    main()
