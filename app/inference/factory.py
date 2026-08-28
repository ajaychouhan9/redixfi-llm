"""Backend selection. One place decides which runtime serves a request."""
from __future__ import annotations

from typing import Optional

from ..config.settings import Settings, get_settings
from .base import BaseBackend
from .echo import EchoBackend
from .openai_compat import OpenAICompatBackend

OPENAI_BASE_URL = "https://api.openai.com/v1"


def build_backend(settings: Optional[Settings] = None) -> BaseBackend:
    settings = settings or get_settings()
    backend = (settings.backend or "echo").lower()

    if backend == "echo":
        return EchoBackend()

    if backend == "vllm":
        return OpenAICompatBackend(
            base_url=settings.vllm_base_url,
            api_key="EMPTY",
            name="vllm",
            timeout_sec=settings.request_timeout_sec,
        )

    if backend == "openai":
        if not settings.openai_api_key:
            raise RuntimeError(
                "LLM_BACKEND=openai requires OPENAI_API_KEY. Note the evaluation "
                "does not need it — reference outputs come from exported fixtures."
            )
        return OpenAICompatBackend(
            base_url=OPENAI_BASE_URL,
            api_key=settings.openai_api_key,
            name="openai",
            timeout_sec=settings.request_timeout_sec,
        )

    raise ValueError(f"unknown LLM_BACKEND '{settings.backend}'. Use: echo | vllm | openai")
