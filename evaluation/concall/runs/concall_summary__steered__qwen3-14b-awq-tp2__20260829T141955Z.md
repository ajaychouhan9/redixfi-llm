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
| Run id | `20260829T141955Z` (2026-08-29T14:19:55.946730+00:00) |
| LLM project commit | `None` |
| GPU | 2x Tesla T4 (29.12 GB total) |
| CUDA / torch / vLLM | 13.0 / 2.13.0+cu130 / None |

## Objective signals (mechanical only — no judgement)

| Metric | Value |
|---|---|
| cases | 20 |
| generated_ok | 14 |
| generation_failures | 6 |
| candidate_compliance_failures | 6 |
| reference_backstop_artifacts | 0 |
| reference_compliance_failures | 0 |
| cases_with_reference | 20 |
| structured_output_used | 20 |
| json_repair_used | 0 |
| guided_and_clean | 20 |
| guided_but_repaired | 0 |
| unguided | 0 |
| mean_latency_sec | 71.895 |
| total_prompt_tokens | 388670 |
| total_completion_tokens | 13728 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| tone_label_agreement_rate | 0.7857 |
| invalid_tone_labels | 0 |
| tone_confusion | Mixed->None=5, Positive->Positive=7, Positive->None=1, Neutral->Neutral=4, Mixed->Neutral=1, Positive->Mixed=2 |
| mean_lexical_overlap | 0.2204 |

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

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'expected'
- pass 2: forward-tense word 'forecasting'
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
| Latency | 84.8554 s |
| Input / output tokens | 34678 / 753 |
| Tokens/sec (output) | 8.9 |

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

The investor presentation for Sunteck Realty Limited's Q4 and full year FY26 results highlights strong financial performance, with revenue reaching ~Rs 339 crores in Q4FY26 and ~Rs 1,124 crores for the full year, representing 65% and 32% YoY growth respectively. EBITDA and PAT also showed significant increases, with EBITDA at ~Rs 97 crores in Q4FY26 and ~Rs 305 crores annually, up 41% and 64% YoY, while PAT reached ~Rs 63 crores in Q4FY26 and ~Rs 202 crores annually, up 25% and 34% YoY. Operational metrics include pre-sales of ~Rs 1,064 crores in Q4FY26 and ~Rs 3,157 crores annually, up 22% and 25% YoY, and collections of ~Rs 432 crores in Q4FY26 and ~Rs 1,433 crores annually, up 39% and 14% YoY. The company reported a net cash flow surplus of ~Rs 552 crores, up 48% YoY, and a net debt to equity ratio of 0.06x. Key strengths include a strong foothold in the Mumbai Metropolitan Region (MMR), well-timed capital allocation, an expanding annuity income portfolio, and successful equity partnerships. The presentation also notes the company's strong financials, including an AA long-term credit rating from India Ratings (Fitch), and highlights ESG achievements such as a GRESB score of 99 and a 5-star rating, along with LEED GOLD certification for its headquarters.

**tone_note**

The document emphasizes strong financial growth, operational performance, and strategic strengths.

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
| Lexical overlap | 0.4245 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 65.6754 s |
| Input / output tokens | 16725 / 957 |
| Tokens/sec (output) | 14.6 |

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
| Latency | 79.9446 s |
| Input / output tokens | 19896 / 1615 |
| Tokens/sec (output) | 20.2 |

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

The investor presentation for Coromandel International Limited's conference call discussing Q4FY26 results was uploaded to the company's website on May 8, 2026, as required by SEBI regulations. The call was scheduled for the same day at 2:30 PM IST. The document does not provide specific financial results, growth metrics, operational updates, or management commentary from the presentation itself, only administrative details about the disclosure process.

**tone_note**

The summary reflects the neutral administrative nature of the document, which only confirms the disclosure of the presentation without providing substantive content or directional language.

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
| Lexical overlap | 0.2632 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 4.5482 s |
| Input / output tokens | 1808 / 133 |
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
| Latency | 110.0658 s |
| Input / output tokens | 38292 / 1034 |
| Tokens/sec (output) | 9.4 |

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

