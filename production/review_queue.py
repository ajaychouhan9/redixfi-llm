"""Enqueue a failed/held Qwen case for human review instead of dropping it.

Shared by the writeback scripts. Before this, a case that failed validation
produced exactly one line of stdout and then ceased to exist:

    if not row.get("ok"):
        print(f"  SKIP {filing_id}: generation failed ({row.get('error')})")
        skipped += 1
        continue

The GPU time was spent, the model produced something, a validator rejected
it — and none of that was recorded. `human_review_required` and
`human_review_reason` were computed all the way through TaskResult and then
thrown away at the last step. This module is where they land instead.

The queue schema is defined once, on the API side, in
`api/app/core/review_queue.py`; this is the producer for it. Field names are
duplicated here rather than imported because this script runs on the VM
against llm-pipeline's own path, not inside the API package — the two are
kept in sync by hand, and `--verify-schema` below fails loudly if they drift.

SAFETY: enqueueing NEVER writes to annual_reports/investor_calls. A held
case leaves the real document untouched; only an approval in the admin UI
publishes anything.
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from typing import Any, Optional

REVIEW_QUEUE = "llm_review_queue"
PENDING = "pending"
RETRY_QUEUED = "retry_queued"


def queue_id(task: str, doc_id: str) -> str:
    return f"{task}:{doc_id}"


def enqueue_for_review(db, task: str, doc_id: str, row: dict,
                       symbol: Optional[str] = None,
                       confirm: bool = False) -> str:
    """Upsert one held case. Returns the action taken, for the caller's log.

    Upsert, not insert: re-running a batch that still fails must update the
    existing row, not stack a duplicate the reviewer has to triage twice.
    `retry_count` and the original `created_at` survive the update, so the
    queue can answer "how many times has this specific document failed".

    A row already resolved by a human is NOT reopened by a later batch —
    that would silently undo an admin's discard.
    """
    from review_guard import complete_result
    failed = dict(row, ok=False, human_review_required=True)
    failed["symbol"] = symbol or row.get("symbol")
    return complete_result(db, task, doc_id, failed, lambda: None, confirm)

def ensure_indexes(db) -> None:
    """`state` drives the admin list query; `created_at` its sort order."""
    db[REVIEW_QUEUE].create_index("state")
    db[REVIEW_QUEUE].create_index([("state", 1), ("created_at", 1)])
    db[REVIEW_QUEUE].create_index("task")


def verify_schema_matches_api(api_module_path: str) -> bool:
    """Guard against the hand-sync between this producer and the API-side
    consumer drifting. Compares the constants that actually matter."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("_rq_api", api_module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    problems = []
    if mod.REVIEW_QUEUE != REVIEW_QUEUE:
        problems.append(f"collection name: {mod.REVIEW_QUEUE!r} != {REVIEW_QUEUE!r}")
    if mod.PENDING != PENDING:
        problems.append(f"PENDING: {mod.PENDING!r} != {PENDING!r}")
    if mod.queue_id("t", "d") != queue_id("t", "d"):
        problems.append("queue_id() formats differ")
    for p in problems:
        print(f"SCHEMA DRIFT: {p}", file=sys.stderr)
    if not problems:
        print("schema matches the API-side definition")
    return not problems


if __name__ == "__main__":
    ok = verify_schema_matches_api(
        "/home/ubuntu/redixfi-backend/api/app/core/review_queue.py")
    sys.exit(0 if ok else 1)
