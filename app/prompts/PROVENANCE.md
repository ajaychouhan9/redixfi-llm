# Vendored-from-RedixFi provenance register

Every prompt, template, and validator in this project that was copied from
RedixFi is listed here. **Nothing in this repository imports RedixFi code at
runtime** (founder decision, 2026-08-28) — the copies exist so the LLM service
can reproduce RedixFi's exact LLM workload while staying fully independent.

The cost of vendoring is silent divergence. This register plus the
per-file `PROVENANCE` header is the mitigation: re-check these against the
RedixFi source before trusting any evaluation result produced after the
copy date.

RedixFi backend repo: `https://github.com/ajaychouhan9/redixfi-backend`
Local checkout used for the copy: `C:\Redixfi`
Repo HEAD at copy time: **`8bb3170`**
Copy date: **2026-08-28**

| Vendored file | Original RedixFi file | Function / section | Source commit | Dated |
|---|---|---|---|---|
| `app/compliance/validators.py` | `data-pipeline/annual_report_summarizer.py` | `_violation()`, `FORBIDDEN_WORDS_RE`, `FORWARD_TENSE_RE`, `_BUY_SELL_RE`, `_BUY_SELL_SAFE_RE`, `FINANCIAL_FIGURE_RE` | `b9e40c4` | 2026-08-24 |
| `app/compliance/validators.py` | `api/app/core/document_retrieval.py` | `_chunk_fails_compliance()`, `_CALL_MEETING_SAFE_RE`, `_TRADING_CONTEXT_NEAR_CALL_RE` | `ed253bb` | 2026-08-27 |
| `app/compliance/validators.py` | `data-pipeline/risk_flag_classifier.py` | `_violation()` (risk-summary variant) | `b9e40c4` | 2026-08-24 |
| `app/prompts/annual_report_summary.py` | `data-pipeline/annual_report_summarizer.py` | `SYSTEM_PROMPT`, `_user_content()`, `BULLET_MIN`/`BULLET_MAX`, `MAX_ATTEMPTS` | `b9e40c4` | 2026-08-24 |
| `app/prompts/red_flag.py` | `data-pipeline/risk_flag_classifier.py` | `_SYSTEM_PROMPT`, user-content shape, `RISK_FLAG_CATEGORIES`, `_KEYWORD_PATTERNS` | `b9e40c4` | 2026-08-24 |
| `app/prompts/ask_ai.py` | `api/app/core/ask.py` | `ASK_SYSTEM_TEMPLATE`, `GENERAL_SYSTEM_TEMPLATE`, `call_llm_ask()` user-content assembly | `454a07a` | 2026-08-27 |

## Deliberately NOT vendored

* **`data-pipeline/evidence_finder.py`** — evidence SELECTION is not
  reproduced here. `scripts/export_fixtures.py` runs on the RedixFi VM and
  calls the real `evidence_finder.py`, storing its output in the fixture.
  This project consumes that evidence; it never invents a competing
  selection algorithm.
* **`api/app/core/evidence_router.py` / `evidence_fusion.py`** — Ask AI
  retrieval/fusion is not re-implemented. Fixtures carry the assembled fact
  packet exactly as production built it.
* **`api/app/core/red_flag_ask.py`** — the query-time answer assembly does
  ZERO LLM calls, so there is no LLM workload to reproduce. The Red Flag LLM
  workload is `risk_flag_classifier.classify_chunk`, which IS vendored.

## Known deviations from the register above

* **`app/prompts/red_flag.py` — permanent, intentional fork from
  RedixFi as of 2026-09-19 (Stage 1 promotion).** RedixFi's
  `data-pipeline/risk_flag_classifier.py::_SYSTEM_PROMPT` was rewritten
  2026-09-19 (topic-detection vs. actual-Red-Flag distinction, new
  `is_red_flag` field, a deterministic `_contradicts_evidence()` guard —
  see `docs/00_MASTER_CONTEXT.md`, "risk-topic detection != Red Flag").
  This project's copy went through its own, separate path the same day:
  Stage 0 reverted the "CONTROLLED FIX (2026-08-30)" paragraph (a
  previously-undetected net regression: 26 new false negatives for 7
  false positives fixed, n=60), then Stage 1 replaced the whole prompt
  with an independently-designed, Qwen-specific rewrite (formerly
  `app/prompts/red_flag_stage1_v1.py`) — same semantic contract as
  RedixFi's new prompt (topic vs. instance, `is_red_flag`), different
  wording, asymmetric per category (full exclusion framing for
  `contingent_liability`/`related_party_transaction`, positive-only
  framing for `auditor_qualification` — never naming "Key Audit Matter"/
  "unmodified opinion" as exclusions, per the redixfi-qwen-prompt-
  negation-priming finding). Validated on Kaggle T4x2/qwen3-14b-awq-tp2
  against the 60-case `red_flag_benchmark.json`, re-scored against
  RedixFi's CORRECTED gpt-4o-mini classifier (not the stale original
  reference, which itself only agreed with the corrected one on 27/60 =
  0.450 cases): 54/60 = 0.900 agreement. This file will NOT be resynced
  to RedixFi's literal prompt text going forward — the two are
  independently maintained, model-specific prompts on the same contract.
  `test_prompts_match_redixfi.py::test_red_flag_system_prompt_matches`
  reflects this: it asserts the CONTROLLED FIX text stays gone, the
  `is_red_flag` contract is present, and the negation-priming precaution
  holds, but does not compare text against live RedixFi HEAD.

## Re-verification command

Run from the RedixFi checkout to see whether any source has moved since the
copy date:

```bash
for f in api/app/core/ask.py api/app/core/document_retrieval.py \
         data-pipeline/annual_report_summarizer.py \
         data-pipeline/risk_flag_classifier.py; do
  echo "$f -> $(git log -1 --format='%h %ad' --date=short -- $f)"
done
```

Expected at copy time: `454a07a`, `ed253bb`, `b9e40c4`, `b9e40c4`.
Any different hash means this register is stale — re-check the diff before
trusting a comparison.
