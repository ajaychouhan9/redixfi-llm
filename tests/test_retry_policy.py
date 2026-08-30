"""The retry policy must change retries and ONLY retries.

The production default has to stay byte-identical in behaviour, because
every earlier benchmark number was produced under it and the comparison
against gpt-4o-mini depends on that.
"""
from app.tasks.retry_policy import (IMPROVED_POLICY, PRODUCTION_POLICY,
                                    build_corrective_note)


class TestProductionUnchanged:
    def test_temperature_never_varies(self):
        for attempt in range(1, 7):
            assert PRODUCTION_POLICY.temperature_for(attempt, 0.0) == 0.0

    def test_seed_never_varies(self):
        for attempt in range(1, 7):
            assert PRODUCTION_POLICY.seed_for(attempt, 0) == 0

    def test_note_is_the_validators_message_verbatim(self):
        reason = "forward-tense word 'expected'"
        out = {"summary": "Revenue is expected to grow."}
        assert build_corrective_note(reason, out, ["summary"],
                                     PRODUCTION_POLICY) == reason


class TestImprovedVariesOnlyOnRetry:
    def test_attempt_one_stays_deterministic(self):
        """The baseline must remain reproducible — that is the whole reason
        attempt 1 is excluded from the change."""
        assert IMPROVED_POLICY.temperature_for(1, 0.0) == 0.0
        assert IMPROVED_POLICY.seed_for(1, 0) == 0

    def test_retries_sample_differently(self):
        assert IMPROVED_POLICY.temperature_for(2, 0.0) > 0.0
        assert IMPROVED_POLICY.seed_for(2, 0) != 0

    def test_each_retry_differs_from_the_one_before(self):
        seeds = [IMPROVED_POLICY.seed_for(a, 0) for a in range(1, 7)]
        assert len(set(seeds)) == len(seeds)

    def test_seed_shift_is_reproducible(self):
        """Varying is not the same as random: re-running the benchmark must
        reproduce the identical sequence."""
        assert ([IMPROVED_POLICY.seed_for(a, 7) for a in range(1, 5)]
                == [IMPROVED_POLICY.seed_for(a, 7) for a in range(1, 5)])

    def test_none_seed_stays_none(self):
        assert IMPROVED_POLICY.seed_for(3, None) is None


class TestDirectiveNote:
    def test_quotes_the_rejected_sentence(self):
        """The measured failure was the model repeating the SAME clause, so
        the note has to name that clause, not just the rule."""
        out = {"summary": "Revenue rose 12%. Production is expected to "
                          "commence in September 2026. Margins held."}
        note = build_corrective_note("forward-tense word 'expected'", out,
                                     ["summary"], IMPROVED_POLICY)
        assert "Production is expected to commence in September 2026." in note
        assert "Revenue rose 12%" not in note      # only the offending sentence
        assert "REWRITE" in note

    def test_offers_the_compliant_reframing(self):
        note = build_corrective_note("forward-tense word 'expected'",
                                     {"summary": "It is expected to rise."},
                                     ["summary"], IMPROVED_POLICY)
        assert "management set a goal of" in note

    def test_searches_list_fields(self):
        out = {"summary": "", "key_points": ["Capacity grew.",
                                             "Output will double."]}
        note = build_corrective_note("forward-tense word 'will'", out,
                                     ["summary", "key_points"], IMPROVED_POLICY)
        assert "Output will double." in note

    def test_falls_back_when_clause_not_locatable(self):
        """A reason whose word appears in no field must still produce usable
        instruction rather than an empty or misleading quote."""
        note = build_corrective_note("forward-tense word 'forecast'",
                                     {"summary": "Nothing matching here."},
                                     ["summary"], IMPROVED_POLICY)
        assert "forecast" in note
        assert "REWRITE THIS SENTENCE" not in note

    def test_unquotable_reason_passes_through(self):
        reason = "key_points count 7 outside [3, 5]"
        assert build_corrective_note(reason, {}, ["summary"],
                                     IMPROVED_POLICY) == reason


class TestRetriesExtendedVariant:
    """The original retries_6 result (repaired 2/5) was measured under
    PRODUCTION_POLICY, where every attempt is temperature=0 and therefore
    a retry mostly reproduces attempt 1's rejected text verbatim. That
    tested "does budget help when retries are identical" — a different
    question from "does budget help now that retries genuinely differ".
    These pin that the extended variant asks the SECOND question."""

    def test_uses_improved_policy_not_production(self):
        from app.experiments.concall_variants import retries_extended_variant
        v = retries_extended_variant()
        assert v.policy is IMPROVED_POLICY

    def test_prompt_is_unmodified_production(self):
        from app.experiments.concall_variants import retries_extended_variant
        from app.prompts import concall_summary as prod
        v = retries_extended_variant()
        assert v.system_prompt == prod.SYSTEM_PROMPT

    def test_default_budget_is_8_not_the_old_6(self):
        from app.experiments.concall_variants import retries_extended_variant
        v = retries_extended_variant()
        assert v.max_attempts == 8

    def test_budget_is_configurable(self):
        from app.experiments.concall_variants import retries_extended_variant
        v = retries_extended_variant(max_attempts=10)
        assert v.max_attempts == 10

    def test_old_retries_variant_default_is_unaffected(self):
        """retries_variant(6) with no policy arg must still behave exactly
        as it did when the original retries_6 result was measured — every
        existing conclusion drawn from that result depends on this."""
        from app.experiments.concall_variants import retries_variant
        from app.tasks.retry_policy import PRODUCTION_POLICY as PP
        v = retries_variant(6)
        assert v.policy is PP
        assert v.max_attempts == 6
