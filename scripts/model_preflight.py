#!/usr/bin/env python3
"""GPU / model preflight. RUN THIS BEFORE ANY EVALUATION BATCH.

Reports, in order, and stops at the first hard failure:

  GPU count · GPU model · VRAM per GPU · total VRAM · CUDA version ·
  PyTorch version · inference-runtime version · model size · quantization ·
  model loading time · available VRAM after load · prompt token count ·
  output token count · generation latency · tokens/sec

OOM POLICY (founder instruction, 2026-08-28)
--------------------------------------------
On OOM this script:
  1. records the EXACT error text verbatim,
  2. prints the reduced-context retry it suggests,
  3. does NOT silently change model or quantization.
Switching model is a human decision, made with the recorded error in hand.

T4 REALITY CHECK
----------------
Kaggle gives 2x T4 (Turing, SM75, 16 GB each). No bf16, no FP8, no
FlashAttention-2. `dtype` must be float16 explicitly. Start with
`qwen3-14b-awq`; attempt `qwen3-30b-a3b-awq` only after that works.

USAGE
    python scripts/model_preflight.py --model qwen3-14b-awq
    python scripts/model_preflight.py --model qwen3-14b-awq --json out.json
    python scripts/model_preflight.py --inspect-only      # no weights loaded
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import sys
import time
import traceback
from datetime import datetime, timezone
from typing import Any, Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.registry import get_model_spec, list_models  # noqa: E402

PROMPT = (
    "Summarize, in two neutral sentences, what a corporate annual report's "
    "management discussion section typically covers. Use past or present "
    "tense only."
)


def section(title: str) -> None:
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")


def collect_hardware() -> Dict[str, Any]:
    info: Dict[str, Any] = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "gpu_count": 0,
        "gpus": [],
        "total_vram_gb": 0.0,
        "cuda_version": None,
        "torch_version": None,
        "torch_available": False,
    }
    try:
        import torch
        info["torch_available"] = True
        info["torch_version"] = torch.__version__
        info["cuda_version"] = torch.version.cuda
        info["cuda_available"] = torch.cuda.is_available()
        if torch.cuda.is_available():
            count = torch.cuda.device_count()
            info["gpu_count"] = count
            total = 0.0
            for index in range(count):
                props = torch.cuda.get_device_properties(index)
                vram_gb = props.total_memory / (1024 ** 3)
                total += vram_gb
                capability = f"{props.major}.{props.minor}"
                info["gpus"].append({
                    "index": index,
                    "name": props.name,
                    "vram_gb": round(vram_gb, 2),
                    "compute_capability": capability,
                    "supports_bf16": props.major >= 8,
                    "supports_flash_attn_2": props.major >= 8,
                })
            info["total_vram_gb"] = round(total, 2)
    except ImportError:
        info["error"] = "torch not installed — GPU inspection unavailable"
    return info


def collect_runtime() -> Dict[str, Any]:
    info: Dict[str, Any] = {"vllm_available": False, "vllm_version": None}
    try:
        import vllm
        info["vllm_available"] = True
        info["vllm_version"] = getattr(vllm, "__version__", "unknown")
    except ImportError:
        info["note"] = "vllm not installed — expected on a local dev machine"
    return info


def warn_on_hardware(hardware: Dict[str, Any], spec) -> List[str]:
    warnings: List[str] = []
    if not hardware.get("gpu_count"):
        warnings.append("No CUDA GPU detected — model load will not be attempted.")
        return warnings

    for gpu in hardware["gpus"]:
        if not gpu["supports_bf16"] and spec.dtype == "bfloat16":
            warnings.append(
                f"GPU {gpu['index']} ({gpu['name']}, SM{gpu['compute_capability']}) "
                "has no bf16 support but the spec requests bfloat16 — this WILL fail."
            )
        if gpu["compute_capability"].startswith("7."):
            warnings.append(
                f"GPU {gpu['index']} is Turing (SM{gpu['compute_capability']}): "
                "no bf16, no FP8, no FlashAttention-2. vLLM falls back to "
                "xformers — expected, not a defect."
            )

    needed = spec.approx_weights_gb
    available = hardware["total_vram_gb"]
    if spec.tensor_parallel_size > hardware["gpu_count"]:
        warnings.append(
            f"spec wants tensor_parallel_size={spec.tensor_parallel_size} but only "
            f"{hardware['gpu_count']} GPU(s) are present — this WILL fail."
        )
    if needed > available * 0.85:
        warnings.append(
            f"weights ~{needed} GB against {available} GB total VRAM leaves little "
            "room for the KV cache. KV cache, not weights, is the usual OOM cause."
        )
    if spec.is_moe and any(g["compute_capability"].startswith("7.") for g in hardware["gpus"]):
        warnings.append(
            "MoE model on Turing: quantized-MoE kernel coverage is the weakest "
            "combination in vLLM's support matrix. A failure here is a plausible "
            "outcome to record, not necessarily a fixable bug."
        )
    return warnings


def run_load_and_generate(spec, max_tokens: int) -> Dict[str, Any]:
    result: Dict[str, Any] = {"attempted": True, "loaded": False, "generated": False}
    try:
        from vllm import LLM, SamplingParams
    except ImportError:
        result.update({"attempted": False, "error": "vllm not installed"})
        return result

    section("MODEL LOAD")
    kwargs = spec.to_vllm_kwargs()
    print(json.dumps(kwargs, indent=2))

    started = time.perf_counter()
    try:
        llm = LLM(**kwargs)
    except Exception as exc:
        elapsed = time.perf_counter() - started
        error_text = f"{type(exc).__name__}: {exc}"
        result.update({
            "error": error_text,
            "traceback": traceback.format_exc(),
            "load_time_sec": round(elapsed, 2),
        })
        is_oom = "out of memory" in error_text.lower() or "OutOfMemory" in error_text
        section("LOAD FAILED — EXACT ERROR RECORDED VERBATIM")
        print(error_text)
        if is_oom:
            print(
                "\nOOM POLICY — do NOT silently switch model. Options, in order:\n"
                f"  1. Reduce context:  --max-model-len {max(2048, spec.max_model_len // 2)}\n"
                f"  2. Lower memory utilisation: --gpu-memory-utilization 0.85\n"
                f"  3. If TP={spec.tensor_parallel_size} on 1 GPU, try TP=2 to split weights\n"
                "  4. Only then, with this error recorded, consider the fallback model.\n"
            )
            result["oom"] = True
        return result

    load_time = time.perf_counter() - started
    result.update({"loaded": True, "load_time_sec": round(load_time, 2)})
    print(f"\nModel loaded in {load_time:.1f}s")

    try:
        import torch
        free_bytes, total_bytes = torch.cuda.mem_get_info(0)
        result["free_vram_gb_after_load"] = round(free_bytes / (1024 ** 3), 2)
        result["total_vram_gb_device0"] = round(total_bytes / (1024 ** 3), 2)
        print(f"Free VRAM on device 0 after load: {result['free_vram_gb_after_load']} GB")
    except Exception:
        pass

    section("GENERATION")
    try:
        tokenizer = llm.get_tokenizer()
        prompt_tokens = len(tokenizer.encode(PROMPT))
    except Exception:
        prompt_tokens = 0

    params = SamplingParams(temperature=0.0, max_tokens=max_tokens, seed=0)
    started = time.perf_counter()
    outputs = llm.generate([PROMPT], params)
    latency = time.perf_counter() - started

    text = outputs[0].outputs[0].text if outputs else ""
    try:
        completion_tokens = len(outputs[0].outputs[0].token_ids)
    except Exception:
        completion_tokens = len(text) // 4

    result.update({
        "generated": True,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "generation_latency_sec": round(latency, 3),
        "tokens_per_sec": round(completion_tokens / latency, 2) if latency > 0 else 0.0,
        "sample_output": text[:400],
    })
    print(f"Prompt tokens      : {prompt_tokens}")
    print(f"Completion tokens  : {completion_tokens}")
    print(f"Latency            : {latency:.3f}s")
    print(f"Tokens/sec         : {result['tokens_per_sec']}")
    print(f"\nSample output:\n{text[:400]}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="GPU / model preflight")
    parser.add_argument("--model", default="qwen3-14b-awq", choices=list_models())
    parser.add_argument("--max-tokens", type=int, default=128)
    parser.add_argument("--inspect-only", action="store_true",
                        help="report hardware and the plan; never load weights")
    parser.add_argument("--json", help="write the full report to this path")
    args = parser.parse_args()

    spec = get_model_spec(args.model)

    section("HARDWARE")
    hardware = collect_hardware()
    print(f"Python            : {hardware['python']}")
    print(f"Platform          : {hardware['platform']}")
    print(f"PyTorch           : {hardware['torch_version']}")
    print(f"CUDA              : {hardware['cuda_version']}")
    print(f"GPU count         : {hardware['gpu_count']}")
    for gpu in hardware["gpus"]:
        print(f"  [{gpu['index']}] {gpu['name']}  {gpu['vram_gb']} GB  "
              f"SM{gpu['compute_capability']}  bf16={gpu['supports_bf16']}  "
              f"flash_attn2={gpu['supports_flash_attn_2']}")
    print(f"Total VRAM        : {hardware['total_vram_gb']} GB")

    section("RUNTIME")
    runtime = collect_runtime()
    print(f"vLLM available    : {runtime['vllm_available']}")
    print(f"vLLM version      : {runtime['vllm_version']}")

    section("MODEL PLAN")
    print(f"Registry name     : {spec.name}")
    print(f"HF repo           : {spec.hf_repo}")
    print(f"Quantization      : {spec.quantization}")
    print(f"dtype             : {spec.dtype}")
    print(f"Tensor parallel   : {spec.tensor_parallel_size}")
    print(f"max_model_len     : {spec.max_model_len}")
    print(f"Approx weights    : {spec.approx_weights_gb} GB")
    print(f"MoE               : {spec.is_moe}")
    print(f"\nNotes: {spec.notes}")

    warnings = warn_on_hardware(hardware, spec)
    if warnings:
        section("WARNINGS")
        for warning in warnings:
            print(f"  ! {warning}")

    report: Dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "model_spec": {
            "hf_repo": spec.hf_repo, "quantization": spec.quantization,
            "dtype": spec.dtype, "tensor_parallel_size": spec.tensor_parallel_size,
            "max_model_len": spec.max_model_len, "is_moe": spec.is_moe,
            "approx_weights_gb": spec.approx_weights_gb,
        },
        "hardware": hardware,
        "runtime": runtime,
        "warnings": warnings,
    }

    if args.inspect_only:
        report["load_test"] = {"attempted": False, "reason": "--inspect-only"}
        print("\n--inspect-only: no weights loaded, no GPU time consumed.")
    elif not hardware.get("gpu_count"):
        report["load_test"] = {"attempted": False, "reason": "no CUDA GPU detected"}
        print("\nNo GPU detected — skipping load test. Run this on Kaggle.")
    else:
        report["load_test"] = run_load_and_generate(spec, args.max_tokens)

    section("VERDICT")
    load_test = report.get("load_test") or {}
    if load_test.get("generated"):
        print(f"PASS — {args.model} loaded and generated on this hardware.")
        print(f"       {load_test['tokens_per_sec']} tok/s, "
              f"{load_test['load_time_sec']}s load.")
        print("       Safe to proceed to an evaluation batch.")
    elif load_test.get("attempted"):
        print(f"FAIL — {args.model} did not run. Exact error recorded above and in the "
              "JSON report. Do NOT switch models silently; decide with the error in hand.")
    else:
        print(f"NOT TESTED — {load_test.get('reason')}")

    if args.json:
        os.makedirs(os.path.dirname(os.path.abspath(args.json)), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2, default=str)
        print(f"\nReport written to {args.json}")


if __name__ == "__main__":
    main()
