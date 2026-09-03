"""Push an AR/concall embedding kernel to Kaggle, pinned to a real T4.

Reads a staged kernel directory (kernel-metadata.json + the script named
in its code_file) and pushes it with GPU enabled AND machine_shape forced
to a real Tesla T4 - see WHY THE T4 PIN IS REQUIRED below. This is the
GPU-launch step: staging (export_embed_batch.py, a dataset push) is not
gated, but running this script is, and should only happen on the
founder's explicit go-ahead per this project's standing rule.

Usage:
    export KAGGLE_CONFIG_DIR=/home/ubuntu/.kaggle_profiles/annual_report
    export KAGGLE_API_TOKEN=$(python3 -c 'import json;print(json.load(open("/home/ubuntu/.kaggle_profiles/annual_report/kaggle.json"))["key"])')
    python3 push_embed_kernel.py [/path/to/staged/kernel/dir]

WHY THE T4 PIN IS REQUIRED (2026-09-03, found via a real failed run)
----------------------------------------------------------------------
The first version of this script did not set machine_shape, on the
reasoning "single-GPU model, no override needed like the 2xT4 generation
kernels." That reasoning was wrong. Without an explicit machine_shape,
Kaggle assigns from its generic single-GPU pool, which is NOT guaranteed
to be a T4 - confirmed live via the kernel's own post-run metadata
(`machineShape: 'Gpu'`) and its log (`Found GPU0 Tesla P100-PCIE-16GB ...
sm_60 ... not compatible with the current PyTorch installation`). A real
100-document, 42,180-chunk batch ran with every single chunk failing
`CUDA error: no kernel image is available for execution on the device` -
the installed PyTorch build has no compiled kernels for Pascal (sm_60),
only for what the T4 (sm_75) needs, which is what every embedding
preflight this project has run on (12.19 chunks/sec, measured). The kernel
still reached Kaggle status COMPLETE (the script caught each batch's
exception and kept going) but embedded 0 of 42,180 chunks - real GPU time
spent for zero result, invisible unless the kernel's own OUTPUT is
checked, not just its Kaggle status.

Same class of gotcha push_kernel_2xt4.py already documents for the 2xT4
generation kernels - KaggleApi.kernels_push()'s high-level wrapper does
not expose machine_shape at all, so it must be forced via the low-level
ApiSaveKernelRequest, same mechanism, just pinned to a single T4 here
rather than 2.
"""
import json
import os
import sys

from kaggle.api.kaggle_api_extended import KaggleApi
from kagglesdk.kernels.types.kernels_api_service import ApiSaveKernelRequest

KERNEL_DIR = sys.argv[1] if len(sys.argv) > 1 else "/home/ubuntu/embed_kernel"

api = KaggleApi()
api.authenticate()

meta = json.load(open(os.path.join(KERNEL_DIR, "kernel-metadata.json")))
script_body = open(os.path.join(KERNEL_DIR, meta["code_file"]), encoding="utf-8").read()

with api.build_kaggle_client() as kaggle:
    request = ApiSaveKernelRequest()
    request.slug = meta["id"]
    request.new_title = meta["title"]
    request.text = script_body
    request.language = meta["language"]
    request.kernel_type = meta["kernel_type"]
    request.is_private = meta["is_private"]
    request.enable_gpu = meta["enable_gpu"]
    request.enable_internet = meta["enable_internet"]
    request.dataset_data_sources = meta["dataset_sources"]
    # THE FIX: force a real T4 (sm_75), known-good on this project (the
    # v1/v2/v3 embedding preflights all measured 12.19 chunks/sec on a real
    # T4 this same session). Without this, Kaggle's generic "Gpu" pool can
    # hand out a P100 (sm_60) instead, which the installed torch build
    # cannot run at all - confirmed live, not hypothetical.
    request.machine_shape = "NvidiaTeslaT4"
    resp = kaggle.kernels.kernels_api_client.save_kernel(request)
    print("PUSHED:", getattr(resp, "url", None) or getattr(resp, "ref", None))
    print("Poll with: kaggle kernels status", meta["id"])
    print("Fetch output with: kaggle kernels output", meta["id"], "-p /home/ubuntu/embed_output")
