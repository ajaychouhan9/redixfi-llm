"""Qwen embedding configuration - ONE definition, imported by every load site.

WHY THIS MODULE EXISTS
----------------------
The dtype below is not a style preference; it is a 4.58x throughput
difference, measured in a controlled head-to-head on the real 2xT4
hardware (2026-09-02, preflight v3: same 436 real chunks, same order,
same batch sweep, same session, fresh model load per arm, dtype the only
variable):

    default (torch.bfloat16)   2.66 chunks/sec   OOM at batch 64
    explicit torch.float16    12.19 chunks/sec   no OOM, 6.5GB at batch 32

Loading without an explicit dtype silently gets the SLOW arm. Every load
site must import from here rather than passing its own literal, so a new
call site cannot quietly reintroduce the 2.66/sec path.

THE MISLEADING FLAG - do not "fix" this by checking capability at runtime
-------------------------------------------------------------------------
On this Tesla T4 (sm_75), `torch.cuda.is_bf16_supported()` returns
**True**. It is not usable bf16 in any performance sense - the benchmark
above is the real evidence, and it agrees with this project's own earlier
"no bf16 on 2xT4" finding from the fine-tuning feasibility work. Anyone
gating dtype on that flag will land back on the slow path.

DISPROVEN HYPOTHESIS - recorded so it is not retried
-----------------------------------------------------
Before the dtype cause was found, the suspected culprit was padding waste
from the default 32k max_seq_length (real token lengths: min 211 / p50 490
/ p95 694 / max 1075 / mean 499). Pinning max_seq_length=2048 was tested
as a same-session control and gave **0.9x - no speedup, marginally
slower**. sentence-transformers already sorts by length and pads
efficiently. Do not re-litigate; it is disproven, not untested.
"""
from __future__ import annotations

MODEL_ID = "Qwen/Qwen3-Embedding-0.6B"

#: Output dimensionality. The /data/chroma collections were recreated
#: unpinned and take their dimension from the first real write, so this
#: must stay consistent once the first production embed lands.
EMBED_DIM = 1024

#: MEASURED best (12.19 chunks/sec). Larger batches were slower AND used
#: more VRAM on this hardware - 16 -> 11.37, 32 -> 9.69, 64 -> 8.69 - so
#: this is not a conservative default, it is the fastest measured setting.
EMBED_BATCH_SIZE = 8

#: String form, resolved to a torch dtype by resolve_dtype() so this module
#: stays importable without torch (the VM-side export/writeback scripts
#: have no torch installed; only the Kaggle kernel does).
TORCH_DTYPE = "float16"


def resolve_dtype():
    """torch.float16, imported lazily so VM-side callers need no torch."""
    import torch
    return {"float16": torch.float16, "bfloat16": torch.bfloat16,
            "float32": torch.float32}[TORCH_DTYPE]


def load_embedding_model(device: str = "cuda:0"):
    """THE single supported way to load the embedding model.

    Uses model_kwargs={"torch_dtype": ...} because SentenceTransformer
    forwards it to the underlying transformers load - passing dtype any
    other way is silently ignored and yields the 2.66/sec bf16 path.
    """
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(
        MODEL_ID, device=device,
        model_kwargs={"torch_dtype": resolve_dtype()},
    )
