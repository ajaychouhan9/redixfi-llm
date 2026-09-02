#!/usr/bin/env python3
"""COMPREHENSIVE READ-ONLY PREFLIGHT for the fixture export. RUNS ON THE VM.

WRITES NOTHING. Every operation in this file is one of:
  * MongoDB  : count_documents, find (with a projection), aggregate ($match/
               $group/$project only — no $out, no $merge)
  * ChromaDB : count(), get() with include=[] or ["metadatas"]
  * filesystem: reading a file's SIZE only

There is no insert/update/delete/index/drop path anywhere here, and no
OpenAI or other network call. It is safe to run while the annual-report
backfill is writing, though counts it reports are a moving snapshot.

Run:
    cd /home/ubuntu/redixfi-backend
    api/.venv/bin/python /home/ubuntu/llm_preflight/vm_preflight.py
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone

REDIXFI_ROOT = os.getenv("REDIXFI_ROOT", "/home/ubuntu/redixfi-backend")
# 2026-09-02: repointed at the new dedicated /data/chroma mount (127GB
# ext4, permanent in /etc/fstab) after the chroma_production wipe -- a
# separate top-level mount, not derived from REDIXFI_ROOT anymore.
CHROMA_PATH = os.getenv("CHROMA_PATH", "/data/chroma")
sys.path.insert(0, REDIXFI_ROOT)

RESULT = {"generated_at": datetime.now(timezone.utc).isoformat()}


def head(title):
    print("\n" + "=" * 74)
    print(title)
    print("=" * 74)


def row(label, value, note=""):
    print(f"  {label:<46} {str(value):>12}  {note}")


# ---------------------------------------------------------------------------
# Connections
# ---------------------------------------------------------------------------
from config.db import get_db  # noqa: E402

db = get_db()

# The app DB (`redixfi_app`) uses a DIFFERENT credential from the pipeline
# DB — the pipeline user is not authorized on it. Obtain the connection the
# way RedixFi itself does (api/app/core/db.py::get_app_db, which reads
# MONGO_URI_APP from api/.env) rather than handling a credential here. The
# URI is never read, printed, or stored by this script.
app_db = None
try:
    _api_dir = os.path.join(REDIXFI_ROOT, "api")
    if _api_dir not in sys.path:
        sys.path.insert(0, _api_dir)
    _cwd = os.getcwd()
    os.chdir(_api_dir)  # api/app/core/config.py resolves api/.env relatively
    try:
        from app.core.db import get_app_db  # type: ignore
        app_db = get_app_db()
        app_db.list_collection_names()  # prove authorization before relying on it
    finally:
        os.chdir(_cwd)
except Exception as exc:
    app_db = None
    print(f"[WARN] app_db unavailable ({type(exc).__name__}): "
          f"{str(exc)[:160]}")

head("0. ENVIRONMENT")
row("pipeline db", db.name)
row("app db", app_db.name if app_db is not None else "UNAVAILABLE")
row("chroma path", CHROMA_PATH)
import subprocess  # noqa: E402
commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REDIXFI_ROOT,
                        capture_output=True, text=True).stdout.strip()
row("redixfi commit", commit)
backfill = subprocess.run(["pgrep", "-af", "annual_report_api"],
                          capture_output=True, text=True).stdout.strip()
row("backfill running", "YES" if backfill else "no",
    "counts below are a MOVING SNAPSHOT" if backfill else "")
RESULT["environment"] = {"commit": commit, "backfill_running": bool(backfill),
                         "chroma_path": CHROMA_PATH}

# ---------------------------------------------------------------------------
# 1. ANNUAL REPORT
# ---------------------------------------------------------------------------
head("1. ANNUAL REPORT (mongo: annual_reports)")
AR = db["annual_reports"]
ar = {}
ar["total"] = AR.count_documents({})
ar["extraction_ok"] = AR.count_documents({"extraction_status": "OK"})
ar["eligible_raw_text"] = AR.count_documents(
    {"extraction_status": "OK", "raw_text": {"$exists": True, "$ne": ""}})
ar["with_summary"] = AR.count_documents({"summary": {"$exists": True}})
ar["with_executive_summary"] = AR.count_documents({"executive_summary": {"$exists": True}})
ar["with_key_points"] = AR.count_documents({"key_points": {"$exists": True}})
ar["with_important_risks"] = AR.count_documents({"important_risks": {"$exists": True}})
ar["with_key_takeaway"] = AR.count_documents({"key_takeaway": {"$exists": True}})
ar["embedded"] = AR.count_documents({"embedded": True})
ar["with_filing_id"] = AR.count_documents({"filing_id": {"$exists": True, "$ne": ""}})
ar["benchmarkable"] = AR.count_documents(
    {"extraction_status": "OK", "raw_text": {"$exists": True, "$ne": ""},
     "summary": {"$exists": True, "$ne": ""}})

row("total documents", ar["total"])
row("extraction_status OK", ar["extraction_ok"])
row("ELIGIBLE (OK + non-empty raw_text)", ar["eligible_raw_text"])
row("with summary (legacy field)", ar["with_summary"])
row("with executive_summary (new schema)", ar["with_executive_summary"])
row("with key_points", ar["with_key_points"])
row("with important_risks", ar["with_important_risks"])
row("with key_takeaway", ar["with_key_takeaway"])
row("with filing_id", ar["with_filing_id"])
row("embedded into ChromaDB", ar["embedded"])
row("BENCHMARKABLE (eligible + summary)", ar["benchmarkable"], "<- Phase A ceiling")

# which summarizer version produced them
models = list(AR.aggregate([
    {"$match": {"summary_model": {"$exists": True}}},
    {"$group": {"_id": "$summary_model", "n": {"$sum": 1}}}]))
ar["summary_models"] = {m["_id"]: m["n"] for m in models}
print(f"\n  summary_model breakdown: {ar['summary_models']}")

# Evidence Finder feasibility — sampled, NOT run over the whole corpus.
head("1b. EVIDENCE FINDER feasibility (sampled, read-only)")
sys.path.insert(0, os.path.join(REDIXFI_ROOT, "data-pipeline"))
import evidence_finder as ef  # noqa: E402

sample = list(AR.find(
    {"extraction_status": "OK", "raw_text": {"$exists": True, "$ne": ""},
     "summary": {"$exists": True, "$ne": ""}},
    {"_id": 0, "symbol": 1, "fiscal_year": 1, "filing_id": 1, "raw_text": 1,
     "page_count": 1}).limit(8))

ev_ok = 0
ev_tokens = []
ev_bytes = []
for d in sample:
    chunks = ef.chunks_from_raw_text(d.get("raw_text") or "", symbol=d.get("symbol") or "",
                                     token_target=500, page_count=d.get("page_count"))
    if not chunks:
        print(f"  [NO CHUNKS] {d.get('symbol')}")
        continue
    res = ef.build_narrative_evidence_result(chunks, max_tokens=20000)
    if res.get("text"):
        ev_ok += 1
        ev_tokens.append(res["total_tokens"])
        ev_bytes.append(len(res["text"].encode("utf-8")))
        print(f"  [OK] {d.get('symbol'):<12} {d.get('fiscal_year'):<12} "
              f"chunks={len(chunks):<5} selected={res['selected_chunks']:<3} "
              f"tokens={res['total_tokens']:<6} bytes={ev_bytes[-1]:,}")
    else:
        print(f"  [NO EVIDENCE] {d.get('symbol')}")

ar["evidence_sampled"] = len(sample)
ar["evidence_ok"] = ev_ok
ar["evidence_mean_tokens"] = int(sum(ev_tokens) / len(ev_tokens)) if ev_tokens else 0
ar["evidence_mean_bytes"] = int(sum(ev_bytes) / len(ev_bytes)) if ev_bytes else 0
print(f"\n  Evidence produced for {ev_ok}/{len(sample)} sampled documents")
print(f"  mean evidence: {ar['evidence_mean_tokens']} tokens, "
      f"{ar['evidence_mean_bytes']:,} bytes/case")
RESULT["annual_report"] = ar

# ---------------------------------------------------------------------------
# 2. CONCALL
# ---------------------------------------------------------------------------
head("2. CONCALL (mongo: investor_calls)")
IC = db["investor_calls"]
cc = {}
cc["total"] = IC.count_documents({})
cc["extraction_ok"] = IC.count_documents({"extraction_status": "OK"})
cc["eligible_transcript"] = IC.count_documents(
    {"extraction_status": "OK", "raw_transcript_text": {"$exists": True, "$ne": ""}})
cc["with_summary"] = IC.count_documents({"summary": {"$exists": True}})
cc["with_tone_label"] = IC.count_documents({"tone_label": {"$exists": True}})
cc["with_tone_note"] = IC.count_documents({"tone_note": {"$exists": True}})
cc["benchmarkable"] = IC.count_documents(
    {"extraction_status": "OK", "raw_transcript_text": {"$exists": True, "$ne": ""},
     "summary": {"$exists": True, "$ne": ""}})
row("total documents", cc["total"])
row("extraction_status OK", cc["extraction_ok"])
row("ELIGIBLE (OK + non-empty transcript)", cc["eligible_transcript"])
row("with summary (gpt-4o-mini output)", cc["with_summary"])
row("with tone_label", cc["with_tone_label"])
row("with tone_note", cc["with_tone_note"])
row("BENCHMARKABLE (transcript + summary)", cc["benchmarkable"], "<- Phase D ceiling")

models = list(IC.aggregate([
    {"$match": {"summary_model": {"$exists": True}}},
    {"$group": {"_id": "$summary_model", "n": {"$sum": 1}}}]))
cc["summary_models"] = {m["_id"]: m["n"] for m in models}
print(f"\n  summary_model breakdown: {cc['summary_models']}")

sizes = list(IC.aggregate([
    {"$match": {"raw_transcript_text": {"$exists": True, "$ne": ""},
                "summary": {"$exists": True}}},
    {"$project": {"len": {"$strLenCP": "$raw_transcript_text"}}},
    {"$group": {"_id": None, "avg": {"$avg": "$len"}, "max": {"$max": "$len"},
                "min": {"$min": "$len"}}}]))
if sizes:
    cc["transcript_chars"] = {k: int(v) for k, v in sizes[0].items() if k != "_id"}
    print(f"  transcript chars (min/avg/max): {cc['transcript_chars']['min']:,} / "
          f"{cc['transcript_chars']['avg']:,} / {cc['transcript_chars']['max']:,}")
    print("  NOTE: concall_summarizer sends raw_transcript_text[:120000] — a flat "
          "front slice, NOT Evidence Finder.")
RESULT["concall"] = cc

# ---------------------------------------------------------------------------
# 3. RED FLAG
# ---------------------------------------------------------------------------
head("3. RED FLAG (ChromaDB metadata)")
rf = {}
try:
    import chromadb
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    try:
        names = [c.name for c in client.list_collections()]
    except Exception:
        names = list(client.list_collections())
    rf["collections"] = {}
    print(f"  collections: {names}\n")

    CATS = ["auditor_qualification", "contingent_liability",
            "related_party_transaction", "promoter_pledge"]

    for name in names:
        col = client.get_collection(name)
        info = {"vectors": col.count()}

        def count_where(where):
            """ids-only paginated count — include=[] keeps it cheap and stays
            well under SQLite's bound-parameter ceiling."""
            total, offset = 0, 0
            while True:
                page = col.get(where=where, include=[], limit=1000, offset=offset)
                got = len(page.get("ids") or [])
                total += got
                if got < 1000:
                    return total
                offset += got

        try:
            info["risk_classified"] = count_where({"risk_classified": True})
        except Exception as exc:
            info["risk_classified"] = f"ERROR: {exc}"
        try:
            info["risk_flag_type_any"] = count_where({"risk_flag_type": {"$in": CATS}})
        except Exception as exc:
            info["risk_flag_type_any"] = f"ERROR: {exc}"

        info["by_category"] = {}
        for cat in CATS:
            try:
                info["by_category"][cat] = count_where({"risk_flag_type": cat})
            except Exception as exc:
                info["by_category"][cat] = f"ERROR: {exc}"

        # summaries present on flagged chunks
        try:
            flagged = col.get(where={"risk_flag_type": {"$in": CATS}},
                              include=["metadatas"], limit=1000)
            metas = flagged.get("metadatas") or []
            info["with_summary_sampled"] = sum(
                1 for m in metas if (m or {}).get("risk_flag_summary"))
            info["sampled_flagged"] = len(metas)
        except Exception as exc:
            info["with_summary_sampled"] = f"ERROR: {exc}"

        # metadata key census on a small sample
        try:
            s = col.get(include=["metadatas"], limit=200)
            keys = Counter()
            for m in (s.get("metadatas") or []):
                keys.update((m or {}).keys())
            info["metadata_keys_sampled"] = dict(keys)
        except Exception:
            pass

        rf["collections"][name] = info
        print(f"  --- {name} ---")
        row("vectors", info["vectors"])
        row("risk_classified = True", info["risk_classified"])
        row("risk_flag_type present", info["risk_flag_type_any"])
        for cat, n in info["by_category"].items():
            row(f"  {cat}", n)
        row("flagged chunks carrying a summary",
            f"{info.get('with_summary_sampled')}/{info.get('sampled_flagged')}")
        print(f"    metadata keys seen: {sorted(info.get('metadata_keys_sampled', {}))}")
        print()
