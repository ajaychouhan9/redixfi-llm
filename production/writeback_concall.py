#!/usr/bin/env python3
"""Write Qwen's generated concall output back into the REAL
`investor_calls` Mongo collection, matched by `filing_id` — the SAME key
concall_summarizer.py itself uses. Field shape mirrors it exactly.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, "/home/ubuntu/redixfi-backend")
from config.db import get_db  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_queue import ensure_indexes, enqueue_for_review  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kaggle-output", required=True)
    ap.add_argument("--confirm", action="store_true")
    args = ap.parse_args()

    doc = json.load(open(args.kaggle_output, encoding="utf-8"))
    print(f"generated_ok: {doc['generated_ok']}/{doc['cases']}  "
         f"model={doc['model']}  policy={doc['policy']}")

    db = get_db()
    col = db["investor_calls"]

    written = skipped = held = 0
    if args.confirm:
        ensure_indexes(db)
    for row in doc["results"]:
        filing_id = row.get("filing_id")
        from review_guard import write_summary
        out = row.get("output") or {}
        update = {k: out[k] for k in ("summary", "tone_label", "tone_note", "bullets", "key_takeaway") if out.get(k) is not None}
        update.update(summary_model=doc["model"], summarized_at=row.get("generated_at") or datetime.now(timezone.utc).isoformat())
        action = write_summary(db, "concall", row, update, args.confirm)
        print(f"  {filing_id}: {action}")
        written += action in ("PUBLISHED", "WOULD PUBLISH", "ALREADY PUBLISHED")
        held += action in ("HELD", "WOULD HOLD")
        skipped += action.startswith("BLOCKED")

    print(f"\n{'WROTE' if args.confirm else 'WOULD WRITE'} {written}, skipped {skipped}, held for review {held}")
    if not args.confirm:
        print("DRY RUN — nothing was written. Re-run with --confirm to write.")


if __name__ == "__main__":
    main()
