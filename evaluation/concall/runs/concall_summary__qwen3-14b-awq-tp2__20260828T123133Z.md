# Evaluation review sheet — concall_summary

> **EXPERIMENTAL / NOT PRODUCTION.** Nothing here is evidence that the candidate model is fit for use. The objective columns below are mechanical checks; every quality judgement is left blank for a human reviewer, by design.

## Run configuration

- **Model:** `qwen3-14b-awq-tp2`
- **Weights:** `Qwen/Qwen3-14B-AWQ` (quantization: `awq`, dtype: `float16`, TP: 2, max_model_len: 32768)
- **Backend:** `echo`
- **Sampling:** temperature=0.0, max_tokens=1024, seed=0
- **Fixture:** `fixtures/concall_benchmark.json` (exported 2026-08-28T12:23:05.734646+00:00)
- **Cases run:** 20 of 20
- **LLM project commit:** `aad9946`
- **Run id:** `20260828T123133Z` (2026-08-28T12:31:33.229559+00:00)

> ⚠️ **This run used the `echo` backend.** No model was consulted. These results validate the harness only and must never be read as a model comparison.

## Objective signals (mechanical, no judgement)

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
| total_prompt_tokens | 150832 |
| total_completion_tokens | 2600 |
| quality_verdict | NOT COMPUTED — requires human review, by design |
| tone_label_agreement_rate | 0.2 |
| invalid_tone_labels | 0 |
| tone_confusion | Mixed->Neutral=6, Positive->Neutral=10, Neutral->Neutral=4 |
| mean_lexical_overlap | 0.047 |

## Side-by-side cases

### 1. `BATAINDIA` — fixture `CC_BATAINDIA_106539458`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0435 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

### 2. `SUNTECK` — fixture `CC_SUNTECK_106596830`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0349 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

### 3. `KANPRPLA` — fixture `CC_KANPRPLA_106607445`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.043 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

### 4. `COROMANDEL` — fixture `CC_COROMANDEL_106614369`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0161 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

### 5. `ALKYLAMINE` — fixture `CC_ALKYLAMINE_106620224`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.036 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

### 6. `AARTIDRUGS` — fixture `CC_AARTIDRUGS_106626214`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0632 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

### 7. `INDIQUBE` — fixture `CC_INDIQUBE_106632356`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0357 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

### 8. `TVSELECT` — fixture `CC_TVSELECT_106638347`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0638 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

### 9. `KUANTUM` — fixture `CC_KUANTUM_106643553`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0404 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

### 10. `SIGACHI` — fixture `CC_SIGACHI_106649351`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0421 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

### 11. `SDBL` — fixture `CC_SDBL_106655906`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0526 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

### 12. `PNB` — fixture `CC_PNB_106702450`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0476 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

### 13. `MANYAVAR` — fixture `CC_MANYAVAR_106711176`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0521 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

### 14. `GOCOLORS` — fixture `CC_GOCOLORS_106717019`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0588 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

### 15. `UNIMECH` — fixture `CC_UNIMECH_106722740`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0612 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

### 16. `RATEGAIN` — fixture `CC_RATEGAIN_106728376`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0577 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

### 17. `EMAMILTD` — fixture `CC_EMAMILTD_106734041`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0556 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

### 18. `JNKINDIA` — fixture `CC_JNKINDIA_106738190`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0421 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

### 19. `FINOPB` — fixture `CC_FINOPB_106742828`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0495 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

### 20. `KIRIINDUS` — fixture `CC_KIRIINDUS_106747935`

**REFERENCE (production, gpt-4o-mini)** — refused=None

_(empty)_

**CANDIDATE** — refused=None

_(empty)_

**Compliance —** candidate: ✅ pass · reference: ✅ pass

**Lexical overlap:** 0.0446 _(triage aid only — not a quality score)_

**Human review** — fill this in:

| Criterion | Reference (OpenAI) | Candidate | Notes |
|---|---|---|---|
| factual correctness |  |  |  |
| numerical accuracy |  |  |  |
| financial terminology |  |  |  |
| evidence grounding |  |  |  |
| hallucination (none = good) |  |  |  |
| completeness |  |  |  |
| relevance |  |  |  |
| reasoning quality |  |  |  |
| source/citation correctness |  |  |  |
| risk identification accuracy |  |  |  |
| consistency |  |  |  |
| formatting |  |  |  |
| usefulness to an investor |  |  |  |


---

## Reviewer verdict

After completing the tables above, record ONE of:

- **ACCEPTABLE** — quality is close enough to production to justify a narrow, reversible pilot on one workload.
- **NOT ACCEPTABLE** — name the specific failure mode.
- **INCONCLUSIVE** — say what additional cases would settle it.

Verdict: _______   Reviewer: _______   Date: _______