except Exception as exc:
    rf["error"] = str(exc)
    print(f"  [ERROR] {exc}")
RESULT["red_flag"] = rf

# ---------------------------------------------------------------------------
# 4. ASK AI
# ---------------------------------------------------------------------------
head("4. ASK AI (app db: ask_log + ask_conversations)")
ask = {}
if app_db is None:
    ask["error"] = "app db unavailable"
    print("  [ERROR] app db unavailable")
else:
    AL = app_db["ask_log"]
    AC = app_db["ask_conversations"]
    ask["ask_log_total"] = AL.count_documents({})
    ask["with_question"] = AL.count_documents({"question": {"$exists": True, "$ne": ""}})
    ask["with_symbol"] = AL.count_documents({"symbol": {"$ne": None}})
    ask["with_conversation_id"] = AL.count_documents(
        {"conversation_id": {"$exists": True, "$ne": None}})
    ask["with_sources_used"] = AL.count_documents({"sources_used": {"$exists": True}})
    ask["with_retrieval_plan"] = AL.count_documents({"retrieval_plan": {"$ne": None}})
    ask["with_weight"] = AL.count_documents({"weight": {"$exists": True}})
    ask["refused_true"] = AL.count_documents({"refused": True})
    ask["conversations_total"] = AC.count_documents({})

    row("ask_log documents", ask["ask_log_total"])
    row("with question", ask["with_question"])
    row("with symbol", ask["with_symbol"])
    row("with conversation_id", ask["with_conversation_id"])
    row("with sources_used", ask["with_sources_used"])
    row("with retrieval_plan (new telemetry)", ask["with_retrieval_plan"],
        "<- only these can show routing")
    row("with weight", ask["with_weight"])
    row("refused = true", ask["refused_true"])
    row("ask_conversations documents", ask["conversations_total"])

    by_mode = list(AL.aggregate([{"$group": {"_id": "$mode", "n": {"$sum": 1}}},
                                 {"$sort": {"n": -1}}]))
    ask["by_mode"] = {str(m["_id"]): m["n"] for m in by_mode}
    by_model = list(AL.aggregate([{"$group": {"_id": "$model", "n": {"$sum": 1}}},
                                  {"$sort": {"n": -1}}]))
    ask["by_model"] = {str(m["_id"]): m["n"] for m in by_model}
    print(f"\n  by mode : {ask['by_mode']}")
    print(f"  by model: {ask['by_model']}")

    # How many can actually be joined to a real assistant answer?
    joinable = 0
    checked = 0
    answer_lens = []
    for r in AL.find({"mode": "symbol", "question": {"$exists": True, "$ne": ""},
                      "conversation_id": {"$ne": None}},
                     {"_id": 0, "conversation_id": 1, "question": 1, "model": 1}
                     ).sort("_id", -1).limit(300):
        checked += 1
        convo = AC.find_one({"_id": r["conversation_id"]}, {"messages": 1})
        for msg in reversed((convo or {}).get("messages") or []):
            if msg.get("role") == "assistant" and msg.get("content"):
                joinable += 1
                answer_lens.append(len(msg["content"]))
                break
    ask["join_checked"] = checked
    ask["join_resolved_to_answer"] = joinable
    ask["mean_answer_chars"] = int(sum(answer_lens) / len(answer_lens)) if answer_lens else 0
    print(f"\n  join test (newest {checked} symbol-mode rows):")
    row("resolved to a real assistant answer", joinable, "<- Phase C ceiling (sampled)")
    row("mean answer length (chars)", ask["mean_answer_chars"])
    print("\n  NOTE: ask_log stores NO fact packet. A packet must be REBUILT, and a")
    print("        rebuild is not byte-identical to what the LLM originally saw.")
