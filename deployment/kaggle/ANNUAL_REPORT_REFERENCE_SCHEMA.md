# Annual Report: the reference-schema problem, and what it costs to fix

**Short version.** There is no current-schema gpt-4o-mini annual-report
output in production — anywhere. Not "hard to get": it has never been
generated. A true apples-to-apples comparison is still possible, but only
via the legacy replay, and that needs a 64K context the approved config
does not have.

## What the database actually says

Queried read-only on 2026-08-29:

| | |
|---|---|
| `annual_reports` documents | 8,354 |
| with legacy `summary` | **72** |
| with `executive_summary` (current schema) | **0** |
| with `key_points` | **0** |
| with `important_risks` | **0** |
| with `evidence_tokens` (Evidence-Finder-era marker) | **0** |
| `summarized_at` range | 2026-08-16 12:42 → 16:44 **only** |

Every stored summary predates the Evidence Finder unification (2026-08-24).
`evidence_tokens: 0` is the decisive one: **no document has ever been
summarized through the current Stage 3 path.** The credit outage stalled
Stage 3 before it ever ran under the new pipeline.

## So there are exactly three options, and none is free

### A. Legacy replay — the genuine like-for-like

Replay `annual_report_summary_legacy`: same prompt, same
`raw_text[:150_000]` front-slice input, same 3-field schema
(`summary`/`bullets`/`key_takeaway`) that gpt-4o-mini actually used. The
dual-input fixture already carries everything needed.

**Cost:** measured prompt size is up to **61,432 tokens**.

| config | cases that fit |
|---|---|
| `qwen3-14b-awq-tp2` (32K, approved) | **0 / 20** |
| `qwen3-14b-awq-tp2-64k` (64K, YaRN) | **20 / 20** |

So this requires the 64K variant, which needs **YaRN rope scaling** —
Qwen3-14B's native context is 32,768. YaRN is registered but **unvalidated
on this hardware**, and it can degrade long-context quality. If Qwen scores
poorly under it, we would not be able to separate "the model is worse" from
"YaRN hurt it" — which would confound the very comparison this option
exists to make clean.

### B. Current-pipeline replay — what the expanded run does

Replay `annual_report_summary`: Evidence Finder evidence in, 4-field schema
out. Fits 32K comfortably (max 15,267 tokens), no YaRN.

**Cost:** the reference is legacy-shaped, so **both the input and the output
schema differ** from what the model is asked to produce. The comparator
already detects this and sets `reference_schema_matches_replay: False`,
suppresses the meaningless field-level compliance comparison, and prints a
banner on the review sheet. Nothing is silently compared.

This is what the expanded run uses — it is honest about its own limits and
costs no extra GPU or unvalidated config.

### C. Regenerate the reference with gpt-4o-mini

Run the current Stage 3 prompt + Evidence Finder evidence through
gpt-4o-mini for these 20 documents, producing a genuine current-schema
reference, then compare.

**Cost:** needs OpenAI credits (the outage is what caused this problem in
the first place), and it is a new generation rather than a preserved
production artifact. It would NOT need to write to production — the outputs
could live only in the benchmark — so it does not violate the read-only
rule. Roughly 20 calls at Stage 3's measured ~$0.0032/doc ≈ **$0.07**.

Of the three this is the only one that yields a clean, current-schema,
like-for-like comparison with no unvalidated inference config. It is also
the only one that spends money and creates a reference that production
itself has never produced.

## Recommendation

**B now (done, flagged), C when convenient, A only if C is unavailable.**

B is already running and costs nothing extra. C is ~7 cents and gives the
cleanest answer to "is Qwen as good as gpt-4o-mini at the job Stage 3
actually does today". A is a fallback whose result would carry a permanent
asterisk about YaRN.

**This is a founder decision, not a silent default.** The expanded run
proceeds with B and says so per case; nothing here has been quietly
compared across mismatched schemas.
