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
| Fixture | `/kaggle/input/datasets/ajaychouhan9/redixfi-llm-fixtures/red_flag_benchmark.json` |
| Cases | 60 of 60 |
| Run id | `20260829T073830Z` (2026-08-29T07:38:30.297951+00:00) |
| LLM project commit | `unknown` |
| GPU | 2x Tesla T4 (29.12 GB total) |
| CUDA / torch / vLLM | 13.0 / 2.13.0+cu130 / None |

## Objective signals (mechanical only — no judgement)

| Metric | Value |
|---|---|
| cases | 60 |
| generated_ok | 60 |
| generation_failures | 0 |
| candidate_compliance_failures | 0 |
| reference_backstop_artifacts | 0 |
| reference_compliance_failures | 0 |
| cases_with_reference | 60 |
| structured_output_used | 60 |
| json_repair_used | 0 |
| guided_and_clean | 60 |
| guided_but_repaired | 0 |
| unguided | 0 |
| mean_latency_sec | 1.802 |
| total_prompt_tokens | 39126 |
| total_completion_tokens | 3066 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| outcomes | agree=38, false_negative=2, agree_no_flag=13, false_positive=7 |
| agreement_rate | 0.85 |

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
| Latency | 1.9405 s |
| Input / output tokens | 601 / 54 |
| Tokens/sec (output) | 27.8 |

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

### Case 2 — `RF_ASIANPAINT_AR_ASIANPAINT_716`

#### SOURCE / EVIDENCE

- **Symbol:** ASIANPAINT
- **Company:** Asian Paints Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_ASIANPAINT_716
- **Polarity:** positive
- **Keyword candidates:** `auditor_qualification`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
 are independent of the Group and its associates in 
accordance with the Code of Ethics issued by the Institute 
of Chartered Accountants of India (“ICAI”) together with the 
ethical requirements that are relevant to our audit of the 
Consolidated Financial Statements under the provisions of 
the Act and the Rules made thereunder, and we have fulfilled 
our other ethical responsibilities in accordance with these 
requirements and the ICAI’s Code of Ethics. We believe that 
the audit evidence obtained by us and the audit evidence 
obtained by the other auditors in terms of their reports 
referred to in the Other Matters section below, is sufficient 
and appropriate to provide a basis for our audit opinion on 
the Consolidated Financial Statements. 
Key Audit Matters
Key audit matters are those matters that, in our professional 
judgment, were of most significance in our audit of the 
Consolidated Financial Statements of the current period. 
These matters were addressed in the context of our audit 
of the Consolidated Financial Statements as a whole, and 
in forming our opinion thereon, and we do not provide a 
separate opinion on these matters. We have determined the 
matters described below to be the key audit matters to be 
communicated in our report.
Key Audit Matter
Auditor’s Response
Revenue recognition – the Parent (Refer note 1.4 (e) and 23A of the Consolidated Financial Statements)
Revenue is one of the key profit drivers and is therefore susceptible 
to misstatement. 

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

The excerpt discusses the audit process and the key audit matters identified during the audit of the Consolidated Financial Statements, including revenue recognition and its susceptibility to misstatement.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `auditor_qualification`

**risk_flag_summary**

The auditor states their independence and ethical compliance in accordance with ICAI's Code of Ethics and describes key audit matters related to revenue recognition and goodwill impairment.

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
| Latency | 1.6011 s |
| Input / output tokens | 605 / 46 |
| Tokens/sec (output) | 28.7 |

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

### Case 3 — `RF_BRITANNIA_AR_BRITANNIA_334`

#### SOURCE / EVIDENCE

- **Symbol:** BRITANNIA
- **Company:** Britannia Industries Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_BRITANNIA_334
- **Polarity:** positive
- **Keyword candidates:** `auditor_qualification`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
the other auditors on separate financial 
statements of the subsidiaries, associate companies 
and a joint venture company, were of most significance 
in our audit of the consolidated financial statements of 
the current period. These matters were addressed in 
the context of our audit of the consolidated financial 
statements as a whole, and in forming our opinion 
thereon, and we do not provide a separate opinion on 
these matters.
We have determined the matters described below to be the key audit matters to be communicated in our report.
Key audit matter
How our audit addressed the key audit matter
Revenue Recognition (refer note 3(i) and 29 to the 
consolidated financial statements)
The revenue of the Group consists primarily of sale of food 
products that are sold through distributors, modern trade 
and direct sale channels amongst others.
Revenue is recognized when the control of products is 
transferred to the customer and there is no unfulfilled 
obligation.
Our key audit procedures around revenue recognition 
included, but were not limited to, the following:
•	
Assessed 
the 
appropriateness 
of 
the 
revenue 
recognition accounting policies of the Group including 
those relating to rebates and trade discounts, by 
evaluating compliance with the applicable accounting 
standards.
•	
Evaluated the design and tested the operating 
effectiveness of the key controls with respect to 
revenue recognition including general and specific 
information technology controls.
INDEP

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

The excerpt discusses key audit matters related to revenue recognition in the context of the audit of consolidated financial statements, highlighting the significant risk and the auditor's attention required in this area.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `auditor_qualification`

**risk_flag_summary**

The excerpt discusses the auditor's focus on revenue recognition as a key audit matter, including their procedures to assess accounting policies and controls related to revenue recognition.

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
| Latency | 1.5742 s |
| Input / output tokens | 595 / 45 |
| Tokens/sec (output) | 28.6 |

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

### Case 4 — `RF_ETERNAL_AR_ETERNAL_428`

#### SOURCE / EVIDENCE

- **Symbol:** ETERNAL
- **Company:** ETERNAL LIMITED
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_ETERNAL_428
- **Polarity:** positive
- **Keyword candidates:** `auditor_qualification`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
, in our 
professional judgment, were of most significance in 
our audit of the standalone financial statements of 
the current period. These matters were addressed in 
the context of our audit of the standalone financial 
statements as a whole, and in forming our opinion 
thereon, and we do not provide a separate opinion 
on these matters. We have determined the matters 
described below to be the key audit matters to be 
communicated in our report:
Financial Statements: Standalone
Statutory Reports
Company Overview
Sr. No. Key Audit Matter
Auditor’s Response
1.
Fair valuation of investment in other entities
(Refer note 5 & 29 of the standalone financial 
statement)
The Company has made investments 
in CureFit Healthcare Private Limited, 
Shiprocket Limited, Samast Technologies 
Private Limited and Adonmo Private Limited 
where the aggregate carrying value of these 
investments as on March 31, 2026, is INR 1,781 
crores. These investments are measured 
at Fair Value through Other Comprehensive 
Income (‘FVTOCI’) as at March 31, 2026.
We considered the valuation assumptions 
relating to weighted average cost of capital, 
terminal growth rate, revenue multiple and 
the methodology in estimation of fair value of 
these investments as a key audit matter due 
to the significance of the investment amount 
and the significant estimates and judgement 
involved in determination of fair value.
Principal audit procedures performed:
•	 Evaluated the design, implementation and tested 
op

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

The excerpt discusses key audit matters identified during the audit of the standalone financial statements, specifically focusing on the fair valuation of investments in other entities and the significant estimates and judgments involved in determining their fair value.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `auditor_qualification`

**risk_flag_summary**

The auditor identified the fair valuation of investments in other entities as a key audit matter due to the significant estimates and judgments involved in determining their fair value. The auditor evaluated internal controls, the specialist's valuation report, and the reasonableness of the methodology used.

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
| Latency | 2.1372 s |
| Input / output tokens | 619 / 67 |
| Tokens/sec (output) | 31.3 |

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

### Case 5 — `RF_HDFCBANK_AR_HDFCBANK_766`

#### SOURCE / EVIDENCE

- **Symbol:** HDFCBANK
- **Company:** HDFC Bank Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_HDFCBANK_766
- **Polarity:** positive
- **Keyword candidates:** `auditor_qualification`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
d General IT Controls (GITC) over key financial 
accounting and reporting systems (referred to as “in-scope 
systems”) which covered access controls, program / system 
changes, program development and computer operations;
•	
Understood the IT infrastructure i.e. operating systems and 
databases and related data security controls;
•	
Tested controls over IT infrastructure covering user access 
including privilege users and system changes;
•	
Evaluated design and operating effectiveness for in-scope 
systems and application controls which covered segregation 
of duties, system interfaces, completeness and accuracy of 
data feeds and system reconciliation controls; and
•	
Evaluated policies and strategies adopted by the Company in 
relation to operational security of key information infrastructure, 
data and client information management and monitoring.
Integrated Annual Report 2024-25
Statutory Reports and Financial Statements
Valuation and impairment determination of Investments 
Refer Schedule 8 of the Special Purpose Financial Information
Key audit matter
How the matter was addressed in our audit
The Company’s investment portfolio has been bifurcated into 
Policyholders investments and Shareholders investments in terms 
of IRDAI guidelines. Total investments represent 85.11 percent of 
the Company’s total assets as at 31 March 2025. 
Investments are valued in accordance with the provisions of the 
Insurance Act, the IRDA Financial Statements Regulations, orders / 
directions

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

The excerpt discusses the evaluation of the company's investment portfolio and the key audit matter related to the valuation and impairment determination of investments, which is a focus area in the audit process.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `auditor_qualification`

**risk_flag_summary**

The excerpt discusses the auditor's evaluation of the company's IT controls, including access controls, system changes, segregation of duties, and data security, as well as the design and operating effectiveness of in-scope systems.

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
| Latency | 1.9102 s |
| Input / output tokens | 614 / 58 |
| Tokens/sec (output) | 30.4 |

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

### Case 6 — `RF_INDIGO_AR_INDIGO_264`

#### SOURCE / EVIDENCE

- **Symbol:** INDIGO
- **Company:** InterGlobe Aviation Limited
- **Fiscal year:** FY2026
- **Doc type:** annual_report
- **Chunk id:** AR_INDIGO_264
- **Polarity:** positive
- **Keyword candidates:** `auditor_qualification`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
, our audit included the performance of procedures designed to respond to our 
assessment of the risks of material misstatement of the standalone financial statements. The results of our audit procedures, including 
the procedures performed to address the matters below, provide the basis for our audit opinion on the accompanying standalone 
financial statements.
Key audit matters
How our audit addressed the key audit matter
Recognition of Passenger Revenue (refer note 23 to the standalone financial statements)
The Company recognises passenger revenue on flown basis 
i.e., when the service is rendered. Moreover, fees charged for 
cancellation of flight tickets is recognised as revenue on rendering 
of the said service.
The determination of passenger revenue to be recognised for 
each flight requires complex IT systems and involves high volume 
of transactions.
We identified revenue recognition as a key audit matter because 
passenger revenue is one of the Company’s key performance 
indicators, it involves complicated IT systems that handle large 
volumes of transaction data, includes exchange of information 
with industry systems and partner airlines and judgement is 
required by management in determining the unexercised rights of 
passengers, all of which give rise to an inherent risk that revenue 
could be recorded in the incorrect period or at incorrect amount.
Our procedures included, but were not limited to the following:
 
 
assessed that the revenue recognition policy i

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

The excerpt discusses the audit procedures related to the recognition of passenger revenue, identifying it as a key audit matter due to the complexity and judgment involved in the revenue recognition process. It outlines the assessment of the revenue recognition policy and the involvement of IT specialists in evaluating the effectiveness of internal controls over the Company's IT systems.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `auditor_qualification`

**risk_flag_summary**

The auditor discusses the key audit matter of revenue recognition, highlighting the complexity of passenger revenue recognition and the procedures performed to address the risks of material misstatement.

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
| Latency | 1.5755 s |
| Input / output tokens | 571 / 46 |
| Tokens/sec (output) | 29.2 |

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

### Case 7 — `RF_LT_AR_LT_718`

#### SOURCE / EVIDENCE

- **Symbol:** LT
- **Company:** Larsen & Toubro Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_LT_718
- **Polarity:** positive
- **Keyword candidates:** `auditor_qualification`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
es relating to billing of contract assets 
and recoverability of overdue trade receivable with actual billing and collections during the year.
	
•	
In case of certain Defence contracts, (a) performed alternative procedures over progressive billing 
and collections from customer and (b) obtained specific management representation and also direct 
confirmation from the customer with respect to confidentiality restrictions.     
	
•	
Read and tested the presentation and disclosure in the financial statements are in accordance with 
applicable accounting standards.
Impairment of Investment in a Subsidiary
Key audit matter 
description
As at March 31, 2025, the Company held investment with a carrying amount of ¢ 7,412.99 crore (excluding 
investment of ¢ 973.73 crore in debentures) in L&T Metro Rail (Hyderabad) Limited, a wholly owned subsidiary. 
This investment is carried at cost less impairment in the Company’s Standalone Financial Statements. Consequent 
to accumulation of losses incurred by the subsidiary, the Company’s management has tested this investment for 
impairment in accordance with Ind AS 36 by comparing its recoverable amount with it carrying amount as at March 
31, 2025. The recoverable amount of the investment in the subsidiary is assessed based on future discounted cash 
flows of the subsidiary, over the entire concession period.
We considered this as a key audit matter due to significant judgement involved in estimating future cash flows of 
the subsidiary an

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

The excerpt discusses a key audit matter related to the impairment of an investment in a subsidiary, highlighting the significant judgment involved in estimating future cash flows and determining the discount rate for the impairment assessment.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `auditor_qualification`

**risk_flag_summary**

The auditor discusses the key audit matter related to the impairment of an investment in a subsidiary, highlighting the significant judgment involved in estimating future cash flows and discount rates, which could impact the impairment assessment.

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
| Latency | 1.8066 s |
| Input / output tokens | 607 / 54 |
| Tokens/sec (output) | 29.9 |

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

### Case 8 — `RF_ONGC_AR_ONGC_547`

#### SOURCE / EVIDENCE

