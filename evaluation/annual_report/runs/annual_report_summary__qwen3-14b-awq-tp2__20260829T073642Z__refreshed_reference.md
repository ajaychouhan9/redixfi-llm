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
| Fixture | `/kaggle/input/datasets/ajaychouhan9/redixfi-llm-fixtures/annual_report_benchmark.json` |
| Cases | 20 of 20 |
| Run id | `20260829T073642Z` (2026-08-29T07:36:42.054951+00:00) |
| LLM project commit | `unknown` |
| GPU | 2x Tesla T4 (29.12 GB total) |
| CUDA / torch / vLLM | 13.0 / 2.13.0+cu130 / None |

## Objective signals (mechanical only — no judgement)

| Metric | Value |
|---|---|
| cases | 20 |
| generated_ok | 17 |
| generation_failures | 3 |
| candidate_compliance_failures | 3 |
| reference_backstop_artifacts | 0 |
| reference_compliance_failures | 0 |
| cases_with_reference | 20 |
| structured_output_used | 20 |
| json_repair_used | 0 |
| guided_and_clean | 20 |
| guided_but_repaired | 0 |
| unguided | 0 |
| mean_latency_sec | 77.88 |
| total_prompt_tokens | 443916 |
| total_completion_tokens | 10590 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| mean_lexical_overlap | 0.2512 |

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

The annual report for Vedanta Limited for FY 2024-25 highlighted the company's strategic focus on operational efficiency, sustainability, and market positioning amidst a challenging global economic landscape. Management emphasized the importance of adapting to geopolitical tensions and climate change impacts while pursuing growth through disciplined capital allocation and innovation in production processes. The report also noted the company's commitment to enhancing its value-added product offerings and maintaining a strong financial position.

**bullets**

- Management emphasized the need for operational stability and cost efficiency in response to global market volatility.
- The report highlighted ongoing investments in sustainability initiatives and technology to enhance supply chain resilience.
- Management stated a plan to increase the share of value-added products in their portfolio to meet evolving customer needs.
- The company focused on maintaining a robust balance sheet while pursuing growth opportunities in key sectors.
- Management outlined strategic priorities including exploration and resource upgrading to sustain long-term production.

**key_takeaway**

Management underscored the importance of sustainability and operational excellence as core components of Vedanta's growth strategy.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact '19%'
- pass 2: financial figure stated as fact '19%'
- pass 3: financial figure stated as fact '19%'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ❌ no — failed validation after 3 attempts |
| Attempts used | 3 |
| Compliance — **Qwen** | ❌ FAIL — executive_summary: empty text |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.0 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 118.9491 s |
| Input / output tokens | 44133 / 839 |
| Tokens/sec (output) | 7.1 |

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

The annual report for FY 2024-25 from Britannia Industries Limited outlines the company's commitment to resilience, innovation, and sustainability amidst economic challenges. Management emphasized the importance of maintaining market leadership through strategic distribution expansion, brand investments, and cost efficiency initiatives. The report also highlights the company's focus on community impact and employee well-being as integral to its operational strategy.

**bullets**

- Management stated a commitment to sustainability through energy conservation and reduced carbon footprint.
- The report highlighted a focus on consumer-centric innovation and premiumization in product offerings.
- Management emphasized the importance of community engagement and social responsibility initiatives.
- The company outlined its strategy for supply chain optimization and technology-driven solutions.
- Management noted the significance of employee well-being and development programs.

**key_takeaway**

Management underscored the importance of resilience and innovation as foundational to Britannia's strategy for sustainable growth.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**executive_summary**

Britannia Industries Limited's FY2024-25 annual report highlights strategic focus on sustainability, innovation, and strengthening distribution networks. The company emphasizes reducing its carbon footprint through energy-efficient practices and renewable energy adoption. It also outlines initiatives to enhance brand value through consumer-centric innovation and premiumization in bakery products. Corporate governance and ethical practices are prioritized, with a commitment to community development and employee well-being.

**key_points**

- Commitment to sustainability through energy conservation and renewable energy adoption.
- Focus on consumer-centric innovation and premiumization in bakery products.
- Strengthening distribution networks and expanding market reach.
- Corporate governance with emphasis on transparency and ethical practices.
- Initiatives for community development and employee well-being.

**important_risks**

- Rising input costs for key commodities like wheat and edible oil.
- Global trade disruptions and geopolitical tensions affecting international operations.
- Increased competition from local and global players in both organized and unorganized segments.

**key_takeaway**

Britannia Industries Limited is prioritizing sustainability, innovation, and robust distribution strategies to maintain market leadership and drive long-term value creation.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.3433 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 59.5218 s |
| Input / output tokens | 11839 / 238 |
| Tokens/sec (output) | 4.0 |

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

Dixon Technologies (India) Limited's annual report for FY 2024-25 highlighted the company's commitment to engineering excellence and sustainable growth. Management emphasized the importance of integrating ESG principles into operations and expanding its product offerings, particularly in digital signage and advanced manufacturing capabilities. The report also detailed the company's focus on corporate governance and community welfare initiatives, reinforcing its dedication to long-term value creation for stakeholders.

**bullets**

