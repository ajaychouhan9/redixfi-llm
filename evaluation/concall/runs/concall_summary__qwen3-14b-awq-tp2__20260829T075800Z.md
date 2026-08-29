# Review sheet — concall_summary

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
| Fixture | `/kaggle/input/datasets/ajaychouhan9/redixfi-llm-fixtures/concall_benchmark.json` |
| Cases | 20 of 20 |
| Run id | `20260829T075800Z` (2026-08-29T07:58:00.178905+00:00) |
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
| mean_latency_sec | 58.488 |
| total_prompt_tokens | 308184 |
| total_completion_tokens | 10248 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| tone_label_agreement_rate | 0.7333 |
| invalid_tone_labels | 0 |
| tone_confusion | Mixed->Neutral=2, Positive->Positive=5, Positive->None=4, Neutral->Neutral=4, Mixed->Mixed=2, Mixed->None=1, Mixed->Positive=1, Positive->Mixed=1 |
| mean_lexical_overlap | 0.2333 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Neutral`

**summary**

Bata India Limited reported 3% turnover growth in Q3 FY26, driven by elevated marketing spend and the zero-based merchandising (ZBM) project, which now operates in 400 stores. Key metrics showed double-digit margin growth, with improvements in inventory freshness and store resupply efficiency. The company noted strong performance from Hush Puppies, Power, and Floatz brands, while the MBO channel showed renewed growth after prior challenges. Franchise expansion is nearing 2,000 stores, and e-commerce growth accelerated, with 14% of D2C sales through the Bata app. Management emphasized ongoing initiatives like product funnel reimagining, inventory optimization, and digital marketing shifts to social influencers. Concerns were raised about younger consumer recall and inventory sustainability, but management highlighted structural improvements and long-term growth strategies. The discussion concluded with no forward-looking guidance provided.

**tone_note**

The summary presents factual outcomes and management statements without overtly positive or negative language.

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
| Lexical overlap | 0.3358 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 50.6854 s |
| Input / output tokens | 10707 / 218 |
| Tokens/sec (output) | 4.3 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Positive`

**summary**

Sunteck Realty Limited's Q4 and full year FY26 investor presentation highlights strong financial and operational performance. Revenue grew to ~Rs. 339 cr in Q4FY26 and ~Rs. 1,124 cr in FY26, up 65% and 32% YoY respectively. EBITDA increased to ~Rs. 97 cr in Q4FY26 and ~Rs. 305 cr in FY26, up 41% and 64% YoY. PAT rose to ~Rs. 63 cr in Q4FY26 and ~Rs. 202 cr in FY26, up 25% and 34% YoY. EBITDA and PAT margins remained strong at 29% and 19% in Q4FY26. Pre-sales reached ~Rs. 1,064 cr in Q4FY26 and ~Rs. 3,157 cr in FY26, up 22% and 25% YoY. Collections stood at ~Rs. 432 cr in Q4FY26 and ~Rs. 1,433 cr in FY26, up 39% and 14% YoY. The company reported a net cash flow surplus of ~Rs 552 cr, up 48% YoY, and a net debt-to-equity ratio of 0.06x. Key strengths include a strong foothold in the Mumbai Metropolitan Region (MMR), well-timed capital allocation with acquisitions of ~50 mn sq ft and GDV of ~Rs 41,030 cr, an expanding annuity income portfolio with ~Rs 300 cr+ in rentals and potential capital value creation of up to ~Rs 5,000 cr, and successful equity partnerships with entities like IFC-World Bank Group, Kotak Fund, and Ajay Piramal Group. The company also emphasized its strong financial performance, AA credit rating from India Ratings (Fitch), and sustainability achievements, including a GRESB score of 99 and a 5-star rating, as well as a DJSI ESG score of 78. The presentation also detailed project-specific financials, balance sheet details, and ESG initiatives.

**tone_note**

The document emphasizes strong financial growth, operational performance, and strategic strengths, indicating a positive tone.

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
| Lexical overlap | 0.328 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 42.6775 s |
| Input / output tokens | 7532 / 534 |
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
| Latency | 52.7926 s |
| Input / output tokens | 17337 / 1064 |
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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Neutral`

**summary**

The investor presentation for Coromandel International Limited's conference call discussing Q4FY26 results, scheduled for May 8, 2026 at 02:30 PM IST, has been uploaded to the company's website as required by SEBI regulations. The document confirms the submission of this presentation to the National Stock Exchange of India and BSE Limited, with the request that the submission be recorded. The presentation itself is not included in the text provided, only the notice of its availability and the compliance filing.

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
| Lexical overlap | 0.3148 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 4.4395 s |
| Input / output tokens | 1041 / 146 |
| Tokens/sec (output) | 32.9 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Mixed`

