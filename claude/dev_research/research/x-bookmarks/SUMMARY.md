# X Bookmarks — Career and Learning Signals

Last updated: 2026-09-15 by Codex.

**November 9 resume note:** retained discovery history and source links. The market sample was
subsequently collected; do not restart its collection from the old open questions below. Current
priorities and next steps are in `/home/colligo/hs_scripts/claude/dev_research/PROJECT_STATE.md`.
The raw bookmark export on volatile storage is missing; this synthesis remains useful evidence.

## Scope and method

- Source: `/mnt/localssd/x_bookmarks_2026-09-15/bookmarks.json`.
- Exported: 2026-09-15 at 08:48 UTC.
- Reviewed: all 327 bookmarks, including attached text and the external links that appeared
  relevant and safe for work.
- Purpose: discover role families, skills, projects, primary resources, and career themes. Current
  job advertisements are inputs to skill research, not application recommendations.
- Excluded: health, investing, real estate, entertainment, politics, and other bookmarks without a
  meaningful connection to this project. These were intentionally not catalogued individually.

X is primarily a **discovery source**. Posts, screenshots, compensation claims, and author opinions
remain **UNVERIFIED** unless this summary names a primary or independently corroborating source.
The bookmark export is also incomplete for some reply threads, images, and deleted destinations.

Confidence labels follow `/home/colligo/hs_scripts/claude/dev_research/research-plan.md`:

- **VERIFIED:** supported by a current primary source or multiple reliable sources.
- **ASSUMED:** a transparent interpretation that still needs testing.
- **UNVERIFIED:** plausible, but unsupported enough that it cannot drive the curriculum.
- **USER-CONFIRMED:** supplied directly by Hooman; authoritative for preferences and recollection,
  not independent evidence of business impact.

## Executive synthesis

1. **[VERIFIED — current platform documentation]** Modern inference engineering is a real,
   substantial systems domain. Current vLLM, SGLang, and NVIDIA Dynamo documentation covers model
   serving, quantization, batching, cache management, distributed execution, routing, autoscaling,
   observability, and benchmarking. The bookmarks' recurring technical vocabulary maps to actual
   production systems rather than being purely social-media fashion.
2. **[ASSUMED — repeated bookmark pattern plus primary-platform corroboration]** The most useful
   learning center for Hooman is likely the intersection of inference mechanics, distributed
   serving, performance measurement, and production reliability—not generic prompt engineering or
   model training in isolation. The job-market sample must measure how often each skill appears.
3. **[VERIFIED — secondary analysis of 113 postings; employer samples still needed]** Forward
   Deployed Engineer and customer-facing applied-AI roles combine requirements discovery,
   production implementation, integration, deployment, evaluation, and product feedback. This is
   unusually close to Hooman's Foundry experience and should be included as a role family in the
   market sample.
4. **[ASSUMED — repeated bookmark pattern]** Evaluation, orchestration, context construction,
   routing, observability, guardrails, and cost control form a second adjacent skill cluster often
   described as AI engineering, harness engineering, or agent infrastructure. These skills connect
   model capabilities to dependable business workflows.
5. **[VERIFIED — current Google role pages]** Research-engineer and research-scientist paths in
   contemporary multimodal modeling ask for current framework, training, applied-research, and in
   some cases publication depth. This keeps modeling as a credible secondary branch but suggests a
   larger refresh cost than the production-systems path.
6. **[ASSUMED — synthesis of career evidence and bookmark evidence]** Hooman likely does not need a
   broad beginner AI curriculum. The probable leverage lies in deepening and demonstrating GPU and
   runtime mechanics, modern serving engines, performance engineering, and reproducible systems
   work while preserving his differentiating customer-workflow experience.

## Skill map discovered in the bookmarks

### 1. Inference foundations

The recurring foundation is understanding what happens during prefill and decode, and how compute,
memory bandwidth, model weights, activations, and KV cache constrain performance.

- transformer inference mechanics: prefill versus decode and compute- versus memory-bound work;
- latency measures: time to first token (TTFT), inter-token latency/time per output token, and tail
  latency;
- throughput, concurrency, saturation, and quality/cost trade-offs;
- model and cache memory sizing;
- precision and quantization: FP16/BF16, FP8, INT8/INT4, AWQ, GPTQ, and quality validation;
- attention and kernels: FlashAttention, kernel fusion, Triton/CUDA concepts, and profiling; and
- disciplined benchmarking rather than isolated headline numbers.

