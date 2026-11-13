# Attention — Model Semantics and Inference Engineering

Last updated: 2026-10-05  
Scope: decoder-style LLM inference, especially vLLM on NVIDIA Hopper/H200. This is a growing note.

## Confidence and version scope

- **VERIFIED — public primary sources, retrieved 2026-10-05:** the attention equation, chat-model
  execution model, vLLM backend-selection behavior, and current vLLM v0.31.0 Hopper preference.
- **VERIFIED — direct local inspection, 2026-10-05:** the checked Adobe environment contains vLLM
  0.16.0, PyTorch 2.9.1+cu130, and both FlashAttention and FlashInfer implementations. Current
  Adobe application code also targets newer vLLM behavior, so no single local version represents
  every deployment.
- **UNVERIFIED for Hooman's Week 1 Pluto allocation:** exact installed versions, H200 topology,
  selected backend, and performance. Capture these from the live job before drawing conclusions.

## 1. The core model operation

For one attention head, the simplified operation is:

```text
Attention(Q, K, V) = softmax((Q Kᵀ / √d_head) + mask) V
```

The model projects each token representation into:

- **query (Q):** what this token is looking for;
- **key (K):** what each candidate token advertises; and
- **value (V):** the information returned when that candidate receives attention.

`QKᵀ` produces similarity scores. Division by `√d_head` keeps their scale stable. The causal mask
prevents a generated token from seeing future tokens. Softmax converts scores to weights, and the
weighted sum of `V` supplies context for the next layer.

Multi-head attention performs this operation in parallel subspaces. The major variants matter to
serving because they change how many K/V heads must be cached:

| Architecture | Query heads | K/V heads | Serving consequence |
|---|---:|---:|---|
| MHA | many | one per query head | largest conventional KV cache |
| GQA | many | shared by groups of query heads | smaller KV cache with much of MHA's capacity |
| MQA | many | one shared K/V head | smallest conventional KV cache, cheaper decode |
| MLA | many | compressed latent K/V representation | different cache and specialized kernels |

These are model-architecture choices encoded in the model configuration and weights. A runtime
cannot arbitrarily turn an MHA model into an MLA model without changing the model.

## 2. Training, prefill, and decode

The same attention math appears in three very different execution regimes:

1. **Training:** process whole sequences, retain activations for backpropagation, and compute
   gradients. Memory pressure includes parameters, optimizer state, gradients, and activations.
2. **Prefill:** process all prompt tokens, usually in parallel, and create a K/V entry for each
   layer and token. Long prompts make this compute-intensive because token-to-token attention grows
   quadratically with sequence length for full attention.
3. **Decode:** generate one new token per sequence per step. The new query attends over the existing
   KV cache. Decode is commonly constrained by reading model weights and a growing KV cache from
   HBM, so memory bandwidth and batching are central.

A useful approximate KV-cache formula for a conventional decoder is:

```text
bytes per cached token
  ≈ 2 (K and V) × layers × KV heads × head dimension × bytes per element
```

Multiply by active cached tokens across all requests. GQA/MQA reduce `KV heads`; FP8 KV cache
reduces bytes per element. Real engines also need block metadata, workspaces, fragmentation
headroom, and other allocations.

## 3. Why FlashAttention and PagedAttention are different ideas

Naive attention materializes the large score/probability matrix in HBM. **FlashAttention** computes
the same exact attention result in tiles, keeping useful blocks in faster on-chip memory and
reducing HBM reads/writes. It changes the kernel/data movement, not the model's learned function or
the asymptotic `O(T²)` arithmetic of full attention.

**PagedAttention** addresses KV-cache allocation. Instead of requiring one contiguous allocation
per request, it stores KV data in fixed-size blocks and maps a request's logical token positions to
physical blocks. This reduces fragmentation and enables flexible growth and prefix sharing.
PagedAttention is therefore a memory-management scheme plus kernels that understand the block
table; it is not a new learned attention architecture.

## 4. What an attention backend is

An attention backend is an interchangeable implementation of the runtime attention operator. It
must honor the model's required semantics—causal versus non-causal masking, MHA/GQA/MQA/MLA,
sliding windows, attention sinks, dtypes, and KV-cache layout—but may use different CUDA/Triton
kernels and workspace strategies.

The stack is:

```text
model architecture and weights
    ↓ specify attention semantics and tensor shapes
vLLM Attention layer
    ↓ asks the platform selector for a compatible backend
FlashAttention / FlashInfer / Triton / another implementation
    ↓ launches kernels and reads/writes the paged KV cache
CUDA runtime + driver → GPU SMs, SRAM/registers, and HBM
```

In inspected vLLM code, the `Attention` layer passes model/runtime properties such as head size,
dtype, KV-cache dtype, block size, attention type, MLA, sinks, sparse attention, multimodal-prefix
attention, and sliding-window behavior into backend selection. The CUDA platform validates
candidates and chooses the first compatible backend in its version-specific priority list. A
manual override still goes through validation and fails if incompatible.

This is how the same model can run with different backends: the model-level operation stays the
same while its systems-level implementation changes. Expect small floating-point differences from
operation ordering; verify quality or exactness requirements rather than assuming bitwise identity.

## 5. Which backend is best on H200?

There is no universal fastest backend. The answer depends on:

- vLLM and backend versions;
- GPU generation and compute capability;
- model attention architecture and head dimensions;
- model and KV-cache dtype;
- prompt length, output length, batch/concurrency, and prefix reuse;
- prefill versus decode dominance; and
- required features such as sliding windows, multimodal prefix masks, sinks, speculative decoding,
  CUDA graphs, or context parallelism.

