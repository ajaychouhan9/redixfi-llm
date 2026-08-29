"""The steered variant must teach framings that ACTUALLY pass.

The whole premise of the content-steering change is that it shows the
model constructions harvested from real gpt-4o-mini output which the real
validator accepts. If an exemplar were invented — or harvested wrongly —
the prompt would be teaching Qwen to fail, and a poor result would be
misread as "steering doesn't work" rather than "the examples were bad".
"""
import re

import pytest

from app.compliance.validators import summarizer_violation
from app.prompts import concall_summary as prod
from app.prompts import concall_summary_steered as steered

# The exemplars are rendered as bulleted quotes:  - "..."  [SYMBOL]
_EXEMPLAR = re.compile(r'-\s+"([^"]+)"\s+\[([A-Z]+)\]')
EXEMPLARS = _EXEMPLAR.findall(steered._REAL_COMPLIANT_EXAMPLES)


def test_exemplars_were_actually_parsed():
    """Guards the guard: a formatting change that broke the regex would
    otherwise make every check below vacuously pass."""
    assert len(EXEMPLARS) >= 6


@pytest.mark.parametrize("sentence,symbol", EXEMPLARS)
def test_every_taught_example_passes_the_real_validator(sentence, symbol):
    assert summarizer_violation(sentence) is None, (
        f"exemplar from {symbol} does not pass: {sentence!r}")


def test_forward_guidance_is_still_conveyed_not_omitted():
    """Steering must not degenerate into 'say nothing about the future' —
    the point is attribution, not omission. At least one exemplar carries
    concrete forward guidance (a future fiscal year or a capacity plan)."""
    assert any(re.search(r"FY\s?20\d\d|MTPA", s) for s, _ in EXEMPLARS)


class TestVariantIsolation:
    def test_production_prompt_is_the_prefix_verbatim(self):
        """The variant must extend production, never edit it — otherwise a
        result difference is not attributable to the steering alone."""
        assert steered.SYSTEM_PROMPT.startswith(prod.SYSTEM_PROMPT)

    def test_variant_actually_adds_something(self):
        assert len(steered.SYSTEM_PROMPT) > len(prod.SYSTEM_PROMPT)

    def test_user_content_is_unchanged(self):
        """Only the SYSTEM prompt varies; the evidence the model sees must
        be identical, or the comparison changes two things at once."""
        fx = {"company_name": "X Ltd", "symbol": "X", "filing_date": "2026-01-01",
              "input_text": "some transcript"}
        assert steered.build_variant_user_content(fx) == prod.build_user_content(fx)

    def test_retry_budget_matches_production(self):
        assert steered.MAX_ATTEMPTS == prod.MAX_ATTEMPTS
