"""READ-ONLY accessors for RedixFi's production stores.

SCOPE AND SAFETY — read before using anything here.

1. **Read-only by construction.** Every function in this module issues only
   `find`, `find_one`, `count_documents`, or ChromaDB `get`/`count`. There
   is no insert/update/delete/upsert path, and there must never be one. If
   a future need arises to persist evaluation results, it goes to a JSON
   file or a SEPARATE database — never back into `redixfi` or
   `redixfi_app`.

2. **Runs ON the RedixFi VM only.** MongoDB is bound to loopback there;
   ChromaDB is an embedded PersistentClient over a local directory. Neither
   is reachable from anywhere else, and this module does not pretend
   otherwise — there is no host/port network client here.

3. **NOT required for the initial evaluation** (founder decision,
   2026-08-28). Kaggle runs entirely from exported fixture files. This
   module exists so `scripts/export_fixtures.py` has one audited place
   where production reads happen, and as the prepared foundation for any
   future integration.
"""
from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..config.settings import Settings, get_settings

# Collections this module is permitted to read. Anything outside this set is
# refused — a narrow allowlist is easier to audit than a broad prohibition.
ALLOWED_COLLECTIONS = frozenset({
    "annual_reports",
    "investor_calls",
    "promoter_pledge_history",
    "measured_signals",
    "fundamentals_derived",
    "signal_change_log",
    "news_events",
    "symbols_master",
    "ask_log",
    "ask_conversations",
})


class ReadOnlyGuard(Exception):
    """Raised when something attempts a non-read operation or an
    out-of-allowlist collection."""


class RedixFiMongoReader:
    def __init__(self, settings: Optional[Settings] = None) -> None:
        self.settings = settings or get_settings()
        self._client = None

    def _connect(self):
        if self._client is None:
            from pymongo import MongoClient
            self._client = MongoClient(
                self.settings.mongo_uri,
                serverSelectionTimeoutMS=10_000,
                # Belt-and-braces: even if a caller found a write path, the
                # driver would refuse it against a secondary. Harmless on a
                # standalone, meaningful on a replica set.
                readPreference="secondaryPreferred",
            )
        return self._client

    def _collection(self, name: str, app_db: bool = False):
        if name not in ALLOWED_COLLECTIONS:
            raise ReadOnlyGuard(
                f"collection '{name}' is not in the read allowlist: "
                f"{sorted(ALLOWED_COLLECTIONS)}"
            )
        client = self._connect()
        db_name = self.settings.mongo_app_db_name if app_db else self.settings.mongo_db_name
        return client[db_name][name]

    def count(self, name: str, query: Optional[Dict[str, Any]] = None, app_db: bool = False) -> int:
        return self._collection(name, app_db).count_documents(query or {})

    def find(
        self,
        name: str,
        query: Optional[Dict[str, Any]] = None,
        projection: Optional[Dict[str, Any]] = None,
        sort: Optional[List[tuple]] = None,
        limit: int = 0,
        app_db: bool = False,
    ) -> Iterator[Dict[str, Any]]:
        cursor = self._collection(name, app_db).find(query or {}, projection)
        if sort:
            cursor = cursor.sort(sort)
        if limit:
            cursor = cursor.limit(limit)
        return cursor

    def find_one(
        self,
        name: str,
        query: Dict[str, Any],
        projection: Optional[Dict[str, Any]] = None,
        sort: Optional[List[tuple]] = None,
        app_db: bool = False,
    ) -> Optional[Dict[str, Any]]:
        return self._collection(name, app_db).find_one(query, projection, sort=sort)

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None


class RedixFiChromaReader:
    """Embedded ChromaDB reader. NOTE: a PersistentClient over a directory,
    NOT a network client — there is no host/port because RedixFi has none."""

    def __init__(self, settings: Optional[Settings] = None) -> None:
        self.settings = settings or get_settings()
        self._client = None

    def _connect(self):
        if self._client is None:
            import chromadb
            self._client = chromadb.PersistentClient(path=self.settings.chroma_path)
        return self._client

    def collection_names(self) -> List[str]:
        client = self._connect()
        try:
            return [c.name for c in client.list_collections()]
        except Exception:
            # Newer chromadb returns bare strings from list_collections().
            return list(client.list_collections())

    def count(self, name: str) -> int:
        return self._connect().get_collection(name).count()

    def get_page(
        self,
        name: str,
        limit: int = 500,
        offset: int = 0,
        where: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Paginated read. The page size matters: RedixFi hit
        `chromadb.errors.InternalError: too many SQL variables` in
        production (2026-08-23) from an unbounded `.get()`, because SQLite's
        999-parameter ceiling is trivially exceeded by rows x metadata keys.
        500 is the batch size RedixFi settled on after reproducing it."""
        collection = self._connect().get_collection(name)
        kwargs: Dict[str, Any] = {
            "include": ["documents", "metadatas"],
            "limit": limit,
            "offset": offset,
        }
        if where:
            kwargs["where"] = where
        return collection.get(**kwargs)

    def iter_chunks(
        self,
        name: str,
        where: Optional[Dict[str, Any]] = None,
        page_size: int = 500,
        max_items: Optional[int] = None,
    ) -> Iterator[Dict[str, Any]]:
        offset = 0
        yielded = 0
        while True:
            page = self.get_page(name, limit=page_size, offset=offset, where=where)
            ids = page.get("ids") or []
            if not ids:
                return
            docs = page.get("documents") or []
            metas = page.get("metadatas") or []
            for chunk_id, document, metadata in zip(ids, docs, metas):
                yield {"id": chunk_id, "document": document, "metadata": metadata or {}}
                yielded += 1
                if max_items and yielded >= max_items:
                    return
            offset += len(ids)
