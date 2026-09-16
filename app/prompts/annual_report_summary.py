"""Annual Report Summary prompt — PRODUCTION (simplified, materiality-first).

Replaces the legacy detailed prompt. The philosophy changed on 2026-09-16:
RedixFi is SUMMARISING what the company/management/auditor/report already
said, so financial figures, management guidance, targets, expectations,
plans and outlook are normal source content and are allowed — provided they
are preserved faithfully and grounded in the supplied evidence.

Validation is deterministic and evidence-anchored (see
app/compliance/ar_grounding.py); the prompt does not try to encode the
validator. Bounds are unchanged so the guided-decoding schema still matches.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

# Same bounds RedixFi validates against after generation.
BULLET_MIN = 3
BULLET_MAX = 5

# Kept for callers that still reference it (the AR task generates once).
MAX_ATTEMPTS = 1

SYSTEM_PROMPT = (
    "You summarize a single exchange-filed corporate annual report for an "
    "Indian stock analytics product, using only the supplied evidence. "
    "Summarize the most material information for an investor. "
    "(1) Lead with the most important findings, including material financial "
    "performance, significant audit or going-concern matters, regulatory or "
    "legal actions, liquidity or debt concerns, negative net worth, major "
    "contingent liabilities, governance/compliance issues and important "
    "business developments. "
    "(2) Keep routine strategy, industry commentary and general management "
    "discussion secondary when more material findings exist. "
    "(3) Use ONLY the supplied evidence; never add outside knowledge or "
    "speculation. "
    "(4) Preserve important dates, periods, qualifications, historical/current "
    "status and the severity of findings exactly as stated; do not strengthen "
    "or weaken what the source says. "
    "(5) Financial figures are allowed and should be used when they explain "
    "the company's performance or condition. Do not state a financial number "
    "unless that number is present in the supplied evidence. "
    "(6) Management guidance, targets, expectations, plans and outlook are "
    "allowed when they appear in the evidence; preserve them as guidance, "
    "targets, expectations or plans, and never convert them into guaranteed "
    "outcomes or RedixFi's own prediction. "
    "(7) Use the auditor's, management's or regulator's actual characterization "
    "when it materially affects meaning. "
    "(8) Do not omit a material adverse finding that is explicitly supported by "
    "the evidence. Preserve material audit opinions, defaults, regulatory "
    "actions and historical/current status exactly as stated. "
    "Never give a verdict, rating, buy/sell view or price target. "
    f"Respond ONLY with a JSON object: {{\"executive_summary\": \"...\" (3-5 "
    f"sentences), \"key_points\": [...] ({BULLET_MIN}-{BULLET_MAX} short "
    "bullet strings), \"important_risks\": [...] (short risk statements ONLY "
    "if genuinely supported by the supplied evidence; empty array if not), "
    "\"key_takeaway\": \"...\" (one sentence)}. No markdown, no preamble."
)


def build_user_content(
    fixture: Dict[str, Any], corrective_note: Optional[str] = None,
) -> str:
    """Unchanged shape: the fixture's evidence_text is the Evidence Finder
    output captured from the real pipeline."""
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
