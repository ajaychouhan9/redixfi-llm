"""Real regression test for the 2026-09-04 field-mapping bug:
writeback_annual_report.py unconditionally wrote `summary: None` /
`bullets: None` for real Qwen output (which only ever populates
executive_summary/key_points/important_risks), nulling out a perfectly
good pre-existing gpt-4o-mini summary on real production documents
(ADANIPOWER, SBILIFE both went blank on the live Research page).

Uses the REAL Qwen output shape from the first real AR pipeline test run
this session produced (not a synthetic shape) as the primary fixture.

Run: python production/test_writeback_field_mapping.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from writeback_annual_report import build_update

FAIL = []


def check(label: str, cond: bool, detail: str = ""):
    print(f"[{'PASS' if cond else 'FAIL'}] {label}")
    if not cond:
        FAIL.append(f"{label} — {detail}")


# THE REAL BUG CASE — Qwen's real output shape (verified against the
# actual ADANIPOWER kaggle-output row this session), no summary/bullets
# keys at all, only the newer schema.
qwen_real_shape = {
    "executive_summary": "Adani Power Limited's FY2025-26 Integrated Annual Report outlines strategic priorities.",
    "key_points": ["Strategic focus on infrastructure expansion.", "Commitment to sustainability."],
    "important_risks": ["Regulatory and commodity price risks."],
    "key_takeaway": "Adani Power Limited is prioritizing infrastructure growth.",
}
u = build_update(qwen_real_shape, "qwen3-14b-awq-tp2", "2026-09-04T00:00:00+00:00")

check("summary is populated (derived from executive_summary), not null",
     u.get("summary") == qwen_real_shape["executive_summary"], str(u.get("summary")))
check("bullets is populated (derived from key_points), not null",
     u.get("bullets") == qwen_real_shape["key_points"], str(u.get("bullets")))
check("key_takeaway passes through unchanged",
     u.get("key_takeaway") == qwen_real_shape["key_takeaway"], "")
check("the newer fields (executive_summary/key_points/important_risks) "
     "are ALSO written, not replaced by the derived ones",
     u.get("executive_summary") == qwen_real_shape["executive_summary"]
     and u.get("key_points") == qwen_real_shape["key_points"], "")
check("no key in the update has a None value — THE core regression",
     all(v is not None for v in u.values()), str(u))
check("summary_model and summarized_at are always present",
     u.get("summary_model") == "qwen3-14b-awq-tp2" and u.get("summarized_at"), "")

# THE OLD-SCHEMA CASE — a producer that DOES supply summary/bullets
# directly (e.g. the legacy gpt-4o-mini path, or a future producer)
# must have those values preferred over any derived fallback.
legacy_shape = {
    "summary": "A directly-supplied legacy summary.",
    "bullets": ["legacy bullet one"],
    "key_takeaway": "legacy takeaway",
    "executive_summary": "should NOT be used — summary was supplied directly",
    "key_points": ["should NOT be used — bullets was supplied directly"],
}
u2 = build_update(legacy_shape, "gpt-4o-mini", "2026-09-04T00:00:00+00:00")
check("a directly-supplied summary is preferred over the derived fallback",
     u2["summary"] == "A directly-supplied legacy summary.", str(u2["summary"]))
check("directly-supplied bullets are preferred over the derived fallback",
     u2["bullets"] == ["legacy bullet one"], str(u2["bullets"]))

# THE TRUE-EMPTY CASE — Qwen produced genuinely nothing for a field (both
# sources absent). The key must be DROPPED from the update entirely, never
# written as an explicit null — dropping means "don't touch existing data",
# which is the safe direction to fail in.
empty_shape = {"key_takeaway": "only this field is present"}
u3 = build_update(empty_shape, "qwen3-14b-awq-tp2", "2026-09-04T00:00:00+00:00")
check("a field neither source populated is DROPPED, not set to null",
     "summary" not in u3 and "bullets" not in u3
     and "executive_summary" not in u3 and "key_points" not in u3
     and "important_risks" not in u3, str(u3))
check("the one real field present IS written",
     u3.get("key_takeaway") == "only this field is present", "")
check("summary_model/summarized_at are still always written even when "
     "every content field is empty (so provenance is never lost)",
     u3.get("summary_model") == "qwen3-14b-awq-tp2" and u3.get("summarized_at"), "")

print()
if FAIL:
    print(f"{len(FAIL)} FAILURE(S): {FAIL}")
    sys.exit(1)
print("All checks passed.")
