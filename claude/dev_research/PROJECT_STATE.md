# Project State — Live Checkpoint

Last updated: **2026-11-15**, Codex queue-visibility/database-lease Q&A (prior work preserved).

## Contents

- [Current status](#current-status)
- [Cleanup and recovery](#cleanup-and-recovery)
- [Confirmed current direction](#confirmed-current-direction)
- [Canonical deliverables](#canonical-deliverables)
- [Batches completed and findings](#batches-completed-and-findings)
- [Source availability and environment](#source-availability-and-environment)
- [Historical completed work and parked backlog](#historical-completed-work-and-parked-backlog)
- [Remaining gaps](#remaining-gaps)
- [Next exact step](#next-exact-step)

## Current status

**Latest request, November 15 — parallel document additions and the next lesson:** the section 12
interview rehearsal sample is now saved beside the six-point presentation list, and section 10's
five-question alternatives expansion was independently reviewed. A Batch clarification was inserted:
an ambiguous accepted `SubmitJob` retry can launch duplicate Batch containers; each must acquire
application database ownership before work. All existing review-guide bytes, table and update/date
lines were preserved. These are teaching additions, not evidence of deployment or adopted policy.

**Lesson 2 prepared, November 15 — bounded ML/inference fundamentals:** the new guide and exercise
are at the absolute Mac paths indexed in `CLAUDE.md` and the learning plan. They explain tensors,
training/evaluation, causal generation, prefill/decode, GQA/KV memory, bandwidth/batching and trace
boundaries, with a closed answer key separate from the assignment. Official PyTorch, Hugging Face,
scikit-learn, vLLM, NVIDIA and original attention/GQA sources were checked. Model sizes and trace
timestamps are synthetic; arithmetic and structure were checked, with no live benchmark or endpoint.
Current internal monorepo access was unavailable at the checked Mac paths. No human completion,
mastery, curriculum advancement or current GPU allocation is inferred.

**Current exact next step:** after reading the two requested additions, make one short unaided
video-job design attempt using the existing `STUDY_GUIDE.md`; identify any reopened-guide parts.
Then read `ML_INFERENCE_GUIDE.md` and execute `ML_INFERENCE_EXERCISE.md`: local matrix arithmetic,
learning/evaluation scenarios, KV/weight memory estimate and supplied serving-trace analysis.
Bring the diagram, calculations/code, trace table and remaining questions for review before
starting the planned timed-coding stage. The older next-action paragraphs remain historical
resume context; this paragraph records the latest requested packet and immediate action.

**Workflow preference recorded, November 15 — answer first, update quietly:** answer every study-
document question immediately in the main thread, then delegate the authorized automatic
collapsible Q&A insertion to a separate background agent without user-facing progress or routine
completion interruptions. The updater retains both question and answer beside the relevant
passage and preserves all existing bytes, including date lines. No study guide was changed because
this request contained no new technical Q&A.

**Latest alternatives-table expansion saved, November 15:** added one section 10 clarification
covering DynamoDB key/access-pattern design, database-queue load and recovery measurement,
`FOR UPDATE SKIP LOCKED`, RabbitMQ/Amazon MQ/Kafka, and EC2/ECS/Fargate/AWS Batch. Bounded official
AWS, PostgreSQL, RabbitMQ and Apache Kafka sources support the explanations. All examples and load
figures are illustrative; no product choice, benchmark, failure drill, deployment, exercise
completion or mastery is recorded. Verified insertion-only preservation against fresh snapshots.

**Latest answer review saved, November 15 — six concept checks:** Hooman supplied answers to all
six section 11 understanding questions and received item-by-item feedback. The main corrections
cover SQS Standard ordering, SQS being outside the PostgreSQL job/outbox transaction, paused versus
dead workers, complete guarded-publication predicates, and S3 rather than database object versions.
The saved review also distinguishes receiving a notification, owning a job and publishing output.
The response format is unknown, so this is not labeled unaided or closed-book and does not establish
mastery, completion of the companion design exercise or permission to advance the curriculum.
Verified insertion-only changes against fresh snapshots. Next: revisit the corrected distinctions,
then attempt or continue the companion design prompt when Hooman is ready.

**Latest clarification saved, November 15 — stopping GPU work is separate from publication:**
added Hooman's cancellation tangent beside section 8's best-effort paragraph, including cooperative
safe-boundary checks, isolated-process escalation, shared-engine request aborts, a flow, conceptual
pseudocode and an execution-arrangement table. Bounded current PyTorch, NVIDIA CUDA, Python/POSIX
and vLLM primary documentation supports the scoped mechanics; the recorded internal endpoint was
unavailable from this Mac. No GPU work, signal, reset or cancellation path was run. This is design
guidance, not an adopted cancellation policy or deployment, and the original cancellation semantics
remain unchanged. Verified insertion-only changes against fresh snapshots. Next: distinguish
logical cancellation from physical resource reclamation, then continue section 9.

**Latest clarification saved, November 15 — cancellation controller is a responsibility:** added
Hooman's question, conceptual conditional transition and two-path flow beside section 8's controller
discussion. A worker may finalize `CANCEL_REQUESTED → CANCELLED`; reconciliation is the fallback
when no worker observes the request. The responsibility can live in a worker, API or reconciliation
loop, and committing `CANCELLED` changes the database state rather than an SQS message. These are
alternatives, not an adopted deployment or policy; the existing state machine, cancellation meaning
and terminal-only acknowledgement rule remain unchanged. Verified insertion-only changes against
fresh snapshots. Next: continue section 8's receipt and best-effort stopping discussion.

**Latest clarification saved, November 15 — cancellation completion and queue acknowledgement:**
added Hooman's question, state-flow diagram and supplied alternatives beside section 8's receipt
paragraph. The tutorial keeps deletion after the terminal `CANCELLED` outcome; early deletion at
`CANCEL_REQUESTED` is safe only when an independent durable controller will discover and finish
pending cancellation. Queue retention does not finish cancellation, deletion does not stop GPU
work, and guarded publication is already blocked after the cancellation transition. This is design
reasoning, not a selected policy or runtime test; the original acknowledgement and cancellation
rules remain unchanged. Verified insertion-only changes against fresh snapshots. Next: continue
section 8's state race and best-effort stopping discussion.

**Latest clarification saved, November 15 — terminal-only cleanup is a simpler alternative:**
added Hooman's question, a status/action table and the supplied limits beside section 7's cleanup
discussion. The alternative leaves active-job uploads alone, removes unused terminal-job uploads,
and preserves a successful job's exact selected version through its retention period. It may retain
stuck-job data and require a later pass for uploads completed after terminalization. This is design
reasoning, not a selected production policy or runtime test; the guide's existing grace, metadata
and selected-version protections remain unchanged. Verified insertion-only changes against fresh
snapshots. Next: continue section 7's two-write failure cases and then cancellation.

**Latest clarification saved, November 15 — an orphan upload can still name its job:** added
Hooman's question and explanation beside section 7's existing cleanup paragraph. It distinguishes
the producing job/attempt from the database's selected official output: an upload can exist between
the S3 write and guarded PostgreSQL success update, or remain unselected after a crash or ownership
loss. Cleanup must not race a still-authorized finalization and must preserve the selected version.
This is an illustrative flow, not a deployed test or adopted policy change. The original wording,
lease rules and output-selection design remain unchanged. Checked insertion-only changes against
pre-edit snapshots. Next: continue section 7's two-write failure cases and then cancellation.

**Latest clarification saved, November 15 — long jobs renew rather than age out:** added Hooman's
question and the supplied explanation beside section 6's lease/heartbeat definition. The example
keeps attempt 1 alive by renewing a two-minute lease every 30 seconds, distinguishes the database
lease from SQS visibility, and records responsive renewal, timing margins, bounded retries and a
separate stuck-job deadline/progress policy. The intervals are illustrative; no runtime test or
human mastery is claimed. Existing lease checks, strict completion rule, SQL and guide text remain
unchanged. Checked this batch against pre-edit snapshots. Next: continue the guarded-completion
example and section 7 after discussing any remaining lease questions.

**Latest clarification saved, November 15 — late success before takeover:** added a collapsible
question/answer beside section 6's expiry rule. Explained that the tutorial deliberately rejects
completion after expiry, while an alternative can accept late completion if a locked, atomic
transition still matches the running job, owner and attempt. Takeover or cancellation winning
first rejects that completion. This is a design alternative, not an adopted policy or runtime
test. Existing rule and SQL remain unchanged. Checked insertion-only changes against this batch's
snapshots. Next: discuss expiry versus supersession, then continue guarded completion and section 7.

**Latest request completed, November 15 — automatic collapsible Q&A:** Hooman requested the
notification-retention clarification and instructed that subsequent study questions and answers
be saved automatically as collapsible additions. Added that Q&A beside the quoted paragraph and
the earlier expired-lease question beside the claim example. Recorded the standing workflow in
global instructions and the decisions log. Checked this batch against snapshots of the current
documents: additions only, with the original guide text, SQL and date line preserved. No new
queue experiment or exercise completion is inferred. Next: continue section 6's takeover and
guarded-completion example; save future clarifications in the same way.

**Latest instruction and correction, November 15:** Hooman requires document additions to leave
all existing material untouched unless he explicitly requests edits. The guide's update line
was changed during the two additions; restored it and retained the requested outbox note and
collapsible visibility/lease Q&A. Verified that removing only these added blocks reproduces the
pre-addition guide byte for byte. Recorded the rule in global instructions and the decisions log.
Future additions must have insertion-only diffs, including no incidental date/formatting changes.
The lesson resume point below remains available; no completed study or new exercise is inferred.

**Completed November 15 queue-visibility/database-lease follow-up:** saved Hooman's question and
the explanation in a closed-by-default details section under section 6's two-timer discussion.
It covers the normal flow, multiple messages for one job, duplicate delivery, independently
expiring timers, guarded finalization and when a simpler consumer can omit a database lease.
The separate chat question about `RUNNING` with an expired lease was answered: the claim creates
a new attempt for the same job, not a continuation of the old attempt. Existing source evidence
was reused; no new queue experiment, deployment or completed human exercise is claimed.
Reviewed the added text, checked details/fence structure and Git whitespace, and preserved the
earlier outbox note. Next: continue section 6's takeover and guarded-completion example.

**Completed November 15 outbox-identifier clarification:** Hooman asked why the outbox needs
`event_id` rather than just `job_id` and `sent_at`, then requested that the explanation be saved.
Added the note beside section 5's existing table in the first review guide. A unique `job_id` is
sufficient when there is one notification row per job; separate IDs allow distinct initial and
recovery reminders for the same job. Retrying the same reminder retains its ID. This clarifies
the existing teaching design; it is not a schema implementation or evidence of exercise completion.
Reviewed the added text and checked Git whitespace. Work was performed in the Mac checkout at
`/Users/ana.rodrigues/Desktop/hooman/hs_scripts`; Pluto storage/backup status was not reverified.
Next: continue section 5's sending flow, then section 6's worker ownership and recovery checks.

**Completed November 12 receipt-handle clarification:** expanded section 3 at the first receipt-
handle mention with a 0/30/31/40-second two-worker example. The same message gets a new handle on
another receive; the previous worker's stored string is not updated or forwarded. Explained
visibility expiry, same-worker redelivery, old-handle deletion ambiguity, and visibility extensions
without new handles. Reopened AWS DeleteMessage/visibility primary documentation. This is a
source-checked example, not an SQS experiment. Next: discuss delivery identity versus job ownership
and continue the normal flow/section 6; no exercise completion is inferred.

**Completed November 12 RSA exponent question:** added the modular-algebra explanation inside
section 3's optional RSA mechanics. Correct substitution is `m ≡ m^(d*e) (mod n)`; ordinary logs
cannot discard the remainder. Verified the toy `n=55, e=3, d=7, m=7` signature/verification and
`lambda(55)=20` arithmetic in Python. Explained that modular inversion is easy once the secret-
factor-derived period is known, distinguished modulus `n` from `lambda(n)`, and avoided claiming
all RSA forgery is proven equivalent to factoring. Updated the RFC 8017 key-definition reference.
No cryptographic deployment, real keys or curriculum changes. Next: discuss the remainder/period
intuition before returning to token verification; no human mastery is inferred.

**Completed November 12 signature-verification follow-up:** expanded the authentication section
with JWT signing-input bytes, SHA-256, RS256 sign/verify flow, optional RSA mathematics and a runnable
in-memory example. Opened RFCs 7515, 7518 and 8017 and checked the exact signing-input/encoding rules.
Executed the exact guide snippet on Python 3.10.12 with cryptography 50.0.2: original token passed;
changed user, changed header and wrong public key each failed. All guide Python/JSON blocks parsed,
markup/sequence-label checks and Git whitespace checks passed. No keys or token values were printed
or stored. This demonstrates signature mechanics only, not full authentication or a security audit.
Next: explain the public/private operation and separate signature validity from claims/permissions.

**Completed November 12 issuer/JWKS follow-up:** clarified the same authentication section in
`/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/REVIEW_GUIDE.md`.
It now shows a fictional Cognito user-pool issuer URL, deployment settings, `iss` matching,
the public JWKS URL/document, `kid` selection, signature validation and key rotation. The membership
table separates issuer, user, tenant and role instead of saying “Our configured issuer.” Checked
current AWS verification/access-token documentation again. Example URLs and key values are labeled
illustrative; no actual user pool, credentials or authentication deployment was created. Next:
explain issuer versus tenant and why verification keys must come from a trusted configured source.

**November 12 diagram correction:** the reported authentication diagram contained an unescaped
semicolon in message text. Mermaid treats that as a statement separator. Replaced it with plain
wording and fixed three matching labels in the ownership diagram. Checked Mermaid's official
sequence-diagram syntax documentation and all sequence blocks for the same issue. The Markdown
Mermaid fences remain intact; no local Mermaid renderer is installed, so no browser-render claim
is made. Source: https://mermaid.js.org/syntax/sequenceDiagram.html#entity-codes-to-escape-characters.

**Completed November 12 authentication question:** expanded section 3 of
`/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/REVIEW_GUIDE.md`
with a login/token/membership diagram, first-use definitions, a bearer-header example, illustrative
claims and a tenant-membership table. The central clarification is that verified identity and
permission are separate: our API validates a provider token and checks trusted membership records
before assigning or accepting a tenant selection. Cognito is a concrete teaching choice, not an
observed Adobe implementation or a configured service. Sources and limits are recorded in the guide.

Verified a bounded set of current AWS primary pages on token verification, claims and login flow;
reviewed the example logic and checked Python/JSON syntax and Markdown navigation. No live login,
authentication service or cloud resources were created. The local checkout still resolves under
`/home/colligo/hs_scripts`; no bulk data, credentials or existing HTTP files were moved or changed.
The next step is to discuss this authentication explanation, then continue the first lesson.

**Completed November 12 HTTP follow-up:** saved and expanded the requested explanation at
`/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/http_protocol.md`.
It separates TCP connection lifetime, HTTP response completion and background-job lifetime,
then explains all six delivery patterns with diagrams and server/client Python examples.
The companion runnable server is
`/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/http_demo.py`.

All six exact documented clients passed against real loopback listeners: delayed response;
polling with observed HTTP/1.1 connection reuse; completion-triggered long polling and an
actual 20-second unfinished timeout; incremental SSE and WebSocket updates; and a later
webhook POST to a separate receiver. Syntax-tree parity and correctness lint passed.
Both owned listeners are closed. Primary documentation and scope/production limitations
are recorded in the lesson; no live frontend/deployment verification is claimed.
The first validation attempt exposed a Python 3.10/3.11 timeout-API mismatch; both examples
and checker were made Python 3.10 compatible before the successful full check.

This is a user-requested supporting topic, not a curriculum change or evidence of completed
human exercises. Prior lesson, positioning and application boundaries remain unchanged.

**Completed November 10 request:** rewrote the first review guide as a concept-first tutorial at
`/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/REVIEW_GUIDE.md`.
It starts with the whole design and one normal request, with four diagrams and concrete AWS choices.
New terms are defined at first use; request/message/database examples explain the mechanics.
Failures introduce the fixes they motivate: safe submission retries, outbox/reconciliation,
worker ownership, version-specific output selection and cancellation. SQL details are optional;
interview presentation is a separate final section.

Updated the companion exercise and project teaching rules: Hooman may learn unfamiliar concepts
before attempting a prompt; foundational guides can be longer and shorten as familiarity grows.
The overall learning sequence is unchanged. The existing GPT-5.6 worker checked current primary
sources and reviewed the final mechanics; root integrated fixes and independently spot-checked
critical documentation and the Adobe source hash. No deployment or human completion is claimed.

The accelerated plan, positioning proposal and prior cleanup remain complete. Existing staged
changes were preserved; this revision is in the working tree, with one new source-audit JSON.
Next: Hooman reads the tutorial and identifies questions or attempts the companion exercise.

## Cleanup and recovery

**Completed November 9 request:** clean up unneeded files and make the handoff durable while Hooman reads
our documents. That cleanup reduced the file count from **27 to 24**. The November 10 lesson adds
one needed source-audit JSON; it does not restore obsolete scaffolding. The current plan, first-pass
exercise/review, positioning proposal and résumé retain their paths. No completed study or profile
approval is inferred from the user's acknowledgment or reading activity.

Removed the abandoned browser launcher and duplicate research hub. Consolidated the historical
inference notes/lab/quiz/15 answers into
`/home/colligo/hs_scripts/claude/dev_research/learning/inference-baseline.md`, then removed the old
cycle/week files and empty directories. The reference answers are collapsible; the current first-
pass exercise still has a separate review guide.

Retained unique topic evidence, market descriptions, source manifests, historical validation
results and the reproduction script. The removed hub's findings already exist in the topic
summaries/learnings. Updated the charter file map, resume instructions, resource links and stale
historical next-action labels. Do not recreate the removed scaffolding during resume.

Before any removal, all four affected originals were verified byte-for-byte against Git commit
`403310d404a2ac7790df5cc2466e3cbb719aae27` in `/home/colligo/hs_scripts`:

- `/home/colligo/hs_scripts/claude/dev_research/tools/browser_session.sh`
- `/home/colligo/hs_scripts/claude/dev_research/research/SUMMARY.md`
- `/home/colligo/hs_scripts/claude/dev_research/learning/cycle-1/week-01/STUDY_GUIDE.md`
- `/home/colligo/hs_scripts/claude/dev_research/learning/cycle-1/week-01/QUIZ_ANSWERS.md`

These originals are recoverable from that commit. For example, inspect the removed launcher with:

```bash
git -C /home/colligo/hs_scripts show 403310d404a2ac7790df5cc2466e3cbb719aae27:claude/dev_research/tools/browser_session.sh
```

If extraction is necessary, write to a new path without overwriting current work. Keep historical
manifest paths/hashes unchanged: they describe what was originally read, not today's folder layout.
No repository move, remote push, browser launch, profile change or application was part of cleanup.

## Confirmed current direction

- Target an **accepted offer** in about two months, around January 9, 2027. No current recruiter
  conversations or interviews. Hooman will request application help after the plan and LinkedIn
  are ready. An offer is the goal, not a guaranteed plan outcome.
- Cover essential interview breadth in the first month; use the second for deeper drills and
  actual interview formats. Increased effort replaces the former 5–6-hour cap; sequence matters
  more than a rigid timetable.
- Start with **system design and ML/inference fundamentals**, then timed coding. Explaining
  experience is not the main weakness. No actual completed-work inventory or unaided scores supplied.
- Target **Senior IC and Staff/Principal AI infrastructure/inference**. Exclude engineering-manager
  roles. Use one core curriculum with deeper scope/follow-ups for Staff/Principal.
- Hooman lives in **San Jose, California**, remains employed at **Adobe — Machine Learning Engineer,
  ASML**, October 2023–Present, and says **no sponsorship needed for applying**. Do not infer an
  immigration category or answer differently scoped future-sponsorship questions from this alone.
- Hooman supplied https://www.linkedin.com/in/hoomanshariati/ and is unsure whether an export
  exists. No export was found under this project. Public-disclosure and job-visibility preferences
  were not selected; conservative copy and recruiter-only visibility are researcher proposals.
- Use `gpt-5.6-sol` at `xhigh` for bounded execution; keep planning, ambiguity resolution,
  integration and review with the primary agent. Two workers successfully completed evidence tasks.

## Canonical deliverables

- `/home/colligo/hs_scripts/claude/dev_research/learning/LEARNING_PLAN.md` — current seven-stage
  first pass, second-month drill method, assessment gates, IC-level differences, reused resources,
  explicit deferrals and execution/review contract.
- `/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/STUDY_GUIDE.md` — first system-
  design practice prompt to attempt after learning unfamiliar concepts; no prior platform setup required.
- `/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/REVIEW_GUIDE.md` — separate
  expanded concept-first tutorial with five diagrams, first-use definitions, concrete AWS examples,
  optional SQL and separate interview rehearsal. Read before attempting when the material is new.
- `/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/http_protocol.md` — requested
  HTTP tutorial, connection-lifetime corrections and six tested server/client examples; companion
  `/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/http_demo.py` runs locally.
- `/home/colligo/hs_scripts/claude/dev_research/learning/inference-baseline.md` — consolidated
  historical serving notes, baseline lab and quiz/answers; optional reference, not the next task.
- `/home/colligo/hs_scripts/claude/dev_research/positioning/POSITIONING.md` — concrete LinkedIn
  headline/About/Adobe bullets, San Jose corrections, GitHub/Skills/Featured/résumé updates, future
  application workflow, source ledger, public/live-access limits and external execution boundary.
- `/home/colligo/hs_scripts/claude/dev_research/positioning/HOOMAN_SHARIATI_RESUME.md` — retained
  canonical résumé with two corrected facts/wordings: CVPR Workshops and over a decade. Existing
  named customers/metrics remain; do not upload publicly without reviewing that disclosure boundary.
- `/home/colligo/hs_scripts/claude/dev_research/career/CAREER_EVIDENCE.md` — source-labeled career
  record, updated current facts and independently checked publication bibliography.
- `/home/colligo/hs_scripts/claude/dev_research/research/plan-comparison/SUMMARY.md` — completed
  October friend-plan comparison, preserved as historical evidence with superseded schedule marked.

## Batches completed and findings

1. **Resume/storage preflight:** read the full current research playbook, memory index/relevant
   preferences, charter, state, decisions, learnings, roadmap and relevant topic material. Git root
   and realpath both resolve to `/home/colligo/hs_scripts`, within the user-designated durable home.
   The environment reports an overlay mount; no independent backup-service verification is claimed.
2. **Five diagnostics:** asked and received all five replies. The final reply supplied the existing
   public profile URL; full export and disclosure settings remain open without blocking a general draft.
3. **Curriculum evidence audit:** GPT-5.6 read the old plan, comparison, market summary, Week 1,
   attention and LoRA notes. Strong reusable reference material exists; it does not prove human
   completion. Diffusion LoRA examples do not substitute for an LLM SFT exercise. Integrated by root.
4. **Positioning audit:** GPT-5.6 inspected career evidence and public LinkedIn/GitHub/CVF sources.
   Root independently fetched the decision-driving location and publication sources. LinkedIn shows
   Vancouver; GitHub shows Canada. The paper is CVPR Workshops 2019, pages 26–32, Hooman first in the
   listed author order. Full account/profile fields remain gated. Root integrated and corrected copy.
5. **New plan:** root wrote the shared IC sequence and reconciled charter, method, decisions,
   learnings and roadmap. Profile readiness overlaps learning; application work remains inactive
   until requested. Broad platform/kernel projects are not first-month prerequisites.
6. **First packet:** GPT-5.6 generated the bounded stage-1 exercise and separate review, opened
   PostgreSQL/Kubernetes/AWS primary references and inspected one current Adobe endpoint source.
   Root independently opened the cited public sources, verified the current Adobe source hash,
   and clarified cancellation linearization and mandatory lease-recovery/acknowledgement semantics.
   The packet is reviewed; no code execution or human exercise completion is claimed.

7. **November 10 teaching revision:** root replaced the compressed answer sheet with one practical
   video-job tutorial and aligned the exercise, charter, resume rules, curriculum and roadmap.
   GPT-5.6 verified primary SQS/PostgreSQL/S3/DynamoDB documentation and the current Adobe endpoint;
   root fixed the review findings and the final independent consistency check passed. JSON examples,
   Python snippet syntax, Markdown fences/contents anchors and capacity arithmetic were checked;
   Git whitespace validation passed. Diagrams were reviewed as source, not browser-rendered.
   The SQS baseline now deletes after a terminal database outcome; early deletion is a separate
   alternative. Output reads pin the selected S3 version, and lease checks occur under brief row
   locks using current database time. No cloud service was deployed or exercised.

## Source availability and environment

**Missing at the old volatile paths as of November 9:**

- `/mnt/localssd/2026-b-share.zip`
- `/mnt/localssd/dev_research_inputs/friend-plan-2026-10-14/`
- `/mnt/localssd/hs_aupera_resume.pdf`
- `/mnt/localssd/adobe_checkins/`
- `/mnt/localssd/x_bookmarks_2026-09-15/bookmarks.json`
- `/mnt/localssd/dev_research_browser/profile`

The friend archive was read in full on October 14: 47 files, 231,063 uncompressed bytes, SHA-256
`72f7b97500cd3406ddaafb1106573fec547e8bee4b578095c0aedd9cf060e962`.
Durable summary, source manifest and historical checks survive under
`/home/colligo/hs_scripts/claude/dev_research/research/plan-comparison/`.
Those records are not a restored raw archive. No new raw-source reading or validator run is claimed.
A bounded filename search under `/sensei-fs/users/hshariati/claude_backup` found no matching source
archive/check-in/export files. If recovered, copy non-destructively into durable project storage,
verify size/hash manifests, and record source/backup/restore paths before relying on the copy.

`/home/colligo/colligo` now exists, superseding the October access failure. Current source/code
findings still require actual inspection. The first packet records the one inspected file/revision.
Remote Chromium/noVNC was previously stopped at Hooman's request; it was not restarted. Public
LinkedIn access is not authenticated access. Use the working laptop for a current full-field read.

Codex HTTP and stream retries in `/home/colligo/.codex/config.toml` remain **100**. Current local
model setting is `gpt-6-astra` with `high` effort, changed since October's snapshot. Applicability to
hosted-session retry behavior remains unverified; no settings were changed and rate limits are not
claimed fixed. Official agent configuration documentation was fetched November 9; model availability
was also observed by successful worker completion.

## Historical completed work and parked backlog

- September 15: all 327 X bookmarks reviewed for discovery, and 60 employer postings from 20
  companies collected, balanced 30 inference/platform and 30 customer/FDE. These are historical
  snapshots, not current active vacancies or interview frequencies. Required/preferred normalization
  remains incomplete; it must not delay the accelerated learning path.
- October 4–5: original private inference-platform plan and Week 1/attention/LoRA resources created.
  Prior permission allowed Adobe/Pluto and assumed two H200 GPUs. No current allocation or completed
  baseline is established. Verify compute before a lab; use a trace exercise if unavailable.
- October 7: general Staff/Principal résumé created using confirmed Adobe title/start date.
- October 14: complete friend-plan comparison; three Python examples passed historical bounded
  checks. Correctness caveats include Redis score precision, worker ownership and reconciliation.
- Parked: broad market re-collection, new management curriculum, broad kernel/compiler study,
  multi-node platform builds, full customer applications and mandatory public portfolio production.

## Remaining gaps

- Independently observed design/coding/domain performance and completed lab artifacts.
- Full current LinkedIn fields and private settings for an exact merged edit.
- Public-disclosure choices, current role work-location field, and approved metrics/customer names.
- Actual live role preferences: compensation floor, work arrangement, target companies and round
  formats. Collect when application work is requested; do not silently reuse old salary assumptions.
- Any future sponsorship wording broader than the already answered application-purpose statement.

## Next exact step

Continue section 6's claim and takeover example: a `RUNNING` row with an expired lease is eligible
for a new attempt, which increments `attempt_no`. Follow the guarded-completion update to see why
the expired attempt cannot publish. The new collapsible two-timer Q&A and section 5's outbox-ID
note are available for review. No first-exercise completion is established; retain the earlier
follow-up paths below as needed.

Read section 3's “Why can a receipt handle become old?” and follow message M through deliveries R1
and R2. A later receive creates the new handle; visibility renewal does not. Then connect that
transport behavior to section 6's separate database ownership checks.

Read section 3, including issuer/JWKS and signature verification, in the first review guide. The
optional RSA detail and runnable snippet answer the latest question. Trace login →
verified access token → active membership/permission → tenant-scoped job. Discuss any unclear step
before adding authentication implementation work; no such deployment or human completion is assumed.

For the supporting HTTP topic, read sections 6–8 of the supporting HTTP tutorial and use the
companion local demo if desired. All six implementations are complete; do not infer human
completion, repeat paid generations, or start remote/browser infrastructure.

Hooman should read sections 1–3 of the expanded tutorial for the big picture and normal flow,
then sections 4–8 for the failure cases. Discuss unclear concepts before compressing this into an
interview answer. When ready, attempt the companion exercise and record unaided explanations and
remaining gaps. Do not generate the next lesson or infer completion just because this guide exists.

Follow the new teaching preferences in the charter for future lessons. Current recommendation:
continue to the bounded ML/inference fundamentals stage after this representative design attempt;
there is no requirement to memorize every implementation detail or build the service first.

The existing LinkedIn proposal and future application workflow remain unchanged; no live edits or
applications have been authorized by this lesson request. Previous cleanup originals and source
availability details are recorded above.
