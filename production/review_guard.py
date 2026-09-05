"""Import the shared VM coordinator without colliding with either app package."""
import os
from pathlib import Path
import sys
sys.path.append(str(Path(os.getenv("REDIXFI_ROOT", "/home/ubuntu/redixfi-backend")) / "api"))
from review_lifecycle import allowed, complete_result, identity, review_lock  # noqa: F401

def write_summary(db, task, row, update, confirm=False):
    collection = {"annual_report": "annual_reports", "concall": "investor_calls"}[task]
    doc_id = row.get("filing_id")
    target = db[collection].find_one({"filing_id": doc_id})
    if target is None:
        return "BLOCKED: missing source document"
    # Defense for legacy documents already marked reviewed but lacking a queue
    # row. Never authorize by symbol, model name, or a client-provided role.
    if target.get("summary_reviewed_by"):
        return "BLOCKED: human-reviewed source"
    if target.get("status") in ("pending_review", "discarded") and not row.get("dispatch_token"):
        return "BLOCKED: held source without an authorized retry"
    def publish():
        if not update.get("summary"):
            raise ValueError("PASS has no usable summary")
        fields = {**update, "status": "published"}
        result = db[collection].update_one({"filing_id": doc_id,
            "summary_reviewed_by": {"$exists": False}}, {"$set": fields})
        if result.matched_count != 1:
            raise ValueError("source changed or was human-reviewed")
        actual = db[collection].find_one({"filing_id": doc_id})
        if any(actual.get(k) != v for k, v in fields.items()):
            raise ValueError("publication verification failed")
    return complete_result(db, task, doc_id, row, publish, confirm)

def write_red_flag(db, col, collection, row, meta, confirm=False):
    cid = row.get("chunk_id")
    task = "red_flag"
    # Red-flag identity includes collection because chunk ids can overlap.
    doc_id = f"{collection}:{cid}"
    existing = col.get(ids=[cid], include=["metadatas"])
    if not existing.get("ids"):
        return "BLOCKED: missing chunk"
    current = existing["metadatas"][0] or {}
    # Respect existing per-chunk human/pending markers, including legacy ones.
    if current.get("status") in ("pending_review", "discarded") or current.get("summary_reviewed_by"):
        return "BLOCKED: protected chunk"
    def publish():
        col.update(ids=[cid], metadatas=[meta])
        actual = col.get(ids=[cid], include=["metadatas"])["metadatas"][0] or {}
        if any(actual.get(k) != v for k,v in meta.items()):
            raise ValueError("red flag verification failed")
    # RF's established invalid/no-match result is a validated unflagged result;
    # it does not share AR/concall's summary-editor human-review workflow.
    if row.get("ok") is not True:
        return "SKIPPED: failed red-flag generation (no publication)"
    return complete_result(db, task, doc_id, row, publish, confirm)
