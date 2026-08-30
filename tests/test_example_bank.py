"""The example bank: storage, retrieval, and the leave-one-out guarantee
a fair test depends on.
"""
import json
import os

import pytest

from app.example_bank import (load_bank, record_result, retrieval_text_for,
                              retrieve, save_bank)


@pytest.fixture()
def bank_dir(tmp_path):
    return str(tmp_path / "example_bank")


class TestStorage:
    def test_empty_bank_when_file_absent(self, bank_dir):
        assert load_bank("concall_summary", bank_dir) == []

    def test_save_then_load_round_trips(self, bank_dir):
        entries = [{"benchmark_id": "X", "output": {"summary": "s"}}]
        path = save_bank("concall_summary", entries, bank_dir)
        assert os.path.exists(path)
        assert load_bank("concall_summary", bank_dir) == entries

    def test_tasks_are_isolated_in_separate_files(self, bank_dir):
        save_bank("concall_summary", [{"benchmark_id": "A"}], bank_dir)
        save_bank("red_flag", [{"benchmark_id": "B"}], bank_dir)
        assert load_bank("concall_summary", bank_dir) == [{"benchmark_id": "A"}]
        assert load_bank("red_flag", bank_dir) == [{"benchmark_id": "B"}]


class TestRecordResult:
    FIXTURE = {"benchmark_id": "CC_TEST_1", "company_name": "Test Ltd",
              "symbol": "TEST", "doc_kind": "earnings concall transcript",
              "input_text": "Test Ltd reported strong quarterly results."}

    def test_records_a_validated_output(self, bank_dir):
        record_result("concall_summary", self.FIXTURE, {"summary": "s", "tone_label": "Positive",
                                                         "tone_note": "n"},
                      attempts_used=1, model="qwen3-14b-awq-tp2", run_id="r1",
                      bank_dir=bank_dir)
        entries = load_bank("concall_summary", bank_dir)
        assert len(entries) == 1
        assert entries[0]["benchmark_id"] == "CC_TEST_1"
        assert entries[0]["was_hard_case"] is False

    def test_multi_attempt_case_flagged_as_hard(self, bank_dir):
        record_result("concall_summary", self.FIXTURE, {"summary": "s"},
                      attempts_used=4, model="m", run_id="r1", bank_dir=bank_dir)
        assert load_bank("concall_summary", bank_dir)[0]["was_hard_case"] is True

    def test_recording_the_same_case_again_replaces_not_duplicates(self, bank_dir):
        record_result("concall_summary", self.FIXTURE, {"summary": "old"},
                      attempts_used=3, model="m", run_id="r1", bank_dir=bank_dir)
        record_result("concall_summary", self.FIXTURE, {"summary": "new"},
                      attempts_used=1, model="m", run_id="r2", bank_dir=bank_dir)
        entries = load_bank("concall_summary", bank_dir)
        assert len(entries) == 1
        assert entries[0]["output"]["summary"] == "new"

    def test_missing_benchmark_id_is_not_recorded(self, bank_dir):
        record_result("concall_summary", {}, {"summary": "s"},
                      attempts_used=1, model="m", run_id="r1", bank_dir=bank_dir)
        assert load_bank("concall_summary", bank_dir) == []


class TestRetrieve:
    ENTRIES = [
        {"benchmark_id": "A", "retrieval_text": "steel manufacturer capacity expansion quarterly results"},
        {"benchmark_id": "B", "retrieval_text": "pharmaceutical company drug approval revenue growth"},
        {"benchmark_id": "C", "retrieval_text": "steel producer plant capacity utilization results"},
    ]

    def test_retrieves_the_most_similar_entries(self):
        # Query about steel/capacity should rank A and C above B.
        top = retrieve(self.ENTRIES, "steel capacity expansion results", k=2)
        ids = {e["benchmark_id"] for e in top}
        assert ids == {"A", "C"}

    def test_excludes_the_current_case_by_id(self):
        """The core guarantee a leave-one-out test depends on: a case must
        never retrieve its own stored answer."""
        top = retrieve(self.ENTRIES, "steel capacity expansion results",
                       k=3, exclude_benchmark_id="A")
        ids = {e["benchmark_id"] for e in top}
        assert "A" not in ids

    def test_zero_similarity_entries_are_never_returned(self):
        """A completely unrelated entry should not fill out the top-k just
        because k asks for more than there are good matches."""
        top = retrieve([{"benchmark_id": "Z", "retrieval_text": ""}],
                       "steel capacity expansion", k=2)
        assert top == []

    def test_empty_bank_returns_nothing(self):
        assert retrieve([], "anything", k=2) == []


