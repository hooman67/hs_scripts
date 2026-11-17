# Learnings

## 2026-11-16 — job-search workflow and Markdown viewer source review

- **[VERIFIED — REPOSITORY SOURCE]** `hooman67/job-search` is a Markdown/agent workflow plus uv
  helpers. Its `record-call` skill processes existing recordings; the Python helper calls OpenAI,
  while the agent separately performs digestion and Drive archival. Recording and continuous
  ingestion are not built-in services. Its original external-application/profile actions are manual.
- **[VERIFIED — REPOSITORY SOURCE]** `hooman67/md-viewer` 0.18.0 runs standalone with Python 3.13+
  and uv. Notes and Edit saves mutate source Markdown. The README understates current write
  capability. Browser CDNs and remote PlantUML rendering mean local serving is not fully offline.
- **[PRIMARY-VENDOR-DOC-SUPPORTED PROPOSAL]** MacWhisper supports local transcription, system
  audio and Pro local speaker recognition/watch-folder/CLI features. These were not tested;
  phone-only audio capture remains a separate boundary. Local transcription does not imply
  cloud-agent digestion is local.
- **[USER-CONFIRMED / CURRENT-MAC CHECK]** Mac only, all calls, no existing recordings, local
  transcription preferred, persistent viewer optional. Observed arm64/24 GiB/macOS 15.7.4;
  uv and the viewer were not installed at inspected paths. Recheck before setup.
- **Evidence and exact pinned revisions:**
  `/Users/ana.rodrigues/Desktop/hooman/hs_scripts/claude/dev_research/research/job-search-tooling/SUMMARY.md`.


## 2026-11-15 — inference memory and timing require explicit boundaries

- **[PRIMARY-DOC-SUPPORTED TEACHING PACKET — checked November 15]** PyTorch and Hugging Face
  documentation supports the distinction between learned parameters and inference state, batched
  projection shapes, chat serialization and per-layer K/V caching. Original attention/GQA papers
  support scaled causal attention and sharing K/V heads. The derived full-context KV payload is
  `2 × layers × KV_heads × head_dimension × total_cached_tokens × element_bytes`; allocator,
  activations and workspaces are separate. These are scoped teaching mechanisms, not measured
  hardware capacity or human performance. Exact links and assumptions are in the new lesson 2 guide.
- **[PRIMARY-DOC-SUPPORTED MEASUREMENT CLARIFICATION — vLLM metrics, checked November 15]** Client
  TTFT includes work before the first delivered token; queue and engine timings use different
  boundaries. The supplied trace explicitly uses `(last − first)/(N − 1)` for mean token interval,
  and aggregate throughput needs its own observation window. Its four invented timelines cannot
  establish p99 or service capacity. No current Adobe implementation or serving run was inspected.
- **[PRIMARY-DOC-SUPPORTED DISPATCH CLARIFICATION — AWS Batch SubmitJob, checked November 15]**
  Repeated submission with the same job name is not an API idempotency guarantee. An accepted
  request with a lost response can be retried as a second Batch job; application database claims
  must protect the one-logical-job contract. The existing diagram was preserved and clarified
  additively. No Batch job was submitted or cancellation/dispatch policy adopted.

## 2026-11-15 — cancellation separates publication safety from compute reclamation

- **[PRIMARY-DOC-SUPPORTED TEACHING CLARIFICATION — PyTorch, CUDA, Python/POSIX and vLLM,
  checked November 15]** Cooperative cancellation stops new GPU submissions at responsive safe
  boundaries; an already-launched asynchronous operation may finish. Forced process termination is
  suitable only when the process is isolated to the job and requires supervisor-managed cleanup,
  descendant handling and durable reconciliation. Shared servers need engine-level request aborts;
  current vLLM provides one such version-specific example. CUDA context destruction cleans its
  resources but OS signals do not certify instantaneous kernel cessation or allocation release.
  The internal endpoint path was unavailable from this Mac and no runtime cancellation experiment
  was performed. This is design guidance, not a user-adopted policy or evidence of implementation.

## 2026-11-15 — a cancellation controller is a durable responsibility, not a required service

