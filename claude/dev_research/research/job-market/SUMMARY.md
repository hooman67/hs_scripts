# External Job Market — Staff/Principal AI Systems

Last updated: 2026-09-15 by Codex.

**November 9 resume note:** historical September 15 evidence. The current curriculum and IC
scope are in `/home/colligo/hs_scripts/claude/dev_research/learning/LEARNING_PLAN.md`.
Required/preferred normalization is parked; the final section describes optional future work,
not the current next action. Live applications require a fresh role check when requested.

## Status

Initial collection complete: 60 live postings from 20 employers, balanced at 30 roles per primary
family. A conservative first-pass mention analysis is complete. Required-versus-preferred coding
and comparison against Hooman's evidence remain in progress, so curriculum conclusions are still
provisional.

## Research objective

Measure current skills, scope, and evidence expectations for well-compensated external IC roles
near:

1. inference, serving, runtime, optimization, and AI/ML platform; and
2. Forward Deployed/customer-facing AI engineering and end-to-end applied AI systems.

The listings are skill evidence, not jobs Hooman intends to apply to now.

## Confirmed sampling design

- Target 50–75 unique, live, external postings.
- Keep the two primary families approximately equal by primary classification.
- Cast a wide title net: Staff, Principal, Senior Staff, Member of Technical Staff, Research
  Engineer, Forward Deployed Engineer, Applied AI Engineer, Solutions/Field AI Engineer, and
  closely equivalent senior IC titles.
- Prefer roles whose published US base-salary range exceeds $200K at either bound or materially
  crosses $200K. Compensation means base salary, not assumed equity or total compensation.
- Include highly relevant roles without published compensation; record compensation as missing.
- Use the employer's current career page as the canonical source. Search engines, boards, and X
  are discovery surfaces only.
- Record retrieval date and active-page status. Do not silently treat expired or inaccessible
  pages as current evidence.
- De-duplicate reposts and location variants when responsibilities and qualifications are
  materially identical.
- Limit employer concentration so one large hiring program does not dominate frequencies.
- Keep modeling-heavy roles outside the balanced core unless they materially overlap inference or
  customer AI systems. Modeling remains a bounded comparison branch, not half of this sample.

## Evidence fields

For each posting, preserve:

- company, exact title, level, location, and work arrangement;
- canonical employer URL and retrieval date;
- active, expired, inaccessible, or uncertain status;
- primary role family and secondary tags;
- published base minimum/maximum, currency, period, and location caveat;
- required and preferred skills in the employer's language;
- normalized skill categories in separate fields;
- responsibility, scope, customer-contact, and Staff-level signals;
- years or equivalent-experience requirements;
- interview-process evidence, if the employer publishes it;
- confidence and collection notes; and
- duplicate relationship, when applicable.

## Quality and stopping rules

- Do not infer demand from raw counts before controlling for duplicate employers, location copies,
  and family balance.
- Do not convert “preferred” into “required.”
- Do not infer missing compensation.
- A company or social-media description cannot replace the actual job page.
- Continue until at least 25 usable roles exist in each primary family and the total lies between
  50 and 75. Replace inaccessible, expired, or duplicate records rather than counting them.
- After collection, normalize skills once, inspect contradictions, and only then calculate
  frequencies or curriculum implications.

## Initial sample — completed 2026-09-15

- 60 currently listed employer postings.
- All 60 canonical employer URLs returned a successful HTTP response during validation on
  2026-09-15; all 60 also appeared in the corresponding employer ATS feed.
- 20 employers.
- 30 inference/platform roles.
- 30 Forward Deployed/customer AI roles.
- 1–5 roles per employer; no employer contributes more than 8.3% of the sample.
- All 60 publish a compensation range, though six ranges are OTE, commission-bearing, or
  ambiguously labeled rather than verified base salary.
- 49 of 60 have a published or reasonably identified USD **base-salary** maximum above $200K:
  all 30 inference/platform roles and 19 of 30 Forward Deployed/customer AI roles.
- 27 of 60 have a USD base-salary minimum at or above $200K: 22 inference/platform and five
  Forward Deployed/customer AI roles.

These compensation proportions describe this deliberately high-paying sample. They do **not**
estimate the percentage of all market roles above $200K.

### Employer coverage

Inference/platform coverage includes OpenAI, Baseten, Modal, Anyscale, Cohere, Perplexity, Harvey,
Crusoe, Cartesia, Thinking Machines Lab, Together AI, and CoreWeave.

Forward Deployed/customer AI coverage includes OpenAI, Baseten, Modal, Anyscale, Cohere, Sierra,
Writer, Decagon, LangChain, Cartesia, Anthropic, Scale AI, Together AI, Glean, CoreWeave, and
Snorkel AI.

The source-of-truth record is
`/home/colligo/hs_scripts/claude/dev_research/research/job-market/postings.jsonl`. Each line contains
the employer URL, retrieval date, active status, published compensation, full captured description,
primary family, role subtype, and conservative normalized mention tags.

