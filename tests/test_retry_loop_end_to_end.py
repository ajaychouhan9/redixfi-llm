"""End-to-end proof that the retry fix changes what the loop actually does.

Unit-testing `RetryPolicy` proves the arithmetic. It does NOT prove the
policy is wired into the task runners — and a policy that is correct but
unwired would produce exactly the same benchmark numbers as before while
looking fixed. These tests drive the real `run()` with a fake backend that
reproduces the OBSERVED failure mode:

    at temperature 0 the model re-emits the identical rejected clause;
    given a different temperature/seed it can produce something else.

That is the KANPRPLA pattern ("expected to commence production in
September 2026" five times running) in miniature.
"""
import json

from app.inference.base import GenerationResult
from app.tasks import concall_summary as task_cc
from app.tasks.retry_policy import IMPROVED_POLICY, PRODUCTION_POLICY

FORBIDDEN = ("Management said the plant is expected to commence production "
             "in September 2026.")
COMPLIANT = ("Management highlighted plans to commission the plant, and "
             "reported that construction is on schedule.")


class StuckBackend:
    """Deterministic sampling reproduces the rejected text; varied sampling
    lets a different phrasing through. Records every request for assertion."""

    name = "stuck-fake"

    def __init__(self):
        self.requests = []

    def generate(self, request):
        self.requests.append(request)
        varied = request.temperature > 0.0
        summary = COMPLIANT if varied else FORBIDDEN
        return GenerationResult(
            text=json.dumps({"summary": summary, "tone_label": "Neutral",
                             "tone_note": "The presentation highlighted results."}),
            model=request.model,
            backend=self.name,
        )


FIXTURE = {"benchmark_id": "CC_TEST_1", "company_name": "Test Ltd",
           "symbol": "TEST", "filing_date": "2026-01-01",
           "input_text": "transcript text"}


class TestProductionStillReproducesTheBug:
    """The baseline must keep failing exactly as measured — otherwise the
    17/20 and 15/20 numbers would not be comparable to the new run."""

    def test_all_attempts_identical_and_run_fails(self):
        backend = StuckBackend()
        result = task_cc.run(backend, FIXTURE, "m", policy=PRODUCTION_POLICY)

        assert result.ok is False
        assert result.attempts == 3
        temps = [r.temperature for r in backend.requests]
        seeds = [r.seed for r in backend.requests]
        assert temps == [0.0, 0.0, 0.0]
        assert seeds == [0, 0, 0]
        texts = {r["text"]["summary"] for r in result.rejections}
        assert texts == {FORBIDDEN}, "the bug is identical text on every retry"


class TestImprovedPolicyBreaksTheLoop:
    def test_retry_varies_sampling_and_succeeds(self):
        backend = StuckBackend()
        result = task_cc.run(backend, FIXTURE, "m", policy=IMPROVED_POLICY)

        assert result.ok is True
        assert result.attempts == 2, "should recover on the first varied retry"
        assert result.output["summary"] == COMPLIANT

    def test_attempt_one_is_still_deterministic(self):
        """Non-negotiable: the first attempt must match the baseline exactly,
        or the new run stops being comparable to the old one."""
        backend = StuckBackend()
        task_cc.run(backend, FIXTURE, "m", policy=IMPROVED_POLICY)
        first = backend.requests[0]
        assert first.temperature == 0.0
        assert first.seed == 0

    def test_retry_sampling_differs_from_attempt_one(self):
        backend = StuckBackend()
        task_cc.run(backend, FIXTURE, "m", policy=IMPROVED_POLICY)
        second = backend.requests[1]
        assert second.temperature > 0.0
        assert second.seed != 0

    def test_rejections_record_the_sampling_used(self):
        """The spot-check in the re-test reads these fields; if they were
        missing the verification would silently become an assumption."""
        backend = StuckBackend()
        result = task_cc.run(backend, FIXTURE, "m", policy=IMPROVED_POLICY)
        rejection = result.rejections[0]
        assert rejection["sampling"] == {"temperature": 0.0, "seed": 0}
        assert "raw_text" in rejection

    def test_retry_prompt_carries_the_directive_note(self):
        """The second request's user content must quote the rejected clause,
        not merely name the violated rule."""
        backend = StuckBackend()
        task_cc.run(backend, FIXTURE, "m", policy=IMPROVED_POLICY)
        retry_user_msg = backend.requests[1].messages[-1].content
        assert "REWRITE THIS SENTENCE" in retry_user_msg
        assert FORBIDDEN in retry_user_msg
        assert "management set a goal of" in retry_user_msg

    def test_production_note_stays_descriptive(self):
        backend = StuckBackend()
        task_cc.run(backend, FIXTURE, "m", policy=PRODUCTION_POLICY)
        retry_user_msg = backend.requests[1].messages[-1].content
        assert "REWRITE THIS SENTENCE" not in retry_user_msg
