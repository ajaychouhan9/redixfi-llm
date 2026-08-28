"""Offline backend — no GPU, no network, deterministic.

Its whole job is to let the API layer, task layer, evaluation harness and
test suite be exercised end-to-end before a single Kaggle GPU-hour is
spent, which is the explicit sequencing the founder set on 2026-08-28.

It returns SCHEMA-VALID, COMPLIANCE-CLEAN JSON for each of the three task
types so the full pipeline (generate -> parse -> validate -> compare)
runs green. It is not a model and its output is not evidence of anything —
`is_synthetic` is set on every result so no evaluation report can quietly
present echo output as a real model comparison.
"""
from __future__ import annotations

import json
from typing import Any, Dict

from .base import BaseBackend, GenerationRequest, GenerationResult

_AR_STUB = {
    "executive_summary": (
        "The report described the company's stated priorities across its "
        "operating segments. Management said it focused on capacity, "
        "governance and sustainability during the period. The document "
        "outlined the areas management identified as central to its "
        "strategy."
    ),
    "key_points": [
        "Management described a focus on capacity and operational resilience",
        "The report stated continued investment in sustainability programmes",
        "Management said governance practices were reviewed during the year",
    ],
    "important_risks": [],
    "key_takeaway": (
        "The report centred on management's stated operating priorities for "
        "the period."
    ),
}

_CONCALL_STUB = {
    "summary": (
        "Management reported on operating activity during the period. The "
        "document described commissioning progress at the company's "
        "facilities and management said demand from domestic customers "
        "remained the largest contributor to order intake. Management also "
        "described the sourcing programme as extended to further component "
        "categories during the quarter under review."
    ),
    "tone_label": "Neutral",
    "tone_note": (
        "Management described operating activity in even terms without "
        "emphasising either strength or weakness."
    ),
}

# The legacy annual-report contract: summary/bullets/key_takeaway, and no
# important_risks — that field did not exist before 2026-08-24.
_AR_LEGACY_STUB = {
    "summary": (
        "The report described the company's stated priorities across its "
        "operating segments. Management said it focused on capacity, "
        "governance and sustainability during the period."
    ),
    "bullets": [
        "Management described a focus on capacity and operational resilience",
        "The report stated continued investment in sustainability programmes",
        "Management said governance practices were reviewed during the year",
    ],
    "key_takeaway": (
        "The report centred on management's stated operating priorities for "
        "the period."
    ),
}

_RED_FLAG_STUB = {
    "category": None,
    "summary": "",
}

_ASK_STUB = {
    "answer": "The fact packet does not contain the data needed to answer that.",
    "refused": True,
    "refusal_reason": "offline echo backend — no model was consulted",
}


class EchoBackend(BaseBackend):
    name = "echo"

    def _detect_task(self, request: GenerationRequest) -> str:
        system = ""
        for message in request.messages:
            if message.role == "system":
                system = message.content
                break
        if "summarize a single exchange-filed corporate annual report" in system:
            # The legacy and current annual-report prompts share an opening
            # line; they are told apart by their output contract, which is
            # the only thing that actually differs for a responder.
            if "important_risks" in system:
                return "annual_report_summary"
            return "annual_report_summary_legacy"
        if "summarize a single exchange-filed corporate document" in system:
            return "concall_summary"
        if "confirm whether a document excerpt genuinely discusses" in system:
            return "red_flag"
        if "fact packet" in system:
            return "ask_ai"
        return "unknown"

    def _generate(self, request: GenerationRequest) -> GenerationResult:
        task = self._detect_task(request)
        payload: Dict[str, Any]
        if task == "annual_report_summary":
            payload = dict(_AR_STUB)
        elif task == "annual_report_summary_legacy":
            payload = dict(_AR_LEGACY_STUB)
        elif task == "concall_summary":
            payload = dict(_CONCALL_STUB)
        elif task == "red_flag":
            payload = dict(_RED_FLAG_STUB)
        elif task == "ask_ai":
            payload = dict(_ASK_STUB)
        else:
            payload = {"answer": "", "refused": True, "refusal_reason": "unknown task"}

        text = json.dumps(payload, ensure_ascii=False)
        # Echo emits a bare JSON object by construction, so when a schema was
        # requested it is honestly reporting that the shape was enforced —
        # which keeps the offline harness test meaningful.
        schema_requested = request.json_schema is not None
        prompt_chars = sum(len(m.content) for m in request.messages)
        return GenerationResult(
            text=text,
            model=request.model,
            backend=self.name,
            # Rough char/4 estimate, clearly labelled — never presented as a
            # measured token count.
            prompt_tokens=prompt_chars // 4,
            completion_tokens=len(text) // 4,
            total_tokens=(prompt_chars + len(text)) // 4,
            finish_reason="stop",
            structured_output_used=schema_requested,
            structured_output_mode="json_schema" if schema_requested else None,
            raw={"is_synthetic": True, "detected_task": task,
                 "token_counts_are_estimates": True},
        )

    def health(self) -> Dict[str, Any]:
        return {"backend": self.name, "status": "ok", "is_synthetic": True}
