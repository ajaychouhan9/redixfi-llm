"""Annual Report Summary — LEGACY (pre-Evidence-Finder) prompt. VENDORED COPY.

PROVENANCE
----------
Original RedixFi file: data-pipeline/annual_report_summarizer.py
Sections copied:  SYSTEM_PROMPT, _user_content(), _build_report_text()'s
                  front-slice contract, BULLET_MIN/BULLET_MAX, MAX_ATTEMPTS
Source commit:    b9e40c4~1 — i.e. the tree immediately BEFORE the Evidence
                  Finder unification landed (b9e40c4, 2026-08-24)
RedixFi HEAD at copy time: 8bb3170
Date copied:      2026-08-28

WHY A SECOND, OLDER COPY OF THE SAME PROMPT EXISTS
--------------------------------------------------
All 72 production annual-report summaries were written on **2026-08-16**,
between 12:42 and 16:44 (`summarized_at`). The Evidence Finder unification
landed **2026-08-24**. So every stored reference was produced by THIS
prompt against THIS input contract — not by the current Stage 3.

Keeping the legacy pair lets the benchmark compare like with like:
  * LEGACY_REFERENCE : gpt-4o-mini + front-slice input + 3-field schema
  * candidate replay : same prompt, same input, different model
and separately run the CURRENT pipeline (Evidence Finder + 4-field schema)
without conflating the two.

DEPLOYMENT AMBIGUITY — CHECKED, NOT ASSUMED
-------------------------------------------
Three commits touched this file on 2026-08-16 (921e121 16:54 IST, 80a954d
18:39 IST, f25d480 22:59 IST), so which one was live during the run is not
knowable from the data. It does not matter: SYSTEM_PROMPT is **byte-
identical across all three and through b9e40c4~1** (verified by md5). The
prompt is therefore unambiguous.

The INPUT path is not equally unambiguous — f25d480 added BUG 10's
token-aware fallback. It only diverges for a document whose
`raw_text[:150_000]` exceeds MAX_REPORT_TOKENS, so the exporter measures
each document and marks any that could have taken a different path. For a
document under the limit both versions produce a byte-identical slice.

OUTPUT SCHEMA — 3 fields, NOT 4
-------------------------------
`summary` / `bullets` / `key_takeaway`. There is NO `important_risks` and
NO `executive_summary`. Confirmed against production: `executive_summary`
and `key_points` exist on 0 documents; `summary`, `bullets` and
`key_takeaway` on exactly 72.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

PIPELINE_VERSION = "legacy_front_slice_pre_evidence_finder"
SOURCE_COMMIT = "b9e40c4~1"
PROMPT_VERSION = "annual_report_summarizer@2026-08-16"

BULLET_MIN = 3
BULLET_MAX = 5
MAX_ATTEMPTS = 3

# The legacy input contract: a flat front slice of raw_text.
MAX_REPORT_CHARS = 150_000
# BUG 10's ceiling (added f25d480). Only relevant to documents whose slice
# exceeds it — see the deployment-ambiguity note above.
MAX_REPORT_TOKENS = 100_000

SYSTEM_PROMPT = (
    "You summarize a single exchange-filed corporate annual report for a "
    "pre-RA (pre-SEBI-registration) Indian stock analytics product. "
    "STRICT RULES: "
    "(1) Base the summary ONLY on the text given below — never use outside "
    "knowledge about this company, never speculate. "
    "(2) Write NEUTRALLY and ATTRIBUTIVELY — always frame statements as "
    "what management/the report said or stated (\"management said\", "
    "\"the report stated\"), never as RedixFi's own claim or opinion. "
    "(3) Past/present tense only — describe what was said or what the "
    "document states, never what might happen next. Never use: expect, "
    "likely, will, outlook, target, forecast, going to, should rise/fall, "
    "recommend, buy, sell, calls, picks, tips, predictions, stop-loss, "
    "accuracy — INCLUDING when describing guidance/goals management "
    "stated: rephrase as \"management set a goal of X\" / \"management "
    "stated a plan to reach X\", never \"targeting X\" or \"expects X\". "
    "(4) NEVER state a specific financial figure as fact — no revenue, "
    "profit, margin, growth-rate, or any other number, currency amount, or "
    "percentage, even if the document appears to state one. This is because "
    "PDF table extraction from annual reports can mislabel figures (e.g. "
    "confusing revenue with order backlog) — describe direction or theme in "
    "words only (e.g. \"the report described continued investment in "
    "capacity expansion\"), never a quantity. "
    "(5) Cover ONLY qualitative strategic themes — manufacturing strategy, "
    "sustainability, market positioning, stated priorities, capital "
    "allocation focus, governance — never treat the document as a source "
    "of verified financial data. "
    "(6) Never add a verdict, rating, or directional view on the stock — "
    "this is a summary of a document, not investment advice or a signal. "
    f"Respond ONLY with a JSON object: {{\"summary\": \"...\" (3-4 "
    f"sentences), \"bullets\": [...] ({BULLET_MIN}-{BULLET_MAX} short "
    "strategic-theme bullet strings), \"key_takeaway\": \"...\" (one "
    "sentence — the single most important qualitative point in the "
    "document)}. No markdown, no preamble."
)


def build_user_content(
    fixture: Dict[str, Any], corrective_note: Optional[str] = None,
) -> str:
    """Reproduces the LEGACY _user_content(). Identical in shape to the
    current one — only the text it wraps differs, and that text is
    `legacy_input_text` (the front slice) rather than Evidence Finder
    evidence."""
    content = (
        f"Company: {fixture.get('company_name')} ({fixture.get('symbol')})\n"
        f"Document type: annual report\n"
        f"Fiscal year: {fixture.get('fiscal_year')}\n"
        f"Filing date: {fixture.get('filing_date')}\n"
        f"Page count: {fixture.get('page_count')}\n\n"
        f"Document text:\n{fixture.get('legacy_input_text') or ''}"
    )
    if corrective_note:
        content += (
            f"\n\n(Your previous attempt was rejected: {corrective_note}. "
            "Rewrite following the rules exactly.)"
        )
    return content