- **Symbol:** ONGC
- **Company:** Oil & Natural Gas Corporation Limited
- **Fiscal year:** FY2026
- **Doc type:** annual_report
- **Chunk id:** AR_ONGC_547
- **Polarity:** positive
- **Keyword candidates:** `auditor_qualification`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
ial Statements 
Consolidated Financial Statements
Annexures to the Board’s Report
Sr. 
No.
Key Audit Matter
How our audit addressed the matter
Evaluation of adequacy of provision for impairment for tangible 
and intangible assets 
(Refer Note 48 to the Standalone Financial Statements) 
Management has assessed whether any provision needs to be 
recognized on account of impairment of tangible and intangible 
assets. 
The Company reviews the carrying amount of its tangible and 
intangible assets (Oil and Gas Assets including Capital Work-
in-Progress (CWIP) & Development Wells in Progress (DWIP), 
Other Property, Plant & Equipment (including Capital Works-in-
Progress, Right of Use Assets) for the “Cash Generating Unit” 
(CGU) determined at the end of each reporting period to assess 
whether there is any indication that those assets have suffered 
any impairment loss. 
Oil and Gas price assumptions have a significant impact on 
CGU impairment assessments and are inherently uncertain. 
Furthermore, oil and gas prices are subject to increased 
uncertainty, given regulatory guidelines including notified gas 
prices, impact of climate change and the global energy transition.
The management’s assumptions for prices of oil and gas in 
future are highly judgmental and may not be reflective of above 
factors, leading to a risk of material misstatement of the financial 
performance and position. 
Given the long timeframes involved, certain recoverable amounts 
of assets are sensitive to 

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

The excerpt discusses the evaluation of the adequacy of provision for impairment of tangible and intangible assets, highlighting the management's assessment and the inherent uncertainties in oil and gas price assumptions that could lead to material misstatements.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

<details><summary>Rejected attempts</summary>

- pass 1: summary failed compliance: forward-tense word 'forecasts'

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
| Latency | 1.901 s |
| Input / output tokens | 594 / 58 |
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

### Case 9 — `RF_POWERGRID_AR_POWERGRID_688`

#### SOURCE / EVIDENCE

- **Symbol:** POWERGRID
- **Company:** Power Grid Corporation of India Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_POWERGRID_688
- **Polarity:** positive
- **Keyword candidates:** `auditor_qualification`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
billed i.e., Unbilled Revenue.
Our audit approach involved:
	

Obtaining an understanding of the CERC Tariff 
Regulations, Orders, Circulars, Guidelines and the 
Company’s internal circulars and procedures 
in respect of recognition and measurement of 
revenue from transmission of power.
	

Evaluated and tested the effectiveness of 
the design of Internal controls relating to 
recognition and measurement of revenue from 
Transmission.
	

Verified the transmission revenue based on 
the CERC Tariff Regulation, Orders, Circulars, 
Guidelines and the Company’s internal circulars.
Standalone Financial Statements
INTEGRATED ANNUAL REPORT 2025-26
INTEGRATED ANNUAL REPORT 2025-26
Sr. 
No.
Key Audit Matters
How the matter was addressed in our audit
This is considered as Key Audit Matter due to the 
nature and extent of estimates made as per CERC 
Tariff Regulations and contracts with customers 
for recognition of revenue.
(Refer Note No. 35(b)(ii) of Standalone Financial 
Statements)
	

Verified on test basis, the income recognised on 
provisional basis, as per the regulatory guidelines 
and orders of the CERC in recent cases where 
tariff orders were issued, for the assets whose 
final orders are yet to be notified by CERC, based 
on the date of commercial operation (DOCO) 
letters issued by Regional technical heads, and 
capital cost, as certified by the Management. 
	

Assessed 
the 
relevant 
disclosures 
made 
within the standalone financial statements as 
per the requiremen

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

The excerpt discusses the audit approach taken regarding the recognition and measurement of revenue from the transmission of power, highlighting key audit matters and the evaluation of internal controls. It mentions that the nature and extent of estimates made as per CERC Tariff Regulations are considered key audit matters.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `auditor_qualification`

**risk_flag_summary**

The audit focused on revenue recognition based on CERC regulations and internal procedures, including verification of provisional income and reassessment of deferred tax liabilities due to regulatory changes.

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
| Latency | 1.691 s |
| Input / output tokens | 658 / 47 |
| Tokens/sec (output) | 27.8 |

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

### Case 10 — `RF_TATAPOWER_AR_TATAPOWER_756`

#### SOURCE / EVIDENCE

- **Symbol:** TATAPOWER
- **Company:** Tata Power Company Limited
- **Fiscal year:** FY2026
- **Doc type:** annual_report
- **Chunk id:** AR_TATAPOWER_756
- **Polarity:** positive
- **Keyword candidates:** `auditor_qualification`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
nsibilities described in the Auditor’s 
responsibilities for the audit of the consolidated financial 
statements section of our report, including in relation to these 
matters. Accordingly, our audit included the performance of 
procedures designed to respond to our assessment of the 
risks of material misstatement of the consolidated financial 
statements. The results of audit procedures performed by 
us and by other auditors of components not audited by us, 
as reported by them in their audit reports furnished to us by 
the management, including those procedures performed 
to address the matters below, provide the basis for our 
audit opinion on the accompanying consolidated financial 
statements.
Key audit matters
How our audit addressed the key audit matter
Management assessment of appropriateness of Going Concern assumptions (as described in Note 44.4.3 of the 
consolidated Ind AS financial statements)
The Group has current liabilities of ` 39,223.57 crore and 
current assets of ` 30,571.05 crore as at March 31, 2026.
In the power sector, capital expenditure is typically funded 
through a combination of borrowings and equity. While the 
Group predominantly uses long-term borrowings to fund its 
capital expenditure, it also utilises short-term borrowings for 
long-term purposes such as capex, as short-term funds are 
available at comparatively lower interest rates. Therefore, 
Current liabilities exceed current assets as at the year end.
Our audit procedures and procedure

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

The excerpt discusses the auditor's responsibilities and procedures related to the assessment of risks of material misstatement in the consolidated financial statements, including the management's assessment of going concern assumptions.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `auditor_qualification`

**risk_flag_summary**

The excerpt discusses the auditor's procedures related to assessing the appropriateness of going concern assumptions, including understanding the process for approving annual business plans and managing short-term borrowings.

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
| Latency | 1.7099 s |
| Input / output tokens | 601 / 50 |
| Tokens/sec (output) | 29.2 |

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

### Case 11 — `RF_ABB_AR_ABB_312`

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `contingent_liability`

**risk_flag_summary**

The excerpt discusses the company's estimation of provisions for litigations and contingencies, including the recognition of contingent liabilities when there is a possible obligation.

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
| Latency | 1.6012 s |
| Input / output tokens | 598 / 46 |
| Tokens/sec (output) | 28.7 |

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

### Case 12 — `RF_ASIANPAINT_AR_ASIANPAINT_848`

#### SOURCE / EVIDENCE

- **Symbol:** ASIANPAINT
- **Company:** Asian Paints Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_ASIANPAINT_848
- **Polarity:** positive
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
g capital is to safeguard its ability to 
continue as a going concern and to maintain an optimal capital structure so as to maximize shareholder value.
The capital structure of the Group consists of debt, which includes the borrowings disclosed in Note 16 and equity attributable 
to owners of the Parent Company, comprising issued capital, reserves and accumulated profits as presented in the Consolidated 
Statements of changes in Equity.	 	
	
	
	
	
Consequent to such capital structure, there are no externally imposed capital requirements. In order to maintain or achieve an 
optimal capital structure, the Group allocates its capital for distribution as dividend or re-investment into business based on its 
long term financial plans.	
	
	
Note 31 : Earnings Per Share
Year
2025-26
Year
2024-25
Basic earnings per share in rupees (face value – ₹1 per share) (in ₹)
Diluted earnings per share in rupees (face value – ₹1 per share) (in ₹)
Profit used as Numerator
	
Profit after tax attributable to owners of the Parent Company as per Consolidated 	
Statement of Profit and Loss (₹ in crores)
Weighted Average Number of Shares used as Denominator
	
Basic EPS
95,86,16,565
95,87,21,421
	
Diluted EPS
95,87,91,026
95,88,73,609
Reconciliation of Weighted Average Number of Shares Outstanding
	
Number of equity shares outstanding during the year
95,91,97,790
95,91,97,790
	
Less : Weighted average shares held by ESOP trust as treasury shares
(5,81,225)
(4,76,369)
	
Weighted average number of equi

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

The excerpt includes a section titled 'Contingent Liabilities and Commitments' which indicates that there are performance bonds and other contingent liabilities as of specific dates.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `contingent_liability`

**risk_flag_summary**

The excerpt mentions contingent liabilities, including performance bonds and other unspecified contingent liabilities as of 31.03.2026 and 31.03.2025.

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
| Latency | 2.1024 s |
| Input / output tokens | 785 / 56 |
| Tokens/sec (output) | 26.6 |

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

### Case 13 — `RF_BRITANNIA_AR_BRITANNIA_274`

#### SOURCE / EVIDENCE

- **Symbol:** BRITANNIA
- **Company:** Britannia Industries Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_BRITANNIA_274
- **Polarity:** positive
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
e, the risks specific to the liability. When discounting is used, the increase in 
the provision due to the passage of time is recognised as a finance cost.
	
	
ii.	
Contingent liabilities
	
	
	
A disclosure for contingent liabilities is made where there is a possible obligation or a present obligation 
that may probably not require an outflow of resources. When there is a possible or a present obligation 
where the likelihood of outflow of resources is remote, no provision or disclosure is made.
	
	
iii.	
Onerous contracts
	
	
	
Provision for onerous contracts. i.e. contracts where the expected unavoidable cost of meeting the 
obligations under the contract exceed the economic benefits expected to be received under it, are recognised 
when it is probable that an outflow of resources embodying economic benefits will be required to settle a 
present obligation as a result of an obligating event based on a reliable estimate of such obligation.
	
(o)	
Employee benefits 
	
	
i. 	
Short-term employee benefits
	
	
	
All employee benefits falling due wholly within twelve months of rendering the services are classified 
as short-term employee benefits, which include benefits like salaries, wages, short-term compensated 
absences and performance incentives and are recognised as expenses in the period in which the employee 
renders the related service.
	
	
ii.	
Post-employment benefits
	
	
	
Contributions to defined contribution schemes such as Provident Fund, Pension Fund, etc., are r

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

The excerpt discusses contingent liabilities, stating that a disclosure is made for possible or present obligations that may not require an outflow of resources, while no provision or disclosure is made if the likelihood of outflow is remote.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `contingent_liability`

**risk_flag_summary**

The excerpt discusses contingent liabilities, explaining that a disclosure is made when there is a possible or present obligation that may probably not require an outflow of resources. No provision or disclosure is made if the likelihood of outflow is remote.

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
| Latency | 1.9981 s |
| Input / output tokens | 585 / 62 |
| Tokens/sec (output) | 31.0 |

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

### Case 14 — `RF_DRREDDY_AR_DRREDDY_783`

#### SOURCE / EVIDENCE

- **Symbol:** DRREDDY
- **Company:** Dr. Reddy's Laboratories Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_DRREDDY_783
- **Polarity:** positive
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
elf against the allegations. Any liability that may arise on account of these claims is 
unascertainable at this time. Accordingly, no provision was made in these consolidated financial statements.
Class Action under the Canadian Competition Act filed in Federal Court in Toronto, Canada
On June 03, 2020, a Class Action Statement of Claim was filed by an individual consumer in Federal Court in Toronto, Canada, 
against the Company’s U.S. and Canadian subsidiaries and 52 other generic drug companies. The Statement of Claim alleges 
an industry-wide, overarching conspiracy to violate Sections 45 and 46 of the Canadian Competition Act by conspiring to 
allocate the market, fix prices, and maintain the supply of generic drugs in Canada. The action is brought on behalf of a class of 
all persons, from January 01, 2012 to the present, who purchased generic drugs in the private sector. The Statement of Claim 
states that it seeks damages against all defendants on a joint and several basis, attorney’s fees and costs of investigation 
and prosecution. An Amended Statement of Claim was served on the Company’s U.S. and Canadian subsidiaries on 15 
January 2021 and added an additional 20 generic drug companies. The Amended Statement of Claim also removed the 
identification of defendant companies with conspiracy allegations regarding specific generic drugs and alleges a conspiracy 
to allocate the North America Market as to all generic drugs in Canada. A Second Fresh as Amended Statement 

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

The excerpt discusses a class action lawsuit filed against the company and its subsidiaries, alleging conspiracy to violate competition laws, with potential liabilities that are currently unascertainable. It notes that no provision has been made in the financial statements for these claims.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `contingent_liability`

**risk_flag_summary**

The excerpt discusses a class action lawsuit filed against the company's subsidiaries and other generic drug companies under the Canadian Competition Act. The potential liability from this litigation is uncertain, and no provision has been made in the financial statements.

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
| Latency | 1.999 s |
| Input / output tokens | 626 / 60 |
| Tokens/sec (output) | 30.0 |

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

### Case 15 — `RF_HDFCBANK_AR_HDFCBANK_600`

#### SOURCE / EVIDENCE

- **Symbol:** HDFCBANK
- **Company:** HDFC Bank Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_HDFCBANK_600
- **Polarity:** positive
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
ank.
B	
BASIS OF PREPARATION
	
The standalone financial statements have been prepared 
and presented under the historical cost convention and 
accrual basis of accounting, unless otherwise stated and 
are in accordance with Generally Accepted Accounting 
Principles in India (‘Indian GAAP’), statutory requirements 
prescribed under the Third Schedule of the Banking 
Regulation Act, 1949, directions, circulars, notifications 
and guidelines issued by the Reserve Bank of India (‘RBI’) 
from time to time (RBI guidelines), Accounting Standards 
(‘AS’) specified under Section 133 of the Companies Act, 
2013 read together with the Companies (Accounts) Rules, 
2014 and the Companies (Accounting Standards) Rules, 
2021, in so far as they apply to banks.
	
Use of estimates
	
The preparation of financial statements in conformity with 
Indian GAAP requires the management to make estimates 
and necessary assumptions in the reported amounts of 
assets and liabilities (including contingent liabilities) as 
at the date of the financial statements and the reported 
income and expenses for the reporting year. Management 
believes that the estimates used in the preparation of the 
financial statements are prudent and reasonable. Actual 
results could differ from these estimates. The impact of 
any revision in the accounting estimates is recognised 
prospectively from the period of change.
C	
SIGNIFICANT ACCOUNTING POLICIES
1.	
Investments 
	
The RBI, vide its master direction dated September

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

The excerpt mentions that the preparation of financial statements requires management to make estimates regarding the reported amounts of assets and liabilities, including contingent liabilities.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `contingent_liability`

**risk_flag_summary**

The excerpt mentions that the preparation of financial statements requires management to make estimates and assumptions regarding contingent liabilities as of the financial statement date.

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
| Latency | 1.5525 s |
| Input / output tokens | 633 / 42 |
| Tokens/sec (output) | 27.1 |

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

### Case 16 — `RF_INFY_AR_INFY_174`

#### SOURCE / EVIDENCE

- **Symbol:** INFY
- **Company:** Infosys Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_INFY_174
- **Polarity:** positive
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
on resolution of the disputes, an amount aggregating to ₹86 
crore has been reduced from contingent liabilities.
During fiscal 2025, the Company received orders under Section 
250 of the Income-Tax Act, 1961, from the Income-Tax Authorities 
in India for the assessment years 2016-17 and 2019-20. These 
orders confirmed the Company's position with respect to tax 
treatment of certain matters. As a result, interest income (pre-
tax) of ₹327 crore was recognized and provision for income tax 
aggregating to ₹183 crore was reversed with a corresponding 
credit to the Statement of Profit and Loss. Also, upon resolution 
of the disputes, an amount aggregating to ₹1,068 crore has been 
reduced from contingent liabilities.
6.	 Segmental profitability
The Company’s operations predominantly relate to providing 
end-to-end business solutions to enable clients to enhance 
performance of their business. Business segments of the 
Company are primarily enterprises in Financial Services 
and Insurance; Manufacturing; Retail, Consumer Packaged 
Goods and Logistics; Energy, Utilities, Resources and Services; 
Communication, Telecom OEM and Media; Hi-Tech; Life Sciences 
and Healthcare; and all other segments. All other segments 
represent the operating segments of businesses in India, Japan, 
China, Infosys Public Services and identified enterprises in public 
services. This is discussed in detail in Note 2.26 to the Consolidated 
Financial Statement in this Integrated Annual Report.
Management

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

The excerpt discusses the reduction of amounts from contingent liabilities, specifically mentioning ₹86 crore and ₹1,068 crore that have been reduced upon resolution of disputes.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `contingent_liability`

**risk_flag_summary**

The company reduced contingent liabilities by ₹86 crore and ₹1,068 crore upon resolution of disputes related to tax treatment matters.

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
| Latency | 1.6313 s |
| Input / output tokens | 669 / 44 |
| Tokens/sec (output) | 27.0 |

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

### Case 17 — `RF_MANKIND_AR_MANKIND_503`

#### SOURCE / EVIDENCE

- **Symbol:** MANKIND
- **Company:** Mankind Pharma Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_MANKIND_503
- **Polarity:** positive
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
imited
 - 
 - 
 - 
 - 
 - 
 - 
 - 
 - 
 - 
 - 
Appian Properties Private 
Limited
 - 
 - 
 - 
 - 
 - 
 - 
 - 
 - 
 - 
 - 
Mediforce Healthcare 
Private Limited
 - 
 - 
 - 
 - 
 - 
 - 
 - 
 - 
 - 
 - 
 - 
 - 
 - 
 - 
 - 
 - 
 - 
 - 
Mankind Pharma Limited  Annual Report 2024-25
Financial statements
Statutory reports
Corporate overview
Notes to the Standalone Financial Statements 
for the year ended March 31, 2025 
 All amounts are in INR crores unless otherwise stated
Notes to the Standalone Financial Statements 
for the year ended March 31, 2025 
 All amounts are in INR crores unless otherwise stated
Particulars of 
investments
As at March 31, 2025
As at March 31, 2024
Investments 
made/ 
(withdrawn)/ 
adjustments
Outstanding 
balance
Maximum 
amount 
outstanding
Investments 
made/ 
(withdrawn)/ 
adjustments
Outstanding 
balance
Maximum 
amount 
outstanding
Sirmour Remedies Private 
Limited
 - 
 - 
Mankind Prime Labs 
Private Limited
 - 
 - 
Lifestar Pharmaceuticals 
Private Limited
Mankind Life Sciences 
Private Limited
 - 
Appify Infotech LLP
Mankind Petcare Private 
Limited (formerly known 
as Mankind Consumer 
Healthcare Private 
Limited)
Mankind Pharma FZ LLC
Mankind Agritech Private 
Limited
 - 
Mankind Medicare Private 
Limited
Mankind Consumer 
Products Private Limited
 - 
 - 
 - 
Packtime Innovations 
Private Limited
 - 
Total
Less : Provision for the 
impairment in the value of 
investment
Total
Notes:
a)	
During the previous year, advance to North East Pharma Pack

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

