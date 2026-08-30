# Self-improvement mechanism — investigation and recommendation

**EXPERIMENTAL / NOT PRODUCTION.** No production-readiness declaration.
The founder decides whether/how to act on this.

**The question:** manual prompt tuning this session showed diminishing
returns — content steering backfired (likely negation priming), and
red_flag's instance-check fix traded 7 false positives for 26 new false
negatives. Is there a mechanism that lets this system improve from real
outcomes instead of another hand-tuned round each time a gap is found?

---

## Option A — Retrieval-augmented few-shot example bank

### 1. What already exists that this could reuse

Checked before building anything:

- **This project's own `jaccard()`** (`app/evaluation/compare.py`) — a
  tested, zero-dependency word-set-overlap similarity function, already
  used as the lexical-overlap triage signal in every review sheet.
- **RedixFi's production pattern**, confirmed in `00_MASTER_CONTEXT.md`'s
  Annual Report RAG work: a real embedding call
  (`text-embedding-3-small`, ~$0.07 measured, ~203s for the reference
  spike). This is the right choice at production retrieval scale — precise
  semantic matching over thousands of chunks — but it is a paid, network-
  dependent OpenAI call, and using it here for a ~20-entry concept test
  would be over-building for what needed proving first.
- **`RedixFiChromaReader`** (`app/integrations/redixfi_readonly.py`) — a
  read-only ChromaDB accessor for RedixFi's production vector store. Not
  used: it is explicitly read-only, points at production data this
  project must not write to, and this bank is Qwen's own accumulating
  behaviour, not a copy of RedixFi's document corpus.

**Decision:** reuse `jaccard()` for retrieval. It costs nothing per
query, needs no new dependency, and is already proven correct in this
codebase. If retrieval quality becomes the limiting factor once the bank
is larger, swapping in a real embedding call is a contained change —
everything downstream of `retrieve()` is metric-agnostic by design.

### 2. Concrete design (implemented)

