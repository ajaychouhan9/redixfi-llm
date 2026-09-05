"""Production review lifecycle with real helpers and controlled Mongo/LLM I/O."""
import copy
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
import os
from pathlib import Path
import sys
import threading

import mongomock
import pytest

ROOT = Path(os.environ["REDIXFI_ROOT"])
sys.path.append(str(ROOT / "api"))
from review_lifecycle import (QUEUE, CLAIMS, allowed, reserve, cancel_selection,
                              complete_result, identity, now, review_lock)
from production.export_generation_batch import select_documents, export, build_case
from production.review_guard import write_summary, write_red_flag

@pytest.fixture
def db():
    return mongomock.MongoClient().redixfi

def seed(db, doc_id="old", state=None, task="annual_report"):
    coll = "annual_reports" if task == "annual_report" else "investor_calls"
    db[coll].insert_one({"filing_id": doc_id, "symbol": "SAME", "raw_text": "source",
        "raw_transcript_text": "transcript", "extraction_status": "OK", "summary": "previous"})
    if state:
        db[QUEUE].insert_one({"_id": identity(task, doc_id), "doc_id": doc_id, "task": task,
            "state": state, "symbol": "SAME", "retry_count": 1, "reason": "original reason",
            "qwen_output": {"summary": "held"}, "review_note": "reviewer note", "created_at": now(), "updated_at": now()})

def result(doc_id="old", token=None, passed=True):
    return {"filing_id": doc_id, "dispatch_token": token, "ok": passed,
        "final_status": "QWEN_PASS" if passed else "HUMAN_REVIEW_REQUIRED",
        "human_review_required": not passed, "output": {"summary": "new"} if passed else {},
        "symbol": "SAME", "rejections": [{"text": {"summary": "attempted"}}],
        "human_review_reason": "new reason", "attempts": 2}

@pytest.mark.parametrize("task", ["annual_report", "concall"])
@pytest.mark.parametrize("state", ["approved", "discarded", "pending", "retry_queued"])
def test_review_states_block_unrelated_pass(db, task, state):
    seed(db, state=state, task=task)
    before = copy.deepcopy(list(db[QUEUE].find()))
    assert write_summary(db, task, result(), {"summary": "unrelated"}, True).startswith("BLOCKED")
    assert list(db[QUEUE].find()) == before
    assert db["annual_reports" if task == "annual_report" else "investor_calls"].find_one()["summary"] == "previous"

def test_retry_selection_fairness_and_same_symbol_new_filing(db):
    for i in range(10):
        seed(db, f"retry{i}", "retry_queued")
        seed(db, f"new{i}")
    seed(db, "resolved", "approved")
    chosen, unavailable = select_documents(db, "annual_report", 8)
    assert not unavailable and len(chosen) == 8
    assert sum(retry for _, retry in chosen) == 2
    assert all(d["filing_id"] != "resolved" for d, _ in chosen)
    assert any(d["filing_id"].startswith("new") for d, _ in chosen)
    with pytest.raises(ValueError):
        select_documents(db, "annual_report", 1)

def test_retry_claim_is_unique_and_does_not_publish(db):
    seed(db, state="retry_queued")
    with ThreadPoolExecutor(max_workers=2) as pool:
        tokens = list(pool.map(lambda _: reserve(db, "annual_report", "old", "batch"), range(2)))
    assert sum(t is not None for t in tokens) == 1
    r = db[QUEUE].find_one()
    assert r["state"] == "retry_queued" and r["retry_count"] == 1
    assert r["review_note"] == "reviewer note" and r["qwen_output"]["summary"] == "held"
    assert db.annual_reports.find_one()["summary"] == "previous"

@pytest.mark.parametrize("task", ["annual_report", "concall"])
def test_retry_pass_and_replay(db, task):
    seed(db, state="retry_queued", task=task)
    token = reserve(db, task, "old", "batch")
    row = result(token=token)
    assert write_summary(db, task, row, {"summary": "new"}, False) == "WOULD PUBLISH"
    assert db[QUEUE].find_one()["state"] == "retry_queued"
    assert write_summary(db, task, row, {"summary": "new"}, True) == "PUBLISHED"
    r = db[QUEUE].find_one()
    assert r["state"] == "approved" and r["resolution_kind"] == "validated_retry"
    assert r["retry_count"] == 1 and r["history"][0]["reason"] == "original reason"
    assert write_summary(db, task, row, {"summary": "overwrite"}, True).startswith("BLOCKED")