class TestRetrievalTextForConcall:
    def test_builds_from_company_symbol_and_opening_text(self):
        fixture = {"company_name": "Acme Ltd", "symbol": "ACME",
                  "doc_kind": "earnings concall transcript",
                  "input_text": "Acme reported revenue growth this quarter."}
        text = retrieval_text_for("concall_summary", fixture)
        assert "Acme Ltd" in text
        assert "ACME" in text
        assert "revenue growth" in text

    def test_truncates_the_input_text_not_the_whole_transcript(self):
        fixture = {"company_name": "X", "input_text": "word " * 5000}
        text = retrieval_text_for("concall_summary", fixture)
        # 800-char cap on the input slice keeps retrieval topical, not a
        # full-document comparison dominated by boilerplate structure.
        assert len(text) < 1000


# --------------------------------------------------------------------------
# The ongoing-accumulation hook in app/evaluation/runner.py. This is the
# part that makes the bank a MECHANISM rather than a one-time bootstrap —
# every real run must grow it automatically, and an offline/echo rehearsal
# must never write fake examples into it.
# --------------------------------------------------------------------------
import sys as _sys

from app.evaluation import fixtures as fixtures_mod  # noqa: E402
from app.evaluation.runner import run_evaluation  # noqa: E402
from app.inference.echo import EchoBackend  # noqa: E402

# Reuse the real ScriptedBackend from the harness tests rather than a
# second hand-rolled stub.
_TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TESTS_DIR not in _sys.path:
    _sys.path.insert(0, _TESTS_DIR)
from test_tasks_and_harness import ScriptedBackend  # noqa: E402


_REAL_SAMPLE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "fixtures", "sample_concall_summary.json")


def _concall_fixture_set(tmp_path):
    """A one-case concall fixture built by taking the FIRST real case from
    fixtures/sample_concall_summary.json and overwriting only its
    benchmark_id/input_text — guarantees every schema-required field
    (provenance, input_stats, etc.) is present and valid, since it comes
    from a fixture that already loads successfully, rather than a
    hand-rolled guess at the schema."""
    doc = json.loads(open(_REAL_SAMPLE, encoding="utf-8").read())
    case = dict(doc["cases"][0])
    case["benchmark_id"] = "CC_RUNNER_TEST"
    case["company_name"] = "Runner Ltd"
    case["input_text"] = "Runner Ltd reported results."
    doc["cases"] = [case]
    path = tmp_path / "concall_fixture.json"
    path.write_text(json.dumps(doc), encoding="utf-8")
    return fixtures_mod.load(str(path))


class TestRunnerAccumulatesTheBank:
    VALID_RESPONSE = json.dumps({"summary": "Runner Ltd reported steady results.",
                                 "tone_label": "Neutral", "tone_note": "Neutral tone."})

    def test_a_real_backends_ok_result_is_recorded(self, tmp_path):
        bank_dir = str(tmp_path / "bank")
        fs = _concall_fixture_set(tmp_path)
        run_evaluation(ScriptedBackend([self.VALID_RESPONSE]), fs, "test-model",
                       bank_dir=bank_dir)
        entries = load_bank("concall_summary", bank_dir)
        assert len(entries) == 1
        assert entries[0]["benchmark_id"] == "CC_RUNNER_TEST"

    def test_echo_backend_never_writes_to_the_bank(self, tmp_path):
        """The critical safety gate: an offline rehearsal must never pollute
        the accumulating store with synthetic text."""
        bank_dir = str(tmp_path / "bank")
        fs = _concall_fixture_set(tmp_path)
        run_evaluation(EchoBackend(), fs, "echo-model", bank_dir=bank_dir)
        assert load_bank("concall_summary", bank_dir) == []

    def test_record_to_bank_false_opts_out_even_for_a_real_backend(self, tmp_path):
        bank_dir = str(tmp_path / "bank")
        fs = _concall_fixture_set(tmp_path)
        run_evaluation(ScriptedBackend([self.VALID_RESPONSE]), fs, "test-model",
                       bank_dir=bank_dir, record_to_bank=False)
        assert load_bank("concall_summary", bank_dir) == []

    def test_the_default_bank_dir_is_the_real_repo_location(self):
        """Guards against a regression where the default silently pointed
        somewhere other than the shared, committed example_bank/ directory
        — the whole mechanism depends on every caller landing in one place
        unless they explicitly redirect it (as every test here does)."""
        import inspect

        from app import example_bank as eb
        sig = inspect.signature(run_evaluation)
        assert sig.parameters["bank_dir"].default == eb.BANK_DIR

    def test_recorded_entry_carries_the_same_run_id_as_the_saved_run(self, tmp_path):
        """run_id used to be generated a second time at the end of
        run_evaluation, producing a DIFFERENT timestamp than whatever was
        attached to bank entries during the loop. Pin that both match."""
        bank_dir = str(tmp_path / "bank")
        fs = _concall_fixture_set(tmp_path)
        run = run_evaluation(ScriptedBackend([self.VALID_RESPONSE]), fs, "test-model",
                             bank_dir=bank_dir)
        entries = load_bank("concall_summary", bank_dir)
        assert entries[0]["run_id"] == run["run_id"]
