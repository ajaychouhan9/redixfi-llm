"""Inference backend abstraction.

Every backend takes the same request shape and returns the same
`GenerationResult`, so switching runtime (vLLM on Kaggle, OpenAI for a
reference re-run, echo for offline tests) is a config change and never an
architectural one. This is the seam that later lets RedixFi point at a
self-hosted endpoint instead of api.openai.com.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Optional, Protocol


@dataclass
class Message:
    role: str
    content: str

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass
class GenerationRequest:
    messages: List[Message]
    model: str
    temperature: float = 0.0
    max_tokens: int = 1024
    seed: Optional[int] = 0
    # RedixFi uses OpenAI JSON mode on every call. Backends that cannot
    # enforce it must still accept the flag and degrade gracefully — the
    # task layer re-parses and re-validates regardless.
    json_mode: bool = False
    # GUIDED (structured) DECODING. When set, the backend must constrain
    # generation to this JSON Schema so valid JSON is produced BY
    # CONSTRUCTION rather than repaired afterwards. Backends that cannot
    # enforce it must ignore it and leave `structured_output_used` False on
    # the result — silently pretending would hide exactly the measurement
    # this exists to produce. See app/schemas/output_schemas.py.
    json_schema: Optional[Dict[str, Any]] = None
    stop: Optional[List[str]] = None

    def messages_as_dicts(self) -> List[Dict[str, str]]:
        return [m.to_dict() for m in self.messages]


@dataclass
class GenerationResult:
    text: str
    model: str
    backend: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_sec: float = 0.0
    finish_reason: Optional[str] = None
    error: Optional[str] = None
    # True only when the backend actually applied a grammar/schema
    # constraint at decode time. The whole point of guided decoding is
    # being able to show json_repair_used drops to ~0 BECAUSE this is True,
    # so the two must be recorded independently.
    structured_output_used: bool = False
    structured_output_mode: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.error is None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "model": self.model,
            "backend": self.backend,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "latency_sec": round(self.latency_sec, 4),
            "finish_reason": self.finish_reason,
            "error": self.error,
            "structured_output_used": self.structured_output_used,
            "structured_output_mode": self.structured_output_mode,
        }


class Backend(Protocol):
    name: str

    def generate(self, request: GenerationRequest) -> GenerationResult: ...

    def stream(self, request: GenerationRequest) -> Iterator[str]: ...

    def health(self) -> Dict[str, Any]: ...


class BaseBackend:
    """Shared timing/error plumbing. Subclasses implement `_generate`."""

    name = "base"

    def generate(self, request: GenerationRequest) -> GenerationResult:
        started = time.perf_counter()
        try:
            result = self._generate(request)
        except Exception as exc:  # fail-soft, same posture as RedixFi
            return GenerationResult(
                text="",
                model=request.model,
                backend=self.name,
                latency_sec=time.perf_counter() - started,
                error=f"{type(exc).__name__}: {exc}",
            )
        result.latency_sec = time.perf_counter() - started
        result.backend = self.name
        return result

    def _generate(self, request: GenerationRequest) -> GenerationResult:
        raise NotImplementedError

    def stream(self, request: GenerationRequest) -> Iterator[str]:
        """Default: no true streaming, emit the whole answer once. Backends
        with real streaming override this."""
        yield self.generate(request).text

    def health(self) -> Dict[str, Any]:
        return {"backend": self.name, "status": "unknown"}