- Management stated a commitment to engineering excellence as a cornerstone of sustainable success.
- The report described ongoing investments in advanced manufacturing capabilities and new product categories.
- Management emphasized the integration of ESG principles into daily operations to ensure sustainable value.
- The company highlighted its focus on corporate governance and community welfare initiatives.
- Dixon is expanding its global footprint through exports and exploring new markets.

**key_takeaway**

The most important qualitative point in the document is Dixon's commitment to integrating sustainability and engineering excellence into its growth strategy.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**executive_summary**

Dixon Technologies (India) Limited's FY2024-25 annual report highlights strategic initiatives focused on expanding its electronics manufacturing services (EMS) footprint, both domestically and internationally. The company emphasized investments in advanced manufacturing capabilities, including robotic panel assembly lines, and entry into new product categories like industrial, institutional, and automotive displays. Sustainability and ESG principles were integrated into operations, with initiatives aimed at reducing energy consumption and operational emissions. The report also detailed corporate governance practices, including board structure, committee functions, and internal control systems, alongside efforts in employee engagement and CSR activities.

**key_points**

- Expansion of EMS capabilities through advanced manufacturing technologies and entry into new product segments.
- Commitment to sustainability with energy efficiency measures and ESG integration.
- Strengthened corporate governance with structured board committees and internal controls.

**important_risks**

_(none)_

**key_takeaway**

Dixon Technologies is prioritizing growth in electronics manufacturing through technological advancement and sustainability, supported by robust governance frameworks.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.246 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 59.686 s |
| Input / output tokens | 12013 / 210 |
| Tokens/sec (output) | 3.5 |

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

The report highlighted Larsen & Toubro's commitment to fostering an inclusive work environment, particularly through initiatives aimed at enhancing gender diversity within the workforce. Management emphasized the importance of resilience in navigating market volatility and expressed gratitude to stakeholders for their support. The company outlined its strategic focus on achieving its long-term goals while maintaining a strong emphasis on corporate governance and sustainability.

**bullets**

- Management stated a commitment to gender diversity, with initiatives supporting women's career advancement.
- The company emphasized resilience in facing market volatility, guided by a proactive approach.
- Management highlighted the importance of corporate governance and internal controls in achieving sustainable growth.
- The report detailed strategic restructuring efforts to streamline operations and enhance digital capabilities.
- Management expressed appreciation for stakeholder support in pursuing excellence and innovation.

**key_takeaway**

Management underscored the importance of stakeholder trust and corporate governance in driving the company's growth and sustainability initiatives.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**executive_summary**

The report highlights Larsen & Toubro Limited's (LT) focus on fostering an inclusive work environment, particularly through initiatives aimed at increasing women's participation in the workforce. It also emphasizes the company's resilience in navigating global uncertainties and its commitment to sustainable growth. LT acknowledges ongoing challenges such as competition, pricing pressures, and global economic volatility, while maintaining a strong internal control framework and corporate governance structure.

**key_points**

- Commitment to creating an inclusive work environment with initiatives to increase women's participation in the workforce
- Resilience in navigating global uncertainties and maintaining strong stakeholder relationships
- Focus on sustainable growth and strategic restructuring to streamline operations and enhance digital commerce initiatives
- Robust internal control framework and corporate governance practices to ensure compliance and risk management

**important_risks**

- Competition from domestic and international firms impacting margins and project securing capabilities
- Global economic volatility and structural shifts in trade architecture affecting business stability
- Financial risks related to managing exposures and potential impacts from commodity price fluctuations

**key_takeaway**

Larsen & Toubro Limited is committed to fostering an inclusive work environment and maintaining resilience in the face of global uncertainties, supported by strong corporate governance and strategic initiatives to drive sustainable growth.

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact '10%'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 2 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.3556 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 74.0726 s |
| Input / output tokens | 23002 / 581 |
| Tokens/sec (output) | 7.8 |

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

Adani Power Limited's Integrated Annual Report for FY 2025-26 outlines the company's strategic focus on capacity expansion, sustainability, and operational excellence. Management emphasized a commitment to enhancing energy efficiency and reducing greenhouse gas emissions while maintaining high operational reliability. The report also highlights the company's dedication to community engagement and corporate social responsibility initiatives, reflecting its broader vision of sustainable growth.

**bullets**

- Management stated a plan to expand capacity significantly to meet India's energy needs.
- The report described a commitment to contributing towards a low carbon economy through renewable energy adoption.
- Management highlighted leveraging digital technology to enhance operational efficiency and sustainability.
- The company emphasized its focus on community engagement and social responsibility initiatives.
- Governance and diversity remain key priorities in the company's operational strategy.

**key_takeaway**

The report underscores Adani Power's strategic commitment to sustainable growth through capacity expansion and operational excellence.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**executive_summary**

Adani Power Limited's FY2025-26 Integrated Annual Report outlines strategic priorities centered on infrastructure expansion, digital transformation, and sustainability. The company emphasizes capacity growth through large-scale projects, operational efficiency improvements, and integration of renewable energy sources like biomass co-firing. The report highlights a commitment to ESG principles, including community engagement, employee development, and environmental stewardship. Governance structures and risk management frameworks are also detailed, with a focus on compliance and stakeholder transparency.

**key_points**

- Strategic focus on infrastructure expansion and digital transformation to meet India's energy demands
- Commitment to sustainability through renewable energy integration and environmental initiatives
- Emphasis on operational efficiency, including energy conservation and emission reduction technologies
- Strengthening corporate governance, risk management, and stakeholder engagement practices

