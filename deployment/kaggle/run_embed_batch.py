"""PRODUCTION Qwen embedding kernel — embeds a real batch of real chunks.

Input:  an export from production/export_embed_batch.py (real chunk texts
        + their filing_id/chunk_index/metadata, exported read-only from
        Mongo on the VM).
Output: one JSON with a real 1024-dim vector per chunk, downloaded back to
        the VM and applied by production/writeback_embeddings.py.

WHY THE ROUND TRIP LOOKS LIKE THIS
----------------------------------
Kaggle cannot reach the VM: Mongo is loopback-bound there and /data/chroma
is a local mount. So the kernel never touches a database — it takes text
in and hands vectors back, exactly like the existing generation kernels
(deployment/kaggle/production_generate.py) hand summaries back.

DTYPE IS LOAD-BEARING — see app/embedding_config.py
----------------------------------------------------
This kernel loads via load_embedding_model(), which pins torch.float16.
Loading without an explicit dtype silently runs bf16 on the T4 at
2.66 chunks/sec instead of 12.19 (4.58x slower, measured head-to-head on
this exact hardware). Do not "simplify" the load call.

Per-case checkpointing, same reasoning as production_generate.py: each
batch's vectors are written to the output file as they complete, so one
failure late in a long run cannot discard the GPU time already spent.
"""
import glob
import json
import os
import subprocess
import sys
import time

OUT = "/kaggle/working/embed_batch_output.json"


def log(msg):
    print(msg, flush=True)


log("installing sentence-transformers...")
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--no-cache-dir",
                "sentence-transformers"], check=False)

# The project module ships in the attached dataset, same staleness-guard
# pattern production_generate.py uses.
hits = glob.glob("/kaggle/input/**/app/embedding_config.py", recursive=True)
assert hits, "app/embedding_config.py not found under /kaggle/input"
project_root = hits[0].split("/app/")[0]
sys.path.insert(0, project_root)
log(f"project root: {project_root}")

from app.embedding_config import (  # noqa: E402
    EMBED_BATCH_SIZE, EMBED_DIM, MODEL_ID, TORCH_DTYPE, load_embedding_model,
)

log(f"config: model={MODEL_ID} dtype={TORCH_DTYPE} batch={EMBED_BATCH_SIZE} dim={EMBED_DIM}")

in_hits = glob.glob("/kaggle/input/**/embed_batch_input.json", recursive=True)
assert in_hits, "embed_batch_input.json not found under /kaggle/input"
payload = json.load(open(in_hits[0], encoding="utf-8"))
chunks = payload["chunks"]
log(f"loaded {len(chunks)} real chunks to embed")

t0 = time.time()
model = load_embedding_model(device="cuda:0")
log(f"model loaded in {time.time() - t0:.1f}s")

# Assert the dtype that actually ended up on the parameters, not the one we
# asked for — the preflight showed a requested dtype can differ from what
# is really in use, and that difference is the whole 4.58x.
real_dtype = str(next(model.parameters()).dtype)
log(f"REAL dtype in use: {real_dtype}")
if real_dtype != "torch.float16":
    log(f"*** WARNING: expected torch.float16, got {real_dtype} — "
        f"this is the 2.66 chunks/sec path, not 12.19 ***")

results = []
meta = {"model": MODEL_ID, "dtype": real_dtype, "batch_size": EMBED_BATCH_SIZE,
        "requested_dim": EMBED_DIM, "input_chunks": len(chunks)}


def flush(done):
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({**meta, "complete": done, "embedded": len(results),
                   "results": results}, f)


t_start = time.time()
CHECKPOINT_EVERY = 200
for i in range(0, len(chunks), EMBED_BATCH_SIZE):
    batch = chunks[i:i + EMBED_BATCH_SIZE]
    try:
        vecs = model.encode([c["text"] for c in batch],
                            batch_size=EMBED_BATCH_SIZE,
                            convert_to_numpy=True, show_progress_bar=False)
    except Exception as e:
        log(f"  batch at offset {i} FAILED: {type(e).__name__}: {e}")
        continue
    for c, v in zip(batch, vecs):
        if len(v) != EMBED_DIM:
            log(f"  *** dim mismatch: got {len(v)}, expected {EMBED_DIM} — "
                f"chunk {c.get('filing_id')}_{c.get('chunk_index')} skipped ***")
            continue
        results.append({
            "filing_id": c["filing_id"], "chunk_index": c["chunk_index"],
            "symbol": c.get("symbol"), "doc_type": c.get("doc_type"),
            "source": c.get("source"), "page_number": c.get("page_number", 0),
            "embedding": [float(x) for x in v],
        })
    if len(results) % CHECKPOINT_EVERY < EMBED_BATCH_SIZE:
        flush(False)
        el = time.time() - t_start
        log(f"  {len(results)}/{len(chunks)} embedded "
            f"({len(results)/max(el,0.001):.1f} chunks/sec)")

el = time.time() - t_start
meta["seconds"] = round(el, 2)
meta["chunks_per_sec"] = round(len(results) / max(el, 0.001), 2)
flush(True)
log("")
log(f"DONE: {len(results)}/{len(chunks)} chunks embedded in {el:.1f}s "
    f"({meta['chunks_per_sec']} chunks/sec)")
log(f"wrote {OUT}")