**summary**

The earnings call for Alkyl Amines Chemicals Limited on May 6, 2026, discussed the company's Q4FY26 financial performance. Management noted that both revenue and profit remained flat compared to the previous year, with minor fluctuations of around 1%. The company faced challenges in sourcing ammonia, particularly in March, but managed to maintain operations through inventory. However, ongoing geopolitical tensions, such as the war affecting supply chains, remain a concern. Demand for products has not significantly declined, as customers absorb higher prices due to the relatively minor cost of the company's products in their overall expenses. Volume growth was flat, with a slight decline in both price and volume. The company is working on a new project in Kurkumbh, slightly delayed to the next quarter, but the economics remain unchanged. Management expressed cautious optimism about future growth, citing potential benefits from reduced Chinese competition and improved margins. However, uncertainties remain regarding the duration of current price levels and the impact of new competitors entering the methylamine market. The company is also exploring R&D initiatives for new products but has not yet announced specifics. Overall, the company is navigating a challenging environment with a focus on maintaining market share and managing supply chain disruptions.

**tone_note**

The tone is mixed as the document acknowledges both challenges and cautious optimism, highlighting uncertainties and potential benefits.

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
| Lexical overlap | 0.2675 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 62.6835 s |
| Input / output tokens | 11908 / 288 |
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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Neutral`

**summary**

Aarti Drugs Limited's Q4 and FY26 investor presentation highlights a 6% year-on-year revenue growth to Rs. 721.1 crore, with EBITDA flat at Rs. 96.6 crore and a margin decline of 60 bps to 13.4%. Sequentially, Q4 FY26 saw a 20% revenue increase and 72% EBITDA growth, driven by the Sayakha facility's operational scale-up and improved product mix. The company reported a 16% increase in PAT to Rs. 194.9 crore, with a margin improvement of 60 bps to 7.6%. The presentation details a diversified business with API contributing 77% of sales, supported by strong regulatory approvals and a focus on regulated and export markets. Strategic initiatives include backward integration, capacity expansion, and R&D investments, with plans to enhance margin resilience and profitability. The balance sheet shows strong cash flow generation, with net operating cash flow of Rs. 1,549 crore and a debt-to-equity ratio of 0.44. The company emphasizes its leadership in API manufacturing, global regulatory compliance, and expansion into formulations and oncology products.

**tone_note**

The presentation provides factual financial and operational updates without overtly positive or negative language.

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
| Lexical overlap | 0.2397 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 80.6515 s |
| Input / output tokens | 13983 / 292 |
| Tokens/sec (output) | 3.6 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Positive`

**summary**

Indiqube Spaces Limited's investor presentation for FY26 highlights strong financial performance, with total income of ₹1,491 crore, a 37% YoY revenue growth, and a 145% increase in PAT to ₹125 crore. EBITDA margins improved to 21%, and operating cashflows reached ₹304 crore. The company expanded to 17 cities, managing 9.66 million sq.ft. of office space with 88% steady-state occupancy. Key operational highlights include adding 28,000 seats and strengthening its presence in PAN India. The presentation also details IGAAP-equivalent financials, emphasizing profitability and resilience amid geopolitical and AI-related uncertainties. Management emphasized disciplined expansion, operational strength, and long-term growth opportunities. The document addresses investor questions on lease liabilities, lock-in periods with landlords, and the impact of Ind AS accounting adjustments on financials.

**tone_note**

The document emphasizes strong financial growth, operational expansion, and resilience amid challenges, with management expressing confidence in long-term opportunities.

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
| Latency | 61.926 s |
| Input / output tokens | 12157 / 235 |
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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Neutral`

**summary**

TVS Electronics Limited's Q4-FY26 earnings presentation highlights revenue growth across its segments. The Products and Solutions Group (PSG) reported revenue of INR 804 Mn in Q4-FY26, a 2.3% increase from Q3-FY26 and 3.0% year-over-year (Y-o-Y) growth for FY26. Customer Support Services (CSS) revenue rose to INR 370 Mn in Q4-FY26, a 5.7% increase from Q3-FY26 and 12.7% Y-o-Y growth for FY26. Overall revenue for Q4-FY26 was INR 1,174 Mn, up 3.3% Q-o-Q and 2.4% Y-o-Y, with FY26 revenue reaching INR 4,552 Mn, a 5.7% Y-o-Y increase. EBITDA for Q4-FY26 was INR 70 Mn, with a margin of 5.96%, up 24 basis points (Bps) Q-o-Q and 413 Bps Y-o-Y. FY26 EBITDA was INR 195 Mn, with a margin of 4.28%, up 172 Bps from FY25. The company noted improved margins due to better product mix and TCM initiatives. The balance sheet showed a debt-to-equity ratio of 0.43x as of FY26, with total liabilities at INR 1,866 Mn and equity at INR 959 Mn. The stock price as of March 31, 2026, was INR 360.5, with a market cap of INR 6,723.4 Mn. The presentation included forward-looking statements with disclaimers about risks and uncertainties.

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
| Lexical overlap | 0.2167 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 31.8103 s |
| Input / output tokens | 6192 / 444 |
| Tokens/sec (output) | 14.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Neutral`

