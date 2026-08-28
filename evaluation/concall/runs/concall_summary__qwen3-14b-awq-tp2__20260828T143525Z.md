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
| Fixture | `/kaggle/input/datasets/ajaychouhan9/redixfi-llm-fixtures/concall_sample15.json` |
| Cases | 3 of 3 |
| Run id | `20260828T143525Z` (2026-08-28T14:35:25.033025+00:00) |
| LLM project commit | `unknown` |
| GPU | 2x Tesla T4 (29.12 GB total) |
| CUDA / torch / vLLM | 13.0 / 2.13.0+cu130 / None |

## Objective signals (mechanical only — no judgement)

| Metric | Value |
|---|---|
| cases | 3 |
| generated_ok | 3 |
| generation_failures | 0 |
| candidate_compliance_failures | 0 |
| reference_backstop_artifacts | 0 |
| reference_compliance_failures | 0 |
| cases_with_reference | 3 |
| json_repair_used | 3 |
| mean_latency_sec | 76.687 |
| total_prompt_tokens | 37421 |
| total_completion_tokens | 2660 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| tone_label_agreement_rate | 0.6667 |
| invalid_tone_labels | 0 |
| tone_confusion | Mixed->Mixed=1, Neutral->Neutral=1, Positive->Mixed=1 |
| mean_lexical_overlap | 0.2409 |

## Cases

---

### Case 1 — `CC_ALKYLAMINE_106620224`

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

The earnings call for Alkyl Amines Chemicals Limited's Q4FY26 reported flat revenue and profit growth compared to the prior year, with minor fluctuations of ±1%. Management noted challenges in raw material sourcing, particularly ammonia, in March but stated operations were stabilized. They emphasized retained or slightly increased market share despite slower market growth. Rising raw material prices led to higher finished product prices, though demand impact remains uncertain. A project initially slated for Q1-Q2FY26 was delayed to the next quarter, but its economics remain unaffected. Competition in methylamines increased with new entrants, while ethylamines face less pressure. Management expressed cautious optimism about future margins as supply chains stabilize, though they acknowledged ongoing uncertainties, including geopolitical factors. They noted pharma and agro segments remain key, with pharma showing resilience. No major capex plans were announced for FY27-FY28, focusing instead on maintenance and existing projects. R&D initiatives are ongoing but not disclosed until products reach market.

**tone_note**

The document reflects both challenges (flat growth, supply disruptions) and cautious optimism (market share retention, margin potential) without definitive directional language.

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
| tone_label — reference | `Mixed` |
| tone_label — Qwen | `Mixed` |
| tone_label valid (closed set) | ✅ |
| tone_label agrees | ✅ yes |
| Lexical overlap | 0.2194 _(triage aid, NOT a score)_ |
| JSON repair needed | yes |
| Latency | 117.3487 s |
| Input / output tokens | 23836 / 1297 |
| Tokens/sec (output) | 11.1 |

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

### Case 2 — `CC_COROMANDEL_106614369`

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

The investor presentation for Coromandel International Limited's conference call discussing Q4FY26 results, scheduled for May 8, 2026 at 02:30 PM IST, has been uploaded to the company's website as required by SEBI regulations. The document confirms the availability of the presentation at the specified URL and requests stakeholders to take the submission on record. The communication follows a prior notice dated May 5, 2026, regarding the conference call. No specific financial results, strategic updates, or operational performance details are disclosed in the text provided. The filing adheres to regulatory requirements under SEBI's Listing Obligations and Disclosure Requirements Regulations, 2015. The company secretary, B. Shanmugasundaram, digitally signed the document on May 8, 2026.

**tone_note**

The document is a standard compliance communication confirming the availability of a presentation without expressing sentiment or directional views.

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
| Lexical overlap | 0.2817 _(triage aid, NOT a score)_ |
| JSON repair needed | yes |
| Latency | 15.8782 s |
| Input / output tokens | 1041 / 561 |
| Tokens/sec (output) | 35.3 |

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

### Case 3 — `CC_KIRIINDUS_106747935`

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

**tone_label:** `Mixed`

**summary**

Kiri Industries Limited reported Q1 FY27 results showing improved performance in its dyes, intermediates, and basic chemicals business, with standalone material margins rising to 31.9% due to favorable pricing differentials. Revenue from operations grew 63% YoY to INR 295 crore, driven by higher average selling prices. Consolidated EBITDA reached INR 37 crore, supported by other income from treasury activities. The company emphasized progress on its integrated copper and fertilizer project, now in structured construction phase with phased commissioning of downstream facilities by FY28-FY29. Management highlighted engagement with international mining firms for raw materials and discussed capital deployment of INR 1,400 crore in the copper project, all equity-funded currently. Shareholders were informed that no dividend decision has been made, with capital prioritized for growth. Challenges included input cost pressures, unresolved litigation affecting the MCB Copper-Gold project, and reliance on external financing for project completion. The company also addressed questions on operational timelines, debt repayment starting in 2029, and potential equity financing options.

**tone_note**

The document highlights both progress in projects and improved financials, alongside ongoing challenges like litigation, input costs, and dependency on external factors.

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
| Lexical overlap | 0.2215 _(triage aid, NOT a score)_ |
| JSON repair needed | yes |
| Latency | 96.8333 s |
| Input / output tokens | 12544 / 802 |
| Tokens/sec (output) | 8.3 |

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
