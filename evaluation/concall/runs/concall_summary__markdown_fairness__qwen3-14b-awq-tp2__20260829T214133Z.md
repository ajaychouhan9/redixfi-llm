# Review sheet — concall_summary

> **EXPERIMENTAL / NOT PRODUCTION.** This file is evidence for a human to review, not a verdict. No quality score is computed anywhere in it, and no LLM judge was used. The candidate model is NOT declared better or worse than gpt-4o-mini by this tooling.

## Run configuration

| | |
|---|---|
| Model | `qwen3-14b-awq-tp2` |
| Backend | `vllm-inprocess` |
| Sampling | temperature=0.0, max_tokens=1024, seed=0 |
| Fixture | `/kaggle/input/datasets/ajaychouhan9/redixfi-llm-evaluation-2026/concall_benchmark.json` |
| Cases | 20 of 20 |
| Run id | `20260829T214133Z` (2026-08-29T21:41:33.031544+00:00) |
| LLM project commit | `None` |
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
| mean_latency_sec | 60.504 |
| total_prompt_tokens | 308008 |
| total_completion_tokens | 11037 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| tone_label_agreement_rate | 0.8 |
| invalid_tone_labels | 0 |
| tone_confusion | Mixed->Mixed=2, Positive->Positive=6, Positive->None=3, Neutral->Neutral=4, Mixed->Neutral=1, Mixed->None=2, Mixed->Positive=1, Positive->Mixed=1 |
| mean_lexical_overlap | 0.2434 |

## Cases

---

### Case 1 — `CC_BATAINDIA_106539458`

#### SOURCE / EVIDENCE

- **Symbol:** BATAINDIA
- **Company:** Bata India Limited
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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Mixed`

**summary**

Bata India Limited's earnings conference call on February 13, 2026, highlighted a turnover growth of 3% for the quarter, attributed to the implementation of a zero-based merchandising project across 400 stores and increased marketing expenditures. Management noted improvements in key metrics such as inventory freshness and turnaround times. The company reported a double-digit underlying PBT growth of 10%, with significant contributions from brands like Hush Puppies and Power. The franchise network expanded to nearly 2,000 outlets, and e-commerce sales grew, with 14% of direct-to-consumer business coming from a newly launched app. Management acknowledged challenges in achieving double-digit growth aspirations but emphasized ongoing initiatives in marketing, product development, and channel expansion to drive future growth. The discussion also touched on the impact of GST on sales and the company's strategy to enhance brand relevance among younger consumers.

**tone_note**

Management reported growth and improvements while acknowledging challenges in achieving higher growth rates.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Mixed`

**summary**

Bata India Limited's Q3 and FY '26 earnings call highlighted 3% turnover growth and double-digit EBITDA improvement, driven by zero-based merchandising (ZBM) in 400 stores, elevated marketing spend, and product innovation. Management noted stronger performance from Hush Puppies, Power, and Floatz brands, as well as improved margins from inventory rationalization and agent inventory freshness. Franchise expansion reached nearly 2,000 stores, with plans to grow further. E-commerce growth accelerated, with 14% of D2C sales via the Bata app. The MBO channel showed renewed momentum after prior challenges. Management emphasized ongoing efforts in product funnel reimagining, digital marketing shifts, and store modernization to attract younger consumers. Inventory efficiency improvements were reported, with 11% reduction in aged stock. While growth remains in single digits, management outlined strategies for future expansion and product innovation to drive momentum.

**tone_note**

The document acknowledges both progress in growth and margin improvements while noting ongoing challenges in reaching double-digit growth and addressing younger consumer recall.

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
| tone_label — reference | `Mixed` |
| tone_label — Qwen | `Mixed` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ✅ yes |
| Lexical overlap | 0.3111 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 65.6718 s |
| Input / output tokens | 21580 / 508 |
| Tokens/sec (output) | 7.7 |

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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

Sunteck Realty Limited reported its financial results for Q4 and the full year FY26, highlighting a revenue increase to approximately Rs. 339 crore in Q4FY26 and Rs. 1,124 crore for FY26, representing year-on-year growth of 65% and 32%, respectively. EBITDA also saw significant growth, reaching around Rs. 97 crore in Q4FY26 and Rs. 305 crore for FY26, up 41% and 64% YoY. The company reported a PAT of Rs. 63 crore in Q4FY26 and Rs. 202 crore for FY26, marking increases of 25% and 34% YoY. Operationally, pre-sales grew to Rs. 1,064 crore in Q4FY26 and Rs. 3,157 crore for FY26, with collections at Rs. 432 crore and Rs. 1,433 crore, respectively. The company maintained a strong net debt to equity ratio of 0.06x and reported a net cash flow surplus of Rs. 552 crore, up 48% YoY. Sunteck emphasized its strong market position and successful equity partnerships.

**tone_note**

