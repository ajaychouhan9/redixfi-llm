# Review sheet — concall_summary

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
| Fixture | `/kaggle/input/datasets/ajaychouhan9/redixfi-llm-evaluation-2026/concall_benchmark.json` |
| Cases | 20 of 20 |
| Run id | `20260829T200720Z` (2026-08-29T20:07:20.630896+00:00) |
| LLM project commit | `unknown` |
| GPU | 2x Tesla T4 (29.12 GB total) |
| CUDA / torch / vLLM | 13.0 / 2.13.0+cu130 / None |

## Objective signals (mechanical only — no judgement)

| Metric | Value |
|---|---|
| cases | 20 |
| generated_ok | 15 |
| generation_failures | 5 |
| candidate_compliance_failures | 5 |
| reference_backstop_artifacts | 0 |
| reference_compliance_failures | 0 |
| cases_with_reference | 20 |
| structured_output_used | 20 |
| json_repair_used | 0 |
| guided_and_clean | 20 |
| guided_but_repaired | 0 |
| unguided | 0 |
| mean_latency_sec | 65.88 |
| total_prompt_tokens | 364781 |
| total_completion_tokens | 14941 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| tone_label_agreement_rate | 0.6667 |
| invalid_tone_labels | 0 |
| tone_confusion | Mixed->Positive=1, Positive->Positive=7, Neutral->Neutral=1, Mixed->None=3, Mixed->Mixed=2, Neutral->Positive=1, Neutral->Mixed=2, Positive->None=2, Positive->Mixed=1 |
| mean_lexical_overlap | 0.206 |

## Cases

---

### Case 1 — `CC_BATAINDIA_106539458`

#### SOURCE / EVIDENCE

- **Symbol:** BATAINDIA
- **Company:** Bata India Limited
- **Filing id:** 106539458
- **Doc type:** concall_transcript
- **Doc kind:** earnings concall transcript

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
BATA INDIA LIMITED 
CIN: L19201WB1931PLC007261 
Registered Office: 27B, Camac Street, 1st Floor, Kolkata-700016, West Bengal II Tel.: (033) 22895796 II Fax: (033) 22895748 
E-mail: in-customer.service@bata.com II Website: www.bata.in 
 
      February 18, 2026 
 
The Manager, CRD 
BSE Limited 
P J Towers, Dalal Street, Fort, 
Mumbai - 400001 
The Manager, Listing Department 
National Stock Exchange of India Limited 
Exchange Plaza, 5th Floor,  
Plot No. C-1, Block G, BKC, Bandra (E), 
Mumbai - 400051     
 
The Secretary 
The 
Calcutta 
Stock 
Exchange 
Limited 
7, Lyons Range, 
Kolkata - 700001 
BSE Security Code: 500043 
NSE Symbol: BATAINDIA  
CSE Scrip Code: 10000003  
 
Dear Sir/Madam, 
 
Subject: Post Earnings Call  
This is further to our letters dated January 28, 2026, February 12, 2026 and February 13, 2026, on the captioned 
subject. 
Pursuant to Regulation 30 of the SEBI (Listing Obligations and Disclosure Requirements) Regulations, 2015, we 
are enclosing herewith the transcript of the Post Earnings Call (Group Call) held on Friday, February 13, 2026. 
The above information shall also be made available on Company’s website viz., www.bata.in  
This is for your information and records. 
 
Thanking you, 
Yours faithfully, 
For BATA INDIA LIMITED 
 
  
NITIN BAGARIA 
AVP – Company Secretary & Compliance Officer 
 
 
Encl.: As above 
Digitally signed by NITIN BAGARIA

Page 1 of 14 
 
 
Bata India Limited 
Q3 and FY '26 Earnings Conference Call 
February 13, 2026 
 
 
 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Mixed`

**summary**

Bata India Limited's earnings conference call on February 13, 2026, highlighted a turnover growth of 3% for the quarter, attributed to the implementation of a zero-based merchandising project across 400 stores and increased marketing expenditures. Management noted improvements in key metrics such as inventory freshness and turnaround times. The company reported a double-digit underlying PBT growth of 10%, with significant contributions from brands like Hush Puppies and Power. The franchise network expanded to nearly 2,000 outlets, and e-commerce sales grew, with 14% of direct-to-consumer business coming from a newly launched app. Management acknowledged challenges in achieving double-digit growth aspirations but emphasized ongoing initiatives in marketing, product development, and channel expansion to drive future growth. The discussion also touched on the impact of GST on sales and the company's strategy to enhance brand relevance among younger consumers.

**tone_note**

Management reported growth and improvements while acknowledging challenges in achieving higher growth rates.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**tone_label:** `Positive`

**summary**

Bata India Limited’s Q3 and FY ’26 earnings conference call highlighted a **3% turnover growth** driven by initiatives like **zero-based merchandising (ZBM)**, expanded to **400 stores**, and **double-digit marketing spend increases**. Management emphasized **Hush Puppies, Power, and Floatz brands** as key growth drivers, with **Hush Puppies contributing ~15–20% of retail sales (INR 700 crore)**. The **corner stores channel** showed a turnaround with strong margins, while **franchise expansion (now ~700 stores, aiming for 1,000+)** and **e-commerce (mid-teens contribution, 15% QoQ growth)** were noted as high-potential areas. **Inventory efficiency improved by 11%**, with **aged inventory at all-time lows**, and **EBITDA rose by 200 bps**. Challenges included **GST-related disruptions (partially recovered)** and **competitive pressure in value/premium segments**, addressed via **product funnel reimagining, digital marketing, and store renovations**. Management reiterated **no forward guidance** but cited **network expansion and product innovation** as long-term growth levers. **Export ambitions (historically ~700K–1M pairs) were noted as scaling post-FTA**, though specifics were deferred. **Consumer age demographics (avg. 31–32 years)** and **manufacturing rationalization (in-house down to mid-teens%)** were also discussed as strategic focuses.

**tone_note**

Management emphasized **momentum, green shoots, and tangible improvements** in key metrics like turnover, margins, and channel performance, framing current initiatives as growth enablers.

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'targets'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 2 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Mixed` |
| tone_label — Qwen | `Positive` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ❌ no |
| Lexical overlap | 0.2515 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 74.0121 s |
| Input / output tokens | 23460 / 764 |
| Tokens/sec (output) | 10.3 |

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

### Case 2 — `CC_SUNTECK_106596830`

#### SOURCE / EVIDENCE

- **Symbol:** SUNTECK
- **Company:** Sunteck Realty Limited
- **Filing id:** 106596830
- **Doc type:** concall_transcript
- **Doc kind:** investor presentation

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
Sunteck Realty Ltd. 
                   
 
5th Floor, Sunteck Centre, 37-40 Subhash Road, Vile Parle (East), Mumbai 400057. Tel: +91 22 4287 7800 Fax: +91 22 4287 7890  
Website: www.sunteckindia.com CIN: L32100MH1981PLC025346 Email Id: cosec@sunteckindia.com  
  Date: 22nd April, 2026 
 
National Stock Exchange of India Ltd 
Exchange Plaza, Plot no. C/1, G Block, 
Bandra-Kurla Complex, Bandra (East),  
Mumbai - 400 051 
Symbol: SUNTECK 
BSE Limited 
Phiroze Jeejeebhoy Tower, 
Dalal Street, 
Mumbai - 400 001 
Scrip Code: 512179 
 
Sub: Investor Presentation on Q4 and Full Year FY26 Results 
 
Dear Sir/Madam, 
 
Please find enclosed the Investor Presentation with regard to the Financial Results of the Company for the 
quarter and year ended 31st March, 2026. 
 
The Investor Presentation shall also be placed on the Company’s website. 
 
This is for your information and records. 
 
Yours sincerely, 
For Sunteck Realty Limited 
 
 
 
Rachana Hingarajia 
Company Secretary 
(ACS No.: 23202) 
Encl: a/a 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Rachana 
Vipul 
Hingarajia
Digitally signed by 
Rachana Vipul 
Hingarajia 
Date: 2026.04.22 
14:22:38 +05'30'

Sunteck Realty Limited
Investor Presentation
Q4 & Full Year FY26 
April 2026
NSE: SUNTECK | BSE: 512179 | Bloomberg: SRIN: IN  | Reuters: SUNT.NS / SUNT.BO 

Disclaimer
By attending the meeting where this presentation is made and any additional material is provided (“Presentation”) or by reading the Presentation, you (“Recipient”),

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

Sunteck Realty Limited reported its financial results for Q4 and the full year FY26, highlighting a revenue increase to approximately Rs. 339 crore in Q4FY26 and Rs. 1,124 crore for FY26, representing year-on-year growth of 65% and 32%, respectively. EBITDA also saw significant growth, reaching around Rs. 97 crore in Q4FY26 and Rs. 305 crore for FY26, up 41% and 64% YoY. The company reported a PAT of Rs. 63 crore in Q4FY26 and Rs. 202 crore for FY26, marking increases of 25% and 34% YoY. Operationally, pre-sales grew to Rs. 1,064 crore in Q4FY26 and Rs. 3,157 crore for FY26, with collections at Rs. 432 crore and Rs. 1,433 crore, respectively. The company maintained a strong net debt to equity ratio of 0.06x and reported a net cash flow surplus of Rs. 552 crore, up 48% YoY. Sunteck emphasized its strong market position and successful equity partnerships.

**tone_note**

Management highlighted strong financial and operational growth metrics.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**tone_label:** `Positive`

**summary**

The investor presentation for Sunteck Realty Ltd. reported strong financial and operational performance for Q4 and full-year FY26. Revenue grew **65% YoY** to **₹339 cr** in Q4FY26 and **32% YoY** to **₹1,124 cr** for FY26, with EBITDA rising **41% YoY** to **₹97 cr** in Q4 and **64% YoY** to **₹305 cr** for FY26. PAT increased **25% YoY** to **₹63 cr** in Q4 and **34% YoY** to **₹202 cr** for FY26, maintaining EBITDA and PAT margins at **29%/19%** (Q4) and **27%/18%** (FY26). Pre-sales surged **22% YoY** to **₹1,064 cr** in Q4 and **25% YoY** to **₹3,157 cr** for FY26, while collections grew **39% YoY** to **₹432 cr** in Q4 and **14% YoY** to **₹1,433 cr** for FY26. Net cash flow surplus reached **₹552 cr** (up **48% YoY**), and net debt-to-equity stood at **0.06x**. The company highlighted its **MMR-focused luxury portfolio**, **strategic acquisitions** (50+ million sq ft, **₹41,030 cr GDV**), and **expanding annuity income** (₹300+ cr rental, **₹5,000 cr capital value potential**). Partnerships with **IFC-World Bank**, **Kotak Fund**, and **Ajay Piramal Group** were emphasized, alongside a **AA credit rating** and **ESG leadership** (GRESB 5-star, DJSI 78/100 score).

**tone_note**

