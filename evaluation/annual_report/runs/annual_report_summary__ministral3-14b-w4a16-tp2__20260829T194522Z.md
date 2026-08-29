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
| Cases | 20 of 20 |
| Run id | `20260829T194522Z` (2026-08-29T19:45:22.890584+00:00) |
| LLM project commit | `unknown` |
| GPU | 2x Tesla T4 (29.12 GB total) |
| CUDA / torch / vLLM | 13.0 / 2.13.0+cu130 / None |

## Objective signals (mechanical only — no judgement)

| Metric | Value |
|---|---|
| cases | 20 |
| generated_ok | 3 |
| generation_failures | 17 |
| candidate_compliance_failures | 17 |
| reference_backstop_artifacts | 0 |
| reference_compliance_failures | 0 |
| cases_with_reference | 20 |
| structured_output_used | 20 |
| json_repair_used | 0 |
| guided_and_clean | 20 |
| guided_but_repaired | 0 |
| unguided | 0 |
| mean_latency_sec | 139.252 |
| total_prompt_tokens | 755350 |
| total_completion_tokens | 35080 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| mean_lexical_overlap | 0.0072 |

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

- pass 1: forward-tense word 'targeting'
- pass 2: financial figure stated as fact '70%'
- pass 3: financial figure stated as fact '70%'

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
| Latency | 197.0165 s |
| Input / output tokens | 47974 / 2231 |
| Tokens/sec (output) | 11.3 |

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
- pass 2: forward-tense word 'targeted'
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
| Latency | 129.8275 s |
| Input / output tokens | 39552 / 1634 |
| Tokens/sec (output) | 12.6 |

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

### Case 3 — `AR_DIXON_AR_29048_DIXON_2024_2025_A_14468137_15092025224042`

#### SOURCE / EVIDENCE

- **Symbol:** DIXON
- **Company:** Dixon Technologies (India) Limited
- **Fiscal year:** FY2024-25
- **Filing id:** AR_29048_DIXON_2024_2025_A_14468137_15092025224042
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 11, page ~7]
vernment of India 
(“MCA”), and the Securities and Exchange Board of India 
(“SEBI”), have allowed companies to conduct Annual 
General Meetings through VC/OAVM, without the physical 
presence of members and, therefore, pursuant to General 
Circular Nos. 14/ 2020 dated 8th April 2020 and 17/2020 
dated 13th April 2020, followed by General Circular Nos. 
20/2020 dated 5th May 2020, and subsequent circulars 
issued in this regard, the latest being Circular No. 9/2024 
dated 19th September 2024 by the MCA (“MCA Circulars”) 
and 
SEBI 
Circular 
No. 
SEBI/HO/CFD/CFD-PoD-2/P/
CIR/2024/133 dated 3rd October 2024 issued by the SEBI 
(“SEBI Circular”) and in compliance with the provisions 
of the Act and SEBI (Listing Obligations and Disclosure 
Requirements) Regulations, 2015, as amended from 
time to time (“SEBI LODR Regulations”), the Company is 
convening the 32nd AGM through VC/OAVM, which does not 
require physical presence of members at a common venue.
2. 	
In accordance with the revised Secretarial Standard-2 
on General Meetings issued by the Institute of Company 
Secretaries of India (“ICSI”) read with Clarification / 
Guidance on applicability of Secretarial Standards - 1 and 2 
dated 15th April, 2020 issued by the ICSI, the proceedings of 
the AGM will be deemed to be conducted at the Registered 
Office of the Company at B-14 & 15, Phase – II, Noida – 
201305, India. 
3. 	
The Company has engaged KFin Technologies Limited, 
Registrar and Trans

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

Dixon Technologies (India) Limited's annual report for FY2024-25 outlines the company's strategic focus on engineering excellence and sustainable growth. Management emphasized their commitment to innovation, expanding into new product categories, and enhancing manufacturing capabilities, particularly in digital signage and telecom products. The report also highlighted ongoing investments in advanced technologies and a strong commitment to environmental, social, and governance (ESG) principles.

**bullets**

- Management emphasized a focus on engineering excellence and innovation.
- The company plans to expand into new product categories, including digital signage.
- Dixon is investing in advanced manufacturing capabilities and technologies.
- Management highlighted a commitment to sustainability and ESG principles.
- The report noted ongoing efforts to strengthen partnerships and global market presence.

**key_takeaway**

The most important qualitative point in the document is Dixon's commitment to engineering excellence and sustainable growth through innovation and advanced manufacturing.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact 'rs,'
- pass 2: financial figure stated as fact 'rs,'
- pass 3: financial figure stated as fact 'rs,'

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
| Latency | 144.4432 s |
| Input / output tokens | 40429 / 1862 |
| Tokens/sec (output) | 12.9 |

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

### Case 4 — `AR_LT_AR_29259_LT_2025_2026_A_29793480_14052026183032`

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

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact '10%'
- pass 2: forward-tense word 'targets'
- pass 3: financial figure stated as fact '10%'

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
| Latency | 147.9905 s |
| Input / output tokens | 38803 / 2044 |
| Tokens/sec (output) | 13.8 |

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

### Case 5 — `AR_ADANIPOWER_AR_29298_ADANIPOWER_2025_2026_A_16975380_29052026213520`

#### SOURCE / EVIDENCE

- **Symbol:** ADANIPOWER
- **Company:** Adani Power Limited
- **Fiscal year:** FY2025-26
- **Filing id:** AR_29298_ADANIPOWER_2025_2026_A_16975380_29052026213520
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 2, page ~2]
anies
1.
Corporate Overview
24	 India’s power demand
28	 Capacity Expansion at a Historical Scale
34	 Message from the Chairman
40 	 Letter from the MD and CEO
44 	 About the Company
50	 Assets Across the Country
54	 Technology and Digital Excellence
58	 Investment Case
2.
Contents
5.
6.
3.
Strategic Review
64 	 Business Model
68 	 Stakeholder Engagement 
76  	 Material Matters
86 	 Risk Management
92	 Strategy
98 	 Key Performance Indicators
100	Operational Performance
4.
Environmental, Social and Governance
Our ESG Approach
Environmental
194	 Occupational Health and Safety
204	 Social: Employees
232	 Responsible Sourcing
240	 Corporate Social Responsibility
264	 Corporate Governance
286	 Board of Directors
296	 Our Tax and Other Contributions
Statutory Reports
304	 Corporate Information
305	 Directors' Report
326	 Management Discussion & Analysis
338	 Corporate Governance Report
382	 Business Responsibility and   
	
Sustainability Report
440	 Assurance Statement
Financial Statements
448	 Standalone Financials
578	 Consolidated Financials
708	 Notice
The transformative changes
we are making will ensure
we are ready for the next
phase of our growth
- Gautam Adani