def test_retry_failure_preserves_history_returns_pending_no_loop(db):
    seed(db, state="retry_queued")
    token = reserve(db, "annual_report", "old", "batch")
    assert write_summary(db, "annual_report", result(token=token, passed=False), {}, True) == "HELD"
    r = db[QUEUE].find_one()
    assert r["state"] == "pending" and r["retry_count"] == 1
    assert r["history"][0]["review_note"] == "reviewer note"
    assert r["qwen_output"]["summary"] == "attempted" and r["reason"] == "new reason"
    assert db.annual_reports.find_one()["summary"] == "previous"
    assert not select_documents(db, "annual_report", 8)[0]
    # Another explicit human request, rather than a loop, authorizes a new claim.
    db[QUEUE].update_one({"_id": r["_id"]}, {"$set": {"state": "retry_queued"}, "$inc": {"retry_count": 1}})
    assert reserve(db, "annual_report", "old", "batch2") not in (None, token)
    assert db[QUEUE].find_one()["retry_count"] == 2

def test_cancel_fences_late_output(db):
    seed(db, state="retry_queued")
    token = reserve(db, "annual_report", "old", "batch")
    cancel_selection(db, "annual_report", "old", token)
    new_token = reserve(db, "annual_report", "old", "batch2")
    assert new_token and new_token != token
    assert not allowed(db, "annual_report", "old", token)
    assert allowed(db, "annual_report", "old", new_token)

def test_export_inspection_no_mutation_and_active_batch_reused(db, tmp_path):
    seed(db, state="retry_queued")
    seed(db, "new")
    builder = lambda task, d: {"filing_id": d["filing_id"], "symbol": d["symbol"], "input_text": "source"}
    path = tmp_path / "batch.json"
    inspected = export(db, "annual_report", 4, path, False, builder)
    assert len(inspected["cases"]) == 2 and db[CLAIMS].count_documents({}) == 0
    assert not path.exists()
    first = export(db, "annual_report", 4, path, True, builder)
    second = export(db, "annual_report", 4, path, True, builder)
    assert first == second
    assert db[CLAIMS].count_documents({}) == 2

def test_interrupted_publication_replays_same_result_only(db):
    seed(db, state="retry_queued")
    token = reserve(db, "annual_report", "old", "batch")
    row = result(token=token)
    def broken():
        raise RuntimeError("write unavailable")
    with pytest.raises(RuntimeError):
        complete_result(db, "annual_report", "old", row, broken, True)
    assert not reserve(db, "annual_report", "old", "another")
    with pytest.raises(ValueError):
        complete_result(db, "annual_report", "old", {**row, "output": {"summary": "different"}}, lambda: None, True)
    assert write_summary(db, "annual_report", row, {"summary": "new"}, True) == "PUBLISHED"

def test_admin_and_automatic_writer_are_serialized(db):
    seed(db)
    entered = threading.Event()
    finished = threading.Event()
    def writer():
        entered.set()
        action = write_summary(db, "annual_report", result(), {"summary": "bad"}, True)
        finished.set()
        return action
    with ThreadPoolExecutor(max_workers=1) as pool:
        with review_lock(identity("annual_report", "old")):
            future = pool.submit(writer)
            assert entered.wait(2)
            assert not finished.is_set()
            db[QUEUE].insert_one({"_id": identity("annual_report", "old"), "state": "approved"})
        assert future.result(timeout=3).startswith("BLOCKED")

class Chunk:
    def __init__(self):
        self.meta = {"risk_flag_type": "old"}
    def get(self, **kw):
        return {"ids": ["chunk"], "metadatas": [self.meta.copy()]}
    def update(self, ids, metadatas):
        self.meta.update(metadatas[0])

