# Study-plan comparison — interview preparation and technical depth

As of: 2026-10-14. **Status: complete comparison; revised schedule is a proposal, not an accepted replacement.**

**November 9 update:** The comparison below is historical and complete. Its 12-week/5.5-hour
proposal is superseded by Hooman's accelerated goal and the current sequence in
`/home/colligo/hs_scripts/claude/dev_research/learning/LEARNING_PLAN.md`. The original ZIP and
extracted source directory are now missing from volatile storage; the source ledger and historical
validation results survive. No new raw-source reading or validation run is claimed.

## Contents

- [Recommendation](#recommendation)
- [Evidence and scope](#evidence-and-scope)
- [How the approaches differ](#how-the-approaches-differ)
- [Topic-by-topic comparison](#topic-by-topic-comparison)
- [What our original plan got wrong](#what-our-original-plan-got-wrong)
- [What to adopt and correct in the shared material](#what-to-adopt-and-correct-in-the-shared-material)
- [Proposed 12-week replacement](#proposed-12-week-replacement)
- [First week and assessment gates](#first-week-and-assessment-gates)
- [Keep the useful platform work](#keep-the-useful-platform-work)
- [Source quality and validation](#source-quality-and-validation)
- [Sources and complete reading record](#sources-and-complete-reading-record)
- [Open inputs and next decision](#open-inputs-and-next-decision)
- [Retry-setting check](#retry-setting-check)

## Recommendation

**Adopt the friend’s interview-oriented organization and practice method, then build a schedule for Hooman. Replace the existing 36-week sequence as the default readiness schedule; retain its strongest serving exercises as a smaller technical-depth track. Do not copy the shared workspace wholesale.**

This is a **RECOMMENDATION**, with high confidence in the documented coverage and sequencing differences, and moderate confidence that the proposed allocation is the better use of Hooman’s next study hours. Neither workspace contains outcome evidence proving one method produces more offers.

Hooman’s concern is supported: our plan is practical at operating and measuring an inference service, but it under-schedules several capabilities needed to demonstrate readiness in an interview. His friend’s material repeatedly practices turning an ambiguous question into a bounded design, explaining it, and handling failure and follow-ups. The strongest revision combines that practice with measured technical depth and Hooman’s existing career evidence.

The archive is explicitly a **sanitized template**. The actual weekly schedule, study capacity, personal answers, applications and most interview records are placeholders. Consequently, there is no complete personal schedule here to adopt directly. Its worked examples are useful source material, not a certified answer key.

**Planning assumptions:** retain the previously confirmed 5–6 hours/week, Staff/Principal AI platform/inference and customer AI targets, private Adobe/Pluto use where available, and bounded modeling scope. A 12-week proposal is a first review horizon, not a promise of interview readiness in 12 weeks. A confirmed imminent interview would change ordering and allocation. Equal qualifications and target jobs are USER-CONFIRMED; equal current fluency is not established.

## Evidence and scope

Hooman requested a full archive reading, comparison of approach and topics, and advice on adoption or modification. All **47 source files**, totaling **231,063 uncompressed bytes**, were read completely, including the code and tooling. No application, Slack or OCR tool was run. The three self-contained coding examples were subsequently executed and checked locally.

| Source class | Files | Treatment |
|---|---:|---|
| Root instructions, README and Makefile | 3 | Read as the friend’s operating method |
| Personal background, résumé and LinkedIn templates | 3 | Placeholders; no invented personal facts |
| Preparation entry points and procedures | 8 | Read for schedule, study and rehearsal structure |
| Company-record template and Netflix culture note | 2 | Distinguish placeholders from authored study content |
| Worked system designs | 7 | Read in full; inspect representative correctness gaps |
| Coding exercises and SQL note | 4 | Read in full; run the three Python examples |
| ML infrastructure/company notes | 5 | Read in full; external technical claims require their own verification |
| Search tracker, procedures and example application | 5 | Workflow/template evidence, not real applications |
| Planning procedure and examples | 3 | Workflow/template evidence |
| Supporting tools | 7 | Full code inspection; do not adopt automatically |
| **Total** | **47** | **Complete source reading** |

The current curriculum, Week 1 packet, attention and LoRA notes, career inventory, market summaries, decisions and live handoff were also reviewed. Current plan and source hashes are retained in the manifest [A1]. The 60-posting market sample is a **2026-09-15 snapshot**, not a current application shortlist or a measurement of interview-round frequency. Its unresolved required/preferred normalization remains unresolved.

**Labels used here:** VERIFIED means direct inspection or a stated local reproduction, limited to its scope and date; USER-CONFIRMED means Hooman’s stated preferences/account; ASSUMED means a planning inference; RECOMMENDATION means proposed action; UNVERIFIED means unsupported or not independently checked. Document observations below are VERIFIED as of 2026-10-14; judgments and future allocations are recommendations, not observed outcomes.

## How the approaches differ

| Dimension | Friend’s shared material | Our current plan | Implication |
|---|---|---|---|
| Organizing question | What must I explain, solve and rehearse for an interview area or upcoming round? | What must I build and measure to operate a credible inference platform? | Use interview capabilities to choose study units; use experiments to support difficult answers. |
| Unit of progress | An exercise, a worked design, a reading takeaway, a practiced answer | A weekly platform capability and experiment | Measure unaided performance as well as saved artifacts. |
| Schedule | Template for weekly work, interview calendar and next actions; actual schedule removed | Detailed first 12 weeks and two further 12-week cycles | Keep a short rolling schedule and reassess from performance. |
| Feedback | Coding tests, lessons from mistakes, company conversations, design pacing | Measurements, weekly verbal explanations, questions every four weeks, cycle demos | Start timed coding and complete design rehearsal immediately. |
| Breadth | Coding, SQL/distributed systems, ML infrastructure, behavioral, screening, company context | Serving/performance dominates, followed by deeper runtime and later customer workflow | Bring missing interview areas into every week. |
| Technical depth | Compact explanations, trade-offs and selected production case studies | Explicit GPU experiments, benchmark controls, deployment and profiling | Preserve a small measured lab; add depth when a target or diagnosis warrants it. |
| Personal evidence | Intended reuse of first-person career accounts; shared copy is blank | Substantial Adobe/Aupera evidence, but no active story-rehearsal schedule | Convert existing evidence into spoken answers now. |
| Information management | One daily entry point, concise topic indexes, one note per substantial concept | Strong provenance and durable handoffs, plus substantial process and curriculum documents | Keep research bookkeeping out of Hooman’s weekly study burden. |

The friend’s root instructions explicitly remember an earlier attempt where **“process grew faster than study.”** That is evidence of a workflow lesson, not proof of interview success. It is directly relevant to keeping this project usable.

## Topic-by-topic comparison

“Scheduled” means the curriculum names future work; it does not imply Hooman has completed it. “Present” means the shared archive contains material, not that the friend mastered it.

| Topic | Friend: what is actually present | Ours: what is actually present/scheduled | Proposed treatment |
|---|---|---|---|
| Timed coding and data structures | Rotate image; hit counter; map/heap TTL cache; tests and complexity discussions. Actual timed performance missing. | Python self-rating; implementation work, but no recurring algorithm/coding-interview block. | Add weekly blank-editor practice, review and a variant. Expand from three examples only when the diagnostic shows the need. |
| SQL and graph traversal | Recursive CTE/BFS, cycle behavior, schemas and access patterns in designs. | No explicit SQL interview practice. | Add bounded SQL, joins/indexes and graph reasoning. |
| Transactions and consistency | CAS/version checks, idempotency, reconciliation, partitioning, offline synchronization. | Distributed systems taught mostly through GPU parallelism, orchestration and failure labs. | Make storage correctness and external side effects core, using Hooman’s data/workflow experience. |
| General system design | Seven worked cases: payments, book purchasing, Twitter, WhatsApp, deletion-aware chat, metadata filesystem and YouTube. | Architecture reviews and a serving artifact; no comparable bank of complete non-serving designs. | Practice a few distinct problem families with variations; do not memorize all seven. |
| Interview communication | Explicit APIs → data → map → flows → scale/failure; simple design by minute 20, extensions by 30, failures by 40. | Five-minute weekly explanations; longer demos/reviews at cycle gates. | Rehearse a full answer under time pressure and respond to changed constraints. |
| LLM serving mechanics | Prefill/decode, KV memory, continuous batching, prefix caching, chunked prefill, metrics. | Week 1–4 plus attention notes and later engine internals. | Strong overlap. Reuse existing material; link each concept to a design decision and one observation. |
| Serving scale/routing | Replicas versus sharding, cache locality, llm-d/Dynamo, prefill/decode separation, goodput. | TP in week 6; advanced routing/engine comparisons mainly weeks 19–24; gateway later. | Move architectural reasoning earlier; multi-node implementation can remain optional. |
| GPU/CUDA/Triton/profiling | Conceptual coverage and references; no supplied GPU experiment suite. | Detailed profiling, precision and parallelism work; CUDA/Triton weeks 13–16. | Keep memory/bandwidth/compute/collective literacy early; specialist kernel labs depend on target and assessed gap. |
| Kubernetes and operations | Discussed through serving, Netflix orchestration and platform examples; no supplied K8s lab. | Explicit foundations and GPU deployment weeks 9–10; observability/failure week 11. | Retain a small deployment/debugging exercise because the recorded K8s baseline is 0/3. Avoid a production dashboard project as an early prerequisite. |
| Data/workflow platforms | Metadata filesystem, YouTube DAG, Metaflow/Maestro, researcher workflow and lifecycle references. | Narrower inference-first sequence; broader data work primarily exists in career evidence. | Add workflow retry/recovery, lineage and metadata reasoning; directly relevant to Glimmer/Kaizen stories. |
| Structured output and engine state | Detailed constrained decoding: masks, request identity versus batch slot, partial prefill and preemption. | Sampling/chat templates covered; constrained decoding has no comparable dedicated module. | Add one focused failure/constraint exercise; distinguish valid syntax from valid business output. |
| Training/post-training/LoRA | Netflix post-training/RL/DPO reading links; no complete supplied training lab. | Detailed LoRA note; training/serving exercise weeks 31–32. | Teach the operational overview early; perform an adapter experiment if a target or diagnostic justifies it. Neither archive supports broad modeling-interview readiness. |
| Evaluation and customer AI | Readings and product/gateway context; no substantial supplied end-to-end evaluated FDE exercise. | Explicit customer-success contract weeks 25–26 and eval/tracing weeks 29–30. | Keep this differentiator and move a small customer/evaluation design into the first block. |
| Behavioral and leadership | Real question categories, concise answer form and Netflix prompts; actual stories removed. | Strong raw career evidence; most interview-story work remains a future action. | Rehearse real architecture, disagreement, failure and customer outcomes every week. |
| Company/product understanding | Netflix and Databricks notes; business, customers, serving products, recruiter links and culture. | Broad market research, little company-specific rehearsal. | Add only when a company/team becomes relevant; avoid memorizing volatile company numbers. |
| Reproducibility and proof | Testable coding exercises and reasoned notes, but no measured serving artifact supplied. | Strongest area: version pins, workload control, repeated runs, quality and recovery gates. | Preserve evidence discipline and a compact lab. |

## What our original plan got wrong

1. **It committed too much of the default schedule to one project before measuring interview gaps.** At the default 5.5 hours/week, 36 weeks represents **198 hours** (180–216 at the stated 5–6 range). Building a platform has proof value in Hooman’s own history, but that does not establish that it deserves nearly the whole initial schedule.
2. **It conflated Python proficiency with preparedness for a constrained coding round.** Writing production code and solving an unfamiliar timed problem are different capabilities. The curriculum needs direct evidence for both; a 3/3 self-rating does not settle the second.
3. **It underrepresented core distributed-system reasoning outside inference.** Queue ownership, transaction boundaries, retryable side effects, consistency, indexing, pagination and data lifecycle are useful across the target roles and connect naturally to Hooman’s experience.
4. **It delayed customer/evaluation breadth despite making it a target family.** Customer workflow begins at week 25 and evaluation/tracing at weeks 29–30. Small versions should appear much earlier. This does not mean recreating a whole customer product immediately.
5. **It delayed learning whether Hooman can perform a full interview.** Weekly verbal explanations are valuable, but they do not test a 40-minute design with interruptions and follow-ups or a coding exercise from a blank editor.
6. **It allowed the first packet to grow beyond its initial budget.** Its eight required public readings total roughly 115–120 minutes, plus 30–40 minutes of notes, a 180-minute lab and a 30–45 minute review/quiz: about **355–385 minutes**, before additional required Adobe orientation. These are the packet’s estimates, not measured study times. The upper bound exceeds six hours before the internal reading.

The original plan also got important things right: primary resources, controlled experiments, private compute, honest quality/performance trade-offs, security boundaries, and one coherent artifact. Those are worth retaining. Its error is allocation and sequencing, not the idea of hands-on learning.

## What to adopt and correct in the shared material

### Adopt

- One short weekly entry point with specific exercises and completion evidence.
- Separate practice in coding, design, domain depth, and career narrative.
- Start with a simple design, then justify each extra component through a requirement or measured constraint.
- Work through concrete failures: timeout after a successful side effect, duplicate delivery, stale cache, worker death, offline deletion.
- Read production case studies critically and connect them to one’s own work.
- Keep a short mistake record: failed assumption, missing invariant/test, corrected answer, and next reattempt.
- Prepare company-specific material just in time, informed by a real role or recruiter brief.

### Correct or qualify

These are examples from a bounded quality check, not an exhaustive defect audit or a judgment of the friend’s ability.

| Source | Finding and evidence | How to use it safely |
|---|---|---|
| Twitter design [F3] | It uses a full 64-bit Snowflake ID as a Redis sorted-set score. Redis documents exact integer representation only through ±2^53 [P1]; two distinct example IDs collide as binary64 scores [A2]. The member strings remain distinct, but numeric cursor/ordering assumptions need repair. | Choose a lossless ordering/cursor scheme, such as a fixed-width lexicographic ID index, or a timestamp score with explicit tie handling. |
| Book purchase design [F4] | The worker claim accepts both `pending` and `running`. Two sequential claim attempts both match [A2]; the predicate does not establish the assumed single writer. Queue visibility alone is not exclusive ownership. | Define an atomic claim, owner/lease and recovery semantics; protect external actions with stable idempotency keys. |
| Payment design [F5] | The failure discussion says a crash leaves a `pending` transaction for reconciliation, but its query selects only `pending_resolution`. This is an internal inconsistency in the written design. | Reconcile stale ambiguous states, including `pending`, using the provider contract; distinguish no result yet from authoritative non-execution. |
| Hit counter [F6] | Original assertions pass, but its test moves time backward twice despite requiring non-decreasing calls. Separate valid monotonic tests passed [A2]. | Repair the example test contract before treating it as a template. This is not evidence that the implementation fails under its documented input contract. |
| General storage framework [F2] | Specific writer/QPS/storage thresholds and “always SQL” style rules are presented compactly. They are workload assumptions and teaching heuristics, not universal architectural laws. | Ask for requirements/SLOs first, state estimates, and choose storage from access patterns, invariants and failure needs. |
| Company/business notes [F7] | Many precise October 2026 numbers, product limits and architectural claims. They were not independently audited in full here. | Recheck the few facts needed for a real interview; do not memorize the whole table as verified truth. |

A further useful lesson is to test a proposed recovery mechanism at every crash boundary. For example, a database write followed by a Redis decrement is not automatically one atomic operation. Several notes make strong recovery claims that need a more explicit state machine before they become implementation specifications.

**Avoid copying the tooling by default.** It is convenience infrastructure, not interview curriculum. The Markdown viewer sends PlantUML diagram source to a public renderer and loads remote browser scripts [F8]. For confidential Adobe diagrams, use local rendering or existing approved tools. The OCR scripts send images to an API, and the Slack reader opens/gets a self-DM. None is needed to adopt the study method; none was executed in this review.

## Proposed 12-week replacement

**PROPOSAL — NOT YET CONFIRMED.** Eight weeks of broad practice, followed by four weeks driven by measured weaknesses and concrete target roles. At 5.5 hours/week this is **66 hours**, including 44 hours in the first block. It intentionally does not promise all the depth of the old 198-hour program in one-third the time.

### Weekly budget

| Work | Minutes | Completion evidence |
|---|---:|---|
| Coding | 90 | 45-minute unaided attempt, 30-minute review, 15-minute reattempt or variation |
| System design | 90 | 40–45-minute narrated design, review, one changed constraint |
| ML infrastructure / focused lab | 120 | Selected reading and Adobe cross-check, a small experiment or failure trace, then an explanation; all inside the two hours |
| Career narrative and next-week update | 30 | One spoken answer with a follow-up; a short record of the gap and next action |
| **Total** | **330 = 5.5 hours** | No additional compulsory reading or administration |

Use four study blocks if convenient; daily study is not assumed. Unfinished exercises consume the next relevant block. Additions replace planned work. Mock interviews occupy existing coding/design/domain blocks rather than becoming extra homework.

### Eight-week core

The rows identify bounded prompts, not a mandate to master entire subjects in one week. In each domain block, read only enough to answer the question or run the experiment. A lab that overruns replaces the next domain task.

| Week | Coding focus | Design prompt | Two-hour domain focus |
|---|---|---|---|
| 1 | Diagnostic: TTL cache with explicit expiry and complexity | Design a multi-tenant LLM endpoint from a blank page | Explain prefill/decode and derive KV memory; inspect what baseline already exists; identify the actual gaps |
| 2 | Hit counter; boundary tests and monotonic time | Chat with offline deletion: delivery, ordering, retention | Complete/reuse the single-GPU baseline; pin versions, preserve the exact request and restart result; continue into week 3 if necessary |
| 3 | Heap/top-k or merging streams, chosen from the diagnostic | Feed/fan-out or a smaller equivalent queue/cache problem | Measure one workload contrast: short versus long prompt, or low versus higher concurrency; explain TTFT, TPOT and throughput |
| 4 | Graph traversal plus a bounded SQL query | Strongly consistent metadata over object storage | Small K8s deployment/debug exercise or a concrete worker-recovery trace, selected from the demonstrated gap; first four-week assessment |
| 5 | Queue/scheduler problem: fairness and starvation | GPU serving: replicate versus shard, queue limits and cache-aware routing | Estimate memory and communication; compare TP1/TP2 only if the allocation is readily available, otherwise analyze a trace and record the missing experiment |
| 6 | Idempotent operation/deduplication problem | Workflow with external side effects; payment or book-purchase variation | Small customer AI evaluation exercise: fixed examples, success/failure definition, quality/latency/cost, and invalid-output handling |
| 7 | One weak coding pattern from prior attempts | Data/evaluation pipeline or video-processing DAG | Retry/resume/lineage reasoning; short practical overview of LoRA/SFT versus prompting/RAG, with a model-state/adapter explanation |
| 8 | Fresh timed problem plus follow-up | Fresh design with changed requirements | ML systems deep-dive mock and gap review; choose the next four weeks from evidence |

The first four weeks use a common interview foundation. The next four retain serving specialization while adding customer/evaluation and data-platform reasoning. The coding problems are transferable practice; they are not represented as confirmed current questions at a particular employer.

### Weeks 9–12: choose a branch, not three simultaneous curricula

Keep the same weekly budget. Coding and narrative continue; design and domain blocks are targeted using actual recruiter guidance, a current role or observed weakness.

| Branch | Focused domain/design work | Deferred unless relevant |
|---|---|---|
| Inference/performance | One profiling trace; scheduling/KV behavior; precision/quality experiment; collectives/topology; optionally one small Triton kernel if the target expects it | A broad kernel library, every serving engine, or multi-node deployment without a question to test |
| ML platform/infrastructure | Durable queues, workflow scheduling, metadata/lineage, quotas, developer experience, one deployment/failure exercise | General-purpose platform construction and large observability installations |
| Customer/FDE/applied AI | Requirements and acceptance criteria, structured output, retrieval or tool integration where needed, evaluation, tenant controls and cost per successful task | Deep GPU-kernel implementation unless the actual role includes it |

Week 9 establishes target-specific gaps; week 10 tests the hardest gap; week 11 rehearses a representative round with an unfamiliar variation; week 12 repeats the failed capabilities and reviews readiness. These are planning recommendations. If target-role evidence is still unavailable, choose the weakest assessed capability rather than guessing a company’s interview.

**If an interview is imminent:** replace the next week’s general case study with its confirmed round and recruiter brief. If coding already passes repeatedly, transfer some coding time to a demonstrated domain/design weakness. If inference explanations are shallow, retain more lab time. A schedule should respond to evidence rather than defend its original allocation.

## First week and assessment gates

This first week is deliberately usable without creating a new application, setting up a viewer, or deploying a platform.

1. **90 minutes — coding:** implement a TTL cache from a blank editor. Define the expiry boundary and refresh behavior first. Test it, give complexity, then handle a changed requirement. Inspect the friend’s solution only after the attempt. If already familiar with it, use a new cache/rate-limiter variation.
2. **90 minutes — design:** design a multi-tenant LLM endpoint. Clarify workload, latency/availability objectives and trust boundaries first; then API, data/control flow, admission, execution, retries and failure. At minute 30 introduce a long-prompt burst or GPU-worker failure. Preserve a single diagram and the two largest unanswered questions.
3. **120 minutes — technical depth:** explain prefill/decode, KV growth and batching without notes; derive a memory estimate; inspect existing environment/baseline artifacts if available. Use the remaining time to read and test the most important weak point. Adobe documentation or code inspection is part of this budget. Do not repeat completed setup just to satisfy a calendar row.
4. **30 minutes — narrative:** explain Glimmer 2.0 or a production video/evaluation project in three minutes, then answer two follow-ups about a decision, alternative or failure. Use documented evidence and honest uncertainty; record the next weak point.

Use one simple 0–3 scale: 0 = cannot yet do it; 1 = succeeds with substantial help; 2 = independently handles a bounded case; 3 = handles changed constraints and defends choices. This is a proposed learning rubric, not an employer hiring threshold.

- **Coding:** correct bounded solution, explicit invariants/complexity, relevant boundary tests, and a follow-up handled without a model writing the answer.
- **Design:** clarify the actual problem; produce a coherent simple system; justify the key data/consistency/scale choice; trace a failure; respond to a changed requirement inside 40–45 minutes.
- **Domain:** explain and estimate, connect to an observation, and distinguish measured results from expectations. A missing experiment remains missing evidence.
- **Narrative:** state personal role, decision, trade-off and outcome; handle attribution and metric questions without inventing details.

At weeks 4 and 8, repeat a fresh variant. Scores of 2 or better on repeated, unfamiliar bounded problems justify moving time elsewhere. Weak dimensions get more time; familiar answers memorized from notes do not count as a pass. Actual interview performance remains a separate observation.

## Keep the useful platform work

Retain the current Week 1 packet as a reference, not a compulsory wall of reading. Keep the attention and LoRA notes as targeted resources. Preserve all completed experiments; completion is currently unconfirmed.

The initial technical artifact can be small:

- a reproducible endpoint with the chosen model/environment and exact launch/request;
- a saved workload comparison with TTFT/TPOT/throughput and a clear limitation;
- one observed recovery behavior, or a clearly labeled missing experiment;
- a small fixed quality/evaluation set where comparing behaviors;
- a diagram and a five-minute explanation connecting the measurements to decisions.

Use existing vLLM benchmark/metrics tools before writing a new harness. Keep the metric definitions precise: the current vLLM page distinguishes inter-token latency from per-request TPOT [P3]. Do not present one request or a tiny sample as evidence about p99 or maximum throughput.

**Defer from the default first block:** a complete Prometheus/Grafana/DCGM setup, broad multi-node work, mandatory vLLM/SGLang bake-off, full kernel curriculum, elaborate gateway implementation and a production-size customer app. Reintroduce a component when a measured weakness or concrete target makes it valuable.

Reuse real career material early: Glimmer for state/recovery/architecture simplification; production video pipelines for technical transfer and workflow boundaries; Kaizen for evaluation/platform adoption; Foundry programs for ambiguous customer needs and delivery trade-offs. These are candidate story uses, not newly verified impact claims. Do not transfer the friend’s anecdotes into Hooman’s answers.

## Source quality and validation

### Local checks

The validation script [A2] verifies all extracted hashes against the source manifest, executes the original three Python examples, checks rotation against an independent reference for sizes 1–20, and checks hit-counter and both TTL implementations across 1,000 deterministic valid-time operations each. All those valid-input checks passed. It also records the hit-test time reversals, a binary64 score collision, and the non-exclusive book-worker claim predicate.

The archive contains four broken Markdown link occurrences pointing to two omitted documents: a data-processing note and a prior Meta interview record. A referenced coding procedure document is also absent. These omissions are consistent with a partial sanitized export; they do not show the original workspace lacks those materials. The manifest lists exact affected paths.

Seven worked designs and three small coding programs do not establish comprehensive interview coverage. The archive’s “interview reports say” claims and recruiter/candidate observations were not independently corroborated here. Its actual practice completion and outcome records are missing.

### Primary checks and Adobe context

- Redis’s official sorted-set documentation confirms the binary64 precision limit [P1].
- Stripe’s authorization/capture documentation makes expiry and method/network validity windows explicit [P2]; an authorization is not an unconditional timeless promise that capture must succeed.
- Current vLLM metrics documentation confirms the metrics used for the retained lab [P3].
- The Adobe checkout formerly referenced at `/home/colligo/colligo` is **absent in this environment**. No current Adobe implementation claim was verified from that checkout today.
- Existing internal synthesis pages were read [I1, I2]. Their July 2026 timestamps and documentation provenance remain visible. They support topics to revisit—worker/pipeline separation, queues, backpressure and recovery—but are not a substitute for checking the deployed implementation when executing a learning module.

This is sufficient evidence for a bounded curriculum comparison. It does not certify every technical claim, company statistic or linked article in either collection. A full audit of every external link would be a separate task.

### Alternatives and reversal conditions

- **Keep the old schedule:** reasonable if Hooman deliberately prioritizes deep platform construction over broad readiness, or assessments show interview fluency is already strong. It currently lacks evidence that those other capabilities are strong.
- **Copy the friend’s workspace unchanged:** useful as a personal template but incomplete as a curriculum, because the schedule and personal content were stripped and some examples need correction.
- **Recommended adaptation:** faster feedback across interview capabilities while retaining measured serving depth; its cost is less early implementation depth than the old program.

The recommendation should change if a confirmed interview loop demands extensive kernel/live-model implementation, if coding/design diagnostics repeatedly pass while domain depth fails, if available hours change, or if the purpose shifts explicitly toward long-term platform mastery. The cheapest validation is the proposed first week, followed by a fresh variant—not more broad job collection.

## Sources and complete reading record

### Hooman’s canonical material

- [H1] `/home/colligo/hs_scripts/claude/dev_research/learning/LEARNING_PLAN.md`
- [H2] `/home/colligo/hs_scripts/claude/dev_research/learning/inference-baseline.md` — consolidated
  November 9 from the original Week 1 packet. The October source manifest deliberately retains
  original paths and hashes; the pre-consolidation files remain in Git commit
  `403310d404a2ac7790df5cc2466e3cbb719aae27`.
- [H3] `/home/colligo/hs_scripts/claude/dev_research/career/CAREER_EVIDENCE.md`
- [H4] `/home/colligo/hs_scripts/claude/dev_research/research/job-market/SUMMARY.md`
- [H5] `/home/colligo/hs_scripts/claude/dev_research/DECISIONS.md`
- [H6] `/home/colligo/hs_scripts/claude/dev_research/learning/attention.md`
- [H7] `/home/colligo/hs_scripts/claude/dev_research/learning/lora.md`

### Shared archive and representative citations

Original: `/mnt/localssd/2026-b-share.zip`.
SHA-256: `72f7b97500cd3406ddaafb1106573fec547e8bee4b578095c0aedd9cf060e962`.
All 47 exact member/extracted paths and hashes appear in [A1]. Publication dates are not consistently recorded; retrieval/read date is 2026-10-14. The original README labels the copy sanitized.

- [F1] `/mnt/localssd/dev_research_inputs/friend-plan-2026-10-14/README.md`
- [F2] `/mnt/localssd/dev_research_inputs/friend-plan-2026-10-14/prep/system-design.md`
- [F3] `/mnt/localssd/dev_research_inputs/friend-plan-2026-10-14/prep/system-design/twitter.md`
- [F4] `/mnt/localssd/dev_research_inputs/friend-plan-2026-10-14/prep/system-design/book-price-aggregator.md`
- [F5] `/mnt/localssd/dev_research_inputs/friend-plan-2026-10-14/prep/system-design/payment-system.md`
- [F6] `/mnt/localssd/dev_research_inputs/friend-plan-2026-10-14/prep/coding/hit-counter.py`
- [F7] `/mnt/localssd/dev_research_inputs/friend-plan-2026-10-14/prep/ml-infra/databricks-business.md`
- [F8] `/mnt/localssd/dev_research_inputs/friend-plan-2026-10-14/tools/md-server.py`
- [F9] `/mnt/localssd/dev_research_inputs/friend-plan-2026-10-14/prep/README.md`
- [F10] `/mnt/localssd/dev_research_inputs/friend-plan-2026-10-14/prep/AGENTS.md`
- [F11] `/mnt/localssd/dev_research_inputs/friend-plan-2026-10-14/prep/ml-infra/llm-serving.md`
- [F12] `/mnt/localssd/dev_research_inputs/friend-plan-2026-10-14/prep/ml-infra/constrained-decoding.md`

### Primary external sources, opened 2026-10-14

- [P1] Redis, ZADD command reference, “Range of integer scores that can be expressed precisely”: https://redis.io/docs/latest/commands/zadd/
- [P2] Stripe, “Authorize and capture a payment separately”: https://docs.stripe.com/payments/place-a-hold-on-a-payment-method
- [P3] vLLM, “Metrics Design”: https://docs.vllm.ai/en/latest/design/metrics/
- [P4] OpenAI, configuration reference (retry check only): https://learn.chatgpt.com/docs/config-file/config-reference

### Internal documentary context

- [I1] `/home/colligo/hs_scripts/claude/obsidian/hs_base/wiki/concepts/colligo-inference.md` — updated 2026-07-04; synthesis of internal documentation.
- [I2] `/home/colligo/hs_scripts/claude/obsidian/hs_base/wiki/concepts/v3-inference-framework.md` — updated 2026-07-05; synthesis of internal documentation.

### Audit artifacts

- [A1] `/home/colligo/hs_scripts/claude/dev_research/research/plan-comparison/data/source-manifest.json`
- [A2] `/home/colligo/hs_scripts/claude/dev_research/research/plan-comparison/scripts/validate_examples.py`; results: `/home/colligo/hs_scripts/claude/dev_research/research/plan-comparison/data/example-validation.json`
- [A3] `/home/colligo/hs_scripts/claude/dev_research/research/plan-comparison/data/primary-source-checks.json`

## Open inputs and next decision

Five diagnostic questions were asked: desired interview horizon, weekly hours, completed work/current unaided capability, the friend’s actual interview feedback/outcomes, and the part of his approach Hooman finds most useful. Hooman subsequently instructed continuation twice while reporting rate limits; substantive diagnostic answers have not arrived.

The recommendations therefore use existing confirmed constraints and state the unknowns. No imminent interview, additional weekly hours, completed lab or successful interview outcome has been assumed. The comparison of the documents is complete; exact personal pacing remains adjustable. The actual current skill gap should be assessed through the first week rather than inferred from equal qualifications.

Next decision: retain the old default or accept/revise this proposed interview-oriented schedule. If accepted, integrate the chosen schedule into Hooman’s canonical learning plan, preserve useful resources/finished work, and create only the next week’s concise practice packet. Do not create a parallel set of competing active plans or import the friend’s operating instructions automatically.

## Retry-setting check

Official OpenAI documentation [P4] identifies `request_max_retries` for HTTP requests and `stream_max_retries` for stream interruptions. Both are already 100 in `/home/colligo/.codex/config.toml`. That file selects `gpt-5.6-sol`; the reported hosted-session error names `gpt-6-astra` in `eastus2`. It has not been established that this session reads that local provider configuration. No retry configuration was changed, and the rate limit was not claimed fixed.