- **[TEACHING CLARIFICATION — first review guide, section 8 Q&A]** A worker can conditionally
  transition `CANCEL_REQUESTED` to `CANCELLED` and then acknowledge its own notification under the
  tutorial's current rule. A fallback reconciliation path is still needed when no worker observes
  pending cancellation. The same responsibility may run in a worker, API or existing loop; a
  separate deployment is not inherently required. A direct API transition is another contract
  option when no intermediate cancellation work must finish. These are unadopted design alternatives,
  not deployment or runtime findings; changing job state does not mutate the SQS message.

## 2026-11-15 — early cancellation acknowledgement needs independent durable recovery

- **[DESIGN ALTERNATIVE — first review guide, section 8 Q&A]** SQS does not require waiting for
  `CANCELLED` before deleting a receipt. Deletion at `CANCEL_REQUESTED` can be safe only when a
  durable controller independently discovers pending cancellations and records their terminal
  outcomes. Keeping the notification preserves another inspection trigger but does not perform
  cancellation; deleting it does not stop computation. Once cancellation wins, guarded success
  publication and `RUNNING`-conditioned heartbeat/progress updates are no longer valid. This is
  illustrative policy reasoning, not a user-adopted change or runtime verification.

## 2026-11-15 — terminal-only object cleanup trades simplicity for later reclamation

- **[DESIGN ALTERNATIVE — first review guide, section 7 Q&A]** Waiting until a job is terminal
  avoids deciding which active-job attempts are permanently unable to finalize. It can safely
  remove unused uploads after terminalization while preserving the exact selected successful
  output for its retention period. The tradeoff is retained storage for stuck active jobs and a
  need to rediscover uploads that finish after the terminal transition. Early abandoned-attempt
  cleanup is a reclamation optimization, not a prerequisite for guarded result selection. This
  alternative is not user-adopted or runtime-tested and does not replace the guide's current policy.

## 2026-11-15 — an orphan upload is unselected, not necessarily jobless

- **[TEACHING CLARIFICATION — first review guide, section 7 Q&A]** The worker and object path can
  identify the producing job and attempt while no job row yet selects that exact S3 version as its
  official output. This window exists between upload and the guarded success update, and can persist
  after a crash or rejected stale-owner update. Current nonselection alone is unsafe evidence for
  deletion because finalization may still be in progress; cleanup must establish that the producing
  attempt can no longer finalize and preserve the selected version. This is illustrative design
  reasoning, not a deployment observation, new cleanup policy or human-mastery claim.

## 2026-11-15 — renewable leases bound missed heartbeats, not total job duration

- **[TEACHING CLARIFICATION — first review guide, section 6 Q&A]** A long-running attempt can
  remain current by renewing before expiry; the lease interval bounds time between successful
  renewals rather than total processing time. Renewal code must stay responsive during blocking
  work and allow operational margin. Repeated expiries need bounded recovery and investigation,
  while a separate job deadline or progress timeout handles workers that renew indefinitely.
  A heartbeat renews ownership but does not prove meaningful progress. The timeline is illustrative,
  not an executed test; the tutorial's strict expiry and guarded-completion checks remain unchanged.

## 2026-11-15 — lease expiry and supersession are distinct completion policies

- **[DESIGN REASONING — first review guide, section 6 Q&A]** Strict expiry rejects late completion
  even without a replacement owner. A different policy can allow late result selection while
  state, owner and attempt still match in the same protected database operation. Takeover and
  cancellation must use the same serialization boundary. The alternative can save completed work,
  but does not protect unrelated external effects or change the tutorial's selected policy.
  This is an illustrative design analysis, not observed production behavior or a user decision.

## 2026-11-15 — an unexpired lease does not establish worker health

- **[TEACHING CLARIFICATION — existing queue semantics and illustrative failure trace]** A
  worker may crash while its database lease remains valid, and a later receiver may receive the
  same SQS message rather than a second message. Deleting it can remove the queue-based recovery
  trigger. Early deletion remains an alternative when durable database recovery is responsible
  for unfinished work. The question, answer and timeline are preserved as a collapsible section
  beside the relevant paragraph. This is a design explanation, not a new experiment.

## 2026-11-15 — message visibility and job ownership protect different records