Business risks
R1
Mergers and 
acquisitions Risk
R2
Regulatory Risk
R3
Commodity price Risk
R4
Reputation Risk
S1
Expand capabilities to deliver the 
nation’s energy needs
S2
To contribute towards 
low carbon economy
S3
Leveraging digital technology to 
enhance sustainable business deli

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

Adani Power Limited's annual report for FY 2024-25 highlighted the company's commitment to sustainable growth and operational excellence in the thermal power sector. Management emphasized their strategic focus on expanding capacity through acquisitions and organic growth, aiming to meet India's increasing power demand while maintaining a strong emphasis on environmental responsibility. The report also detailed the company's initiatives in digital transformation and risk management, reinforcing their position as a leader in the energy sector.

**bullets**

- Management stated a plan to expand operational capacity significantly by 2030.
- The report described ongoing investments in ultra-supercritical technology to enhance efficiency and reduce emissions.
- Management highlighted a commitment to digital transformation to improve operational efficiency.
- The report emphasized strong governance practices and stakeholder engagement.
- Management outlined a proactive approach to risk management and sustainability initiatives.

**key_takeaway**

The most important qualitative point in the document is Adani Power's strategic commitment to expanding capacity while prioritizing sustainability and operational excellence.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'targeting'
- pass 2: financial figure stated as fact '3.7%'
- pass 3: financial figure stated as fact 'rs,'

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
| Latency | 164.234 s |
| Input / output tokens | 41454 / 2170 |
| Tokens/sec (output) | 13.2 |

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

### Case 6 — `AR_INFY_AR_29313_INFY_2025_2026_U_8985411_30052026200413`

#### SOURCE / EVIDENCE

- **Symbol:** INFY
- **Company:** Infosys Limited
- **Fiscal year:** FY2025-26
- **Filing id:** AR_29313_INFY_2025_2026_U_8985411_30052026200413
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 75, page ~38]
rtner, differentiated by strong 
account management, partnership 
orientation, and consistent delivery 
excellence supported by experienced 
subject-matter experts.
Tenured client relationships reinforce 
trust and business alignment, while 
proactive AI, automation, and 
strategic technology advisory are 
increasingly recognized as value 
drivers.
Clients indicate an expectation for 
forward-looking, business-led AI 
advisory to support the evolution 
of AI roadmaps, identification of 
high-value use cases, and scalable 
business outcomes, with Infosys 
viewed positively in this context.
Loyalty
2023-24
2024-25
2025-26
Advocacy
Satisfaction
Business value
Client satisfaction: Trend of key 
outcomes (scale 1 to 7)
Community
Digital skilling at scale
Infosys Springboard is Infosys’ 
flagship digital learning platform 
that empowers people with skills to 
be successful in the 21st century. Till 
date, we have reached 15 million+ 
people including employees, client’s 
workforce, students, teachers and 
communities with digital skilling 
initiatives.
Infosys Foundation 
Infosys Foundation has touched over 
7 million lives in the last year alone 
through its programs in the areas 
of education, healthcare, women 
empowerment, and environmental 
sustainability, among others, to create 
long-lasting impact. Recognizing 
that social innovations from the 
heart could transform societies, the 
Foundation launched the Aarohan 
Social Innovation Awards in 20

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

The Infosys Integrated Annual Report for FY2025-26 outlines the company's strategic focus on AI and digital transformation, emphasizing its AI First Value Framework to help clients unlock value at scale. Management highlighted the importance of reimagining legacy systems and processes to integrate AI effectively, while also addressing the need for responsible and ethical AI practices. The report also details Infosys' commitment to sustainability, showcasing initiatives aimed at achieving climate positivity and enhancing social responsibility through various community programs.

**bullets**

- Management emphasized the shift from AI experimentation to enterprise-scale adoption.
- The report outlined a commitment to sustainability and climate positivity.
- Infosys is focused on reimagining legacy systems to integrate AI effectively.
- The company aims to enhance social responsibility through community initiatives.
- Management highlighted the importance of responsible and ethical AI practices.

**key_takeaway**

Infosys is positioning itself as a leader in AI services, focusing on responsible integration of AI into enterprise systems while committing to sustainability and social responsibility.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'expectations'
- pass 2: financial figure stated as fact '85%'
- pass 3: forward-tense word 'expectations'

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
| Latency | 123.3319 s |
| Input / output tokens | 39841 / 1500 |
| Tokens/sec (output) | 12.2 |

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

### Case 7 — `AR_HINDZINC_AR_29349_HINDZINC_2025_2026_A_20195576_05062026130301`

#### SOURCE / EVIDENCE

- **Symbol:** HINDZINC
- **Company:** Hindustan Zinc Limited
- **Fiscal year:** FY2025-26
- **Filing id:** AR_29349_HINDZINC_2025_2026_A_20195576_05062026130301
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 65, page ~43]
sting Obligations and Disclosure Requirements) 
Regulations, 2015 and the prescribed Secretarial Standards
APPROACH TO
INTEGRATED REPORTING 
For detailed disclosures on our key non-financial or ESG aspects, 
refer to our Sustainability Report, which can be accessed on our 
website www.hzlindia.com
	 Indian Accounting Standards
	 National Guidelines on Responsible Business Conduct 
(NGRBC)
APPROACH TO MATERIALITY
Several issues, opportunities, and challenges can materially 
impact our business and our ability to create stakeholder 
value. Such matters form the base of disclosures in our 
Integrated Annual Report. We have identified by applying 
the principles of materiality, involving and gathering insights 
from all our business units and key stakeholders. We rank 
these issues as per their relevance and potential impact on 
stakeholders, strategy, and value creation, helping us shape 
future-ready business strategies and goals.
Read more on our material topics on 
page 80 of this Report.
BOARD AND MANAGEMENT ASSURANCE
The Board of Directors and the management of Hindustan 
Zinc acknowledge their shared responsibility for the integrity 
and completeness of the information contained in it. They 
have applied their collective knowledge and have been 
actively involved in the Report’s development. They are of 
the opinion that the Report captures all relevant material 
issues, and presents an accurate, fair, and balanced view of 
Hindustan Zinc’s 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

The annual report for Hindustan Zinc Limited for FY2024-25 highlighted the company's commitment to sustainability and innovation in the mining sector. Management emphasized their leadership in critical minerals, particularly zinc and silver, which are essential for the global energy transition. The report detailed strategic initiatives aimed at capacity expansion, technological advancements, and enhancing operational efficiencies, while also focusing on community development and environmental stewardship.

**bullets**

- Management emphasized leadership in critical minerals and sustainability.
- The report outlined plans for capacity expansion and technological innovation.
- Management highlighted community development initiatives and environmental stewardship.
- The company aims to enhance operational efficiencies and reduce production costs.

**key_takeaway**