Management highlighted strong financial and operational growth metrics.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Positive`

**summary**

Sunteck Realty Limited reported strong financial and operational performance in Q4 and FY26. Revenue grew to ~Rs. 339 cr in Q4FY26 and ~Rs. 1,124 cr in FY26, up 65% and 32% YoY respectively. EBITDA increased to ~Rs. 97 cr in Q4FY26 and ~Rs. 305 cr in FY26, up 41% and 64% YoY. PAT rose to ~Rs. 63 cr in Q4FY26 and ~Rs. 202 cr in FY26, up 25% and 34% YoY. EBITDA and PAT margins remained strong at 29% and 19% in Q4FY26. Pre-sales reached ~Rs. 1,064 cr in Q4FY26 and ~Rs. 3,157 cr in FY26, up 22% and 25% YoY. Collections stood at ~Rs. 432 cr in Q4FY26 and ~Rs. 1,433 cr in FY26, up 39% and 14% YoY. The company reported a net cash flow surplus of ~Rs. 552 cr, up 48% YoY. The net debt-to-equity ratio was 0.06x. Key strengths include a strong foothold in the Mumbai Metropolitan Region (MMR), well-timed capital allocation with acquisitions of ~50 mn sq ft and GDV of ~Rs. 41,030 cr, an expanding annuity income portfolio with ~Rs. 300 cr in rentals and potential capital value creation of up to ~Rs. 5,000 cr, and successful equity partnerships with entities like IFC-World Bank Group, Kotak Fund, and Ajay Piramal Group. The company also highlighted its strong financial performance, AA credit rating, and ESG achievements, including a GRESB score of 99 and a 5-star rating, as well as a DJSI ESG score of 78. Green building initiatives include EDGE and LEED certifications for several projects.

**tone_note**

The document emphasizes strong financial growth, operational performance, and strategic strengths, with no significant negative factors mentioned.

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
| Lexical overlap | 0.3193 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 43.586 s |
| Input / output tokens | 7604 / 524 |
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

### Case 3 — `CC_KANPRPLA_106607445`

#### SOURCE / EVIDENCE

- **Symbol:** KANPRPLA
- **Company:** Kanpur Plastipack Limited
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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

The investor presentation by Kanpur Plastipack Limited detailed the company's financial results for the quarter and financial year ended March 31, 2026. The presentation highlighted a total income of Rs. 18,505 lakhs for Q4 FY26, reflecting a year-on-year growth of 7.26%. EBITDA for the same quarter was reported at Rs. 2,556 lakhs, with a margin of 13.81%, up from 12.28% in the previous year. Net profit increased by 24.70% to Rs. 1,492 lakhs, with an EPS of 6.2. The company emphasized its strong export model, with approximately 70% of revenue derived from international markets, and outlined strategic initiatives for capacity expansion and diversification into technical textiles. Sustainability efforts were also highlighted, with nearly 50% of energy needs met through solar power. The presentation concluded with a focus on disciplined diversification and capital allocation.

**tone_note**

Management emphasized growth in financial performance and strategic initiatives.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'expected'
- pass 2: forward-tense word 'expected'
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
| Latency | 51.7424 s |
| Input / output tokens | 17553 / 1003 |
| Tokens/sec (output) | 19.4 |

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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Neutral`

**summary**

Coromandel International Limited announced the scheduling of a conference call to discuss its Q4FY26 results, which took place on May 8, 2026. The investor presentation related to this call was made available on the company's website, in compliance with SEBI regulations. The communication was signed by B. Shanmugasundaram, the Company Secretary and Compliance Officer, and requested acknowledgment of the submission.

**tone_note**

The document provided factual information regarding the conference call and investor presentation.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Neutral`

**summary**

The investor presentation for Coromandel International Limited's conference call discussing Q4FY26 results, scheduled for May 8, 2026 at 02:30 PM IST, has been uploaded to the company's website as required by SEBI regulations. The document confirms the submission of this presentation to the National Stock Exchange of India and BSE Limited, with the request that the submission be recorded. The presentation itself is not included in the text provided, only the notice of its availability. The company secretary, B. Shanmugasundaram, digitally signed the notice on May 8, 2026.

**tone_note**

The document provides factual information about the submission and availability of the investor presentation without expressing positive or negative sentiment.

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
| Lexical overlap | 0.3519 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 5.185 s |
| Input / output tokens | 1113 / 169 |
| Tokens/sec (output) | 32.6 |

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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Mixed`

**summary**

The earnings conference call for Alkyl Amines Chemicals Limited, held on May 6, 2026, featured management discussing the company's financial performance for Q4FY26. Management reported that both the top line and bottom line remained flat, with a slight increase in market share despite challenging market conditions. They noted that raw material prices, particularly ammonia, had risen significantly due to geopolitical factors, impacting production costs. Management indicated that while they had managed to source ammonia, the future supply chain remained uncertain. They mentioned a cautious optimism regarding potential volume growth of 5% to 10% in the upcoming year, contingent on market stability. Additionally, management highlighted ongoing projects and the potential for new product launches, while emphasizing the importance of maintaining competitive margins amidst fluctuating raw material prices. The call concluded with management expressing gratitude for investor interest and engagement.

**tone_note**