- **[TEACHING CLARIFICATION — existing AWS evidence and illustrative database design]** A job
  can have multiple queue messages, so hiding one message cannot establish ownership of the job.
  SQS visibility and the database lease expire and renew independently. The tutorial's guarded
  database writes enforce current ownership and state; a simpler duplicate-safe consumer can omit
  a separate database lease when its contract permits. Saved as a collapsible question/answer in
  section 6 of the first review guide. No new queue experiment or human mastery is inferred.

## 2026-11-15 — a job and its notification need not share an identifier

- **[DESIGN CLARIFICATION — user-requested note]** One outbox row per job can use a unique
  `job_id` without a separate `event_id`. Retaining multiple initial/recovery notifications for
  the same job needs a way to distinguish those rows; the tutorial uses separate event IDs.
  Retries of one reminder retain its ID. This is schema reasoning for the illustrative design,
  not a deployed-system finding or a duplicate-delivery guarantee. The explanation is saved beside
  section 5's outbox example in
  `/Users/ana.rodrigues/Desktop/hooman/hs_scripts/claude/dev_research/learning/first-pass/REVIEW_GUIDE.md`.

## 2026-11-12 — queue identity is separate from delivery identity

- **[VERIFIED — AWS DeleteMessage and visibility documentation, November 12]** Each receive of
  the same SQS message returns a new receipt handle. Another worker can receive that handle
  without updating the earlier worker. Old-handle deletion can report success without removing
  the message; visibility extension uses the current handle and does not issue another one.
- **[TEACHING CLARIFICATION]** Added the explicit timeout/redelivery timeline where the term first
  appears in the canonical guide. Possessing a handle does not establish indefinite visibility or
  job ownership. The example is illustrative; no live queue was used.

## 2026-11-12 — identity does not establish tenant permission by itself

- **[VERIFIED — RFC 8017 and local arithmetic, November 12]** RSA exponent recovery cannot drop
  the modulo after substitution: `m ≡ m^(d*e) (mod n)`. The private exponent is an inverse of `e`
  modulo `lambda(n)`, not modulo public `n`; known prime factors make that period/inverse easy
  to compute. The guide's deliberately insecure 55/3/7 example reproduces sign/verify results.
  Multiple valid exponents alone do not establish security; any usable equivalent exponent would
  suffice for an attacker. This is conceptual arithmetic, not a proof of cryptographic hardness.
- **[VERIFIED — RFCs 7515/7518/8017 and local experiment, November 12]** RS256 protects the exact
  encoded JWT header and payload, joined by a period. Verification checks the trusted RSA public
  key against the prescribed SHA-256 signature encoding; hashing or decoding alone is insufficient.
  The guide's in-memory demonstration accepted the original and rejected modified payload/header
  and wrong-key cases (Python 3.10.12, cryptography 50.0.2). It does not validate claim policy or
  prove a deployed authentication system secure; no real keys/tokens were used or persisted.
- **[VERIFIED — AWS primary documentation, November 12 follow-up]** A Cognito user pool has an
  issuer URL and a public JWKS endpoint. JWT `kid` selects a candidate verification key; signature,
  issuer and intended-use checks still determine validity. Rotation requires refresh, and a caller's
  arbitrary issuer/key URL cannot establish trust. The guide now makes these mechanics explicit
  with fictional settings and an expanded issuer/user/tenant table. No new curriculum decision.
- **[USER-REQUESTED CLARIFICATION]** Hooman asked how an API obtains the tenant from an
  authenticated identity. Added the concrete login/token/authorization flow to the canonical
  first review guide, including a diagram and membership examples.
- **[VERIFIED — AWS primary documentation, November 12]** Cognito issues signed access tokens;
  decoding their claims is not signature/issuer/expiry/intended-use validation. `client_id`
  identifies the application, not the customer tenant. Sources and limits are recorded in
  `/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/REVIEW_GUIDE.md`.
- **[DESIGN EXAMPLE]** A server-controlled active-membership table can map verified issuer/user
  identity to tenant and permissions. A requested tenant is acceptable only after checking that
  membership. Local signature validation alone does not implement immediate revocation. No Adobe
  authentication implementation, deployed system or human mastery is inferred.

## 2026-11-10 — foundational teaching needs a causal story

