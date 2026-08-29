"""EXPERIMENTAL concall prompt variant — ONE line forbidding markdown.

⚠️ NOT THE PRODUCTION PROMPT. `app/prompts/concall_summary.py` holds the
vendored production copy, guarded by `tests/test_prompts_match_redixfi.py`.
Nothing in the standard benchmark path imports this file.

WHY THIS EXISTS
---------------
The head-to-head eval (2026-08-29) found Qwen3-14B and Ministral 3 14B
TIED on concall generation (15/20 both), but on annual_report Ministral
scored 3/20 against Qwen's 17/20, and the dominant reason was NOT the
compliance content — it was markdown: Ministral emitted `**bold**` in
18/20 annual_report outputs and 15/20 concall outputs against Qwen's 0/20
on both, despite the production prompt already stating "No markdown, no
preamble" once, at the very end.

That single terminal instruction evidently is not landing for Ministral.
This variant adds exactly ONE additional, explicit, unambiguous line
forbidding markdown — nothing else about the prompt changes. It is applied
IDENTICALLY to both models, at PRODUCTION retry policy (no sampling
variation, no directive notes) and the production 3-attempt budget, so any
difference in outcome is attributable to this one line and nothing else.

THIS IS A FAIRNESS TEST, NOT A TUNING PASS FOR EITHER MODEL
-------------------------------------------------------------
The question it answers is narrow: does naming the markdown prohibition
more forcefully change behaviour, and if so, does that also make the
forbidden-figure violations (33%, 70%, 1.01% — previously found INSIDE the
markdown) go away, or were those independent of the markdown itself?
Neither outcome should be read as a verdict on either model — see
MINISTRAL_EVAL.md for that discussion, and the founder's own read of the
resulting numbers.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from .concall_summary import (  # noqa: F401  (re-exported for the runner)
    MAX_ATTEMPTS,
    TONE_LABELS,
    build_user_content,
)
from .concall_summary import SYSTEM_PROMPT as _PRODUCTION_SYSTEM_PROMPT

VARIANT_NAME = "concall_markdown_fairness_v1"

# ONE added instruction. Direct, unambiguous, and framed as an absolute
# rule rather than a stylistic preference, since the existing terminal
# "No markdown, no preamble" phrasing was not enough for one of the two
# models under test.
_MARKDOWN_BAN = (
    " ABSOLUTE FORMATTING RULE: your response must be PLAIN TEXT ONLY. Do "
    "NOT use asterisks, bold, italics, underlines, headers, bullet points, "
    "numbered lists, or any markdown formatting of any kind, anywhere in "
    "your response — including inside the JSON string values. Write every "
    "sentence as plain prose with no special characters for emphasis."
)

# Production text imported, never retyped, so this variant cannot drift
# from production independently of the vendored copy. The ban is appended
# as the LAST instruction so it is not visually buried by rules (1)-(7).
SYSTEM_PROMPT = _PRODUCTION_SYSTEM_PROMPT + _MARKDOWN_BAN


def build_variant_user_content(
    fixture: Dict[str, Any], corrective_note: Optional[str] = None,
) -> str:
    """Identical to production's user content — only the SYSTEM prompt
    differs, so the evidence the model sees is unchanged."""
    return build_user_content(fixture, corrective_note)