Management conveyed both challenges and cautious optimism regarding future performance.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Mixed`

**summary**

The earnings call for Alkyl Amines Chemicals Limited on May 6, 2026, discussed the company's Q4FY26 financial performance. Management noted that both revenue and profit remained flat compared to the previous year, with minor fluctuations of around 1%. The company faced challenges in sourcing ammonia, particularly in March, but managed to maintain operations through inventory. However, ongoing geopolitical tensions, such as the war affecting supply chains, remain a concern. Demand for products has not significantly declined, as customers absorb higher prices due to the relatively minor cost of the company's products in their overall expenses. Volume growth was flat, with a slight decline in both price and volume. The company is working on a new project in Kurkumbh, slightly delayed to the next quarter, but the economics remain unchanged. Management expressed cautious optimism about future growth, citing potential benefits from reduced Chinese competition and improved margins. However, uncertainties remain regarding the duration of current price levels and the impact of new competitors entering the methylamine market. The company is also exploring R&D initiatives for new products but has not yet announced specifics. Capacity utilization across plants is between 60% and 85%, and there are no major capex plans for FY27 and FY28 unless new R&D projects require it. The company is monitoring green ammonia and alternative raw material sourcing strategies for long-term stability.

**tone_note**

The summary reflects both cautious optimism about potential growth and ongoing challenges such as supply chain issues and market competition.

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
| Lexical overlap | 0.2456 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 65.8077 s |
| Input / output tokens | 11980 / 323 |
| Tokens/sec (output) | 4.9 |

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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Mixed`

**summary**

Aarti Drugs Limited's investor presentation for Q4 and FY26 highlighted a total revenue of Rs. 721.1 crore for Q4 FY26, marking a 6% year-over-year increase. EBITDA was reported at Rs. 96.6 crore, with a margin of 13.4%, reflecting a decline of 60 basis points compared to the previous year. The presentation noted that the company's profitability was affected by start-up losses from new facilities and weakness in the domestic antibiotics market. However, sequentially, revenue and EBITDA improved by 20% and 72%, respectively. The management emphasized a shift towards regulated markets, with contributions increasing from 66% in FY25 to 73% in FY26. The company also reported a strong focus on expanding its product pipeline and enhancing operational capabilities, particularly in oncology and specialty chemicals. Overall, the presentation outlined the company's strategic initiatives and resilience amid industry challenges.

**tone_note**

The presentation conveyed both positive growth in certain areas and challenges affecting profitability.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Neutral`

**summary**

Aarti Drugs Limited's Q4 and FY26 investor presentation highlights a 6% year-on-year revenue growth to Rs. 721.1 crore, with EBITDA flat at Rs. 96.6 crore and a margin decline of 60 bps to 13.4%. Sequentially, Q4 FY26 saw a 20% revenue increase and 72% EBITDA growth, driven by the Sayakha facility's operational scale-up and improved product mix. The company reported a 16% increase in PAT to Rs. 194.9 crore, with a margin improvement of 60 bps to 7.6%. The presentation noted challenges including start-up losses from new facilities and weak domestic antibiotic markets, but emphasized recovery in regulated and export markets, which now contribute 73% and 38% of revenue, respectively. The company's diversified product portfolio, regulatory approvals, and backward integration initiatives are positioned to enhance profitability and return ratios in FY27 and beyond. The balance sheet showed strong cash flow generation, with net operating cash flow of Rs. 1,549 crore and a debt-to-equity ratio of 0.44 as of March 2026. The company also outlined growth strategies, including expanding into oncology and complex generics, and completing Rs. 600 crore in capex to boost capacity and margins.

**tone_note**

The presentation provides factual financial performance and strategic initiatives without overtly positive or negative language.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Mixed` |
| tone_label — Qwen | `Neutral` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ❌ no |
| Lexical overlap | 0.2992 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 84.636 s |
| Input / output tokens | 14055 / 332 |
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

### Case 7 — `CC_INDIQUBE_106632356`

#### SOURCE / EVIDENCE

- **Symbol:** INDIQUBE
- **Company:** Indiqube Spaces Limited
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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

Indiqube Spaces Limited reported a record financial performance for FY26, with total income reaching ₹1,491 crore, a year-on-year growth of 37%. The company achieved a profit after tax (PAT) of ₹125 crore, reflecting a significant increase of 145% compared to the previous year. Management highlighted the resilience of their business model amid geopolitical volatility and AI-related uncertainties. The company expanded its presence to 17 cities, operating 130 properties with over 9.66 million square feet of office space, maintaining a steady occupancy rate of 88%. The earnings presentation outlined a disciplined expansion strategy, with a focus on enhancing client value and operational efficiency. Key highlights included the addition of 28,000 seats and a growing contribution from value-added services, which accounted for 15% of total revenue. The management expressed confidence in the long-term growth potential of their workspace platform.

**tone_note**

The document emphasized strong financial growth and operational resilience.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Positive`

**summary**

Indiqube Spaces Limited's investor presentation for FY26 highlights strong financial performance, with total income of ₹1,491 crore, a 37% YoY revenue growth, and a 145% increase in PAT to ₹125 crore. EBITDA margins improved to 21%, and operating cashflows reached ₹304 crore. The company expanded to 17 cities, managing 9.66 million sq.ft. of office space with 88% steady-state occupancy. Key operational highlights include adding 28,000 seats and strengthening its presence in PAN India. The presentation also details IGAAP-equivalent financials, emphasizing profitability and resilience amid geopolitical and AI-related uncertainties. Management emphasized disciplined expansion, operational strength, and long-term growth opportunities. The document addresses investor questions on lease liabilities, lock-in periods with landlords, and the impact of Ind AS accounting adjustments on financials.

**tone_note**

The tone_label is Positive as the document emphasizes strong financial growth, improved margins, and operational resilience, with management expressing confidence in long-term opportunities.

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
| Lexical overlap | 0.3415 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 63.5106 s |
| Input / output tokens | 12229 / 240 |
| Tokens/sec (output) | 3.8 |

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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Neutral`

