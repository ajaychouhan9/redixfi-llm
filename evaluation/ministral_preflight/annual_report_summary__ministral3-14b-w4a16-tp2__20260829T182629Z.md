# Review sheet — annual_report_summary

> **EXPERIMENTAL / NOT PRODUCTION.** This file is evidence for a human to review, not a verdict. No quality score is computed anywhere in it, and no LLM judge was used. The candidate model is NOT declared better or worse than gpt-4o-mini by this tooling.

> ⚠️ **Not a like-for-like comparison.** The stored reference was produced on 2026-08-16 by the LEGACY pipeline (raw_text front slice, `summary`/`bullets`/`key_takeaway`). This replay uses the CURRENT pipeline (Evidence Finder evidence, `executive_summary`/`key_points`/`important_risks`). Both the input AND the output schema differ. The like-for-like replay is `annual_report_summary_legacy`, which needs a 64k context.

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
| Fixture | `/kaggle/input/datasets/ajaychouhan9/redixfi-llm-evaluation-2026/annual_report_benchmark.json` |
| Cases | 2 of 20 |
| Run id | `20260829T182629Z` (2026-08-29T18:26:29.987852+00:00) |
| LLM project commit | `unknown` |
| GPU | 2x Tesla T4 (29.12 GB total) |
| CUDA / torch / vLLM | 13.0 / 2.13.0+cu130 / None |

## Objective signals (mechanical only — no judgement)

| Metric | Value |
|---|---|
| cases | 2 |
| generated_ok | 0 |
| generation_failures | 2 |
| candidate_compliance_failures | 2 |
| reference_backstop_artifacts | 0 |
| reference_compliance_failures | 0 |
| cases_with_reference | 2 |
| structured_output_used | 2 |
| json_repair_used | 0 |
| guided_and_clean | 2 |
| guided_but_repaired | 0 |
| unguided | 0 |
| mean_latency_sec | 129.019 |
| total_prompt_tokens | 87644 |
| total_completion_tokens | 2538 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| mean_lexical_overlap | 0.0 |

## Cases

---

### Case 1 — `AR_VEDL_AR_26570_VEDL_2024_2025_A_18062025151918`

#### SOURCE / EVIDENCE

- **Symbol:** VEDL
- **Company:** Vedanta Limited
- **Fiscal year:** FY2024-25
- **Filing id:** AR_26570_VEDL_2024_2025_A_18062025151918
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 272, page ~77]
r aggressive rate hikes. While 
interest rate cuts have been limited, the more predictable 
inflation path has helped stabilize financial markets and 
laid the foundation for a gradual economic recovery.
However, this progress has been overshadowed by 
renewed geopolitical and trade tensions, particularly 
between the United States and China. Early in the fiscal 
year, the U.S. upheld steep tariffs on Chinese imports, 
averaging over 145%. In March 2025, U.S. also imposed 
a 25% duty on all steel and aluminium products, citing 
national security concerns. China responded with its own 
set of tariffs, some reaching 125%, triggering a sharp 
decline in bilateral trade and causing ripple effects across 
global supply chains.
A pivotal moment came in May 2025, when both nations 
agreed in Geneva to a 90-day suspension of tariffs 
exceeding 100%, aiming to de-escalate tensions and 
reopen dialogue. President Trump reduced tariffs on 
Chinese goods to 30%, while China lowered its tariffs 
on U.S. products to 10%. Despite this temporary truce, 
deeper issues remain unresolved, particularly around 
U.S. export controls on advanced semiconductors and 
China’s restrictions on rare earth minerals, both critical to 
high‑tech and automotive industries.
High-level negotiations resumed in London in June, 
focusing on technology transfer, export licensing, and the 
broader tariff framework. Yet, the U.S. simultaneously 
proposed to raise steel and aluminium ta

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

The annual report for Vedanta Limited for FY 2025-26 outlines the company's strategic transformation into a leader in natural resources, energy, and technology, termed 'Vedanta 2.0'. Management emphasized a commitment to sustainability, operational excellence, and innovation, aiming to create long-term value for stakeholders. The report also highlights the company's focus on disciplined capital allocation, community engagement, and the importance of critical minerals in supporting India's growth and energy transition.

**bullets**

