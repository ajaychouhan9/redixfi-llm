"""Shared task plumbing: JSON extraction and the task result record."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..inference.base import GenerationResult

# Some models wrap JSON in a markdown fence even under an explicit
# instruction not to. RedixFi never had to handle this (OpenAI JSON mode
# guarantees a bare object), so this is a CANDIDATE-SIDE tolerance, applied
# identically to every candidate model. It is recorded in the result via
# `json_repair_used` so a model that needs the crutch is visible in the
# report rather than silently flattered.
_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)
_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)


def parse_json_object(text: str) -> tuple[Optional[Dict[str, Any]], bool, Optional[str]]:
    """Returns (parsed, repair_used, error). Never raises."""
    if not text or not text.strip():
        return None, False, "empty response"
    try:
        return json.loads(text), False, None
    except json.JSONDecodeError:
        pass

    fenced = _FENCE_RE.search(text)
    if fenced:
        try:
            return json.loads(fenced.group(1)), True, None
        except json.JSONDecodeError:
            pass

    braced = _OBJECT_RE.search(text)
    if braced:
        try:
            return json.loads(braced.group(0)), True, None
        except json.JSONDecodeError as exc:
            return None, True, f"json decode failed after repair: {exc}"

    return None, False, "no JSON object found in response"


@dataclass
class TaskResult:
    task: str
    fixture_id: str
    ok: bool
    output: Dict[str, Any] = field(default_factory=dict)
    attempts: int = 0
    rejections: List[Dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None
    json_repair_used: bool = False
    model: str = ""
    backend: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_sec: float = 0.0

    def absorb(self, generation: GenerationResult) -> None:
        self.model = generation.model
        self.backend = generation.backend
        self.prompt_tokens += generation.prompt_tokens
        self.completion_tokens += generation.completion_tokens
        self.total_tokens += generation.total_tokens
        self.latency_sec += generation.latency_sec

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task": self.task,
            "fixture_id": self.fixture_id,
            "ok": self.ok,
            "output": self.output,
            "attempts": self.attempts,
            "rejections": self.rejections,
            "error": self.error,
            "json_repair_used": self.json_repair_used,
            "model": self.model,
            "backend": self.backend,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "latency_sec": round(self.latency_sec, 4),
        }
