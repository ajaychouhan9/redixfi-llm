#!/usr/bin/env bash
# Kaggle GPU environment bootstrap.
#
# RUN THIS IN A KAGGLE NOTEBOOK CELL WITH:
#   Accelerator = GPU T4 x2
#   Internet    = ON   (required: pip + Hugging Face weight download)
#
# Kaggle is EPHEMERAL. Nothing here persists: not the repo, not the weights,
# not the venv, not the IP. Every session re-runs this script from scratch,
# which is precisely why it exists as a script rather than as instructions.
#
# GPU quota is ~30 h/week. This script does NOT load a model — it only
# prepares the environment. Loading happens in model_preflight.py so that a
# failed setup costs seconds, not a model download.
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/ajaychouhan9/redixfi-llm.git}"
REPO_DIR="${REPO_DIR:-/kaggle/working/LLM}"
BRANCH="${BRANCH:-main}"

echo "=============================================================="
echo " RedixFi self-hosted LLM — Kaggle bootstrap (EXPERIMENTAL)"
echo "=============================================================="

# ---------------------------------------------------------------------------
# 1. Hardware check FIRST — fail before spending time on anything else.
# ---------------------------------------------------------------------------
echo ""
echo "--- GPU ---"
nvidia-smi --query-gpu=index,name,memory.total,compute_cap --format=csv || {
  echo "FATAL: no GPU. Set Accelerator = GPU T4 x2 in the notebook settings."
  exit 1
}

GPU_COUNT="$(nvidia-smi --list-gpus | wc -l)"
echo ""
echo "GPU count: ${GPU_COUNT}"
if [ "${GPU_COUNT}" -lt 2 ]; then
  echo "WARNING: fewer than 2 GPUs. qwen3-14b-awq (TP=1) still works;"
  echo "         qwen3-30b-a3b-awq (TP=2) will NOT."
fi

# ---------------------------------------------------------------------------
# 2. Code.
# ---------------------------------------------------------------------------
echo ""
echo "--- Repository ---"
if [ -d "${REPO_DIR}/.git" ]; then
  git -C "${REPO_DIR}" fetch --depth 1 origin "${BRANCH}"
  git -C "${REPO_DIR}" reset --hard "origin/${BRANCH}"
else
  git clone --depth 1 --branch "${BRANCH}" "${REPO_URL}" "${REPO_DIR}"
fi
cd "${REPO_DIR}"
echo "Commit: $(git rev-parse --short HEAD)"

# ---------------------------------------------------------------------------
# 3. Dependencies.
#
# Deliberately NOT reinstalling torch. Kaggle ships torch built against the
# image's exact CUDA; replacing it is the single most reliable way to waste a
# GPU session rebuilding wheels. vLLM resolves against what is already there.
# ---------------------------------------------------------------------------
echo ""
echo "--- Dependencies ---"
pip install -q --no-cache-dir vllm
pip install -q --no-cache-dir fastapi "uvicorn[standard]" pydantic

python - <<'PY'
import torch
print(f"torch  : {torch.__version__}  CUDA {torch.version.cuda}")
for i in range(torch.cuda.device_count()):
    p = torch.cuda.get_device_properties(i)
    print(f"  [{i}] {p.name}  {p.total_memory / 1024**3:.1f} GB  SM{p.major}.{p.minor}"
          f"  bf16={'yes' if p.major >= 8 else 'NO (Turing)'}")
try:
    import vllm
    print(f"vllm   : {vllm.__version__}")
except Exception as exc:
    print(f"vllm   : IMPORT FAILED — {exc}")
PY

# ---------------------------------------------------------------------------
# 4. Secrets — from Kaggle Secrets, never from a file in the repo.
# ---------------------------------------------------------------------------
echo ""
echo "--- Secrets ---"
python - <<'PY'
import os
try:
    from kaggle_secrets import UserSecretsClient
    client = UserSecretsClient()
    for name in ("HF_TOKEN",):
        try:
            os.environ[name] = client.get_secret(name)
            print(f"  {name}: loaded from Kaggle Secrets")
        except Exception:
            print(f"  {name}: not set (fine unless the weights are gated)")
except ImportError:
    print("  kaggle_secrets unavailable — not running on Kaggle?")
PY

echo ""
echo "=============================================================="
echo " Setup complete. NO model has been loaded and NO GPU time spent"
echo " on inference yet."
echo ""
echo " Next:"
echo "   cd ${REPO_DIR}"
echo "   python scripts/model_preflight.py --model qwen3-14b-awq --json preflight.json"
echo ""
echo " Start with qwen3-14b-awq. Attempt the 30B only after the 14B works."
echo "=============================================================="
