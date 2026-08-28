#!/usr/bin/env python3
"""Local development setup check — no GPU, no network, no database.

Verifies the project is ready for offline work and reports honestly on what
is NOT ready. Run it first on a new machine.

    python scripts/local_setup.py
"""
from __future__ import annotations

import importlib
import importlib.util
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

CORE = ["fastapi", "uvicorn", "pydantic"]
VM_ONLY = ["pymongo", "chromadb", "tiktoken"]
GPU_ONLY = ["torch", "vllm"]


def check(label: str, ok: bool, detail: str = "") -> bool:
    print(f"  [{'OK ' if ok else 'MISS'}] {label}{('  — ' + detail) if detail else ''}")
    return ok


def main() -> None:
    print("=" * 72)
    print("LOCAL SETUP CHECK — RedixFi self-hosted LLM (EXPERIMENTAL)")
    print("=" * 72)

    print(f"\nPython: {sys.version.split()[0]}  ({sys.executable})")
    if sys.version_info < (3, 10):
        print("  ! Python 3.10+ required")

    print("\n--- Core dependencies (needed for offline work) ---")
    core_ok = all(
        check(name, importlib.util.find_spec(name) is not None) for name in CORE
    )

    print("\n--- VM export dependencies (only needed on the RedixFi VM) ---")
    for name in VM_ONLY:
        check(name, importlib.util.find_spec(name) is not None,
              "install only where you run export_fixtures.py")

    print("\n--- GPU dependencies (Kaggle only — do NOT install locally) ---")
    for name in GPU_ONLY:
        present = importlib.util.find_spec(name) is not None
        check(name, present, "expected absent on a dev machine" if not present else "")

    print("\n--- Project imports ---")
    imports_ok = True
    for module in (
        "app.config.settings", "app.models.registry", "app.inference.factory",
        "app.tasks.annual_report_summary", "app.tasks.red_flag", "app.tasks.ask_ai",
        "app.evaluation.runner", "app.compliance.validators",
    ):
        try:
            importlib.import_module(module)
            check(module, True)
        except Exception as exc:
            imports_ok = check(module, False, str(exc)) and imports_ok

    print("\n--- Configuration ---")
    env_path = os.path.join(ROOT, ".env")
    check(".env.example present", os.path.exists(os.path.join(ROOT, ".env.example")))
    if os.path.exists(env_path):
        check(".env present", True, "git-ignored, never commit it")
    else:
        print("  [INFO] no .env — defaults apply (LLM_BACKEND=echo). "
              "Copy .env.example to .env to override.")

    print("\n--- RedixFi checkout (for the prompt drift guard) ---")
    redixfi = os.getenv("REDIXFI_ROOT_LOCAL", r"C:\Redixfi")
    if os.path.isdir(redixfi):
        check(f"found at {redixfi}", True)
        try:
            out = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                                 cwd=redixfi, capture_output=True, text=True, timeout=10)
            head = out.stdout.strip()
            print(f"         HEAD {head} (prompts were vendored at 8bb3170)")
            if head and head != "8bb3170":
                print("         ! RedixFi has moved since the vendoring — the drift "
                      "guard will tell you whether it matters.")
        except Exception:
            pass
    else:
        print(f"  [INFO] not found at {redixfi} — the drift guard will skip. "
              "Set REDIXFI_ROOT_LOCAL if your checkout is elsewhere.")

    print("\n--- Sample fixtures ---")
    fixtures_dir = os.path.join(ROOT, "fixtures")
    samples = [f for f in os.listdir(fixtures_dir) if f.startswith("sample_")] \
        if os.path.isdir(fixtures_dir) else []
    if samples:
        check(f"{len(samples)} synthetic sample fixture(s)", True, ", ".join(samples))
    else:
        print("  [INFO] none yet — run: python scripts/make_sample_fixtures.py")

    print("\n" + "=" * 72)
    if core_ok and imports_ok:
        print("READY for offline work. Next:")
        print("  python scripts/make_sample_fixtures.py")
        print("  python scripts/run_evaluation.py --fixture fixtures/sample_ask_ai.json --backend echo")
        print("  python -m pytest")
        print("\nNo GPU quota and no production read is needed for any of that.")
    else:
        print("NOT READY. Install core dependencies:")
        print("  pip install -r requirements-dev.txt")
    print("=" * 72)


if __name__ == "__main__":
    main()
