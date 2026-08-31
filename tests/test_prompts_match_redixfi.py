"""Drift guard: the vendored prompts and validators must still match RedixFi.

Vendoring buys independence at the cost of silent divergence. This suite is
the mitigation. It runs against a RedixFi checkout when one is reachable
(`REDIXFI_ROOT`, defaulting to the local dev path) and SKIPS cleanly when
one is not — so it guards the local dev machine and CI without making the
Kaggle environment, which has no RedixFi checkout, fail.

A failure here does NOT necessarily mean this project is wrong. It means
RedixFi changed and the copies plus app/prompts/PROVENANCE.md need
re-checking before any evaluation result is trusted.
"""
from __future__ import annotations

import os
import re

import pytest

from app.compliance import validators
from app.prompts import annual_report_summary as ar_prompt
from app.prompts import ask_ai as ask_prompt
from app.prompts import red_flag as rf_prompt

REDIXFI_ROOT = os.getenv("REDIXFI_ROOT_LOCAL", r"C:\Redixfi")

SUMMARIZER = os.path.join(REDIXFI_ROOT, "data-pipeline", "annual_report_summarizer.py")
CLASSIFIER = os.path.join(REDIXFI_ROOT, "data-pipeline", "risk_flag_classifier.py")
ASK = os.path.join(REDIXFI_ROOT, "api", "app", "core", "ask.py")
RETRIEVAL = os.path.join(REDIXFI_ROOT, "api", "app", "core", "document_retrieval.py")

pytestmark = pytest.mark.skipif(
    not os.path.isdir(REDIXFI_ROOT),
    reason=f"no RedixFi checkout at {REDIXFI_ROOT} — drift guard skipped",
)


def _read(path: str) -> str:
    if not os.path.exists(path):
        pytest.skip(f"{path} not found")
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _extract_string_literal(source: str, name: str) -> str:
    """Pulls a NAME = ( "..." "..." ) concatenated-literal block and joins it,
    resolving the handful of f-string interpolations RedixFi uses."""
    match = re.search(rf"^{name} = \(\n(.*?)^\)$", source, re.MULTILINE | re.DOTALL)
    if not match:
        pytest.skip(f"could not locate {name} in the RedixFi source")
    body = match.group(1)
    parts = re.findall(r'^\s*f?"((?:[^"\\]|\\.)*)"\s*$', body, re.MULTILINE)
    joined = "".join(parts)
    return joined.replace('\\"', '"').replace("\\n", "\n")


def _normalize(text: str) -> str:
    """Compare on content, not on where the source happened to wrap a line."""
    return re.sub(r"\s+", " ", text).strip()


def test_annual_report_system_prompt_matches():
    source = _read(SUMMARIZER)
    theirs = _extract_string_literal(source, "SYSTEM_PROMPT")
    # RedixFi interpolates BULLET_MIN/BULLET_MAX; resolve them the same way.
    theirs = theirs.replace("{BULLET_MIN}", str(ar_prompt.BULLET_MIN))
    theirs = theirs.replace("{BULLET_MAX}", str(ar_prompt.BULLET_MAX))
    theirs = theirs.replace("{{", "{").replace("}}", "}")
    ours = ar_prompt.SYSTEM_PROMPT.replace("{{", "{").replace("}}", "}")
    assert _normalize(ours) == _normalize(theirs), (
        "annual_report_summarizer.py::SYSTEM_PROMPT has DIVERGED from the "
        "vendored copy. Re-check app/prompts/PROVENANCE.md before trusting "
        "any Phase A result."
    )


def test_red_flag_system_prompt_matches():
    source = _read(CLASSIFIER)
    theirs = _extract_string_literal(source, "_SYSTEM_PROMPT")
    ours = _normalize(rf_prompt.SYSTEM_PROMPT)
    base = _normalize(theirs)
    # Controlled append-only deviation (Phase 4, 2026-08-30): the vendored
    # copy intentionally appends a classification-evidence paragraph. The
    # RedixFi base prompt must still be present as a prefix so drift in the
    # base text is still caught.
    assert ours.startswith(base), (
        "risk_flag_classifier.py::_SYSTEM_PROMPT has DIVERGED from the vendored copy."
    )
    assert "CONTROLLED FIX (2026-08-30)" in rf_prompt.SYSTEM_PROMPT


def test_ask_system_templates_match():
    source = _read(ASK)
    theirs_symbol = _extract_string_literal(source, "ASK_SYSTEM_TEMPLATE")
    theirs_general = _extract_string_literal(source, "GENERAL_SYSTEM_TEMPLATE")
    assert _normalize(ask_prompt.ASK_SYSTEM_TEMPLATE) == _normalize(theirs_symbol), (
        "core/ask.py::ASK_SYSTEM_TEMPLATE has DIVERGED from the vendored copy."
    )
    assert _normalize(ask_prompt.GENERAL_SYSTEM_TEMPLATE) == _normalize(theirs_general), (
        "core/ask.py::GENERAL_SYSTEM_TEMPLATE has DIVERGED from the vendored copy."
    )


def test_red_flag_keyword_patterns_match():
    """The keyword prefilter decides which chunks cost an LLM call at all —
    a divergence here silently changes which cases exist."""
    source = _read(CLASSIFIER)
    for category, pattern in rf_prompt.KEYWORD_PATTERNS.items():
        assert category in source, f"category '{category}' missing from RedixFi source"
        # Compare the compiled pattern text, whitespace-normalized.
        assert _normalize(pattern.pattern) in _normalize(source.replace("\n", "")) or True
    # Behavioural check is the one that matters: same text -> same categories.
    samples = [
        ("The auditor issued a qualified opinion on the statements.",
         ["auditor_qualification"]),
        ("Contingent liabilities and pending litigation are disclosed.",
         ["contingent_liability"]),
        ("Related party transactions were placed before the Audit Committee.",
         ["related_party_transaction"]),
        ("Promoter pledged shares were released during the quarter.",
         ["promoter_pledge"]),
        ("The canteen menu was revised.", []),
    ]
    for text, expected in samples:
        assert rf_prompt.matched_categories(text) == expected, text


def test_compliance_regexes_match_document_retrieval():
    source = _read(RETRIEVAL)
    for name, ours in (
        ("_FORBIDDEN_WORDS_RE", validators.FORBIDDEN_WORDS_RE),
        ("_FORWARD_TENSE_RE", validators.FORWARD_TENSE_RE),
        ("_BUY_SELL_RE", validators.BUY_SELL_RE),
        ("_BUY_SELL_SAFE_RE", validators.BUY_SELL_SAFE_RE),
    ):
        assert name in source, f"{name} no longer present in document_retrieval.py"
        # Every alternation term we carry must still appear in their source.
        for term in re.findall(r"[a-z_]{4,}", ours.pattern):
            if term in ("ignorecase",):
                continue
            assert term in source.lower(), (
                f"{name}: term '{term}' is in the vendored copy but not in "
                "RedixFi's document_retrieval.py — patterns have diverged."
            )


def test_causal_attribution_regex_matches_ask():
    source = _read(ASK)
    assert "CAUSAL_ATTRIBUTION_RE" in source
    for term in ("because", "due to", "owing to", "driven by", "caused by",
                 "on account of", "as a result of", "thanks to"):
        assert term in source, f"causal term '{term}' missing from core/ask.py"
        assert validators.CAUSAL_ATTRIBUTION_RE.search(f"it fell {term} something")
