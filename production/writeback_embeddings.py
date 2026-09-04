#!/usr/bin/env python3
"""Write Kaggle-produced Qwen vectors into the REAL /data/chroma store,
and the matching chunk text into Mongo's `chunk_text` collection.

This is the VM-side half of the embedding round trip: Kaggle returns
vectors (it cannot reach the VM), this applies them.

Storage architecture (2026-09-02, measured 59.91% cut): Chroma holds
vectors + minimal metadata, NEVER `documents=` — passing chunk text to
Chroma unconditionally triggers chromadb's trigram FTS5 index, which this
project never queries. Chunk text lives in Mongo `chunk_text`, keyed
`_id = "{filing_id}_{chunk_index}"`, and is fetched at query time by
api/app/core/document_retrieval.py::_fetch_chunk_texts.

SAFETY: --confirm required to write; without it this is a dry run that
touches nothing, matching writeback_annual_report.py / writeback_concall.py
/ writeback_red_flag.py. Verifies each write by reading it back.

  python3 writeback_embeddings.py --kaggle-output out.json            # dry run
  python3 writeback_embeddings.py --kaggle-output out.json --confirm  # writes
"""
from __future__ import annotations

import argparse
import json
import os
import sys

REDIXFI_ROOT = os.getenv("REDIXFI_ROOT", "/home/ubuntu/redixfi-backend")
sys.path.insert(0, REDIXFI_ROOT)
sys.path.insert(0, os.path.join(REDIXFI_ROOT, "data-pipeline"))

import chromadb  # noqa: E402
from pymongo import ReplaceOne  # noqa: E402

from config.db import get_db  # noqa: E402

CHROMA_PATH = os.getenv("CHROMA_PATH", "/data/chroma")
COLLECTION_FOR = {"annual_reports": "annual_reports",
                  "investor_calls": "investor_calls"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kaggle-output", required=True)
    ap.add_argument("--input-batch", required=False,
                    help="the export fed to Kaggle; supplies chunk TEXT, which "
                         "the kernel does not echo back")
    ap.add_argument("--confirm", action="store_true")
    args = ap.parse_args()

    doc = json.load(open(args.kaggle_output, encoding="utf-8"))
    results = doc.get("results", [])
    print(f"[INFO] kernel output: {doc.get('embedded')}/{doc.get('input_chunks')} "
          f"embedded | dtype={doc.get('dtype')} | "
          f"{doc.get('chunks_per_sec')} chunks/sec | complete={doc.get('complete')}")
    if doc.get("dtype") and doc["dtype"] != "torch.float16":
        print(f"[WARN] kernel ran {doc['dtype']}, not float16 — that is the "
              f"2.66 chunks/sec path; vectors are still valid, throughput was not")
    if not results:
        print("[INFO] nothing to write.")
        return 0

    text_by_key = {}
    if args.input_batch:
        src = json.load(open(args.input_batch, encoding="utf-8"))
        for c in src["chunks"]:
            text_by_key[f"{c['filing_id']}_{c['chunk_index']}"] = c["text"]
        print(f"[INFO] loaded chunk text for {len(text_by_key)} chunk(s) from the input batch")
    else:
        print("[WARN] no --input-batch given: chunk_text rows will NOT be written, "
              "so retrieval would find vectors with no recoverable text")

    db = get_db()
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    by_source = {}
    for r in results:
        by_source.setdefault(r.get("source") or "annual_reports", []).append(r)

    total_vec = total_txt = 0
    for source, rows in by_source.items():
        cname = COLLECTION_FOR.get(source)
        if not cname:
            print(f"[WARN] unknown source {source!r}, skipping {len(rows)} row(s)")
            continue
        col = client.get_or_create_collection(cname)
        ids = [f"{r['filing_id']}_{r['chunk_index']}" for r in rows]
        embs = [r["embedding"] for r in rows]
        metas = [{"chunk_index": r["chunk_index"], "symbol": r.get("symbol") or "",
                  "filing_id": r["filing_id"], "doc_type": r.get("doc_type") or "",
                  "page_number": r.get("page_number", 0)} for r in rows]

        dims = {len(e) for e in embs}
        print(f"[INFO] {cname}: {len(rows)} vector(s), dim(s)={dims}")
        if len(dims) != 1:
            print(f"[ERROR] inconsistent vector dimensions {dims} — refusing to write")
            return 1

        print(f"  {'WRITE' if args.confirm else 'WOULD WRITE'} {len(ids)} vector(s) "
              f"into Chroma '{cname}'")
        if args.confirm:
            # 2026-09-04: chromadb enforces its OWN max batch size per
            # upsert() call — found live on the first real production-scale
            # writeback (42,180 vectors in one batch): "Batch size of 42180
            # is greater than max batch size of 5461". Invisible at every
            # smaller scale this project tested at (the round-trip test was
            # 40 vectors). Queried at runtime via client.get_max_batch_size()
            # rather than hardcoded, so a future chromadb version changing
            # the limit doesn't silently reintroduce this. The failed call
            # raised before writing anything (confirmed live: Chroma count
            # was unchanged after the failure), so batching here is a real
            # fix, not a recovery from partial corruption.
            max_batch = client.get_max_batch_size()
            landed_total = 0
            for i in range(0, len(ids), max_batch):
                bi, be, bm = ids[i:i + max_batch], embs[i:i + max_batch], metas[i:i + max_batch]
                col.upsert(ids=bi, embeddings=be, metadatas=bm)
                got = col.get(ids=bi, include=[])
                landed = len(got.get("ids") or [])
                landed_total += landed
                if landed != len(bi):
                    print(f"    VERIFY batch [{i}:{i+len(bi)}]: {landed}/{len(bi)} "
                          f"present in Chroma — MISMATCH, INVESTIGATE")
                    return 1
            print(f"    VERIFY: {landed_total}/{len(ids)} present in Chroma "
                  f"{'OK' if landed_total == len(ids) else 'MISMATCH — INVESTIGATE'} "
                  f"({(len(ids) + max_batch - 1) // max_batch} batch(es) of <= {max_batch})")
        total_vec += len(ids)

        if text_by_key:
            ops, wrote = [], 0
            for r, _id in zip(rows, ids):
                txt = text_by_key.get(_id)
                if txt is None:
                    continue
                ops.append(ReplaceOne(
                    {"_id": _id},
                    {"_id": _id, "filing_id": r["filing_id"],
                     "chunk_index": r["chunk_index"], "text": txt},
                    upsert=True))
                wrote += 1
            print(f"  {'WRITE' if args.confirm else 'WOULD WRITE'} {wrote} chunk_text row(s)")
            if args.confirm and ops:
                db["chunk_text"].bulk_write(ops, ordered=False)
                back = db["chunk_text"].count_documents({"_id": {"$in": ids}})
                print(f"    VERIFY: {back}/{wrote} chunk_text row(s) readable "
                      f"{'OK' if back == wrote else 'MISMATCH — INVESTIGATE'}")
            total_txt += wrote

        if args.confirm:
            fids = sorted({r["filing_id"] for r in rows})
            db[source].update_many(
                {"filing_id": {"$in": fids}},
                {"$set": {"embedded": True, "embed_model": doc.get("model")}})
            print(f"  marked {len(fids)} source document(s) embedded=True")

    print(f"\n{'WROTE' if args.confirm else 'WOULD WRITE'} {total_vec} vector(s), "
          f"{total_txt} chunk_text row(s)")
    if not args.confirm:
        print("DRY RUN — nothing was written. Re-run with --confirm.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
