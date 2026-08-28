#!/usr/bin/env python3
"""Export evaluation fixtures from RedixFi production. READ-ONLY.

RUNS ON THE REDIXFI VM ONLY. MongoDB there is loopback-bound and ChromaDB is
an embedded PersistentClient over a local directory, so this cannot run
anywhere else — and it does not pretend it can.

WRITE SAFETY — the guarantee this script makes
----------------------------------------------
It performs ONLY reads (`find`, `count_documents`, ChromaDB `get`). It never
inserts, updates, deletes, creates an index, or writes any file inside the
RedixFi checkout. Its sole output is JSON written to a path you choose,
which defaults to OUTSIDE the RedixFi tree. `--dry-run` (the default for
`--preflight`) reports what it would export without writing anything.

WHY IT CALLS REDIXFI'S OWN evidence_finder.py
---------------------------------------------
Phase A must evaluate against the EXACT evidence RedixFi's Stage 3 would
have sent. Re-implementing that selection here would create a competing
evidence system — explicitly out of bounds. So this script imports the real
`data-pipeline/evidence_finder.py` (read-only, no side effects: it only
chunks text and applies regexes) and records its output verbatim. Same for
`risk_flag_classifier.matched_categories()` on the Red Flag side.

Note Stage 3 re-chunks Mongo `raw_text` in-process and does NOT read
ChromaDB on its normal path — so Phase A fixtures need no vector store.

USAGE
-----
    export REDIXFI_ROOT=/home/ubuntu/redixfi-backend
    export CHROMA_PATH=$REDIXFI_ROOT/data/chroma_production

    # 1. Look before you leap — reports availability, writes nothing.
    python3 export_fixtures.py --preflight

    # 2. Export each phase.
    python3 export_fixtures.py --task annual_report_summary --limit 20 \
        --out ~/llm_fixtures/annual_report_summary.json
    python3 export_fixtures.py --task red_flag --limit 60 \
        --out ~/llm_fixtures/red_flag.json
    python3 export_fixtures.py --task ask_ai --limit 40 \
        --out ~/llm_fixtures/ask_ai.json

Then copy the JSON files off the VM; they are the entire evaluation input.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config.settings import get_settings  # noqa: E402
from app.evaluation.fixtures import build_document, save, validate_document  # noqa: E402
from app.integrations.redixfi_readonly import (  # noqa: E402
    RedixFiChromaReader,
    RedixFiMongoReader,
)

EVIDENCE_MAX_TOKENS = int(os.getenv("EVIDENCE_MAX_TOKENS", "20000"))


# ---------------------------------------------------------------------------
# RedixFi module loading — read-only import of the real pipeline code
# ---------------------------------------------------------------------------
def load_redixfi_modules(redixfi_root: str):
    """Imports the REAL evidence_finder and risk_flag_classifier.

    Both are pure/deterministic: evidence_finder chunks text and applies
    regexes; matched_categories() is a regex scan. Neither opens a database
    or writes anything at import time. evidence_finder itself imports
    annual_report_embedder for chunk_text_blocks/is_table_noise/is_garbled,
    which is why data-pipeline must be on sys.path.
    """
    pipeline_dir = os.path.join(redixfi_root, "data-pipeline")
    if not os.path.isdir(pipeline_dir):
        raise SystemExit(
            f"REDIXFI_ROOT={redixfi_root!r} has no data-pipeline/ directory. "
            "Set REDIXFI_ROOT to the RedixFi checkout."
        )
    if pipeline_dir not in sys.path:
        sys.path.insert(0, pipeline_dir)
    import evidence_finder  # noqa: E402
    import risk_flag_classifier  # noqa: E402
    return evidence_finder, risk_flag_classifier


def _source_meta(extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    settings = get_settings()
    meta: Dict[str, Any] = {
        "exported_by": "LLM/scripts/export_fixtures.py",
        "read_only": True,
        "mongo_db": settings.mongo_db_name,
        "mongo_app_db": settings.mongo_app_db_name,
        "chroma_path": settings.chroma_path,
        "redixfi_root": settings.redixfi_root,
        "host": os.uname().nodename if hasattr(os, "uname") else "unknown",
    }
    try:
        import subprocess
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=settings.redixfi_root, capture_output=True, text=True, timeout=10,
        )
        meta["redixfi_commit"] = out.stdout.strip() or "unknown"
    except Exception:
        meta["redixfi_commit"] = "unknown"
    if extra:
        meta.update(extra)
    return meta


# ---------------------------------------------------------------------------
# PHASE A — Annual Report Summary
# ---------------------------------------------------------------------------
def export_annual_report(
    mongo: RedixFiMongoReader, limit: int, symbols: Optional[List[str]],
) -> Dict[str, Any]:
    evidence_finder, _ = load_redixfi_modules(get_settings().redixfi_root)

    query: Dict[str, Any] = {
        "extraction_status": "OK",
        "raw_text": {"$exists": True, "$ne": ""},
        # Only documents that ALREADY have a production summary can serve as
        # a reference. As of 2026-08-28 that is ~72 of ~2,000 documents —
        # the OpenAI credit outage, not a code fault.
        "summary": {"$exists": True},
    }
    if symbols:
        query["symbol"] = {"$in": symbols}

    projection = {
        "_id": 0, "symbol": 1, "company_name": 1, "fiscal_year": 1,
        "filing_date": 1, "page_count": 1, "raw_text": 1, "filing_id": 1,
        "summary": 1, "bullets": 1, "executive_summary": 1, "key_points": 1,
        "important_risks": 1, "key_takeaway": 1, "summary_model": 1,
        "summarized_at": 1,
    }

    cases: List[Dict[str, Any]] = []
    for doc in mongo.find("annual_reports", query, projection, limit=limit):
        symbol = doc.get("symbol") or ""
        chunks = evidence_finder.chunks_from_raw_text(
            doc.get("raw_text") or "", symbol=symbol,
            token_target=500, page_count=doc.get("page_count"),
        )
        if not chunks:
            print(f"[SKIP] {symbol}: raw_text produced no chunks")
            continue
        result = evidence_finder.build_narrative_evidence_result(
            chunks, max_tokens=EVIDENCE_MAX_TOKENS,
        )
        if not result.get("text"):
            print(f"[SKIP] {symbol}: Evidence Finder returned no narrative evidence")
            continue

        fiscal_year = doc.get("fiscal_year") or "UNKNOWN"
        cases.append({
            "fixture_id": f"{symbol}:{fiscal_year}",
            "symbol": symbol,
            "company_name": doc.get("company_name"),
            "fiscal_year": fiscal_year,
            "filing_date": doc.get("filing_date"),
            "page_count": doc.get("page_count"),
            "filing_id": doc.get("filing_id"),
            "evidence_text": result["text"],
            "evidence_stats": {
                "evidence_tokens": result.get("total_tokens"),
                "evidence_chunks": result.get("selected_chunks"),
                "total_tagged": result.get("total_tagged"),
                "total_chunks": len(chunks),
                "by_category": result.get("by_category"),
                "fallback": result.get("fallback"),
                "budget_max_tokens": EVIDENCE_MAX_TOKENS,
            },
            "reference": {
                "executive_summary": doc.get("executive_summary") or doc.get("summary"),
                "key_points": doc.get("key_points") or doc.get("bullets") or [],
                "important_risks": doc.get("important_risks") or [],
                "key_takeaway": doc.get("key_takeaway"),
                "summary": doc.get("summary"),
                "bullets": doc.get("bullets") or [],
                "summary_model": doc.get("summary_model"),
                "summarized_at": doc.get("summarized_at"),
            },
        })
        print(f"[OK]   {symbol} {fiscal_year}: "
              f"{result.get('total_tokens')} evidence tokens, "
              f"{result.get('selected_chunks')} chunks")

    return build_document(
        "annual_report_summary", cases,
        _source_meta({"collection": "annual_reports",
                      "evidence_finder": "RedixFi data-pipeline/evidence_finder.py (real)",
                      "evidence_max_tokens": EVIDENCE_MAX_TOKENS}),
        datetime.now(timezone.utc).isoformat(),
    )


# ---------------------------------------------------------------------------
# PHASE B — Red Flag classification
# ---------------------------------------------------------------------------
def export_red_flag(
    chroma: RedixFiChromaReader, limit: int, symbols: Optional[List[str]],
) -> Dict[str, Any]:
    _, risk_flag_classifier = load_redixfi_modules(get_settings().redixfi_root)

    cases: List[Dict[str, Any]] = []
    flagged_seen = 0
    for collection_name in ("annual_reports", "investor_calls"):
        if len(cases) >= limit:
            break
        try:
            available = chroma.count(collection_name)
        except Exception as exc:
            print(f"[WARN] chroma collection '{collection_name}' unavailable: {exc}")
            continue
        print(f"[INFO] scanning chroma '{collection_name}' ({available} vectors)")

        where = {"symbol": {"$in": symbols}} if symbols else None
        for item in chroma.iter_chunks(collection_name, where=where, page_size=500):
            if len(cases) >= limit:
                break
            document = item.get("document") or ""
            metadata = item.get("metadata") or {}

            # Re-derive candidates with RedixFi's OWN keyword prefilter. A
            # chunk with no candidates costs zero LLM calls in production, so
            # including it would evaluate nothing.
            candidates = risk_flag_classifier.matched_categories(document)
            if not candidates:
                continue

            reference: Dict[str, Any] = {}
            if metadata.get("risk_flag_type"):
                reference["risk_flag_type"] = metadata["risk_flag_type"]
                reference["risk_flag_summary"] = metadata.get("risk_flag_summary") or ""
                flagged_seen += 1
            elif metadata.get("risk_classified"):
                # Production ran the classifier and confirmed NOTHING. That is
                # a real reference outcome (a true negative), not missing data.
                reference["risk_flag_type"] = None
                reference["risk_flag_summary"] = ""

            cases.append({
                "fixture_id": item.get("id"),
                "chunk_id": item.get("id"),
                "symbol": metadata.get("symbol"),
                "company_name": metadata.get("company_name"),
                "doc_type": metadata.get("doc_type") or collection_name,
                "fiscal_year": metadata.get("fiscal_year"),
                "page_number": metadata.get("page_number"),
                "source_pdf_url": metadata.get("source_pdf_url"),
                "chunk_text": document,
                "candidates": candidates,
                "production_risk_classified": bool(metadata.get("risk_classified")),
                "reference": reference or None,
            })

    with_reference = sum(1 for c in cases if c.get("reference"))
    print(f"[INFO] {len(cases)} candidate chunks, {with_reference} carry a production "
          f"reference ({flagged_seen} of them a confirmed flag)")
    if with_reference == 0:
        print(
            "[WARN] NO production reference outputs found. This means "
            "risk_flag_backfill.py has not been run against this ChromaDB store "
            "(consistent with MASTER_CONTEXT's 2026-08-23 note). Phase B can "
            "still GENERATE candidate output, but there is nothing to compare "
            "it against — say so explicitly in any report."
        )

    return build_document(
        "red_flag", cases,
        _source_meta({"collections": ["annual_reports", "investor_calls"],
                      "keyword_prefilter": "RedixFi risk_flag_classifier.matched_categories (real)",
                      "cases_with_reference": with_reference,
                      "confirmed_flags_in_reference": flagged_seen}),
        datetime.now(timezone.utc).isoformat(),
    )


# ---------------------------------------------------------------------------
# PHASE C — Ask AI
# ---------------------------------------------------------------------------
def export_ask_ai(mongo: RedixFiMongoReader, limit: int) -> Dict[str, Any]:
    """Ask AI fact packets are NOT persisted anywhere — `ask_log` stores the
    question and metadata, `ask_conversations` stores the answer text. So a
    packet must be REBUILT.

    Rebuilding is done by importing RedixFi's own build_fact_packet (read-
    only against Mongo). One honest caveat is recorded on every case: the
    document_chunks section needs a live OpenAI embedding call, and with the
    account out of credits that call fails soft to an empty list. A packet
    rebuilt in that state is LEANER than the one production actually used,
    which is recorded as `packet_degraded` rather than hidden.
    """
    settings = get_settings()
    api_dir = os.path.join(settings.redixfi_root, "api")
    if api_dir not in sys.path:
        sys.path.insert(0, api_dir)

    try:
        from app.core import ask as redixfi_ask  # type: ignore
        from app.core import evidence_router  # type: ignore
        from app.core.db import get_db  # type: ignore
    except Exception as exc:
        raise SystemExit(
            f"could not import RedixFi's Ask AI modules from {api_dir}: {exc}\n"
            "Run this on the VM with the api/ virtualenv active."
        )

    openai_key = os.getenv("OPENAI_API_KEY", "")
    db = get_db()

    projection = {"_id": 0, "question": 1, "symbol": 1, "mode": 1, "model": 1,
                  "refused": 1, "weight": 1, "sources_used": 1,
                  "source_citations": 1, "conversation_id": 1,
                  "retrieval_plan": 1, "created_at": 1}
    rows = list(mongo.find(
        "ask_log",
        {"symbol": {"$ne": None}, "mode": "symbol"},
        projection, sort=[("_id", -1)], limit=limit * 3, app_db=True,
    ))

    cases: List[Dict[str, Any]] = []
    for row in rows:
        if len(cases) >= limit:
            break
        question = row.get("question")
        symbol = row.get("symbol")
        if not question or not symbol:
            continue

        # Reference answer lives on the conversation's assistant message.
        answer = None
        convo_id = row.get("conversation_id")
        if convo_id:
            convo = mongo.find_one("ask_conversations", {"_id": convo_id}, app_db=True)
            for message in reversed((convo or {}).get("messages") or []):
                if message.get("role") == "assistant" and message.get("content"):
                    answer = message["content"]
                    break
        if not answer:
            continue  # no reference output -> not a comparison case

        doc_log: List[str] = []
        retrieval_meta: Dict[str, Any] = {}
        try:
            plan = evidence_router.classify(question)
            packet = redixfi_ask.build_fact_packet(
                db, symbol, question, api_key=openai_key,
                doc_retrieval_log=doc_log, plan=plan, retrieval_meta=retrieval_meta,
            )
        except Exception as exc:
            print(f"[SKIP] {symbol}: packet rebuild failed: {exc}")
            continue

        degraded = bool(doc_log)
        change_explanation = packet.get("change_explanation")
        causal_backstop = not (
            isinstance(change_explanation, dict)
            and bool(change_explanation.get("cause_available"))
        )

        cases.append({
            "fixture_id": f"{symbol}:{abs(hash(question)) % 10**10}",
            "symbol": symbol,
            "mode": row.get("mode"),
            "question": question,
            "fact_packet": packet,
            "history": None,
            "causal_backstop": causal_backstop,
            "packet_degraded": degraded,
            "packet_degraded_reason": doc_log or None,
            "retrieval_plan": row.get("retrieval_plan"),
            "reference": {
                "answer": answer,
                "refused": row.get("refused"),
                "model": row.get("model"),
                "sources_used": row.get("sources_used") or [],
                "source_citations": row.get("source_citations") or [],
                "weight": row.get("weight"),
            },
        })
        flag = " [DEGRADED PACKET]" if degraded else ""
        print(f"[OK]   {symbol}: {question[:60]}...{flag}")

    degraded_count = sum(1 for c in cases if c.get("packet_degraded"))
    if degraded_count:
        print(f"[WARN] {degraded_count}/{len(cases)} packets were rebuilt WITHOUT "
              "document_chunks (embedding call failed — likely the OpenAI credit "
              "outage). These packets are leaner than production's; the "
              "comparison understates document grounding on both sides.")

    return build_document(
        "ask_ai", cases,
        _source_meta({"collections": ["ask_log", "ask_conversations"],
                      "packet_rebuilt_via": "RedixFi core/ask.py::build_fact_packet (real)",
                      "degraded_packets": degraded_count}),
        datetime.now(timezone.utc).isoformat(),
    )


# ---------------------------------------------------------------------------
# Preflight — availability report, writes nothing
# ---------------------------------------------------------------------------
def preflight(mongo: RedixFiMongoReader, chroma: RedixFiChromaReader) -> None:
    settings = get_settings()
    print("=" * 72)
    print("FIXTURE EXPORT PREFLIGHT — read-only, writes nothing")
    print("=" * 72)
    print(f"REDIXFI_ROOT : {settings.redixfi_root}")
    print(f"MONGO_URI    : {settings.mongo_uri}")
    print(f"CHROMA_PATH  : {settings.chroma_path}\n")

    print("--- PHASE A: annual_report_summary ---")
    try:
        total = mongo.count("annual_reports")
        with_summary = mongo.count("annual_reports", {"summary": {"$exists": True}})
        embedded = mongo.count("annual_reports", {"embedded": True})
        print(f"  annual_reports documents      : {total}")
        print(f"  with a production summary     : {with_summary}   <- Phase A ceiling")
        print(f"  embedded into ChromaDB        : {embedded}")
        if with_summary == 0:
            print("  [BLOCKED] no reference summaries exist — nothing to compare against")
    except Exception as exc:
        print(f"  [ERROR] {exc}")

    print("\n--- PHASE B: red_flag ---")
    try:
        for name in chroma.collection_names():
            print(f"  chroma '{name}': {chroma.count(name)} vectors")
        sample = list(chroma.iter_chunks("annual_reports", page_size=500, max_items=2000))
        classified = sum(1 for c in sample if c["metadata"].get("risk_classified"))
        flagged = sum(1 for c in sample if c["metadata"].get("risk_flag_type"))
        print(f"  sampled {len(sample)} chunks: {classified} risk_classified, {flagged} flagged")
        if classified == 0:
            print("  [WARNING] no risk_classified metadata in the sample — "
                  "risk_flag_backfill.py appears never to have run here. "
                  "Phase B would have NO reference output.")
    except Exception as exc:
        print(f"  [ERROR] {exc}")

    print("\n--- PHASE C: ask_ai ---")
    try:
        logs = mongo.count("ask_log", app_db=True)
        symbol_logs = mongo.count("ask_log", {"mode": "symbol"}, app_db=True)
        convos = mongo.count("ask_conversations", app_db=True)
        print(f"  ask_log documents             : {logs}")
        print(f"  ask_log mode='symbol'         : {symbol_logs}   <- Phase C candidates")
        print(f"  ask_conversations documents   : {convos}   <- hold the reference answers")
        if not os.getenv("OPENAI_API_KEY"):
            print("  [NOTE] OPENAI_API_KEY unset — rebuilt packets will omit "
                  "document_chunks and be flagged packet_degraded")
    except Exception as exc:
        print(f"  [ERROR] {exc}")

    print("\nNothing was written. Re-run with --task <name> --out <path> to export.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export RedixFi evaluation fixtures (READ-ONLY)",
    )
    parser.add_argument("--task", choices=["annual_report_summary", "red_flag", "ask_ai"])
    parser.add_argument("--out", help="output JSON path (outside the RedixFi tree)")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--symbols", help="comma-separated symbol filter")
    parser.add_argument("--preflight", action="store_true",
                        help="report availability and exit; writes nothing")
    parser.add_argument("--dry-run", action="store_true",
                        help="build the fixture but print a summary instead of writing it")
    args = parser.parse_args()

    settings = get_settings()
    mongo = RedixFiMongoReader(settings)
    chroma = RedixFiChromaReader(settings)

    if args.preflight or not args.task:
        preflight(mongo, chroma)
        return

    symbols = [s.strip().upper() for s in args.symbols.split(",")] if args.symbols else None

    if args.task == "annual_report_summary":
        doc = export_annual_report(mongo, args.limit, symbols)
    elif args.task == "red_flag":
        doc = export_red_flag(chroma, args.limit, symbols)
    else:
        doc = export_ask_ai(mongo, args.limit)

    problems = validate_document(doc)
    print(f"\n[SUMMARY] task={doc['task']} cases={len(doc['cases'])} "
          f"with_reference={sum(1 for c in doc['cases'] if c.get('reference'))}")
    if problems:
        print("[INVALID] " + "\n           ".join(problems))

    if args.dry_run or not args.out:
        print("\nDry run — nothing written. Pass --out <path> to write.")
        print(json.dumps(doc["source"], indent=2, default=str))
        return

    save(doc, args.out)
    print(f"\n[WROTE] {args.out}")
    print("This is the ONLY file this script created. No production store was modified.")


if __name__ == "__main__":
    main()
