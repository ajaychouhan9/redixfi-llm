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

CHECKPOINTING — see app/embed_checkpoint.py (2026-09-04 REWRITTEN)
--------------------------------------------------------------------
The original inline mechanism re-serialized the ENTIRE accumulated
results list on every 200-chunk checkpoint — real, measured O(n^2)
checkpoint I/O on top of O(n) encoding (a real 42,180-chunk batch: 14.7
chunks/sec on the first checkpoint, matching the 12.19 preflight, but a
5.41 chunks/sec CUMULATIVE average by the end as the 868MB output file
got progressively more expensive to rewrite — 131.8 minutes actual vs a
~58-minute pure-encode estimate). Fixed by moving the checkpoint logic
into EmbedCheckpointer (app/embed_checkpoint.py), which appends only NEW
rows to a JSONL file per checkpoint (O(new rows), not O(total so far))
and writes the full writeback-shaped output exactly once, at the true
end. See that module's docstring for the full reasoning, including how
crash survival is preserved.
"""
import glob
import json
import os
import subprocess
import sys
import time

OUT = "/kaggle/working/embed_batch_output.json"
CHECKPOINT_JSONL = "/kaggle/working/embed_batch_checkpoint.jsonl"
CHECKPOINT_META = "/kaggle/working/embed_batch_checkpoint_meta.json"


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

from app.embed_checkpoint import EmbedCheckpointer  # noqa: E402
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
ckpt = EmbedCheckpointer(results, meta, CHECKPOINT_JSONL, CHECKPOINT_META, OUT)

t_start = time.time()
CHECKPOINT_EVERY = 200
try:
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
            ckpt.append()
            el = time.time() - t_start
            log(f"  {len(results)}/{len(chunks)} embedded "
                f"({len(results)/max(el,0.001):.1f} chunks/sec)")

    el = time.time() - t_start
    meta["seconds"] = round(el, 2)
    meta["chunks_per_sec"] = round(len(results) / max(el, 0.001), 2)
    ckpt.append()  # capture any tail since the last 200-boundary
    ckpt.write_final(True)
    log("")
    log(f"DONE: {len(results)}/{len(chunks)} chunks embedded in {el:.1f}s "
        f"({meta['chunks_per_sec']} chunks/sec)")
    log(f"wrote {OUT}")
except Exception:
    # An uncaught exception at the script level (not the per-batch one
    # above, which already continues past individual failures) — still
    # leave a usable OUT behind from whatever is in `results`, same "do
    # not discard GPU time already spent" reasoning as
    # production_generate.py's checkpointing. complete=False, unchanged
    # contract — a caller must already treat complete=False as "check
    # before trusting this as the full batch."
    ckpt.append()
    el = time.time() - t_start
    meta["seconds"] = round(el, 2)
    meta["chunks_per_sec"] = round(len(results) / max(el, 0.001), 2)
    ckpt.write_final(False)
    log(f"*** UNCAUGHT EXCEPTION after {len(results)}/{len(chunks)} embedded — "
        f"wrote partial {OUT} (complete=False) and {CHECKPOINT_JSONL} before re-raising ***")
    raise
