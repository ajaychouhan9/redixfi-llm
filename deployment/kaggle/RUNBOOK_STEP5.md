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

| Run | Generated | Compliance fails | Tone agreement |
|---|---|---|---|
| annual_report **baseline** | 17 / 20 | 3 | — |
| annual_report **+ retry fix** | **18 / 20** | **2** | — |
| concall **baseline** | 15 / 20 | 5 | 0.7333 |
| concall **+ retry fix** | **17 / 20** | **3** | 0.7059 |
| concall **+ retry fix + steering** | **14 / 20** | **6** | 0.7857 |

GPU: **68.9 min** of generation (44.9 benchmark + 24.0 steered), 77 min
total kernel wall time including install and model load. 67.3 s/case.
`json_repair_used` 0/40, `guided_and_clean` 40/40 — guided decoding held.

### ⚠️ The finding that governs how to read the table above

**Generation on this hardware is not reproducible run-to-run, even at
`temperature=0` with a fixed seed.** Attempt 1 uses identical settings and
an identical prompt in every run, so it should be byte-identical. It is
not. Re-running the same fixtures:

| | attempt-1 output differed | attempt-1 pass/fail **flipped** |
|---|---|---|
| annual_report | 4 / 20 | **1** |
| concall | 7 / 20 | **3** |

The likely cause is continuous batching and non-deterministic reduction
order across the two T4s, not the sampling settings.

**So the improvements — annual report +1, concall +2 — sit inside the
noise floor of the measurement.** They are the right direction, and they
are not evidence of a real gain at n=20. Anyone reading `17 → 18` as "the
fix works" is reading noise. Establishing a real effect needs repeated
runs, or a larger fixture, or both.

`CC_ALKYLAMINE` illustrates this directly: it passed on attempt 1 in the
baseline and failed on attempt 1 in the re-test, under identical settings.
That regression is nondeterminism, not the change.

### What IS established, independent of the counts

The mechanism does what it was built to do, confirmed from recorded raw
generations rather than assumed:

* Attempt 1 recorded `temperature=0.0, seed=0`; attempt 2 recorded
  `temperature=0.4, seed=1000`, exactly as designed.
* Retry text is genuinely different — similarity 0.04–0.36 across sampled
  cases, against the 1.000 identical regenerations seen in the baseline.
* The directive note is obeyed literally. AR_BAJFINANCE attempt 1 wrote
  *"a 22% increase in consolidated AUM to C 509,975 crore"*; after the note
  quoted that clause, attempt 2 wrote *"crossing a major milestone in
  consolidated AUM"* — figure removed, meaning kept.

### Content steering (change 3) made things WORSE — reported as measured

17 → 14 generated, 4 newly failing against 1 repaired. That is a larger
delta than the noise floor in the unfavourable direction, so unlike the
improvements it is unlikely to be pure noise. Tone agreement did rise
(0.7059 → 0.7857) and latency rose 13 s/case on the longer prompt.

The steering partly worked: SIGACHI produced *"the Dahej-2 capacity
expansion is progressing on schedule, aiming to elevate total MCC capacity
to 30,000 MTPA"* — almost exactly the taught exemplar. It then tripped
`target` elsewhere in the same summary.

**Leading hypothesis — negation priming.** Forbidden-word mentions in the
system prompt track with failures in the wrong direction:

| Prompt | Chars | Forbidden-word mentions | Result |
|---|---|---|---|
| production | 2,370 | 14 | 15/20 → 17/20 with retry fix |
| `concall_fewshot_v1` | 3,920 | 27 | repaired 1 of 5 |
| `concall_steered_v2` | 5,709 | 28 | **14/20** |

Every prompt that teaches the rule by *naming* the banned vocabulary and
showing WRONG examples appears to raise that vocabulary's probability.
This is correlational across three prompts at n=20 with known
nondeterminism — a hypothesis, not a result. The testable next version
teaches **only** the positive constructions and never enumerates a
forbidden word.

---

## Next steps, in the order the evidence supports them

1. **Establish the noise floor properly** before trusting any further
   delta: run the same fixture 3× unchanged and record the spread. Every
   conclusion below depends on knowing it.
2. **Positive-only steering prompt** — the priming hypothesis is the
   clearest lead and is cheap to test.
3. **Financial-figure directive note.** Both remaining annual-report
   failures are that rule (`rs,`, `22%`), not forward tense. It bans the
   quantity itself; the prompt's own remedy is "describe direction or
   theme in words only", and the regenerated gpt-4o-mini references comply
   by staying entirely qualitative. The note currently gives a generic
   "remove that term" instead of that specific remedy.

None of this makes either category production-ready, and this document
does not claim it. That judgement is the founder's after reading the
sheets.