**Confidence:** **VERIFIED** that these capabilities exist in current serving stacks;
**ASSUMED** priority and depth for Hooman until the job-posting skills matrix is complete.

### 2. Serving engines and request scheduling

- vLLM, SGLang, and TensorRT-LLM concepts and operational trade-offs;
- continuous and dynamic batching;
- paged attention and KV-cache allocation;
- prefix/prompt caching, chunked prefill, and speculative decoding;
- request queues, admission control, fairness, starvation, and priority scheduling;
- multi-model routing, retries, fallbacks, budgets, and rate limits; and
- streaming behavior and backpressure.

A particularly useful practice problem is to design a scheduler for eight GPUs where small jobs use
one GPU, large jobs require all eight, arrivals are continuous, and the design must avoid starving
large jobs while preserving throughput. The X post's claim that this is a frequently asked
Anthropic interview question is **UNVERIFIED**; the problem itself is valuable systems practice.

### 3. Distributed inference and platform engineering

- tensor, pipeline, data, and expert parallelism;
- disaggregated prefill/decode and KV-aware routing;
- multi-node orchestration with Kubernetes, Ray, or Slurm;
- autoscaling from queue depth and service objectives;
- model-weight packaging, sharding, distribution, lazy loading, and startup time;
- GPU partitioning, utilization, topology, and contention;
- multi-tenancy, quotas, isolation, and security; and
- regional failover, checkpoint/recovery behavior, and fault injection.

The official NVIDIA Dynamo documentation is strong evidence that several of these themes now form
an integrated inference-platform layer rather than isolated optimizations.

### 4. Measurement, reliability, and economics

- instrument queue, prefill, decode, cache, model, and accelerator behavior separately;
- measure p50/p95/p99 TTFT, token latency, throughput, error rate, quality, GPU utilization, and
  cost per token/request;
- test under concurrency and realistic input/output-length distributions;
- compare precision, engine, batching, cache, and routing choices without silently changing model
  quality;
- support canaries, shadow traffic, rollback, overload behavior, and failure recovery; and
- connect technical metrics to cost per successful task, gross margin, human escalation, and
  business value.

The unit-economics framing is an important senior-level complement to pure kernel or serving
performance. Exact formulas and claimed savings in X posts remain **UNVERIFIED** until reproduced.

### 5. Applied AI, harnesses, and evaluation

Repeated bookmarks describe a production layer around foundation models:

- deterministic orchestration and durable workflows;
- context assembly, retrieval, memory, and prompt/version management;
- model routing and semantic caching;
- structured output and tool execution;
- offline and online evaluation, regression suites, and CI quality gates;
- tracing, observability, guardrails, audit, and human escalation; and
- data flywheels that incorporate reviewed failures.

**[VERIFIED — OpenAI first-party engineering article]** OpenAI describes using executable Runme
notebooks with Codex for repeatable evaluation and cloud workflows. Humans review plans and
alternatives; notebooks preserve commands, dead ends, decisions, and results; a Markdown index
makes prior work discoverable. This supports learning AI-native engineering workflows and durable
documentation, not merely using a chatbot interactively.

**[VERIFIED — arXiv primary source]** Memex(RL) proposes keeping concise indexed summaries in the
working context while retaining full-fidelity experience externally for selective retrieval. It
supports the general long-session pattern of a compact live handoff plus accessible underlying
evidence. It does not independently prove that this project's exact file structure is optimal.

### 6. Forward-deployed and customer AI systems

An analysis of 113 Forward Deployed Engineer postings published in 2026 reported these recurring
responsibilities: customer engagement (92%), production building/deployment (87%), integration
(62%), requirements/scoping (51%), testing/evaluation/monitoring (41%), and product feedback (39%).
Reported technology frequencies included Python (89%), AWS/GCP/Azure, Docker, Kubernetes, RAG,
prompt engineering, agents, and vector databases.

This is a **VERIFIED report of the article's dataset and findings**, not yet an independently
reproduced market estimate. It is nevertheless important because the work shape matches Hooman's
experience delivering end-to-end customer AI workflows across Home Depot, Coca-Cola, HP, Lionsgate,
Humain, and Tesco. Representative employer postings should test:

- whether Staff/Principal-equivalent versions meet the compensation target;
- how titles vary: Forward Deployed Engineer, Applied AI Engineer, AI Architect, Solutions/Field AI
  Engineer, Research Engineer, or Member of Technical Staff;
