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

import re
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
    "You are a compliance editor for a financial summary.\n"
    "Rewrite ONLY the supplied Qwen summary to address the supplied validator finding.\n"
    "Preserve all factual information and material quantitative details.\n"
    "Do NOT create a new summary.\n"
    "Do NOT add facts.\n"
    "Do NOT infer facts.\n"
    "Do NOT consult or reconstruct the original source.\n"
    "Do NOT remove a number, date, percentage, target, projection, guidance, risk, "
    "or business fact merely to make the validator pass.\n"
    "When the supplied information is clearly management guidance, preserve it and "
    "attribute it appropriately.\n"
    "Every forward-looking term (expect*, target*, forecast*, outlook) must appear "
    "in a sentence that explicitly names management or the report as the source; "
    "if it is not already attributed, rewrite the sentence to attribute it.\n"
    "Never leave an unattributed 'is expected' / 'are expected' phrase. Rewrite it "
    "as 'Management expects X to be ...' or 'Management expects X at ...'.\n"
    "Example: 'Capital expenditure is expected at INR300-350 crores' -> "
    "'Management expects capital expenditure to be INR300-350 crores'.\n"
    "Example: 'The company targets X' -> 'Management has stated a target of X.'\n"
    "Example: 'The company will achieve X' -> 'Management expects to achieve X.'\n"
    "If the information cannot be preserved while satisfying the current validator "
    "policy, DO NOT silently generalize or delete it. In that situation return the "
    "information as faithfully as possible and mark the case for human review.\n"
    "Return only the required summary output.\n"
)

# Task-specific policy notes. These describe the EXISTING RedixFi policy;
# they do not invent new policy.
TASK_POLICY_NOTES = {
    "annual_report_summary": (
        "Annual Report policy: financial figures are allowed when explicitly "
        "attributed to management/source (e.g. 'management's stated target to "
        "expand ... to 1 billion tonnes'). PRESERVE material quantitative facts, "
        "numbers, dates, percentages, targets, projections, guidance, risks and "
        "meaning. Attribute figures to management or the report when needed. "
        "Do NOT delete or generalize figures merely to pass the validator."
    ),
    "concall_summary": (
        "Concall policy: financial figures are allowed and should be preserved. "
        "Do not present management guidance as guaranteed fact; attribute "
        "expectations, targets, projections or plans to management in the SAME "
        "sentence where the forward-looking term appears. Rewrite unattributed "
        "'is expected' phrases as 'Management expects X to be ...'."
    ),
}

_MATERIAL_TOKEN_RE = re.compile(
    r"\b\d[\d,]*(?:\.\d+)?\b"
    r"|\bFY\d{2}-\d{2}\b"
    r"|\b20\d{2}\b"
    r"|\bQ[1-4]\s*FY\d{2}\b"
    r"|\b\d+(?:\.\d+)?\s*%",
    re.IGNORECASE,
)


def _text_of(output: Dict[str, Any]) -> str:
    parts: List[str] = []
    for value in output.values():
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    parts.append(item)
    return " ".join(parts)


def extract_material_tokens(text: str) -> set:
    return {m.group(0).lower().replace(" ", "") for m in _MATERIAL_TOKEN_RE.finditer(text)}


def information_preservation_check(
    qwen_output: Dict[str, Any],
    gpt_output: Dict[str, Any],
) -> Dict[str, Any]:
    """Deterministic guard: if GPT removed any material number/date/percentage
    that was present in the Qwen summary, do NOT silently accept it."""
    qwen_tokens = extract_material_tokens(_text_of(qwen_output))
    gpt_tokens = extract_material_tokens(_text_of(gpt_output))
    missing = sorted(qwen_tokens - gpt_tokens)
    if missing:
        return {"status": "HUMAN_REVIEW_REQUIRED", "missing_material_tokens": missing}
    return {"status": "PASS", "missing_material_tokens": []}


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


