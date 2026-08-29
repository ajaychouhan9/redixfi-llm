# Review sheet — annual_report_summary

> **EXPERIMENTAL / NOT PRODUCTION.** This file is evidence for a human to review, not a verdict. No quality score is computed anywhere in it, and no LLM judge was used. The candidate model is NOT declared better or worse than gpt-4o-mini by this tooling.

> ⚠️ **`echo` backend — NO MODEL WAS CONSULTED.** These results validate the harness only and are not a model comparison.

> ⚠️ **Not a like-for-like comparison.** The stored reference was produced on 2026-08-16 by the LEGACY pipeline (raw_text front slice, `summary`/`bullets`/`key_takeaway`). This replay uses the CURRENT pipeline (Evidence Finder evidence, `executive_summary`/`key_points`/`important_risks`). Both the input AND the output schema differ. The like-for-like replay is `annual_report_summary_legacy`, which needs a 64k context.

## Run configuration

| | |
|---|---|
| Model | `qwen3-14b-awq` |
| Weights | `Qwen/Qwen3-14B-AWQ` |
| Quantization / dtype | `awq` / `float16` |
| Tensor parallel | 1 |
| Context length | 16384 |
| Backend | `echo` |
| Sampling | temperature=0.0, max_tokens=1024, seed=0 |
| Fixture | `fixtures/annual_report_benchmark.json` |
| Cases | 20 of 20 |
| Run id | `20260828T123134Z` (2026-08-28T12:31:34.051079+00:00) |
| LLM project commit | `aad9946` |

## Objective signals (mechanical only — no judgement)

| Metric | Value |
|---|---|
| cases | 20 |
| generated_ok | 20 |
| generation_failures | 0 |
| candidate_compliance_failures | 0 |
| reference_compliance_failures | 0 |
| cases_with_reference | 20 |
| json_repair_used | 0 |
| mean_latency_sec | 0.0 |
| total_prompt_tokens | 257232 |
| total_completion_tokens | 3140 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| mean_lexical_overlap | 0.0537 |

## Cases

---

### Case 1 — `AR_VEDL_AR_26570_VEDL_2024_2025_A_18062025151918`

#### SOURCE / EVIDENCE

- **Symbol:** VEDL
- **Company:** Vedanta Limited
- **Fiscal year:** FY2024-25
- **Filing id:** AR_26570_VEDL_2024_2025_A_18062025151918
- **Doc type:** annual_report

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0455 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 12897 / 157 |
| Tokens/sec (output) | 0.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0476 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 12766 / 157 |
| Tokens/sec (output) | 0.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0217 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 13071 / 157 |
| Tokens/sec (output) | 0.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0769 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 12768 / 157 |
| Tokens/sec (output) | 0.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0909 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 12764 / 157 |
| Tokens/sec (output) | 0.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0213 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 13066 / 157 |
| Tokens/sec (output) | 0.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0465 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 13010 / 157 |
| Tokens/sec (output) | 0.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0698 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 12926 / 157 |
| Tokens/sec (output) | 0.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0435 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 12771 / 157 |
| Tokens/sec (output) | 0.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0682 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 12770 / 157 |
| Tokens/sec (output) | 0.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0952 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 12765 / 157 |
| Tokens/sec (output) | 0.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0222 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 12933 / 157 |
| Tokens/sec (output) | 0.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0526 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 12767 / 157 |
| Tokens/sec (output) | 0.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0698 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 12767 / 157 |
| Tokens/sec (output) | 0.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0698 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 12760 / 157 |
| Tokens/sec (output) | 0.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0667 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 12765 / 157 |
| Tokens/sec (output) | 0.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0222 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 13072 / 157 |
| Tokens/sec (output) | 0.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0213 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 12758 / 157 |
| Tokens/sec (output) | 0.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.0476 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 12767 / 157 |
| Tokens/sec (output) | 0.0 |

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

#### NEW — QWEN OUTPUT (`qwen3-14b-awq`)

**executive_summary**

The report described the company's stated priorities across its operating segments. Management said it focused on capacity, governance and sustainability during the period. The document outlined the areas management identified as central to its strategy.

**key_points**

- Management described a focus on capacity and operational resilience
- The report stated continued investment in sustainability programmes
- Management said governance practices were reviewed during the year

**important_risks**

_(none)_

**key_takeaway**

The report centred on management's stated operating priorities for the period.

#### OBJECTIVE VALIDATION

| Check | Result |
|---|---|
| Generation succeeded | ✅ yes |
| Attempts used | 1 |
| Compliance — **Qwen** | ✅ PASS |
| Compliance — reference | ⚠️ not comparable (schema mismatch) |
| Lexical overlap | 0.075 _(triage aid, NOT a score)_ |
| Output shape | unguided, but output parsed cleanly |
| Structured mode | `none` |
| Latency | 0.0 s |
| Input / output tokens | 13069 / 157 |
| Tokens/sec (output) | 0.0 |

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