Management emphasized robust YoY growth in revenue, profitability, and pre-sales, alongside strategic acquisitions, strong cash flows, and ESG achievements.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Positive` |
| tone_label — Qwen | `Positive` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ✅ yes |
| Lexical overlap | 0.3333 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 39.2395 s |
| Input / output tokens | 8000 / 514 |
| Tokens/sec (output) | 13.1 |

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

### Case 3 — `CC_KANPRPLA_106607445`

#### SOURCE / EVIDENCE

- **Symbol:** KANPRPLA
- **Company:** Kanpur Plastipack Limited
- **Filing id:** 106607445
- **Doc type:** concall_transcript
- **Doc kind:** investor presentation

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
Manufacturers & Exporters: 
Flexible Intermediate Bulk Container (FIBC) I PP Multifilament Yarn I UV Master Batches I Fabrics I CPP Films 
CIN: L25209UP1971PLC003444 
 
 
 
D-19,20 Panki Industrial Area, 
Kanpur-208022, India
+91(512) 2691113-116
info@kanplas.com
www.kanplas.com
May 02, 2026 
BSE Limited 
Phiroze Jeejeebhoy Towers,  
Dalal Street, 
Mumbai 400 001 
 
Scrip Code: 507779 
National Stock Exchange of India Limited 
Exchange Plaza, Plot No. C/1, 
G Block, Bandra – Kurla Complex,  
Bandra (East), Mumbai 400 051 
 
Trading Symbol: KANPRPLA 
 
Sub:- Intimation under Regulation 30 of the SEBI (Listing Obligations and Disclosure 
Requirements) Regulations, 2015 - Investor Presentation on Financial Results for the Quarter and 
Financial Year ended March 31, 2026. 
 
Dear Sir, 
 
Pursuant to Regulation 30 of the SEBI (Listing Obligations and Disclosure Requirements) Regulations, 
2015, please find enclosed herewith the Investor Presentation on the Financial Results for the Quarter and 
Financial Year ended March 31, 2026. 
 
The aforesaid Investor Presentation is also available on the website of the Company at: 
 
https://www.kanplas.com/report_pdf/KPL_Investor_Presentation_Q4_FY26._1777724631.pdf 
 
 
Please take this on record and oblige. 
Thanking You. 
 
Yours Faithfully, 
For Kanpur Plastipack Limited 
 
 
 
(Ankur Srivastava) 
Company Secretary 
 
Encl: A/a 
 
Ankur 
Srivastava
Digitally signed by Ankur Srivastava 
DN: c=IN, o=Personal, postalCode=208014, l=Kanpur N

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

The investor presentation by Kanpur Plastipack Limited detailed the company's financial results for the quarter and financial year ended March 31, 2026. The presentation highlighted a total income of Rs. 18,505 lakhs for Q4 FY26, reflecting a year-on-year growth of 7.26%. EBITDA for the same quarter was reported at Rs. 2,556 lakhs, with a margin of 13.81%, up from 12.28% in the previous year. Net profit increased by 24.70% to Rs. 1,492 lakhs, with an EPS of 6.2. The company emphasized its strong export model, with approximately 70% of revenue derived from international markets, and outlined strategic initiatives for capacity expansion and diversification into technical textiles. Sustainability efforts were also highlighted, with nearly 50% of energy needs met through solar power. The presentation concluded with a focus on disciplined diversification and capital allocation.

**tone_note**

Management emphasized growth in financial performance and strategic initiatives.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**tone_label:** `Positive`

**summary**

The investor presentation for Kanpur Plastipack Limited (Q4 FY26) highlighted a **27% year-over-year revenue growth** (₹73,132 lakhs) and a **42% EBITDA expansion** (₹7,770 lakhs), driven by export-led demand (70% of revenue) and a diversified product portfolio. Management emphasized **FIBCs as the core growth engine**, with Q4 FY26 revenue from FIBCs at ₹28,657 lakhs (39% of total revenue), alongside expansion into **premium PP yarn and non-woven fabrics**—the latter set to commence commercial production in September 2026. The company reported **margin improvements** (EBITDA margin up 113 BPS YoY to 10.62%) and **sustainability initiatives**, including 50% solar-powered energy and zero-liquid-discharge operations. Strategic moves included the **acquisition of Valex Ventures Ltd (UK)** and a **50:50 JV with Essegomma S.p.A. (Italy)** to strengthen Europe’s export footprint. Capacity expansions—such as the **Unit 3 FIBC facility (completed ahead of schedule)**—were noted to support long-term volume growth. The presentation also detailed a **shift toward value-added products** (e.g., food-grade FIBCs, UV masterbatches) and **B2C-linked premium applications** (e.g., automotive textiles, medical fabrics) to reduce cyclicality. Financials showed **consolidated net profit growth of 76% YoY** (₹4,080 lakhs) and **standalone net profit growth of 68% YoY** (₹3,819 lakhs), with Q4 FY26 standalone EBITDA at ₹2,506 lakhs (13.68% margin).

**tone_note**

Management emphasized record revenue and EBITDA growth, strategic acquisitions, capacity expansions, and margin improvements while outlining disciplined diversification into high-margin segments.

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'outlook'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 2 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Positive` |
| tone_label — Qwen | `Positive` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ✅ yes |
| Lexical overlap | 0.2162 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 43.9132 s |
| Input / output tokens | 12504 / 868 |
| Tokens/sec (output) | 19.8 |

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

### Case 4 — `CC_COROMANDEL_106614369`

#### SOURCE / EVIDENCE

- **Symbol:** COROMANDEL
- **Company:** Coromandel International Limited
- **Filing id:** 106614369
- **Doc type:** concall_transcript
- **Doc kind:** investor presentation

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
Ref. No: 2026-27/008 
 
  May 08, 2026 
National Stock Exchange of India Limited 
Exchange Plaza, 5th Floor, 
Bandra-Kurla Complex, 
Bandra (E), Mumbai 400 051 
Symbol: COROMANDEL 
BSE Limited, 
Phiroze Jeejeebhoy Towers, 
Dalal Street, 
Mumbai 400 001.p 
Scrip Code: 506395 
 
Dear Sir / Madam,  
 
Sub 
: 
Investor Presentation of Conference Call to discuss the Q4FY26 results to be held on May 
8, 2026 
This is further to our letter(s) ref no. 2026-27/005 dated May 05, 2026 regarding Conference Call to discuss 
financial results of the Company for the quarter ended March 31, 2026. 
 
In this regard, we wish to inform that the Investor presentation to be made at the Conference Call scheduled 
today i.e., May 8, 2026 at 02:30 PM (IST) has been uploaded on the website of the Company at 
https://www.coromandel.biz/investors/corporate-presentation/ as required pursuant to Regulation 
46(2)(o) of the SEBI (Listing Obligations and Disclosure Requirements) Regulations, 2015. 
 
We kindly request you to take the above submission on record. 
 
Thanking you, 
 
Yours truly, 
For Coromandel International Limited 
 
 
 
B. Shanmugasundaram  
Company Secretary & Compliance Officer 
 
BALASUBRAM
ANIAN 
SHANMUGASU
NDARAM
Digitally signed by 
BALASUBRAMANIAN 
SHANMUGASUNDARA
M 
Date: 2026.05.08 
13:11:27 +05'30'
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Neutral`

**summary**

Coromandel International Limited announced the scheduling of a conference call to discuss its Q4FY26 results, which took place on May 8, 2026. The investor presentation related to this call was made available on the company's website, in compliance with SEBI regulations. The communication was signed by B. Shanmugasundaram, the Company Secretary and Compliance Officer, and requested acknowledgment of the submission.

**tone_note**

The document provided factual information regarding the conference call and investor presentation.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**tone_label:** `Neutral`

**summary**

The investor presentation for Coromandel International Limited’s Q4FY26 earnings conference call, held on May 8, 2026, was uploaded to the company’s website as required by SEBI regulations. The document, referenced as 2026-27/008, confirms the scheduled conference call at 02:30 PM IST to discuss financial results for the quarter ended March 31, 2026. The presentation is available under the ‘Corporate Presentation’ section of the company’s investor relations webpage. No specific financial or operational details were provided in this filing, as it primarily serves as a procedural notification for the upcoming conference call.

**tone_note**

The document contained only procedural and compliance-related information without any evaluative or directional commentary.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Neutral` |
| tone_label — Qwen | `Neutral` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ✅ yes |
| Lexical overlap | 0.2787 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 5.0473 s |
| Input / output tokens | 1123 / 183 |
| Tokens/sec (output) | 36.3 |

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

### Case 5 — `CC_ALKYLAMINE_106620224`

#### SOURCE / EVIDENCE

- **Symbol:** ALKYLAMINE
- **Company:** Alkyl Amines Chemicals Limited
- **Filing id:** 106620224
- **Doc type:** concall_transcript
- **Doc kind:** earnings concall transcript

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
May 13, 2026 
 
To,  
BSE Limited 
P. J. Towers, Dalal Street,  
Mumbai - 400 001  
SCRIP CODE: 506767  
 
 
The NaƟonal Stock Exchange of India Limited 
Exchange Plaza, Bandra Kurla Complex,  
Bandra - (E), Mumbai - 400 051 
SYMBOL: ALKYLAMINE 
Dear Sir / Madam, 
 
Subject: Transcript of Conference Call held on May 6, 2026 with investors and analyst on financial 
performance of Q4FY26 
 
Pursuant to Regulation 30 of the SEBI (Listing Obligations and Disclosure Requirements) Regulations, 
2015, we are enclosing herewith the transcript of the Conference Call held on Wednesday, May 6, 
2026 at 3.00 p.m. (IST) with investors and analyst on financial performance of Q4FY26. 
 
The said transcript will also be made available at the website of the Company at www.alkylamines.com 
under Investor Relations>Investor Center>Conference Call Transcripts 
 
You are requested to kindly take the same on your record.   
 
Thanking you, 
 
For Alkyl Amines Chemicals Limited 
 
 
 
Chintamani Thatte 
General Manager (Legal) & Company Secretary  
& Compliance Oﬃcer 
 
Encl: As above 
Chintamani 
Dattatraya 
Thatte
Digitally signed by 
Chintamani 
Dattatraya Thatte 
Date: 2026.05.13 
12:42:34 +05'30'

Page 1 of 16 
 
 
 
“Alkyl Amines Chemicals Limited 
Q4 and FY26 Earnings Conference Call” 
May 06, 2026 
 
 
 
 
 
 
       
 
 
MANAGEMENT: MR. KIRAT PATEL – EXECUTIVE DIRECTOR – ALKYL 
AMINES CHEMICALS LIMITED 
 
MRS. KANCHAN SHINDE – CHIEF FINANCIAL OFFICER 
– ALKYL AMINES CHEMICALS LIMITED 
 
MR

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Mixed`

**summary**

The earnings conference call for Alkyl Amines Chemicals Limited, held on May 6, 2026, featured management discussing the company's financial performance for Q4FY26. Management reported that both the top line and bottom line remained flat, with a slight increase in market share despite challenging market conditions. They noted that raw material prices, particularly ammonia, had risen significantly due to geopolitical factors, impacting production costs. Management indicated that while they had managed to source ammonia, the future supply chain remained uncertain. They mentioned a cautious optimism regarding potential volume growth of 5% to 10% in the upcoming year, contingent on market stability. Additionally, management highlighted ongoing projects and the potential for new product launches, while emphasizing the importance of maintaining competitive margins amidst fluctuating raw material prices. The call concluded with management expressing gratitude for investor interest and engagement.

**tone_note**

Management conveyed both challenges and cautious optimism regarding future performance.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'likely'
- pass 2: forward-tense word 'expected'
- pass 3: forward-tense word 'targets'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ❌ no — failed validation after 3 attempts |
| Attempts used | 3 |
| Compliance — **Qwen** | ❌ FAIL — empty text |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Mixed` |
| tone_label — Qwen | `None` |
| tone_label valid (closed set) | ❌ |
| tone_label agrees | — |
| Lexical overlap | 0.0 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 104.36 s |
| Input / output tokens | 38743 / 1195 |
| Tokens/sec (output) | 11.5 |

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

