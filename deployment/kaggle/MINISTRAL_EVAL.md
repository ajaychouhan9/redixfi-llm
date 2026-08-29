# Ministral 3 14B vs Qwen3-14B — first look

**EXPERIMENTAL / NOT PRODUCTION.** Nothing here declares either model
production-ready. That judgement is the founder's after reading the sheets.

Both models ran the SAME 100 fixture cases (20 annual_report, 20 concall,
60 red_flag) under stock/baseline settings — production retry mechanics,
production prompts, no steering, no Ministral-specific tuning.

---

## Headline

| | Qwen3-14B-AWQ | Ministral 3 14B |
|---|---|---|
| annual_report generated | **17/20** (18/20 with retry fix) | **3/20** |
| concall generated | 15/20 (17/20 with retry fix) | **15/20** |
| concall tone agreement | 0.7333 | 0.6667 |
| red_flag agreement | **0.85** | **0.5833** |
| red_flag false negatives | 2 | **21** |
| guided decoding | 100/100, 0 repairs | **100/100, 0 repairs** |
| load time | ~244 s | 234.8 s |
| VRAM per card | ~13.3 / 14.56 GB | 13.4 / 14.56 GB |
| output tok/s | 7.2 | **12.5** |
| sec/case | 67.3 | **41.8** |

**Ministral is the faster model and the weaker one on this workload.**
Concall is the one category where they are level.

The annual_report and red_flag gaps are far outside the measured noise
floor (±1–3 cases at n=20 — see `REVIEW_INDEX.md`), so unlike the retry-fix
deltas they are real signal, not variance.

---

## A production bug this surfaced — worth fixing regardless of model choice

`FINANCIAL_FIGURE_RE`, vendored verbatim from RedixFi's
`annual_report_summarizer.py`, fires on ordinary English:

```python
r"(?:₹|rs\.?|inr)\s*[\d,]+(?:\.\d+)?"
```

`[\d,]+` matches a **bare comma with no digits at all**, and there is no
word boundary before `rs`. So the letters "rs" ending any plural, followed
by a comma, are read as a rupee figure:

| text | matched as a financial figure |
|---|---|
| `shareholders, employees` | `rs,` |
| `dealers, alongside` | `rs,` |
| `generators, solar` | `rs,` |
| `suppliers, customers and peers` | `rs,` |
| `directors, auditors` | `rs,` |

This is not hypothetical and not confined to this benchmark: **the real
gpt-4o-mini reference regeneration hit it too** — SBILIFE was rejected on
attempt 1 for `financial figure stated as fact 'rs,'` and had to be
regenerated. In production this silently costs a retry, and on a summary
that keeps the word it can burn all three attempts and store nothing.

A candidate fix — word boundary, and require at least one digit:

```python
r"(?:₹|\brs\.?|\binr)\s*\d[\d,]*(?:\.\d+)?"
```

Verified to still catch `Rs. 1,234 crore`, `Rs 500`, `₹2,00,000`,
`INR 45.6 million`, `12%`, while no longer firing on any row above.

**RedixFi was NOT modified** — this project is read-only against it. This
is a report, not a change.

### It does NOT explain Ministral's result

Re-scoring every recorded attempt through the real validator with only
that regex swapped:

| run | as measured | with the fixed regex |
|---|---|---|
| Ministral (stock) | 3/20 | **5/20** |
| Qwen (baseline) | 17/20 | 19/20 |
| Qwen (retry fix) | 18/20 | 19/20 |

A 14-case gap survives. The bug is real and worth fixing; it is not the
cause.

---

## What actually drives the annual_report gap: instruction-following

The annual-report prompt says *"No markdown, no preamble"* and rule (4)
bans **every** figure — "describe direction or theme in words only".

| | markdown bold in output | |
|---|---|---|
| Qwen annual_report | **0 / 20** | |
| Ministral annual_report | **18 / 20** | |
| Qwen concall | **0 / 20** | |
| Ministral concall | **15 / 20** | |

