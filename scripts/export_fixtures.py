#!/usr/bin/env python3
"""Export evaluation fixtures from RedixFi production. READ-ONLY.

RUNS ON THE REDIXFI VM ONLY. MongoDB there is loopback-bound and ChromaDB is
an embedded PersistentClient over a local directory, so this cannot run
anywhere else — and it does not pretend it can.

WRITE SAFETY — the guarantee this script makes
----------------------------------------------
It performs ONLY reads (`find`, `count_documents`, ChromaDB `get`). It never
inserts, updates, deletes, creates an index, or writes any file inside the
RedixFi checkout. Its only output is JSON written to `--out`, which must sit
outside the RedixFi tree. `--validate` builds every case in memory and
reports on it while writing nothing at all.

NO OPENAI CALLS. The Ask AI packet rebuild passes an EMPTY api_key, so
`retrieve_document_chunks` short-circuits to [] before any network request.
`--allow-embedding` exists to re-enable it if credits ever return, and is
off by default.

THE FOUR BENCHMARKS
-------------------
  concall_summary        PRIMARY. 4,157 gpt-4o-mini references, and the code
                         path that produced them is unchanged, so the input
                         is exactly reproducible.
  annual_report_summary  SECONDARY, DUAL-INPUT. All 72 references were
                         written 2026-08-16, BEFORE the Evidence Finder
                         unification (2026-08-24). Each case therefore
                         carries BOTH the legacy front-slice input (which
                         produced the reference) and the current Evidence
                         Finder evidence, so the legacy replay is
                         like-for-like and the current pipeline can be
                         measured separately without conflating the two.
  red_flag               STRATIFIED over the real production risk tags:
                         4 positive categories plus confirmed negatives.
  ask_ai                 Only cases joinable to a real LLM answer. Every one
                         is stamped PACKET_RECONSTRUCTION_PARTIAL.

WHY IT CALLS REDIXFI'S OWN CODE
-------------------------------
Evidence selection is never reimplemented here. This script imports the real
`data-pipeline/evidence_finder.py` and `risk_flag_classifier.matched_
categories()` and records their output verbatim.

USAGE
    export REDIXFI_ROOT=/home/ubuntu/redixfi-backend
    export CHROMA_PATH=$REDIXFI_ROOT/data/chroma_production

    python3 export_fixtures.py --validate                    # writes nothing
    python3 export_fixtures.py --task concall_summary --limit 20 \
        --out /home/ubuntu/llm_fixtures/concall_benchmark.json
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.evaluation.fixtures import build_document, save, validate_document  # noqa: E402

REDIXFI_ROOT = os.getenv("REDIXFI_ROOT", "/home/ubuntu/redixfi-backend")
CHROMA_PATH = os.getenv("CHROMA_PATH", os.path.join(REDIXFI_ROOT, "data/chroma_production"))
EVIDENCE_MAX_TOKENS = int(os.getenv("EVIDENCE_MAX_TOKENS", "20000"))

# Legacy Stage 3 contract — see app/prompts/annual_report_summary_legacy.py
LEGACY_MAX_REPORT_CHARS = 150_000
LEGACY_MAX_REPORT_TOKENS = 100_000
CONCALL_MAX_TRANSCRIPT_CHARS = 120_000

RISK_CATEGORIES = ("auditor_qualification", "contingent_liability",
                   "related_party_transaction", "promoter_pledge")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def stable_id(*parts: Any) -> str:
    """Deterministic fallback when a natural identifier is missing. A hash of
    the real content beats inventing a sequence number — it is reproducible
    across runs and cannot silently collide with a real id."""
    blob = "|".join(str(p) for p in parts)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()[:12]


def sanitize(value: Any) -> str:
    return str(value or "UNKNOWN").replace(" ", "-").replace("/", "-")


def count_tokens(text: str) -> int:
    try:
        import tiktoken
        return len(tiktoken.encoding_for_model("gpt-4o-mini").encode(text))
    except Exception:
        return max(1, int(len(text) / 2.5))


def spread_sample(items: List[Any], n: int) -> List[Any]:
    """Evenly-strided sample rather than first-N.

    First-N over a ChromaDB scan or a Mongo cursor concentrates on whichever
    symbols happen to sort first, which would make a 'stratified' sample
    stratified by category but not by company. Striding spreads the draw
    across the whole population and is deterministic, so a re-run reproduces
    the same fixture."""
    if n >= len(items):
        return list(items)
    if n <= 0:
        return []
    step = len(items) / n
    return [items[int(i * step)] for i in range(n)]


_redixfi_modules: Dict[str, Any] = {}


def load_redixfi_modules():
    """Imports the REAL evidence_finder and risk_flag_classifier.

    Both are deterministic and side-effect-free: evidence_finder chunks text
    and applies regexes, matched_categories() is a regex scan. Neither writes
    anything. evidence_finder imports annual_report_embedder for
    chunk_text_blocks/is_table_noise/is_garbled, which is why data-pipeline
    must be on sys.path — and why MONGO_URI must be set (that module reads
    config.db at import time).
    """
    if _redixfi_modules:
        return _redixfi_modules
    pipeline_dir = os.path.join(REDIXFI_ROOT, "data-pipeline")
    if not os.path.isdir(pipeline_dir):
        raise SystemExit(f"REDIXFI_ROOT={REDIXFI_ROOT!r} has no data-pipeline/")
    for path in (REDIXFI_ROOT, pipeline_dir):
        if path not in sys.path:
            sys.path.insert(0, path)
    import evidence_finder
    import risk_flag_classifier
    _redixfi_modules["evidence_finder"] = evidence_finder
    _redixfi_modules["risk_flag_classifier"] = risk_flag_classifier
    return _redixfi_modules


def get_pipeline_db():
    for path in (REDIXFI_ROOT,):
        if path not in sys.path:
            sys.path.insert(0, path)
    from config.db import get_db
    return get_db()


_redixfi_api: Dict[str, Any] = {}


def load_redixfi_api():
    """Load RedixFi's `app.core.*` despite a PACKAGE-NAME COLLISION.

    This project's own package is also called `app`, and RedixFi's API code
    uses relative imports (`from .document_retrieval import ...`), so it must
    be imported as the top-level package `app` — it cannot be aliased.
    Whichever `app` is in sys.modules wins, and ours is (this script imports
    app.evaluation.fixtures at module scope), which is why a naive import
    raises `ModuleNotFoundError: No module named 'app.core'`.

    Resolution: everything needed from OUR `app` is already imported and
    bound by the time this runs, so ours is evicted from sys.modules and
    sys.path, RedixFi's is imported wholesale, and then ours is restored.
    RedixFi's modules are cached here so the swap happens exactly once and
    sys.modules is never left half-and-half.

    `redixfi_app` also uses a DIFFERENT credential from the pipeline DB;
    get_app_db() reads MONGO_URI_APP from api/.env. The URI is never read,
    printed or stored by this script.
    """
    if _redixfi_api:
        return _redixfi_api
    with redixfi_app_context() as api_dir:
        from app.core import ask as redixfi_ask
        from app.core import evidence_router
        from app.core import red_flag_ask
        from app.core.db import get_app_db
        _redixfi_api.update({
            "ask": redixfi_ask,
            "evidence_router": evidence_router,
            "red_flag_ask": red_flag_ask,
            "app_db": get_app_db(),
            "api_dir": api_dir,
        })
    return _redixfi_api


@contextlib.contextmanager
def redixfi_app_context():
    """Make `app` resolve to RedixFi's api/app for the duration of the block.

    The swap must stay active for the whole CALL, not just the import:
    `build_fact_packet` and its dependencies do lazy `app.core.*` imports
    from inside function bodies, so restoring our package too early raises
    `No module named 'app.core'` at call time rather than at import time.

    Also chdir's into api/, because api/app/core/config.py resolves api/.env
    relative to the working directory.
    """
    api_dir = os.path.join(REDIXFI_ROOT, "api")
    llm_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    saved_modules = {name: mod for name, mod in sys.modules.items()
                     if name == "app" or name.startswith("app.")}
    saved_path = list(sys.path)
    saved_cwd = os.getcwd()

    for name in saved_modules:
        del sys.modules[name]
    sys.path = [p for p in sys.path
                if os.path.abspath(p) != os.path.abspath(llm_root)]
    sys.path.insert(0, api_dir)
    os.chdir(api_dir)
    try:
        yield api_dir
    finally:
        os.chdir(saved_cwd)
        # Drop RedixFi's app.* and restore ours, so sys.modules is never left
        # with our `app` and their `app.core` side by side.
        for name in [n for n in sys.modules
                     if n == "app" or n.startswith("app.")]:
            del sys.modules[name]
        sys.path = saved_path
        sys.modules.update(saved_modules)


def redixfi_commit() -> str:
    try:
        import subprocess
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REDIXFI_ROOT,
                              capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:
        return "unknown"


def source_meta(extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    meta: Dict[str, Any] = {
        "exported_by": "LLM/scripts/export_fixtures.py",
        "read_only": True,
        "openai_calls_made": 0,
        "redixfi_root": REDIXFI_ROOT,
        "redixfi_commit": redixfi_commit(),
        "chroma_path": CHROMA_PATH,
        "host": os.uname().nodename if hasattr(os, "uname") else "unknown",
    }
    if extra:
        meta.update(extra)
    return meta


# ---------------------------------------------------------------------------
# A. ANNUAL REPORT — dual-input, legacy reference preserved
# ---------------------------------------------------------------------------
def build_annual_report(limit: int, symbols: Optional[List[str]]) -> Dict[str, Any]:
    ef = load_redixfi_modules()["evidence_finder"]
    db = get_pipeline_db()

    query: Dict[str, Any] = {
        "extraction_status": "OK",
        "raw_text": {"$exists": True, "$ne": ""},
        "summary": {"$exists": True, "$ne": ""},
    }
    if symbols:
        query["symbol"] = {"$in": symbols}

    projection = {
        "_id": 0, "symbol": 1, "company_name": 1, "fiscal_year": 1, "filing_date": 1,
        "page_count": 1, "raw_text": 1, "filing_id": 1, "source_pdf_url": 1,
        "summary": 1, "bullets": 1, "key_takeaway": 1, "summary_model": 1,
        "summarized_at": 1,
    }

    # Draw from the WHOLE legacy-reference population, then stride, so the 20
    # are spread across the 72 rather than being whichever 20 sort first.
    # Sorted explicitly. Without a sort MongoDB returns natural order, which
    # is NOT stable between runs — two validation passes selected different
    # 20-document samples (4.80 MB vs 4.54 MB) before this was fixed. A
    # fixture must be reproducible, so the draw is deterministic: sort by
    # filing_id, then stride.
    population = list(db["annual_reports"].find(query, projection).sort("filing_id", 1))
    print(f"  legacy-reference population: {len(population)} documents")
    chosen = spread_sample(population, limit)

    cases: List[Dict[str, Any]] = []
    skipped: List[Dict[str, str]] = []

    for doc in chosen:
        symbol = doc.get("symbol") or ""
        filing_id = doc.get("filing_id") or stable_id(symbol, doc.get("source_pdf_url"))
        raw_text = doc.get("raw_text") or ""

        # --- current pipeline input: Evidence Finder -----------------------
        chunks = ef.chunks_from_raw_text(raw_text, symbol=symbol, token_target=500,
                                         page_count=doc.get("page_count"))
        evidence = ef.build_narrative_evidence_result(
            chunks, max_tokens=EVIDENCE_MAX_TOKENS) if chunks else {"text": ""}
        if not evidence.get("text"):
            skipped.append({"symbol": symbol, "reason": "Evidence Finder produced no evidence"})
            continue

        # --- legacy input: the exact front slice that produced the reference
        legacy_text = raw_text[:LEGACY_MAX_REPORT_CHARS]
        legacy_tokens = count_tokens(legacy_text)
        # BUG 10 (f25d480) added a token-aware fallback mid-day on 2026-08-16.
        # It only diverges above MAX_REPORT_TOKENS; below it, every 08-16
        # commit produces a byte-identical slice.
        legacy_ambiguous = legacy_tokens > LEGACY_MAX_REPORT_TOKENS

        cases.append({
            "benchmark_id": f"AR_{sanitize(symbol)}_{sanitize(filing_id)}",
            "symbol": symbol,
            "company_name": doc.get("company_name"),
            "fiscal_year": doc.get("fiscal_year") or "UNKNOWN",
            "filing_id": filing_id,
            "filing_date": doc.get("filing_date"),
            "page_count": doc.get("page_count"),
            "source_pdf_url": doc.get("source_pdf_url"),
            "doc_type": "annual_report",

            # INPUT 1 — current pipeline
            "evidence_text": evidence["text"],
            "evidence_stats": {
                "evidence_tokens": evidence.get("total_tokens"),
                "evidence_chunks": evidence.get("selected_chunks"),
                "total_tagged": evidence.get("total_tagged"),
                "total_chunks": len(chunks),
                "by_category": evidence.get("by_category"),
                "fallback": evidence.get("fallback"),
                "budget_max_tokens": EVIDENCE_MAX_TOKENS,
            },

            # INPUT 2 — legacy pipeline (what produced the reference)
            "legacy_input_text": legacy_text,
            "legacy_input_stats": {
                "chars": len(legacy_text),
                "tokens": legacy_tokens,
                "raw_text_chars_total": len(raw_text),
                "truncated": len(raw_text) > LEGACY_MAX_REPORT_CHARS,
                "max_report_chars": LEGACY_MAX_REPORT_CHARS,
                "exceeds_legacy_token_ceiling": legacy_ambiguous,
                "input_path_ambiguous": legacy_ambiguous,
                "input_path_note": (
                    "raw_text[:150000] exceeds MAX_REPORT_TOKENS=100000, so the "
                    "post-BUG-10 code would have taken a RAG/truncation fallback "
                    "instead. Which commit was deployed during the 2026-08-16 run "
                    "is not knowable from the data, so this case's legacy input is "
                    "NOT certain to be what the reference actually saw."
                ) if legacy_ambiguous else (
                    "under MAX_REPORT_TOKENS, so every 2026-08-16 commit produces "
                    "this byte-identical slice — the legacy input is certain."
                ),
            },

            # REFERENCE — legacy, preserved verbatim
            "reference": {
                "summary": doc.get("summary"),
                "bullets": doc.get("bullets") or [],
                "key_takeaway": doc.get("key_takeaway"),
                "summary_model": doc.get("summary_model"),
                "summarized_at": doc.get("summarized_at"),
            },

            "provenance": {
                "reference_set": "LEGACY_REFERENCE",
                "pipeline_version": "legacy_front_slice_pre_evidence_finder",
                "input_type": "dual: legacy_front_slice + evidence_finder",
                "reference_model": doc.get("summary_model") or "gpt-4o-mini",
                "reference_generated_at": doc.get("summarized_at"),
                "reference_prompt_version": "annual_report_summarizer@2026-08-16",
                "reference_prompt_source_commit": "b9e40c4~1",
                "reference_output_schema": ["summary", "bullets", "key_takeaway"],
                "current_pipeline_version": "evidence_finder@b9e40c4",
                "current_prompt_version": "annual_report_summarizer@8bb3170",
                "current_output_schema": ["executive_summary", "key_points",
                                          "important_risks", "key_takeaway"],
                "redixfi_commit_at_export": redixfi_commit(),
                "limitations": [
                    "The stored reference PREDATES the Evidence Finder layer "
                    "(reference 2026-08-16, Evidence Finder 2026-08-24).",
                    "Replaying as 'annual_report_summary_legacy' is like-for-like. "
                    "Replaying as 'annual_report_summary' changes BOTH the input "
                    "and the output schema, and is NOT a like-for-like comparison.",
                ] + ([
                    "Legacy input path is AMBIGUOUS for this document — see "
                    "legacy_input_stats.input_path_note."
                ] if legacy_ambiguous else []),
            },
        })

    return build_document(
        "annual_report_summary", cases,
        source_meta({
            "collection": "annual_reports",
            "reference_set": "LEGACY_REFERENCE (72 summaries written 2026-08-16)",
            "population_size": len(population),
            "evidence_finder": "RedixFi data-pipeline/evidence_finder.py (real)",
            "evidence_max_tokens": EVIDENCE_MAX_TOKENS,
            "skipped": skipped,
        }),
        datetime.now(timezone.utc).isoformat(),
    )


# ---------------------------------------------------------------------------
# B. CONCALL — primary summarization benchmark
# ---------------------------------------------------------------------------
def build_concall(limit: int, symbols: Optional[List[str]]) -> Dict[str, Any]:
    db = get_pipeline_db()
    query: Dict[str, Any] = {
        "extraction_status": "OK",
        "raw_transcript_text": {"$exists": True, "$ne": ""},
        "summary": {"$exists": True, "$ne": ""},
    }
    if symbols:
        query["symbol"] = {"$in": symbols}

    projection = {
        "_id": 0, "symbol": 1, "company_name": 1, "filing_date": 1, "subject": 1,
        "filing_id": 1, "source_pdf_url": 1, "raw_transcript_text": 1,
        "summary": 1, "tone_label": 1, "tone_note": 1, "summary_model": 1,
        "summarized_at": 1,
    }

    # Identity only first, so 4,157 full transcripts are never pulled into
    # memory just to pick 20.
    ids = [d["filing_id"] for d in db["investor_calls"].find(
        query, {"_id": 0, "filing_id": 1}) if d.get("filing_id")]
    print(f"  reference population: {len(ids)} documents")
    chosen_ids = spread_sample(sorted(ids), limit)

    cases: List[Dict[str, Any]] = []
    skipped: List[Dict[str, str]] = []
    for filing_id in chosen_ids:
        doc = db["investor_calls"].find_one({"filing_id": filing_id}, projection)
        if not doc:
            skipped.append({"filing_id": filing_id, "reason": "not found on re-read"})
            continue
        transcript = doc.get("raw_transcript_text") or ""
        input_text = transcript[:CONCALL_MAX_TRANSCRIPT_CHARS]
        symbol = doc.get("symbol") or ""
        # Exactly the label production derives in _user_content().
        doc_kind = ("earnings concall transcript"
                    if doc.get("subject") == "EARNINGS_CALL_TRANSCRIPT"
                    else "investor presentation")

        cases.append({
            "benchmark_id": f"CC_{sanitize(symbol)}_{sanitize(filing_id)}",
            "symbol": symbol,
            "company_name": doc.get("company_name"),
            "filing_id": filing_id,
            "filing_date": doc.get("filing_date"),
            "subject": doc.get("subject"),
            "doc_kind": doc_kind,
            "doc_type": "concall_transcript",
            "source_pdf_url": doc.get("source_pdf_url"),

            "input_text": input_text,
            "input_stats": {
                "chars": len(input_text),
                "tokens": count_tokens(input_text),
                "transcript_chars_total": len(transcript),
                "truncated": len(transcript) > CONCALL_MAX_TRANSCRIPT_CHARS,
                "max_transcript_chars": CONCALL_MAX_TRANSCRIPT_CHARS,
            },

            "reference": {
                "summary": doc.get("summary"),
                "tone_label": doc.get("tone_label"),
                "tone_note": doc.get("tone_note"),
                "summary_model": doc.get("summary_model"),
                "summarized_at": doc.get("summarized_at"),
            },

            "provenance": {
                "reference_set": "CURRENT_PIPELINE",
                "pipeline_version": "concall_front_slice",
                "input_type": "raw_transcript_text[:120000] front slice",
                "reference_model": doc.get("summary_model") or "gpt-4o-mini",
                "reference_generated_at": doc.get("summarized_at"),
                "reference_prompt_version": "concall_summarizer@8bb3170",
                "reference_output_schema": ["summary", "tone_label", "tone_note"],
                "redixfi_commit_at_export": redixfi_commit(),
                "limitations": [
                    "None material: concall_summarizer.py has NOT been rewired "
                    "through Evidence Finder, so the code path that produced this "
                    "reference is the code path that exists today. The input is "
                    "exactly reproducible and this is a like-for-like comparison.",
                ],
            },
        })

    return build_document(
        "concall_summary", cases,
        source_meta({
            "collection": "investor_calls",
            "population_size": len(ids),
            "skipped": skipped,
        }),
        datetime.now(timezone.utc).isoformat(),
    )


# ---------------------------------------------------------------------------
# C. RED FLAG — stratified over real production tags
# ---------------------------------------------------------------------------
def build_red_flag(limit: int, symbols: Optional[List[str]],
                   negatives_share: float = 0.34) -> Dict[str, Any]:
    rfc = load_redixfi_modules()["risk_flag_classifier"]
    import chromadb
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    # investor_calls is excluded deliberately: only 2 of its 2,622 vectors
    # carry a risk_flag_type, and its metadata has no fiscal_year.
    collection = client.get_collection("annual_reports")

    def ids_where(where) -> List[str]:
        out, offset = [], 0
        while True:
            page = collection.get(where=where, include=[], limit=1000, offset=offset)
            got = page.get("ids") or []
            out.extend(got)
            if len(got) < 1000:
                return out
            offset += len(got)

    print("  scanning production risk tags (read-only)...")
    positives_by_cat = {cat: ids_where({"risk_flag_type": cat}) for cat in RISK_CATEGORIES}
    for cat, ids in positives_by_cat.items():
        print(f"    {cat:<30} {len(ids)} available")

    n_negatives = int(round(limit * negatives_share))
    n_positives = limit - n_negatives
    per_cat = max(1, n_positives // len(RISK_CATEGORIES))

    # Balanced draw, then redistribute whatever a scarce category cannot fill
    # (promoter_pledge has only 26 in production) so the total still lands on
    # `limit` rather than silently coming up short.
    picked: Dict[str, List[str]] = {}
    shortfall = 0
    for cat in RISK_CATEGORIES:
        want = per_cat
        have = positives_by_cat[cat]
        take = min(want, len(have))
        shortfall += want - take
        picked[cat] = spread_sample(sorted(have), take)
    if shortfall:
        for cat in sorted(RISK_CATEGORIES, key=lambda c: -len(positives_by_cat[c])):
            if shortfall <= 0:
                break
            spare = [i for i in sorted(positives_by_cat[cat]) if i not in set(picked[cat])]
            extra = spread_sample(spare, min(shortfall, len(spare)))
            picked[cat].extend(extra)
            shortfall -= len(extra)

    positive_ids = [(i, cat) for cat, ids in picked.items() for i in ids]

    # Negatives: risk_classified=True but NO risk_flag_type. Chroma has no
    # "$exists: false", so subtract the flagged set from the classified set.
    print("  selecting confirmed negatives...")
    all_flagged = set()
    for ids in positives_by_cat.values():
        all_flagged.update(ids)
    classified = ids_where({"risk_classified": True})
    negative_pool = sorted(set(classified) - all_flagged)
    print(f"    negatives available: {len(negative_pool)}")

    cases: List[Dict[str, Any]] = []
    dropped_no_candidates = 0

    def add_case(chunk_id: str, category: Optional[str], polarity: str) -> bool:
        nonlocal dropped_no_candidates
        got = collection.get(ids=[chunk_id], include=["documents", "metadatas"])
        docs = got.get("documents") or []
        metas = got.get("metadatas") or []
        if not docs:
            return False
        text, meta = docs[0] or "", metas[0] or {}
        if symbols and meta.get("symbol") not in symbols:
            return False

        # Re-derive candidates with RedixFi's OWN prefilter. A chunk with no
        # candidates costs zero LLM calls in production, so it would evaluate
        # nothing and must not enter the fixture.
        candidates = rfc.matched_categories(text)
        if not candidates:
            dropped_no_candidates += 1
            return False

        symbol = meta.get("symbol") or "UNKNOWN"
        cases.append({
            "benchmark_id": f"RF_{sanitize(symbol)}_{sanitize(chunk_id)}",
            "chunk_id": chunk_id,
            "symbol": symbol,
            "company_name": meta.get("company_name"),
            "doc_type": meta.get("doc_type") or "annual_report",
            "fiscal_year": meta.get("fiscal_year"),
            "page_number": meta.get("page_number"),
            "chunk_index": meta.get("chunk_index"),
            "source_pdf_url": meta.get("source_pdf_url"),

            "chunk_text": text,
            "candidates": candidates,
            "case_polarity": polarity,

            "reference": {
                "risk_flag_type": meta.get("risk_flag_type"),   # None == true negative
                "risk_flag_summary": meta.get("risk_flag_summary") or "",
            },

            "provenance": {
                "reference_set": "CURRENT_PIPELINE",
                "pipeline_version": "risk_flag_classifier@b9e40c4",
                "input_type": "chromadb chunk text (annual_reports)",
                "reference_model": "gpt-4o-mini",
                "reference_prompt_version": "risk_flag_classifier@b9e40c4",
                "reference_output_schema": ["risk_classified", "risk_flag_type",
                                            "risk_flag_summary"],
                "keyword_prefilter": "RedixFi risk_flag_classifier.matched_categories (real)",
                "production_risk_classified": bool(meta.get("risk_classified")),
                "redixfi_commit_at_export": redixfi_commit(),
                "limitations": [
                    "A negative case means production's classifier RAN and confirmed "
                    "nothing — a true negative, not missing data.",
                    "investor_calls chunks are excluded: only 2 of 2,622 carry a "
                    "risk_flag_type and their metadata has no fiscal_year.",
                ],
            },
        })
        return True

    for chunk_id, cat in positive_ids:
        add_case(chunk_id, cat, "positive")

    # NEGATIVES — the subtle half of this benchmark.
    #
    # Most of the 53,305 unflagged-but-classified chunks never matched a
    # keyword at all. Those are worthless as evaluation cases: production
    # spends ZERO LLM calls on them, so a candidate model is never asked
    # anything about them either.
    #
    # The negatives worth having are chunks that DID trip the keyword
    # prefilter and were then REJECTED by the LLM confirmation step — the
    # false-positive-resistance cases. They must be found by scanning, since
    # ChromaDB metadata does not record "matched a keyword but was rejected".
    # Fetch in batches rather than one id at a time.
    print("  searching negatives for keyword-matched (LLM-rejected) cases...")
    negatives_added = 0
    scanned = 0
    batch_size = 200
    search_pool = spread_sample(negative_pool, min(len(negative_pool), 6000))
    for start in range(0, len(search_pool), batch_size):
        if negatives_added >= n_negatives:
            break
        batch = search_pool[start:start + batch_size]
        got = collection.get(ids=batch, include=["documents", "metadatas"])
        for chunk_id, text, meta in zip(got.get("ids") or [],
                                        got.get("documents") or [],
                                        got.get("metadatas") or []):
            scanned += 1
            if negatives_added >= n_negatives:
                break
            if not rfc.matched_categories(text or ""):
                continue  # no keyword hit -> production never asked the LLM
            if symbols and (meta or {}).get("symbol") not in symbols:
                continue
            if add_case(chunk_id, None, "negative"):
                negatives_added += 1
    print(f"    scanned {scanned} negatives, kept {negatives_added} "
          f"keyword-matched (LLM-rejected) cases")

    strata: Dict[str, int] = {}
    for c in cases:
        key = (c["reference"]["risk_flag_type"] or "negative_unflagged")
        strata[key] = strata.get(key, 0) + 1

    return build_document(
        "red_flag", cases,
        source_meta({
            "collection": "chromadb annual_reports",
            "available_positives": {c: len(v) for c, v in positives_by_cat.items()},
            "available_negatives": len(negative_pool),
            "strata": strata,
            "dropped_no_keyword_candidates": dropped_no_candidates,
            "sampling": "evenly-strided over sorted ids (deterministic), not first-N",
        }),
        datetime.now(timezone.utc).isoformat(),
    )


# ---------------------------------------------------------------------------
# D. ASK AI — partial reconstruction, always stamped
# ---------------------------------------------------------------------------
def build_ask_ai(limit: int, allow_embedding: bool = False) -> Dict[str, Any]:
    api = load_redixfi_api()
    redixfi_ask = api["ask"]
    evidence_router = api["evidence_router"]
    red_flag_ask = api["red_flag_ask"]
    db = get_pipeline_db()
    adb = api["app_db"]
    AL, AC = adb["ask_log"], adb["ask_conversations"]

    # An empty api_key makes retrieve_document_chunks short-circuit to []
    # BEFORE any network request — this is what keeps the export at zero
    # OpenAI calls. --allow-embedding exists for a future run with credits.
    api_key = os.getenv("OPENAI_API_KEY", "") if allow_embedding else ""

    rows = list(AL.find(
        {"model": "gpt-4o-mini", "mode": "symbol", "refused": False,
         "question": {"$exists": True, "$ne": ""}, "conversation_id": {"$ne": None}},
        {"_id": 1, "conversation_id": 1, "question": 1, "symbol": 1, "mode": 1,
         "model": 1, "refused": 1, "sources_used": 1, "source_citations": 1,
         "weight": 1, "retrieval_plan": 1, "charged_to": 1},
    ).sort("_id", -1))
    print(f"  joinable population (gpt-4o-mini + symbol + answered): {len(rows)}")

    cases: List[Dict[str, Any]] = []
    skipped: List[Dict[str, str]] = []

    # The swap must stay active for EVERY build_fact_packet call, not just
    # the import — see redixfi_app_context's docstring.
    with redixfi_app_context():
      for row in rows:
          if len(cases) >= limit:
              break
          answer = None
          convo = AC.find_one({"_id": row.get("conversation_id")}, {"messages": 1})
          for msg in reversed((convo or {}).get("messages") or []):
              if msg.get("role") == "assistant" and msg.get("content"):
                  answer = msg["content"]
                  break
          if not answer:
              skipped.append({"ask_log_id": str(row["_id"]), "reason": "no assistant answer"})
              continue

          symbol, question = row.get("symbol"), row.get("question")
          doc_log: List[str] = []
          retrieval_meta: Dict[str, Any] = {}
          try:
              # Reproduce core/ask.py::run_ask's own router call EXACTLY — both
              # flags are computed there and passed in, and is_causal in
              # particular floors the causal/signals weights, which changes
              # which sections get fetched.
              plan = evidence_router.classify_question_sources(
                  question,
                  is_red_flag=red_flag_ask.is_red_flag_question(question),
                  is_causal=redixfi_ask.is_causal_question(question),
              )
              packet = redixfi_ask.build_fact_packet(
                  db, symbol, question, api_key=api_key,
                  doc_retrieval_log=doc_log, plan=plan, retrieval_meta=retrieval_meta)
          except Exception as exc:
              skipped.append({"ask_log_id": str(row["_id"]),
                              "reason": f"packet rebuild failed: {exc}"})
              continue

          change_explanation = packet.get("change_explanation")
          causal_backstop = not (isinstance(change_explanation, dict)
                                 and bool(change_explanation.get("cause_available")))
          chunks_omitted = not bool(packet.get("document_chunks"))

          cases.append({
              "benchmark_id": f"ASK_{sanitize(symbol)}_{row['_id']}",
              "ask_log_id": str(row["_id"]),
              "conversation_id": str(row.get("conversation_id")),
              "symbol": symbol,
              "mode": row.get("mode"),
              "question": question,

              "fact_packet": packet,
              "history": None,
              "causal_backstop": causal_backstop,

              "reference": {
                  "answer": answer,
                  "refused": row.get("refused"),
                  "model": row.get("model"),
                  "sources_used": row.get("sources_used") or [],
                  "source_citations": row.get("source_citations") or [],
                  "weight": row.get("weight"),
              },

              "reconstruction_status": "PACKET_RECONSTRUCTION_PARTIAL",
              "provenance": {
                  "reference_set": "CURRENT_PIPELINE",
                  "pipeline_version": "ask@8bb3170",
                  "input_type": "REBUILT fact_packet (NOT the historical packet)",
                  "reference_model": row.get("model"),
                  "reference_prompt_version": "ask@454a07a",
                  "reference_output_schema": ["answer", "refused", "refusal_reason"],
                  "historical_retrieval_plan": row.get("retrieval_plan"),
                  "document_chunks_omitted": chunks_omitted,
                  "packet_rebuild_log": doc_log or None,
                  "redixfi_commit_at_export": redixfi_commit(),
                  "limitations": [
                      "PACKET_RECONSTRUCTION_PARTIAL — ask_log stores no fact packet, "
                      "so this one was REBUILT and is NOT the historical input.",
                      "measured_signals / signal_change_log / news_events / "
                      "fundamentals_derived are read LIVE and have moved on since the "
                      "question was asked.",
                      ("document_chunks is EMPTY: the rebuild ran with no api_key, so "
                       "no embedding call was made. The rebuilt packet is LEANER than "
                       "the original.") if chunks_omitted else
                      "document_chunks was repopulated via a live embedding call.",
                      ("retrieval_plan is absent on this row (telemetry only exists for "
                       "rows written after 2026-08-27), so which sections production "
                       "actually fetched cannot be confirmed.")
                      if not row.get("retrieval_plan") else
                      "retrieval_plan present — production's routing decision is known.",
                  ],
              },
          })

    return build_document(
        "ask_ai", cases,
        source_meta({
            "collections": ["ask_log", "ask_conversations"],
            "population_size": len(rows),
            "packet_rebuilt_via": "RedixFi core/ask.py::build_fact_packet (real)",
            "embedding_enabled": allow_embedding,
            "skipped": skipped,
        }),
        datetime.now(timezone.utc).isoformat(),
    )


BUILDERS = {
    "annual_report_summary": lambda a: build_annual_report(a.limit, a.symbol_list),
    "concall_summary": lambda a: build_concall(a.limit, a.symbol_list),
    "red_flag": lambda a: build_red_flag(a.limit, a.symbol_list),
    "ask_ai": lambda a: build_ask_ai(a.limit, a.allow_embedding),
}

DEFAULT_LIMITS = {"annual_report_summary": 20, "concall_summary": 20,
                  "red_flag": 60, "ask_ai": 30}

DEFAULT_FILENAMES = {
    "annual_report_summary": "annual_report_benchmark.json",
    "concall_summary": "concall_benchmark.json",
    "red_flag": "red_flag_benchmark.json",
    "ask_ai": "ask_ai_benchmark.json",
}


# ---------------------------------------------------------------------------
# PRE-EXPORT VALIDATION — builds everything, writes nothing
# ---------------------------------------------------------------------------
def validate_all(args) -> None:
    print("=" * 74)
    print("PRE-EXPORT VALIDATION — builds every case in memory, WRITES NOTHING")
    print("=" * 74)
    print(f"REDIXFI_ROOT : {REDIXFI_ROOT}   commit {redixfi_commit()}")
    print(f"CHROMA_PATH  : {CHROMA_PATH}")

    totals = {}
    for task in ("annual_report_summary", "concall_summary", "red_flag", "ask_ai"):
        print(f"\n--- {task} ---")
        args.limit = DEFAULT_LIMITS[task]
        try:
            doc = BUILDERS[task](args)
        except Exception as exc:
            print(f"  [ERROR] {type(exc).__name__}: {exc}")
            totals[task] = {"error": str(exc)}
            continue

        cases = doc["cases"]
        problems = validate_document(doc)
        blob = json.dumps(doc, ensure_ascii=False, default=str).encode("utf-8")
        with_ref = sum(1 for c in cases if c.get("reference"))

        totals[task] = {
            "cases": len(cases),
            "with_reference": with_ref,
            "bytes": len(blob),
            "problems": problems,
            "source": doc["source"],
        }
        print(f"  cases              : {len(cases)} (requested {DEFAULT_LIMITS[task]})")
        print(f"  with reference     : {with_ref}")
        print(f"  size               : {len(blob) / 1e6:.2f} MB")
        print(f"  schema valid       : {'YES' if not problems else 'NO'}")
        for p in problems[:10]:
            print(f"     - {p}")

        if task == "red_flag":
            print(f"  strata             : {doc['source'].get('strata')}")
            print(f"  available positives: {doc['source'].get('available_positives')}")
            print(f"  available negatives: {doc['source'].get('available_negatives')}")
        if task == "annual_report_summary":
            amb = sum(1 for c in cases
                      if (c.get("legacy_input_stats") or {}).get("input_path_ambiguous"))
            has_legacy = sum(1 for c in cases if c.get("legacy_input_text"))
            has_ev = sum(1 for c in cases if c.get("evidence_text"))
            print(f"  legacy input present : {has_legacy}/{len(cases)}")
            print(f"  evidence present     : {has_ev}/{len(cases)}")
            print(f"  legacy path AMBIGUOUS: {amb}")
            print(f"  skipped              : {doc['source'].get('skipped')}")
        if task == "ask_ai":
            stamped = sum(1 for c in cases
                          if c.get("reconstruction_status") == "PACKET_RECONSTRUCTION_PARTIAL")
            omitted = sum(1 for c in cases
                          if (c.get("provenance") or {}).get("document_chunks_omitted"))
            print(f"  PACKET_RECONSTRUCTION_PARTIAL stamped: {stamped}/{len(cases)}")
            print(f"  document_chunks omitted              : {omitted}/{len(cases)}")
            plans = sum(1 for c in cases
                        if (c.get("provenance") or {}).get("historical_retrieval_plan"))
            print(f"  historical retrieval_plan known      : {plans}/{len(cases)}")
            skipped = doc["source"].get("skipped") or []
            print(f"  skipped                              : {len(skipped)}")
            for s_ in skipped[:5]:
                print(f"     - {s_}")
        if task == "concall_summary":
            tones = {}
            for c in cases:
                t = (c.get("reference") or {}).get("tone_label")
                tones[t] = tones.get(t, 0) + 1
            print(f"  reference tone_label spread: {tones}")

    print("\n" + "=" * 74)
    print("TOTALS")
    print("=" * 74)
    total_bytes = sum(t.get("bytes", 0) for t in totals.values())
    print(f"  {'benchmark':<26} {'cases':>7} {'w/ref':>7} {'size':>10}  valid")
    for task, t in totals.items():
        if "error" in t:
            print(f"  {task:<26} {'ERROR':>7}")
            continue
        print(f"  {task:<26} {t['cases']:>7} {t['with_reference']:>7} "
              f"{t['bytes'] / 1e6:>9.2f}M  {'YES' if not t['problems'] else 'NO'}")
    print(f"  {'TOTAL':<26} {'':>7} {'':>7} {total_bytes / 1e6:>9.2f}M   4 files")

    print("\n  SAFETY: no Mongo writes, no Chroma writes, no updates, no deletes,")
    print("          no index changes, no scheduler changes, no OpenAI calls.")
    print("          Nothing was written to disk by this validation run.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export RedixFi evaluation fixtures (READ-ONLY)")
    parser.add_argument("--task", choices=sorted(BUILDERS))
    parser.add_argument("--out")
    parser.add_argument("--out-dir", default="/home/ubuntu/llm_fixtures")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--symbols")
    parser.add_argument("--validate", action="store_true",
                        help="build every benchmark in memory and report; writes nothing")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--allow-embedding", action="store_true",
                        help="ask_ai only: permit the live OpenAI embedding call during "
                             "packet rebuild (OFF by default — the export makes zero "
                             "OpenAI calls)")
    args = parser.parse_args()
    args.symbol_list = ([s.strip().upper() for s in args.symbols.split(",")]
                        if args.symbols else None)

    if args.validate or not args.task:
        validate_all(args)
        return

    if args.limit is None:
        args.limit = DEFAULT_LIMITS[args.task]
    doc = BUILDERS[args.task](args)
    problems = validate_document(doc)

    print(f"\n[SUMMARY] task={doc['task']} cases={len(doc['cases'])} "
          f"with_reference={sum(1 for c in doc['cases'] if c.get('reference'))}")
    if problems:
        print("[INVALID]\n  - " + "\n  - ".join(problems))
        raise SystemExit(2)

    if args.dry_run:
        print("\nDry run — nothing written.")
        return

    out = args.out or os.path.join(args.out_dir, DEFAULT_FILENAMES[args.task])
    if os.path.abspath(out).startswith(os.path.abspath(REDIXFI_ROOT)):
        raise SystemExit(f"refusing to write inside the RedixFi tree: {out}")
    save(doc, out)
    print(f"\n[WROTE] {out}")
    print("This is the ONLY file this script created. No production store was modified.")


if __name__ == "__main__":
    main()
