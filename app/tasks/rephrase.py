"""Single GPT-4o-mini compliance-EDITOR layer.

Architecture (2026-08-31 controlled fix)
---------------------------------------
Qwen is the primary summarizer. When the validator rejects a Qwen summary for
an eligible wording/compliance issue, we send ONLY the Qwen summary + the
validator finding + a short policy note to GPT-4o-mini for a one-shot edit.
The original source/transcript/evidence is never sent. GPT-4o-mini is an
EDITOR, not a summarizer: it returns the same schema with the minimal wording
changes needed to pass the validator.

There is exactly ONE GPT call per case, and only for eligible failures.
Technical failures (context overflow, model unavailable, invalid JSON, missing
evidence) are never routed here.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..compliance.validators import summarizer_violation
from ..config.settings import get_settings
from ..inference.base import Backend, GenerationRequest, Message
from ..inference.factory import OPENAI_BASE_URL
from ..inference.openai_compat import OpenAICompatBackend
from ..prompts.annual_report_summary import BULLET_MAX, BULLET_MIN
from ..prompts.concall_summary import TONE_LABELS

REPHRASE_MODEL = "gpt-4o-mini"

EDITOR_SYSTEM_PROMPT = (
    "You are the final compliance editor for a financial summary.\n"
    "You will receive an already-generated Qwen summary and a specific validator finding.\n"
    "Rewrite ONLY the supplied summary so that it satisfies the supplied validator finding.\n"
    "Preserve all factual information, numbers, dates, risks and meaning wherever permitted.\n"
    "Do not add facts. Do not invent information. Do not consult or infer from the original source.\n"
    "Do not create a new summary. Do not remove useful information unless required by the stated policy.\n"
    "For management guidance, explicitly attribute expectations, targets, projections or plans to "
    "management when required.\n"
    "Return ONLY the corrected summary as a JSON object matching the required schema.\n"
)

# Task-specific policy notes. These describe the EXISTING RedixFi policy;
# they do not invent new policy.
TASK_POLICY_NOTES = {
    "annual_report_summary": (
        "Annual Report policy: do not state specific financial figures as fact; "
        "rephrase or remove them. The validator treats any number followed by "
        "crore/lakh/million/billion/bn/mn as a financial figure (for example "
        "'1 billion tonnes' still trips it), so generalize or remove such "
        "digit+unit quantities (e.g. 'over a billion tonnes' or 'significant "
        "capacity expansion'). Preserve non-financial facts, dates, management "
        "guidance (attributed to management), risks, and meaning."
    ),
    "concall_summary": (
        "Concall policy: financial figures are allowed and should be preserved. "
        "Do not present management guidance as guaranteed fact; attribute "
        "expectations, targets, projections or plans to management."
    ),
}


def is_eligible_for_rephrase(reason: Optional[str]) -> bool:
    """Only editorial/compliance wording failures qualify for GPT editing.

    Technical/infrastructure failures (context overflow, model unavailable,
    malformed request, invalid JSON, missing evidence) never do.
    """
    if not reason:
        return False
    low = reason.lower()
    if low.startswith(("forward-tense word", "forbidden word",
                       "financial figure stated as fact")):
        return True
    return False


def collect_validator_findings(task: str, out: Dict[str, Any]) -> List[str]:
    """Collects ALL validator findings, not just the first, so the editor can
    fix every issue in its single attempt."""
    findings: List[str] = []
    if task == "annual_report_summary":
        for field in ("executive_summary", "key_takeaway"):
            bad = summarizer_violation(str(out.get(field, "")), check_financial_figures=True)
            if bad:
                findings.append(f"{field}: {bad}")
        for idx, bullet in enumerate(out.get("key_points") or [], start=1):
            bad = summarizer_violation(str(bullet), check_financial_figures=True)
            if bad:
                findings.append(f"key_points[{idx}]: {bad}")
        for idx, risk in enumerate(out.get("important_risks") or [], start=1):
            bad = summarizer_violation(str(risk), check_financial_figures=True)
            if bad:
                findings.append(f"important_risks[{idx}]: {bad}")
        count = len(out.get("key_points") or [])
        if not (BULLET_MIN <= count <= BULLET_MAX):
            findings.append(
                f"key_points count {count} outside [{BULLET_MIN}, {BULLET_MAX}]")
        return findings
    if task == "concall_summary":
        for field in ("summary", "tone_note"):
            bad = summarizer_violation(str(out.get(field, "")))
            if bad:
                findings.append(f"{field}: {bad}")
        tone = str(out.get("tone_label", ""))
        if tone not in TONE_LABELS:
            findings.append(f"invalid tone_label {tone!r}")
        return findings
    return findings


def build_rephrase_user_content(
    task: str,
    qwen_output: Dict[str, Any],
    validator_findings: List[str],
) -> str:
    policy = TASK_POLICY_NOTES.get(task, TASK_POLICY_NOTES["concall_summary"])
    findings_text = "\n".join(f"- {f}" for f in validator_findings)
    return (
        f"Validator finding(s):\n{findings_text}\n\n"
        f"Policy note: {policy}\n\n"
        f"Qwen summary (JSON):\n"
        f"{_json_dumps(qwen_output)}\n\n"
        "Return ONLY the corrected summary as a JSON object with the same "
        "fields/schema."
    )


def build_rephrase_request(
    task: str,
    qwen_output: Dict[str, Any],
    validator_findings: List[str],
    schema: Dict[str, Any],
    max_tokens: int = 1024,
) -> GenerationRequest:
    return GenerationRequest(
        messages=[
            Message("system", EDITOR_SYSTEM_PROMPT),
            Message("user", build_rephrase_user_content(task, qwen_output, validator_findings)),
        ],
        model=REPHRASE_MODEL,
        temperature=0.0,
        max_tokens=max_tokens,
        seed=0,
        json_mode=True,
        json_schema=schema,
    )


def build_rephrase_backend() -> Backend:
    """Reuses the existing OpenAI-compatible backend + RedixFi API config."""
    settings = get_settings()
    if not settings.openai_api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is required for the GPT-4o-mini rephrase layer"
        )
    return OpenAICompatBackend(
        base_url=OPENAI_BASE_URL,
        api_key=settings.openai_api_key,
        name="openai",
        timeout_sec=settings.request_timeout_sec,
    )


def _json_dumps(value: Any) -> str:
    import json
    return json.dumps(value, ensure_ascii=False, indent=2)