**summary**

TVS Electronics Limited's investor presentation for Q4-FY26 reported a revenue from operations of INR 1,174 million, reflecting a 2.4% year-over-year increase and a 3.3% quarter-over-quarter increase. The Customer Support Services segment generated revenue of INR 370 million in Q4-FY26, up 10.4% year-over-year, while the Products and Solutions Group reported INR 804 million, a slight decrease of 0.9% year-over-year. The overall FY26 revenue reached INR 4,552 million, marking a 5.7% increase from FY25. EBITDA for Q4-FY26 was INR 70 million, with an EBITDA margin of 5.96%, showing significant improvement from the previous year. The presentation highlighted strategic priorities, including enhancing tech products and strengthening supply chain capabilities. The company also emphasized its commitment to local manufacturing under the 'Make in India' initiative. The document concluded with a focus on integrated solutions for various sectors, including retail and logistics.

**tone_note**

The presentation provided a balanced overview of financial performance and strategic initiatives without strong emphasis on growth or challenges.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Neutral`

**summary**

TVS Electronics Limited's Q4-FY26 earnings presentation highlights revenue growth across its business segments. The Products and Solutions Group generated INR 804 Mn in Q4-FY26, a 2.3% increase from Q3-FY26 and 3.0% year-over-year. Customer Support Services revenue rose to INR 370 Mn in Q4-FY26, up 5.7% from Q3-FY26 and 12.7% year-over-year. Total revenue for Q4-FY26 was INR 1,174 Mn, reflecting a 3.3% quarter-over-quarter increase and 2.4% year-over-year growth. For FY26, total revenue reached INR 4,552 Mn, up 5.7% year-over-year. EBITDA for Q4-FY26 was INR 70 Mn with a margin of 5.96%, up 24 basis points from Q3-FY26 and 413 basis points from Q4-FY25. FY26 EBITDA was INR 195 Mn, with a margin of 4.28%, up 172 basis points from FY25. The company reported a net profit of INR 13 Mn for FY26, compared to a net loss of INR 39 Mn in FY25. Operational highlights include expansion of manufacturing capabilities, strategic partnerships, and focus on local value addition through 'Make in India' initiatives. The balance sheet shows an increase in total liabilities to INR 1,866 Mn in FY26, while total assets grew to INR 2,825 Mn. The company emphasized improving product mix and cost management initiatives as key drivers of margin improvement.

**tone_note**

The document presents factual financial and operational data without overtly positive or negative language.

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
| Lexical overlap | 0.3578 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 31.6832 s |
| Input / output tokens | 6264 / 423 |
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

### Case 9 — `CC_KUANTUM_106643553`

#### SOURCE / EVIDENCE

- **Symbol:** KUANTUM
- **Company:** Kuantum Papers Limited
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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Neutral`

**summary**

Kuantum Papers Limited's investor presentation for the quarter and financial year ended March 31, 2026, detailed the company's operational and financial performance. The presentation reported a total operational income of INR 10,932 million for FY26, a slight decrease from INR 11,070 million in FY25. EBITDA margins fell to 14.80% from 21.92% in the previous year, attributed to increased costs and a drop in net selling rates. For Q4 FY26, operational income was INR 3,009 million, with EBITDA margins improving to 15.89% from 13.55% in Q3 FY26. The company highlighted its strategic initiatives, including plant upgrades and sustainability efforts, such as expanding its Social Farm Forestry Program. Kuantum's product portfolio includes a variety of paper types, and it has increased its export footprint to 24 countries. The presentation also outlined future growth strategies focused on capacity expansion and technological advancements.

**tone_note**

The presentation provided a balanced overview of financial performance and strategic initiatives without strong emphasis on positive or negative aspects.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Neutral`

**summary**

The investor presentation for Kuantum Papers Limited for Q4-FY26 outlines the company's operational and financial performance. Operational income for FY26 was INR 10,932 Mn, a slight decline from FY25, but the company maintained a production volume of 162,885 MT despite strategic shutdowns for upgrades. EBITDA margins fell to 14.8% from 21.9% in FY25 due to lower net sales realization (NSR) and increased costs. For Q4-FY26, operational income rose to INR 3,009 Mn, with EBITDA margins improving to 15.9% despite market challenges. The company highlighted mill expansion projects, including upgrades to Paper Machine 2 and the Two-stage Recausticizing Plant, as well as new technology implementations under Project Nirmaan. Sustainability initiatives include expanding Social Farm Forestry to 18,300+ acres. Financially, FY26 saw a significant drop in PAT to INR 420 Mn from INR 1,152 Mn in FY25, with PAT margins declining to 3.84%. The company also noted increased net debt and a lower net worth. The presentation included forward-looking statements about future growth strategies, including leveraging single-use plastic bans and exploring Industry 4.0 technologies, but emphasized that these are subject to risks and uncertainties. The company's share price as of March 31, 2026, was INR 66.1, with a market cap of INR 5,767.3 Mn.

**tone_note**

The presentation provides factual data and acknowledges both operational challenges and strategic initiatives without overtly positive or negative language.

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
| Lexical overlap | 0.3116 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 39.944 s |
| Input / output tokens | 8004 / 386 |
| Tokens/sec (output) | 9.7 |

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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Mixed`