- **[USER-REPORTED]** The initial review guide introduced unfamiliar terms and too many facts
  before establishing the design and its purpose. Hooman specifically needed explanations of
  brokers/message infrastructure, JSON work notifications, outbox/reconciliation and who creates
  an idempotency key. This feedback is about teaching quality, not an unaided skill assessment.
- **[USER-CONFIRMED PREFERENCE]** Start with diagrams and one practical example, introduce terms
  once when needed, then add a failure and explain the corresponding fix/alternatives. Separate
  learning from interview presentation. Shorten future material as familiarity develops.
- **[VERIFIED — official docs, November 10]** SQS visibility does not establish database ownership;
  a receipt handle is distinct from a job ID. PostgreSQL uniqueness needs required non-null key
  fields; CURRENT_TIMESTAMP is transaction-start time. An S3 key alone does not pin a version.
  Evidence and precise limits are retained in
  `/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/data/source-checks-2026-11-10.json`.
- **[DESIGN REVIEW]** Keep queue-deletion policy consistent across success, retry and cancellation;
  protect final output selection and cleanup against competing attempts. The revised tutorial
  makes these decisions explicit. No executed-system correctness claim follows from document review.

## 2026-11-09 — useful evidence versus obsolete scaffolding

- **[VERIFIED — local inventory and content comparison]** The cleanup reduced this project from
  27 files to 24: two obsolete files removed, two reference files consolidated into one. All
  inference reference notes/lab material and 15 answers were preserved. Current deliverables retain
  their paths. The file index in `/home/colligo/hs_scripts/claude/dev_research/CLAUDE.md` is the entry
  point; no duplicate research index is needed.
- **[AGENT DECISION]** Preserve unique historical evidence and its provenance even if its original
  volatile input disappeared. Removing a source ledger or validation recipe would reduce auditability
  rather than simplify the current workflow. Historical manifests intentionally keep original paths.

## 2026-11-09 — accelerated planning and public evidence review

- **[USER-CONFIRMED]** First-month breadth and second-month depth serve an accepted-offer goal;
  system design/ML-inference comes before timed coding. Explaining experience is not the main
  weakness. IC roles only; Senior and Staff/Principal share a core but level-specific scope is a
  company-dependent planning interpretation, not a standardized requirement.
- **[VERIFIED — local audit]** Existing material covers inference concepts, attention, and LoRA
  mathematics, but saved teaching material is not evidence of completed human drills. The LoRA
  note's examples are primarily diffusion-centered; an LLM SFT exercise is a separate task.
- **[VERIFIED — public pages, November 9]** LinkedIn displays Vancouver and its About opening
  points to GitHub. GitHub displays Canada. Full signed-in LinkedIn fields remain inaccessible to
  the public fetch. Source record and proposed corrections are in
  `/home/colligo/hs_scripts/claude/dev_research/positioning/POSITIONING.md`.
- **[VERIFIED — CVF primary source, November 9]** The paper is in CVPR Workshops 2019, pages
  26–32, with Hooman first in the listed author order. Individual contribution is not inferred.
  The local résumé venue is corrected. The documented work supports “over a decade”; precise
  cumulative 12+ years would need a clarified definition/additional evidence.
- **[VERIFIED — filesystem check, November 9]** Real checkout is under `/home/colligo/hs_scripts`;
  old raw sources on `/mnt/localssd` are missing. Durable summaries/audit JSON remain, but do not
  constitute restored raw files. `/home/colligo/colligo` now exists, superseding the October
  environment-specific absence finding below; existence alone does not verify deployed behavior.
- **[VERIFIED — this session]** Two `gpt-5.6-sol` / `xhigh` workers completed independent evidence
  audits; root reviewed and integrated the results. Task splitting worked here. Equivalent model
  quality, unlimited quota and permanent elimination of rate limits have not been established.

## 2026-10-14 — interview preparation versus platform curriculum

Sources: all 47 files in `/mnt/localssd/2026-b-share.zip`, the current learning plan, and the
checks recorded in `/home/colligo/hs_scripts/claude/dev_research/research/plan-comparison/SUMMARY.md`.

- **[VERIFIED — source inspection]** The friend’s archive is explicitly sanitized. Its weekly
  schedule, personal answers and process outcomes are largely placeholders; its exercises and
  procedures support a method comparison, not claims about actual pace, mastery or hiring success.
