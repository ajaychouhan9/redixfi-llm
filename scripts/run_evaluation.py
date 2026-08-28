#!/usr/bin/env python3
"""Run an evaluation phase against a fixture file and write the results plus
a human review sheet.

    # Phase A
    python scripts/run_evaluation.py \
        --fixture fixtures/annual_report_summary.json \
        --model qwen3-14b-awq --backend vllm

    # Harness self-check, no GPU, no network
    python scripts/run_evaluation.py \
        --fixture fixtures/annual_report_summary.json --backend echo

Outputs land in evaluation/<phase>/runs/:
  * <task>__<model>__<run_id>.json  — full machine-readable run
  * <task>__<model>__<run_id>.md    — side-by-side human review sheet

Nothing is written to any production store. Nothing is auto-scored for
quality — the review sheet's scoring tables are deliberately blank.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config.settings import get_settings  # noqa: E402
from app.evaluation import context_check  # noqa: E402
from app.evaluation import fixtures as fixtures_mod  # noqa: E402
from app.evaluation import report as report_mod  # noqa: E402
from app.evaluation.runner import run_evaluation, save_run  # noqa: E402
from app.inference.factory import build_backend  # noqa: E402
from app.models.registry import get_model_spec  # noqa: E402

OUT_DIRS = {
    "annual_report_summary": "evaluation/annual_report/runs",
    "annual_report_summary_legacy": "evaluation/annual_report/runs",
    "concall_summary": "evaluation/concall/runs",
    "red_flag": "evaluation/red_flags/runs",
    "ask_ai": "evaluation/ask_ai/runs",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run an evaluation phase")
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--model", default=None, help="registry name; defaults to LLM_MODEL")
    parser.add_argument("--backend", default=None, choices=["echo", "vllm", "openai"])
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--max-tokens", type=int, default=None)
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out-dir", default=None)
    parser.add_argument("--max-report-cases", type=int, default=25)
    parser.add_argument("--replay-as", default=None,
                        help="which runner interprets the fixture. Defaults to the "
                             "fixture's own task; the annual-report fixture also "
                             "accepts 'annual_report_summary_legacy' for the "
                             "like-for-like replay against the pipeline that "
                             "actually produced its reference.")
    parser.add_argument("--ignore-context-check", action="store_true",
                        help="run even when prompts exceed the model's context window "
                             "(the overflowing requests will fail and be recorded)")
    args = parser.parse_args()

    if args.backend:
        os.environ["LLM_BACKEND"] = args.backend
    settings = get_settings(refresh=True)

    model = args.model or settings.model
    temperature = settings.temperature if args.temperature is None else args.temperature
    max_tokens = settings.max_tokens if args.max_tokens is None else args.max_tokens
    seed = settings.seed if args.seed is None else args.seed

    fixture_set = fixtures_mod.load(args.fixture)
    replay_as = args.replay_as or fixture_set.task
    if replay_as not in fixture_set.replayable_as():
        raise SystemExit(
            f"fixture task '{fixture_set.task}' cannot be replayed as "
            f"'{replay_as}'; allowed: {fixture_set.replayable_as()}")
    backend = build_backend(settings)

    total_cases = len(fixture_set.cases)
    with_reference = len(fixture_set.with_reference())
    print(f"Task            : {fixture_set.task}")
    print(f"Replayed as     : {replay_as}"
          + ("   <- LIKE-FOR-LIKE (matches the reference's own pipeline)"
             if replay_as == "annual_report_summary_legacy" else ""))
    print(f"Fixture         : {args.fixture} ({total_cases} cases, "
          f"{with_reference} with a production reference)")
    print(f"Model / backend : {model} / {settings.backend}")
    print(f"Sampling        : temperature={temperature} max_tokens={max_tokens} seed={seed}\n")

    if with_reference == 0:
        print("WARNING: no case carries a production reference output. This run can "
              "GENERATE output but cannot COMPARE it. Report accordingly.\n")
    if settings.backend == "echo":
        print("WARNING: echo backend — no model is consulted. Harness validation only.\n")

    # Context budget check BEFORE any generation. On Kaggle this is the
    # difference between failing in seconds and failing after the weights
    # have downloaded and the server has started.
    try:
        spec = get_model_spec(model)
    except KeyError:
        spec = None
    cases_to_check = fixture_set.cases[:args.limit] if args.limit else fixture_set.cases
    budget = context_check.check(replay_as, cases_to_check, spec, max_tokens)
    print(context_check.render(budget) + "\n")

    if not budget.get("fits") and not args.ignore_context_check:
        print("ABORTING: every overflowing request would be rejected by the server, "
              "wasting GPU quota for no result.\n"
              "Pick one of the options above, or pass --ignore-context-check to "
              "proceed anyway and record the failures.")
        raise SystemExit(2)

    def progress(index: int, total: int, fixture_id: str) -> None:
        print(f"  [{index}/{total}] {fixture_id}")

    run = run_evaluation(
        backend, fixture_set, model,
        temperature=temperature, max_tokens=max_tokens, seed=seed,
        limit=args.limit, progress=progress, replay_as=replay_as,
    )

    out_dir = args.out_dir or OUT_DIRS.get(replay_as, "evaluation/runs")
    json_path = save_run(run, out_dir)
    md_path = json_path.replace(".json", ".md")
    report_mod.save(run, md_path, max_cases=args.max_report_cases)

    print("\n" + "=" * 72)
    print("SUMMARY (objective signals only — quality is NOT auto-scored)")
    print("=" * 72)
    for key, value in (run.get("summary") or {}).items():
        print(f"  {key:35s} {value}")

    print(f"\nResults      : {json_path}")
    print(f"Review sheet : {md_path}")
    print("\nNext step: a human fills in the review sheet's scoring tables. "
          "No quality claim is valid until that is done.")


if __name__ == "__main__":
    main()
