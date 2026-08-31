"""RedixFi compliance validators — VENDORED COPY, do not edit to "fix" a
failing evaluation.

PROVENANCE
----------
Original RedixFi files / sections:
  * data-pipeline/annual_report_summarizer.py
      - FORBIDDEN_WORDS_RE, FORWARD_TENSE_RE, _BUY_SELL_RE,
        _BUY_SELL_SAFE_RE, FINANCIAL_FIGURE_RE, _violation()
      - source commit b9e40c4 (2026-08-24)
  * api/app/core/document_retrieval.py
      - _CALL_MEETING_SAFE_RE, _TRADING_CONTEXT_NEAR_CALL_RE,
        _chunk_fails_compliance()
      - source commit ed253bb (2026-08-27)
  * data-pipeline/risk_flag_classifier.py
      - _violation() (risk-summary variant; identical pattern set to the
        summarizer's minus FINANCIAL_FIGURE_RE)
      - source commit b9e40c4 (2026-08-24)
RedixFi repo HEAD at copy time: 8bb3170
Date copied: 2026-08-28

WHY VENDORED
------------
This project must not import RedixFi code at runtime (founder decision,
2026-08-28). RedixFi itself already duplicates this regex set across ~6
files by an explicit "duplicate and keep in sync manually" convention
documented in core/ask.py's own module docstring; this file is one more
instance of that convention, in a separate repository.

WHY IT MATTERS FOR EVALUATION
-----------------------------
These validators are the objective, non-LLM-judge half of the comparison.
RedixFi's pre-RA compliance rules are enforced in code, so "did the
candidate model's output pass the same validator the production output had
to pass" is a real pass/fail signal that needs no human and no LLM judge.
Both sides of every comparison are run through this module.

See app/prompts/PROVENANCE.md for the full register and the re-verification
command.
"""
from __future__ import annotations

import re
from typing import Optional

# --- shared pattern set ----------------------------------------------------
FORBIDDEN_WORDS_RE = re.compile(
    r"\b(calls?|picks?|tips?|predictions?|predict(?:s|ed|ing)?|target\s*price|"
    r"stop[\s-]?loss|accuracy)\b", re.IGNORECASE,
)
BUY_SELL_RE = re.compile(r"\b(buy|sell)\b", re.IGNORECASE)
BUY_SELL_SAFE_RE = re.compile(r"\bnet\s+(buy|sell)\b", re.IGNORECASE)
FORWARD_TENSE_RE = re.compile(
    r"\b(expect\w*|likely|will|outlook|target\w*|forecast\w*|going to|"
    r"should\s+rise|should\s+fall|recommend\w*)\b", re.IGNORECASE,
)

# Controlled fix (2026-08-31): reporting management's OWN stated expectation,
# target, forecast, or outlook is legitimate source-grounded guidance — the
# validator must not reject it. Asserting a future event as fact ("will",
# "likely", "going to") remains forbidden even when the company is the
# subject, because that is a future claim, not reported guidance.
_ATTRIBUTED_GUIDANCE_RE = re.compile(
    r"\b(management|company|report|document|presentation|board|directors?|chairman|ceo|cfo)\b\s+"
    r"(said|stated|reported|guided|indicated|outlines?|details?|describes?|presents?|notes?|highlights?|announced|"
    r"expects?|targets?|plans?|forecasts?|intends?|committed|outlook|guidance)"
    r"|\b(management|company|report|document|presentation|board)\s+(guidance|outlook|target)"
    r"|\b(stated|said|reported|guided|indicated|outlined|detailed|described|presented|noted|highlighted|announced)\s+that",
    re.IGNORECASE,
)
_ALLOWED_ATTRIBUTED_FORWARD = ("expect", "target", "forecast", "outlook")

# Looser attribution check: a reporting subject AND a non-forward reporting
# verb anywhere earlier in the same sentence (e.g. "Management noted ... but
# expects ..." / "FY27 guidance indicates ..."). The verb list deliberately
# excludes expect/target/forecast/outlook so a bare future word cannot
# attribute itself.
_ATTRIBUTION_SUBJECT_RE = re.compile(
    r"\b(management|company|report|document|presentation|board|directors?|"
    r"chairman|ceo|cfo|guidance|management team)\b", re.IGNORECASE,
)
_ATTRIBUTION_VERB_RE = re.compile(
    r"\b(said|stated|noted|notes?|mentioned|indicat\w*|guided|emphasized|highlighted|"
    r"reiterated|maintained|outlined|detailed|described|presented|announced|"
    r"reported|commented|added|confirmed|guided toward|set)\b", re.IGNORECASE,
)