For **standard MHA/MQA/GQA on Hopper/H200**, current vLLM v0.31.0 prioritizes FlashAttention over
FlashInfer when both are compatible; its current policy defaults the FlashAttention backend to FA3
on SM90/Hopper. That makes automatic selection the correct Week 1 default—not proof that
FlashAttention wins every workload.

Practical characterization:

- **FlashAttention:** highly optimized exact attention, with FA3 specialized for Hopper. It is the
  current vLLM default priority for ordinary Hopper attention.
- **FlashInfer:** a serving-oriented kernel library with strong paged-KV, decode, sampling, and MLA
  paths. It can win for particular models, dtypes, batch shapes, or decode-heavy workloads.
- **Triton attention:** portable, inspectable kernels and useful fallback/specialized paths. It is
  usually not the first standard-attention choice on Hopper in current vLLM.
- **Torch SDPA:** a valuable reference/fallback abstraction, especially outside vLLM-specific
  serving paths, but not the default standard decoder backend in the current Hopper priority list.

The correct engineering procedure is to let vLLM auto-select, record the selected backend from the
startup log, then benchmark compatible alternatives under the exact workload. Compare correctness,
TTFT, inter-token latency, request throughput, token throughput, peak/steady HBM, and tail latency.

## 6. Adobe implementation lessons

Direct inspection found several production lessons worth carrying into the learning project:

1. Adobe's V3 Foundry vLLM worker renders the tokenizer's chat template with
   `add_generation_prompt=True` before submission to `AsyncLLM`.
2. Its request path uses `AsyncLLM.generate(...)` and consumes the result with `async for`; this is
   the concurrent serving counterpart to the synchronous offline `LLM.generate(...)` API.
3. The web application awaits the worker boundary and keeps HTTP/I/O concerns outside the GPU
   worker. This is a concrete example of separating protocol, orchestration, and model execution.
4. Tensor-parallel size is derived from allocated devices, avoiding a deployment setting that can
   drift from actual GPU allocation.
5. Internal history includes an explicit FlashInfer choice for one Qwen model and automatic FA3
   selection for a newer hybrid model, plus backend-specific workarounds. This is strong practical
   evidence that backend choice is version/model/workload specific and must be tested.
6. The internal webapp does not perform authorization itself because it is intended to be
   reachable only in-cluster; the customer gateway owns authentication and authorization. This is
   safe only while that network and gateway boundary remains true.

Internal sources inspected:

- `/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/vllm_serve/actors/vllm_worker.py`
- `/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/vllm_serve/actors/webapp.py`
- `/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/vllm_serve/aidoc/development.md`
- `/home/colligo/colligo/models/colligo/models/firefly/lego_vllm_v4/scripts/eval/model_comparison_report.md`
- `/home/colligo/colligo/managed_services/.venv/lib/python3.13/site-packages/vllm/v1/attention/selector.py`
- `/home/colligo/colligo/managed_services/.venv/lib/python3.13/site-packages/vllm/platforms/cuda.py`
- Obsidian synthesis `[[wiki/concepts/colligo-inference]]` at
  `/home/colligo/hs_scripts/claude/obsidian/hs_base/wiki/concepts/colligo-inference.md`
- Obsidian synthesis `[[wiki/concepts/v3-inference-framework]]` at
  `/home/colligo/hs_scripts/claude/obsidian/hs_base/wiki/concepts/v3-inference-framework.md`
- Obsidian synthesis `[[wiki/concepts/mori-parallelism]]` at
  `/home/colligo/hs_scripts/claude/obsidian/hs_base/wiki/concepts/mori-parallelism.md`

## 7. Suggested experiments for later weeks

Do not add these variables to the first baseline. After the baseline is stable:

1. Record the automatically selected backend and exact versions.
2. Build a matrix with short/long prompts, short/long outputs, and low/high concurrency.
3. Force only compatible backends one at a time.
4. Hold model revision, dtype, KV dtype, context cap, request set, and seed policy constant.
5. Compare output validity and numerical/quality drift before comparing speed.
6. Repeat runs and report distributions, especially p95/p99—not only one average.

## Public primary sources

- vLLM Quickstart, retrieved 2026-10-05:
  https://docs.vllm.ai/en/latest/getting_started/quickstart/
- vLLM attention backend behavior, retrieved 2026-10-05:
  https://docs.vllm.ai/en/latest/design/attention_backends/
- vLLM v0.31.0 release, published 2026-10-05:
  https://github.com/vllm-project/vllm/releases/tag/v0.31.0
- FlashAttention paper:
  https://arxiv.org/abs/2205.14135
- FlashAttention-2 paper:
  https://arxiv.org/abs/2307.08691
- FlashAttention-3 paper:
  https://arxiv.org/abs/2407.08608
- FlashInfer paper:
  https://arxiv.org/abs/2501.01005
- vLLM/PagedAttention paper:
  https://arxiv.org/abs/2309.06180
- Hugging Face chat-template guide, retrieved 2026-10-05:
  https://huggingface.co/docs/transformers/main/en/chat_templating

## Open questions

- Which exact vLLM/PyTorch/CUDA versions are installed in the Week 1 Pluto job?
- Which backend does that version select for the pinned Qwen2.5 model on the allocated H200?
- What H200 form factor and interconnect topology does the allocation expose?
- Under Hooman's eventual workload, is prefill, decode, queueing, or application orchestration the
  dominant bottleneck?