def _resolve_openai_key_in_kaggle_env() -> None:
    """Populate os.environ["OPENAI_API_KEY"] from a Kaggle-native source
    when running inside a Kaggle kernel, where the VM's own .env never
    reaches (Kaggle kernels are isolated cloud sandboxes with their own
    environment — see the 2026-09-01 production run, where both AR and
    concall crashed with `OPENAI_API_KEY is required` for exactly this
    reason). No-op when the env var is already set (the normal VM/local
    path) so this never changes existing behavior outside Kaggle.

    Two sources are tried, in order of preference:
    1. A true Kaggle Secret named OPENAI_API_KEY, via kaggle_secrets
       (Add-ons > Secrets in the kernel editor — the Kaggle-native
       mechanism; requires the founder to attach it once per kernel
       through the web UI, since neither the kaggle CLI nor kagglesdk
       exposes any API to do this — confirmed by grepping both packages'
       source for "secret": zero hits, and `kaggle kernels push -h` has
       no such flag).
    2. A private per-account Kaggle Dataset (`redixfi-openai-key`)
       carrying a single `openai_key.txt` file, mounted the same way the
       code/fixture datasets already are — the automatable fallback,
       still keeps the key out of any script/notebook body and out of
       git; only ever read, never logged or echoed.
    """
    import os
    if os.environ.get("OPENAI_API_KEY"):
        return

    # Diagnostic logging only (2026-09-01 follow-up) -- the prior version
    # of this function swallowed every exception silently, so two real
    # Kaggle runs both failed with the exact same downstream RuntimeError
    # and gave no way to tell WHICH resolution path failed or why (not
    # attached / wrong secret name / wrong kernel scope / import error /
    # empty value / API error). Every branch below now prints exactly one
    # line naming its own outcome. Never logs the key's VALUE -- only
    # whether one was found, and if not, why not. Behavior is unchanged:
    # still tries kaggle_secrets first, then the dataset-file fallback,
    # still a silent no-op on success (build_rephrase_backend's existing
    # RuntimeError is still what surfaces on total failure).
    try:
        from kaggle_secrets import UserSecretsClient
    except Exception as e:
        print(f"[rephrase key-resolve] kaggle_secrets import failed: "
             f"{type(e).__name__}: {e}", flush=True)
    else:
        try:
            key = UserSecretsClient().get_secret("OPENAI_API_KEY")
        except Exception as e:
            print(f"[rephrase key-resolve] UserSecretsClient().get_secret "
                 f"raised: {type(e).__name__}: {e}", flush=True)
        else:
            if key:
                print("[rephrase key-resolve] resolved OPENAI_API_KEY from "
                     "a Kaggle Secret", flush=True)
                os.environ["OPENAI_API_KEY"] = key
                return
            print("[rephrase key-resolve] UserSecretsClient().get_secret "
                 "returned None/empty -- secret not attached to this "
                 "kernel, wrong name, or its access toggle is off",
                 flush=True)

    try:
        import glob
        hits = glob.glob("/kaggle/input/**/openai_key.txt", recursive=True)
        if not hits:
            print("[rephrase key-resolve] no dataset fallback file found "
                 "either (no openai_key.txt under /kaggle/input) -- "
                 "OPENAI_API_KEY will remain unset", flush=True)
        else:
            with open(hits[0], encoding="utf-8") as fh:
                key = fh.read().strip()
            if key:
                print("[rephrase key-resolve] resolved OPENAI_API_KEY from "
                     "the dataset fallback file", flush=True)
                os.environ["OPENAI_API_KEY"] = key
            else:
                print(f"[rephrase key-resolve] dataset fallback file {hits[0]} "
                     "exists but is empty -- OPENAI_API_KEY will remain unset",
                     flush=True)
    except Exception as e:
        print(f"[rephrase key-resolve] dataset fallback lookup raised: "
             f"{type(e).__name__}: {e} -- OPENAI_API_KEY will remain unset",
             flush=True)


def build_rephrase_backend() -> Backend:
    """Reuses the existing OpenAI-compatible backend + RedixFi API config."""
    _resolve_openai_key_in_kaggle_env()
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
