"""build_review_index.py must never let one model's run silently overwrite
another's — twice found doing exactly that, once for baseline runs and
once for prompt-variant runs sharing a name across models.

Loaded by file path, not by package import: scripts/ has no __init__.py
and is invoked as `python scripts/build_review_index.py`, matching the
convention already used for deployment/kaggle/kaggle_run.py in
test_kaggle_launcher.py.
"""
from __future__ import annotations

import importlib.util
import json
import os

import pytest


def _load_module():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "scripts", "build_review_index.py")
    spec = importlib.util.spec_from_file_location("build_review_index", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def bri():
    return _load_module()


def _run(task, model, run_id, cases=20, variant=None):
    """Minimal run doc — just enough for _latest_runs to key and rank it."""
    doc = {
        "task": task, "model": model, "run_id": run_id, "backend": "vllm",
        "results": [{"ok": True}] * cases,
        "summary": {"cases": cases, "generated_ok": cases},
    }
    if variant:
        doc["variant"] = {"name": variant, "max_attempts": 3,
                          "retry_policy": "production", "description": "d"}
    return doc


def test_two_models_on_the_same_task_both_survive(bri, tmp_path, monkeypatch):
    """The bug: Ministral's run was newer and silently displaced Qwen's row
    under a heading that then read as though it covered the whole category."""
    d = tmp_path / "runs"
    d.mkdir()
    (d / "a.json").write_text(json.dumps(_run("concall_summary", "qwen", "20260829T000000Z")))
    (d / "b.json").write_text(json.dumps(_run("concall_summary", "ministral", "20260829T999999Z")))

    monkeypatch.chdir(tmp_path)
    best, variants = bri._latest_runs(str(d / "*.json"), min_cases=5)
    models = {run.get("model") for _, run in best.values()}
    assert models == {"qwen", "ministral"}, (
        f"one model's run displaced the other's: {models}")


def test_two_models_sharing_a_variant_name_both_survive(bri, tmp_path, monkeypatch):
    """The same bug, found a second time in the variant bucket: two models
    can run the identical named variant (a fairness test), and the variant
    key must include the model or the second overwrites the first."""
    d = tmp_path / "runs"
    d.mkdir()
    (d / "a.json").write_text(json.dumps(
        _run("concall_summary", "qwen", "20260829T210000Z",
             variant="concall_markdown_fairness_v1")))
    (d / "b.json").write_text(json.dumps(
        _run("concall_summary", "ministral", "20260829T220000Z",
             variant="concall_markdown_fairness_v1")))

    monkeypatch.chdir(tmp_path)
    best, variants = bri._latest_runs(str(d / "*.json"), min_cases=5)
    models = {run.get("model") for _, run in variants.values()}
    assert models == {"qwen", "ministral"}, (
        f"one model's variant run displaced the other's: {models}")


def test_newer_run_still_wins_within_the_same_model(bri, tmp_path, monkeypatch):
    """The fix must not stop the index from picking up a genuinely newer
    run of the SAME model — only cross-model overwrites are the bug."""
    d = tmp_path / "runs"
    d.mkdir()
    (d / "a.json").write_text(json.dumps(_run("concall_summary", "qwen", "20260829T000000Z")))
    (d / "b.json").write_text(json.dumps(_run("concall_summary", "qwen", "20260829T999999Z")))

    monkeypatch.chdir(tmp_path)
    best, variants = bri._latest_runs(str(d / "*.json"), min_cases=5)
    assert len(best) == 1
    (_, run), = best.values()
    assert run["run_id"] == "20260829T999999Z"