Hindustan Zinc Limited is focused on becoming a leader in critical minerals while committing to sustainability and community development.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'outlook'
- pass 2: financial figure stated as fact '100%'
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
| Latency | 156.6428 s |
| Input / output tokens | 40355 / 2104 |
| Tokens/sec (output) | 13.4 |

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

### Case 8 — `AR_ASIANPAINT_AR_29385_ASIANPAINT_2025_2026_A_26278926_12062026160918`

#### SOURCE / EVIDENCE

- **Symbol:** ASIANPAINT
- **Company:** Asian Paints Limited
- **Fiscal year:** FY2025-26
- **Filing id:** AR_29385_ASIANPAINT_2025_2026_A_26278926_12062026160918
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 1, page ~1]
of the AGM and Integrated 
Annual Report for the financial year 2025-26 can be accessed is being sent. 
 
The Notice of the AGM along with the Integrated Annual Report for the financial year 2025-26 is 
also uploaded on the Company’s website at https://www.asianpaints.com/AnnualReports.html and 
the website of National Securities Depository Limited at www.evoting.nsdl.com. 
 
You are requested to take the above information on record. 
 
Thanking you, 
 
Yours truly, 
 
For ASIAN PAINTS LIMITED  
 
 
 
R J JEYAMURUGAN 
CFO & COMPANY SECRETARY 
 
Encl.: As above 
JEYAMURUGAN 
RAMALINGAM 
JEYAPANDIYAN
Digitally signed by 
JEYAMURUGAN 
RAMALINGAM 
JEYAPANDIYAN 
Date: 2026.06.12 15:57:21 
+05'30'

Integrated Annual Report 2025-26
Bringing joy 
to people’s lives 
Responsible. Resilient. Radiant.

PINK MIST
Bringing joy  
to people’s lives
IMPACT THAT TRANSCENDS JOY
About this report 
FY 2025-26 highlights  
ESG performance snapshot
Corporate Overview
Asian Paints at a glance 
Our products and services 
Our global footprint 
Chairman’s letter  
MD & CEO’s message  
Board of Directors
Management Discussion and Analysis
Macroeconomic landscape 
Business review 
Financial review
Managing risks
Awards and recognitions
Ten-year review
Value Proposition
Value creation model 
Stakeholder engagement 
Materiality 
Innovation and manufacturing excellence 
INSIDE OUR 
CANVAS
ESG PERFORMANCE REVIEW
Sustainable operations 
Synergising relationships

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

The Integrated Annual Report for FY 2025-26 from Asian Paints Limited outlines the company's commitment to sustainability, innovation, and market leadership in the decorative coatings sector. Management emphasized a strategic focus on brand equity, regional market execution, and the expansion of service offerings to enhance consumer engagement. The report also highlights the company's dedication to environmental stewardship and ethical governance, aiming to create long-term value for stakeholders while navigating a dynamic market landscape.

**bullets**

- Management emphasized a commitment to sustainability and responsible business practices.
- The report highlighted a focus on innovation and product differentiation to enhance market positioning.
- Management stated a plan to deepen regional market execution and consumer engagement.
- The company aims to expand its service offerings to provide comprehensive solutions for customers.

**key_takeaway**

Asian Paints Limited's report underscores its strategic focus on sustainability, innovation, and enhancing consumer experiences in a competitive market.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'forecasting'
- pass 2: forward-tense word 'forecasting'
- pass 3: forward-tense word 'forecasting'

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
| Latency | 148.1554 s |
| Input / output tokens | 41522 / 1864 |
| Tokens/sec (output) | 12.6 |

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

### Case 9 — `AR_TECHM_AR_29435_TECHM_2025_2026_A_15304795_23062026234616`

#### SOURCE / EVIDENCE

- **Symbol:** TECHM
- **Company:** Tech Mahindra Limited
- **Fiscal year:** FY2025-26
- **Filing id:** AR_29435_TECHM_2025_2026_A_15304795_23062026234616
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 51, page ~34]
erations with 
over 50 employees.
External assurance
This Report has been assured by Third 
Party Auditors, DNV Business Assurance 
India Private Limited (“DNV”). The scope and 
basis of assurance have been described 
in the Assurance Statement issued by 
DNV on page 80. 
Safe harbour
Certain statements in this Report 
concerning our future growth prospects 
are forward-looking in nature, which involve 
a number of risks, and uncertainties that 
could cause our actual results to differ 
materially from those expressed or implied 
in such forward-looking statements. 
Global geopolitical and socio-economic 
conditions, in particular, the continuing 
impact of wars, climate-change impact, 
could affect customers’ technology 
spending, delay purchasing decisions, affect 
demand for our services; all of which could 
adversely affect our future revenues, 
margins and overall financial performance. 
Our operations may also be affected by a 
range of other external factors that are 
beyond our control. 
We do not undertake to update any 
forward-looking statement that may 
be made from time to time, by us 
or on our behalf.
Corporate Information 
Directors’ Report
Management Discussion and Analysis 
Corporate Governance Report
Business Responsibility and 
Sustainability Report  
Standalone
Consolidated
 
Statutory Reports
Financial Statements
Integrated Data 
Governance and 
Cybersecurity
Supply Chain 
Management 
Co-innovation
Product Social 
Responsibi

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

Tech Mahindra Limited's annual report for the fiscal year 2025-26 outlines the company's strategic focus on AI-driven transformation and operational excellence. Management emphasized the importance of integrating AI into core business processes to enhance productivity and innovation while maintaining a commitment to sustainability and stakeholder engagement. The report also highlights the company's achievements in expanding its client base and improving operational margins, alongside a strong emphasis on governance and responsible AI practices.

**bullets**

- Management highlighted a commitment to AI-driven transformation.
- The report emphasized operational excellence and margin improvement.
- Sustainability and stakeholder engagement were key strategic focuses.
- Tech Mahindra aims to integrate AI into core business processes.
- The company reported strong client acquisition and retention efforts.

**key_takeaway**

The most significant qualitative point in the document is Tech Mahindra's strategic commitment to AI integration and operational excellence as a means to drive sustainable growth.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'targets'
- pass 2: financial figure stated as fact '58.8%'
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
| Latency | 151.8069 s |
| Input / output tokens | 41028 / 1959 |
| Tokens/sec (output) | 12.9 |

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

### Case 10 — `AR_CGPOWER_AR_29493_CGPOWER_2025_2026_A_11109518_30062026162136`

#### SOURCE / EVIDENCE