- Management stated a plan to enhance operational efficiency through digital transformation and innovation.
- The report described ongoing investments in critical minerals to support India's energy transition.
- Management emphasized a commitment to sustainability and community welfare as central to business strategy.
- The report highlighted disciplined capital allocation to drive long-term growth and shareholder value.
- Management outlined goals for achieving net carbon neutrality and water positivity by 2030.

**key_takeaway**

Management articulated a vision for Vedanta 2.0, focusing on sustainability, innovation, and the strategic importance of critical minerals in driving India's growth.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'targets'
- pass 2: forward-tense word 'targets'
- pass 3: forward-tense word 'targets'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ❌ no — failed validation after 3 attempts |
| Attempts used | 3 |
| Compliance — **Qwen** | ❌ FAIL — executive_summary: empty text |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 149.9762 s |
| Input / output tokens | 48032 / 1397 |
| Tokens/sec (output) | 9.3 |

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

### Case 2 — `AR_BRITANNIA_AR_27040_BRITANNIA_2024_2025_A_19072025234802`

#### SOURCE / EVIDENCE

- **Symbol:** BRITANNIA
- **Company:** Britannia Industries Limited
- **Fiscal year:** FY2024-25
- **Filing id:** AR_27040_BRITANNIA_2024_2025_A_19072025234802
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 2, page ~2]
allows you to steady 
yourself amidst adversities, and come back 
stronger. Together, they form the foundation 
not just for sport, but for life.
- Avani Lekhara, Paralympic Shooter
Find a Way or Make One

Contents
CORPORATE OVERVIEW ………………..........................……………………….….…………..…...…......1-32
STATUTORY REPORTS
Board's Report ……………………………………………………………………………..............................33-68
Management Discussion and Analysis Report. …………………....………………................69-78
Corporate Governance Report……………..…………...……………………………........................79-106
Business Responsibility and Sustainability Report..….……………………….....….........107-158
FINANCIAL STATEMENTS
Auditor's Report and Standalone Financial Statements ………………..…..….…......159-244
Auditor's Report and Consolidated Financial Statements...…...…………….……....245-330
Ten-Year Financial Statistics..…….………………………………….……………...........……….............331

Challenges since Covid
Changing Channel Landscape
Slowdown in Consumption
High Inﬂation
Focus on the Basics
Marketing
Elevate Brand
Experience
Sales &
Distribution
Redefine
Route-To-Market
Sustainability
Reduce Carbon Footprint
Innovation
Agile Product Launches
Cost Efﬁciency
Across Value Chain

Strengthened Distribution
Mar‘20
Mar‘21
Mar‘22
Mar‘23
Mar‘24
Mar‘25
Number of Outlets (in Lakhs)
Mar‘20
Mar‘21
Mar‘22
Mar‘23
Mar‘24
Mar‘25
Number of Rural Preferred Dealers (in Thousands)
Direct Reach
Rural Distribution
Increased Service to
High Potential Out

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

The annual report for FY 2024-25 from Britannia Industries Limited highlighted the company's resilience in navigating a challenging macroeconomic environment marked by inflation and fluctuating consumer demand. Management emphasized a commitment to quality, innovation, and sustainability, focusing on operational enhancements and technological advancements to strengthen their market position. The report also detailed strategic initiatives aimed at expanding distribution, enhancing consumer engagement, and integrating sustainability across operations, reinforcing Britannia's goal of becoming a 'Global Total Foods Company.'

**bullets**

- Management emphasized resilience and adaptability in operations.
- Focus on quality, innovation, and sustainability as core values.
- Strategic initiatives aimed at expanding distribution and consumer engagement.
- Integration of technology and operational enhancements to drive efficiency.
- Commitment to sustainability reflected in various ESG initiatives.

**key_takeaway**

Britannia's management underscored a strong commitment to quality, innovation, and sustainability as foundational elements for future growth.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact 'rs,'
- pass 2: forward-tense word 'targets'
- pass 3: financial figure stated as fact '3%'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ❌ no — failed validation after 3 attempts |
| Attempts used | 3 |
| Compliance — **Qwen** | ❌ FAIL — executive_summary: empty text |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 108.0623 s |
| Input / output tokens | 39612 / 1141 |
| Tokens/sec (output) | 10.6 |

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
