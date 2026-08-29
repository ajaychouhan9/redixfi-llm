"""EXPERIMENTAL concall prompt variant — few-shot compliant rephrasing.

⚠️ THIS IS NOT THE PRODUCTION PROMPT AND MUST NOT BECOME ONE SILENTLY.
`app/prompts/concall_summary.py` holds the vendored copy of RedixFi's
production prompt, guarded by `tests/test_prompts_match_redixfi.py`. This
file is a SEPARATE experiment. Nothing in the standard benchmark path
imports it.

WHY IT EXISTS
-------------
Concalls discuss forward guidance far more than annual reports do, and the
production prompt's compliance rules forbid the natural vocabulary for it
(`expect`, `will`, `outlook`, `target`, `forecast`). The prompt already
prescribes the fix in prose — "rephrase as 'management set a goal of X'" —
and gpt-4o-mini demonstrably follows it: all 20 production reference
summaries in the benchmark fixture pass the compliance validator, including
ones conveying explicit FY27 revenue guidance.

So the validator is not miscalibrated and the task is not impossible; the
gap is instruction-following. This variant tests whether SHOWING the
conversion (few-shot) closes it where TELLING it did not.

THE EXAMPLES ARE REAL, NOT INVENTED
-----------------------------------
Every exemplar below is a verbatim compliant sentence harvested from the
production gpt-4o-mini summaries in `fixtures/concall_benchmark.json`
(symbols noted). Using real accepted output rather than hand-written
guesses means the model is being shown patterns already proven to pass this
exact validator on this exact content type.

INTERPRETING A RESULT FROM THIS VARIANT — read before citing one
----------------------------------------------------------------
A pass rate obtained here is NOT directly comparable to gpt-4o-mini's,
because gpt-4o-mini achieved its result under the PRODUCTION prompt. If
this variant closes the gap, the honest conclusion is "Qwen needs a
stronger prompt than gpt-4o-mini does for this task" — and the fair next
step would be adopting the improved prompt in RedixFi for BOTH models, not
keeping it as a Qwen-only crutch that quietly changes what is being
measured.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from .concall_summary import (  # noqa: F401  (re-exported for the runner)
    MAX_ATTEMPTS,
    TONE_LABELS,
    build_user_content,
)

VARIANT_NAME = "concall_fewshot_v1"

# Verbatim from production gpt-4o-mini summaries that PASSED the validator.
_REAL_COMPLIANT_EXAMPLES = (
    "Management set a goal of achieving revenue between INR 1,400 crores "
    "and INR 1,500 crores for FY 2027, contingent on the resolution of "
    "licensing issues at the Bhopal facility.  [SDBL]\n"
    "Management highlighted plans to diversify into offshore, metals & "
    "minerals, and renewable energy sectors.  [JNKINDIA]\n"
    "Management indicated that while they had managed to source ammonia, "
    "the future supply chain remained uncertain.  [ALKYLAMINE]\n"
    "Management noted ongoing inflationary pressures affecting input costs "
    "and margins.  [SDBL]\n"
    "Management noted challenges from geopolitical uncertainties and "
    "inflationary pressures but expressed confidence in the bank's "
    "resilience.  [PNB]"
)

# The production prompt verbatim, plus an appended few-shot section. The
# base text is imported rather than retyped so this variant cannot drift
# from production independently of the vendored copy.
from .concall_summary import SYSTEM_PROMPT as _PRODUCTION_SYSTEM_PROMPT

SYSTEM_PROMPT = _PRODUCTION_SYSTEM_PROMPT + (
    " "
    "HOW TO WRITE ABOUT FORWARD-LOOKING CONTENT — worked examples. A concall "
    "usually contains guidance, plans and outlook. You must still report that "
    "content; you may not use the forbidden vocabulary to do it. Convert it "
    "into reported past-tense observation of what management SAID. "
    "WRONG (forbidden words in bold): 'The company EXPECTS revenue to grow', "
    "'Management is TARGETING INR 1,500 crores', 'The OUTLOOK remains "
    "positive', 'Margins WILL improve next year', 'Management FORECASTS "
    "recovery'. "
    "RIGHT — these are real sentences that passed this exact check: "
    f"{_REAL_COMPLIANT_EXAMPLES} "
    "Note the pattern: attribute to management, in the past tense, as "
    "something they stated/noted/set/highlighted/indicated — never as a "
    "property of the future. Before emitting your answer, re-read it and "
    "replace any occurrence of expect, will, outlook, target, forecast, "
    "going to, likely, or recommend with one of these constructions."
)


def build_variant_user_content(
    fixture: Dict[str, Any], corrective_note: Optional[str] = None,
) -> str:
    """Identical to production's user content — only the SYSTEM prompt
    differs in this variant, so the evidence the model sees is unchanged."""
    return build_user_content(fixture, corrective_note)