**summary**

The investor presentation for Q4 FY 2025-26 from Sigachi Industries Limited outlined the company's operational and financial highlights, emphasizing a year of resilience and strategic growth. Management reported that the Dahej-2 capacity expansion is on schedule, aiming to elevate total MCC capacity to 30,000 MTPA. The presentation highlighted a global customer base of over 500 across 65 countries and noted a 19.92% revenue CAGR over five years. Financially, the company reported a revenue of Rs. 1,219 million for Q4 FY26, a 4.01% increase QoQ, but a 4.91% decrease YoY. EBITDA margin was reported at 12.63%, down from 22.31% YoY. Management set a goal for FY27 to achieve revenue between Rs. 6,500 - 6,750 million and an EBITDA margin of 18% - 20%. The presentation also emphasized the company's commitment to sustainability and community engagement through CSR initiatives.

**tone_note**

The presentation highlighted both challenges and strategic growth initiatives.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

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
| Compliance — **Qwen** | ❌ FAIL — empty text |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Mixed` |
| tone_label — Qwen | `None` |
| tone_label valid (closed set) | ❌ |
| tone_label agrees | — |
| Lexical overlap | 0.0 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 60.7888 s |
| Input / output tokens | 22819 / 940 |
| Tokens/sec (output) | 15.5 |

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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Mixed`

**summary**

During the earnings conference call held on June 2, 2026, management reported that Som Distilleries & Breweries Limited faced a challenging fiscal year 2026, with consolidated revenue declining by 14.8% to INR 1,233 crores, impacted by operational disruptions and subdued demand in key markets. Beer volumes decreased by 20%, while the Indian Made Foreign Liquor (IMFL) segment grew by 32%. Management noted ongoing inflationary pressures affecting input costs and margins. Despite these challenges, the company maintained healthy operating cash flows and continued investments in a greenfield brewery project in Uttar Pradesh, which is on schedule. Management set a goal of achieving revenue between INR 1,400 crores and INR 1,500 crores for FY 2027, contingent on the resolution of licensing issues at the Bhopal facility. The call concluded with management expressing confidence in recovering market share and improving operational performance in the upcoming quarters.

**tone_note**

Management highlighted both challenges and opportunities for recovery in the business.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'expected'
- pass 2: forward-tense word 'expected'
- pass 3: forward-tense word 'expected'

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
| Latency | 98.1569 s |
| Input / output tokens | 34453 / 1037 |
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

### Case 12 — `CC_PNB_106702450`

#### SOURCE / EVIDENCE

- **Symbol:** PNB
- **Company:** Punjab National Bank
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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

The investor presentation by Punjab National Bank (PNB) detailed the unaudited financial results for the quarter ended June 30, 2026. Management reported a net profit of ₹5,253 crore, reflecting a year-on-year increase of 213.6%. The bank's return on assets (ROA) was 1.04%, and the gross non-performing assets (GNPA) ratio improved to 2.78%, down 100 basis points from the previous year. Global business reached ₹29,97,970 crore, growing 10.2% year-on-year. The presentation highlighted strong credit growth, particularly in retail and MSME sectors, and emphasized the bank's digital transformation initiatives. Management noted challenges from geopolitical uncertainties and inflationary pressures but expressed confidence in the bank's resilience and growth potential. The document also outlined the bank's commitment to environmental, social, and governance (ESG) initiatives, showcasing various awards and recognitions received.

**tone_note**

Management highlighted significant growth in profitability and business metrics.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Positive`

**summary**

Punjab National Bank (PNB) reported its unaudited financial results for the quarter ended 30 June 2026. The bank achieved a net profit of ₹5,253 crore, representing a 213.6% year-over-year (YoY) increase. Operating profit rose by 6.2% YoY to ₹7,519 crore. Return on assets (ROA) stood at 1.04%, while book value per share (tangible) increased to ₹108.58. Asset quality improved, with gross NPA at 2.78% and net NPA at 0.28%, both down YoY. The bank’s capital adequacy ratio (CRAR) was 14.52%, and CET-1 ratio reached 14.52%. Business performance included a 10.2% YoY growth in global business to ₹29,97,970 crore, with global deposits and advances rising by 8.5% and 12.7% YoY, respectively. Digital initiatives showed progress, with PNB One activated users reaching 365 lakh and digital transactions hitting ₹357 crore. The bank also highlighted ESG efforts, including green financing and sustainability initiatives. Guidance for FY27 included credit growth of 12-13% and deposit growth of 9-10%, though actuals for June 2026 showed deposit growth at 8.5% and credit growth at 12.7%.

**tone_note**

The document emphasizes strong financial performance, improved asset quality, and progress in digital and ESG initiatives.

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
| Lexical overlap | 0.2846 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 167.797 s |
| Input / output tokens | 21052 / 369 |
| Tokens/sec (output) | 2.2 |

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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

Vedant Fashions Limited submitted an investor presentation on July 25, 2026, detailing its performance for the quarter ended June 30, 2026. The presentation highlighted a 3.4% increase in retail sales and a 7.2% growth in revenue from operations compared to the same quarter in the previous year. The company reported a gross margin of 65.7% and a profit after tax (PAT) growth of 14.7%, achieving a PAT margin of 26.7%. Vedant Fashions emphasized its market leadership in Indian wedding and celebration wear, with a diversified brand portfolio and a strong omni-channel presence. The company also noted its unique business model, which includes no end-of-season sales for its Manyavar brand. The presentation outlined key investment highlights, including a disciplined approach to acquisitions and a focus on technology-driven supply chain management.

**tone_note**

The presentation emphasized growth and strong financial performance.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Positive`

