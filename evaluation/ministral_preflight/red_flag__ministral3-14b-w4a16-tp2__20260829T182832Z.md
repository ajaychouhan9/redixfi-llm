# Review sheet — red_flag

> **EXPERIMENTAL / NOT PRODUCTION.** This file is evidence for a human to review, not a verdict. No quality score is computed anywhere in it, and no LLM judge was used. The candidate model is NOT declared better or worse than gpt-4o-mini by this tooling.

## Run configuration

| | |
|---|---|
| Model | `ministral3-14b-w4a16-tp2` |
| Weights | `cyankiwi/Ministral-3-14B-Instruct-2512-AWQ-4bit` |
| Quantization / dtype | `compressed-tensors` / `float16` |
| Tensor parallel | 2 |
| Context length | 32768 |
| Backend | `vllm-inprocess` |
| Sampling | temperature=0.0, max_tokens=1024, seed=0 |
| Fixture | `/kaggle/input/datasets/ajaychouhan9/redixfi-llm-evaluation-2026/red_flag_sample15.json` |
| Cases | 2 of 6 |
| Run id | `20260829T182832Z` (2026-08-29T18:28:32.240898+00:00) |
| LLM project commit | `unknown` |
| GPU | 2x Tesla T4 (29.12 GB total) |
| CUDA / torch / vLLM | 13.0 / 2.13.0+cu130 / None |

## Objective signals (mechanical only — no judgement)

| Metric | Value |
|---|---|
| cases | 2 |
| generated_ok | 2 |
| generation_failures | 0 |
| candidate_compliance_failures | 0 |
| reference_backstop_artifacts | 0 |
| reference_compliance_failures | 0 |
| cases_with_reference | 2 |
| structured_output_used | 2 |
| json_repair_used | 0 |
| guided_and_clean | 2 |
| guided_but_repaired | 0 |
| unguided | 0 |
| mean_latency_sec | 1.428 |
| total_prompt_tokens | 1331 |
| total_completion_tokens | 71 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| outcomes | false_negative=1, agree=1 |
| agreement_rate | 0.5 |

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

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

<details><summary>Rejected attempts</summary>

- pass 1: model returned no category (genuine non-match)

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `auditor_qualification` |
| Category — Qwen | `— (no flag)` |
| Outcome | **false_negative** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 0.8871 s |
| Input / output tokens | 653 / 11 |
| Tokens/sec (output) | 12.4 |

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

### Case 2 — `RF_ABB_AR_ABB_312`

#### SOURCE / EVIDENCE

- **Symbol:** ABB
- **Company:** ABB India Limited
- **Fiscal year:** FY2026
- **Doc type:** annual_report
- **Chunk id:** AR_ABB_312
- **Polarity:** positive
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
ring the period. Application 
of accounting policies that require critical accounting 
estimates involving complex and subjective judgments 
and the use of assumptions in these standalone financial 
statements have been disclosed in Note 2.3. Accounting 
estimates could change from period to period. Actual 
results could differ from those estimates. Appropriate 
changes in estimates are made as management 
becomes 
aware 
of 
changes 
in 
circumstances 
surrounding the estimates. Changes in estimates are 
reflected in the financial statements in the period in 
which changes are made and, if material, their effects 
are disclosed in the notes to the standalone financial 
statements. Estimates and underlying assumptions are 
reviewed on an ongoing basis.
2.3	 Critical accounting estimates and judgements
	
a.	
Project revenue and costs (refer note 2.6)
	
	
The Company uses the percentage-of-completion 
method in accounting for its fixed-price contracts. 
Use of the percentage-of-completion method 
requires the Company to measure the costs 
expended to date as a proportion of the total 
costs estimated to be incurred. Costs expended 
have been used to measure progress towards 
completion as there is a direct relationship 
between input and productivity. Provisions for 
estimated losses, if any, on uncompleted contracts 
are recorded in the period in which such losses 
become probable based on the expected contract 
estimates at the reporting date.
	
b.	
Provision for litigations 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `contingent_liability`

**risk_flag_summary**

The excerpt discusses the company's provisions for litigations and contingencies, indicating that provisions are estimated for present obligations that may require resource outflow. It also mentions the assessment of contingent liabilities based on significant judgments.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**risk_flag_type:** `contingent_liability`

**risk_flag_summary**

The excerpt discusses the company's process for estimating and adjusting provisions for litigations and contingencies, including the recognition of contingent liabilities when there is a possible obligation and the use of significant judgments to assess them.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `contingent_liability` |
| Category — Qwen | `contingent_liability` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.968 s |
| Input / output tokens | 678 / 60 |
| Tokens/sec (output) | 30.5 |

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