The excerpt mentions financial guarantees given as of March 31, 2025, which may indicate the presence of contingent liabilities.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `contingent_liability`

**risk_flag_summary**

The excerpt mentions financial guarantees given by the company as of March 31, 2025, and March 31, 2024.

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
| Latency | 1.976 s |
| Input / output tokens | 808 / 50 |
| Tokens/sec (output) | 25.3 |

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

### Case 18 — `RF_ONGC_AR_ONGC_1293`

#### SOURCE / EVIDENCE

- **Symbol:** ONGC
- **Company:** Oil & Natural Gas Corporation Limited
- **Fiscal year:** FY2026
- **Doc type:** annual_report
- **Chunk id:** AR_ONGC_1293
- **Polarity:** positive
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
er 27, 2025, wherein most 
of the grounds were decided in favour of the Company. An 
application has also been filed to give effect to the said 
CIT(A) order. Based on the disallowances made in the 
assessment order, the AO had earlier raised a tax demand 
of `11,676.43 million. However, since the CIT(A) has 
substantially decided the matter in favour of the Company, 
the demand raised by the AO would be reduced to Nil 
and accordingly, no continent liability has been reported 
against the said demand. For the assessment year 2018-
19, the AO had made certain disallowances amounting to 
` 656.70 million in the Assessment order against which 
appeal was filed before CIT (A) by the Company, which is 
pending for disposal. Since no demand was raised by the 
AO on completion of assessment, no contingent liability 
has been reported. For the assessment year 2020-21, 
the AO had made certain disallowances amounting to ` 
1,011.71 million in the Assessment order against which 
appeal was filed before CIT (A) by the Company, which is 
pending for disposal. Since no demand was raised by the 
AO on completion of assessment, no contingent liability 
has been reported.
57.1.9	 	The Service Tax Department had issued a total of 8 demand 
cum show-cause notices on similar contentions requiring 
the Company to show cause why service tax totaling to 
` 78,779.90 million (including Education Cess and SHE 
Cess), the interest on such amount and penalty should not 
be demanded and recovered from

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

The excerpt discusses the absence of contingent liabilities reported by the Company regarding tax demands raised by the Assessment Officer, as the matters are pending appeal and no demands were made upon completion of assessments.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `contingent_liability`

**risk_flag_summary**

The excerpt discusses tax demands and pending appeals where no contingent liability has been reported due to the Company's favorable rulings and pending assessments.

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
| Latency | 1.5871 s |
| Input / output tokens | 678 / 42 |
| Tokens/sec (output) | 26.5 |

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

### Case 19 — `RF_POWERGRID_AR_POWERGRID_690`

#### SOURCE / EVIDENCE

- **Symbol:** POWERGRID
- **Company:** Power Grid Corporation of India Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_POWERGRID_690
- **Polarity:** positive
- **Keyword candidates:** `auditor_qualification, contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
ess of 
related disclosures in the standalone financial 
statements.
Assessment of Contingent liabilities in respect of 
certain litigations including land compensation, 
direct and indirect taxes, various claims filed by 
other parties not acknowledged as debt. 
There is a high level of judgement required 
in 
estimating 
the 
contingent 
liabilities. 
The 
Company’s assessment of contingent liabilities is 
supported by the facts of the matter, Company’s 
judgement thereon, past experience and advices 
from legal and independent tax consultants 
wherever necessary.
We identified the above area as Key Audit Matter 
in view of associated uncertainty relating to the 
outcome of these matters.
(Refer Note No. 58 of Standalone Financial 
Statements)
We have obtained an understanding of the 
Company’s procedure in respect of estimation and 
disclosure of contingent liabilities and adopted the 
following audit procedures:
	

Reviewed the current status and material 
developments of legal matters.
	

Reviewed the legal and other professional 
expenses and enquired with the management 
for recent developments and the status of the 
material litigations.
	

Performed our assessment on a test basis 
on the underlying calculations supporting 
the 
contingent 
liabilities/other 
significant 
litigations disclosed in the Standalone Financial 
Statements.
	

Examined 
recent 
orders 
from 
competent 
authorities and/ or communication received 
from various authorities, judicial forums 

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

The excerpt discusses the assessment of contingent liabilities related to certain litigations, including land compensation and various claims. It highlights the judgment required in estimating these liabilities and the audit procedures performed to review their status and disclosures.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `contingent_liability`

**risk_flag_summary**

The excerpt discusses the assessment of contingent liabilities related to litigations, land compensation, taxes, and claims, noting the high level of judgment required and the support from legal and tax consultants. The audit procedures reviewed the status of legal matters and evaluated disclosures in the financial statements.

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
| Latency | 2.2366 s |
| Input / output tokens | 598 / 71 |
| Tokens/sec (output) | 31.7 |

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

### Case 20 — `RF_TCS_AR_TCS_343`

#### SOURCE / EVIDENCE

- **Symbol:** TCS
- **Company:** Tata Consultancy Services Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_TCS_343
- **Polarity:** positive
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
ge 
exchange rates. Translation adjustments have been reported 
as foreign currency translation reserve in the statement of 
changes in equity. When a foreign operation is disposed 
off in its entirety or partially such that control, significant 
Notes forming part of Consolidated Financial Statements
Integrated Annual Report 2024-25
Notes forming part of Consolidated Financial Statements
Consolidated Financial Statements 2024-25
influence or joint control is lost, the cumulative amount 
of exchange differences related to that foreign operation 
recognised in OCI is reclassified to statement of profit and 
loss as part of the gain or loss on disposal.
5)	
Use of estimates and judgements
	
The preparation of consolidated financial statements in 
conformity with the recognition and measurement principles 
of Ind AS requires management of the Group to make 
estimates and judgements that affect the reported balances 
of assets and liabilities, disclosures of contingent liabilities 
as at the date of consolidated financial statements and the 
reported amounts of income and expenses for the periods 
presented.
	
Estimates and underlying assumptions are reviewed on 
an ongoing basis. Revisions to accounting estimates are 
recognised in the period in which the estimates are revised 
and future periods are affected.
	
The Group uses the following critical accounting judgements, 
estimates and assumptions in preparation of its consolidated 
financial statements:
	
(a)	 Revenue recognit

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

The excerpt discusses the preparation of consolidated financial statements and mentions the disclosures of contingent liabilities as part of the reported balances of assets and liabilities.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `contingent_liability`

**risk_flag_summary**

The excerpt mentions disclosures of contingent liabilities as at the date of consolidated financial statements.

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
| Latency | 1.2247 s |
| Input / output tokens | 567 / 32 |
| Tokens/sec (output) | 26.1 |

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

### Case 21 — `RF_ABB_AR_ABB_122`

#### SOURCE / EVIDENCE

- **Symbol:** ABB
- **Company:** ABB India Limited
- **Fiscal year:** FY2026
- **Doc type:** annual_report
- **Chunk id:** AR_ABB_122
- **Polarity:** positive
- **Keyword candidates:** `related_party_transaction`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
vernance reports under Regulation 
27(2) are accurate and specific which re-directs to the relevant document(s)/ 
section of the website
Yes
None
4)
Disqualification of Director:
None of the Directors of the Company are disqualified under Section 164 of 
Companies Act, 2013, as confirmed by the listed entity.
Yes
None
ANNEXURE- C
WE HEREBY REPORT THAT, DURING THE REVIEW PERIOD, THE COMPLIANCE 
STATUS OF THE LISTED ENTITY IS AS GIVEN HEREUNDER:
Boards’ Report
Sr. 
No. Particulars
Compliance status 
(Yes/No/NA)
Observations / 
Remarks by PCS
5)
Details related to Subsidiaries of listed entities have been examined w.r.t., 
a)	 Identification of material subsidiary companies
b)	 Requirements with respect to disclosure of material as well as other 
subsidiaries
Yes
None
6)
Preservation of Documents:
The listed entity is preserving and maintaining records as prescribed under SEBI 
Regulations and disposal/archival of records is being carried out as per Policy 
of Preservation of Documents and Archival policy prescribed under SEBI Listing 
Regulations. 
Yes
None
7)
Performance Evaluation:
The listed entity has conducted performance evaluation of the Board, 
Independent Directors and the Committees at the start of every financial year/
during the financial year as prescribed in SEBI Regulations
Yes
None
8)
Related Party Transactions:
a)	 The listed entity has obtained prior approval of Audit Committee for all 
Related party transactions, or
b)	 The Listed entity has provided detailed

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `related_party_transaction`

**risk_flag_summary**

The listed entity has obtained prior approval of the Audit Committee for all related party transactions and provided detailed reasons regarding the approval status of transactions that did not receive prior approval.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `related_party_transaction`

**risk_flag_summary**

The listed entity has obtained prior approval of the Audit Committee for all related party transactions or provided detailed reasons and confirmation of subsequent approval, rejection, or ratification by the Audit Committee if no prior approval was obtained.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `related_party_transaction` |
| Category — Qwen | `related_party_transaction` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.9177 s |
| Input / output tokens | 646 / 56 |
| Tokens/sec (output) | 29.2 |

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

### Case 22 — `RF_ADANIPOWER_AR_ADANIPOWER_841`

#### SOURCE / EVIDENCE

- **Symbol:** ADANIPOWER
- **Company:** Adani Power Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_ADANIPOWER_841
- **Polarity:** positive
- **Keyword candidates:** `related_party_transaction`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
ited
Kodad Khammam Road Private Limited
75	 Related party transactions (Contd...)
Notes to Consolidated Financial Statements 
for the year ended March 31, 2025
Integrated Annual Report 2024-25
ADANI POWER LIMITED
Description of Relationship
Name of Related Parties
Entities over which one 
or more Key Management 
Personnel (“KMP”) or their 
relatives have significant 
influence  / control / joint 
control; entities having 
significant influence over the 
Company have significant 
influence / control / joint 
control through voting power 
or otherwise
Kurmitar Iron Ore Mining Private Limited
Kutch Copper Limited
Kutch Copper Tubes Limited
Lucknow International Airport Limited
Mahanadi Mines and Minerals Private Limited
Maharashtra Border Check Post Network Limited
Maharashtra Eastern Grid Power Transmission Company Limited
Mancherial Repallewada Road Private Limited
Mangaluru International Airport Limited
Marine Infrastructure Developer Private Limited
MH Natural Resources Private Limited
Mining Tech Consultancy Services Limited (formerly known as Mining 
Tech Consultancy Services Private Limited)
MP Natural Resources Private Limited
MP Power Transmission Package-II Limited
MPSEZ Utilities Limited
Mumbai International Airport Limited
Mundra International Airport Limited (formerly known as Mundra 
International Airport Private Limited)
Mundra Petrochem Limited
Mundra Solar Energy Limited
Mundra Solar PV Limited
Mundra Solar Technology Limited
Nanasa Pidgaon Road Private Limited


… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `related_party_transaction`

**risk_flag_summary**

The excerpt discusses related party transactions involving various entities that have significant influence or control over the company, as noted in the consolidated financial statements.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `related_party_transaction`

**risk_flag_summary**

The excerpt lists multiple entities that are related parties to Adani Power Limited, including companies with which the company has significant influence or control, or that have significant influence over the company.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `related_party_transaction` |
| Category — Qwen | `related_party_transaction` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.7198 s |
| Input / output tokens | 624 / 50 |
| Tokens/sec (output) | 29.1 |

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

### Case 23 — `RF_BAJFINANCE_AR_BAJFINANCE_288`

#### SOURCE / EVIDENCE

- **Symbol:** BAJFINANCE
- **Company:** Bajaj Finance Limited
- **Fiscal year:** FY2026
- **Doc type:** annual_report
- **Chunk id:** AR_BAJFINANCE_288
- **Polarity:** positive
- **Keyword candidates:** `related_party_transaction`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
 directors. Members of the Committee have necessary accounting or financial 
management related expertise and are considered financially literate in terms of the SEBI Listing Regulations.
The terms of reference (hereinafter in this report referred as “ToR”) of the Committee are in accordance with 
the Act, SEBI Listing Regulations and RBI Directions. The Board reviews the working of the Committee from 
time to time to bring about greater effectiveness and to ensure compliance with the various requirements 
under the Act, SEBI Listing Regulations and RBI Directions. The ToR of the Committee was reviewed during the 
year. The Matters pertaining to Artificial Intelligence and data privacy governance were added to the ToR. The 
ToR can be accessed at https://www.bajajfinserv.in/content/dam/bajajfinserv/web/in/en/global/document/
corporate/bfl-new/bfl-investor-relations/shareholders-information/terms-of-reference/terms-of-reference-
of-audit-committee.pdfe.
Broadly the key terms of reference of the Committee are as under:
Particulars
Periodicity
Oversight of financial reporting process:
Review of financial results/statements & Auditor’s Report
Quarterly
Reviewing with the management Changes, if any, in accounting policies and practices
Annually
Discussion with the Auditors on items of significant judgement, Audit Plan, matter of 
emphasis, if any
Quarterly / Annually
Oversight of Related Party & its transaction:
Approval or any subsequent modification of transactions with related 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `related_party_transaction`

**risk_flag_summary**

The excerpt discusses the oversight of related party transactions by the Committee, including the approval and review of such transactions on an annual and quarterly basis.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `related_party_transaction`

**risk_flag_summary**

The excerpt mentions oversight of related party transactions, including approval of transactions with related parties and quarterly reviews of such transactions.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `related_party_transaction` |
| Category — Qwen | `related_party_transaction` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.3874 s |
| Input / output tokens | 601 / 37 |
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

### Case 24 — `RF_CIPLA_AR_CIPLA_391`

#### SOURCE / EVIDENCE

- **Symbol:** CIPLA
- **Company:** Cipla Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_CIPLA_391
- **Polarity:** positive
- **Keyword candidates:** `auditor_qualification, related_party_transaction`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
ndards, laws and regulations. 
The Audit Committee regularly received updates and 
confirmations regarding the corrective actions taken 
to further strengthen the controls within the Company’s 
internal financial control framework. These updates 
were further supported by reviews conducted by the 
Internal Audit team and the Statutory Auditors, who 
offer additional assurance to the Committee on the 
effectiveness of these controls. The Committee affirms 
that there was no material weakness in the Company’s 
internal financial control system.
IX.	 Vigil Mechanism and POSH:
	
During the year, the Committee reviewed functioning 
of the whistle blower mechanism and the mechanism 
for Prevention of Sexual Harassment (‘POSH’) at the 
workplace and noted that the complaints received 
were investigated and appropriate actions were taken/
being taken wherever necessary. No person was denied 
access to the Chairman of the Audit Committee and 
the Committee was assured that none of the whistle 
blowers were victimised. The Committee also reviewed 
the system for identification and rectification of data 
integrity concerns and noted that effective mitigation 
measures were in place. 
X.	
Related Party Transactions:
	
The Committee (i) approved all related party 
transactions, as per the Company’s Policy on Related 
Party Transactions (‘RPT Policy’) and (ii) reviewed the 
related party transactions entered on a quarterly 
basis. Majority of the transactions were between the 
Company and 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `related_party_transaction`

**risk_flag_summary**

The Audit Committee approved all related party transactions in accordance with the Company’s Policy on Related Party Transactions and reviewed them quarterly. The transactions were conducted in the ordinary course of business and at arm’s length, with approvals granted only by independent directors.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `related_party_transaction`

**risk_flag_summary**

The Audit Committee approved all related party transactions in accordance with the Company’s RPT Policy, reviewed them quarterly, and ensured they were conducted at arm’s length. The transactions were approved by independent directors and were not material during the year.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `related_party_transaction` |
| Category — Qwen | `related_party_transaction` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.981 s |
| Input / output tokens | 589 / 61 |
| Tokens/sec (output) | 30.8 |

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

### Case 25 — `RF_EICHERMOT_AR_EICHERMOT_742`

#### SOURCE / EVIDENCE

- **Symbol:** EICHERMOT
- **Company:** Eicher Motors Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_EICHERMOT_742
- **Polarity:** positive
- **Keyword candidates:** `related_party_transaction`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
dated November 22, 2021, are as follows:
Sl. No.
Particulars
Details
Name of the related party and its 
relationship with the listed entity or its 
subsidiary, including nature of its concern 
or interest (financial or otherwise)
VE Commercial Vehicles Limited (VECV) is a joint venture company between Aktiebolaget 
Volvo (PUBL), Sweden and the Company. VECV is an unlisted material subsidiary of 
the Company and the Company holds 54.40% of equity share capital of VECV and the 
remaining 45.60% of the equity share capital of VECV is held by Aktiebolaget Volvo 
(PUBL), Sweden and Volvo Truck Corporation, Sweden. Accordingly, VECV is a related party 
of the Company in terms of Regulation 2(1)(zb) of the SEBI Listing Regulations and section 
2(76) of the Companies Act, 2013.
Volvo Group India Private Limited (VGIPL) is an unlisted private limited company and is 
part of Volvo Group of Companies.
VECV and VGIPL are related parties pursuant to Regulation 2(1)(zb) of the SEBI Listing 
Regulations.
Type, material terms and particulars of the 
proposed transaction;
VECV has undertaken and continues to undertake various related party transactions 
(“RPTs”) with VGIPL. The RPTs involve:
(i) 	
Purchase of goods;
(ii) 	 Purchase of capital goods (demo trucks and tech tools) /services;
(iii) 	 Sale of finished goods/services;
(iv) 	 Incentives on part sales, expenses recovered;
(v) 	 Reimbursement of expenses, purchase consideration and other related transactions.
The RPTs are at arm’s leng

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `related_party_transaction`

**risk_flag_summary**

The excerpt discusses various related party transactions between VE Commercial Vehicles Limited (VECV) and Volvo Group India Private Limited (VGIPL), including the purchase and sale of goods and services. It states that these transactions are at arm's length and in the ordinary course of business.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `related_party_transaction`

**risk_flag_summary**

The excerpt discusses transactions between VECV, a joint venture subsidiary of the company, and VGIPL, part of the Volvo Group. These transactions include purchases, sales, and reimbursements, occurring at arm's length and in the ordinary course of business.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `related_party_transaction` |
| Category — Qwen | `related_party_transaction` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 2.2586 s |
| Input / output tokens | 708 / 66 |
| Tokens/sec (output) | 29.2 |

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

### Case 26 — `RF_HINDALCO_AR_HINDALCO_1460`

#### SOURCE / EVIDENCE

- **Symbol:** HINDALCO
- **Company:** Hindalco Industries Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_HINDALCO_1460
- **Polarity:** positive
- **Keyword candidates:** `related_party_transaction`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
tions.
18.	Other Income
	
Interest Income
	
Interest income from a financial asset is recognised when it is probable that the economic benefits will flow to the 
Company and the amount of income can be measured reliably. Interest income is accrued on a time proportion basis, by 
reference to the principal outstanding and at the effective interest rate applicable, which is the rate that exactly discounts 
estimated future cash receipts through the expected life of the financial asset to that asset’s net carrying amount on initial 
recognition.
	
(` Crore)
	