- **[VERIFIED — document comparison]** The existing 36-week plan specifies substantial measured
  serving work but no recurring coding-interview block or comparable bank of general system-design
  rehearsals. It places customer workflow at weeks 25–26 and evaluation/tracing at weeks 29–30.
- **[RECOMMENDATION — NOT USER-ACCEPTED]** Organize the next study block around recurring coding,
  full design rehearsal, domain depth and real career stories; retain a smaller inference lab.
  Validate allocation through performance, not source counts or the apparent polish of notes.
- **[VERIFIED — bounded local checks and primary Redis docs]** The supplied Python examples pass
  valid-input checks, but a hit-counter test violates its time-order contract. Written designs
  contain a binary64/Snowflake ordering issue and an exclusive-worker claim gap. Useful examples
  still require critical reasoning; this is not a complete correctness audit of the archive.
- **[VERIFIED — filesystem check, current environment only]** `/home/colligo/colligo` is absent.
  Existing July 2026 wiki syntheses remain accessible but do not establish current production
  implementation behavior. Re-check access when a learning exercise needs current code.

## 2026-10-07 — first current résumé artifact

- **[USER-CONFIRMED]** Adobe start date is October 2023 and the current official title is Machine
  Learning Engineer, ASML.
- **[ARTIFACT CREATED]** A one-page Staff/Principal résumé now balances production inference and
  evaluation platforms, distributed data infrastructure, and hands-on enterprise AI delivery.
- **[OPEN]** The strongest next résumé improvement is to replace broad scope language with
  externally usable outcome metrics and clarify whether customer names may remain in every
  recipient-specific version.

Durable findings across career evidence, market research, learning, and positioning. Every
factual learning must include a source or project-experience note, date, and confidence label.

## 2026-09-15 — inherited research-method lessons

Source: current files and project summaries in `/home/colligo/hs_scripts/claude/auto_research`
and `/home/colligo/hs_scripts/claude/fin_research`, reviewed for this project's setup.

- **[VERIFIED — prior-project documentation]** Long-running work survives session or machine
  failure when the repository contains a short live checkpoint, explicit decisions, durable
  learnings, and one exact next action. Important results cannot live only in chat.
- **[VERIFIED — prior-project documentation]** A small number of canonical, human-readable
  Markdown files works better than many overlapping status notes. Separate topics only when they
  become substantial, and give each topic one summary that compounds over time.
- **[VERIFIED — prior-project documentation]** Research conclusions need evidence classes,
  source/as-of dates, contradiction checks, and an explicit separation between reported fact and
  analyst inference. Weak or missing evidence should remain visible rather than being smoothed
  into confident prose.
- **[VERIFIED — prior-project documentation]** Parallel work is valuable for independent source
  collection, while normalization, ranking, decisions, and canonical-summary edits need a single
  integrator. Dependency chains should remain serial.
- **[VERIFIED — prior-project documentation]** Reassess options on current evidence instead of
  defending an earlier choice because work has already been invested in it. Preserve a decision's
  rationale, but do not give it an incumbent advantage.

## 2026-09-15 — input inventory

- **[VERIFIED — source inspection]** The pre-Adobe résumé supplies a strong historical base in
  computer vision, production ML, C++/Python, Linux, real-time systems, deployment, customer
  requirements, and technical/team leadership. It is not evidence of current proficiency by
  itself; recency must be established separately.
- **[SUPERSEDED]** The first Adobe check-in exports contained only completion metadata. Hooman
  replaced them on 2026-09-15 with eight detailed exports; use the finding below.
- **[VERIFIED — source inspection]** The replacement Adobe exports contain substantial FY24–FY26
  employee narratives and limited but useful manager corroboration. They document a progression
  from production video inference and evaluation, through data-platform ownership and a hands-on
  Glimmer redesign, to Foundry customer/workflow leadership. Exact intra-year dates remain absent.
- **[CHECKIN-MANAGER-CORROBORATED]** A manager stated that Hooman exceeded expectations after
  taking over the data team, improved cross-team collaboration, and delivered vLLM integration and
  Marketplace 0.1 as foundational work. Later feedback affirmed major progress under difficult
  circumstances and identified situational decision-making and patience as growth areas.