Aarti Drugs Limited's Q4 and FY26 investor presentation highlights a 6% year-on-year revenue growth to Rs. 721.1 crore, with EBITDA flat at Rs. 96.6 crore and a margin decline of 60 bps to 13.4%. Sequentially, Q4 FY26 saw a 20% revenue increase and 72% EBITDA growth, driven by the Sayakha facility's operational scale-up and improved product mix. The company reported a 7% total revenue growth for FY26, with EBITDA rising 3% to Rs. 311.6 crore and PAT increasing 16% to Rs. 194.9 crore. The API segment contributed 77% of sales, with formulations and specialty chemicals growing 33% and 37% YoY, respectively. The balance sheet showed a net debt-to-equity ratio of 0.44, with strong cash flow generation and a robust asset base. Management noted challenges including pricing pressures in API segments, raw material volatility, and start-up losses from new facilities, but highlighted improved operational efficiency and a shift toward regulated and export markets. Strategic initiatives include backward integration, regulatory approvals in key markets, and expansion into oncology and formulations. The company emphasized its competitive strengths, including diversified product mix, strong R&D, and global regulatory compliance.

**tone_note**

The summary reflects a balanced presentation of financial performance, challenges, and strategic initiatives without overtly positive or negative emphasis.

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
| Lexical overlap | 0.3203 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 90.1473 s |
| Input / output tokens | 14750 / 336 |
| Tokens/sec (output) | 3.7 |

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

The investor presentation for Indiqube Spaces Limited for FY26 and Q4 highlights strong financial performance, with total income of ₹1,491 crore, PAT of ₹125 crore, and EBITDA margins at 21%. The company achieved YoY revenue growth of 37% and PAT growth of 145%, driven by disciplined expansion and operational strength. Operational highlights include 130 centers across 17 cities, 9.66 million sq.ft. of office space, and 88% steady-state occupancy. Key deals in Q4 included agreements with GCC and Japanese e-commerce clients. The company emphasized its focus on flexibility, technology, and green solutions, with a strong balance sheet and credit rating reaffirmed at 'CRISIL A+ / Stable'. The presentation also detailed accounting adjustments under Ind AS, explaining the impact on financial metrics and clarifying lease liabilities and profitability under different accounting frameworks.

**tone_note**

The document emphasizes strong financial results, operational expansion, and positive financial metrics, reflecting confidence in the company's performance.

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
| Lexical overlap | 0.2481 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 89.6763 s |
| Input / output tokens | 25986 / 627 |
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

TVS Electronics Limited's Q4-FY26 financial results show revenue of INR 1,174 Mn, representing a 3.3% quarter-over-quarter increase and a 2.4% year-over-year increase. The Products and Solutions Group generated INR 804 Mn, up 2.3% quarter-over-quarter, driven by higher volumes of existing and new products in manufacturing and logistics segments, with a 3.0% year-over-year revenue growth. The Customer Support Services segment reported INR 370 Mn, a 5.7% quarter-over-quarter increase and 12.7% year-over-year growth, attributed to higher volumes across business verticals. EBITDA for Q4-FY26 was INR 70 Mn, with a margin of 5.96%, up 24 basis points quarter-over-quarter and 413 basis points year-over-year. For FY26, total revenue reached INR 4,552 Mn, a 5.7% year-over-year increase, with EBITDA of INR 195 Mn and a margin of 4.28%, up 172 basis points from FY25. The improvement in margins was attributed to better product mix and TCM initiatives. The company reported a net profit of INR 13 Mn for FY26, with a PAT margin of 0.29%, compared to a net loss of INR 39 Mn in FY25. The balance sheet shows total liabilities of INR 1,866 Mn as of FY26, with equity at INR 959 Mn. The company emphasized strategic priorities including enhancing in-house designed technology products, strengthening manufacturing capabilities, and expanding supply chain ecosystems to meet evolving customer needs. The presentation also highlighted the company's focus on integrated hardware and software solutions, contract manufacturing services for tech partners, and its commitment to 'Make in India' initiatives.

**tone_note**

The summary presents factual financial results and operational highlights without overtly positive or negative language.

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
| Lexical overlap | 0.4083 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 35.3971 s |
| Input / output tokens | 6959 / 447 |
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

The investor presentation for Kuantum Papers Limited for Q4-FY26 and FY26 outlines the company's operational and financial performance. Operational income for FY26 was INR 10,932 million, a 1.2% decline from FY25, attributed to a drop in net sales realization (NSR) by INR 2,000/MT and increased costs by INR 3,200/MT, influenced by cheaper imports and Nil GST on the notebook segment. EBITDA for FY26 was INR 1,618 million, with EBITDA margins at 14.80%, down from 21.92% in FY25. For Q4-FY26, operational income was INR 3,009 million, up 8.5% year-on-year, with EBITDA margins improving to 15.89% from 13.55% in Q3-FY26, driven by a higher NSR of INR 3,700/MT. However, costs rose by INR 2,000/MT due to higher raw material, chemical, and fuel prices amid the West Asia war. The company reported a net profit of INR 420 million for FY26, with PAT margins at 3.84%, down from 10.41% in FY25. Diluted EPS was INR 4.81 for FY26, a 63.6% decrease from FY25. Key operational updates include the completion of Paper Machine 2 rebuild, progress on the Displacement Digester System (DDS) project, and the installation of a Syncro Sheeter. The company also added 854 acres to its Social Farm Forestry program, reaching 18,300+ acres. Financially, total liabilities increased to INR 11,706 million in FY26, with net debt to equity at 0.66x. The company's share price as of 31 March 2026 was INR 66.1, with a market cap of INR 5,767.3 million.