Year ended
31/03/2026
31/03/2025
Interest Income, (Refer Note - 33(a)(iii))
On Non-Current Investments
On Current Investments
On Others
Dividend Income, (Refer Note - 33(a)(iii))
On Non-Current Investments - (d)
Rent Income
Income from Government Grants (c)
Gain/ (Loss) on Property, Plant and Equipment, Asset held for sale and Intangible Assets 
sold/ discarded (Net) (b)
Gain/ (Loss) on Investments Measured at FVTPL (Net)
On sale of Financial Assets
On change of Fair Value of Financial Assets
Other Non-Operating Income - (a)
(a)	
Includes gain on modification of borrowings ` 108 Crore (year ended 31/03/2025 ` 50 Crore) resulting from change in 
benchmark interest rate and timing of expected cash flows on term loans.
(b)	
During the previous year, the Company signed Conveyance and Development Agreement (“agreement”) with a buyer 
for sale of land situated in Kalwa, Maharashtra, the Company had recognised ` 571 Crore (discoun

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `related_party_transaction`

**risk_flag_summary**

The excerpt references Note 30 for related party transactions, indicating that there are transactions disclosed with related parties.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `related_party_transaction`

**risk_flag_summary**

The excerpt mentions that details of related party transactions can be found in Note 30.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `related_party_transaction` |
| Category — Qwen | `related_party_transaction` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.3745 s |
| Input / output tokens | 698 / 32 |
| Tokens/sec (output) | 23.3 |

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

### Case 27 — `RF_JIOFIN_AR_JIOFIN_154`

#### SOURCE / EVIDENCE

- **Symbol:** JIOFIN
- **Company:** Jio Financial Services Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_JIOFIN_154
- **Polarity:** positive
- **Keyword candidates:** `related_party_transaction`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
xecutive Officer of the Company, effective from the date of approval 
of Reserve Bank of India.
e. Alteration of Articles of Association of the Company.
Held through video 
conference/other audio-
visual means
(Deemed venue – 9th 
Floor, Maker Chambers 
IV, 222, Nariman Point, 
Mumbai - 400 021)
August 2, 2022
11:30 a.m.
No special resolution was passed.
Held through video 
conference/other audio-
visual means
(Deemed venue – 9th 
Floor, Maker Chambers 
IV, 222, Nariman Point, 
Mumbai - 400 021)
All the resolutions moved at the last three (3) AGMs were passed by the Members.
Resolutions passed through Postal Ballot
During the FY2024-25, members of the Company approved the resolutions, stated in the table below by requisite majority, through postal 
ballot:
Date of Postal 
Ballot Notice
Resolution passed through Postal 
Ballot
Votes in favour/against 
the resolution (% of total 
number of valid votes)
Approval date
Date of Scrutinizer 
Report
May 18, 2024
Alteration of the Objects Clause of the 
Memorandum of Association of the 
Company (Special Resolution)
Votes in favour: 99.9426%
Votes against: 0.0574%
June 22, 2024
June 24, 2024
Material Related Party Transactions of 
subsidiaries of the Company (Ordinary 
Resolution)
Votes in favour: 99.9906%
Votes against: 0.0094%
Foreign investments (including foreign 
portfolio investments) in the equity share 
capital of the Company up to 49% (forty 
nine percent) of the paid-up equity share 
capital of the Company (post conversion 
a

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `related_party_transaction`

**risk_flag_summary**

The excerpt mentions the approval of material related party transactions of subsidiaries of the Company through a postal ballot resolution.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `related_party_transaction`

**risk_flag_summary**

The excerpt mentions the approval of Material Related Party Transactions of subsidiaries of the Company through a postal ballot, which was passed by members with a high percentage of votes in favor.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `related_party_transaction` |
| Category — Qwen | `related_party_transaction` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.8931 s |
| Input / output tokens | 778 / 48 |
| Tokens/sec (output) | 25.4 |

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

### Case 28 — `RF_MAZDOCK_AR_MAZDOCK_154`

#### SOURCE / EVIDENCE

- **Symbol:** MAZDOCK
- **Company:** Mazagon Dock Shipbuilders Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_MAZDOCK_154
- **Polarity:** positive
- **Keyword candidates:** `related_party_transaction`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
gularity or a 
failure of Internal Control Systems of 
a material nature and reporting the 
matter to the Board; 
xvii.	 Review observations of statutory, 
internal & government auditors and 
provide recommendations based on 
the same; 
xviii.	 To review the follow up action on 
the audit observations of the C&AG 
audit; 
xix.	
discussion with Statutory Auditors 
before the audit commences, about 
the nature and scope of audit as well 
as post-audit discussion to ascertain 
any area of concern; 
xx.	
To 
look 
into 
the 
reasons 
for 
substantial defaults in the payment 
of 
the 
Depositors, 
Debenture 
holders, Shareholders (in case of non-
payment of declared dividend and 
creditors); 
xxi.	
To review the functioning of the 
Whistle Blower Mechanism;
xxii.	 Approval of appointment of Chief 
Financial 
Officer 
after 
assessing 
the qualifications, experience and 
background etc., of the candidate;
xxiii.	 Review and monitor the Auditor’s 
independence and performance and 
effectiveness of audit process; 
xxiv.	 Examination 
of 
the 
Financial 
Statements and Auditor’s Report 
thereon; 
xxv.	 Carrying out any other function or 
matter that may be referred to the 
Audit Committee by the Board from 
time to time; 
xxvi.	 Reviewing the utilisation of loans and/ 
or advances from/ investment by the 
holding company in the subsidiary 
exceeding ₹100 crores or 10% of the 
asset size of the subsidiary, which-
ever is lower including existing loans/ 
advances/ investments existing a

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `related_party_transaction`

**risk_flag_summary**

The excerpt mentions the review of significant related party transactions as defined by the Audit Committee, which is submitted by management.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `related_party_transaction`

**risk_flag_summary**

The excerpt mentions the review of statement of significant related party transactions submitted by management.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `related_party_transaction` |
| Category — Qwen | `related_party_transaction` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.2857 s |
| Input / output tokens | 674 / 30 |
| Tokens/sec (output) | 23.3 |

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

### Case 29 — `RF_POWERGRID_AR_POWERGRID_609`

#### SOURCE / EVIDENCE

- **Symbol:** POWERGRID
- **Company:** Power Grid Corporation of India Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_POWERGRID_609
- **Polarity:** positive
- **Keyword candidates:** `related_party_transaction`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
una Transmission Limited
Powergrid Ajmer Phagi Transmission Limited
Powergrid Fatehgarh Transmission Limited
Powergrid Rampur Sambhal Transmission Limited
Powergrid Meerut Simbhavali Transmission Limited
 - 
Central Transmission Utility of India Limited
Powergrid Himachal Transmission Limited
Powergrid Bikaner Transmission System Limited
Powergrid Sikar Transmission Limited
 - 
Powergrid Aligarh Sikar Transmission Limited
 - 
Powergrid Teleservices Limited
Powergrid Energy Services Limited
 - 
Powergrid Gomti Yamuna Transmission Limited
 - 
Powergrid Neemuch Transmission System Limited
Powergrid ER NER Transmission Limited
 - 
Powergrid KPS3 Transmission Limited
 - 
Total
Joint Ventures
 
 
Powerlinks Transmission Limited
Torrent Power Grid Limited
 - 
Parbati Koldam Transmission Company Limited
Sikkim Power Transmission Limited
 - 
North East Transmission Company Limited
Bihar Grid Company Limited
 - 
Cross Border Power Transmission Company Limited
Power Transmission Company Nepal Limited
Total
Associates
 
 
Kala Amb Transmission Limited 
 - 
Jabalpur Power Transmission Limited
 - 
Warora Transmission Limited
 - 
Parli Power Transmission Limited
 - 
Total
 - 
Other Related Parties
 
 
POWERGRID Infrastructure Investment Trust
Total
Dividend Income
 
 
 
Other Income
 
 
Subsidiaries
 
 
Powergrid Unchahar Transmission Limited
Powergrid Narela Transmission Limited
 - 
Powergrid Ramgarh Transmission Limited
 - 
Powergrid Khavda II-C Transmission Limited
 - 
Powergrid Bhadla S

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `related_party_transaction`

**risk_flag_summary**

The excerpt discusses various entities and joint ventures related to Powergrid, including disclosures as per Ind AS 24 regarding related party transactions.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `related_party_transaction`

**risk_flag_summary**

The excerpt lists various entities under different categories such as Joint Ventures, Associates, Other Related Parties, and Subsidiaries, indicating a structured disclosure of related party transactions as per Ind AS 24.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `related_party_transaction` |
| Category — Qwen | `related_party_transaction` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.8964 s |
| Input / output tokens | 652 / 55 |
| Tokens/sec (output) | 29.0 |

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

### Case 30 — `RF_SUNPHARMA_AR_SUNPHARMA_150`

#### SOURCE / EVIDENCE

- **Symbol:** SUNPHARMA
- **Company:** Sun Pharmaceutical Industries Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_SUNPHARMA_150
- **Polarity:** positive
- **Keyword candidates:** `related_party_transaction`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
 a member effective from 22 May 2025.
3.	 Mr. Sudhir Valia ceased to be a member due to his retirement from the Board effective from 31 July 2025.
4.	
Mr. C. S. Muralidharan superannuated effective from 01 July 2025.
4.6	Corporate Governance and ESG Committee (“CGESGC”)
	
The CGESGC is established to enhance the Company's corporate governance initiatives, oversee its policies and practices 
regarding related party transactions and monitor the Company's ESG and sustainability compliance. The CGESGC reports 
to the Audit Committee on matters concerning related party transactions.
	
The terms of reference of the CGESGC, inter alia, include, reviewing compliance with the Company’s Global Code 
of Conduct and Legal Compliance Policy; reviewing and recommending the best corporate governance practices; 
formulating, reviewing and implementing Policy on Materiality and Dealing with Related Party Transactions; providing 
guidance, reviewing and monitoring ESG strategies, goals and initiatives; overseeing the identification of risks and 
opportunities relating to sustainability; monitoring compliances with various guidelines applicable to the Company etc.
Corporate Governance Report
Advancing Innovation Globally for Better Patient Care
Statutory Reports
Corporate Overview
Financial Statements
	
Meetings and Composition:
	
Five meetings of the CGESGC were held during the financial year ended 31 March 2026 on 21 May 2025, 30 July 2025, 
04 November 2025, 30 January 2026 and 23 March 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `related_party_transaction`

**risk_flag_summary**

The Corporate Governance and ESG Committee is responsible for overseeing the Company's policies and practices regarding related party transactions and ensuring compliance with related guidelines.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

<details><summary>Rejected attempts</summary>

- pass 1: summary failed compliance: forward-tense word 'recommends'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `related_party_transaction` |
| Category — Qwen | `— (no flag)` |
| Outcome | **false_negative** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 2.229 s |
| Input / output tokens | 691 / 66 |
| Tokens/sec (output) | 29.6 |

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

### Case 31 — `RF_ADANIENT_AR_ADANIENT_926`

#### SOURCE / EVIDENCE

- **Symbol:** ADANIENT
- **Company:** Adani Enterprises Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_ADANIENT_926
- **Polarity:** positive
- **Keyword candidates:** `promoter_pledge`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
f 1 year 
MCLR+5BPS p.a. aggregating to ` 133.93 crore(Previous year: ` Nil). First pari passu charge by way of 
hypothecation of all movable assets of the Company including, but not limited to plant & machinery, 
spares tools & accessories, current assets of the Company. First pari passu charge on all rights, title, 
interests, benefits, claims and demands whatesover of the Company with respect to the insurance 
contracs, all money receivables under the insured assets of the Company. First pari passu floatng 
charge on book debts, operating cash flows, receivables, commissions, revenue of whatsover nature.
23.	Non-Current Borrowings (Contd.)
23.	Non-Current Borrowings (Contd.)
Notes forming part of the Consolidated Financial Statements
for the year ended March 31, 2026
Notes forming part of the Consolidated Financial Statements
for the year ended March 31, 2026
Portfolio  
Overview
Corporate 
Overview
Strategic 
Review
ESG 
Overview
Statutory 
Reports
Financial 
Statements
ADANI ENTERPRISES LIMITED
Integrated Annual Report 2025-26
	
	
	
First pari passu charge on all the bank accounts of the Company. Pledge of shares to the extent of 
51% of the total paid up equity shares of the company subject to complianc of section 19(2),(3) of 
the Banking Regulation Acrore 1949, and Non Discloure Undertaking (NDU) of the remailng shares. 
Stand by Letter of Credit from a reputable overseas bank, to the satisfaction of the Lender for 40 % of 
facility amount including interest and othe

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The excerpt discusses the pledge of shares amounting to 51% of the total paid-up equity shares of the company, subject to compliance with specific regulations and a Non-Disclosure Undertaking for the remaining shares.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The excerpt mentions the pledge of 51% of the company's total paid-up equity shares as a security measure, subject to compliance with specific legal provisions and a non-disclosure undertaking for the remaining shares.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `promoter_pledge` |
| Category — Qwen | `promoter_pledge` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 2.0069 s |
| Input / output tokens | 697 / 57 |
| Tokens/sec (output) | 28.4 |

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

### Case 32 — `RF_ADANIGREEN_AR_ADANIGREEN_788`

#### SOURCE / EVIDENCE

- **Symbol:** ADANIGREEN
- **Company:** Adani Green Energy Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_ADANIGREEN_788
- **Polarity:** positive
- **Keyword candidates:** `promoter_pledge`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
ni Solar Energy Jodhpur Four Private Limited (ASEJ4L)
Rupee Term Loan from Bank aggregating ` 240 crore (Previous year ` 256 crore) is secured or to be secured by first 
charge on entire movable assets both present and future including inventory, receivables, machinery spares and all other 
movable properties of the borrower and mortgage and charge on all present and future immovable properties, both 
freehold and leasehold land of the company and is further secured by pledge 51% of total paid up equity share capital and 
Non-Disposal Under Taking from the sponsor for the balance 49% shareholding held by Adani Energy Holdings Limited 
(Formerly known as SB Energy Holdings Limited) ("the Holding Company") . The facilities are repayable in 78 structured 
quarterly instalments. Borrowing carry an interest rate range of 9.40% to 10.30% p.a. on Rupee term loan.
19.	Financial Liabilities: Borrowings (Contd.)
Portfolio Overview
Financial Statements
Statutory Reports
ESG Overview
Strategic Review
Corporate Overview
Notes to Consolidated Financial Statements
as at March 31, 2025
All amounts are in ` crore, unless otherwise stated
Adani Solar Energy RJ Two Private Limited (ASERJ2PL)
Rupee term loan from a Financial Institution of Nil (Previous year ` 732 crore) is secured by first charge by way of 
mortgage of Borrower’s all immovable properties, present and future including the Project Land, movable properties, 
pertaining to the Project, including plant and machinery, machinery spare

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The excerpt discusses the pledge of 51% of the total paid-up equity share capital as security for a term loan, along with a non-disposal undertaking for the remaining 49% shareholding held by the holding company.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The excerpt mentions a pledge of 51% of the total paid-up equity share capital and a non-disposal undertaking from the sponsor for the balance 49% shareholding held by the Holding Company.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `promoter_pledge` |
| Category — Qwen | `promoter_pledge` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.9616 s |
| Input / output tokens | 658 / 57 |
| Tokens/sec (output) | 29.1 |

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

### Case 33 — `RF_IRFC_AR_IRFC_264`

#### SOURCE / EVIDENCE

- **Symbol:** IRFC
- **Company:** Indian Railway Finance Corporation Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_IRFC_264
- **Polarity:** positive
- **Keyword candidates:** `promoter_pledge`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```

-
(a)
(i)	
Individual-
Holding Nom. Val. 
upto H 1 lakhs
 
(ii)	 Individual-
Holding Nom. Val. 
greater then H 1 
lakhs
-
-
(0.57) 
(b)
Nbfc Registered with 
RBI
-
-
-
-
-
-
-
-
-
Annual Report 2024-25
Category of Shareholder
No. of shares held at the beginning  
of the year i.e., 01.04.2024
No. of shares held at the end of  
the year i.e., 31.03.2025
% Change 
during the 
year
Demat 
Physical 
Total
Total % 
of shares
Demat 
Physical 
Total
Total % of 
shares
(c)
Employees Trust
-
-
-
-
-
-
-
-
-
(d)
Overseas Depository 
Holding DRs
-
-
-
-
-
-
-
-
-
(e)
Any Other- Key 
Managerial Personnel 
(KMP)
-
-
Other - Body Corp
-
-
(0.09)
Other - Trusts
-
-
Other - Clearing 
Member
-
-
Other - N R I - Non - 
Repatriable
-
-
Other - N R I - 
Repatriable
-
-
(0.01)
Other - Individual 
HUF
-
-
(0.05)
Other - QIB
-
-
-
-
-
-
-
-
-
Other-Foreign 
Nationals
-
-
-
Sub-total (B)(3)
(0.36)
Total Public 
Shareholding
-
(C) 
Shares held by 
custodians
-
-
-
-
-
-
-
-
-
GRAND TOTAL 
(A+B+C):
1250 13068506000
-
Sr. No.
Shareholder’s name
Shareholding at the beginning of the year
Shareholding at the end of the year
% change in the 
share- holding 
during the year
No. of Shares
% of total 
shares of the 
Company
% of Shares Pledged 
/ encumbered to 
total shares
No. of Shares
% of total 
shares of the 
Company
% of Shares Pledged 
/ encumbered to 
total shares
President of India 
through Ministry of 
Railways
Nil
Nil
Nil
Total
Nil
Nil
Nil
Sr. 
No.
Promoter
Shareholding at the beginning 
of the yea

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The excerpt discusses the shareholding of promoters, including details about the number of shares held and the percentage of shares pledged or encumbered to total shares. It also mentions changes in promoters' shareholding during the year.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The excerpt mentions the percentage of shares pledged or encumbered by promoters relative to total shares, indicating a disclosure about promoter shareholding encumbrances.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `promoter_pledge` |
| Category — Qwen | `promoter_pledge` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.9481 s |
| Input / output tokens | 860 / 46 |
| Tokens/sec (output) | 23.6 |

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

### Case 34 — `RF_JINDALSTEL_AR_JINDALSTEL_517`

#### SOURCE / EVIDENCE

- **Symbol:** JINDALSTEL
- **Company:** JINDAL STEEL LIMITED
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_JINDALSTEL_517
- **Polarity:** positive
- **Keyword candidates:** `promoter_pledge`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
d 45,27,09,000 no. 
of fully paid up Compulsory convertible preference shares (CCPS) of JSO (100% of total CCPS). 
Further, Company has given undertaking to the Lenders for investment in JSOL upto C 12,495 crore (C 10,888.25 
crore infused till 31st March, 2026) (Refer Note no. 47(d)).
4)	
Investment in JSO includes the deemed equity investment C 84.85 crore being difference between fair value 
of land transferred & consideration received.
5)	
During the year, Company has made provision for diminution in investment in Urtan North Mining Company 
Limited of C 0.65 crore (Previous Year Shresht Mining and Metals Private Limited, Jindal Steel Jindalgarh Limited 
and Jindal Naveen Avsar Limited of  9.29 crore, C 0.10 crore and C 0.03 crore respectively).
6)	
Pari Passu charge by way of Pledge of shares of Jindal Paradip Port Limited (JPPL) held by the Company.  As 
on 31st March, 2026, in terms of debt facilities of C 2,854.43 crore sanctioned by lenders of JPPL, the Company 
has pledged 13,17,12,154 no. of fully paid up equity shares (upto 51% of total Jindal Steel shareholding) (Refer 
Note no. 47(d)).
7)	
During the year, Company has converted 2,02,09,125 (Previous Year 2,37,40,000) nos. of fully paid up 0.1% 
optionally convertible redeemable preference shares amounting to C 20.21 crore (Previous year C 23.74 crore) 
into 2,02,09,125 (Previous Year 2,37,40,000) nos. of fully paid up equity shares.
8)	
Amalgamated into Siddeshwari Tradex Private Limited.
9)	
During the ea

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The Company has pledged 13,17,12,154 fully paid up equity shares of Jindal Paradip Port Limited, which constitutes up to 51% of the total Jindal Steel shareholding, as part of debt facilities sanctioned by lenders.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The company has pledged 13,17,12,154 fully paid up equity shares of Jindal Paradip Port Limited (JPPL) as a pari passu charge under debt facilities sanctioned by lenders of JPPL.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `promoter_pledge` |
| Category — Qwen | `promoter_pledge` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 2.4616 s |
| Input / output tokens | 867 / 65 |
| Tokens/sec (output) | 26.4 |

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

