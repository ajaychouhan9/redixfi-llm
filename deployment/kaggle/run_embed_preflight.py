"""QWEN EMBEDDING PREFLIGHT - measures what Part 4's scheduling estimates depend on.

Answers, with real numbers on real 2xT4 hardware:
  1. Real VRAM footprint of Qwen3-Embedding-0.6B (per GPU, before/after load)
  2. Real embedding throughput (chunks/sec) on REAL production chunks
  3. Real output dimensionality (must be 1024 to match the recreated
     /data/chroma collections)
  4. Real vectors for 10 real chunks, emitted to JSON so the Part 1.4
     retrieval round-trip can run on the VM WITHOUT a second GPU launch
     (Kaggle cannot reach the VM's /data/chroma, so writeback must happen
     on the VM side afterward).

DELIBERATELY NOT co-loading the Qwen3-14B generation model. In this
architecture each Kaggle kernel runs ONE workload - embedding will run as
its own kernel, never concurrent with generation - so co-loading would
answer a question production does not pose, while burning ~3min of GPU and
risking an OOM that kills this run before the throughput number lands.
Per-GPU free VRAM is reported precisely instead, so the "would they fit
together" question is answerable arithmetically against the generation
workload's already-measured 5.77 GiB/GPU.
"""
import glob
import json
import os
import subprocess
import sys
import time

MODEL_ID = "Qwen/Qwen3-Embedding-0.6B"
OUT = "/kaggle/working/qwen_embed_preflight_result.json"
R = {"model": MODEL_ID, "steps": [], "ok": False}


def log(msg):
    print(msg, flush=True)


def gpu_mem():
    """Real per-GPU memory via nvidia-smi (MiB used/total)."""
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=index,memory.used,memory.total,name",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=30).stdout.strip()
        gpus = []
        for line in out.splitlines():
            i, used, total, name = [x.strip() for x in line.split(",")]
            gpus.append({"index": int(i), "used_MiB": int(used),
                         "total_MiB": int(total), "name": name})
        return gpus
    except Exception as e:
        return [{"error": str(e)}]


log("=" * 70)
log("STEP 1 - hardware + VRAM BEFORE any model load")
log("=" * 70)
before = gpu_mem()
for g in before:
    log(f"  GPU{g.get('index')}: {g.get('name')} "
        f"{g.get('used_MiB')}/{g.get('total_MiB')} MiB used")
R["gpus_before"] = before
R["gpu_count"] = len([g for g in before if "index" in g])
log(f"  GPU count: {R['gpu_count']}")

log("")
log("=" * 70)
log("STEP 2 - install sentence-transformers (Qwen3-Embedding documented path)")
log("=" * 70)
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--no-cache-dir",
                "sentence-transformers"], check=False)

import torch  # noqa: E402

log(f"  torch {torch.__version__} | cuda available: {torch.cuda.is_available()} "
    f"| device count: {torch.cuda.device_count()}")

log("")
log("=" * 70)
log("STEP 3 - load the model, measure REAL VRAM cost")
log("=" * 70)
from sentence_transformers import SentenceTransformer  # noqa: E402

# 2026-09-02: dtype is explicit and comes from app/embedding_config.py.
# Loading without it silently gets bf16 on this T4 = 2.66 chunks/sec vs
# 12.19 with fp16 (4.58x), measured head-to-head. See that module.
t0 = time.time()
model = SentenceTransformer(
    MODEL_ID, device="cuda:0",
    model_kwargs={"torch_dtype": torch.float16},
)
load_sec = time.time() - t0
after_load = gpu_mem()
log(f"  loaded in {load_sec:.1f}s")
for g in after_load:
    log(f"  GPU{g.get('index')}: {g.get('used_MiB')}/{g.get('total_MiB')} MiB used")
R["load_seconds"] = round(load_sec, 1)
R["gpus_after_load"] = after_load
try:
    d0b = next(g for g in before if g.get("index") == 0)
    d0a = next(g for g in after_load if g.get("index") == 0)
    R["model_vram_MiB_gpu0"] = d0a["used_MiB"] - d0b["used_MiB"]
    R["free_after_load_MiB_gpu0"] = d0a["total_MiB"] - d0a["used_MiB"]
    log(f"  => model VRAM on GPU0: {R['model_vram_MiB_gpu0']} MiB")
    log(f"  => free remaining on GPU0: {R['free_after_load_MiB_gpu0']} MiB")
except Exception as e:
    log(f"  (vram delta calc failed: {e})")

