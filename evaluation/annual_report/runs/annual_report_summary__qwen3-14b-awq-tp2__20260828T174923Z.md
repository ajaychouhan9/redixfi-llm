# Review sheet — annual_report_summary

> **EXPERIMENTAL / NOT PRODUCTION.** This file is evidence for a human to review, not a verdict. No quality score is computed anywhere in it, and no LLM judge was used. The candidate model is NOT declared better or worse than gpt-4o-mini by this tooling.

> ⚠️ **Not a like-for-like comparison.** The stored reference was produced on 2026-08-16 by the LEGACY pipeline (raw_text front slice, `summary`/`bullets`/`key_takeaway`). This replay uses the CURRENT pipeline (Evidence Finder evidence, `executive_summary`/`key_points`/`important_risks`). Both the input AND the output schema differ. The like-for-like replay is `annual_report_summary_legacy`, which needs a 64k context.

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
| Fixture | `/kaggle/input/datasets/ajaychouhan9/redixfi-llm-fixtures/annual_report_sample15.json` |
| Cases | 1 of 3 |
| Run id | `20260828T174923Z` (2026-08-28T17:49:23.852532+00:00) |
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
| mean_latency_sec | 79.364 |
| total_prompt_tokens | 23638 |
| total_completion_tokens | 580 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| mean_lexical_overlap | 0.0606 |

## Cases

---

### Case 1 — `AR_ETERNAL_AR_30059_ETERNAL_2025_2026_A_48211721_29072026204435`

#### SOURCE / EVIDENCE

- **Symbol:** ETERNAL
- **Company:** ETERNAL LIMITED
- **Fiscal year:** FY2025-26
- **Filing id:** AR_30059_ETERNAL_2025_2026_A_48211721_29072026204435
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 1, page ~2]
re registered with the Company/ 
registrar and share transfer agent/ depositories/ depository participants. 
 
The Board has appointed National Securities Depository Limited (“NSDL”) as the e-voting 
agency. Members of the Company holding shares in demat or physical form as on Wednesday, 
August 19, 2026 (“Cut-off date”) are entitled to cast their vote on the resolutions as set out in 
the Notice by electronic means, through remote e-voting facility which shall commence on 
Saturday, August 22, 2026 at 9:00 A.M. (IST) and end on Tuesday, August 25, 2026 at 5:00 P.M. 
(IST) or through e-voting at the AGM. 
 
The Notice convening the AGM along with the Annual Report are uploaded on the Company’s 
website at www.eternal.com and also at the website of NSDL at www.evoting.nsdl.com. 
 
For Eternal Limited 
(Formerly known as Zomato Limited) 
 
 
 
Sandhya Sethia 
Company Secretary & Compliance Officer 
Date: July 28, 2026 
Encl.: As above 
SANDHY
A SETHIA
Digitally signed by 
SANDHYA SETHIA 
Date: 2026.07.29 
20:34:18 +05'30'

Annual Report 2025-26
NATIONAL SPORTS STADIUM
Powering India's changing lifestyles

Our mission statement
Powering India's
changing lifestyles
Our vision statements 
Better food for more people
ZOMATO
Instant commerce indistinguishable from magic
BLINKIT
World class going-out experiences in India
DISTRICT
Building Indiaˇss most trusted food supply chain
HYPERPURE
Make India malnutrition free
FEEDING INDIA

Table of contents
Company

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

Eternal Limited's annual report for FY2025-26 outlines the company's commitment to building a sustainable business across four key segments: food delivery, quick commerce, going-out experiences, and B2B supplies. Management emphasized the importance of innovation and customer engagement, highlighting initiatives like the Healthy Mode on the Zomato app and the expansion of the Blinkit quick commerce platform. The report also detailed the company's focus on sustainability, including significant investments in electric vehicle delivery and efforts to minimize plastic waste, while maintaining a strong governance framework to support its operations.

**bullets**

- Management highlighted a commitment to sustainability and reducing carbon emissions.
- The company focused on expanding its quick commerce and food delivery segments.
- Eternal Limited emphasized innovation in customer engagement through new app features.
- Management reported on the importance of governance and ethical business practices.
- The report detailed efforts to support local communities and enhance food supply chains.

**key_takeaway**

Eternal Limited is dedicated to building a sustainable and innovative business model while enhancing customer experiences across its diverse service offerings.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**executive_summary**

Eternal Limited, formerly Zomato, reported significant growth in FY2025-26 driven by a shift to inventory ownership in its quick commerce segment, which expanded revenue to include full monetary value of goods sold. The company highlighted growth across food delivery, quick commerce, and going-out segments, alongside challenges in its B2B supplies business. Strategic focus areas included operational efficiency, stakeholder management, and risk mitigation through diversified supply chains and technological investments.

**key_points**

- Shift to inventory ownership in quick commerce significantly expanded revenue scope, including full monetary value of goods sold.
- Food delivery and going-out segments showed growth, while B2B supplies faced challenges due to business model adjustments.
- Emphasis on operational efficiency, stakeholder alignment, and risk mitigation through diversified supply chains and technology.

**important_risks**

- Intensifying competition across segments threatens growth and profitability.
- Stakeholder management challenges, including labor volatility and supply chain constraints.
- Macro-economic fluctuations and geopolitical risks impacting consumer spending and logistics.

**key_takeaway**

Eternal's strategic shift to inventory ownership in quick commerce drove substantial revenue growth, but the company faces ongoing challenges in managing competition, stakeholder dynamics, and macroeconomic risks.

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact '169%'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 2 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0606 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 79.3635 s |
| Input / output tokens | 23638 / 580 |
| Tokens/sec (output) | 7.3 |

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
