"""Controlled production-storage smoke test; isolated temporary collections.

Requires --confirm-test-records. Never reads/writes real queue/source rows.
Drops only this invocation's uniquely named test collections in finally.
No GPU/model/API authentication involved.
"""
import argparse
import os
from pathlib import Path
import sys
import uuid

ROOT = Path(os.getenv("REDIXFI_ROOT", "/home/ubuntu/redixfi-backend"))
sys.path.insert(0, str(ROOT))
sys.path.append(str(ROOT / "api"))
from review_lifecycle import reserve, cancel_selection, allowed, QUEUE, CLAIMS
from review_guard import write_summary

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--confirm-test-records", action="store_true", required=True)
    p.parse_args()
    from config.db import get_db
    real = get_db()
    prefix = "__review_test_" + uuid.uuid4().hex + "_"
    names = set()
    class Isolated:
        def __getitem__(self, name):
            assert name in (QUEUE, CLAIMS, "annual_reports", "investor_calls")
            full = prefix + name
            names.add(full)
            return real[full]
    db = Isolated()
    checks = 0
    try:
        for task, collection in (("annual_report", "annual_reports"), ("concall", "investor_calls")):
            for state in ("approved", "discarded", "pending", "retry_queued", None):
                doc_id = prefix + task + str(state)
                key = task + ":" + doc_id
                db[collection].insert_one({"filing_id": doc_id, "summary": "previous"})
                if state:
                    db[QUEUE].insert_one({"_id": key, "doc_id": doc_id, "task": task, "state": state,
                        "retry_count": 1, "qwen_output": {"summary": "held"}, "reason": "original"})
                row = {"filing_id": doc_id, "ok": True, "final_status": "QWEN_PASS", "output": {"summary": "safe"}}
                if state:
                    assert write_summary(db, task, row, {"summary": "unsafe"}, True).startswith("BLOCKED")
                    assert db[collection].find_one({"filing_id": doc_id})["summary"] == "previous"
                    checks += 1
                if state in (None, "retry_queued"):
                    token = reserve(db, task, doc_id, prefix)
                    assert token and not reserve(db, task, doc_id, prefix)
                    row["dispatch_token"] = token
                    assert write_summary(db, task, row, {"summary": "safe"}, True) == "PUBLISHED"
                    assert db[collection].find_one({"filing_id": doc_id})["summary"] == "safe"
                    assert not allowed(db, task, doc_id, token)
                    checks += 1
        print(f"{checks} real-Mongo controlled checks passed; real review rows untouched")
    finally:
        for name in names:
            assert name.startswith(prefix)
            real.drop_collection(name)
        assert not any(n.startswith(prefix) for n in real.list_collection_names())
        print("All invocation-specific test collections removed")

if __name__ == "__main__":
    main()
