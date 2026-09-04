"""Checkpointing for the embedding kernel — O(1)/O(batch) per checkpoint,
not O(total accumulated so far).

2026-09-04. The original mechanism (inline in run_embed_batch.py) called
`json.dump()` on the ENTIRE accumulated results list on every 200-chunk
checkpoint. Real, measured cost on a 100-document/42,180-chunk batch: the
first checkpoint ran at 14.7 chunks/sec (matching the 12.19 chunks/sec
preflight), but the CUMULATIVE average degraded to 5.41 chunks/sec by the
end, because each of the 211 rewrites got more expensive as the output
file grew toward its final 868MB — O(n^2) checkpoint I/O on top of O(n)
encoding. 131.8 minutes actual vs a ~58-minute pure-encode estimate.

THE FIX: separate "durable, crash-safe checkpoint" from "final,
writeback-shaped output."

  - append() writes ONLY the rows completed since the last checkpoint, as
    JSON Lines (one object per line, opened in append mode). Cost is
    O(new rows), independent of how many rows already exist on disk.
  - A tiny constant-size meta file is rewritten every checkpoint (safe —
    its size never depends on `results`), so progress is visible without
    touching the JSONL at all.
  - write_final() — the one O(n) write of the full, writeback-shaped
    output — is meant to be called exactly ONCE, at the true end of a run
    (success or a caught top-level exception), not per-checkpoint.

CRASH SURVIVAL — the actual reason checkpointing exists, unchanged: every
append() call is a real, already-flushed-to-disk write that happened
DURING the run, before any later crash (including a hard kill that runs
no Python cleanup at all) could happen. If write_final() never runs,
reconstruct() rebuilds the exact same output shape from the JSONL alone —
see reconstruct_embed_checkpoint.py, and this module's own
`reconstruct()` function it wraps.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional


class EmbedCheckpointer:
    """One instance per run. `results` is the SAME list object the caller
    appends new rows to — this class only ever reads from it, at the
    index it has not yet persisted."""

    def __init__(self, results: List[Dict[str, Any]], meta: Dict[str, Any],
                checkpoint_jsonl: str, checkpoint_meta: str, out_path: str):
        self.results = results
        self.meta = meta
        self.checkpoint_jsonl = checkpoint_jsonl
        self.checkpoint_meta = checkpoint_meta
        self.out_path = out_path
        self._last_appended = 0
        # Fresh start each run — a stale checkpoint left over from a PRIOR
        # run would otherwise silently prepend old rows onto a new batch.
        if os.path.exists(self.checkpoint_jsonl):
            os.remove(self.checkpoint_jsonl)

    def append(self) -> int:
        """O(new rows). Returns how many rows were newly appended (0 is a
        legitimate, cheap no-op call)."""
        new_rows = self.results[self._last_appended:]
        if not new_rows:
            return 0
        with open(self.checkpoint_jsonl, "a", encoding="utf-8") as f:
            for row in new_rows:
                f.write(json.dumps(row, ensure_ascii=False))
                f.write("\n")
        self._last_appended = len(self.results)
        with open(self.checkpoint_meta, "w", encoding="utf-8") as f:
            json.dump({**self.meta, "complete": False,
                      "embedded": len(self.results)}, f)
        return len(new_rows)

    def write_final(self, done: bool) -> None:
        """The ONE O(n) write of the full, writeback-shaped output. Call
        exactly once per run — at the true end (done=True) or from a
        caught top-level exception (done=False) — never per-checkpoint."""
        with open(self.out_path, "w", encoding="utf-8") as f:
            json.dump({**self.meta, "complete": done,
                      "embedded": len(self.results),
                      "results": self.results}, f)


def reconstruct(checkpoint_jsonl: str, checkpoint_meta: str) -> Dict[str, Any]:
    """Rebuild the full output SHAPE from the durable checkpoint files
    alone — the recovery path for a run that never reached write_final()
    at all (a hard kill). `complete` is always False here: a
    reconstruction from checkpoints is definitionally a run that did not
    finish on its own."""
    meta = json.load(open(checkpoint_meta, encoding="utf-8"))
    results = []
    if os.path.exists(checkpoint_jsonl):
        with open(checkpoint_jsonl, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    results.append(json.loads(line))
                except json.JSONDecodeError:
                    # A hard kill mid-write can leave the LAST line
                    # truncated (that one write() was interrupted).
                    # Every earlier line is a complete, already-written
                    # JSON object — skip only the trailing partial one.
                    continue
    return {
        "model": meta.get("model"), "dtype": meta.get("dtype"),
        "batch_size": meta.get("batch_size"),
        "requested_dim": meta.get("requested_dim"),
        "input_chunks": meta.get("input_chunks"),
        "seconds": meta.get("seconds"), "chunks_per_sec": meta.get("chunks_per_sec"),
        "complete": False, "embedded": len(results), "results": results,
    }
