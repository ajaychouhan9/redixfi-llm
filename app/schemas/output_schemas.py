"""JSON Schemas for guided (structured) decoding — one per benchmark task.

WHY THIS EXISTS
---------------
The first GPU run produced `json_repair_used = True` on **all 15 cases**.
`VLLMInProcessBackend` accepted `json_mode` on the request and then silently
dropped it, so every response was free-form text that had to be salvaged
afterwards by `app/tasks/base.py::parse_json_object`. Production's reference
path uses OpenAI JSON mode, so the eval was comparing content but NOT output
shape — and post-hoc repair on every call does not scale to a bulk backfill
of ~1,972 annual reports, ~1,343 concalls and red-flag classification over
the same corpus.

These schemas are enforced at DECODE time instead, so valid JSON is produced
by construction.

THE SCHEMAS MUST MATCH THE PARSERS, NOT JUST BE VALID JSON
----------------------------------------------------------
A schema that is valid JSON but the wrong shape moves the failure rather
than fixing it. Each schema below is derived from the corresponding
`app/tasks/*.py::_normalize()` and its validator, and
`tests/test_schemas_match_parsers.py` asserts that a schema-shaped payload
survives the real parser with every field populated.

xgrammar COMPATIBILITY (vLLM 0.28.0, backend='auto')
----------------------------------------------------
Verified against vllm/v1/structured_output/backend_xgrammar.py at tag
v0.28.0 (`has_xgrammar_unsupported_json_features`). A schema is pushed off
xgrammar onto a fallback backend if it uses any of:

    multipleOf                      (integer/number)
    uniqueItems, contains,
    minContains, maxContains        (array)
    an unsupported string `format`
    patternProperties, propertyNames (object)

None of those appear here. `minItems`/`maxItems` are NOT on that list, so
the 3-5 bound on annual-report bullets is expressible without forcing a
backend switch.

WHAT IS DELIBERATELY *NOT* CONSTRAINED
--------------------------------------
Only SHAPE is enforced. Compliance (forward-tense words, forbidden
vocabulary, financial figures) stays with the validators in
`app/compliance/validators.py`, which run after generation exactly as
RedixFi's do. Encoding compliance into the grammar would silently change
what the model is being measured on: production's gpt-4o-mini reference
had to satisfy those rules through the prompt alone, so the candidate must
too, or the comparison stops being like-for-like.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from ..prompts.annual_report_summary import BULLET_MAX, BULLET_MIN
from ..prompts.concall_summary import TONE_LABELS

# A nullable string, spelled the way xgrammar handles cleanly.
_NULLABLE_STRING: Dict[str, Any] = {
    "anyOf": [{"type": "string"}, {"type": "null"}]
}


def annual_report_summary_schema() -> Dict[str, Any]:
    """CURRENT Stage 3 contract — see app/tasks/annual_report_summary.py.

    `key_points` carries the 3-5 bound the validator enforces, so a
    count violation is prevented at decode time rather than costing a
    regenerate attempt. `important_risks` has NO minItems: an empty list is
    a legitimate, common answer ("no risks genuinely supported by the
    selected evidence").
    """
    return {
        "type": "object",
        "properties": {
            "executive_summary": {"type": "string"},
            "key_points": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": BULLET_MIN,
                "maxItems": BULLET_MAX,
            },
            "important_risks": {"type": "array", "items": {"type": "string"}},
            "key_takeaway": {"type": "string"},
        },
        "required": [
            "executive_summary", "key_points", "important_risks", "key_takeaway",
        ],
        "additionalProperties": False,
    }


def annual_report_summary_legacy_schema() -> Dict[str, Any]:
    """LEGACY (pre-Evidence-Finder) 3-field contract — `bullets`, not
    `key_points`, and NO `important_risks`. See
    app/prompts/annual_report_summary_legacy.py for why this era still
    matters: all 72 production references were written under it."""
    return {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "bullets": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": BULLET_MIN,
                "maxItems": BULLET_MAX,
            },
            "key_takeaway": {"type": "string"},
        },
        "required": ["summary", "bullets", "key_takeaway"],
        "additionalProperties": False,
    }


def concall_summary_schema() -> Dict[str, Any]:
    """Concall contract. `tone_label` is a CLOSED SET, and constraining it
    here is the single highest-value use of guided decoding in this project:
    it is the one objectively-scorable field in any summarization phase, and
    an out-of-set label is a hard validation failure in production."""
    return {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "tone_label": {"type": "string", "enum": list(TONE_LABELS)},
            "tone_note": {"type": "string"},
        },
        "required": ["summary", "tone_label", "tone_note"],
        "additionalProperties": False,
    }


def red_flag_schema(candidates: Sequence[str]) -> Dict[str, Any]:
    """PER-REQUEST schema — the only dynamic one.

    `category` must be one of THIS chunk's keyword candidates, or null. It
    is not the full RISK_FLAG_CATEGORIES set: app/tasks/red_flag.py rejects
    a category outside the candidate list, mirroring
    risk_flag_classifier.classify_chunk. Building the enum from the
    candidates makes that rejection unreachable rather than merely handled.

    null is a first-class value here: "this excerpt does not genuinely
    discuss any candidate category" is the correct answer for a keyword
    false positive, and 2 of the 6 first-run cases were exactly that.
    """
    cats = [c for c in candidates if c]
    if not cats:
        raise ValueError(
            "red_flag_schema requires at least one candidate category; a chunk "
            "with no keyword match never reaches an LLM call in production"
        )
    return {
        "type": "object",
        "properties": {
            "category": {
                "anyOf": [
                    {"type": "string", "enum": cats},
                    {"type": "null"},
                ]
            },
            # Empty string is the documented value when category is null.
            "summary": {"type": "string"},
        },
        "required": ["category", "summary"],
        "additionalProperties": False,
    }


def ask_ai_schema() -> Dict[str, Any]:
    """Ask AI contract — mirrors core/ask.py::call_llm_ask's parse:
    {"answer": str, "refused": bool, "refusal_reason": str|null}."""
    return {
        "type": "object",
        "properties": {
            "answer": {"type": "string"},
            "refused": {"type": "boolean"},
            "refusal_reason": _NULLABLE_STRING,
        },
        "required": ["answer", "refused", "refusal_reason"],
        "additionalProperties": False,
    }


# Static schemas by task name. red_flag is absent on purpose: it is built
# per request from the case's candidates via schema_for_task().
STATIC_SCHEMAS = {
    "annual_report_summary": annual_report_summary_schema,
    "annual_report_summary_legacy": annual_report_summary_legacy_schema,
    "concall_summary": concall_summary_schema,
    "ask_ai": ask_ai_schema,
}


def schema_for_task(
    task: str, fixture: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    """The schema a task should decode against, or None if it has no
    enforceable shape. `fixture` is only needed for red_flag."""
    if task == "red_flag":
        candidates: List[str] = list((fixture or {}).get("candidates") or [])
        if not candidates:
            return None
        return red_flag_schema(candidates)
    builder = STATIC_SCHEMAS.get(task)
    return builder() if builder else None


# ---------------------------------------------------------------------------
# xgrammar compatibility guard
# ---------------------------------------------------------------------------
# Mirrors has_xgrammar_unsupported_json_features from
# vllm/v1/structured_output/backend_xgrammar.py @ v0.28.0. Kept here so a
# future schema edit that would silently push decoding onto a fallback
# backend fails a local test instead of surprising a metered GPU run.
_XGRAMMAR_UNSUPPORTED = {
    ("integer", "multipleOf"), ("number", "multipleOf"),
    ("array", "uniqueItems"), ("array", "contains"),
    ("array", "minContains"), ("array", "maxContains"),
    ("object", "patternProperties"), ("object", "propertyNames"),
}
# xgrammar's own supported string formats at v0.28.0.
_XGRAMMAR_STRING_FORMATS = {
    "date-time", "date", "time", "duration", "email", "hostname",
    "ipv4", "ipv6", "uuid",
}


def xgrammar_unsupported_features(schema: Dict[str, Any]) -> List[str]:
    """Returns the unsupported constructs found, empty when xgrammar-safe."""
    found: List[str] = []

    def walk(obj: Any, path: str = "$") -> None:
        if isinstance(obj, dict):
            node_type = obj.get("type")
            for t, key in _XGRAMMAR_UNSUPPORTED:
                if node_type == t and key in obj:
                    found.append(f"{path}: '{key}' on type '{t}'")
            if node_type == "string" and "format" in obj:
                if obj["format"] not in _XGRAMMAR_STRING_FORMATS:
                    found.append(f"{path}: unsupported string format {obj['format']!r}")
            for key, value in obj.items():
                walk(value, f"{path}.{key}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                walk(item, f"{path}[{i}]")

    walk(schema)
    return found