### Case 35 — `RF_MANKIND_AR_MANKIND_441`

#### SOURCE / EVIDENCE

- **Symbol:** MANKIND
- **Company:** Mankind Pharma Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_MANKIND_441
- **Polarity:** positive
- **Keyword candidates:** `promoter_pledge`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
red by exclusive pledge of shares and securities of Bharat Serums and Vaccines Limited 
acquired by the Company.
	
The Company has complied with all financial covenants as at the reporting date and there is no indication of 
any default or breach of these covenants. These covenants are tested semi-annually as per the terms of the 
debenture trust deed.
	
(b)	 Packing credit facility from bank:
	
Packing credit facility obtained by Company from ICICI Bank and Kotak Mahindra Bank at rate of interest- 
4.89% p.a. to 5.33% p.a. (March 31, 2024 : Nil). These facilities are secured by following:-
	
(i)	
Exclusive charge on present and future inventory and book debts of Company.
	
(c)	 Cash credit facility from bank:
	
Pursuant to scheme of amalgamation, cash credit facility availed to INR 30 crores (March 31, 2024 : INR 35 
crores), outstanding at INR 29 crores (March 31, 2024 : 14.93 crores), rate of interest- 8.50% p.a. (March 31, 
2024 : 8.50% p.a.) obtained from ICICI Bank (previous year from HDFC Bank) and INR 3.48 crores (March 31, 
2024 : INR Nil), outstanding at INR 3.48 crores (March 31, 2024 : INR Nil), rate of interest- 8.50% p.a. (March 31, 
2024 : Nil) obtained from Kotak Mahindra Bank, transferred to the Company are secured by way of following 
of JPR Labs Private Limited (transferor Company), (refer note 49):
Mankind Pharma Limited  Annual Report 2024-25
Financial statements
Statutory reports
Corporate overview
Notes to the Standalone Financial Statements 
for the

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The excerpt mentions an exclusive pledge of shares and securities of Bharat Serums and Vaccines Limited acquired by the Company.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The Company's shares and securities of Bharat Serums and Vaccines Limited are exclusively pledged. The Company has complied with financial covenants and there are no defaults or breaches.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `promoter_pledge` |
| Category — Qwen | `promoter_pledge` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.9827 s |
| Input / output tokens | 795 / 51 |
| Tokens/sec (output) | 25.7 |

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

### Case 36 — `RF_PFC_AR_PFC_799`

#### SOURCE / EVIDENCE

- **Symbol:** PFC
- **Company:** Power Finance Corporation Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_PFC_799
- **Polarity:** positive
- **Keyword candidates:** `promoter_pledge`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
s / statutory and non- statutory 
clearances related to the project etc. and in general to ensure bankability of the project & protection of 
the interest of the Company as a lender for timely servicing of debt. The Company has an authorisation 
/ delegation structure for the approval of credit facilities commensurating with the size of the loan.
	
(ii)	 Security and Covenants
	
	
PFC stipulates a package of security measures/covenants to mitigate risks during the construction and post 
COD (commercial operation date) stage of the project. Based on the risk appetite and appraisal of the project, 
PFC adopts a combination of the following measures:
	
	
(a)	
Primary Security -Charge on Project Assets and / or State Government Guarantees
	
	
(b)	 Collateral Securities - Corporate guarantee, Personal guarantee of promoters, Pledge of shares, Charge 
on assets / revenues of group/other companies
	
	
(c)	
Payment Security Mechanism - Escrow Account / Letter of Credit, Trust and Retention Account (TRA)
	
	
(d)	 Other covenants - Assignment of all project contracts, documents, insurance policies in favour of 
the Company, Upfront equity requirement, Debt Service Reserve Account (DSRA), Debt Equity ratio, 
shareholders’ agreements, financial closure, etc.
Notes to the Consolidated Financial Statements
for the year ended March 31, 2026
40th Annual Report 2025-26
	
(iii)	 Project Monitoring
	
	
PFC has comprehensive project/loan monitoring guidelines that captures aspects relating t

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The excerpt discusses security measures and covenants related to a project, including the personal guarantee of promoters and the pledge of shares as part of the collateral securities.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The excerpt mentions that promoters may pledge their shares as collateral securities under the security measures adopted by PFC to mitigate risks.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `promoter_pledge` |
| Category — Qwen | `promoter_pledge` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.4443 s |
| Input / output tokens | 619 / 39 |
| Tokens/sec (output) | 27.0 |

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

### Case 37 — `RF_TATAPOWER_AR_TATAPOWER_617`

#### SOURCE / EVIDENCE

- **Symbol:** TATAPOWER
- **Company:** Tata Power Company Limited
- **Fiscal year:** FY2026
- **Doc type:** annual_report
- **Chunk id:** AR_TATAPOWER_617
- **Polarity:** positive
- **Keyword candidates:** `promoter_pledge`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
 of Quoted Investments 
ii.
Aggregate Carrying Value of Quoted Investments 
iii.
Aggregate Carrying Value of Unquoted Investments (Net)
iv.
Aggregate amount of impairment in value of Investments
Non-Current Investments (Contd.)
Financial Statements
Financial Statements
Standalone Financial Report
Standalone Financial Report
Powering a Billion Aspirations, Lifelong
Integrated Annual Report 2025-26
Notes to the Standalone Financial Statements
Notes to the Standalone Financial Statements
	
