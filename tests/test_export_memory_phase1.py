import importlib.util
import json


SPEC = importlib.util.spec_from_file_location(
    "export_generation_batch",
    "production/export_generation_batch.py",
)
EXPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORT)


class Cursor(list):
    def sort(self, fields):
        for field, direction in reversed(fields):
            super().sort(key=lambda row: row.get(field), reverse=direction < 0)
        return self

    def limit(self, amount):
        return Cursor(self[:amount])


def project(doc, projection):
    if not projection:
        return dict(doc)
    include = {key for key, value in projection.items() if value and key != "_id"}
    return {key: value for key, value in doc.items() if key in include}


class FakeCollection:
    def __init__(self, rows):
        self.rows = rows
        self.projections = []

    def find(self, query, projection=None):
        rows = []
        for row in self.rows:
            if query.get("task") and row.get("task") != query["task"]:
                continue
            if query.get("state") and row.get("state") != query["state"]:
                continue
            if query.get("doc_id") and row.get("doc_id") != query["doc_id"]:
                continue
            if query.get("filing_id"):
                clause = query["filing_id"]
                if "$nin" in clause and row.get("filing_id") in clause["$nin"]:
                    continue
                if "$exists" in clause and clause["$exists"] and "filing_id" not in row:
                    continue
            if query.get("extraction_status") and row.get("extraction_status") != query["extraction_status"]:
                continue
            text_clause = query.get("raw_text")
            if text_clause and text_clause.get("$exists") and not row.get("raw_text"):
                continue
            if query.get("summary_reviewed_by", {}).get("$exists") and "summary_reviewed_by" in row:
                continue
            rows.append(project(row, projection))
        self.projections.append(projection)
        return Cursor(rows)

    def find_one(self, query, projection=None):
        for row in self.rows:
            if query.get("filing_id") and row.get("filing_id") != query["filing_id"]:
                continue
            if query.get("extraction_status") and row.get("extraction_status") != query["extraction_status"]:
                continue
            clause = query.get("raw_text")
            if clause and clause.get("$exists") and not row.get("raw_text"):
                continue
            self.projections.append(projection)
            return project(row, projection)
        self.projections.append(projection)
        return None


class FakeDB:
    def __init__(self, documents, queue=None, claims=None):
        self.collections = {
            "annual_reports": FakeCollection(documents),
            "llm_review_queue": FakeCollection(queue or []),
            "llm_generation_claims": FakeCollection(claims or []),
        }

    def __getitem__(self, name):
        return self.collections[name]

    @property
    def llm_generation_batches(self):
        return FakeCollection([])


def test_selection_keeps_retry_state_bounded_and_projected():
    docs = [
        {"filing_id": f"retry-{i}", "raw_text": "source", "extraction_status": "OK"}
        for i in range(100)
    ] + [
        {"filing_id": f"normal-{i}", "raw_text": "source", "extraction_status": "OK",
         "filing_date": i}
        for i in range(100)
    ]
    queue = [{"doc_id": f"retry-{i}", "task": "annual_report", "state": "retry_queued",
              "updated_at": i} for i in range(100)]
    db = FakeDB(docs, queue=queue)

    refs, unavailable = EXPORT.select_document_refs(db, "annual_report", 20)

    assert len(refs) == 20
    assert not unavailable
    assert all(isinstance(doc_id, str) and isinstance(retry, bool) for doc_id, retry in refs)
    retry_projections = db.collections["annual_reports"].projections[:100]
    assert retry_projections
    assert all(set(projection) <= {"filing_id", "_id"} for projection in retry_projections if projection)


def test_export_cases_preserve_contract_with_one_document_at_a_time(tmp_path):
    docs = [
        {"filing_id": "a", "symbol": "AAA", "company_name": "A", "filing_date": "2026-01-01",
         "raw_text": "alpha", "extraction_status": "OK"},
        {"filing_id": "b", "symbol": "BBB", "company_name": "B", "filing_date": "2026-01-02",
         "raw_text": "bravo", "extraction_status": "OK"},
    ]
    db = FakeDB(docs)

    def builder(task, doc):
        return {"filing_id": doc["filing_id"], "input_text": doc["raw_text"]}

    original = EXPORT.review_lock
    class NoopLock:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
    EXPORT.review_lock = lambda _: NoopLock()
    try:
        payload = EXPORT.export(db, "annual_report", 2, str(tmp_path / "out.json"), builder=builder)
    finally:
        EXPORT.review_lock = original

    assert [(case["filing_id"], case["input_text"]) for case in payload["cases"]] == [
        ("a", "alpha"), ("b", "bravo")
    ]
    assert payload["schema_version"] == 2


def test_self_memory_monitor_writes_peak_record(tmp_path):
    path = tmp_path / "telemetry.json"
    monitor = EXPORT._SelfMemoryMonitor(str(path), "annual_report_summary", 2)
    monitor.start()
    monitor.stop()
    record = json.loads(path.read_text())
    assert record["job_name"] == "export_generation_batch"
    assert record["starting_rss_kb"] >= 0
    assert record["peak_rss_kb"] >= record["starting_rss_kb"]
