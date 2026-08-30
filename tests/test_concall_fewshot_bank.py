"""The retrieval-augmented few-shot variant must leave the system prompt
completely untouched and only add retrieved content to the user message.
"""
from app.example_bank import record_result
from app.experiments.concall_variants import fewshot_bank_variant
from app.prompts import concall_summary as prod
from app.prompts import concall_summary_fewshot_bank as fb


class TestSystemPromptUnmodified:
    def test_system_prompt_is_byte_identical_to_production(self):
        """The whole premise of this variant is that it changes a
        DIFFERENT axis than every other prompt experiment this session —
        the system prompt must not drift by even one character."""
        assert fb.SYSTEM_PROMPT == prod.SYSTEM_PROMPT

    def test_no_forbidden_vocabulary_is_named_anywhere(self):
        """Contrast with markdown-fairness/steering/instance-check, which
        all named forbidden words or added new rules. This variant must
        add ZERO new prompt text — only retrieved case content."""
        assert fb.SYSTEM_PROMPT == prod.SYSTEM_PROMPT  # nothing appended at all


class TestUserContentRetrieval:
    FIXTURE = {"benchmark_id": "CC_QUERY", "company_name": "Query Ltd",
              "symbol": "QRY", "doc_kind": "earnings concall transcript",
              "input_text": "Query Ltd steel manufacturer reported capacity expansion."}

    BANK = [
        {"benchmark_id": "CC_SIMILAR",
         "retrieval_text": "Similar Ltd steel manufacturer capacity expansion results",
         "output": {"summary": "Similar Ltd summary text.", "tone_label": "Positive",
                    "tone_note": "Positive tone."}},
        {"benchmark_id": "CC_UNRELATED",
         "retrieval_text": "Pharma Ltd drug approval trial results",
         "output": {"summary": "Pharma summary.", "tone_label": "Neutral",
                    "tone_note": "Neutral tone."}},
    ]

    def test_no_bank_falls_back_to_production_content_exactly(self):
        assert (fb.build_variant_user_content(self.FIXTURE, [])
                == prod.build_user_content(self.FIXTURE))

    def test_retrieved_example_is_prepended(self):
        content = fb.build_variant_user_content(self.FIXTURE, self.BANK, k=2)
        assert "Similar Ltd summary text." in content
        assert content.index("Similar Ltd summary text.") < content.index("Query Ltd")

    def test_production_content_is_still_present_verbatim_after_examples(self):
        content = fb.build_variant_user_content(self.FIXTURE, self.BANK)
        assert prod.build_user_content(self.FIXTURE) in content

    def test_a_case_never_retrieves_its_own_bank_entry(self):
        """The current case's own benchmark_id must be excluded even if it
        happens to already be in the bank — the leave-one-out guarantee."""
        bank_with_self = self.BANK + [{
            "benchmark_id": "CC_QUERY",
            "retrieval_text": "Query Ltd steel manufacturer capacity expansion",
            "output": {"summary": "THIS MUST NEVER APPEAR", "tone_label": "Positive",
                      "tone_note": "n"},
        }]
        content = fb.build_variant_user_content(self.FIXTURE, bank_with_self)
        assert "THIS MUST NEVER APPEAR" not in content

    def test_corrective_note_still_passes_through_to_production_content(self):
        content = fb.build_variant_user_content(self.FIXTURE, [], corrective_note="fix this")
        assert "fix this" in content


class TestVariantConfig:
    def test_defaults_to_improved_policy(self):
        from app.tasks.retry_policy import IMPROVED_POLICY
        v = fewshot_bank_variant([])
        assert v.policy is IMPROVED_POLICY

    def test_max_attempts_defaults_to_production(self):
        v = fewshot_bank_variant([])
        assert v.max_attempts == prod.MAX_ATTEMPTS

    def test_max_attempts_overridable(self):
        v = fewshot_bank_variant([], max_attempts=8)
        assert v.max_attempts == 8

    def test_user_content_fn_is_wired(self):
        bank = [{"benchmark_id": "X", "retrieval_text": "steel capacity",
                "output": {"summary": "s", "tone_label": "Positive", "tone_note": "n"}}]
        fixture = {"benchmark_id": "Y", "company_name": "Y Ltd",
                  "input_text": "Y Ltd steel capacity expansion"}
        v = fewshot_bank_variant(bank, k=1)
        content = v.user_content_fn(fixture, None)
        assert "s" in content or "summary" in content.lower()
        assert content != prod.build_user_content(fixture)  # bank entry actually changed it

    def test_description_states_no_forbidden_vocabulary_is_named(self):
        d = fewshot_bank_variant([]).description
        assert "forbidden vocabulary" in d.lower() or "no forbidden" in d.lower()


class TestEndToEndWithRealRecordedResult:
    """Bank entries recorded via record_result() must be directly usable by
    the variant — the storage format and the consumption format must
    actually agree, not just look compatible on paper."""

    def test_a_recorded_result_is_retrievable_and_renderable(self, tmp_path):
        from app.example_bank import load_bank
        bank_dir = str(tmp_path / "bank")
        source_fixture = {"benchmark_id": "CC_SOURCE", "company_name": "Source Ltd",
                          "symbol": "SRC", "doc_kind": "earnings concall transcript",
                          "input_text": "Source Ltd steel manufacturer capacity expansion."}
        record_result("concall_summary", source_fixture,
                      {"summary": "Source Ltd summary.", "tone_label": "Positive",
                       "tone_note": "n"},
                      attempts_used=2, model="qwen3-14b-awq-tp2", run_id="r1",
                      bank_dir=bank_dir)
        bank = load_bank("concall_summary", bank_dir)

        query_fixture = {"benchmark_id": "CC_QUERY2", "company_name": "Query Ltd",
                         "input_text": "Query Ltd steel manufacturer capacity expansion."}
        content = fb.build_variant_user_content(query_fixture, bank)
        assert "Source Ltd summary." in content
