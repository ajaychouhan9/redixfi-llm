#!/usr/bin/env python3
"""CONTROLLED FIX RETEST kernel — small targeted sample, one model load.

Loads qwen3-14b-awq-tp2 once, then runs three tiny retest batches with the
Phase 1-4 code changes:

  * annual_report_summary  -> IMPROVED_POLICY (Phase 2 shared retry)
  * concall_summary        -> retries_extended_variant(8) + Phase 3 prompt
  * red_flag               -> Phase 4 classification prompt + Phase 1 consistency

Inputs are fixture-shaped JSON files (one per category) from the attached
dataset. Outputs are written to /kaggle/working/output_<task>.json.
"""
import glob
import json
import os
import subprocess
import sys
import time

if os.environ.get("_RETEST_VLLM_INSTALL_TRIED") != "1":
    try:
        import vllm  # noqa: F401
    except ImportError:
        print("installing vLLM...", flush=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                        "--no-cache-dir", "vllm"], check=False)
        os.environ["_RETEST_VLLM_INSTALL_TRIED"] = "1"
        os.execv(sys.executable, [sys.executable] + sys.argv)

print("=" * 72, flush=True)
hits = glob.glob("/kaggle/input/**/app/tasks/concall_summary.py", recursive=True)
assert hits, "llm project not found under /kaggle/input"
project_root = hits[0].split("/app/tasks/")[0]
sys.path.insert(0, project_root)
print("project root:", project_root, flush=True)

from app.models.registry import get_model_spec  # noqa: E402
from app.tasks import annual_report_summary as task_ar  # noqa: E402
from app.tasks import concall_summary as task_cc  # noqa: E402
from app.tasks import red_flag as task_rf  # noqa: E402
from app.tasks.retry_policy import IMPROVED_POLICY  # noqa: E402
from app.experiments.concall_variants import retries_extended_variant, run_variant  # noqa: E402

MODEL = "qwen3-14b-awq-tp2"
OUT_DIR = "/kaggle/working"
AR_IN = glob.glob("/kaggle/input/**/retest_ar_3.json", recursive=True)[0]
CC_IN = glob.glob("/kaggle/input/**/retest_cc_3.json", recursive=True)[0]
RF_IN = glob.glob("/kaggle/input/**/retest_rf_5.json", recursive=True)[0]

spec = get_model_spec(MODEL)
print(f"loading {spec.hf_repo} ...", flush=True)
t0 = time.time()
from vllm import LLM  # noqa: E402
llm = LLM(**spec.to_vllm_kwargs())
print(f"loaded in {time.time()-t0:.1f}s", flush=True)

from app.inference.vllm_inprocess import VLLMInProcessBackend  # noqa: E402
chat_native = spec.extra_vllm_args.get("tokenizer_mode") == "mistral"
backend = VLLMInProcessBackend(llm, MODEL, chat_native=chat_native)

CC_VARIANT = retries_extended_variant(8)


def load_cases(path):
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    return doc.get("cases", [])


def run_ar(cases):
    results = []
    for i, case in enumerate(cases, 1):
        cid = case.get("benchmark_id") or case.get("fixture_id")
        print(f"  AR [{i}/{len(cases)}] {cid}", flush=True)
        r = task_ar.run(backend, case, MODEL, policy=IMPROVED_POLICY)
        row = r.to_dict()
        row["case_id"] = cid
        row["symbol"] = case.get("symbol")
        results.append(row)
    return results


def run_cc(cases):
    results = []
    for i, case in enumerate(cases, 1):
        cid = case.get("benchmark_id") or case.get("fixture_id")
        print(f"  CC [{i}/{len(cases)}] {cid}", flush=True)
        r = run_variant(backend, case, MODEL, CC_VARIANT)
        row = r.to_dict()
        row["case_id"] = cid
        row["symbol"] = case.get("symbol")
        results.append(row)
    return results


def run_rf(cases):
    results = []
    for i, case in enumerate(cases, 1):
        cid = case.get("benchmark_id") or case.get("chunk_id")
        print(f"  RF [{i}/{len(cases)}] {cid}", flush=True)
        r = task_rf.run(backend, case, MODEL)
        row = r.to_dict()
        row["case_id"] = cid
        row["symbol"] = case.get("symbol")
        results.append(row)
    return results


def write(name, results):
    path = os.path.join(OUT_DIR, name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"model": MODEL, "results": results}, fh, ensure_ascii=False,
                  indent=2, default=str)
    print("wrote", path, flush=True)


ar_results = run_ar(load_cases(AR_IN))
write("output_annual_report_summary.json", ar_results)
cc_results = run_cc(load_cases(CC_IN))
write("output_concall_summary.json", cc_results)
rf_results = run_rf(load_cases(RF_IN))
write("output_red_flag.json", rf_results)

print("DONE", flush=True)
