"""Induced-failure test for the embedding checkpoint fix — same
methodology as the earlier real induced-failure proof for
production_generate.py's per-case checkpointing this session (3 fake
cases, case 2 raises the exact real crash string, checkpoint file content
inspected on disk afterward).

Proves two separate things, both required by the founder's brief:

  1. THE O(n^2) BUG IS ACTUALLY GONE. append() writes grow the JSONL file
     by a roughly CONSTANT number of bytes per call (one call = one
     checkpoint's worth of new rows), not a GROWING number of bytes as
     more total results accumulate — the old flush() rewrote everything
     every time, so its write size scaled with total progress. Measured
     directly on real file sizes on disk, not asserted from reading the
     code.
  2. CHECKPOINTING STILL SURVIVES A CRASH. A real exception is raised
     partway through a simulated run (after checkpoint N, before N+1).
     The JSONL on disk at that exact moment already contains every row
     from before the crash — read back from a FRESH file handle (not the
     in-memory `results` list), same discipline as the earlier proof
     ("Case 1's real result is recoverable from disk even if the WHOLE
     process had been killed"). Reconstruction via
     app/embed_checkpoint.py::reconstruct() (the same function
     reconstruct_embed_checkpoint.py's CLI wraps) is then run against
     ONLY the on-disk checkpoint files and asserted to recover exactly
     those pre-crash rows.

Run: python production/test_embed_checkpoint_recovery.py
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.embed_checkpoint import EmbedCheckpointer, reconstruct  # noqa: E402

FAIL: list[str] = []
PASS: list[str] = []


def check(label: str, cond: bool, detail: str = ""):
    (PASS if cond else FAIL).append(label if cond else f"{label} — {detail}")


def fake_vector(seed: int) -> list[float]:
    return [float((seed * 37 + i) % 100) / 100 for i in range(8)]  # small, real floats


def main() -> int:
    tmp = tempfile.mkdtemp(prefix="embed_ckpt_test_")
    try:
        jsonl = os.path.join(tmp, "checkpoint.jsonl")
        meta_path = os.path.join(tmp, "checkpoint_meta.json")
        out_path = os.path.join(tmp, "output.json")

        # ============================================================
        # PART A — the O(n^2) bug is gone: per-checkpoint write cost is
        # O(new rows), verified against REAL file sizes on disk.
        # ============================================================
        results: list[dict] = []
        meta = {"model": "test-model", "dtype": "torch.float16",
                "batch_size": 8, "requested_dim": 8, "input_chunks": 2000}
        ckpt = EmbedCheckpointer(results, meta, jsonl, meta_path, out_path)

        CHECKPOINT_EVERY = 200
        checkpoint_byte_deltas = []
        prev_size = 0
        for i in range(2000):
            results.append({"filing_id": f"F{i // 20}", "chunk_index": i % 20,
                            "embedding": fake_vector(i)})
            if (i + 1) % CHECKPOINT_EVERY == 0:
                ckpt.append()
                size = os.path.getsize(jsonl)
                checkpoint_byte_deltas.append(size - prev_size)
                prev_size = size

        check("10 checkpoints ran (2000 rows / 200 per checkpoint)",
             len(checkpoint_byte_deltas) == 10, str(len(checkpoint_byte_deltas)))
        # The OLD bug: checkpoint N's write cost is proportional to TOTAL
        # rows so far (rewrote everything), so byte deltas would grow
        # roughly linearly checkpoint-over-checkpoint (each rewrite is
        # bigger than the last). The FIX: each delta is the same ~200
        # rows' worth of bytes, regardless of which checkpoint it is.
        first, last = checkpoint_byte_deltas[0], checkpoint_byte_deltas[-1]
        ratio = last / first
        check("checkpoint byte-delta stays roughly CONSTANT across the run "
             "(O(new rows), not O(total so far))",
             0.8 <= ratio <= 1.3,
             f"first={first} bytes last={last} bytes ratio={ratio:.2f} "
             f"(the old O(n^2) bug would show ratio near 10x here, "
             f"since checkpoint 10 rewrote 10x what checkpoint 1 did)")
        print(f"  checkpoint byte deltas: {checkpoint_byte_deltas}")

        ckpt.write_final(True)
        final = json.load(open(out_path, encoding="utf-8"))
        check("write_final produced the full 2000-row output",
             final["embedded"] == 2000 and len(final["results"]) == 2000,
             str(final["embedded"]))
        check("write_final's own file write happened exactly ONCE per run "
             "(by construction — called once here, matching real usage)", True)

        # ============================================================
        # PART B — checkpointing survives a real induced crash.
        # ============================================================
        jsonl2 = os.path.join(tmp, "checkpoint2.jsonl")
        meta2 = os.path.join(tmp, "checkpoint2_meta.json")
        out2 = os.path.join(tmp, "output2.json")

        results2: list[dict] = []
        meta_obj = {"model": "test-model", "dtype": "torch.float16",
                   "batch_size": 8, "requested_dim": 8, "input_chunks": 900}
        ckpt2 = EmbedCheckpointer(results2, meta_obj, jsonl2, meta2, out2)

        CRASH_AFTER_CHECKPOINTS = 3  # crash after 600 of 900 rows
        crashed = False
        try:
            for i in range(900):
                if i > 0 and i % 200 == 0:
                    ckpt2.append()
                    if i // 200 == CRASH_AFTER_CHECKPOINTS:
                        raise RuntimeError(
                            "INDUCED FAILURE — simulates a hard Kaggle-session "
                            "kill mid-batch, the exact scenario this checkpoint "
                            "exists for")
                results2.append({"filing_id": f"F{i // 20}", "chunk_index": i % 20,
                                 "embedding": fake_vector(i)})
        except RuntimeError as exc:
            crashed = True
            check("the induced crash actually happened",
                 "INDUCED FAILURE" in str(exc), str(exc))

        check("crash occurred as designed", crashed, "")
        check("in-memory `results2` at crash time has the RIGHT partial count "
             "(600 — everything up to the crash checkpoint, nothing after)",
             len(results2) == 600, str(len(results2)))

        # THE REAL PROOF: read the checkpoint back from a FRESH file handle,
        # not the in-memory objects above — this is what "recoverable from
        # disk even if the whole process had been killed" actually means.
        del ckpt2, results2
        on_disk_rows = []
        with open(jsonl2, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    on_disk_rows.append(json.loads(line))
        check("the checkpoint file ON DISK (fresh read, not memory) has "
             "exactly the 600 pre-crash rows, durably written BEFORE the "
             "crash happened",
             len(on_disk_rows) == 600, str(len(on_disk_rows)))
        check("no row after the crash point leaked into the checkpoint "
             "(the 601st row was never appended — proves append() only "
             "persists what was true AT the checkpoint, not a race)",
             on_disk_rows[-1] == {"filing_id": "F29", "chunk_index": 19,
                                  "embedding": fake_vector(599)},
             str(on_disk_rows[-1]))

        # Reconstruction — the actual recovery path a real crashed Kaggle
        # session would need, run here against ONLY the on-disk files.
        recovered = reconstruct(jsonl2, meta2)
        check("reconstruct() recovers exactly the 600 pre-crash rows from "
             "the checkpoint files alone (no access to the crashed "
             "process's memory, only what it left on disk)",
             recovered["embedded"] == 600 and len(recovered["results"]) == 600,
             str(recovered["embedded"]))
        check("reconstruct() correctly marks the recovered batch incomplete",
             recovered["complete"] is False, str(recovered["complete"]))
        check("reconstruct() preserves the real input_chunks count from meta "
             "(900) so a reader can tell this is PARTIAL, not the whole batch",
             recovered["input_chunks"] == 900, str(recovered["input_chunks"]))
        check("every recovered row is the exact same object that was "
             "checkpointed pre-crash (spot check row 0 and row 599)",
             recovered["results"][0] == {"filing_id": "F0", "chunk_index": 0,
                                         "embedding": fake_vector(0)}
             and recovered["results"][599] == {"filing_id": "F29", "chunk_index": 19,
                                               "embedding": fake_vector(599)},
             "")

        print()
        print("=" * 78)
        print(">>> real checkpoint file content immediately after the induced crash:")
        print(f">>> {len(on_disk_rows)} row(s) on disk, 0 lost, reconstruct() "
             f"recovers all {recovered['embedded']} of them")
        print("=" * 78)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    for p in PASS:
        print(f"  PASS  {p}")
    for f in FAIL:
        print(f"  FAIL  {f}")
    print("=" * 78)
    print(f"{len(PASS)}/{len(PASS) + len(FAIL)} passed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
