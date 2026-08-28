"""Side-by-side comparison metrics.

DELIBERATE DESIGN LIMIT — read this before adding a "score".

The founder's instruction is explicit: no LLM judge as the final authority,
human comparison required first. So this module computes only OBJECTIVE,
mechanically-checkable signals and refuses to emit an overall quality
number. It answers questions with a defensible right answer:

  * did the candidate output pass the SAME compliance validator the
    production output had to pass?
  * for red_flag, did it reach the same category decision? (a real
    confusion matrix — this is the one task with genuine ground truth)
  * did it obey the schema RedixFi's parser requires?
  * how do lengths, refusal rates and grounding overlap compare?

It does NOT judge factual correctness, reasoning quality, financial
terminology, or usefulness to an investor. Those are on the human review
sheet the report generates, and they stay there until a human fills them in.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Set

from ..compliance.validators import (ask_answer_violation, summarizer_violation,
                                      violation)
from ..prompts.concall_summary import TONE_LABELS

_WORD_RE = re.compile(r"[a-z0-9]+")
_STOPWORDS = frozenset({
    "the", "a", "an", "and", "or", "of", "to", "in", "for", "on", "with", "as",
    "is", "was", "were", "are", "be", "been", "by", "that", "this", "it", "its",
    "at", "from", "not", "no", "has", "have", "had", "which", "their", "they",
})


def _tokens(text: str) -> Set[str]:
    return {w for w in _WORD_RE.findall((text or "").lower()) if w not in _STOPWORDS and len(w) > 2}


def jaccard(a: str, b: str) -> float:
    ta, tb = _tokens(a), _tokens(b)
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def _ar_text(payload: Dict[str, Any]) -> str:
    parts = [
        payload.get("executive_summary") or "",
        " ".join(payload.get("key_points") or []),
        " ".join(payload.get("important_risks") or []),
        payload.get("key_takeaway") or "",
    ]
    return " ".join(p for p in parts if p)


def compare_annual_report(case: Dict[str, Any], candidate: Dict[str, Any]) -> Dict[str, Any]:
    reference = case.get("reference") or {}
    ref_text, cand_text = _ar_text(reference), _ar_text(candidate)

    def compliance(payload: Dict[str, Any]) -> Optional[str]:
        for field in ("executive_summary", "key_takeaway"):
            reason = summarizer_violation(payload.get(field) or "",
                                          check_financial_figures=True)
            if reason:
                return f"{field}: {reason}"
        for field in ("key_points", "important_risks"):
            for item in payload.get(field) or []:
                reason = summarizer_violation(item, check_financial_figures=True)
                if reason:
                    return f"{field}: {reason}"
        return None

    # SCHEMA MISMATCH GUARD. Production's 72 annual-report references are
    # LEGACY-shaped (summary/bullets/key_takeaway); this comparator reads the
    # CURRENT shape (executive_summary/key_points/important_risks). Running
    # the current-pipeline replay against a legacy reference therefore finds
    # no executive_summary and would report "empty text" as a COMPLIANCE
    # FAILURE for all 20 references — a reviewer would reasonably read that
    # as production having emitted non-compliant text, which is false. All 20
    # legacy references pass compliance when read with their own schema.
    reference_is_legacy_shaped = bool(reference) and (
        "executive_summary" not in reference and "summary" in reference)

    return {
        "reference_present": bool(reference),
        "reference_schema_matches_replay": not reference_is_legacy_shaped,
        "schema_mismatch_note": (
            "Reference is LEGACY-shaped (summary/bullets/key_takeaway) but this "
            "replay uses the CURRENT schema. Field-level comparison is not "
            "meaningful here — replay as 'annual_report_summary_legacy' for the "
            "like-for-like reading."
        ) if reference_is_legacy_shaped else None,
        "candidate_compliance": compliance(candidate),
        # Suppressed on a schema mismatch — see the guard above.
        "reference_compliance": (None if reference_is_legacy_shaped
                                 else (compliance(reference) if reference else None)),
        "candidate_key_point_count": len(candidate.get("key_points") or []),
        "reference_key_point_count": len(reference.get("key_points") or []),
        "candidate_risk_count": len(candidate.get("important_risks") or []),
        "reference_risk_count": len(reference.get("important_risks") or []),
        "candidate_chars": len(cand_text),
        "reference_chars": len(ref_text),
        "lexical_overlap": round(jaccard(ref_text, cand_text), 4),
        # Overlap is a WEAK signal — two faithful summaries of the same
        # evidence can word things very differently. It is reported to help
        # a human triage which cases to read closely, never as a score.
        "overlap_is_triage_only": True,
    }


def compare_red_flag(case: Dict[str, Any], candidate: Dict[str, Any]) -> Dict[str, Any]:
    reference = case.get("reference") or {}
    ref_category = reference.get("risk_flag_type")      # absent == not confirmed
    cand_category = candidate.get("risk_flag_type")

    if ref_category and cand_category:
        outcome = "agree" if ref_category == cand_category else "category_mismatch"
    elif ref_category and not cand_category:
        outcome = "false_negative"
    elif cand_category and not ref_category:
        outcome = "false_positive"
    else:
        outcome = "agree_no_flag"

    cand_summary = candidate.get("risk_flag_summary") or ""
    ref_summary = reference.get("risk_flag_summary") or ""

    return {
        "reference_present": bool(reference),
        "reference_category": ref_category,
        "candidate_category": cand_category,
        "outcome": outcome,
        "candidate_compliance": violation(cand_summary) if cand_summary else None,
        "reference_compliance": violation(ref_summary) if ref_summary else None,
        "candidate_summary_chars": len(cand_summary),
        "reference_summary_chars": len(ref_summary),
        "summary_overlap": round(jaccard(ref_summary, cand_summary), 4)
        if (ref_summary and cand_summary) else None,
    }


def _ask_reference_compliance(ref_answer: str, causal_backstop: bool):
    """Returns (reported_failure, is_backstop_artifact).

    A reference that passes WITHOUT the causal backstop but fails WITH it is
    an artifact of packet reconstruction (see compare_ask_ai), not evidence
    that production emitted non-compliant text. It is reported separately and
    not counted as a reference compliance failure."""
    if not ref_answer:
        return None, False
    with_backstop = ask_answer_violation(ref_answer, causal_backstop)
    if not with_backstop:
        return None, False
    without_backstop = ask_answer_violation(ref_answer, False)
    if causal_backstop and not without_backstop:
        return None, True          # artifact: suppressed, flagged
    return with_backstop, False


def compare_ask_ai(case: Dict[str, Any], candidate: Dict[str, Any]) -> Dict[str, Any]:
    reference = case.get("reference") or {}
    causal_backstop = bool(candidate.get("causal_backstop"))
    ref_answer = reference.get("answer") or ""
    cand_answer = candidate.get("answer") or ""

    ref_refused = reference.get("refused")
    cand_refused = bool(candidate.get("refused"))

    return {
        "reference_present": bool(reference),
        "candidate_refused": cand_refused,
        "reference_refused": ref_refused,
        "refusal_agreement": (None if ref_refused is None else cand_refused == bool(ref_refused)),
        "candidate_compliance": ask_answer_violation(cand_answer, causal_backstop),
        # RECONSTRUCTION ARTIFACT GUARD. `causal_backstop` is derived from the
        # REBUILT packet, not the historical one. If the packet carried a real
        # cause when production answered, the backstop was OFF and causal
        # language ("due to") was legitimately allowed; the rebuilt packet has
        # since lost that news event, so the backstop now reads ON and the same
        # answer looks non-compliant. Reporting that as a production compliance
        # failure would be wrong, so it is separated out rather than counted.
        "reference_compliance": _ask_reference_compliance(ref_answer, causal_backstop)[0],
        "reference_compliance_backstop_artifact":
            _ask_reference_compliance(ref_answer, causal_backstop)[1],
        "candidate_chars": len(cand_answer),
        "reference_chars": len(ref_answer),
        "lexical_overlap": round(jaccard(ref_answer, cand_answer), 4),
        "overlap_is_triage_only": True,
    }



def compare_annual_report_legacy(case, candidate):
    """LEGACY 3-field contract: summary / bullets / key_takeaway.

    This is the LIKE-FOR-LIKE comparison for Phase A — same prompt, same
    front-slice input, same schema as the gpt-4o-mini run that produced the
    stored reference on 2026-08-16. Only the model differs.
    """
    reference = case.get("reference") or {}

    def text_of(payload):
        return " ".join(p for p in [
            payload.get("summary") or "",
            " ".join(payload.get("bullets") or []),
            payload.get("key_takeaway") or "",
        ] if p)

    def compliance(payload):
        for field in ("summary", "key_takeaway"):
            reason = summarizer_violation(payload.get(field) or "",
                                          check_financial_figures=True)
            if reason:
                return f"{field}: {reason}"
        for item in payload.get("bullets") or []:
            reason = summarizer_violation(item, check_financial_figures=True)
            if reason:
                return f"bullets: {reason}"
        return None

    return {
        "reference_present": bool(reference),
        "comparison_is_like_for_like": True,
        "candidate_compliance": compliance(candidate),
        "reference_compliance": compliance(reference) if reference else None,
        "candidate_bullet_count": len(candidate.get("bullets") or []),
        "reference_bullet_count": len(reference.get("bullets") or []),
        "candidate_chars": len(text_of(candidate)),
        "reference_chars": len(text_of(reference)),
        "lexical_overlap": round(jaccard(text_of(reference), text_of(candidate)), 4),
        "overlap_is_triage_only": True,
    }


def compare_concall(case, candidate):
    """Concall carries the one genuinely objective quality signal in any
    summarization phase: `tone_label` is a 4-way CLOSED-SET classification
    the production model already committed to, so agreement on it is a real
    accuracy number rather than a similarity heuristic."""
    reference = case.get("reference") or {}
    ref_tone = reference.get("tone_label")
    cand_tone = candidate.get("tone_label")

    return {
        "reference_present": bool(reference),
        "reference_tone_label": ref_tone,
        "candidate_tone_label": cand_tone,
        "tone_label_agrees": (None if not (ref_tone and cand_tone)
                              else ref_tone == cand_tone),
        "tone_label_valid": cand_tone in TONE_LABELS if cand_tone else False,
        # summarizer_violation, NOT violation: concall_summarizer.py carries
        # the "call"-means-a-meeting carve-out, so "the earnings conference
        # call" is correct output. Using the risk-classifier variant here
        # flagged 6 of 20 REAL production references as non-compliant.
        "candidate_compliance": summarizer_violation(candidate.get("summary") or "")
                                or summarizer_violation(candidate.get("tone_note") or ""),
        "reference_compliance": (summarizer_violation(reference.get("summary") or "")
                                 or summarizer_violation(reference.get("tone_note") or ""))
                                if reference else None,
        "candidate_chars": len(candidate.get("summary") or ""),
        "reference_chars": len(reference.get("summary") or ""),
        "lexical_overlap": round(jaccard(reference.get("summary") or "",
                                         candidate.get("summary") or ""), 4),
        "overlap_is_triage_only": True,
    }


COMPARATORS = {
    "annual_report_summary": compare_annual_report,
    "annual_report_summary_legacy": compare_annual_report_legacy,
    "concall_summary": compare_concall,
    "red_flag": compare_red_flag,
    "ask_ai": compare_ask_ai,
}


def compare(task: str, case: Dict[str, Any], candidate: Dict[str, Any]) -> Dict[str, Any]:
    comparator = COMPARATORS.get(task)
    if comparator is None:
        return {"error": f"no comparator for task '{task}'"}
    return comparator(case, candidate)


def aggregate(task: str, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Roll-up of the objective signals only. Explicitly carries no overall
    quality verdict — that is the human reviewer's output, not this
    module's."""
    total = len(rows)
    if not total:
        return {"cases": 0}

    comparisons = [r.get("comparison") or {}for r in rows]
    generated = [r for r in rows if r.get("ok")]

    summary: Dict[str, Any] = {
        "cases": total,
        "generated_ok": len(generated),
        "generation_failures": total - len(generated),
        "candidate_compliance_failures": sum(
            1 for c in comparisons if c.get("candidate_compliance")
        ),
        "reference_backstop_artifacts": sum(
            1 for c in comparisons if c.get("reference_compliance_backstop_artifact")
        ),
        "reference_compliance_failures": sum(
            1 for c in comparisons if c.get("reference_compliance")
        ),
        "cases_with_reference": sum(1 for c in comparisons if c.get("reference_present")),
        "json_repair_used": sum(1 for r in rows if r.get("json_repair_used")),
        "mean_latency_sec": round(
            sum(r.get("latency_sec") or 0 for r in rows) / total, 3
        ),
        "total_prompt_tokens": sum(r.get("prompt_tokens") or 0 for r in rows),
        "total_completion_tokens": sum(r.get("completion_tokens") or 0 for r in rows),
        "quality_verdict": "NOT COMPUTED — requires human review, by design",
    }

    if task == "red_flag":
        outcomes: Dict[str, int] = {}
        for c in comparisons:
            key = c.get("outcome") or "unknown"
            outcomes[key] = outcomes.get(key, 0) + 1
        summary["outcomes"] = outcomes
        decided = sum(
            outcomes.get(k, 0) for k in
            ("agree", "agree_no_flag", "category_mismatch", "false_positive", "false_negative")
        )
        if decided:
            agree = outcomes.get("agree", 0) + outcomes.get("agree_no_flag", 0)
            summary["agreement_rate"] = round(agree / decided, 4)

    if task == "concall_summary":
        decided = [c for c in comparisons if c.get("tone_label_agrees") is not None]
        if decided:
            summary["tone_label_agreement_rate"] = round(
                sum(1 for c in decided if c["tone_label_agrees"]) / len(decided), 4)
        summary["invalid_tone_labels"] = sum(
            1 for c in comparisons
            if c.get("candidate_tone_label") and not c.get("tone_label_valid"))
        tones = {}
        for c in comparisons:
            key = f"{c.get('reference_tone_label')}->{c.get('candidate_tone_label')}"
            tones[key] = tones.get(key, 0) + 1
        summary["tone_confusion"] = tones

    if task == "ask_ai":
        decided = [c for c in comparisons if c.get("refusal_agreement") is not None]
        if decided:
            summary["refusal_agreement_rate"] = round(
                sum(1 for c in decided if c["refusal_agreement"]) / len(decided), 4
            )

    overlaps = [c["lexical_overlap"] for c in comparisons
                if isinstance(c.get("lexical_overlap"), (int, float))]
    if overlaps:
        summary["mean_lexical_overlap"] = round(sum(overlaps) / len(overlaps), 4)

    return summary
