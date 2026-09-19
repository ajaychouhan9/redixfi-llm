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


# 2026-09-19 STAGE 1 PROMOTION — production prompt. History:
#   Original (pre-2026-08-30): pure topic-relevance confirmation.
#   CONTROLLED FIX (2026-08-30): one blanket "policy vs instance"
#     instruction appended, uniformly across all 4 categories. Measured
#     (n=60, evaluation/red_flags/runs/) as a NET REGRESSION: fixed all 7
#     known false positives but caused 26 new false negatives (agreement
#     0.85 -> 0.5167), concentrated in auditor_qualification wrongly
#     excluding genuine adverse Key Audit Matters. Never reverted after
#     that finding — production ran this worse-than-original prompt from
#     2026-08-30 until today (confirmed live on the VM, 2026-09-19).
#   STAGE 0 REVERT (2026-09-19, earlier today): removed the CONTROLLED FIX
#     paragraph, restoring the original text (0.85 agreement, already
#     known better than the alternative) as a zero-eval-needed correctness
#     fix.
#   STAGE 1 (this promotion): a from-scratch rewrite (formerly `app/
#     prompts/red_flag_stage1_v1.py`, VARIANT_NAME="red_flag_stage1_v1"),
#     informed by BOTH the CONTROLLED FIX regression AND RedixFi's own
#     2026-09-19 gpt-4o-mini fix (data-pipeline/risk_flag_classifier.py) —
#     asymmetric per category (full policy-vs-instance framing for
#     contingent_liability/related_party_transaction, ONLY positive
#     framing for auditor_qualification, never naming "Key Audit Matter"/
#     "unmodified opinion" as exclusions, per the redixfi-qwen-prompt-
#     negation-priming finding on a different task) and adds an explicit
#     `is_red_flag` field. VALIDATED before promotion: run on Kaggle
#     T4x2/qwen3-14b-awq-tp2 against the 60-case red_flag_benchmark.json.
#     The raw comparison against the OLD (pre-fix) reference showed only
#     0.45 agreement — alarming at first read, until the reference itself
#     was re-scored against RedixFi's CORRECTED gpt-4o-mini classifier:
#     the OLD reference agreed with the CORRECTED one on only 27/60 =
#     0.450 cases — the exact same number, proving the "regression" was
#     entirely an artifact of comparing against a known-stale reference.
#     Re-scored against the CORRECTED reference, this prompt agreed on
#     54/60 = 0.900, with the 6 disagreements individually reviewed as
#     ordinary model-to-model judgment calls (e.g. a claim-types-named-
#     but-no-amount contingent-liability case), not systematic
#     over-suppression like the CONTROLLED FIX regression. See
#     docs/00_MASTER_CONTEXT.md for the full writeup.
SYSTEM_PROMPT = (
    "You decide whether a document excerpt establishes an ACTUAL, "
    "company-specific Red Flag in one of a small set of governance/risk "
    "categories — not merely whether the excerpt discusses, defines, or "
    "routinely/compliantly discloses that topic. A topic mention alone is "
    "never sufficient.\n\n"
    "Categories:\n"
    "- auditor_qualification: the auditor's report states an ACTUAL "
    "qualified opinion, adverse opinion, disclaimer of opinion, explicit "
    "qualification/reservation, inability to obtain sufficient audit "
    "evidence, or a material weakness/exception the auditor actually "
    "found and described. Confirm only when the excerpt itself states "
    "such an adverse conclusion about this company.\n"
    "- contingent_liability: Indian annual reports include a standard "
    "accounting-POLICY note (often numbered, e.g. \"Provisions and "
    "Contingent Liabilities\") that defines WHEN a company would "
    "recognise or disclose such an item in general, as a matter of "
    "accounting standard (Ind-AS 37). Nearly every company's report "
    "contains this near-identical paragraph, and it does NOT by itself "
    "mean the company has any such item. Confirm this category ONLY if "
    "the excerpt discloses an ACTUAL, SPECIFIC contingent liability, "
    "claim, dispute, litigation, or guarantee that exists NOW for THIS "
    "company (ideally with an amount, counterparty, or matter named). "
    "Merely defining the accounting treatment is NOT an instance.\n"
    "- related_party_transaction: Indian annual reports include a "
    "standard RPT POLICY/approval-process paragraph (Audit Committee "
    "review, arm's-length/ordinary-course confirmation, Ind AS 24/"
    "Section 188 compliance statements) that nearly every company's "
    "report contains, and it does NOT by itself mean anything adverse "
    "happened. Confirm this category ONLY if the excerpt describes an "
    "ACTUAL adverse or governance-relevant related-party condition — "
    "explicitly NOT at arm's length, outside the ordinary course of "
    "business, an unresolved conflict of interest, or a transaction the "
    "excerpt itself characterizes as unusually large relative to the "
    "company's own stated turnover/net worth. A bare RPT policy "
    "description, a routine Audit Committee approval, a statement that "
    "transactions were at arm's length/ordinary course, or a statement "
    "that there were no materially significant related-party "
    "transactions are NOT instances.\n"
    "- promoter_pledge: the excerpt states an ACTUAL disclosed pledge or "
    "encumbrance of promoter shares (e.g. a stated percentage/quantity "
    "pledged). A passage that only defines what a pledge is, with no "
    "actual disclosed pledge named, is not enough.\n\n"
    "Given the excerpt and its candidate categories, respond with JSON: "
    "{\"category\": one of the candidate category strings, or null if "
    "none apply, \"is_red_flag\": true only when the excerpt itself "
    "establishes an actual adverse/exceptional company-specific "
    "condition as described above, false otherwise (including whenever "
    "category is null), \"summary\": a short, neutral, factual 1-2 "
    "sentence restatement of what the excerpt states, with no "
    "commentary, no forward-looking language, no investment advice — "
    "empty string if category is null}."
)


def build_user_content(fixture: Dict[str, Any]) -> str:
    """Reproduces risk_flag_classifier.py::_call_llm_confirm's user content."""
    candidates = fixture.get("candidates") or []
    return (
        f"Candidate categories: {', '.join(candidates)}\n\n"
        f"Excerpt:\n{fixture.get('chunk_text') or ''}"
    )
