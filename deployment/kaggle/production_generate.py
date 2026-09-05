#!/usr/bin/env python3
"""PRODUCTION generation kernel — real documents, real output, no eval
scoring (there is no reference to compare against; this generates NEW
production content). Reuses the SAME validated task code
(app/tasks/<task>.py) and model registry as the eval harness — no
prompt/validator logic is reimplemented here.

Input:  a fixture-shaped JSON batch exported from real Mongo/Chroma data
        (see production/export_*.py on the VM).
Output: one JSON per case: the task's structured output dict, or a
        recorded failure — never partial/placeholder content, matching
        every task's own fail-soft posture.

concall uses the CONFIRMED retry-budget-8 fix (production prompt,
IMPROVED retry policy, 8 attempts) — the one change this project found to
be a real, unambiguous improvement (20/20 vs 15/20 baseline) rather than
a single-run curiosity. annual_report and red_flag run with production
settings (3 attempts / single-shot) as validated during eval — no
unconfirmed prompt changes (steering, red_flag instance-check) are
carried into production; both were found to backfire or regress.
"""
import argparse
import glob
import json
import os
import subprocess
import sys
import time

# --- vLLM install + re-exec -------------------------------------------
# Every real Kaggle run this project has done needed vLLM installed fresh
# (it is not on the base image) before it becomes importable. Verified
# 2026-08-30 on this image: vLLM imports and loads correctly WITHOUT the
# CUDA-13-runtime-lib workaround an earlier image needed (those installs
# now fail to build wheels and are harmless to skip — vLLM proceeded past
# them to a real model load). Kept minimal: just the one install this
# image actually needs, re-exec'd into a fresh interpreter afterward so a
# process that imported torch before the install exists can't silently
# miss it (the same reasoning kaggle_run.py's own re-exec documents).
if os.environ.get("_PRODUCTION_VLLM_INSTALL_TRIED") != "1":
    try:
        import vllm  # noqa: F401
    except ImportError:
        print("installing vLLM...", flush=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                        "--no-cache-dir", "vllm"], check=False)
        os.environ["_PRODUCTION_VLLM_INSTALL_TRIED"] = "1"
        os.execv(sys.executable, [sys.executable] + sys.argv)

print("=" * 72)
print("STALENESS GUARD")
print("=" * 72)
hits = glob.glob("/kaggle/input/**/app/tasks/concall_summary.py", recursive=True)
assert hits, "llm-pipeline project not found under /kaggle/input"
project_root = hits[0].split("/app/tasks/")[0]
sys.path.insert(0, project_root)
print("project root:", project_root)

REQUIRED = {
    "app/tasks/retry_policy.py": ["IMPROVED_POLICY"],
    "app/tasks/concall_summary.py": ["policy.temperature_for"],
}
for rel, needles in REQUIRED.items():
    text = open(os.path.join(project_root, rel), encoding="utf-8").read()
    missing = [n for n in needles if n not in text]
    if missing:
        sys.exit(f"STALE PROJECT: {rel} missing {missing} — refusing to run")
print("guard passed.\n")

ap = argparse.ArgumentParser()
ap.add_argument("--task", required=True,
                choices=("annual_report_summary", "concall_summary", "red_flag"))
ap.add_argument("--model", default="qwen3-14b-awq-tp2")
ap.add_argument("--input", required=True, help="fixture-shaped batch JSON")
ap.add_argument("--output", required=True)
ap.add_argument("--retry-policy", default=None, choices=(None, "production", "improved"))
ap.add_argument("--max-attempts", type=int, default=None)
args = ap.parse_args()

from app.models.registry import get_model_spec  # noqa: E402
from app.tasks import annual_report_summary as task_ar  # noqa: E402
from app.tasks import concall_summary as task_cc  # noqa: E402
from app.tasks import red_flag as task_rf  # noqa: E402
from app.tasks.retry_policy import IMPROVED_POLICY, PRODUCTION_POLICY  # noqa: E402

TASK_RUNNERS = {"annual_report_summary": task_ar.run, "concall_summary": task_cc.run,
                "red_flag": task_rf.run}
DEFAULT_POLICY = {"annual_report_summary": IMPROVED_POLICY,  # Phase 2 shared retry fix
                  "concall_summary": IMPROVED_POLICY,   # the CONFIRMED fix
                  "red_flag": PRODUCTION_POLICY}
DEFAULT_ATTEMPTS = {"annual_report_summary": None, "concall_summary": 8, "red_flag": None}

policy = ({"production": PRODUCTION_POLICY, "improved": IMPROVED_POLICY}[args.retry_policy]
          if args.retry_policy else DEFAULT_POLICY[args.task])
max_attempts = args.max_attempts or DEFAULT_ATTEMPTS[args.task]
print(f"task={args.task} model={args.model} policy={policy.name} "
      f"max_attempts_override={max_attempts}")

spec = get_model_spec(args.model)
print(f"loading {spec.hf_repo} ...", flush=True)
t0 = time.time()
from vllm import LLM  # noqa: E402
llm = LLM(**spec.to_vllm_kwargs())
print(f"loaded in {time.time()-t0:.1f}s", flush=True)

