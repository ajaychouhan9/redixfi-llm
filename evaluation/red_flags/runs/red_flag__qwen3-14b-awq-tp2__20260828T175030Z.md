# Review sheet — red_flag

> **EXPERIMENTAL / NOT PRODUCTION.** This file is evidence for a human to review, not a verdict. No quality score is computed anywhere in it, and no LLM judge was used. The candidate model is NOT declared better or worse than gpt-4o-mini by this tooling.

## Run configuration

| | |
|---|---|
| Model | `qwen3-14b-awq-tp2` |
| Weights | `Qwen/Qwen3-14B-AWQ` |
| Quantization / dtype | `awq` / `float16` |
| Tensor parallel | 2 |
| Context length | 32768 |
| Backend | `vllm-inprocess` |
| Sampling | temperature=0.0, max_tokens=1024, seed=0 |
| Fixture | `/kaggle/input/datasets/ajaychouhan9/redixfi-llm-fixtures/red_flag_sample15.json` |
| Cases | 1 of 6 |
| Run id | `20260828T175030Z` (2026-08-28T17:50:30.635004+00:00) |
| LLM project commit | `unknown` |
| GPU | 2x Tesla T4 (29.12 GB total) |
| CUDA / torch / vLLM | 13.0 / 2.13.0+cu130 / None |

## Objective signals (mechanical only — no judgement)

| Metric | Value |
|---|---|
| cases | 1 |
| generated_ok | 1 |
| generation_failures | 0 |
| candidate_compliance_failures | 0 |
| reference_backstop_artifacts | 0 |
| reference_compliance_failures | 0 |
| cases_with_reference | 1 |
| structured_output_used | 1 |
| json_repair_used | 0 |
| guided_and_clean | 1 |
| guided_but_repaired | 0 |
| unguided | 0 |
| mean_latency_sec | 2.021 |
| total_prompt_tokens | 601 |
| total_completion_tokens | 54 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| outcomes | agree=1 |
| agreement_rate | 1.0 |

**Reading the outcomes:** `false_positive` = Qwen flagged where production did not · `false_negative` = Qwen missed a flag production confirmed · `category_mismatch` = both flagged, different category.

## Cases

---

### Case 1 — `RF_ABB_AR_ABB_277`

#### SOURCE / EVIDENCE

- **Symbol:** ABB
- **Company:** ABB India Limited
- **Fiscal year:** FY2026
- **Doc type:** annual_report
- **Chunk id:** AR_ABB_277
- **Polarity:** positive
- **Keyword candidates:** `auditor_qualification`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
ndependent of the Company in accordance with the Code 
of Ethics issued by the Institute of Chartered Accountants 
of India together with the ethical requirements that are 
relevant to our audit of the standalone financial statements 
under the provisions of the Act and the Rules thereunder, 
and we have fulfilled our other ethical responsibilities in 
accordance with these requirements and the Code of Ethics. 
We believe that the audit evidence we have obtained is 
sufficient and appropriate to provide a basis for our opinion 
on the standalone financial statements.
KEY AUDIT MATTERS
Key audit matters are those matters that, in our professional judgment, were of most significance in our audit of the 
standalone financial statements of the current period. These matters were addressed in the context of our audit of the 
standalone financial statements as a whole, and in forming our opinion thereon, and we do not provide a separate opinion 
on these matters.
Revenue from fixed price contracts using percentage of completion method
See Note 2.3(a) and 2.6 to the standalone financial statements.
The key audit matter
How the matter was addressed in our audit
Revenue from fixed price contracts are recognized in 
accordance with Ind AS 115, Revenue from Contracts with 
Customers, and as detailed in note 2.3(a) and 2.6 of the 
“material accounting policies” in the standalone financial 
statements.
There are key judgments and estimates involved in the 
recognition of revenue relating t

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `auditor_qualification`

**risk_flag_summary**

The excerpt discusses the audit process and key audit matters related to the standalone financial statements, including the recognition of revenue from fixed price contracts and the judgments and estimates involved in this process.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `auditor_qualification`

**risk_flag_summary**

The auditor discusses their independence and ethical compliance in accordance with the Code of Ethics and the Act. They mention key audit matters related to revenue recognition from fixed price contracts using the percentage of completion method.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `auditor_qualification` |
| Category — Qwen | `auditor_qualification` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 2.0214 s |
| Input / output tokens | 601 / 54 |
| Tokens/sec (output) | 26.7 |

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
