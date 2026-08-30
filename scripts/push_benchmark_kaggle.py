#!/usr/bin/env python3
"""Push ONE benchmark category to Kaggle and (optionally) poll + retrieve.

Reuses the exact staging/push/poll machinery from scripts/run_production_batch.py
(stage_dataset / push_dataset / stage_and_push_kernel / poll_and_retrieve) so
this benchmark does not invent a second Kaggle path.

Run on the VM (Linux) with the benchmark Kaggle profile active:

    source /home/ubuntu/.kaggle_profiles/env_helper.sh
    kaggle_env benchmark
    python3 scripts/push_benchmark_kaggle.py \
        --task annual_report_summary \
        --fixture /home/ubuntu/llm_fixtures/annual_report_72.json \
        --dataset-slug redixfi-benchmark-ar-20260830 \
        --kernel-slug redixfi-benchmark-ar-20260830 \
        --stage-dir /home/ubuntu/benchmark_stage_ar \
        --out-dir /home/ubuntu/benchmark_out_ar \
        --poll
"""
from __future__ import annotations

import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.run_production_batch import (  # noqa: E402
    poll_and_retrieve,
    push_dataset,
    stage_and_push_kernel,
    stage_dataset,
)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True,
                    choices=("annual_report_summary", "concall_summary", "red_flag"))
    ap.add_argument("--fixture", required=True)
    ap.add_argument("--kaggle-owner", default="ajaychouhan9")
    ap.add_argument("--dataset-slug", required=True)
    ap.add_argument("--kernel-slug", required=True)
    ap.add_argument("--stage-dir", required=True)
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--poll", action="store_true")
    ap.add_argument("--timeout-sec", type=int, default=10800)
    args = ap.parse_args()

    stage_dir = os.path.join(args.stage_dir, args.task)
    kernel_dir = os.path.join(args.stage_dir, args.task + "_kernel")
    out_dir = args.out_dir or os.path.join(args.stage_dir, args.task + "_output")
    output_basename = f"output_{args.task}.json"

    print(f"[1/4] staging dataset {args.kaggle_owner}/{args.dataset_slug}...")
    stage_dataset(stage_dir, args.fixture, args.kaggle_owner, args.dataset_slug)

    print(f"[2/4] pushing dataset {args.kaggle_owner}/{args.dataset_slug}...")
    push_dataset(stage_dir, args.kaggle_owner, args.dataset_slug)

    print(f"[3/4] staging + pushing kernel {args.kaggle_owner}/{args.kernel_slug}...")
    stage_and_push_kernel(
        kernel_dir, args.task, os.path.basename(args.fixture), output_basename,
        args.kaggle_owner, args.kernel_slug, args.kaggle_owner, args.dataset_slug,
    )

    if not args.poll:
        print("[4/4] SKIPPED (--poll not set)")
        return

    print(f"[4/4] polling {args.kaggle_owner}/{args.kernel_slug}...")
    poll_and_retrieve(args.kaggle_owner, args.kernel_slug, out_dir,
                      timeout_sec=args.timeout_sec)
    output_file = os.path.join(out_dir, output_basename)
    print(f"\nDone. Output: {output_file}")


if __name__ == "__main__":
    main()