**tone_note**

The summary presents factual financial and operational data without overtly positive or negative language.

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
| Lexical overlap | 0.259 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 48.5974 s |
| Input / output tokens | 8699 / 512 |
| Tokens/sec (output) | 10.5 |

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

- pass 1: forward-tense word 'target'
- pass 2: forward-tense word 'targets'
- pass 3: forward-tense word 'target'

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
| Latency | 72.0535 s |
| Input / output tokens | 25157 / 1085 |
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
- pass 2: forward-tense word 'expects'
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
| Latency | 109.7424 s |
| Input / output tokens | 36754 / 1134 |
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

The investor presentation for Punjab National Bank (PNB) for the quarter ended 30th June 2026 highlights strong financial performance, with net profit of ₹5,253 crore, a 213.6% year-over-year increase. Operating profit rose to ₹7,519 crore, up 17.2% YoY, while return on assets (ROA) stood at 1.04%. The bank reported a 10.2% YoY growth in global business, with global deposits up 8.5% and global advances increasing 12.7%. Asset quality improved, with gross NPA at 2.78% and net NPA at 0.28%, down from previous periods. The CASA share was 36.7%, with domestic deposits growing 8.6% YoY. Digital initiatives showed progress, including 365 lakh PNB One activated users and 357 crore digital transactions in Q1 FY27. The bank also emphasized ESG achievements, including mobilizing ₹610 crore in green deposits during FY2025-26 and securing the Viksit Bharat Ambassador for Change Award in Climate Finance. Management set a goal of achieving net-zero emissions by 2060. The presentation also outlined guidance for FY27, including credit growth of 12-13% and a CASA share of 38%.

**tone_note**

The tone is positive due to the emphasis on strong financial growth, improved asset quality, and progress in digital and ESG initiatives.

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'target'

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
| Lexical overlap | 0.2977 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 200.3865 s |
| Input / output tokens | 43631 / 684 |
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

The investor presentation for Vedant Fashions Limited (MANYAVAR) for July 2026 outlined the company's financial performance for Q1 FY27, which ended June 30, 2026. Revenue from operations increased by 7.2% compared to Q1 FY26, while gross profit margin remained stable at 65.7%. Profit after tax (PAT) grew by 14.7% year-over-year, with a PAT margin of 26.7%. The company reported a domestic same-store sales growth (SSSG) of 3.8% for Q1 FY27. The presentation highlighted the company's extensive retail network, including 501 exclusive brand outlets (EBOs) across 205 domestic cities and towns, as well as international stores in 9 global cities. The company also emphasized its diversified brand portfolio, including Manyavar, Mohey, Twamev, and Mebaz, with management noting that each brand serves distinct segments of the Indian wedding and celebration wear market. The presentation also detailed the company's growth strategy, focusing on up-selling, cross-selling, retail expansion, and disciplined acquisitions. Additionally, it provided a historical financial summary showing consistent revenue and profit growth over the past few fiscal years.

**tone_note**

The tone of the document is positive, reflecting on strong financial performance and growth in key metrics.

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
| Lexical overlap | 0.3583 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 51.0765 s |
| Input / output tokens | 16416 / 638 |
| Tokens/sec (output) | 12.5 |

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

Go Fashion (India) Limited's Q1 FY27 investor presentation highlights revenue of Rs. 161 crores, a 2% YoY increase, with gross profit at Rs. 50 crores (2% YoY growth) and a gross margin of 62.9% (down 10 bps). Profit after tax (PAT) was Rs. 8 crores (4% YoY growth), while EBITDA stood at Rs. 67 crores (2% YoY decline). The company reported a 11% YoY drop in EBITDA margins to 30.3%. Retail space added during the quarter was 7,016 sq. ft., primarily due to the closure of 66 stores as part of store network optimization. The presentation noted a 1.2% increase in average selling price (ASP) and 94% full-price sales. Working capital days were 24.7, and cash flow from operations was Rs. 25.4 crores. The company emphasized its product portfolio evolution, with non-leggings products contributing ~70% of revenues. Strategic initiatives include expanding larger EBO stores (700+ sq. ft.) in Tier 2 and Tier 3 cities, enhancing online sales, and leveraging technology for cost efficiency. The company's historical financials show consistent revenue growth, with PAT margins fluctuating between 7.1% and 11.0% over the past five fiscal years. The presentation also outlined plans to nearly double retail area over the next five years to support revenue maximization and cost optimization.