- **Storage:** `app/example_bank.py` — one JSON file per task under
  `example_bank/` (e.g. `example_bank/concall_summary.json`), a plain
  list of entries: `benchmark_id`, `added_at`, `run_id`, `model`,
  `attempts_used`, `was_hard_case` (attempts > 1), a short
  `retrieval_text` built for matching (company/symbol/doc_kind + an
  800-character topical slice — not the full transcript, so document
  boilerplate doesn't dominate the similarity score), and the validated
  `output`.
- **Eligibility:** only `TaskResult.ok is True` outputs are ever stored —
  the SAME pass/fail gate the task's real validator already applies.
  Nothing here re-judges quality.
- **Retrieval:** `retrieve(entries, query_text, k=2, exclude_benchmark_id)`
  — top-k by jaccard similarity, always excluding the current case's own
  id. Confirmed empirically (not assumed) that self-exclusion holds for
  all 20 concall cases and that retrieval genuinely varies per case (not
  a degenerate fixed top-2).
- **Prompt injection:** `app/prompts/concall_summary_fewshot_bank.py` —
  the SYSTEM prompt is production, byte-identical, unmodified. Retrieved
  examples are prepended to the USER message only, as positive
  demonstrations with no forbidden vocabulary named anywhere — a
  deliberate contrast with every other prompt change tried this session
  (markdown ban, steering, instance-check), all of which added new rules
  or named forbidden words in the system prompt.

### 3. Cost/complexity — actually cheap, confirmed not estimated

No training. No new dependency (jaccard already existed). No new
infrastructure beyond a `Variant.user_content_fn` hook (one new optional
field, defaulting to `None` so every existing variant is unaffected).
GPU cost is the same as any other concall variant run — dominated by
generation, not retrieval (jaccard over 20 entries is sub-millisecond).
**This did not need scaling down; the minimal design was sufficient.**

### 4. Implementation and test

Bootstrapped the bank from the retries8 run (the most recent fully-
validated concall run): **20/20 real entries, 6 flagged as hard cases**
(needed >1 attempt: KANPRPLA, SDBL, PNB, MANYAVAR, UNIMECH, KIRIINDUS —
one more than the 5 named in the brief, UNIMECH, also genuinely marginal
at 2 attempts).

GPU test: full 20-case `concall_benchmark.json`, production SYSTEM
prompt (unmodified), IMPROVED retry policy (already committed), but
tested at **production's 3-attempt budget, not 8** — deliberately, so any
effect is attributable to retrieval alone and not layered with the
already-separately-tested budget increase.

### 5. Result — no net change in generation count; a real but small effect underneath it

| | Generated | Compliance fails | Tone agreement |
|---|---|---|---|
| retry fix, 3 attempts, **no** few-shot | 17/20 | 3 | 0.7059 |
| retry fix, 3 attempts, **with** few-shot | **17/20** | **3** | 0.7647 |

**The exact same 3 cases fail, identically, in both runs**
(CC_ALKYLAMINE, CC_KIRIINDUS, CC_SDBL). At the level of final pass/fail,
few-shot changed nothing.

**But the mechanism demonstrably engaged, not a no-op or a silent
fallback to baseline** — confirmed from raw generated text, not assumed:
attempt-1 text on the 3 persistently-failing cases differs substantially
between the two runs (similarity 0.069–0.39, never 1.000), so the
retrieved examples reached the model and changed its output; they just
didn't change which forbidden-vocabulary category it reached for.

**Attempts-needed shifted on 5 of 20 cases**, netting to zero on the
final count:

| Case | Baseline attempts | With few-shot | |
|---|---|---|---|
| CC_MANYAVAR | 2 | **1** | fewer needed |
| CC_PNB | 2 | **1** | fewer needed |
| CC_UNIMECH | 2 | **1** | fewer needed |
| CC_EMAMILTD | 1 | **3** | more needed (still passed) |
| CC_SIGACHI | 2 | **3** | more needed (still passed) |

The three cases that needed FEWER attempts are exactly three of the
bank's own six "hard case" entries — plausible, though not provable at
n=1, that seeing a real example of a previously-hard case resolved
compliantly helped a structurally similar case land faster. The two
cases that needed MORE attempts were previously-easy cases, a small
possible cost of the added prompt length/distraction. Both effects are
small (one attempt in either direction) and this is a single run.

**Plain interpretation, per this project's noise-floor discipline:**
this is genuinely **inconclusive at n=20, one run** — not a confirmed
win, not a confirmed no-op. It is a materially different result from
every hand-written prompt change tried this session: it neither closed
a gap outright (unlike the retry-budget fix) nor caused a regression
(unlike steering and the red_flag instance-check). The interesting
signal is the attempts-needed reshuffling, which a single run cannot
distinguish from chance. **This is exactly the situation the mechanism
is meant for**: it costs nothing to keep running as the bank grows, and
whether the reshuffling effect is real becomes answerable with more
data, not more manual tuning.

---

## Option B — Actual model fine-tuning (QLoRA/LoRA)

### 1. VRAM requirements — real published figures, not estimated

Sourced from [Spheron's 2026 GPU VRAM sizing guide](https://www.spheron.network/blog/gpu-vram-requirements-fine-tune-llm-2026/)
and cross-checked against general QLoRA literature:

| Model size | QLoRA total VRAM (batch=1, seq_len=512, rank=64) |
|---|---|
| 7B | ~8 GB |
| **13-14B** | **~14 GB** (base 4-bit NF4: 7 GB, adapters BF16: 0.4 GB, gradients: 0.4 GB, optimizer: 0.8 GB, activations: 5 GB) |
| 30B MoE (Qwen3-30B-A3B class) | ~21 GB |

The source explicitly adds 15-20% headroom for real training runs, and
recommends a 32 GB card (RTX 5090) as the practical minimum for 14B —
**not** a 14.56 GB T4, even before this project's own workload is
considered.

**The critical, decisive problem: sequence length.** The 14 GB figure
above assumes **sequence length 512**. This project's actual concall
input is up to ~19,308 tokens; annual_report's current pipeline is
~16,291 tokens (the legacy replay is 38,792–62,456). That is **30-40x
longer** than the benchmark figure. Activation memory during training
scales with sequence length — even generously assuming gradient
checkpointing buys a 5x reduction (a large assumption; typical published
figures are closer to 2-3x for transformer activations), a 30-40x longer
sequence overwhelms any plausible saving. The realistic conclusion:
**training at this project's actual sequence lengths does not fit
in 14.56 GB per card, and very likely not in 29.12 GB combined either**,
without a training-specific engineering effort (sequence packing,
aggressive gradient checkpointing, FlashAttention-style memory-efficient
attention — none of which T4/Turing supports well; FlashAttention-2
needs Ampere+, already noted as unavailable on this hardware for
inference in `app/models/registry.py`) well beyond what this
investigation is scoped to attempt.

### 2. bf16 — T4 cannot run the standard recipe

[Confirmed](https://medium.com/@aminfadaeinejad.edu/fine-tuning-an-llm-with-lora-and-qlora-a-hands-on-guide-441ea09360c5):
QLoRA's standard recipe trains LoRA adapters in bf16. **Turing (T4) has
no bf16 datapath** — the same constraint already documented in this
project's inference registry (`app/models/registry.py`: "NO bfloat16.
Turing has no bf16 datapath"). The fp16 workaround exists and is used by
some tooling (Unsloth auto-detects and switches), but fp16 training is
well-documented as less numerically stable than bf16 for LLM fine-tuning
(narrower dynamic range, more prone to loss-scaling overflow) — this is a
real execution risk layered on top of the memory problem, not just a
config flag flip.

### 3. Base checkpoint and tooling

Contrary to an initial assumption in this investigation (corrected after
checking): QLoRA **can** train LoRA adapters on top of an already-
quantized base — the base is frozen either way, so starting from
`Qwen/Qwen3-14B-AWQ` (already deployed for inference) rather than
re-downloading a fresh bf16 checkpoint is not itself blocked. However,
mainstream PEFT/bitsandbytes tooling is built around bitsandbytes NF4
quantization specifically; AWQ-base LoRA training is less standard and
would need its own verification, on top of every other blocker below.

This project's dependencies (`requirements.txt`, `requirements-gpu.txt`)
currently center on vLLM for inference only. Training would need
`transformers` + `peft` + `bitsandbytes` (or an AWQ-specific adapter-
training path) + a training loop (`trl` or hand-rolled) — a materially
different toolchain, untested in this project, with its own installation
and compatibility risk on top of the hardware questions above.

### 4. GPU-hour budget

Kaggle's free tier is ~30 GPU-hours/week, shared across everything this
project already does with it. Cumulative spend to date across all
sessions: **~271.5 + ~50 minutes (this session, once totalled below) ≈
5.4 GPU-hours**. A meaningful QLoRA run — even a small one, before
considering whether it fits VRAM at all — typically needs multiple
epochs and, on T4-class compute with fp16's instability risk, likely
several debugging/retry cycles. This would compete directly with the
eval and production-backfill work this budget already needs to cover.

### 5. Data volume — insufficient regardless of hardware

Independent of every hardware question above: the example bank currently
holds **20 real validated concall examples** (from a single fixture's
worth of coverage — 20 of the ~4,157 real investor-call documents
RedixFi's production has processed). Fine-tuning a 14B model on 20
examples is far below any reasonable threshold for a meaningful effect —
LoRA fine-tuning literature generally expects hundreds to low thousands
of instruction examples before an effect is distinguishable from noise or
overfitting, even accounting for LoRA's lower sample-complexity relative
to full fine-tuning. **This alone rules out Option B today, independent
of the VRAM/bf16/tooling problems.**

### 6. Conclusion — plain, not hedged

**Option B is not feasible now.** Four independent reasons, any one of
which is sufficient on its own:

1. **VRAM.** Even the toy benchmark figure (14 GB at seq_len=512)
   exceeds a single T4's 14.56 GB once realistic headroom is added, and
   this project's real sequence lengths (16k-19k tokens) are 30-40x
   longer than that benchmark — activation memory does not survive that
   scaling on this hardware.
2. **bf16.** T4 cannot run the standard QLoRA recipe's dtype; the fp16
   workaround is a real numerical-stability risk, not a drop-in swap.
3. **Tooling.** No training infrastructure exists in this project today;
   building it (transformers+peft+bitsandbytes, sequence-length handling,
   likely distributed training across both T4s via DeepSpeed/FSDP to even
   attempt combining VRAM) is a substantial new engineering effort, not a
   config change.
4. **Data.** 20 real examples is far short of what would make a LoRA
   fine-tune meaningful, independent of whether the hardware could run it.

**Recommend revisiting when BOTH of the following hold, not either
alone:** (a) Option A has been running long enough to accumulate a real
corpus of at least several hundred validated examples per task category,
and (b) better hardware is available — specifically, Ampere-or-newer GPUs
with native bf16 and enough VRAM per card to hold this project's actual
sequence lengths during training (a rough floor, given the 30-40x
sequence-length multiplier found above, would be a card class with at
least 40-48 GB, not the 24-32 GB the toy-scale benchmark alone would
suggest). Until then, this is a clean "not now," not an ambiguous "maybe."

---

## What accumulates automatically, and what doesn't — read before relying on this

`app/evaluation/runner.py::run_evaluation()` — the STANDARD path used for
a normal production-shape eval run — records every real (non-echo)
`ok=True` result to the bank automatically. This is deliberate and
sufficient for the mechanism's intended use: whenever concall (or
annual_report or red_flag) is run normally, the bank grows on its own,
no manual step required.

**This session's GPU test did NOT go through that path.** It ran via
`app/experiments/concall_variants.py::run_variant_evaluation()` — the
harness built for one-off comparison tests, which does not auto-record.
This is also deliberate, not an oversight: a variant run is testing a
hypothesis (a different prompt, a different retry policy), and its
outputs should not silently become "validated examples" without a human
deciding they're worth keeping — unlike a normal run, whose whole point
is to reflect production-shape behaviour. If the founder wants this
run's 17 successes folded into the bank, that's one command:

    python scripts/bootstrap_example_bank.py \
        --run evaluation/concall/runs/concall_summary__fewshot_bank__qwen3-14b-awq-tp2__20260830T060722Z.json \
        --task concall_summary

Not run here, so the current bank still reflects only the retries8
bootstrap (20 entries, 6 flagged hard) — a deliberate choice to keep
"what's in the bank" traceable to one clear decision rather than
silently absorbing every experimental variant this project runs.

## How this keeps accumulating, going forward

1. Every normal (non-variant, non-echo) concall/annual_report/red_flag
   evaluation run — on Kaggle or locally — writes its `ok=True` results
   into `example_bank/<task>.json` automatically via the runner hook.
2. Kaggle is ephemeral: nothing survives the session. The bank file must
   be downloaded from the kernel's output and merged back into the repo
   the same way run artifacts already are (`git add example_bank/`,
   commit, and the NEXT dataset push carries the updated bank forward).
3. A deliberate experimental variant's results are NOT auto-included —
   run `scripts/bootstrap_example_bank.py` explicitly if a variant run's
   outputs should be treated as validated examples going forward.
4. Retrieval quality is worth re-examining once the bank is meaningfully
   larger (see the negation-priming style risk that recurred this
   session — a growing bank with mixed-quality examples could plausibly
   need curation, not just accumulation). Not a concern yet at 20 entries.

## GPU cost

| Phase | Time |
|---|---|
| Concall fewshot-bank test (20 cases, 3-attempt budget) | 22.4 min generation |
| Kernel overhead (load, install) | 10.1 min |
| **This session total** | **32.4 min** |

**Cumulative across all sessions to date:** ~271.5 min (prior sessions) +
32.4 min (this session) = **~303.9 min (~5.06 GPU-hours)**.

Kaggle's remaining weekly quota is not queryable through this session's
API access (no such endpoint exists in the `kaggle` package) — check the
Kaggle notebooks/GPU-quota page directly for the current balance.

Sources:
- [GPU VRAM Requirements to Fine-Tune LLMs in 2026: Full, LoRA, and QLoRA Sizing and Cost by Model](https://www.spheron.network/blog/gpu-vram-requirements-fine-tune-llm-2026/)
- [Fine-Tuning an LLM with LoRA and QLoRA: A Hands-On Guide](https://medium.com/@aminfadaeinejad.edu/fine-tuning-an-llm-with-lora-and-qlora-a-hands-on-guide-441ea09360c5)
- [QLoRA: Efficient Finetuning of Quantized LLMs (Dettmers et al.)](https://arxiv.org/pdf/2305.14314)
