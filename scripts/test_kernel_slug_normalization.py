"""Regression test for the 2026-09-08 overnight loss.

Kaggle normalizes a pushed kernel slug (underscores -> hyphens) but keeps
the title verbatim. The scheduler built its slug from the phase name
(embed_ar), so the push created redixfi-prod-embed-ar-daily while every
later status/output call used redixfi-prod-embed_ar-daily -> 403 Forbidden
on ListKernelSessionOutput. All five phases ran to completion on Kaggle and
every output was discarded: real GPU time spent, zero writeback, no
production data changed.

Asserts (a) the normalizer is correct for every real phase, (b) the
caller-side slug builder in the backend repo agrees with it, and (c) the
launcher structurally cannot re-derive a different ref for poll/retrieve.

Run: python scripts/test_kernel_slug_normalization.py
"""
from __future__ import annotations

import importlib.util
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from launch_staged_kaggle_batch import normalize_kernel_slug

FAIL = []


def check(label, cond, detail=""):
    print("[%s] %s" % ("PASS" if cond else "FAIL", label))
    if not cond:
        FAIL.append("%s - %s" % (label, detail))


PHASES = ["embed_ar", "embed_cc", "generate_ar", "generate_cc", "reclassify_rf"]

# (a) the normalizer itself
for phase in PHASES:
    slug = normalize_kernel_slug("redixfi-prod-%s-daily" % phase)
    check("normalized slug for %s has no underscore (%s)" % (phase, slug),
          "_" not in slug, slug)

check("the exact failing ref from last night normalizes to the ref that worked",
      normalize_kernel_slug("redixfi-prod-embed_ar-daily") == "redixfi-prod-embed-ar-daily",
      normalize_kernel_slug("redixfi-prod-embed_ar-daily"))
check("an already-correct slug is unchanged (idempotent)",
      normalize_kernel_slug("redixfi-prod-embed-ar-daily") == "redixfi-prod-embed-ar-daily")

# (b) the caller side, read from the real backend file so the two repos
# cannot drift apart silently
root = Path(os.getenv("REDIXFI_ROOT", "/home/ubuntu/redixfi-backend"))
stage_path = root / "data-pipeline" / "kaggle_daily_stage.py"
if stage_path.is_file():
    spec = importlib.util.spec_from_file_location("kds", stage_path)
    kds = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kds)
    for phase in PHASES:
        built = kds.kernel_slug_for_phase(phase)
        check("caller builds an already-normalized slug for %s (%s)" % (phase, built),
              "_" not in built and built == normalize_kernel_slug(built), built)
    check("caller and launcher agree on every phase",
          all(kds.kernel_slug_for_phase(p) == normalize_kernel_slug(
              "redixfi-prod-%s-daily" % p) for p in PHASES))
else:
    check("backend kaggle_daily_stage.py reachable for cross-repo check", False,
          "not found at %s (run this on the VM for the full check)" % stage_path)

# (c) structural guard: nothing after normalization may use args.kernel_slug
src = (Path(__file__).resolve().parent / "launch_staged_kaggle_batch.py").read_text(encoding="utf-8")
main_body = src.split("def main()", 1)[1]
after_norm = main_body.split("kernel_slug = normalize_kernel_slug", 1)[1]
check("push/poll/retrieve never re-read args.kernel_slug after normalizing",
      "args.kernel_slug" not in after_norm.split("return 0")[0],
      "found a raw args.kernel_slug use after normalization")
check("poll_and_retrieve is called with the normalized slug",
      re.search(r"poll_and_retrieve\(\s*args\.dataset_owner,\s*kernel_slug", main_body) is not None)

print()
if FAIL:
    print("%d FAILURE(S): %s" % (len(FAIL), FAIL))
    sys.exit(1)
print("All checks passed.")
