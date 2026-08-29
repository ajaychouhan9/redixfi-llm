"""The markdown-fairness variant must isolate exactly ONE change.

This is a fairness test between two models, so it matters more than usual
that the variant does nothing except add one line: production prompt
verbatim as a prefix, production retry policy, production attempt budget,
identical user content. If any of those drifted, a result difference would
not be attributable to the markdown instruction alone.
"""
from app.experiments.concall_variants import markdown_fairness_variant
from app.prompts import concall_summary as prod
from app.prompts import concall_summary_markdown_fairness as fairness
from app.tasks.retry_policy import PRODUCTION_POLICY


class TestPromptIsolation:
    def test_production_prompt_is_the_prefix_verbatim(self):
        """The variant must extend production, never edit it."""
        assert fairness.SYSTEM_PROMPT.startswith(prod.SYSTEM_PROMPT)

    def test_exactly_one_line_is_added(self):
        added = fairness.SYSTEM_PROMPT[len(prod.SYSTEM_PROMPT):]
        assert added.strip(), "the fairness variant added nothing"
        # "one line" == one added sentence/instruction, not a multi-rule block.
        assert added.count(". ") <= 2, (
            f"expected one short instruction, found what looks like several: "
            f"{added!r}")

    def test_added_line_explicitly_names_markdown_and_asterisks(self):
        added = fairness.SYSTEM_PROMPT[len(prod.SYSTEM_PROMPT):].lower()
        assert "markdown" in added
        assert "asterisk" in added or "bold" in added

    def test_user_content_is_unchanged(self):
        fx = {"company_name": "X Ltd", "symbol": "X", "filing_date": "2026-01-01",
              "input_text": "some transcript"}
        assert fairness.build_variant_user_content(fx) == prod.build_user_content(fx)


class TestVariantConfig:
    def test_uses_production_retry_policy_not_the_improved_one(self):
        """This is a fairness test of ONE prompt line, not a retry-mechanics
        test. Mixing in the improved policy would make a result ambiguous
        between 'the line worked' and 'the sampling varied'."""
        v = markdown_fairness_variant()
        assert v.policy is PRODUCTION_POLICY
        assert v.policy.retry_temperature == 0.0
        assert v.policy.directive_notes is False

    def test_attempt_budget_matches_production(self):
        v = markdown_fairness_variant()
        assert v.max_attempts == prod.MAX_ATTEMPTS == 3

    def test_no_config_argument_needed(self):
        """Unlike steered_variant, this must not take a policy override —
        the whole point is that it is fixed to production mechanics."""
        import inspect
        sig = inspect.signature(markdown_fairness_variant)
        assert len(sig.parameters) == 0
