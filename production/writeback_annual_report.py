#!/usr/bin/env python3
"""Write Qwen's generated annual_report output back into the REAL
`annual_reports` Mongo collection, matched by `filing_id` (the export
drops `_id`; `filing_id` is confirmed unique across all 8,354 documents).

Field shape mirrors annual_report_summarizer.py's own `update` dict
EXACTLY, so downstream consumers (Research page, Ask AI) see no schema
difference from a gpt-4o-mini-authored document — only `summary_model`
distinguishes provenance.

SAFETY: only writes fields this dict names. Never touches raw_text,
extraction_status, or any other field. Requires --confirm to actually
write; without it, prints what WOULD be written and touches nothing.
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
    ap.add_argument("--kaggle-output", required=True,
                    help="the production_generate.py output JSON")
    ap.add_argument("--confirm", action="store_true",
                    help="without this, DRY-RUN only — no writes")
    args = ap.parse_args()

    doc = json.load(open(args.kaggle_output, encoding="utf-8"))
    print(f"generated_ok: {doc['generated_ok']}/{doc['cases']}  "
         f"model={doc['model']}  policy={doc['policy']}")

    db = get_db()
    col = db["annual_reports"]

    written = skipped = held = 0
    ensure_indexes(db)
    for row in doc["results"]:
        filing_id = row.get("filing_id")
        if not row.get("ok"):
            # Held for human review rather than dropped. This branch used to
            # print one line and lose the case forever — see production/
            # review_queue.py for why that mattered.
            action = enqueue_for_review(db, "annual_report", filing_id, row,
                                        symbol=row.get("symbol"),
                                        confirm=args.confirm)
            print(f"  HELD {filing_id}: {row.get('human_review_reason') or row.get('error')}"
                  f" [{action}]")
            held += 1
            continue
        out = row.get("output") or {}
        update = {
            "executive_summary": out.get("executive_summary"),
            "key_points": out.get("key_points"),
            "important_risks": out.get("important_risks"),
            "summary": out.get("summary"),
            "bullets": out.get("bullets"),
            "key_takeaway": out.get("key_takeaway"),
            "summary_model": doc["model"],
            "summarized_at": datetime.now(timezone.utc).isoformat(),
        }
        existing = col.find_one({"filing_id": filing_id})
        if existing is None:
            print(f"  SKIP {filing_id}: no matching document found — refusing to write")
            skipped += 1
            continue

        print(f"  {'WRITE' if args.confirm else 'WOULD WRITE'} {filing_id} "
             f"({row.get('symbol')})")
        if args.confirm:
            result = col.update_one({"filing_id": filing_id}, {"$set": update})
            # VERIFY immediately: re-read and confirm the write landed exactly.
            reread = col.find_one({"filing_id": filing_id},
                                  {k: 1 for k in update})
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
