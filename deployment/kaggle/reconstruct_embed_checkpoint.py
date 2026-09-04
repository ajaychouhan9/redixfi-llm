"""Rebuild a full, writeback-compatible embed_batch_output.json from
run_embed_batch.py's incremental checkpoint files alone.

Exists for exactly the case run_embed_batch.py's OUT file cannot cover on
its own: a hard kill (host preemption, OOM-kill, a Kaggle session timeout)
that stops the process before it reaches its normal end or even the
in-Python exception handler. run_embed_batch.py's own OUT is only written
at the true end (success) or from its except block (an in-Python
exception) — neither runs on a hard kill. The checkpoint JSONL is
different: every row in it was durably appended to disk DURING the run,
before any later crash could happen, so it survives a hard kill intact up
to whatever the last checkpoint call completed.

Thin CLI wrapper around app/embed_checkpoint.py::reconstruct() — the same
function production/test_embed_checkpoint_recovery.py exercises directly,
so this script and that test are provably using identical logic, not two
copies that could drift.

Usage (against a downloaded checkpoint pair, e.g. after `kaggle kernels
output` on a run that did not finish cleanly):

    python3 reconstruct_embed_checkpoint.py \
        --checkpoint-jsonl embed_batch_checkpoint.jsonl \
        --checkpoint-meta embed_batch_checkpoint_meta.json \
        --out embed_batch_output.json

Output is byte-for-byte the same SHAPE run_embed_batch.py's own OUT uses,
so production/writeback_embeddings.py consumes it with zero changes.
"""
from __future__ import annotations

import argparse
import json
import os
import sys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint-jsonl", required=True)
    ap.add_argument("--checkpoint-meta", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    # app/ ships alongside this script in the same Kaggle dataset payload
    # as embedding_config.py; when run on the VM (the real usage — a
    # crashed kernel's downloaded output), it's llm-pipeline/app.
    here = os.path.dirname(os.path.abspath(__file__))
    for candidate in (os.path.join(here, ".."), here):
        if os.path.isdir(os.path.join(candidate, "app")):
            sys.path.insert(0, candidate)
            break

    from app.embed_checkpoint import reconstruct

    out = reconstruct(args.checkpoint_jsonl, args.checkpoint_meta)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f)

    print(f"[INFO] reconstructed {out['embedded']} result(s) from "
         f"{args.checkpoint_jsonl} -> {args.out}")
    print(f"[INFO] input_chunks was {out.get('input_chunks')}; this is a "
         f"PARTIAL batch (complete=False) unless embedded == input_chunks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
