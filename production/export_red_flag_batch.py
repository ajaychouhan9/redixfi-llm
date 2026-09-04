#!/usr/bin/env python3
"""Export a real batch of ALREADY-CLASSIFIED chunks for RECLASSIFICATION
with Qwen — READ-ONLY against ChromaDB. Unlike export_fixtures.py's
build_red_flag() (a stratified eval SAMPLE from annual_reports only, for
comparing against a reference), this selects real production chunks from
BOTH collections in filing order, for an actual reclassification run.

`candidates` is recomputed via the REAL matched_categories() keyword
prefilter — the same one Chroma metadata itself does not store, so this
mirrors exactly what classify_chunk() would receive live.
"""
import argparse
import json
import os
import sys

REDIXFI_ROOT = os.getenv("REDIXFI_ROOT", "/home/ubuntu/redixfi-backend")
sys.path.insert(0, REDIXFI_ROOT)
sys.path.insert(0, os.path.join(REDIXFI_ROOT, "data-pipeline"))
# 2026-09-02: repointed at the new dedicated /data/chroma mount (127GB
# ext4, permanent in /etc/fstab) after the chroma_production wipe -- a
# separate top-level mount, not derived from REDIXFI_ROOT anymore.
CHROMA_PATH = os.getenv("CHROMA_PATH", "/data/chroma")

# 2026-09-04: `col.get(..., include=["documents", ...])` below used to be
# the real chunk text. Since the 2026-09-02 storage-reduction change
# (annual_report_embedder.py / writeback_embeddings.py stopped passing
# `documents=` to Chroma at all), that field is unconditionally None for
# every chunk written since -- confirmed live: a real post-2026-09-02
# chunk's `documents` comes back `[None]`. Chunk text now lives in Mongo's
# `chunk_text` collection, keyed `_id = "{filing_id}_{chunk_index}"` -- the
# same convention api/app/core/document_retrieval.py::_fetch_chunk_texts
# and risk_flag_backfill.py's 2026-09-04 fix both use.


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--collection", choices=("annual_reports", "investor_calls"),
                    default="annual_reports")
    ap.add_argument("--limit", type=int, default=2)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    import chromadb
    from risk_flag_classifier import matched_categories
    from config.db import get_db

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    col = client.get_collection(args.collection)
    db = get_db()

    cases = []
    offset = 0
    while len(cases) < args.limit:
        page = col.get(limit=500, offset=offset, include=["metadatas"])
        ids = page.get("ids") or []
        if not ids:
            break
        text_by_id = {r["_id"]: r.get("text", "") for r in
                     db["chunk_text"].find({"_id": {"$in": ids}}, {"_id": 1, "text": 1})}
        for cid, meta in zip(ids, page.get("metadatas") or []):
            meta = meta or {}
            doc = text_by_id.get(cid, "")
            if meta.get("risk_classified") is None:
                continue   # only re-classify chunks already touched once
            cands = matched_categories(doc or "")
            if not cands:
                continue   # nothing for the LLM to confirm — skip, matches production's own short-circuit
            cases.append({
                "chunk_id": cid,
                "benchmark_id": f"RF_{cid}",
                "candidates": cands,
                "chunk_text": doc or "",
                "previous_classification": {
                    "risk_flag_type": meta.get("risk_flag_type"),
                    "risk_flag_summary": meta.get("risk_flag_summary"),
                },
                "source_collection": args.collection,
            })
            if len(cases) >= args.limit:
                break
        offset += len(ids)

    doc_out = {"schema_version": 2, "task": "red_flag",
              "source": {"synthetic": False, "read_only": True,
                        "note": "real production chunks, for reclassification"},
              "cases": cases}
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(doc_out, fh, ensure_ascii=False, indent=2, default=str)
    print(f"[{args.collection}] exported {len(cases)} real chunks -> {args.out}")
    print("This is the ONLY file this script created. No production store was modified.")


if __name__ == "__main__":
    main()
