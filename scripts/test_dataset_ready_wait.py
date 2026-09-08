#!/usr/bin/env python3
"""Regression guard for the 2026-09-08 dataset-ready race.

A kernel launched immediately after push_dataset() died in 18s with
"production_generate.py not found under /kaggle/input": Kaggle processes an
uploaded dataset version asynchronously, and a FIRST-EVER slug has no prior
ready version to serve in the meantime. These tests pin the behavior that
closes it, including the two ways a naive implementation gets it wrong:
treating a brand-new dataset's 403 as fatal, and launching anyway on timeout.
"""
import sys
import time
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_production_batch as rpb


class FakeApi:
    """Returns a scripted sequence of statuses; raisable entries are raised."""

    def __init__(self, sequence):
        self.sequence = list(sequence)
        self.calls = 0

    def dataset_status(self, ref):
        self.calls += 1
        item = self.sequence[min(self.calls - 1, len(self.sequence) - 1)]
        if isinstance(item, Exception):
            raise item
        return item


def http_error(code):
    exc = Exception(f"HTTP {code}")
    exc.status = code
    return exc


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


real_sleep = time.sleep
# Cap, do not null, the poll interval: a no-op sleep turns the timeout test
# into a hot loop that emits ~1M log lines. Capping keeps every test fast
# while still letting `interval` actually pace the loop.
rpb.time = types.SimpleNamespace(
    time=time.time, sleep=lambda s: real_sleep(min(s, 0.001)))

print("dataset-ready wait:")


def test_ready_immediately():
    api = FakeApi(["ready"])
    assert rpb.wait_for_dataset_ready(api, "o/s", timeout=30) == "ready"
    assert api.calls == 1, f"expected 1 status call, got {api.calls}"


check("returns as soon as status is ready", test_ready_immediately)


def test_waits_through_processing():
    api = FakeApi(["processing", "processing", "ready"])
    assert rpb.wait_for_dataset_ready(api, "o/s", timeout=30) == "ready"
    assert api.calls == 3, f"expected 3 status calls, got {api.calls}"


check("polls through 'processing' until ready", test_waits_through_processing)


def test_first_push_403_is_not_fatal():
    # THE reported bug: a brand-new private dataset 403s before it is
    # visible. That must mean "not ready yet", never "give up".
    api = FakeApi([http_error(403), http_error(404), "ready"])
    assert rpb.wait_for_dataset_ready(api, "o/s", timeout=30) == "ready"
    assert api.calls == 3, f"expected 3 status calls, got {api.calls}"


check("treats first-push 403/404 as not-ready, not fatal",
      test_first_push_403_is_not_fatal)


def test_real_http_error_propagates():
    api = FakeApi([http_error(500)])
    try:
        rpb.wait_for_dataset_ready(api, "o/s", timeout=30)
    except Exception as exc:  # noqa: BLE001
        assert getattr(exc, "status", None) == 500, f"wrong error surfaced: {exc}"
        return
    raise AssertionError("a 500 should propagate, not be swallowed as not-ready")


check("propagates non-403/404 API errors", test_real_http_error_propagates)


def test_processing_failure_raises_fast():
    api = FakeApi(["processing", "error"])
    try:
        rpb.wait_for_dataset_ready(api, "o/s", timeout=30)
    except RuntimeError as exc:
        assert "processing failed" in str(exc), str(exc)
        assert api.calls == 2, f"should fail fast, took {api.calls} calls"
        return
    raise AssertionError("status 'error' must raise, not keep polling")


check("fails fast on a real processing failure", test_processing_failure_raises_fast)


def test_timeout_refuses_to_launch():
    # The whole point: never hand a kernel a dataset Kaggle cannot serve.
    api = FakeApi(["processing"])
    try:
        rpb.wait_for_dataset_ready(api, "o/s", timeout=0.05, interval=0.01)
    except RuntimeError as exc:
        assert "did not reach 'ready'" in str(exc), str(exc)
        return
    raise AssertionError("timeout must raise so no kernel is launched")


check("raises on timeout instead of launching anyway", test_timeout_refuses_to_launch)


def test_push_dataset_waits_by_default():
    """push_dataset must wait — the fix has to be on the default path."""
    import inspect
    sig = inspect.signature(rpb.push_dataset)
    assert sig.parameters["wait_ready"].default is True, \
        "wait_ready must default to True or the race stays open"
    src = inspect.getsource(rpb.push_dataset)
    assert "wait_for_dataset_ready" in src, \
        "push_dataset does not call wait_for_dataset_ready"
    # the wait must come AFTER the upload calls, not before
    assert (src.index("wait_for_dataset_ready")
            > src.index("dataset_create_new")), \
        "wait must follow the upload, otherwise it checks the OLD version"


check("push_dataset waits after upload, by default",
      test_push_dataset_waits_by_default)

time.sleep = real_sleep
print()
if failures:
    print(f"FAILED: {len(failures)} check(s): {', '.join(failures)}")
    sys.exit(1)
print("all checks passed")
