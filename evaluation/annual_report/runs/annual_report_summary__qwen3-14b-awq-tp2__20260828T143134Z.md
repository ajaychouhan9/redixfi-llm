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
| Cases | 3 of 3 |
| Run id | `20260828T143134Z` (2026-08-28T14:31:34.911449+00:00) |
| LLM project commit | `unknown` |
| GPU | 2x Tesla T4 (29.12 GB total) |
| CUDA / torch / vLLM | 13.0 / 2.13.0+cu130 / None |

## Objective signals (mechanical only — no judgement)

| Metric | Value |
|---|---|
| cases | 3 |
| generated_ok | 1 |
| generation_failures | 2 |
| candidate_compliance_failures | 2 |
| reference_backstop_artifacts | 0 |
| reference_compliance_failures | 0 |
| cases_with_reference | 3 |
| json_repair_used | 3 |
| mean_latency_sec | 137.157 |
| total_prompt_tokens | 83459 |
| total_completion_tokens | 5066 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| mean_lexical_overlap | 0.0214 |

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

Eternal Limited, formerly Zomato, reported a significant shift in its business model with a move to inventory ownership in quick commerce, driving substantial revenue growth. The company emphasized strategic expansion across food delivery, quick commerce, going-out experiences, and B2B supplies, while highlighting governance, risk management, and sustainability initiatives. The report outlined challenges including competitive pressures, stakeholder management, and macroeconomic uncertainties.

**key_points**

- Adoption of inventory ownership in quick commerce to expand revenue scope beyond marketplace commissions
- Strategic diversification across food delivery, quick commerce, going-out experiences, and B2B supply chains
- Focus on corporate governance, risk mitigation frameworks, and compliance with regulatory requirements
- Commitment to sustainability through energy conservation and operational efficiency measures

**important_risks**

- Intensifying competition in quick commerce and food delivery sectors
- Vulnerability to labor strikes and supply chain disruptions in distributed operations
- Macroeconomic volatility impacting consumer spending and logistics
- Potential for black swan events disrupting urban mobility and supply networks

**key_takeaway**

The company's strategic pivot to inventory ownership in quick commerce fundamentally reshaped its revenue model and operational focus, underscoring a shift from pure marketplace facilitation to integrated supply chain control.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0642 _(triage aid, NOT a score)_ |
| JSON repair needed | yes |
| Latency | 78.7751 s |
| Input / output tokens | 11807 / 581 |
| Tokens/sec (output) | 7.4 |

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

### Case 2 — `AR_LT_AR_29259_LT_2025_2026_A_29793480_14052026183032`

#### SOURCE / EVIDENCE

- **Symbol:** LT
- **Company:** Larsen & Toubro Limited
- **Fiscal year:** FY2025-26
- **Filing id:** AR_29259_LT_2025_2026_A_29793480_14052026183032
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 23, page ~14]
pment 
programme is in progress to fast-track 
the careers of potential leaders.  
Committed to create an inclusive 
work environment, your Company 
has introduced several career-assisting 
schemes for women and a number 
of women-friendly initiatives. These 
initiatives have significantly advanced 
our Lakshya 2026 gender diversity 
goal, with women employees now 
constituting close to 10% of the total 
workforce. The growing participation 
of women across both engineering and 
non-engineering roles is contributing 
to a more diverse and effective 
talent base. 
A culture of recognition and 
celebration continues to fuel 
high performance, foster healthy 
competition, and reinforces mutual 
respect among teams. This employee-
centric approach has once again 
earned the Company the prestigious 
‘Great Place to Work’ (GPTW) 
certification – for the third consecutive 
year, reaffirming L&T’s position as an 
employer of choice. 
Navigating the future 
together 
The global environment remains 
uncertain, and the near term may 
continue to see phases of volatility. 
Your Company, however, has 
navigated multiple cycles of disruption 
in recent decades. On each occasion, 
it has demonstrated resilience and 
emerged stronger, supported by the 
enduring trust and partnership of all 
its stakeholders — customers, vendor 
partners, investors, employees, as well 
as the government. This time too, 
your Company remains guided by its 
enduring mantra of ‘Can 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