- **[WORKING HYPOTHESIS]** Glimmer 2.0 is currently the best candidate for a deep Staff-level
  systems story; Clineto/VIQ and Kaizen provide strong model-to-production and evaluation stories;
  Data Marketplace and Foundry provide cross-organizational and customer-outcome stories.
- **[USER-CONFIRMED]** Hooman's Adobe experience spans hands-on AI/video pipelines, model
  integration and technical transfer, Foundry management plus IC work, shared data systems,
  multiple enterprise-customer programs, and a recent Home Depot rewriter. Scope and impact
  details remain to be documented.
- **[WORKING HYPOTHESIS]** Hooman may have unusually strong fit for roles that connect model
  capabilities, production systems, and customer workflows. This must be tested against current
  Staff/Principal market evidence and not protected from contradictory findings.

## 2026-09-15 — X-bookmark discovery batch

Source: all 327 items in `/mnt/localssd/x_bookmarks_2026-09-15/bookmarks.json`, selected external
links, and the primary sources cited in
`/home/colligo/hs_scripts/claude/dev_research/research/x-bookmarks/SUMMARY.md`.

- **[VERIFIED — current primary documentation]** vLLM, SGLang, and NVIDIA Dynamo expose a broad,
  concrete inference-systems surface: serving, scheduling, quantization, KV/cache management,
  distributed execution, routing, autoscaling, observability, and benchmarking.
- **[WORKING HYPOTHESIS]** Hooman's highest-leverage technical gaps are more likely to be deep
  GPU/runtime mechanics, modern serving-engine internals, performance engineering, and a
  reproducible proof artifact than general AI or introductory modeling. Confirm through career
  calibration and live Staff/Principal postings.
- **[VERIFIED — secondary study, not independently reproduced]** A published analysis of 113
  Forward Deployed Engineer postings found frequent customer engagement, production deployment,
  integration, requirements discovery, evaluation/monitoring, and product-feedback work.
- **[WORKING HYPOTHESIS]** Forward-deployed/customer AI systems is an important target role family,
  not merely a variant of engineering management. It may make Hooman's customer-program experience
  a differentiator while sharing the inference/platform learning core.
- **[WORKING HYPOTHESIS]** Evaluation, orchestration, context construction, routing, guardrails,
  observability, and task economics constitute an adjacent AI/harness engineering cluster worth
  measuring separately from both model research and core inference runtime work.
- **[VERIFIED — current Google role samples]** Modeling-heavy research-engineering paths ask for
  current framework, training, model-development, and sometimes publication depth. This supports
  keeping modeling as a deliberate secondary branch with its own evidence and gap assessment.
- **[VERIFIED — arXiv primary source]** A 1,902-run multi-agent coding study found that coordination
  structure and task shape matter; shared files reduced output tokens on message-heavy eight-agent
  work but added overhead when files already carried coordination. This reinforces selective—not
  automatic—parallelization.
- **[VERIFIED — OpenAI first-party article and arXiv memory paper]** Compact indexes and summaries
  paired with retrievable full evidence are a recurring long-horizon workflow pattern. This
  supports the project's live checkpoint plus topic-summary organization.

## 2026-09-15 — direction confirmed by Hooman

- **[USER-CONFIRMED]** Forward-deployed/customer AI engineering strongly matches Hooman's Foundry
  experience and should be treated as a target role family.
- **[USER-CONFIRMED]** Modeling should initially extend only through LoRA and practical
  fine-tuning; its ultimate importance remains uncertain.
- **[USER-CONFIRMED]** A deep inference-platform artifact has unusually high personal proof value:
  Hooman's Aupera inference platform and live interview demonstration were instrumental in his
  Adobe hiring. A modern successor is therefore supported by his own hiring history, not just by
  generic portfolio advice.

## 2026-09-15 — initial external market sample

Source: 60 active employer postings from 20 companies, preserved with retrieval dates and full
descriptions in
`/home/colligo/hs_scripts/claude/dev_research/research/job-market/postings.jsonl`; methodology and
limitations are in
`/home/colligo/hs_scripts/claude/dev_research/research/job-market/SUMMARY.md`.

- **[VERIFIED — sample-specific]** The inference/platform half strongly clusters around measured
  performance, GPUs, distributed systems, serving, orchestration, reliability/observability,
  Python, CUDA, and PyTorch. Kernel specialization is one depth track, not the whole field.