- whether these roles preserve enough technical depth and product ownership; and
- whether remote arrangements are materially rarer than in other role families.

The core lesson is not to replace inference with consulting. It is to preserve customer discovery,
workflow design, integration, and value measurement as differentiators while deepening the shared
systems foundation.

### 7. Modeling and applied research

The bookmarks contain useful material on multimodal/world models, diffusion, reinforcement learning,
fine-tuning, and small task-specific models. However, isolated papers and promotional threads do not
establish curriculum priority.

**[VERIFIED — current Google career pages]** Sample Gemini Omni research roles asked for current
JAX/PyTorch/TensorFlow experience, ML and language/multimodal-model depth, research-to-production
work, and—for scientist roles—PhD-equivalent research credentials and publications. This indicates
that a modeling-heavy branch should be deliberate and evidence-based rather than a generic survey of
new papers.

Sebastian Raschka's `LLMs-from-scratch` repository and TrenTorch are possible fundamentals refreshers.
TrenTorch builds tensors, autograd, layers, optimizers, convolution, tokenization, attention,
transformers, profiling, quantization, and acceleration with NumPy. It is pedagogically useful but
not a substitute for real distributed serving, accelerator profiling, or production operations.

## Role-family implications

Use these as research hypotheses, not final career choices:

| Role family | Current fit hypothesis | Likely incremental gap | Bookmark evidence quality |
|---|---|---|---|
| Inference / AI systems | Strong adjacent fit from deployment, vLLM, pipelines, and distributed systems | Deeper GPU/runtime, kernels, modern engine internals, reproducible benchmarking | Medium: primary stack docs plus unverified job discovery |
| AI platform / ML infrastructure | Strong | Current platform patterns, reliability, observability, and explicit Staff-level system evidence | Medium |
| Forward-deployed / customer AI | Potentially very strong and differentiated | Codify business discovery, architecture, measurement, and externally safe impact stories | Medium: one systematic secondary study plus career evidence |
| Applied AI / agent infrastructure | Strong adjacent fit | Evals, harnesses, routing, guardrails, and cost/quality operations | Medium |
| Modeling / research engineering | Plausible secondary path | Current training framework, model architecture, experimentation, and research depth | Medium: primary role samples, thin overall sample |

## Job-discovery signals—not an application shortlist

One bookmark collected screenshots of inference-related roles at Baseten, SpaceX, Luma, NVIDIA,
AMD, Cohere, OpenAI, Perplexity, F5, Amazon, Etched, Zoox, Rhoda AI, and Cartesia. Titles ranged
across inference engineering, inference systems, model optimization/deployment, site reliability,
data engineering, and model efficiency. The breadth suggests that inference work exists at model
labs, accelerator vendors, serving companies, product companies, and infrastructure providers—not
only at frontier labs.

The screenshots displayed base ranges from roughly $165K to $555K for selected US roles, including
several whose lower bound exceeded $200K. These are **UNVERIFIED discovery signals**: screenshots
can be stale, omit level/location, mix base with other compensation, or outlive a job page. They
cannot support compensation conclusions until checked against live employer pages.

Other bookmarks pointed to roles involving:

- evaluation frameworks and orchestration between foundation models and products;
- AI ingestion and data pipelines using Python, queues, streaming, and cloud services;
- internal AI automation spanning developer tools, knowledge/data systems, and 0-to-1 delivery;
- large-scale distributed systems, data processing, ambiguity decomposition, and precise technical
  communication; and
- agents, long-horizon autonomy, reinforcement learning/post-training, multimodal systems,
  reasoning, and forward-deployed engineering.

The last group came largely from recruiter or social posts and is **UNVERIFIED**. It supplies search
terms for the market sample, not evidence that every theme is common or high priority.

## Candidate proof artifacts—not yet a curriculum

The strongest idea is one integrated, reproducible inference lab rather than fifteen disconnected
demos. A bounded version could:

1. serve one open model through vLLM and SGLang;
2. report TTFT, token latency, throughput, memory, utilization, quality, and cost under controlled
   loads;
3. compare precision/quantization, continuous batching, prefix caching, and one additional
   optimization;
4. expose routing, rate limits, autoscaling signals, and useful telemetry; and
5. inject overload or worker failure and document behavior, trade-offs, and recovery.

**[ASSUMED]** This artifact would efficiently expose real gaps and demonstrate several recurring
skills. It should enter the learning plan only after the representative market sample and a check
against available compute, confidentiality, and time constraints.

Two smaller complementary artifacts may be valuable:

