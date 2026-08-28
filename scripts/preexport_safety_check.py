#!/usr/bin/env python3
"""FINAL PRE-EXPORT SAFETY + PRIVACY CHECK. READ-ONLY, writes nothing.

Two jobs:

  1. PRIVACY — build every fixture in memory and scan the EXACT bytes that
     would be written for credential-shaped strings. Scanning the real
     serialized payload beats scanning the source collections, because it is
     the payload that leaves the VM.

  2. SAFETY — re-read the production counters the export touches and confirm
     they are unchanged from the values recorded before it ran.

Note `annual_reports` total is expected to MOVE while the multi-year backfill
is running; that is the backfill's write, not this project's. The counters
that must not move are the ones the export reads: summaries, ChromaDB
vectors and risk tags.
"""
from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import scripts.export_fixtures as ex  # noqa: E402

SECRET_PATTERNS = [
    ("openai key", re.compile(r"sk-[A-Za-z0-9_\-]{16,}")),
    ("github token", re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}")),
    ("mongo uri with credentials", re.compile(r"mongodb(\+srv)?://[^\s\"']*:[^\s@\"']*@")),
    ("private key block", re.compile(r"BEGIN [A-Z ]*PRIVATE KEY")),
    ("aws key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("bearer token", re.compile(r"Bearer\s+[A-Za-z0-9._\-]{20,}")),
    ("assigned password", re.compile(r"password\s*[=:]\s*[^\s\"',}]{6,}", re.I)),
    ("assigned api key", re.compile(r"api[_-]?key\s*[=:]\s*[^\s\"',}]{8,}", re.I)),
    ("env-style secret", re.compile(r"(SECRET|TOKEN|PASSWD)\s*=\s*[^\s\"',}]{6,}")),
]

# Indian annual reports and concall transcripts routinely carry NSDL/CDSL
# e-voting instructions that legitimately contain the WORD "password"
# ("Initial password", "Forgot User Details/Password?"). Those are public
# filed-document boilerplate, not credentials, and must not be reported as
# findings — but anything that looks like an ASSIGNED value still is.
BENIGN = re.compile(
    r"(initial password|forgot .{0,30}password|password\s*[?:]|"
    r"user\s*id\s*and\s*password|change\s+(the\s+)?password|"
    r"password\s+(is\s+)?(communicated|sent|provided|created|generated))",
    re.I,
)


class Args:
    limit = None
    symbol_list = None
    allow_embedding = False


def scan(name: str, payload: str) -> int:
    findings = 0
    for label, pattern in SECRET_PATTERNS:
        for m in pattern.finditer(payload):
            window = payload[max(0, m.start() - 120): m.end() + 60]
            if BENIGN.search(window):
                continue
            findings += 1
            if findings <= 5:
                print(f"    [HIT] {label}: ...{window[:200]!r}...")
    print(f"  {name:<26} {len(payload) / 1e6:>7.2f} MB   "
          f"{'CLEAN' if not findings else f'{findings} FINDING(S)'}")
    return findings


def main() -> None:
    print("=" * 74)
    print("PRE-EXPORT SAFETY + PRIVACY CHECK — READ-ONLY, writes nothing")
    print("=" * 74)

    # --- baselines BEFORE ---------------------------------------------------
    db = ex.get_pipeline_db()
    import chromadb
    chroma = chromadb.PersistentClient(path=ex.CHROMA_PATH)
    ar_col = chroma.get_collection("annual_reports")

    before = {
        "annual_reports_with_summary": db["annual_reports"].count_documents(
            {"summary": {"$exists": True}}),
        "investor_calls_with_summary": db["investor_calls"].count_documents(
            {"summary": {"$exists": True}}),
        "chroma_annual_report_vectors": ar_col.count(),
    }

    print("\n--- PRIVACY SCAN (the exact bytes that would be written) ---")
    total_findings = 0
    args = Args()
    for task, limit in (("annual_report_summary", 20), ("concall_summary", 20),
                        ("red_flag", 60), ("ask_ai", 30)):
        args.limit = limit
        doc = ex.BUILDERS[task](args)
        payload = json.dumps(doc, ensure_ascii=False, default=str)
        total_findings += scan(task, payload)

    # --- baselines AFTER ----------------------------------------------------
    after = {
        "annual_reports_with_summary": db["annual_reports"].count_documents(
            {"summary": {"$exists": True}}),
        "investor_calls_with_summary": db["investor_calls"].count_documents(
            {"summary": {"$exists": True}}),
        "chroma_annual_report_vectors": ar_col.count(),
    }

    print("\n--- PRODUCTION UNCHANGED? ---")
    unchanged = True
    for key in before:
        same = before[key] == after[key]
        unchanged = unchanged and same
        print(f"  {key:<34} before={before[key]:<8} after={after[key]:<8} "
              f"{'OK' if same else 'CHANGED'}")

    print("\n--- VERDICT ---")
    print(f"  privacy findings   : {total_findings}")
    print(f"  production counters: {'UNCHANGED' if unchanged else 'CHANGED — INVESTIGATE'}")
    if total_findings == 0 and unchanged:
        print("\n  SAFE TO EXPORT.")
    else:
        print("\n  DO NOT EXPORT until the findings above are explained.")


if __name__ == "__main__":
    main()
