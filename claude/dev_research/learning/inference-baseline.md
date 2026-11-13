# Inference Baseline — Reference Notes, Lab and Quiz

Consolidated: **2026-11-09** from the October 4–5 platform packet. This is a topic reference,
not a second active curriculum. The original notes, readings, lab and all 15 answers are retained;
references to “Week 1” and later weeks below describe the historical exercise sequence only.
Use selected sections to support the current plan at
`/home/colligo/hs_scripts/claude/dev_research/learning/LEARNING_PLAN.md`.

Historical setup: Adobe/Pluto, a single H200 from an assumed two-GPU allocation, and
`Qwen/Qwen2.5-7B-Instruct` at revision `a09a35458c702b33eeacc393d103063234e8bc28`.
Availability, software versions and hardware must be checked before executing the lab. The old
5–6-hour estimate is not the current study budget. No lab completion is recorded.

The current first exercise and its separate review guide remain at
`/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/STUDY_GUIDE.md` and
`/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/REVIEW_GUIDE.md`.

## Contents

- [Outcome](#outcome)
- [Study sequence](#study-sequence)
- [Concise notes](#concise-notes)
- [Required external readings](#required-external-readings)
- [Lab — establish the baseline](#lab--establish-the-baseline)
- [Required baseline record](#required-baseline-record)
- [Week 1 completion gate](#week-1-completion-gate)
- [Quiz](#quiz)
- [What to send Codex when you need help](#what-to-send-codex-when-you-need-help)
- [Quiz answers](#quiz-answers)

## Outcome

By the end of this week, you will have a text-generation endpoint running through vLLM on one H200
and enough recorded state for another session to reproduce it. The endpoint itself is not the main
achievement. The achievement is establishing a trustworthy baseline from which later performance
experiments can be compared.

You should be able to explain:

1. the major layers between an HTTP request and GPU execution;
2. why “the server ran once” is not a reproducible experiment;
3. which hardware, software, model, configuration, request, and result fields must be recorded;
4. what the initial vLLM launch flags control; and
5. why Week 1 deliberately uses only one H200.

## Study sequence

1. Read the concise notes below: 30–40 minutes.
2. Complete the required external readings: 60–90 minutes.
3. Perform the lab: approximately 3 hours.
4. Review your captured baseline and take the quiz: 30–45 minutes.

The reference answer key is in [Quiz answers](#quiz-answers) at the end of this document.

Do not read the answer key until you have written your own answers.

## Concise notes

### 1. What vLLM is doing for you

At the surface, vLLM exposes a model through HTTP endpoints compatible with the OpenAI API. Below
that surface it owns important inference behavior: tokenization and chat-template handling, request
admission and scheduling, batching, KV-cache management, model execution, and communication with
PyTorch/CUDA kernels.

For this week, use this mental model:

```text
client request
    ↓
OpenAI-compatible HTTP API
    ↓
tokenizer + chat template
    ↓
vLLM request scheduler and engine
    ↓
model runner / PyTorch operations / compiled kernels
    ↓
CUDA runtime and NVIDIA driver
    ↓
H200 compute + HBM memory
```

Every layer can change behavior or performance. A model can produce different output because its
revision or tokenizer changed. A server can use different kernels because vLLM, PyTorch, CUDA, or
the GPU changed. The same launch command can behave differently under a different driver or package
set.

### 2. “It works” versus a baseline

A smoke test proves that one request completed. A baseline is a controlled reference point against
which later changes can be compared.

A useful baseline records six classes of state:

| Class | Examples |
|---|---|
| Hardware | GPU model/count, HBM size, topology, MIG status, CPU/RAM |
| System | OS/kernel, NVIDIA driver, CUDA runtime/toolkit, container/image if used |
| Software | Python, PyTorch, vLLM, Transformers and relevant package versions |
| Model | repository, exact revision, tokenizer/chat template, dtype, maximum context |
| Serving configuration | every vLLM flag and environment variable that changes execution |
| Workload and result | exact request, seed/sampling settings, timestamps, latency, GPU memory, output or error |

If any one of these is missing, future you may not know whether a result changed because of your
experiment or because the environment drifted.

### 3. Why begin with a small model on one H200

The 7B model is not intended to use the H200 efficiently. It is intended to shorten the
edit-launch-test loop and reduce the number of failure sources.

One GPU removes inter-GPU communication and parallelism from the first baseline. Week 6 introduces
two-GPU tensor parallelism only after the single-GPU behavior is understood. This sequencing gives
you a control case: if two GPUs behave unexpectedly, you have a known single-GPU reference.

### 4. Model choice and pinning

`Qwen/Qwen2.5-7B-Instruct` is the Week 1 default because its Hugging Face page currently reports:

- Apache-2.0 license;
- public and ungated access;
- text-generation/Transformers support; and
- safetensors artifacts.

Those facts were verified through the Hugging Face model API on 2026-10-04. The recorded repository
revision is `a09a35458c702b33eeacc393d103063234e8bc28`.

Pinning the revision protects you from silent changes to weights, tokenizer files, configuration,
or chat templates. If the model cannot be accessed from Pluto, stop and ask for help before
substituting another model: the replacement and reason must be recorded.

### 5. The initial vLLM flags

The Week 1 command uses only a few explicit controls:

- `--tensor-parallel-size 1`: use one GPU; distributed inference is not part of this baseline.
- `--dtype bfloat16`: use BF16 where supported. H200 supports BF16, and this avoids an automatic
  choice changing across environments.
- `--max-model-len 8192`: cap context for a quick, bounded starting configuration. This is not a
  claim that 8192 is optimal.
- `--gpu-memory-utilization 0.80`: give vLLM a conservative starting budget rather than consuming
  nearly all available HBM. Later weeks measure and tune this.
- `--served-model-name week1-qwen`: give clients a stable API-visible name independent of the
  Hugging Face repository string.
- `--revision`: pin model artifacts.

Do not add optimization flags this week. Each unexplained flag creates another uncontrolled
variable.

### 6. H200 context

An H200 SXM-class GPU is commonly specified with 141 GB of HBM3e and 4.8 TB/s peak memory bandwidth,
but the actual Pluto device and topology are the authority for your experiment. Capture what
`nvidia-smi` reports rather than copying product-page specifications into results.

The Week 1 model will leave most H200 capacity unused. That is expected. Capacity and saturation
become relevant only after the service is reproducible.

### 7. What not to conclude this week

Do not claim:

- maximum throughput;
- production readiness;
- multi-user scalability;
- optimal memory use;
- benefit from H200 versus another GPU; or
- benefit from any vLLM optimization.

Week 1 creates the reference system required to test those claims later.

### 8. Hardware inventory terms: HBM, topology, and MIG

- **HBM (High Bandwidth Memory)** is the memory physically close to the GPU. Model weights, KV
  cache, activations, and kernel workspaces compete for its capacity; its bandwidth often matters
  as much as compute during token-by-token decode.
- **Topology** is how GPUs and CPUs are connected: PCIe, NVLink/NVSwitch, and CPU NUMA paths.
  It matters most when tensor parallelism makes GPUs exchange data on every layer. Record
  `nvidia-smi topo -m`; do not infer the topology from the GPU model name.
- **MIG (Multi-Instance GPU)** partitions one physical GPU into isolated GPU instances with only a
  portion of its compute and HBM. A process seeing “one GPU” may therefore see a slice rather than
  the full device. `nvidia-smi -L` and the main `nvidia-smi` table reveal MIG configuration.

### 9. Sampling: temperature and nucleus probability

The model produces one logit per possible next token. Sampling is a decoding policy applied after
the model predicts those logits; it does not retrain or modify the model.

- **Temperature `T`** rescales logits before softmax: `softmax(logits / T)`. Below 1 sharpens the
  distribution; above 1 flattens it. In vLLM, `temperature=0` means greedy decoding.
- **Nucleus sampling (`top_p`)** sorts tokens by probability and keeps the smallest set whose
  cumulative probability reaches `p`, then renormalizes and samples from that set. Unlike `top_k`,
  the candidate count adapts to the shape of the distribution.

Example: if sorted probabilities are `0.60, 0.25, 0.10, 0.05`, `top_p=0.80` retains the first two
tokens because their cumulative mass is `0.85`. Temperature changes those probabilities before the
cutoff is applied. For a reproducible baseline use greedy decoding; for creative behavior, measure
quality/diversity with an explicit temperature, `top_p`, and seed policy.

### 10. Offline, synchronous, asynchronous, and online

`LLM(...)` loads and executes the model in the Python process on the hardware visible to that
process. “Offline” means there is no HTTP service boundary; it does not mean the CPU is used or that
the machine never accesses the network. Model artifacts may still be downloaded initially.

`LLM.generate(...)` is deliberately synchronous. It queues all prompts, repeatedly advances the
engine until every request is finished, and only then returns the list. No `await` is needed or
valid. vLLM's `AsyncLLM.generate(...)` is the asynchronous serving API: it returns an async stream
consumed with `async for`. The OpenAI SDK likewise has synchronous `OpenAI` and asynchronous
`AsyncOpenAI` clients.

### 11. Chat templates and `add_generation_prompt`

A causal language model always sees one token sequence, not Python role dictionaries. A chat
template converts messages into the exact control-token format used during instruction tuning.
For example, two models may encode the same user turn as either:

```text
<s>[INST] Hello [/INST]
```

or:

```text
<|user|>
Hello</s>
<|assistant|>
```

Using the wrong template can materially degrade behavior even when the underlying base model is
similar. `LLM.generate` accepts raw/formatted prompts and does not infer chat structure. `LLM.chat`
accepts OpenAI-shaped `{"role": ..., "content": ...}` messages and applies the model's template.

`add_generation_prompt=True` appends the control tokens that say, “the next turn is the
assistant's.” For Qwen2.5 that ends the prompt with `<|im_start|>assistant\n`. Without it, the model
may continue the user's turn instead of answering. Do not combine it with “continue the final
assistant message” semantics.

### 12. Completions, chat completions, and chat context

- `/v1/completions` receives one already formatted text prompt. The caller owns all roles and
  separators. It is appropriate for base models or deliberately preformatted prompts.
- `/v1/chat/completions` receives structured messages. The server applies the model's chat template
  and returns an assistant message. It is usually the correct interface for Instruct/Chat models.

Neither endpoint gives the model durable conversational memory. The application stores the
conversation and sends the relevant history on every new request:

```python
messages = [{"role": "system", "content": "You are a helpful assistant."}]
messages.append({"role": "user", "content": "My name is Hooman."})
reply = client.chat.completions.create(model="week1-qwen", messages=messages)
messages.append(reply.choices[0].message.model_dump(exclude_none=True))
messages.append({"role": "user", "content": "What is my name?"})
reply = client.chat.completions.create(model="week1-qwen", messages=messages)
```

The history consumes the model's context window. Production applications need an explicit policy
for truncation, summarization, retrieval, persistence, retention, and tenant isolation. Prefix/KV
caching can avoid recomputing repeated history, but it is a performance optimization—not semantic
memory and not a durable conversation store.

### 13. API-key and network security

The quickstart's `api_key="EMPTY"` is only a placeholder for a local vLLM server started without
authentication; the OpenAI client constructor requires a value. If the server starts with
`--api-key` or `VLLM_API_KEY`, the client must send the matching value as
`Authorization: Bearer <key>`. `OpenAI(api_key=...)` adds that header automatically.

```bash
# Have Pluto/Vault inject VLLM_API_KEY; do not type or save the value in Git or shell history.
test -n "$VLLM_API_KEY" || { echo 'VLLM_API_KEY is missing' >&2; exit 1; }
vllm serve Qwen/Qwen2.5-1.5B-Instruct
```

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key=os.environ["VLLM_API_KEY"],
)
```

For Week 1, keep `--host 127.0.0.1`; then no remote client can reach the listener and an API key is
not needed. If the service binds to `0.0.0.0` or crosses a machine/network boundary, use an injected
secret, never place it in source or the baseline, and add TLS plus gateway/network controls. A vLLM
API key authenticates possession of a bearer secret; by itself it does not provide encryption,
fine-grained authorization, tenant isolation, quotas, rate limiting, or safe prompt retention.

Also treat model artifacts as code/supply-chain inputs. Pin revisions and avoid
`--trust-remote-code` unless the model requires it and the repository/revision has been reviewed.

### 14. Attention orientation

The model computes `softmax(QKᵀ / √d + mask)V`. Model architecture determines semantics such as
MHA/GQA/MQA/MLA and causal/sliding-window behavior. An attention backend—FlashAttention,
FlashInfer, Triton, and others—is a systems implementation of those semantics. vLLM validates
backend compatibility against the GPU, dtype, head size, KV-cache layout, and model features.

On Hopper/H200, current vLLM v0.31.0 prioritizes FlashAttention for ordinary compatible attention
and defaults to FA3 within that backend. This is a version-scoped default, not a universal
performance result. Let vLLM auto-select during Week 1, record the startup log, and delay backend
A/B tests until the baseline is stable.

The growing deep-dive is:
`/home/colligo/hs_scripts/claude/dev_research/learning/attention.md`.

### 15. Adobe implementation cross-check

The local Adobe stack provides concrete examples of these concepts:

- V3 Foundry code renders the tokenizer chat template before sending a prompt to vLLM.
- Its GPU worker uses `AsyncLLM.generate(...)` and consumes an async generator, while the public
  web layer awaits the worker call.
- The inner service relies on a private in-cluster boundary; authentication and authorization are
  enforced at the customer gateway rather than inside the vLLM worker.
- Internal model/version history uses different backend choices and workarounds for different
  Qwen variants. Therefore backend selection must be versioned and benchmarked, not memorized.

Read these after the public quickstart; focus on architecture and control flow rather than trying
to understand every production feature:

- `/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/vllm_serve/README.md`
- `/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/vllm_serve/aidoc/development.md`
- `/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/vllm_serve/actors/vllm_worker.py`
- `/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/vllm_serve/actors/webapp.py`

The first two are required orientation; the code files are guided references, not required
line-by-line reading this week.

## Required external readings

Read in this order. Focus on the specified sections rather than reading every linked page.

### 1. vLLM Quickstart — 15 minutes

https://docs.vllm.ai/en/latest/getting_started/quickstart/

Focus on installation choices, `vllm serve`, and the distinction between offline and online
inference.

### 2. GPU installation — 10–15 minutes

https://docs.vllm.ai/en/latest/getting_started/installation/gpu/

Focus on environment compatibility and why vLLM/PyTorch/CUDA combinations matter. Do not reinstall
or upgrade the Pluto environment merely because the page shows a newer option.

### 3. OpenAI-compatible server — 20 minutes

https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/

Focus on `/v1/models`, `/v1/chat/completions`, API model names, chat templates, and authentication
options.

### 4. `vllm serve` CLI — 15 minutes

https://docs.vllm.ai/en/latest/cli/serve/

Find and read the entries for `--revision`, `--dtype`, `--max-model-len`,
`--gpu-memory-utilization`, `--tensor-parallel-size`, `--served-model-name`, `--host`, and `--port`.

### 5. Model card — 15 minutes

https://huggingface.co/Qwen/Qwen2.5-7B-Instruct

Focus on license, model type, chat use, context claims, tokenizer/chat-template requirements, and
the recommended generation behavior. Treat performance claims as model-author claims, not as your
measured results.

### 6. H200 overview — 10 minutes

https://www.nvidia.com/en-us/data-center/h200/

Focus on HBM capacity/bandwidth and interconnect context. Then compare the product claims with the
actual Pluto hardware inventory.

### 7. Chat templates — 15 minutes

https://huggingface.co/docs/transformers/main/en/chat_templating

Focus on why role dictionaries become control tokens, `add_generation_prompt`, and the warning
about duplicating special tokens.

### 8. Attention backends — 15 minutes

https://docs.vllm.ai/en/latest/design/attention_backends/

Focus on automatic selection, compatibility validation, and the CUDA priority rules. Read
`/home/colligo/hs_scripts/claude/dev_research/learning/attention.md` for the model-versus-systems
mental model; do not force a backend in the Week 1 baseline.

### Optional reference

Supported model architectures:
https://docs.vllm.ai/en/latest/models/supported_models/

## Lab — establish the baseline

Run commands from the allocated Pluto environment. You do the work; bring any error or unclear
output back to Codex for diagnosis.

### Step 1 — create the experiment area

Create these paths:

```text
/home/colligo/hs_scripts/claude/dev_research/inference-platform/
/home/colligo/hs_scripts/claude/dev_research/inference-platform/experiments/week-01/
```

Week 1 should ultimately produce only these durable artifacts:

```text
/home/colligo/hs_scripts/claude/dev_research/inference-platform/experiments/week-01/BASELINE.md
/home/colligo/hs_scripts/claude/dev_research/inference-platform/experiments/week-01/serve.sh
/home/colligo/hs_scripts/claude/dev_research/inference-platform/experiments/week-01/smoke-request.json
```

Do not create a separate note for every command or observation. Consolidate them into
`/home/colligo/hs_scripts/claude/dev_research/inference-platform/experiments/week-01/BASELINE.md`.

### Step 2 — inventory the environment

Run and preserve the relevant output:

```bash
date --iso-8601=seconds
uname -a
cat /etc/os-release
nvidia-smi
nvidia-smi -L
nvidia-smi topo -m
nvidia-smi --query-gpu=index,name,uuid,memory.total,driver_version,pstate --format=csv
python --version
python -c 'import torch; print("torch", torch.__version__); print("torch_cuda", torch.version.cuda); print("cuda_available", torch.cuda.is_available()); print("device_count", torch.cuda.device_count())'
python -c 'import vllm; print("vllm", vllm.__version__)'
python -c 'import transformers; print("transformers", transformers.__version__)'
vllm collect-env
```

If `vllm collect-env` is unavailable, record that fact; do not treat it as a lab failure.

Also record:

- how the Pluto instance/job was requested;
- the container image name and immutable digest, if a container is used;
- mounted cache/weight paths;
- whether MIG is enabled; and
- which GPU will be visible to the server.

Do not store credential values or access tokens in the baseline.

### Step 3 — write the launch command

The initial command template is:

```bash
export CUDA_VISIBLE_DEVICES=0
export MODEL_ID='Qwen/Qwen2.5-7B-Instruct'
export MODEL_REVISION='a09a35458c702b33eeacc393d103063234e8bc28'

vllm serve "$MODEL_ID" \
  --revision "$MODEL_REVISION" \
  --host 127.0.0.1 \
  --port 8000 \
  --tensor-parallel-size 1 \
  --dtype bfloat16 \
  --max-model-len 8192 \
  --gpu-memory-utilization 0.80 \
  --served-model-name week1-qwen
```

Save the final, actually executed command in:
`/home/colligo/hs_scripts/claude/dev_research/inference-platform/experiments/week-01/serve.sh`.

If network topology requires binding beyond loopback, record the reason and use the private
environment's authentication/network controls. Do not silently change the host.

Record:

- launch start time;
- time at which `/v1/models` first becomes healthy;
- model download/load time if distinguishable;
- vLLM startup log and any warnings; and
- `nvidia-smi` memory/utilization after the model is idle and ready.

### Step 4 — verify API identity

```bash
curl --fail --silent --show-error \
  http://127.0.0.1:8000/v1/models | python -m json.tool
```

Confirm that the API-visible model name is `week1-qwen`.

### Step 5 — run a deterministic smoke request

Save this request as:
`/home/colligo/hs_scripts/claude/dev_research/inference-platform/experiments/week-01/smoke-request.json`.

```json
{
  "model": "week1-qwen",
  "messages": [
    {
      "role": "user",
      "content": "In exactly three bullet points, explain why reproducibility matters in inference benchmarking."
    }
  ],
  "temperature": 0,
  "max_tokens": 160
}
```

Run it while capturing total client-observed time:

```bash
curl --fail --silent --show-error \
  -o /tmp/week01-response.json \
  -w 'http_code=%{http_code}\ntime_total_seconds=%{time_total}\n' \
  -H 'Content-Type: application/json' \
  --data-binary '@/home/colligo/hs_scripts/claude/dev_research/inference-platform/experiments/week-01/smoke-request.json' \
  http://127.0.0.1:8000/v1/chat/completions

python -m json.tool /tmp/week01-response.json
```

Record the full response, total time, prompt/completion token counts, and post-request GPU memory.
The temporary response need not become another permanent file; copy its relevant contents into
`/home/colligo/hs_scripts/claude/dev_research/inference-platform/experiments/week-01/BASELINE.md`.

### Step 6 — restart and reproduce

Stop the server cleanly, launch it again with the saved command, and repeat `/v1/models` plus the
smoke request.

Compare:

- model identity;
- startup warnings;
- idle GPU memory;
- token counts and output;
- client-observed request time; and
- any unexplained difference.

The two request times do not need to be identical. Week 3 establishes benchmarking rigor. This
week, you need to notice and preserve differences rather than explain them away.

## Required baseline record

`/home/colligo/hs_scripts/claude/dev_research/inference-platform/experiments/week-01/BASELINE.md`
should contain:

1. date and environment location;
2. hardware/topology summary;
3. system and package versions;
4. model repository and pinned revision;
5. exact launch command and environment variables;
6. model-ready time and idle HBM;
7. exact smoke request;
8. first and second response summaries, token counts, total times, and GPU memory;
9. warnings, failures, and deviations from the guide;
10. what remains unknown; and
11. the exact Week 2 starting point.

## Week 1 completion gate

Week 1 is complete only if:

- the endpoint ran on exactly one visible H200;
- the model revision and software versions were recorded;
- the exact launch command and request were saved;
- `/v1/models` and chat completion succeeded twice across a restart;
- hardware state and basic timing were captured; and
- you can explain the serving stack and every explicit launch flag.

Do not proceed merely because the endpoint returned text.

## Quiz

Write your answers before opening the answer file.

1. What additional evidence turns a successful request into a reproducible baseline?
2. List the major layers between a chat request and H200 execution.
3. Why is Week 1 restricted to one GPU even though two H200s are available?
4. What does `CUDA_VISIBLE_DEVICES=0` control, and what does it not prove?
5. Why pin the model revision instead of only recording `Qwen/Qwen2.5-7B-Instruct`?
6. What is the purpose of `--served-model-name week1-qwen`?
7. What does `--gpu-memory-utilization 0.80` mean conceptually, and why is it not an optimal value
   claim?
8. Why explicitly set `--max-model-len 8192` for the baseline?
9. Name three conclusions that the Week 1 smoke request cannot support.
10. If the second launch has materially different idle GPU memory, what should you do before
    accepting the baseline?
11. Explain the difference among HBM, GPU topology, and MIG, and how each can affect an experiment.
12. Explain how temperature and top-p change next-token selection.
13. Why does offline `LLM.generate(...)` not use `await`, while an `AsyncLLM` serving loop does?
14. Where does multi-turn chat state live, and why is a prefix/KV cache not durable chat memory?
15. What does a vLLM API key protect, and which production security controls does it not replace?

## What to send Codex when you need help

Provide:

- the exact command;
- the complete error and the preceding relevant log lines;
- environment/version output;
- expected versus observed behavior; and
- what changed since the last successful step.

Do not summarize an error as “vLLM failed.” The raw error is part of the learning material.

## Quiz answers

Attempt the quiz first. This answer key is retained for the reference exercise, not for the current
system-design packet.

<details>
<summary>Show the 15 reference answers</summary>

### 1. Successful request versus reproducible baseline

A baseline records the hardware/topology, system and driver/CUDA environment, relevant package
versions, exact model repository and revision, tokenizer/chat-template context, every execution-
changing flag/environment variable, exact request/sampling settings, logs/warnings, hardware state,
and measured result. It also demonstrates that the procedure works again after a restart.

### 2. Major serving layers

One useful decomposition is:

1. client and HTTP/OpenAI-compatible API;
2. tokenizer and chat template;
3. vLLM request engine/scheduler and KV-cache management;
4. model runner plus PyTorch/compiled kernels;
5. CUDA runtime and NVIDIA driver; and
6. H200 compute and HBM.

The exact boundaries vary, but omitting the API/tokenization, serving engine, execution runtime, or
hardware layers produces an incomplete explanation.

### 3. Why one GPU first

One GPU removes inter-GPU communication, topology, collective libraries, and parallel partitioning
from the initial system. It creates a control case for Week 6. Two GPUs are valuable only after you
can distinguish scaling effects from ordinary environment or serving variability.

### 4. `CUDA_VISIBLE_DEVICES=0`

It limits/remaps which physical GPUs the process can see, exposing only the selected device in this
case. It does not prove that no other process uses that GPU, that MIG is disabled, that the GPU has
full capacity, or that vLLM actually allocated the expected memory. Verify those separately through
`nvidia-smi`, process inspection, and logs.

### 5. Why pin the model revision

Repository names are mutable references. Weights, tokenizer files, configuration, generation
defaults, and chat templates can change. A commit revision identifies the precise artifact set used
by the experiment and prevents silent model drift.

### 6. `--served-model-name`

It defines the stable model identifier clients send to the API. This decouples the public API
contract from the storage/repository identifier and makes future backend replacement or versioning
easier to manage deliberately.

### 7. `--gpu-memory-utilization 0.80`

It gives vLLM a target fraction/budget of visible GPU memory for its execution/cache planning. The
exact behavior depends on the current vLLM version and other memory users. `0.80` is a conservative
starting control, not evidence that 80% maximizes throughput, avoids all OOMs, or is production-
optimal. Those claims require later experiments.

### 8. Why cap model length

Maximum model length affects memory planning, especially KV-cache capacity, and can change startup
or request capacity. Explicitly setting 8192 makes the baseline bounded and prevents model defaults
or version changes from silently altering the experiment. It is not a recommendation for every
workload.

### 9. Unsupported Week 1 conclusions

Any three of the following are sufficient:

- maximum throughput;
- p95/p99 latency;
- production readiness;
- safe concurrency limit;
- optimal memory utilization;
- H200 advantage over another GPU;
- benefit of vLLM over another engine;
- quality superiority;
- benefit of two GPUs; or
- effectiveness of caching, batching, quantization, or another optimization.

A single or repeated smoke request is not a controlled performance study.

### 10. Different idle memory after restart

Do not average or dismiss it. Confirm the same model revision, visible GPU, launch command, package
versions, model length, dtype, and clean process state. Check for other GPU processes, stale workers,
MIG differences, cache/compilation behavior, and startup warnings. Reproduce again after isolating
the suspected cause. Record unresolved variance as a limitation rather than accepting the baseline
as stable.

### 11. HBM, topology, and MIG

HBM is the GPU's high-bandwidth memory and holds weights, KV cache, activations, and workspaces.
Topology describes GPU-to-GPU and GPU-to-CPU links such as NVLink/NVSwitch, PCIe, and NUMA paths.
MIG partitions a physical GPU into isolated slices, so a visible CUDA device may have only part of
the GPU's compute and HBM. All three can materially change capacity or performance.

### 12. Temperature and top-p

Temperature divides logits before softmax: below 1 sharpens the distribution, above 1 flattens it,
and 0 requests greedy decoding in vLLM. Top-p keeps the smallest probability-ranked token set whose
cumulative mass reaches `p`, renormalizes it, and samples. Temperature shapes the probabilities;
top-p chooses the adaptive candidate set.

### 13. Why `LLM.generate` has no `await`

The offline `LLM.generate` API is synchronous and blocks while it queues prompts and steps the
engine until every request finishes. `AsyncLLM.generate` is a different API that produces an async
stream and is consumed with `async for`; `AsyncOpenAI` is the corresponding asynchronous HTTP
client.

### 14. Chat memory

The vLLM chat-completions endpoint is stateless with respect to conversational meaning. The client
or application stores prior user and assistant messages and resends the relevant history each
turn. KV/prefix caching may reuse computation but is not durable chat memory. The application must
also handle context limits, summarization/retrieval, retention, and tenant isolation.

### 15. API key limitations

The configured key is sent as an HTTP bearer token, normally through the OpenAI client's
`api_key` argument. It proves possession of one shared secret. It does not encrypt traffic or
provide fine-grained authorization, quotas, rate limiting, audit policy, or prompt-data controls.
Use loopback for the Week 1 local baseline; for a network service add injected secrets, TLS, a
private network/gateway, authorization, rotation, logging controls, and abuse limits.

</details>
