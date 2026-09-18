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
import codecs
import contextlib
import gc
import json
import os
import sys

REDIXFI_ROOT = os.getenv("REDIXFI_ROOT", "/home/ubuntu/redixfi-backend")
sys.path.insert(0, REDIXFI_ROOT)
sys.path.insert(0, os.path.join(REDIXFI_ROOT, "data-pipeline"))

import chromadb  # noqa: E402
from pymongo import ReplaceOne  # noqa: E402

from config.db import get_db  # noqa: E402
from config.chroma_safety import (  # noqa: E402
    QWEN_DIMENSION,
    QWEN_MODEL,
    get_existing_qwen_collection,
    global_chroma_write_lock,
    validate_qwen_vectors,
)

CHROMA_PATH = os.getenv("CHROMA_PATH", "/data/chroma")
ANNUAL_REPORT_CHROMA_PATH = os.getenv("ANNUAL_REPORT_CHROMA_PATH", CHROMA_PATH)
COLLECTION_FOR = {"annual_reports": "annual_reports",
                  "investor_calls": "investor_calls"}


def path_for_collection(name: str) -> str:
    if name == "annual_reports" and not os.getenv("ANNUAL_REPORT_CHROMA_PATH"):
        raise RuntimeError(
            "ANNUAL_REPORT_CHROMA_PATH is required for annual_reports writeback; "
            "refusing to fall back to the legacy Chroma root"
        )
    return ANNUAL_REPORT_CHROMA_PATH if name == "annual_reports" else CHROMA_PATH


def json_header(path: str, array_key: str) -> dict:
    """Read only the small object prefix before a large JSON array."""
    needle = ('"' + array_key + '"').encode("ascii")
    with open(path, "rb") as fh:
        prefix = fh.read(1 << 20)
    pos = prefix.find(needle)
    if pos < 0:
        raise ValueError(f"JSON array {array_key!r} not found in {path}")
    head = prefix[:pos].decode("utf-8").rstrip()
    if head.endswith(":"):
        head = head[:-1].rstrip()
    if head.endswith(","):
        head = head[:-1]
    return json.loads(head + "}")


def iter_json_array(path: str, array_key: str, chunk_size: int = 1 << 20):
    """Yield array objects without deserializing the complete JSON document."""
    decoder = json.JSONDecoder()
    needle = ('"' + array_key + '"').encode("ascii")
    buffer = ""
    started = False
    done = False
    # 2026-09-18: a raw `block.decode("utf-8")` on each independently-read
    # chunk raises UnicodeDecodeError whenever a multi-byte UTF-8 character
    # (e.g. a rupee sign or other non-ASCII text in a chunk/company name)
    # straddles a chunk_size boundary -- confirmed live, a real production
    # writeback crash exactly at byte offset 1,048,574/1,048,575, one byte
    # before the 1<<20 default chunk_size. An incremental decoder correctly
    # carries any incomplete trailing byte(s) over to the next chunk instead
    # of treating them as a truncated file.
    text_decoder = codecs.getincrementaldecoder("utf-8")()
    with open(path, "rb") as fh:
        while not done:
            block = fh.read(chunk_size)
            if block:
                buffer += text_decoder.decode(block, final=False)
            elif not started:
                raise ValueError(f"JSON array {array_key!r} not found in {path}")
            elif not buffer.strip():
                raise ValueError(f"unterminated JSON array {array_key!r} in {path}")
            else:
                # True EOF: flush the decoder. A genuinely truncated file
                # (a real incomplete multi-byte sequence with no more bytes
                # coming) still raises here, correctly.
                buffer += text_decoder.decode(b"", final=True)

            if not started:
                pos = buffer.find(needle.decode("ascii"))
                if pos < 0:
                    if not block:
                        raise ValueError(f"JSON array {array_key!r} not found in {path}")
                    buffer = buffer[-len(needle):]
                    continue
                pos = buffer.find("[", pos + len(needle))
                if pos < 0:
                    if not block:
                        raise ValueError(f"JSON array {array_key!r} has no '['")
                    continue
                buffer = buffer[pos + 1:]
                started = True

            while True:
                buffer = buffer.lstrip()
                if buffer.startswith("]"):
                    done = True
                    break
                if not buffer:
                    break
                try:
                    item, end = decoder.raw_decode(buffer)
                except json.JSONDecodeError:
                    break
                yield item
                buffer = buffer[end:]
                buffer = buffer.lstrip()
                if buffer.startswith(","):
                    buffer = buffer[1:]
                    continue
                if buffer.startswith("]"):
                    done = True
                break
            if not block and not done:
                raise ValueError(f"unterminated JSON array {array_key!r} in {path}")


