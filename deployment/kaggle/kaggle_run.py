#!/usr/bin/env python3
"""ONE-SHOT KAGGLE DEPLOYMENT + 15-CASE BENCHMARK.

Runs, in order, and STOPS at the first hard failure:

   1  environment + CUDA check          6  load model (preflight)
   2  detect both T4 GPUs               7  VRAM after load
   3  install inference runtime         8  start OpenAI-compatible server
   4  download Qwen3-14B-AWQ            9  verify /health and /v1/models
   5  record versions                  10  minimal inference smoke test
                                       11  the 15-case benchmark, then STOP

DESIGN RULES THIS SCRIPT OBEYS
------------------------------
* Qwen3-14B-AWQ at **32K context, TP=2, no YaRN** (founder decision).
* Fixtures are the ONLY data source. No Mongo, no ChromaDB, no RedixFi VM,
  no production API. This script opens no database connection at all.
* On model-load failure it records the EXACT error and STOPS. It never
  silently switches model, quantization, or context.
* On OOM it prints the documented ladder and stops for a human decision.
* It runs 15 cases and stops. It will not touch the remaining 115.
* GPU wall-clock is tracked and reported throughout.
* The project location is AUTO-DETECTED (see _find_project_root below) — it
  no longer assumes a manual staging command ran first, and no longer
  trusts a hardcoded /kaggle/working/LLM path. A prior run reached step 4
  with `ModuleNotFoundError: No module named 'app'` because that staging
  command silently extracted nothing when the dataset's layout changed.

USAGE — paste into a Kaggle notebook cell. Run it straight from wherever
the attached dataset mounts it; no staging cell is required first:

    !python /kaggle/input/<your-dataset>/llm_project/deployment/kaggle/kaggle_run.py \
        --fixtures /kaggle/input/<your-dataset>

(If the dataset happens to be mounted read-only under /kaggle/input, the
script copies itself to /kaggle/working/LLM automatically before doing
anything that needs to write — benchmark results are written there, not
back into the read-only mount.)

Add --skip-benchmark to do deployment + preflight only.
Add --repo-dir <path> only to override auto-detection.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

START = time.time()
STATE = {"steps": [], "gpu": {}, "preflight": {}, "benchmark": {}}


# ---------------------------------------------------------------------------
def elapsed() -> str:
    m, s = divmod(int(time.time() - START), 60)
    return f"{m:02d}m{s:02d}s"


def head(n, title):
    print(f"\n{'=' * 74}\n[{elapsed()}] STEP {n} — {title}\n{'=' * 74}", flush=True)


def ok(msg):
    print(f"  ✅ {msg}", flush=True)


def warn(msg):
    print(f"  ⚠️  {msg}", flush=True)


def die(step, msg, detail=""):
    """Record the exact failure and stop. Never fall back to another model."""
    print(f"\n{'!' * 74}\n  ❌ HARD STOP at step {step}: {msg}\n{'!' * 74}", flush=True)
    if detail:
        print(detail, flush=True)
    STATE["fatal"] = {"step": step, "error": msg, "detail": detail[:4000],
                      "gpu_minutes_used": round((time.time() - START) / 60, 2)}
    _save()
    print("\n  NO MODEL SUBSTITUTION WAS MADE. Report this error before changing "
          "any configuration.", flush=True)
    sys.exit(1)


def _save():
    try:
        with open("/kaggle/working/kaggle_run_state.json", "w") as fh:
            json.dump(STATE, fh, indent=2, default=str)
    except OSError:
        with open("kaggle_run_state.json", "w") as fh:
            json.dump(STATE, fh, indent=2, default=str)


def sh(cmd, check=True, quiet=False):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if not quiet and r.stdout.strip():
        print("  " + r.stdout.strip().replace("\n", "\n  "), flush=True)
    if check and r.returncode != 0:
        return None, r.stderr
    return r.stdout, r.stderr


# ---------------------------------------------------------------------------
# PROJECT LOCATION — never trust a hardcoded staging path.
#
# A prior run reached STEP 4 with `ModuleNotFoundError: No module named
# 'app'`. Root cause: this script used to unconditionally
# `sys.path.insert(0, "/kaggle/working/LLM")` and `os.chdir()` there,
# trusting that a manual `tar xzf ... -C /kaggle/working/LLM` cell in the
# runbook had staged the project first. When the dataset's shape changed
# (an already-extracted `llm_project/` directory instead of a
# `llm_project.tar.gz`), that staging command silently extracted nothing —
# `/kaggle/working/LLM` existed (from `mkdir -p`) but was EMPTY. Steps 1-3
# (CUDA check, GPU detection, runtime install) never import `app`, so
# nothing caught this until step 4's first `from app...` import, three
# steps and several minutes of log output away from the actual cause.
#
# Fixed the way the Step 3 mount-path guessing bug was fixed: stop
# hardcoding a path and locate the real one instead, verifying with a
# concrete file check rather than "the directory exists".
# ---------------------------------------------------------------------------
_MARKER = os.path.join("app", "models", "registry.py")
# Module-level so tests can monkeypatch them to a temp directory instead of
# real /kaggle/... paths, which do not exist off Kaggle.
_INPUT_PREFIX = "/kaggle/input"
_STAGING_DIR = "/kaggle/working/LLM"
_SEARCH_BASES = ("/kaggle/input", "/kaggle/working")


def _has_app(path) -> bool:
    return bool(path) and os.path.isfile(os.path.join(path, _MARKER))


def _find_project_root(explicit: str) -> str:
    """Returns a directory confirmed to contain the `app` package, or None.

    Tries, in order: an explicit `--repo-dir` (validated, not trusted
    blindly), this script's own location (`kaggle_run.py` lives at
    `<root>/deployment/kaggle/kaggle_run.py`, so two parents up IS the
    root whenever the script runs in place), the documented staging path,
    then a recursive search under _SEARCH_BASES as a last resort — the
    same "find it, don't guess it" fix that solved the Step 3
    dataset-mount-path problem.
    """
    if explicit:
        if _has_app(explicit):
            return os.path.abspath(explicit)
        warn(f"--repo-dir {explicit!r} has no {_MARKER} — ignoring it and searching")

    here_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for candidate in (here_root, _STAGING_DIR):
        if _has_app(candidate):
            return os.path.abspath(candidate)

    for base in _SEARCH_BASES:
        for hit in sorted(glob.glob(os.path.join(base, "**", _MARKER), recursive=True)):
            found = hit[: -(len(_MARKER) + 1)]
            return os.path.abspath(found)

    return None


def _resolve_project_root(explicit: str) -> str:
    """Finds the project, copies it to a writable location if it is on a
    read-only Kaggle input mount, and re-verifies AFTER the copy — so a
    bad copy fails here with a clear message, not three steps later on the
    first `from app...` import."""
    root = _find_project_root(explicit)
    if root is None:
        die(0, "could not locate the llm_project directory anywhere",
            f"Looked for {_MARKER} under:\n"
            f"  --repo-dir (if given): {explicit!r}\n"
            f"  this script's own location (two parents up)\n"
            f"  {_STAGING_DIR}\n"
            f"  a recursive search under {', '.join(_SEARCH_BASES)}\n\n"
            "This means the dataset was not attached, or its internal layout "
            "changed again. Check the notebook's Input panel and adjust "
            "--fixtures / --repo-dir to match — do not restage blindly.")

    # /kaggle/input is READ-ONLY. The benchmark step writes results under
    # evaluation/*/runs using paths relative to os.chdir(root), so running
    # in place would fail with a read-only-filesystem error the first time
    # anything tries to save. Copy once, up front, rather than discovering
    # this mid-benchmark after weight download and model load already
    # spent the real GPU time.
    if root.startswith(_INPUT_PREFIX):
        writable = _STAGING_DIR
        print(f"  {root} is on a read-only input mount — copying to {writable}",
              flush=True)
        if os.path.isdir(writable):
            shutil.rmtree(writable)
        shutil.copytree(root, writable)
        root = writable

    if not _has_app(root):
        die(0, f"copied project to {root} but {_MARKER} is still missing",
            f"contents: {os.listdir(root) if os.path.isdir(root) else '(not a directory)'}")

    return root


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-dir", default=None,
                    help="path to llm_project. Auto-detected by default — "
                         "see _find_project_root(); only pass this to force "
                         "a specific location.")
    ap.add_argument("--fixtures", default="/kaggle/input/redixfi-llm-fixtures")
    ap.add_argument("--model", default="qwen3-14b-awq-tp2",
                    help="32K, TP=2, no YaRN — the approved config for this phase")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--runtime", default="auto",
                    choices=["auto", "vllm", "transformers"],
                    help="auto tries vLLM then falls back to Transformers+AWQ")
    ap.add_argument("--skip-benchmark", action="store_true")
    ap.add_argument("--smoke", action="store_true",
                    help="GUIDED-DECODING SMOKE RUN: one case per category (4 "
                         "total) to confirm structured output works on real "
                         "hardware before committing quota to the full set")
    ap.add_argument("--limit-per-task", type=int, default=None,
                    help="cap cases per benchmark (--smoke implies 1)")
    ap.add_argument("--server-timeout", type=int, default=1800)
    args = ap.parse_args()

    repo_dir = _resolve_project_root(args.repo_dir)

    # Belt-and-suspenders: _resolve_project_root() cannot currently return a
    # path that doesn't exist (every branch either verifies a marker file
    # first or shutil.copytree's one into existence), but a bare os.chdir()
    # on a bad path raises a raw, undiagnosable FileNotFoundError — exactly
    # what happened when a STALE kaggle_run.py (predating this whole
    # auto-detection fix) was executed from an old dataset snapshot and fell
    # through to its old hardcoded `args.repo_dir` default of
    # "/kaggle/working/LLM", which nothing had created. Checking explicitly
    # here means ANY future regression of that kind — including "the code
    # running on Kaggle is not actually this version" — dies with a clear,
    # actionable message instead of a bare traceback three lines in.
    if not os.path.isdir(repo_dir):
        die(0, f"resolved project root does not exist: {repo_dir}",
            "This should be impossible given the current _resolve_project_root() "
            "logic. If you see this, the code actually executing on Kaggle is "
            "NOT this version of kaggle_run.py — re-clone/re-upload the latest "
            "commit rather than reusing a cached dataset or notebook copy.")

    sys.path.insert(0, repo_dir)
    os.chdir(repo_dir)
    print(f"[{elapsed()}] project root: {repo_dir}", flush=True)
    STATE["repo_dir"] = repo_dir

    # Verify import ACTUALLY works from here, before anything else runs —
    # this is what turns a ModuleNotFoundError three steps from now into a
    # clear failure at the very first opportunity.
    try:
        import app.models.registry  # noqa: F401
    except ImportError as exc:
        die(0, f"app package still not importable from {repo_dir} after path setup",
            f"{type(exc).__name__}: {exc}")
    ok("app package imports cleanly from the resolved project root")

    # Same principle applied to --fixtures: a wrong path here does NOT
    # raise later — the benchmark loop (step 10) only `warn()`s and skips a
    # category whose file is missing, which would otherwise let a
    # mis-mounted dataset "succeed" with zero cases in every category,
    # burning the model-load GPU cost for a run that measured nothing.
    # Checked here, before that cost is spent, unless the benchmark itself
    # is being skipped.
    if not args.skip_benchmark:
        expected = ["annual_report_sample15.json", "concall_sample15.json",
                    "red_flag_sample15.json", "ask_ai_sample15.json"]
        missing = [f for f in expected
                  if not os.path.isfile(os.path.join(args.fixtures, f))]
        if missing:
            hits = sorted(glob.glob(os.path.join("/kaggle/input", "**", expected[0]),
                                    recursive=True))
            die(0, f"--fixtures {args.fixtures!r} is missing {missing}",
                "Found matching files elsewhere:\n  " +
                ("\n  ".join(hits) if hits else "(none found under /kaggle/input either)"))
        ok(f"all 4 sample15 fixtures found under {args.fixtures}")

    # -- 1 ------------------------------------------------------------------
    head(1, "ENVIRONMENT + CUDA")
    print(f"  python : {sys.version.split()[0]}")
    out, _ = sh("nvidia-smi --query-gpu=index,name,memory.total,compute_cap "
                "--format=csv,noheader", check=False)
    if not out:
        die(1, "no GPU detected — set Accelerator = GPU T4 x2 in notebook settings")

    # -- 2 ------------------------------------------------------------------
    head(2, "GPU DETECTION")
    try:
        import torch
    except ImportError:
        die(2, "torch not available in the Kaggle image")
    if not torch.cuda.is_available():
        die(2, "torch.cuda.is_available() is False")

    gpus = []
    for i in range(torch.cuda.device_count()):
        p = torch.cuda.get_device_properties(i)
        gpus.append({"index": i, "name": p.name,
                     "vram_gb": round(p.total_memory / 1024**3, 2),
                     "compute_capability": f"{p.major}.{p.minor}",
                     "supports_bf16": p.major >= 8})
        print(f"  [{i}] {p.name}  {gpus[-1]['vram_gb']} GB  "
              f"SM{gpus[-1]['compute_capability']}  bf16="
              f"{'yes' if p.major >= 8 else 'NO (Turing — float16 is pinned)'}")
    STATE["gpu"] = {"count": len(gpus), "gpus": gpus,
                    "name": gpus[0]["name"] if gpus else None,
                    "total_vram_gb": round(sum(g["vram_gb"] for g in gpus), 2),
                    "cuda": torch.version.cuda, "torch": torch.__version__}
    ok(f"{len(gpus)} GPU(s), {STATE['gpu']['total_vram_gb']} GB total, "
       f"CUDA {torch.version.cuda}, torch {torch.__version__}")
    if len(gpus) < 2:
        die(2, f"{args.model} needs tensor_parallel_size=2 but only "
               f"{len(gpus)} GPU is present")

    # -- 3 ------------------------------------------------------------------
    head(3, "INFERENCE RUNTIME")
    # MEASURED ON THIS IMAGE (2026-08-28), not assumed:
    #   driver 580.159.04 -> CUDA 13 IS supported by the driver
    #   torch 2.10.0+cu128, transformers 5.0.0, autoawq importable, 2x T4
    #
    # vLLM's wheels are compiled against CUDA 13 (`vllm._C_stable_libtorch`
    # -> libcudart.so.13). Releases 0.20-0.28 all ship that ABI, so pinning
    # torch to a cu128 build does NOT help - proven on 0.26.0/0.25.1/0.24.0.
    #
    # WHY THIS RE-EXECS. A previous run installed the CUDA 13 runtime libs
    # and verified `import vllm` in a SUBPROCESS, which passed - then the
    # main process still died at `from vllm import LLM`. The subprocess
    # imported torch AFTER the libs were installed, so it picked up their
    # .so paths; the main process had imported torch at step 2, BEFORE they
    # existed, and could never see them. A subprocess probe therefore proves
    # nothing about this process. The only honest check is to install and
    # then re-exec, so the decision is made by a fresh interpreter.
    #
    # A runtime fallback is NOT a model switch: same weights, same AWQ
    # quantization, same 32K context. It is recorded in the run state and
    # printed in every report so no result is read without it.
    runtime = None
    forced = (args.runtime or "auto").lower()

    def _probe_vllm():
        try:
            import vllm  # noqa: F401
            return vllm.__version__
        except Exception as exc:
            STATE["vllm_import_error"] = f"{type(exc).__name__}: {exc}"
            return None

    if forced == "transformers":
        runtime = "transformers"
        print("  --runtime transformers: skipping vLLM entirely", flush=True)
    else:
        version = _probe_vllm()
        if version:
            runtime = "vllm"
            ok(f"vllm importable in THIS process: {version}")
        elif os.environ.get("_VLLM_INSTALL_TRIED") == "1":
            # Already installed and re-exec'd once; it still cannot import.
            warn(f"vLLM still unusable after install + re-exec: "
                 f"{STATE.get('vllm_import_error')}")
            if forced == "vllm":
                die(3, "vLLM required by --runtime vllm but not importable",
                    STATE.get("vllm_import_error", ""))
            runtime = "transformers"
        else:
            print("  installing vLLM + CUDA 13 runtime libs, then re-executing...",
                  flush=True)
            sh("pip install -q --no-cache-dir vllm", check=False, quiet=True)
            # Separately: one bad package name in a combined install silently
            # kills the whole command, which cost an earlier diagnostic.
            for pkg in ("nvidia-cuda-runtime-cu13", "nvidia-cublas-cu13",
                        "nvidia-cuda-nvrtc-cu13"):
                sh(f"pip install -q --no-cache-dir {pkg}", check=False, quiet=True)
            os.environ["_VLLM_INSTALL_TRIED"] = "1"
            _save()
            print("  re-executing with a fresh interpreter...", flush=True)
            os.execv(sys.executable, [sys.executable] + sys.argv)

    if runtime == "transformers":
        print("\n  --- RUNTIME: in-process Transformers + AWQ ---", flush=True)
        print("  Same model, same AWQ quantization, same 32K context.", flush=True)
        print("  Trade-offs that affect SPEED, not output quality:", flush=True)
        print("    * single-stream (no continuous batching) -> tok/s is a FLOOR", flush=True)
        print("    * device_map='auto' shards layers across both T4s (pipeline,", flush=True)
        print("      not tensor parallel) -> slower than a served deployment", flush=True)
        print("    * no guided JSON mode -> json_repair_used tracks any reliance", flush=True)
        sh("pip install -q --no-cache-dir autoawq accelerate", check=False, quiet=True)

    STATE["runtime"] = runtime
    STATE["gpu"]["runtime"] = runtime
    ok(f"runtime selected: {runtime}")
    _save()

    sh("pip install -q --no-cache-dir tiktoken", check=False, quiet=True)

    # -- 4 ------------------------------------------------------------------
    head(4, "MODEL PREFLIGHT - download, load, measure (the first real GPU spend)")
    from app.models.registry import get_model_spec
    spec = get_model_spec(args.model)
    print(f"  runtime      : {runtime}")
    print(f"  repo         : {spec.hf_repo}")
    print(f"  quantization : {spec.quantization}   dtype: {spec.dtype}")
    print(f"  tensor par.  : {spec.tensor_parallel_size}")
    print(f"  context      : {spec.max_model_len}")
    if spec.extra_vllm_args:
        die(4, f"{args.model} carries rope-scaling args ({spec.extra_vllm_args}); "
               "this phase is explicitly 32K WITHOUT YaRN")

    free_before = torch.cuda.mem_get_info(0)[0] / 1024**3
    backend = None
    llm = None
    SamplingParams = None
    t0 = time.time()

    if runtime == "vllm":
        from vllm import LLM, SamplingParams
        try:
            llm = LLM(**spec.to_vllm_kwargs())
        except Exception as exc:
            text = f"{type(exc).__name__}: {exc}"
            import traceback
            tb = traceback.format_exc()
            if "out of memory" in text.lower() or "OutOfMemory" in text:
                print("\n  OOM LADDER - apply IN ORDER, reporting each result:")
                print(f"    1. --max-model-len {max(4096, spec.max_model_len // 2)}")
                print("    2. --gpu-memory-utilization 0.85")
                print("    3. only then reconsider, with this error in hand")
                print("  DO NOT switch model or quantization to make this pass.")
            die(4, f"model load failed (vllm): {text}", tb)
    else:
        os.environ["LLM_BACKEND"] = "transformers"
        os.environ["LLM_MODEL"] = args.model
        from app.config.settings import get_settings
        from app.inference.factory import build_backend
        get_settings(refresh=True)
        backend = build_backend()
        try:
            meta = backend.load()
            print(f"  device_map   : {meta.get('device_map')}")
        except Exception as exc:
            text = f"{type(exc).__name__}: {exc}"
            import traceback
            tb = traceback.format_exc()
            if "out of memory" in text.lower():
                print("\n  OOM LADDER - apply IN ORDER, reporting each result:")
                print(f"    1. reduce context to {max(4096, spec.max_model_len // 2)}")
                print("    2. constrain with max_memory per device")
                print("    3. only then reconsider, with this error in hand")
                print("  DO NOT switch model or quantization to make this pass.")
            die(4, f"model load failed (transformers): {text}", tb)

    load_time = time.time() - t0
    free_after = torch.cuda.mem_get_info(0)[0] / 1024**3
    ok(f"loaded in {load_time:.1f}s")

    head(5, "VRAM AFTER LOAD")
    vram = []
    for i in range(torch.cuda.device_count()):
        free, total = torch.cuda.mem_get_info(i)
        used = (total - free) / 1024**3
        vram.append({"index": i, "used_gb": round(used, 2),
                     "free_gb": round(free / 1024**3, 2),
                     "total_gb": round(total / 1024**3, 2)})
        print(f"  [{i}] used {used:.2f} GB / {total/1024**3:.2f} GB  "
              f"(free {free/1024**3:.2f} GB)")
    STATE["preflight"] = {"runtime": runtime, "model": args.model,
                          "hf_repo": spec.hf_repo,
                          "quantization": spec.quantization, "dtype": spec.dtype,
                          "tensor_parallel_size": spec.tensor_parallel_size,
                          "context_length": spec.max_model_len,
                          "load_time_sec": round(load_time, 2),
                          "free_vram_gb_before": round(free_before, 2),
                          "free_vram_gb_after": round(free_after, 2),
                          "vram_per_gpu": vram}
    _save()

    # -- 6 ------------------------------------------------------------------
    head(6, "GENERATION SMOKE TEST")
    prompt = ("Summarize, in two neutral sentences, what a corporate annual "
              "report's management discussion section typically covers. Use "
              "past or present tense only.")
    from app.inference.base import GenerationRequest, Message

    if runtime == "vllm":
        try:
            p_tokens = len(llm.get_tokenizer().encode(prompt))
        except Exception:
            p_tokens = 0
        t0 = time.time()
        outs = llm.generate([prompt], SamplingParams(temperature=0.0,
                                                     max_tokens=128, seed=0))
        lat = time.time() - t0
        text = outs[0].outputs[0].text if outs else ""
        try:
            c_tokens = len(outs[0].outputs[0].token_ids)
        except Exception:
            c_tokens = len(text) // 4
    else:
        res = backend.generate(GenerationRequest(
            messages=[Message("user", prompt)], model=args.model,
            temperature=0.0, max_tokens=128, seed=0))
        if not res.ok:
            die(6, f"smoke generation failed: {res.error}")
        text, lat = res.text, res.latency_sec
        p_tokens, c_tokens = res.prompt_tokens, res.completion_tokens

    tps = c_tokens / lat if lat else 0
    print(f"  prompt {p_tokens} tok - output {c_tokens} tok - {lat:.2f}s - {tps:.1f} tok/s")
    print(f"  sample: {text[:300]}")
    STATE["preflight"].update({"smoke_prompt_tokens": p_tokens,
                               "smoke_output_tokens": c_tokens,
                               "smoke_latency_sec": round(lat, 3),
                               "smoke_tokens_per_sec": round(tps, 2),
                               "smoke_output": text[:1000]})
    if not text.strip():
        die(6, "model loaded but generated empty output")
    ok("generation works")
    _save()

    # -- 7/8/9 --------------------------------------------------------------
    head(7, "OpenAI-COMPATIBLE API (serving the already-loaded engine)")
    # NO SECOND LOAD. Measured on this hardware: a load costs ~244 s and
    # leaves 0.43 GB free per card, so spawning `vllm serve` would mean
    # paying that twice and risking OOM. Both runtimes are wrapped by a
    # Backend and served through app/api/server.py instead - same
    # /v1/chat/completions, /v1/models and /health over real HTTP.
    import threading
    import uvicorn
    from app.api.server import create_app

    if runtime == "vllm":
        from app.inference.vllm_inprocess import VLLMInProcessBackend
        backend = VLLMInProcessBackend(llm, args.model)
        ok("wrapped the in-process vLLM engine (no second load)")
    else:
        ok("using the in-process Transformers backend")

    os.environ["LLM_MODEL"] = args.model
    api_app = create_app()
    api_app.state.backend = backend   # inject; do NOT let it build a second one
    cfg = uvicorn.Config(api_app, host="127.0.0.1", port=args.port,
                         log_level="warning")
    srv = uvicorn.Server(cfg)
    threading.Thread(target=srv.run, daemon=True).start()
    deadline = time.time() + 120
    while time.time() < deadline and not srv.started:
        time.sleep(1)
    if not srv.started:
        die(7, "in-process API server did not start within 120s")
    ok(f"OpenAI-compatible API serving on port {args.port}")

    base = f"http://127.0.0.1:{args.port}/v1"

    head(8, "VERIFY /v1/models AND /health")
    with urllib.request.urlopen(f"{base}/models", timeout=15) as r:
        served = [m["id"] for m in json.loads(r.read()).get("data", [])]
    print(f"  /v1/models -> {served}")
    if args.model not in served:
        die(8, f"served model ids {served} do not include {args.model}")
    ok("/v1/models correct")

    with urllib.request.urlopen(
            f"http://127.0.0.1:{args.port}/health", timeout=15) as r:
        hj = json.loads(r.read())
    print(f"  /health -> status={hj.get('status')} "
          f"experimental={hj.get('experimental')} "
          f"integrated_into_redixfi={hj.get('integrated_into_redixfi')}")
    if hj.get("status") != "ok":
        die(8, f"/health reported {hj.get('status')}")
    if hj.get("integrated_into_redixfi") is not False:
        die(8, "/health must report integrated_into_redixfi=false")
    ok("/health correct")
    STATE["api"] = {"models": served, "health": hj.get("status"),
                    "experimental": hj.get("experimental")}

    head(9, "MINIMAL INFERENCE SMOKE TEST THROUGH THE HTTP API")
    body = json.dumps({
        "model": args.model,
        "messages": [{"role": "system", "content": "Reply with JSON only."},
                     {"role": "user",
                      "content": 'Return {"ok": true} and nothing else.'}],
        "temperature": 0, "max_tokens": 48,
        "response_format": {"type": "json_object"},
    }).encode()
    req = urllib.request.Request(f"{base}/chat/completions", data=body,
                                 headers={"Content-Type": "application/json"},
                                 method="POST")
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=300) as r:
        payload = json.loads(r.read())
    api_lat = time.time() - t0
    content = payload["choices"][0]["message"]["content"]
    usage = payload.get("usage", {})
    print(f"  -> {content[:200]!r}")
    print(f"     {api_lat:.2f}s - {usage.get('prompt_tokens')}/"
          f"{usage.get('completion_tokens')} tokens")
    if not content.strip():
        die(9, "API smoke test returned empty content")
    ok("HTTP API smoke test passed")
    STATE["preflight"]["api_smoke_latency_sec"] = round(api_lat, 3)
    _save()

    if args.skip_benchmark:
        print(f"\n[{elapsed()}] --skip-benchmark set. Deployment verified; "
              "no benchmark run.")
        _save()
        return

    # -- 10 -----------------------------------------------------------------
    per_task = 1 if args.smoke else args.limit_per_task
    label = ("GUIDED-DECODING SMOKE RUN (1 case per category)" if args.smoke
             else "15-CASE BENCHMARK (small sample — STOPS after this)")
    head(10, label)
    if args.smoke:
        print("  Purpose: confirm structured output works on THIS hardware.", flush=True)
        print("  Success = structured_output_used equals the case count AND", flush=True)
        print("            json_repair_used is 0. Anything else means guided", flush=True)
        print("            decoding is not actually engaging — do NOT spend", flush=True)
        print("            quota on the full run until it is.", flush=True)
    from app.evaluation import fixtures as fx
    from app.evaluation import report as report_mod
    from app.evaluation.runner import run_evaluation, save_run

    jobs = [
        ("annual_report_sample15.json", "annual_report_summary", "evaluation/annual_report/runs"),
        ("concall_sample15.json",       "concall_summary",       "evaluation/concall/runs"),
        ("red_flag_sample15.json",      "red_flag",              "evaluation/red_flags/runs"),
        ("ask_ai_sample15.json",        "ask_ai",                "evaluation/ask_ai/runs"),
    ]
    bench_start = time.time()
    totals = {"cases": 0, "ok": 0, "failed": 0,
              "prompt_tokens": 0, "completion_tokens": 0, "latency": 0.0,
              "structured_output_used": 0, "json_repair_used": 0,
              "guided_and_clean": 0, "guided_but_repaired": 0, "unguided": 0}

    for fname, task, outdir in jobs:
        path = os.path.join(args.fixtures, fname)
        if not os.path.exists(path):
            warn(f"missing fixture {path} — skipping {task}")
            continue
        fs = fx.load(path)
        print(f"\n  --- {task}: {len(fs.cases)} cases ---", flush=True)

        run = run_evaluation(
            backend, fs, args.model, temperature=0.0, max_tokens=1024, seed=0,
            limit=per_task,
            replay_as=task, gpu=dict(STATE["gpu"], **{
                "context_length": spec.max_model_len,
                "quantization": spec.quantization}),
            progress=lambda i, n, bid: print(f"    [{i}/{n}] {bid}", flush=True))

        jpath = save_run(run, outdir)
        report_mod.save(run, jpath.replace(".json", ".md"), max_cases=25)

        s = run["summary"]
        totals["cases"] += s["cases"]
        totals["ok"] += s["generated_ok"]
        totals["failed"] += s["generation_failures"]
        totals["prompt_tokens"] += s["total_prompt_tokens"]
        totals["completion_tokens"] += s["total_completion_tokens"]
        totals["latency"] += s["mean_latency_sec"] * s["cases"]
        for key in ("structured_output_used", "json_repair_used",
                    "guided_and_clean", "guided_but_repaired", "unguided"):
            totals[key] += s.get(key, 0)
        for k, v in s.items():
            print(f"      {k:34s} {v}")
        print(f"      review sheet -> {jpath.replace('.json', '.md')}")

    bench_time = time.time() - bench_start
    tps = totals["completion_tokens"] / bench_time if bench_time else 0
    per_case = bench_time / totals["cases"] if totals["cases"] else 0
    STATE["benchmark"] = dict(
        totals, wall_sec=round(bench_time, 1),
        sec_per_case=round(per_case, 2),
        output_tokens_per_sec=round(tps, 2),
        cases_per_hour=round(3600 / per_case, 1) if per_case else 0,
        capacity_25_gpu_hours=round(25 * 3600 / per_case) if per_case else 0)

    head(11, "SUMMARY")
    print(f"  cases            : {totals['ok']}/{totals['cases']} generated "
          f"({totals['failed']} failures)")
    print()
    print("  --- GUIDED DECODING SCORECARD (the point of this run) ---")
    print(f"  structured_output_used : {totals['structured_output_used']}/{totals['cases']}")
    print(f"  json_repair_used       : {totals['json_repair_used']}/{totals['cases']}"
          "   <- target 0")
    print(f"  guided_and_clean       : {totals['guided_and_clean']}/{totals['cases']}"
          "   <- target = case count")
    print(f"  guided_but_repaired    : {totals['guided_but_repaired']}"
          "   <- non-zero means the grammar is not holding")
    print(f"  unguided               : {totals['unguided']}"
          "   <- non-zero means the schema never reached the engine")
    if totals["cases"]:
        if totals["guided_and_clean"] == totals["cases"]:
            print("  VERDICT: guided decoding is WORKING on this hardware.")
        else:
            print("  VERDICT: guided decoding did NOT fully engage — investigate "
                  "before spending quota on the full run.")
    print()
    print(f"  benchmark wall   : {bench_time/60:.1f} min "
          f"({per_case:.1f}s per case)")
    print(f"  output tok/s     : {tps:.1f}")
    print(f"  throughput       : {STATE['benchmark']['cases_per_hour']} cases/hour")
    print(f"  25 GPU-h capacity: ~{STATE['benchmark']['capacity_25_gpu_hours']:,} cases")
    print(f"  TOTAL GPU TIME   : {elapsed()}")
    _save()

    print("\n  STOPPING AS INSTRUCTED. The remaining 115 cases were NOT run.")
    print("  Download before the session ends:")
    print(f"    !cd {repo_dir} && zip -r /kaggle/working/eval_results.zip "
          "evaluation/ && cp /kaggle/working/kaggle_run_state.json /kaggle/working/")
    # The API runs on a daemon thread and the engine lives in this process,
    # so returning from main() releases the GPU. Nothing to terminate.
    ok("run complete — GPU released on process exit")


if __name__ == "__main__":
    main()
