#!/usr/bin/env python3
"""Write Qwen's red_flag reclassification back into ChromaDB chunk
metadata — a METADATA-ONLY `collection.update()`, exactly matching
risk_flag_backfill.py's own write mechanism. No re-embedding, no
re-chunking, no touch of the source document text.

2026-09-05 CLEAR-FLAG FIX — ChromaDB `collection.update()` MERGES the
supplied metadata with what is already stored; it does not remove keys
that are omitted. For a reclassification whose Qwen output has no
`risk_flag_type` (the two real ACMESOLAR disagreements on 2026-09-04),
the old write only sent `{"risk_classified": True}`, so a previously
confirmed `risk_flag_type`/`risk_flag_summary` stayed in place and the
chunk remained visible on the user-facing red-flag path despite Qwen
having cleared it. The no-flag branch now writes explicit empty strings
for both keys; empty strings are not in RISK_FLAG_CATEGORIES, so every
reader treats the chunk as unflagged while Chroma's merge keeps the
metadata self-consistent.
"""
import argparse
import json
import os
import sys

REDIXFI_ROOT = os.getenv("REDIXFI_ROOT", "/home/ubuntu/redixfi-backend")
# 2026-09-02: repointed at the new dedicated /data/chroma mount (127GB
# ext4, permanent in /etc/fstab) after the chroma_production wipe -- a
# separate top-level mount, not derived from REDIXFI_ROOT anymore.
CHROMA_PATH = os.getenv("CHROMA_PATH", "/data/chroma")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kaggle-output", required=True)
    ap.add_argument("--confirm", action="store_true")
    args = ap.parse_args()

    doc = json.load(open(args.kaggle_output, encoding="utf-8"))
    print(f"generated_ok: {doc['generated_ok']}/{doc['cases']}  "
         f"model={doc['model']}")

    import chromadb
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Group by source collection (chunks can come from annual_reports or
    # investor_calls), since collection.update() is per-collection.
    by_collection = {}
    for row in doc["results"]:
        cid = row.get("chunk_id")
        by_collection.setdefault(row.get("source_collection", "annual_reports"),
                                 []).append(row)

    written = skipped = 0
    for coll_name, rows in by_collection.items():
        col = client.get_collection(coll_name)
        ids, metas = [], []
        for row in rows:
            cid = row.get("chunk_id")
            if not row.get("ok"):
                print(f"  SKIP {cid}: generation failed ({row.get('error')})")
                skipped += 1
                continue
            out = row.get("output") or {}
            # Chroma update() merges metadata; omitting a key never removes
            # an old value. When Qwen clears a previously-confirmed flag,
            # write explicit empty strings so stale risk_flag_type /
            # risk_flag_summary cannot keep the chunk on user-facing
            # red-flag paths. Empty strings are not in RISK_FLAG_CATEGORIES,
            # so readers treat them as no flag.
            meta = {"risk_classified": True}
            if out.get("risk_flag_type"):
                meta["risk_flag_type"] = out["risk_flag_type"]
                meta["risk_flag_summary"] = out.get("risk_flag_summary") or ""
            else:
                meta["risk_flag_type"] = ""
                meta["risk_flag_summary"] = ""
            print(f"  {'WRITE' if args.confirm else 'WOULD WRITE'} {cid} "
                 f"[{coll_name}] -> {meta.get('risk_flag_type') or 'no flag'}")
            ids.append(cid)
            metas.append(meta)
            written += 1

        if args.confirm and ids:
            col.update(ids=ids, metadatas=metas)
            # VERIFY immediately.
            check = col.get(ids=ids, include=["metadatas"])
            ok = True
            for cid, expected in zip(ids, metas):
                idx = check["ids"].index(cid)
                actual = check["metadatas"][idx] or {}
                for k, v in expected.items():
                    if actual.get(k) != v:
                        ok = False
            print(f"    [{coll_name}] updated {len(ids)} chunks  "
                 f"VERIFY={'OK' if ok else 'MISMATCH — INVESTIGATE'}")
            if not ok:
                sys.exit(1)

    print(f"\n{'WROTE' if args.confirm else 'WOULD WRITE'} {written}, skipped {skipped}")
    if not args.confirm:
        print("DRY RUN — nothing was written. Re-run with --confirm to write.")


if __name__ == "__main__":
    main()