### Case 6 — `CC_AARTIDRUGS_106626214`

#### SOURCE / EVIDENCE

- **Symbol:** AARTIDRUGS
- **Company:** Aarti Drugs Limited
- **Filing id:** 106626214
- **Doc type:** concall_transcript
- **Doc kind:** investor presentation

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
Ref: ADL/SE/2026-27/11 
        May 16, 2026 
 
To, 
Listing/ Compliance Department 
BSE Limited 
Phiroze Jeejeebhoy Towers,  
Dalal Street,  
Mumbai – 400 001 
BSE CODE: 524348 
To, 
Listing/ Compliance Department 
National Stock Exchange of India Limited, 
“Exchange Plaza”, Plot No. C/1, 
G Block Bandra - Kurla Complex,  
Bandra (East), Mumbai – 400051 
NSE SYMBOL: AARTIDRUGS 
Dear Sir/Madam, 
       
Ref:   Regulation 30 of SEBI (Listing Obligations and Disclosure 
Requirements) Regulations, 2015. 
 
Sub:  Investor Presentation 
 
Please find attached herewith Q4 & FY26 Investor Presentation. 
 
Kindly take the same on record. 
 
Thanking you, 
Yours faithfully, 
FOR AARTI DRUGS LIMITED 
 
 
RUSHIKESH DEOLE  
COMPANY SECRETARY & COMPLIANCE OFFICER 
ICSI M. No.: F12932 
 
 
 
RUSHIKESH 
VIVEK DEOLE
Digitally signed by RUSHIKESH VIVEK DEOLE 
DN: c=IN, postalCode=421301, st=MAHARASHTRA, street=THANE,B-2, 
DEVIPRASAD SOCIETY, AGRA ROAD ,421301, l=THANE, o=Personal, 
serialNumber=9b60f64457feab7f455d17463ebe710861bf01b575f6fc04
84483273dabfc17f, pseudonym=39fdd8cc665b44adb709d2b2c0bc1ffe, 
2.5.4.20=76af11ab2ea790a8aec8b0d90f9da6fdb715f5b922a7af009bb3f
93dc014e116, email=RUSHIKESH.DEOLE@AARTIDRUGS.COM, 
cn=RUSHIKESH VIVEK DEOLE 
Date: 2026.05.16 14:27:54 +05'30'

Aarti Drugs Limited
Q4 & FY26 Investor Presentation
May 2026

Safe Harbor 
This presentation and the accompanying slides (the “Presentation”), which have been prepared by Aarti Drugs Limited (the “Company”), have been p

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Mixed`

**summary**

Aarti Drugs Limited's investor presentation for Q4 and FY26 highlighted a total revenue of Rs. 721.1 crore for Q4 FY26, marking a 6% year-over-year increase. EBITDA was reported at Rs. 96.6 crore, with a margin of 13.4%, reflecting a decline of 60 basis points compared to the previous year. The presentation noted that the company's profitability was affected by start-up losses from new facilities and weakness in the domestic antibiotics market. However, sequentially, revenue and EBITDA improved by 20% and 72%, respectively. The management emphasized a shift towards regulated markets, with contributions increasing from 66% in FY25 to 73% in FY26. The company also reported a strong focus on expanding its product pipeline and enhancing operational capabilities, particularly in oncology and specialty chemicals. Overall, the presentation outlined the company's strategic initiatives and resilience amid industry challenges.

**tone_note**

The presentation conveyed both positive growth in certain areas and challenges affecting profitability.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**tone_label:** `Mixed`

**summary**

Aarti Drugs Limited’s Q4 & FY26 investor presentation highlighted a **6% YoY revenue increase** to **Rs. 721.1 crore**, driven by sequential growth of **20% QoQ** and **72% EBITDA growth** in Q4 FY26, attributed to the **Sayakha facility’s scale-up** (1,000 tonnes/month run-rate) and improved export traction. EBITDA margins contracted **60 bps YoY to 13.4%** due to **start-up losses** and **domestic antibiotics market weakness**, though sequential margin expansion of **410 bps** was noted. Segment-wise, **APIs contributed 77% of revenue**, while **Formulations and Specialty Chemicals grew 33% and 37% YoY**, respectively. The company emphasized **backward integration** (e.g., anti-diabetic and antiprotozoal expansions) and **regulated market penetration** (73% of FY26 revenue), alongside **38% export contribution**. Management cited **pricing stabilization in APIs** post-H1 FY26 and **cost mitigation via product mix optimization**, though **raw material and logistics inflation** persisted. The **balance sheet remained robust**, with **net debt-to-equity at 0.4x** and **cash flow generation improving sequentially**. Strategic priorities include **oncology development (Rs. 200 crore investment)**, **USFDA/MHRA approvals**, and **geographic expansion** (e.g., Latin America, Africa). Historical trends showed **revenue volatility** (FY22–FY26: **2,488.6–2,716.1 crore**) and **EBITDA margin compression** (13.7% in FY22 to 12.1% in FY26), offset by **PAT growth (16% YoY in FY26)** and **dividend/buyback distributions (~Rs. 278 crore over 7 years)**. The presentation underscored **operational leverage** from **greenfield projects** and **R&D focus** (Rs. 66 crore in FY26) on **complex generics and regulated-market products**.

**tone_note**

Management acknowledged sequential recovery in Q4 FY26 but also cited persistent headwinds like pricing pressure, raw material inflation, and facility start-up losses, while highlighting strategic initiatives to improve margin resilience and revenue mix.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Mixed` |
| tone_label — Qwen | `Mixed` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ✅ yes |
| Lexical overlap | 0.2083 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 88.8335 s |
| Input / output tokens | 15082 / 557 |
| Tokens/sec (output) | 6.3 |

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

### Case 7 — `CC_INDIQUBE_106632356`

#### SOURCE / EVIDENCE

- **Symbol:** INDIQUBE
- **Company:** Indiqube Spaces Limited
- **Filing id:** 106632356
- **Doc type:** concall_transcript
- **Doc kind:** investor presentation

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
Indiqube Spaces Limited  
(formerly known as Indiqube Spaces Private Limited, Innovent Spaces Private Limited)                                 nfo@indiqube.com  
Registered and Corporate Office:                                                                                                                                   www.indiqube.com 
Plot # 53, Careernet Campus, Kariyammanna Agrahara Road, Devarabisanahalli,                                                   +91 9900092210 
Outer Ring Road, Bangalore, Karnataka, India, 560103                                                                                                 
CIN - L45400KA2015PLC133523                                                                                                                                    
                                                                                          
 
May 20, 2026  
To, 
 
BSE Limited, 
20th Floor, P.J. Towers, 
Dalal Street, 
Mumbai - 400001 
BSE Scrip Code: 544454 
National Stock Exchange of India Limited, 
Exchange Plaza, C-1, Block G, 
Bandra Kurla Complex, Bandra (E),  
Mumbai – 400 051 
NSE Scrip Symbol: INDIQUBE 
 
 
Subject: Subject: Disclosure under Regulation 30 of the Securities and Exchange Board 
of India (Listing Obligations and Disclosure Requirements) Regulations, 2015 - 
Presentation on the Financial Results 
 
This is with reference to our intimation dated May 14, 2026, regarding intimation of Investors/ 
Analysts call of Indiqube Spa

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

Indiqube Spaces Limited reported a record financial performance for FY26, with total income reaching ₹1,491 crore, a year-on-year growth of 37%. The company achieved a profit after tax (PAT) of ₹125 crore, reflecting a significant increase of 145% compared to the previous year. Management highlighted the resilience of their business model amid geopolitical volatility and AI-related uncertainties. The company expanded its presence to 17 cities, operating 130 properties with over 9.66 million square feet of office space, maintaining a steady occupancy rate of 88%. The earnings presentation outlined a disciplined expansion strategy, with a focus on enhancing client value and operational efficiency. Key highlights included the addition of 28,000 seats and a growing contribution from value-added services, which accounted for 15% of total revenue. The management expressed confidence in the long-term growth potential of their workspace platform.

**tone_note**

The document emphasized strong financial growth and operational resilience.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**tone_label:** `Positive`

**summary**

Indiqube Spaces Limited’s FY26 investor presentation reported record financial performance, with total income of ₹1,491 crore (up 37% YoY) and PAT of ₹125 crore (up 145% YoY), alongside healthy EBITDA margins of 21%. Management attributed growth to disciplined expansion—adding 28,000 seats and 13 new centers, expanding to 17 cities—and a steady-state occupancy of 88%. Key operational highlights included a 15% YoY increase in area under management (AUM) to 9.66 million sq. ft., a 36% YoY rise in recurring revenue, and a 15% contribution from value-added services (VAS) to total revenue. The company also emphasized its tech-enabled workspace solutions (MiQube platform) and green workspace initiatives. Leadership noted resilience amid geopolitical and AI-driven uncertainties, while financial metrics improved, including a 21% EBITDA margin and a 9% PAT margin. The presentation also clarified accounting adjustments under Ind AS 116, highlighting that lease liabilities and depreciation on right-of-use assets were non-cash items not indicative of operational cash flow health. The company’s debt-to-equity ratio improved to 0.08, and cash flow from operations grew to ₹304 crore. Operational breakeven was achieved at 55–60% occupancy, with a 3.3 million sq. ft. headroom in occupancy demand. The presentation concluded with a focus on scaling across India’s growth corridors and fostering workspaces for large enterprises.

**tone_note**

Management emphasized record revenue, profitability, and operational expansion while highlighting resilience and strategic growth initiatives.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Positive` |
| tone_label — Qwen | `Positive` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ✅ yes |
| Lexical overlap | 0.2903 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 65.3806 s |
| Input / output tokens | 13167 / 393 |
| Tokens/sec (output) | 6.0 |

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

### Case 8 — `CC_TVSELECT_106638347`

#### SOURCE / EVIDENCE

- **Symbol:** TVSELECT
- **Company:** TVS Electronics Limited
- **Filing id:** 106638347
- **Doc type:** concall_transcript
- **Doc kind:** investor presentation

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
TVS Electronics Limited 
       “Arihant E-Park”, No.117/1, 9th Floor, L.B. Road, Adyar, Chennai – 600 020. Tel.: +91-44-42005200 
     Registered Office: Harita Towers, 2nd Floor, No.119, St. Mary’s Road, Abhiramapuram, Chennai- 600 018 
     Corporate Identity Number: L30007TN1995PLC032941 
     E-mail id: webmaster@tvs-e.in Website: www.tvs-e.in 
 
 
 
 
 
 
 
 
 
24th May 2026 
 
 
BSE Limited 
Phiroze Jeejeebhoy Towers 
Dalal Street 
Mumbai - 400 001 
Scrip Code - 532513 
 
National Stock Exchange of India Limited Exchange 
Plaza, 5th Floor 
Plot No. C/1 G Block 
Bandra - Kurla Complex, Bandra - (E) 
Mumbai - 400 051 
Scrip Symbol - TVSELECT 
 
 
Dear Sir/ Madam, 
 
Sub: Earnings Presentation – Q4- FY26/ FY26 
 
Pursuant to Regulation 30(2) and other respective Regulations of SEBI (Listing Obligations and 
Disclosure Requirements) Regulations, 2015, we are herewith enclosing the copy of Earnings 
Presentation – Q4-FY26/FY26. 
 
Kindly take the above information on record. 
Thanking you, 
Yours truly, 
For TVS Electronics Limited 
 
 
 
 
K Santosh 
Company Secretary 
 
 
 
 
 
 
 
 
 
SANTOSH 
KRISHNADASS
Digitally signed by 
SANTOSH KRISHNADASS 
Date: 2026.05.24 
13:31:42 +05'30'

1
TVS Elecronics Limited
Earnings Presentation
Q1-FY25
EARNINGS 
PRESENTATION
Q4-FY26/FY26

2
Snapshot
State-of-the-art 
hardware solutions for 
retail, BFSI & logistics 
industries.
Unique edge of 
customizing & bundling 
hardware and software 
solutions
Indian electronics 
manufacturer with 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Neutral`

