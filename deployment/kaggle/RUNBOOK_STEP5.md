# STEP 5 — annual-report reference + the retry-loop fix

**EXPERIMENTAL / NOT PRODUCTION.** Nothing in this step declares any
category production-ready. That call belongs to the founder after reading
the updated review sheets.

Scope is **annual report and concall only**. Red Flag is excluded on
purpose — its problem is discernment and content selection, not retry
mechanics, and it is deferred to its own session. Ask AI is out of scope
for the Qwen migration entirely and stays on OpenAI.

---

## ACTION 1 — the annual-report reference was not real, and now is

### The problem

Measured against production on 2026-08-28:

| | |
|---|---|
| `annual_reports` documents | 8,354 |
| …with any summary at all | 72 |
| …with **current-schema** output | **0** |

Every stored summary is legacy-shaped (`summary` / `bullets` /
`key_takeaway`), written 2026-08-16, before the pipeline was rewired
through Evidence Finder. Not one document carries `executive_summary`,
`key_points`, `important_risks` or `evidence_tokens`.

So for all 20 sample cases the review sheet was comparing Qwen's
current-schema output against a ~150-character legacy stub produced from
*different input*. That is not a weak comparison — it is not a comparison.
It is why the sheet carried a caveat banner instead of a verdict.

### The fix

`scripts/regenerate_annual_report_reference.py` runs the same 20 benchmark
cases through gpt-4o-mini on the **current** prompt with the **same**
evidence block the benchmark hands Qwen, under **production** retry
mechanics — deliberately not the improved policy, so the reference is not
generated under friendlier conditions than the output it judges.

```bash
python scripts/regenerate_annual_report_reference.py --dry-run   # price it
python scripts/regenerate_annual_report_reference.py --apply     # run it
python scripts/apply_new_reference.py                            # re-score
```

The key is read into the shell for the single command and never written to
disk; the script refuses to read a `.env`.

### Result

| | |
|---|---|
| Generated | **20 / 20** |
| Tokens | 298,443 in / 5,963 out |
| **Actual cost** | **$0.0483** |
| Estimate quoted to founder | $0.07 |
| Verdict | **under estimate — no flag** |

Cost is computed from the API's own `usage` counts, not estimated
afterwards.

**Side-finding worth keeping:** gpt-4o-mini itself needed a second attempt
on **6 of 20** cases (LT, INFY, CHOLAFIN, BAJFINANCE, SBILIFE, JIOFIN). It
trips this validator too. It just recovers.

### Effect on the comparison

`scripts/apply_new_reference.py` swaps the reference in and re-scores. **No
GPU was spent and no candidate output was touched** — the candidate column
of the re-rendered sheet is byte-identical to the one already reviewed.

| Signal | Before | After |
|---|---|---|
| `reference_schema_matches_replay` | **0 / 20** | **20 / 20** |
| Mean lexical overlap | 0.0578 | 0.2512 |
| Reference chars (typical) | ~150 | ~1,300 |
| `reference_compliance_failures` | 0 | **0** |
| Qwen `generated_ok` | 17 / 20 | 17 / 20 *(unchanged, by design)* |

All 20 regenerated references pass the compliance validator. Combined with
the same finding on concall, **the validator is well calibrated for both
categories** — a Qwen failure is a real failure, not a miscalibrated rule.

The three cases at 0.0 overlap (VEDL, CHOLAFIN, BAJFINANCE) are exactly the
three where Qwen generated nothing. Consistent, not a new signal.

> The regenerated reference is a **replay**, not the text production
> actually stored. Production stored nothing in this schema. It is the
> right baseline for judging the model, and it is not evidence about what
> production has historically shown users.

---

## ACTION 2 — the retry-loop fix

### What the loop did wrong

`app/tasks/retry_policy.py` carries the full account. In short: on a
compliance rejection the loop re-ran the generation and collected the same
failure.

**A correction to the original diagnosis, from re-reading the run
artifacts.** Retries were *not* uniformly identical. The corrective note
changes the prompt, so attempt 2 usually differed substantially
(similarity 0.09–0.26). The identical regenerations happen specifically
when the **rejection reason repeats**: same reason → byte-identical prompt
→ temperature 0 reproduces the output exactly. That is CHOLAFIN 2→3 at
similarity **1.000** and KANPRPLA 2→3 at **1.000**.

