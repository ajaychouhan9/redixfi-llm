# Actions 1–3, in full — and a correction to the record

**Read this before trusting any number from Actions 1–3.** The retry-fix
re-test was compared against a methodology description ("5-repeat runs on
10 selected cases", "Set A / Set B with different stocks") that does not
match what was actually run. This document says plainly what was done,
what was not, and what can honestly be concluded from what exists.

---

## What "the noise floor" actually is — and isn't

**What exists:** exactly TWO full runs per category — the original
baseline and the single retry-fix re-test — each on the SAME 20
`annual_report_benchmark.json` / `concall_benchmark.json` cases, at
identical settings (`temperature=0.0`, `seed=0` for attempt 1). Comparing
attempt-1 output between those two runs (n=2 samples per case, not 5):

| | attempt-1 output differed | attempt-1 pass/fail **flipped** |
|---|---|---|
| annual_report | 4 / 20 | 1 |
| concall | 7 / 20 | 3 |

**What does NOT exist:**

- **No 5-repeat study.** No fixture was run 5 times to build a
  distribution. The "±1–3 cases" noise-floor figure quoted throughout
  `MINISTRAL_EVAL.md`, `CONCALL_MARKDOWN_FAIRNESS.md` and
  `REVIEW_INDEX.md` is an estimate from a SINGLE before/after pair, not a
  measured spread across repeats.
- **No Set A / Set B split.** There is one `annual_report_benchmark.json`
  (20 cases) and one `concall_benchmark.json` (20 cases) in this project,
  full stop — confirmed by listing `fixtures/*.json`. The retry-fix
  re-test used the SAME 20+20 cases as the original baseline, not a
  same-stocks "Set A" plus a different-stocks "Set B". No second,
  new-stock fixture was ever created or run.
- **This was known and flagged, not missed silently.** `RUNBOOK_STEP5.md`'s
  own "Next steps" section, written at the end of that session, lists as
  item 1: *"Establish the noise floor properly before trusting any further
  delta: run the same fixture 3× unchanged and record the spread. Every
  conclusion below depends on knowing it."* That step was never executed
  before attention moved to the Ministral comparison.

So Part 1's items 1–3 as specified (a 5-repeat noise floor measurement,
a Set A retest, a Set B retest) were **not completed**. What follows is
what the simpler, already-completed two-run comparison actually shows —
which is weaker evidence than the terms "noise floor measurement" and
"Set A/B retest" imply, and should be read accordingly.

---

## The two-run comparison that DOES exist

| Run | Generated | Compliance fails | Tone agreement |
|---|---|---|---|
| annual_report **baseline** | 17 / 20 | 3 | — |
| annual_report **+ retry fix** | 18 / 20 | 2 | — |
| concall **baseline** | 15 / 20 | 5 | 0.7333 |
| concall **+ retry fix** | 17 / 20 | 3 | 0.7059 |

("+ retry fix" = varied sampling on retry + directive corrective notes;
content steering was tested separately, made concall worse — 14/20 — and
was reverted, not carried into any later run.)

Both deltas (+1 for annual_report, +2 for concall) are the same size as,
or smaller than, the disagreement already observed between two runs with
**no change applied at all** (4/20 and 7/20 differing, 1 and 3 flipping).
A change and no-change both produce deltas in the same range.

### The honest verdict, per category, stated plainly

**annual_report: inconclusive.** A +1 improvement (17→18) sits inside a
measured single-comparison disagreement of 4/20 with 1 flip. This is not
distinguishable from noise with the evidence that exists. Not confirmed
as an improvement; not confirmed as no-improvement either — genuinely
unresolved.

**concall: inconclusive, leaning toward "the fix is not doing nothing" but
short of confirmed.** A +2 improvement (15→17) sits inside a measured
disagreement of 7/20 with 3 flips, so the count alone is not proof.
However, two things push this past pure noise-floor ambiguity, WITHOUT
constituting confirmation:

1. The retry text itself is not noise — attempt-2 text differs from
   attempt-1 with similarity 0.04–0.36 under the fix, against 1.000
   (byte-identical) under the old mechanics. The MECHANISM change is
   real and measured directly from raw generations, independent of the
   pass/fail count.
2. `AR_BAJFINANCE`'s directive note was followed literally — "a 22%
   increase in consolidated AUM to C 509,975 crore" became "crossing a
   major milestone in consolidated AUM" after the note quoted the
   rejected clause. That is a specific, traceable causal link from the
   fix to a specific repair, not just a count moving.

So: **the mechanism is confirmed working as designed. Whether it reliably
moves the pass-rate at n=20 is still not established**, and a proper
answer needs the repeated-run study that was never done. Do not read
"15→17" as proof by itself.

**What would actually resolve this:** run the SAME 20-case fixture 3–5×
unchanged (no code change between runs) to measure the TRUE spread, then
compare that spread to the retry-fix delta. This was recommended at the
end of the prior session and has still not been done. It was not
attempted in this session either — Part 2 and Part 3 below spend the
available GPU time on new prompt/retry-budget experiments instead, per
this session's explicit brief (no new noise-floor work, no Set A/B
repeat).

---

## Why this correction matters

Reporting "±1–3 cases is the noise floor, so the retry fix's +1/+2 improvements
sit inside it" was accurate as far as it went, but describing that finding
with the vocabulary of a rigorous methodology it never was ("5-repeat",
"Set A/Set B") risked the number being trusted more than the underlying
evidence supports. The actual evidence is a single before/after
comparison — weaker than a repeated-trial measurement, though not
nothing, and it happens to point the same direction (inconclusive) either
way. Stating the methodology precisely, not just the number, is the point
of this correction.