v.	
The Company has invested in unsecured subordinated perpetual securities issued by its subsidiary companies. These 
securities are redeemable at the issuer’s option and carry non-cumulative interest coupon at the rate of dividend paid 
on the issuer’s ordinary shares. The interest can be deferred if the issuer does not pay any dividend on its ordinary 
shares for the financial year. The issuer has classified this instrument as equity under Ind AS - 32 ‘Financial Instruments 
Presentation’. Accordingly, the Company has classified this investment as Equity Instrument and has accounted at cost 
as per Ind AS - 27 ‘Separate Financial Statements’.
	
vi.	
During the current and previous year the Company has subscribed to the right issue of equity shares offered by 
TPCODL,TPWODL,TPSODL and TPNODL.
	
vii.	 Shares pledged :
	
	
The Company has pledged shares of subsidiaries and joint ventures with the lenders for borrowings availed by the 
respective subsidiaries and joint ventures.
Details
Categor

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The Company has pledged shares of subsidiaries and joint ventures with lenders for borrowings availed by the respective subsidiaries and joint ventures.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The Company has pledged shares of subsidiaries and joint ventures with lenders for borrowings availed by the respective subsidiaries and joint ventures.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `promoter_pledge` |
| Category — Qwen | `promoter_pledge` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.6077 s |
| Input / output tokens | 723 / 40 |
| Tokens/sec (output) | 24.9 |

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

### Case 38 — `RF_TATAPOWER_AR_TATAPOWER_929`

#### SOURCE / EVIDENCE

- **Symbol:** TATAPOWER
- **Company:** Tata Power Company Limited
- **Fiscal year:** FY2026
- **Doc type:** annual_report
- **Chunk id:** AR_TATAPOWER_929
- **Polarity:** positive
- **Keyword candidates:** `promoter_pledge`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
 
certain entities, both present and future and are also secured by way of charge on tangible and intangible assets, current assets, receivables 
and stores and spares, uncalled capital receivables, rights under project documents, project cash flows, pledge of shares and monies 
receivable of the respective entities. Range of interest rates is 5.90% p.a. to 9.40% p.a (March 31, 2025 - 4.50% p.a. to 10.90% p.a).
	
Current borrowings secured against current assets	
	
The quarterly returns or statements of current assets filed by the Group with the banks or financial institutions are in agreement with the 
books of accounts.
Financial Statements
Financial Statements
Consolidated Financial Report
Consolidated Financial Report
Powering a Billion Aspirations, Lifelong
Integrated Annual Report 2025-26
Notes to the Consolidated Financial Statements
Notes to the Consolidated Financial Statements
32.	Revenue from Operations
	
Revenue recognition
 
Accounting Policy
	
Revenue from contracts with customers is recognised when control of the goods or services are transferred to the customer 
at an amount that reflects the consideration to which the Group expects to be entitled in exchange for those goods or 
services.
	
Description of performance obligations are as follows:
	
(i)	
Sale of Power - Generation
	
	
Revenue from sale of power is recognised (net of cash discount) over time for each unit of electricity delivered.
	
	
a)	
Contract price determined as per tariff regulations
	
	
	
T

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The excerpt mentions a pledge of shares as part of the security for borrowings, indicating that shares are encumbered.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The excerpt mentions the pledge of shares and monies receivable of the respective entities as collateral for borrowings secured against current assets.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `promoter_pledge` |
| Category — Qwen | `promoter_pledge` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.4949 s |
| Input / output tokens | 614 / 41 |
| Tokens/sec (output) | 27.4 |

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

### Case 39 — `RF_VEDL_AR_VEDL_1233`

#### SOURCE / EVIDENCE

- **Symbol:** VEDL
- **Company:** Vedanta Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_VEDL_1233
- **Polarity:** positive
- **Keyword candidates:** `promoter_pledge`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
on on the specified movable 
fixed assets of the Company pertaining to its manufacturing facilities comprising:-
(i)	 alumina refinery having output of 1 MTPA along with co- generation captive 
power plant with an aggregate capacity of 75 MW at Lanjigarh, Odisha; 
(ii)	 aluminium smelter having output of 1.6 MTPA along with a 1,215 (9xl35) MW 
CPP Jharsuguda, Odisha
First pari passu charge by way of hypothecation of the specified movable fixed 
assets both present and future comprising:-
(i)	 6 MTPA alumina refinery along with 270 MW co-generation captive power plant 
(operating capacity) in Lanjigarh, Odisha.
(ii)	 1.8 MTPA aluminium smelter plant along with 1,215 MW (9x135 MW) captive 
power plant in Jharsuguda, Odisha.
(iii)	 1,800 MW Power Plant CPP located at Jharsuguda, Odisha
Integrated Report and Annual Accounts 2025-26
Statutory Reports
Financial Statements
Vedanta Limited
Corporate Overview
Standalone
Notes
forming part of the financial statements as at and for the year ended 31 March 2026
Notes
forming part of the financial statements as at and for the year ended 31 March 2026
(` in Crore)
Facility 
Category
Security details
As at 
31 March 2026
As at 
31 March 2025 
Term Loan by Union Bank - 
Charge on certain assets of VEDL including but not limited to identified movable 
fixed assets and immovable properties (both freehold and leasehold) pertaining to 
(1) aluminium division, (2) iron ore division, (3) copper division owned by VEDL as 
more particularly set 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The excerpt discusses a first ranking exclusive pledge over shares held by Vedanta Limited in Hindustan Zinc Limited, which is intended to cover a loan with a specified minimum coverage ratio.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The excerpt mentions a first exclusive charge over shares held by VEDL in HZL, with a minimum coverage of 1.10 times the loan, and a 50.1% non-dilution undertaking over HZL shares.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `promoter_pledge` |
| Category — Qwen | `promoter_pledge` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 2.3535 s |
| Input / output tokens | 753 / 67 |
| Tokens/sec (output) | 28.5 |

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

### Case 40 — `RF_VEDL_AR_VEDL_939`

#### SOURCE / EVIDENCE

- **Symbol:** VEDL
- **Company:** Vedanta Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_VEDL_939
- **Polarity:** positive
- **Keyword candidates:** `promoter_pledge`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
 
at Jharsuguda and
(ii)	 1 MTPA Alumina refinery along with CPP of 75 MW (captive power plant) at 
Lanjigarh, Odisha
A First Pari-passu first charge by way of hypothecation on the Specified movable 
fixed assets of the Company pertaining to its manufacturing facilities comprising 
of:
(i)	 alumina refinery having output of 1 MTPA along with co- generation captive 
power plant with an aggregate capacity of 75 MW at Lanjigorh, Odisha; 
(ii) 	 aluminium smelter having output of 1.6 MTPA along with a 1215 (9*135) MW 
CPP al Jharsuguda, Odisha"
Secured  by a first pari passu charge on the identified fixed assets of the Borrower 
both present and future, pertaining to its Aluminium business (Jharsuguda Plant, 
Lanjigarh Plant), 2400 MW power plant assets at Jharsuguda, Copper Plant 
assets at Silvasa, Iron ore business in the states of Karnataka and Goa, dividends 
receivable from Hindustan Zinc Limited (“HZL”), and the DSRA placed opened for 
the Facility along with the amount lying to the credit thereof, and  Pledge of shares 
of HZL held by company with a minimum coverage of 1.1X. Negative lien on oil & 
gas fixed assets.
Secured by first pari passu charge by way of mortgage / hypothecation over the 
specified immovable and movable fixed assets of the Company.Security shall 
comprise of assets of the Aluminum & Power Division of the Company, comprising 
of: 
(i)	 1.6 MTPA Aluminium Smelter along with 1215 MW CPP (captive power plant) 
at Jharsuguda, Odisha;  and
(ii)	 1 MT

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The excerpt discusses a pledge of shares of Hindustan Zinc Limited (HZL) held by the company, which is part of the security for a financial facility. It mentions a minimum coverage ratio for the pledged shares.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `promoter_pledge`

**risk_flag_summary**

The excerpt mentions a pledge of shares of HZL held by the company with a minimum coverage of 1.1X.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `promoter_pledge` |
| Category — Qwen | `promoter_pledge` |
| Outcome | **agree** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.6862 s |
| Input / output tokens | 754 / 41 |
| Tokens/sec (output) | 24.3 |

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

### Case 41 — `RF_ADANIGREEN_AR_ADANIGREEN_1065`

#### SOURCE / EVIDENCE

- **Symbol:** ADANIGREEN
- **Company:** Adani Green Energy Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_ADANIGREEN_1065
- **Polarity:** negative
- **Keyword candidates:** `related_party_transaction`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
ith previous transactions during a financial year, whether 
directly and/or through its subsidiary(ies), exceed(s) 
` 1,000 crore or 10% of the annual consolidated turnover 
as per the last audited financial statements of the listed 
entity, whichever is lower. Further, the definition of 
Related Party Transaction as per Regulation 2(1)(zc) of 
the SEBI Listing Regulations includes the transaction 
involving a transfer of resources, services or obligations 
between a listed entity or any of its subsidiaries on one 
hand and a related party of the listed entity or any of its 
subsidiaries on the other hand.
The Company proposes to enter into a related party 
transaction(s) as mentioned below, on mutually agreed 
terms and conditions, and the aggregate of such 
transaction(s), are expected to cross the applicable 
materiality thresholds as mentioned above. Accordingly, as 
per the SEBI Listing Regulations, prior approval of the 
Members is being sought for all such arrangements / 
transactions proposed to be undertaken by the Company. 
The said transactions shall be in the ordinary course of 
business of the Company and on an arm’s length basis.
The Audit Committee of the Company (comprising solely 
of the Independent and Nominee Directors) has, on the 
basis of relevant details provided by the management 
as required by the law, at its meeting held on March 28, 
2025 reviewed and approved the said transaction(s), 
subject to approval of the Members, while noting that 
such tra

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

<details><summary>Rejected attempts</summary>

- pass 1: summary failed compliance: forward-tense word 'expected'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `— (no flag)` |
| Category — Qwen | `— (no flag)` |
| Outcome | **agree_no_flag** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 2.4524 s |
| Input / output tokens | 625 / 78 |
| Tokens/sec (output) | 31.8 |

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

### Case 42 — `RF_ASIANPAINT_AR_ASIANPAINT_679`

#### SOURCE / EVIDENCE

- **Symbol:** ASIANPAINT
- **Company:** Asian Paints Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_ASIANPAINT_679
- **Polarity:** negative
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
petition 
Act, 2002. The Company has filed its responses from time to time with respect to the 
information sought by the DG. 
	
Based on the present status and the Company’s assessment of the proceedings, the Company 
believes that it has a reasonable basis to defend its position in this matter. Considering the 
early stage of the investigation and inherent uncertainties associated with such proceedings, 
it is not possible to estimate the likelihood of potential financial impact, if any.
	
-
-
Total
	
^The above claims are pending before various Appellate Authorities. The management, including its advisors, expect that its position will likely be 
upheld on ultimate resolution and will not have a material adverse effect on the Company’s financial statements.  
It is not practicable for the Company to estimate the timings of cash outflows, if any, in respect of the pending resolution of the respective 
proceedings as it is determinable only on receipt of judgements/ decisions pending with various forums/ authorities. The Company does not 
expect any reimbursements in respect of the contingent liabilities.
	
*Towards custom duty and IGST for capital goods imported under Manufacturing & Other operation in Warehouse Regulation (MOOWR) scheme 
against which the Company has executed a bond which is three times of the custom duty calculated at the time of import. The amount and timing 
of liability towards such custom duty and IGST will crystalize at the time of filing of ex-bo

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

<details><summary>Rejected attempts</summary>

- pass 1: summary failed compliance: forward-tense word 'expects'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `— (no flag)` |
| Category — Qwen | `— (no flag)` |
| Outcome | **agree_no_flag** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.6779 s |
| Input / output tokens | 629 / 47 |
| Tokens/sec (output) | 28.0 |

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

### Case 43 — `RF_BAJAJFINSV_AR_BAJAJFINSV_334`

#### SOURCE / EVIDENCE

- **Symbol:** BAJAJFINSV
- **Company:** Bajaj Finserv Limited
- **Fiscal year:** FY2026
- **Doc type:** annual_report
- **Chunk id:** AR_BAJAJFINSV_334
- **Polarity:** negative
- **Keyword candidates:** `auditor_qualification`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
ressed an unmodified opinion on the financial statements. Based on consideration of 
their report, the following key audit matters have been included by us on as is where is basis as under:
Sr. No. Key audit matter
How the matter was addressed in our audit
Assessment of impairment loss allowance 
based on expected credit loss (‘ECL’) on Loans
As at 31 March 2026, the outstanding balances of 
loans granted by the Company aggregated to  
H 376,792.12 crore and the associated impairment 
loss allowance recognised in the books aggregated 
to H 9,566.16 crore. 
The impairment loss allowance is determined in 
accordance with the expected credit loss (‘ECL’) 
model specified under Ind AS 109 ‘Financial 
Instruments’ and involves exercise of judgment 
by the Management in estimating the expected 
losses using components of ECL such as probability 
of default (‘PD’), loss given default (‘LGD’) and 
exposure at default (expected balance at default 
together with expected drawdown from committed 
lines) (‘EAD’), staging of loans, etc.
Quantitative factors like days past due, behaviour 
of the loan portfolio, historical losses incurred 
on defaults, macro-economic data points and 
recovery post default, and qualitative factors like 
nature of the underlying loan, deterioration in credit 
quality, correlation of macro-economic variables 
to determine expected losses, probability weights 
applied to reflect future economic conditions and 
related Reserve Bank of India (‘RBI’) guidelines, 


… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

<details><summary>Rejected attempts</summary>

- pass 1: summary failed compliance: forward-tense word 'expected'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `— (no flag)` |
| Category — Qwen | `— (no flag)` |
| Outcome | **agree_no_flag** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 2.1584 s |
| Input / output tokens | 641 / 66 |
| Tokens/sec (output) | 30.6 |

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

### Case 44 — `RF_BAJAJHLDNG_AR_BAJAJHLDNG_268`

#### SOURCE / EVIDENCE

- **Symbol:** BAJAJHLDNG
- **Company:** Bajaj Holdings & Investment Limited
- **Fiscal year:** FY2025
- **Doc type:** annual_report
- **Chunk id:** AR_BAJAJHLDNG_268
- **Polarity:** negative
- **Keyword candidates:** `auditor_qualification`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
oning, de-provisioning, access 
review, password management, sensitive access 
rights and segregation of duties to ensure that 
privilege access to applications, operating systems 
and databases in the production environment were 
granted only to authorised personnel;
-	
Program development, which includes controls over 
IT application development or implementation and 
related infrastructure, data migration from one LMS 
to another LMS;
-	
IT operations, which includes job scheduling, 
monitoring, data backup and recovery;
-	
Performed procedures to assess the completeness 
and accuracy of data migrated from the legacy LMS 
to the new LMS.
•	
Evaluated the design and tested the operating 
effectiveness of relevant key IT dependencies 
within the key business processes, which included 
testing automated controls, automated calculations/
accounting procedures, interfaces, segregation of 
duties and system generated reports, as applicable.
•	
Communicated with the Management and those 
charged with governance and tested a combination 
of compensating controls, remediated controls and/or 
performed alternative audit procedures, where necessary.
Independent Auditors' Report on the Consolidated Financial Statements (Contd.)
158 80th Annual Report 2024-25
The following key audit matters were reported by joint auditors of Bajaj Finance Ltd. pertaining to Bajaj Housing 
Finance Ltd., a step-down subsidiary of Bajaj Finserv Ltd. (Associate Entity), which are reproduced by us 
as 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

<details><summary>Rejected attempts</summary>

- pass 1: summary failed compliance: forbidden word 'accuracy'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `— (no flag)` |
| Category — Qwen | `— (no flag)` |
| Outcome | **agree_no_flag** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.6689 s |
| Input / output tokens | 630 / 47 |
| Tokens/sec (output) | 28.2 |

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

### Case 45 — `RF_BAJFINANCE_AR_BAJFINANCE_435`

#### SOURCE / EVIDENCE

- **Symbol:** BAJFINANCE
- **Company:** Bajaj Finance Limited
- **Fiscal year:** FY2026
- **Doc type:** annual_report
- **Chunk id:** AR_BAJFINANCE_435
- **Polarity:** negative
- **Keyword candidates:** `auditor_qualification`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
icance in our 
audit of the standalone financial statements of the current period. These matters were addressed in the 
context of our audit of the standalone financial statements as a whole and in forming our opinion thereon, 
and we do not provide a separate opinion on these matters. We have determined the matters described 
below to be the key audit matters to be communicated in our report.
Assessment of impairment loss allowance based on expected credit loss (ECL) on Loans (refer note no. 9 of the 
standalone financial statements)
Key audit matter
How our audit addressed the key audit matter
As at 31 March 2026, the outstanding balances of loans 
granted by the Company aggregated to C 376,792.12 crore 
and the associated impairment loss allowance recognised 
in the books aggregated to C 9,566.16 crore. 
The impairment loss allowance is determined in 
accordance with the Expected Credit Loss (‘ECL’) model 
specified under Ind AS 109 'Financial Instruments' and 
involves exercise of judgement by the Management in 
estimating the expected losses using components of ECL 
such as Probability of Default (‘PD’), Loss Given Default 
(‘LGD’) and Exposure at Default (expected balance at 
default together with expected drawdown from committed 
lines) (‘EAD’), Staging of Loans, etc.
The procedures performed by us included the 
following: 
• Understood and evaluated the design and tested 
the operating effectiveness of the key controls put 
in place by the Company’s Management over t

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

<details><summary>Rejected attempts</summary>

- pass 1: summary failed compliance: forward-tense word 'expected'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `— (no flag)` |
| Category — Qwen | `— (no flag)` |
| Outcome | **agree_no_flag** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 2.1122 s |
| Input / output tokens | 651 / 64 |
| Tokens/sec (output) | 30.3 |

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

### Case 46 — `RF_BAJFINANCE_AR_BAJFINANCE_488`

#### SOURCE / EVIDENCE

- **Symbol:** BAJFINANCE
- **Company:** Bajaj Finance Limited
- **Fiscal year:** FY2026
- **Doc type:** annual_report
- **Chunk id:** AR_BAJFINANCE_488
- **Polarity:** negative
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
atement of Profit and Loss.
3.7	 Intangible assets and amortisation thereof
 
The Company measures Intangible assets, representing softwares, licenses etc. initially at cost and 
subsequently at cost less accumulated amortisation and accumulated impairment, if any.
 
The Company recognises internally generated intangible assets when the Company is certain that 
intangible asset would support/result in furtherance of Company’s existing and/or new business and cost 
of such intangible asset identifiable and reliably measurable. The cost of an internally generated intangible 
asset comprises of all directly attributable costs necessary to create, produce, and prepare the asset to be 
capable of operating in the manner intended by the Company.
 
All the intangible assets including those internally generated are amortised using the straight line method 
over a period of five years, which is the Management's estimate of its useful life.
 
An intangible asset is derecognised on disposal, or when no future economic benefits are expected 
from use or disposal. Gains or losses arising from derecognition of an intangible asset, measured as the 
difference between the net disposal proceeds and the carrying amount of the asset are recognised in the 
Statement of Profit and Loss when the asset is derecognised.
Summary of material accounting policies (Contd.)
256 39th Annual Report 2025-26
Notes to standalone financial statements for the year ended 31 March 2026 (Contd.)
3.8	 Provisions

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `contingent_liability`

**risk_flag_summary**

The excerpt discusses the company's accounting policies for provisions and contingent liabilities, including when a provision is created and when a contingent liability is disclosed.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `— (no flag)` |
| Category — Qwen | `contingent_liability` |
| Outcome | **false_positive** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.5556 s |
| Input / output tokens | 605 / 44 |
| Tokens/sec (output) | 28.3 |

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

### Case 47 — `RF_CIPLA_AR_CIPLA_507`

#### SOURCE / EVIDENCE

- **Symbol:** CIPLA
- **Company:** Cipla Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_CIPLA_507
- **Polarity:** negative
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
ing fixed deposit with original 
maturity period of three months or less and short-term 
highly liquid investments with an original maturity of 
three months or less.
	
1.3.16	Provisions
	
	
Provisions are recognised when the Company has a 
present obligation (legal or constructive) as a result of 
a past event, it is probable that an outflow of resources 
embodying economic benefits will be required to settle 
the obligation and a reliable estimate can be made of 
the amount of the obligation.
	
	
Provisions are measured at the best estimate of the 
expenditure required to settle the present obligation at 
the Balance Sheet date. If the effect of the time value 
of money is material, provisions are discounted to 
reflect its present value using a current pre-tax rate that 
reflects the current market assessment of the time value 
of money and the risks specific to the obligation. When 
discounting is used, the increase in the provision due to 
the passage of time is recognised as a finance cost.
	
	
Provision for onerous contracts
	
	
A provision for onerous contracts is recognised in 
the standalone statement of profit and loss when the 
expected benefits to be derived by the Company 
from a contract are lower than the unavoidable cost 
of meeting its obligations under the contract. The 
provision is measured at the present value of the lower 
of the expected cost of terminating the contract and 
the expected net cost of continuing with the contract. 
Before a provision is 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `contingent_liability`

**risk_flag_summary**

The excerpt discusses contingent liabilities, which are disclosed when there is a possible obligation from past events, confirmed by uncertain future events. It also covers provisions for onerous contracts and their measurement.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `— (no flag)` |
| Category — Qwen | `contingent_liability` |
| Outcome | **false_positive** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.8096 s |
| Input / output tokens | 609 / 54 |
| Tokens/sec (output) | 29.8 |

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

### Case 48 — `RF_DRREDDY_AR_DRREDDY_586`

#### SOURCE / EVIDENCE

- **Symbol:** DRREDDY
- **Company:** Dr. Reddy's Laboratories Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_DRREDDY_586
- **Polarity:** negative
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
he Company which were carried 
out remained open during the year ended March 31, 2026:
Located in India
Month and year
Unit
Details of observations
October 2023 
and September 
Biologics, Hyderabad, 
India
Nine observations were noted in the U.S. FDA inspection. The Company responded to the 
observations.
Further to this inspection, five observations were noted in the Pre-Approval Inspection (“PAI”) 
conducted by the U.S. FDA from September 4-12, 2025, to which the Company has responded 
within the stipulated timelines. The Company has received a Post Application Action Letter 
(“PAAL”) from the U.S. FDA on January 9, 2026 to which the Company has responded within the 
stipulated timelines and has received dates for inspection.
	
Other indirect tax related matters
	
Additionally, the Company is in receipt of various demand notices from the Indian Sales and Service Tax authorities. 
The total disputed amount is ` 482. The Company has responded to such demand notices and believes that the chances of 
any liability arising from such notices are not probable. Accordingly, no provision is made in these financial statements as of 
March 31, 2026.
	
Tax claim for Merger of Dr. Reddy’s Holdings Limited into Dr. Reddy’s Laboratories Limited
	
The Company received a reassessment notice from the Income Tax Department of India for income alleged to have 
escaped assessment due to the merger of Dr. Reddy’s Holdings Limited into Dr. Reddy’s Laboratories Limited. For details, 
see Note 2.

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

<details><summary>Rejected attempts</summary>

- pass 1: summary failed compliance: forward-tense word 'will'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `— (no flag)` |
| Category — Qwen | `— (no flag)` |
| Outcome | **agree_no_flag** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.7005 s |
| Input / output tokens | 639 / 48 |
| Tokens/sec (output) | 28.2 |

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

### Case 49 — `RF_ETERNAL_AR_ETERNAL_486`

#### SOURCE / EVIDENCE

- **Symbol:** ETERNAL
- **Company:** ETERNAL LIMITED
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_ETERNAL_486
- **Polarity:** negative
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
e transactions are treated as vested irrespective 
of whether the market or non-vesting condition is 
satisfied, provided that all other performance and/or 
service conditions are satisfied.
When the terms of an equity-settled award are 
modified, the minimum expense recognized is the 
expense had the terms had not been modified, if the 
original terms of the award are met. An additional 
expense is recognized for any modification that 
increases the total fair value of the share-based 
payment transaction, or is otherwise beneficial to the 
employee as measured at the date of modification.
The dilutive effect of outstanding options is reflected 
as additional share dilution in the computation of 
diluted earnings per share.
xiii.	 Earnings per share
Basic earnings per share are calculated by dividing 
the net profit or loss for the year attributable to equity 
shareholders by the weighted average number of 
equity shares.
Financial Statements: Standalone
Statutory Reports
Company Overview
Material Accounting Policies to the Standalone 
Financial Statements
for the year ended March 31, 2026
CIN : L93030DL2010PLC198141
For the purpose of calculating diluted earnings per 
share, the net profit or loss for the year attributable to 
equity shareholders of the Company and the weighted 
average number of shares outstanding during the year 
are adjusted for the effects of all dilutive potential 
equity shares.
xiv.	Provisions and Contingent liabilities
Provisions
Provisions are reco

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

<details><summary>Rejected attempts</summary>

- pass 1: summary failed compliance: forward-tense word 'will'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `— (no flag)` |
| Category — Qwen | `— (no flag)` |
| Outcome | **agree_no_flag** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 2.0921 s |
| Input / output tokens | 623 / 65 |
| Tokens/sec (output) | 31.1 |

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

### Case 50 — `RF_GAIL_AR_GAIL_522`

#### SOURCE / EVIDENCE

- **Symbol:** GAIL
- **Company:** GAIL (India) Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_GAIL_522
- **Polarity:** negative
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
respect 
of its following Financial Guarantee as on 31st March 2025: 
	
	 During the year, based on the fair valuation of GAIL Global USA Inc. (GGUI), the Company has provided for Expected Credit Loss of 
₹ 49.32 crore (Previous Year: ₹ 46.05 crore) against Corporate Guarantee provided by the company on behalf of GGUI. 
49.	 	 In compliance of Ind AS 37 on “Provisions, Contingent liabilities and Contingent Assets”, the required information on Provision for 
Probable Obligations is as under:
(` in crore)
Provisions
Opening Balance
Addition during 
the year 
Reversal/adjusted 
during the year
Closing Balance
(incl. OCI)
(incl. OCI)
Employee Benefit
Liability for Abandonment Costs
 - 
 - 
