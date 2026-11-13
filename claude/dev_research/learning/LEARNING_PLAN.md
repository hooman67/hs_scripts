# Learning Plan — Accelerated AI Infrastructure IC Readiness

As of: **2026-11-10** (teaching-method update; curriculum set November 9). This is the current
curriculum, replacing the 36-week schedule and the
October 12-week proposal. The goal and ordering are user-confirmed; the exercises and gates below
are researcher recommendations, not evidence of completed work or a guarantee of an offer.

## Contents

- [Goal and boundaries](#goal-and-boundaries)
- [The sequence](#the-sequence)
- [How to work through the first month](#how-to-work-through-the-first-month)
- [Second month: deeper drills and interviews](#second-month-deeper-drills-and-interviews)
- [One curriculum across IC levels](#one-curriculum-across-ic-levels)
- [Profile and application preparation](#profile-and-application-preparation)
- [Reuse and defer](#reuse-and-defer)
- [Agent execution and review](#agent-execution-and-review)
- [Evidence and limitations](#evidence-and-limitations)
- [Primary resources](#primary-resources)
- [Next action](#next-action)

## Goal and boundaries

**Target:** an accepted offer in approximately two months, around January 9, 2027. Cover the
essential interview areas in the first month, then deepen weak and company-specific areas in the
second. Hiring timing remains outside this plan's control. This is a first pass through the core,
not mastery of every AI specialty in one month.

**USER-CONFIRMED, November 9:** pursue Senior IC and Staff/Principal AI infrastructure/inference;
exclude engineering-manager roles. Start with system design and ML/inference fundamentals, then
move to timed coding. Explaining experience is not the main weakness. Hooman is still employed at
Adobe, lives in San Jose, and says no sponsorship is needed for applying. No recruiter conversations
are underway. He will request application help after the plan and LinkedIn are ready.

The old 5–6-hour cap no longer applies. Use the ordered stages and performance gates below rather
than a fixed weekly timetable. Retain hands-on leadership in the narrative; do not create a second
management curriculum. Customer AI/evaluation remains useful systems breadth and career evidence,
not a competing full FDE specialization in this first pass.

**Unknown:** completed exercises and independently demonstrated skill level. The October
self-ratings are historical context, not a current assessment. Discreet search and conservative
public descriptions are proposals because disclosure preferences were not explicitly answered.

## The sequence

Stages 1–2 establish the foundation Hooman requested. Stage 3 introduces timed coding; it then
continues alongside stages 4–7. Do not wait to finish the entire technical curriculum before coding.
Each stage produces one small piece of evidence. Profile preparation runs in parallel.

| Order | Learn and practice | Required output before moving on |
|---|---|---|
| **1. System-design foundations** | Requirements/SLOs and workload estimates; API and data model; SQL/indexes versus object storage; caching; queues; consistency; partitioning; retries, idempotency and leases. Walk through one small design, then design a durable video-processing job service. | One diagram, a job-state model, the principal trade-off, and a worker-crash/duplicate-delivery trace. Explain why each component exists. |
| **2. ML and inference fundamentals** | Tensor shapes and matmul; inference versus training; losses, overfitting, train/validation/test leakage; tokenization/chat templates; attention and transformer blocks; prefill/decode; weights/activations/KV memory; batching; GPU compute versus bandwidth; latency and throughput. | Closed-book explanation, one memory estimate, and interpretation of a serving trace. Reuse an existing endpoint if available; a new GPU platform is not a prerequisite. |
| **3. Timed coding and SQL** | Begin with arrays/hash maps, two pointers/sliding windows, stacks/queues; then heaps/top-k, binary search/intervals, trees/graphs. Add recursion/basic dynamic programming after core patterns. Refresh joins, aggregation, window functions, indexes and pagination. | A blank-editor attempt, tests, complexity and a changed constraint. Establish the weak patterns; continue fresh coding problems throughout the remaining stages. |
| **4. Production inference system design** | Admission control, bounded queues, continuous batching, KV/prefix cache, routing, replicas versus tensor/pipeline parallelism, streaming/cancellation, deadlines, quotas, tenant isolation and SLOs. | A complete multi-tenant LLM-serving design; handle a long-prompt burst, GPU-worker loss and cancellation. Defend scale-out versus sharding without adding machinery by habit. |
| **5. Operations and measured performance** | Container/process lifecycle; Kubernetes Pods/Deployments/Services, requests/limits, GPU scheduling, readiness and rollout; logs/events and failure diagnosis; TTFT/TPOT/throughput, workload control, warm-up and errors. | One small deploy/break/diagnose exercise, plus one controlled serving comparison or an explicitly supplied trace analysis if compute is unavailable. Preserve observations and limitations. |
| **6. Evaluation and applied ML breadth** | Task acceptance criteria, fixed eval sets and leakage; quality/latency/cost; embeddings/retrieval and reranking; RAG versus prompting versus SFT/LoRA; structured output; tool failures, permissions and prompt injection; basic rollout/rollback. | Design one evaluated document-answering or customer workflow. Compare alternatives, trace a wrong answer/tool failure, and justify a release decision. Explain LoRA parameter savings and its limits. |
| **7. Generalization and first full assessment** | Rehearse a metadata/data-workflow design outside LLM serving. Then attempt fresh coding, a full design, and an ML/inference deep dive. Briefly refresh two existing technical stories. | Record unaided performance and the three most consequential gaps. Finish the first-month coverage pass even if some areas remain weak; those gaps drive month two. |

### Stage 1: learn the design process once

Learn through **big picture and diagrams → normal flow and components → concrete examples →
problems and constraints → motivated solutions and alternatives**. Define unfamiliar terms when
first used and name real implementation choices (for example, SQS, PostgreSQL/RDS and S3). Read
the first tutorial before attempting the exercise when the material is new.

Interview presentation is separate and comes after understanding: clarify → simple design and
estimate → selected failure case → trade-offs. Timing cues belong in rehearsal, not the initial
teaching sequence. Introductory guides may be substantial; shorten later guides as familiarity grows.

For the job-service exercise, explicitly answer: what does an accepted request mean, who owns a
job, what is durable, what happens after a side effect succeeds but its acknowledgement is lost,
and how can recovery avoid silently losing or duplicating work? Explain which invariant requires
an atomic database operation and which external effect needs idempotency or reconciliation.

Start from an architecture you understand from work, then change the workload or failure. Never
copy confidential implementation details into public materials.

### Stage 2: bounded fundamentals, then application

Refresh ML concepts only to the depth needed to reason, implement a small example, or diagnose an
error. Include gradients/backprop and optimizer basics, precision, classification versus ranking
metrics, distribution shift, and the distinction among pretraining, SFT and preference optimization.
Do not expand into a full introductory ML course unless a diagnostic exposes that need.

For a conventional decoder transformer, derive the approximate unshared KV payload:
`2 × layers × KV_heads × head_dimension × total_cached_tokens × bytes_per_element`.
State assumptions about GQA/MQA, padding/block overhead, prefix sharing and architecture; this is
not total GPU memory. Separate attention IO optimization from KV allocation/paging. Explain which
measurements would distinguish compute, memory, communication and queueing bottlenecks.

Use the existing notes and quizzes selectively. Learn unfamiliar concepts through a worked example
with definitions before attempting an explanation. For familiar concepts, attempt first, read to
repair a specific gap, then explain again without notes.

### Stage 3 onward: make coding recurring

Practice coding after the initial systems/ML pass, not after achieving mastery. Start untimed only
long enough to recover a pattern, then move to the likely interview format. Use Python initially
unless a target explicitly requires C++ or another language. Practical coding, concurrency,
iterators, parsers, caches and testing can matter alongside algorithm questions; the actual round
brief should determine the mix.

For each attempt: clarify the contract, solve without model-written code, test boundaries, explain
complexity, then handle one follow-up. Review the failure and retry a different problem using the
same principle. Reading an answer or solving the same memorized example is not a fresh pass.

SQL is a small parallel component, not a month-long database course. Practice a join/aggregation,
a latest-row-per-entity or ranking query, and the index/transaction reasoning behind a job claim.
Deep dynamic programming, advanced graph algorithms, lock-free C++, and specialized coding formats
move up only when evidence from the target round warrants them.

## How to work through the first month

For unfamiliar material use **understand a worked example → exercise → explain → record one
correction**. For familiar material, attempt first and read to repair gaps. Efficient learning
means understanding why the design works; compressed terminology is not a substitute.
Complete one representative attempt in every core area before extending any area into a course.
After stage 3 starts, alternate coding with the current design/domain stage. Keep one current weak
point per track; do not accumulate a long reading backlog.

Use the same small 0–3 practice rubric: 0 cannot yet do it; 1 substantial help; 2 independently
handles the bounded case; 3 handles changed constraints and defends trade-offs. It is a planning
rubric, not an employer's hiring threshold. A first pass can finish with recorded 0s or 1s; do not
let one difficult area consume the whole month. Repeated fresh 2s support reducing its allocation.

- **Design:** coherent API/data/flows, explicit invariants, defensible estimates, failure trace,
  trade-off and response to a changed requirement.
- **Domain:** correct explanation and estimate; distinguish observed behavior from expectation;
  identify a plausible diagnostic measurement.
- **Coding:** correct independent solution, appropriate complexity, edge cases and follow-up.
- **Operations/evaluation:** diagnose evidence, choose a fix or release decision, and explain
  rollback and remaining uncertainty.

Keep experience rehearsal light: two strong existing examples, one short technical explanation and
one deeper architecture discussion. Increase this only if a mock reveals a problem. Support claims
with Hooman's actual decisions and outcomes, not a generated success story.

**Bound the artifact:** reuse or make one endpoint, one controlled workload comparison, one failure
observation, one diagram and a five-minute explanation. Use existing benchmark tools. No requirement
to build a gateway, evaluation platform, dashboard suite or benchmark framework. Tiny samples cannot
establish p99 or maximum capacity. Missing compute is recorded, not disguised as a measurement.

## Second month: deeper drills and interviews

The second month is driven by actual failures and confirmed interview formats, not another broad
survey. Continue the job process once Hooman requests it; do not wait for all practice gates to pass
before approaching employers.

1. **Choose the next bottleneck.** Use the first-month assessment or a recruiter-provided round
   format. Fix the most consequential failed capability, then validate with a fresh problem.
2. **Select one depth branch per target.** Inference/performance: profile interpretation, batching,
   cache behavior, quantization/quality and communication; one small Triton/CUDA exercise only if
   relevant. ML platform: orchestration, metadata/lineage, recovery, quotas, developer experience
   and operational diagnosis. Applied AI breadth: evaluation/retrieval/tool reliability if the role
   actually includes it. Do not run all branches as separate curricula.
3. **Run complete mock rounds.** Include interruptions and changed constraints. Have an independent
   reviewer inspect reasoning and evidence; model praise alone is not a score. Actual interviews
   provide separate feedback and may change the next practice task.
4. **Prepare each company just in time.** Read the current role and team/product context; confirm
   coding language, format and loop with the recruiter. Map two genuine accomplishments to the
   role and rehearse the hardest likely technical discussion. Do not memorize company trivia or
   claim that a historical question bank predicts today's loop.
5. **Review outcomes.** Distinguish no response, screen rejection, technical failure and leveling
   feedback. Each implies a different correction. Revisit the target mix if evidence supports it;
   do not respond to every setback by adding more frameworks to study.

## One curriculum across IC levels

Senior, Staff and Principal share core technical domains. **ASSUMED, company-dependent:** the
expected independence, ambiguity, depth and organizational scope generally rise with level.
Titles are not standardized; verify the particular team's role and interview rubric.

| Shared exercise | Senior-ready discussion | Staff/Principal extension |
|---|---|---|
| Inference service | Build and operate the service; diagnose failures; justify local choices. | Define service boundaries/SLOs across teams; capacity economics; migration and adoption strategy. |
| Distributed workflow | Correct state transitions, retries, data model and recovery. | Cross-team contracts, evolutionary architecture, blast radius, ownership and competing priorities. |
| ML/evaluation | Choose metrics and diagnose model/system failure. | Connect technical metrics to product risk, rollout decisions, reproducibility and platform leverage. |

The higher-level extensions require actual scope evidence, not more management interview modules.
Keep the official Adobe title accurate in public materials; desired level belongs in targeting.

## Profile and application preparation

Run alongside stages 1–2: correct San Jose location, prepare LinkedIn headline/About/Experience,
correct the GitHub location, and align the résumé and paper citation. Use the concrete copy and
execution checklist in `/home/colligo/hs_scripts/claude/dev_research/positioning/POSITIONING.md`.
No public portfolio build is required before the first applications.

Hooman will request application assistance after the plan and profile are ready. When requested:
verify a small first set of live employer roles, choose the best-fitting IC roles, tailor from one
accurate résumé, and track every next action. Resolve salary range, work arrangement and actual
role constraints from the live posting/conversation. The old approximately $500K total compensation
is historical context, not an assumed new minimum or equivalent to $200K base.

An accepted offer within two months is ambitious from zero conversations; readiness and recruiting
must overlap. Avoid spending the entire first month polishing before beginning the pipeline. This
is a recommendation about sequencing, not authorization to apply or send messages now.

## Reuse and defer

Reuse these resources as targeted references, not cover-to-cover prerequisites:

- `/home/colligo/hs_scripts/claude/dev_research/learning/inference-baseline.md` — retained serving
  notes, baseline lab, quiz and collapsible answer key; inspect versions before use and attempt the
  quiz before opening its answers. This replaces the old cycle/week reference layout.
- `/home/colligo/hs_scripts/claude/dev_research/learning/attention.md` — attention, prefill/decode,
  FlashAttention versus PagedAttention, and implementation evidence.
- `/home/colligo/hs_scripts/claude/dev_research/learning/lora.md` — low-rank math and limitations;
  examples are mainly diffusion/image/video, not an LLM SFT exercise.
- `/home/colligo/hs_scripts/claude/dev_research/research/plan-comparison/SUMMARY.md` — friend-method
  comparison, design/coding rubric and correctness caveats; its old schedule is superseded.
- `/home/colligo/hs_scripts/claude/dev_research/career/CAREER_EVIDENCE.md` — real technical stories.

Defer broad CUDA/Triton study, multi-node deployment, an SGLang/Dynamo bake-off, a complete production
platform, a full LoRA training pipeline, and new public portfolio construction unless a target or
assessment justifies them. Reuse existing work before building. For every applicable technical
packet, inspect current Adobe code/documentation when accessible and explain its security boundary.
A blocked internal source does not block learning the general concept.

The previous full schedule is preserved in Git commit
`b2ff360a25da04ea8c32ea674ba12c3a6767b1a6` for
`/home/colligo/hs_scripts/claude/dev_research/learning/LEARNING_PLAN.md`.
Its detailed labs remain optional depth material, not concurrent requirements.

## Agent execution and review

**USER-CONFIRMED workflow:** primary agent plans, resolves ambiguity, integrates and reviews;
GPT-5.6 at extra-high effort handles bounded execution. This session successfully dispatched
`gpt-5.6-sol` with `xhigh` using explicit model overrides. This verifies availability here, not a
claim of unlimited quota or identical quality across models.

| Owner | Work | Completion check |
|---|---|---|
| Primary/Astra | Choose the next competency and scope, resolve conflicting evidence, review technical reasoning and consequential public claims. | Priorities match this plan and actual performance; final claims are supported. |
| GPT-5.6 xhigh | Draft the next exercise/answer key, collect bounded primary sources, prepare profile variants, implement specified helpers, run meaningful checks. | Returns exact paths, sources, diff, validation and unresolved gaps; no invented results. |
| Hooman | Solve/explain unaided, identify unclear teaching, review public wording and authorize external actions. | Human performance is recorded separately from model-generated artifacts. |

Send a compact task packet, not the whole conversation: goal, exact input paths, confirmed
constraints, output path, source/evidence rules, acceptance gate and stopping condition. Generate
only the next study packet and a separate answer key. Keep independent source/profile work
parallel; integrate lessons before assigning dependent exercises. Workers do not edit shared
canonical summaries. Canonical teaching lives in one packet; remove temporary duplicate prose once
integrated and retain essential audit data.

Use shell/Python for deterministic inventories, arithmetic, formatting and link checks. Escalate
contradictory sources, ambiguous claims, changed scope, repeated task failure or external actions
to the primary agent. Review every public career claim and core technical invariant; spot-check
routine extraction. If quality slips, narrow the task or change reviewer/model rather than silently
accepting lower quality. Do not ask two models to research the entire project independently.

Official OpenAI documentation on agent-specific model/reasoning configuration was fetched November 9:
https://developers.openai.com/codex/multi-agent/ . It does not establish the quota of this deployment.
Local HTTP and stream retries in `/home/colligo/.codex/config.toml` are already 100; no setting was
changed. More retries do not increase the provider's token allowance. Small tasks and selective
Astra review reduce requests sent to the constrained model.

## Evidence and limitations

The curriculum is a **RECOMMENDATION**, with high confidence about documented omissions and the
user's new constraints; moderate confidence in the initial allocation until performance is observed.
Evidence: the November 9 replies; the October 14 comparison of all 47 friend files; existing
teaching material; and the September 15, 60-posting market snapshot. That sample shows topic
mentions, not current vacancies, required/preferred frequencies or interview-question frequencies.

The friend archive was sanitized and contains no complete personal schedule/outcome record. Its
method is reusable; neither its examples nor our original plan prove interview success. The raw
archive and several old inputs are now missing from volatile storage. Durable summaries and
historical checks remain; no new raw-archive reading is claimed.

A credible alternative is specialist-first preparation when an actual imminent interview demands
kernel/model implementation. That would change the next stage. Another is more coding immediately
if a diagnostic reveals a severe gap; for now respect the requested initial systems/ML pass while
keeping coding inside month one. These are reversible allocations.

## Primary resources

Historical resource list checked 2026-10-04; not all links or current package versions were reverified
November 9. Read only the section needed for the current exercise; workers must verify decision-driving
claims and commands when building that packet.

### vLLM and inference

- https://docs.vllm.ai/en/latest/getting_started/quickstart/
- https://docs.vllm.ai/en/latest/design/metrics/
- https://docs.vllm.ai/en/latest/contributing/benchmarks/
- https://docs.vllm.ai/en/latest/serving/parallelism_scaling/
- https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/
- https://docs.vllm.ai/en/latest/features/quantization/
- https://docs.vllm.ai/en/latest/features/speculative_decoding/
- https://docs.vllm.ai/en/latest/features/lora/
- https://docs.sglang.ai/
- https://docs.nvidia.com/dynamo/latest/

### GPU and profiling

- https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html
- https://triton-lang.org/main/getting-started/tutorials/index.html
- https://docs.pytorch.org/tutorials/recipes/recipes/profiler_recipe.html
- https://docs.nvidia.com/nsight-systems/UserGuide/index.html

### Kubernetes and observability

- https://kubernetes.io/docs/tutorials/kubernetes-basics/
- https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/
- https://docs.nvidia.com/datacenter/cloud-native/gpu-telemetry/latest/dcgm-exporter.html
- https://prometheus.io/docs/introduction/overview/
- https://prometheus.io/docs/prometheus/latest/getting_started/

### LoRA and fine-tuning

- https://huggingface.co/docs/peft/main/en/developer_guides/lora
- https://huggingface.co/docs/trl/main/en/sft_trainer

## Next action

Start stage 1 with the expanded teaching guide at
`/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/REVIEW_GUIDE.md`.
Understand the diagrams and worked example, then use the separate practice prompt at
`/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/STUDY_GUIDE.md`. Then complete
stage 2's bounded ML/inference pass and begin stage 3 coding. Record completed attempts and the next
weak point in `/home/colligo/hs_scripts/claude/dev_research/PROJECT_STATE.md`; no completion is assumed.
