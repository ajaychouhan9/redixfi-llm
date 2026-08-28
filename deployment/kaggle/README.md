# Kaggle deployment

**EXPERIMENTAL. Nothing here is wired into RedixFi production.**

Do not start a GPU session until the founder says to deploy. Everything in
this project up to that point runs locally with no GPU quota spent.

## What Kaggle actually gives you

| | |
|---|---|
| GPU | 2 × NVIDIA T4, 16 GB each (32 GB total) |
| Architecture | Turing, SM75 — **no bf16, no FP8, no FlashAttention-2** |
| Quota | ~30 GPU-hours/week, per account |
| Session | ~9 h max, killed on idle. **Everything is wiped.** |
| Networking | Outbound only (with Internet ON). **No inbound ports.** |

The last row matters more than it looks. A Kaggle notebook **cannot be
reached from the internet**, so the vLLM server it runs is reachable only
from inside that notebook. That is why the evaluation runs *inside* the
notebook against `127.0.0.1:8000` rather than exposing an endpoint.

It is also why fixtures, not database connections, carry the data: RedixFi's
MongoDB is loopback-bound on its own VM and its ChromaDB is a local
directory, so nothing on Kaggle could reach either even if we wanted it to.

## Prerequisites

1. Fixtures exported from the RedixFi VM (`scripts/export_fixtures.py`),
   uploaded as a **private** Kaggle Dataset.
2. Kaggle notebook settings: **Accelerator = GPU T4 ×2**, **Internet = ON**.
3. Optional Kaggle Secret `HF_TOKEN`, only if the weights are gated.

> Fixtures can contain full annual-report text and real user questions from
> `ask_log`. Upload the dataset as **private**. Never make it public.

## Procedure

### Step 1 — bootstrap (~3 min, no model loaded)

```python
!bash /kaggle/working/LLM/deployment/kaggle/kaggle_setup.sh
```

Or, before the repo exists:

```python
!git clone --depth 1 https://github.com/<you>/redixfi-llm.git /kaggle/working/LLM
!bash /kaggle/working/LLM/deployment/kaggle/kaggle_setup.sh
```

Confirm the output shows 2 GPUs and `bf16=NO (Turing)`. That line is
expected — it is why the registry pins `--dtype float16`.

### Step 2 — preflight (~5–10 min, the first real GPU spend)

```python
%cd /kaggle/working/LLM
!python scripts/model_preflight.py --model qwen3-14b-awq --json preflight_14b.json
```

Read the VERDICT block.

- **PASS** → continue to step 3.
- **FAIL** → the exact error is recorded verbatim in `preflight_14b.json`.
  Follow the printed OOM ladder (reduce `--max-model-len`, lower
  `--gpu-memory-utilization`, try TP=2). **Do not switch models silently** —
  that is a decision to make with the error in hand.

Only attempt the 30B **after** the 14B passes:

```python
!python scripts/model_preflight.py --model qwen3-30b-a3b-awq --json preflight_30b.json
```

Expect this to be the risky one. Qwen3-30B-A3B is MoE, and quantized-MoE
kernels on Turing are the weakest-supported combination in vLLM. A clean
failure here, recorded, is a legitimate and useful result.

### Step 3 — serve, and which model each phase needs

**Measured, not assumed.** RedixFi's Evidence Finder builds annual-report
evidence under a 20,000-token budget. Run against real reports (ABB, TCS,
RELIANCE), a Phase A prompt measures **~23,600 tokens**, needing **~24,600**
once the completion budget is added.

| Phase | Prompt size | Model to serve | Why |
|---|---|---|---|
| A — Annual Report | ~24,600 | **`qwen3-14b-awq-tp2`** | 16k does not fit; TP=2 gives 32k |
| B — Red Flag | ~1,000 | `qwen3-14b-awq` | one chunk per call |
| C — Ask AI | ~6,000 | `qwen3-14b-awq` | packet budget caps at 6k |

`scripts/run_evaluation.py` checks this before generating anything and
**aborts rather than burning quota** on requests the server would reject.

Serve B and C first (they share one model), then restart for A:

```python
import subprocess, os
os.environ["MODEL"] = "qwen3-14b-awq"      # phases B and C
server = subprocess.Popen(
    ["bash", "deployment/kaggle/serve_vllm.sh"],
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
)
```

Wait for `Application startup complete`, then check:

```python
!curl -s http://127.0.0.1:8000/v1/models
```

### Step 4 — evaluate

```python
%env LLM_BACKEND=vllm
%env VLLM_BASE_URL=http://127.0.0.1:8000/v1

# Phases B and C against the currently-served qwen3-14b-awq
!python scripts/run_evaluation.py \
    --fixture /kaggle/input/redixfi-llm-fixtures/red_flag.json \
    --model qwen3-14b-awq --backend vllm

!python scripts/run_evaluation.py \
    --fixture /kaggle/input/redixfi-llm-fixtures/ask_ai.json \
    --model qwen3-14b-awq --backend vllm
```

Then stop the server and restart it on the TP=2 variant for Phase A:

```python
server.terminate(); server.wait()
os.environ["MODEL"] = "qwen3-14b-awq-tp2"
server = subprocess.Popen(
    ["bash", "deployment/kaggle/serve_vllm.sh"],
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
)
# wait for startup, then:
!python scripts/run_evaluation.py \
    --fixture /kaggle/input/redixfi-llm-fixtures/annual_report_summary.json \
    --model qwen3-14b-awq-tp2 --backend vllm
```

### Step 5 — get the results out before the session dies

```python
!cd /kaggle/working/LLM && zip -r /kaggle/working/eval_results.zip evaluation/ preflight_*.json
```

Download `eval_results.zip` from the notebook's Output panel. **A session
that ends without this step loses every result**, and the GPU hours with it.

## Expected quota cost

| Step | GPU time |
|---|---|
| Bootstrap | ~0 (no model loaded) |
| 14B preflight | ~10 min incl. weight download |
| 30B preflight | ~20 min, or fails fast |
| Serve + 3 evaluation phases (~120 cases) | ~30–60 min |
| **Total for one full pass** | **~1–1.5 h of a ~30 h weekly budget** |

## Recovery

| Symptom | Cause | Action |
|---|---|---|
| `CUDA out of memory` on load | KV cache, usually not weights | Halve `--max-model-len`; drop utilisation to 0.85 |
| `bfloat16 is not supported` | dtype leaked through | The registry pins float16 — check nothing overrode it |
| MoE kernel / `unsupported` error on 30B | Turing + quantized MoE | Record it. This is the expected failure mode. Stay on 14B |
| Weight download stalls | Internet off, or gated repo | Turn Internet ON; add the `HF_TOKEN` secret |
| Server never becomes ready | Load failed silently | Read the captured `server.stdout` |
| Session died mid-run | Idle timeout / 9 h cap | Re-run from step 1. Results are only kept if step 5 ran |