**tone_note**

The summary presents factual reporting of financial performance, operational changes, and strategic initiatives without overtly positive or negative language.

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
| Lexical overlap | 0.3015 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 57.2716 s |
| Input / output tokens | 10744 / 378 |
| Tokens/sec (output) | 6.6 |

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

Unimech Aerospace and Manufacturing Limited reported strong Q1 FY27 results, with revenue reaching ₹1,076.2 million, a 71% year-over-year increase, and EBITDA of ₹392.5 million, up 98% YoY. EBITDA margins rose to 36.5%, up 5 percentage points YoY, while PAT reached ₹278.6 million, a 46% increase YoY. The company highlighted strategic acquisitions, including the Hobel Bellows acquisition completed in April 2026, and signed long-term agreements with FACC and a semiconductor equipment OEM. Order book momentum was strong, with a total order book of ₹2,803 million as of June 30, 2026, including a nuclear order of ₹873 million. The company emphasized qualification-led growth, aiming to increase qualifications in FY27 compared to previous years, and noted improved capacity utilization as qualification programs transition to serial production. Management expressed confidence in FY27 as a year of strong growth and value creation, supported by a healthy order pipeline and expanding customer relationships. The company also detailed its manufacturing capabilities, including five facilities, advanced CNC machining, and certifications such as AS9100 and ISO. Strategic initiatives included the acquisition of Hobel Bellows and the establishment of a joint venture in Saudi Arabia to expand its manufacturing footprint and access new markets. The company’s financials showed revenue growth over FY23-FY26, though ROCE and ROE declined in FY26, reflecting increased capital expenditures and debt.

**tone_note**

The document emphasizes strong revenue and EBITDA growth, strategic acquisitions, and confidence in future growth, reflecting a positive tone.

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
| Lexical overlap | 0.2905 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 40.339 s |
| Input / output tokens | 8310 / 377 |
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

The investor presentation for Q1 FY2027 reports robust revenue growth, with operating revenue increasing by 187.6% year-over-year to INR 785.0 crores. Adjusted EBITDA grew by 289.3% to INR 193.4 crores, and adjusted PAT rose by 148.8% to INR 116.8 crores. The company highlighted strong operating margins, with EBITDA margins at 24.6% and gross margins at 75.0%. Revenue was diversified across subscription, transaction, and hybrid models, with subscription contributing 79.1% of total revenue. The customer base expanded to 14,158, with 1,261 added through the Sojern acquisition. Key growth drivers included AI-powered innovations in distribution, DaaS, and MarTech, along with strategic partnerships. The company emphasized operational efficiency, with free cash flow conversion at 78.8% and a 47.3% increase in employee headcount. Management noted sustained financial health, with net cash and equivalents at INR 255.6 crores and a net debt of INR 615.4 crores. The presentation also outlined future focus areas, including AI integration, geographic expansion, and inorganic growth opportunities.

**tone_note**

The document emphasizes strong financial performance, growth in key metrics, and confidence in future AI-driven innovations and strategic initiatives.

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
| Lexical overlap | 0.2652 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 43.6403 s |
| Input / output tokens | 9153 / 329 |
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
| Latency | 92.0861 s |
| Input / output tokens | 30294 / 1201 |
| Tokens/sec (output) | 13.0 |

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

**tone_label:** `Positive`

**summary**