def iter_stock_pairs(output_path: str, input_path: str, pair_size: int = 2):
    """Join output vectors to input text in order, yielding at most two stocks."""
    output_rows = iter_json_array(output_path, "results")
    input_rows = iter_json_array(input_path, "chunks")
    pair = []
    pair_filing_ids = []
    try:
        for result in output_rows:
            try:
                chunk = next(input_rows)
            except StopIteration as exc:
                raise ValueError("Kaggle output has more rows than the input batch") from exc
            result_id = f"{result['filing_id']}_{result['chunk_index']}"
            input_id = f"{chunk['filing_id']}_{chunk['chunk_index']}"
            if result_id != input_id:
                raise ValueError(
                    f"Kaggle/input order mismatch at {result_id}; expected {input_id}"
                )
            filing_id = result["filing_id"]
            if filing_id not in pair_filing_ids:
                if len(pair_filing_ids) == pair_size:
                    yield pair
                    pair = []
                    pair_filing_ids = []
                pair_filing_ids.append(filing_id)
            pair.append((result, chunk))
        try:
            next(input_rows)
        except StopIteration:
            pass
        else:
            raise ValueError("input batch has more rows than Kaggle output")
        if pair:
            yield pair
    finally:
        del output_rows, input_rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kaggle-output", required=True)
    ap.add_argument("--input-batch", required=False,
                    help="the export fed to Kaggle; supplies chunk TEXT, which "
                         "the kernel does not echo back")
    ap.add_argument("--confirm", action="store_true")
    args = ap.parse_args()

    doc = json_header(args.kaggle_output, "results")
    print(f"[INFO] kernel output: {doc.get('embedded')}/{doc.get('input_chunks')} "
          f"embedded | dtype={doc.get('dtype')} | "
          f"{doc.get('chunks_per_sec')} chunks/sec | complete={doc.get('complete')}")
    if doc.get("dtype") and doc["dtype"] != "torch.float16":
        print(f"[WARN] kernel ran {doc['dtype']}, not float16 — that is the "
              f"2.66 chunks/sec path; vectors are still valid, throughput was not")
    if doc.get("model") != QWEN_MODEL:
        print(f"[ERROR] output model {doc.get('model')!r} != required {QWEN_MODEL!r}")
        return 1
    if doc.get("requested_dim") != QWEN_DIMENSION:
        print(f"[ERROR] output requested_dim={doc.get('requested_dim')!r} "
              f"!= required {QWEN_DIMENSION}")
        return 1
    if doc.get("complete") is not True or doc.get("embedded") != doc.get("input_chunks"):
        print("[ERROR] embedding output is partial/incomplete — refusing writeback")
        return 1
    if args.confirm and not args.input_batch:
        print("[ERROR] --input-batch is required for confirmed writeback; "
              "vectors without immutable Mongo chunk text are not recoverable")
        return 1

    if args.input_batch:
        print("[INFO] streaming chunk text and vectors in two-stock pairs")
    else:
        print("[WARN] no --input-batch given: chunk_text rows will NOT be written, "
              "so retrieval would find vectors with no recoverable text")

    total_vec = total_txt = 0
    lock_context = (
        global_chroma_write_lock("writeback_embeddings")
        if args.confirm else contextlib.nullcontext()
    )
    with lock_context:
      db = get_db()
      if not args.input_batch:
          raise RuntimeError("confirmed writeback requires --input-batch")
      for pair in iter_stock_pairs(args.kaggle_output, args.input_batch):
        rows = [result for result, _ in pair]
        chunks = [chunk for _, chunk in pair]
        source = rows[0].get("source") or "annual_reports"
        if any((r.get("source") or "annual_reports") != source for r in rows):
            raise ValueError("a two-stock pair contains multiple sources")
        cname = COLLECTION_FOR.get(source)
        if not cname:
            print(f"[WARN] unknown source {source!r}, skipping {len(rows)} row(s)")
            continue
        store_path = path_for_collection(cname)
        client = chromadb.PersistentClient(path=store_path)
        try:
            col = get_existing_qwen_collection(client, cname)
        except Exception as exc:
            print(f"[ERROR] {cname} contract/open failed — refusing write: {exc}")
            client.close()
            return 1
        ids = [f"{r['filing_id']}_{r['chunk_index']}" for r in rows]
        embs = [r["embedding"] for r in rows]
        metas = [{"chunk_index": r["chunk_index"], "symbol": r.get("symbol") or "",
                  "filing_id": r["filing_id"], "doc_type": r.get("doc_type") or "",
                  "page_number": r.get("page_number", 0)} for r in rows]

        try:
            validate_qwen_vectors(embs)
        except ValueError as exc:
            print(f"[ERROR] invalid Qwen vector batch — refusing write: {exc}")
            client.close()
            return 1
        print(f"[INFO] {cname}: {len(rows)} vector(s), dim={QWEN_DIMENSION}, "
              f"model={QWEN_MODEL}, path={store_path}")

        print(f"  {'WRITE' if args.confirm else 'WOULD WRITE'} {len(ids)} vector(s) "
              f"into existing Chroma '{cname}'")
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

        ops = [ReplaceOne(
            {"_id": _id},
            {"_id": _id, "filing_id": r["filing_id"],
             "chunk_index": r["chunk_index"], "text": c["text"]},
            upsert=True)
            for r, c, _id in zip(rows, chunks, ids)]
        print(f"  {'WRITE' if args.confirm else 'WOULD WRITE'} {len(ops)} chunk_text row(s)")
        if args.confirm and ops:
            db["chunk_text"].bulk_write(ops, ordered=False)
            back = db["chunk_text"].count_documents({"_id": {"$in": ids}})
            print(f"    VERIFY: {back}/{len(ops)} chunk_text row(s) readable "
                  f"{'OK' if back == len(ops) else 'MISMATCH — INVESTIGATE'}")
        total_txt += len(ops)

        if args.confirm:
            client.close()
            fids = sorted({r["filing_id"] for r in rows})
            db[source].update_many(
                {"filing_id": {"$in": fids}},
                {"$set": {"embedded": True, "embed_model": doc.get("model")}})
            print(f"  marked {len(fids)} source document(s) embedded=True")
        else:
            client.close()
        del pair, rows, chunks, ids, embs, metas, ops
        gc.collect()
        print("  released current two-stock pair")

    print(f"\n{'WROTE' if args.confirm else 'WOULD WRITE'} {total_vec} vector(s), "
          f"{total_txt} chunk_text row(s)")
    if not args.confirm:
        print("DRY RUN — nothing was written. Re-run with --confirm.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