## First-pass skill evidence

The following tables count whether a concept is mentioned anywhere in a posting. They do **not**
claim that every mention is a hard requirement. Employer boilerplate can still cause occasional
false positives; exact required/preferred classification is the next normalization pass.

### Inference/platform — 30 postings

| Normalized concept | Postings | Share |
|---|---:|---:|
| Performance, optimization, latency, throughput, or profiling | 24 | 80% |
| GPUs or accelerators | 23 | 77% |
| Observability, reliability, high availability, or operations | 19 | 63% |
| Kubernetes or containers | 17 | 57% |
| LLMs or foundation models | 17 | 57% |
| Distributed systems or multi-node computing | 16 | 53% |
| End-to-end ownership | 16 | 53% |
| Inference serving/runtime | 16 | 53% |
| Python | 16 | 53% |
| CUDA | 15 | 50% |
| PyTorch | 12 | 40% |
| Evaluation or benchmarking | 10 | 33% |
| Batching, KV/prefix caching, or scheduling | 9 | 30% |
| LoRA, fine-tuning, post-training, or reinforcement learning | 9 | 30% |
| Rust | 9 | 30% |
| Triton or custom GPU kernels | 9 | 30% |
| HPC networking: NCCL, InfiniBand, NVLink, or RDMA | 8 | 27% |
| Quantization | 6 | 20% |

### Forward Deployed/customer AI — 30 postings

| Normalized concept | Postings | Share |
|---|---:|---:|
| LLMs or foundation models | 25 | 83% |
| Written, verbal, or technical communication | 24 | 80% |
| Direct customer work | 23 | 77% |
| Agents, agentic workflows, or tool use | 20 | 67% |
| Evaluation or benchmarking | 18 | 60% |
| Python | 17 | 57% |
| End-to-end ownership | 15 | 50% |
| Requirements discovery or scoping | 13 | 43% |
| Product or cross-functional partnership | 12 | 40% |
| Kubernetes or containers | 11 | 37% |
| Observability or production reliability | 11 | 37% |
| Cloud platforms or cloud infrastructure | 10 | 33% |
| Performance or inference optimization | 8 | 27% |
| RAG, retrieval, embeddings, or vector databases | 8 | 27% |
| LoRA, fine-tuning, post-training, or reinforcement learning | 7 | 23% |
| Data pipelines or data processing | 6 | 20% |
| Distributed systems | 6 | 20% |

## What is already clear

### 1. The shared center is production AI systems

**[VERIFIED — this 60-posting sample]** Both families reward end-to-end production ownership,
Python, evaluation, cross-functional work, and operational awareness. They diverge in emphasis:

- inference/platform moves downward into accelerators, runtimes, kernels, distributed execution,
  orchestration, and measured performance;
- Forward Deployed/customer AI moves outward into problem discovery, architecture, integrations,
  agents, evaluation, adoption, and business outcomes.

This supports a T-shaped strategy: deep inference/platform capability with customer-workflow breadth.
It does not require choosing between “pure infrastructure” and “business-facing AI” as unrelated
careers.

### 2. Forward Deployed AI is technically heterogeneous

The 30-role family contains three materially different subtypes:

- 18 hands-on Forward Deployed/deployment/field engineering roles;
- seven solutions architecture or enablement roles; and
- five applied-AI customer-delivery roles.

The hands-on subtype is the closest match to the desired Staff/Principal IC direction. Some
solutions roles carry sales quotas or OTE compensation, so they must not be treated as equivalent
to engineering roles when comparing pay or required depth.

Representative evidence:

- OpenAI asks Forward Deployed Software Engineers to embed with strategic customers, turn
  ambiguous requirements into scoped full-stack production systems, code alongside customer teams,
  and feed reusable abstractions back to product and research:
  https://jobs.ashbyhq.com/openai/00207abc-49b7-465c-a219-f7c1140f8047
- Baseten explicitly combines customer problem framing, evaluation, production deployment,
  monitoring, latency, quality, and cost:
  https://jobs.ashbyhq.com/baseten/84c1801c-1a65-49fb-aaaa-beeafd530e7e
- Modal separates ML and systems FDEs, showing that forward deployment can demand real depth in
  serving, training, cloud architecture, networking, storage, containers, and distributed systems:
  https://jobs.ashbyhq.com/modal/9fadb51f-ce11-41b1-84d5-470e66cc8ee9 and
  https://jobs.ashbyhq.com/modal/cbbbee50-3d3b-4873-8ae8-ff4b885b8e54
- Together AI's FDE combines inference-engine selection and tuning, KV cache, speculative decoding,
  tensor parallelism, quantization, LoRA/SFT/DPO/RLHF/GRPO, and strategic customer ownership:
  https://job-boards.greenhouse.io/togetherai/jobs/5131941007
