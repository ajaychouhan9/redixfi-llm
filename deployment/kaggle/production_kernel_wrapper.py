"""Template for a per-category Kaggle kernel entry point.

Kaggle's `kernel_type: script` needs one concrete .py file per kernel —
it cannot take CLI arguments at invocation time. So each category gets a
tiny, near-identical wrapper (generated from this template, not hand-
copied) that just locates `production_generate.py` in the attached
dataset and the input batch, then calls it with that category's task
name. vLLM installation is handled INSIDE production_generate.py itself
— this wrapper does nothing else.

Generate one per category with `scripts/stage_production_kernel.py`
rather than editing this file directly.
"""
import glob
import os
import subprocess
import sys

TASK = "{{TASK}}"                    # annual_report_summary | concall_summary | red_flag
INPUT_BASENAME = "{{INPUT_BASENAME}}"  # e.g. prod_batch_ar.json
OUTPUT_BASENAME = "{{OUTPUT_BASENAME}}"  # e.g. prod_output_ar.json

hits = glob.glob("/kaggle/input/**/deployment/kaggle/production_generate.py", recursive=True)
assert hits, "production_generate.py not found under /kaggle/input"
script = hits[0]
input_json = glob.glob(f"/kaggle/input/**/{INPUT_BASENAME}", recursive=True)[0]

cmd = [sys.executable, script, "--task", TASK, "--model", "qwen3-14b-awq-tp2",
       "--input", input_json, "--output", f"/kaggle/working/{OUTPUT_BASENAME}"]
print("RUNNING:", " ".join(cmd), flush=True)
sys.exit(subprocess.run(cmd).returncode)
