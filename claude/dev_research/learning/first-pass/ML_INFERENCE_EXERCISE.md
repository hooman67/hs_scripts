# Lesson 2 — ML and Inference Fundamentals Exercise

Prepared: **2026-11-15**. This is an assignment, not a completed exercise or benchmark.
Use the worked guide first when concepts are unfamiliar:
`/Users/ana.rodrigues/Desktop/hooman/hs_scripts/claude/dev_research/learning/first-pass/ML_INFERENCE_GUIDE.md`.

## Start here

After finishing the video-job clarifications, make one short design attempt using the existing
prompt at `/Users/ana.rodrigues/Desktop/hooman/hs_scripts/claude/dev_research/learning/first-pass/STUDY_GUIDE.md`.
Send a diagram, acceptance rule, ownership/publication rule and late-worker trace. Note any part
for which you reopened the guide. A remaining gap is useful evidence; it is not a reason to study
every queue product before starting the next fundamentals topic.

Then read lesson 2's guide and attempt the tasks below. For unfamiliar parts, repair understanding
before the closed-book explanation. There is no requirement to allocate a GPU, install PyTorch,
download weights or launch a network service.

## A. Draw and explain one generation request

Draw the path from two chat messages to an output token. Label the chat template, token IDs,
embedding vectors, transformer, logits, token-selection policy, prefill, decode and KV cache.
Explain each label in your own words, including:

1. Why are a chat template and tokenizer different responsibilities?
2. Which quantities are learned and which change during an ordinary inference request?
3. Why can prompt positions be processed together, while later output choices depend on earlier ones?
4. Why is a KV cache not a persistent store of the customer's conversation?

## B. Execute a small tensor calculation on your CPU

Use ordinary Python lists or an existing numerical library. Write a function that multiplies
two compatible two-dimensional matrices. It should reject incompatible dimensions.

```python
a = [[1, 2], [3, 4]]
b = [[5, 6], [7, 8]]
```

Compute `a @ b` manually first, then run your function and compare. Also try multiplication
by an identity matrix and one incompatible-shape input. This is a shape/arithmetic exercise,
not a benchmark or a replacement for the timed-coding stage.

Next, reason about a model projection without allocating the arrays:

```text
X shape = [3, 5, 4]
W shape = [4, 6]
```

What is `X @ W`'s shape? How many output elements does it contain? Which dimension contracts?
What breaks if `W` has shape `[5, 6]` instead?

If useful, save your solution at:
`/Users/ana.rodrigues/Desktop/hooman/hs_scripts/claude/dev_research/learning/first-pass/ML_INFERENCE_ATTEMPT.py`.
This optional source file need only contain your small calculation and checks.

## C. Distinguish learning, testing and product quality

For `prediction = w × x`, `x = 3`, target `y = 9`, initial `w = 1`, squared loss, and learning
rate `0.05`, calculate the prediction, loss, gradient with respect to `w`, and one update.
Explain what would change in an inference-only pass.

Then answer these scenarios:

1. Training loss improves but validation performance worsens. What are two plausible causes,
   and what evidence would distinguish them?
2. Clips from the same source video occur in both training and test. Why can this overstate
   generalization to new source videos? What split boundary would you use?
3. You fit preprocessing statistics on the whole dataset before splitting. What information
   crossed the evaluation boundary?
4. A fine-tuned chatbot has lower next-token loss. Does that prove its factual answers improved?
   Name a product-level measurement you would want.
5. Does changing temperature update learned parameters? Contrast it with SFT.

## D. Make and defend a memory estimate

These are **fictional exercise inputs**, not a benchmark or a real model configuration:

| Input | Value |
|---|---|
| Stored parameters | exactly 7,000,000,000 |
| Decoder layers | 32, all using ordinary full-context attention |
| Query heads / K/V heads | 32 / 8 |
| Head dimension | 128 |
| Stored weights / K/V representation | BF16 / BF16, two bytes per element |
| Active requests | 8 |
| Cached tokens per request | 4,096, including cached prompt and generated context |
| Device capacity | 24 GiB, one device, no offload or sharding |
| Cache simplifications | no prefix sharing, compression, windowing, padding or block overhead |

Calculate raw weight bytes and GiB, KV bytes per cached token, total KV GiB and their sum.
Keep the factor of two for K and V visible. Say what storage your calculation excludes.

Handle each changed constraint **independently**, starting from the baseline:

1. Each request has 8,192 cached tokens.
2. There are 16 requests with 4,096 cached tokens each.
3. There are 32 K/V heads rather than 8.
4. Raw weights use one byte per parameter while K/V remains BF16. Ignore quantization
   metadata only for this arithmetic, and state that omission.

Which case definitely exceeds 24 GiB from weights plus KV payload alone? Why doesn't a payload
estimate below 24 GiB guarantee that the workload runs without an out-of-memory failure?

## E. Interpret a supplied serving trace

This is a **synthetic teaching trace**, not an endpoint measurement. Times are seconds on one
common illustrative clock. Arrival is the specified request boundary, processing start is the
scheduler marker, and first/last are token-delivery observations. Every row delivers 41 output
tokens. Real instruments require matching timing boundaries and appropriate clocks.

| Request | Prompt tokens | Arrival | Processing start | First token | Last token | Output tokens |
|---|---:|---:|---:|---:|---:|---:|
| A | 128 | 0.00 | 0.00 | 0.08 | 0.88 | 41 |
| B | 4,096 | 0.00 | 0.00 | 0.40 | 1.20 | 41 |
| C | 128 | 0.00 | 0.50 | 0.58 | 1.38 | 41 |
| D | 128 | 0.00 | 0.00 | 0.08 | 1.68 | 41 |

For each row calculate:

- Queue wait = `processing_start − arrival`.
- TTFT = `first_token − arrival`.
- Mean inter-token time = `(last_token − first_token) / (output_tokens − 1)`.
- End-to-end latency = `last_token − arrival`.

Use milliseconds when comparing delays. A 41-token response has 40 intervals after its first
token. This is the exercise's explicit mean-TPOT convention, not a promise that every serving
library defines that metric identically.

Then explain:

1. What differs between A and B? What phase would you investigate, and what timing detail
   would you collect before attributing the difference to GPU prefill?
2. Why does C's long TTFT suggest a different first investigation from B's?
3. What differs between A and D? Name a possible cause and a measurement to check it.
4. Why do these four traces not establish p99 latency or the service's capacity?
5. What comparison would test whether a larger batch helps aggregate throughput while
   hurting individual latency? State the workload/configuration you would hold fixed.

## What to send back

Send your request-path diagram, tiny calculation/code, learning/evaluation answers, memory
arithmetic and completed trace table. Finish with a five-minute explanation from memory and
list the two parts that remain unclear. Label any portion for which you used the guide.

The review will check shape reasoning, training versus inference, leakage, memory assumptions,
timing arithmetic and evidence-based diagnosis. No score or mastery is inferred from receiving
this packet. Once a representative attempt identifies the gaps, repair the important ones
and start the planned timed-coding stage; do not extend fundamentals into an entire ML course.
