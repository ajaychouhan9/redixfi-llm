"""VM retry worker; --inspect is read-only, --confirm permits GPU/writeback.

Run by the existing scheduler, not a second scheduler or an API background
thread. Accounts/dataset attachments must be supplied in a reviewed JSON
configuration. No credentials are copied into that configuration.
"""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
import sys

PIPELINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE))
from production.retry_dispatch import tick, verify_output
from production.export_generation_batch import ROOT, TASKS
from review_lifecycle import review_lock


def field(obj, name):
    return obj.get(name) if isinstance(obj, dict) else getattr(obj, name, None)


def quota_busy(payload):
    """Kaggle currently returns protobuf durations as seconds/nanos objects.

    The VM's installed SDK incorrectly parses these as timedelta strings.
    Fail closed if the endpoint changes shape instead of assuming free GPU.
    """
    quota = payload.get("gpuQuota", {})
    values = []
    for name in ("timeReserved", "timeUsed", "totalTimeAllowed"):
        duration = quota.get(name)
        if not isinstance(duration, dict) or "seconds" not in duration:
            raise ValueError("GPU quota/availability response incomplete")
        values.append(float(duration["seconds"]) + float(duration.get("nanos", 0)) / 1e9)
    reserved, used, allowed = values
    return reserved > 0 or used >= allowed


class KaggleAdapter:
    def __init__(self, db, task, config):
        self.db, self.task, self.config = db, task, config
        self.owner = config["owner"]
        self.directory = Path(config["work_dir"])
        self.batch_path = self.directory / "batch.json"
        profile = Path(config["profile_dir"])
        os.environ["KAGGLE_CONFIG_DIR"] = str(profile)
        # Existing production authentication pattern; never log the key.
        os.environ["KAGGLE_API_TOKEN"] = json.loads((profile / "kaggle.json").read_text())["key"]
        from kaggle.api.kaggle_api_extended import KaggleApi
        self.api = KaggleApi()
        self.api.authenticate()

    def ref(self, job):
        return self.owner + "/redixfi-retry-" + job["_id"]

    def status_ref(self, ref):
        try:
            raw = field(self.api.kernels_status(ref), "status")
        except Exception as exc:
            if getattr(exc, "status", None) == 404 or getattr(getattr(exc, "response", None), "status_code", None) == 404:
                return "missing"
            raise
        value = str(getattr(raw, "name", raw)).lower().split(".")[-1]
        for known in ("complete", "running", "queued", "error", "cancelled"):
            if value == known:
                return known
        raise ValueError("unknown kernel status")

    def status(self, job):
        return self.status_ref(self.ref(job))

    def account_busy(self):
        import requests
        response = requests.get("https://www.kaggle.com/api/v1/kernels/quota",
            headers={"Authorization": "Bearer " + os.environ["KAGGLE_API_TOKEN"]}, timeout=30)
        response.raise_for_status()
        if quota_busy(response.json()):
            return True
        # Conservatively wait for ANY saved notebook running in this account,
        # including embedding and manually launched production notebooks.
        # A rejected/uncertain push is fenced by the durable launching state.
        page = 1
        while True:
            kernels = self.api.kernels_list(mine=True, page=page, page_size=100)
            for kernel in kernels:
                ref = field(kernel, "ref")
                if not ref:
                    if not field(kernel, "id") and not field(kernel, "slug"):
                        continue  # observed empty SDK placeholder, not a notebook
                    raise ValueError("kernel listing omitted identity")
                if self.status_ref(ref) in ("running", "queued"):
                    return True
            if len(kernels) < 100:
                return False
            page += 1

    def prepare(self, job):
        from scripts.run_production_batch import stage_dataset, push_dataset
        directory = self.directory / job["_id"]
        directory.mkdir(parents=True, exist_ok=True)
        batch_path = directory / "input.json"
        batch_path.write_text(json.dumps(job["batch"], default=str), encoding="utf-8")
        ref = self.ref(job)
        try:
            status = self.api.dataset_status(ref)
        except Exception as exc:
            code = getattr(exc, "status", None) or getattr(getattr(exc, "response", None), "status_code", None)
            if code != 404:
                raise
            stage_dir = directory / "dataset"
            stage_dataset(str(stage_dir), str(batch_path), self.owner, ref.split("/")[1])
            push_dataset(str(stage_dir), self.owner, ref.split("/")[1])
            return False
        if status in ("ready",):
            return True
        if status in ("error", "failed"):
            raise ValueError("Kaggle dataset processing failed")
        return False

    def launch(self, job):
        from scripts.run_production_batch import stage_and_push_kernel
        directory = self.directory / job["_id"]
        stage_and_push_kernel(str(directory / "kernel"), job["batch"]["task"],
                              "input.json", "output.json", self.owner,
                              self.ref(job).split("/")[1], self.owner,
                              self.ref(job).split("/")[1],
                              extra_dataset_sources=self.config["editor_dataset_sources"])

    def collect_and_write(self, job):
        directory = self.directory / job["_id"] / "output"
        path = directory / "output.json"
        if not path.exists():
            self.api.kernels_output(self.ref(job), path=str(directory))
        output = json.loads(path.read_text(encoding="utf-8"))
        verify_output(job["batch"], output)
        name = "annual_report" if self.task == "annual_report" else "concall"
        command = [sys.executable, str(PIPELINE / "production" / ("writeback_" + name + ".py")),
                   "--kaggle-output", str(path)]
        subprocess.run(command, check=True)
        subprocess.run(command + ["--confirm"], check=True)
        # Writers can skip protected rows. Do not report the execution complete
        # while an unresolved selected/writing receipt still needs recovery.
        if self.db.llm_generation_claims.count_documents(
                {"batch_id": job["_id"], "state": {"$in": ["selected", "writing"]}}):
            raise ValueError("batch still has unresolved receipts")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--inspect", action="store_true")
    mode.add_argument("--confirm", action="store_true")
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    sys.path.insert(0, str(ROOT))
    from config.db import get_db
    db = get_db()
    for task, settings in config.items():
        if task not in TASKS.values():
            raise ValueError("retry worker only supports annual_report and concall")
        if args.inspect:
            print(json.dumps({"task": task, "enabled": settings.get("enabled", False),
                "queued": db.llm_review_queue.count_documents({"task": task, "state": "retry_queued"}),
                "jobs": list(db.llm_gpu_dispatch_jobs.find({"task": task}, {"batch": 0}))}, default=str))
        elif settings.get("enabled", False):
            with review_lock("kaggle-account:" + settings["owner"]):
                adapter = KaggleAdapter(db, task, settings)
                print(task, tick(db, task, adapter, datetime.utcnow(), settings.get("limit", 20)))


if __name__ == "__main__":
    main()
