# Expanded review — index

> **EXPERIMENTAL / NOT PRODUCTION.** Nothing here scores quality. The tables below carry only mechanically-checkable signals and a suggested reading order; every quality judgement lives in the blank HUMAN REVIEW NOTES tables inside the per-case sheets.

_Generated 2026-08-30 06:12 UTC_

> ## ⚠️ Read this before comparing any two runs
>
> **Generation on this hardware is NOT reproducible run-to-run, even at `temperature=0` with a fixed seed.** Observed from a SINGLE before/after comparison (n=2 samples per case, not a repeated-trial measurement — see `ACTIONS_1_3_FULL_RESULTS.md` for the precise accounting of what was and wasn't measured): re-running the same fixtures with identical settings, attempt-1 output differed on **4 of 20** annual-report cases and **7 of 20** concall cases, and the attempt-1 pass/fail verdict itself flipped on **1** annual-report and **3** concall cases. The likely cause is continuous batching and non-deterministic reduction order across the two T4s, not the sampling settings.
>
> **Consequence: at n=20, a difference of ±1–3 cases between runs is inside this observed range and should not be read as a confirmed improvement or regression on its own.** A properly measured noise floor (3-5x repeat, never yet run) could show a tighter or wider range than this — treat ±1-3 as a lower bound on the uncertainty, not a precise figure. Larger deltas (roughly 5+ cases) are unlikely to be pure noise. This applies to every before/after number in this index.
>
> **Session documents, in the order the work happened:** `ACTIONS_1_3_FULL_RESULTS.md` (the noise-floor correction above), `MINISTRAL_EVAL.md` (head-to-head vs Ministral 3 14B, shelved), `CONCALL_MARKDOWN_FAIRNESS.md` (one-line markdown ban, both models), `CONCALL_AND_REDFLAG_TUNING.md` (retry-budget 20/20 for concall; red_flag instance-check — net regression, not adopted).

## What ran

| Category | Model | Cases | Generated | Compliance fails | Guided / repaired | Sheet |
|---|---|---|---|---|---|---|
| Annual Report (current pipeline) | `ministral3-14b-w4a16-tp2` | 20 | 3 | 17 | 20 / 0 | [annual_report_summary__ministral3-14b-w4a16-tp2__20260829T194522Z__refreshed_reference.md](annual_report/runs/annual_report_summary__ministral3-14b-w4a16-tp2__20260829T194522Z__refreshed_reference.md) |
| Annual Report (current pipeline) | `qwen3-14b-awq-tp2` | 20 | 18 | 2 | 20 / 0 | [annual_report_summary__qwen3-14b-awq-tp2__20260829T133627Z__refreshed_reference.md](annual_report/runs/annual_report_summary__qwen3-14b-awq-tp2__20260829T133627Z__refreshed_reference.md) |
| Concall | `ministral3-14b-w4a16-tp2` | 20 | 15 | 5 | 20 / 0 | [concall_summary__ministral3-14b-w4a16-tp2__20260829T200720Z.md](concall/runs/concall_summary__ministral3-14b-w4a16-tp2__20260829T200720Z.md) |
| Concall | `qwen3-14b-awq-tp2` | 20 | 17 | 3 | 20 / 0 | [concall_summary__qwen3-14b-awq-tp2__20260829T135557Z.md](concall/runs/concall_summary__qwen3-14b-awq-tp2__20260829T135557Z.md) |
| Red Flag | `ministral3-14b-w4a16-tp2` | 60 | 60 | 0 | 60 / 0 | [red_flag__ministral3-14b-w4a16-tp2__20260829T200841Z.md](red_flags/runs/red_flag__ministral3-14b-w4a16-tp2__20260829T200841Z.md) |
| Red Flag | `qwen3-14b-awq-tp2` | 60 | 60 | 0 | 60 / 0 | [red_flag__qwen3-14b-awq-tp2__20260829T073830Z.md](red_flags/runs/red_flag__qwen3-14b-awq-tp2__20260829T073830Z.md) |

## Annual Report (current pipeline) — `ministral3-14b-w4a16-tp2`

> ✅ **Reference regenerated — the comparison is now schema-matched.** Production holds no current-schema annual-report output, so the reference was regenerated with `gpt-4o-mini` on the CURRENT prompt from the SAME evidence block Qwen received, under production retry mechanics (cost $0.0483). Both sides now differ only by model. The reference is a REPLAY, not the text production actually stored — production stored nothing in this schema.

- Model: `ministral3-14b-w4a16-tp2` (ctx 32768, compressed-tensors, TP=2)
- Run id: `20260829T194522Z`
- cases: **20**
- generated_ok: **3**
- generation_failures: **17**
- candidate_compliance_failures: **17**
- reference_compliance_failures: **0**
- guided_and_clean: **20**
- json_repair_used: **0**

### Read these first — 17 case(s) where the models differ or a check failed

| Case | What differs |
|---|---|
| `AR_VEDL_AR_26570_VEDL_2024_2025_A_18062025151918` | GENERATION FAILED — failed validation after 3 attempts |
| `AR_BRITANNIA_AR_27040_BRITANNIA_2024_2025_A_19072025234802` | GENERATION FAILED — failed validation after 3 attempts |
| `AR_DIXON_AR_29048_DIXON_2024_2025_A_14468137_15092025224042` | GENERATION FAILED — failed validation after 3 attempts |
| `AR_LT_AR_29259_LT_2025_2026_A_29793480_14052026183032` | GENERATION FAILED — failed validation after 3 attempts |
| `AR_ADANIPOWER_AR_29298_ADANIPOWER_2025_2026_A_16975380_29052026213520` | GENERATION FAILED — failed validation after 3 attempts |
| `AR_INFY_AR_29313_INFY_2025_2026_U_8985411_30052026200413` | GENERATION FAILED — failed validation after 3 attempts |
| `AR_HINDZINC_AR_29349_HINDZINC_2025_2026_A_20195576_05062026130301` | GENERATION FAILED — failed validation after 3 attempts |
| `AR_ASIANPAINT_AR_29385_ASIANPAINT_2025_2026_A_26278926_12062026160918` | GENERATION FAILED — failed validation after 3 attempts |
| `AR_TECHM_AR_29435_TECHM_2025_2026_A_15304795_23062026234616` | GENERATION FAILED — failed validation after 3 attempts |
| `AR_CGPOWER_AR_29493_CGPOWER_2025_2026_A_11109518_30062026162136` | GENERATION FAILED — failed validation after 3 attempts |
| `AR_M&M_AR_29572_M&M_2025_2026_A_16591991_04072026174358` | GENERATION FAILED — failed validation after 3 attempts |
| `AR_CHOLAFIN_AR_29596_CHOLAFIN_2025_2026_A_8171029_06072026201106` | GENERATION FAILED — failed validation after 3 attempts |
| `AR_BAJFINANCE_AR_29642_BAJFINANCE_2025_2026_A_23098027_07072026220255` | GENERATION FAILED — failed validation after 3 attempts |
| `AR_MANKIND_AR_29682_MANKIND_2025_2026_A_16593335_09072026165705` | GENERATION FAILED — failed validation after 3 attempts |
| `AR_SIEMENS_AR_29759_SIEMENS_2024_2026_A_21354062_13072026172733` | GENERATION FAILED — failed validation after 3 attempts |
| `AR_ETERNAL_AR_30059_ETERNAL_2025_2026_A_48211721_29072026204435` | GENERATION FAILED — failed validation after 3 attempts |
| `AR_JIOFIN_AR_30141_JIOFIN_2025_2026_A_8079244_03082026130114` | GENERATION FAILED — failed validation after 3 attempts |

## Annual Report (current pipeline) — `qwen3-14b-awq-tp2`

> ✅ **Reference regenerated — the comparison is now schema-matched.** Production holds no current-schema annual-report output, so the reference was regenerated with `gpt-4o-mini` on the CURRENT prompt from the SAME evidence block Qwen received, under production retry mechanics (cost $0.0483). Both sides now differ only by model. The reference is a REPLAY, not the text production actually stored — production stored nothing in this schema.

> ⚠️ **Retry policy `improved` — NOT like-for-like.** gpt-4o-mini was measured under production retry mechanics (every attempt deterministic, descriptive corrective note). This run varied sampling on retries and sent a directive note. The fair remedy, if this is what closes the gap, is adopting it in RedixFi for both models — not treating it as a Qwen-only crutch.

- Model: `qwen3-14b-awq-tp2` (ctx 32768, awq, TP=2)
- Run id: `20260829T133627Z`
- cases: **20**
- generated_ok: **18**
- generation_failures: **2**
- candidate_compliance_failures: **2**
- reference_compliance_failures: **0**
- guided_and_clean: **20**
- json_repair_used: **0**

### Read these first — 2 case(s) where the models differ or a check failed

| Case | What differs |
|---|---|
| `AR_CHOLAFIN_AR_29596_CHOLAFIN_2025_2026_A_8171029_06072026201106` | GENERATION FAILED — failed validation after 3 attempts |
| `AR_BAJFINANCE_AR_29642_BAJFINANCE_2025_2026_A_23098027_07072026220255` | GENERATION FAILED — failed validation after 3 attempts |

## Concall — `ministral3-14b-w4a16-tp2`

- Model: `ministral3-14b-w4a16-tp2` (ctx 32768, compressed-tensors, TP=2)
- Run id: `20260829T200720Z`
- cases: **20**
- generated_ok: **15**
- generation_failures: **5**
- candidate_compliance_failures: **5**
- reference_compliance_failures: **0**
- guided_and_clean: **20**
- json_repair_used: **0**
- tone_label_agreement_rate: **0.6667**

### Read these first — 10 case(s) where the models differ or a check failed

| Case | What differs |
|---|---|
| `CC_BATAINDIA_106539458` | tone: ref=Mixed qwen=Positive |
| `CC_ALKYLAMINE_106620224` | GENERATION FAILED — failed validation after 3 attempts |
| `CC_TVSELECT_106638347` | tone: ref=Neutral qwen=Positive |
| `CC_KUANTUM_106643553` | tone: ref=Neutral qwen=Mixed |
| `CC_SIGACHI_106649351` | GENERATION FAILED — failed validation after 3 attempts |
| `CC_PNB_106702450` | GENERATION FAILED — failed validation after 3 attempts |
| `CC_GOCOLORS_106717019` | tone: ref=Neutral qwen=Mixed |
| `CC_EMAMILTD_106734041` | GENERATION FAILED — failed validation after 3 attempts |
| `CC_FINOPB_106742828` | tone: ref=Positive qwen=Mixed |
| `CC_KIRIINDUS_106747935` | GENERATION FAILED — failed validation after 3 attempts |

## Concall — `qwen3-14b-awq-tp2`

> ⚠️ **Retry policy `improved` — NOT like-for-like.** gpt-4o-mini was measured under production retry mechanics (every attempt deterministic, descriptive corrective note). This run varied sampling on retries and sent a directive note. The fair remedy, if this is what closes the gap, is adopting it in RedixFi for both models — not treating it as a Qwen-only crutch.

- Model: `qwen3-14b-awq-tp2` (ctx 32768, awq, TP=2)
- Run id: `20260829T135557Z`
- cases: **20**
- generated_ok: **17**
- generation_failures: **3**
- candidate_compliance_failures: **3**
- reference_compliance_failures: **0**
- guided_and_clean: **20**
- json_repair_used: **0**
- tone_label_agreement_rate: **0.7059**

### Read these first — 8 case(s) where the models differ or a check failed

| Case | What differs |
|---|---|
| `CC_BATAINDIA_106539458` | tone: ref=Mixed qwen=Neutral |
| `CC_ALKYLAMINE_106620224` | GENERATION FAILED — failed validation after 3 attempts |
| `CC_AARTIDRUGS_106626214` | tone: ref=Mixed qwen=Neutral |
| `CC_SDBL_106655906` | GENERATION FAILED — failed validation after 3 attempts |
| `CC_PNB_106702450` | tone: ref=Positive qwen=Mixed |
| `CC_EMAMILTD_106734041` | tone: ref=Mixed qwen=Positive |
| `CC_FINOPB_106742828` | tone: ref=Positive qwen=Mixed |
| `CC_KIRIINDUS_106747935` | GENERATION FAILED — failed validation after 3 attempts |

## Red Flag — `ministral3-14b-w4a16-tp2`

- Model: `ministral3-14b-w4a16-tp2` (ctx 32768, compressed-tensors, TP=2)
- Run id: `20260829T200841Z`
- cases: **60**
- generated_ok: **60**
- generation_failures: **0**
- candidate_compliance_failures: **0**
- reference_compliance_failures: **0**
- guided_and_clean: **60**
- json_repair_used: **0**
- agreement_rate: **0.5833**
- outcomes: **{'false_negative': 21, 'agree': 19, 'agree_no_flag': 16, 'false_positive': 4}**

### Read these first — 25 case(s) where the models differ or a check failed

| Case | What differs |
|---|---|
| `RF_ABB_AR_ABB_277` | category false_negative: ref=auditor_qualification qwen=None |
| `RF_ASIANPAINT_AR_ASIANPAINT_716` | category false_negative: ref=auditor_qualification qwen=None |
| `RF_BRITANNIA_AR_BRITANNIA_334` | category false_negative: ref=auditor_qualification qwen=None |
| `RF_ETERNAL_AR_ETERNAL_428` | category false_negative: ref=auditor_qualification qwen=None |
| `RF_HDFCBANK_AR_HDFCBANK_766` | category false_negative: ref=auditor_qualification qwen=None |
| `RF_INDIGO_AR_INDIGO_264` | category false_negative: ref=auditor_qualification qwen=None |
| `RF_LT_AR_LT_718` | category false_negative: ref=auditor_qualification qwen=None |
| `RF_ONGC_AR_ONGC_547` | category false_negative: ref=auditor_qualification qwen=None |
| `RF_POWERGRID_AR_POWERGRID_688` | category false_negative: ref=auditor_qualification qwen=None |
| `RF_TATAPOWER_AR_TATAPOWER_756` | category false_negative: ref=auditor_qualification qwen=None |
| `RF_ASIANPAINT_AR_ASIANPAINT_848` | category false_negative: ref=contingent_liability qwen=None |
| `RF_HDFCBANK_AR_HDFCBANK_600` | category false_negative: ref=contingent_liability qwen=None |
| `RF_MANKIND_AR_MANKIND_503` | category false_negative: ref=contingent_liability qwen=None |
| `RF_BAJFINANCE_AR_BAJFINANCE_288` | category false_negative: ref=related_party_transaction qwen=None |
| `RF_HINDALCO_AR_HINDALCO_1460` | category false_negative: ref=related_party_transaction qwen=None |
| `RF_MAZDOCK_AR_MAZDOCK_154` | category false_negative: ref=related_party_transaction qwen=None |
| `RF_POWERGRID_AR_POWERGRID_609` | category false_negative: ref=related_party_transaction qwen=None |
| `RF_SUNPHARMA_AR_SUNPHARMA_150` | category false_negative: ref=related_party_transaction qwen=None |
| `RF_ADANIENT_AR_ADANIENT_926` | category false_negative: ref=promoter_pledge qwen=None |
| `RF_PFC_AR_PFC_799` | category false_negative: ref=promoter_pledge qwen=None |
| `RF_VEDL_AR_VEDL_1233` | category false_negative: ref=promoter_pledge qwen=None |
| `RF_CIPLA_AR_CIPLA_507` | category false_positive: ref=None qwen=contingent_liability |
| `RF_GRASIM_AR_GRASIM_922` | category false_positive: ref=None qwen=contingent_liability |
| `RF_JINDALSTEL_AR_JINDALSTEL_649` | category false_positive: ref=None qwen=contingent_liability |
| `RF_MOTHERSON_AR_MOTHERSON_470` | category false_positive: ref=None qwen=contingent_liability |

## Red Flag — `qwen3-14b-awq-tp2`

- Model: `qwen3-14b-awq-tp2` (ctx 32768, awq, TP=2)
- Run id: `20260829T073830Z`
- cases: **60**
- generated_ok: **60**
- generation_failures: **0**
- candidate_compliance_failures: **0**
- reference_compliance_failures: **0**
- guided_and_clean: **60**
- json_repair_used: **0**
- agreement_rate: **0.85**
- outcomes: **{'agree': 38, 'false_negative': 2, 'agree_no_flag': 13, 'false_positive': 7}**

### Read these first — 9 case(s) where the models differ or a check failed

| Case | What differs |
|---|---|
| `RF_ONGC_AR_ONGC_547` | category false_negative: ref=auditor_qualification qwen=None |
| `RF_SUNPHARMA_AR_SUNPHARMA_150` | category false_negative: ref=related_party_transaction qwen=None |
| `RF_BAJFINANCE_AR_BAJFINANCE_488` | category false_positive: ref=None qwen=contingent_liability |
| `RF_CIPLA_AR_CIPLA_507` | category false_positive: ref=None qwen=contingent_liability |
| `RF_GODREJCP_AR_GODREJCP_432` | category false_positive: ref=None qwen=auditor_qualification |
| `RF_GRASIM_AR_GRASIM_922` | category false_positive: ref=None qwen=contingent_liability |
| `RF_HINDALCO_AR_HINDALCO_764` | category false_positive: ref=None qwen=contingent_liability |
| `RF_PFC_AR_PFC_439` | category false_positive: ref=None qwen=auditor_qualification |
| `RF_PFC_AR_PFC_700` | category false_positive: ref=None qwen=contingent_liability |

## Prompt-variant runs (full fixture)

> These use a NON-PRODUCTION system prompt. The reference model achieved its result on the production prompt, so a variant number is not a like-for-like comparison against it — it shows what the candidate model needs to get there, or (for a fairness test run identically on two candidate models) how they compare to EACH OTHER under the same added instruction. Read it against the baseline row for the same model above, not against the reference.

| Variant | Model | Task | Cases | Generated | Compliance fails | Tone agreement | Outcome breakdown | Sheet |
|---|---|---|---|---|---|---|---|---|
| `concall_fewshot_bank_v1` | `qwen3-14b-awq-tp2` | Concall | 20 | 17 | 3 | 0.7647 | — | [concall_summary__fewshot_bank__qwen3-14b-awq-tp2__20260830T060722Z.md](concall/runs/concall_summary__fewshot_bank__qwen3-14b-awq-tp2__20260830T060722Z.md) |
| `concall_markdown_fairness_v1` | `ministral3-14b-w4a16-tp2` | Concall | 20 | 13 | 7 | 0.7692 | — | [concall_summary__markdown_fairness__ministral3-14b-w4a16-tp2__20260829T221613Z.md](concall/runs/concall_summary__markdown_fairness__ministral3-14b-w4a16-tp2__20260829T221613Z.md) |
| `concall_markdown_fairness_v1` | `qwen3-14b-awq-tp2` | Concall | 20 | 15 | 5 | 0.8 | — | [concall_summary__markdown_fairness__qwen3-14b-awq-tp2__20260829T214133Z.md](concall/runs/concall_summary__markdown_fairness__qwen3-14b-awq-tp2__20260829T214133Z.md) |
| `concall_steered_v2` | `qwen3-14b-awq-tp2` | Concall | 20 | 14 | 6 | 0.7857 | — | [concall_summary__steered__qwen3-14b-awq-tp2__20260829T141955Z.md](concall/runs/concall_summary__steered__qwen3-14b-awq-tp2__20260829T141955Z.md) |
| `retries_8_improved` | `qwen3-14b-awq-tp2` | Concall | 20 | 20 | 0 | 0.75 | — | [concall_summary__retries_extended__qwen3-14b-awq-tp2__20260830T041530Z.md](concall/runs/concall_summary__retries_extended__qwen3-14b-awq-tp2__20260830T041530Z.md) |
| `red_flag_instance_check_v1` | `qwen3-14b-awq-tp2` | Red Flag | 60 | 60 | 0 | — | false_negative=28, agree=12, agree_no_flag=19, false_positive=1 | [red_flag__instance_check__qwen3-14b-awq-tp2__20260830T041647Z.md](red_flags/runs/red_flag__instance_check__qwen3-14b-awq-tp2__20260830T041647Z.md) |

- **`concall_fewshot_bank_v1`** (attempts 3, retry policy `improved`): Production SYSTEM prompt, completely unmodified. Only the user message differs: up to 2 REAL validated prior successes, retrieved by jaccard similarity from the accumulating example bank, prepended before the current document. No forbidden vocabulary is named anywhere — the examples are positive demonstrations only, testing a mechanism different from every other prompt change tried this session.
- **`concall_markdown_fairness_v1`** (attempts 3, retry policy `production`): Production prompt plus ONE explicit line forbidding markdown/asterisks/bold. Production retry policy — no sampling variation, no directive notes, no content steering. Isolates whether a stronger markdown instruction alone changes behaviour, and whether forbidden-figure violations found inside markdown persist once the markdown itself is suppressed.
- **`concall_steered_v2`** (attempts 3, retry policy `improved`): Content-preference steering: report period results first and abstract forward guidance into attributed past-tense framings harvested from real gpt-4o-mini output. Layered on the improved retry policy, so its delta is measured against retry_policy_improved, not against the baseline.
- **`retries_8_improved`** (attempts 8, retry policy `improved`): Production PROMPT (unmodified) + the improved retry policy (varied sampling, directive notes) + a larger budget (8 attempts, vs production's 3). Isolates budget size as the only additional variable on top of the already-committed retry-mechanics fix — no steering, no markdown instruction, no other prompt change.
- **`red_flag_instance_check_v1`**: Production prompt plus ONE added instruction distinguishing a policy DESCRIPTION from an actual disclosed INSTANCE, using the real confirmed false-positive chunk (BAJFINANCE-488) as the negative example. MEASURED: fixed all 7 known false positives, but introduced 26 new false negatives (2 -> 28) by over-suppressing genuine instances across every category, including real Key Audit Matters gpt-4o-mini itself confirms elsewhere. Net regression (agreement 0.85 -> 0.5167) — NOT a fix as written.

## Concall fix experiments

Repair targets: ['CC_KANPRPLA_106607445', 'CC_KIRIINDUS_106747935', 'CC_MANYAVAR_106711176', 'CC_PNB_106702450', 'CC_SDBL_106655906']

| Variant | Attempts budget | Repaired |
|---|---|---|
| `retries_6` | 6 | 2/5 |
| `concall_fewshot_v1` | 3 | 1/5 |

> A variant that passes on a **different prompt** or a **larger retry budget** has not matched gpt-4o-mini like-for-like — gpt-4o-mini achieved its result on the production prompt at 3 attempts. If the few-shot variant closes the gap, the fair remedy is adopting that prompt in RedixFi for both models, not keeping it as a Qwen-only crutch.

## How to review

1. Start with the *Read these first* lists above — that is where the two models actually diverge.
2. Open the per-category sheet and fill in the HUMAN REVIEW NOTES table for those cases.
3. Then sample a handful of agreeing cases, to check that agreement reflects genuine quality rather than both models being vague.
4. Record a verdict per category. A small sample cannot establish production-readiness however good the output looks.