def _is_attributed_guidance(text: str, match: "re.Match") -> bool:
    """True when a forward word is explicitly attributed to management/source
    as reported guidance (e.g. 'Management stated that it expects ...')."""
    word = match.group(0).lower()
    if not any(word.startswith(prefix) for prefix in _ALLOWED_ATTRIBUTED_FORWARD):
        return False
    sentence_start = text.rfind(".", 0, match.start()) + 1
    sentence_end = text.find(".", match.end())
    sentence_end = len(text) if sentence_end == -1 else sentence_end + 1
    window = text[sentence_start:sentence_end]
    pre = window[:max(0, match.end() - sentence_start + 80)]
    if _ATTRIBUTED_GUIDANCE_RE.search(pre):
        return True
    return bool(_ATTRIBUTION_SUBJECT_RE.search(pre)
                and _ATTRIBUTION_VERB_RE.search(pre))


def _is_attributed_figure(text: str, match: "re.Match") -> bool:
    """Annual Report controlled fix (2026-08-31): a financial figure is
    allowed when it is explicitly attributed to management/source (e.g.
    'management's stated target to expand ... to 1 billion tonnes'). Bare
    figures stated as fact ('revenue was ₹43,541 crore') still fail."""
    sentence_start = text.rfind(".", 0, match.start()) + 1
    sentence_end = text.find(".", match.end())
    sentence_end = len(text) if sentence_end == -1 else sentence_end + 1
    window = text[sentence_start:sentence_end]
    pre = window[:max(0, match.end() - sentence_start + 80)]
    if _ATTRIBUTED_GUIDANCE_RE.search(pre):
        return True
    return bool(_ATTRIBUTION_SUBJECT_RE.search(pre)
                and _ATTRIBUTION_VERB_RE.search(pre))


def _forward_tense_reason(text: str) -> Optional[str]:
    """Returns the first UN-ATTRIBUTED forward-tense violation, or None."""
    for m in FORWARD_TENSE_RE.finditer(text):
        if _is_attributed_guidance(text, m):
            continue
        return f"forward-tense word '{m.group(0)}'"
    return None

# Annual-report-specific. RedixFi forbids stating any financial figure as
# fact in an annual report summary, because PDF table extraction has a
# CONFIRMED real failure mode (two different LLMs mislabeled the same figure
# as "revenue" vs "order backlog" from the same chunk — 2026-08-12 eval,
# finding #4). Only the summarizer applies this; the risk classifier and Ask
# AI do not.
FINANCIAL_FIGURE_RE = re.compile(
    r"(?:₹|rs\.?|inr)\s*[\d,]+(?:\.\d+)?"
    r"|\b[\d,]+(?:\.\d+)?\s*(?:crore|lakh|million|billion|bn|mn)\b"
    r"|\b\d+(?:\.\d+)?\s*%",
    re.IGNORECASE,
)

# The "call" carve-out. A concall/earnings call is a meeting, not a trading
# call — but "last call price" / "call option" must NOT slip through, hence
# the wider trading-context window check.
CALL_MEETING_SAFE_RE = re.compile(
    r"\b(?:conference|earnings|analyst|investor|quarterly|q\d)\s*[\s-]?calls?\b"
    r"|\b(?P<temporal>last|this|the|recent|previous|prior|latest)\s+calls?\b",
    re.IGNORECASE,
)
TRADING_CONTEXT_NEAR_CALL_RE = re.compile(
    r"\b(buy|sell|option|options|price|premium|strike|put|puts)\b", re.IGNORECASE,
)


def violation(text: str, *, check_financial_figures: bool = False) -> Optional[str]:
    """Mirrors risk_flag_classifier.py::_violation ONLY.

    IMPORTANT — this variant has NO "call"-means-a-meeting carve-out,
    because risk_flag_classifier.py deliberately has none: it uses a plain
    FORBIDDEN_WORDS_RE.search(). Verified against the RedixFi source.

    The two SUMMARIZERS are different — both annual_report_summarizer.py
    and concall_summarizer.py DO carry the carve-out. Use
    summarizer_violation() for those, never this. Getting it wrong rejects
    a legitimate "earnings conference call" as forbidden language, which is
    exactly what happened before this split existed: 6 of 20 real
    production concall references were flagged as non-compliant by this
    function.

    Returns a human-readable reason string when `text` must be REJECTED,
    or None when it passes. Order matters and is preserved from the
    original: forward-tense first, then forbidden words, then buy/sell with
    its "net buy/sell" carve-out, then (optionally) financial figures.
    """
    if not text:
        return "empty text"
    reason = _forward_tense_reason(text)
    if reason:
        return reason
    m = FORBIDDEN_WORDS_RE.search(text)
    if m:
        return f"forbidden word '{m.group(0)}'"
    m = BUY_SELL_RE.search(text)
    if m:
        window = text[max(0, m.start() - 4):m.end()]
        if not BUY_SELL_SAFE_RE.search(window):
            return f"forbidden word '{m.group(0)}'"
    if check_financial_figures:
        m = FINANCIAL_FIGURE_RE.search(text)
        if m:
            return f"financial figure stated as fact '{m.group(0).strip()}'"
    return None


