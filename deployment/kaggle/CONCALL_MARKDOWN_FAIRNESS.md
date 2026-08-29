# Concall markdown-fairness test — Qwen vs Ministral

**EXPERIMENTAL / NOT PRODUCTION.** Scope is concall only, per instruction.
Annual_report and red_flag are not re-touched — those decisions stand.

**This document lays out numbers, not a recommendation.** Whether the
markdown finding changes anything about Ministral for concall is the
founder's call.

## What changed

ONE line added to the concall system prompt, applied identically to both
models, at production retry policy (no sampling variation, no directive
notes, no content steering — the same settings as the original head-to-head
eval):

> "ABSOLUTE FORMATTING RULE: your response must be PLAIN TEXT ONLY. Do NOT
> use asterisks, bold, italics, underlines, headers, bullet points,
> numbered lists, or any markdown formatting of any kind, anywhere in your
> response — including inside the JSON string values."

Both models ran the identical 20 `concall_benchmark.json` cases used in
the head-to-head eval. Two separate Kaggle kernels (one model per kernel;
they cannot share a loaded engine) — Qwen first, Ministral second.

## Results

| | Qwen — before | Qwen — after | Ministral — before | Ministral — after |
|---|---|---|---|---|
| Markdown present | 0/20 | 0/20 | **15/20** | **0/20** |
| Generated | 15/20 | 15/20 | 15/20 | **13/20** |
| Compliance failures | 5 | 5 | 5 | **7** |
| Tone agreement | 0.7333 | 0.80 | 0.6667 | 0.7692 |
| Lexical overlap | 0.2333 | 0.2434 | 0.206 | 0.2031 |

("Before" numbers are the existing head-to-head eval runs, re-cited for
reference — not re-run here, per instruction to avoid re-measuring what is
already known.)

## The one-line instruction worked completely, on markdown specifically

Ministral's markdown rate went **15/20 → 0/20**. Confirmed from raw
generated text, not just the automated check — e.g. CC_BATAINDIA attempt 1:

- Before: `"a **3% turnover growth** driven by initiatives like **zero-based merchandising (ZBM)**, expanded to **400 stores**"`
- After: `"a 3% turnover growth, driven by elevated marketing investments and the zero-based merchandising (ZBM) project, now scaled to 400 stores"`

Same content, markdown entirely gone. The existing terminal "No markdown,
no preamble" line was evidently too weak for this model on this task; a
direct, explicit, front-loaded restatement was not.

## It did NOT close the compliance gap — if anything, slightly worse

Ministral's generated count moved **15/20 → 13/20** and compliance
failures **5 → 7**. That is a small move at n=20, inside or near this
hardware's measured noise floor (±1–3 cases — see `REVIEW_INDEX.md`), so
it should not be read as the instruction making things worse. The honest
reading is: **no improvement**, and the direction of the noise happened to
be negative rather than positive.

Qwen was unaffected on generation (15/20 both), as expected since it never
violated markdown to begin with.

## The forbidden-figure question doesn't have a concall-side answer

The task asked whether Ministral's forbidden-figure violations (33%, 70%,
1.01%) found "inside markdown" go away once markdown is suppressed, or
persist independently.

**Checking this against source: concall's validator never checks
financial figures at all.** `concall_summary.validate()` calls
`summarizer_violation(text)` with the default `check_financial_figures=False`
— that flag is `True` only for `annual_report_summary`. The 33%/70%/1.01%
figures I reported were from the **annual_report** eval, not concall; I
should have been precise about that the first time. There is no concall
figure-violation count to compare before/after, because the concall
validator does not produce one.

What concall's validator DOES check — and what actually failed in both
runs — is **forward-tense forbidden words**: `expected`, `targeting`,
`expects`, `outlook`, `forecasting`, `target`, `will`. These fired at a
comparable or slightly higher rate after markdown was suppressed (19
attempts before → 26 after, across all retry attempts on 20 cases).

**So for concall specifically, the answer is clean: markdown and the
forward-tense violations are independent failure modes.** Suppressing
markdown completely did not touch the forward-tense rate. This means the
earlier hypothesis — that markdown suppression might also fix the
compliance content — does not hold for concall. (Whether it holds for
annual_report, where figures ARE checked and WERE found inside markdown,
is a separate, out-of-scope question this test was not designed to
answer.)

## Tone agreement and lexical overlap

Both moved up for both models (Qwen 0.7333→0.80, Ministral 0.6667→0.7692).
Given the measured ±1–3 case noise floor at n=20 and that these are
4-way/continuous metrics computed over the same small sample, this is not
attributable to the one-line change with any confidence — it is presented
for completeness, not as a finding.

Lexical overlap moved only slightly for both (Qwen 0.2333→0.2434, Ministral
0.206→0.2031). For Ministral specifically: **the previously-noted markdown
corruption of this metric is now moot** — with markdown removed, the
metric is no longer being deflated by `**word**` failing to token-match
`word`, and its value (0.2031) is now in the same range as Qwen's
(0.2434), rather than the near-zero (0.0072) seen on the markdown-corrupted
annual_report run. For concall specifically, the metric was never as
badly corrupted (0.206 before vs 0.2031 after) since concall summaries
carry less structured content, but it is now unambiguously readable
rather than needing the "ignore this" caveat from the head-to-head report.

## Plain interpretation

- **The markdown instruction can be made to work on Ministral** — a
  stronger, more explicit restatement fully suppresses it, where the
  weaker terminal line did not.
- **That does not close the concall compliance gap.** Ministral's
  forward-tense violations are a separate, independent issue from its
  markdown habit — for concall, markdown was a correlated symptom of
  weaker instruction-following in general, not the root cause of the
  compliance failures specifically.
- Concall remains close to a tie between the two models either way (15 vs
  13, or read the before numbers as 15 vs 15) — this test does not move
  that conclusion in either direction.

Whether this is worth acting on — e.g. adopting the stronger markdown line
in production for either model, or treating it as evidence Ministral needs
more explicit instructions across the board — is the founder's call.

## GPU cost

| | |
|---|---|
| Qwen markdown-fairness (20 cases) | 28.6 min |
| Ministral markdown-fairness (20 cases) | 32.6 min |
| **This test total** | **61.2 min** |

Cumulative today: 77 min (Actions 1–3) + ~102 min (Ministral preflight +
eval) + 61.2 min (this test) = **~240 min (~4.0 GPU-hours)**. Kaggle's
remaining weekly quota is not queryable through the API used in this
session — check the Kaggle notebooks/GPU quota page directly for the
current remaining balance.
