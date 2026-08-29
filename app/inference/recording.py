"""Backend wrapper that records every request/response pair verbatim.

WHY A WRAPPER RATHER THAN EDITING THE TASK RUNNERS
--------------------------------------------------
Diagnosing the concall failures needs the RAW generated text of every
attempt, including the ones the retry loop rejected. The task runners do
record rejections, but they store the PARSED output dict (or, on a JSON
failure, only the first 500 characters of raw text) — enough to know why an
attempt was rejected, not enough to see how the model was drifting.

Editing the runners to capture more would mean changing evaluation logic
mid-investigation, which is exactly what makes a result hard to trust
afterwards. Wrapping the backend instead leaves every prompt, validator,
retry budget and comparison byte-identical: this class only observes.

Recording is off the hot path in every sense — it appends to a list and
does no I/O — so it does not perturb the latency numbers the run reports.
"""
from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from .base import Backend, GenerationRequest, GenerationResult


class RecordingBackend(Backend):
    """Transparent pass-through that keeps a full transcript.

    `transcript` accumulates one entry per generate() call, in order, each
    carrying the exact prompt sent and the exact text returned.
    """

    def __init__(self, inner: Backend, tag: str = "") -> None:
        self._inner = inner
        self.tag = tag
        self.transcript: List[Dict[str, Any]] = []
        # Mirror the wrapped backend's identity so anything reading
        # `backend.name` (the runner records it into every result) sees the
        # real runtime, not the wrapper. A run must never look like it was
        # produced by something called "recording".
        self.name = getattr(inner, "name", "unknown")

    def generate(self, request: GenerationRequest) -> GenerationResult:
        result = self._inner.generate(request)
        system = next((m.content for m in request.messages if m.role == "system"), "")
        user = next((m.content for m in request.messages if m.role == "user"), "")
        self.transcript.append({
            "tag": self.tag,
            "model": request.model,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "json_schema_sent": request.json_schema is not None,
            "system_prompt_sha": _sha(system),
            "system_prompt_chars": len(system),
            # The user content carries the full evidence/transcript slice and
            # can be ~50-150 KB; the tail is what matters for seeing whether
            # a corrective note was appended on a retry.
            "user_prompt_chars": len(user),
            "user_prompt_tail": user[-1200:],
            "raw_output": result.text,          # verbatim, NOT truncated
            "raw_output_chars": len(result.text or ""),
            "completion_tokens": result.completion_tokens,
            "finish_reason": result.finish_reason,
            "structured_output_used": result.structured_output_used,
            "error": result.error,
        })
        return result

    def stream(self, request: GenerationRequest) -> Iterator[str]:
        return self._inner.stream(request)

    def health(self) -> Dict[str, Any]:
        return self._inner.health()

    # -- helpers -----------------------------------------------------------
    def reset(self, tag: str = "") -> None:
        self.transcript = []
        self.tag = tag

    def attempts_for_tag(self, tag: str) -> List[Dict[str, Any]]:
        return [e for e in self.transcript if e["tag"] == tag]


def _sha(text: str) -> str:
    import hashlib
    return hashlib.sha1((text or "").encode("utf-8")).hexdigest()[:12]
