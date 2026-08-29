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
| Cases | 2 of 20 |
| Run id | `20260829T182829Z` (2026-08-29T18:28:29.367417+00:00) |
| LLM project commit | `unknown` |
| GPU | 2x Tesla T4 (29.12 GB total) |
| CUDA / torch / vLLM | 13.0 / 2.13.0+cu130 / None |

## Objective signals (mechanical only — no judgement)

| Metric | Value |
|---|---|
| cases | 2 |
| generated_ok | 1 |
| generation_failures | 1 |
| candidate_compliance_failures | 1 |
| reference_backstop_artifacts | 0 |
| reference_compliance_failures | 0 |
| cases_with_reference | 2 |
| structured_output_used | 2 |
| json_repair_used | 0 |
| guided_and_clean | 2 |
| guided_but_repaired | 0 |
| unguided | 0 |
| mean_latency_sec | 59.66 |
| total_prompt_tokens | 43279 |
| total_completion_tokens | 1291 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| tone_label_agreement_rate | 1.0 |
| invalid_tone_labels | 0 |
| tone_confusion | Mixed->None=1, Positive->Positive=1 |
| mean_lexical_overlap | 0.1991 |

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
| Latency | 81.7734 s |
| Input / output tokens | 35259 / 858 |
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

Sunteck Realty Limited’s investor presentation for Q4 and full-year FY26 reported strong financial and operational growth. Revenue rose to Rs. 339 crore in Q4FY26 (65% YoY growth) and Rs. 1,124 crore in FY26 (32% YoY growth), with EBITDA and PAT also increasing by 41% and 25% YoY, respectively. EBITDA margins stood at 29% in Q4FY26 and 27% for FY26, while PAT margins were 19% and 18%, respectively. Pre-sales grew to Rs. 1,064 crore in Q4FY26 and Rs. 3,157 crore in FY26, up 22% and 25% YoY, respectively, with collections at Rs. 432 crore and Rs. 1,433 crore, respectively. The company highlighted a net cash flow surplus of Rs. 552 crore (48% YoY growth) and a net debt-to-equity ratio of 0.06x. Sunteck emphasized its strong foothold in the Mumbai Metropolitan Region (MMR), strategic acquisitions (50+ million sq. ft., GDV of Rs. 41,030 crore), and expanding annuity income portfolio (Rs. 300+ crore in rentals). The presentation also noted successful equity partnerships, including a Rs. 750 crore joint investment platform with IFC-World Bank Group, and sustainability achievements such as a 99 GRESB score and inclusion in the Dow Jones Sustainability Index (ESG score of 78).

**tone_note**

Management emphasized robust revenue, EBITDA, and PAT growth, alongside strong operational metrics like pre-sales and collections, while highlighting strategic acquisitions and sustainability accolades.

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
| Lexical overlap | 0.3981 _(triage aid, NOT a score)_ |
| Output shape | ✅ guided decoding — valid JSON by construction |
| Structured mode | `json_schema` |
| Latency | 37.5469 s |
| Input / output tokens | 8020 / 433 |
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

## Overall reviewer verdict

Fill this in only AFTER completing the per-case tables above.

- **Verdict (ACCEPTABLE / NOT ACCEPTABLE / INCONCLUSIVE):** ______
- **If NOT ACCEPTABLE — the specific failure mode:** ______
- **If INCONCLUSIVE — what additional cases would settle it:** ______
- **Reviewer:** ______   **Date:** ______

This was a small sample. It cannot establish production-readiness regardless of how good the outputs look.