**summary**

TVS Electronics Limited's investor presentation for Q4-FY26 reported a revenue from operations of INR 1,174 million, reflecting a 2.4% year-over-year increase and a 3.3% quarter-over-quarter increase. The Customer Support Services segment generated revenue of INR 370 million in Q4-FY26, up 10.4% year-over-year, while the Products and Solutions Group reported INR 804 million, a slight decrease of 0.9% year-over-year. The overall FY26 revenue reached INR 4,552 million, marking a 5.7% increase from FY25. EBITDA for Q4-FY26 was INR 70 million, with an EBITDA margin of 5.96%, showing significant improvement from the previous year. The presentation highlighted strategic priorities, including enhancing tech products and strengthening supply chain capabilities. The company also emphasized its commitment to local manufacturing under the 'Make in India' initiative. The document concluded with a focus on integrated solutions for various sectors, including retail and logistics.

**tone_note**

The presentation provided a balanced overview of financial performance and strategic initiatives without strong emphasis on growth or challenges.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**tone_label:** `Positive`

**summary**

The Q4-FY26/FY26 earnings presentation for TVS Electronics Limited reported revenue growth and operational improvements. For FY26, total revenue increased 5.7% year-over-year (YoY) to INR 4,552 Mn, with the **Products and Solutions Group (PSG)** contributing INR 3,164 Mn (up 3.0% YoY) and **Customer Support Services (CSS)** contributing INR 1,388 Mn (up 12.7% YoY). EBITDA rose 77.3% YoY to INR 195 Mn, with an EBITDA margin improving 172 basis points (BPs) to 4.28%, driven by a better product mix and cost management initiatives. Q4-FY26 revenue was INR 1,174 Mn (up 3.3% quarter-over-quarter [QoQ] and 2.4% YoY), with EBITDA at INR 70 Mn (5.96% margin, up 413 BPs YoY). The company highlighted expansion in manufacturing and logistics segments, new customer additions, and strategic investments in its Tumakuru facility, including a new Surface Mount Technology (SMT) line. The balance sheet showed a debt-to-equity ratio of 0.43x, while PAT turned positive at INR 13 Mn (0.29% margin) after losses in FY25. Management emphasized growth in **Customer Support Services** and **EMS (Electronics Manufacturing Services)**, alongside a focus on digital transformation in retail and logistics sectors. The presentation also noted a 100% increase in other income YoY to INR 54 Mn and a reduction in finance costs to INR 69 Mn (down from INR 54 Mn in FY25).

**tone_note**

Management emphasized revenue growth, margin expansion, and operational improvements across segments, alongside strategic investments and new customer wins.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Neutral` |
| tone_label — Qwen | `Positive` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ❌ no |
| Lexical overlap | 0.2632 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 30.2808 s |
| Input / output tokens | 6596 / 451 |
| Tokens/sec (output) | 14.9 |

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

### Case 9 — `CC_KUANTUM_106643553`

#### SOURCE / EVIDENCE

- **Symbol:** KUANTUM
- **Company:** Kuantum Papers Limited
- **Filing id:** 106643553
- **Doc type:** concall_transcript
- **Doc kind:** investor presentation

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
27.05.2026 
BSE Limited                                             
Phiroze Jeejeebhoy Towers                      
Dalal Street                                               
Mumbai 400 001                                       
Scrip Code: 532937     
Scrip ID: KUANTUM                                
National Stock Exchange of India Limited 
Exchange Plaza 
Plot No. C/1, G Block,                                           
Bandra-Kurla Complex, Bandra (East)                   
Mumbai 400 051 
Trading Symbol: KUANTUM 
 
 
Reg: Earnings Presentation – Disclosure under Regulation 30 of SEBI (Listing 
Obligations and Disclosure Requirements) Regulations, 2015 
 
Dear Sir/Madam, 
 
Pursuant to Regulation 30 of SEBI (Listing Obligations and Disclosure Requirements) 
Regulations, 2015, please find attached herewith a copy of Earnings Presentation for Quarter 
and Financial Year ended 31st March, 2026 for your information and record purposes.   
The said presentation is also being made available on the Company’s website i.e.  
www.kuantumpapers.com. 
 
Kindly take the same on record. 
 
Thanking you, 
 
Yours faithfully, 
For Kuantum Papers Limited 
 
 
 
 
(Gurinder Singh Makkar) 
Company Secretary & Compliance Officer 
M. No.: F5124 
 
 
 
 
 
 
 
 
 
1l. Kuantum Papers ltd 
© kuantumpapers.com 
S kuantumcorp@kuantumpapers.com 
S kuantummill@kuantumpapers.com 
Corp Office WlA FF Tower A Godrej Eternia Plot 70 lndl Area 1 Chandigarh 160 002 Ph -0172 5172737 
Regd Office & Works Sa

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Neutral`

**summary**

Kuantum Papers Limited's investor presentation for the quarter and financial year ended March 31, 2026, detailed the company's operational and financial performance. The presentation reported a total operational income of INR 10,932 million for FY26, a slight decrease from INR 11,070 million in FY25. EBITDA margins fell to 14.80% from 21.92% in the previous year, attributed to increased costs and a drop in net selling rates. For Q4 FY26, operational income was INR 3,009 million, with EBITDA margins improving to 15.89% from 13.55% in Q3 FY26. The company highlighted its strategic initiatives, including plant upgrades and sustainability efforts, such as expanding its Social Farm Forestry Program. Kuantum's product portfolio includes a variety of paper types, and it has increased its export footprint to 24 countries. The presentation also outlined future growth strategies focused on capacity expansion and technological advancements.

**tone_note**

The presentation provided a balanced overview of financial performance and strategic initiatives without strong emphasis on positive or negative aspects.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**tone_label:** `Mixed`

**summary**

Kuantum Papers Limited’s earnings presentation for Q4-FY26/FY26 reported a **1.2% YoY decline in operational income** to **INR 10,932 Mn**, driven by a **4% QoQ revenue increase in Q4-FY26** (INR 3,009 Mn) despite market challenges. **EBITDA margins contracted sharply** to **14.8% (FY26) and 15.9% (Q4-FY26)** from **21.9% (FY25)**, attributed to a **INR 2,000/MT drop in net selling rate (NSR)** and **INR 3,200/MT higher costs** due to cheaper imports, nil GST on notebooks, and rising raw material/energy prices. **PAT fell 63.5% YoY to INR 420 Mn**, with **PAT margins at 3.84% (vs. 10.41% in FY25)**. The company highlighted **operational upgrades**, including the **completion of Paper Machine 2 rebuild (75 TPD capacity)**, **commissioning of a Two-stage Recausticizing Plant**, and **progress on the Displacement Digester System (DDS)** for wood pulping. **Debottlenecking and Industry 4.0 initiatives** (AI, IoT) were emphasized for future efficiency gains. **Export growth to 24 countries** and **specialty product development** (e.g., dye-free Kappa Premium III CRM) were noted as strategic focuses. **Social Farm Forestry expansion** added **854 acres in Q4-FY26**, bringing total plantation to **18,300+ acres**.

**tone_note**

The presentation reported **financial headwinds** (margin compression, cost pressures) while **highlighting operational upgrades and strategic initiatives** to mitigate challenges.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Neutral` |
| tone_label — Qwen | `Mixed` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ❌ no |
| Lexical overlap | 0.2806 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 39.4791 s |
| Input / output tokens | 8595 / 446 |
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

### Case 10 — `CC_SIGACHI_106649351`

#### SOURCE / EVIDENCE

- **Symbol:** SIGACHI
- **Company:** Sigachi Industries Limited
- **Filing id:** 106649351
- **Doc type:** concall_transcript
- **Doc kind:** investor presentation

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
To 
 
 
 
 
 
 
 
                    Date: May 30, 2026 
 
The Manager 
BSE Limited 
P. J. Towers, Dalal Street 
Mumbai-400001(BSE 
Scrip Code: 543389) 
The Manager 
National Stock Exchange of India Limited 
Exchange Plaza, Bandra Kurla Complex 
Bandra (E), Mumbai- 400051 
(NSE Symbol: SIGACHI) 
 
 
 
Dear Sir/Madam, 
 
Sub: Investor Presentation for Q4 FY 2025-26 
 
 
Pursuant to Regulation 30 of SEBI (Listing Obligations and Disclosure Requirements) 2015, 
and with reference to the subject cited, please find enclosed the Investor Presentation for Q4 
FY 2025-26. The same is also uploaded on the website of the Company  www.sigachi.com  
 
Request you to kindly take the same on record. 
 
Thanking You, 
 
Yours faithfully 
For Sigachi Industries Limited 
 
 
 
Vivek Kumar 
Company Secretary & Compliance Officer 
 
 
 
 
VIVEK 
KUMAR
Digitally signed 
by VIVEK KUMAR 
Date: 2026.05.30 
16:02:36 +05'30'

SIGACHI INDUSTRIES LTD
Q 4 F Y 26 
Investor Pres entation 
30 th May ’ 2 0 2 6

No representation or warranty, express or implied, is made as to, and no reliance should be placed on, the fairness, accuracy, completeness or 
correctness of the information or opinions contained in this presentation. Such information and opinions are in all events not current after the 
date of this presentation. Certain statements made in this presentation may not be based on historical information or facts and may be 
"forward looking statements" based on the currently held beliefs and assumptio

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Mixed`

**summary**

The investor presentation for Q4 FY 2025-26 from Sigachi Industries Limited outlined the company's operational and financial highlights, emphasizing a year of resilience and strategic growth. Management reported that the Dahej-2 capacity expansion is on schedule, aiming to elevate total MCC capacity to 30,000 MTPA. The presentation highlighted a global customer base of over 500 across 65 countries and noted a 19.92% revenue CAGR over five years. Financially, the company reported a revenue of Rs. 1,219 million for Q4 FY26, a 4.01% increase QoQ, but a 4.91% decrease YoY. EBITDA margin was reported at 12.63%, down from 22.31% YoY. Management set a goal for FY27 to achieve revenue between Rs. 6,500 - 6,750 million and an EBITDA margin of 18% - 20%. The presentation also emphasized the company's commitment to sustainability and community engagement through CSR initiatives.

**tone_note**

