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
    # Second AR generation lane on the Red Flag account's spare GPU hours
    # — identical task, writeback and validators to generate_ar; separate
    # phase key only so its directories/marker do not collide. See
    # data-pipeline/kaggle_daily_stage.py's PHASES entry for why the two
    # lanes must never overlap in time.
    "generate_ar_rf": {
        "kind": "generate", "task": "annual_report_summary",
        "writeback": "writeback_annual_report.py",
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


def normalize_kernel_slug(slug: str) -> str:
    """THE single definition of a Kaggle kernel slug for this pipeline.

    2026-09-08, after a real overnight loss: Kaggle NORMALIZES a pushed
    kernel slug (underscores -> hyphens) but keeps the TITLE verbatim. The
    scheduler built its slug from the phase name (`embed_ar`), so the push
    created `redixfi-prod-embed-ar-daily` while every later status/output
    call used `redixfi-prod-embed_ar-daily` -> 403 Forbidden on
    ListKernelSessionOutput. All five phases ran to completion on Kaggle
    and every one of them had its output thrown away: zero writeback,
    ~2.5 real GPU-hours wasted, no production data changed.

    Normalizing here (and again at the caller that builds the slug) means
    push, poll and retrieve physically cannot use different refs: they all
    read the same normalized variable rather than re-deriving it.
    """
    return slug.replace("_", "-")


def mark_pushed(marker_path: str | None, kernel_ref: str) -> None:
    """Record kernel_pushed=true the moment the push succeeds.

    Previously the parent process set this only after the whole round trip
    returned, so last night's markers all said kernel_pushed=false even
    though every kernel had been pushed and had run — the flag lied about
    real GPU work precisely when something later failed, which is exactly
    when an accurate record matters most.
    """
    if not marker_path:
        return
    try:
        path = Path(marker_path)
        marker = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
        marker.update({
            "kernel_pushed": True,
            "kernel_ref": kernel_ref,
            "kernel_pushed_at": __import__("datetime").datetime.now(
                __import__("datetime").timezone.utc).isoformat(),
        })
        path.write_text(json.dumps(marker, indent=2), encoding="utf-8")
    except Exception as exc:  # never let bookkeeping break a real run
        print(f"[WARN] could not update marker {marker_path}: {exc}", flush=True)


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


def staged_unit_count(batch_path: Path, kind: str) -> int | None:
    """How many units we actually staged, for the stale-output check.

    Embed batches are hundreds of MB (219MB for 96,409 chunks), so this
    stream-counts the per-chunk key rather than doing a second full
    json.load in the launcher on top of the one the writeback already
    does. Each chunk record carries exactly one "chunk_index" key under
    export_embed_batch.py's schema, so the count is exact for this
    writer. Generation batches are small enough to parse directly.
    """
    try:
        if kind == "embed":
            needle = b'"chunk_index"'
            total, tail = 0, b""
            with batch_path.open("rb") as fh:
                while True:
                    block = fh.read(8 << 20)
                    if not block:
                        break
                    buf = tail + block
                    total += buf.count(needle)
                    # keep an overlap so a key split across reads is not lost
                    tail = buf[-(len(needle) - 1):]
            return total
        with batch_path.open(encoding="utf-8") as fh:
            return len(json.load(fh).get("cases") or [])
    except Exception as exc:  # never block a good run on a counting failure
        print(f"[WARN] could not count staged units in {batch_path}: {exc}",
              flush=True)
        return None


def returned_unit_count(doc: dict, kind: str) -> int | None:
    if kind == "embed":
        return doc.get("input_chunks")
    if isinstance(doc.get("cases"), int):
        return doc["cases"]
    results = doc.get("results")
    return len(results) if isinstance(results, list) else None


def assert_complete(path: Path, phase: str, batch_path: Path | None = None) -> dict:
    if not path.is_file():
        raise RuntimeError(f"Kaggle output missing: {path}")
    with path.open(encoding="utf-8") as fh:
        doc = json.load(fh)
    if not doc.get("complete"):
        raise RuntimeError(f"Kaggle output is not complete for {phase}: {path}")

    # STALE-OUTPUT GUARD, 2026-09-08. A kernel launched before Kaggle
    # finished processing a freshly pushed dataset version silently
    # mounted the PREVIOUS version: we staged 96,409 chunks and the
    # kernel embedded last night's 37,443, upserted them idempotently,
    # and reported "WROTE 37443 ... COMPLETE". Nothing errored, the log
    # looked like success, and the database did not move at all. That is
    # far more dangerous than the first-push variant of the same race,
    # which at least fails loudly.
    #
    # push_dataset() now waits for the dataset to be ready, so this
    # should not recur — but "should not" is not a check. Comparing what
    # we staged against what came back is cheap, independent of the
    # upload path, and is the assertion that would have caught the
    # incident immediately instead of reporting success on a no-op.
    if batch_path is not None and batch_path.is_file():
        kind = PHASE_CONFIG[phase]["kind"]
        staged = staged_unit_count(batch_path, kind)
        returned = returned_unit_count(doc, kind)
        unit = "chunk" if kind == "embed" else "case"
        if staged and returned is not None and staged != returned:
            raise RuntimeError(
                f"STALE OR MISMATCHED Kaggle output for {phase}: staged "
                f"{staged} {unit}(s) but the kernel processed {returned}. "
                f"The kernel almost certainly ran against an older dataset "
                f"version (see push_dataset's ready-wait). REFUSING to write "
                f"back — writing this would report success while leaving the "
                f"staged batch unprocessed. Re-run the launcher once the "
                f"dataset reports ready.")
        if staged and returned is not None:
            print(f"[INFO] output matches staged batch: {returned} {unit}(s)",
                  flush=True)
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
    ap.add_argument("--marker-path", default=None,
                    help="ready-marker JSON to stamp kernel_pushed=true on, "
                         "the moment the push succeeds")
    ap.add_argument("--timeout", type=int, default=4 * 60 * 60)
    args = ap.parse_args()

    cfg = PHASE_CONFIG[args.phase]
    stage_dir = Path(args.stage_dir)
    batch_path = Path(args.batch_path)
    out_dir = Path(args.out_dir)
    kernel_dir = stage_dir.parent / f"{args.phase}_kernel"
    dataset_ref = f"{args.dataset_owner}/{args.dataset_slug}"
    # ONE normalized slug, derived once, used for push AND poll AND
    # retrieve. See normalize_kernel_slug() for the real incident this
    # closes. Nothing below may re-derive a ref from args.kernel_slug.
    kernel_slug = normalize_kernel_slug(args.kernel_slug)
    kernel_ref = f"{args.dataset_owner}/{kernel_slug}"
    if kernel_slug != args.kernel_slug:
        print(f"[INFO] normalized kernel slug {args.kernel_slug!r} -> "
             f"{kernel_slug!r} (Kaggle hyphenates on push)", flush=True)
    # The GPT-4o-mini editor inside the kernel resolves its key from a
    # mounted private dataset (Kaggle Secrets is unreachable from kernels
    # — a ConnectionError confirmed again in last night's logs). Without
    # this second dataset attached, every case needing the editor dies
    # with "OPENAI_API_KEY is required": 7 of 20 AR and 7 of 20 concall
    # cases were lost that way last night. Embed phases never call the
    # editor, so they do not need it.
    extra_datasets = ([] if cfg["kind"] == "embed"
                      else [f"{args.dataset_owner}/redixfi-openai-key"])

    configure_kaggle(args.kaggle_account)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if cfg["kind"] == "embed":
        stage_and_push_embed_kernel(kernel_dir, args.dataset_owner,
                                    kernel_slug, dataset_ref)
    else:
        if kernel_dir.exists():
            shutil.rmtree(kernel_dir)
        stage_and_push_kernel(
            str(kernel_dir), cfg["task"], batch_path.name,
            f"output_{args.phase}.json", args.dataset_owner, kernel_slug,
            args.dataset_owner, args.dataset_slug,
            extra_dataset_sources=extra_datasets)
    mark_pushed(args.marker_path, kernel_ref)

    print(f"POLLING: {dataset_ref} kernel={kernel_ref}", flush=True)
    poll_and_retrieve(args.dataset_owner, kernel_slug, str(out_dir), args.timeout)
    output = output_contract(args.phase, out_dir)
    assert_complete(output, args.phase, batch_path)
    writeback(args.phase, output, batch_path)
    print(f"COMPLETE: {args.phase} output={output}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
