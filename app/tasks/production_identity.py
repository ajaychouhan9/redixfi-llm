"""Carry immutable dispatch identity through normal generation/validation."""
from datetime import datetime, timezone

def attach_identity(row, case):
    row = dict(row)
    for key in ("filing_id", "chunk_id", "symbol", "source_collection", "dispatch_token"):
        row[key] = case.get(key)
    row["generated_at"] = datetime.now(timezone.utc).isoformat()
    return row