**important_risks**

- Regulatory and commodity price risks impacting operations
- Reputation risks associated with large-scale projects and environmental performance
- Operational challenges in executing complex capacity expansion programs

**key_takeaway**

Adani Power Limited is prioritizing infrastructure growth, digital innovation, and sustainability, supported by robust governance and risk management frameworks to ensure long-term value creation and stakeholder trust.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.2932 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 64.9976 s |
| Input / output tokens | 12414 / 252 |
| Tokens/sec (output) | 3.9 |

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

The report highlighted Infosys' commitment to enhancing client relationships through strong account management and technology advisory services, particularly in AI and automation. It emphasized the company's focus on digital skilling initiatives, reaching millions through its learning platform, and its social impact through the Infosys Foundation. Additionally, the report outlined the company's capital allocation policy aimed at returning a significant portion of free cash flow to shareholders through dividends and buybacks.

**bullets**

- Management emphasized the importance of long-term client relationships and proactive technology advisory services.
- The report described extensive digital skilling initiatives aimed at empowering diverse communities.
- Infosys Foundation's programs focus on education, healthcare, and environmental sustainability.
- Management set a goal of returning a substantial portion of free cash flow to shareholders through dividends and buybacks.
- The company maintains a strong commitment to corporate governance and employee welfare.

**key_takeaway**

The report underscored Infosys' strategic focus on client relationships, digital empowerment, and sustainable social impact.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**executive_summary**

The report outlines Infosys' strategic focus on client-centric AI advisory, digital skilling initiatives, and robust corporate governance. It highlights the company's commitment to ESG goals, including employment creation and environmental sustainability. The document also details Infosys' capital allocation policy, emphasizing returns to shareholders through dividends and buybacks, alongside strong internal controls and risk management frameworks.

**key_points**

- Infosys emphasizes client-centric AI advisory and digital transformation as key growth drivers.
- The company has invested in large-scale digital skilling through its Springboard platform and foundation initiatives.
- Infosys has a capital allocation policy focused on returning a significant portion of free cash flow to shareholders via dividends and buybacks.

**important_risks**

- Economic uncertainties and geopolitical factors could impact operations and financial performance.
- Technological disruptions and regulatory changes, particularly in the U.S., pose potential challenges.
- Cybersecurity risks and pending legal matters may affect business continuity and reputation.

**key_takeaway**

Infosys is prioritizing AI-driven client solutions, ESG initiatives, and shareholder returns through its capital allocation policy, while maintaining strong governance and risk management practices.

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact '85%'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 2 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.2576 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 81.4988 s |
| Input / output tokens | 24778 / 572 |
| Tokens/sec (output) | 7.0 |

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

The annual report of Hindustan Zinc Limited for FY2025-26 outlines the company's commitment to sustainability and integrated reporting, emphasizing the importance of materiality in shaping business strategies. Management highlighted their focus on expanding capacities and diversifying into critical minerals to align with India's growth trajectory. The report also underscores the company's robust governance framework and proactive risk management strategies to navigate uncertainties in the market.

**bullets**

- Management emphasized a commitment to sustainability and responsible business practices.
- The company aims to expand its portfolio into critical minerals to support energy transition.
- Hindustan Zinc is focused on maintaining operational excellence and cost leadership.
- The report highlights a disciplined approach to capital allocation and risk management.
- Management stated a goal of enhancing community engagement and social responsibility.

**key_takeaway**

Hindustan Zinc is positioned to leverage India's growth in critical minerals while maintaining a strong focus on sustainability and risk management.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**executive_summary**

Hindustan Zinc Limited's FY2026 Integrated Annual Report outlines the company's strategic focus on expanding its multi-metal portfolio, enhancing operational efficiency, and strengthening sustainability practices. The report highlights the company's commitment to responsible sourcing, ESG alignment, and risk management frameworks. Management emphasized the importance of navigating global and domestic market dynamics while prioritizing long-term value creation through disciplined capital allocation and innovation in critical minerals.

**key_points**

- Strategic expansion into critical minerals and multi-metal production to align with India's resource security goals.
- Commitment to ESG practices, including responsible sourcing and sustainability initiatives, with a focus on reducing environmental impact.
- Robust risk management frameworks aligned with global standards such as ISO 31000 and ICMM principles to ensure operational resilience.
- Emphasis on technological innovation and automation to enhance safety, efficiency, and long-term growth.

**important_risks**

- Potential disruptions from geopolitical tensions and supply chain uncertainties affecting raw material procurement and market access.
- Commodity price volatility, particularly in zinc and silver, which could impact profitability and project execution.
- Operational risks related to safety, structural integrity, and environmental compliance, requiring continuous monitoring and mitigation strategies.

**key_takeaway**

Hindustan Zinc is positioning itself as a leader in critical minerals and multi-metal production, leveraging India's growth trajectory and global demand for transition metals, while prioritizing disciplined risk management and sustainability.

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact '100%'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 2 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.2651 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 82.1048 s |
| Input / output tokens | 23853 / 664 |
| Tokens/sec (output) | 8.1 |

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

