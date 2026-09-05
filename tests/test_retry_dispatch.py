from datetime import datetime, timedelta
from types import SimpleNamespace

import mongomock
import pytest

from production import retry_dispatch as worker
from production.run_retry_dispatch import quota_busy


@pytest.mark.parametrize("reserved,used,allowed,busy", [(1, 0, 30, True), (0, 30, 30, True), (0, 0, 30, False)])
def test_live_quota_response_shape(reserved, used, allowed, busy):
    payload = {"gpuQuota": {name: {"seconds": value, "nanos": 0} for name, value in
                           zip(("timeReserved", "timeUsed", "totalTimeAllowed"), (reserved, used, allowed))}}
    assert quota_busy(payload) is busy


def test_unknown_quota_shape_fails_closed():
    with pytest.raises(ValueError):
        quota_busy({})


@pytest.fixture
def setup(monkeypatch):
    db = mongomock.MongoClient().redixfi
    db.llm_review_queue.insert_one({"task": "annual_report", "state": "retry_queued", "retry_count": 1})
    batch = {"batch_id": "batch1", "task": "annual_report_summary", "cases": [
        {"filing_id": "original", "dispatch_token": "receipt", "is_review_retry": True}]}
    monkeypatch.setattr(worker, "export", lambda *a, **kw: batch)
    calls = []
    adapter = SimpleNamespace(batch_path="unused", account_busy=lambda: False,
        prepare=lambda job: True, launch=lambda job: calls.append("launch"),
        status=lambda job: "running", collect_and_write=lambda job: calls.append("write"))
    return db, adapter, calls, datetime(2026, 9, 5), batch


def test_busy_waits_full_hour_across_ticks_then_launches_once(setup):
    db, adapter, calls, now, _ = setup
    adapter.account_busy = lambda: True
    assert worker.tick(db, "annual_report", adapter, now) == "waiting_gpu"
    adapter.account_busy = lambda: False
    assert worker.tick(db, "annual_report", adapter, now + timedelta(minutes=59)) == "waiting"
    assert worker.tick(db, "annual_report", adapter, now + timedelta(hours=1)) == "running"
    worker.tick(db, "annual_report", adapter, now + timedelta(hours=2))
    assert calls == ["launch"]
    assert db.llm_review_queue.find_one()["retry_count"] == 1


def test_repeated_busy_checks_do_not_generate_or_change_review(setup):
    db, adapter, calls, now, _ = setup
    adapter.account_busy = lambda: True
    original = db.llm_review_queue.find_one()
    for hour in range(12):
        assert worker.tick(db, "annual_report", adapter, now + timedelta(hours=hour)) == "waiting_gpu"
    assert calls == []
    assert db.llm_review_queue.find_one() == original


def test_launch_timeout_reconciles_existing_run_without_repush(setup):
    db, adapter, calls, now, _ = setup
    def uncertain(job):
        calls.append("launch")
        raise TimeoutError()
    adapter.launch = uncertain
    assert worker.tick(db, "annual_report", adapter, now) == "launching"
    assert worker.tick(db, "annual_report", adapter, now + timedelta(hours=1)) == "running"
    assert calls == ["launch"]


def test_unprovable_launch_stops_for_attention(setup):
    db, adapter, calls, now, _ = setup
    adapter.launch = lambda job: (_ for _ in ()).throw(TimeoutError())
    worker.tick(db, "annual_report", adapter, now)
    adapter.status = lambda job: "missing"
    assert worker.tick(db, "annual_report", adapter, now + timedelta(hours=1)) == "attention"
    assert worker.tick(db, "annual_report", adapter, now + timedelta(hours=2)) == "attention"


def test_completion_collects_and_does_not_launch_again_after_validation_failure(setup):
    db, adapter, calls, now, _ = setup
    worker.tick(db, "annual_report", adapter, now)
    adapter.status = lambda job: "complete"
    def fail_review(job):
        calls.append("write")
        db.llm_review_queue.update_one({}, {"$set": {"state": "pending"}})
    adapter.collect_and_write = fail_review
    assert worker.tick(db, "annual_report", adapter, now + timedelta(minutes=1)) == "complete"
    assert worker.tick(db, "annual_report", adapter, now + timedelta(hours=2)) == "idle"
    assert calls == ["launch", "write"]


def test_writeback_failure_retries_collection_only(setup):
    db, adapter, calls, now, _ = setup
    worker.tick(db, "annual_report", adapter, now)
    adapter.status = lambda job: "complete"
    adapter.collect_and_write = lambda job: (_ for _ in ()).throw(ConnectionError())
    assert worker.tick(db, "annual_report", adapter, now + timedelta(minutes=1)) == "running"
    assert calls == ["launch"]


@pytest.mark.parametrize("status", ["error", "cancelled"])
def test_gpu_failure_never_starts_infinite_generation_loop(setup, status):
    db, adapter, calls, now, _ = setup
    worker.tick(db, "annual_report", adapter, now)
    adapter.status = lambda job: status
    assert worker.tick(db, "annual_report", adapter, now + timedelta(minutes=1)) == "attention"
    worker.tick(db, "annual_report", adapter, now + timedelta(hours=2))
    assert calls == ["launch"]


def test_dataset_processing_does_not_launch(setup):
    db, adapter, calls, now, _ = setup
    adapter.prepare = lambda job: False
    assert worker.tick(db, "annual_report", adapter, now) == "waiting_gpu"
    assert calls == []


def test_unavailable_retry_does_not_trigger_endless_normal_batches(setup):
    db, adapter, calls, now, batch = setup
    batch["cases"][0]["is_review_retry"] = False
    assert worker.tick(db, "annual_report", adapter, now) == "no eligible retry source"
    assert db.llm_gpu_dispatch_jobs.count_documents({}) == 0
    assert calls == []


@pytest.mark.parametrize("change", ["partial", "foreign", "duplicate", "wrong_task"])
def test_output_identity_and_completeness_checked_before_write(setup, change):
    _, _, _, _, batch = setup
    output = {"complete": True, "task": batch["task"], "results": list(batch["cases"])}
    worker.verify_output(batch, output)
    if change == "partial":
        output["complete"] = False
    elif change == "foreign":
        output["results"] = [{"filing_id": "another", "dispatch_token": "receipt"}]
    elif change == "duplicate":
        output["results"] *= 2
    else:
        output["task"] = "concall_summary"
    with pytest.raises(ValueError):
        worker.verify_output(batch, output)
