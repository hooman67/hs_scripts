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

<details>
<summary>Examples and explanation for every step in the request path</summary>

**Question:** “Add a collapsable section under this table that gives examples for each row.
Along with more explaination.”

**Answer:** Follow one request: a customer asks, “Why is the sky blue?” The token IDs, vectors,
weights and scores below are invented teaching values. They are not outputs from a real tokenizer
or a measured model run. A real vocabulary and vector width are much larger.

| Step | Concrete example | What is happening |
|---|---|---|
| Customer's messages | `[{"role": "system", "content": "Answer briefly."}, {"role": "user", "content": "Why is the sky blue?"}]` | The application holds structured messages. The role identifies who supplied each message; content holds its text. Relevant earlier conversation can be included too. |
| Chat template | `[SYSTEM]Answer briefly.[END][USER]Why is the sky blue?[END][ASSISTANT]` | A template puts the messages into the order and boundary format expected by the model. The final assistant marker invites the model to continue with an answer. These markers are fictional; use the actual model's template. |
| Tokenizer | The question might be split into `Why`, ` is`, ` the`, ` sky`, ` blue`, `?`, with toy IDs `[101, 42, 9, 812, 506, 30]`. | Each token maps to an integer vocabulary entry. Spaces can belong to tokens. The instructions and template markers also contribute model input; this short list shows only the question portion. A different tokenizer can split the same text differently. |
| Embedding lookup | Toy token ID `812` selects an embedding row such as `[-0.2, 0.4, 0.9]`. | A learned table turns an integer ID into a vector the model can compute with. An ID is an address, not a numeric measure of meaning: ID `812` is not “more sky” than ID `506`. The vector coordinates do not have simple human labels. |
| Transformer layers | After processing the prompt, a toy final-position representation is `h = [1, 0.5, 0]`. | Attention mixes information from allowed earlier positions, and feed-forward layers transform the representations. The last prompt position can therefore reflect the question, instructions and earlier conversation. This vector is contextual; it is different from a token's initial embedding. |
| Output projection | `h @ W` gives toy logits `[2, 1, 0]` for three candidate tokens: `Light`, `Water`, `Bananas`. | A learned projection turns the contextual vector into one score per vocabulary token. We show a three-token toy vocabulary to make the arithmetic visible. Logits are scores, not probabilities or complete answers. |
| Decoding policy | With temperature `T = 1`, those logits give probabilities of approximately `66.52%`, `24.47%`, and `9.00%`. Greedy selection chooses `Light`; sampling could choose another candidate. | The policy selects the next token using the scores and settings. Sampling is a probability-weighted draw, not necessarily selection of the largest probability. Learned weights stay unchanged. |
| Append and advance | Append the selected token `Light` to the generated IDs. Process it to obtain scores for the next token, perhaps ` scatters`. | Generation extends the sequence and updates request state. In a conventional KV-cached implementation, processing the newly selected token adds its keys and values; simply selecting it does not already compute those keys and values. Past cached state is reused. |
| Stream and stop | The caller receives fragments such as `Light `, then `scatters `, then the rest of the answer. An end marker or output limit ends generation. | Token IDs are converted back into text and delivered incrementally. Network chunks are not guaranteed to match individual tokens or words. The service can buffer fragments, and stop markers may be consumed without appearing in the displayed answer. |

For the output-projection row, the toy matrix can be:

```text
h = [1, 0.5, 0]
W = [[1, 1, 0],
     [2, 0, 0],
     [0, 0, 1]]

h @ W = [2, 1, 0]
```

There are two phases within this flow. **Prefill** processes the supplied prompt and produces
scores for the first response token. **Decode** processes newly selected tokens and produces
subsequent scores. The service does not normally re-run the chat template and tokenize the whole
conversation after each generated token; it advances the existing request's token sequence and
cache. A later, separate customer request still needs the relevant conversation supplied again
or retrieved by a service that stores it.

The toy example shows mechanics, not a rule that a model always selects a scientifically correct
answer. A high next-token probability does not establish truth.