- Glean's founding FDE emphasizes discovering unsolved business problems, building new product
  surfaces from zero to one, and turning customer-specific work into product:
  https://job-boards.greenhouse.io/gleanwork/jobs/4651991005

### 3. Inference contains distinct depth tracks

The 30-role family contains:

- 11 inference-serving/runtime roles;
- 11 distributed/platform-infrastructure roles;
- seven performance/kernel/model-efficiency roles; and
- one evaluation-platform role.

This matters for the learning plan. A Staff inference-platform generalist should understand all four
layers, but does not need to compete immediately with a full-time kernel specialist. The current
sample supports depth in serving and distributed platform work, plus enough CUDA/Triton literacy to
profile, reason about bottlenecks, and make informed optimization choices.

Representative evidence:

- OpenAI Model Inference combines model architecture, PyTorch, CUDA/NCCL, HPC networking,
  distributed systems, observability, latency, throughput, and GPU utilization:
  https://jobs.ashbyhq.com/openai/83b6755d-7785-4186-9050-5ef3ad127941
- Baseten Model Performance explicitly names quantization, speculative decoding, KV-cache reuse,
  chunked prefill, LoRA, TensorRT-LLM, vLLM, SGLang, CUDA, and continuous batching:
  https://jobs.ashbyhq.com/baseten/d29e748c-7209-460d-a024-8f77ae0a3d4d
- Modal's inference-research role spans kernels and quantization through schedulers, autoscaling,
  disaggregated prefill/decode, observability, cost per token, and tail latency:
  https://jobs.ashbyhq.com/modal/73c97bbc-8e27-4c5d-b38b-90b3afdb0d93
- Together AI's compute-infrastructure role focuses on a Kubernetes-native GPU-fleet control plane,
  scheduling/bin-packing, self-service APIs, health/remediation, topology, and NCCL/CUDA networking:
  https://job-boards.greenhouse.io/togetherai/jobs/5186628007
- Thinking Machines Lab's inference role combines vLLM/SGLang, distributed orchestration,
  performance, reproducibility, and research collaboration:
  https://jobs.ashbyhq.com/thinkingmachines/4087e0f6-4295-419a-ba02-08e95a74ceea
- CoreWeave's kernel role requires reproducible microbenchmarks, roofline analysis, CUDA, attention,
  MoE, quantization, KV cache, and proving that kernel gains improve end-to-end serving:
  https://coreweave.com/careers/job?4697100006&board=coreweave&gh_jid=4697100006

### 4. Bounded LoRA/fine-tuning knowledge is supported

**[VERIFIED — posting-mention count]** Fine-tuning, LoRA, post-training, or reinforcement-learning
language appears in nine of 30 inference/platform postings and seven of 30 Forward Deployed/customer
AI postings. It is meaningful, especially for specialist FDE work, but it is not the dominant common
requirement in this sample.

**[ASSUMED — curriculum implication]** Hooman's chosen boundary—learn enough to implement,
evaluate, and explain LoRA and practical fine-tuning without pursuing a broad model-research
curriculum—is proportionate to this first batch. Required-versus-preferred coding could still
change the exact depth.

### 5. The platform artifact has direct evidentiary value

**[ASSUMED — sample synthesis, supported by user history]** A single deep inference platform can
demonstrate much of the shared core: model serving, performance measurement, GPU/resource behavior,
distributed orchestration, reliability, evaluation, and end-to-end ownership. Adding one realistic
customer workflow can also demonstrate the Forward Deployed side without turning the project into
a collection of unrelated demos.

This is reinforced by Hooman's **USER-CONFIRMED** history: an Aupera inference platform and live
demonstration were instrumental in his Adobe hiring.

## Limitations

- This is a purposive, high-compensation sample, not a random estimate of the entire market.
- Exact title levels are inconsistent across employers; MTS, Research Engineer, and unqualified FDE
  titles can carry senior scope without saying “Staff.”
- Mention counts do not distinguish required, preferred, responsibility, or company-context text.
- Six ranges are OTE, commission-bearing, or internally contradictory and are excluded from verified
  base-salary conclusions.
- Several employers publish multiple location tiers. The raw record preserves all ranges found; no
  currency conversion or total-compensation estimate was performed.
- The sample is geographically concentrated in major US AI hubs because role relevance and base pay
  were selected before work arrangement. It cannot yet support a remote-work availability estimate.
- Active means present in the employer's public ATS feed on 2026-09-15. It does not guarantee that
  recruiting has not paused internally.

## Parked normalization work

1. Separate employer language into required, preferred, and responsibility evidence.
2. Audit each normalized mention to remove boilerplate false positives.
3. Identify Staff-level differentiators versus baseline qualifications.
4. Compare the validated matrix with Hooman's documented career evidence.
5. Convert only the highest-confidence gaps into candidate learning modules and the inference
   platform's requirements.
