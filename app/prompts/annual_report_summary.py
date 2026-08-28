"""Annual Report Summary prompt — VENDORED COPY.

PROVENANCE
----------
Original RedixFi file: data-pipeline/annual_report_summarizer.py
Sections copied:  SYSTEM_PROMPT, _user_content(), BULLET_MIN/BULLET_MAX,
                  MAX_ATTEMPTS, the regenerate-then-validate contract
Source commit:    b9e40c4 (2026-08-24, "Evidence Finder unification")
RedixFi HEAD at copy time: 8bb3170
Date copied:      2026-08-28

The SYSTEM_PROMPT below is character-for-character what RedixFi sends to
gpt-4o-mini today. Do NOT reword it to make a candidate model score better
— that would invalidate the comparison, which is the entire point of this
project.

EVIDENCE, NOT RAW TEXT
----------------------
The `evidence_text` this prompt consumes is produced by RedixFi's own
data-pipeline/evidence_finder.py (deterministic, LLM-free, global 20k-token
budget) and captured into the fixture by scripts/export_fixtures.py. This
project does NOT re-select evidence. Note that RedixFi's Stage 3 re-chunks
Mongo `raw_text` in-process and does NOT read ChromaDB on its normal path.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

# Same bounds RedixFi validates against after generation.
BULLET_MIN = 3
BULLET_MAX = 5

# RedixFi's offline-batch deviation from ask.py's live 2-attempt budget.
MAX_ATTEMPTS = 3

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
    f"Respond ONLY with a JSON object: {{\"executive_summary\": \"...\" (3-4 "
    f"sentences), \"key_points\": [...] ({BULLET_MIN}-{BULLET_MAX} short "
    "strategic-theme bullet strings), \"important_risks\": [...] (an array of "
    "short risk statements ONLY if genuinely supported by the selected "
    "evidence; empty array if not), \"key_takeaway\": \"...\" (one "
    "sentence — the single most important qualitative point in the "
    "document)}. No markdown, no preamble."
)


def build_user_content(
    fixture: Dict[str, Any], corrective_note: Optional[str] = None,
) -> str:
    """Reproduces annual_report_summarizer.py::_user_content() exactly.

    `fixture["evidence_text"]` is the Evidence Finder output captured from
    the real pipeline — it takes the place of `_build_report_text(doc)`,
    which is the ONLY substitution, and it is a substitution of value not
    of shape: the string is byte-identical to what Stage 3 would have
    built for this document.
    """
    content = (
        f"Company: {fixture.get('company_name')} ({fixture.get('symbol')})\n"
        f"Document type: annual report\n"
        f"Fiscal year: {fixture.get('fiscal_year')}\n"
        f"Filing date: {fixture.get('filing_date')}\n"
        f"Page count: {fixture.get('page_count')}\n\n"
        f"Document text:\n{fixture.get('evidence_text') or ''}"
    )
    if corrective_note:
        content += (
            f"\n\n(Your previous attempt was rejected: {corrective_note}. "
            "Rewrite following the rules exactly.)"
        )
    return content