Source: Hugging Face [chat templates](https://huggingface.co/docs/transformers/en/chat_templating)
and the causal-generation/cache sources already listed in section 12.

</details>

<details>
<summary>Question: What is the final-position representation h, and how does it become logits and a token?</summary>

**Question:** “I don't understand these parts: Transformer layers ... a toy final-position
representation is `h = [1, 0.5, 0]`; Output projection ... `h @ W` gives toy logits `[2, 1, 0]`;
Decoding policy ... probabilities approximately `66.52%`, `24.47%`, `9.00%` ... Put more details
there on these things. Give more theory and examples. Like what is a final position representaton
(`h`)?”

**Answer:** The short version is:

```text
one vector per input position
        ↓ many transformer blocks
one contextual vector per position
        ↓ take the row at the final input position
h
        ↓ learned output projection
one logit per vocabulary token
        ↓ softmax and decoding policy
one selected next token
```

`h` is not a token ID, a word, a probability or the complete answer. It is the model's final
hidden-state vector at the sequence position from which it will predict the next token.

### Position, feature coordinate and layer are three different axes

Suppose the serialized model input contains `S` token positions and the model's hidden width is
`H`. At the start, token embeddings plus the architecture's positional information form a matrix:

```text
initial representations: E, shape [S, H]
```

- A **position** chooses one row: which token location in the sequence.
- A **feature coordinate** chooses one number inside that row: one of the `H` hidden values.
- A **network layer** identifies how far the representations have traveled through the model.

Every transformer block produces another `[S, H]` array. Schematically:

```text
Z0 = token embeddings plus positional information       # [S, H]
Z1 = transformer_block_1(Z0)                            # [S, H]
Z2 = transformer_block_2(Z1)                            # [S, H]
...
ZL = transformer_block_L(previous output)               # [S, H]
H_final = final_normalization_if_the_model_uses_one(ZL) # [S, H]

h = H_final[S - 1, :]                                   # [H]
```

The exact order of attention, feed-forward, residual and normalization operations is
architecture-dependent. The important point here is that there is still one hidden vector for
each sequence position after the final block, and `h` selects the whole vector at the final
position. “Final position” does **not** mean the final coordinate of a vector.

It also does not always mean the last ordinary word visible in the user's question. In the
fictional template above, the serialized input ends with an `[ASSISTANT]` control marker. The
position used to request the first response token can therefore be associated with that marker,
depending on the model's actual template and generation interface. The marker is part of the
input sequence, not a human-readable answer token.

### Why the final-position vector contains context

At the embedding lookup, a token has a learned starting vector. For ordinary fixed weights, the
same token ID selects the same embedding row. After causal self-attention and the other block
operations, its hidden vector depends on the allowed earlier context.

For example, these labels are deliberately word-like rather than claims about a real tokenizer:

```text
[river, bank]
[savings, bank]
```

The starting embedding for the same final `bank` token can be identical. Its later contextual
representation can differ because one sequence contains `river` and the other contains `savings`.
That is why `h` is called a **contextual representation** rather than simply the final token's
embedding.

In a causal decoder, position `s` may use information from positions `0` through `s`, but not from
future positions. The last input position can therefore incorporate information from all allowed
prompt positions. “Incorporate” does not mean that every fact is perfectly retained or that one
coordinate has a stable human label such as “blueness.” Information is distributed through learned
features, and a model can still omit, confuse or hallucinate facts.

### A tiny attention-mixture illustration

One attention head calculates relevance scores from queries and keys, applies a causal mask and
softmax, then uses the resulting weights to mix value vectors:

```text
attention_weights = softmax(Q @ K_transpose / sqrt(D) + causal_mask)
attention_result  = attention_weights @ V
```

Suppose the final position has already produced these **assumed** attention weights over three
allowed positions:

```text
weights = [0.2, 0.3, 0.5]

V = [[1, 0, 0],
     [0, 2, 0],
     [0, 0, 3]]
```

The weighted mixture is:

```text
0.2 * [1, 0, 0]
+ 0.3 * [0, 2, 0]
+ 0.5 * [0, 0, 3]
= [0.2, 0.6, 1.5]
```

This demonstrates how one position can mix information associated with earlier positions. The
weights were supplied rather than derived from a real `Q` and `K`. The mixture is also **not** the
guide's `h = [1, 0.5, 0]`: attention output is followed by learned projections and, across the
model, residual paths, normalization, feed-forward transformations and more layers. The final `h`
is the result after that full stack.

The value `h = [1, 0.5, 0]` is invented to make the following arithmetic visible. It cannot be
derived from the English question without the actual tokenizer, model architecture and learned
weights.

### How h becomes one logit per candidate token

The output head maps hidden width `H` to vocabulary size `V`:

```text
h shape = [H]
W shape = [H, V]
h @ W   = [V] logits
```

Each column of `W` contributes to one vocabulary candidate. Reuse the exact toy values already in
the guide:

```text
h = [1, 0.5, 0]

W = [[1, 1, 0],
     [2, 0, 0],
     [0, 0, 1]]

toy vocabulary columns:
column 0 -> Light
column 1 -> Water
column 2 -> Bananas
```

Take the dot product of `h` with each column:

```text
logit(Light)   = [1, 0.5, 0] dot [1, 2, 0]
               = 1*1 + 0.5*2 + 0*0 = 2

logit(Water)   = [1, 0.5, 0] dot [1, 0, 0]
               = 1*1 + 0.5*0 + 0*0 = 1

logit(Bananas) = [1, 0.5, 0] dot [0, 0, 1]
               = 1*0 + 0.5*0 + 0*1 = 0

h @ W = [2, 1, 0]
```

Those three numbers are **logits**: unrestricted real-valued scores. They are not probabilities
and do not need to sum to one. Only their relative values affect the softmax probabilities.

A real model has one score for every vocabulary entry, often many thousands rather than three.
The output head can have an optional bias, and some architectures tie its weights to the token
embedding table. Those are model-specific choices; the no-bias three-token matrix here is the
defined teaching example, not a claim about every model or a proprietary GPT implementation.

### How logits become the shown probabilities

For positive temperature `T`, softmax gives candidate `j` this probability:

```text
p_j = exp(logit_j / T) / sum(exp(logit_i / T) for every candidate i)
```

At `T = 1`, dividing by temperature leaves the toy logits `[2, 1, 0]` unchanged:

```text
exp(2) = 7.38906
exp(1) = 2.71828
exp(0) = 1
total  = 11.10734

P(Light)   = 7.38906 / 11.10734 = 0.66524 = 66.524%
P(Water)   = 2.71828 / 11.10734 = 0.24473 = 24.473%
P(Bananas) = 1       / 11.10734 = 0.09003 =  9.003%
```

Softmax converts scores into positive numbers that sum to one. Adding the same constant to every
logit would not change these probabilities because the common exponential factor cancels.

Temperature changes the sharpness before sampling. A lower positive temperature enlarges score
differences; a higher temperature shrinks them. A `temperature = 0` API setting is normally a
special greedy-mode convention, not division by zero in the displayed formula. Supported ranges
and exact behavior belong to the particular generation API.

### Greedy choice and random sampling are different policies

Greedy decoding selects the largest score or probability, so this step chooses `Light`.

Sampling treats the probabilities as interval sizes on `[0, 1)`. One possible arrangement is:

```text
Light:   [0.00000, 0.66524)
Water:   [0.66524, 0.90997)
Bananas: [0.90997, 1.00000)
```

An illustrative random draw `u = 0.75` lands in the `Water` interval, so sampling would choose
`Water` even though `Light` is the most likely single candidate. A different draw can produce a
different token. Top-p, top-k and other controls can change the candidate distribution before the
draw; they are intentionally absent from this example.

These are probabilities for the **next token under the model and current decoding setup**, not
calibrated probabilities that an entire statement is true. A high `Light` logit does not establish
the scientific correctness of the eventual answer.

### What happens after one token is selected

Suppose the policy selects `Light`:

```text
prompt positions -> final prompt h -> logits -> select Light
append Light
process the appended token with the prior request state
-> new contextual final-position vector
-> new logits
-> select the next token, perhaps " scatters"
```

Selecting `Light` does not update learned weights. During the next decode step, the model processes
that selected token, reuses the prior K/V cache in a conventional cached implementation, adds the
new token's K/V state, and produces a new hidden vector and logits. The previous `h` was the state
used for one next-token decision; it was not a permanent summary used unchanged for the rest of the
answer.

Training is what learns the embedding table, attention/feed-forward weights and output head `W`.
Ordinary inference repeatedly applies those fixed weights while token IDs, hidden states,
activations and request-local cache change.

**Sources checked November 16, 2026:** the original
[Transformer paper](https://arxiv.org/html/1706.03762) defines masked decoder attention,
position-wise feed-forward transformations, residual/normalization structure and a learned linear
map plus softmax for next-token probabilities. Hugging Face's
[causal language-modeling documentation](https://huggingface.co/docs/transformers/v5.23.0/en/tasks/language_modeling)
supports next-token prediction, and its
[generation documentation](https://huggingface.co/docs/transformers/en/main_classes/text_generation)
distinguishes greedy decoding from multinomial sampling. The hidden values, attention values,
candidate tokens and random draw above remain invented teaching examples; no model was run and no
undisclosed model architecture is inferred.

</details>

<details>
<summary>Does this apply to GPT-5.5, or only to decoder-only models?</summary>

**Question:** “Also does this stuff apply to say GPT-5.5 models? or no (this decoder only things).”

**Answer:** Yes, this is a useful conceptual foundation for GPT-5.5's text generation. It is not
a verified diagram of that proprietary model's exact internals. The official GPT-5.5 model page
documents text input/output, image input, reasoning-token support and streaming. It does not
provide the attention layout and implementation details needed to assert that every formula
and architecture choice in this lesson is its exact configuration.

**Decoder-only** describes a transformer architecture: its text-generation stack uses causal
attention to continue a sequence, rather than a separate encoder stack feeding a decoder stack
as in a classic encoder–decoder transformer. It does not mean “cannot accept images,” “cannot
reason,” or “can only produce short answers.” Image inputs can require additional processing
beyond the text tokenizer shown here. Reasoning and tool use can also add work before or between
pieces of user-visible output.

| Lesson idea | How to use it when thinking about GPT-5.5 |
|---|---|
| Structured messages become model input | Applicable as a conceptual distinction. A hosted API handles its required input formatting internally; you should not invent and send your own raw control-token template instead of the documented API messages. |
| Text generation involves token choices | Useful for understanding output lengths, incremental generation and decoding. Do not assume all generated reasoning or control content is streamed as visible prose. |
| Weights, activations and request state are different things | Useful for understanding why generating an answer is not ordinarily a training update, and why context/state can change while model parameters stay fixed. |
| Exact head counts, GQA/MQA choice and KV-memory formula | Architecture-dependent. The conventional cache formulas below cannot give GPT-5.5's actual memory use without its real configuration and implementation. |
| Streaming delivers output incrementally | Documented as supported. It does not reveal the internal GPU scheduling, attention kernels or precise correspondence between network events and model steps. |

Use this lesson to understand the questions to ask about a generation system. Keep numerical
estimates scoped to an open or otherwise documented model whose architecture is known.

Source checked for this clarification: [official OpenAI GPT-5.5 model documentation](https://developers.openai.com/api/docs/models/gpt-5.5).
The distinction about undisclosed internals is limited to what this model page establishes;
no private model implementation was inspected.

</details>

An **embedding** is a learned vector associated with a token. A **logit** is an unnormalized
score: the output projection produces one score per vocabulary entry. A **softmax** converts
those scores into probabilities that sum to one. The decoding policy can pick the largest score
or sample from a distribution. An end-of-sequence marker, requested stop sequence or output limit
can end generation.

**Sampling temperature** is a decoding setting that rescales logits before sampling:
`softmax(logits / T)` for positive `T`. Lower positive temperatures concentrate probability on
higher-scoring tokens; higher temperatures flatten the distribution. The setting changes token
selection, not the learned weights. Greedy selection chooses the highest-scoring token directly.

<details>
<summary>Temperature worked example: logits, softmax, probability changes and allowed values</summary>

**Question:** “Give me exact example of logits and values for T. Give me the equation for
softmax. And explain why lower temps concentrate prob on higher scoring etc. What's the
min/max valus for T.”

**Answer:** A logit is an unrestricted real-valued score. It can be positive, zero or negative;
it is not itself a probability. For this invented three-token vocabulary, suppose the model
produces the following scores at one generation step:

| Candidate token | Logit |
|---|---:|
| `Light` | 2 |
| `Water` | 1 |
| `Bananas` | 0 |

These same model scores will be used for every temperature below. Only decoding changes.

**The softmax equation.** For scores `z_1, ..., z_V`, with `V` vocabulary entries:

```text
softmax(z)_i = exp(z_i) / sum(exp(z_j) for j = 1, ..., V)

with temperature T > 0:
p_i(T) = exp(z_i / T) / sum(exp(z_j / T) for j = 1, ..., V)
```

Here `exp(x) = e^x`, and `e` is approximately `2.71828`. Exponentiation makes every term
positive; division by their total makes the probabilities sum to one.

At `T = 1`, the calculation is:

```text
exp(2) ≈ 7.38906
exp(1) ≈ 2.71828
exp(0) = 1
total  ≈ 11.10734

P(Light)   ≈ 7.38906 / 11.10734 = 0.66524
P(Water)   ≈ 2.71828 / 11.10734 = 0.24473
P(Bananas) ≈ 1       / 11.10734 = 0.09003
```

**Concrete temperature values.** All rows use the same logits `[2, 1, 0]`:

| Temperature `T` | Rescaled logits `z / T` | `P(Light)` | `P(Water)` | `P(Bananas)` |
|---|---|---:|---:|---:|
| 0.1 | `[20, 10, 0]` | 99.9955% | 0.0045% | about 0.000000206% |
| 0.5 | `[4, 2, 0]` | 86.6813% | 11.7310% | 1.5876% |
| 1 | `[2, 1, 0]` | 66.5241% | 24.4728% | 9.0031% |
| 2 | `[1, 0.5, 0]` | 50.6480% | 30.7196% | 18.6324% |
| 10 | `[0.2, 0.1, 0]` | 36.7165% | 33.2225% | 30.0610% |

Percentages are rounded. `T = 10` is a mathematical example, not a claim that a particular API
accepts it. Other generation controls such as top-p filtering are absent from this toy example.

**Why lower temperatures concentrate probability.** Division by a small positive number
enlarges the differences between scores. The exact probability ratio between two candidates is:

```text
p_i(T) / p_j(T) = exp((z_i - z_j) / T)
```

The common softmax denominator cancels. `Light` is one logit point above `Water`, so:

```text
T = 0.5: P(Light) / P(Water) = exp(2)   ≈ 7.39
T = 1:   P(Light) / P(Water) = exp(1)   ≈ 2.72
T = 2:   P(Light) / P(Water) = exp(0.5) ≈ 1.65
```

Lower `T` therefore gives a higher-scoring candidate a stronger advantage. Higher `T` shrinks
the score differences; their exponentials become more similar, so probabilities flatten.
For finite logits in a finite vocabulary, as `T` grows without bound each probability tends
to `1 / V`. As `T` approaches zero from above, probability concentrates on the highest logit;
if several logits tie for the maximum, the limiting mass is shared among those tied candidates.
Equal logits remain equally probable at every positive temperature.

Temperature preserves the ordering of logits for `T > 0`: `Light` remains the most likely
candidate in every row. It changes the strength of the preference, not which score is largest.
It also does not guarantee correctness. Increasing temperature makes lower-scoring continuations
more likely, including undesirable ones.

**Minimum and maximum depend on whether we mean the formula or a product setting:**

| Setting | Minimum/maximum and meaning |
|---|---|
| Mathematical temperature in this formula | Any finite `T > 0`. There is no smallest positive value and no finite maximum. Zero is excluded because division by zero is undefined. |
| A generation engine's `temperature = 0` option | Commonly a special instruction to use greedy selection, not an evaluation of `softmax(z / 0)`. Check the engine's contract. Greedy selection chooses an argmax directly, with an implementation-specific tie rule. |
| OpenAI Chat Completions parameter reference | Documents `0` through `2`, inclusive, for supported uses. A model or reasoning mode can restrict parameter support; this generic range is not proof that every GPT-5.5 mode accepts it. |
| Negative temperature | Outside this lesson's decoding convention. A negative divisor would reverse score ordering; ordinary temperature settings reject it. |

Greedy selection does not need a softmax to find the largest score. Setting temperature to zero
also does not promise bit-for-bit identical results across every backend, model revision or
service execution.

To reproduce the positive-temperature arithmetic without overflowing large exponentials:

```python
import math

def probabilities(logits, temperature):
    if temperature <= 0:
        raise ValueError("This softmax calculation requires T > 0")
    largest = max(logits)
    terms = [math.exp((z - largest) / temperature) for z in logits]
    total = sum(terms)
    return [term / total for term in terms]

print(probabilities([2, 1, 0], 0.5))
# Approximately [0.866813, 0.117310, 0.015876]
```

Subtracting the largest logit from all logits leaves softmax probabilities unchanged: the
common exponential factor cancels from numerator and denominator.

Sources: Hugging Face [generation configuration](https://huggingface.co/docs/transformers/en/main_classes/text_generation)
and the [official OpenAI Chat Completions parameter reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create).
The example probabilities are locally checked arithmetic, not measured model outputs.

</details>

These steps are the work inside a text-generation worker or engine. The previous lesson's
database, storage and recovery design describes how an application manages durable jobs around
computation. A chat endpoint can instead stream a response over the caller's HTTP connection;
it does not automatically need the same durable-job queue.

<details>
<summary>Simple Python example: stream text to an HTTP caller</summary>

**Question:** “In collapsible give me simple python code that streams a text to a http caller.”

**Answer:** This example uses only Python's standard library. The server sends one HTTP
response body in several pieces, rather than building the whole body before sending it.
The text is simulated so that the delivery mechanism is visible without downloading a model.

```python
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import time

class TextHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        if self.path != "/stream":
            self.send_error(404)
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Connection", "close")
        self.end_headers()
        self.close_connection = True

        chunks = ["Light ", "scatters ", "more strongly ",
                  "at shorter wavelengths.\n"]
        for chunk in chunks:
            self.wfile.write(chunk.encode("utf-8"))
            self.wfile.flush()
            time.sleep(0.4)  # Simulate time before another piece is ready.

if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8010), TextHandler)
    print("Open http://127.0.0.1:8010/stream")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
```

If you want to run it, save that block as
`/Users/ana.rodrigues/Desktop/hooman/hs_scripts/claude/dev_research/learning/first-pass/text_stream_example.py`.
That example file is not created by this document addition. In one terminal run:

```bash
python3 /Users/ana.rodrigues/Desktop/hooman/hs_scripts/claude/dev_research/learning/first-pass/text_stream_example.py
```

In a second terminal, use a caller that displays received data without output buffering:

```bash
curl --no-buffer http://127.0.0.1:8010/stream
```

You should see the sentence grow over roughly a second and a half. Stop the server with Ctrl-C.
This is a local teaching server, not a production HTTP deployment.

| Code/action | Meaning |
|---|---|
| `do_GET` | Handle the caller's request for `/stream`. |
| `send_response` and headers | Start one response. They do not finish the response body. |
| `wfile.write` | Write the next bytes of that same response body. |
| `wfile.flush` | Push buffered bytes toward the caller; the network or a proxy may still combine pieces. |
| `Connection: close` | This small example uses connection closure to mark the body's end, rather than a known Content-Length or HTTP chunked framing. |
| Return from the handler | Finish this response and close its connection. The server continues accepting other requests. |

With a real generation engine, replace the fixed chunk list and artificial delay with an iterator
that yields generated text fragments. Text fragments and HTTP/network chunks need not line up
one-to-one with model tokens. A browser UI would read the response incrementally, for example
through `fetch` and its response-body reader, instead of waiting for the whole response text.

There is no database job, outbox or SQS notification in this example: the work belongs to this
live request. If the process or connection fails, this code does not preserve the generation or
resume delivery. Add durable-job storage when the product needs acceptance and recovery across
those failures; streaming alone does not provide that contract.

Source: Python [http.server](https://docs.python.org/3/library/http.server.html), especially
`BaseHTTPRequestHandler` and its output stream. The standard-library server is suitable here
for demonstrating HTTP response delivery, not for serving production traffic.

</details>

<details>
<summary>Question: How does self.close_connection = True actually close the HTTP connection?</summary>

**Question:** “For this line in the example http server you gave:
`self.close_connection = True` How does this actually close the connection? does this mean that
when the function ends/reutnrs, the connection should automatically close”.

**Answer:** Setting the attribute does **not** immediately close the socket. It sets a flag that
`BaseHTTPRequestHandler` checks after the current request handler finishes. In this example,
`do_GET` continues writing every chunk even though the flag is already `True`.

The sequence is:

```text
do_GET starts
  -> response headers are written
  -> close_connection is set to True
  -> all four response-body chunks are still written
  -> do_GET returns
  -> the framework flushes the response stream
  -> its request loop sees close_connection == True and stops
  -> handler/file-wrapper cleanup runs
  -> ThreadingHTTPServer shuts down and closes this accepted client socket
```

The following is deliberately simplified pseudocode showing the relationships. It is not copied
source and omits error handling:

```python
# Simplified BaseHTTPRequestHandler control flow
def handle(self):
    self.close_connection = True
    self.handle_one_request()
    while not self.close_connection:
        self.handle_one_request()

def handle_one_request(self):
    parse_request()
    self.do_GET()       # our method writes chunks and eventually returns
    self.wfile.flush()

# Simplified threaded-server control flow
def process_request_thread(socket):
    try:
        construct_handler_and_run_it(socket)
    finally:
        shutdown_request(socket)  # shut down writing, then close accepted socket
```

More precisely for the locally inspected CPython 3.9.6 implementation:

1. `ThreadingHTTPServer` has accepted a client socket and constructs the request handler around it.
2. `BaseHTTPRequestHandler.handle_one_request()` calls `do_GET()`. Returning from `do_GET()` returns
   control to this framework method, which flushes `wfile`.
3. `BaseHTTPRequestHandler.handle()` loops for another request only while
   `not self.close_connection`. Because the flag is `True`, it leaves the loop.
4. `BaseRequestHandler` runs `finish()` in a `finally` block. `StreamRequestHandler.finish()`
   flushes and closes its read/write file wrappers.
5. The `ThreadingMixIn` worker's own `finally` block calls `shutdown_request()`. For this TCP server,
   that attempts `socket.shutdown(SHUT_WR)` and then `socket.close()`.

So the short answer is: **yes, returning from `do_GET()` lets this particular framework proceed to
connection cleanup because the flag says not to read another request—but ordinary Python function
return does not automatically close sockets.** The server framework owns the socket and performs
the cleanup.

There are two related lines in the example:

```python
self.send_header("Connection", "close")
self.close_connection = True
```

They serve different audiences conceptually:

- The HTTP response header tells the client that this connection will not persist after the
  response.
- The handler flag tells the CPython server not to wait for another request on this client
  connection.

In the inspected CPython 3.9.6 source, `send_header("Connection", "close")` itself also sets
`self.close_connection = True`. The later explicit assignment is therefore redundant for that
implementation, but makes the teaching example's server-side intent visible. Neither line closes
the socket at the moment it executes.

If the flag stayed `False`, HTTP/1.1 could reuse the same client connection and the handler loop
could read a later request—but only when response framing is valid. This small streaming example
sends neither `Content-Length` nor HTTP chunked framing, so connection closure is what tells the
client where this response body ends. Merely changing the flag to `False` would not supply the
missing framing.

Finally, three lifetimes are separate:

```text
do_GET response finishes        one HTTP response is complete
accepted client socket closes   this client's TCP connection ends
serve_forever keeps running     listening server can accept other clients
```

The later `server.server_close()` in the outer `finally` cleans up the **listening server socket**;
it is not the step that closes this individual response's accepted client socket. TCP shutdown and
close request an orderly local teardown, but exact FIN delivery timing still belongs to the OS and
network; the attribute assignment alone does not promise an instantaneous wire-level close.

**Sources checked November 16, 2026:** the local interpreter is CPython 3.9.6. Its inspected
`BaseHTTPRequestHandler.handle`, `handle_one_request` and `send_header` methods match the
version-pinned CPython [`http/server.py`](https://github.com/python/cpython/blob/v3.9.6/Lib/http/server.py);
the handler cleanup and threaded TCP shutdown path match
[`socketserver.py`](https://github.com/python/cpython/blob/v3.9.6/Lib/socketserver.py). The public
class contracts are documented in Python's [`http.server`](https://docs.python.org/3.9/library/http.server.html)
and [`socketserver`](https://docs.python.org/3.9/library/socketserver.html) documentation. No network
server or listener was run for this clarification.

</details>

For chat, a **chat template** turns structured user/assistant messages into the model's expected
text and control tokens. Arbitrary role dictionaries do not become model input by themselves.
Changing the template can change behavior even with unchanged weights. The application must
supply relevant conversation history; request-local caching is not durable conversational memory.

<details>
<summary>A simple chat template, role dictionaries and conversation history</summary>

**Question:** “Give me example of a simple chat template. Also, I don't understand what you
mean by role dictionaries. Or how they don't become input by themselves.”

**Answer:** A **dictionary** is Python's key/value data structure. A message like the following
is a dictionary with two keys:

```python
{"role": "user", "content": "Why is the sky blue?"}
```

`role` tells the application who supplied this message; `content` holds what they said.
“Role dictionaries” in the paragraph means these message dictionaries, each carrying role
metadata. It is not a separate mathematical structure inside the transformer. Common roles
include `system` for instructions, `user` for the customer's input, and `assistant` for previous
model replies; supported roles depend on the model and interface.

Here is a short conversation stored as a list of those dictionaries:

```python
messages = [
    {"role": "system", "content": "Answer briefly."},
    {"role": "user", "content": "Why is the sky blue?"},
    {"role": "assistant", "content": "Shorter wavelengths scatter more strongly."},
    {"role": "user", "content": "Then why not violet?"},
]
```

The model's tensor computation does not inspect Python keys such as `role` and `content`.
Something must convert that application structure into its expected input representation.
For a text-only causal chat model, a chat template provides the serialization step, followed
by tokenization into IDs and embedding lookup.

**A deliberately simple, fictional template:**

```python
def toy_chat_template(messages):
    parts = []
    for message in messages:
        role = message["role"].upper()
        parts.append(f"[{role}]\n{message['content']}\n[END]\n")
    parts.append("[ASSISTANT]\n")
    return "".join(parts)

prompt_text = toy_chat_template(messages)
print(prompt_text)
```

Its output is:

```text
[SYSTEM]
Answer briefly.
[END]
[USER]
Why is the sky blue?
[END]
[ASSISTANT]
Shorter wavelengths scatter more strongly.
[END]
[USER]
Then why not violet?
[END]
[ASSISTANT]
```

The final assistant marker starts a new reply, so generated text continues after it. The earlier
assistant message is conversation context, not a second instruction to generate an answer there.
The boundary markers let a suitably trained model distinguish the speakers and message endings.
Our `[USER]`, `[END]` and other markers are invented for illustration; this function is not a
production template and should not replace a real model's documented format.

| Representation | Example | Who handles it? |
|---|---|---|
| Application messages | The list of dictionaries above | Your application, SDK or API interface |
| Serialized conversation | Instructions and messages with role/end markers | The model's chat template |
| Token IDs | A list such as `[101, 42, ...]` | The matching tokenizer |
| Token vectors | Numeric rows selected from the embedding table | The model's embedding layer |

For an open model using Hugging Face, its tokenizer can apply the actual stored template and
tokenize in one call:

```python
# tokenizer must be loaded for the particular chat model you intend to run.
input_ids = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_tensors="pt",
)
```

Some models already handle the generation prefix through their template; supported options and
formats vary. The fictional template above needs no model download to understand, whereas this
Hugging Face call requires the actual tokenizer and its dependencies.

When a hosted chat API accepts a list of message dictionaries, its server performs the required
conversion. So “do not become model input by themselves” does not mean the API cannot accept
dictionaries. It means an underlying formatting/tokenization step is necessary. Calling
`str(messages)` or inventing arbitrary role tags is not a substitute for the model's template.
Changing those markers can alter token IDs and how the model interprets the conversation even
when every learned weight remains identical.

**Why conversation history is separate from the KV cache:** the dictionaries above explicitly
include the previous user question and assistant answer. If a new request sends only “Then why
not violet?”, it does not automatically inherit those earlier messages. Your application must
send the relevant history, or a documented stateful service must retrieve it. Request-local K/V
state helps execute the current sequence efficiently; it is not, by itself, a durable conversation
record that survives process loss or attaches itself to every later request.

Source: Hugging Face [chat templates](https://huggingface.co/docs/transformers/en/chat_templating),
which explains conversion of `role`/`content` dictionaries into model-specific token sequences.

</details>

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

<details>
<summary>Question: How is [2, 4, 12] calculated, how does matrix multiplication work, and what are packed variable-length representations?</summary>

**Question:** “In collapsible add more details for part 2 ... explain how this is caluclated?
`X @ W` has shape `[2, 4, 12]` Give me a tutorial of matrix multiplication (i know the basics just
remind me how we do it) Also how to calculate the run time. ‘Modern engines also use packed or
variable-length representations’ ALso what does this mean. give me exampls for each”.

**Answer:** There are three related ideas here:

1. Matrix multiplication takes every row on the left and dots it with every column on the right.
2. For `[2, 4, 8] @ [8, 12]`, the final `8` on the left matches the first `8` on the right and is
   summed over; the other dimensions remain, giving `[2, 4, 12]`.
3. Padding, packing and separate variable-length arrays are different ways to represent sequences
   whose lengths are not all equal.

The values and timings below are teaching examples. They were not produced by a model run or GPU
benchmark.

### Matrix multiplication reminder: row times column

For ordinary two-dimensional matrices:

```text
[M, K] @ [K, N] -> [M, N]
```

The two `K` dimensions must match. To calculate output element `C[i, j]`, take row `i` of the left
matrix and column `j` of the right matrix, multiply matching entries and add them:

```text
C[i, j] = sum(A[i, k] * B[k, j] for k = 0, ..., K - 1)
```

For example:

```text
A = [[1, 2],       B = [[5, 6],
     [3, 4]]            [7, 8]]
```

There are four output cells, so there are four row-column dot products:

```text
C[0, 0] = [1, 2] dot [5, 7] = 1*5 + 2*7 = 19
C[0, 1] = [1, 2] dot [6, 8] = 1*6 + 2*8 = 22
C[1, 0] = [3, 4] dot [5, 7] = 3*5 + 4*7 = 43
C[1, 1] = [3, 4] dot [6, 8] = 3*6 + 4*8 = 50

A @ B = [[19, 22],
         [43, 50]]
```

The inner dimension `K = 2` disappears because each output cell sums across it. `M = 2` left rows
and `N = 2` right columns determine the output shape `[2, 2]`.

### Why `[2, 4, 8] @ [8, 12]` becomes `[2, 4, 12]`

Let:

```text
B = 2   sequences
S = 4   token positions per sequence
H = 8   input features per token
N = 12  output features per token

X shape = [B, S, H] = [2, 4, 8]
W shape = [H, N]    = [8, 12]
Y shape = [B, S, N] = [2, 4, 12]
```

`X` contains `2 × 4 = 8` token vectors. Every token vector has eight input numbers. The same learned
matrix `W` maps each of those eight-number vectors to a twelve-number vector:

```text
one token: [8] @ [8, 12] -> [12]
all tokens: [2, 4, 8] @ [8, 12] -> [2, 4, 12]
```

Element by element, the operation is:

```text
Y[b, s, j] = sum(X[b, s, k] * W[k, j] for k = 0, ..., 7)

b = which sequence, 0 or 1
s = which position, 0 through 3
j = which output feature, 0 through 11
k = the input feature being multiplied and summed, 0 through 7
```

Neither the sequence index `b` nor the position index `s` is mixed by this projection. Only the
eight-feature dimension is contracted. A useful conceptual picture is to flatten the first two
dimensions, apply the matrix, and restore them:

```text
[2, 4, 8] -> view as [8, 8]
[8, 8] @ [8, 12] -> [8, 12]
[8, 12] -> view as [2, 4, 12]
```

This reshape is an explanation, not a required manual step. A tensor library can accept the
original `[2, 4, 8]` tensor and apply the same `[8, 12]` matrix to its batched vectors.

### Calculate the work first; elapsed time needs a machine model

For the straightforward dense `[M, K] @ [K, N]` algorithm, there are `M × N` output cells and each
cell uses a length-`K` dot product:

```text
work grows as O(M * K * N)
common approximate count = 2 * M * K * N FLOPs
```

A **FLOP** is one floating-point operation under the stated counting convention. The common
`2MKN` estimate counts one multiplication and one addition for each term. Hardware often performs
a fused multiply-add instruction, but performance specifications conventionally count that as two
FLOPs.

The exact elementary count for ordinary dot products is slightly smaller because a length-`K` dot
product needs `K` multiplications but only `K - 1` additions:

```text
exact elementary operations = M * N * (K + K - 1)
                            = M * N * (2K - 1)
```

For the projection above, combine batch and positions into `M = B × S = 8`, with `K = 8` and
`N = 12`:

```text
output cells       = 8 * 12 = 96
multiplications    = 96 * 8 = 768
additions          = 96 * 7 = 672
exact simple count = 768 + 672 = 1,440 operations

common GEMM estimate = 2 * 8 * 8 * 12 = 1,536 FLOPs
```

Both numbers can be correct if their conventions are stated. `1,440` counts the literal operations
in 96 separate dot products; `1,536` is the usual convenient `2MKN` performance estimate. Neither
number is milliseconds.

A rough runtime model asks about both compute and data movement:

```text
compute lower bound ~= required FLOPs / effective FLOPs per second
memory lower bound  ~= bytes actually transferred / effective bytes per second

rough elapsed time is at least the larger lower bound,
then can be longer because of launch, scheduling, synchronization,
communication and other overheads.
```

Use **effective** rates for the real precision, kernel, shapes and workload—not only a device's peak
specification. Also define the memory boundary. For this tiny example, counting each FP16 input,
weight and output element once gives a simple payload inventory:

```text
X: 8 * 8  = 64 elements
W: 8 * 12 = 96 elements
Y: 8 * 12 = 96 elements
total     = 256 FP16 elements = 512 bytes
```

That is not a measurement of GPU-memory traffic. Tiling, caches, register reuse, intermediate
operations and repeated loads can make traffic at a particular memory level differ from this
one-copy inventory.

For a larger purely illustrative calculation, suppose an operation requires `2,000,000,000` FLOPs
and the chosen kernel sustains `1,000,000,000,000` FLOPs/second:

```text
2e9 FLOPs / 1e12 FLOPs/second = 0.002 seconds = 2 ms
```

If moving the required data at the measured effective bandwidth takes 5 ms, the operation cannot
finish in 2 ms; the memory-side lower bound is already 5 ms, before other overhead. These rates are
assumptions used to show the division, not claims about any GPU.

For the toy `[2, 4, 8] @ [8, 12]` operation, library dispatch and GPU kernel-launch overhead can
easily matter more than its arithmetic. Real elapsed time also depends on data type, kernel choice,
shape alignment, where the tensors already reside, other device load and whether several operations
are fused. GPU work is commonly asynchronous relative to CPU code, so a real benchmark must use
appropriate GPU events or synchronization and a defined warm-up/workload; timing only the Python
call can measure submission rather than completion. No benchmark was run for this explanation.

### Padded, packed and separate variable-length examples

Suppose three sequences contain four, two and three token vectors:

```text
sequence 0: [a, b, c, d]   length 4
sequence 1: [e, f]         length 2
sequence 2: [g, h, i]      length 3
```

Each letter stands for one vector of hidden width `H`.

**1. Padded rectangular representation.** Extend every sequence to the longest length, four:

```text
values, shape [3, 4, H]:
[
  [a, b, c, d],
  [e, f, PAD, PAD],
  [g, h, i, PAD]
]

valid-token mask, shape [3, 4]:
[
  [1, 1, 1, 1],
  [1, 1, 0, 0],
  [1, 1, 1, 0]
]
```

The rectangular tensor has 12 position slots, of which nine are real tokens and three are padding.
The mask tells later operations which entries are not real. Rectangular shapes are convenient for
many kernels, but work or storage may be spent on padded slots unless an implementation avoids it.

**2. Packed representation.** Concatenate only the real token vectors and carry metadata that
preserves the original boundaries:

```text
packed values, shape [9, H]:
[a, b, c, d, e, f, g, h, i]

lengths:            [4, 2, 3]
cumulative offsets: [0, 4, 6, 9]
                     |  |  |  |
                     |  |  |  +-- end of sequence 2
                     |  |  +----- end of sequence 1 / start of sequence 2
                     |  +-------- end of sequence 0 / start of sequence 1
                     +----------- start of sequence 0
```

The slice `values[0:4]` is the first sequence, `values[4:6]` the second and `values[6:9]` the third.
For a token-wise projection, packing is simple:

```text
[9, H] @ [H, N] -> [9, N]
```

The offsets recover three output groups of lengths four, two and three. The projection does not mix
tokens, so concatenating them does not change that projection's mathematics.

Attention is different because it mixes positions. A packed-attention implementation must preserve
sequence boundaries through its mask or length/offset metadata, and position information must match
the intended sequence semantics. If the raw concatenation is treated as one ordinary causal
sequence, token `e` could attend to `a` through `d`; that is cross-sequence contamination, not the
three independent examples intended here.

This `[9, H]` plus offsets layout is a generic illustration. An engine can instead use lengths,
offsets, block tables, a jagged/nested tensor or other metadata. Do not assume every packed API uses
this exact structure. This example also is not a claim about the distinct
`torch.nn.utils.rnn.PackedSequence` API, which has its own ordering and metadata contract.

**3. Separate variable-length arrays.** Keep a collection of individually shaped tensors:

```text
[
  tensor shape [4, H],
  tensor shape [2, H],
  tensor shape [3, H]
]
```

This is conceptually direct and preserves boundaries without padding. A naive implementation may
run three smaller operations or loop over the collection, which can give up some batching
efficiency. A nested/jagged tensor abstraction can present ragged components through one container,
but its supported operations and internal layout are library-specific.

In this example, packing represents nine real positions instead of twelve padded positions—a 25%
reduction in represented token slots for a token-wise projection. That does **not** guarantee a 25%
wall-clock improvement. Kernel efficiency, attention work, metadata handling, memory traffic,
shape alignment and the length distribution determine the observed result.

**Sources checked November 16, 2026:** PyTorch [`torch.matmul`](https://docs.pytorch.org/docs/2.15/generated/torch.matmul.html)
documents batched matrix dimensions; NVIDIA's [matrix-multiplication performance guide](https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html)
supports the `M`, `N`, `K`, FLOP and arithmetic-intensity framework; Hugging Face
[padding and truncation documentation](https://huggingface.co/docs/transformers/main/en/pad_truncation)
describes padding variable-length batches into rectangular tensors; and PyTorch
[nested tensor documentation](https://docs.pytorch.org/docs/2.15/nested.html) describes ragged
sequential data stored in packed form with offsets that delimit batch-item boundaries. These sources
support the scoped mechanisms, not a universal packed-engine layout or a performance result.

</details>

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
