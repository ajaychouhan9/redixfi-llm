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
    _id = queue_id(task, doc_id)
    now = datetime.now(timezone.utc)

    reason = (row.get("human_review_reason") or row.get("error")
              or "validation failed (no reason recorded)")

    # 2026-09-04, found live on this session's first real held case (VEDL):
    # row["output"] is only ever set on a SUCCESSFUL TaskResult (ok=True) -
    # for a held case it is always empty, even when the model produced
    # real, substantive content that merely failed a validator check on one
    # detail. Before this fix, the admin review page's "what Qwen produced"
    # panel showed nothing for every held case, and its own UI copy read
    # "Qwen produced no usable output, so this row must be edited before
    # approval" - actively misleading when real content exists in
    # `rejections`. Falls back to the LAST rejected attempt's parsed text,
    # which is exactly what a reviewer needs to judge whether to approve
    # with a small edit, retry, or discard.
    last_attempt = None
    for r in reversed(row.get("rejections") or []):
        if r.get("text"):
            last_attempt = r["text"]
            break
    qwen_output = row.get("output") or last_attempt

    fields: dict[str, Any] = {
        "task": task,
        "doc_id": doc_id,
        "collection": {"annual_report": "annual_reports",
                       "concall": "investor_calls"}.get(task),
        "symbol": symbol or row.get("symbol"),
        "reason": reason,
        "final_status": row.get("final_status"),
        "qwen_output": qwen_output,
        "model": row.get("model") or "",
        "attempts": row.get("attempts") or 0,
        "rejections": row.get("rejections"),
        "rephrase_log": row.get("rephrase_log"),
        "updated_at": now,
    }

    if not confirm:
        return "WOULD ENQUEUE"

    existing = db[REVIEW_QUEUE].find_one({"_id": _id}, {"state": 1})
    if existing and existing.get("state") not in (PENDING, RETRY_QUEUED):
        # A human already settled this one. Record that it failed again, but
        # do not drag it back into the queue behind their back.
        db[REVIEW_QUEUE].update_one(
            {"_id": _id},
            {"$set": {"last_failed_again_at": now, "updated_at": now},
             "$inc": {"failed_after_resolution": 1}})
        return "ALREADY RESOLVED (recorded, not reopened)"

    db[REVIEW_QUEUE].update_one(
        {"_id": _id},
        {"$set": {**fields, "state": PENDING},
         "$setOnInsert": {"created_at": now, "retry_count": 0,
                          "resolved_at": None, "resolved_by": None,
                          "edited": False, "notified_at": None}},
        upsert=True)
    return "ENQUEUED"


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
