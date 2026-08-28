# Evaluation review sheet — annual_report_summary_legacy

> **EXPERIMENTAL / NOT PRODUCTION.** Nothing here is evidence that the candidate model is fit for use. The objective columns below are mechanical checks; every quality judgement is left blank for a human reviewer, by design.

## Run configuration

- **Model:** `qwen3-14b-awq`
- **Weights:** `Qwen/Qwen3-14B-AWQ` (quantization: `awq`, dtype: `float16`, TP: 1, max_model_len: 16384)
- **Backend:** `echo`
- **Sampling:** temperature=0.0, max_tokens=1024, seed=0
- **Fixture:** `fixtures/sample_annual_report_summary.json` (exported 2026-08-28T10:12:25.577874+00:00)
- **Cases run:** 1 of 1
- **LLM project commit:** `b422751`
- **Run id:** `20260828T101419Z` (2026-08-28T10:14:19.186552+00:00)

> ⚠️ **This run used the `echo` backend.** No model was consulted. These results validate the harness only and must never be read as a model comparison.

## Objective signals (mechanical, no judgement)

| Metric | Value |
|---|---|
| cases | 1 |
| generated_ok | 1 |
| generation_failures | 0 |
| candidate_compliance_failures | 0 |
| reference_compliance_failures | 0 |
| cases_with_reference | 1 |
| json_repair_used | 0 |
| mean_latency_sec | 0.0 |
| total_prompt_tokens | 672 |
| total_completion_tokens | 127 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| mean_lexical_overlap | 0.25 |

## Side-by-side cases

### 1. `SAMPLECO` — fixture `AR_SAMPLECO_SAMPLE-0001`

**Fiscal year:** FY2024-25

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.25 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

## Reviewer verdict

After completing the tables above, record ONE of:

- **ACCEPTABLE** — quality is close enough to production to justify a narrow, reversible pilot on one workload.
- **NOT ACCEPTABLE** — name the specific failure mode.
- **INCONCLUSIVE** — say what additional cases would settle it.

Verdict: _______   Reviewer: _______   Date: _______
