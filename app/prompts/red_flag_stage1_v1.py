"""EXPERIMENTAL red_flag prompt variant — Stage 1 candidate (2026-09-19).

⚠️ NOT THE PRODUCTION PROMPT. `app/prompts/red_flag.py` holds the vendored
production copy (currently the Stage 0 revert — see that file's own
comment). Nothing in the standard benchmark path imports this file.

WHY THIS EXISTS
---------------
The prior attempt at this exact problem (`app/prompts/
red_flag_instance_check.py`, `red_flag_instance_check_v1`, measured
2026-08-30) applied ONE "policy vs. instance" instruction uniformly across
all 4 categories. Result: fixed all 7 known false positives (7 -> 1) but
false negatives rose 2 -> 28 (agreement 0.85 -> 0.5167) — a large net
regression, concentrated in `auditor_qualification`: genuine Key Audit
Matters gpt-4o-mini itself confirms elsewhere (ABB-277, HDFCBANK-766) got
wrongly excluded, because the instruction's own "RIGHT" example explicitly
named "an actual qualified opinion" as the bar, which reads to the model as
"a bare KAM never qualifies" even though some KAMs genuinely do.

That variant's own docstring already recommended the untried next step:
"scope the policy-vs-instance distinction ONLY to contingent_liability
(where it worked cleanly, all 4 fixed, no visible cost) and leave
auditor_qualification alone or give it its own narrower rule that
explicitly preserves ordinary KAMs." This variant does exactly that, plus
two changes informed by later findings:

  1. ASYMMETRIC scope. Full "policy vs. instance" language for
     `contingent_liability` (the proven-clean case) and
     `related_party_transaction` (same structural pattern — a
     near-universal boilerplate policy/approval paragraph vs. an actual
     transaction — not independently proven for Qwen yet, hence this eval).
     For `auditor_qualification`, ONLY positive framing: what DOES count
     (an actual qualified/adverse/disclaimer opinion, a material weakness
     actually identified) — the prompt never says "a Key Audit Matter is
     not enough" or names "unmodified opinion" as an exclusion, on the
     hypothesis (redixfi-qwen-prompt-negation-priming memory, measured on
     a different RedixFi/Qwen task) that naming the exact phrases you want
     the model to avoid confirming can paradoxically raise their
     probability of being confirmed. Untested for this specific task;
     that is what this evaluation run is for.
  2. Explicit `is_red_flag` field (mirrors RedixFi's own 2026-09-19
     risk_flag_classifier.py fix) rather than relying solely on
     `category: null` to carry the "not an actual instance" signal — gives
     the model a second, explicit place to state the same judgment,
     and gives app/tasks/red_flag.py's `run()`/`run_variant()` an
     AND-condition backstop independent of how the model uses `category`.

WHAT IS HELD CONSTANT
----------------------
Same real compliance check, same real JSON parsing, same real dynamic
per-chunk category enum (`schema_for_task`) as production — only the
system prompt and the schema's `is_red_flag` requirement (made REQUIRED
here, unlike the production/baseline schema call, which leaves it optional
for backward compatibility with prompts that never ask for it) vary. See
app/experiments/red_flag_variants.py for how this is wired into the same
`run_variant()` harness that measured the 2026-08-30 regression.
"""
from __future__ import annotations

from typing import Any, Dict

from .red_flag import KEYWORD_PATTERNS, RISK_FLAG_CATEGORIES  # noqa: F401  (re-exported)
from .red_flag import build_user_content  # noqa: F401  (re-exported for the runner)

VARIANT_NAME = "red_flag_stage1_v1"

SYSTEM_PROMPT = (
    "You decide whether a document excerpt establishes an ACTUAL, "
    "company-specific Red Flag in one of a small set of governance/risk "
    "categories — not merely whether the excerpt discusses, defines, or "
    "routinely/compliantly discloses that topic. A topic mention alone is "
    "never sufficient.\n\n"
    "Categories:\n"
    "- auditor_qualification: the auditor's report states an ACTUAL "
    "qualified opinion, adverse opinion, disclaimer of opinion, explicit "
    "qualification/reservation, inability to obtain sufficient audit "
    "evidence, or a material weakness/exception the auditor actually "
    "found and described. Confirm only when the excerpt itself states "
    "such an adverse conclusion about this company.\n"
    "- contingent_liability: Indian annual reports include a standard "
    "accounting-POLICY note (often numbered, e.g. \"Provisions and "
    "Contingent Liabilities\") that defines WHEN a company would "
    "recognise or disclose such an item in general, as a matter of "
    "accounting standard (Ind-AS 37). Nearly every company's report "
    "contains this near-identical paragraph, and it does NOT by itself "
    "mean the company has any such item. Confirm this category ONLY if "
    "the excerpt discloses an ACTUAL, SPECIFIC contingent liability, "
    "claim, dispute, litigation, or guarantee that exists NOW for THIS "
    "company (ideally with an amount, counterparty, or matter named). "
    "Merely defining the accounting treatment is NOT an instance.\n"
    "- related_party_transaction: Indian annual reports include a "
    "standard RPT POLICY/approval-process paragraph (Audit Committee "
    "review, arm's-length/ordinary-course confirmation, Ind AS 24/"
    "Section 188 compliance statements) that nearly every company's "
    "report contains, and it does NOT by itself mean anything adverse "
    "happened. Confirm this category ONLY if the excerpt describes an "
    "ACTUAL adverse or governance-relevant related-party condition — "
    "explicitly NOT at arm's length, outside the ordinary course of "
    "business, an unresolved conflict of interest, or a transaction the "
    "excerpt itself characterizes as unusually large relative to the "
    "company's own stated turnover/net worth. A bare RPT policy "
    "description, a routine Audit Committee approval, a statement that "
    "transactions were at arm's length/ordinary course, or a statement "
    "that there were no materially significant related-party "
    "transactions are NOT instances.\n"
    "- promoter_pledge: the excerpt states an ACTUAL disclosed pledge or "
    "encumbrance of promoter shares (e.g. a stated percentage/quantity "
    "pledged). A passage that only defines what a pledge is, with no "
    "actual disclosed pledge named, is not enough.\n\n"
    "Given the excerpt and its candidate categories, respond with JSON: "
    "{\"category\": one of the candidate category strings, or null if "
    "none apply, \"is_red_flag\": true only when the excerpt itself "
    "establishes an actual adverse/exceptional company-specific "
    "condition as described above, false otherwise (including whenever "
    "category is null), \"summary\": a short, neutral, factual 1-2 "
    "sentence restatement of what the excerpt states, with no "
    "commentary, no forward-looking language, no investment advice — "
    "empty string if category is null}."
)


def build_variant_user_content(fixture: Dict[str, Any]) -> str:
    """Identical to production's user content — only the SYSTEM prompt
    differs, so the evidence the model sees is unchanged."""
    return build_user_content(fixture)
