#!/usr/bin/env python3
"""ACTION 3 diagnostics — did the retry fix actually change anything?

Answers four questions the founder asked, from run artifacts only:

  1. New generated / compliance-failure counts, against the prior run.
  2. For every case that STILL fails: is it failing for a new reason, or
     is it the same clause repeating? The second would mean the sampling
     change did not really take effect.
  3. Did concall's tone_label_agreement_rate move from 0.7333?
  4. SPOT-CHECK: is attempt-2+ text genuinely different from attempt 1?
     Read from the recorded raw generations, never assumed from the fact
     that a temperature was set.

    python scripts/diagnose_retry_fix.py --before <old.json> --after <new.json>
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from typing import Any, Dict, List, Optional


def _sim(a: str, b: str) -> float:
    """Similarity between two attempts. High means the retry regenerated
    essentially the same text — the bug this fix targets."""
    return difflib.SequenceMatcher(None, a or "", b or "").ratio()


def _attempt_text(rej: Dict[str, Any]) -> str:
    t = rej.get("text")
    if isinstance(t, dict):
        parts = []
        for key in ("summary", "tone_note", "executive_summary", "key_takeaway"):
            if t.get(key):
                parts.append(str(t[key]))
        for key in ("key_points", "important_risks", "bullets"):
            for item in t.get(key) or []:
                parts.append(str(item))
        return " ".join(parts)
    return str(t or rej.get("raw_text") or "")


def _summary(run: Dict[str, Any]) -> Dict[str, Any]:
    return run.get("summary") or {}


def _failures(run: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    out = {}
    for row in run.get("results") or []:
        if not row.get("ok"):
            bid = (row.get("case_meta") or {}).get("benchmark_id") or row.get("fixture_id")
            out[bid] = row
    return out


def _quoted_words(rejections: List[Dict[str, Any]]) -> List[Optional[str]]:
    words = []
    for r in rejections:
        m = re.search(r"'([^']+)'", str(r.get("reason") or ""))
        words.append(m.group(1) if m else None)
    return words


def report_case(bid: str, row: Dict[str, Any]) -> None:
    rejections = row.get("rejections") or []
    print(f"\n  {bid}")
    print(f"    attempts: {row.get('attempts')}   error: {row.get('error')}")
    texts = [_attempt_text(r) for r in rejections]
    words = _quoted_words(rejections)
    for i, r in enumerate(rejections):
        samp = r.get("sampling") or {}
        print(f"    attempt {r.get('pass')}: temp={samp.get('temperature')} "
              f"seed={samp.get('seed')}  reason={str(r.get('reason'))[:90]}")
    # Same clause every time, or genuinely different failures?
    if len(texts) >= 2:
        sims = [_sim(texts[i - 1], texts[i]) for i in range(1, len(texts))]
        print(f"    text similarity attempt-to-attempt: "
              f"{', '.join(f'{s:.3f}' for s in sims)}")
        distinct_words = {w for w in words if w}
        if all(s > 0.95 for s in sims):
            verdict = ("STILL REPEATING — retries regenerated near-identical "
                       "text; the sampling change did NOT take effect here")
        elif all(s > 0.80 for s in sims):
            verdict = ("MOSTLY REPEATING — retries varied only slightly; "
                       "sampling took effect but did not escape the phrasing")
        elif len(distinct_words) > 1:
            verdict = (f"NEW REASON — retries produced different text and "
                       f"tripped different rules: {sorted(distinct_words)}")
        else:
            verdict = (f"DIFFERENT TEXT, SAME RULE — retries genuinely varied "
                       f"but kept hitting '{list(distinct_words)[0] if distinct_words else '?'}'")
        print(f"    -> {verdict}")


def spot_check(run: Dict[str, Any], label: str) -> None:
    """Confirm from the RAW recorded text that a retry really differed.
    A policy can be correct and unwired; this reads the evidence."""
    print(f"\n{'=' * 72}\nSPOT-CHECK — is attempt 2+ text actually different? [{label}]\n{'=' * 72}")
    checked = 0
    for row in run.get("results") or []:
        rejections = row.get("rejections") or []
        if len(rejections) < 2:
            continue
        bid = (row.get("case_meta") or {}).get("benchmark_id") or row.get("fixture_id")
        t1, t2 = _attempt_text(rejections[0]), _attempt_text(rejections[1])
        s1 = (rejections[0].get("sampling") or {})
        s2 = (rejections[1].get("sampling") or {})
        sim = _sim(t1, t2)
        print(f"\n  {bid}")
        print(f"    attempt 1 sampling: {s1}")
        print(f"    attempt 2 sampling: {s2}")
        print(f"    similarity: {sim:.4f}  "
              f"({'IDENTICAL — fix not working' if sim > 0.98 else 'genuinely different'})")
        print(f"    attempt 1: {t1[:220]}")
        print(f"    attempt 2: {t2[:220]}")
        checked += 1
        if checked >= 4:
            break
    if not checked:
        print("  No case needed a retry — nothing to spot-check. That is "
              "itself a result: every case passed on attempt 1.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    ap.add_argument("--label", default="")
    args = ap.parse_args()

    before = json.load(open(args.before, encoding="utf-8"))
    after = json.load(open(args.after, encoding="utf-8"))
    label = args.label or after.get("task")

    print("=" * 72)
    print(f"ACTION 3 — {label}")
    print("=" * 72)
    print(f"before: {args.before}\n         run_id={before.get('run_id')} "
          f"policy={(before.get('retry_policy') or {}).get('name', 'production')}")
    print(f"after : {args.after}\n         run_id={after.get('run_id')} "
          f"policy={(after.get('retry_policy') or {}).get('name')}")

    sb, sa = _summary(before), _summary(after)
    print(f"\n{'metric':38} {'before':>10} {'after':>10}   delta")
    print("-" * 72)
    for key in ("cases", "generated_ok", "generation_failures",
                "candidate_compliance_failures", "reference_compliance_failures",
                "tone_label_agreement_rate", "invalid_tone_labels",
                "guided_and_clean", "json_repair_used", "mean_lexical_overlap",
                "mean_latency_sec"):
        if key not in sb and key not in sa:
            continue
        b, a = sb.get(key), sa.get(key)
        delta = ""
        if isinstance(b, (int, float)) and isinstance(a, (int, float)):
            d = a - b
            delta = f"{d:+.4f}" if isinstance(d, float) else f"{d:+d}"
        print(f"{key:38} {str(b):>10} {str(a):>10}   {delta}")

    fb, fa = _failures(before), _failures(after)
    fixed = sorted(set(fb) - set(fa))
    still = sorted(set(fb) & set(fa))
    new = sorted(set(fa) - set(fb))
    print(f"\nREPAIRED ({len(fixed)}): {fixed or '—'}")
    print(f"STILL FAILING ({len(still)}): {still or '—'}")
    print(f"NEWLY FAILING ({len(new)}): {new or '—'}")

    if still:
        print(f"\n{'=' * 72}\nSTILL-FAILING CASES — new reason, or same repetition?\n{'=' * 72}")
        for bid in still:
            report_case(bid, fa[bid])
    if new:
        print(f"\n{'=' * 72}\nNEWLY-FAILING CASES\n{'=' * 72}")
        for bid in new:
            report_case(bid, fa[bid])

    spot_check(after, label)


if __name__ == "__main__":
    main()