**summary**

Vedant Fashions Limited, through its investor presentation dated July 25, 2026, outlined its business operations and financial performance for the quarter ended June 30, 2026. The presentation highlighted the company's position as a market leader in Indian wedding and celebration wear, with a diversified brand portfolio including Manyavar, Mohey, Twamev, and Mebaz. Key financial metrics included a 3.4% growth in retail sales, a 3.8% increase in domestic same-store sales growth (SSSG), a 7.2% rise in revenue from operations, and a 14.7% year-over-year increase in profit after tax (PAT) with a strong PAT margin of 26.7%. The company emphasized its unique business model, technology-driven supply chain, and extensive retail presence across India through its exclusive brand outlets (EBOs). Strategic initiatives included up-selling, cross-selling, retail expansion, and disciplined acquisitions. The presentation also detailed the company's growth trajectory, financial summaries, and awards received over the years.

**tone_note**

The presentation emphasized strong financial performance, market leadership, and strategic growth initiatives.

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
| Lexical overlap | 0.5 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 46.1359 s |
| Input / output tokens | 14904 / 610 |
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

### Case 14 — `CC_GOCOLORS_106717019`

#### SOURCE / EVIDENCE

- **Symbol:** GOCOLORS
- **Company:** Go Fashion (India) Limited
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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Neutral`

**summary**

The investor presentation for Q1 FY 2027 by Go Fashion (India) Limited reported a revenue from operations of Rs. 161 crores, reflecting a 2% year-over-year increase. Gross profit also rose by 2% to Rs. 50 crores, while profit after tax increased by 4% to Rs. 8 crores. However, EBITDA before exceptional items decreased by 2% to Rs. 67 crores, with EBITDA margins at 30.3%, down 70 basis points from the previous year. The presentation highlighted a strategic focus on expanding retail space, with 7,016 sq. ft. added during the quarter, despite the closure of 66 stores. The company emphasized its commitment to enhancing product relevance and customer experience through larger exclusive brand outlets (EBOs) and a diversified product portfolio. Management noted that the bottom-wear segment is evolving, with a significant shift towards value-added products contributing to approximately 70% of revenues.

**tone_note**

The presentation provided a balanced overview of financial performance and strategic initiatives without strong emphasis on growth or challenges.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Neutral`

**summary**

The investor presentation for Q1 FY27 of Go Fashion (India) Limited (GOCOLORS) outlines key financial and operational highlights. Revenue from operations was Rs. 161 crores, a 2% YoY increase, while gross profit rose to Rs. 50 crores, also up 2% YoY. However, profit after tax declined to Rs. 8 crores, down 54% YoY, primarily due to a Rs. 6.5 crore exceptional expense from store closures. The company added 7,016 sq. ft. of retail space, though this was offset by the closure of 66 stores. Average selling price increased by 1.2%, and full-price sales accounted for 94% of EBO sales. The presentation notes a 14.0% EBITDA margin in Q1 FY27, down from 15.9% in Q1 FY26, attributed to higher marketing spend. The company emphasized its strategy to expand larger EBO stores, enhance online sales, leverage technology, and capitalize on the growing women’s bottom-wear market. The presentation also highlights a strong balance sheet with cash reserves of Rs. 202 crores and efficient unit economics, including a payback period of 15–18 months for EBO stores. The company aims to nearly double its retail area over the next five years to drive revenue and cost optimization.

**tone_note**

The document presents factual financial data and strategic initiatives without overtly positive or negative language.

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
| Lexical overlap | 0.2411 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 51.5234 s |
| Input / output tokens | 10049 / 337 |
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

### Case 15 — `CC_UNIMECH_106722740`

#### SOURCE / EVIDENCE

- **Symbol:** UNIMECH
- **Company:** Unimech Aerospace and Manufacturing Limited
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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

The investor presentation from Unimech Aerospace and Manufacturing Limited reported that the company achieved its highest-ever quarterly revenue of ₹1,076.2 million for Q1 FY27, reflecting a 71% year-over-year increase. EBITDA also saw significant growth, rising 98% to ₹392.5 million, with an EBITDA margin of 36.5%. The presentation highlighted the successful integration of Hobel Bellows and the signing of a long-term supply agreement with FACC, a Tier-1 aerospace supplier. Management emphasized a focus on qualification-led growth, aiming to increase qualifications for flying parts and precision manufacturing programs. The total order book as of June 30, 2026, stood at ₹2,803 million, with a healthy order pipeline and expanding customer relationships. The document outlined strategic investments and operational improvements as key drivers for future growth.

**tone_note**

