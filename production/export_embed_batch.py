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

    docs = list(col.find(query))
    print(f"[INFO] {args.source}: {len(docs)} candidate document(s)")

    if args.source == "investor_calls":
        before = len(docs)
        docs = select_recent_quarters(docs, CONCALL_MAX_QUARTERS)
        if before != len(docs):
            print(f"[INFO] retention cap (last {CONCALL_MAX_QUARTERS} quarters): "
                  f"{before} -> {len(docs)}")

    # MOST-RECENT-FIRST — the incremental rollout decision.
    docs.sort(key=lambda d: (d.get("filing_date") or ""), reverse=True)
    docs = docs[:args.limit]
    print(f"[INFO] exporting newest {len(docs)} document(s)")

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