- **[VERIFIED — sample-specific]** The Forward Deployed/customer AI half strongly clusters around
  LLM systems, customer discovery, communication, agents, evaluation, Python, end-to-end delivery,
  and product feedback. Eighteen of the 30 selected roles are hands-on FDE/deployment/field
  engineering rather than solutions architecture or enablement.
- **[VERIFIED — sample-specific]** Fine-tuning, LoRA, post-training, or reinforcement-learning
  language appears in nine of 30 inference/platform postings and seven of 30 Forward
  Deployed/customer AI postings. It is relevant but not the dominant common theme.
- **[WORKING HYPOTHESIS]** The best positioning may be T-shaped: deep inference/platform systems
  plus unusually strong customer-workflow, evaluation, and business-outcome breadth.
- **[WORKING HYPOTHESIS]** The central portfolio artifact should span serving, performance,
  distributed orchestration, observability, failure behavior, and evaluation, with one realistic
  customer workflow layered on top. Exact scope awaits required/preferred normalization and the
  career-gap comparison.

## 2026-10-04 — learning baseline

- **[USER-CONFIRMED]** Learning may use Adobe/Pluto and two NVIDIA H200 GPUs. The artifact is
  private and need not be independently reproducible outside Adobe.
- **[USER-CONFIRMED]** Start with text inference and proceed incrementally; multimodal/video is a
  later option.
- **[USER-CONFIRMED SELF-ASSESSMENT]** Python 3/3; Docker, PyTorch, and vLLM 2/3; distributed
  systems 1/3; Kubernetes, CUDA, and Triton 0/3. Exercises must calibrate these ratings.
- **[AGENT DECISION]** Begin before required/preferred market normalization is complete. Use Cycle
  1 gates and the market audit to revise later cycles.

## 2026-10-05 — vLLM quickstart and Adobe implementation cross-check

Sources: current vLLM v0.31.0 documentation/source retrieved 2026-10-05; Hugging Face chat-template
documentation; local Adobe code under `/home/colligo/colligo`; and Obsidian pages
`[[wiki/concepts/colligo-inference]]`, `[[wiki/concepts/v3-inference-framework]]`,
`[[wiki/concepts/foundry-inference-auth-tokens]]`, and `[[wiki/concepts/mori-parallelism]]`.

- **[VERIFIED — current public primary source]** Offline `LLM.generate(...)` is synchronous: it
  queues the batch, steps the engine until all requests finish, and returns final outputs. Serving
  code that needs concurrency uses the separate `AsyncLLM` interface and consumes an async stream.
- **[VERIFIED — current public primary source]** Chat templates serialize role/content messages
  into the model-specific control-token sequence used during instruction tuning.
  `add_generation_prompt=True` normally marks the start of the assistant turn; it is not universal
  across every model template.
- **[VERIFIED — current public primary source]** Temperature rescales logits before sampling;
  top-p retains the smallest high-probability token set reaching a cumulative threshold. They are
  decoding controls, not model-training parameters.
- **[VERIFIED — vLLM v0.31.0 scope]** For ordinary compatible attention on NVIDIA Hopper, vLLM's
  current automatic priority prefers FlashAttention over FlashInfer, and FA3 is the default
  FlashAttention version on SM90. This is version/model/workload specific, not a universal speed
  ranking.
- **[VERIFIED — direct Adobe code inspection]** Current Foundry V3 code explicitly renders chat
  templates, uses `AsyncLLM.generate(...)` with `async for`, keeps HTTP concerns outside the GPU
  worker, and derives tensor-parallel size from allocated devices. Internal history uses different
  backend choices and workarounds across model/version combinations, reinforcing measurement over
  a fixed backend rule.
- **[VERIFIED — Adobe documentation/code, scoped to the inspected service]** The inner vLLM webapp
  assumes an in-cluster trust boundary and leaves authentication/authorization to the customer
  gateway. A standalone vLLM API key alone would not replace TLS, network isolation, authorization,
  quotas, audit controls, or safe prompt retention.
- **[UNVERIFIED — Week 1 Pluto environment]** The exact vLLM version, selected attention backend,
  topology, and MIG state on Hooman's allocated H200 remain to be recorded from the live job.