The presentation highlighted both challenges and strategic growth initiatives.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'targeting'
- pass 2: forward-tense word 'targeting'
- pass 3: forward-tense word 'targeting'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ❌ no — failed validation after 3 attempts |
| Attempts used | 3 |
| Compliance — **Qwen** | ❌ FAIL — empty text |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Mixed` |
| tone_label — Qwen | `None` |
| tone_label valid (closed set) | ❌ |
| tone_label agrees | — |
| Lexical overlap | 0.0 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 78.809 s |
| Input / output tokens | 24300 / 1492 |
| Tokens/sec (output) | 18.9 |

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

### Case 11 — `CC_SDBL_106655906`

#### SOURCE / EVIDENCE

- **Symbol:** SDBL
- **Company:** Som Distilleries & Breweries Limited
- **Filing id:** 106655906
- **Doc type:** concall_transcript
- **Doc kind:** earnings concall transcript

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
SOM DISTILLERIES AND BREWERIES LIMITED 
Registered Office: I-A, Zee Plaza, Arjun Nagar, Safdarjung Enclave, Kamal Cinema Road, New Delhi - 110029 
Phone: +91-11-26169909, 26169712  Fax: +91-11-26195897 
Corporate Office: SOM House, 23, Zone II, M.P. Nagar, Bhopal, Madhya Pradesh – 462011 
Phone: +91-755-4278827, 4271271  Fax: +91-755-2557470 
Email : compliance@somindia.com   Website: www.somindia.com 
CIN : L74899DL1993PLC052787   
 
         
(BSE : 507514, NSE : SDBL) 
 
    
 
SDBL/BSE/NSE/2026 
 
 
 
 
 
                      5.06.2026 
 
To, 
The Manager, 
Dy. General Manager, 
Listing Department, 
Department of Corporate Services, 
NATIONAL 
STOCK 
EXCHANGE 
OF 
INDIA LIMITED 
BSE LIMITED, 
‘Exchange Plaza’ C-1, Block G, 
First Floor, P.J. Towers, 
Bandra-Kurla Complex, Bandra (E), 
Dalal Street, Fort, 
Mumbai-400 051.  
cmlist@nse.co.in 
Mumbai – 400001. 
corp.compliance@bseindia.com 
Security ID: SDBL 
Security ID: 507514 
 
SUB: INTIMATION UNDER REGULATION 30 OF THE SEBI (LISTING OBLIGATIONS 
AND 
DISCLOSURE 
REQUIREMENTS) 
REGULATIONS, 
2015 
- 
EARNINGS 
CONFERENCE CALL TRANSCRIPT 
 
Dear Sir/ Madam, 
 
Pursuant to Regulation 30 of Listing Regulations, Please find attached Earnings Conference 
Call transcript held on Tuesday, June 2, 2026 with respect to the Audited Financial Results 
for the Q4 & Financial year ended 31st March, 2026.  
 
The transcript of the said Earnings Conference Call is also available on the Company's 
website i.e. www.somindia.com.  
 
Thi

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Mixed`

**summary**

During the earnings conference call held on June 2, 2026, management reported that Som Distilleries & Breweries Limited faced a challenging fiscal year 2026, with consolidated revenue declining by 14.8% to INR 1,233 crores, impacted by operational disruptions and subdued demand in key markets. Beer volumes decreased by 20%, while the Indian Made Foreign Liquor (IMFL) segment grew by 32%. Management noted ongoing inflationary pressures affecting input costs and margins. Despite these challenges, the company maintained healthy operating cash flows and continued investments in a greenfield brewery project in Uttar Pradesh, which is on schedule. Management set a goal of achieving revenue between INR 1,400 crores and INR 1,500 crores for FY 2027, contingent on the resolution of licensing issues at the Bhopal facility. The call concluded with management expressing confidence in recovering market share and improving operational performance in the upcoming quarters.

**tone_note**

Management highlighted both challenges and opportunities for recovery in the business.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**tone_label:** `Mixed`

**summary**

The earnings conference call for Som Distilleries & Breweries Limited (SDBL) for Q4 and FY 2026 highlighted challenges and strategic initiatives. Management reported a 14.8% decline in consolidated revenue to INR1,233 crores, with EBITDA and PAT at INR89.7 crores and INR10.2 crores, respectively. Beer volumes dropped 20% to 187.19 lakh cases, while IMFL volumes grew 32% to 15.03 lakh cases. Key headwinds included operational disruptions at the Bhopal facility due to a license issue and subdued demand in Karnataka and Odisha. Despite these challenges, the company emphasized resilience in its IMFL segment and progress in its greenfield brewery project in Uttar Pradesh, which commenced commercial production in June 2026. Management guided FY27 revenue toward INR1,440–1,450 crores, assuming Bhopal’s resumption and contributions from the UP plant. Cost pressures from input inflation persisted, but the company focused on cost optimization and premiumization. The balance sheet remained stable, with gross debt rising modestly to INR211 crores. Management also addressed investor concerns about regulatory compliance, market share recovery, and operational timelines, reiterating confidence in resolving the Bhopal license issue and restoring market share in Madhya Pradesh within six months. The tone emphasized operational recovery and strategic investments despite short-term setbacks.

**tone_note**

Management acknowledged significant challenges in FY26, including operational disruptions and revenue declines, but also highlighted strategic progress (e.g., UP plant launch) and guided toward revenue recovery in FY27.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Mixed` |
| tone_label — Qwen | `Mixed` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ✅ yes |
| Lexical overlap | 0.2654 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 61.1248 s |
| Input / output tokens | 12521 / 396 |
| Tokens/sec (output) | 6.5 |

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

### Case 12 — `CC_PNB_106702450`

#### SOURCE / EVIDENCE

- **Symbol:** PNB
- **Company:** Punjab National Bank
- **Filing id:** 106702450
- **Doc type:** concall_transcript
- **Doc kind:** investor presentation

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
E] r>nb
J(Z1p S?
Amrit Mahotsav
'B
pab one
#JunOweftpp
...the name you can BANK upon!
Share Department, Board & Coordination Division, Head Office Plot No.4 Sector IO, Dwarka,
New Delhi-llO075, 
E-mail: hQ sa@lpnb,benk,in
Scrip Code: PNB
National Stock Exchange of India Limited
“Exchange Plaza'
Bandra – Kurla Complex, Bandra (E)
Mumbai – 400 051
Scrip Code: 532461
BSE Limited
1 st Floor, Phiroze Jeejeebhoy Towers
DalaI Street
Mumbai – 400 001
Date: 18.07.2026
Dear Sir (s),
Reg.: Analyst Presentation on Unaudited (Reviewed) Financial Results for the
Quarter ended on 30th June, 2026
Pursuant to Regulation 30 read with Clause 15 of Para A of Part A of Schedule III of
the SEBI (LODR) Regulations, 2015, please find enclosed Analyst Presentation on the
Unaudited (Reviewed) Financial Results of the Bank for the quarter ended 30th June,
2026
The same is also available at https://pnb.bank.in/financials-current.html.
You are requested to take the above on record.
Thanking you,
(Bikramjit Shorn)
Company Secretary
Enclosed: As above
dana a9aa 
avm punjab national bank
g gm aT=fm: @fed.4, M!-lo, 
atol. q{feHt-110075
Head Office: Plot No. 4, Sector - 10, Dwarka. New Delhi 110075 India
pnb. bank.in
T: 01 1 28075000, 28045000
E
(f)Oai)@)©)pnbindia @) www.pnb.bank.in
dana anS:Irg;! y•
punjab?asI::!9£Akcjro\\
BIKRAMJIT 
SHOM
Digitally signed by BIKRAMJIT SHOM 
DN: st=West Bengal, 
serialNumber=6f2651546fb6d9dcaa692694280f1d0198
f3f1283652a85f10889a45fae593e8, 
postalCode=700039, o=Personal, c=

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

The investor presentation by Punjab National Bank (PNB) detailed the unaudited financial results for the quarter ended June 30, 2026. Management reported a net profit of ₹5,253 crore, reflecting a year-on-year increase of 213.6%. The bank's return on assets (ROA) was 1.04%, and the gross non-performing assets (GNPA) ratio improved to 2.78%, down 100 basis points from the previous year. Global business reached ₹29,97,970 crore, growing 10.2% year-on-year. The presentation highlighted strong credit growth, particularly in retail and MSME sectors, and emphasized the bank's digital transformation initiatives. Management noted challenges from geopolitical uncertainties and inflationary pressures but expressed confidence in the bank's resilience and growth potential. The document also outlined the bank's commitment to environmental, social, and governance (ESG) initiatives, showcasing various awards and recognitions received.

**tone_note**

Management highlighted significant growth in profitability and business metrics.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'targeting'
- pass 2: forward-tense word 'targets'
- pass 3: forward-tense word 'targets'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ❌ no — failed validation after 3 attempts |
| Attempts used | 3 |
| Compliance — **Qwen** | ❌ FAIL — empty text |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Positive` |
| tone_label — Qwen | `None` |
| tone_label valid (closed set) | ❌ |
| tone_label agrees | — |
| Lexical overlap | 0.0 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 206.1848 s |
| Input / output tokens | 65975 / 1251 |
| Tokens/sec (output) | 6.1 |

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

### Case 13 — `CC_MANYAVAR_106711176`

#### SOURCE / EVIDENCE

- **Symbol:** MANYAVAR
- **Company:** Vedant Fashions Limited
- **Filing id:** 106711176
- **Doc type:** concall_transcript
- **Doc kind:** investor presentation

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
Vedant Fashions Limited  
Registered Office: 19, Canal South Road, Paridhan Garment Park, SDF-1. 4th Floor, A501-A502, Kolkata: 700015, Phone: +91 3361255353 
Email: info@vedantfashions.com | Website: www.vedantfashions.com | CIN: L51311WB2002PLC094677 
 
 
July 25, 2026 
 
 
To,  
National Stock Exchange of India Limited 
Exchange Plaza, 5th Floor, Plot No. C-1, 
Bandra Kurla Complex, Bandra (E), 
Mumbai – 400051 
 
To,  
BSE Limited 
 
 
 
 
Phiroze Jeejeebhoy Towers 
 
 
Dalal Street, Fort, 
Mumbai – 400001 
NSE Symbol: MANYAVAR 
 
BSE Scrip Code: 543463 
 
Madam / Sir, 
 
Sub : 
Submission of Investor Presentation–July 2026 | Vedant Fashions Limited (the ‘Company’) 
Ref : 
Disclosure under Regulation 30 of the Securities and Exchange Board of India (Listing 
Obligations and Disclosure Requirements) Regulations, 2015, as amended (“Listing 
Regulations”) 
Pursuant to Regulation 30 read with Schedule III of the Listing Regulations, please find enclosed a copy of 
‘Investor Presentation – July 2026’ issued in connection with the Unaudited Financial Results of Vedant 
Fashions Limited (“the Company”) for the quarter ended on June 30, 2026. 
 
The aforesaid Investor Presentation is also being made available on the Company’s website 
(www.vedantfashions.com). 
 
We request you to kindly take the aforesaid information on record and disseminate the same on your 
respective websites. 
 
Thank you. 
 
 
For, Vedant Fashions Limited 
 
 
 
_____________________ 
Navin Pareek  
Compan

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