log("")
log("=" * 70)
log("STEP 4 - confirm output dimensionality (MUST be 1024)")
log("=" * 70)
probe = model.encode(["dimension probe"], convert_to_numpy=True)
dim = int(probe.shape[1])
R["output_dim"] = dim
R["dim_matches_chroma_1024"] = (dim == 1024)
log(f"  output dim: {dim}")
log(f"  matches recreated /data/chroma collections (1024): {R['dim_matches_chroma_1024']}")
if dim != 1024:
    log("  *** MISMATCH - do NOT proceed to a real embed; collections expect 1024 ***")

log("")
log("=" * 70)
log("STEP 5 - REAL throughput on REAL production chunks")
log("=" * 70)
hits = glob.glob("/kaggle/input/**/preflight_chunks.json", recursive=True)
assert hits, "preflight_chunks.json not found under /kaggle/input"
data = json.load(open(hits[0], encoding="utf-8"))
chunks = data["chunks"]
texts = [c["text"] for c in chunks]
n_ar = sum(1 for c in chunks if c["source"] == "annual_reports")
n_cc = sum(1 for c in chunks if c["source"] == "investor_calls")
log(f"  loaded {len(texts)} REAL chunks (AR: {n_ar}, concall: {n_cc})")
log(f"  avg chars/chunk: {sum(len(t) for t in texts) // len(texts)}")

# warm-up so the first batch's lazy CUDA init is not charged to the measurement
model.encode(texts[:8], batch_size=8, convert_to_numpy=True)

R["throughput"] = []
# batch 8 is the MEASURED best (12.19/sec); kept as a sweep here
# because this is the preflight whose job is to measure.
for bs in (8, 16, 32, 64):
    t0 = time.time()
    vecs = model.encode(texts, batch_size=bs, convert_to_numpy=True,
                        show_progress_bar=False)
    el = time.time() - t0
    cps = len(texts) / el
    peak = gpu_mem()
    row = {"batch_size": bs, "chunks": len(texts), "seconds": round(el, 2),
           "chunks_per_sec": round(cps, 1),
           "gpu0_used_MiB": next((g["used_MiB"] for g in peak
                                  if g.get("index") == 0), None)}
    R["throughput"].append(row)
    log(f"  batch_size={bs:3d}: {el:6.2f}s for {len(texts)} chunks "
        f"=> {cps:7.1f} chunks/sec  (GPU0 {row['gpu0_used_MiB']} MiB)")

best = max(R["throughput"], key=lambda r: r["chunks_per_sec"])
R["best_chunks_per_sec"] = best["chunks_per_sec"]
R["best_batch_size"] = best["batch_size"]
log(f"  BEST: {best['chunks_per_sec']} chunks/sec at batch_size={best['batch_size']}")

# Real corpus projection using the real measured chunk counts already in the doc
AR_DOCS, AR_CHUNKS_PER_DOC = 8423, 390
CC_DOCS, CC_CHUNKS_PER_DOC = 12907, 31.6
total_chunks = AR_DOCS * AR_CHUNKS_PER_DOC + int(CC_DOCS * CC_CHUNKS_PER_DOC)
hours = total_chunks / best["chunks_per_sec"] / 3600
R["projection"] = {
    "total_corpus_chunks": total_chunks,
    "full_backfill_gpu_hours": round(hours, 2),
    "ar_only_newest_year_gpu_hours": round(
        1972 * AR_CHUNKS_PER_DOC / best["chunks_per_sec"] / 3600, 2),
}
log(f"  => FULL corpus ({total_chunks:,} chunks): {hours:.2f} GPU-hours")
log(f"  => AR newest-year-only (1,972 docs): "
    f"{R['projection']['ar_only_newest_year_gpu_hours']:.2f} GPU-hours")

log("")
log("=" * 70)
log("STEP 6 - real vectors for 10 real chunks (Part 1.4 round-trip seed)")
log("=" * 70)
rt = [c for c in chunks if c.get("roundtrip_sample")]
rt_vecs = model.encode([c["text"] for c in rt], convert_to_numpy=True)
R["roundtrip"] = [
    {"filing_id": c["filing_id"], "chunk_index": c["chunk_index"],
     "symbol": c["symbol"], "doc_type": c["doc_type"], "source": c["source"],
     "text": c["text"], "embedding": [float(x) for x in v]}
    for c, v in zip(rt, rt_vecs)
]
log(f"  emitted {len(R['roundtrip'])} real chunk+vector pairs for VM-side writeback")
log("  (Kaggle cannot reach the VM /data/chroma - the round-trip completes")
log("   on the VM from this output, with no second GPU launch needed)")

R["ok"] = True
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(R, f)
log("")
log(f"wrote {OUT}")
log("PREFLIGHT COMPLETE")
