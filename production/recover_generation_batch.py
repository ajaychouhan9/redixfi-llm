"""Inspect/cancel an abandoned batch; never launch, generate, or publish.

Cancel only after abandoning/stopping its GPU run. Late output is fenced by
the revoked receipt. Retry count is unchanged because this is execution
recovery, not a new human retry. An interrupted write cannot be cancelled:
rerun its writeback with the exact original result to finish verification.
"""
import argparse
import json
import os
from pathlib import Path
import sys

ROOT = Path(os.getenv("REDIXFI_ROOT", "/home/ubuntu/redixfi-backend"))
sys.path.append(str(ROOT / "api"))
sys.path.insert(0, str(ROOT))
from review_lifecycle import CLAIMS, cancel_selection, review_lock

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--batch-id", required=True)
    p.add_argument("--cancel-confirm", action="store_true")
    a = p.parse_args()
    from config.db import get_db
    db = get_db()
    rows = list(db[CLAIMS].find({"batch_id": a.batch_id}))
    print(json.dumps([{k:r.get(k) for k in ("task", "doc_id", "state", "created_at")} for r in rows], default=str))
    if a.cancel_confirm:
        if any(r["state"] == "writing" for r in rows):
            raise SystemExit("Publication started: replay the original result; cancellation refused")
        for r in rows:
            if r["state"] == "selected":
                with review_lock("generation-export:" + r["task"]):
                    cancel_selection(db, r["task"], r["doc_id"], r["token"])
        print("Abandoned selections cancelled; late output is blocked.")

if __name__ == "__main__":
    main()
