"""Fixture format — the contract between the RedixFi VM and this project.

A fixture file is a JSON document:

    {
      "schema_version": 1,
      "task": "annual_report_summary" | "red_flag" | "ask_ai",
      "exported_at": "2026-08-28T…Z",
      "source": { … provenance of the export … },
      "cases": [ { … one evaluation case … }, … ]
    }

Each case carries BOTH the input and the preserved production reference
output, so a comparison never depends on production being reachable again.
Fixtures are produced ONLY by scripts/export_fixtures.py running on the
RedixFi VM (read-only). Nothing in this project writes to production.

WHY THE REFERENCE TRAVELS WITH THE INPUT
----------------------------------------
RedixFi's OpenAI account had no credits as of 2026-08-28, so reference
outputs cannot be regenerated on demand. The 72 stored annual-report
summaries and the existing ask_conversations answers are what exist. The
fixture preserves them verbatim; losing them would mean losing the
comparison baseline entirely.

PER-TASK CASE FIELDS
--------------------
annual_report_summary
  input     : symbol, company_name, fiscal_year, filing_date, page_count,
              evidence_text  (from RedixFi's REAL evidence_finder.py),
              evidence_stats
  reference : reference.{executive_summary,key_points,important_risks,
              key_takeaway,summary,bullets,summary_model,summarized_at}

red_flag
  input     : chunk_id, symbol, doc_type, fiscal_year, chunk_text,
              candidates  (from RedixFi's REAL matched_categories())
  reference : reference.{risk_flag_type, risk_flag_summary} — both absent
              when production confirmed nothing, mirroring the metadata
              contract exactly

ask_ai
  input     : symbol, question, fact_packet, history, causal_backstop
  reference : reference.{answer, refused, model, sources_used,
              source_citations, weight}
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

SCHEMA_VERSION = 1

TASKS = ("annual_report_summary", "red_flag", "ask_ai")

REQUIRED_INPUT_FIELDS: Dict[str, tuple] = {
    "annual_report_summary": ("fixture_id", "symbol", "evidence_text"),
    "red_flag": ("fixture_id", "chunk_text", "candidates"),
    "ask_ai": ("fixture_id", "question", "fact_packet"),
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
        """Cases that actually carry a production reference output. A case
        without one is still a valid generation target, but it cannot be
        part of a side-by-side comparison — and saying so out loud is
        better than silently comparing against nothing."""
        return [c for c in self.cases if c.get("reference")]


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
    partially-broken export can still be inspected rather than just failing."""
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

    seen_ids = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            problems.append(f"case[{index}] is not an object")
            continue
        for field in REQUIRED_INPUT_FIELDS[task]:
            if field not in case or case[field] in (None, ""):
                problems.append(f"case[{index}] missing required field '{field}'")
        fixture_id = case.get("fixture_id")
        if fixture_id in seen_ids:
            problems.append(f"case[{index}] duplicate fixture_id {fixture_id!r}")
        seen_ids.add(fixture_id)

        if task == "red_flag" and isinstance(case.get("candidates"), list):
            # A red_flag case with no candidates costs zero LLM calls and
            # tells us nothing — flag it rather than quietly evaluating it.
            if not case["candidates"]:
                problems.append(
                    f"case[{index}] has an empty candidate list (no keyword match, "
                    "so no LLM call would ever be made — exclude it from the fixture)"
                )
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
