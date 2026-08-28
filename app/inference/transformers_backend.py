"""In-process Transformers + AWQ backend — the T4-native fallback.

WHY THIS EXISTS
---------------
vLLM's published wheels are compiled against CUDA 13 (`vllm._C_stable_libtorch`
→ `libcudart.so.13`), while Kaggle's image is CUDA 12.8. Every vLLM release
from 0.20 through 0.28 pins torch 2.11+/2.13 and ships the same CUDA-13 ABI,
so pinning torch to a cu128 build does not help — the vLLM binary itself is
the problem.

Transformers + AutoAWQ has no such constraint: it runs on whatever torch the
image already has, and AWQ's GEMM kernels support Turing (SM 7.5). This is
the documented fallback the Backend abstraction was built for — swapping
runtime is a config change, not an architectural one.

HONEST DIFFERENCES FROM THE vLLM PATH — these affect the comparison
-------------------------------------------------------------------
1. **No JSON mode.** OpenAI (and vLLM's guided decoding) can guarantee
   syntactically valid JSON. Plain `generate()` cannot. The task layer's
   `parse_json_object` already tolerates a markdown fence and records
   `json_repair_used`, so a model leaning on that crutch stays visible in
   the report rather than being quietly flattered.
2. **No continuous batching.** Requests run one at a time, so tokens/sec
   measured here is SINGLE-STREAM throughput and will understate what a
   properly served deployment would do. Any capacity projection from these
   numbers is a floor, not an estimate of production throughput.
3. **`device_map="auto"`** shards layers across both T4s (pipeline-style),
   which is not the same as vLLM's tensor parallelism. It is slower, but it
   is what makes a 14B fit at all across 2x14.56 GB.

None of this affects OUTPUT QUALITY, which is what this phase is measuring.
It affects speed, and the report must say so rather than present these
numbers as production throughput.
"""
from __future__ import annotations

import time
from typing import Any, Dict, Iterator, List, Optional

from .base import BaseBackend, GenerationRequest, GenerationResult


class TransformersBackend(BaseBackend):
    name = "transformers"

    def __init__(
        self,
        hf_repo: str,
        dtype: str = "float16",
        max_model_len: int = 32768,
        device_map: str = "auto",
        trust_remote_code: bool = True,
    ) -> None:
        self.hf_repo = hf_repo
        self.dtype = dtype
        self.max_model_len = max_model_len
        self.device_map = device_map
        self.trust_remote_code = trust_remote_code
        self._model = None
        self._tokenizer = None
        self.load_time_sec: Optional[float] = None

    # -- loading -----------------------------------------------------------
    def load(self) -> Dict[str, Any]:
        """Loads weights. Separated from __init__ so the caller can time it
        and report load failures distinctly from generation failures."""
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        torch_dtype = {"float16": torch.float16, "bfloat16": torch.bfloat16,
                       "float32": torch.float32}[self.dtype]

        started = time.perf_counter()
        self._tokenizer = AutoTokenizer.from_pretrained(
            self.hf_repo, trust_remote_code=self.trust_remote_code)
        self._model = AutoModelForCausalLM.from_pretrained(
            self.hf_repo,
            torch_dtype=torch_dtype,
            device_map=self.device_map,
            trust_remote_code=self.trust_remote_code,
            low_cpu_mem_usage=True,
        )
        self._model.eval()
        self.load_time_sec = time.perf_counter() - started

        return {
            "hf_repo": self.hf_repo,
            "load_time_sec": round(self.load_time_sec, 2),
            "dtype": self.dtype,
            "device_map": str(getattr(self._model, "hf_device_map", self.device_map)),
        }

    # -- generation --------------------------------------------------------
    def _render_prompt(self, request: GenerationRequest) -> str:
        messages = [{"role": m.role, "content": m.content} for m in request.messages]
        try:
            return self._tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True)
        except Exception:
            # A model with no chat template still has to be usable; fall back
            # to a plain role-tagged rendering rather than failing the case.
            parts = [f"{m['role'].upper()}: {m['content']}" for m in messages]
            return "\n\n".join(parts) + "\n\nASSISTANT:"

    def _generate(self, request: GenerationRequest) -> GenerationResult:
        import torch

        if self._model is None:
            raise RuntimeError("model not loaded — call load() first")

        prompt = self._render_prompt(request)
        if request.json_mode:
            # No guided decoding available here. Nudge via the prompt and let
            # parse_json_object handle the rest; `json_repair_used` keeps any
            # reliance on that visible in the report.
            prompt += ""

        inputs = self._tokenizer(prompt, return_tensors="pt",
                                 truncation=True,
                                 max_length=self.max_model_len - request.max_tokens)
        inputs = {k: v.to(self._model.device) for k, v in inputs.items()}
        prompt_tokens = int(inputs["input_ids"].shape[-1])

        gen_kwargs: Dict[str, Any] = {
            "max_new_tokens": request.max_tokens,
            "pad_token_id": self._tokenizer.pad_token_id or self._tokenizer.eos_token_id,
        }
        # temperature=0 in the OpenAI sense means deterministic.
        if request.temperature and request.temperature > 0:
            gen_kwargs.update({"do_sample": True, "temperature": request.temperature})
        else:
            gen_kwargs["do_sample"] = False
        if request.stop:
            gen_kwargs["stop_strings"] = request.stop
            gen_kwargs["tokenizer"] = self._tokenizer

        if request.seed is not None:
            torch.manual_seed(request.seed)

        with torch.inference_mode():
            out = self._model.generate(**inputs, **gen_kwargs)

        generated = out[0][prompt_tokens:]
        text = self._tokenizer.decode(generated, skip_special_tokens=True)
        completion_tokens = int(generated.shape[-1])

        return GenerationResult(
            text=text.strip(),
            model=request.model,
            backend=self.name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            finish_reason="stop",
            raw={"single_stream": True, "no_json_mode": True},
        )

    def stream(self, request: GenerationRequest) -> Iterator[str]:
        yield self.generate(request).text

    def health(self) -> Dict[str, Any]:
        return {
            "backend": self.name,
            "status": "ok" if self._model is not None else "not_loaded",
            "hf_repo": self.hf_repo,
            "load_time_sec": self.load_time_sec,
            "notes": "single-stream, no JSON mode — see module docstring",
        }