**summary**

The investor presentation for Kuantum Papers Limited (KUANTUM) for Q4-FY26 outlines the company's operational and financial performance, strategic initiatives, and key strengths. Operational income for FY26 was INR 10,932 Mn, a slight decline from FY25, while EBITDA fell to 14.8% from 21.9% due to lower net sales realization (NSR) and rising costs. Quarterly operational income for Q4-FY26 was INR 3,009 Mn, with EBITDA margins improving to 15.9% from 13.6% in Q3-FY26 despite market challenges. The company reported a net profit of INR 420 Mn for FY26, down from INR 1,152 Mn in FY25, with PAT margins at 3.84%. Key operational updates include the completion of Paper Machine 2 rebuild, progress on the Displacement Digester System (DDS) project, and the installation of a Syncro Sheeter. Strategic initiatives focus on plant expansion, sustainability, and leveraging Industry 4.0 technologies. The company also highlighted its Social Farm Forestry program, adding 854 acres in Q4-FY26. Financial highlights show a net debt-to-equity ratio of 0.66x and a market capitalization of INR 5,767.3 Mn as of 31 March 2026. The presentation includes forward-looking statements with disclaimers about risks and uncertainties.

**tone_note**

The document presents factual operational and financial data alongside strategic initiatives without overtly positive or negative language.

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
| Lexical overlap | 0.2969 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 38.4861 s |
| Input / output tokens | 7932 / 371 |
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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Mixed`

**summary**

The investor presentation for Q4 FY2025-26 by Sigachi Industries Limited outlines operational and financial highlights, emphasizing strategic growth initiatives and competitive advantages. Management noted that FY26 concluded with operational continuity, strengthened customer relationships, and a reinforced long-term growth strategy. The Dahej-2 capacity expansion is progressing, aiming to increase total MCC capacity to 30,000 MTPA. A new API R&D Center in Hyderabad is fully operational, supporting API portfolio growth. Financially, Q4 FY26 revenue was Rs. 1,219 Mn, with an EBITDA of Rs. 154 Mn and a PAT of Rs. 76 Mn. The presentation reported a 5-year revenue CAGR of 19.92% and EBITDA CAGR of 6.74%. Guidance for FY27 includes achieving revenue of Rs. 6,500–6,750 Mn, an EBITDA margin of 18–20%, and >65% capacity utilization post-Dahej-2 ramp-up. The document also highlighted ESG performance, including waste recycling rates and CSR initiatives. The tone of the presentation emphasized resilience and strategic positioning despite financial challenges in FY26.

**tone_note**

The presentation acknowledged financial challenges in FY26 while highlighting strategic progress and growth initiatives.

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
| Lexical overlap | 0.3832 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 33.2329 s |
| Input / output tokens | 7521 / 299 |
| Tokens/sec (output) | 9.0 |

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
| Latency | 90.3083 s |
| Input / output tokens | 34237 / 928 |
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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'targets'
- pass 2: forward-tense word 'target'
- pass 3: forward-tense word 'target'

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
| Latency | 215.524 s |
| Input / output tokens | 62982 / 1073 |
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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'targeting'
- pass 2: forward-tense word 'outlook'
- pass 3: forbidden word 'predictions'

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
| Latency | 56.1711 s |
| Input / output tokens | 22151 / 887 |
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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Neutral`

**summary**