- **Symbol:** CGPOWER
- **Company:** CG Power and Industrial Solutions Limited
- **Fiscal year:** FY2025-26
- **Filing id:** AR_29493_CGPOWER_2025_2026_A_11109518_30062026162136
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 30, page ~10]
able future.
We value people, 
partnerships, and the 
planet, thereby fostering 
collaboration and 
inclusivity while advancing 
solutions that are both 
socially responsible 
and environmentally 
conscious.
OWNERSHIP MINDSET
INTEGRITY
RESPECT
CG EDGE is our enterprise-wide way of working that drives execution 
excellence, operational discipline, and continuous improvement across the 
organization.
Embedded across all levels, from leadership teams to the shop ﬂoor— EDGE 
serves as the backbone of how we operate, collaborate, solve problems, and 
create value. 
More than a framework, EDGE enables us to remain agile, customer-focused, 
and future-ready while delivering sustainable business outcomes.
Together, these values foster a culture of trust, accountability, collaboration, and continuous improvement—enabling us to deliver excellence in 
everything we do.
Corporate Overview 
CONTENTS
02   CORPORATE OVERVIEW
22   STATUTORY REPORTS
187   FINANCIAL STATEMENTS
377   ADDITIONAL INFORMATION
Pioneering Innovation for a Sustainable Future
Company Overview
Key Sectors We Serve
Chairman's Message
Managing Director & CEO’s Message
Board of Directors
Corporate Information
Ten Years’ Highlights
Management Discussion and Analysis
Directors’ Report
Report on Corporate Governance
Business Responsibility and Sustainability Report
Standalone Financials
Consolidated Financials
Products and Services
Establishments

Corporate Overview 
Financial Statements
Statuto

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

CG Power and Industrial Solutions Limited's annual report for FY2025-26 highlighted the company's commitment to innovation and sustainability, emphasizing its purpose of 'Pioneering Innovation for a Sustainable Future.' Management noted significant progress in expanding global presence and enhancing manufacturing capabilities, particularly in power systems and semiconductors. The report also detailed strategic investments in technology and a focus on operational excellence through the CG EDGE framework, which aims to align strategy with execution across the organization.

**bullets**

- Management emphasized a commitment to sustainability and innovation.
- The company focused on expanding its global presence and manufacturing capabilities.
- Strategic investments were made in technology and operational excellence.
- CG EDGE framework was highlighted as a key driver for execution and performance.

**key_takeaway**

The most important qualitative point in the document is CG Power's commitment to pioneering innovation while ensuring sustainable practices across its operations.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact '12%'
- pass 2: financial figure stated as fact 'rs,'
- pass 3: financial figure stated as fact 'rs,'

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
| Latency | 134.8476 s |
| Input / output tokens | 37451 / 1876 |
| Tokens/sec (output) | 13.9 |

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

### Case 11 — `AR_M&M_AR_29572_M&M_2025_2026_A_16591991_04072026174358`

#### SOURCE / EVIDENCE

- **Symbol:** M&M
- **Company:** Mahindra & Mahindra Limited
- **Fiscal year:** FY2025-26
- **Filing id:** AR_29572_M&M_2025_2026_A_16591991_04072026174358
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 10, page ~3]
ERS
Integrated Annual Report 2025-26

CONTENTS
Integrated Annual Report 2025-26
CONTENTS
CHAIRMAN’S
 
MESSAGE
GROUP CEO &
 
MD’S MESSAGE
PERFORMANCE
 
HIGHLIGHTS
GROUP
 
OVERVIEW
 
THE MAHINDRA GROUP
 
BOARD OF DIRECTORS
 
GROUP EXECUTIVE BOARD
 
AWARDS & ACCOLADES
RISE TO
 
CREATE VALUE
 
GROUP STRATEGIC OVERVIEW
 
RISK MANAGEMENT
 
OPPORTUNITIES & OUTLOOK
GROUP
 
VALUE CREATION
 
MODEL
RISE TO BE
 
FUTURE-READY
 
MANUFACTURING CAPABILITIES
 
DIGITAL & AI CAPABILITIES
 
NEW PRODUCTS & MILESTONES
RISE FOR A MORE
 
EQUAL WORLD
 
ESG STRATEGY
 
PEOPLE & CULTURE
 
SOCIAL IMPACT
CORPORATE
 
INFORMATION
STATUTORY
 
REPORTS
 
BOARD’S REPORT
 
MANAGEMENT DISCUSSION AND
 
ANALYSIS
 
CORPORATE GOVERNANCE
 
BUSINESS RESPONSIBILITY AND
 
SUSTAINABILITY REPORT
FINANCIAL
 
STATEMENTS
 
STANDALONE ACCOUNTS
 
CONSOLIDATED ACCOUNTS
Announcement
In FY17, Mahindra & Mahindra Ltd. embarked on the journey 
towards Integrated Reporting in keeping with the 
commitment to transparency and the highest standards of 
corporate governance. Since then, our reporting structure 
has continued to evolve. While staying true to the principles 
of the IFRS Foundation’s International Integrated Reporting 
<IR> Framework, we have enhanced the format, clarity, and 
accessibility of the report to offer a more reader-friendly 
and connected experience.
Integrated Reporting takes corporate disclosures beyond 
ﬁnancial performance. It recognises that sustainable value 
creation relies on

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

Mahindra & Mahindra Ltd.'s annual report for FY2024-25 outlines the company's strategic focus on resilience and adaptability in a volatile global environment. Management emphasized the importance of aligning business strategies with national objectives, particularly in sectors like renewable energy and electric vehicles, to capitalize on India's growth potential. The report also highlighted the company's commitment to sustainability, innovation, and creating shared value through various initiatives aimed at empowering communities and enhancing operational efficiency.

**bullets**

- Management emphasized resilience as a core value for navigating uncertainty.
- The company aims to align its strategies with national initiatives like 'Make in India'.
- Sustainability and innovation are central to Mahindra's growth strategy.
- Management highlighted the importance of digital transformation in enhancing operational efficiency.
- The report detailed ongoing efforts in renewable energy and electric vehicle sectors.

**key_takeaway**

The report underscores Mahindra's commitment to resilience, sustainability, and alignment with national growth objectives as key drivers of its business strategy.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact 'rs,'
- pass 2: financial figure stated as fact 'rs,'
- pass 3: financial figure stated as fact 'rs,'

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
| Latency | 130.4056 s |
| Input / output tokens | 40375 / 1599 |
| Tokens/sec (output) | 12.3 |

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

### Case 12 — `AR_CHOLAFIN_AR_29596_CHOLAFIN_2025_2026_A_8171029_06072026201106`

#### SOURCE / EVIDENCE

- **Symbol:** CHOLAFIN
- **Company:** Cholamandalam Investment and Finance Company Limited
- **Fiscal year:** FY2025-26
- **Filing id:** AR_29596_CHOLAFIN_2025_2026_A_8171029_06072026201106
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 29, page ~16]
 are also eligible to apply. The securities that are lodged/re-lodged for transfer as mentioned above, if 
in order, will be issued in demat mode only. Investors may write to the Company or RTA in this regard.

INTEGRITY
PASSION
QUALITY
RESPECT
RESPONSIBILITY
Rooted in values. Driven by purpose.
Creating progress that lasts.
A N N U A L R E P O R T
2025-26








