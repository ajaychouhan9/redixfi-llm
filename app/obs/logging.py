"""Logging and in-process request metrics.

Deliberately dependency-free: Kaggle images vary, and a metrics stack is
not what this project is testing. Counters live in memory and reset with
the process, which is correct for an ephemeral Kaggle session.

SECRETS: never log a token, key, or full prompt body. Prompts can contain
full annual-report text pulled from production.
"""
from __future__ import annotations

import logging
import os
import sys
import threading
import time
from typing import Any, Dict

_CONFIGURED = False


def get_logger(name: str) -> logging.Logger:
    global _CONFIGURED
    if not _CONFIGURED:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)-7s %(name)s | %(message)s")
        )
        root = logging.getLogger()
        root.handlers = [handler]
        root.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())
        _CONFIGURED = True
    return logging.getLogger(name)


class RequestLog:
    """Thread-safe counters for the API layer."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._started = time.time()
        self._requests = 0
        self._failures = 0
        self._streamed = 0
        self._latency_total = 0.0
        self._prompt_tokens = 0
        self._completion_tokens = 0
        self._by_model: Dict[str, int] = {}

    def record(
        self, *, model: str, latency_sec: float, prompt_tokens: int,
        completion_tokens: int, ok: bool, streamed: bool = False,
    ) -> None:
        with self._lock:
            self._requests += 1
            if not ok:
                self._failures += 1
            if streamed:
                self._streamed += 1
            self._latency_total += latency_sec
            self._prompt_tokens += prompt_tokens
            self._completion_tokens += completion_tokens
            self._by_model[model] = self._by_model.get(model, 0) + 1

    def uptime_sec(self) -> float:
        return time.time() - self._started

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            requests = self._requests
            mean_latency = (self._latency_total / requests) if requests else 0.0
            elapsed = max(self.uptime_sec(), 1e-6)
            return {
                "uptime_sec": round(self.uptime_sec(), 1),
                "requests": requests,
                "failures": self._failures,
                "streamed": self._streamed,
                "mean_latency_sec": round(mean_latency, 4),
                "prompt_tokens": self._prompt_tokens,
                "completion_tokens": self._completion_tokens,
                "completion_tokens_per_sec": round(self._completion_tokens / elapsed, 2),
                "by_model": dict(self._by_model),
            }