Go Fashion (India) Limited's Q1 FY27 investor presentation highlights a 2% YoY revenue growth to Rs. 161 crores, with gross profit rising 2% to Rs. 50 crores and a 62.9% gross margin, though down 10 bps. Profit after tax increased 4% to Rs. 8 crores, but online revenue remained flat at Rs. 140 crores. The company closed 66 stores, reducing retail space by 7,016 sq. ft., while expanding larger EBO stores (700+ sq. ft.) to enhance in-store experience. EBITDA before exceptional items was Rs. 67.4 crores (down 2% YoY) with a 30.3% margin, but EBITDA fell 11% to Rs. 60.9 crores after a Rs. 6.5 crore exceptional expense from store closures. Working capital days were 24.7, and cash flow from operations was Rs. 25.4 crores. The company reported 751 EBOs across 195 cities, with a focus on Tier 2 and 3 cities, and plans to nearly double retail area over five years. The product portfolio includes 58% churidar and leggings, with non-leggings products now contributing ~70% of revenue. The presentation notes a 14.0% EBITDA margin (Q1 FY27) due to increased marketing spend, and a 2.3% marketing expense ratio compared to 1.5% in Q1 FY26. The company emphasizes its strong unit economics, efficient supply chain, and expansion strategies, including online growth and technology adoption. Historical financials show revenue growth from Rs. 401 crores in FY22 to Rs. 838 crores in FY26, with PAT rising from Rs. 35.6 crores to Rs. 59.2 crores. RoCE and RoE were 10.8% and 7.9% in Q1 FY27, respectively, with cash reserves at Rs. 202 crores. The company's strategy includes expanding EBOs, leveraging online channels, and enhancing brand visibility through partnerships and advertising.

**tone_note**

The presentation provides factual financial and operational updates without overtly positive or negative language.

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
| Lexical overlap | 0.2468 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 59.2461 s |
| Input / output tokens | 9977 / 530 |
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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Positive`

**summary**

Unimech Aerospace and Manufacturing Limited reported strong Q1 FY27 results with revenue of ₹1,076.2 mn, up 71% year-over-year, and EBITDA of ₹392.5 mn, up 98% year-over-year, reflecting improved customer demand and disciplined execution. The company highlighted strategic investments, including the acquisition of Hobel Bellows, which contributed to expanded growth platforms across aerospace, semiconductor, and energy sectors. Operational highlights included a long-term supply agreement with FACC and an RFQ from a major semiconductor equipment OEM. The order book reached ₹2,803 million as of June 30, 2026, with significant contributions from nuclear and aerospace sectors. Financial metrics showed a 36.5% EBITDA margin, up 5% year-over-year, and a 24.2% PAT margin. The company emphasized qualification-led growth, expanding its precision manufacturing capabilities and customer relationships. Management expressed confidence in FY27 growth, citing strong order pipelines and margin discipline. The presentation included details on manufacturing facilities, certifications, and strategic initiatives like the Kanoo–Unimech joint venture in Saudi Arabia and the acquisition of Hobel Bellows.

**tone_note**

The document emphasizes strong revenue and EBITDA growth, successful strategic acquisitions, and confidence in future growth driven by expanded customer relationships and operational improvements.

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
| Lexical overlap | 0.3675 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 49.1626 s |
| Input / output tokens | 15108 / 688 |
| Tokens/sec (output) | 14.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Positive`

**summary**

The investor presentation for Rategain Travel Technologies Limited (RATEGAIN) for Q1 FY2027 highlights robust financial growth, with operating revenue increasing by 187.6% year-over-year to INR 785.0 crore. Adjusted EBITDA grew by 289.3% to INR 193.4 crore, and adjusted PAT rose by 148.8% to INR 116.8 crore. The company emphasized its AI-driven platform, which supports guest acquisition, retention, and revenue expansion through services like DaaS, Martech, and Distribution. Key business updates include strong operating margins, a 95.3% increase in revenue per employee post-Sojern integration, and a 47.3% rise in employee headcount. The presentation also outlined strategic partnerships, product innovations, and a diversified revenue mix with 79.1% from subscription and hybrid models. Financial metrics show sustained profitability, with free cash flow conversion at 78.8% and a net cash position of INR 255.6 crore. The company noted challenges related to deferred deal considerations from the Sojern acquisition, impacting adjusted EBITDA and PAT. Management highlighted confidence in operational efficiency and growth, with a focus on AI integration, customer expansion, and geographic diversification.

**tone_note**

