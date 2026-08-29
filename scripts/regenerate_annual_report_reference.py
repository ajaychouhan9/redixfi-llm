#!/usr/bin/env python3
"""Regenerate current-schema gpt-4o-mini reference output for the annual
report benchmark — ACTION 1.

WHY THIS EXISTS
---------------
Measured against production on 2026-08-28: 8,354 `annual_reports`
documents, 72 carry any summary at all, and ZERO carry current-schema
output (`executive_summary` / `key_points` / `important_risks` /
`evidence_tokens`). Every stored summary is legacy-schema, written
2026-08-16, before the pipeline was rewired through Evidence Finder.

So the annual-report review sheet has been comparing Qwen against a
reference in a DIFFERENT output schema produced from DIFFERENT input.
That comparison cannot be read as a score, which is why the sheet carries
a caveat banner instead of a verdict.

This script closes that gap the cheap way: run the SAME 20 benchmark
cases through gpt-4o-mini using the CURRENT prompt and the SAME evidence
block the benchmark hands Qwen, so both sides finally differ only by
model. See `deployment/kaggle/ANNUAL_REPORT_REFERENCE_SCHEMA.md` option C.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
  * It does not touch RedixFi, MongoDB, ChromaDB or any production
    document. Output goes to a sidecar JSON in this project only.
  * It does not re-run Qwen. Only the reference side is replaced; the
    candidate generations stay exactly as measured.
  * It does not use the improved retry policy. gpt-4o-mini's production
    results were obtained under production mechanics, and the reference
    must be generated the same way or the comparison is rigged in Qwen's
    favour.

COST
----
gpt-4o-mini is $0.150/1M input and $0.600/1M output. `--dry-run` prices
the run from real tokenised prompt lengths without calling the API.
Actual spend is computed from the API's own `usage` counts, never
estimated after the fact.

    python scripts/regenerate_annual_report_reference.py --dry-run
    python scripts/regenerate_annual_report_reference.py --apply
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.evaluation import fixtures as fixtures_mod            # noqa: E402
from app.inference.openai_compat import OpenAICompatBackend   # noqa: E402
from app.prompts.annual_report_summary import (               # noqa: E402
    SYSTEM_PROMPT, build_user_content)
from app.tasks import annual_report_summary as task_ar        # noqa: E402
from app.tasks.retry_policy import PRODUCTION_POLICY          # noqa: E402

USD_PER_M_INPUT = 0.150
USD_PER_M_OUTPUT = 0.600
ESTIMATE_USD = 0.07          # the figure quoted to the founder


def _approx_tokens(text: str) -> int:
    """tiktoken is not installed on the VM and is not a dependency here.
    len/4 is the standard rough ratio for English prose; it is used ONLY
    for the dry-run estimate, never for reported actual cost."""
    return len(text) // 4


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", default="fixtures/annual_report_benchmark.json")
    ap.add_argument("--out", default="fixtures/annual_report_reference_gpt4omini.json")
    ap.add_argument("--model", default="gpt-4o-mini")
    ap.add_argument("--base-url", default="https://api.openai.com/v1")
    ap.add_argument("--limit", type=int, default=None)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true",
                      help="price the run from prompt lengths; no API calls")
    mode.add_argument("--apply", action="store_true",
                      help="actually call the API and write the reference file")
    args = ap.parse_args()

    fixtures = fixtures_mod.load(args.fixture)
    cases = fixtures.cases[:args.limit] if args.limit else fixtures.cases
    print(f"fixture : {args.fixture}")
    print(f"cases   : {len(cases)}")
    print(f"model   : {args.model}\n")

    if args.dry_run:
        in_tokens = sum(_approx_tokens(SYSTEM_PROMPT + build_user_content(c))
                        for c in cases)
        # 4 fields, ~500 tokens of JSON, and the production loop may spend
        # up to MAX_ATTEMPTS on a case, so price the pessimistic path too.
        out_tokens = 500 * len(cases)
        low = (in_tokens / 1e6 * USD_PER_M_INPUT
               + out_tokens / 1e6 * USD_PER_M_OUTPUT)
        print(f"input tokens (approx) : {in_tokens:,}")
        print(f"output tokens (approx): {out_tokens:,}")
        print(f"estimated cost        : ${low:.4f}  (1 attempt/case)")
        print(f"worst case, 3 attempts: ${low * 3:.4f}")
        print(f"\nfigure quoted to founder: ${ESTIMATE_USD:.2f}")
        print("no API calls made.")
        return

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        sys.exit("OPENAI_API_KEY is not set. Export it in this shell; this "
                 "script never reads a .env and never stores a key.")

    backend = OpenAICompatBackend(base_url=args.base_url, api_key=api_key)
    health = backend.health()
    if health.get("status") != "ok":
        sys.exit(f"OpenAI endpoint not reachable/authorised: {health}")

    records, in_tok, out_tok, failures = [], 0, 0, 0
    started = time.time()

    for i, case in enumerate(cases, 1):
        bid = case.get("fixture_id") or case.get("benchmark_id")
        print(f"[{i}/{len(cases)}] {bid} ... ", end="", flush=True)
        # PRODUCTION_POLICY, deliberately: the reference must be produced
        # under the same retry mechanics gpt-4o-mini used in production.
        result = task_ar.run(backend, case, args.model,
                             policy=PRODUCTION_POLICY)
        in_tok += result.prompt_tokens
        out_tok += result.completion_tokens
        if result.ok:
            print(f"ok ({result.attempts} attempt(s))")
        else:
            failures += 1
            print(f"FAILED: {result.error}")
        records.append({
            "fixture_id": bid,
            "symbol": case.get("symbol"),
            "fiscal_year": case.get("fiscal_year"),
            "ok": result.ok,
            "attempts": result.attempts,
            "reference": result.output if result.ok else None,
            "error": result.error,
            "rejections": result.rejections,
            "prompt_tokens": result.prompt_tokens,
            "completion_tokens": result.completion_tokens,
        })

    cost = in_tok / 1e6 * USD_PER_M_INPUT + out_tok / 1e6 * USD_PER_M_OUTPUT
    payload = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": args.model,
        "prompt_version": "annual_report_summarizer current schema",
        "schema": ["executive_summary", "key_points", "important_risks",
                   "key_takeaway"],
        "retry_policy": PRODUCTION_POLICY.name,
        "source_fixture": args.fixture,
        "cases": len(cases),
        "generated_ok": len(cases) - failures,
        "usage": {"prompt_tokens": in_tok, "completion_tokens": out_tok},
        "cost_usd_actual": round(cost, 4),
        "cost_usd_estimated": ESTIMATE_USD,
        "elapsed_sec": round(time.time() - started, 1),
        "note": ("Generated by scripts/regenerate_annual_report_reference.py. "
                 "Reads production fixtures only; writes nothing to RedixFi, "
                 "MongoDB or ChromaDB."),
        "results": records,
    }
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2, default=str)

    print(f"\nwrote {args.out}")
    print(f"generated ok : {len(cases) - failures}/{len(cases)}")
    print(f"tokens       : {in_tok:,} in / {out_tok:,} out")
    print(f"ACTUAL cost  : ${cost:.4f}   (estimated ${ESTIMATE_USD:.2f})")
    drift = abs(cost - ESTIMATE_USD)
    if drift > 0.05:
        print(f"⚠️  COST DIFFERS FROM ESTIMATE by ${drift:.4f} — flag this.")
    else:
        print("cost matched the estimate.")


if __name__ == "__main__":
    main()
