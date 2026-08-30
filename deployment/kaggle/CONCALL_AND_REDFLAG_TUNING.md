# Concall retry-budget test + Red Flag instance-check test

**EXPERIMENTAL / NOT PRODUCTION.** Qwen only — Ministral is shelved
(founder decision). No production-readiness declaration either way; the
founder decides after reading these numbers.

Both tests ran on the SAME 20-case `concall_benchmark.json` / 60-case
`red_flag_benchmark.json` used throughout this project, sharing one Qwen
load in a single Kaggle kernel. GPU: 20.9 min (concall) + 1.3 min
(red_flag) generation, 30.5 min kernel total including load.

---

## PART 2 — Concall retry budget: a clean 20/20

### The setup

Production prompt, **unmodified**. The already-committed improved retry
policy (temperature/seed variation on retries, directive corrective
notes). Retry budget raised from production's 3 to **8**. Nothing else
changed — isolating budget size as the one new variable.

This specifically was NOT tested before: the earlier `retries_6` result
(repaired 2/5) ran under the OLD deterministic-retry mechanics, where
every attempt was `temperature=0` and a retry mostly reproduced attempt
1's rejected text verbatim (confirmed: similarity 1.000 in that
measurement). That answered "does budget help when retries are
identical" — a different question from "does budget help now that
retries genuinely differ" (confirmed last session: similarity 0.04–0.36
under the fix). This test answers the second question directly.

### Result

| | Generated | Compliance fails | Tone agreement | Lexical overlap |
|---|---|---|---|---|
| baseline (3 attempts, old mechanics) | 15/20 | 5 | 0.7333 | 0.2333 |
| retry fix (3 attempts) | 17/20 | 3 | 0.7059 | 0.2575 |
| **retry fix + 8-attempt budget** | **20/20** | **0** | 0.75 | **0.2975** |

**Every one of the previously chronic failures now passes**, confirmed
from the raw attempt log, not just the pass/fail count:

| Case | Attempts used | What happened |
|---|---|---|
| CC_KANPRPLA | 4 of 8 | expected → outlook → expected → **pass** |
| CC_SDBL | 4 of 8 | expected → target → expected → **pass** |
| CC_KIRIINDUS | 5 of 8 | expected → expected → targeting → expected → **pass** |
| CC_MANYAVAR | 3 of 8 | targeting → outlook → **pass** |
| CC_PNB | 2 of 8 | targets → **pass** |

No case needed the full budget — the maximum used was 5 of 8 attempts.
Attempt text is genuinely different each time (visible directly in the
rejection log's quoted reasons — the model trips a *different* forbidden
word almost every attempt, the "whack-a-mole" pattern already diagnosed
last session), and the eventual passing text is substantive, non-empty,
company-specific content — not a degenerate fallback.

### Read against the noise floor

The prior sessions' deltas (+1 for annual_report, +2 for concall at
3 attempts) were shown to sit inside a measured single-comparison
disagreement of up to 7/20. **This result does not have that problem.**
Going from a best-ever prior score of 17/20 to a clean 20/20 is a larger
jump than any noise-floor disagreement measured so far on this hardware,
and every one of the 5 previously-failing cases is individually
traceable to a specific, different rejection reason resolving within a
bounded number of attempts — this is not a count moving by chance, it is
a mechanism (more genuine chances at temp/seed-varied phrasing) working
on every case it was supposed to help.

**Caveat stated plainly, per this session's own discipline:** this is
still a single run (n=1) — no repeat-run study exists for this budget
either, and Part 1 of this session already established that the proper
noise-floor measurement (3–5× repeat) has never been done for anything in
this project. The magnitude here makes "this is pure noise" implausible,
but "confirmed at the standard of a repeated-trial measurement" is a
claim this session cannot make for any result, including this one.

**Cost:** attempts-used histogram was `{1: 14, 2: 2, 3: 1, 4: 2, 5: 1}` —
most cases still pass on attempt 1; the extra budget only engages when
needed. Total latency for 20 cases: 20.9 minutes (62.8s/case mean),
comparable to the 3-attempt run's 60.5s/case — the budget increase did not
meaningfully increase cost because so few cases used it.

---

## PART 3 — Red Flag instance-check: fixed all 7 false positives, at a severe cost

### The setup

All 7 false positives from the n=60 baseline were checked individually,
not assumed to share one cause:

| Pattern | Cases | Description |
|---|---|---|
| A — policy boilerplate | BAJFINANCE-488, CIPLA-507, GRASIM-922, PFC-700 (4) | Ind-AS 37 "Provisions and Contingent Liabilities" accounting-policy note, near-verbatim across most Indian annual reports, no actual instance disclosed |
| B — genuine Key Audit Matter | GODREJCP-432, PFC-439 (2) | Real, company-specific KAM text — NOT boilerplate. gpt-4o-mini itself flags a structurally similar KAM elsewhere (ONGC-547), so a blanket "KAM ≠ qualification" rule was deliberately NOT written, to avoid an expected regression |
| C — keyword in unrelated list | HINDALCO-764 (1) | "Contingent liabilities" named only as one bullet among several dividend-policy factors, never elaborated |

