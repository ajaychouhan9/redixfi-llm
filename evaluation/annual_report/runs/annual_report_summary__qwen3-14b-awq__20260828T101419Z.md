# Evaluation review sheet — annual_report_summary

> **EXPERIMENTAL / NOT PRODUCTION.** Nothing here is evidence that the candidate model is fit for use. The objective columns below are mechanical checks; every quality judgement is left blank for a human reviewer, by design.

## Run configuration

- **Model:** `qwen3-14b-awq`
- **Weights:** `Qwen/Qwen3-14B-AWQ` (quantization: `awq`, dtype: `float16`, TP: 1, max_model_len: 16384)
- **Backend:** `echo`
- **Sampling:** temperature=0.0, max_tokens=1024, seed=0
- **Fixture:** `fixtures/sample_annual_report_summary.json` (exported 2026-08-28T10:12:25.577874+00:00)
- **Cases run:** 1 of 1
- **LLM project commit:** `b422751`
- **Run id:** `20260828T101419Z` (2026-08-28T10:14:19.901563+00:00)

> ⚠️ **This run used the `echo` backend.** No model was consulted. These results validate the harness only and must never be read as a model comparison.

## Objective signals (mechanical, no judgement)

| Metric | Value |
|---|---|
| cases | 1 |
| generated_ok | 1 |
| generation_failures | 0 |
| candidate_compliance_failures | 0 |
| reference_compliance_failures | 1 |
| cases_with_reference | 1 |
| json_repair_used | 0 |
| mean_latency_sec | 0.0 |
| total_prompt_tokens | 758 |
| total_completion_tokens | 157 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| mean_lexical_overlap | 0.1389 |

## Side-by-side cases

### 1. `SAMPLECO` — fixture ``

**Fiscal year:** FY2024-25

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

The report centred on management's stated consolidation of manufacturing capacity and local sourcing.

**CANDIDATE — executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**CANDIDATE — key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**CANDIDATE — important_risks**

_(none)_

**CANDIDATE — key_takeaway**

The report centred on management's stated operating priorities for the period.

**Compliance —** candidate: ✅ pass · reference: ❌ executive_summary: empty text

**Lexical overlap:** 0.1389 _(triage aid only — not a quality score)_

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