The Integrated Annual Report for FY 2025-26 from Asian Paints Limited highlights the company's commitment to innovation, sustainability, and market leadership amidst a challenging economic landscape. Management emphasized the importance of regionalization strategies and consumer-centric services to enhance market share and brand relevance. The report also outlines the company's focus on backward integration and operational excellence to drive growth and efficiency.

**bullets**

- Management highlighted a strategic focus on premium and luxury product portfolios to enhance brand positioning.
- The report detailed efforts in regionalization to tailor products and marketing strategies to diverse consumer needs.
- Management underscored the importance of sustainability initiatives and responsible operations in their business model.
- The company is investing in backward integration to improve product differentiation and cost efficiency.
- Asian Paints is expanding its B2B and industrial ecosystems to capitalize on infrastructure growth opportunities.

**key_takeaway**

Management emphasized a commitment to innovation and sustainability as core to Asian Paints' strategy for long-term growth.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**executive_summary**

Asian Paints Limited's FY2025-26 Integrated Annual Report highlights strategic focus on premium and luxury product portfolios, regionalisation efforts, and expansion of B2B and industrial segments. The report notes continued investment in manufacturing capacity, including the commissioning of a white cement plant in the UAE and progress on a VAM-VAE plant in Gujarat. The company emphasizes sustainability initiatives, innovation in product development, and strengthening stakeholder engagement through enhanced digital and service offerings. Governance and risk management frameworks are described as robust, with emphasis on compliance, transparency, and enterprise-wide risk oversight.

**key_points**

- Strategic emphasis on premium and luxury product portfolios to drive healthier realisations and brand elevation
- Expansion of B2B and industrial segments driven by infrastructure and manufacturing growth
- Investments in backward integration, including a white cement plant in the UAE and VAM-VAE plant in Gujarat
- Regionalisation strategies tailored to local market demands and cultural identities
- Enhanced digital and service offerings, including AI-enabled tools for customer engagement and service delivery

**important_risks**

- Climate-related physical and transition risks impacting operations
- Non-compliance with evolving regulatory requirements leading to penalties
- Counterfeit products threatening revenue and brand reliability
- Fluctuations in currency and raw material costs affecting profitability
- Operational risks from supply chain disruptions and project execution variability

**key_takeaway**

Asian Paints Limited is prioritizing premium product innovation, regional market customization, and backward integration to strengthen its market position while maintaining a robust risk management framework to address climate, regulatory, and operational challenges.

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'recommendations'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 2 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.2253 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 82.4217 s |
| Input / output tokens | 24360 / 627 |
| Tokens/sec (output) | 7.6 |

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

The annual report for Tech Mahindra Limited for FY2025-26 outlines the company's strategic focus on digital transformation and sustainability initiatives. Management emphasized the importance of aligning operations with global net-zero goals and enhancing customer engagement through innovative solutions. The report also highlights the company's commitment to ethical governance and proactive risk management in a challenging macroeconomic environment.

**bullets**

- Management stated a plan to achieve net-zero emissions by FY35 through operational changes and investments in renewable energy.
- The report described ongoing efforts to enhance customer experience and retention through innovative, client-centric solutions.
- Management highlighted a strong focus on ethical governance, including a comprehensive Code of Conduct and a Whistleblower Policy.
- The report noted the importance of talent retention strategies and employee development programs to build a resilient workforce.
- Management emphasized the need for proactive risk management to navigate macroeconomic uncertainties.

**key_takeaway**

Management underscored a commitment to sustainability and ethical governance as central to Tech Mahindra's strategic direction.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**executive_summary**

The report outlines Tech Mahindra Limited's strategic focus on sustainability, including commitments to reduce greenhouse gas emissions and enhance water efficiency across its global operations. It highlights the company's efforts in digital transformation, employee development, and ethical governance, while acknowledging macroeconomic challenges and risks related to geopolitical factors and market uncertainties. The document emphasizes a structured approach to risk management and corporate responsibility, aligning with global standards and sustainability goals.

**key_points**

- Commitment to reducing greenhouse gas emissions through structured transition plans aligned with global net zero goals
- Focus on water efficiency and recycling initiatives across all locations
- Emphasis on employee development and retention through tailored programs and competitive compensation
- Integration of ethical governance and compliance frameworks with global standards
- Strategic expansion of Global Capability Centres towards higher-value roles in global enterprise ecosystems

**important_risks**

- Macroeconomic uncertainties including inflation and interest rates affecting consumer sentiment and business confidence
- Potential revenue impacts from subdued demand and price pressures
- Cybersecurity and operational risks impacting business continuity and reputation
- Geopolitical and socio-economic factors influencing customer technology spending and demand for services

**key_takeaway**

Tech Mahindra Limited is prioritizing sustainability and ethical governance while navigating macroeconomic challenges through strategic risk management and operational efficiency.

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'targets'
- pass 2: financial figure stated as fact '58.8%'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 3 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.3063 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 106.9705 s |
| Input / output tokens | 36935 / 1082 |
| Tokens/sec (output) | 10.1 |

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

The annual report of CG Power and Industrial Solutions Limited for FY2025-26 highlights the company's commitment to innovation, sustainability, and operational excellence. Management emphasized the importance of their CG EDGE framework, which underpins their operational strategies and fosters a culture of continuous improvement. The report also outlines the company's strategic focus on expanding its global presence and enhancing its technological capabilities to meet evolving market demands.

**bullets**

