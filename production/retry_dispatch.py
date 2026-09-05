"""One durable retry-dispatch tick. No sleeps and no GPU calls at import time.

The scheduler calls tick each minute. Busy accounts are checked again after
one hour. A launch with an uncertain outcome is reconciled, never re-pushed.
Review authority and publication remain in review_lifecycle/review_guard.
"""
from datetime import timedelta

from production.export_generation_batch import export
from review_lifecycle import QUEUE, review_lock

JOBS = "llm_gpu_dispatch_jobs"
TERMINAL = ("complete", "attention")


def tick(db, task, adapter, now, limit=20):
    """adapter implements account_busy/prepare/launch/status/collect_and_write.

    Callers hold an account lock as well when accounts share multiple tasks.
    Timestamps are naive UTC, matching PyMongo's default decoding.
    """
    with review_lock("retry-dispatch:" + task):
        jobs = db[JOBS]
        job = jobs.find_one({"task": task, "state": {"$ne": "complete"}})
        if job and job["state"] == "attention":
            return "attention"
        if not job:
            if not db[QUEUE].find_one({"task": task, "state": "retry_queued"}):
                return "idle"
            preview = export(db, task, limit, adapter.batch_path, confirm=False)
            if not any(c.get("is_review_retry") for c in preview["cases"]) and not db.llm_generation_claims.find_one(
                    {"task": task, "state": {"$in": ["selected", "writing"]}}):
                return "no eligible retry source"
            payload = export(db, task, limit, adapter.batch_path, confirm=True)
            if not payload["cases"]:
                return "no eligible source"
            job = {"_id": payload["batch_id"], "task": task, "state": "waiting_gpu",
                   "created_at": now, "next_check_at": now, "batch": payload}
            jobs.insert_one(job)
        if job.get("next_check_at", now) > now:
            return "waiting"

        def save(state, delay=0, **fields):
            fields.update(state=state, updated_at=now,
                          next_check_at=now + timedelta(seconds=delay))
            jobs.update_one({"_id": job["_id"]}, {"$set": fields})
            job.update(fields)
            return state

        try:
            if job["state"] in ("launching", "running"):
                status = adapter.status(job)
                if status == "complete":
                    # A repeated collection replays the exact output through the
                    # existing receipt/hash guard; it never launches generation.
                    adapter.collect_and_write(job)
                    return save("complete")
                if status in ("running", "queued"):
                    return save("running", 60)
                if status == "missing" and job["state"] == "launching":
                    # API timeout/crash after push: cannot prove non-execution.
                    # Do not retry a spend merely because status is missing.
                    return save("attention", reason="launch outcome unknown; inspect kernel before recovery")
                return save("attention", reason="kernel ended without a complete validated batch: " + status)
            if adapter.account_busy():
                return save("waiting_gpu", 3600, reason="GPU account busy; check again in one hour")
            if not adapter.prepare(job):
                return save("waiting_gpu", 60, reason="dataset processing")
            # Persist BEFORE the irreversible external request. The unique
            # kernel identity is derived from this immutable batch ID.
            save("launching")
            adapter.launch(job)
            return save("running", 60)
        except ValueError as exc:
            return save("attention", reason=str(exc))
        except Exception as exc:
            # In particular, never change launching back to waiting_gpu after
            # a network timeout: that would allow a duplicate GPU launch.
            return save(job["state"], 3600, reason=type(exc).__name__)


def verify_output(batch, output):
    """Reject stale, partial, duplicate or foreign output before any write."""
    expected = {(c["filing_id"], c["dispatch_token"]) for c in batch["cases"]}
    rows = output.get("results", [])
    actual = {(r.get("filing_id"), r.get("dispatch_token")) for r in rows}
    if (output.get("complete") is not True or output.get("task") != batch["task"]
            or actual != expected or len(rows) != len(expected)):
        raise ValueError("output is incomplete or does not match the dispatched batch")