The annual report for Larsen & Toubro Limited for FY 2024-25 highlighted the company's transformative year amidst global challenges, emphasizing its adaptability and commitment to sustainable infrastructure. Management reported a strong performance driven by digital adoption, enhanced project execution, and a robust order book, particularly in the Middle East and domestic markets. The report outlined strategic initiatives in energy transition, safety, and sustainability, alongside a focus on governance and stakeholder engagement.

**bullets**

- Management emphasized a commitment to sustainable infrastructure and energy transition.
- The company reported strong growth in digital adoption and project execution capabilities.
- Safety initiatives included a structured reward and penalty system linked to performance.
- L&T's diversified portfolio and international presence were highlighted as key strengths.
- The report outlined ongoing efforts in governance and stakeholder engagement.

**key_takeaway**

Management underscored the company's resilience and strategic positioning in a rapidly changing global landscape.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'Will'
- pass 2: forward-tense word 'Will'
- pass 3: forward-tense word 'Will'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ❌ no — failed validation after 3 attempts |
| Attempts used | 3 |
| Compliance — **Qwen** | ❌ FAIL — executive_summary: empty text |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0 _(triage aid, NOT a score)_ |
| JSON repair needed | yes |
| Latency | 169.6064 s |
| Input / output tokens | 34509 / 2413 |
| Tokens/sec (output) | 14.2 |

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

### Case 3 — `AR_BEL_AR_30214_BEL_2025_2026_A_16199415_05082026205636`

#### SOURCE / EVIDENCE

- **Symbol:** BEL
- **Company:** Bharat Electronics Limited
- **Fiscal year:** FY2025-26
- **Filing id:** AR_30214_BEL_2025_2026_A_16199415_05082026205636
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 23, page ~8]
 
he´efleYetefle he´ceeCe-he$e peejer keÀjvee, DeoeJeer G®eble Keelee keÀe oeJee / he´efleYetefle 
Type of holder
Process to be followed
The forms for updating the above details/
service request are available at - https://bel-
india.in/investors/#generalinfo and https://
ipostatus.integratedregistry.in/KYCRegister.
aspx.
Demat
Please contact your DP and register your email 
address, KYC details, update of signature, 
nomination/ Cancellation of nomination, bank 
account details etc in your demat account, as 
per the process advised by your DP.
11.	 Members are requested to note that, dividends if not 
encashed for a consecutive period of 7 years from the 
date of transfer to Unpaid Dividend Account of the 
Company, are liable to be transferred to the Investor 
Education and Protection Fund (‘IEPF’). The shares in 
respect of such unclaimed dividends are also liable to be 
transferred to the demat account of the IEPF Authority. 
In view of this, Members are requested to claim their 
dividends from the Company, within the stipulated 
timeline. The Members, whose unclaimed dividends/
shares have been transferred to IEPF, may claim the 
same by making an application to the IEPF Authority in 
Form No. IEPF-5 available on www.iepf.gov.in.
	
During FY 2025-26, an unclaimed/unpaid amount 
pertaining to the Final dividend 2017-18 and 1st 
Interim dividend 2018-19 were transferred to IEPF. The 
Company has posted on its website www.bel-india.in on 
a separa

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

The annual report for Bharat Electronics Limited (BEL) outlines the company's performance and strategic initiatives for the fiscal year 2025-26. Management highlighted a strong focus on innovation, sustainability, and expanding manufacturing capabilities, with significant investments in research and development. The report emphasized BEL's commitment to supporting India's defense sector while also addressing civilian market needs, showcasing a diverse product portfolio and a robust order book.

**bullets**

- Management emphasized a commitment to sustainability and reducing environmental impact.
- The report highlighted significant investments in R&D to drive innovation.
- Management stated a focus on expanding manufacturing capabilities and market presence.
- BEL aims to enhance its role in both defense and civilian sectors.
- The company reported a strong order book and growth in export sales.

**key_takeaway**

Management underscored BEL's strategic focus on innovation and sustainability as key drivers for future growth.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'target'
- pass 2: forward-tense word 'targets'
- pass 3: financial figure stated as fact '88%'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ❌ no — failed validation after 3 attempts |
| Attempts used | 3 |
| Compliance — **Qwen** | ❌ FAIL — executive_summary: empty text |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0 _(triage aid, NOT a score)_ |
| JSON repair needed | yes |
| Latency | 163.0882 s |
| Input / output tokens | 37143 / 2072 |
| Tokens/sec (output) | 12.7 |

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
