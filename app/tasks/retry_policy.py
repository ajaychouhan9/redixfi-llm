"""Retry policy — how a rejected attempt differs from the one before it.

THE BUG THIS EXISTS TO FIX
--------------------------
Measured on real GPU runs, not theorised: with `temperature=0.0` and a
fixed seed, a retry after a compliance rejection regenerates NEARLY
IDENTICAL text.

  * concall CC_KANPRPLA emitted the same "expected to commence production
    in September 2026" clause on five consecutive retries.
  * concall CC_SDBL repeated "expected to start soon" on attempts 2-6.
  * annual_report VEDL / CHOLAFIN repeated the same forbidden figure
    across all three attempts.

The loop was re-running a deterministic generation and collecting the same
deterministic failure. A larger retry budget mostly bought repetition —
which is why raising attempts 3 -> 6 repaired only 2 of 5 concall cases.

Two things change here, and only on RETRIES:

  1. SAMPLING. Attempt 1 stays `temperature=0.0` with the caller's seed, so
     the baseline remains reproducible and comparable to every earlier run.
     From attempt 2 the temperature rises and the seed shifts, so a retry
     can actually explore a different phrasing instead of re-deriving the
     rejected one.

  2. FEEDBACK. The corrective note becomes DIRECTIVE. It used to pass the
     validator's own message through verbatim ("forward-tense word
     'expected'"), which names the rule but not the offending text and not
     the remedy. It now quotes the exact rejected clause and says what to
     do with it.

HONESTY NOTE — this deviates from production
--------------------------------------------
RedixFi's own summarizers retry at `temperature=0` with a descriptive
note, and gpt-4o-mini achieved its results under that. A Qwen result
obtained under PRODUCTION_POLICY is therefore like-for-like; one obtained
under IMPROVED_POLICY is not — it shows what Qwen needs to get there. If
the improved policy is what closes the gap, the fair remedy is adopting it
in RedixFi for both models, not treating it as a Qwen-only crutch.

`PRODUCTION_POLICY` is the default everywhere, so nothing changes unless a
caller opts in.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..compliance.validators import FORWARD_TENSE_RE


@dataclass(frozen=True)
class RetryPolicy:
    name: str
    # Attempt 1 is always the caller's temperature (0.0 in every task), so
    # the first shot stays deterministic and reproducible.
    retry_temperature: float = 0.0
    vary_seed: bool = False
    directive_notes: bool = False
    description: str = ""

    def temperature_for(self, attempt: int, base_temperature: float) -> float:
        if attempt <= 1 or self.retry_temperature <= 0:
            return base_temperature
        return self.retry_temperature

    def seed_for(self, attempt: int, base_seed: Optional[int]) -> Optional[int]:
        if attempt <= 1 or not self.vary_seed or base_seed is None:
            return base_seed
        # Deterministic per attempt: a re-run of the whole benchmark still
        # reproduces exactly, while attempts within a case differ.
        return base_seed + (attempt - 1) * 1000


PRODUCTION_POLICY = RetryPolicy(
    name="production",
    retry_temperature=0.0,
    vary_seed=False,
    directive_notes=False,
    description=("Exactly what RedixFi's summarizers do, and what gpt-4o-mini "
                 "was measured under: every attempt deterministic, corrective "
                 "note = the validator's own message."),
)

IMPROVED_POLICY = RetryPolicy(
    name="improved",
    retry_temperature=0.4,
    vary_seed=True,
    directive_notes=True,
    description=("Attempt 1 unchanged and deterministic. Retries sample at "
                 "temperature 0.4 with a shifted seed so they can differ, and "
                 "receive a directive note quoting the rejected clause."),
)


# ---------------------------------------------------------------------------
# Directive corrective feedback
# ---------------------------------------------------------------------------
_QUOTED_WORD = re.compile(r"'([^']+)'")


def _offending_clause(text: str, word: str) -> Optional[str]:
    """The sentence containing the rejected word, so the note can quote what
    was actually written rather than just naming a rule."""
    if not text or not word:
        return None
    match = re.search(re.escape(word), text, re.IGNORECASE)
    if not match:
        return None
    start = text.rfind(".", 0, match.start()) + 1
    end = text.find(".", match.end())
    end = len(text) if end == -1 else end + 1
    return text[start:end].strip() or None


def build_corrective_note(
    reason: str,
    output: Dict[str, Any],
    fields: List[str],
    policy: RetryPolicy = PRODUCTION_POLICY,
) -> str:
    """Production behaviour returns `reason` unchanged. Under a directive
    policy, locate the offending clause and say what to do with it.

    The diagnosis showed the model repeating the SAME rejected clause, so
    the note has to identify that clause, not restate the rule the model
    already has in its system prompt."""
    if not policy.directive_notes:
        return reason

    quoted = _QUOTED_WORD.search(reason or "")
    word = quoted.group(1) if quoted else None
    if not word:
        return reason

    clause = None
    for field in fields:
        value = output.get(field)
        candidates = value if isinstance(value, list) else [value]
        for candidate in candidates:
            if isinstance(candidate, str):
                clause = _offending_clause(candidate, word)
                if clause:
                    break
        if clause:
            break

    if not clause:
        return (f"{reason}. Remove the word '{word}' entirely and rewrite that "
                "statement as a past-tense observation of what management said.")

    is_forward = bool(FORWARD_TENSE_RE.search(word))
    if is_forward:
        remedy = (
            f"REWRITE THIS SENTENCE: \"{clause}\" — it was rejected because it "
            f"contains the forbidden word '{word}'. Do not reuse that sentence. "
            "Either drop the forward-looking detail entirely and report what was "
            "achieved in the period instead, or attribute it as something "
            "management stated in the past tense — for example 'management set a "
            "goal of ...', 'management highlighted plans to ...', 'management "
            "indicated ...'. Do not simply reword around the same claim while "
            f"keeping '{word}'."
        )
    else:
        remedy = (
            f"REWRITE THIS SENTENCE: \"{clause}\" — it was rejected for "
            f"containing '{word}'. Remove that term and restate the point "
            "without it."
        )
    return remedy
