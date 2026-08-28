# STEP 4 — guided (structured) decoding

**Problem this fixes.** The first GPU run recorded `json_repair_used = True`
on **all 15 cases**. `VLLMInProcessBackend` accepted `json_mode` on the
request and then silently dropped it, so every response was free-form text
salvaged afterwards by `parse_json_object`. Production's reference path uses
OpenAI JSON mode, so the eval compared **content but not output shape** — and
post-hoc repair on every call does not scale to a bulk backfill of ~1,972
annual reports, ~1,343 concalls and red-flag classification over the same
corpus.

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

## Run this FIRST — the smoke run (4 cases, one per category)

```python
!python /kaggle/working/LLM/deployment/kaggle/kaggle_run.py \
    --fixtures /kaggle/input/redixfi-llm-fixtures --smoke
```

Read the **GUIDED DECODING SCORECARD** in step 11:

```
structured_output_used : 4/4      <- schema reached the engine
json_repair_used       : 0/4      <- TARGET 0
guided_and_clean       : 4/4      <- TARGET = case count
guided_but_repaired    : 0        <- non-zero => grammar not holding
unguided               : 0        <- non-zero => schema never reached the engine
VERDICT: guided decoding is WORKING on this hardware.
```

**Do not proceed to the full run unless `guided_and_clean` equals the case
count.** The three failure signatures and what each means:

| Symptom | Meaning |
|---|---|
| `unguided` > 0 | the schema never reached the engine — vLLM lacks the kwarg, or `StructuredOutputsParams` did not import |
| `guided_but_repaired` > 0 | the grammar engaged but output still needed repair — likely an xgrammar fallback, check the engine log for the resolved backend |
| generation failures spike | the grammar may be over-constraining; check `rejections` for `invalid_json` |

## Then the 15-case run (only after the smoke run is clean)

```python
!python /kaggle/working/LLM/deployment/kaggle/kaggle_run.py \
    --fixtures /kaggle/input/redixfi-llm-fixtures
```

## Download before the session ends

```python
!cd /kaggle/working/LLM && zip -r /kaggle/working/eval_results.zip evaluation/
```

## What is NOT in scope this step

- **The full 130-case eval.** Deliberately sequenced after guided decoding
  is confirmed, so quality numbers are not contaminated by shape artifacts.
- **The two known quality gaps** — BEL's `target`/`88%` miss and the 2
  red-flag false negatives (auditor_qualification, promoter_pledge). Real
  and worth fixing, but tuning prompts while shape is unreliable means not
  knowing which variable moved the result. **Explicitly deferred.**

## Honest limits of the offline verification

Proven locally (97 tests): schema validity, xgrammar safety, that a
schema-shaped payload survives each real parser with every field populated,
that every task passes its schema to the backend, that the vLLM call is
built as `structured_outputs=StructuredOutputsParams(json=...)` (against a
stub of the 0.28.0 signature), and that telemetry separates *guided and
clean* from *guided but repaired*.

**Not provable off-GPU:** that xgrammar actually constrains decoding on
T4 / AWQ / TP=2, and that `json_repair_used` genuinely reaches 0 on real
generations. That is exactly what the smoke run exists to establish.