Management highlighted strong financial performance and strategic growth initiatives.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Positive`

**summary**

The investor presentation for Unimech Aerospace and Manufacturing Limited (UNIMECH) for Q1 FY27 highlights strong financial performance, with revenue reaching ₹1,076.2 million, a 71% year-over-year increase, and EBITDA of ₹392.5 million, up 98% YoY. The MD noted improved customer demand, disciplined execution, and strategic investments, including the Hobel Bellows acquisition, which contributed to expanded growth platforms across aerospace, semiconductor, and energy sectors. Operational highlights include a long-term supply agreement with FACC, a completed Hobel acquisition, and an RFQ from a semiconductor equipment OEM. The order book stood at ₹2,803 million as of June 30, 2026, with significant contributions from nuclear and aerospace sectors. Financial metrics show a 46% increase in PAT and a 24.2% PAT margin. The presentation also outlines strategic initiatives, including geographic expansion, capability enhancements, and acquisitions to strengthen Unimech’s position as a global precision engineering platform. Management emphasized qualification-led growth and expanding customer relationships to drive future growth and value creation.

**tone_note**

The document emphasizes strong financial performance, strategic growth initiatives, and expanding market opportunities.

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'expects'

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
| Lexical overlap | 0.3729 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 47.1779 s |
| Input / output tokens | 15251 / 609 |
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

### Case 16 — `CC_RATEGAIN_106728376`

#### SOURCE / EVIDENCE

- **Symbol:** RATEGAIN
- **Company:** Rategain Travel Technologies Limited
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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

The investor presentation by RateGain Travel Technologies Limited detailed the company's un-audited financial results for the quarter ended June 30, 2026. Management reported a significant year-on-year operating revenue growth of 187.6%, with adjusted EBITDA increasing by 289.3% and adjusted PAT rising by 148.8%. The presentation highlighted a diversified revenue stream across various offerings and geographies, with a strong focus on operational excellence and integration following the Sojern acquisition. Key partnerships were noted, including collaborations with Philippine Airlines and Duetto. The company emphasized its vision of leveraging AI to enhance guest acquisition, retention, and revenue expansion. Management also discussed the integration of AI into their products and operations, aiming to optimize pricing and improve customer engagement. The presentation concluded with a focus on continuous product innovation and strategic investments to drive future growth.

**tone_note**

Management emphasized strong growth and operational efficiency.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Positive`

**summary**

The investor presentation for Rategain Travel Technologies Limited (RATEGAIN) for Q1 FY2027 highlights robust financial growth, with operating revenue increasing by 187.6% year-over-year to INR 785.0 crore. Adjusted EBITDA grew by 289.3% to INR 193.4 crore, and adjusted PAT rose by 148.8% to INR 116.8 crore. The company emphasized its AI-driven platform, which integrates distribution, marketing, and technology solutions for the travel and hospitality sectors. Key business updates include strong customer growth, with 14,158 customers as of Q1 FY2027, and a 47.3% increase in employee headcount. Revenue streams are diversified across subscription, transaction, and hybrid models, with 79.1% from subscription services. Strategic partnerships, product innovations like Agentic ARI and RateIQ, and operational efficiencies were highlighted. The company also noted a 95.3% increase in revenue per employee and a free cash flow conversion of 78.8%. Financial metrics show sustained profitability, with operating margins at 75.0% and EBITDA margins at 24.6%. The presentation included details on the Sojern acquisition's deferred deal consideration impact and the company's focus on AI integration, customer retention, and geographic expansion.

**tone_note**

The presentation emphasizes strong financial growth, operational efficiency, and strategic advancements in AI-driven solutions, reflecting a confident and forward-looking tone.

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
| Lexical overlap | 0.2794 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 40.7729 s |
| Input / output tokens | 8458 / 343 |
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

### Case 17 — `CC_EMAMILTD_106734041`

#### SOURCE / EVIDENCE

- **Symbol:** EMAMILTD
- **Company:** Emami Limited
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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Mixed`

**summary**

During the Q1 FY27 earnings conference call, management reported a consolidated revenue growth of 15% to INR 1,039 crores, with domestic business growing by 20%. The company transitioned to category-wise reporting to reflect its diversified portfolio. Key categories included Hair and Scalp care, which grew by 11%, and Skin Care, which saw a 3% increase. The strategic investment portfolio grew by 61%, contributing 18% to domestic business. However, international business declined by 12% due to geopolitical disruptions. Despite inflationary pressures impacting profitability, EBITDA grew by 6% to INR 226 crores. Management highlighted ongoing initiatives to enhance supply chain efficiency and sales productivity. They expressed optimism about growth prospects, supported by strong core brand performance and digital-first initiatives. The effective tax rate normalized to around 25-26%. Overall, management emphasized resilience and a commitment to maintaining margins amid cost pressures.

**tone_note**

The tone reflected both positive growth in certain segments and challenges in profitability and international business.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Positive`

**summary**

The earnings call for Emami Limited's Q1 FY27 reported consolidated revenue growth of 15% to INR1,039 crores, driven by a 20% increase in domestic business and 12% like-to-like growth. Hair and Scalp care saw 11% growth, with Navratna Cool Oil and Kesh King performing strongly. Skin Care grew by 3%, with Talc portfolio delivering high single-digit growth. Healthcare grew by 2%, with the OTC portfolio showing high teens growth and strategic investments growing 61% like-to-like, contributing 18% to domestic business. International business declined 12% due to West Asia conflicts but management noted strategies to realign operations. Inflationary pressures and cost increases impacted margins, though EBITDA grew 6% to INR226 crores and profit before tax rose 4% to INR195 crores. Strategic initiatives include supply chain improvements, AI deployment, and data analytics platforms. Management emphasized confidence in sustaining growth through diversified portfolios and cost management. The strategic investments portfolio, including Axiom and IncNut, showed strong growth but with varying margin profiles, aiming for EBITDA neutrality. Tax rate normalization to 25-26% was noted, and core business growth excluding investments was around 6%.