- the eight-GPU scheduling design and simulator, emphasizing fairness and throughput; and
- an evaluation-driven customer workflow showing reliable orchestration, observability, cost per
  successful task, and human escalation.

## What should not drive the plan

- Viral salary screenshots or recruiter claims without live employer listings.
- Claims that one tool, repository, or contribution path guarantees an inference job.
- Unsupported productivity multipliers, token-savings percentages, or famous-company interview
  claims.
- Long lists of frameworks without a system problem, measurement method, and completion criterion.
- Generic AI news, paper collections, or model releases that do not close a demonstrated gap.
- A large number of toy projects at the expense of one deep, explainable system.

## High-value sources

### Verified or primary sources

- vLLM documentation, retrieved 2026-09-15: https://docs.vllm.ai/en/latest/
- SGLang documentation, retrieved 2026-09-15: https://docs.sglang.io/
- NVIDIA Dynamo documentation, retrieved 2026-09-15: https://docs.nvidia.com/dynamo/latest/
- OpenAI, “Automating repetitive work at OpenAI with Codex,” retrieved 2026-09-15:
  https://learn.chatgpt.com/blog/automating-repetitive-work-at-openai-with-codex
- Google Careers, Gemini Omni search results, retrieved 2026-09-15:
  https://www.google.com/about/careers/applications/jobs/results?q=omni
- OpenAI Cooperative Systems role, retrieved 2026-09-15:
  https://jobs.a16z.com/jobs/openai/241154df-ab1a-4dfa-8b18-66e087d1e636--engineering-manager-cooperative-systems
- Staff privacy-engineering role at a frontier lab, retrieved 2026-09-15:
  https://jobs.ashbyhq.com/g2i/b2f1846c-ae29-4f24-b2b6-33b6b71eb7a4
- Forward-deployed-engineer posting analysis, retrieved 2026-09-15:
  https://aishippingblog.com/p/what-ai-forward-deployed-engineers
- TrenTorch repository, retrieved 2026-09-15: https://github.com/TrenTorch/TrenTorch
- LLMs from Scratch repository, retrieved 2026-09-15:
  https://github.com/rasbt/LLMs-from-scratch
- “When Agents Coordinate,” arXiv:2608.16801, retrieved 2026-09-15:
  https://arxiv.org/abs/2608.16801
- “Memex(RL),” arXiv:2603.04257, retrieved 2026-09-15:
  https://arxiv.org/abs/2603.04257

### Most useful X discovery sources

- Inference skill overview: https://x.com/ashishllm/status/2099711211302682635
- Inference, harness, and evaluation framing:
  https://x.com/amitiitbhu/status/2099392872093221159
- Inference platform and optimization topics:
  https://x.com/ashishllm/status/2099408071558893613
- AI/inference engineering stack: https://x.com/ratishtwts/status/2099032798581653953
- AI-infrastructure project ideas: https://x.com/suraj_sharma14/status/2099113368942465438
- Inference-engineering job screenshots: https://x.com/msharmavikram/status/2099170858602578283
- Cost per successful task and AI economics:
  https://x.com/suraj_sharma14/status/2099475753750446300
- Applied-AI project ideas: https://x.com/suraj_sharma14/status/2098026202464243908
- Agent/system building blocks: https://x.com/suraj_sharma14/status/2097301427957948778
- GPU scheduler exercise: https://x.com/avrldotdev/status/2095803128990007446
- AI-native engineering workflow: https://x.com/clare_liguori/status/2097836812958097915
- Forward-deployed-engineer analysis:
  https://x.com/Al_Grigor/status/2092507344848781736
- OpenAI durable workflow article pointer:
  https://x.com/HamelHusain/status/2092628886572200169
- Multi-agent coordination paper pointer:
  https://x.com/rohanpaul_ai/status/2091493725637857664
- Durable indexed memory paper pointer:
  https://x.com/rohanpaul_ai/status/2071262507944304992

## Open questions for the market-research phase

1. Which inference skills recur in live Staff/Principal postings, and which are specialist-only?
2. How often do employers expect CUDA/Triton and kernel work versus serving-platform architecture?
3. What titles capture the high-seniority, technically deep version of forward-deployed AI work?
4. Which roles cross the compensation target, and how much of posted compensation is base versus
   total compensation?
5. Which existing Adobe accomplishments demonstrate the requirements already, and which gaps are
   only documentation gaps?
6. What computing resources are practical for a reproducible inference artifact?
