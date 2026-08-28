# STEP 3 RUNBOOK — deploy Qwen3-14B-AWQ and run the 15-case test

**EXPERIMENTAL / NOT PRODUCTION.** Everything here is prepared and tested
offline. It has **not** been run on a GPU: this environment has no Kaggle
credentials and no way to open a Kaggle session, so the GPU numbers do not
exist yet and none are reported anywhere in this project.

Config for this phase, per instruction: **Qwen3-14B-AWQ, TP=2, 32K context,
NO YaRN.** `kaggle_run.py` hard-stops if it is handed a rope-scaling config.

---

## What you upload (already built)

`C:\LLM\kaggle_upload\` — 6.3 MB:

| File | Purpose |
|---|---|
| `llm_project.tar.gz` | the LLM project (96 KB, no git/fixtures/runs) |
| `*_sample15.json` | **the 15 cases this run uses** |
| `*_benchmark.json` | the full 130 cases — carried but NOT run |

> Upload as a **PRIVATE** Kaggle Dataset. The fixtures contain full
> annual-report text and real user questions from `ask_log`.

---

## Step 1 — create the dataset

1. kaggle.com → **Datasets** → **New Dataset**
2. Drag in everything from `C:\LLM\kaggle_upload\`
3. Title: `redixfi-llm-fixtures` · Visibility: **Private**
4. Create.

## Step 2 — create the notebook

1. **Code → New Notebook**
2. Settings: **Accelerator = GPU T4 ×2**, **Internet = ON**
3. **Add Input →** your `redixfi-llm-fixtures` dataset

## Step 3 — one cell, unpack

```python
!mkdir -p /kaggle/working/LLM
!tar xzf /kaggle/input/redixfi-llm-fixtures/llm_project.tar.gz -C /kaggle/working/LLM
!ls /kaggle/working/LLM
```

## Step 4 — one cell, everything else

```python
!python /kaggle/working/LLM/deployment/kaggle/kaggle_run.py \
    --fixtures /kaggle/input/redixfi-llm-fixtures
```

This performs, in order, stopping at the first hard failure:

| # | Action |
|---|---|
| 1–2 | CUDA check, detect both T4s, record VRAM/compute capability |
| 3 | install vLLM (**torch is deliberately not reinstalled**) |
| 4 | download + load `Qwen/Qwen3-14B-AWQ`, TP=2, 32K, float16 |
| 5 | VRAM per GPU after load |
| 6 | in-process generation smoke test → tokens/sec |
| 7 | release the model, start the OpenAI-compatible server |
| 8 | verify `/v1/models` and `/health` |
| 9 | minimal inference smoke test through the API |
| 10 | **the 15 cases**, then STOP |

To do deployment + preflight only, add `--skip-benchmark`.

## Step 5 — download BEFORE the session ends

```python
!cd /kaggle/working/LLM && zip -r /kaggle/working/eval_results.zip evaluation/
!cp /kaggle/working/kaggle_run_state.json /kaggle/working/vllm_server.log /kaggle/working/
```

Download `eval_results.zip`, `kaggle_run_state.json`, `vllm_server.log` from
the Output panel. **A session that ends without this loses every result and
the GPU hours with it.**

---

## The 15 cases (deterministic, diversity-picked)

| Benchmark | n | Coverage |
|---|---|---|
| Annual Report | 3 | ETERNAL, LT, BEL — evidence 19,505 / 19,520 / 20,000 tokens |
| Concall | 3 | one per tone (`Mixed`/`Neutral`/`Positive`), 2 transcripts + 1 presentation |
| Red Flag | 6 | one per positive category + 2 LLM-rejected negatives |
| Ask AI | 3 | TCS, BEL, ABB — reference answers 44 / 784 / 1,841 chars |

Context measured against these exact cases at 32K:

| Replay | Max prompt | Needs | 32K |
|---|---|---|---|
| `annual_report_summary` | 13,434 | 14,458 | ✅ |
| `concall_summary` | 13,740 | 14,764 | ✅ |
| `red_flag` | 760 | 1,784 | ✅ |
| `ask_ai` | 4,486 | 5,510 | ✅ |
| `annual_report_summary_legacy` | 61,432 | 62,456 | ❌ **deferred** |

---

## ⚠️ Two limitations of this phase, stated up front

**1. The Annual Report comparison is NOT like-for-like.** The stored
reference was written 2026-08-16 by the legacy pipeline (raw-text front
slice, `summary`/`bullets`/`key_takeaway`). At 32K only the *current*
pipeline replay fits (Evidence Finder evidence,
`executive_summary`/`key_points`/`important_risks`), so **both the input and
the output schema differ**. The review sheet says so at the top of the file
and per case. The like-for-like replay needs 64K/YaRN, excluded from this
phase.

**2. 15 cases cannot establish production-readiness**, however good the
output looks. It is a smoke test of quality, not a verdict.

---

## If the model fails to load

`kaggle_run.py` records the exact error and stops. **It never substitutes a
model.** On OOM it prints the ladder — apply in order, reporting each:

1. `--max-model-len 16384`
2. `--gpu-memory-utilization 0.85`
3. only then reconsider configuration, with the error in hand

Do not change model or quantization to make it pass.

---

## Expected GPU cost

| Phase | Estimate |
|---|---|
| Setup + vLLM install | ~3–5 min (no GPU compute) |
| Weight download + load | ~10–15 min |
| Server start + smoke tests | ~3–5 min |
| 15 cases | unknown until measured |
| **Total** | **~30–45 min of a ~30 h weekly budget** |

The per-case figure is deliberately left blank. It is one of the things this
run exists to measure, and guessing it here would be inventing data.

---

## What comes back for review

`evaluation/<phase>/runs/*.md` — one review sheet per benchmark, each case
laid out as:

```
SOURCE / EVIDENCE          real evidence excerpt + provenance
OLD — GPT-4o-mini OUTPUT   the production reference, verbatim
NEW — QWEN OUTPUT          what the candidate produced
OBJECTIVE VALIDATION       compliance, category/tone agreement, tokens, latency
HUMAN REVIEW NOTES         BLANK — factual quality, grounding, completeness,
                           hallucination, numerical accuracy, readability,
                           compliance
```

No score is computed. No LLM judge is used. Qwen is not declared better or
worse than gpt-4o-mini anywhere by this tooling — that is the reviewer's
call, and the sheets exist to make it possible.
