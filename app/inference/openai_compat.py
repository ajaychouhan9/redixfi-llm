"""OpenAI-compatible HTTP backend.

Serves two roles with one implementation:

  * `vllm`   — talks to the vLLM OpenAI-compatible server running on Kaggle
               (`vllm serve ...` exposes /v1/chat/completions).
  * `openai` — talks to api.openai.com, used ONLY for an optional reference
               re-generation. The evaluation does NOT need it: reference
               outputs come from the exported fixtures, which preserve what
               production already produced. (RedixFi's OpenAI account also
               had zero credits as of 2026-08-28.)

Transport is stdlib urllib, matching RedixFi's own deliberate convention of
not adding the `openai` SDK as a dependency. One less thing to install on a
Kaggle image, and one less version to pin.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Dict, Iterator, List, Optional

from .base import BaseBackend, GenerationRequest, GenerationResult


class OpenAICompatBackend(BaseBackend):
    def __init__(
        self,
        base_url: str,
        api_key: str = "",
        name: str = "openai-compat",
        timeout_sec: int = 180,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.name = name
        self.timeout_sec = timeout_sec

    # -- internals ---------------------------------------------------------
    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        # vLLM accepts any bearer (or none). OpenAI requires a real one.
        headers["Authorization"] = f"Bearer {self.api_key or 'EMPTY'}"
        return headers

    def _body(self, request: GenerationRequest, stream: bool = False) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "model": request.model,
            "messages": request.messages_as_dicts(),
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": stream,
        }
        if request.json_mode:
            body["response_format"] = {"type": "json_object"}
        if request.seed is not None:
            body["seed"] = request.seed
        if request.stop:
            body["stop"] = request.stop
        return body

    def _post(self, path: str, body: Dict[str, Any]) -> Dict[str, Any]:
        req = urllib.request.Request(
            f"{self.base_url}{path}",
            data=json.dumps(body).encode("utf-8"),
            headers=self._headers(),
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout_sec) as resp:
            return json.loads(resp.read().decode("utf-8"))

    # -- Backend protocol --------------------------------------------------
    def _generate(self, request: GenerationRequest) -> GenerationResult:
        try:
            data = self._post("/chat/completions", self._body(request))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:500]
            return GenerationResult(
                text="", model=request.model, backend=self.name,
                error=f"HTTP {exc.code}: {detail}",
            )

        choice = (data.get("choices") or [{}])[0]
        usage = data.get("usage") or {}
        return GenerationResult(
            text=str((choice.get("message") or {}).get("content") or ""),
            model=data.get("model") or request.model,
            backend=self.name,
            prompt_tokens=int(usage.get("prompt_tokens") or 0),
            completion_tokens=int(usage.get("completion_tokens") or 0),
            total_tokens=int(usage.get("total_tokens") or 0),
            finish_reason=choice.get("finish_reason"),
            raw=data,
        )

    def stream(self, request: GenerationRequest) -> Iterator[str]:
        body = self._body(request, stream=True)
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers=self._headers(),
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_sec) as resp:
                for raw_line in resp:
                    line = raw_line.decode("utf-8").strip()
                    if not line.startswith("data:"):
                        continue
                    payload = line[len("data:"):].strip()
                    if payload == "[DONE]":
                        return
                    try:
                        chunk = json.loads(payload)
                    except json.JSONDecodeError:
                        continue
                    delta = ((chunk.get("choices") or [{}])[0].get("delta") or {})
                    piece = delta.get("content")
                    if piece:
                        yield piece
        except Exception:
            # Fail-soft to a single non-streamed emission rather than
            # leaving the caller with a half-written answer.
            yield self.generate(request).text

    def health(self) -> Dict[str, Any]:
        try:
            req = urllib.request.Request(
                f"{self.base_url}/models", headers=self._headers(), method="GET"
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            served: List[str] = [m.get("id") for m in (data.get("data") or [])]
            return {"backend": self.name, "status": "ok", "models": served,
                    "base_url": self.base_url}
        except Exception as exc:
            return {"backend": self.name, "status": "unreachable",
                    "base_url": self.base_url, "error": f"{type(exc).__name__}: {exc}"}
