# Lesson 2 — From an ML Model to a Text-Generation Service

Prepared: **2026-11-15**. This is the next bounded fundamentals packet in the current
curriculum. It does not record completion of the video-job exercise or this lesson.
Examples are deliberately small or synthetic; there are no measured GPU results here.

## How to use this lesson

Read the explanation first, then attempt the separate exercise:
`/Users/ana.rodrigues/Desktop/hooman/hs_scripts/claude/dev_research/learning/first-pass/ML_INFERENCE_EXERCISE.md`.
You can do the entire exercise with Python, paper and a calculator. A model download,
GPU allocation or new inference server is not a prerequisite.

Before changing topics, make one short attempt at the video-job design from:
`/Users/ana.rodrigues/Desktop/hooman/hs_scripts/claude/dev_research/learning/first-pass/STUDY_GUIDE.md`.
Draw its components, state what acceptance promises, and trace a worker takeover and late
completion in your own words. Record what required reopening the tutorial. If a gap remains,
bring that specific gap back; there is no requirement to memorize every AWS alternative.

The goal of lesson 2 is to explain what a model computes, distinguish learning from inference,
estimate its memory, and interpret latency evidence. Production scheduling and deployment get
their own later stages.

## 1. Start with the whole request

Suppose a customer asks a text-generation service, “Explain why the sky is blue.” A typical
decoder-only language model generates a response by repeatedly predicting a next token.
A **token** is an element of the tokenizer's vocabulary: often a word fragment, punctuation,
or a special marker. One word is not necessarily one token.

```text
customer's messages
    ↓
chat template: serialize roles and message boundaries
    ↓
tokenizer: text → integer token IDs
    ↓
embedding lookup: IDs → vectors of numbers
    ↓
transformer layers: use context to transform those vectors
    ↓
output projection: scores for candidate next tokens
    ↓
decoding policy: choose a token
    ↓
append it, update request state, generate another token
    ↓
stream text until a stop condition
```

An **embedding** is a learned vector associated with a token. A **logit** is an unnormalized
score: the output projection produces one score per vocabulary entry. A **softmax** converts
those scores into probabilities that sum to one. The decoding policy can pick the largest score
or sample from a distribution. An end-of-sequence marker, requested stop sequence or output limit
can end generation.

**Sampling temperature** is a decoding setting that rescales logits before sampling:
`softmax(logits / T)` for positive `T`. Lower positive temperatures concentrate probability on
higher-scoring tokens; higher temperatures flatten the distribution. The setting changes token
selection, not the learned weights. Greedy selection chooses the highest-scoring token directly.

These steps are the work inside a text-generation worker or engine. The previous lesson's
database, storage and recovery design describes how an application manages durable jobs around
computation. A chat endpoint can instead stream a response over the caller's HTTP connection;
it does not automatically need the same durable-job queue.

For chat, a **chat template** turns structured user/assistant messages into the model's expected
text and control tokens. Arbitrary role dictionaries do not become model input by themselves.
Changing the template can change behavior even with unchanged weights. The application must
supply relevant conversation history; request-local caching is not durable conversational memory.

## 2. What tensors and matrix multiplication mean here

A **tensor** is an array of numbers with a shape. A vector has one dimension, a matrix has two,
and a batch of token vectors commonly has three. For this explanation:

- `B` = batch size: number of sequences processed together.
- `S` = sequence length: token positions per sequence in the rectangular example.
- `H` = hidden width: numbers in each token vector.

An activation tensor shaped `[B, S, H] = [2, 4, 8]` contains two sequences, four positions each,
and eight numbers at each position. An **activation** is an intermediate value produced while
executing the model, rather than a permanently learned parameter.

A linear projection multiplies those vectors by a weight matrix. If `W` has shape `[8, 12]`,
then `X @ W` has shape `[2, 4, 12]`. The eight input features contract against the eight rows of
`W`; each token gets twelve output features. The batch and position dimensions remain.

For one token, the arithmetic can be as small as:

```text
x = [2, 3]
W = [[1, 0, 1],
     [0, 1, 1]]

x @ W = [2, 3, 5]
```

