# RedixFi self-hosted LLM — evaluation project

> **EXPERIMENTAL / NOT PRODUCTION.**
> Nothing in RedixFi points at this service. No quality claim has been made
> or validated. The purpose of this project is to find out whether a
> self-hosted model can reproduce RedixFi's LLM workloads well enough to
> eventually replace selected OpenAI calls — **quality first, cost after.**

## What this is

A standalone service and evaluation harness that reproduces three RedixFi
LLM workloads exactly, runs them on a self-hosted model, and puts the output
side by side with RedixFi's existing production output for human review.

```
RedixFi (untouched)                    This project (C:\LLM)
──────────────────────                 ─────────────────────────────
Mongo `annual_reports`  ──┐
ChromaDB chunks         ──┼─ export ─> fixtures/*.json ─┐
Mongo `ask_log`         ──┘  (read-only, on the VM)     │
                                                        v
                                        OpenAI-compatible API ──> vLLM ──> Kaggle T4 x2
                                                        │
                                                        v
                                     evaluation/*/runs/*.md (human review sheet)
```

## The three phases

| Phase | RedixFi workload reproduced | Where the LLM call lives in RedixFi |
|---|---|---|
| **A** Annual Report Summary | `annual_report_summarizer.py::generate_summary` | Stage 3, weekly cron |
| **B** Red Flag classification | `risk_flag_classifier.py::classify_chunk` | Ingestion time, per candidate chunk |
| **C** Ask AI | `core/ask.py::generate_answer` | Live, per user question |

**Phase B note that is easy to get wrong:** RedixFi's Red Flag *query* path
(`core/red_flag_ask.py`) makes **zero** LLM calls — it assembles metadata
that was generated at ingestion. The LLM workload is the per-chunk
confirm-and-summarize call, and that is what this project evaluates.

## Architectural rules this project obeys

1. **RedixFi is not modified.** The only permitted change is the
   documentation section appended to `api/docs/00_MASTER_CONTEXT.md`.
2. **No RedixFi code is imported at runtime.** Prompts and validators are
   vendored with provenance headers — see [`app/prompts/PROVENANCE.md`](app/prompts/PROVENANCE.md).
   `tests/test_prompts_match_redixfi.py` fails if they drift.
3. **Evidence selection is never reinvented.** The export script calls
   RedixFi's real `evidence_finder.py` and `matched_categories()` and
   records their output. This project consumes evidence; it never competes
   with the pipeline that produces it.
4. **Retrieval and fusion are not reproduced.** Ask AI fixtures carry the
   fact packet exactly as production assembled it, so the evaluation tests
   the model and nothing else.
5. **Read-only against production.** The export script issues only reads.
   Nothing writes back to `redixfi` or `redixfi_app`.
6. **No false network architecture.** RedixFi's Mongo is loopback-bound and
   its ChromaDB is a `PersistentClient` over a directory — hence
   `CHROMA_PATH` and deliberately no `CHROMA_HOST`/`CHROMA_PORT`.
7. **No LLM judge as final authority.** The harness computes objective
   signals only and emits a review sheet with blank scoring tables.

## Quick start (no GPU, no network, no database)

```bash
pip install -r requirements-dev.txt
python scripts/make_sample_fixtures.py        # synthetic, clearly labelled
python scripts/run_evaluation.py --fixture fixtures/sample_ask_ai.json --backend echo
python -m pytest                              # 42 tests
```

The `echo` backend consults no model. Its output validates the harness and
is stamped synthetic so it can never be mistaken for a model comparison.

## Real evaluation

### 1. Export fixtures — on the RedixFi VM, read-only

```bash
ssh -i <key> ubuntu@92.4.85.177
export REDIXFI_ROOT=/home/ubuntu/redixfi-backend
export CHROMA_PATH=$REDIXFI_ROOT/data/chroma_production

python3 scripts/export_fixtures.py --preflight        # reports, writes nothing
python3 scripts/export_fixtures.py --task annual_report_summary --limit 20 --out ~/llm_fixtures/annual_report_summary.json
python3 scripts/export_fixtures.py --task red_flag --limit 60 --out ~/llm_fixtures/red_flag.json
python3 scripts/export_fixtures.py --task ask_ai --limit 40 --out ~/llm_fixtures/ask_ai.json
```

Run `--preflight` first. It reports how many reference outputs actually
exist, which is the real constraint — see Known limitations.

### 2. Run on Kaggle

See [`deployment/kaggle/README.md`](deployment/kaggle/README.md). Order is
fixed: **`qwen3-14b-awq` first**, `qwen3-30b-a3b-awq` only once the 14B
works.

### 3. Review

Open `evaluation/<phase>/runs/*.md`, read the side-by-side pairs, fill in
the scoring tables, record a verdict. Until that happens, no quality claim
about this model is valid.

## Known limitations — read before interpreting any result

* **Phase A ceiling is ~72 documents.** Only 72 of ~2,000 `annual_reports`
  carry a production summary, because RedixFi's OpenAI account ran out of
  credits (2026-08-28). That is a credit outage, not a code fault, and it
  cannot be worked around from here.
* **Phase B may have no reference at all.** `risk_flag_backfill.py` has not
  been confirmed to have run against production ChromaDB. If it has not,
  Phase B can generate candidate output but has nothing to compare it to.
  `--preflight` reports this explicitly rather than letting it pass quietly.
* **Phase C packets are rebuilt, not recorded.** `ask_log` stores the
  question and metadata; `ask_conversations` stores the answer; the fact
  packet is stored nowhere. Rebuilt packets need a live embedding call for
  `document_chunks`, which fails soft while credits are exhausted. Affected
  cases are marked `packet_degraded` rather than silently accepted.
* **The 30B may not run on T4 at all.** Turing has no bf16/FP8, and
  quantized-MoE kernel support there is the weakest in vLLM's matrix.
* **`echo` output is not evidence of anything.**

## Layout

```
app/
  api/          OpenAI-compatible server (/v1/chat/completions, /v1/models, /health)
  inference/    backend abstraction: vllm | openai | echo
  models/       registry — T4-safe serving args per model
  prompts/      VENDORED RedixFi prompts + PROVENANCE.md
  compliance/   VENDORED RedixFi compliance validators
  tasks/        the three reproduced workloads
  evaluation/   fixture format, runner, comparison, review-sheet generator
  integrations/ read-only RedixFi Mongo/Chroma accessors (VM only)
scripts/        export_fixtures · model_preflight · run_evaluation · serve
deployment/kaggle/  bootstrap, serving, and the deployment runbook
configs/        per-model config, mirrors the registry
tests/          42 offline tests, incl. the drift guard
```

## Security

`.env` is git-ignored and there is a checked-in `.env.example`. No
credential is committed. Fixtures are git-ignored: they can contain full
annual-report text and real user questions, so a Kaggle Dataset holding them
must be **private**.
