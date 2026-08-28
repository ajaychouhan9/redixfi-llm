"""Evaluation runner — fixture in, candidate output + comparison out.

Records the full run configuration alongside the results so any run can be
reproduced or audited later: model, backend, quantization, sampling params,
fixture provenance and this project's git commit.
"""
from __future__ import annotations

import json
import os
import platform
import subprocess
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

from ..inference.base import Backend
from ..models.registry import get_model_spec
from ..tasks import annual_report_summary as task_ar
from ..tasks import annual_report_summary_legacy as task_ar_legacy
from ..tasks import ask_ai as task_ask
from ..tasks import concall_summary as task_cc
from ..tasks import red_flag as task_rf
from . import compare as compare_mod
from .fixtures import FixtureSet

TASK_RUNNERS: Dict[str, Callable] = {
    "annual_report_summary": task_ar.run,
    # The annual-report fixture is DUAL-INPUT and can be replayed two ways:
    # against the current Evidence Finder pipeline (above), or against the
    # legacy front-slice contract that actually produced the stored 2026-08-16
    # reference (below). Only the legacy replay is like-for-like.
    "annual_report_summary_legacy": task_ar_legacy.run,
    "concall_summary": task_cc.run,
    "red_flag": task_rf.run,
    "ask_ai": task_ask.run,
}


def _git_commit() -> str:
    try:
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=root, capture_output=True, text=True, timeout=10,
        )
        return out.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def run_evaluation(
    backend: Backend,
    fixtures: FixtureSet,
    model: str,
    *,
    temperature: float = 0.0,
    max_tokens: int = 1024,
    seed: Optional[int] = 0,
    limit: Optional[int] = None,
    progress: Optional[Callable[[int, int, str], None]] = None,
    replay_as: Optional[str] = None,
) -> Dict[str, Any]:
    """`replay_as` selects which runner interprets the fixture. It defaults
    to the fixture's own task; the annual-report fixture also accepts
    "annual_report_summary_legacy" to replay the pre-Evidence-Finder
    contract its reference was actually produced under."""
    task = replay_as or fixtures.task
    allowed = fixtures.replayable_as()
    if task not in allowed:
        raise ValueError(
            f"fixture task '{fixtures.task}' cannot be replayed as '{task}'; "
            f"allowed: {allowed}")
    runner = TASK_RUNNERS.get(task)
    if runner is None:
        raise ValueError(f"no runner for task '{task}'")

    cases = fixtures.cases[:limit] if limit else fixtures.cases
    rows: List[Dict[str, Any]] = []

    for index, case in enumerate(cases, start=1):
        if progress:
            progress(index, len(cases), str(case.get("benchmark_id") or case.get("fixture_id")))
        result = runner(
            backend, case, model,
            temperature=temperature, max_tokens=max_tokens, seed=seed,
        )
        row = result.to_dict()
        row["comparison"] = compare_mod.compare(task, case, result.output)
        # Keep the reference alongside every row so the output file is
        # self-contained — a reviewer never has to hold two files open, and
        # the reference can never drift away from what it was compared to.
        row["reference"] = case.get("reference")
        row["case_meta"] = {
            k: case.get(k)
            for k in ("benchmark_id", "symbol", "company_name", "fiscal_year",
                      "filing_id", "question", "doc_type", "doc_kind", "chunk_id",
                      "candidates", "case_polarity", "reconstruction_status")
            if k in case
        }
        row["provenance"] = case.get("provenance")
        rows.append(row)

    try:
        spec = get_model_spec(model)
        model_config: Dict[str, Any] = {
            "registry_name": spec.name,
            "hf_repo": spec.hf_repo,
            "quantization": spec.quantization,
            "dtype": spec.dtype,
            "tensor_parallel_size": spec.tensor_parallel_size,
            "max_model_len": spec.max_model_len,
            "is_moe": spec.is_moe,
        }
    except KeyError:
        # A raw model id served directly (e.g. straight from vLLM) is a
        # legitimate case; record it honestly rather than failing the run.
        model_config = {"registry_name": None, "served_model_id": model}

    return {
        "run_id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task": task,
        "fixture_task": fixtures.task,
        "replayed_as": task,
        "model": model,
        "model_config": model_config,
        "backend": getattr(backend, "name", "unknown"),
        "sampling": {"temperature": temperature, "max_tokens": max_tokens, "seed": seed},
        "fixture": {
            "path": fixtures.path,
            "exported_at": fixtures.exported_at,
            "schema_version": fixtures.schema_version,
            "source": fixtures.source,
            "cases_total": len(fixtures.cases),
            "cases_run": len(cases),
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "llm_project_commit": _git_commit(),
        },
        "summary": compare_mod.aggregate(task, rows),
        "results": rows,
    }


def save_run(run: Dict[str, Any], out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    filename = f"{run['task']}__{run['model']}__{run['run_id']}.json"
    path = os.path.join(out_dir, filename)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(run, fh, ensure_ascii=False, indent=2, default=str)
    return path