The same learned matrix can be applied to many token positions. GPUs accelerate operations like
these on large collections of numbers. Increasing `B`, `S` or feature dimensions changes both
work and intermediate storage. Modern engines also use packed or variable-length representations;
the rectangular example teaches shape reasoning, not a mandatory padded implementation.

## 3. Training changes the model; inference uses it

**Parameters**, also called weights, are learned numbers. During **training**, a model makes a
prediction, a **loss function** measures a discrepancy from a target, and an optimizer updates
parameters. A **gradient** tells us how a small parameter change would change the loss.
**Backpropagation** computes these gradients through the composed operations using the chain rule.

For a tiny model `prediction = w × x`, take `x = 2`, target `y = 6`, and `w = 1`:

```text
prediction = 2
squared loss = (prediction − target)² = 16
gradient with respect to w = 2 × (w × x − y) × x = −16

with learning rate 0.1:
new w = old w − 0.1 × gradient = 2.6
new prediction = 5.2; new loss = 0.64
```

This is one illustrative gradient-descent update, not a recommended language-model optimizer.
A **learning rate** sets the update size. Real optimizers can also maintain momentum or other
state, which consumes memory.

For next-token language modeling, training targets are the following tokens in a sequence.
**Cross-entropy loss** penalizes assigning low probability to the target token. An ordinary
training pass can predict at many positions together under a causal mask; generation must
choose a token before it knows the next input token.

During ordinary **inference**, weights stay fixed and no gradient-based parameter update is
performed. Activations and request caches still change. Training often needs gradients,
saved activations and optimizer state in addition to weights; an inference weight estimate
cannot therefore be treated as a training memory estimate.

Evaluation mode and disabling gradient recording are separate controls in frameworks such as
PyTorch. For example, evaluation mode changes behavior of layers such as dropout; it does not
itself disable autograd. Do not equate “we are testing” with “the framework stores no gradients.”

## 4. How to tell whether learning helped

Use a **training set** to fit parameters, a **validation set** to choose settings and models,
and a **test set** reserved for the final assessment. An **overfit** model performs well on the
training examples but generalizes poorly to new examples.

**Leakage** happens when information unavailable at real prediction time influences training
or selection. For example, suppose clips from the same source video appear in both training
and test. The test may reward remembering source-specific details rather than handling a new
video. Split at the meaningful source/customer/time boundary, and fit preprocessing using
training data. Repeatedly tuning against a nominal test set makes it a selection set in practice.

Distinguish the loss used to train from the metric used to accept a product. Lower text loss
does not alone prove fewer factual errors or better customer answers. Accuracy measures a
fraction of correct labels; precision and recall expose different error types; a ranking metric
evaluates ordering. Choose metrics for the actual task and error costs. **Distribution shift**
means production inputs differ from the conditions represented by the evaluation data.

For a chosen positive class, **classification precision** is the fraction of predicted positives
that are actually positive; **recall** is the fraction of actual positives that were found. These
metric terms describe classification errors. Later, “numeric precision” describes how numbers
are stored; that is a different use of the word precision.

For orientation: **pretraining** develops broad capability from a large training corpus;
**supervised fine-tuning (SFT)** trains on examples of desired responses; **preference optimization**
uses preference information to favor some responses over others. Changing sampling temperature
is an inference policy, not one of these training procedures. Detailed training/evaluation
workflows belong to the later applied-ML stage.

## 5. What a transformer layer does

A transformer block combines attention with a feed-forward network and typically includes
normalization and residual connections. A **residual connection** adds a block's input to a
transformed output. The feed-forward network applies learned projections and a nonlinear
function to each position. Attention lets positions exchange information.

For one attention head, learned projections produce:

- **Q, queries:** what information a position is looking for.
- **K, keys:** features used to score how relevant a position is.
- **V, values:** information mixed into the resulting representation.

With `Q`, `K` and `V` shaped `[S, D]`, attention computes:

```text
scores = Q @ Kᵀ / sqrt(D)       # shape [S, S]
weights = softmax(scores + causal_mask)
result = weights @ V           # shape [S, D]
```

