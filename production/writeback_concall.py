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
    ensure_indexes(db)
    for row in doc["results"]:
        filing_id = row.get("filing_id")
        if not row.get("ok"):
            # Held for human review rather than dropped. This branch used to
            # print one line and lose the case forever — see production/
            # review_queue.py for why that mattered.
            action = enqueue_for_review(db, "concall", filing_id, row,
                                        symbol=row.get("symbol"),
                                        confirm=args.confirm)
            print(f"  HELD {filing_id}: {row.get('human_review_reason') or row.get('error')}"
                  f" [{action}]")
            held += 1
            continue
        out = row.get("output") or {}
        update = {
            "summary": out.get("summary"),
            "tone_label": out.get("tone_label"),
            "tone_note": out.get("tone_note"),
            "summary_model": doc["model"],
            "summarized_at": datetime.now(timezone.utc).isoformat(),
        }
        existing = col.find_one({"filing_id": filing_id})
        if existing is None:
            print(f"  SKIP {filing_id}: no matching document found — refusing to write")
            skipped += 1
            continue

        print(f"  {'WRITE' if args.confirm else 'WOULD WRITE'} {filing_id} "
             f"({row.get('symbol')}) tone={update['tone_label']}")
        if args.confirm:
            result = col.update_one({"filing_id": filing_id}, {"$set": update})
            reread = col.find_one({"filing_id": filing_id}, {k: 1 for k in update})
            ok = all(reread.get(k) == v for k, v in update.items())
            print(f"    matched={result.matched_count} modified={result.modified_count} "
                 f"VERIFY={'OK' if ok else 'MISMATCH — INVESTIGATE'}")
            if not ok:
                sys.exit(1)
        written += 1

    print(f"\n{'WROTE' if args.confirm else 'WOULD WRITE'} {written}, skipped {skipped}, held for review {held}")
    if not args.confirm:
        print("DRY RUN — nothing was written. Re-run with --confirm to write.")


if __name__ == "__main__":
    main()