RESULT["ask_ai"] = ask

# ---------------------------------------------------------------------------
# 5. SIZE ESTIMATES
# ---------------------------------------------------------------------------
head("5. STORAGE ESTIMATE (per proposed sample)")
PROPOSED = {"annual_report": 20, "concall": 20, "red_flag": 60, "ask_ai": 40}
est = {}

ar_bytes = ar.get("evidence_mean_bytes", 80000) + 3000
est["annual_report"] = PROPOSED["annual_report"] * ar_bytes
row("annual_report", f"{est['annual_report'] / 1e6:.2f} MB",
    f"{PROPOSED['annual_report']} x ~{ar_bytes / 1000:.0f} KB")

cc_bytes = 120000 + 2000  # transcript slice actually sent + reference
est["concall"] = PROPOSED["concall"] * cc_bytes
row("concall", f"{est['concall'] / 1e6:.2f} MB",
    f"{PROPOSED['concall']} x ~{cc_bytes / 1000:.0f} KB")

rf_bytes = 3000
est["red_flag"] = PROPOSED["red_flag"] * rf_bytes
row("red_flag", f"{est['red_flag'] / 1e6:.2f} MB",
    f"{PROPOSED['red_flag']} x ~{rf_bytes / 1000:.0f} KB")

ask_bytes = 25000
est["ask_ai"] = PROPOSED["ask_ai"] * ask_bytes
row("ask_ai", f"{est['ask_ai'] / 1e6:.2f} MB",
    f"{PROPOSED['ask_ai']} x ~{ask_bytes / 1000:.0f} KB")

row("TOTAL", f"{sum(est.values()) / 1e6:.2f} MB", "4 JSON files")
RESULT["size_estimate_bytes"] = est
RESULT["proposed_samples"] = PROPOSED

# ---------------------------------------------------------------------------
# 6. SAFETY
# ---------------------------------------------------------------------------
head("6. SAFETY — operations performed by THIS script")
for line in [
    "MongoDB      : count_documents, find(+projection), aggregate($match/$group/$project)",
    "ChromaDB     : count(), get(include=[] | ['metadatas'])",
    "Filesystem   : read only (evidence_finder chunking is in-memory)",
    "RedixFi code : imported config.db, data-pipeline/evidence_finder.py (pure)",
    "",
    "NO insert  NO update  NO delete  NO index change  NO drop",
    "NO scheduler change  NO OpenAI call  NO external LLM call  NO file written",
]:
    print("  " + line)

out = "/home/ubuntu/llm_preflight/preflight_result.json"
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w") as fh:
    json.dump(RESULT, fh, indent=2, default=str)
print(f"\n  (machine-readable copy: {out} — outside the RedixFi repo)")
