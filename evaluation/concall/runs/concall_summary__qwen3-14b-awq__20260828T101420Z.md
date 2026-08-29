# Review sheet — concall_summary

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
| Fixture | `fixtures/sample_concall_summary.json` |
| Cases | 1 of 1 |
| Run id | `20260828T101420Z` (2026-08-28T10:14:20.642888+00:00) |
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
| total_prompt_tokens | 752 |
| total_completion_tokens | 130 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| tone_label_agreement_rate | 0.0 |
| invalid_tone_labels | 0 |
| tone_confusion | Positive->Neutral=1 |
| mean_lexical_overlap | 0.4348 |

## Cases

---

### Case 1 — `CC_SAMPLECO_CC-0001`

#### SOURCE / EVIDENCE

- **Symbol:** SAMPLECO
- **Company:** Sample Industries Limited
- **Filing id:** CC-0001
- **Doc type:** concall_transcript
- **Doc kind:** earnings concall transcript

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - SYNTHETIC — not production data.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

Management reported that the Company commissioned a second line at its western facility during the quarter. The presentation described demand from domestic infrastructure customers as the largest contributor to order intake, and management noted that input cost pressure eased relative to the previous quarter. Management also described the local sourcing programme as extended to further component categories.

**tone_note**

Management emphasised commissioning progress and easing input costs in describing the quarter.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**tone_label:** `Neutral`

**summary**

Management reported on operating activity during the period. The document described commissioning progress at the company's facilities and management said demand from domestic customers remained the largest contributor to order intake. Management also described the sourcing programme as extended to further component categories during the quarter under review.

**tone_note**

Management described operating activity in even terms without emphasising either strength or weakness.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Positive` |
| tone_label — Qwen | `Neutral` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ❌ no |
| Lexical overlap | 0.4348 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 752 / 130 |
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