- Management emphasized a commitment to sustainability and social responsibility in operations.
- CG EDGE framework drives operational excellence and agility across the organization.
- The company aims to strengthen its position in power systems, industrial solutions, and emerging technologies.
- Focus on expanding global presence and enhancing technological capabilities.
- Management highlighted the importance of collaboration and partnerships for growth.

**key_takeaway**

Management underscored the importance of innovation and sustainability as core to CG's strategic direction.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**executive_summary**

CG Power and Industrial Solutions Limited emphasizes its commitment to innovation, sustainability, and operational excellence through its CG EDGE framework. The report highlights the company's focus on expanding its global presence, investing in technology and manufacturing capabilities, and aligning with India's growth in infrastructure and renewable energy. It also outlines the company's dedication to responsible business practices, including environmental and social governance initiatives, and mentions the challenges posed by global economic uncertainties and geopolitical tensions.

**key_points**

- Commitment to innovation and operational excellence through the CG EDGE framework.
- Focus on expanding global presence and investing in technology and manufacturing capabilities.
- Alignment with India's infrastructure and renewable energy growth.
- Dedication to responsible business practices and environmental sustainability initiatives.

**important_risks**

- Global economic uncertainties and geopolitical tensions.
- Commodity market volatility and supply chain disruptions.
- Intensifying competition across segments.

**key_takeaway**

CG Power and Industrial Solutions Limited is focused on innovation, sustainability, and operational excellence, positioning itself to capitalize on India's growth in infrastructure and renewable energy despite global challenges.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.3107 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 55.2867 s |
| Input / output tokens | 11346 / 225 |
| Tokens/sec (output) | 4.1 |

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

The Integrated Annual Report for FY2025-26 from Mahindra & Mahindra Limited outlines the company's commitment to integrated reporting, emphasizing sustainable value creation through the management of various capitals. The report highlights the company's strategic focus on innovation, technology, and governance, while also addressing the complexities of the external environment, including geopolitical and economic factors. Management detailed their proactive risk management approach and commitment to enhancing manufacturing capabilities and product offerings across sectors.

**bullets**

- Management emphasized the importance of integrated reporting for transparency and stakeholder value.
- The company is focused on innovation and technology-led growth, particularly in the automotive and farm equipment sectors.
- Management outlined a proactive risk management strategy to navigate external uncertainties.
- Sustainability initiatives are central to the company's operations, including advancements in electrification and clean mobility.
- The report highlights a commitment to strong corporate governance and ethical business practices.

**key_takeaway**

Management underscored their commitment to sustainable value creation through integrated reporting and strategic risk management.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**executive_summary**

Mahindra & Mahindra Limited's FY2025-26 Integrated Annual Report highlights the company's strategic focus on integrated reporting, emphasizing value creation through financial and non-financial capital management. The report outlines a commitment to sustainability, innovation, and robust risk governance, with a strong emphasis on technology-driven growth and market leadership in automotive and farm equipment sectors. The company also details its global expansion strategies, product innovation, and initiatives to enhance operational efficiency and customer engagement.

**key_points**

- Commitment to integrated reporting and value creation through strategic management of financial and non-financial capital.
- Focus on technology-driven innovation, including electric vehicles and AI capabilities, to maintain competitive advantage.
- Robust risk management framework with proactive governance and capital allocation strategies to navigate uncertainties.

**important_risks**

- Global geopolitical conflicts and supply chain disruptions may impact operations and growth prospects.
- Fluctuations in inflation, energy prices, and currency movements could affect cost structures and consumer affordability.
- Regulatory and compliance risks, including potential non-compliance with evolving standards and policies.

**key_takeaway**

Mahindra & Mahindra Limited is prioritizing integrated value creation through strategic technology adoption, robust risk governance, and market leadership in key sectors like automotive and farm equipment.

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact 'rs,'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 2 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.3806 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 78.204 s |
| Input / output tokens | 24225 / 559 |
| Tokens/sec (output) | 7.1 |

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

The annual report for Cholamandalam Investment and Finance Company Limited for FY 2025-26 highlighted the company's commitment to sustainable growth driven by its core values of integrity, passion, quality, respect, and responsibility. Management emphasized a focus on financial inclusion, particularly for underserved markets, and the importance of technology in enhancing operational efficiency and customer engagement. The report also outlined the company's strategic priorities, including maintaining asset quality and strengthening customer relationships.

**bullets**

- Management emphasized a commitment to financial inclusion and responsible lending practices.
- The report highlighted investments in technology to enhance credit delivery and operational efficiency.
- Management stated a focus on sustainable growth and maintaining strong governance practices.
- The company aims to deepen its presence in urban and rural markets while serving diverse customer segments.
- CSR initiatives reflect a commitment to community development and socio-economic advancement.

**key_takeaway**

Management underscored the importance of aligning business growth with societal impact through responsible financial solutions.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

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
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.0 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 95.458 s |
| Input / output tokens | 37879 / 800 |
| Tokens/sec (output) | 8.4 |

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

The annual report for Bajaj Finance Limited for FY2025-26 highlighted the company's commitment to financial inclusion and its transformation into a digital-first financial services provider. Management emphasized the integration of AI across operations to enhance customer engagement and operational efficiency, while also maintaining a strong focus on risk management and governance. The report outlined the company's strategic initiatives aimed at expanding its customer base and product offerings, particularly in underserved segments.