The **causal mask** prevents a position from attending to later positions. It keeps next-token
training from looking at its own future answers. Multiple attention heads let the model form
several such mixtures; their results are combined. Positional information also tells the model
where tokens occur, since the mixing formula alone does not encode their order.

This diagram is the mathematical operation. Efficient implementations can avoid materializing
the full `[S, S]` score array. FlashAttention is an example of changing attention's memory-access
implementation while preserving the intended attention operation; it is not a new training target.

## 6. Prefill, decode and the KV cache

**Prefill** processes the supplied prompt. Its token IDs are already known, so computations for
many prompt positions can run together within the causal architecture. Prefill builds cached
keys and values and supplies logits used to choose the first output token.

**Decode** advances generation after that: process the chosen token, attend to past context,
update the cache, and choose the next token. Within one ordinary autoregressive sequence, the
next choice depends on the previous choice. Engines can batch different requests and use other
techniques; “one token at a time” does not mean one GPU thread or one request per GPU.

```text
prompt tokens [p1 p2 p3] → prefill → choose t1
cached prompt + t1      → decode  → choose t2
cached context + t2     → decode  → choose t3
```

A **KV cache** stores past attention keys and values so they need not be recomputed from the
entire prefix every step. It consumes memory proportional to the cached context for the
conventional full-context architecture used below. Output tokens extend that context too.
Depending on the execution step, the most recently selected token may not yet have had its
K/V computed; the estimate uses the explicitly supplied number of cached tokens.

In **multi-head attention (MHA)**, each query head has corresponding K/V heads. In **grouped-query
attention (GQA)**, several query heads share one K/V head. **Multi-query attention (MQA)** uses
one K/V head shared by all query heads. For KV-memory calculations, use the number of K/V heads,
which can be smaller than the number of query heads. Other architectures, sliding windows and
compressed caches require different accounting.

## 7. Estimate memory by naming the things stored

**Precision** describes the numeric representation. BF16 and FP16 each use two bytes per stored
element, but have different numeric range/precision behavior. FP32 uses four bytes. Lower-precision
weights can reduce their storage; quantization can also introduce scales and metadata and requires
quality/performance evaluation. Weight precision and KV-cache precision are separate settings.

For a model with `P` stored parameters:

```text
raw weight bytes ≈ P × bytes_per_parameter
```

For ordinary, unshared, full-context decoder KV payload across the modeled layers:

```text
KV bytes = 2 × layers × KV_heads × head_dimension
             × total_cached_tokens × bytes_per_KV_element
```

The factor two is for K and V. `total_cached_tokens` is summed across requests; if every one of
`B` requests has length `S`, it is `B × S`. For unequal lengths, sum the lengths. This estimates
payload, not allocation overhead or total GPU memory. It assumes no prefix sharing, compression,
sliding-window reductions or distribution of layers/cache across devices.

Consider a **synthetic** model with 7 billion parameters, 32 layers, 8 K/V heads, head dimension
128, BF16 weights and BF16 K/V. These numbers define an example; they are not a verified model card.

```text
weights = 7,000,000,000 × 2 = 14,000,000,000 bytes
        ≈ 13.04 GiB

KV for one cached token = 2 × 32 × 8 × 128 × 2
                        = 131,072 bytes = 128 KiB

one request with 4,096 cached tokens = 512 MiB = 0.5 GiB
eight such requests = 4 GiB

weights + KV payload ≈ 17.04 GiB
```

`GB` means a billion bytes; `GiB` means `2³⁰` bytes. A nominal “7B model” may have a different
exact parameter count; use the real configuration and representation when sizing hardware.

The GPU also needs transient activations, attention/kernel workspaces, runtime allocations and
possibly preallocated cache blocks. The payload estimate does not establish a safe request limit.
For our assumed 24 GiB device, nominal space after weights and this KV payload is about 6.96 GiB;
whether execution actually fits depends on those remaining allocations and the workload.

Doubling request count or each request's cached length doubles this KV payload. Changing weights
to one-byte storage would reduce raw weight bytes, but would not automatically halve BF16 K/V.
A memory layout optimization changes how cache is allocated; it need not change the number of
mathematical K/V elements. Do not conflate attention IO optimization with cache paging.

