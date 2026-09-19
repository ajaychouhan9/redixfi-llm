"""The stage1_v1 variant must be asymmetric on purpose: full policy-vs-
instance framing for contingent_liability/related_party_transaction, but
ONLY positive framing for auditor_qualification (no "Key Audit Matter"/
"unmodified opinion" named as exclusions — the exact phrasing measured to
correlate with negation priming on a different RedixFi/Qwen task, and the
category where the 2026-08-30 instance_check_v1 variant's blanket rule
caused its 26 new false negatives).
"""
from app.experiments.red_flag_variants import (production_variant,
                                               stage1_v1_variant)
from app.prompts import red_flag as prod
from app.prompts import red_flag_stage1_v1 as stage1


class TestPromptIsolation:
    def test_user_content_is_unchanged(self):
        fx = {"candidates": ["contingent_liability"], "chunk_text": "some excerpt"}
        assert stage1.build_variant_user_content(fx) == prod.build_user_content(fx)

    def test_categories_and_keyword_patterns_are_reexported_unmodified(self):
        """The variant must not redefine the taxonomy or the keyword
        prefilter — only the confirmation prompt changes."""
        assert stage1.RISK_FLAG_CATEGORIES == prod.RISK_FLAG_CATEGORIES
        assert stage1.KEYWORD_PATTERNS is prod.KEYWORD_PATTERNS


class TestAsymmetricScope:
    def test_contingent_liability_gets_policy_vs_instance_framing(self):
        text = stage1.SYSTEM_PROMPT.lower()
        assert "policy note" in text
        assert "ind-as 37" in text

    def test_related_party_transaction_gets_policy_vs_instance_framing(self):
        text = stage1.SYSTEM_PROMPT.lower()
        assert "rpt policy" in text or "policy/approval" in text
        assert "arm's length" in text

    def test_auditor_qualification_never_names_key_audit_matter_as_exclusion(self):
        """The core hypothesis under test: explicitly naming 'Key Audit
        Matter' or 'unmodified opinion' as things that do NOT qualify is
        the exact phrasing pattern the 2026-08-30 regression used and the
        redixfi-qwen-prompt-negation-priming memory warns against. This
        variant states only what DOES count."""
        text = stage1.SYSTEM_PROMPT.lower()
        assert "key audit matter" not in text
        assert "unmodified" not in text
        assert "emphasis of matter" not in text

    def test_is_red_flag_field_is_documented_in_the_contract(self):
        assert "is_red_flag" in stage1.SYSTEM_PROMPT


class TestVariantConfig:
    def test_stage1_v1_variant_uses_the_new_prompt(self):
        v = stage1_v1_variant()
        assert v.system_prompt == stage1.SYSTEM_PROMPT

    def test_stage1_v1_variant_requires_is_red_flag(self):
        v = stage1_v1_variant()
        assert v.requires_is_red_flag is True

    def test_production_variant_requires_is_red_flag(self):
        """2026-09-19 Stage 1 promotion: production's real prompt (now
        stage1_v1's content) asks for is_red_flag, so its own variant
        wrapper must request it too — this flipped from False (pre-
        promotion, when production's prompt predated the field)."""
        v = production_variant()
        assert v.requires_is_red_flag is True