@pytest.mark.parametrize("state", ["approved", "discarded", "pending", "retry_queued"])
def test_red_flag_review_guard(db, state):
    col = Chunk()
    db[QUEUE].insert_one({"_id": "red_flag:annual_reports:chunk", "state": state})
    row = {**result(), "chunk_id": "chunk"}
    assert write_red_flag(db, col, "annual_reports", row, {"risk_flag_type": "new"}, True).startswith("BLOCKED")
    assert col.meta["risk_flag_type"] == "old"
    # Same chunk string in the other collection is a different identity.
    assert write_red_flag(db, col, "investor_calls", row, {"risk_flag_type": ""}, True) == "PUBLISHED"

def test_real_generation_validation_and_editor_then_publication(db):
    from app.tasks import annual_report_summary as ar
    from app.inference.base import GenerationResult
    class Backend:
        def __init__(self, output):
            self.output = output
        def generate(self, request):
            return GenerationResult(text=json.dumps(self.output), model="test", backend="controlled")
    good = {"executive_summary": "The report described management's stated priorities.",
        "key_points": ["Management described capacity work", "The report stated a sourcing programme", "Governance practices were reviewed"],
        "important_risks": [], "key_takeaway": "The report centred on stated operating priorities."}
    seed(db, "new")
    token = reserve(db, "annual_report", "new", "batch")
    case = {"fixture_id": "new", "evidence_text": "Management described capacity work.", "symbol": "SAME"}
    bad = {**good, "executive_summary": "Revenue will expand next year."}
    generated = ar.run(Backend(bad), case, "test", rephrase_backend=Backend(good)).to_dict()
    assert generated["ok"] and generated["final_status"] == "GPT_REPHRASE_PASS"
    from app.tasks.production_identity import attach_identity
    generated = attach_identity(generated, {**case, "filing_id": "new", "dispatch_token": token})
    assert write_summary(db, "annual_report", generated, {"summary": generated["output"]["executive_summary"]}, True) == "PUBLISHED"
    assert db.annual_reports.find_one({"filing_id": "new"})["summary"] == good["executive_summary"]

def test_false_pass_still_holds(db):
    seed(db)
    row = {**result(), "human_review_required": True}
    assert write_summary(db, "annual_report", row, {"summary": "unsafe"}, True) == "HELD"
    assert db.annual_reports.find_one()["summary"] == "previous"

@pytest.mark.parametrize("passed", [True, False])
def test_crash_after_queue_resolution_recovers_receipt(db, monkeypatch, passed):
    seed(db, state="retry_queued")
    token = reserve(db, "annual_report", "old", "batch")
    row = result(token=token, passed=passed)
    update = db[CLAIMS].update_one
    def fail_completion(query, change, **kw):
        if change.get("$set", {}).get("state") == "completed":
            raise RuntimeError("crash after queue transition")
        return update(query, change, **kw)
    monkeypatch.setattr(db[CLAIMS], "update_one", fail_completion)
    with pytest.raises(RuntimeError):
        write_summary(db, "annual_report", row, {"summary": "new"}, True)
    monkeypatch.setattr(db[CLAIMS], "update_one", update)
    action = write_summary(db, "annual_report", row, {"summary": "new"}, True)
    assert action == ("ALREADY PUBLISHED" if passed else "ALREADY HELD")
    assert db[CLAIMS].find_one()["state"] == "completed"

def test_export_claim_interruption_artifact_is_recoverable(db, tmp_path, monkeypatch):
    import production.export_generation_batch as exporter
    seed(db, state="retry_queued")
    original = exporter.reserve
    def crash(*args):
        original(*args)
        raise RuntimeError("crash after reservation")
    monkeypatch.setattr(exporter, "reserve", crash)
    builder = lambda task,d: {"filing_id": d["filing_id"]}
    with pytest.raises(RuntimeError):
        export(db, "annual_report", 2, tmp_path / "batch.json", True, builder)
    monkeypatch.setattr(exporter, "reserve", original)
    batch = export(db, "annual_report", 2, tmp_path / "batch.json", True, builder)
    assert batch["cases"][0]["dispatch_token"] == db[CLAIMS].find_one()["token"]
