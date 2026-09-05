"""Operational AR/concall export. --inspect is read-only; --confirm reserves.

At least one, at most 25% of slots are reserved for oldest explicit retries;
unused slots flow to either lane. Minimum batch size two preserves both lanes.
One active immutable batch per task is reused until handled or cancelled, so
nightly staging cannot overwrite a manually-awaiting-GPU retry. There are no
automatic claim expirations: cancellation explicitly fences an abandoned run.
"""
import argparse
import json
import math
import os
from pathlib import Path
import sys
import uuid

ROOT = Path(os.getenv("REDIXFI_ROOT", "/home/ubuntu/redixfi-backend"))
sys.path.append(str(ROOT / "api"))
from review_lifecycle import CLAIMS, QUEUE, TARGETS, identity, reserve, review_lock

TASKS = {"annual_report_summary": "annual_report", "concall_summary": "concall"}

def select_documents(db, task, limit):
    if limit < 2:
        raise ValueError("generation batch limit must be at least 2 for retry/normal fairness")
    coll = db[TARGETS[task]]
    text_field = "raw_text" if task == "annual_report" else "raw_transcript_text"
    retries = []
    unavailable = []
    for r in db[QUEUE].find({"task": task, "state": "retry_queued",
                              "dispatch_token": {"$exists": False}}).sort([("updated_at", 1), ("_id", 1)]):
        d = coll.find_one({"filing_id": r["doc_id"]})
        if d and d.get(text_field) and d.get("extraction_status") == "OK":
            retries.append(d)
        else:
            unavailable.append(r["doc_id"])
    excluded = {r["doc_id"] for r in db[QUEUE].find({"task": task}, {"doc_id": 1})}
    excluded.update(c["doc_id"] for c in db[CLAIMS].find(
        {"task": task, "state": {"$ne": "cancelled"}}, {"doc_id": 1}))
    query = {"extraction_status": "OK", text_field: {"$exists": True, "$ne": ""},
             "filing_id": {"$exists": True, "$nin": sorted(excluded)},
             "summary_reviewed_by": {"$exists": False},
             "status": {"$nin": ["pending_review", "discarded"]}}
    normals = list(coll.find(query).sort([("filing_date", -1), ("filing_id", 1)]).limit(limit))
    retry_slots = min(len(retries), max(1, math.ceil(limit / 4)))
    chosen = [(d, True) for d in retries[:retry_slots]]
    chosen += [(d, False) for d in normals[:limit - len(chosen)]]
    chosen += [(d, True) for d in retries[retry_slots:retry_slots + limit - len(chosen)]]
    return chosen, unavailable

def build_case(task, doc, evidence_finder=None):
    common = {k: doc.get(k) for k in ("filing_id", "symbol", "company_name", "filing_date", "fiscal_year", "source_pdf_url")}
    common["benchmark_id"] = identity(task, doc["filing_id"])
    common["fixture_id"] = common["benchmark_id"]
    if task == "annual_report":
        if evidence_finder is None:
            sys.path.insert(0, str(ROOT / "data-pipeline"))
            import evidence_finder
        chunks = evidence_finder.chunks_from_raw_text(doc["raw_text"], symbol=doc.get("symbol", ""),
            token_target=500, page_count=doc.get("page_count"))
        evidence = evidence_finder.build_narrative_evidence_result(chunks, max_tokens=20000) if chunks else {}
        if not evidence.get("text"):
            raise ValueError("Evidence Finder produced no evidence")
        common.update(evidence_text=evidence["text"], doc_type="annual_report")
    else:
        common.update(input_text=doc["raw_transcript_text"][:120000],
            doc_kind="earnings concall transcript" if doc.get("subject") == "EARNINGS_CALL_TRANSCRIPT" else "investor presentation",
            doc_type="concall_transcript", subject=doc.get("subject"))
    return common

def export(db, task, limit, out, confirm=False, builder=build_case):
    with review_lock("generation-export:" + task):
        active = db[CLAIMS].find_one({"task": task, "state": {"$in": ["selected", "writing"]}})
        if active:
            batch = db.llm_generation_batches.find_one({"_id": active["batch_id"]})
            if not batch or not Path(batch["path"]).is_file():
                raise RuntimeError("active batch artifact missing; inspect/cancel its selected receipts before re-export")
            payload = json.loads(Path(batch["path"]).read_text(encoding="utf-8"))
            receipts = {c["doc_id"]: c for c in db[CLAIMS].find({"batch_id": active["batch_id"]})}
            payload["cases"] = [c for c in payload["cases"] if
                receipts.get(c["filing_id"], {}).get("token") == c.get("dispatch_token")
                and receipts[c["filing_id"]].get("state") != "cancelled"]
            if not any(c["filing_id"] == active["doc_id"] for c in payload["cases"]):
                raise RuntimeError("active receipt missing from artifact; explicit recovery required")
            if confirm:
                Path(out).parent.mkdir(parents=True, exist_ok=True)
                Path(out).write_text(json.dumps(payload, default=str), encoding="utf-8")
            return payload
        selected, unavailable = select_documents(db, task, limit)
        batch_id = uuid.uuid4().hex
        cases, skipped = [], []
        for doc, retry in selected:
            try:
                case = builder(task, doc)
            except Exception as exc:
                skipped.append({"filing_id": doc["filing_id"], "reason": str(exc)})
                continue
            case["is_review_retry"] = retry
            cases.append(case)
        payload = {"schema_version": 2, "task": next(k for k,v in TASKS.items() if v == task),
                   "batch_id": batch_id, "cases": cases, "skipped": skipped, "unavailable_retries": unavailable}
        if not confirm:
            return payload
        immutable = Path(out).parent / "batches" / (batch_id + ".json")
        immutable.parent.mkdir(parents=True, exist_ok=True)
        for case in cases:
            case["dispatch_token"] = uuid.uuid4().hex
        # Durable intent precedes claims; interrupted export stays fail-closed
        # and reports a recoverable artifact instead of selecting duplicates.
        immutable.write_text(json.dumps(payload, default=str), encoding="utf-8")
        db.llm_generation_batches.insert_one({"_id": batch_id, "task": task, "path": str(immutable)})
        reserved = []
        for case in cases:
            token = reserve(db, task, case["filing_id"], batch_id, case["dispatch_token"])
            if token:
                case["dispatch_token"] = token
                reserved.append(case)
        payload["cases"] = reserved
        temporary = immutable.with_suffix(".tmp")
        temporary.write_text(json.dumps(payload, default=str), encoding="utf-8")
        temporary.replace(immutable)
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(json.dumps(payload, default=str), encoding="utf-8")
        return payload

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=TASKS, required=True)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--out", required=True)
    parser.add_argument("--confirm", action="store_true")
    parser.add_argument("--inspect", action="store_true")
    args = parser.parse_args()
    if args.confirm and args.inspect:
        parser.error("choose --confirm or --inspect")
    sys.path.insert(0, str(ROOT))
    from config.db import get_db
    payload = export(get_db(), TASKS[args.task], args.limit, args.out, args.confirm)
    print(json.dumps({"confirmed": args.confirm, "batch_id": payload["batch_id"],
        "selected": [{k: c.get(k) for k in ("symbol", "filing_id", "is_review_retry")} for c in payload["cases"]],
        "skipped": payload["skipped"], "unavailable_retries": payload["unavailable_retries"]}, default=str))

if __name__ == "__main__":
    main()
