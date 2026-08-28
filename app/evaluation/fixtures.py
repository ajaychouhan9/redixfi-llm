"""Fixture format — the contract between the RedixFi VM and this project.

A fixture file is a JSON document:

    {
      "schema_version": 2,
      "task": "<task name>",
      "exported_at": "2026-08-28T…Z",
      "source": { … provenance of the export … },
      "cases": [ { … one benchmark case … }, … ]
    }

Each case carries BOTH the input and the preserved production reference
output, so a comparison never depends on production being reachable again.
Fixtures are produced ONLY by scripts/export_fixtures.py running on the
RedixFi VM (read-only). Nothing in this project writes to production.

WHY THE REFERENCE TRAVELS WITH THE INPUT
----------------------------------------
RedixFi's OpenAI account had no credits as of 2026-08-28, so reference
outputs cannot be regenerated on demand. The 72 stored annual-report
summaries, the 4,157 concall summaries and the existing ask_conversations
answers are what exist. Losing them would mean losing the baseline.

SCHEMA VERSION 2 — every case is self-describing
------------------------------------------------
v1 carried input + reference and little else. v2 requires PROVENANCE on
every case, because this benchmark deliberately mixes generations of the
same pipeline (notably the legacy pre-Evidence-Finder annual-report
references) and a case that does not say which pipeline produced it can be
silently misread as current. `provenance` is mandatory and must name the
pipeline_version, model, prompt_version and input_type.

PER-TASK CASE FIELDS
--------------------
annual_report_summary        (DUAL-INPUT — carries both eras)
  ids       : benchmark_id "AR_<symbol>_<filing_id>", symbol, fiscal_year,
              filing_id, company_name, filing_date, page_count
  inputs    : legacy_input_text  (raw_text[:150_000] — what produced the
                                  stored reference)
              evidence_text      (current Evidence Finder output)
              evidence_stats, legacy_input_stats
  reference : LEGACY_REFERENCE — summary / bullets / key_takeaway /
              summary_model / summarized_at
  provenance: reference_pipeline vs current_pipeline, both prompt versions

concall_summary              (PRIMARY summarization benchmark)
  ids       : benchmark_id "CC_<symbol>_<filing_id>", symbol, filing_date
  inputs    : input_text (raw_transcript_text[:120_000]), doc_kind
  reference : summary / tone_label / tone_note / summary_model

red_flag
  ids       : benchmark_id "RF_<symbol>_<chunk_id>", symbol, doc_type,
              fiscal_year, chunk_id
  inputs    : chunk_text, candidates (RedixFi's own matched_categories())
  reference : risk_flag_type (None for a true negative), risk_flag_summary
  extra     : case_polarity "positive" | "negative"

ask_ai
  ids       : benchmark_id "ASK_<symbol>_<ask_log_id>", symbol, question
  inputs    : fact_packet (REBUILT), history, causal_backstop
  reference : answer / refused / model / sources_used / source_citations
  extra     : reconstruction_status — ALWAYS "PACKET_RECONSTRUCTION_PARTIAL"
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

SCHEMA_VERSION = 2

TASKS = (
    "annual_report_summary",
    "concall_summary",
    "red_flag",
    "ask_ai",
)

# Tasks the fixture can be REPLAYED as, beyond its own name. The annual
# report fixture is dual-input, so it feeds two runners.
REPLAYABLE_AS = {
    "annual_report_summary": ("annual_report_summary", "annual_report_summary_legacy"),
    "concall_summary": ("concall_summary",),
    "red_flag": ("red_flag",),
    "ask_ai": ("ask_ai",),
}

REQUIRED_INPUT_FIELDS: Dict[str, tuple] = {
    "annual_report_summary": ("benchmark_id", "symbol", "evidence_text"),
    "concall_summary": ("benchmark_id", "symbol", "input_text"),
    "red_flag": ("benchmark_id", "chunk_text", "candidates"),
    "ask_ai": ("benchmark_id", "question", "fact_packet"),
}

REQUIRED_PROVENANCE_FIELDS = ("pipeline_version", "input_type")

BENCHMARK_ID_PREFIX = {
    "annual_report_summary": "AR_",
    "concall_summary": "CC_",
    "red_flag": "RF_",
    "ask_ai": "ASK_",
}


@dataclass
class FixtureSet:
    task: str
    cases: List[Dict[str, Any]]
    source: Dict[str, Any]
    exported_at: str
    schema_version: int = SCHEMA_VERSION
    path: Optional[str] = None

    def __len__(self) -> int:
        return len(self.cases)

    def __iter__(self) -> Iterable[Dict[str, Any]]:
        return iter(self.cases)

    def with_reference(self) -> List[Dict[str, Any]]:
        """Cases carrying a production reference output. A case without one
        is still a valid generation target, but cannot be part of a
        side-by-side comparison — saying so beats comparing against
        nothing."""
        return [c for c in self.cases if c.get("reference")]

    def replayable_as(self) -> tuple:
        return REPLAYABLE_AS.get(self.task, (self.task,))


def build_document(
    task: str, cases: List[Dict[str, Any]], source: Dict[str, Any], exported_at: str,
) -> Dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "task": task,
        "exported_at": exported_at,
        "source": source,
        "cases": cases,
    }


def validate_document(doc: Dict[str, Any]) -> List[str]:
    """Returns a list of problems; empty means valid. Never raises, so a
    partially-broken export can still be inspected rather than just
    failing."""
    problems: List[str] = []

    version = doc.get("schema_version")
    if version != SCHEMA_VERSION:
        problems.append(f"schema_version {version!r} != expected {SCHEMA_VERSION}")

    task = doc.get("task")
    if task not in TASKS:
        problems.append(f"unknown task {task!r}; expected one of {TASKS}")
        return problems

    cases = doc.get("cases")
    if not isinstance(cases, list):
        problems.append("'cases' must be a list")
        return problems
    if not cases:
        problems.append("'cases' is empty")

    prefix = BENCHMARK_ID_PREFIX[task]
    seen_ids = set()

    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            problems.append(f"case[{index}] is not an object")
            continue

        for field in REQUIRED_INPUT_FIELDS[task]:
            if field not in case or case[field] in (None, ""):
                problems.append(f"case[{index}] missing required field '{field}'")

        bid = case.get("benchmark_id")
        if bid:
            if not str(bid).startswith(prefix):
                problems.append(
                    f"case[{index}] benchmark_id {bid!r} does not start with '{prefix}'")
            if bid in seen_ids:
                problems.append(f"case[{index}] duplicate benchmark_id {bid!r}")
            seen_ids.add(bid)

        prov = case.get("provenance")
        if not isinstance(prov, dict):
            problems.append(f"case[{index}] missing 'provenance' object")
        else:
            for field in REQUIRED_PROVENANCE_FIELDS:
                if not prov.get(field):
                    problems.append(f"case[{index}] provenance missing '{field}'")

        # --- per-task invariants ------------------------------------------
        if task == "red_flag":
            if isinstance(case.get("candidates"), list) and not case["candidates"]:
                problems.append(
                    f"case[{index}] has an empty candidate list (no keyword match, so "
                    "no LLM call would ever be made — exclude it from the fixture)")
            if case.get("case_polarity") not in ("positive", "negative"):
                problems.append(
                    f"case[{index}] case_polarity must be 'positive' or 'negative'")
            ref = case.get("reference")
            if not isinstance(ref, dict) or "risk_flag_type" not in ref:
                problems.append(
                    f"case[{index}] red_flag reference must carry 'risk_flag_type' "
                    "(None is valid and means a confirmed true negative)")

        if task == "ask_ai":
            if case.get("reconstruction_status") != "PACKET_RECONSTRUCTION_PARTIAL":
                problems.append(
                    f"case[{index}] ask_ai must be stamped "
                    "reconstruction_status='PACKET_RECONSTRUCTION_PARTIAL' — the "
                    "packet is rebuilt and is never an exact historical reproduction")

        if task == "annual_report_summary":
            # Dual-input is the point of this fixture; a case missing the
            # legacy input can only be replayed one way, so say so loudly.
            if not case.get("legacy_input_text"):
                problems.append(
                    f"case[{index}] has no legacy_input_text — it cannot be replayed "
                    "against the pipeline that produced its reference")

    return problems


def load(path: str) -> FixtureSet:
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    problems = validate_document(doc)
    if problems:
        joined = "\n  - ".join(problems)
        raise ValueError(f"invalid fixture file {path}:\n  - {joined}")
    return FixtureSet(
        task=doc["task"],
        cases=doc["cases"],
        source=doc.get("source") or {},
        exported_at=doc.get("exported_at") or "",
        schema_version=doc["schema_version"],
        path=path,
    )


def save(doc: Dict[str, Any], path: str) -> None:
    problems = validate_document(doc)
    if problems:
        joined = "\n  - ".join(problems)
        raise ValueError(f"refusing to write an invalid fixture file:\n  - {joined}")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2, default=str)