Vedant Fashions Limited submitted an investor presentation on July 25, 2026, detailing its performance for the quarter ended June 30, 2026. The presentation highlighted a 3.4% increase in retail sales and a 7.2% growth in revenue from operations compared to the same quarter in the previous year. The company reported a gross margin of 65.7% and a profit after tax (PAT) growth of 14.7%, achieving a PAT margin of 26.7%. Vedant Fashions emphasized its market leadership in Indian wedding and celebration wear, with a diversified brand portfolio and a strong omni-channel presence. The company also noted its unique business model, which includes no end-of-season sales for its Manyavar brand. The presentation outlined key investment highlights, including a disciplined approach to acquisitions and a focus on technology-driven supply chain management.

**tone_note**

The presentation emphasized growth and strong financial performance.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**tone_label:** `Positive`

**summary**

The July 2026 investor presentation by Vedant Fashions Limited (MANYAVAR) highlighted its position as the largest company in India’s men’s Indian wedding and celebration wear market by revenue, OPBDIT, and PAT, with a diversified brand portfolio including Manyavar, Mohey, Twamev, and Diwas. The company reported Q1 FY27 revenue growth of +7.2% YoY, with a gross margin of 65.7% and PAT growth of +14.7% YoY, achieving a PAT margin of 26.7%. Domestic same-store sales growth (SSSG) rose by +3.8% YoY. The presentation emphasized a franchisee-led, asset-light EBO model, uniform pricing across channels, and a 52-week design collection model. Key strengths included a tech-driven supply chain, emotional marketing campaigns (e.g., ‘Made for Each Other’), and a pan-India omni-channel presence of 501 EBOs across 205 cities. The company also noted a disciplined approach to acquisitions and expansion, both domestically and internationally. Historical milestones included surpassing INR 2,000 crore in retail sales and strategic acquisitions like Mebaz. The presentation underscored industry-leading margins, return metrics, and cash generation, alongside awards for marketing excellence and supply chain management. Financial data showed consistent growth in revenue, EBITDA, and PAT over FY22–FY26, with gross margins stabilizing around 65–67% and PAT margins improving to 26.7% in Q1 FY27.

**tone_note**

The document emphasized strong financial performance, leadership in market share, and strategic growth initiatives without discussing risks or challenges.

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'forecasting'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 2 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Positive` |
| tone_label — Qwen | `Positive` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ✅ yes |
| Lexical overlap | 0.3034 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 46.2243 s |
| Input / output tokens | 15918 / 699 |
| Tokens/sec (output) | 15.1 |

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

### Case 14 — `CC_GOCOLORS_106717019`

#### SOURCE / EVIDENCE

- **Symbol:** GOCOLORS
- **Company:** Go Fashion (India) Limited
- **Filing id:** 106717019
- **Doc type:** concall_transcript
- **Doc kind:** investor presentation

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
July 30, 2026 
 
BSE Limited 
Scrip Code: 543401 
National Stock Exchange of India Ltd. 
Trading Symbol: GOCOLORS 
 
Dear Sir/Madam, 
 
Sub: Investor Presentation for Q1 FY 2027 - Regulation 30 of SEBI (Listing Obligations and 
Disclosure Requirements) Regulations, 2015. 
 
With reference to the above captioned subject, please find enclosed Investor Presentation for Q1 FY 27. 
 
The aforesaid Investor Presentation is also being disseminated on company’s website at 
https://www.gocolors.com/investor-relations. 
 
This is for your information and record. 
 
Thanking You, 
For Go Fashion (India) Limited 
 
 
 
 
Gayathri Kethar 
Company Secretary & Compliance Officer 
 
 
 
 
GAYATHR
I KETHAR
Digitally signed by 
GAYATHRI KETHAR 
Date: 2026.07.30 
13:53:47 +05'30'

Investor Presentation
July 2026

Go Fashion (India) Limited
This presentation has been prepared by and is the sole responsibility of Go Fashion (India) Limited (the “Company”). By accessing this presentation, you are 
agreeing to be bound by the trailing restrictions. 
This presentation does not constitute or form part of any offer or invitation or inducement to sell or issue, or any solicitation of any offer or recommendation to 
purchase or subscribe for, any securities of the Company, nor shall it or any part of it or the fact of its distribution form the basis of, or be relied on in connection 
with, any contract or commitment thereof. In particular, this presentation is not intended to be a prospectus or offer do

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Neutral`

**summary**

The investor presentation for Q1 FY 2027 by Go Fashion (India) Limited reported a revenue from operations of Rs. 161 crores, reflecting a 2% year-over-year increase. Gross profit also rose by 2% to Rs. 50 crores, while profit after tax increased by 4% to Rs. 8 crores. However, EBITDA before exceptional items decreased by 2% to Rs. 67 crores, with EBITDA margins at 30.3%, down 70 basis points from the previous year. The presentation highlighted a strategic focus on expanding retail space, with 7,016 sq. ft. added during the quarter, despite the closure of 66 stores. The company emphasized its commitment to enhancing product relevance and customer experience through larger exclusive brand outlets (EBOs) and a diversified product portfolio. Management noted that the bottom-wear segment is evolving, with a significant shift towards value-added products contributing to approximately 70% of revenues.

**tone_note**

The presentation provided a balanced overview of financial performance and strategic initiatives without strong emphasis on growth or challenges.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**tone_label:** `Mixed`

**summary**

The Q1 FY2027 investor presentation for Go Fashion (India) Limited reported **revenue of Rs. 161 crores** (+2% YoY), with **gross profit of Rs. 50 crores** (+2% YoY) and **PAT of Rs. 8 crores** (+4% YoY). Key highlights included a **54% YoY decline in revenue from MBO & Others**, a **62.9% gross profit margin** (down 10 bps YoY), and a **30.3% EBITDA margin** (down 70 bps YoY), attributed to higher marketing spend (2.3% of revenue vs. 1.5% in Q1 FY26). The company reported an **exceptional expense of Rs. 6.5 crores** due to store closures (66 stores shut) as part of its strategy to optimize the store network. **Same Store Sales Growth (SSSG) was +0.6%**, while **Same Cluster Sales Growth (SCSG) was flat at Rs. 223 crores (0% YoY)**. The company emphasized its **expansion of larger EBO stores (700+ sq. ft.)**, adding **43,283 sq. ft. of retail space** in FY26 (11% YoY growth), with a focus on Tier 2 and Tier 3 cities. The presentation also highlighted a **shift in product mix**, with **~70% of revenues now from value-added bottom wear** (up from 38% in FY19). The company’s **online sales were Rs. 25.3 crores in FY26 (3% of total sales)**, and it plans to strengthen digital engagement. Management noted **strong unit economics**, with an **average payback period of 15-18 months for EBO stores** and **94% of EBO sales at full price**. The company’s **RoCE (pre-Ind AS 116) was 10.8%**, and **RoE was 7.9%**, with **cash and cash equivalents at Rs. 202 crores** (including mutual funds and FDs). The presentation concluded with a focus on **expanding the retail network, growing online sales, leveraging technology for cost efficiency, and capitalizing on the branded women’s bottom wear market’s growth (CAGR of 18%)**.

**tone_note**

The document balanced growth initiatives (expansion of EBO stores, product diversification, and digital focus) with challenges (declining EBITDA margins, store closures, and flat SCSG).

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Neutral` |
| tone_label — Qwen | `Mixed` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ❌ no |
| Lexical overlap | 0.2152 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 59.5902 s |
| Input / output tokens | 10764 / 608 |
| Tokens/sec (output) | 10.2 |

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

### Case 15 — `CC_UNIMECH_106722740`

#### SOURCE / EVIDENCE

- **Symbol:** UNIMECH
- **Company:** Unimech Aerospace and Manufacturing Limited
- **Filing id:** 106722740
- **Doc type:** concall_transcript
- **Doc kind:** investor presentation

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
August 03, 2026 
To,  
National Stock Exchange of India Ltd. 
Symbol: UNIMECH 
BSE Limited 
Scrip Code: 544322 
 
Sub: 
Intimation of Investor Presentation 
Dear Sir/Ma’am, 
In continuation to our letter dated July 29, 2026, pursuant to Regulation 30 of the SEBI (Listing 
Obligations and Disclosure Requirements) Regulations, 2015, we hereby enclose the copy of 
Earnings Presentation on un-audited Financial Results of the Company for the quarter ended June 
30, 2026, which is being placed on the Company’s website, for the Earnings Conference Call 
scheduled on Tuesday, August 04, 2026. 
 
Thanking You,  
Yours Faithfully,  
 
For Unimech Aerospace and Manufacturing Limited 
 
 
Rashmi Gupta 
Company Secretary & Compliance Officer 
M. No: A25382 
 
 
Encl: Annexure-A 
 
RASHMI 
GUPTA
Digitally signed by 
RASHMI GUPTA 
Date: 2026.08.03 
19:24:02 +05'30'

Unimech Aerospace 
and Manufacturing Limited
Investor Presentation
Q1 FY27 – August 2026

Disclaimer
This presentation and the accompanying slides (the “Presentation”), which has been prepared by Unimech Aerospace and Manufacturing Ltd (the “Company”), 
have been prepared solely for information purposes and do not constitute any offer, recommendation or invitation to purchase or subscribe for any securities, 
and shall not form the basis or be relied on in connection with any contract or binding commitment whatsoever. No offering of securities of the Company shall be 
made except by means of a statutory offering document contain

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

The investor presentation from Unimech Aerospace and Manufacturing Limited reported that the company achieved its highest-ever quarterly revenue of ₹1,076.2 million for Q1 FY27, reflecting a 71% year-over-year increase. EBITDA also saw significant growth, rising 98% to ₹392.5 million, with an EBITDA margin of 36.5%. The presentation highlighted the successful integration of Hobel Bellows and the signing of a long-term supply agreement with FACC, a Tier-1 aerospace supplier. Management emphasized a focus on qualification-led growth, aiming to increase qualifications for flying parts and precision manufacturing programs. The total order book as of June 30, 2026, stood at ₹2,803 million, with a healthy order pipeline and expanding customer relationships. The document outlined strategic investments and operational improvements as key drivers for future growth.

**tone_note**

Management highlighted strong financial performance and strategic growth initiatives.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**tone_label:** `Positive`

**summary**

Unimech Aerospace and Manufacturing Limited’s investor presentation for **Q1 FY27 (ended June 30, 2026)** reported record quarterly revenue of **₹1,076.2 million** (up **71% YoY**), driven by strong demand in aerospace, semiconductor, and energy sectors. The company highlighted **EBITDA growth of 98% YoY (₹392.5 million)** and **PAT growth of 46% YoY (₹278.6 million)**, alongside improved EBITDA margins (36.5% vs. 31.4% YoY). Key operational milestones included the completion of Hobel Bellows acquisition (consolidated from May 2026), a **long-term supply agreement with FACC (aerospace Tier-1 supplier)**, and an **RFQ from a semiconductor equipment OEM**. The order book stood at **₹2,803 million** as of June 30, 2026, with contributions from aerospace, nuclear, and semiconductor sectors. Management emphasized **qualification-led growth**, strategic acquisitions, and capacity expansion as drivers for FY27, with a focus on transitioning qualification programs into serial production. The presentation also detailed the company’s **global precision engineering platform**, including **5 manufacturing facilities (563,000 sq. ft.)**, **6,300+ qualified SKUs**, and **96% export revenue**. Historical financials showed **revenue CAGR of 60.4% (FY22-FY26)** and a diversified customer base across **41 global OEMs/Tier-1s** in aerospace, defense, nuclear, and industrial sectors. The document underscored **strategic investments** (e.g., Saudi JV, Hobel Bellows) and **long-term customer engagements** as pillars for sustained growth.

**tone_note**

Management emphasized record revenue, margin expansion, and strategic growth initiatives while highlighting strong order visibility and sectoral diversification.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Positive` |
| tone_label — Qwen | `Positive` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ✅ yes |
| Lexical overlap | 0.3507 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 38.9347 s |
| Input / output tokens | 8384 / 459 |
| Tokens/sec (output) | 11.8 |

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

