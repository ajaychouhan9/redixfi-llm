"""Example bank — an accumulating store of REAL validated generations,
retrieved by similarity for use as few-shot context.

WHY THIS EXISTS
---------------
Manual prompt tuning this session showed diminishing/negative returns:
content steering backfired (negation priming), and the red_flag
instance-check fix traded 7 false positives for 26 new false negatives.
Both were single hand-written instructions applied globally. This is a
different mechanism: instead of writing a new instruction and hoping it
generalizes, accumulate REAL outputs that already passed the SAME
validator production uses, and show the model 1-2 of the most similar
ones at generation time. No training, no new instruction — the examples
ARE the guidance, and they come from what actually worked.

WHAT MAKES AN ENTRY ELIGIBLE
-----------------------------
Only `TaskResult.ok is True` outputs are ever stored — the same pass/fail
gate every task's real validator already applies. Nothing here re-judges
quality; it only remembers what the existing validator already accepted.

SIMILARITY METRIC — reused, not reinvented
-------------------------------------------
`app.evaluation.compare.jaccard` (word-set overlap) is used for
retrieval. RedixFi's own production pattern for this kind of matching is
a real embedding call (`text-embedding-3-small`, confirmed in
00_MASTER_CONTEXT.md's Annual Report RAG work) — a paid, network-
dependent OpenAI call. That is the right choice for retrieval quality at
production scale. It is deliberately NOT used here: this is a cheap
concept test with ~20 candidate entries per bank, jaccard is already
implemented, tested, and used elsewhere in this exact codebase as a
similarity signal, and it costs nothing per query. If retrieval quality
becomes the bottleneck once the bank is larger, swapping in a real
embedding call is a contained change — everything downstream of
`retrieve()` is metric-agnostic.

PERSISTENCE — this is the part that makes it a MECHANISM, not a demo
-----------------------------------------------------------------------
Kaggle is ephemeral: nothing on the compute instance survives past the
session. For this to actually accumulate across FUTURE runs rather than
just this session's test, the bank file must round-trip through the git
repo (or the Kaggle dataset) the same way run artifacts already do:
downloaded from the kernel's output, merged locally, committed, and
re-uploaded as part of the dataset before the next run. See
`scripts/bootstrap_example_bank.py` for the one-time seed and
`record_result()` below for the ongoing accumulation call the evaluation
runner makes after every real (non-echo) generation.

STORAGE FORMAT
---------------
One JSON file per task under `example_bank/`, e.g.
`example_bank/concall_summary.json` — a plain list of entries:

    {
      "benchmark_id": "CC_KANPRPLA_106607445",
      "added_at": "2026-08-30T...",
      "run_id": "20260830T041530Z",
      "model": "qwen3-14b-awq-tp2",
      "attempts_used": 4,
      "was_hard_case": true,
      "retrieval_text": "Kanpur Plastipack Limited ... investor presentation ...",
      "output": {"summary": "...", "tone_label": "...", "tone_note": "..."}
    }

`retrieval_text` is a short, task-specific field built for MATCHING, not
the full input — see `_retrieval_text_for()`. Plain JSON, no database,
so this needs no new dependency and is trivially diffable in a PR.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .evaluation.compare import jaccard

BANK_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "example_bank")


def _bank_path(task: str, bank_dir: str = BANK_DIR) -> str:
    return os.path.join(bank_dir, f"{task}.json")


def load_bank(task: str, bank_dir: str = BANK_DIR) -> List[Dict[str, Any]]:
    path = _bank_path(task, bank_dir)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save_bank(task: str, entries: List[Dict[str, Any]], bank_dir: str = BANK_DIR) -> str:
    os.makedirs(bank_dir, exist_ok=True)
    path = _bank_path(task, bank_dir)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(entries, fh, ensure_ascii=False, indent=2, default=str)
    return path


# ---------------------------------------------------------------------------
# What text represents a case, for matching purposes. Short and topical —
# NOT the full transcript/evidence block, which would make every jaccard
# score dominated by boilerplate document structure rather than content.
# ---------------------------------------------------------------------------
def retrieval_text_for(task: str, fixture: Dict[str, Any]) -> str:
    if task == "concall_summary":
        return " ".join(str(x) for x in (
            fixture.get("company_name"), fixture.get("symbol"),
            fixture.get("doc_kind"),
            (fixture.get("input_text") or "")[:800],   # topical opening, not the whole transcript
        ) if x)
    if task == "annual_report_summary":
        return " ".join(str(x) for x in (
            fixture.get("symbol"), fixture.get("fiscal_year"),
            (fixture.get("evidence_text") or fixture.get("input_text") or "")[:800],
        ) if x)
    if task == "red_flag":
        return " ".join(str(x) for x in (
            ",".join(fixture.get("candidates") or []),
            (fixture.get("chunk_text") or "")[:800],
        ) if x)
    return str(fixture.get("chunk_text") or fixture.get("input_text") or "")[:800]


def output_text_for(task: str, output: Dict[str, Any]) -> str:
    """The stored output rendered back to text — used both for retrieval
    (a stored example's own content also informs matching) and for
    rendering the example into a prompt."""
    if task == "concall_summary":
        return output.get("summary") or ""
    if task == "annual_report_summary":
        return output.get("executive_summary") or ""
    if task == "red_flag":
        return output.get("risk_flag_summary") or ""
    return json.dumps(output, ensure_ascii=False)


def record_result(
    task: str,
    fixture: Dict[str, Any],
    output: Dict[str, Any],
    *,
    attempts_used: int,
    model: str,
    run_id: str,
    bank_dir: str = BANK_DIR,
) -> None:
    """Append one validated success to the bank, if it isn't already there.
    Call this ONLY with an `ok=True` result — never a fail-soft fallback.

    De-duplicates by benchmark_id: a later successful run of the SAME case
    replaces the earlier entry rather than accumulating duplicates, so the
    bank tracks the model's most recent validated behaviour per case, not
    every historical attempt."""
    bid = str(fixture.get("benchmark_id") or fixture.get("fixture_id") or "")
    if not bid:
        return
    entries = load_bank(task, bank_dir)
    entries = [e for e in entries if e.get("benchmark_id") != bid]
    entries.append({
        "benchmark_id": bid,
        "added_at": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id,
        "model": model,
        "attempts_used": attempts_used,
        "was_hard_case": attempts_used > 1,
        "retrieval_text": retrieval_text_for(task, fixture),
        "output": output,
    })
    save_bank(task, entries, bank_dir)


def retrieve(
    entries: List[Dict[str, Any]],
    query_text: str,
    k: int = 2,
    exclude_benchmark_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Top-k entries by jaccard similarity to `query_text`. Excludes the
    current case by id, so a case never retrieves its own stored answer —
    the failure mode that would make a leave-one-out test meaningless."""
    candidates = [e for e in entries if e.get("benchmark_id") != exclude_benchmark_id]
    scored = [(jaccard(query_text, e.get("retrieval_text") or ""), e) for e in candidates]
    scored.sort(key=lambda t: t[0], reverse=True)
    return [e for score, e in scored[:k] if score > 0]
