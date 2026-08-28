# Evaluation review sheet — annual_report_summary

> **EXPERIMENTAL / NOT PRODUCTION.** Nothing here is evidence that the candidate model is fit for use. The objective columns below are mechanical checks; every quality judgement is left blank for a human reviewer, by design.

## Run configuration

- **Model:** `qwen3-14b-awq`
- **Weights:** `Qwen/Qwen3-14B-AWQ` (quantization: `awq`, dtype: `float16`, TP: 1, max_model_len: 16384)
- **Backend:** `echo`
- **Sampling:** temperature=0.0, max_tokens=1024, seed=0
- **Fixture:** `fixtures/annual_report_benchmark.json` (exported 2026-08-28T12:23:41.163189+00:00)
- **Cases run:** 20 of 20
- **LLM project commit:** `aad9946`
- **Run id:** `20260828T123134Z` (2026-08-28T12:31:34.051079+00:00)

> ⚠️ **This run used the `echo` backend.** No model was consulted. These results validate the harness only and must never be read as a model comparison.

## Objective signals (mechanical, no judgement)

| Metric | Value |
|---|---|
| cases | 20 |
| generated_ok | 20 |
| generation_failures | 0 |
| candidate_compliance_failures | 0 |
| reference_compliance_failures | 0 |
| cases_with_reference | 20 |
| json_repair_used | 0 |
| mean_latency_sec | 0.0 |
| total_prompt_tokens | 257232 |
| total_completion_tokens | 3140 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| mean_lexical_overlap | 0.0537 |

## Side-by-side cases

### 1. `VEDL` — fixture ``

**Fiscal year:** FY2024-25

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

Management articulated a vision for Vedanta 2.0, focusing on sustainability, innovation, and the strategic importance of critical minerals in driving India's growth.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0455 _(triage aid only — not a quality score)_

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

### 2. `BRITANNIA` — fixture ``

**Fiscal year:** FY2024-25

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

Britannia's management underscored a strong commitment to quality, innovation, and sustainability as foundational elements for future growth.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0476 _(triage aid only — not a quality score)_

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

### 3. `DIXON` — fixture ``

**Fiscal year:** FY2024-25

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

The most important qualitative point in the document is Dixon's commitment to engineering excellence and sustainable growth through innovation and advanced manufacturing.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0217 _(triage aid only — not a quality score)_

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

### 4. `LT` — fixture ``

**Fiscal year:** FY2025-26

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

Management underscored the company's resilience and strategic positioning in a rapidly changing global landscape.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0769 _(triage aid only — not a quality score)_

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

### 5. `ADANIPOWER` — fixture ``

**Fiscal year:** FY2025-26

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

The most important qualitative point in the document is Adani Power's strategic commitment to expanding capacity while prioritizing sustainability and operational excellence.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0909 _(triage aid only — not a quality score)_

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

### 6. `INFY` — fixture ``

**Fiscal year:** FY2025-26

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

Infosys is positioning itself as a leader in AI services, focusing on responsible integration of AI into enterprise systems while committing to sustainability and social responsibility.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0213 _(triage aid only — not a quality score)_

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

### 7. `HINDZINC` — fixture ``

**Fiscal year:** FY2025-26

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

Hindustan Zinc Limited is focused on becoming a leader in critical minerals while committing to sustainability and community development.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0465 _(triage aid only — not a quality score)_

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

### 8. `ASIANPAINT` — fixture ``

**Fiscal year:** FY2025-26

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

Asian Paints Limited's report underscores its strategic focus on sustainability, innovation, and enhancing consumer experiences in a competitive market.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0698 _(triage aid only — not a quality score)_

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

### 9. `TECHM` — fixture ``

**Fiscal year:** FY2025-26

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

The most significant qualitative point in the document is Tech Mahindra's strategic commitment to AI integration and operational excellence as a means to drive sustainable growth.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0435 _(triage aid only — not a quality score)_

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

### 10. `CGPOWER` — fixture ``

**Fiscal year:** FY2025-26

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

The most important qualitative point in the document is CG Power's commitment to pioneering innovation while ensuring sustainable practices across its operations.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0682 _(triage aid only — not a quality score)_

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

### 11. `M&M` — fixture ``

**Fiscal year:** FY2025-26

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

The report underscores Mahindra's commitment to resilience, sustainability, and alignment with national growth objectives as key drivers of its business strategy.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0952 _(triage aid only — not a quality score)_

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

### 12. `CHOLAFIN` — fixture ``

**Fiscal year:** FY2025-26

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

Cholamandalam's strategic focus on financial inclusion and digital transformation aims to empower underserved communities and enhance customer engagement.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0222 _(triage aid only — not a quality score)_

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

### 13. `BAJFINANCE` — fixture ``

**Fiscal year:** FY2025-26

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

Management underscored a commitment to leveraging AI for operational efficiency and customer engagement.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0526 _(triage aid only — not a quality score)_

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

### 14. `MANKIND` — fixture ``

**Fiscal year:** FY2025-26

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

Management's strategic focus includes expanding into chronic and specialty therapies while enhancing sustainability and digital capabilities.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0698 _(triage aid only — not a quality score)_

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

### 15. `SIEMENS` — fixture ``

**Fiscal year:** FY2024-26

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

The report underscored Siemens Limited's strategic focus on sustainability, technology leadership, and alignment with India's infrastructure development goals.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0698 _(triage aid only — not a quality score)_

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

### 16. `CUMMINSIND` — fixture ``

**Fiscal year:** FY2025-26

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

The most important qualitative point in the document is Cummins India's strategic focus on sustainability and innovation to drive growth and support India's energy transition.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0667 _(triage aid only — not a quality score)_

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

### 17. `SBILIFE` — fixture ``

**Fiscal year:** FY2025-26

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

The report emphasizes SBI Life's commitment to trust, customer-centricity, and sustainable growth as it marks 25 years in the insurance industry.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0222 _(triage aid only — not a quality score)_

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

### 18. `ETERNAL` — fixture ``

**Fiscal year:** FY2025-26

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

Eternal Limited is dedicated to building a sustainable and innovative business model while enhancing customer experiences across its diverse service offerings.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0213 _(triage aid only — not a quality score)_

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

### 19. `JIOFIN` — fixture ``

**Fiscal year:** FY2025-26

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

Management highlighted the company's strategic commitment to leveraging technology for enhancing financial accessibility and customer experience.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0476 _(triage aid only — not a quality score)_

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

### 20. `BEL` — fixture ``

**Fiscal year:** FY2025-26

**REFERENCE (production, gpt-4o-mini) — executive_summary**

_(empty)_

**REFERENCE (production, gpt-4o-mini) — key_points**

_(none)_

**REFERENCE (production, gpt-4o-mini) — important_risks**

_(none)_

**REFERENCE (production, gpt-4o-mini) — key_takeaway**

Management underscored BEL's strategic focus on innovation and sustainability as key drivers for future growth.

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

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.075 _(triage aid only — not a quality score)_

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
