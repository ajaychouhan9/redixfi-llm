# STEP 4 — guided (structured) decoding

**Problem this fixed.** The first GPU run recorded `json_repair_used = True`
on **all 15 cases**. `VLLMInProcessBackend` accepted `json_mode` on the
request and then silently dropped it, so every response was free-form text
salvaged afterwards by `parse_json_object`. Production's reference path uses
OpenAI JSON mode, so the eval compared **content but not output shape** — and
post-hoc repair on every call does not scale to a bulk backfill of ~1,972
annual reports, ~1,343 concalls and red-flag classification over the same
corpus.

## STATUS

| Step | Result |
|---|---|
| Implementation | done — commit `5609895` |
| **Smoke run (4 cases, 1/category)** | **✅ DONE and PASSED, 2026-08-28** — commit `fd9fc31` |
| **15-case re-run** | **← next action, not yet run** |
| 130-case full eval | still deliberately deferred |

The smoke run already answered the question this runbook's old "Run this
FIRST" section asked. Its scorecard, for the record:

```
structured_output_used : 4/4
json_repair_used       : 0/4      (was 15/15 before this fix)
guided_and_clean       : 4/4
guided_but_repaired    : 0
unguided               : 0
VERDICT: guided decoding is WORKING on this hardware.
```

No xgrammar fallback warnings appeared in the engine log; all four
categories reported `structured_output_mode='json_schema'`. **Skip straight
to the 15-case run below** — re-running the smoke test again is not
necessary, though harmless if you want to reconfirm.

## What changed

| | |
|---|---|
| vLLM version | **0.28.0** (from the run's own engine banner) |
| API used | `SamplingParams(structured_outputs=StructuredOutputsParams(json=<schema>))` |
| Import | `vllm.sampling_params` — **not** re-exported from `vllm/__init__.py` |
| Backend | `structured_outputs_config` reports `backend='auto'` → xgrammar |

`guided_json` / `guided_decoding_backend` / `GuidedDecodingParams` are
**entirely removed** in 0.28.0. Writing to them from memory would have
raised — the API was confirmed against the v0.28.0 source, not recalled.

Five schemas added in `app/schemas/output_schemas.py`, one per task. All are
xgrammar-safe: no `multipleOf`, `uniqueItems`, `contains`,
`patternProperties`, `propertyNames`, or unsupported string `format`
(verified against `has_xgrammar_unsupported_json_features` at the v0.28.0
tag). `minItems`/`maxItems` are *not* on that list, so the annual-report 3–5
bullet bound is expressible without forcing a backend switch.

`red_flag` is the one **dynamic** schema: `category` is an enum built from
*that chunk's* keyword candidates plus `null`, mirroring the task's own
rejection rule.

`parse_json_object` is **kept as a fallback** and `json_repair_used` still
reported — the goal is to make repair unnecessary and *prove* it, not to
hide it.

## THE NEXT ACTION — the 15-case re-run

**No code change was needed to enable this.** `kaggle_run.py` uses the
`*_sample15.json` fixtures by default (no flag required) — `--smoke` is
opt-in only and limits each category to 1 case. Omitting it, as below,
already runs the full 15 (AR 3 / concall 3 / red_flag 6 / ask_ai 3) — the
**exact same 15 cases, from the exact same fixture files**, as the original
2026-08-28 evaluation. That identity is what makes this a genuine
like-for-like re-measurement rather than a new sample.

```python
!mkdir -p /kaggle/working/LLM
!tar xzf /kaggle/input/redixfi-llm-fixtures/llm_project.tar.gz -C /kaggle/working/LLM
```

```python
!python /kaggle/working/LLM/deployment/kaggle/kaggle_run.py \
    --fixtures /kaggle/input/redixfi-llm-fixtures
```

Download before the session ends:

```python
!cd /kaggle/working/LLM && zip -r /kaggle/working/eval_results.zip evaluation/
!cp /kaggle/working/kaggle_run_state.json /kaggle/working/
```

## What to check when results come back (do not pre-judge this now)

Compare against the original run (`evaluation/*/runs/*20260828T14*` /
`*20260828T09*`, commit `900aa80`), category by category:

| Signal | Original (unguided) | This run |
|---|---|---|
| `json_repair_used` (all 15) | 15/15 | should be **0/15** — the smoke run's 0/4 was n=4; this is the real sample size |
| `annual_report_summary` generated_ok | 1/3 | ? |
| `red_flag` agreement | 4/6 (2 false negatives) | ? |
| `concall_summary` tone agreement | 2/3 | ? |
| `ask_ai` refusal agreement | 2/3 | ? |

**If the annual_report/red_flag numbers improve**, the earlier failures were
at least partly shape/parsing artifacts of unguided decoding. **If they hold
steady**, that is real evidence the two known gaps (BEL's `target`/`88%`
miss, the auditor_qualification and promoter_pledge false negatives) are
genuine model limitations, not decoding noise — which is exactly the
question this re-run exists to answer. Either way, do not fix or tune
anything based on a single re-run; that is a separate, later step.

## What is NOT in scope this step

- **The full 130-case eval.** Deliberately sequenced after this re-run, so
  quality numbers are not contaminated by shape artifacts.
- **The two known quality gaps** — BEL's `target`/`88%` miss and the 2
  red-flag false negatives (auditor_qualification, promoter_pledge). Real
  and worth fixing, but tuning prompts while the shape/quality question is
  still being separated means not knowing which variable moved the result.
  **Explicitly deferred**, including through this re-run — it re-measures
  with the SAME prompts and validators, nothing about those two cases'
  logic was touched.

## Honest limits of the offline verification

Proven locally (97 tests): schema validity, xgrammar safety, that a
schema-shaped payload survives each real parser with every field populated,
that every task passes its schema to the backend, that the vLLM call is
built as `structured_outputs=StructuredOutputsParams(json=...)` (against a
stub of the 0.28.0 signature), and that telemetry separates *guided and
clean* from *guided but repaired*.

**Not provable off-GPU:** that `json_repair_used` reaches 0 at the full
15-case sample size (only 4 cases were sampled by the smoke run), and
whether the annual_report/red_flag quality numbers move. That is exactly
what this re-run exists to establish.

## Appendix — the smoke run command, for reference / re-confirmation

```python
!python /kaggle/working/LLM/deployment/kaggle/kaggle_run.py \
    --fixtures /kaggle/input/redixfi-llm-fixtures --smoke
```

| Symptom (if you re-run this) | Meaning |
|---|---|
| `unguided` > 0 | the schema never reached the engine — vLLM lacks the kwarg, or `StructuredOutputsParams` did not import |
| `guided_but_repaired` > 0 | the grammar engaged but output still needed repair — likely an xgrammar fallback, check the engine log for the resolved backend |
| generation failures spike | the grammar may be over-constraining; check `rejections` for `invalid_json` |