The presentation emphasizes strong financial growth, operational efficiency, and confidence in AI-driven strategies.

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
| Lexical overlap | 0.2868 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 39.0019 s |
| Input / output tokens | 8386 / 318 |
| Tokens/sec (output) | 8.2 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Positive`

**summary**

In the Q1 FY27 earnings call, Emami Limited reported consolidated revenue growth of 15% to INR1,039 crores, driven by a 20% increase in domestic business and 11% growth in the Hair and Scalp Care category. The Skin Care segment grew by 3%, with Talcum powder showing high single-digit growth despite regional summer season variations. Healthcare revenue rose by 2%, with the OTC portfolio growing in high teens and strategic investments contributing 18% of domestic business, showing 61% like-to-like growth. International business declined by 12% due to West Asia conflicts, but management expressed confidence in recovery. Profitability faced challenges from inflationary pressures and cost increases, though EBITDA grew by 6% to INR226 crores. Strategic initiatives include supply chain optimization, AI deployment for sales, and data analytics platforms. The strategic investment portfolio, including Axiom and IncNut, showed strong growth but with varying margins, aiming for EBITDA neutrality. Management emphasized diversification, cost control, and confidence in future growth despite near-term headwinds.

**tone_note**

The document highlights strong revenue growth, strategic initiatives, and confidence in future recovery despite challenges.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference (gpt-4o-mini) | ✅ PASS |
| tone_label — reference | `Mixed` |
| tone_label — Qwen | `Positive` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ❌ no |
| Lexical overlap | 0.306 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 42.4183 s |
| Input / output tokens | 9239 / 274 |
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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Positive`

**summary**

JNK India Limited's Q1FY27 investor presentation highlights strong financial performance, with Total Income growing by 80.6% YoY to Rs. 186.0 cr, EBITDA increasing by 3.1x to Rs. 21.9 cr, and PAT rising by 8.5x to Rs. 9.6 cr. The company maintained an EBITDA margin of 11.8%, reflecting disciplined growth. The order book stood at Rs 1,801 cr as of June 30, 2026, with a bidding pipeline of Rs. ~6,000 cr across domestic and international markets. Management emphasized diversification into offshore, metals & minerals, and renewable energy, with JNK Chemdist contributing to renewable energy projects like green hydrogen. The company noted an isolated export order cancellation due to technical approval issues but highlighted no material costs. Financial data for prior periods was reclassified for consistency. Strategic initiatives include expanding global presence, enhancing technology capabilities through joint ventures, and focusing on operational excellence and sustainable growth.

**tone_note**

The presentation emphasizes strong financial growth, robust order inflows, and strategic expansion into new markets and technologies.

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
| Lexical overlap | 0.3628 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 23.4589 s |
| Input / output tokens | 5828 / 265 |
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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

**tone_label:** `Mixed`

**summary**

The investor presentation for Fino Payments Bank Limited (FINOPB) for Q1 FY27 highlights key business updates and financial performance. Management reported a 42.8% net revenue margin, driven by higher contributions from the CASA business segment. Average total deposits rose 12% YoY to ₹2,772 crores, with digitally active customers increasing by 22% YoY to 64.6 lakh. Referral loan disbursements surged 214% YoY to ₹628 crores, accounting for ~50% of total referral loans disbursed in FY26. The bank is progressing toward becoming a Small Finance Bank (SFB), with LOS & LMS identified and a consultant partnered for the transition. Financial highlights include a 32% YoY revenue growth to ₹306.9 crores, a 30% YoY increase in EBITDA to ₹43.1 crores, and a 12% YoY rise in average CASA balances. However, the bank reported a net loss of ₹13.7 crores for the quarter. Operational efficiency metrics show a 2.5x increase in throughput per employee, and the bank maintains a low-cost liability franchise with a cost of funds at 1.4%. The presentation also outlines the SFB timeline, with end-to-end process validation and readiness assessment planned for Q3’27 and submission of final readiness to the RBI by Q1’28. The bank's digital footprint, including UPI throughput and digitally active users, continues to grow, though revenue from non-digital transactions remains limited. The presentation notes ongoing challenges, including a decline in digital throughput YoY and a net loss for the quarter, while emphasizing progress in SFB readiness and customer acquisition.

**tone_note**

The document presents both positive financial metrics and operational progress alongside challenges such as a net loss and declining digital throughput.

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
| Lexical overlap | 0.3723 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 31.2343 s |
| Input / output tokens | 6293 / 415 |
| Tokens/sec (output) | 13.3 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq-tp2`)

_(no output)_

<details><summary>Rejected attempts</summary>

- pass 1: forward-tense word 'expected'
- pass 2: forward-tense word 'targeting'
- pass 3: forward-tense word 'will'

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
| Latency | 103.8583 s |
| Input / output tokens | 37673 / 979 |
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

## Overall reviewer verdict

Fill this in only AFTER completing the per-case tables above.

- **Verdict (ACCEPTABLE / NOT ACCEPTABLE / INCONCLUSIVE):** ______
- **If NOT ACCEPTABLE — the specific failure mode:** ______
- **If INCONCLUSIVE — what additional cases would settle it:** ______
- **Reviewer:** ______   **Date:** ______

This was a small sample. It cannot establish production-readiness regardless of how good the outputs look.
