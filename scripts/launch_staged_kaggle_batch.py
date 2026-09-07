#!/usr/bin/env python3
"""Launch one already-staged production batch and write it back safely.

This is deliberately separate from ``kaggle_daily_stage.py`` so that dataset
staging remains safe by default.  The nightly scheduler opts into this script
with ``--auto-launch`` only after the dataset upload succeeds.

The kernel remains isolated from production MongoDB/ChromaDB.  This process
only launches Kaggle, retrieves the completed JSON, validates its completion
flag, and then invokes the existing explicit ``--confirm`` writeback tool.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from run_production_batch import poll_and_retrieve, stage_and_push_kernel


PHASE_CONFIG = {
    "embed_ar": {"kind": "embed", "writeback": "writeback_embeddings.py"},
    "embed_cc": {"kind": "embed", "writeback": "writeback_embeddings.py"},
    "generate_ar": {
        "kind": "generate", "task": "annual_report_summary",
        "writeback": "writeback_annual_report.py",
    },
    "generate_cc": {
        "kind": "generate", "task": "concall_summary",
        "writeback": "writeback_concall.py",
    },
    "reclassify_rf": {
        "kind": "generate", "task": "red_flag",
        "writeback": "writeback_red_flag.py",
    },
}


def configure_kaggle(account: str) -> None:
    profile = Path(os.path.expanduser("~")) / ".kaggle_profiles" / account
    config = profile / "kaggle.json"
    if not config.is_file():
        raise RuntimeError(f"Kaggle profile not found: {profile}")
    os.environ["KAGGLE_CONFIG_DIR"] = str(profile)
    with config.open(encoding="utf-8") as fh:
        os.environ["KAGGLE_API_TOKEN"] = json.load(fh)["key"]


def _embed_wrapper() -> str:
    return '''import glob, subprocess, sys

hits = glob.glob("/kaggle/input/**/deployment/kaggle/run_embed_batch.py", recursive=True)
assert hits, "run_embed_batch.py not found under /kaggle/input"
sys.exit(subprocess.run([sys.executable, hits[0]]).returncode)
'''


def stage_and_push_embed_kernel(kernel_dir: Path, owner: str, slug: str,
                                dataset_ref: str) -> None:
    kernel_dir.mkdir(parents=True, exist_ok=True)
    wrapper_name = f"run_{slug.replace('-', '_')}.py"
    (kernel_dir / wrapper_name).write_text(_embed_wrapper(), encoding="utf-8")
    metadata = {
        "id": f"{owner}/{slug}", "title": slug,
        "code_file": wrapper_name, "language": "python", "kernel_type": "script",
        "is_private": True, "enable_gpu": True, "enable_internet": True,
        "dataset_sources": [dataset_ref], "competition_sources": [],
        "kernel_sources": [],
    }
    (kernel_dir / "kernel-metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8")
    launcher = Path(__file__).parents[1] / "deployment" / "kaggle" / "push_embed_kernel.py"
    subprocess.run([sys.executable, str(launcher), str(kernel_dir)], check=True)


def output_contract(phase: str, out_dir: Path) -> Path:
    return out_dir / ("embed_batch_output.json" if PHASE_CONFIG[phase]["kind"] == "embed"
                       else f"output_{phase}.json")


def assert_complete(path: Path, phase: str) -> dict:
    if not path.is_file():
        raise RuntimeError(f"Kaggle output missing: {path}")
    with path.open(encoding="utf-8") as fh:
        doc = json.load(fh)
    if not doc.get("complete"):
        raise RuntimeError(f"Kaggle output is not complete for {phase}: {path}")
    return doc


def writeback(phase: str, output: Path, batch_path: Path) -> None:
    cfg = PHASE_CONFIG[phase]
    script = Path(__file__).parents[1] / "production" / cfg["writeback"]
    cmd = [sys.executable, str(script), "--kaggle-output", str(output), "--confirm"]
    if cfg["kind"] == "embed":
        cmd += ["--input-batch", str(batch_path)]
    print("WRITEBACK:", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=sorted(PHASE_CONFIG), required=True)
    ap.add_argument("--kaggle-account", required=True)
    ap.add_argument("--dataset-owner", required=True)
    ap.add_argument("--dataset-slug", required=True)
    ap.add_argument("--batch-path", required=True)
    ap.add_argument("--stage-dir", required=True)
    ap.add_argument("--kernel-slug", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--timeout", type=int, default=4 * 60 * 60)
    args = ap.parse_args()

    cfg = PHASE_CONFIG[args.phase]
    stage_dir = Path(args.stage_dir)
    batch_path = Path(args.batch_path)
    out_dir = Path(args.out_dir)
    kernel_dir = stage_dir.parent / f"{args.phase}_kernel"
    dataset_ref = f"{args.dataset_owner}/{args.dataset_slug}"

    configure_kaggle(args.kaggle_account)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if cfg["kind"] == "embed":
        stage_and_push_embed_kernel(kernel_dir, args.dataset_owner,
                                    args.kernel_slug, dataset_ref)
    else:
        if kernel_dir.exists():
            shutil.rmtree(kernel_dir)
        stage_and_push_kernel(
            str(kernel_dir), cfg["task"], batch_path.name,
            f"output_{args.phase}.json", args.dataset_owner, args.kernel_slug,
            args.dataset_owner, args.dataset_slug)

    print(f"POLLING: {dataset_ref} kernel={args.dataset_owner}/{args.kernel_slug}",
          flush=True)
    poll_and_retrieve(args.dataset_owner, args.kernel_slug, str(out_dir), args.timeout)
    output = output_contract(args.phase, out_dir)
    assert_complete(output, args.phase)
    writeback(args.phase, output, batch_path)
    print(f"COMPLETE: {args.phase} output={output}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