One instruction was added distinguishing a policy **description** from an
actual disclosed **instance**, using the real BAJFINANCE-488 boilerplate
text (harvested verbatim from the fixture) as the negative example. The
instruction deliberately avoided naming Key Audit Matters as categorically
excluded, for the Pattern B reason above.

### Result — false positives eliminated, false negatives exploded

| | agree | agree_no_flag | false_negative | false_positive | agreement rate |
|---|---|---|---|---|---|
| baseline | 38 | 13 | 2 | 7 | **0.85** |
| + instance-check line | 12 | 19 | **28** | 1 | **0.5167** |

**All 7 original false positives were fixed** — including, contrary to
the pre-test prediction, the 2 genuine-KAM cases (Pattern B) and the
keyword-coincidence case (Pattern C), not just the 4 boilerplate cases
(Pattern A) the instruction was designed for. One new false positive
appeared elsewhere (ASIANPAINT-679 — a case the model now confirms that
gpt-4o-mini itself left unflagged; a single, minor, likely-borderline
case next to the scale of what follows).

**But 26 previously-correct flags flipped to false negatives** —
`agree` fell from 38 to 12. Broken down by the reference category that
was missed:

| Category | New false negatives |
|---|---|
| auditor_qualification | 9 |
| related_party_transaction | 6 |
| promoter_pledge | 6 |
| contingent_liability | 5 |

Confirmed from raw output, this is exactly the risk flagged before running
the test: the instruction's "RIGHT" example for `auditor_qualification`
named only "actually qualified/adverse/disclaimed" opinions and material
weaknesses — which implicitly excluded ordinary Key Audit Matters, even
though gpt-4o-mini legitimately confirms them. Two concrete regressions:

- **RF_ABB-277** — reference (gpt-4o-mini) confirms `auditor_qualification`
  for a KAM about revenue recognition judgment. Before: Qwen correctly
  agreed. After: Qwen returned no category — *"model returned no category
  (genuine non-match)"*.
- **RF_HDFCBANK-766** — reference confirms `auditor_qualification` for a
  KAM about investment valuation/impairment. Same regression.

The false-negative spike was not confined to `auditor_qualification` —
`related_party_transaction`, `promoter_pledge` and `contingent_liability`
all regressed too, meaning the instruction's general framing ("confirm
ONLY if the excerpt discloses an ACTUAL, SPECIFIC instance") made the
model dramatically more conservative across every category, not just the
one it was aimed at.

### Plain interpretation

**This is a large net regression, not a fix, and should not be adopted
as written.** Overall agreement fell from 0.85 to 0.5167. Trading 6 net
false positives (7 fixed, 1 new) for 26 new false negatives is the wrong
direction for a risk-flagging feature, where missing a genuine disclosure
is normally the costlier error.

The instruction over-generalized: telling the model to require an "ACTUAL
SPECIFIC instance" and giving narrow positive examples caused it to reject
far more genuine instances than the small number of boilerplate false
positives it was meant to filter out. The lesson generalizes something
already seen this session with concall's markdown/steering prompts:
**a single added instruction can have a much larger and more diffuse
effect on model behaviour than its author intends**, and testing narrowly
against only the known failure cases (as the 4/7 prediction implicitly
assumed) would have missed this — the regression only shows up when
re-scoring the FULL 60-case set, including the 51 cases that were already
correct.

**Not attempted here, and worth naming as the more promising next step:**
a narrower instruction that keeps the policy-vs-instance distinction ONLY
for `contingent_liability` (where it demonstrably helped without
apparent cost — Pattern A, all 4 fixed) while leaving
`auditor_qualification` untouched or handled by a separate, more careful
rule that explicitly preserves ordinary Key Audit Matters as
confirmable. That is a real next experiment, not a claim this session
tested it.

---

## GPU cost, this session

| Phase | Time |
|---|---|
| Failed staleness-guard kernel (own bug, caught before any GPU load) | ~1.0 min |
| Concall retry-budget (20 cases) | 20.9 min generation |
| Red_flag instance-check (60 cases) | 1.3 min generation |
| Kernel overhead (load, install) | 8.3 min |
| **This session total** | **31.5 min** |

**Cumulative across all sessions to date:** Actions 1–3 (77 min) +
Ministral preflight/eval (~102 min) + concall markdown-fairness (61.2
min) + this session (31.5 min) = **~271.5 min (~4.53 GPU-hours)**.

Kaggle's remaining weekly quota is not queryable through this session's
API access (no such endpoint exists in the `kaggle` package) — check the
Kaggle notebooks/GPU-quota page directly for the current balance.

---

## Bottom line, no verdict implied

- **Concall retry-budget (8 attempts): a strong, real result** — 20/20,
  every prior chronic failure resolved, with a traceable per-case
  mechanism. The single-run caveat applies, as it does to every result in
  this project, but the effect size here is well outside anything seen
  from noise alone.
- **Red_flag instance-check: a clear net regression** — do not adopt.
  Fixed the false positives it targeted (and more) but broke 26 genuine
  flags in doing so. A narrower, category-scoped version is the logical
  next experiment, not yet run.

Neither category is declared production-ready by this document. That
judgement, and any decision to adopt the retry-budget change or attempt a
narrower red_flag fix, is the founder's.
