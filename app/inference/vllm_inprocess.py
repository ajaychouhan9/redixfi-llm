"""In-process vLLM backend — one model load, served through this project's
own OpenAI-compatible API.

WHY NOT `vllm serve`
--------------------
Measured on Kaggle T4 x2 (2026-08-28): loading Qwen3-14B-AWQ at TP=2 / 32K
takes ~244 s and leaves **0.43 GB free per card** (14.13 of 14.56 GB used —
vLLM preallocates the KV cache to fill `gpu_memory_utilization`).

Spawning `vllm serve` as a second process therefore means a second full
load: another ~4 minutes of a metered GPU budget, and a real OOM risk if
the first process has not fully released its allocation. Wrapping the
already-loaded engine and serving it through `app/api/server.py` gives the
same OpenAI-compatible surface — `/v1/chat/completions`, `/v1/models`,
`/health` over real HTTP — for one load instead of two.

It also removes a whole class of failure: `vllm serve`'s CLI flags move
between releases (`--disable-log-requests` was accepted in older versions
and rejected in this one, which cost a run). The Python API is stabler
than the CLI surface.

TRADE-OFF, stated because it affects the throughput number
----------------------------------------------------------
Requests are issued one at a time here, so tokens/sec measures SINGLE-
STREAM decode. vLLM's continuous batching would do considerably better
under concurrent load. Any capacity projection from these numbers is a
FLOOR, not an estimate of what a properly served deployment achieves.
Output quality — what this phase is measuring — is unaffected.
"""
from __future__ import annotations

import time
from typing import Any, Dict, Iterator, List, Optional

from .base import BaseBackend, GenerationRequest, GenerationResult


class VLLMInProcessBackend(BaseBackend):
    name = "vllm-inprocess"

    def __init__(self, llm: Any, model_name: str) -> None:
        """`llm` is an already-constructed `vllm.LLM`. Construction (and its
        timing) stays with the caller so a load failure is reported
        distinctly from a generation failure."""
        self._llm = llm
        self.model_name = model_name
        self._tokenizer = None
        try:
            self._tokenizer = llm.get_tokenizer()
        except Exception:
            pass

    def _render_prompt(self, request: GenerationRequest) -> str:
        messages = [{"role": m.role, "content": m.content} for m in request.messages]
        if self._tokenizer is not None:
            try:
                return self._tokenizer.apply_chat_template(
                    messages, tokenize=False, add_generation_prompt=True)
            except Exception:
                pass
        parts = [f"{m['role'].upper()}: {m['content']}" for m in messages]
        return "\n\n".join(parts) + "\n\nASSISTANT:"

    def _generate(self, request: GenerationRequest) -> GenerationResult:
        from vllm import SamplingParams

        prompt = self._render_prompt(request)
        params = SamplingParams(
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            seed=request.seed,
            stop=request.stop or None,
        )
        started = time.perf_counter()
        outs = self._llm.generate([prompt], params)
        latency = time.perf_counter() - started

        if not outs or not outs[0].outputs:
            return GenerationResult(text="", model=request.model, backend=self.name,
                                    error="vllm returned no output")
        completion = outs[0].outputs[0]
        text = completion.text or ""

        try:
            prompt_tokens = len(outs[0].prompt_token_ids)
        except Exception:
            prompt_tokens = len(self._tokenizer.encode(prompt)) if self._tokenizer else 0
        try:
            completion_tokens = len(completion.token_ids)
        except Exception:
            completion_tokens = len(text) // 4

        return GenerationResult(
            text=text.strip(),
            model=request.model,
            backend=self.name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            latency_sec=latency,
            finish_reason=getattr(completion, "finish_reason", "stop"),
            raw={"single_stream": True},
        )

    def stream(self, request: GenerationRequest) -> Iterator[str]:
        yield self.generate(request).text

    def health(self) -> Dict[str, Any]:
        return {
            "backend": self.name,
            "status": "ok" if self._llm is not None else "not_loaded",
            "model": self.model_name,
            "notes": "in-process vLLM, single-stream — see module docstring",
        }
