"""Export REAL chunk texts (real production docs, real production chunker)
for the Qwen embedding preflight. No API calls, read-only against Mongo."""
import json, sys
sys.path.insert(0, "/home/ubuntu/redixfi-backend")
sys.path.insert(0, "/home/ubuntu/redixfi-backend/data-pipeline")
from config.db import get_db
from annual_report_embedder import chunk_text_blocks, is_table_noise, is_garbled

db = get_db()
out = {"schema": "qwen_embed_preflight_v1", "chunks": []}

def add_chunks(text, token_target, meta, cap):
    paras = [p for p in text.split("\n\n") if p.strip()] or [text]
    raw, _ = chunk_text_blocks(paras, token_target=token_target)
    kept = [(p, o) for p, o in raw if not is_table_noise(p) and not is_garbled(p)]
    n = 0
    for idx, (piece, _off) in enumerate(kept):
        if n >= cap:
            break
        out["chunks"].append({**meta, "chunk_index": idx, "text": piece})
        n += 1
    return n

# Real AR doc (the established ZOTA median doc) - bulk of the throughput sample
ar = db["annual_reports"].find_one({"filing_id": "AR_26026_ZOTA_2023_2024_0609202418626"})
n_ar = add_chunks(ar.get("raw_text", ""), 500,
                  {"source": "annual_reports", "symbol": ar.get("symbol"),
                   "filing_id": ar.get("filing_id"), "doc_type": "annual_report"}, 390)

# Real concall doc - different chunk size (300), so throughput is measured on
# both real chunk shapes rather than one
cc = db["investor_calls"].find_one({"symbol": "SENORES", "raw_transcript_text": {"$exists": True, "$ne": ""}})
n_cc = add_chunks(cc.get("raw_transcript_text", ""), 300,
                  {"source": "investor_calls", "symbol": cc.get("symbol"),
                   "filing_id": str(cc.get("filing_id")), "doc_type": "concall_transcript"}, 200)

# The handful for the Part 1.4 round-trip test: flag them explicitly
for c in out["chunks"][:10]:
    c["roundtrip_sample"] = True

print(f"AR chunks: {n_ar}  concall chunks: {n_cc}  total: {len(out['chunks'])}")
print(f"roundtrip_sample chunks flagged: {sum(1 for c in out['chunks'] if c.get('roundtrip_sample'))}")
lens = [len(c["text"]) for c in out["chunks"]]
print(f"chunk char len: min {min(lens)} max {max(lens)} avg {sum(lens)//len(lens)}")
with open("/home/ubuntu/kaggle_stage_embed_preflight/preflight_chunks.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False)
print("wrote preflight_chunks.json")
