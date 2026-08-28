#!/usr/bin/env python3
"""Generate SYNTHETIC sample fixtures so the harness can be exercised with
no VM, no GPU and no network.

READ THIS BEFORE USING THE OUTPUT FOR ANYTHING
----------------------------------------------
These fixtures are INVENTED. The text is not from a real annual report or
transcript, the "reference" outputs were not produced by production, and no
number in them means anything. Every generated file is stamped
`"synthetic": true` and named `sample_*` so it cannot be confused with a
real export.

Their only job is to prove the pipeline runs end-to-end before a Kaggle
GPU-hour or a production read is spent. Real evaluation requires real
fixtures from scripts/export_fixtures.py.

They are schema v2, so they also serve as the worked example of the
provenance contract every real case must satisfy.
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
    "read_only": True,
    "openai_calls_made": 0,
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
    "facilities and stated that a third site had entered the design phase."
)

_LEGACY_SLICE = (
    "SAMPLE INDUSTRIES LIMITED\nIntegrated Annual Report FY2024-25\n\n"
    "Chairman's Letter. Management described the year as one focused on "
    "consolidating manufacturing capacity across the Company's three "
    "reportable segments. The report stated that the local sourcing "
    "programme was extended to additional component categories, and "
    "described commissioning work at two facilities.\n\n"
    "Management Discussion and Analysis. The principal activities comprise "
    "the manufacture and supply of industrial equipment. Management said "
    "governance practices were reviewed during the year."
)

_ANNUAL_REPORT_CASES = [
    {
        "benchmark_id": "AR_SAMPLECO_SAMPLE-0001",
        "symbol": "SAMPLECO",
        "company_name": "Sample Industries Limited",
        "fiscal_year": "FY2024-25",
        "filing_id": "SAMPLE-0001",
        "filing_date": "2025-07-14",
        "page_count": 312,
        "doc_type": "annual_report",
        "evidence_text": _EVIDENCE,
        "evidence_stats": {
            "evidence_tokens": 190, "evidence_chunks": 3, "total_tagged": 9,
            "total_chunks": 480,
            "by_category": {"management_discussion": 1, "business_overview": 1,
                            "capex_expansion": 1},
            "fallback": False, "budget_max_tokens": 20000,
        },
        "legacy_input_text": _LEGACY_SLICE,
        "legacy_input_stats": {
            "chars": len(_LEGACY_SLICE), "tokens": 120,
            "raw_text_chars_total": len(_LEGACY_SLICE), "truncated": False,
            "max_report_chars": 150000, "exceeds_legacy_token_ceiling": False,
            "input_path_ambiguous": False,
            "input_path_note": "under MAX_REPORT_TOKENS — legacy input is certain.",
        },
        "reference": {
            "summary": (
                "The annual report of Sample Industries Limited for FY2024-25 "
                "outlined management's focus on consolidating manufacturing "
                "capacity across its three reportable segments. Management said "
                "the local sourcing programme was extended to further component "
                "categories during the year."
            ),
            "bullets": [
                "Management described a focus on consolidating manufacturing capacity",
                "The report stated the local sourcing programme was extended",
                "Commissioning work was described at two facilities",
            ],
            "key_takeaway": (
                "The report centred on management's stated consolidation of "
                "manufacturing capacity and local sourcing."
            ),
            "summary_model": "gpt-4o-mini",
            "summarized_at": "2026-08-16T14:02:11.000000",
        },
        "provenance": {
            "reference_set": "LEGACY_REFERENCE",
            "pipeline_version": "legacy_front_slice_pre_evidence_finder",
            "input_type": "dual: legacy_front_slice + evidence_finder",
            "reference_model": "gpt-4o-mini",
            "reference_prompt_version": "annual_report_summarizer@2026-08-16",
            "reference_output_schema": ["summary", "bullets", "key_takeaway"],
            "current_prompt_version": "annual_report_summarizer@8bb3170",
            "limitations": ["SYNTHETIC — not production data."],
        },
    },
]

_CONCALL_CASES = [
    {
        "benchmark_id": "CC_SAMPLECO_CC-0001",
        "symbol": "SAMPLECO",
        "company_name": "Sample Industries Limited",
        "filing_id": "CC-0001",
        "filing_date": "2025-08-02",
        "subject": "EARNINGS_CALL_TRANSCRIPT",
        "doc_kind": "earnings concall transcript",
        "doc_type": "concall_transcript",
        "input_text": (
            "Moderator: Good evening, and welcome to the Q1 FY2026 earnings "
            "conference call of Sample Industries Limited.\n\n"
            "Management: Thank you. During the quarter the Company commissioned "
            "its second line at the western facility. Management said demand "
            "from domestic infrastructure customers remained the largest "
            "contributor to order intake, and noted that input cost pressure "
            "eased relative to the previous quarter. On the analyst call we "
            "described the local sourcing programme as extended to further "
            "component categories."
        ),
        "input_stats": {"chars": 480, "tokens": 110,
                        "transcript_chars_total": 480, "truncated": False,
                        "max_transcript_chars": 120000},
        "reference": {
            "summary": (
                "Management reported that the Company commissioned a second line "
                "at its western facility during the quarter. The presentation "
                "described demand from domestic infrastructure customers as the "
                "largest contributor to order intake, and management noted that "
                "input cost pressure eased relative to the previous quarter. "
                "Management also described the local sourcing programme as "
                "extended to further component categories."
            ),
            "tone_label": "Positive",
            "tone_note": (
                "Management emphasised commissioning progress and easing input "
                "costs in describing the quarter."
            ),
            "summary_model": "gpt-4o-mini",
            "summarized_at": "2026-08-20T09:15:00.000000",
        },
        "provenance": {
            "reference_set": "CURRENT_PIPELINE",
            "pipeline_version": "concall_front_slice",
            "input_type": "raw_transcript_text[:120000] front slice",
            "reference_model": "gpt-4o-mini",
            "reference_prompt_version": "concall_summarizer@8bb3170",
            "reference_output_schema": ["summary", "tone_label", "tone_note"],
            "limitations": ["SYNTHETIC — not production data."],
        },
    },
]

_RED_FLAG_PROVENANCE = {
    "reference_set": "CURRENT_PIPELINE",
    "pipeline_version": "risk_flag_classifier@b9e40c4",
    "input_type": "chromadb chunk text (annual_reports)",
    "reference_model": "gpt-4o-mini",
    "reference_prompt_version": "risk_flag_classifier@b9e40c4",
    "reference_output_schema": ["risk_classified", "risk_flag_type", "risk_flag_summary"],
    "limitations": ["SYNTHETIC — not production data."],
}

_RED_FLAG_CASES = [
    {
        "benchmark_id": "RF_SAMPLECO_AR_SAMPLECO_0102",
        "chunk_id": "AR_SAMPLECO_0102",
        "symbol": "SAMPLECO",
        "company_name": "Sample Industries Limited",
        "doc_type": "annual_report",
        "fiscal_year": "FY2024-25",
        "page_number": 102,
        "chunk_text": (
            "Related party transactions that are repetitive in nature are placed "
            "before the Audit Committee and reviewed by the Statutory Auditors. "
            "The Company did not enter into any material related party "
            "transactions during the year."
        ),
        "candidates": ["related_party_transaction"],
        "case_polarity": "positive",
        "reference": {
            "risk_flag_type": "related_party_transaction",
            "risk_flag_summary": (
                "The excerpt states that repetitive related party transactions are "
                "reviewed by the Statutory Auditors and that no material related "
                "party transactions were entered into during the year."
            ),
        },
        "provenance": dict(_RED_FLAG_PROVENANCE),
    },
    {
        "benchmark_id": "RF_SAMPLECO_AR_SAMPLECO_0210",
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
        "case_polarity": "negative",
        # Production's classifier RAN and confirmed nothing — a true negative,
        # which is a real reference outcome, not missing data.
        "reference": {"risk_flag_type": None, "risk_flag_summary": ""},
        "provenance": dict(_RED_FLAG_PROVENANCE),
    },
]

_ASK_AI_CASES = [
    {
        "benchmark_id": "ASK_SAMPLECO_6a8ae0d241d8e26028edd77d",
        "ask_log_id": "6a8ae0d241d8e26028edd77d",
        "conversation_id": "convo-sample-1",
        "symbol": "SAMPLECO",
        "mode": "symbol",
        "question": "What did management say about manufacturing strategy?",
        "causal_backstop": True,
        "reconstruction_status": "PACKET_RECONSTRUCTION_PARTIAL",
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
            "document_chunks": [],
            "education_content": [],
        },
        "history": None,
        "reference": {
            "answer": (
                "Management described the year as one focused on **consolidating "
                "manufacturing capacity**, according to the annual report excerpt "
                "in the fact packet."
            ),
            "refused": False,
            "model": "gpt-4o-mini",
            "sources_used": ["document_chunks", "measured_signals"],
            "source_citations": [{"type": "annual_report", "label": "FY2024-25 · p8"}],
            "weight": 2,
        },
        "provenance": {
            "reference_set": "CURRENT_PIPELINE",
            "pipeline_version": "ask@8bb3170",
            "input_type": "REBUILT fact_packet (NOT the historical packet)",
            "reference_model": "gpt-4o-mini",
            "reference_prompt_version": "ask@454a07a",
            "reference_output_schema": ["answer", "refused", "refusal_reason"],
            "document_chunks_omitted": True,
            "limitations": [
                "SYNTHETIC — not production data.",
                "PACKET_RECONSTRUCTION_PARTIAL — the packet is rebuilt, never the "
                "historical input.",
            ],
        },
    },
]

BUILDERS = {
    "annual_report_summary": _ANNUAL_REPORT_CASES,
    "concall_summary": _CONCALL_CASES,
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
