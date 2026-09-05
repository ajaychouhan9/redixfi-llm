#!/usr/bin/env python3
"""Orchestrate ONE production batch: export real docs -> Kaggle Qwen
generation -> retrieve output. Writeback is a SEPARATE, explicit step
(production/writeback_*.py) — this script never writes to Mongo/Chroma.

Designed to run ON THE VM (co-located with Mongo/Chroma for export, and
with internet access for Kaggle). Requires:
  * REDIXFI_ROOT / CHROMA_PATH env (defaults match the VM's real paths)
  * a Kaggle credential profile per category:
        export KAGGLE_CONFIG_DIR=/home/ubuntu/.kaggle_profiles/<category>
        export KAGGLE_API_TOKEN=<same key, as a raw string — REQUIRED for
            kernels_push/status/output; kaggle.json alone 401s on these
            2026-era tokens, see redixfi_kaggle_new_token_bearer_auth
            memory / this script's own comments>

    python scripts/run_production_batch.py \
        --task concall_summary --kaggle-user aurataxai \
        --dataset-slug redixfi-prod-concall-batch \
        --kernel-slug redixfi-prod-concall-test \
        --limit 20 --poll
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REDIXFI_ROOT = os.getenv("REDIXFI_ROOT", "/home/ubuntu/redixfi-backend")
STAGE_DIR = os.getenv("PROD_STAGE_DIR", "/home/ubuntu/prod_stage")


def _run(cmd, **kw):
    print("  $", " ".join(cmd), flush=True)
    return subprocess.run(cmd, check=True, **kw)


def export_batch(task: str, limit: int, out_path: str, red_flag_collection: str):
    llm_pipeline = os.path.join(REDIXFI_ROOT, "llm-pipeline")
    if task == "red_flag":
        _run([sys.executable, os.path.join(llm_pipeline, "production",
                                           "export_red_flag_batch.py"),
             "--collection", red_flag_collection, "--limit", str(limit),
             "--out", out_path])
    else:
        _run([sys.executable, os.path.join(llm_pipeline, "production",
                                           "export_generation_batch.py"),
             "--task", task, "--limit", str(limit), "--out", out_path,
             "--confirm"])


def stage_dataset(stage_dir: str, batch_path: str, dataset_owner: str, dataset_slug: str):
    project_dir = os.path.join(stage_dir, "llm_project")
    if os.path.isdir(project_dir):
        subprocess.run(["rm", "-rf", project_dir])
    os.makedirs(project_dir, exist_ok=True)
    llm_pipeline = os.path.join(REDIXFI_ROOT, "llm-pipeline")
    tar_cmd = (
        f'cd "{llm_pipeline}" && tar -cf - --exclude=".git" --exclude="__pycache__" '
        '--exclude="*.pyc" --exclude="evaluation/*/runs" '
        'app deployment scripts tests example_bank production README.md '
        f'2>/dev/null | tar -xf - -C "{project_dir}"'
    )
    subprocess.run(tar_cmd, shell=True, check=True)
    import shutil
    shutil.copy(batch_path, os.path.join(stage_dir, os.path.basename(batch_path)))
    with open(os.path.join(stage_dir, "dataset-metadata.json"), "w") as fh:
        json.dump({"title": dataset_slug, "id": f"{dataset_owner}/{dataset_slug}",
                  "licenses": [{"name": "other"}]}, fh)


def push_dataset(stage_dir: str, dataset_owner: str, dataset_slug: str):
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    try:
        api.dataset_status(f"{dataset_owner}/{dataset_slug}")
        exists = True
    except Exception:
        exists = False
    if exists:
        api.dataset_create_version(stage_dir, version_notes="production batch update",
                                   dir_mode="zip")
    else:
        api.dataset_create_new(stage_dir, dir_mode="zip", public=False)


def stage_and_push_kernel(kernel_dir: str, task: str, batch_basename: str,
                          output_basename: str, kernel_owner: str, kernel_slug: str,
                          dataset_owner: str, dataset_slug: str):
    os.makedirs(kernel_dir, exist_ok=True)
    template_path = os.path.join(ROOT, "deployment", "kaggle",
                                 "production_kernel_wrapper.py")
    wrapper_name = f"run_{kernel_slug.replace('-', '_')}.py"
    with open(template_path, encoding="utf-8") as fh:
        body = fh.read()
    body = (body.replace('"{{TASK}}"', repr(task))
                .replace('"{{INPUT_BASENAME}}"', repr(batch_basename))
                .replace('"{{OUTPUT_BASENAME}}"', repr(output_basename)))
    with open(os.path.join(kernel_dir, wrapper_name), "w", encoding="utf-8") as fh:
        fh.write(body)
    with open(os.path.join(kernel_dir, "kernel-metadata.json"), "w", encoding="utf-8") as fh:
        json.dump({
            "id": f"{kernel_owner}/{kernel_slug}", "title": kernel_slug,
            "code_file": wrapper_name, "language": "python", "kernel_type": "script",
            "is_private": True, "enable_gpu": True, "enable_internet": True,
            "dataset_sources": [f"{dataset_owner}/{dataset_slug}"],
            "competition_sources": [], "kernel_sources": [],
        }, fh)

    # machine_shape=NvidiaTeslaT4 is required for a real 2xT4 session — the
    # standard KaggleApi.kernels_push() wrapper does not expose this field
    # at all (confirmed 2026-08-30: without it, a single-GPU session is
    # provisioned and tensor_parallel_size=2 fails with "World size (2) is
    # larger than the number of available GPUs (1)"). Built manually via
    # kagglesdk rather than the incomplete high-level wrapper.
    from kaggle.api.kaggle_api_extended import KaggleApi
    from kagglesdk.kernels.types.kernels_api_service import ApiSaveKernelRequest
    api = KaggleApi()
    api.authenticate()
    meta_data = json.load(open(os.path.join(kernel_dir, "kernel-metadata.json")))
    script_body = open(os.path.join(kernel_dir, wrapper_name), encoding="utf-8").read()
    with api.build_kaggle_client() as kaggle:
        request = ApiSaveKernelRequest()
        request.slug = meta_data["id"]
        request.new_title = meta_data["title"]
        request.text = script_body
        request.language = meta_data["language"]
        request.kernel_type = meta_data["kernel_type"]
        request.is_private = meta_data["is_private"]
        request.enable_gpu = meta_data["enable_gpu"]
        request.enable_internet = meta_data["enable_internet"]
        request.dataset_data_sources = meta_data["dataset_sources"]
        request.machine_shape = "NvidiaTeslaT4"
        resp = kaggle.kernels.kernels_api_client.save_kernel(request)
        print("  pushed:", getattr(resp, "url", None))


def poll_and_retrieve(kernel_owner: str, kernel_slug: str, out_dir: str,
                      timeout_sec: int = 3600):
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    ref = f"{kernel_owner}/{kernel_slug}"
    t0 = time.time()
    last = None
    while True:
        try:
            s = api.kernels_status(ref)
            st = str(s.get("status") if isinstance(s, dict) else getattr(s, "status", None))
        except Exception as exc:
            st = f"POLL_ERROR {exc}"
        if st != last:
            print(f"  [{(time.time()-t0)/60:5.1f}m] {st}", flush=True)
            last = st
        if any(x in st.upper() for x in ("COMPLETE", "ERROR", "CANCEL")):
            break
        if time.time() - t0 > timeout_sec:
            sys.exit("TIMEOUT waiting for kernel")
        time.sleep(20)
    api.kernels_output(ref, path=out_dir)
    if "ERROR" in last.upper():
        sys.exit(f"kernel finished with status {last} — inspect {out_dir} before proceeding")
    print(f"  output retrieved -> {out_dir}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True,
                    choices=("annual_report_summary", "concall_summary", "red_flag"))
    ap.add_argument("--kaggle-owner", required=True,
                    help="the Kaggle account owning the profile currently active "
                         "via KAGGLE_CONFIG_DIR/KAGGLE_API_TOKEN")
    ap.add_argument("--dataset-slug", required=True)
    ap.add_argument("--kernel-slug", required=True)
    ap.add_argument("--limit", type=int, default=2)
    ap.add_argument("--red-flag-collection", choices=("annual_reports", "investor_calls"),
                    default="annual_reports")
    ap.add_argument("--poll", action="store_true",
                    help="wait for the kernel and retrieve output; without this, "
                         "the script exits right after pushing")
    ap.add_argument("--out-dir", default=None)
    args = ap.parse_args()

    if not os.environ.get("KAGGLE_API_TOKEN"):
        sys.exit("KAGGLE_API_TOKEN is not set — kernel push/status/output will "
                 "401 without it even with a valid kaggle.json. See "
                 "deployment/kaggle/production_generate.py's module docstring "
                 "or the redixfi_kaggle_new_token_bearer_auth memory.")

    stage_dir = os.path.join(STAGE_DIR, args.task)
    kernel_dir = os.path.join(STAGE_DIR, args.task + "_kernel")
    batch_path = os.path.join(stage_dir, f"batch_{args.task}.json")
    output_basename = f"output_{args.task}.json"

    print(f"[1/4] exporting {args.limit} real case(s) for {args.task}...")
    os.makedirs(stage_dir, exist_ok=True)
    export_batch(args.task, args.limit, batch_path, args.red_flag_collection)

    print(f"[2/4] staging + pushing dataset {args.kaggle_owner}/{args.dataset_slug}...")
    stage_dataset(stage_dir, batch_path, args.kaggle_owner, args.dataset_slug)
    push_dataset(stage_dir, args.kaggle_owner, args.dataset_slug)

    print(f"[3/4] staging + pushing kernel {args.kaggle_owner}/{args.kernel_slug}...")
    stage_and_push_kernel(kernel_dir, args.task, os.path.basename(batch_path),
                          output_basename, args.kaggle_owner, args.kernel_slug,
                          args.kaggle_owner, args.dataset_slug)

    if not args.poll:
        print("\n[4/4] SKIPPED (--poll not set). Kernel is running; check status "
             "and retrieve output manually, or re-run with --poll.")
        return

    print("[4/4] polling for completion...")
    out_dir = args.out_dir or os.path.join(STAGE_DIR, args.task + "_output")
    poll_and_retrieve(args.kaggle_owner, args.kernel_slug, out_dir)

    output_file = os.path.join(out_dir, output_basename)
    print(f"\nDone. Output: {output_file}")
    print(f"Next step (dry-run first, always): "
         f"python production/writeback_{'concall' if args.task=='concall_summary' else args.task.replace('annual_report_summary','annual_report')}.py "
         f"--kaggle-output {output_file}")


if __name__ == "__main__":
    main()
