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
| Cases | 1 of 3 |
| Run id | `20260828T175028Z` (2026-08-28T17:50:28.599874+00:00) |
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
| mean_latency_sec | 64.702 |
| total_prompt_tokens | 11908 |
| total_completion_tokens | 288 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| tone_label_agreement_rate | 1.0 |
| invalid_tone_labels | 0 |
| tone_confusion | Mixed->Mixed=1 |
| mean_lexical_overlap | 0.2675 |

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
| Latency | 64.7016 s |
| Input / output tokens | 11908 / 288 |
| Tokens/sec (output) | 4.5 |

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