## 8. Relate compute and memory to batching

A GPU has both a compute rate and a rate at which it can move bytes from its memory. **Memory
bandwidth** is bytes moved per second; it differs from memory capacity, which is bytes stored.
A rough lower-bound way to reason about an operation is:

```text
time cannot be less than either:
  required operations / usable compute rate
  required transferred bytes / usable memory bandwidth
```

Actual execution can be slower because of scheduling, communication, kernel overhead or poor
utilization. Peak specifications are not measured usable rates.

During low-batch decode, repeatedly moving weights for limited new-token computation can make
memory bandwidth important. Batching lets a weight read contribute to more token vectors and
can improve throughput. Long-prompt prefill has larger matrix operations and can use compute
well, while long-context attention and cache traffic add their own costs. These are tendencies,
not a rule that every prefill is compute-bound or every decode is memory-bound.

**Throughput** is completed work per time, such as aggregate output tokens/second. **Latency** is
the time experienced by a request. A larger batch can improve total throughput while increasing
an individual request's waiting time or token delay. A fixed batch groups requests for execution;
continuous batching lets an engine admit and retire requests as generation progresses. Detailed
scheduler policies are a later design lesson.

## 9. Read the timeline before proposing an optimization

For this lesson, define the timestamps on one common illustrative clock:

```text
request arrives → waits → processing starts → first token arrives → last token arrives
```

- **TTFT (time to first token):** first-token time minus request-arrival time, at the specified
  observation boundary. It includes waiting and other work before the first token reaches it.
- **Queue wait:** processing-start time minus arrival time, for this supplied trace.
- **Mean inter-token time:** `(last − first) / (output_tokens − 1)` when at least two tokens
  were delivered. We use this as the exercise's explicit mean TPOT convention.
- **End-to-end latency:** last-token time minus request-arrival time, ignoring any subsequent
  transport-close overhead in this example.

**TPOT** means time per output token. Libraries and benchmarks can define it using different
internal timing boundaries or denominators; check the metric's documentation. A one-token
response has no observed interval between output tokens. Real streaming chunks can also contain
multiple tokens, so chunk-arrival timestamps are not automatically token-arrival timestamps.

The exercise supplies four synthetic request timelines. A long TTFT with a large queue wait
suggests a different investigation from a long TTFT with immediate processing. Similar first-token
times with different inter-token times suggest examining the generation phase. Tokenization,
networking and scheduler overhead still matter; these timelines are not a GPU profiler.

Measure prompt/output lengths, concurrent requests, scheduler wait, first-token delay,
inter-token delays, memory usage and errors when comparing a real serving change. Hold workload
and relevant configuration constant. A few examples can teach arithmetic, but cannot establish
p99 latency or maximum sustainable capacity.

## 10. Keep the first exercise local and the evidence honest

The exercise uses public concepts and invented numbers. It needs no credentials, customer media,
network listener or model artifact. If you later use a real endpoint, use an approved private
environment and synthetic prompts; keep access tokens and private outputs out of study notes.
Model downloads and remote-code execution have a separate trust boundary: pin reviewed artifacts
and do not enable arbitrary model repository code as a shortcut.

The existing serving reference and attention deep dive are optional references when a term needs
more detail:

- `/Users/ana.rodrigues/Desktop/hooman/hs_scripts/claude/dev_research/learning/inference-baseline.md`
- `/Users/ana.rodrigues/Desktop/hooman/hs_scripts/claude/dev_research/learning/attention.md`

Their old platform setup and version statements remain historical. They do not require recreating
the former lab layout or assume a currently available H200. This lesson has not exercised an
Adobe endpoint or inspected a currently deployed inference engine.

## 11. Separately: the explanation to practice after the exercise

Without the guide, explain this to a colleague:

> “The request becomes token IDs and vectors. A decoder transformer uses causal attention and
> learned projections to produce next-token scores. Prefill processes the known prompt and
> builds K/V state; decode uses that state to generate subsequent tokens. Weights remain fixed
> during inference, but request cache and activations consume memory. I would size weights and
> KV separately, then measure queue delay, first-token latency and token intervals before choosing
> an optimization.”