Legal & Arbitration Cases (including taxes)
Total
Energizing Excellence in Integrated Business
50.	 Unhedged Foreign Currency Exposure:
(` in crore)
Particulars
Currencies
31st March 2025
31st March 2024
Trade Payables / Deposits and Retention Amount
USD
EURO
Others
Trade / Other Receivables and Bank Balances
USD
Others
Unexecuted amount of contracts 
USD
EURO
Others
Capital Contribution Receivable from SEAGP
USD
 - 
51.	 Details of Loans, Investments, Guarantees and Securities given by the Company covered u/s 186 (4) of the Companies Act 2013:
I.	
Investments made and Loans given are disclosed under the respective notes No 5 & 7.
II. 	
a.   Corporate Guarantees given by the Company on behalf of its Subsidiaries/ JVs/ Associates in respect of loans are as under:
(` in crore)
Sl. No.
Name of the

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

<details><summary>Rejected attempts</summary>

- pass 1: summary failed compliance: forward-tense word 'expected'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `— (no flag)` |
| Category — Qwen | `— (no flag)` |
| Outcome | **agree_no_flag** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 2.0379 s |
| Input / output tokens | 779 / 54 |
| Tokens/sec (output) | 26.5 |

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

### Case 51 — `RF_GODREJCP_AR_GODREJCP_432`

#### SOURCE / EVIDENCE

- **Symbol:** GODREJCP
- **Company:** Godrej Consumer Products Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_GODREJCP_432
- **Polarity:** negative
- **Keyword candidates:** `auditor_qualification`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
sses in overseas geographies during 
previous year, there are impairment triggers requiring 
evaluation.
The impairment assessment involves use of significant 
estimates and judgements due to the inherent uncertainty 
involved in forecasting discounting future cash flows and 
determining the recoverable amounts.
In view of the significance of these investments and 
estimates and judgments involved, we consider 
impairment evaluation of investments in subsidiaries to be 
a key audit matter.
Our audit procedures included:
•	
Evaluating design and implementation and testing operating 
effectiveness of controls over the Company’s process of impairment 
assessment and approval of forecasts;
•	
Assessing the indicators for impairment of the subsidiaries and 
understanding the Company’s assessment of those indicators;
•	
Assessing the valuation methodology and challenging the 
assumptions used, in particular those relating to forecast revenue 
growth and earnings, weighted average cost of capital and long-term 
growth rates, with the assistance of our valuation specialists;
•	
Assessing the reliability of the financial projections prepared by the 
Company by comparing projections for previous financial years with 
actual results realized and analysis of significant variances;
•	
Performing sensitivity analysis by assessing the effect of possible 
reductions in the above assumptions on the recoverable amount; and
•	
Comparing the carrying amount of investments with recoverable 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `auditor_qualification`

**risk_flag_summary**

The audit procedures focused on evaluating the impairment assessment of investments in subsidiaries, including testing controls, assessing valuation methodologies, and analyzing financial projections.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `— (no flag)` |
| Category — Qwen | `auditor_qualification` |
| Outcome | **false_positive** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.472 s |
| Input / output tokens | 572 / 42 |
| Tokens/sec (output) | 28.5 |

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

### Case 52 — `RF_GRASIM_AR_GRASIM_922`

#### SOURCE / EVIDENCE

- **Symbol:** GRASIM
- **Company:** Grasim Industries Limited
- **Fiscal year:** FY2025
- **Doc type:** annual_report
- **Chunk id:** AR_GRASIM_922
- **Polarity:** negative
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
Minimum Alternate Tax (MAT) Credit 
are in the form of unused tax credits that are carried 
forward by the Group for a specified period of time, 
hence, it is presented with Deferred Tax Asset.
544 Grasim Industries Limited
Notes
forming part of the Consolidated Financial Statements for the year ended 31st March 2025
1.36	Provisions and Contingent Liabilities:
	
Provisions are recognised when the Group has a 
present obligation (legal or constructive), as a result 
of a past event, it is probable that the Group will 
be required to settle the obligation, and a reliable 
estimate can be made of the amount of the obligation.
	
If the effect of the time value of money is material, 
provisions are determined by discounting the 
expected future cash flows to the net present value 
using an appropriate pre-tax discount rate that 
reflects current market assessments of the time value 
of money and, where appropriate, the risks specific to 
the liability.
	
A present obligation that arises from past events, 
where it is either not probable that an outflow of 
resources will be required to settle or a reliable 
estimate of the amount cannot be made, is disclosed 
as a contingent liability. Contingent liabilities are also 
disclosed when there is a possible obligation arising 
from past events, the existence of which will be 
confirmed only by the occurrence or non-occurrence 
of one or more uncertain future events, not wholly 
within the control of the Group.
	
Claims against the 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `contingent_liability`

**risk_flag_summary**

The excerpt discusses the recognition and disclosure of contingent liabilities, including when they are disclosed and when they are not, based on the probability of an outflow of resources and the ability to estimate the amount.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `— (no flag)` |
| Category — Qwen | `contingent_liability` |
| Outcome | **false_positive** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.8909 s |
| Input / output tokens | 628 / 56 |
| Tokens/sec (output) | 29.6 |

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

