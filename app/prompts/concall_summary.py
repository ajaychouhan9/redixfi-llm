"""Concall / investor-presentation summary prompt — VENDORED COPY.

PROVENANCE
----------
Original RedixFi file: data-pipeline/concall_summarizer.py
Sections copied:  SYSTEM_PROMPT, _user_content()'s input contract,
                  TONE_LABELS, MAX_TRANSCRIPT_CHARS, MAX_ATTEMPTS,
                  generate_summary()'s validation set
Source commit:    f49c989-era file, unchanged through 8bb3170
RedixFi HEAD at copy time: 8bb3170
Date copied:      2026-08-28

WHY THIS IS THE PRIMARY SUMMARIZATION BENCHMARK
-----------------------------------------------
Two reasons, both measured against production on 2026-08-28:

  1. **Volume.** 4,157 documents carry a gpt-4o-mini `summary` +
     `tone_label` + `tone_note`, against 72 for annual reports.
  2. **No pipeline drift.** `concall_summarizer.py` sends a flat
     `raw_transcript_text[:120_000]` front slice and has NOT been rewired
     through Evidence Finder. The code path that produced every stored
     reference is the code path that exists today, so the input is exactly
     reproducible — unlike Phase A, where the references predate the
     Evidence Finder change.

OUTPUT CONTRACT
---------------
`{"summary": 120-180 words, "tone_label": one of TONE_LABELS,
  "tone_note": one sentence}`.

`tone_label` is a CLOSED SET. A candidate model returning anything outside
it is a hard validation failure, exactly as it is in production — that is
a genuinely objective, non-judgement signal, and one of the few places a
summarization benchmark gets one.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

PIPELINE_VERSION = "concall_front_slice"
PROMPT_VERSION = "concall_summarizer@8bb3170"

TONE_LABELS = ("Positive", "Neutral", "Negative", "Mixed")
MAX_TRANSCRIPT_CHARS = 120_000
MAX_ATTEMPTS = 3

SYSTEM_PROMPT = (
    "You summarize a single exchange-filed corporate document (an earnings "
    "concall transcript or investor presentation) for a pre-RA "
    "(pre-SEBI-registration) Indian stock analytics product. "
    "STRICT RULES: "
    "(1) Base the summary ONLY on the text given below — never use outside "
    "knowledge about this company, never speculate. "
    "(2) Write NEUTRALLY and ATTRIBUTIVELY — always frame statements as "
    "what management/the document said or reported (\"management said\", "
    "\"the presentation reported\"), never as RedixFi's own claim or "
    "opinion. "
    "(3) Past/present tense only — describe what was said or what the data "
    "in the document shows, never what might happen next. Never use: "
    "expect, likely, will, outlook, target, forecast, going to, should "
    "rise/fall, recommend, buy, sell, calls, picks, tips, predictions, "
    "stop-loss, accuracy — INCLUDING when describing guidance/goals "
    "management stated: rephrase as \"management set a goal of X\" / "
    "\"management guided toward X\" / \"the document stated a plan to "
    "reach X\", never \"targeting X\", \"expects X\", or \"aims for an "
    "outlook of X\". "
    "(4) Never add a verdict, rating, or directional view on the stock — "
    "this is a summary of a document, not investment advice or a signal. "
    "(5) tone_label describes ONLY the language/emphasis used IN THIS "
    "DOCUMENT (e.g. management emphasizing growth vs. flagging "
    "headwinds) — it is NOT a prediction or rating of the stock. Pick "
    f"exactly one of: {', '.join(TONE_LABELS)}. "
    "(6) tone_note is one short neutral sentence explaining the tone_label "
    "choice, following the same past-tense/no-forward-language/no-verdict "
    "rules as the summary. "
    "(7) When referring to this document as a meeting, always qualify the "
    "word \"call\" with what kind of call it is — \"the earnings call\", "
    "\"the conference call\", \"the analyst call\" — never a bare \"the "
    "call\"/\"a call\"/\"this call\" on its own with no qualifier "
    "immediately before it (WRONG: \"The call concluded with...\". RIGHT: "
    "\"The earnings call concluded with...\" or \"The discussion "
    "concluded with...\"). This is because the bare word \"call\" alone "
    "is reserved in this product for forbidden trading-recommendation "
    "language, but \"earnings call\"/\"conference call\" describing the "
    "actual document is fine and expected. "
    "Respond ONLY with a JSON object: {\"summary\": \"...\" (120-180 "
    f"words), \"tone_label\": one of {list(TONE_LABELS)}, \"tone_note\": "
    "\"...\"}. No markdown, no preamble."
)


def build_user_content(
    fixture: Dict[str, Any], corrective_note: Optional[str] = None,
) -> str:
    """Reproduces concall_summarizer.py::_user_content().

    `input_text` is the already-sliced `raw_transcript_text[:120_000]`,
    captured at export time so the benchmark never has to re-derive it (and
    so the slice can never drift from what production actually sent).

    `doc_kind` is the same derived label production computes:
    `subject == "EARNINGS_CALL_TRANSCRIPT"` -> "earnings concall transcript",
    anything else -> "investor presentation". It is resolved at export time
    from the real `subject` field, not guessed here."""
    content = (
        f"Company: {fixture.get('company_name')} ({fixture.get('symbol')})\n"
        f"Document type: {fixture.get('doc_kind') or 'investor presentation'}\n"
        f"Filing date: {fixture.get('filing_date')}\n\n"
        f"Document text:\n{fixture.get('input_text') or ''}"
    )
    if corrective_note:
        content += (
            f"\n\n(Your previous attempt was rejected: {corrective_note}. "
            "Rewrite following the rules exactly.)"
        )
    return content
