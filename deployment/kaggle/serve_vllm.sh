#!/usr/bin/env bash
# Start the vLLM OpenAI-compatible server on Kaggle.
#
# Run this ONLY after model_preflight.py has passed for the same model.
# Preflight loads the model once and reports whether it fits; discovering an
# OOM through a half-started server wastes far more of the weekly quota.
#
#   MODEL=qwen3-14b-awq bash deployment/kaggle/serve_vllm.sh
#
# The server listens on 127.0.0.1:8000 inside the notebook. Kaggle exposes NO
# inbound ports, so nothing outside the notebook can reach it — see
# deployment/kaggle/README.md for what that means and does not mean.
set -euo pipefail

MODEL="${MODEL:-qwen3-14b-awq}"
PORT="${PORT:-8000}"
REPO_DIR="${REPO_DIR:-/kaggle/working/LLM}"
cd "${REPO_DIR}"

# The registry is the single source of T4-safe serving arguments — dtype,
# tensor-parallel size, context length. Reading them from there keeps the
# server, the preflight and the evaluation on one identical configuration.
ARGS="$(python - <<PY
from app.models.registry import get_model_spec
print(" ".join(get_model_spec("${MODEL}").to_server_args()))
PY
)"

echo "Serving ${MODEL} on port ${PORT}"
echo "vllm serve ${ARGS} --port ${PORT} --served-model-name ${MODEL}"
echo ""

# --served-model-name pins the id clients must send, so the evaluation's
# --model value matches what the server answers to.
exec vllm serve ${ARGS} \
  --port "${PORT}" \
  --served-model-name "${MODEL}" \
  --disable-log-requests