Cholamandalam Investment and Finance Company Limited
Annual Report / 2025-26
Across this report, the word ‘Chola’ refers to ‘Cholamandalam Investment and 
Finance Company Limited.’
Forward-looking statement
In this Annual Report we may have disclosed forward-looking information to enable 
investors to comprehend our prospects and take informed investment decisions. 
This report and other statements - written and oral - that we periodically make, 
may contain forward-looking statements that set out anticipated results based on 
the management’s plans and assumptions. We have tried wherever possible to 
identify such statements by using words such as ‘anticipates’, ‘estimates’, ‘expects’, 
‘projects’, ‘intends’, ‘plans’, ‘believes’ and words of similar substance in connection 
with any discussion of future performance.
We cannot guarantee that these forward-looking statements will be realised, 
although we believe we have been prudent in our assumptions. The achievement of 
results is subject to risks, uncertainties and inaccurate assumptions. Should known 
or unknown ris

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

The annual report for Cholamandalam Investment and Finance Company Limited for FY 2024-25 highlighted the company's commitment to transforming lives and elevating communities through accessible financial solutions. Management emphasized their focus on expanding their presence in underserved markets, particularly in Tier-III to Tier-VI towns, and enhancing customer engagement through digital transformation. The report also detailed the company's strategic initiatives in various business segments, including vehicle finance, home loans, and small and medium enterprise loans, aimed at fostering economic growth and financial inclusion.

**bullets**

- Management emphasized a commitment to financial inclusion in underserved markets.
- The report highlighted digital transformation as a key strategy for enhancing customer experience.
- Chola's focus on expanding its product offerings includes new segments like gold loans and consumer durables.
- Management underscored the importance of sustainable practices and corporate social responsibility initiatives.
- The company aims to strengthen its operational foundations while driving growth across various business segments.

**key_takeaway**

Cholamandalam's strategic focus on financial inclusion and digital transformation aims to empower underserved communities and enhance customer engagement.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact 'rs,'
- pass 2: financial figure stated as fact 'rs,'
- pass 3: forward-tense word 'targeting'

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
| Latency | 157.1386 s |
| Input / output tokens | 41689 / 2021 |
| Tokens/sec (output) | 12.9 |

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

### Case 13 — `AR_BAJFINANCE_AR_29642_BAJFINANCE_2025_2026_A_23098027_07072026220255`

#### SOURCE / EVIDENCE

- **Symbol:** BAJFINANCE
- **Company:** Bajaj Finance Limited
- **Fiscal year:** FY2025-26
- **Filing id:** AR_29642_BAJFINANCE_2025_2026_A_23098027_07072026220255
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 76, page ~47]
e: 29 April 2026
Place: Pune

39th ANNUAL REPORT
2025-2026

Corporate  
Overview
FY2026: Highlights
Chairman’s Letter
Our Leadership
Corporate Information
Our Products
Digital-first Engagement Driving 
Financial Inclusion
FINAI Transformation
Bold Reimagination of Finance with AI
People and Culture
Our ESG Priorities
Corporate Social Responsibility
Our Refreshed Brand Identity
02-32
Contents
33-223
Statutory 
Reports
Management Discussion and Analysis
Directors’ Report
119 Report on Corporate Governance
150 General Shareholder Information
161 Business Responsibility &  
 
Sustainability Report
225-479
Financial  
Statements
225 Standalone Financial Statements
365 Consolidated Financial Statements
A Founding Principle. 
Financial Inclusion.
A Transformative Purpose 
BFL was born in 1986-87 as a captive auto-financing 
unit to make mobility affordable to India's middle 
classes. Its first customers were school teachers from 
Solapur, who sought loans to buy two-wheelers to 
reach villages where they taught. That act of enabling 
aspiration became the template for the future and 
a steady march toward bringing millions into India’s 
formal financial system.
Built for Scale
Today, BFL is India’s largest private sector NBFC, 
serving 1 in 3 Indian households, disbursing a loan 
every second, and offering the full suite of financial 
products: loans, Fixed Deposits, payments, insurance, 
mutual funds, and wealth management, across App, 
Web and Pan-In

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

The annual report for Bajaj Finance Limited outlines the company's performance and strategic initiatives for FY2026. Management highlighted significant growth in customer franchise and assets under management, emphasizing a commitment to financial inclusion and digital transformation through AI. The report also details governance changes, including board member retirements and reappointments, as well as plans for capital allocation and related party transactions.

**bullets**

- Management emphasized a focus on financial inclusion and digital transformation.
- The report detailed governance changes, including board member retirements.
- Management outlined plans for capital allocation and related party transactions.
- The company aims to enhance operational efficiency through AI integration.

**key_takeaway**

Management underscored a commitment to leveraging AI for operational efficiency and customer engagement.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact '1.01%'
- pass 2: forward-tense word 'target'
- pass 3: financial figure stated as fact '1.01%'

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
| Latency | 146.1626 s |
| Input / output tokens | 39350 / 1974 |
| Tokens/sec (output) | 13.5 |

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

### Case 14 — `AR_MANKIND_AR_29682_MANKIND_2025_2026_A_16593335_09072026165705`

#### SOURCE / EVIDENCE

- **Symbol:** MANKIND
- **Company:** Mankind Pharma Limited
- **Fiscal year:** FY2025-26
- **Filing id:** AR_29682_MANKIND_2025_2026_A_16593335_09072026165705
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 30, page ~11]
an Resources.....................................................74
Overview of Business Functions
ESG Goals.................................................................. 78
Environmental........................................................... 80
Social .......................................................................... 84
Governance............................................................... 88
ESG Matters
Management Discussion and Analysis.............. 96
Board’s Report........................................................113
Corporate Governance Report ..........................143
Business Responsibility and  
Sustainability Report............................................173
Statutory Reports
Standalone Financial Statements.....................229
Consolidated Financial Statements..................384
Financial Statements
Financial Highlights................................................ 36
10-Year Business Highlights................................. 38
Therapy-Wise Performance ................................ 40
Awards and Recognition....................................... 42
Performance Review
Mankind is the youngest 
pharmaceutical company 
amongst Top 5 in IPM, 
with a stronger presence 
in India. Operating across 
pharmaceutical formulations 
and consumer healthcare, 
the Company is committed to 
improving lives through quality 
healthcare that is accessible, 
affordable and innovation-led. 
To view this report o

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

The annual report for Mankind Pharma Limited for the fiscal year 2024-25 outlines the company's strategic focus on expanding its presence in chronic and specialty therapies, enhancing its consumer healthcare segment, and integrating sustainability into its operations. Management highlighted the acquisition of Bharat Serums and Vaccines Limited as a significant step towards strengthening its super-specialty portfolio. The report emphasized ongoing investments in research and development, digital transformation, and a commitment to quality and compliance across all operations.

**bullets**

