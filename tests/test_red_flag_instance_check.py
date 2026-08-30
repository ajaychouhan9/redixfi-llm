"""The instance-check variant must isolate exactly ONE added instruction,
and its negative example must be the REAL confirmed false-positive text,
not an invented paraphrase.
"""
from app.experiments.red_flag_variants import (instance_check_variant,
                                               production_variant)
from app.prompts import red_flag as prod
from app.prompts import red_flag_instance_check as fixed


class TestPromptIsolation:
    def test_production_prompt_is_the_prefix_verbatim(self):
        assert fixed.SYSTEM_PROMPT.startswith(prod.SYSTEM_PROMPT)

    def test_something_was_actually_added(self):
        assert len(fixed.SYSTEM_PROMPT) > len(prod.SYSTEM_PROMPT)

    def test_user_content_is_unchanged(self):
        fx = {"candidates": ["contingent_liability"], "chunk_text": "some excerpt"}
        assert fixed.build_variant_user_content(fx) == prod.build_user_content(fx)

    def test_categories_and_keyword_patterns_are_reexported_unmodified(self):
        """The variant must not redefine the taxonomy or the keyword
        prefilter — only the confirmation prompt changes."""
        assert fixed.RISK_FLAG_CATEGORIES == prod.RISK_FLAG_CATEGORIES
        assert fixed.KEYWORD_PATTERNS is prod.KEYWORD_PATTERNS


class TestNegativeExampleIsReal:
    def test_negative_example_is_the_actual_bajfinance_chunk_language(self):
        """This must be the REAL confirmed false-positive text, harvested
        from fixtures/red_flag_benchmark.json case RF_BAJFINANCE_AR_
        BAJFINANCE_488 — not a paraphrase invented for the prompt."""
        added = fixed.SYSTEM_PROMPT[len(prod.SYSTEM_PROMPT):]
        assert "present obligation as a result of a past event" in added
        assert "probably requires an outflow of resources" in added

    def test_distinguishes_policy_from_instance_explicitly(self):
        added = fixed.SYSTEM_PROMPT[len(prod.SYSTEM_PROMPT):].lower()
        assert "actual" in added
        assert "instance" in added
        assert "policy" in added or "rule" in added


class TestVariantConfig:
    def test_instance_check_variant_uses_the_new_prompt(self):
        v = instance_check_variant()
        assert v.system_prompt == fixed.SYSTEM_PROMPT

    def test_production_variant_uses_the_unmodified_prompt(self):
        v = production_variant()
        assert v.system_prompt == prod.SYSTEM_PROMPT

    def test_description_names_which_cases_it_targets_and_which_it_does_not(self):
        """The description must not overclaim — 3 of 7 known false
        positives are explicitly NOT expected to be fixed by this."""
        d = instance_check_variant().description
        assert "4" in d
        assert "not" in d.lower() or "other" in d.lower()