### Case 16 — `CC_RATEGAIN_106728376`

#### SOURCE / EVIDENCE

- **Symbol:** RATEGAIN
- **Company:** Rategain Travel Technologies Limited
- **Filing id:** 106728376
- **Doc type:** concall_transcript
- **Doc kind:** investor presentation

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
Corporate Office Address: Plot No. 3,4,5, Club 125, Tower A, 4th Floor 
Sector – 125 Noida – 201301, Uttar Pradesh India 
Registered Office Address: M-140, Greater Kailash, Part-II, Delhi-110048 
Tel: +91 120 5057000 
CIN: L72900DL2012PLC244966 
Website: www.rategain.com 
E-mail: help@rategain.com 
 
 
August 06, 2026 
 
To, 
National Stock Exchange of India Limited 
(NSE: RATEGAIN) 
 
BSE Limited 
(BSE: 543417) 
 
Subject: Investor Presentation on the Un-Audited (Standalone and Consolidated) Financial 
Results of the Company for the Quarter ended June 30, 2026 
 
Dear Sir/Ma’am, 
 
Pursuant to Regulation 30 of SEBI (Listing Obligations and Disclosure Requirements) 
Regulations, 2015, please find enclosed herewith Investor Presentation on Un-Audited 
(Standalone and Consolidated) Financial Results of the Company for the Quarter ended June 30, 
2026. 
 
Please take the above information on record.  
 
Yours faithfully, 
 
For RATEGAIN TRAVEL TECHNOLOGIES LIMITED 
 
 
Mukesh Kumar 
General Counsel,  
Company Secretary & Compliance Officer 
Membership No.: A17925 
 
Encl.: As above 
 
 
 
 
 
Mukesh 
Kumar
Digitally signed by 
Mukesh Kumar 
Date: 2026.08.06 
13:34:15 +05'30'

Investor 
Presentation
Q1 FY2027

Safe Harbor
This presentation and the accompanying slides (the “Presentation”), which have been prepared by 
Rate Gain Travel Technologies 
Limited (the “Company”), have been prepared solely for information purposes and do not constitute any offer, recommendation o
r 
invit

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

The investor presentation by RateGain Travel Technologies Limited detailed the company's un-audited financial results for the quarter ended June 30, 2026. Management reported a significant year-on-year operating revenue growth of 187.6%, with adjusted EBITDA increasing by 289.3% and adjusted PAT rising by 148.8%. The presentation highlighted a diversified revenue stream across various offerings and geographies, with a strong focus on operational excellence and integration following the Sojern acquisition. Key partnerships were noted, including collaborations with Philippine Airlines and Duetto. The company emphasized its vision of leveraging AI to enhance guest acquisition, retention, and revenue expansion. Management also discussed the integration of AI into their products and operations, aiming to optimize pricing and improve customer engagement. The presentation concluded with a focus on continuous product innovation and strategic investments to drive future growth.

**tone_note**

Management emphasized strong growth and operational efficiency.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**tone_label:** `Positive`

**summary**

The investor presentation for **Rategain Travel Technologies Limited** (Q1 FY2027) highlighted **strong year-over-year growth** in operating revenue (187.6%), adjusted EBITDA (289.3%), and adjusted PAT (148.8%), driven by the integration of **Sojern** and diversified revenue streams across **hospitality, DMOs, OTAs, and airlines**. Management emphasized **AI-driven product innovation**, including **Agentic ARI** (for real-time revenue optimization), **RateIQ** (to detect revenue leaks), and **RG Pay** (a unified payment infrastructure), which contributed to a **24.6% adjusted EBITDA margin** and **14.9% adjusted PAT margin**. The company reported **healthy revenue retention (95.6% GRR, 106.8% NRR)** and a **14.1x LTV-to-CAC ratio**, alongside a **47.3% YoY increase in employee headcount** and **95.3% YoY revenue growth per employee**. Key partnerships (e.g., **Philippine Airlines, Duetto, Cinko**) and awards (e.g., **Best in SaaS for AI-Powered Travel Marketing**) were noted. The presentation also detailed **operational efficiency**, with **free cash flow conversion at 78.8%** and a **net debt of INR 615.4 Cr** against **INR 664 Cr in net cash equivalents**. Management guided toward **sustained financial discipline** while scaling AI-driven solutions and geographic expansion, particularly in **North America (82.4% of revenue)** and **Asia Pacific**.

**tone_note**

Management explicitly framed the quarter as one of **strong growth, operational health, and strategic momentum**, repeatedly emphasizing **record revenue, margin expansion, and AI-driven innovation** as key achievements.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Positive` |
| tone_label — Qwen | `Positive` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ✅ yes |
| Lexical overlap | 0.2847 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 41.3132 s |
| Input / output tokens | 9082 / 424 |
| Tokens/sec (output) | 10.3 |

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

### Case 17 — `CC_EMAMILTD_106734041`

#### SOURCE / EVIDENCE

- **Symbol:** EMAMILTD
- **Company:** Emami Limited
- **Filing id:** 106734041
- **Doc type:** concall_transcript
- **Doc kind:** earnings concall transcript

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
10th August, 2026 
 
The Manager – Listing 
National Stock Exchange of India Ltd. 
Exchange Plaza, Plot No. C/1, Block – G 
Bandra Kurla Complex, Bandra (E) 
Mumbai – 400 051 
Scrip Code: EMAMILTD 
The Manager – Listing 
BSE Limited 
Phiroze Jeejeebhoy Towers 
Dalal Street 
 
 
 
 
Mumbai – 400 001 
 
   
     
Scrip Code: 531162 
 
Sub: Transcript of Investor’s Conference Call of the Company for Q1 FY 27 – Financial Results 
Dear Sir/ Madam, 
Pursuant to Regulation 30 of the SEBI (Listing Obligations and Disclosure Requirements) 
Regulations, 2015, please find enclosed herewith the transcript of the Conference Call with 
Analysts / Investors held on 4th August, 2026, post declaration of the Unaudited Financial 
Results (Standalone & Consolidated) for the quarter ended 30th June, 2026.  
The said transcript is also available on the Company’s website at www.emamiltd.in.  
This is for your information and record. 
Thanking you, 
Yours faithfully, 
For Emami Limited 
 
 
 
 
Ravi Varma 
Company Secretary & Compliance Officer 
Membership No: F9531 
 
(Encl: As above) 
Ravi 
Varma
Digitally signed 
by Ravi Varma 
Date: 2026.08.10 
11:39:46 +05'30'

Page 1 of 12 
 
 
“Emami Limited 
Q1 FY27 Earnings Conference Call” 
August 04, 2026 
  
 
 
 
 
MANAGEMENT: MR. MOHAN GOENKA – WHOLE-TIME DIRECTOR 
AND VICE CHAIRMAN – EMAMI LIMITED 
 
MR. VIVEK DHIR – CHIEF EXECUTIVE OFFICER – 
INTERNATIONAL BUSINESS – EMAMI LIMITED 
 
MR. DHRUV AGGARWAL – CHIEF GROWTH 
OFFICER – EMAMI LIMITED 
 
MR. 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Mixed`

**summary**

During the Q1 FY27 earnings conference call, management reported a consolidated revenue growth of 15% to INR 1,039 crores, with domestic business growing by 20%. The company transitioned to category-wise reporting to reflect its diversified portfolio. Key categories included Hair and Scalp care, which grew by 11%, and Skin Care, which saw a 3% increase. The strategic investment portfolio grew by 61%, contributing 18% to domestic business. However, international business declined by 12% due to geopolitical disruptions. Despite inflationary pressures impacting profitability, EBITDA grew by 6% to INR 226 crores. Management highlighted ongoing initiatives to enhance supply chain efficiency and sales productivity. They expressed optimism about growth prospects, supported by strong core brand performance and digital-first initiatives. The effective tax rate normalized to around 25-26%. Overall, management emphasized resilience and a commitment to maintaining margins amid cost pressures.

**tone_note**

The tone reflected both positive growth in certain segments and challenges in profitability and international business.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'expects'
- pass 2: forward-tense word 'targeting'
- pass 3: forward-tense word 'expectations'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ❌ no — failed validation after 3 attempts |
| Attempts used | 3 |
| Compliance — **Qwen** | ❌ FAIL — empty text |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Mixed` |
| tone_label — Qwen | `None` |
| tone_label valid (closed set) | ❌ |
| tone_label agrees | — |
| Lexical overlap | 0.0 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 96.7645 s |
| Input / output tokens | 30479 / 1530 |
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

### Case 18 — `CC_JNKINDIA_106738190`

#### SOURCE / EVIDENCE

- **Symbol:** JNKINDIA
- **Company:** JNK India Limited
- **Filing id:** 106738190
- **Doc type:** concall_transcript
- **Doc kind:** investor presentation

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
JNK India Limited 
(Formerly known as JNK India Private Limited) 
CIN: L29268MH2010PLC204223 
 
203 to 206, Centrum, Plot No. C-3, S.G. Barve Road, Wagle Estate,  
Thane (W) – 400604, Maharashtra, INDIA Tel : 91-22-68858000 
Email: admin@jnkindia.com Website: www.jnkindia.com 
 
  Date: August 11, 2026 
To,  
BSE Limited, 
The General Manager,  
Department of Listing Operations,  
Phiroze Jeejeebhoy Towers,  
Dalal Street, Mumbai – 400 001 
To,  
National Stock Exchange of India Limited, 
The Manager, Listing Department, 
Exchange Plaza, C-1, Block-G,  
Bandra Kurla Complex, Bandra (East), 
Mumbai – 400 051 
Scrip code: 544167 
Security Symbol: JNKINDIA 
 
Dear Sir/Madam, 
Sub.: Q1FY27 Investor Presentation 
 
Pursuant to Regulation 30 of the SEBI (Listing Obligations and Disclosure Requirements) 
Regulations, 2015, we enclose herewith a copy of Q1FY27 Investor Presentation. 
 
We request you to take note of the same. 
 
Thanking you, 
Yours faithfully, 
For JNK India Limited 
 
 
Ashish Soni 
Company Secretary and Compliance Officer 
 
Encl: a/a 
ASHIS
H SONI
Digitally signed 
by ASHISH SONI 
Date: 
2026.08.11 
23:50:07 +05'30'

INVESTOR PRESENTATION
Q1FY27
Results
August 2026  
Engineering 
Excellence,
Delivered.
JNK India Ltd. · NSE: JNKINDIA · BSE: 544220

2
Safe Harbor
This presentation and the accompanying slides (the “Presentation”), which have been prepared by JNK India Limited (the “Company”), have been prepared solely for information 
purposes and do not constitute 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

JNK India Limited reported a strong start to FY27, with total income increasing by over 80.6% year-on-year to Rs. 186.0 crore in Q1FY27, compared to Rs. 103.0 crore in Q1FY26. EBITDA grew 3.1 times to Rs. 21.9 crore, while profit after tax (PAT) surged 8.5 times to Rs. 9.6 crore. The company maintained an EBITDA margin of 11.8%. As of June 30, 2026, the order book stood at Rs. 1,801 crore, with a bidding pipeline of approximately Rs. 6,000 crore. Management highlighted plans to diversify into offshore, metals & minerals, and renewable energy sectors, with JNK Chemdist contributing to the renewable energy segment through a green hydrogen project. The presentation emphasized the company's focus on executing existing projects and expanding into new markets and segments.

**tone_note**

Management highlighted strong financial growth and strategic expansion initiatives.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**tone_label:** `Positive`

**summary**

The Q1FY27 investor presentation reported strong year-over-year financial growth for JNK India Limited. Management stated total income rose **80.6%** YoY to **Rs. 186.0 cr**, with EBITDA increasing **3.1x** to **Rs. 21.9 cr** and PAT growing **8.5x** to **Rs. 9.6 cr**. The presentation highlighted an **EBITDA margin of 11.8%** and an **order book of Rs. 1,801 cr** as of June 30, 2026, alongside a **Rs. 6,000 cr bidding pipeline** split equally between domestic and export markets. Management also noted diversification efforts into **renewable energy, off-shore projects, and metals & minerals**, with JNK Chemdist contributing **Rs. 16.5 cr** in revenue—new to the consolidated income. The document emphasized **execution discipline, global collaboration with JNK Global, and strategic JV with Chemdist** for technology-led growth. A single **Rs. 624 cr export order cancellation** (no execution commenced) was cited as an isolated incident due to technical approval delays. The standalone P&L showed **gross profit growth of 42.8%** YoY but a **negative PAT of Rs. 0.8 cr** due to higher taxes and lower EBITDA margins (5.6% vs. 6.9% YoY). Management’s commentary focused on **sustaining growth, expanding into new sectors, and leveraging existing capabilities** while maintaining margin stability.

**tone_note**

Management emphasized strong YoY financial growth, a robust order pipeline, and strategic diversification into high-growth sectors like renewable energy.

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'targeting'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 2 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Positive` |
| tone_label — Qwen | `Positive` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ✅ yes |
| Lexical overlap | 0.3387 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 40.4853 s |
| Input / output tokens | 12564 / 768 |
| Tokens/sec (output) | 19.0 |

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

