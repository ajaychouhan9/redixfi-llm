"""Model registry — short name -> HF repo + quantization + T4-safe serving args.

WHY A REGISTRY AND NOT A RAW REPO ID
------------------------------------
Kaggle's GPUs are 2x NVIDIA T4. T4 is Turing (compute capability 7.5), and
that single fact drives every serving argument in this file:

  * NO bfloat16. Turing has no bf16 datapath. Qwen3 checkpoints are
    bf16-native, so `dtype` MUST be float16 explicitly — letting vLLM infer
    the checkpoint dtype produces either a hard failure or a silent
    emulated-bf16 slowdown.
  * NO FP8, NO FlashAttention-2 (both need Ampere/SM80+). vLLM falls back
    to xformers on Turing automatically; this is expected, not a defect.
  * 16 GB VRAM per card, 32 GB total. A bf16 14B (~28 GB) or bf16 30B
    (~61 GB) does not fit. 4-bit AWQ is the only realistic path, and even
    then the KV cache, not the weights, is usually what OOMs first — hence
    the deliberately modest max_model_len defaults below.

MODEL ORDER IS A FOUNDER DECISION (2026-08-28)
----------------------------------------------
Validate the whole stack on `qwen3-14b-awq` FIRST. It is dense (no MoE
kernels), roughly 9 GB quantized, and comfortably fits one T4 — so a
failure there is a stack problem, not a capacity problem. Only once that
is proven should `qwen3-30b-a3b-awq` be attempted. Do not burn Kaggle
quota fighting the 30B first.

HONEST RISK ON THE 30B
----------------------
Qwen3-30B-A3B is a Mixture-of-Experts model. Quantized-MoE kernel support
on Turing is the weakest-covered combination in vLLM's support matrix. It
may simply not run on T4 regardless of how the memory arithmetic looks.
That is a real possibility the preflight is designed to discover cheaply,
and it is exactly why the fallback exists and why nothing in this project
depends on which of the two wins.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ModelSpec:
    name: str
    hf_repo: str
    quantization: Optional[str]
    dtype: str
    tensor_parallel_size: int
    max_model_len: int
    gpu_memory_utilization: float
    is_moe: bool
    approx_weights_gb: float
    notes: str
    extra_vllm_args: Dict[str, Any] = field(default_factory=dict)

    def to_vllm_kwargs(self) -> Dict[str, object]:
        kwargs: Dict[str, object] = {
            "model": self.hf_repo,
            "dtype": self.dtype,
            "tensor_parallel_size": self.tensor_parallel_size,
            "max_model_len": self.max_model_len,
            "gpu_memory_utilization": self.gpu_memory_utilization,
            "trust_remote_code": True,
        }
        if self.quantization:
            kwargs["quantization"] = self.quantization
        kwargs.update(self.extra_vllm_args)
        return kwargs

    def to_server_args(self) -> List[str]:
        """Command-line args for `vllm serve`, used by the Kaggle scripts."""
        args = [
            self.hf_repo,
            "--dtype", self.dtype,
            "--tensor-parallel-size", str(self.tensor_parallel_size),
            "--max-model-len", str(self.max_model_len),
            "--gpu-memory-utilization", str(self.gpu_memory_utilization),
            "--trust-remote-code",
        ]
        if self.quantization:
            args += ["--quantization", self.quantization]
        for key, value in self.extra_vllm_args.items():
            # dict/list values must cross the CLI as JSON. str() would emit a
            # Python repr with single quotes, which vLLM's parser rejects.
            rendered = (json.dumps(value) if isinstance(value, (dict, list))
                        else str(value))
            args += [f"--{key.replace('_', '-')}", rendered]
        return args


REGISTRY: Dict[str, ModelSpec] = {
    # ---- PRIMARY TARGET FOR FIRST PREFLIGHT (founder decision) ------------
    "qwen3-14b-awq": ModelSpec(
        name="qwen3-14b-awq",
        hf_repo="Qwen/Qwen3-14B-AWQ",
        quantization="awq",
        dtype="float16",           # Turing: NEVER bfloat16
        tensor_parallel_size=1,    # ~9 GB fits one T4; TP=1 avoids NCCL entirely
        max_model_len=16384,
        gpu_memory_utilization=0.90,
        is_moe=False,
        approx_weights_gb=9.0,
        notes=(
            "Dense, no MoE kernels, fits a single T4. Validate the full stack "
            "here before attempting the 30B. TP=1 deliberately: it removes "
            "multi-GPU NCCL as a variable while proving serving works. "
            "MEASURED against the real exported fixtures: fits red_flag (944), "
            "ask_ai (4,640) and the CURRENT annual_report_summary replay "
            "(16,291, just inside 16k). Does NOT fit concall_summary (19,308) "
            "or the legacy annual-report replay (62,456)."
        ),
    ),
    # ---- PHASE A variant: same weights, context headroom -------------------
    "qwen3-14b-awq-tp2": ModelSpec(
        name="qwen3-14b-awq-tp2",
        hf_repo="Qwen/Qwen3-14B-AWQ",
        quantization="awq",
        dtype="float16",
        tensor_parallel_size=2,
        max_model_len=32768,
        gpu_memory_utilization=0.90,
        is_moe=False,
        approx_weights_gb=9.0,
        notes=(
            "REQUIRED FOR concall_summary (max 19,308 tokens, over 16k). Same "
            "weights as qwen3-14b-awq, split across both T4s; splitting halves "
            "per-card KV cache, which is what makes 32k affordable on 16 GB "
            "cards at all. Also comfortably fits the current "
            "annual_report_summary replay. "
            "NOTE the earlier ~24,600-token estimate for Phase A came from "
            "local spike files with tiktoken installed; production's VM has NO "
            "tiktoken, so its Evidence Finder uses a len/2.5 fallback and "
            "selects ~45% fewer real tokens than its 20k budget implies. The "
            "real exported figure is 16,291."
        ),
    ),
    # ---- LEGACY ANNUAL-REPORT REPLAY ONLY: needs a 64k context ------------
    "qwen3-14b-awq-tp2-64k": ModelSpec(
        name="qwen3-14b-awq-tp2-64k",
        hf_repo="Qwen/Qwen3-14B-AWQ",
        quantization="awq",
        dtype="float16",
        tensor_parallel_size=2,
        max_model_len=65536,
        gpu_memory_utilization=0.90,
        is_moe=False,
        approx_weights_gb=9.0,
        # Qwen3-14B's NATIVE context is 32,768. 65,536 requires YaRN rope
        # scaling, which vLLM must be told about explicitly.
        extra_vllm_args={"rope_scaling": '{"rope_type":"yarn","factor":2.0,'
                                         '"original_max_position_embeddings":32768}'},
        notes=(
            "ONLY for the legacy annual-report replay. Measured on the real "
            "exported fixture, the legacy front-slice prompt needs 38,792-62,456 "
            "tokens (median 41,763) — 0 of 20 cases fit 32k, 20 of 20 fit 64k. "
            "VRAM arithmetic works (KV ~160 KB/token, 10.2 GB at 64k, ~5.1 GB per "
            "card at TP=2, plus ~4.5 GB of weights per card). "
            "TWO CAVEATS, both UNVALIDATED: this exceeds the model's native "
            "context so YaRN is required, and YaRN can degrade quality at long "
            "context — which would confound a quality benchmark. Preflight this "
            "separately and treat a poor result here as possibly the rope "
            "scaling, not the model."
        ),
    ),
    # ---- COMPARISON MODEL (founder request, 2026-08-29) -------------------
    "ministral3-14b-w4a16-tp2": ModelSpec(
        name="ministral3-14b-w4a16-tp2",
        # NOT an AutoAWQ checkpoint despite the repo name. Mistral publishes
        # no int4 build, and EVERY community int4 of this model is
        # compressed-tensors / pack-quantized. Verified by reading
        # quantization_config from each candidate repo, not from the name.
        hf_repo="cyankiwi/Ministral-3-14B-Instruct-2512-AWQ-4bit",
        quantization="compressed-tensors",
        dtype="float16",           # checkpoint is bfloat16; Turing has none
        tensor_parallel_size=2,
        max_model_len=32768,       # native is 262,144 — capped, see notes
        gpu_memory_utilization=0.90,
        is_moe=False,
        approx_weights_gb=9.7,
        # Text-only workload on a vision-language model. Without this, vLLM's
        # memory profiling reserves for dummy IMAGE inputs at image_size 1540,
        # which on a 14.5 GB card is a real OOM risk for capacity we never use.
        extra_vllm_args={
            "limit_mm_per_prompt": {"image": 0},
            # The preflight ran WITHOUT this and transformers warned:
            # "MistralCommonBackend.apply_chat_template(..., tokenize=False)
            # is unsafe and may lead to unexpected behavior". Rendering the
            # chat template to a string and re-encoding can produce a
            # different token sequence than Tekken intends, which for a
            # compliance benchmark means the model may not have been given
            # the prompt in the form it expects. "mistral" routes through
            # mistral-common directly, the model-correct path.
            # UNVALIDATED — added after the preflight, not yet run on GPU.
            "tokenizer_mode": "mistral",
        },
        notes=(
            "Ministral 3 14B Instruct (Mistral AI, Apache-2.0). Registered for "
            "a like-for-like comparison against qwen3-14b-awq-tp2. "
            "T4 VIABILITY, verified against the vLLM v0.28.0 SOURCE rather than "
            "assumed: CompressedTensorsConfig.get_min_capability()==70 and the "
            "W4A16 scheme's ==75, commented 'Turing and up'. The checkpoint is "
            "symmetric int4 (GPTQ-style uint4b8, no zero-point) at group_size "
            "32, and MARLIN_SUPPORTED_GROUP_SIZES is [-1,32,64,128] — so the "
            "Marlin path accepts it at capability 75. "
            "MULTIMODAL: architecture is Mistral3ForConditionalGeneration with "
            "a Pixtral vision tower, registered in vLLM 0.28.0. The vision "
            "tower is left UNQUANTIZED by the checkpoint (it is in the config's "
            "`ignore` list), which is part of why 9.7 GB is larger than a plain "
            "int4 13.5B. "
            "CONTEXT: native max_position_embeddings is 262,144. Capped to "
            "32,768 to match qwen3-14b-awq-tp2 exactly — the comparison must "
            "not differ by context window, and KV at 0.156 MB/token would be "
            "40 GB at full context. "
            "UNVALIDATED UNTIL THE PREFLIGHT RUNS: that Marlin int4 actually "
            "executes on Turing for THIS checkpoint, and that the Tekken "
            "tokenizer loads in HF mode. Treat a failure as a finding."
        ),
    ),
    # ---- STRETCH TARGET, ATTEMPT ONLY AFTER 14B IS PROVEN -----------------
    "qwen3-30b-a3b-awq": ModelSpec(
        name="qwen3-30b-a3b-awq",
        hf_repo="Qwen/Qwen3-30B-A3B-Instruct-2507-AWQ",
        quantization="awq",
        dtype="float16",
        tensor_parallel_size=2,    # needs both T4s
        # 32768 so Phase A fits. Qwen3-30B-A3B uses 4 KV heads (GQA), so KV
        # cache is ~96 KB/token — roughly 2.4 GB at 24k tokens, split across
        # two cards. Weights (~18 GB) dominate; the KV cache is affordable.
        # If this OOMs, drop to 16384 and run Phase A on qwen3-14b-awq-tp2.
        max_model_len=32768,
        gpu_memory_utilization=0.92,
        is_moe=True,
        approx_weights_gb=18.0,
        notes=(
            "30.5B total / ~3.3B active MoE. NON-THINKING model — do NOT design "
            "around <think> output. Quantized-MoE on Turing is the weakest "
            "combination in vLLM's support matrix; treat a failure here as an "
            "expected outcome to be recorded, not a bug to be forced."
        ),
    ),
}

# Which registry entry each evaluation phase should use, given the measured
# prompt sizes. run_evaluation.py's context check enforces this rather than
# trusting it, but stating it here keeps the Kaggle runbook honest.
RECOMMENDED_MODEL_BY_TASK = {
    # Measured against the REAL exported fixtures on 2026-08-28, not estimated.
    "concall_summary": "qwen3-14b-awq-tp2",              # max 19,308 -> needs >16k
    "annual_report_summary": "qwen3-14b-awq",            # max 16,291 -> fits 16k
    "annual_report_summary_legacy": "qwen3-14b-awq-tp2-64k",  # max 62,456 -> needs 64k
    "red_flag": "qwen3-14b-awq",                         # max 944
    "ask_ai": "qwen3-14b-awq",                           # max 4,640
}

DEFAULT_MODEL = "qwen3-14b-awq"


def get_model_spec(name: str) -> ModelSpec:
    key = (name or "").strip().lower()
    if key not in REGISTRY:
        available = ", ".join(sorted(REGISTRY))
        raise KeyError(f"unknown model '{name}'. Registered: {available}")
    return REGISTRY[key]


def list_models() -> List[str]:
    return sorted(REGISTRY)