def summarizer_violation(
    text: str, *, check_financial_figures: bool = False,
) -> Optional[str]:
    """Mirrors annual_report_summarizer.py::_violation and
    concall_summarizer.py::_violation.

    PROVENANCE: both are byte-identical to chunk_fails_compliance's
    forbidden-word handling (they carry the same "call"-means-a-meeting
    carve-out), and the annual report one appends FINANCIAL_FIGURE_RE.
    Source commits b9e40c4 (AR) and 8bb3170 (concall), copied 2026-08-28.

      annual_report_summarizer -> check_financial_figures=True
      concall_summarizer       -> check_financial_figures=False

    The carve-out is not cosmetic: a concall summary that says "the
    earnings conference call" is correct and expected output, and must not
    be rejected.
    """
    reason = chunk_fails_compliance(text)
    if reason:
        return reason
    if check_financial_figures:
        for m in FINANCIAL_FIGURE_RE.finditer(text):
            if not _is_attributed_figure(text, m):
                return f"financial figure stated as fact '{m.group(0).strip()}'"
    return None


def chunk_fails_compliance(text: str) -> Optional[str]:
    """Mirrors core/document_retrieval.py::_chunk_fails_compliance — the
    RETRIEVED-CHUNK variant, which differs from violation() above by
    carrying the "call"-means-a-meeting carve-out. Applied to evidence
    before it reaches the model, not to generated output.

    Kept as a separate function rather than a flag on violation() because
    that is how RedixFi splits them, and collapsing the two would make a
    future divergence harder to see.
    """
    if not text:
        return "empty text"
    reason = _forward_tense_reason(text)
    if reason:
        return reason
    for m in FORBIDDEN_WORDS_RE.finditer(text):
        word = m.group(0).lower()
        if word in ("call", "calls"):
            window = text[max(0, m.start() - 15):m.end()]
            safe = CALL_MEETING_SAFE_RE.search(window)
            if safe and not (
                safe.group("temporal")
                and TRADING_CONTEXT_NEAR_CALL_RE.search(
                    text[max(0, m.start() - 20):min(len(text), m.end() + 15)]
                )
            ):
                continue
        return f"forbidden word '{m.group(0)}'"
    m = BUY_SELL_RE.search(text)
    if m:
        window = text[max(0, m.start() - 4):m.end()]
        if not BUY_SELL_SAFE_RE.search(window):
            return f"forbidden word '{m.group(0)}'"
    return None


# ---------------------------------------------------------------------------
# ASK AI answer validator.
#
# PROVENANCE: api/app/core/ask.py::_violation + CAUSAL_ATTRIBUTION_RE,
# source commit 454a07a (2026-08-27), copied 2026-08-28.
#
# Differs from violation() above in two ways, both deliberate and both
# preserved: it carries the "call"-means-a-meeting carve-out (so it is built
# on chunk_fails_compliance, not violation), and it adds a CAUSAL BACKSTOP.
# The backstop fires only when the fact packet carried no real cause — it
# stops a model inventing "because of profit booking" when
# change_explanation.cause_available was false. It does NOT apply financial-
# figure checking; that belongs only to the annual report summarizer.
# ---------------------------------------------------------------------------
CAUSAL_ATTRIBUTION_RE = re.compile(
    r"\b(because|due to|owing to|driven by|caused by|attribut\w*|"
    r"on account of|as a result of|thanks to|the reason (is|was))\b",
    re.IGNORECASE,
)


def ask_answer_violation(answer: str, causal_backstop: bool = False) -> Optional[str]:
    """Mirrors core/ask.py::_violation(answer, causal_backstop)."""
    reason = chunk_fails_compliance(answer)
    if reason:
        return reason
    if causal_backstop:
        m = CAUSAL_ATTRIBUTION_RE.search(answer)
        if m:
            return (
                f"fabricated causal attribution '{m.group(0)}' "
                "with no matched news event"
            )
    return None
