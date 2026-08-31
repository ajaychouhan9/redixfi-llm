#!/usr/bin/env python3
"""APLLTD-only targeted rephrase test (one GPT call max)."""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from app.experiments.concall_variants import retries_extended_variant, run_variant
from app.inference.base import GenerationRequest, GenerationResult
from app.tasks.rephrase import build_rephrase_backend


class StaticQwen:
    name = "static-qwen"

    def __init__(self, output_dict):
        self.output_dict = output_dict

    def generate(self, request: GenerationRequest) -> GenerationResult:
        return GenerationResult(
            text=json.dumps(self.output_dict), model=request.model,
            backend=self.name, prompt_tokens=0, completion_tokens=0, total_tokens=0)


def main() -> None:
    cid = "CC_APLLTD_106633638"
    cc_before = json.load(open(os.path.join(
        ROOT, "evaluation", "fix_validation", "retest_outputs",
        "output_concall_summary.json"), encoding="utf-8"))["results"]
    result = next(r for r in cc_before if r.get("case_id") == cid)
    qwen_text = next(rej["text"] for rej in (result.get("rejections") or [])
                     if isinstance(rej.get("text"), dict) and rej["text"])

    cc_fix = json.load(open(os.path.join(
        ROOT, "fixtures", "retest_cc_3.json"), encoding="utf-8"))["cases"]
    fixture = next(c for c in cc_fix if c["benchmark_id"] == cid)

    gpt = build_rephrase_backend()
    r = run_variant(StaticQwen(qwen_text), fixture, "qwen3-14b-awq-tp2",
                    retries_extended_variant(8), rephrase_backend=gpt)

    out = {
        "case_id": cid,
        "symbol": "APLLTD",
        "qwen_output": qwen_text,
        "validator_finding": (r.rejections or [{}])[0].get("reason"),
        "gpt_rephrase_called": bool(r.rephrase_log),
        "gpt_input_tokens": r.rephrase_log.get("gpt_input_tokens") if r.rephrase_log else 0,
        "gpt_output_tokens": r.rephrase_log.get("gpt_output_tokens") if r.rephrase_log else 0,
        "gpt_rephrased_output": r.rephrase_log.get("gpt_rephrased_output") if r.rephrase_log else None,
        "validator_after": r.rephrase_log.get("validator_status_after_rephrase") if r.rephrase_log else None,
        "information_preservation_check": r.information_preservation_check,
        "final_output": r.output,
        "final_source": r.final_source,
        "final_status": r.final_status,
        "human_review_required": r.human_review_required,
        "human_review_reason": r.human_review_reason,
        "result": "PASS" if r.ok else "FAIL",
        "notes": r.error or "",
    }
    out_path = os.path.join(ROOT, "evaluation", "fix_validation",
                            "rephrase_retest_outputs", "aplltd_fix_results.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, default=str)
    print("APLLTD_FIX", json.dumps(out, ensure_ascii=False, default=str)[:1500])
    print("WROTE", out_path)


if __name__ == "__main__":
    main()
