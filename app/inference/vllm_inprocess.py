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

    def __init__(self, llm: Any, model_name: str, chat_native: bool = False) -> None:
        """`llm` is an already-constructed `vllm.LLM`. Construction (and its
        timing) stays with the caller so a load failure is reported
        distinctly from a generation failure.

        `chat_native` routes generation through `llm.chat()` instead of
        rendering the template ourselves and calling `llm.generate()`.

        WHY THIS EXISTS, AND WHY IT IS NOT A TUNING ADVANTAGE
        -----------------------------------------------------
        `_render_prompt` calls `apply_chat_template(tokenize=False)` and
        feeds the resulting STRING to `generate()`. That is correct for a
        model with an HF Jinja chat template (Qwen), and it is what produced
        every Qwen number so far — so it must not change, or those numbers
        stop being comparable.

        It is NOT correct for a Mistral model using the Tekken tokenizer.
        The Ministral preflight logged: "MistralCommonBackend.
        apply_chat_template(..., tokenize=False) is unsafe and may lead to
        unexpected behavior". Rendering to a string and re-encoding can
        produce a different token sequence than the model expects, which on
        a compliance benchmark reads as a quality failure when it is really
        a formatting failure.

        `llm.chat()` hands the messages to vLLM, which applies whatever
        templating that model's tokenizer mode requires. So this flag does
        not give either model a better prompt — it gives each model ITS OWN
        prompt, in the form that model expects. The prompt TEXT is identical
        either way.
        """
        self._llm = llm
        self.model_name = model_name
        self.chat_native = chat_native
        # Recorded so a result can never be read without knowing which
        # grammar backend produced it ('auto' resolves to xgrammar or a
        # fallback at request time).
        self.structured_backend = self._detect_structured_backend(llm)
        self._tokenizer = None
        try:
            self._tokenizer = llm.get_tokenizer()
        except Exception:
            pass

    @staticmethod
    def _detect_structured_backend(llm: Any) -> Optional[str]:
        """Best-effort read of the engine's configured structured-output
        backend. Never raises — this is telemetry, not control flow."""
        for path in (("llm_engine", "vllm_config", "structured_outputs_config"),
                     ("llm_engine", "model_config", "structured_outputs_config")):
            obj: Any = llm
            for attr in path:
                obj = getattr(obj, attr, None)
                if obj is None:
                    break
            backend = getattr(obj, "backend", None)
            if backend:
                return str(backend)
        return None

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

    def _structured_outputs(self, request: GenerationRequest):
        """Build vLLM 0.28.0 structured-output params, or None.

        API CONFIRMED AGAINST THE INSTALLED VERSION, NOT MEMORY. The first
        GPU run's engine banner reports `v0.28.0` with
        `structured_outputs_config=StructuredOutputsConfig(backend='auto', ...)`.
        In that release:

          * the field on SamplingParams is `structured_outputs`
          * it takes `vllm.sampling_params.StructuredOutputsParams`
          * `StructuredOutputsParams(json=<schema>)` is the JSON-Schema form,
            `json_object=True` the "any valid JSON" form
          * the whole `guided_json` / `guided_decoding_backend` /
            `GuidedDecodingParams` family is GONE — writing to it would raise

        `StructuredOutputsParams` is not re-exported from `vllm/__init__.py`,
        hence the submodule import. Returns (params, mode) so the caller can
        record WHICH constraint was applied, and (None, None) when the
        request asked for nothing.
        """
        if not request.json_schema and not request.json_mode:
            return None, None
        try:
            from vllm.sampling_params import StructuredOutputsParams
        except ImportError:
            # Older/newer vLLM with a different structured-output surface.
            # Degrade to unguided rather than crash a long run, and leave
            # structured_output_used False so the report shows the truth.
            return None, None

        if request.json_schema:
            return StructuredOutputsParams(json=request.json_schema), "json_schema"
        return StructuredOutputsParams(json_object=True), "json_object"

    def _generate(self, request: GenerationRequest) -> GenerationResult:
        from vllm import SamplingParams

        messages = [{"role": m.role, "content": m.content} for m in request.messages]
        prompt = None if self.chat_native else self._render_prompt(request)
        structured, so_mode = self._structured_outputs(request)

        kwargs = dict(
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            seed=request.seed,
            stop=request.stop or None,
        )
        if structured is not None:
            kwargs["structured_outputs"] = structured
        try:
            params = SamplingParams(**kwargs)
        except TypeError:
            # This vLLM does not accept `structured_outputs`. Fall back to an
            # unguided request so the run continues, but report it honestly —
            # a silent downgrade here would look like guided decoding
            # succeeding while json_repair quietly does all the work.
            kwargs.pop("structured_outputs", None)
            params = SamplingParams(**kwargs)
            structured, so_mode = None, None
        started = time.perf_counter()
        if self.chat_native:
            # vLLM applies the model's own templating (mistral-common for a
            # Tekken tokenizer). Same messages, same text — correct encoding.
            outs = self._llm.chat(messages, params, use_tqdm=False)
        else:
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
            structured_output_used=structured is not None,
            structured_output_mode=so_mode,
            raw={"single_stream": True,
                 "structured_outputs_backend": self.structured_backend},
        )

    def stream(self, request: GenerationRequest) -> Iterator[str]:
        yield self.generate(request).text

    def health(self) -> Dict[str, Any]:
        return {
            "backend": self.name,
            "status": "ok" if self._llm is not None else "not_loaded",
            "model": self.model_name,
            "structured_outputs_backend": self.structured_backend,
            "notes": "in-process vLLM, single-stream — see module docstring",
        }