**bullets**

- Management emphasized a digital-first approach to drive financial inclusion.
- The company is integrating AI across all operational workflows to enhance efficiency.
- Bajaj Finance maintains a strong risk management framework to mitigate potential risks.
- The report highlighted a commitment to sustainability and responsible financial solutions.
- Management outlined strategic partnerships to expand product offerings and customer reach.

**key_takeaway**

Bajaj Finance Limited is focused on leveraging technology and AI to enhance customer experience while maintaining a robust risk management framework.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact '22%'
- pass 2: financial figure stated as fact '22%'
- pass 3: financial figure stated as fact 'rs,'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ❌ no — failed validation after 3 attempts |
| Attempts used | 3 |
| Compliance — **Qwen** | ❌ FAIL — executive_summary: empty text |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.0 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 109.4954 s |
| Input / output tokens | 36762 / 1143 |
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

The annual report for Mankind Pharma Limited for FY2025-26 outlines the company's commitment to improving lives through accessible and affordable healthcare. Management emphasized a strategic focus on expanding its specialty chronic portfolio and enhancing its presence in high-potential therapeutic areas through acquisitions and partnerships. The report also highlighted the company's dedication to sustainability and corporate governance, aiming to build a future-ready organization.

**bullets**

- Management stated a commitment to improving healthcare accessibility and affordability.
- The company focused on expanding its specialty chronic portfolio through acquisitions and partnerships.
- Management emphasized the importance of sustainability and corporate governance in their operations.
- The report highlighted ongoing investments in research and development to drive innovation.
- Mankind Pharma aims to consolidate market share in key therapeutic areas while exploring whitespace opportunities.

**key_takeaway**

Mankind Pharma is focused on enhancing its specialty chronic portfolio and sustainability efforts to drive long-term growth.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**executive_summary**

Mankind Pharma Limited, a top Indian pharmaceutical company, emphasizes its commitment to accessible, affordable, and innovation-led healthcare. The report highlights strategic focus on expanding its chronic and specialty therapy portfolio, including acquisitions like Rivotril and Bharat Serums and Vaccines (BSV), to strengthen its presence in high-growth areas such as women's health and critical care. The company also outlines plans to leverage digital platforms and AI/ML technologies for business transformation and productivity improvements, while maintaining a balanced portfolio and multiple growth engines across its base business, specialty chronic, BSV, and OTC segments for long-term sustainable growth.

**key_points**

- Expansion of chronic and specialty therapy portfolio through acquisitions and in-licensing partnerships with global innovators.
- Strategic focus on digital transformation and AI/ML technologies to enhance productivity and business processes.
- Strengthening presence in high-growth areas like women's health, fertility, and critical care through acquisitions such as BSV.
- Commitment to long-term sustainable growth with a balanced portfolio and multiple growth engines across business segments.

**important_risks**

- Potential impact of geopolitical tensions and trade uncertainties on supply chains and business operations.
- Challenges in managing growth and maintaining market share in competitive therapy areas.
- Risks associated with regulatory approvals and compliance with evolving healthcare policies.

**key_takeaway**

Mankind Pharma is strategically expanding its chronic and specialty therapy portfolio through acquisitions and partnerships, while focusing on digital transformation and long-term sustainable growth across multiple business segments.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.2424 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 68.029 s |
| Input / output tokens | 12396 / 315 |
| Tokens/sec (output) | 4.6 |

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

The annual report for Siemens Limited highlighted the company's advancements in technology and infrastructure, particularly in the Mobility sector, where significant contracts were secured for electric locomotives and high-speed rail projects. Management emphasized the importance of sustainability and digitalization in driving future growth, while also acknowledging the challenges posed by inflation and global uncertainties. The report outlined the company's commitment to corporate governance and risk management, ensuring alignment with India's development priorities.

**bullets**

- Strengthened position in Mobility with major contracts for electric locomotives and high-speed rail projects.
- Focus on sustainability and digitalization as key drivers for future growth.
- Commitment to corporate governance and risk management practices.
- Investment in energy conservation and renewable energy initiatives.
- Emphasis on local manufacturing and technology leadership in India.

**key_takeaway**

Siemens Limited is focused on leveraging technology and sustainability to enhance its market position while navigating economic challenges.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**executive_summary**

Siemens Limited highlighted its strategic focus on electrification, automation, and digitalization across key sectors like railways, urban mobility, and industrial infrastructure in FY2024-26. The company secured major contracts, including India's first high-speed rail project and the production of 1,200 electric locomotives, emphasizing Made in India technologies. The Chairman noted strong market opportunities driven by structural trends like sustainability and digitalization, while cautioning about inflation, commodity volatility, and global uncertainties. The company also emphasized corporate governance, diversity initiatives, and sustainability efforts, including energy conservation and renewable energy adoption.

**key_points**

- Strengthened position in India's rail infrastructure through landmark projects like the Mumbai–Ahmedabad high-speed rail and D9 electric locomotives.
- Focused on electrification, automation, and digitalization across power utilities, railways, urban mobility, and industrial sectors.
- Emphasized sustainability, energy efficiency, and renewable energy adoption, including rooftop solar expansion and CO2 emission reductions.
- Enhanced corporate governance with structured board committees, diversity initiatives, and compliance with regulatory standards.
- Secured significant contracts in mobility solutions, including signaling technologies for metro projects and rail infrastructure.