from app.inference.vllm_inprocess import VLLMInProcessBackend  # noqa: E402
chat_native = spec.extra_vllm_args.get("tokenizer_mode") == "mistral"
backend = VLLMInProcessBackend(llm, args.model, chat_native=chat_native)

class _Cases:
    """Production batches are a different shape than eval fixtures — no
    reference, no provenance object required (nothing here is being
    scored against gpt-4o-mini; this generates NEW production content).
    Loaded directly rather than through app.evaluation.fixtures.load(),
    whose validator was built for the benchmark fixture schema and would
    otherwise reject a perfectly valid production batch for missing
    fields that only matter for an eval comparison."""
    def __init__(self, cases):
        self.cases = cases


with open(args.input, encoding="utf-8") as fh:
    _doc = json.load(fh)
fs = _Cases(_doc["cases"])
print(f"loaded {len(fs.cases)} real production case(s) from {args.input}")

# concall's confirmed retry-budget-8 fix needs a NON-DEFAULT max_attempts.
# app.tasks.concall_summary.run() reads MAX_ATTEMPTS as a module-level name
# imported at load time from app.prompts.concall_summary — mutating the
# PROMPT module's attribute afterward does not change the TASK module's
# already-bound name (a `from x import y` copies the reference once; it is
# not a live alias). Rather than patch that fragile seam, reuse the exact
# machinery this project already validated the 20/20 result with:
# concall_variants.retries_extended_variant(), production prompt UNCHANGED,
# only policy/budget varied — same code path, same 20/20 evidence.
if args.task == "concall_summary" and policy is IMPROVED_POLICY:
    # retries_extended_variant() hardcodes IMPROVED_POLICY internally (it
    # takes no policy argument) — it IS the exact function this project
    # validated the 20/20 result with, so it is called exactly as tested
    # rather than approximated with a policy override that doesn't exist
    # on its signature.
    from app.experiments.concall_variants import (retries_extended_variant,
                                                   run_variant)
    variant = retries_extended_variant(max_attempts or 8)
    print(f"  using validated variant machinery: {variant.name}")

    def runner(backend, case, model):
        return run_variant(backend, case, model, variant)
elif args.task == "annual_report_summary":
    # Phase 2 (2026-08-30 controlled fix): the shared directive-retry
    # mechanism (improved policy) is now applied to Annual Report as well
    # as Concall. Attempt 1 stays deterministic; retries vary sampling and
    # receive directive corrective feedback.
    def runner(backend, case, model):
        return task_ar.run(backend, case, model, policy=IMPROVED_POLICY)
else:
    # red_flag keeps its single-shot production behavior — Phase 4 changes
    # classification/evidence logic, not retry mechanics.
    runner = TASK_RUNNERS[args.task]

def _write_checkpoint(path, task, model, policy_name, results, wall, complete):
    """Persist EVERY case's result as soon as it lands, not only once the
    whole batch finishes. 2026-09-01's real production run lost VEDL's and
    BAJFINANCE's already-completed, already-GPU-paid-for output when a
    LATER case (COALINDIA / APLLTD) crashed the process before this
    function existed — nothing was written until the end, so one case's
    failure discarded every earlier case's real work. Atomic write (temp
    file + os.replace) so a mid-write crash/kill can never leave a
    truncated/corrupt output file for writeback_*.py to trip over.
    """
    ok = sum(1 for r in results if r.get("ok"))
    tmp = path + ".tmp"
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump({"task": task, "model": model, "policy": policy_name,
                  "generated_ok": ok, "cases": len(results), "wall_sec": wall,
                  "complete": complete, "results": results},
                  fh, ensure_ascii=False, indent=2, default=str)
    os.replace(tmp, path)


results = []
t0 = time.time()
for i, case in enumerate(fs.cases, 1):
    bid = case.get("benchmark_id") or case.get("fixture_id") or case.get("filing_id") or case.get("chunk_id")
    print(f"  [{i}/{len(fs.cases)}] {bid}", flush=True)
    try:
        result = runner(backend, case, args.model)
        row = result.to_dict()
    except Exception as e:
        # A single case's crash (missing dependency, unhandled API error,
        # etc.) must not discard every earlier case's already-completed
        # result — see _write_checkpoint's docstring for exactly what this
        # fixes. Recorded as a normal failed case; the loop continues.
        import traceback
        tb = traceback.format_exc()
        print(f"    CASE FAILED: {type(e).__name__}: {e}", flush=True)
        row = {"ok": False, "error": f"{type(e).__name__}: {e}", "traceback": tb}
    row["case_id"] = bid
    from app.tasks.production_identity import attach_identity
    row = attach_identity(row, case)
    results.append(row)
    _write_checkpoint(args.output, args.task, args.model, policy.name,
                      results, time.time() - t0, complete=False)
wall = time.time() - t0

ok = sum(1 for r in results if r["ok"])
print(f"\ngenerated_ok: {ok}/{len(results)}   wall: {wall/60:.1f} min")

_write_checkpoint(args.output, args.task, args.model, policy.name,
                  results, wall, complete=True)
print(f"wrote {args.output}")
