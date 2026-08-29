# Review sheet — annual_report_summary_legacy

> **EXPERIMENTAL / NOT PRODUCTION.** This file is evidence for a human to review, not a verdict. No quality score is computed anywhere in it, and no LLM judge was used. The candidate model is NOT declared better or worse than gpt-4o-mini by this tooling.

> ⚠️ **`echo` backend — NO MODEL WAS CONSULTED.** These results validate the harness only and are not a model comparison.

## Run configuration

| | |
|---|---|
| Model | `qwen3-14b-awq` |
| Weights | `Qwen/Qwen3-14B-AWQ` |
| Quantization / dtype | `awq` / `float16` |
| Tensor parallel | 1 |
| Context length | 16384 |
| Backend | `echo` |
| Sampling | temperature=0.0, max_tokens=1024, seed=0 |
| Fixture | `fixtures/sample_annual_report_summary.json` |
| Cases | 1 of 1 |
| Run id | `20260828T101419Z` (2026-08-28T10:14:19.186552+00:00) |
| LLM project commit | `b422751` |

## Objective signals (mechanical only — no judgement)

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

## Cases

---

### Case 1 — `AR_SAMPLECO_SAMPLE-0001`

#### SOURCE / EVIDENCE

- **Symbol:** SAMPLECO
- **Company:** Sample Industries Limited
- **Fiscal year:** FY2024-25
- **Filing id:** SAMPLE-0001
- **Doc type:** annual_report

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - SYNTHETIC — not production data.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

The annual report of Sample Industries Limited for FY2024-25 outlined management's focus on consolidating manufacturing capacity across its three reportable segments. Management said the local sourcing programme was extended to further component categories during the year.

**bullets**

- Management described a focus on consolidating manufacturing capacity
- The report stated the local sourcing programme was extended
- Commissioning work was described at two facilities

**key_takeaway**

The report centred on management's stated consolidation of manufacturing capacity and local sourcing.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period.

**bullets**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.25 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 672 / 127 |
| Tokens/sec (output) | 0.0 |

#### HUMAN REVIEW NOTES

| Dimension | What to look for | Qwen | Reference | Notes |
|---|---|---|---|---|
| **factual quality** | Are the stated facts correct against the source? |  |  |  |
| **evidence grounding** | Is every claim traceable to the supplied evidence? |  |  |  |
| **completeness** | Are the important points from the evidence covered? |  |  |  |
| **hallucination** | Anything asserted that is NOT in the evidence? (none = good) |  |  |  |
| **numerical accuracy** | Any figure stated, and is it right? (AR: figures are forbidden) |  |  |  |
| **readability** | Would an investor find it clear and usable? |  |  |  |
| **compliance** | Beyond the regex: any forward-looking or advice-like tone? |  |  |  |

**Case verdict (ACCEPTABLE / NOT ACCEPTABLE / INCONCLUSIVE):** ______


---

## Overall reviewer verdict

Fill this in only AFTER completing the per-case tables above.

- **Verdict (ACCEPTABLE / NOT ACCEPTABLE / INCONCLUSIVE):** ______
- **If NOT ACCEPTABLE — the specific failure mode:** ______
- **If INCONCLUSIVE — what additional cases would settle it:** ______
- **Reviewer:** ______   **Date:** ______

This was a small sample. It cannot establish production-readiness regardless of how good the outputs look.
