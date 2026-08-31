"""Red Flag / risk classification prompt — VENDORED COPY.

PROVENANCE
----------
Original RedixFi file: data-pipeline/risk_flag_classifier.py
Sections copied:  _SYSTEM_PROMPT, _call_llm_confirm()'s user-content shape,
                  RISK_FLAG_CATEGORIES, _KEYWORD_PATTERNS / matched_categories()
Source commit:    b9e40c4 (2026-08-24)
RedixFi HEAD at copy time: 8bb3170
Date copied:      2026-08-28

WHICH LLM WORKLOAD THIS ACTUALLY IS — read before evaluating
------------------------------------------------------------
RedixFi's Red Flag feature has two stages, and only ONE of them uses an LLM:

  * INGESTION TIME  -> risk_flag_classifier.classify_chunk(): a keyword
    prefilter, then ONE gpt-4o-mini call per matched chunk that confirms a
    genuine category match and writes a short neutral summary. THIS is the
    workload reproduced here.
  * QUERY TIME      -> api/app/core/red_flag_ask.py: ZERO LLM calls. It
    assembles the already-stored risk_flag_summary metadata into a table.
    There is no generation to compare, so it is not evaluated.

Comparing "Red Flag output" therefore means comparing per-chunk
confirm-and-summarize decisions, which is what the fixtures carry.

METADATA CONTRACT (reproduced faithfully in app/tasks/red_flag.py):
a confirmed result yields risk_flag_type + risk_flag_summary; anything
unconfirmed, non-compliant, or failed yields neither key — never a null.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List

RISK_FLAG_CATEGORIES = (
    "auditor_qualification", "contingent_liability",
    "related_party_transaction", "promoter_pledge",
)

# Verbatim from risk_flag_classifier.py::_KEYWORD_PATTERNS. Included so a
# fixture's candidate list can be re-derived offline and asserted equal to
# what the pipeline recorded — a guard against silent divergence, not a
# second implementation of evidence selection.
KEYWORD_PATTERNS: Dict[str, "re.Pattern"] = {
    "auditor_qualification": re.compile(
        r"\bqualified\s+opinion\b|\bemphasis\s+of\s+matter\b|\bauditor'?s?\s+qualification\b|"
        r"\badverse\s+opinion\b|\bdisclaimer\s+of\s+opinion\b|\bmaterial\s+weakness\b|"
        r"\bkey\s+audit\s+matter\b",
        re.IGNORECASE,
    ),
    "contingent_liability": re.compile(
        r"\bcontingent\s+liabilit(y|ies)\b|\bcontingent\s+claims?\b|"
        r"\bpending\s+litigation\b|\blegal\s+proceedings?\s+against\b|\bguarantees?\s+given\b",
        re.IGNORECASE,
    ),
    "related_party_transaction": re.compile(
        r"\brelated\s+part(y|ies)\s+transactions?\b|\brelated\s+part(y|ies)\s+disclosures?\b|"
        r"\btransactions?\s+with\s+related\s+part(y|ies)\b",
        re.IGNORECASE,
    ),
    "promoter_pledge": re.compile(
        r"\bpledge\s+of\s+shares?\b|\bpledged\s+shares?\b|\bshares?\s+pledged\b|"
        r"\bpromoter\s+pledg\w*\b|\bencumbrance\s+of\s+promoter\b",
        re.IGNORECASE,
    ),
}


def matched_categories(text: str) -> List[str]:
    """Verbatim from risk_flag_classifier.py::matched_categories."""
    return [cat for cat, pat in KEYWORD_PATTERNS.items() if pat.search(text or "")]


SYSTEM_PROMPT = (
    "You confirm whether a document excerpt genuinely discusses one of a "
    "small set of governance/risk categories, or is just a false keyword "
    "match. Categories: auditor_qualification (a qualified/adverse audit "
    "opinion, emphasis of matter, material weakness), contingent_liability "
    "(a contingent liability, pending litigation, guarantee given), "
    "related_party_transaction (a disclosed transaction with a related "
    "party/promoter entity), promoter_pledge (promoter shares pledged or "
    "encumbered). Given the excerpt and its candidate categories, respond "
    "with JSON: {\"category\": one of the candidate category strings, or "
    "null if the excerpt does not genuinely discuss any of them, "
    "\"summary\": a short, neutral, factual 1-2 sentence restatement of "
    "what the excerpt states about it, with no commentary, no numbers, no "
    "forward-looking language, no investment advice — empty string if "
    "category is null}."
    " CONTROLLED FIX (2026-08-30): A disclosure is NOT automatically a "
    "material red flag. Key Audit Matters, Emphasis of Matter paragraphs, "
    "standard audit disclosures, generic definitions of contingent "
    "liabilities, routine related-party disclosures, and ordinary "
    "promoter-pledge notes are evidence that a topic was mentioned — not "
    "proof that a material governance/financial risk exists. Only confirm a "
    "category when the excerpt shows a company-specific fact/event/risk: an "
    "actual qualified/adverse audit opinion, an actual pending claim or "
    "guarantee against the company, an actual transaction with a related "
    "party/promoter entity that creates risk, or an actual pledge of "
    "promoter shares. If the excerpt only describes a definition, generic "
    "policy, or standard disclosure without a company-specific material "
    "fact, return category: null. The summary must restate the specific "
    "company fact that justifies the category, not the generic definition."
)


def build_user_content(fixture: Dict[str, Any]) -> str:
    """Reproduces risk_flag_classifier.py::_call_llm_confirm's user content."""
    candidates = fixture.get("candidates") or []
    return (
        f"Candidate categories: {', '.join(candidates)}\n\n"
        f"Excerpt:\n{fixture.get('chunk_text') or ''}"
    )
