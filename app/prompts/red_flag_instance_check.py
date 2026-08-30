"""EXPERIMENTAL red_flag prompt variant — policy vs. actual instance.

⚠️ NOT THE PRODUCTION PROMPT. `app/prompts/red_flag.py` holds the vendored
production copy. Nothing in the standard benchmark path imports this file.

WHY THIS EXISTS
---------------
At n=60, red_flag showed 7 false positives, all `contingent_liability` or
`auditor_qualification` where gpt-4o-mini correctly returned no flag.
Checked individually rather than assumed to share one cause — they do NOT:

  * 4 of 7 (BAJFINANCE-488, CIPLA-507, GRASIM-922, PFC-700) are the SAME
    root cause: the chunk is the company's generic Ind-AS 37 accounting
    POLICY note ("Provisions are recognised when...", "A disclosure for a
    contingent liability is made when...") — a definition of WHEN such an
    item would be recognised, appearing near-verbatim across most Indian
    annual reports, with no actual instance of a contingent liability
    disclosed anywhere in the chunk. This is the pattern this variant
    targets.
  * 2 of 7 (GODREJCP-432, PFC-439) are genuine, company-specific Key Audit
    Matter text — NOT boilerplate, and not clearly the same bug: gpt-4o-mini
    itself flags a structurally similar KAM elsewhere in the same 60-case
    set (ONGC-547, "adequacy of provision for impairment"), so "a KAM is
    never an auditor_qualification" is not a safe rule to add — it would
    likely trade these false positives for new false negatives. NOT
    addressed by this variant; flagged for separate investigation.
  * 1 of 7 (HINDALCO-764) is a third pattern: "contingent liabilities" is
    named only as one bullet in an unrelated dividend-policy factors list,
    never elaborated on. Whether the instruction below also helps this one
    is tested empirically, not assumed.

THE ONE ADDED INSTRUCTION
--------------------------
Distinguishes a POLICY DESCRIPTION (how the company would account for a
category of item, in general, as a matter of accounting standard) from an
ACTUAL DISCLOSED INSTANCE (a specific case that has happened or exists).
The negative example is the REAL BAJFINANCE-488 chunk_text verbatim, not
invented — the same chunk that produced the confirmed false positive.
"""
from __future__ import annotations

from typing import Any, Dict

from .red_flag import KEYWORD_PATTERNS, RISK_FLAG_CATEGORIES  # noqa: F401  (re-exported)
from .red_flag import build_user_content  # noqa: F401  (re-exported for the runner)
from .red_flag import SYSTEM_PROMPT as _PRODUCTION_SYSTEM_PROMPT

VARIANT_NAME = "red_flag_instance_check_v1"

# Verbatim from fixtures/red_flag_benchmark.json, case RF_BAJFINANCE_AR_BAJFINANCE_488
# — the confirmed false-positive chunk, used as the negative example.
_REAL_POLICY_BOILERPLATE_EXAMPLE = (
    "\"3.8 Provisions and contingent liabilities. The Company creates a "
    "provision when there is present obligation as a result of a past "
    "event that probably requires an outflow of resources and a reliable "
    "estimate can be made of the amount of the obligation. A disclosure "
    "for a contingent liability is made when there is a possible "
    "obligation or a present obligation that may, but probably will not, "
    "require an outflow of resources.\""
)

_INSTANCE_CHECK = (
    " "
    "CRITICAL DISTINCTION — policy description vs. an actual disclosed "
    "instance. Indian annual reports include a standard accounting-POLICY "
    "note (usually numbered, e.g. \"Provisions and Contingent Liabilities\") "
    "that defines WHEN a company would recognise or disclose such an item "
    "in general, as a matter of accounting standard (Ind-AS 37). Nearly "
    "every company's annual report contains this near-identical paragraph, "
    "and it does NOT by itself mean the company has any such item. Confirm "
    "a category ONLY if the excerpt discloses an ACTUAL, SPECIFIC instance "
    "— a contingent liability, litigation, or guarantee that exists NOW for "
    "THIS company; an audit opinion that was actually qualified/adverse/"
    "disclaimed or a material weakness that was actually identified; a "
    "related-party transaction or promoter pledge that actually occurred. "
    "Merely defining the accounting treatment, or naming a category as one "
    "factor among several in an unrelated list (e.g. a dividend policy "
    "listing \"contingent liabilities\" as one of several factors "
    "considered), is NOT an instance and must be returned as null. "
    "WRONG (do not confirm this): "
    f"{_REAL_POLICY_BOILERPLATE_EXAMPLE} — this describes the RULE for when "
    "a disclosure would be made; it does not disclose that one exists. "
    "RIGHT (confirm this): a note that says the company IS party to specific "
    "pending litigation, HAS given a specific guarantee, or WAS the subject "
    "of an actual qualified opinion for a stated reason."
)

# Production text imported, never retyped, so this variant cannot drift
# from production independently of the vendored copy.
SYSTEM_PROMPT = _PRODUCTION_SYSTEM_PROMPT + _INSTANCE_CHECK


def build_variant_user_content(fixture: Dict[str, Any]) -> str:
    """Identical to production's user content — only the SYSTEM prompt
    differs, so the evidence the model sees is unchanged."""
    return build_user_content(fixture)