In annual_report, Ministral writes `**bold**` almost everywhere despite
the instruction, and readily emits percentages (`33%`, `70%`, `10%`,
`1.01%`) that the prompt forbids outright — rejection reasons there are
dominated by `financial figure stated as fact` and forward-tense words.
**Concall's validator never checks financial figures at all** (only
annual_report does — see `concall_summary.validate()`), so its 15/20
markdown cases are a pure instruction-following signal with no figure
component; its rejections there are forward-tense words only
(`targeting`, `targets`, `forecasting`, `targeted`, `expectations`). See
`CONCALL_MARKDOWN_FAIRNESS.md` for the follow-up test isolating whether
suppressing concall's markdown also closes its compliance gap (it does
not — the two are independent failure modes for concall specifically).

The markdown also corrupts the lexical-overlap triage number (0.0072 as
measured) — `**word**` does not token-match `word`. That metric is
uninformative for Ministral and should be ignored, not read as "no
content in common".

**The prose quality itself is not obviously poor.** Read the sheets: the
summaries are well-attributed, on-theme and specific. Ministral fails this
task on *constraint compliance*, not on comprehension — which is a
meaningful distinction, because RedixFi's use case is defined by those
constraints.

---

## red_flag: under-flagging

| | agree | agree_no_flag | false negative | false positive |
|---|---|---|---|---|
| Qwen | 38 | 13 | 2 | 7 |
| Ministral | 19 | 16 | **21** | 4 |

Opposite error profiles. Qwen over-flags (7 FP / 2 FN); Ministral
under-flags badly (21 FN). For a risk-detection feature a false negative
is the more costly direction — a missed auditor qualification or promoter
pledge is exactly what the feature exists to catch.

---

## Fairness caveats, stated so the result can be discounted properly

1. **Stock settings, by instruction.** None of this session's Qwen fixes
   (varied retry sampling, directive corrective notes, content steering)
   were applied to Ministral. Qwen's *baseline* column is the like-for-like
   one; its retry-fix column is not.
2. **The tokenizer objection was addressed, not ignored.** The preflight
   showed `apply_chat_template(..., tokenize=False)` is unsafe for Tekken,
   so this run used `tokenizer_mode="mistral"` and routed prompts through
   `llm.chat()`. `chat_native: True` is recorded in the run state. Ministral
   still scored 3/20, so the formatting theory did **not** account for the
   preflight's weak result.
3. **No prompt tuning was attempted for Ministral.** A markdown-suppressing
   or figure-suppressing instruction might close much of the annual_report
   gap. That is an untested hypothesis, and it would apply to both models.
4. **n=20 per summarization category.** The gaps here are large enough to
   exceed the noise floor; the concall tie (15 vs 15) and the tone-agreement
   difference (0.7333 vs 0.6667) are **not** — treat those as level.

---

## Recommendation

**Do not switch to Ministral for annual_report or red_flag on this
evidence.** The gaps are large, consistent, and in the costly direction.

**Concall is genuinely level** (15/20 vs 15/20), and Ministral is ~40%
faster. If a second model is ever wanted for concall specifically, it is
not ruled out.

**UPDATE, follow-up test run (2026-08-29, concall only):** the one-line
markdown fix was tried, on both models, at production settings. It fully
suppressed Ministral's concall markdown (15/20 → 0/20, confirmed from raw
text) but did not close the compliance gap (13/20 generated after, against
15/20 before) — markdown and the forward-tense violations turned out to be
independent failure modes for concall. See `CONCALL_MARKDOWN_FAIRNESS.md`
for the full numbers. Whether the same test would move the annual_report
number (where figures ARE checked and WERE found inside markdown, unlike
concall) remains untested and out of scope for that follow-up.

---

## GPU cost

| | |
|---|---|
| preflight (6 cases) | 15.2 min |
| failed guard attempt | 7.3 min |
| full eval (100 cases) | 79.1 min |
| **Ministral total** | **~102 min** |

Full eval alone: 4,184 s of generation (41.8 s/case) plus ~20 min of
install, 9.7 GB download and load.

Plus the markdown-fairness follow-up (concall only, both models — see
`CONCALL_MARKDOWN_FAIRNESS.md`): +61.2 min. **Running total across
Ministral work: ~163 min.**
