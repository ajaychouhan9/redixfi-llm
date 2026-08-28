#!/usr/bin/env python3
"""READ-ONLY Ask AI preflight (section 4 only).

Split out from vm_preflight.py so re-running it does not re-scan 56,913
ChromaDB vectors for numbers already collected.

WRITES NOTHING: count_documents, find(+projection), aggregate
($match/$group/$sort only). No OpenAI call, no packet rebuild — a rebuild
would issue an embedding request, which this preflight must not do.

The `redixfi_app` database uses a DIFFERENT credential from the pipeline
DB. This script obtains it the way RedixFi itself does — via
api/app/core/db.py::get_app_db(), which reads MONGO_URI_APP from api/.env.
The URI is never read, printed, or written anywhere by this script.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone

REDIXFI_ROOT = os.getenv("REDIXFI_ROOT", "/home/ubuntu/redixfi-backend")
sys.path.insert(0, REDIXFI_ROOT)


def head(title):
    print("\n" + "=" * 74)
    print(title)
    print("=" * 74)


def row(label, value, note=""):
    print(f"  {label:<46} {str(value):>12}  {note}")


_api_dir = os.path.join(REDIXFI_ROOT, "api")
sys.path.insert(0, _api_dir)
_cwd = os.getcwd()
os.chdir(_api_dir)
try:
    from app.core.db import get_app_db  # type: ignore
    app_db = get_app_db()
    collections = app_db.list_collection_names()
finally:
    os.chdir(_cwd)

head("4. ASK AI (app db: ask_log + ask_conversations)")
row("app db", app_db.name)
print(f"  collections: {sorted(collections)}\n")

AL = app_db["ask_log"]
AC = app_db["ask_conversations"]
ask = {}

ask["ask_log_total"] = AL.count_documents({})
ask["with_question"] = AL.count_documents({"question": {"$exists": True, "$ne": ""}})
ask["with_symbol"] = AL.count_documents({"symbol": {"$ne": None}})
ask["with_conversation_id"] = AL.count_documents(
    {"conversation_id": {"$exists": True, "$ne": None}})
ask["with_sources_used"] = AL.count_documents({"sources_used": {"$exists": True}})
ask["with_source_citations"] = AL.count_documents({"source_citations": {"$exists": True}})
ask["with_retrieval_plan"] = AL.count_documents({"retrieval_plan": {"$ne": None}})
ask["with_weight"] = AL.count_documents({"weight": {"$exists": True}})
ask["refused_true"] = AL.count_documents({"refused": True})
ask["conversations_total"] = AC.count_documents({})

row("ask_log documents", ask["ask_log_total"])
row("  with question", ask["with_question"])
row("  with symbol", ask["with_symbol"])
row("  with conversation_id", ask["with_conversation_id"])
row("  with sources_used", ask["with_sources_used"])
row("  with source_citations", ask["with_source_citations"])
row("  with retrieval_plan (post-08-27 only)", ask["with_retrieval_plan"])
row("  with weight", ask["with_weight"])
row("  refused = true", ask["refused_true"])
row("ask_conversations documents", ask["conversations_total"])

for field, label in (("mode", "by mode"), ("model", "by model")):
    rows = list(AL.aggregate([{"$group": {"_id": f"${field}", "n": {"$sum": 1}}},
                              {"$sort": {"n": -1}}]))
    ask[f"by_{field}"] = {str(r["_id"]): r["n"] for r in rows}
    print(f"\n  {label}: {ask[f'by_{field}']}")

# Can a case be joined to a real assistant answer? ask_log stores no answer.
head("4b. JOINABILITY — ask_log -> ask_conversations (the reference answer)")
joinable = checked = 0
answer_lens = []
examples = []
for r in AL.find(
    {"question": {"$exists": True, "$ne": ""}, "conversation_id": {"$ne": None}},
    {"_id": 1, "conversation_id": 1, "question": 1, "model": 1, "symbol": 1,
     "mode": 1, "refused": 1, "sources_used": 1},
).sort("_id", -1).limit(500):
    checked += 1
    convo = AC.find_one({"_id": r["conversation_id"]}, {"messages": 1})
    for msg in reversed((convo or {}).get("messages") or []):
        if msg.get("role") == "assistant" and msg.get("content"):
            joinable += 1
            answer_lens.append(len(msg["content"]))
            if len(examples) < 5:
                examples.append({
                    "ask_log_id": str(r["_id"]), "symbol": r.get("symbol"),
                    "mode": r.get("mode"), "model": r.get("model"),
                    "question": (r.get("question") or "")[:90],
                    "answer_chars": len(msg["content"]),
                    "sources_used": r.get("sources_used"),
                })
            break

ask["join_checked"] = checked
ask["join_resolved"] = joinable
ask["mean_answer_chars"] = int(sum(answer_lens) / len(answer_lens)) if answer_lens else 0
row("newest rows checked", checked)
row("resolved to a real assistant answer", joinable, "<- Phase C ceiling (sampled)")
row("mean answer length (chars)", ask["mean_answer_chars"])

# Of the joinable ones, how many are a real (non-refused, model-generated) answer?
ask["by_model_joinable"] = {}
for r in AL.find({"question": {"$exists": True, "$ne": ""},
                  "conversation_id": {"$ne": None}},
                 {"model": 1}).sort("_id", -1).limit(500):
    m = str(r.get("model"))
    ask["by_model_joinable"][m] = ask["by_model_joinable"].get(m, 0) + 1
print(f"\n  model breakdown of those {checked} rows: {ask['by_model_joinable']}")
print("  (only model='gpt-4o-mini' rows are a real LLM answer; 'template',")
print("   'document-not-found', 'red-flag-ask' etc. are deterministic paths")
print("   with no LLM generation to compare against)")

print("\n  sample joinable cases:")
for e in examples:
    print(f"    ASK_{e['ask_log_id']}  {e['symbol']}  model={e['model']}  "
          f"{e['answer_chars']}ch  q={e['question']!r}")

head("4c. PACKET RECONSTRUCTION — honest status")
print("""  ask_log does NOT store the fact packet. Neither does ask_conversations.
  The packet can only be REBUILT by calling core/ask.py::build_fact_packet
  again, and that rebuild is NOT byte-identical to what the LLM originally
  saw, because:

    1. measured_signals / signal_change_log / news_events / fundamentals_
       derived are read LIVE and have moved on since the question was asked.
    2. document_chunks requires a live OpenAI embedding call. With the
       account out of credits it fails soft to [], so the rebuilt packet is
       LEANER than the original.
    3. retrieval_plan is only stored on rows written after 2026-08-27, so
       older rows cannot even confirm which sections were fetched.

  Every exported ask_ai case must therefore be stamped
  PACKET_RECONSTRUCTION_PARTIAL. No export should claim an exact packet.""")

out = "/home/ubuntu/llm_preflight/preflight_ask.json"
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w") as fh:
    json.dump({"generated_at": datetime.now(timezone.utc).isoformat(),
               "ask_ai": ask, "examples": examples}, fh, indent=2, default=str)
print(f"\n  (machine-readable copy: {out})")