### Case 53 — `RF_HINDALCO_AR_HINDALCO_764`

#### SOURCE / EVIDENCE

- **Symbol:** HINDALCO
- **Company:** Hindalco Industries Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_HINDALCO_764
- **Polarity:** negative
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
e considering strategic capital 
expenditure and debt repayments/pre-payments) of the relevant year subject to compliances of the Companies Act, 
2013 and all other applicable Regulations.
3.	
Factors to be considered for Dividend Payout
	
The Board will consider various internal and external factors, including but not limited to the following before making any 
recommendation for dividends:
	
•	
Free Cash Flow of the relevant year (as defined above)
	
•	
Stability of earnings
	
•	
Future capital expenditure, inorganic growth plans and reinvestment opportunities
	
•	
Industry outlook and stage of business cycle for underlying businesses
	
•	
Leverage profile and capital adequacy metrics
	
•	
Overall economic I regulatory environment
	
•	
Contingent liabilities
	
•	
Past dividend trends
	
•	
Buyback of shares or any such alternate profit distribution measure
	
•	
Any other contingency plans.
4.	
Review
	
This policy would be subject to revision I amendment on a periodic basis, as may be necessary.
5.	
Disclosure
	
This policy as amended from time to time will be available on the Company’s website and in the Integrated Annual Report.
Annexure II
Annexure III
AOC-1
Statement containing salient features of the financial statement of subsidiary, associate and joint ventures
Part A: Subsidiaries
Figures Indian Rupees [INR] in Crores & Foreign Currency [FC] in Million
Sr. Name of the Subsidiary 
Company 
 Country 
Reporting 
currency 
 Capital 
 Reserves  Total Assets 
 Total 
Liabi

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `contingent_liability`

**risk_flag_summary**

The excerpt mentions contingent liabilities as one of the factors considered by the Board when evaluating dividend payouts.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `— (no flag)` |
| Category — Qwen | `contingent_liability` |
| Outcome | **false_positive** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.3986 s |
| Input / output tokens | 668 / 35 |
| Tokens/sec (output) | 25.0 |

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

### Case 54 — `RF_INFY_AR_INFY_729`

#### SOURCE / EVIDENCE

- **Symbol:** INFY
- **Company:** Infosys Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_INFY_729
- **Polarity:** negative
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
 statements’ within the meaning of Section 27A of the Securities Act of 1933, as amended 
and Section 21E of the Securities Exchange Act of 1934, as amended. Forward-looking statements generally relate to future events or our 
future financial or operating performance and are based on our current expectations, assumptions, estimates and projections about the 
Company, our industry, economic conditions in the markets in which we operate, and certain other matters. Generally, these forward-
looking statements can be identified by the use of forward-looking terminology such as ‘may’, ‘anticipate’, ‘believe’, ‘estimate’, ‘expect’, 
‘continue’, ‘intend’, ‘will’, ‘project’, ‘seek’, ‘could’, ‘would’, ‘should’ and similar expressions. These statements are subject to substantial 
known and unknown risks, uncertainties and other factors, which may cause actual results or outcomes to differ materially from those 
implied by the forward-looking statements. Important factors that may cause actual results or outcomes to differ from those implied by 
the forward-looking statements include, but are not limited to, risks and uncertainties regarding the execution of our business strategy, 
increased competition for talent, our ability to attract and retain personnel, increase in wages, investments to reskill our employees, 
our ability to effectively implement a hybrid work model, economic uncertainties and geopolitical situations, technological disruptions 
and innovations such as artificial 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

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
| Category — reference | `— (no flag)` |
| Category — Qwen | `— (no flag)` |
| Outcome | **agree_no_flag** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 0.6943 s |
| Input / output tokens | 568 / 11 |
| Tokens/sec (output) | 15.8 |

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

### Case 55 — `RF_JINDALSTEL_AR_JINDALSTEL_649`

#### SOURCE / EVIDENCE

- **Symbol:** JINDALSTEL
- **Company:** JINDAL STEEL LIMITED
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_JINDALSTEL_649
- **Polarity:** negative
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
ovisions are recognized for present obligations of 
uncertain timing or amount arising as a result of a 
past event where a reliable estimate can be made 
and it is probable that an outflow of resources 
embodying economic benefits will be required to 
settle the obligation.
	
Where it is not probable that an outflow of 
resources embodying economic benefits will 
be required or the amount cannot be estimated 
reliably, the obligation is disclosed as a contingent 
liability and commitments, unless the probability 
of outflow of resources embodying economic 
benefits is remote.
	
Contingent assets are not recognized but disclosed 
in the financial statements when an inflow of 
economic benefits is probable.
	
If the effect of the time value of money is material, 
provisions are discounted using a current pre-
tax rate that reflects, when appropriate, the risks 
specific to the liability. When discounting is used, 
the increase in the provision due to the passage of 
time is recognised as a finance cost.
XI.	 Investment in Associates and Joint Ventures
	
An associate is an entity over which the Group has 
significant influence. Significant influence is the 
power to participate in the financial and operating 
policy decisions of the investee but is not control or 
joint control over those policies.
	
A joint venture is a joint arrangement whereby 
the parties that have joint control of the 
arrangement have rights to the net assets of the 
joint arrangement. Joint control 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

<details><summary>Rejected attempts</summary>

- pass 1: summary failed compliance: forward-tense word 'will'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `— (no flag)` |
| Category — Qwen | `— (no flag)` |
| Outcome | **agree_no_flag** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.6771 s |
| Input / output tokens | 597 / 49 |
| Tokens/sec (output) | 29.2 |

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

### Case 56 — `RF_JIOFIN_AR_JIOFIN_264`

#### SOURCE / EVIDENCE

- **Symbol:** JIOFIN
- **Company:** Jio Financial Services Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_JIOFIN_264
- **Polarity:** negative
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
 includes purchase price, borrowing costs 
and any cost directly attributable to bringing the asset to its 
working condition for the intended use, net charges on foreign 
exchange contracts and adjustments arising from exchange 
rate variations attributable to the other intangible assets.
Administrative and other general overhead expenses that are 
specifically attributable to the acquisition of other intangible 
assets are allocated and capitalised as part of the cost of the 
other intangible assets. Expenses on software support and 
maintenance are charged to the standalone statement of profit 
and loss during the year in which such costs are incurred.
Gains or losses arising from derecognition of an other 
intangible asset are measured as the difference between the 
net disposal proceeds and the carrying amount of the asset 
and are recognised in the standalone statement of profit and 
loss when the asset is derecognised.
Intangible Assets are amortised using the straight line method 
on cost over the useful life of the assets.
Other intangible assets not ready for the intended use on the 
date of the Balance Sheet are disclosed as ‘Intangible assets 
under development’.
The amortisation period and the amortisation method for 
other intangible assets with a finite useful life are reviewed at 
each reporting date.
C.9	 Provision and contingent liabilities/
assets
l	
Provisions:
Provisions are recognised when the Company has a 
present obligation (legal or constructive) as 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

<details><summary>Rejected attempts</summary>

- pass 1: summary failed compliance: forward-tense word 'expected'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `— (no flag)` |
| Category — Qwen | `— (no flag)` |
| Outcome | **agree_no_flag** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.8874 s |
| Input / output tokens | 582 / 58 |
| Tokens/sec (output) | 30.7 |

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

### Case 57 — `RF_MAZDOCK_AR_MAZDOCK_223`

#### SOURCE / EVIDENCE

- **Symbol:** MAZDOCK
- **Company:** Mazagon Dock Shipbuilders Limited
- **Fiscal year:** FY2024-25
- **Doc type:** annual_report
- **Chunk id:** AR_MAZDOCK_223
- **Polarity:** negative
- **Keyword candidates:** `auditor_qualification, contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
s contract. A 
provision for expected loss for onerous contracts 
was recognized as per Ind AS 37, Provisions, 
Contingent Liabilities and Contingent Assets. 
This was identified as a Key Audit Matter due to 
the material impact on the financial statements, 
significant judgment in cost estimation, and risk of 
misstatement in the provision (Refer Note 61 in the 
financial statements).
For the year ended March 31,2025, the provision 
for expected loss on onerous contracts amounted 
to ₹ 52,138 Lakhs (PY Nil). 
Evaluated 
processes 
deployed 
by 
Management 
for 
identifying onerous contracts as per Ind AS 37.
Tested cost estimates against project cost, historical data, 
and estimates made at the time of bidding.
Reviewed the accuracy of provision recognized for full 
expected loss on each of identified onerous contracts.
Compared total estimated cost under each contract, cost 
already incurred and expected future cost for fulfilling 
contract obligations, determined by the Management to 
arrive at expected loss on each contract.
We have verified the contractual terms with respect to 
performance obligations and criteria for transfer of control 
of goods to customer for recognition of revenue on these 
onerous contracts in accordance with Indian Accounting 
Standard. 
Examined cost overrun causes and controls identified by 
Management.
We had assessed appropriateness of disclosure made as 
per applicable Indian Accounting Standards and applicable 
financial reporting framework

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

<details><summary>Rejected attempts</summary>

- pass 1: summary failed compliance: forward-tense word 'expected'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `— (no flag)` |
| Category — Qwen | `— (no flag)` |
| Outcome | **agree_no_flag** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.8961 s |
| Input / output tokens | 605 / 58 |
| Tokens/sec (output) | 30.6 |

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

### Case 58 — `RF_MOTHERSON_AR_MOTHERSON_470`

#### SOURCE / EVIDENCE

- **Symbol:** MOTHERSON
- **Company:** Samvardhana Motherson International Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_MOTHERSON_470
- **Polarity:** negative
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
 to the liability. When discounting is used, the increase in the provision due to the passage of 
time is recognised as a finance cost.
annual report (&(+#(&(,
)+-
NOTES TO THE FINANCIAL STATEMENTS
(All amounts are in INR Million, unless otherwise stated)
Warranty provisions
In cases where the obligations include warranty liabilities, the Company provides warranties for general repairs of defects 
that existed at the time of sale, as required by law. Provisions related to these assurance-type warranties are recognised 
when the product is sold or the service is provided to the customer. Initial recognition is based on historical experience. The 
initial estimate of warranty-related costs is revised annually.
Contingent Liabilities
Contingent liabilities are disclosed when there is a possible obligation arising from past events, the existence of which will be 
confirmed only by the occurrence or non-occurrence of one or more uncertain future events not wholly within the control of 
the Company or a present obligation that arises from past events where it is either not probable that an outflow of resources 
will be required to settle or a reliable estimate of the amount cannot be made.
(t)
Employee benefits
Short-term obligations
Liabilities for wages and salaries, including non-monetary benefits that are expected to be settled wholly within 12 months 
after the end of the period in which the employees render the related service are recognised in respect of employees’ 
services

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

<details><summary>Rejected attempts</summary>

- pass 1: summary failed compliance: forward-tense word 'will'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `— (no flag)` |
| Category — Qwen | `— (no flag)` |
| Outcome | **agree_no_flag** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 2.0566 s |
| Input / output tokens | 577 / 65 |
| Tokens/sec (output) | 31.6 |

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

### Case 59 — `RF_PFC_AR_PFC_439`

#### SOURCE / EVIDENCE

- **Symbol:** PFC
- **Company:** Power Finance Corporation Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_PFC_439
- **Polarity:** negative
- **Keyword candidates:** `auditor_qualification`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
d AS, estimate the Probabilities of Default (PD), Loss 
Given Default (LGD) and Individually assessed Stage 
3 carrying value. The carrying value of loans and 
advances to borrowers may be materially misstated 
if individual impairments are not appropriately 
estimated based upon certain assumptions, future 
cash flow and asset valuations.
Considering the effect of these matters, as part of 
our risk assessment, we determined that the value 
of Expected Credit Loss (ECL) has a high degree of 
estimation & uncertainty. In view of the significance 
of the amount of loan assets out of total assets in 
the Standalone Financial Statements, impairments 
of loan assets have been considered as key audit 
matter in our audit.
[Refer Note No. 40.1.2 and 40.1.3 to the Standalone 
Financial Statements read with Note No. 5.3.1 (iii) 
and Note.6.2 (ii)]
(ii)
Fair Valuation of Derivative financial instruments 
The Company enters into derivative contracts 
in accordance with RBI guidelines to mitigate its 
currency and interest rate risk in accordance with 
currency risk management policy approved by the 
Board of Directors of the Company.
Derivative contracts are either categorized at 
Fair Value through P&L (FVTPL) or under cash 
flow hedge (Hedge Accounting). Mark to market 
gain/loss on derivatives categorized at FVTPL is 
recognized in Statement of Profit and Loss and that 
of Hedge Accounting is recognized in the Other 
Comprehensive Income. 
We consider the valuation of the derivative

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `auditor_qualification`

**risk_flag_summary**

The audit identified key audit matters related to the estimation of credit losses and the valuation of derivative instruments due to high uncertainty and potential material impact on financial statements.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `— (no flag)` |
| Category — Qwen | `auditor_qualification` |
| Outcome | **false_positive** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.6462 s |
| Input / output tokens | 637 / 46 |
| Tokens/sec (output) | 27.9 |

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

### Case 60 — `RF_PFC_AR_PFC_700`

#### SOURCE / EVIDENCE

- **Symbol:** PFC
- **Company:** Power Finance Corporation Limited
- **Fiscal year:** FY2025-26
- **Doc type:** annual_report
- **Chunk id:** AR_PFC_700
- **Polarity:** negative
- **Keyword candidates:** `contingent_liability`

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
 rather than through 
continuing use and the sale is highly probable. A sale is 
considered as highly probable when such assets have 
been decided to be sold by the Group; are available 
for immediate sale in their present condition; are 
being actively marketed for sale at a price and the 
sale has been agreed or is expected to be concluded 
within one year of the date of classification. Such 
non-current assets are measured at lower of carrying 
amount or fair value less cost to sell.
	
Non-current assets are not depreciated or amortised 
while they are classified as held for sale. Non-current 
assets held for sale are presented separately from 
other assets in the Consolidated Balance Sheet.
	
Where the Group is committed to a sale plan involving 
loss of control of an entity, it classifies investment 
Notes to the Consolidated Financial Statements
for the year ended March 31, 2026
40th Annual Report 2025-26
in the entity (i.e. all the assets and liabilities of that 
entity) as held for sale.
6.11	Provisions, Contingent Liabilities and 
Contingent Assets
	
(i)	
Provisions are recognised when the Group has 
a present legal or constructive obligation as a 
result of a past event, if it is probable that the 
Group will be required to settle the obligation 
and a reliable estimate can be made of the 
amount of the obligation.
	
(ii)	 The amount recognised as a provision is the 
best estimate of the consideration required to 
settle the present obligation at the end of the

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `risk_flag_classifier@b9e40c4` · model `gpt-4o-mini` · prompt `risk_flag_classifier@b9e40c4`
- **Recorded limitations:**
  - A negative case means production's classifier RAN and confirmed nothing — a true negative, not missing data.
  - investor_calls chunks are excluded: only 2 of 2,622 carry a risk_flag_type and their metadata has no fiscal_year.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**risk_flag_type:** `— (no flag)`

**risk_flag_summary**

_(empty)_

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**risk_flag_type:** `contingent_liability`

**risk_flag_summary**

The excerpt discusses the recognition and measurement of provisions, contingent liabilities, and contingent assets, including conditions for their recognition and the estimation of obligations.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Category — reference | `— (no flag)` |
| Category — Qwen | `contingent_liability` |
| Outcome | **false_positive** |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 1.6079 s |
| Input / output tokens | 648 / 44 |
| Tokens/sec (output) | 27.4 |

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