In Q1FY27, JNK India Limited reported a significant increase in Total Income, growing by 80.6% YoY to Rs. 186.0 crores, compared to Rs. 103.0 crores in Q1FY26. This growth was driven by the inclusion of Rs. 16.5 crores from JNK Chemdist Limited, which was not part of the previous year's revenue. EBITDA increased by 3.1x YoY to Rs. 21.9 crores, and Profit After Tax (PAT) surged by 8.5x YoY to Rs. 9.6 crores. The company maintained an EBITDA margin of 11.8%, reflecting strong project execution and stable margin management. The order book as of June 30, 2026, stood at Rs. 1,801 crores, with a robust bidding pipeline of approximately Rs. 6,000 crores across domestic and international markets. Management highlighted diversification into offshore, metals & minerals, and renewable energy sectors, with JNK Chemdist actively pursuing green hydrogen projects. The company emphasized its focus on executing existing projects, converting the strong opportunity pipeline into new orders, and expanding into newer markets and segments. The presentation also noted a large export order cancellation due to technical approval issues, though it was an isolated incident with no material costs incurred. The company's strategic joint venture with Chemdist aims to enhance technology capabilities and expand into renewable energy, with JNK Renewable Energy Private Limited building capabilities in clean energy infrastructure. The company's fabrication infrastructure in Mundra, Gujarat, supports export-oriented fabrication and modularization, with a strategic location near a deep draft port for efficient logistics and global project delivery. The board of directors includes individuals with extensive experience in the capital equipment, oil and gas, and petrochemical industries, along with independent directors with expertise in finance and governance.

**tone_note**

The presentation highlights strong financial performance, significant revenue growth, and positive strategic initiatives, indicating a positive tone.

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
| Lexical overlap | 0.3595 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 33.2261 s |
| Input / output tokens | 6595 / 445 |
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

The investor presentation for Fino Payments Bank Limited for Q1 FY27 highlights several key developments. Revenue for the quarter reached ₹306.9 crores, reflecting a 32% year-over-year (YoY) increase, driven by higher contributions from the CASA business segment. The net revenue margin improved significantly to 42.8%, up 925 basis points YoY. Average total deposits rose by 12% YoY to ₹2,772 crores, supported by a 22% YoY growth in digitally active customers, reaching 64.6 lakh users. Referral loan disbursements surged 214% YoY to ₹628 crores, with approximately 50% of FY26's referral loans disbursed in Q1 FY27. The bank is progressing on its Small Finance Bank (SFB) transition, with end-to-end process validation and readiness assessments underway, and senior leadership positions identified. Operational efficiency was maintained, with throughput per employee increasing to ₹179.4 crores annually. The cost of funds remained low at 1.4%, contributing to a robust liability franchise. The bank also reported a 14% YoY increase in UPI P2M throughput to ₹60.063 crores and a 38% YoY growth in FinoPay users to 8.4 lakh. However, the bank reported a net loss of ₹13.7 crores for the quarter, indicating ongoing challenges despite the positive growth metrics.

**tone_note**

The summary reflects both positive growth metrics and a net loss for the quarter.

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
| Lexical overlap | 0.3798 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 32.1757 s |
| Input / output tokens | 7060 / 355 |
| Tokens/sec (output) | 11.0 |

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

**tone_label:** `Mixed`

**summary**

Kiri Industries Limited reported Q1 FY27 results with standalone revenue of INR 295 crore, a 63% YoY increase, driven by improved pricing in dyes, intermediates, and basic chemicals. Standalone EBITDA was INR 17 crore (5.86% margin), while consolidated revenue reached INR 312 crore (55% YoY growth). Other income of INR 286 crore, primarily from treasury activities, boosted profit after tax to INR 270 crore. The integrated copper and fertilizer project advanced from design to construction, with key infrastructure like the captive jetty and power systems progressing. Copper tube plant commissioning is planned for Q1 FY28, followed by the rod plant in FY28 and refinery in Q3 FY29. Management emphasized disciplined execution of the project, with phased downstream operations. In the existing chemical business, improved pricing and margin management drove a standalone material margin of 31.9%, up from 23.5% in Q1 FY26. The company noted ongoing input cost pressures but highlighted strong demand for H-acid and Vinyl Sulphone. Management discussed challenges in securing long-term copper concentrate supply and ongoing legal disputes affecting the MCB Copper-Gold project. The company remains focused on capital deployment for growth, with no dividend declared yet, and is exploring equity financing options for the copper project.

**tone_note**

The summary reflects both positive operational progress and ongoing challenges such as legal disputes and input cost pressures.

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'expected'

</details>

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 2 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Positive` |
| tone_label — Qwen | `Mixed` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ❌ no |
| Lexical overlap | 0.2313 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 96.9991 s |
| Input / output tokens | 26763 / 688 |
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

## Overall reviewer verdict

Fill this in only AFTER completing the per-case tables above.

- **Verdict (ACCEPTABLE / NOT ACCEPTABLE / INCONCLUSIVE):** ______
- **If NOT ACCEPTABLE — the specific failure mode:** ______
- **If INCONCLUSIVE — what additional cases would settle it:** ______
- **Reviewer:** ______   **Date:** ______

This was a small sample. It cannot establish production-readiness regardless of how good the outputs look.
