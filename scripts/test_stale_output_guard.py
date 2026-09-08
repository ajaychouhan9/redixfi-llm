#!/usr/bin/env python3
"""Regression guard for the 2026-09-08 silent stale-output writeback.

embed_ar staged 96,409 chunks. The kernel mounted the PREVIOUS dataset
version, embedded last night's 37,443 chunks, upserted them idempotently and
reported "WROTE 37443 ... COMPLETE". Nothing errored; the database did not
move. These tests pin the assertion that makes that loud, and — just as
importantly — that it does not fire on legitimate runs.
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import launch_staged_kaggle_batch as L

TMP = Path(tempfile.mkdtemp(prefix="stale_guard_"))
failures = []


def check(name, fn):
    try:
        fn()
        print(f"  PASS  {name}")
    except AssertionError as exc:
        failures.append(name)
        print(f"  FAIL  {name}: {exc}")
    except Exception as exc:  # noqa: BLE001
        failures.append(name)
        print(f"  ERROR {name}: {type(exc).__name__}: {exc}")


def write(name, obj):
    p = TMP / name
    p.write_text(json.dumps(obj), encoding="utf-8")
    return p


def embed_batch(n, name):
    return write(name, {"schema": "qwen_embed_batch_v1", "source": "annual_reports",
                        "chunks": [{"filing_id": f"f{i}", "chunk_index": i,
                                    "text": "x", "symbol": "S"} for i in range(n)]})


def gen_batch(n, name):
    return write(name, {"schema_version": 2, "task": "annual_report_summary",
                        "batch_id": "abc", "cases": [{"filing_id": f"f{i}"} for i in range(n)]})


print("stale-output guard:")


def test_counts_embed_chunks_exactly():
    assert L.staged_unit_count(embed_batch(1234, "c.json"), "embed") == 1234


check("stream-counts embed chunks exactly", test_counts_embed_chunks_exactly)


def test_stream_count_survives_block_boundaries():
    """The key must not be lost when a read splits it in half."""
    p = embed_batch(5000, "big.json")
    real = L.staged_unit_count(p, "embed")
    orig = Path.open

    def tiny_read(self, *a, **kw):  # force many tiny blocks
        fh = orig(self, *a, **kw)
        if "b" in (a[0] if a else kw.get("mode", "")):
            real_read = fh.read
            fh.read = lambda _n=0: real_read(7)
        return fh

    Path.open = tiny_read
    try:
        chopped = L.staged_unit_count(p, "embed")
    finally:
        Path.open = orig
    assert chopped == real == 5000, f"boundary loss: {chopped} vs {real}"


check("stream count survives split reads", test_stream_count_survives_block_boundaries)


def test_the_real_incident_is_rejected():
    """96,409 staged, 37,443 returned, complete=true — must refuse."""
    batch = embed_batch(96409, "staged.json")
    out = write("stale_out.json", {"complete": True, "embedded": 37443,
                                   "input_chunks": 37443})
    try:
        L.assert_complete(out, "embed_ar", batch)
    except RuntimeError as exc:
        assert "STALE OR MISMATCHED" in str(exc), str(exc)
        assert "96409" in str(exc) and "37443" in str(exc), \
            f"error must name both counts: {exc}"
        return
    raise AssertionError("the exact production incident was NOT caught")


check("rejects the real incident (96,409 staged vs 37,443 returned)",
      test_the_real_incident_is_rejected)


def test_matching_embed_output_passes():
    batch = embed_batch(250, "ok.json")
    out = write("ok_out.json", {"complete": True, "embedded": 250, "input_chunks": 250})
    doc = L.assert_complete(out, "embed_ar", batch)
    assert doc["embedded"] == 250


check("passes a matching embed run", test_matching_embed_output_passes)


def test_generate_mismatch_rejected():
    batch = gen_batch(140, "g.json")
    out = write("g_out.json", {"complete": True, "cases": 90,
                               "results": [{} for _ in range(90)]})
    try:
        L.assert_complete(out, "generate_ar_rf", batch)
    except RuntimeError as exc:
        assert "STALE OR MISMATCHED" in str(exc), str(exc)
        return
    raise AssertionError("generation lane mismatch was not caught")


check("rejects a generation lane mismatch", test_generate_mismatch_rejected)


def test_generate_partial_success_still_passes():
    """98 of 140 generated OK is a NORMAL outcome — 140 cases came back.

    The guard must compare cases PROCESSED, not cases that succeeded, or it
    would block every batch that legitimately holds some cases for review.
    """
    batch = gen_batch(140, "g2.json")
    out = write("g2_out.json", {"complete": True, "cases": 140, "generated_ok": 98,
                                "results": [{} for _ in range(140)]})
    doc = L.assert_complete(out, "generate_ar_rf", batch)
    assert doc["generated_ok"] == 98


check("does NOT fire on a partial-success generation batch",
      test_generate_partial_success_still_passes)


def test_incomplete_still_rejected():
    batch = embed_batch(10, "i.json")
    out = write("i_out.json", {"complete": False, "input_chunks": 10})
    try:
        L.assert_complete(out, "embed_ar", batch)
    except RuntimeError as exc:
        assert "not complete" in str(exc), str(exc)
        return
    raise AssertionError("complete=false must still be rejected")


check("still rejects complete=false", test_incomplete_still_rejected)


def test_missing_batch_does_not_block():
    """No batch to compare against must not break a valid run."""
    out = write("nb_out.json", {"complete": True, "input_chunks": 5})
    assert L.assert_complete(out, "embed_ar", TMP / "does_not_exist.json")
    assert L.assert_complete(out, "embed_ar", None)


check("absent batch file does not block writeback", test_missing_batch_does_not_block)


def test_guard_runs_before_writeback():
    """Order matters: validating after writing back would be useless."""
    import inspect
    src = inspect.getsource(L.main)
    assert src.index("assert_complete") < src.index("writeback("), \
        "assert_complete must run BEFORE writeback"
    assert "assert_complete(output, args.phase, batch_path)" in src, \
        "assert_complete must receive the staged batch, or it cannot compare"


check("guard runs before writeback, with the batch", test_guard_runs_before_writeback)

print()
if failures:
    print(f"FAILED: {len(failures)} check(s): {', '.join(failures)}")
    sys.exit(1)
print("all checks passed")
