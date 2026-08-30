"""EXPERIMENTAL concall variant — retrieval-augmented few-shot from the
example bank, not a hand-written instruction.

⚠️ NOT THE PRODUCTION PROMPT. `app/prompts/concall_summary.py` holds the
vendored production copy. The SYSTEM PROMPT here is that copy, UNMODIFIED
— this variant changes only the USER content, by prepending 1-2 real
retrieved prior successes before the current case's document text.

WHY THE SYSTEM PROMPT STAYS UNTOUCHED
--------------------------------------
Every hand-written system-prompt addition tried this session either
helped narrowly (the markdown ban) or backfired broadly (steering,
red_flag's instance-check). The suspected common thread is negation
priming — naming forbidden vocabulary to warn against it appears to
raise its own probability (see the retry_policy_negation_priming
finding). Retrieved examples sidestep that: they are POSITIVE
demonstrations of real accepted input->output pairs, with no forbidden
words named, no new rules stated, and no system-prompt text at all. If
this variant changes behaviour, the mechanism is different from every
other change tried this session, which is the point of testing it.

WHY EXAMPLES GO IN THE USER MESSAGE, NOT THE SYSTEM MESSAGE
--------------------------------------------------------------
The system prompt states timeless rules; per-case content belongs in the
user message, and retrieved examples are exactly that — dynamic,
case-specific content chosen fresh for every request. Putting them in the
system message would also make this indistinguishable from the
already-tried few-shot variant (`concall_summary_variant.py`), which
hard-codes a FIXED set of examples in the system prompt. The whole point
here is that the examples are RETRIEVED per case from an ACCUMULATING
bank, not fixed.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..example_bank import output_text_for, retrieval_text_for, retrieve
from .concall_summary import build_user_content as _production_user_content
from .concall_summary import SYSTEM_PROMPT  # noqa: F401  (re-exported, unmodified)

VARIANT_NAME = "concall_fewshot_bank_v1"


def _format_example(entry: Dict[str, Any], index: int) -> str:
    out = entry.get("output") or {}
    summary = out.get("summary") or ""
    tone_label = out.get("tone_label") or ""
    tone_note = out.get("tone_note") or ""
    return (
        f"--- Real example {index}, previously accepted for a similar document ---\n"
        f"{{\"summary\": {summary!r}, \"tone_label\": {tone_label!r}, "
        f"\"tone_note\": {tone_note!r}}}"
    )


def build_variant_user_content(
    fixture: Dict[str, Any],
    bank_entries: List[Dict[str, Any]],
    corrective_note: Optional[str] = None,
    k: int = 2,
) -> str:
    """Retrieves up to `k` similar validated examples from the bank
    (excluding this fixture's own benchmark_id, so a case never retrieves
    its own stored answer) and prepends them before the PRODUCTION user
    content, which is otherwise byte-identical to the unmodified path."""
    bid = str(fixture.get("benchmark_id") or fixture.get("fixture_id") or "")
    query = retrieval_text_for("concall_summary", fixture)
    examples = retrieve(bank_entries, query, k=k, exclude_benchmark_id=bid)

    base = _production_user_content(fixture, corrective_note)
    if not examples:
        return base

    header = (
        "Before the document to summarize, here are real examples of "
        "compliant summaries this system previously produced for similar "
        "documents. They show accepted STYLE and PHRASING for content like "
        "this — do not copy their facts, only their approach to compliant "
        "phrasing of similar situations.\n\n"
    )
    blocks = "\n\n".join(_format_example(e, i + 1) for i, e in enumerate(examples))
    return header + blocks + "\n\n" + base