### Case 19 — `CC_FINOPB_106742828`

#### SOURCE / EVIDENCE

- **Symbol:** FINOPB
- **Company:** Fino Payments Bank Limited
- **Filing id:** 106742828
- **Doc type:** concall_transcript
- **Doc kind:** investor presentation

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
Fino Payments Bank Limited 
Registered Office: Mindspace Juinagar, Plot No Gen 2/1/F, Tower 1, 8th Floor, TTC Industrial Area, MIDC Shirwane, Juinagar, Navi Mumbai  
- 400 706 | CIN: L65100MH2007PLC171959 | Tel: (+91 22) 7104 7000 | Website: www.fino.bank.in | Email: cs@fino.bank.in  
 
August 13, 2026 
 
BSE Limited 
P.J. Towers, 
Dalal Street,  
Mumbai- 400 001 
 
(Scrip Code: 543386) 
National Stock Exchange of India Limited 
Exchange Plaza, 5th Floor, Plot No. C/1, G 
Block, Bandra - Kurla Complex,  
Bandra (E), Mumbai - 400 051 
 
(Symbol: FINOPB) 
 
Dear Sir/Madam, 
 
Sub: Investor Presentation under Regulation 30 of the Securities and Exchange Board of 
India (Listing Obligations and Disclosure Requirements) Regulations, 2015 (“SEBI 
Listing Regulations”)  
 
Pursuant to Regulation 30 of SEBI Listing Regulations, enclosed herewith the Investor 
Presentation on Un-audited Financial Results for the first quarter ended June 30, 2026 of Fino 
Payments Bank Limited (“Bank”). 
  
The said presentation will also available on the Bank’s website i.e. www.fino.bank.in  
 
Kindly take the same on record. 
 
Thanking You 
 
Yours faithfully, 
For Fino Payments Bank Limited 
 
 
 
Basavraj Loni 
Company Secretary & Compliance Officer 
 
Place: Navi Mumbai 
 
 
Encl: a/a 
 
Basavraj 
Shivanand Loni
Digitally signed by 
Basavraj Shivanand Loni 
Date: 2026.08.13 
19:30:54 +05'30'

On Our Journey to Become a 
Small Finance Bank
Investor Pre se n tation 
Q1 FY’ 27

Table of Content
Key 

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

Fino Payments Bank Limited's investor presentation for Q1 FY'27 highlighted several key business updates and financial metrics. Management reported the highest quarterly net revenue margin of 42.8%, driven by increased contributions from the CASA business segment. The average total deposits rose by 12% year-over-year to ₹2,772 crores, and digitally active users grew by 22% to 64.6 lakh. Loan referral disbursements surged 214% year-over-year, totaling ₹628 crores. The bank's preparations for transitioning to a Small Finance Bank (SFB) are on track, with key systems identified and a consultant engaged for the transition. Financial highlights included a revenue of ₹306.9 crores, a 32% increase, and an EBITDA of ₹43.1 crores, reflecting a 30% growth. The presentation also noted a net loss of ₹13.7 crores for the quarter. Overall, the document provided a comprehensive overview of the bank's performance and strategic direction.

**tone_note**

Management emphasized growth in key financial metrics and strategic initiatives.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

**tone_label:** `Mixed`

**summary**

Fino Payments Bank’s Q1 FY’27 investor presentation highlighted strong growth in key metrics. Net revenue margin rose to **42.8%** (up **925 bps YoY**), driven by a **54% CASA contribution** to revenue (vs. 34% YoY prior). Deposits grew **12% YoY** to ₹2,772 crore, while digitally active users surged **22% YoY** to 64.6 lakh, with FinoPay users expanding **38% YoY** to 8.4 lakh. Loan referral disbursals jumped **214% YoY** to ₹628 crore (~50% of FY’26 total). Digital throughput reached ₹63.4k crore (7% YoY growth), with UPI volumes at ₹60.1k crore (14% YoY). However, **PAT turned negative at ₹13.7 crore** due to higher other financial costs and depreciation, despite **EBITDA of ₹43.1 crore** (30% YoY decline). Operational efficiency improved, with throughput per employee rising to ₹179.4 crore (annualized). The bank emphasized **SFB transition readiness**, with LOS/LMS identified and RBI submission planned for Q4’27. Geographical expansion continued, with merchant adoption rising across states like Maharashtra, Karnataka, and Uttar Pradesh. The presentation underscored a **liability-first strategy** and digital ecosystem growth, though near-term headwinds included revenue compression and cost pressures.

**tone_note**

Management emphasized record margins and digital growth while acknowledging revenue compression and a negative PAT due to cost pressures.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Positive` |
| tone_label — Qwen | `Mixed` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ❌ no |
| Lexical overlap | 0.2394 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 28.4282 s |
| Input / output tokens | 6665 / 395 |
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

### Case 20 — `CC_KIRIINDUS_106747935`

#### SOURCE / EVIDENCE

- **Symbol:** KIRIINDUS
- **Company:** Kiri Industries Limited
- **Filing id:** 106747935
- **Doc type:** concall_transcript
- **Doc kind:** earnings concall transcript

<details><summary>Evidence supplied to the model (first 1,500 chars)</summary>

```
CIN No.: L24231GJ1998PLC034094 
 
Date: August 18, 2026 
 
To,
BSE Limited 
Phiroze Jeejeebhoy Towers,  
Dalal Street, Mumbai- 400 001 
Scrip Code: 532967 
To,
National Stock Exchange of India Limited 
Exchange Plaza, Bandra Kurla Complex, 
Bandra (E), Mumbai - 400 051 
Scrip ID - KIRIINDUS 
 
Dear Sir/Madam, 
 
Sub: Submission of Transcript for Q1-FY27 Earnings Conference call 
 
In compliance with Regulation 30 of SEBI (Listing Obligations and Disclosure Requirements) 
Regulations, 2015, please find attached herewith the Transcript of Q1-FY27 Earnings Conference 
Call held on Thursday, August 13, 2026 at 10:30 A.M. 
 
The Transcript of Q1-FY27 Earnings Conference Call is also available on website of the Company 
at www.kiriindustries.com. 
 
You are kindly requested to take note of the same. 
 
Thanking You, 
 
Yours faithfully, 
 
For Kiri Industries Limited 
 
 
 
Suresh Gondalia 
Company Secretary 
M No. : F7306 
Encl: As stated 
 
GONDALIA 
SURESH 
SAVAJIBHAI
Digitally signed by GONDALIA SURESH SAVAJIBHAI 
DN: c=IN, postalCode=380015, st=GUJARAT, street=21, 
BHAVI APARTMENT, ,156 NEHRU 
PARK, ,AHMADABAD,VASTRAPUR ,380015, l=AHMADABAD, 
o=Personal, 
serialNumber=61ef2e945d9b4545361118485ed828d8e6a1
7a5394d0cc83c0083d7fae6378bf, 
pseudonym=df3fa15041844632b83c6e37da8b7e34, 
2.5.4.20=2ffb8407a32dbc76dc1756ccf827b5ded85b5aad6
7c9ece0e2e2eb8303f03eca, 
email=SURESH.GONDALIA@KIRIINDUSTRIES.COM, 
cn=GONDALIA SURESH SAVAJIBHAI 
Date: 2026.08.18 10:36:36 +05'30'

 
 
Page 1 of 1

… truncated for review; full text is in the fixture …
```

</details>

- **Reference pipeline:** `concall_front_slice` · model `gpt-4o-mini` · prompt `concall_summarizer@8bb3170`
- **Recorded limitations:**
  - None material: concall_summarizer.py has NOT been rewired through Evidence Finder, so the code path that produced this reference is the code path that exists today. The input is exactly reproducible and this is a like-for-like comparison.

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

Kiri Industries Limited held its Q1 FY27 Earnings Conference Call on August 13, 2026, where management provided updates on their integrated copper and fertilizer project, which has moved into the construction phase. Management reported that orders for long-lead packages have been placed and highlighted the project's alignment with their long-term growth strategy. The operating environment for the dyes and chemicals business improved, with a 63% year-on-year revenue growth to INR 295 crore, driven by better pricing and operational efficiency. Standalone EBITDA was reported at INR 17 crore, while consolidated revenue reached INR 312 crore, marking a 55% increase. Management noted that the company remains focused on maintaining a prudent capital structure and executing projects efficiently. The discussion also addressed shareholder concerns regarding dividends, with management emphasizing the need to reinvest profits for growth. The call concluded with management expressing optimism about future performance and project timelines.

**tone_note**

Management emphasized strong performance and growth potential in their projects.

#### NEW — QWEN OUTPUT (`ministral3-14b-w4a16-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'expected'
- pass 2: forward-tense word 'targeted'
- pass 3: forward-tense word 'expected'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ❌ no — failed validation after 3 attempts |
| Attempts used | 3 |
| Compliance — **Qwen** | ❌ FAIL — empty text |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Positive` |
| tone_label — Qwen | `None` |
| tone_label valid (closed set) | ❌ |
| tone_label agrees | — |
| Lexical overlap | 0.0 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 129.1917 s |
| Input / output tokens | 40859 / 1548 |
| Tokens/sec (output) | 12.0 |

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
