#!/usr/bin/env python3
"""Write Qwen's generated annual_report output back into the REAL
`annual_reports` Mongo collection, matched by `filing_id` (the export
drops `_id`; `filing_id` is confirmed unique across all 8,354 documents).

FIELD MAPPING — CORRECTED 2026-09-04 after a real, live bug
--------------------------------------------------------------
This docstring used to claim the field shape "mirrors annual_report_
summarizer.py's own update dict EXACTLY, so downstream consumers see no
schema difference." That claim was never actually checked against Qwen's
real output and was false: Qwen's real schema (app/prompts/
annual_report_summary.py) produces executive_summary/key_points/
important_risks/key_takeaway. The real production read path
(api/app/routers/research.py::_annual_report_block) queries and projects
summary/bullets/key_takeaway — the OLD gpt-4o-mini field names. Found live
on the very first real AR generation run this project has done: writing
Qwen's output unconditionally set `summary: None` and `bullets: None`
(out.get() on keys Qwen's schema doesn't have), NULLING OUT a perfectly
good pre-existing gpt-4o-mini summary on two real production documents
(ADANIPOWER, SBILIFE) — both went blank on the real Research page.
Confirmed by querying research.py's own real filter afterward: the
document still matched (`summary: {"$exists": True}` matches a null
value), but `summary`/`bullets` came back null, only `key_takeaway`
survived.

Fixed by deriving the fields the reader needs from whichever schema
actually produced content, rather than assuming one specific schema:
`summary` falls back to `executive_summary`, `bullets` falls back to
`key_points`, when the direct field is absent. And a field is never
written as an explicit null — if neither source produced a value, that
key is dropped from the update entirely rather than clobbering whatever
was there. This is not a one-off patch for two documents: since Qwen's
real schema never produces plain `summary`/`bullets` at all, EVERY future
AR generation run would have silently blanked the Research page for
every document it touched, without this fix.

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


def build_update(out: dict, model: str, now_iso: str) -> dict:
    """Pure function, no I/O — the actual field-mapping fix, kept separate
    from main() so it is directly unit-testable (see
    test_writeback_field_mapping.py) without a real Mongo connection.
    `out` is one case's `row["output"]` from a real kaggle-output JSON.
    """
    summary_text = out.get("summary") or out.get("executive_summary")
    bullets_list = out.get("bullets") or out.get("key_points")
    update = {
        "executive_summary": out.get("executive_summary"),
        "key_points": out.get("key_points"),
        "important_risks": out.get("important_risks"),
        "summary": summary_text,
        "bullets": bullets_list,
        "key_takeaway": out.get("key_takeaway"),
        "summary_model": model,
        "summarized_at": now_iso,
    }
    return {k: v for k, v in update.items() if v is not None}


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
    if args.confirm:
        ensure_indexes(db)
    for row in doc["results"]:
        filing_id = row.get("filing_id")
        from review_guard import write_summary
        out = row.get("output") or {}
        update = build_update(out, doc["model"], row.get("generated_at") or datetime.now(timezone.utc).isoformat())
        action = write_summary(db, "annual_report", row, update, args.confirm)
        print(f"  {filing_id}: {action}")
        written += action in ("PUBLISHED", "WOULD PUBLISH", "ALREADY PUBLISHED")
        held += action in ("HELD", "WOULD HOLD")
        skipped += action.startswith("BLOCKED")

    print(f"\n{'WROTE' if args.confirm else 'WOULD WRITE'} {written}, skipped {skipped}, held for review {held}")
    if not args.confirm:
        print("DRY RUN — nothing was written. Re-run with --confirm to write.")


if __name__ == "__main__":
    main()