Then defend one changed constraint: twice the context, twice the requests, fewer K/V heads, or a
queue-dominated first-token delay. The criterion is explaining the reason, not reciting this text.

## 12. Sources and scope

The mathematics and examples are a teaching composition. Source verification supports individual
mechanisms; it does not certify a complete serving deployment or Hooman's performance. Current
primary-source checks for this packet are recorded below before final delivery.

**Checked November 15, 2026:** high confidence in the scoped documented mechanisms and checked
arithmetic. The workload, model configuration and serving trace are invented exercise inputs;
performance tendencies are conditional design reasoning, not measured outcomes.

| Concept | Checked primary source and scope |
|---|---|
| Tensor shapes, gradients and training loop | PyTorch [matmul](https://docs.pytorch.org/docs/2.15/generated/torch.matmul.html) and [optimization tutorial](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html): batched matrix dimensions, backward/optimizer steps and evaluation controls. The local list exercise demonstrates arithmetic, not autograd. |
| Chat serialization and next-token objective | Hugging Face [chat templates](https://huggingface.co/docs/transformers/v5.23.0/en/chat_templating) and [causal language modeling](https://huggingface.co/docs/transformers/v5.23.0/en/tasks/language_modeling): model-specific control tokens, token sequences and causal prediction. |
| Decoding controls | Hugging Face [generation configuration](https://huggingface.co/docs/transformers/en/main_classes/text_generation): temperature changes next-token probabilities during generation. |
| Evaluation and leakage | scikit-learn [common pitfalls](https://scikit-learn.org/1.9/common_pitfalls.html#data-leakage) and [cross-validation](https://scikit-learn.org/1.9/modules/cross_validation.html): held-out evaluation and fitting preprocessing on training data. Group/time splitting is a task-dependent teaching application. |
| Attention and GQA | Original [Transformer paper](https://arxiv.org/html/1706.03762) and [GQA paper](https://arxiv.org/html/2305.13245): scaled attention and query groups sharing K/V heads. Paper-specific speed/quality results are not adopted here. |
| Attention IO implementation | Original [FlashAttention paper](https://arxiv.org/abs/2205.14135): exact attention using tiling to reduce HBM reads/writes. No backend choice or hardware speed claim is inferred. |
| Cache shape and growth | Hugging Face [cache explanation](https://huggingface.co/docs/transformers/v5.23.0/en/cache_explanation): per-layer K/V tensors and appending generated context. The KV formula is derived payload arithmetic with the stated architecture assumptions. |
| Latency boundaries | vLLM [benchmark latency metrics](https://docs.vllm.ai/en/latest/benchmarking/cli/#understanding-the-latency-metrics) and [engine metrics](https://docs.vllm.ai/en/latest/design/metrics/): client/server boundaries and differing ITL/TPOT conventions. The exercise explicitly defines its own observations. |
| Compute versus bandwidth | NVIDIA [matrix multiplication performance guide](https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html): arithmetic-intensity reasoning as a simplified rule of thumb. Its older-device examples are not estimates for current hardware. |
| SFT and preference training | Hugging Face TRL [SFT trainer](https://huggingface.co/docs/trl/en/sft_trainer) and [DPO trainer](https://huggingface.co/docs/trl/en/dpo_trainer): supervised examples and preference-pair training. These are orientation references, not required training labs. |

**Internal-access limit:** neither `/home/colligo/colligo` nor
`/Users/ana.rodrigues/Desktop/hooman/colligo` was available at the checked Mac paths. No current
Adobe implementation was inspected for this packet. Earlier internal observations in the retained
references remain dated observations. The real Git checkout here is under
`/Users/ana.rodrigues/Desktop/hooman/hs_scripts`; this session did not verify Pluto's durable-home
placement or backup service. Only small source/study files were created, with no bulk artifacts.

## 13. Exercise answer key

<details>
<summary>Open after attempting the separate lesson 2 exercise</summary>

These are reference answers to the companion questions, not evidence of Hooman's independent
performance. Consult only the part needed to repair a gap.

**A — Request path.** Messages are serialized with the model's chat template and tokenized into
IDs. Embeddings turn IDs into vectors; transformer layers produce representations; an output
projection produces logits and a decoding policy chooses a token. Prefill handles known prompt
tokens and builds K/V; subsequent decode steps reuse and extend K/V. Parameters remain fixed
during ordinary inference, while activations and request state change. The application must still
supply/persist conversation history as required by its product contract.

**B — Arithmetic and shapes.**

```text
[[1, 2], [3, 4]] @ [[5, 6], [7, 8]]
    = [[19, 22], [43, 50]]

[3, 5, 4] @ [4, 6] → [3, 5, 6], with 90 output elements
```

The contraction dimension is four. A `[5, 6]` matrix has the wrong input dimension. Identity
multiplication leaves the original matrix unchanged. This key supplies expected results; writing
and running the multiplication is the learner's task, not a recorded successful code execution.

**C — Training and evaluation.** With `x = 3`, `y = 9`, `w = 1`, prediction is `3`, squared loss
is `36`, and gradient is `2 × (3 − 9) × 3 = −36`. The update gives `w = 2.8`, prediction `8.4`
and loss `0.36`. An inference-only pass uses weights without a gradient-based update.

Worsening validation performance alongside better training loss can reflect overfitting or a
different/shifted validation distribution; preprocessing or label problems are also possibilities.
Inspect split boundaries, learning curves and data/error distributions rather than choosing a cause
from the curves alone. Related clips crossing train/test can leak source-specific information;
grouping by source video is a reasonable boundary when the goal is performance on new source videos.
Whole-dataset preprocessing lets held-out data influence the fitted transformation. A lower
language-model loss does not establish factual accuracy: evaluate a held-out task set against the
product's answer-quality criteria. Temperature changes token choice; SFT changes learned weights.

**D — Memory.** Baseline raw weights are 14 billion bytes, approximately 13.04 GiB. K/V is
128 KiB per cached token, 0.5 GiB per 4,096-token request, and 4 GiB for eight requests. Their
sum is approximately 17.04 GiB. Activations, workspaces, runtime/cache-allocation overhead and
architecture-specific extras are excluded.

| Independent change | KV payload | Raw weights + KV payload |
|---|---:|---:|
| Baseline | 4 GiB | 17.04 GiB |
| 8,192 cached tokens per request | 8 GiB | 21.04 GiB |
| 16 baseline-length requests | 8 GiB | 21.04 GiB |
| 32 K/V heads | 16 GiB | 29.04 GiB |
| One-byte raw weights, BF16 K/V | 4 GiB | 10.52 GiB |

The 32-K/V-head case already exceeds the assumed 24 GiB device before other allocations.
The other payload sums alone do not establish that actual execution fits. One-byte weights
would also need a real representation's quantization metadata and quality checks.

**E — Trace arithmetic and diagnosis.**

| Request | Queue wait | TTFT | Mean inter-token time | End-to-end latency |
|---|---:|---:|---:|---:|
| A | 0 ms | 80 ms | 20 ms | 880 ms |
| B | 0 ms | 400 ms | 20 ms | 1,200 ms |
| C | 500 ms | 580 ms | 20 ms | 1,380 ms |
| D | 0 ms | 80 ms | 40 ms | 1,680 ms |

B differs from A before the first token, with a longer prompt and no observed queue wait.
Longer prefill is a hypothesis: collect tokenization, engine prefill and delivery timings before
assigning the entire difference to GPU compute. C spends 500 ms waiting, so inspect admission,
queue/scheduler state and available execution capacity first. D has larger generation intervals;
inspect decode load, context/batch composition, memory traffic and delivery overhead. The trace
does not uniquely identify a bottleneck.

A batching comparison should hold the model, hardware, precision, prompt/output-length workload,
arrival pattern and relevant settings fixed while changing the batching control. Measure aggregate
tokens per explicit wall-clock window as well as queue wait, TTFT, token delays, errors and quality.
Four invented examples establish neither p99 nor maximum capacity. Aggregate throughput under
concurrency is not obtained by taking the reciprocal of a mean per-request token interval.

</details>
