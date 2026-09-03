#!/usr/bin/env python3
"""Export a real batch of real chunks for Qwen embedding on Kaggle.

READ-ONLY against Mongo. Chunks are produced by the REAL production
chunker (data-pipeline/annual_report_embedder.py's chunk_text_blocks +
noise filters), so what gets embedded is byte-identical to what the
embedder itself would have produced — no reimplementation.

Most-recent-first by default, per the incremental-rollout decision:
newest filings are embedded first so the useful corpus is live early,
with historical depth filling in behind it.

Concall respects the 8-quarter retention cap (data-pipeline/
concall_retention.py); annual reports are deliberately uncapped.

  python3 export_embed_batch.py --source annual_reports --limit 100 --out /tmp/in.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys

REDIXFI_ROOT = os.getenv("REDIXFI_ROOT", "/home/ubuntu/redixfi-backend")
sys.path.insert(0, REDIXFI_ROOT)
sys.path.insert(0, os.path.join(REDIXFI_ROOT, "data-pipeline"))

from config.db import get_db  # noqa: E402
from annual_report_embedder import (  # noqa: E402
    chunk_text_blocks, is_garbled, is_table_noise,
)
from concall_retention import CONCALL_MAX_QUARTERS, select_recent_quarters  # noqa: E402

SOURCES = {
    "annual_reports": {"text_field": "raw_text", "token_target": 500,
                       "doc_type": "annual_report"},
    "investor_calls": {"text_field": "raw_transcript_text", "token_target": 300,
                       "doc_type": "concall_transcript"},
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=sorted(SOURCES), required=True)
    ap.add_argument("--limit", type=int, default=100,
                    help="max DOCUMENTS (not chunks) to export")
    ap.add_argument("--out", required=True)
    ap.add_argument("--force", action="store_true",
                    help="include documents already marked embedded=True")
    args = ap.parse_args()

    cfg = SOURCES[args.source]
    db = get_db()
    col = db[args.source]

    query = {"extraction_status": "OK",
             cfg["text_field"]: {"$exists": True, "$ne": ""}}
    if not args.force:
        query["embedded"] = {"$exists": False}

    # 2026-09-03 MEMORY FIX: this used to be `docs = list(col.find(query))`
    # with NO projection — pulling every candidate document's full raw_text/
    # raw_transcript_text into memory just to sort and slice off the top
    # --limit. On the real 8,423-candidate AR backlog that is enough full
    # annual-report text to OOM-kill the process (confirmed live: RSS hit
    # 11.5GB before the kernel killed it, on a host with 10GB free at the
    # time). A "small daily batch" driver script cannot carry an O(whole
    # backlog) memory footprint. Fixed in two passes: gather ONLY the
    # lightweight sort/filter fields for every candidate first, pick the
    # final N ids in Python, then fetch full text for just those N.
    light_projection = {"_id": 1, "filing_date": 1, "symbol": 1}
    light_docs = list(col.find(query, light_projection))
    print(f"[INFO] {args.source}: {len(light_docs)} candidate document(s)")

    if args.source == "investor_calls":
        before = len(light_docs)
        light_docs = select_recent_quarters(light_docs, CONCALL_MAX_QUARTERS)
        if before != len(light_docs):
            print(f"[INFO] retention cap (last {CONCALL_MAX_QUARTERS} quarters): "
                  f"{before} -> {len(light_docs)}")

    # MOST-RECENT-FIRST — the incremental rollout decision.
    light_docs.sort(key=lambda d: (d.get("filing_date") or ""), reverse=True)
    chosen_ids = [d["_id"] for d in light_docs[:args.limit]]
    print(f"[INFO] exporting newest {len(chosen_ids)} document(s)")

    # Second pass: full text for ONLY the chosen documents, order preserved.
    full_by_id = {d["_id"]: d for d in col.find({"_id": {"$in": chosen_ids}})}
    docs = [full_by_id[i] for i in chosen_ids if i in full_by_id]

    out = {"schema": "qwen_embed_batch_v1", "source": args.source, "chunks": []}
    for doc in docs:
        text = doc.get(cfg["text_field"], "")
        paras = [p for p in text.split("\n\n") if p.strip()] or [text]
        raw, _ = chunk_text_blocks(paras, token_target=cfg["token_target"])
        kept = [(p, o) for p, o in raw
                if not is_table_noise(p) and not is_garbled(p)]
        total_chars = len(text) or 1
        page_count = doc.get("page_count", 0) or 0
        for idx, (piece, off) in enumerate(kept):
            page_number = (max(1, round(off / total_chars * page_count))
                           if page_count else 0)
            out["chunks"].append({
                "filing_id": str(doc.get("filing_id", "")),
                "chunk_index": idx,
                "symbol": doc.get("symbol", ""),
                "doc_type": cfg["doc_type"],
                "source": args.source,
                "page_number": page_number,
                "text": piece,
            })

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    print(f"[INFO] {len(out['chunks'])} chunk(s) from {len(docs)} document(s)")
    print(f"[WROTE] {args.out}")
    print("This script created only that file. No production store was modified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