- Management emphasized a focus on chronic and specialty therapies.
- The acquisition of Bharat Serums and Vaccines Limited was highlighted as a strategic move.
- Sustainability initiatives are integrated into operational practices.
- Investments in R&D and digital transformation are ongoing priorities.

**key_takeaway**

Management's strategic focus includes expanding into chronic and specialty therapies while enhancing sustainability and digital capabilities.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact 'rs,'
- pass 2: financial figure stated as fact 'rs,'
- pass 3: financial figure stated as fact 'rs,'

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
| Latency | 155.8744 s |
| Input / output tokens | 41464 / 2014 |
| Tokens/sec (output) | 12.9 |

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

### Case 15 — `AR_SIEMENS_AR_29759_SIEMENS_2024_2026_A_21354062_13072026172733`

#### SOURCE / EVIDENCE

- **Symbol:** SIEMENS
- **Company:** Siemens Limited
- **Fiscal year:** FY2024-26
- **Filing id:** AR_29759_SIEMENS_2024_2026_A_21354062_13072026172733
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 5, page ~4]
iconductors, batteries and green hydrogen. 
The Company further strengthened its position through several significant milestones in the Mobility business. A particularly 
proud moment for Siemens was the flagging off by the Hon’ble Prime Minister of India Shri Narendra Modi of the first of the 
new D9 – 9,000 HP electric locomotives for Indian Railways from the Dahod factory in Gujarat. This milestone is part of the 
landmark project for the design, engineering, manufacturing, and maintenance of 1,200 locomotives. Approximately 90% of 
the technologies for these are Made in India. 
The Company also reinforced its role in India’s next-generation rail infrastructure through the award of a landmark contract 
for the country’s first high-speed rail project, under which a Siemens-led consortium will deliver advanced ETCS Level 2-based 
signaling and telecommunication technologies for the Mumbai–Ahmedabad corridor, supporting train operations at speeds 
of up to 350 km/h. In addition, the Company secured orders for advanced signaling and telecommunication technologies for 
Nagpur Metro Rail Project Phase 2, further strengthening its presence in urban mobility through solutions that enhance safety, 
punctuality, energy efficiency and passenger experience. The Company also received an internal work allocation from its group 
company for manufacturing and supply of bogies, traction motors and gearboxes, valued at ` 18.25 billion.

Annual Report 2026
Siemens

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

Siemens Limited's annual report for FY 2024-26 highlighted a period of transition and resilience amid global economic challenges. Management emphasized the company's alignment with India's growth priorities in electrification, automation, and infrastructure, while also focusing on sustainability and technology leadership. The report detailed significant milestones, including the successful demerger of the Energy business and advancements in rail infrastructure projects, showcasing the company's commitment to innovation and market leadership.

**bullets**

- Management emphasized alignment with India's growth priorities in electrification and automation.
- The report highlighted the successful demerger of the Energy business.
- Management noted advancements in rail infrastructure projects as key milestones.
- Sustainability and technology leadership were central themes in the company's strategy.
- The company focused on enhancing operational efficiency and customer relevance.

**key_takeaway**

The report underscored Siemens Limited's strategic focus on sustainability, technology leadership, and alignment with India's infrastructure development goals.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact '90%'
- pass 2: financial figure stated as fact 'rs,'
- pass 3: financial figure stated as fact 'rs,'

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
| Latency | 152.5476 s |
| Input / output tokens | 41156 / 1971 |
| Tokens/sec (output) | 12.9 |

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

### Case 16 — `AR_CUMMINSIND_AR_29916_CUMMINSIND_2025_2026_U_15157578_20072026204111`

#### SOURCE / EVIDENCE

- **Symbol:** CUMMINSIND
- **Company:** Cummins India Limited
- **Fiscal year:** FY2025-26
- **Filing id:** AR_29916_CUMMINSIND_2025_2026_U_15157578_20072026204111
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 22, page ~17]
ncial Officer and Company Secretary. 
During his 38-year association with the Tatas, he has been on the boards of various Tata 
companies and is currently the Vice Chairman of Tata Investment Corporation Limited and 
serves on the boards of Tata Capital and Tata Industries. He is also the Non-Executive 
Chairman of DCB Bank Limited. In the past, Farokh has been the President of the Bombay 
Chamber of Commerce and Industry. He holds a bachelor’s degree in commerce and is a 
Member of The Institute of Chartered Accountants of India and The Institute of Company 
Secretaries of India.
FAROKH N. SUBEDAR  
INDEPENDENT DIRECTOR 
Sekhar Natarajan is a Non-Executive Independent Director at Cummins India Limited. In 
his long career, Sekhar has led and built Monsanto India as a leading growth and innovation 
company in the agriculture sector, first as its Managing Director, then as South Asia Leader 
and later as both Executive and Non-Executive Chairman of its Board, until its merger with 
Bayer in 2019. He is a recognized leader and a strategic thinker with rich global experience 
in Business Development and Mergers & Acquisitions. Currently, he is the Managing Partner 
of M/s SN Consultants and a Founding Partner of AgVaya LLP, where he provides strategic 
advice and guidance to local and international companies. He also works closely with industry 
forums on policy and advocacy matters. 
SEKHAR NATARAJAN  
INDEPENDENT DIRECTOR*
Vibha Paul Rishi is a No

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

Cummins India Limited's annual report for FY 2024-25 highlighted the company's commitment to innovation, sustainability, and inclusive growth. Management emphasized the importance of their 'Destination Zero™' strategy, which focuses on reducing emissions and enhancing product offerings to meet stringent environmental standards. The report also detailed the company's efforts in fostering a diverse and inclusive workplace, alongside significant advancements in technology and manufacturing capabilities to support India's energy transition and infrastructure development.

**bullets**

- Management emphasized a commitment to sustainability through the 'Destination Zero™' strategy.
- The report highlighted ongoing investments in innovation and technology to enhance product offerings.
- Management focused on fostering a diverse and inclusive workplace culture.
- The company aims to support India's energy transition and infrastructure development.
- Management noted strong partnerships with key sectors such as railways, defense, and marine.

**key_takeaway**

The most important qualitative point in the document is Cummins India's strategic focus on sustainability and innovation to drive growth and support India's energy transition.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**executive_summary**

The FY2025-26 annual report of Cummins India Limited highlights a strategic focus on localization and sustainability, with continued investment in manufacturing and product innovation to align with India’s ‘Make in India’ and ‘Atmanirbhar Bharat’ initiatives. Management emphasized growth in high-horsepower engines, cleaner technology adoption, and expansion into alternate energy solutions, while also addressing regulatory pressures on emissions. The report underscores robust governance, including a structured risk management framework and compliance with SEBI’s corporate governance norms, alongside a commitment to ESG and social responsibility through initiatives like the Nurturing Brilliance Scholarship Program and Cummins College of Engineering for Women.

**key_points**

- Management stated a focus on **localization and ‘Make in India’ alignment**, investing in domestic manufacturing to support government-driven industrial growth and supply chain resilience.
- The company emphasized **sustainability and decarbonization**, including Product Carbon Footprint certification for engines and compliance with stricter emission norms, while positioning itself for future demand in cleaner energy solutions.
- Strategic priorities included **expansion in high-horsepower engines** for data centers and industrial applications, alongside aftermarket growth driven by maintenance and service contracts in sectors like railways and infrastructure.
- Governance structures were reinforced with a **Risk Management Committee** overseeing enterprise-wide risk, cybersecurity, and compliance, alongside a **Corporate Social Responsability and Sustainability Committee** focusing on ESG reporting and stakeholder initiatives.
- Leadership development and talent deployment were highlighted as core HR strategies, with programs like the ‘Hire-to-Develop’ philosophy and global leadership training initiatives to build future-ready capabilities.

**important_risks**

- The report noted **geopolitical and trade policy uncertainties** as potential headwinds, including tariff announcements and supply chain disruptions that could impact global demand and commodity markets.
- Regulatory pressures were identified, particularly from **emission control mandates** (e.g., NGT/CAQM directives) requiring retrofitting of diesel generators and adoption of cleaner technologies, which may entail higher R&D and compliance costs.
- Market volatility in **crude oil and energy prices** was flagged as a risk, given India’s reliance on imports and the direct impact on operational costs and pricing strategies.
- The company acknowledged **external demand uncertainty** in key sectors like infrastructure and construction, which could affect utilization rates and aftermarket revenue streams.

**key_takeaway**

The report positioned Cummins India’s growth strategy on **localized manufacturing, sustainability leadership, and aftermarket expansion**, while navigating regulatory and macroeconomic risks through a structured governance and risk management framework.

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'targets'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 2 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0469 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 96.8604 s |
| Input / output tokens | 25958 / 1035 |
| Tokens/sec (output) | 10.7 |

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

### Case 17 — `AR_SBILIFE_AR_29974_SBILIFE_2025_2026_A_12296748_23072026224207`

#### SOURCE / EVIDENCE

- **Symbol:** SBILIFE
- **Company:** SBI Life Insurance Company Limited
- **Fiscal year:** FY2025-26
- **Filing id:** AR_29974_SBILIFE_2025_2026_A_12296748_23072026224207
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 32, page ~11]
s of the 
Comptroller and Auditor 
General of India (C&AG)
272	 	Financial Statements
Additional Information 
482	 	Embedded Value Report 
485	 	Independent Actuary’s Opinion
486	 	Corporate Information 
487	 	Glossary of Terms
Scan the QR 
code to view 
this report 
online
REPORT
IN THIS

Approach to Reporting
At SBI Life Insurance Company Limited, our approach to reporting reflects the way we run the business, 
integrated, transparent and aligned to long-term value creation.
As we complete over 25 years of operations, our reporting philosophy has evolved from presenting 
financial outcomes to delivering a more connected view of performance, bringing together strategy, 
governance, risk, sustainability and stakeholder engagement into a cohesive narrative.
This Integrated Annual Report for FY26 provides a balanced perspective of our financial and non-
financial performance, key priorities, risks and opportunities, aligned with regulatory requirements and 
global best practices.
Reporting Objective
Our objective is to present relevant, 
consistent and comparable 
information that enables stakeholders 
to make well-informed decisions. 
Scope and Boundary
This Report covers SBI Life’s 
operations and performance for the 
period April 1, 2025 to March 31, 
2026, including both financial and 
non-financial aspects.
Reporting Framework
This Report has been prepared in 
compliance with applicable laws and 
regulations, including:
 Insurance Act, 1938, 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

SBI Life Insurance Company Limited's Integrated Annual Report for FY 2025-26 outlines the company's commitment to building trust and providing financial protection to Indian families over its 25-year history. The report highlights the company's strategic focus on customer-centric growth, digital transformation, and sustainable practices, emphasizing its role in enhancing insurance accessibility across diverse demographics. Management stated a goal of expanding its distribution network and product offerings to meet evolving customer needs while maintaining strong governance and risk management practices.

**bullets**

- Management emphasized a commitment to customer-centric growth and digital transformation.
- The report highlighted the importance of sustainability and responsible business practices.
- Management stated a focus on expanding insurance accessibility across underserved markets.
- The company aims to enhance its distribution network and product offerings.
- Strong governance and risk management practices were underscored as key priorities.

**key_takeaway**

The report emphasizes SBI Life's commitment to trust, customer-centricity, and sustainable growth as it marks 25 years in the insurance industry.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**executive_summary**

SBI Life Insurance’s FY2025-26 Integrated Annual Report emphasizes its **25-year legacy of trust-based growth**, positioning itself as a leader in India’s evolving life insurance sector. The company highlights **five strategic pillars**—distribution reach, sustainable value creation, customer experience, workforce development, and digital expansion—while aligning with **regulatory reforms (e.g., Sabka Bima Sabki Raksha Act, 2025)** and **global ESG standards**. Management underscores **technology-driven innovation** (AI, IoT, RPA) and **stakeholder-centric governance**, including board oversight of risk, investment, and sustainability. The report also reflects a **shift toward protection and retirement products**, driven by demographic trends and rising financial awareness in India.

**key_points**

- Management stated a **long-term strategy** centered on **five interconnected capitals**: human (skilled workforce), financial (prudent capital management), service (distribution network), social (customer/partner relationships), and digital (technology-driven capabilities).
- The company **prioritizes sustainable growth** through **enhanced customer engagement**, **expanded digital footprints**, and **product innovation** (e.g., retirement solutions, ULIPs), while maintaining a **robust distribution model** (agents, bancassurance, digital channels).
- SBI Life **aligns with regulatory reforms** (e.g., increased FDI limits, universal insurance coverage by 2047) and **global reporting frameworks** (<IR>, SEBI LODR), emphasizing **transparency, governance, and ESG integration** (e.g., CSR, sustainability committees).
- The **Board’s oversight** includes dedicated committees for **risk management, investment, corporate governance, and ESG**, with a focus on **actuarial soundness, cybersecurity, and stakeholder accountability**. Independent directors confirm compliance with **ICSI Secretarial Standards and IRDAI regulations**.
- Awards and recognitions (e.g., **ET Now Insurance Summit, ICC Emerging Asia Conclave, ICAI Financial Reporting Excellence**) underscore **operational resilience, digital transformation, and social impact initiatives** (e.g., healthcare CSR, financial inclusion).

**important_risks**

- Management acknowledged **geopolitical and macroeconomic uncertainties** (e.g., global inflation, interest rate volatility) as potential risks to **investment performance and market-linked products** (e.g., ULIPs).
- The report highlighted **regulatory risks**, including **IRDAI’s evolving guidelines** (e.g., product mix shifts, solvency requirements) and **litigation exposures**, though no material contingent liabilities were disclosed.
- Operational risks were mitigated through **proactive risk management frameworks**, including **quarterly investment reviews, concurrent audits, and exception-reporting mechanisms** for process compliance (e.g., underwriting, claims).
- Stakeholder risks were addressed via **enhanced governance structures**, such as the **Board Stakeholders’ Relationship and Sustainability Committee**, focusing on **ESG alignment and policyholder protection** (e.g., extended free-look period, transparent bonus policies).

**key_takeaway**

SBI Life’s FY2025-26 strategy is **anchored in trust, digital-first execution, and stakeholder-centric governance**, positioning it to capitalize on India’s **growing demand for protection and retirement solutions** while navigating regulatory and macroeconomic challenges.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.04 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 87.5087 s |
| Input / output tokens | 13559 / 759 |
| Tokens/sec (output) | 8.7 |

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

### Case 18 — `AR_ETERNAL_AR_30059_ETERNAL_2025_2026_A_48211721_29072026204435`

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

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact '33%'
- pass 2: financial figure stated as fact '33%'
- pass 3: financial figure stated as fact '33%'

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
| Latency | 126.657 s |
| Input / output tokens | 39249 / 1600 |
| Tokens/sec (output) | 12.6 |

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

### Case 19 — `AR_JIOFIN_AR_30141_JIOFIN_2025_2026_A_8079244_03082026130114`

#### SOURCE / EVIDENCE

- **Symbol:** JIOFIN
- **Company:** Jio Financial Services Limited
- **Fiscal year:** FY2025-26
- **Filing id:** AR_30141_JIOFIN_2025_2026_A_8079244_03082026130114
- **Doc type:** annual_report

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
[Evidence chunk 36, page ~11]
 exchange of securities certificate; endorsement; sub-division / splitting of securities certificate; consolidation of securities 
certificates / folios; transmission and transposition. Accordingly, members are requested to make service requests for issue 
of duplicate securities certificate; claim from unclaimed suspense account; renewal / exchange of securities certificate etc., by 
submitting a duly filled and signed Form ISR-4 (Request for issue of Duplicate Certificate and other Service Requests)along with 
requisite supporting documents to KFinTech as per the requirement of the aforesaid circular.
 
The aforesaid forms can be downloaded from the Company’s website at https://www.jfs.in/forms/ and are also available on 
the website of KFinTech at https://ris.kfintech.com/clientservices/isc/#div_rights. For additional information, the members 
may refer the shareholders’ referencer uploaded on the Company’s website at https://www.jfs.in/forms / 
All aforesaid documents / requests should be submitted to KFinTech, at the address mentioned under Note No. 13.E. above.
24.	
Shareholders’ Referencer gives guidance on securities related matters and is uploaded on the Company’s website and can be 
accessed at link: https://www.jfs.in/forms / 
JIO FINANCIAL SERVICES LIMITED l ANNUAL REPORT F Y 2025-26

STATEMENT PURSUANT TO SECTION 102(1) OF THE COMPANIES ACT, 2013 AND 
ADDITIONAL INFORMATION AS REQUIRED UNDER THE SECURITIES AND EXCHANGE 
BOARD OF INDI

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `legacy_front_slice_pre_evidence_finder` · model `gpt-4o-mini` · prompt `annual_report_summarizer@2026-08-16`
- **Recorded limitations:**
  - The stored reference PREDATES the Evidence Finder layer (reference 2026-08-16, Evidence Finder 2026-08-24).
  - Replaying as 'annual_report_summary_legacy' is like-for-like. Replaying as 'annual_report_summary' changes BOTH the input and the output schema, and is NOT a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**summary**

The annual report for Jio Financial Services Limited for FY2024-25 outlines the company's strategic focus on digital-first financial services aimed at enhancing customer accessibility and experience. Management emphasized the importance of leveraging technology and data analytics to deliver personalized financial solutions, while also highlighting the establishment of a joint venture with BlackRock to democratize investment access in India. The report also noted significant growth in customer engagement and product offerings, reinforcing the company's commitment to sustainable growth and stakeholder value.

**bullets**

- Focus on digital-first financial services
- Joint venture with BlackRock for investment solutions
- Emphasis on technology and data analytics
- Significant growth in customer engagement
- Commitment to sustainable growth and stakeholder value

**key_takeaway**

Management highlighted the company's strategic commitment to leveraging technology for enhancing financial accessibility and customer experience.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact '250%'
- pass 2: forward-tense word 'targeted'
- pass 3: financial figure stated as fact '83%'

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
| Latency | 125.2421 s |
| Input / output tokens | 36629 / 1739 |
| Tokens/sec (output) | 13.9 |

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

### Case 20 — `AR_BEL_AR_30214_BEL_2025_2026_A_16199415_05082026205636`

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

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**executive_summary**

Bharat Electronics Limited (BEL) reported a year of strategic execution in FY2025-26, emphasizing **defense electronics leadership**, **sustainability initiatives**, and **expansion of manufacturing and export capabilities**. Management highlighted continued investment in R&D, digital transformation, and ESG practices, while reinforcing its role in India’s defense self-reliance and global market positioning. The report also underscored governance compliance, stakeholder engagement, and operational excellence across its domestic and international operations.

**key_points**

- Management stated a **focus on defense electronics dominance**, with defense contributing the majority of revenue, while expanding non-defense and export segments (e.g., civil aviation, global defense markets).
- The company emphasized **strategic R&D investments**, including AI policy guidelines, indigenization efforts, and partnerships with defense labs and academic institutions to strengthen technological self-reliance.
- BEL outlined **sustainability commitments**, including a roadmap to achieve **net-zero Scope 1 & 2 emissions by 2030**, water conservation, e-waste management, and compliance with RoHS standards.
- Operational priorities included **digital transformation** (e.g., Industry 4.0, API-based tender automation) and **supply chain optimization**, such as digitizing LTAs and enhancing MSME procurement processes.
- The report highlighted **governance and ESG leadership**, including awards for cybersecurity, quality management, and sustainability, alongside compliance with corporate governance and SEBI regulations.

**important_risks**

- Management noted **geopolitical and global economic uncertainties** as potential headwinds, particularly for export-driven growth.
- The company acknowledged **dependency on defense budgets and government policies** as a key risk factor for order inflows and revenue stability.
- BEL identified **talent retention and skill development** as critical challenges, given the need for continuous upskilling in emerging technologies like AI and cybersecurity.

**key_takeaway**

BEL’s FY2025-26 strategy centered on **defense electronics leadership, technological indigenization, and sustainable growth**, while navigating global and domestic market dynamics through governance and innovation-driven execution.

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact '88%'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 2 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0581 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 108.3486 s |
| Input / output tokens | 27512 / 1124 |
| Tokens/sec (output) | 10.4 |

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
