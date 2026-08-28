#!/usr/bin/env python3
"""Start the OpenAI-compatible API.

    python scripts/serve.py                       # echo backend, no GPU
    LLM_BACKEND=vllm python scripts/serve.py      # in front of a vLLM server

This is the service RedixFi would eventually point at. It is EXPERIMENTAL
and nothing in RedixFi points here today.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config.settings import get_settings  # noqa: E402


def main() -> None:
    import uvicorn
    settings = get_settings()
    print("Starting RedixFi self-hosted LLM API (EXPERIMENTAL)")
    for key, value in settings.redacted().items():
        print(f"  {key:24s} {value}")
    uvicorn.run(
        "app.api.server:app",
        host=settings.api_host,
        port=settings.api_port,
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
    )


if __name__ == "__main__":
    main()