So "every retry was identical" was too strong. The fix is still aimed
correctly — a shifted seed breaks that tie, and a note quoting the
*specific clause* differs even when the rule name does not — but the
dominant concall pattern is something else: the model trips **different**
forbidden words on each attempt (KIRIINDUS: `expected` → `targeting` →
`will`; MANYAVAR: `targeting` → `outlook` → `predictions`). That is
content selection, not repetition, which is what change 3 targets.

### The three changes

1. **Vary sampling on retry.** Attempt 1 stays `temperature=0` with the
   caller's seed, so the baseline stays reproducible and comparable to the
   17/20 and 15/20 runs. From attempt 2, temperature 0.4 and a shifted
   seed. The shift is deterministic (`seed + (attempt-1)*1000`), so a
   re-run of the whole benchmark still reproduces exactly.

2. **Directive corrective feedback.** The note used to be the validator's
   own message (`forward-tense word 'expected'`) — naming the rule but
   neither the offending text nor the remedy. It now locates and quotes
   the rejected sentence and says what to do with it.

3. **Concall content-preference steering** (`concall_steered_v2`). Steers
   *what to report* before *how to phrase it*: fill the summary from
   reporting-period facts first, and include forward material only
   abstracted and attributed. Every framing it teaches was harvested from
   the 20 production gpt-4o-mini references by filtering for forward
   intent **and** passing `summarizer_violation()` — `highlighted` (15),
   `noted` (6), `aiming` (3), `on schedule` (2), `set a goal of` (2). A
   test asserts each exemplar really passes, so the prompt cannot teach
   phrasing that fails.

### Safety of the change

`PRODUCTION_POLICY` is the default everywhere. Nothing changes unless a
caller opts in, and the policy is recorded in each run JSON with an
explicit `like_for_like_with_reference` flag.

> **A result under the improved policy is NOT like-for-like with
> gpt-4o-mini**, which was measured under production mechanics. If the
> improved policy is what closes the gap, the fair remedy is adopting it
> in RedixFi **for both models**, not keeping it as a Qwen-only crutch
> that quietly changes what is being measured.

---

## ACTION 3 — the re-test

Same fixture files as the baselines, so the numbers are directly
comparable. Three phases on one loaded model:

| Phase | Prompt | Retry policy | Isolates |
|---|---|---|---|
| annual_report (20) | production | improved | the retry fix |
| concall (20) | production | improved | the retry fix |
| concall steered (20) | `concall_steered_v2` | improved | the prompt, on top |

```bash
python <dataset>/llm_project/deployment/kaggle/kaggle_run.py \
    --fixtures <dataset-root> \
    --jobs annual_report_benchmark.json:annual_report_summary,\
concall_benchmark.json:concall_summary \
    --retry-policy improved \
    --concall-steered
```

The kernel runs a **staleness guard** first: it asserts the mounted dataset
actually contains the fix and prints a fingerprint of each file. An earlier
run cost real GPU time to a stale copy executing on Kaggle while the fix
sat in the local repo, and the traceback pointed at a line number that no
longer existed in committed code. The guard now fails in seconds rather
than quietly re-measuring old behaviour and reporting it as new.

### Analysing the result

```bash
python scripts/diagnose_retry_fix.py --before <baseline.json> --after <new.json>
```

It reports count deltas, classifies every still-failing case as *still
repeating* / *different text same rule* / *new reason*, and **spot-checks
from the recorded raw generations** that attempt-2+ text really differs —
read from the artifact, never inferred from the fact that a temperature
was set.

### RESULTS

_Filled in when the run lands. Baselines to beat: annual_report **17/20
generated, 3 compliance failures**; concall **15/20 generated, 5 compliance
failures, tone agreement 0.7333**._

---

## Known next refinement, if annual report does not move

All 3 annual-report failures are the **financial-figure** rule
(`22%`, `19%`, `rs,`), not forward tense. That rule bans the *quantity
itself* — the prompt's own remedy is "describe direction or theme in words
only" — and the regenerated gpt-4o-mini references comply by staying
entirely qualitative.

The directive note currently gives a generic "remove that term" for this
case rather than the prompt's specific remedy. If the annual-report number
does not move, that is the first thing to fix, and it is a prompt-side
change, not a model verdict.