**important_risks**

- Potential impact of inflationary pressures, commodity volatility, and foreign exchange movements on costs and investment sentiment.
- Global uncertainties and geopolitical risks, including conflicts in West Asia, affecting growth and supply chains.
- Dependence on imported energy and associated risks from crude oil price volatility.

**key_takeaway**

Siemens Limited is capitalizing on India's structural trends in sustainability and digitalization through strategic projects in rail infrastructure and industrial automation, while managing risks related to global uncertainties and energy costs.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.2938 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 71.8008 s |
| Input / output tokens | 12570 / 360 |
| Tokens/sec (output) | 5.0 |

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

The annual report for Cummins India Limited for FY 2025-26 provides insights into the company's governance, strategic initiatives, and operational updates. Management highlighted a focus on sustainability, innovation in product offerings, and a commitment to enhancing corporate governance practices. The report also detailed the company's risk management framework and its approach to human resources development.

**bullets**

- Management emphasized a commitment to sustainability and decarbonization efforts.
- The company is focused on enhancing product offerings in response to market demands, particularly in high horsepower and cleaner technology.
- Management outlined a robust Enterprise Risk Management framework to identify and mitigate risks.
- The report highlighted ongoing investments in employee development and leadership training.
- Governance practices were reinforced with a focus on compliance and ethical conduct.

**key_takeaway**

Management underscored a strong commitment to sustainability and innovation as central to the company's strategic direction.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**executive_summary**

The report outlines Cummins India Limited's FY2025-26 performance, highlighting a focus on corporate governance, risk management, and sustainability initiatives. It details the company's robust enterprise risk management framework, ongoing efforts in environmental sustainability, and strategic investments in localization and innovation. The report also emphasizes the company's commitment to ethical practices, stakeholder engagement, and adherence to regulatory requirements.

**key_points**

- Robust enterprise risk management framework with structured governance mechanisms.
- Commitment to sustainability and decarbonization, including renewable energy and emission control solutions.
- Strategic investments in localization and innovation to support India's 'Make in India' and 'Atmanirbhar Bharat' initiatives.
- Enhanced corporate governance practices, including independent directorships and compliance with SEBI regulations.

**important_risks**

- Global trade policy uncertainty and geopolitical tensions affecting external demand.
- Volatility in commodity and energy markets, particularly crude oil prices.
- Regulatory and compliance risks related to evolving environmental and labor standards.

**key_takeaway**

Cummins India Limited emphasizes a comprehensive risk management approach and strategic alignment with sustainability and localization initiatives to navigate market challenges and support long-term growth.

<details><summary>Rejected attempts</summary>

- pass 1: financial figure stated as fact 'rs,'
- pass 2: financial figure stated as fact '17%'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 3 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.2479 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 88.9198 s |
| Input / output tokens | 36077 / 779 |
| Tokens/sec (output) | 8.8 |

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

SBI Life Insurance Company Limited's Integrated Annual Report for FY2025-26 outlines the company's commitment to integrated and transparent reporting, emphasizing long-term value creation. The report highlights the evolution of its reporting philosophy to include a cohesive narrative that integrates strategy, governance, risk, sustainability, and stakeholder engagement. Management stated a focus on aligning strategic priorities with risk management and capital allocation to deliver sustainable value for stakeholders.

**bullets**

- Management emphasized an integrated approach to decision-making.
- The report highlighted a commitment to transparency and responsible business practices.
- SBI Life aims to enhance customer engagement and experience.
- Management outlined strategic priorities including expanding digital footprints and building a skilled workforce.
- The company continues to align its initiatives with the United Nations Sustainable Development Goals.

**key_takeaway**

The report underscores SBI Life's commitment to creating sustainable value through integrated governance and strategic alignment.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**executive_summary**

SBI Life Insurance Company Limited's FY2025-26 Integrated Annual Report emphasizes a strategic focus on integrated reporting, transparency, and long-term value creation. The report highlights the company's commitment to sustainability, ESG initiatives, and stakeholder engagement, aligning with global reporting standards. Key priorities include robust distribution, sustainable growth, customer engagement, team development, and digital expansion. The report also outlines the company's adherence to regulatory frameworks and its proactive approach to risk management and governance.

**key_points**

- Commitment to integrated reporting and transparency aligned with global standards
- Focus on sustainability, ESG initiatives, and stakeholder engagement
- Strategic priorities include robust distribution, sustainable growth, customer engagement, team development, and digital expansion

**important_risks**

_(none)_

**key_takeaway**

SBI Life Insurance Company Limited is committed to integrated reporting, sustainability, and stakeholder engagement, with strategic priorities focused on robust distribution, sustainable growth, and digital expansion.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.3804 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 60.6809 s |
| Input / output tokens | 12160 / 206 |
| Tokens/sec (output) | 3.4 |

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

The annual report for Eternal Limited for FY2025-26 outlines the company's strategic focus on enhancing its operational efficiency and market positioning across its key business segments, including food delivery, quick commerce, and going-out experiences. Management emphasized a commitment to sustainability and social responsibility, alongside a robust governance framework to navigate competitive pressures and operational risks. The report also highlights the company's initiatives in energy conservation and employee engagement through stock option plans and inclusive workplace policies.