**tone_note**

The document highlights strong revenue growth, positive performance in key categories, and confidence in future growth despite challenges.

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'expects'

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
| Lexical overlap | 0.2887 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 58.799 s |
| Input / output tokens | 18643 / 606 |
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

### Case 18 — `CC_JNKINDIA_106738190`

#### SOURCE / EVIDENCE

- **Symbol:** JNKINDIA
- **Company:** JNK India Limited
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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

JNK India Limited reported a strong start to FY27, with total income increasing by over 80.6% year-on-year to Rs. 186.0 crore in Q1FY27, compared to Rs. 103.0 crore in Q1FY26. EBITDA grew 3.1 times to Rs. 21.9 crore, while profit after tax (PAT) surged 8.5 times to Rs. 9.6 crore. The company maintained an EBITDA margin of 11.8%. As of June 30, 2026, the order book stood at Rs. 1,801 crore, with a bidding pipeline of approximately Rs. 6,000 crore. Management highlighted plans to diversify into offshore, metals & minerals, and renewable energy sectors, with JNK Chemdist contributing to the renewable energy segment through a green hydrogen project. The presentation emphasized the company's focus on executing existing projects and expanding into new markets and segments.

**tone_note**

Management highlighted strong financial growth and strategic expansion initiatives.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'outlook'
- pass 2: forward-tense word 'outlook'
- pass 3: forward-tense word 'outlook'

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
| Latency | 47.0483 s |
| Input / output tokens | 17744 / 869 |
| Tokens/sec (output) | 18.5 |

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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

Fino Payments Bank Limited's investor presentation for Q1 FY'27 highlighted several key business updates and financial metrics. Management reported the highest quarterly net revenue margin of 42.8%, driven by increased contributions from the CASA business segment. The average total deposits rose by 12% year-over-year to ₹2,772 crores, and digitally active users grew by 22% to 64.6 lakh. Loan referral disbursements surged 214% year-over-year, totaling ₹628 crores. The bank's preparations for transitioning to a Small Finance Bank (SFB) are on track, with key systems identified and a consultant engaged for the transition. Financial highlights included a revenue of ₹306.9 crores, a 32% increase, and an EBITDA of ₹43.1 crores, reflecting a 30% growth. The presentation also noted a net loss of ₹13.7 crores for the quarter. Overall, the document provided a comprehensive overview of the bank's performance and strategic direction.

**tone_note**

Management emphasized growth in key financial metrics and strategic initiatives.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Mixed`

**summary**

The investor presentation for Fino Payments Bank Limited for Q1 FY27 highlights key business updates, financial performance, and product performance. Management reported a 42.8% net revenue margin, driven by higher contributions from the CASA business segment. Average total deposits increased by 12% YoY to ₹2,772 crores, with digitally active customers growing by 22% YoY to 64.6 lakh. Referral loan disbursements surged 214% YoY to ₹628 crores, accounting for ~50% of total referral loans disbursed in FY26. The bank is progressing with preparations to transition to a Small Finance Bank (SFB), including identifying senior leadership positions and developing internal API integrations. Financial highlights include a 32% YoY revenue growth to ₹306.9 crores, though the bank reported a net loss of ₹13.7 crores for Q1 FY27. Operational efficiency metrics show a 2.5x increase in throughput per employee. The bank's liability franchise continues to strengthen with a low-cost deposit base, and digital payment services, including UPI, saw growth in throughput and user base. The presentation also outlines the SFB timeline, with end-to-end process validation and readiness assessment planned for Q3 FY27 and submission of final readiness to the RBI by Q1 FY28.

**tone_note**

The document presents both positive financial metrics such as increased deposits and revenue margin improvements alongside challenges like a net loss and operational costs.

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
| Lexical overlap | 0.3643 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 28.6962 s |
| Input / output tokens | 6365 / 335 |
| Tokens/sec (output) | 11.7 |

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

#### OLD — GPT-4o-mini OUTPUT (production reference)

**tone_label:** `Positive`

**summary**

Kiri Industries Limited held its Q1 FY27 Earnings Conference Call on August 13, 2026, where management provided updates on their integrated copper and fertilizer project, which has moved into the construction phase. Management reported that orders for long-lead packages have been placed and highlighted the project's alignment with their long-term growth strategy. The operating environment for the dyes and chemicals business improved, with a 63% year-on-year revenue growth to INR 295 crore, driven by better pricing and operational efficiency. Standalone EBITDA was reported at INR 17 crore, while consolidated revenue reached INR 312 crore, marking a 55% increase. Management noted that the company remains focused on maintaining a prudent capital structure and executing projects efficiently. The discussion also addressed shareholder concerns regarding dividends, with management emphasizing the need to reinvest profits for growth. The call concluded with management expressing optimism about future performance and project timelines.

**tone_note**

Management emphasized strong performance and growth potential in their projects.

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'expected'
- pass 2: forward-tense word 'expected'
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
| Latency | 111.4154 s |
| Input / output tokens | 37888 / 1074 |
| Tokens/sec (output) | 9.6 |

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
