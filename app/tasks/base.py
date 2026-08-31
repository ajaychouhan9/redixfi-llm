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
    # Did post-hoc repair have to salvage the output? With guided decoding
    # working this should be False everywhere; it is the number the fix is
    # measured by, so it is NOT removed.
    json_repair_used: bool = False
    # Did the backend actually constrain decoding to a schema? Recorded
    # separately from json_repair_used: "guided ON and no repair needed" and
    # "guided OFF and no repair needed" are very different facts, and only
    # the first proves the shape is enforced rather than lucky.
    structured_output_used: bool = False
    structured_output_mode: Optional[str] = None
    model: str = ""
    backend: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_sec: float = 0.0
    # Pre-generation context-budget log (see app/tasks/context_budget.py).
    context_log: Optional[Dict[str, Any]] = None
    # One-shot GPT-4o-mini compliance-edit log (see app/tasks/rephrase.py).
    rephrase_log: Optional[Dict[str, Any]] = None
    # Where the final output came from: qwen | gpt_rephrase | failed_human_review.
    final_source: str = "qwen"

    def absorb(self, generation: GenerationResult) -> None:
        self.model = generation.model
        self.backend = generation.backend
        # Sticky across retries: if ANY attempt was guided, the case was.
        self.structured_output_used = (
            self.structured_output_used or generation.structured_output_used)
        self.structured_output_mode = (
            generation.structured_output_mode or self.structured_output_mode)
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
            "structured_output_used": self.structured_output_used,
            "structured_output_mode": self.structured_output_mode,
            "model": self.model,
            "backend": self.backend,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "latency_sec": round(self.latency_sec, 4),
            "context_log": self.context_log,
            "rephrase_log": self.rephrase_log,
            "final_source": self.final_source,
        }
