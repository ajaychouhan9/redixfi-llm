#!/usr/bin/env python3
"""Generate SYNTHETIC sample fixtures so the harness can be exercised with
no VM, no GPU and no network.

READ THIS BEFORE USING THE OUTPUT FOR ANYTHING
----------------------------------------------
These fixtures are INVENTED. The text is not from a real annual report, the
"reference" outputs were not produced by production, and no number in them
means anything. Every generated file is stamped `"synthetic": true` in its
source block, and `--out` defaults to a filename containing `sample_` so it
cannot be confused with a real export.

Their only job is to prove the pipeline runs end-to-end before a single
Kaggle GPU-hour or production read is spent. Real evaluation requires real
fixtures from scripts/export_fixtures.py.
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.evaluation.fixtures import build_document, save  # noqa: E402

_SYNTHETIC_SOURCE = {
    "synthetic": True,
    "warning": (
        "SYNTHETIC SAMPLE — invented text and invented reference outputs. "
        "Not from RedixFi production. Harness validation only; never cite "
        "results from this fixture as a model comparison."
    ),
    "exported_by": "LLM/scripts/make_sample_fixtures.py",
}

_EVIDENCE = (
    "[Evidence chunk 12, page ~8]\n"
    "Management Discussion and Analysis. The Company operates across three "
    "reportable segments and management described the year as one focused on "
    "consolidating manufacturing capacity. The report stated that the local "
    "sourcing programme was extended to additional component categories.\n\n"
    "[Evidence chunk 41, page ~26]\n"
    "Business Overview. The principal activities of the Company comprise the "
    "manufacture and supply of industrial equipment. Management said the "
    "domestic order book remained the primary contributor to segment "
    "activity during the period under review.\n\n"
    "[Evidence chunk 88, page ~54]\n"
    "Capex and Expansion. The report described commissioning work at two "
    "facilities and stated that a third site had entered the design phase. "
    "Management set a goal of raising the share of locally manufactured "
    "components across the product range."
)

_ANNUAL_REPORT_CASES = [
    {
        "fixture_id": "SAMPLECO:FY2024-25",
        "symbol": "SAMPLECO",
        "company_name": "Sample Industries Limited",
        "fiscal_year": "FY2024-25",
        "filing_date": "2025-07-14",
        "page_count": 312,
        "filing_id": "SAMPLE-0001",
        "evidence_text": _EVIDENCE,
        "evidence_stats": {
            "evidence_tokens": 210, "evidence_chunks": 3, "total_tagged": 9,
            "total_chunks": 480,
            "by_category": {"management_discussion": 1, "business_overview": 1,
                            "capex_expansion": 1},
            "fallback": False, "budget_max_tokens": 20000,
        },
        "reference": {
            "executive_summary": (
                "The annual report of Sample Industries Limited for FY2024-25 "
                "outlined management's focus on consolidating manufacturing "
                "capacity across its three reportable segments. Management said "
                "the local sourcing programme was extended to further component "
                "categories during the year. The report also described "
                "commissioning work at two facilities and a third site in design."
            ),
            "key_points": [
                "Management described a focus on consolidating manufacturing capacity",
                "The report stated the local sourcing programme was extended",
                "Commissioning work was described at two facilities",
                "Management set a goal of raising locally manufactured component share",
            ],
            "important_risks": [],
            "key_takeaway": (
                "The report centred on management's stated consolidation of "
                "manufacturing capacity and local sourcing."
            ),
            "summary_model": "gpt-4o-mini",
            "summarized_at": "2026-08-24T21:41:00+00:00",
        },
    },
]

_RED_FLAG_CASES = [
    {
        "fixture_id": "AR_SAMPLECO_0102",
        "chunk_id": "AR_SAMPLECO_0102",
        "symbol": "SAMPLECO",
        "company_name": "Sample Industries Limited",
        "doc_type": "annual_report",
        "fiscal_year": "FY2024-25",
        "page_number": 102,
        "source_pdf_url": "https://example.invalid/sample.pdf",
        "chunk_text": (
            "Related party transactions that are repetitive in nature are placed "
            "before the Audit Committee and reviewed by the Statutory Auditors. "
            "The Company did not enter into any material related party "
            "transactions during the year. Related party disclosures have been "
            "made in accordance with Ind AS 24."
        ),
        "candidates": ["related_party_transaction"],
        "production_risk_classified": True,
        "reference": {
            "risk_flag_type": "related_party_transaction",
            "risk_flag_summary": (
                "The excerpt states that repetitive related party transactions are "
                "reviewed by the Statutory Auditors and that no material related "
                "party transactions were entered into during the year."
            ),
        },
    },
    {
        "fixture_id": "AR_SAMPLECO_0210",
        "chunk_id": "AR_SAMPLECO_0210",
        "symbol": "SAMPLECO",
        "doc_type": "annual_report",
        "fiscal_year": "FY2024-25",
        "page_number": 210,
        "chunk_text": (
            "The Nomination and Remuneration Committee reviewed the composition "
            "of the Board. A guarantee given by a subsidiary in a prior period "
            "was referenced in the notes for completeness of disclosure."
        ),
        "candidates": ["contingent_liability"],
        "production_risk_classified": True,
        # Production ran the classifier and confirmed NOTHING — a true negative,
        # which is a real reference outcome, not missing data.
        "reference": {"risk_flag_type": None, "risk_flag_summary": ""},
    },
]

_ASK_AI_CASES = [
    {
        "fixture_id": "SAMPLECO:sample-question-1",
        "symbol": "SAMPLECO",
        "mode": "symbol",
        "question": "What did management say about manufacturing strategy?",
        "causal_backstop": True,
        "packet_degraded": False,
        "fact_packet": {
            "symbol": "SAMPLECO",
            "measured_signals": {
                "date": "2026-08-27", "composite_score": 58, "delta_1d": -1.2,
                "delta_5d": 3.4, "sector": "NIFTY CAPITAL MARKETS",
                "signal_states": [], "component_changes": [],
                "signals": {"trend_10d_pct": 2.1, "volume_ratio_5d": 0.9,
                            "delivery_pct": 41.2, "rsi_14": 52.0},
            },
            "fundamentals_derived": None,
            "signal_change_log": [],
            "news_events": [],
            "change_explanation": {"cause_available": False,
                                   "note": "No matched news event for this change."},
            "investor_calls": [],
            "document_chunks": [{
                "doc_type": "annual_report",
                "symbol": "SAMPLECO",
                "fiscal_year": "FY2024-25",
                "page_number": 8,
                "text": (
                    "The following annual report excerpts provide qualitative "
                    "strategic context. Do not treat any specific financial "
                    "figures in these excerpts as authoritative — they may be "
                    "incorrectly labeled due to PDF table extraction "
                    "limitations. For precise financial data, refer to the "
                    "structured fundamentals data above.\n\nManagement "
                    "described the year as one focused on consolidating "
                    "manufacturing capacity, and stated that the local "
                    "sourcing programme was extended to additional component "
                    "categories."
                ),
            }],
            "education_content": [],
        },
        "history": None,
        "reference": {
            "answer": (
                "Management described the year as one focused on **consolidating "
                "manufacturing capacity**, according to the annual report excerpt "
                "in the fact packet. The report also stated that the local "
                "sourcing programme was extended to additional component "
                "categories."
            ),
            "refused": False,
            "model": "gpt-4o-mini",
            "sources_used": ["document_chunks", "measured_signals"],
            "source_citations": [
                {"type": "annual_report", "label": "FY2024-25 · p8"}
            ],
            "weight": 2,
        },
    },
]

BUILDERS = {
    "annual_report_summary": _ANNUAL_REPORT_CASES,
    "red_flag": _RED_FLAG_CASES,
    "ask_ai": _ASK_AI_CASES,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic sample fixtures")
    parser.add_argument("--out-dir", default="fixtures")
    parser.add_argument("--task", choices=sorted(BUILDERS), default=None)
    args = parser.parse_args()

    tasks = [args.task] if args.task else sorted(BUILDERS)
    now = datetime.now(timezone.utc).isoformat()

    for task in tasks:
        doc = build_document(task, BUILDERS[task], dict(_SYNTHETIC_SOURCE), now)
        path = os.path.join(args.out_dir, f"sample_{task}.json")
        save(doc, path)
        print(f"[WROTE] {path}  ({len(doc['cases'])} synthetic cases)")

    print("\nSYNTHETIC DATA — harness validation only. Real evaluation needs "
          "fixtures from scripts/export_fixtures.py run on the RedixFi VM.")


if __name__ == "__main__":
    main()