**bullets**

- Management stated a focus on transitioning to an inventory ownership model in quick commerce to enhance control over pricing and margins.
- The report highlighted ongoing investments in sustainability initiatives aimed at reducing the company's carbon footprint.
- Management emphasized the importance of stakeholder engagement and responsive communication protocols to mitigate operational risks.
- The company outlined its commitment to corporate governance and compliance, including regular board evaluations and adherence to regulatory standards.
- Eternal Limited aims to foster a culture of inclusivity and support for employees through comprehensive parental leave policies.

**key_takeaway**

Eternal Limited is committed to enhancing operational efficiency and sustainability while navigating competitive challenges in its diverse business segments.

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
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.2679 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 76.8475 s |
| Input / output tokens | 23638 / 580 |
| Tokens/sec (output) | 7.5 |

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

The annual report of Jio Financial Services Limited for FY 2025-26 outlines the company's strategic focus on digital transformation and customer-centric financial solutions. Management emphasized the integration of AI and data intelligence to enhance operational efficiency and customer experience. The report also highlighted the company's commitment to sustainability and local economic growth through various initiatives.

**bullets**

- Management stated a plan to democratize financial services through the JioFinance app.
- The report described a focus on embedding AI across operations to improve customer engagement and risk management.
- Management highlighted a commitment to sustainability through eco-friendly practices and responsible financing.
- The report emphasized the importance of governance and ethical conduct in corporate operations.
- Management outlined a strategy to support local economic growth by investing in MSMEs and community initiatives.

**key_takeaway**

Management underscored the goal of making sophisticated financial guidance accessible to all Indians through innovative technology and personalized services.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**executive_summary**

Jio Financial Services Limited (JFSL) emphasizes its transition from foundational infrastructure to aggressive scaling, leveraging its JioFinance app as a central platform for personalized financial services. The company highlights strategic partnerships with global entities like BlackRock and Allianz, focusing on digital transformation, AI integration, and sustainable practices. Governance and compliance are prioritized, with a strong emphasis on risk management, ethical conduct, and stakeholder engagement.

**key_points**

- Strategic focus on digital transformation and AI-driven personalization to enhance customer experience and operational efficiency.
- Expansion through global joint ventures in asset management, wealth advisory, and insurance underwriting.
- Commitment to sustainability, including initiatives for climate action, waste reduction, and responsible workplace practices.
- Robust governance framework with emphasis on compliance, risk management, and ethical standards.
- Strengthening of corporate social responsibility (CSR) initiatives and community engagement through various programs.

**important_risks**

- Sensitivity to macroeconomic conditions, including interest rate fluctuations and foreign exchange risks.
- Regulatory and compliance challenges, despite no penalties in FY2025-26.
- Potential impact of market manipulation allegations, though resolved in favor of the company.

**key_takeaway**

JFSL is aggressively scaling its digital financial services through AI and strategic partnerships, emphasizing sustainability and robust governance to drive long-term value creation.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.2595 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 57.0225 s |
| Input / output tokens | 11169 / 287 |
| Tokens/sec (output) | 5.0 |

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

The annual report for Bharat Electronics Limited (BEL) for FY 2025-26 outlines the company's strategic focus on enhancing its core defence business while expanding into non-defence and export markets. Management emphasized the importance of research and development, sustainability initiatives, and operational excellence as key drivers of growth. The report also highlights BEL's commitment to corporate governance and community development, reflecting its role as a leader in the defence electronics sector.

**bullets**

- Management highlighted a strong focus on R&D to drive innovation and technological leadership.
- The report emphasized sustainability efforts, including a roadmap to achieve net-zero emissions by 2030.
- Management stated a commitment to expanding both domestic and international market presence.
- The company aims to enhance its operational efficiency through digital transformation and Industry 4.0 initiatives.
- BEL's governance framework includes robust risk management and compliance with corporate governance standards.

**key_takeaway**

Management underscored the importance of sustainable practices and innovation as central to BEL's growth strategy.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**executive_summary**

Bharat Electronics Limited (BEL) reported on its FY2025-26 performance, emphasizing strategic priorities such as strengthening core defense capabilities, expanding into non-defense and export markets, and enhancing operational efficiency. The report highlighted continued investment in R&D to drive innovation and support India's technological self-reliance. BEL also outlined its commitment to sustainable practices, including a roadmap to achieve Net Zero Scope 1 & 2 emissions by 2030. The company noted robust order inflows, a growing domestic and international presence, and a focus on ESG principles to ensure long-term growth and responsible business practices.

**key_points**

- Strategic focus on strengthening core defense business and expanding into non-defense and export markets
- Commitment to achieving Net Zero Scope 1 & 2 emissions by 2030
- Continued investment in R&D to drive innovation and support India's technological self-reliance
- Robust order inflows and growing domestic and international presence
- Emphasis on ESG principles and sustainable practices

**important_risks**

_(none)_

**key_takeaway**

BEL's strategic focus on strengthening its core defense business, expanding into non-defense and export markets, and enhancing operational efficiency through innovation and sustainable practices positions it for long-term growth and resilience.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| Lexical overlap | 0.3482 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 65.6261 s |
| Input / output tokens | 12367 / 271 |
| Tokens/sec (output) | 4.1 |

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
