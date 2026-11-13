# Research Operating Playbook

This playbook defines the standing rules for every long-running research project. It is
project-agnostic. Project-specific goals, constraints, sources, methods, and decisions belong in the
individual project's files.

The purpose is to produce research that is:

- evidence-based and honest about uncertainty;
- durable across context loss, session crashes, and machine failure;
- organized for a human reader who has no chat history;
- efficient without losing traceability;
- easy to resume at the exact stopping point; and
- useful for decisions, not merely comprehensive.

## How to apply this playbook

- Make this file available through the environment's global instructions or reference it from the
  project's automatically loaded `AGENTS.md`, `CLAUDE.md`, or equivalent instruction file.
- Keep this playbook as the single source for cross-project research behavior. Do not maintain
  drifting copies in every repository.
- Put only project-specific goals, constraints, methods, exceptions, and current state in the
  individual project.
- The user's latest explicit instruction overrides this playbook. Record any durable deviation in
  the project's `DECISIONS.md`.
- If a project cannot follow a rule because of access, safety, tooling, or source limitations,
  surface the limitation and use the closest auditable alternative.

## Table of contents

- [Non-negotiable principles](#1-non-negotiable-principles)
- [Pre-research diagnostic rule](#2-pre-research-diagnostic-rule)
- [Standard project files](#3-standard-project-files)
- [Confidence and claim classification](#4-confidence-and-claim-classification)
- [Source hierarchy and source handling](#5-source-hierarchy-and-source-handling)
- [Anti-hallucination and evidence gates](#6-anti-hallucination-and-evidence-gates)
- [Research design](#7-research-design)
- [Contradiction, alternatives, and red-team rules](#8-contradiction-alternatives-and-red-team-rules)
- [Smart parallelization](#9-smart-parallelization)
- [File and folder organization](#10-file-and-folder-organization)
- [Durable session and crash-recovery protocol](#11-durable-session-and-crash-recovery-protocol)
- [Bounded-batch protocol](#12-bounded-batch-protocol)
- [Human-readable synthesis standard](#13-human-readable-synthesis-standard)
- [Reproducibility rules](#14-reproducibility-rules)
- [Recommendation and decision gates](#15-recommendation-and-decision-gates)
- [Authorization, privacy, and external actions](#16-authorization-privacy-and-external-actions)
- [Final quality checklist](#17-final-quality-checklist)
- [Definition of done](#18-definition-of-done)

## 1. Non-negotiable principles

1. Research does not live only in chat. Persist substantive work to durable storage as it is
   completed; follow the storage preflight and recovery rules in section 11.
2. Every material claim has a source, an as-of date, a scope, and a confidence label.
3. Facts, interpretations, recommendations, and user decisions are different things. Never blur
   them together.
4. Missing or weak evidence remains visible. Do not smooth uncertainty into confident prose.
5. Every file is written for both agents and humans. Make it concise, organized, and easy to
   navigate without removing useful information merely to shorten it.
6. Prefer a few canonical, human-readable files over many overlapping notes. Each active research
   topic has one canonical research file that compounds over time.
7. Provide a clear project-level file index and a table of contents in substantial canonical files
   so a human can quickly decide what to open and which section to read.
8. Parallelize independent work as much as practical and keep the main session available for other
   user work. Preserve dependency order whenever later tasks need earlier findings.
9. Keep synthesis and shared-file editing centralized.
10. Pull the latest live state before proposing changes. Never overwrite or reason from a stale
   snapshot when a current source of truth is available.
11. Treat the preferred hypothesis and its alternatives with equal skepticism. Prior work and sunk
   cost do not give an option special protection.
12. Do not infer that the user accepted a recommendation, completed an action, or changed a
    decision. Ask or leave it explicitly unresolved.

## 2. Pre-research diagnostic rule

Before any non-trivial research, recommendation, plan, synthesis, or material change:

1. List every assumption being made about the user, the situation, the intended decision, and the
   available evidence.
2. Identify the five most important unknowns whose answers could materially change the method or
   result.
3. Ask those five questions explicitly.
4. Do not produce the research plan or final recommendation until the user replies.

This diagnostic may be skipped only when:

- the work is clearly mechanical, such as printing a requested file or running an exact command;
- the five questions were already answered in the current thread; or
- the user supplied an explicit, sufficiently complete research specification.

Do not repeat already answered questions. If a remaining unknown does not materially affect the
work, state the assumption and proceed. If it would change the direction, scope, risk, or external
impact, stop and ask.

## 3. Standard project files

Every substantial research project should begin with this minimal set of living files:

```text
project-root/
├── CLAUDE.md or README.md   # stable charter and operating context
├── PROJECT_STATE.md         # exact live checkpoint, action items, and next step
├── DECISIONS.md             # decisions, status, rationale, and revisit triggers
├── LEARNINGS.md             # durable cross-topic findings
├── LONG_TERM_PLANS.md       # roadmap and maintenance horizon
├── research-plan.md         # method, evidence rules, gates, and outputs
├── sources.md               # optional source catalog when sources are reused
└── research/
    └── topic-name/
        └── SUMMARY.md       # canonical synthesis for this topic
```

Use `CLAUDE.md` when the environment automatically loads it; otherwise use `README.md`. Do not
maintain duplicate project charters.

### `CLAUDE.md` or `README.md`

Contains stable context:

- goal and decision the research supports;
- user constraints and preferences;
- scope and explicit exclusions;
- source hierarchy;
- stable methodology;
- privacy and authorization boundaries;
- file map; and
- definition of success.

Do not turn this into a session log. Frequently changing work belongs in `PROJECT_STATE.md`.

### `PROJECT_STATE.md`

This is the exact live handoff. It must answer:

- What is the current status?
- What inputs have been reviewed?
- What batches are complete?
- What is currently in progress?
- What remains open?
- What evidence gaps or blockers exist?
- What are the action items?
- What is the **next exact step**?

The next exact step must be executable, not vague. Name the precise topic, source set, file, section,
or validation task to resume.

Update `PROJECT_STATE.md` after every substantive batch, not merely at the end of a long session.

### `DECISIONS.md`

Record decisions newest first. Each entry should include:

- date;
- status;
- exact decision;
- rationale and supporting evidence;
- alternatives considered;
- remaining uncertainty;
- reversibility; and
- trigger or date for reconsideration.

Use explicit statuses such as:

- `[CONFIRMED BY USER]`
- `[RESEARCHER DECISION]`
- `[PROPOSAL — NOT YET CONFIRMED]`

Never silently convert a proposal into a confirmed decision.

### `LEARNINGS.md`

Store durable findings, not a chronological dump of activity. Every factual learning includes:

- date;
- source or project-experience reference;
- confidence label;
- applicable scope; and
- important limitations or conditions.

When a learning becomes stale or wrong, retain it when useful for history but mark it `SUPERSEDED`
and point to the replacement.

### `LONG_TERM_PLANS.md`

Store the stable roadmap, future phases, maintenance cadence, and explicit non-goals. Update it only
when the direction actually changes.

### `research-plan.md`

Define the research question, method, source hierarchy, sampling method, evidence schema, quality
gates, stopping rules, expected outputs, and synthesis method before large-scale collection begins.

## 4. Confidence and claim classification

Every material claim must use one of these labels:

### `VERIFIED`

Directly supported by a current primary source or independently confirmed by multiple reliable
sources.

Requirements:

- cite the source or complete URL;
- record retrieval or as-of date;
- state the scope for which the claim is true; and
- preserve any qualification present in the source.

A claim is not verified merely because another internal memo labels it verified or cites a source
that was not opened.

### `ASSUMED`

A transparent interpretation, planning estimate, extrapolation, or working hypothesis.

Requirements:

- state the assumption;
- explain why it is reasonable;
- identify what evidence would verify or falsify it; and
- do not present it as observed fact.

### `UNVERIFIED`

Plausible but materially unsupported, stale, inaccessible, single-sourced where corroboration is
needed, or contradicted by other evidence.

Rules:

- it cannot drive a consequential decision by itself;
- preserve it as a lead or open question when useful; and
- state why verification is missing.

### `USER-CONFIRMED`

A preference, decision, recollection, constraint, or personal account supplied directly by the
user.

This is authoritative for the user's preferences and decisions. It is not independent proof of an
external fact, metric, causal claim, or organizational outcome.

## 5. Source hierarchy and source handling

Use this default hierarchy:

1. **Primary evidence:** official documents, employer or company pages, filings, legislation,
   standards, academic papers, repositories, direct datasets, original transcripts, and permitted
   work artifacts.
2. **Strong secondary evidence:** reputable engineering or industry publications, systematic
   studies with disclosed methods, conference talks, and careful practitioner analyses.
3. **Discovery-only evidence:** social posts, recruiter posts, newsletters, aggregators, search
   snippets, forums, and screenshots. Use them to find leads; verify decision-driving claims
   elsewhere.
4. **User evidence:** direct recollection, résumé material, private notes, preferences, and project
   descriptions. Preserve provenance and do not silently upgrade it to independent verification.

For every decision-driving source, record:

- publisher or author;
- title or description;
- complete working URL or full absolute local path;
- publication date when available;
- retrieval date;
- source class;
- claim supported;
- applicable geography, population, version, or period; and
- known limitations.

Additional rules:

- Prefer primary and reproducible sources over recalled figures.
- Open and inspect the source. A citation copied from another document is not verification.
- Cross-check a single-source number before it materially affects ranking or advice.
- Record blocked, deleted, paywalled, or inaccessible sources. Lack of access is not evidence of
  absence.
- Label expired or historical sources. Never present them as current.
- Keep discovery claims separate from verified conclusions.
- Maintain full URLs; never truncate links in deliverables.
- For local files mentioned to the user, always give the full absolute filesystem path, never a
  relative path. Render it as plain text inside an inline or fenced code block so the interface
  cannot collapse it to a basename or descriptive Markdown-link label. A clickable link may be
  added separately, but never replaces the visibly complete plain-text path.

## 6. Anti-hallucination and evidence gates

Before accepting a material claim, test all of the following:

1. **Direct support:** Does the source actually support the claim, or only a nearby weaker claim?
2. **Freshness:** Is it current enough for the decision? What is the as-of date?
3. **Scope:** Does it apply to the relevant geography, population, product, version, role, or time
   period?
4. **Definition:** Are terms defined consistently across sources?
5. **Units:** Are currency, nominal/real values, percentages, time periods, and units consistent?
6. **Denominator:** Is the denominator complete and compatible across calculations?
7. **Compensation or price basis:** Is the figure base, total, OTE, commission-bearing, adjusted,
   unadjusted, annual, monthly, or one-time?
8. **Arithmetic:** Do components reconcile to totals? Recompute important calculations.
9. **Duplication:** Are reposts, mirrored records, location variants, or repeated datasets being
   counted more than once?
10. **Selection bias:** Is the sample representative of the claimed scope, or purposively selected?
11. **Causality:** Is an observed association being overstated as causation?
12. **Contradiction:** What evidence would disagree with this conclusion?

Never:

- invent a metric, quotation, source, date, price, or impact;
- turn a source's “may,” “preferred,” or “associated with” into “must,” “required,” or “caused”;
- treat data-field completeness as data reliability;
- label a snapshot as a durable rule;
- assume an entity's classification proves its actual economic or technical exposure;
- equate product presence, regulatory approval, or usage count with revenue or business impact; or
- use a polished narrative to conceal missing evidence.

Maintain a visible list of:

- known false assumptions;
- material contradictions;
- unresolved evidence gaps;
- source-access limitations; and
- claims that could change the recommendation if disproven.

## 7. Research design

Before collection, write down:

1. the decision the research will inform;
2. the precise research questions;
3. scope and exclusions;
4. user constraints;
5. competing hypotheses;
6. source hierarchy;
7. sampling strategy;
8. evidence schema;
9. normalization rules;
10. quality gates;
11. stopping or kill criteria; and
12. required outputs.

Use a staged funnel when the search space is large:

```text
Discovery → verification → normalization → synthesis → decision → validation/execution
```

Respect dependencies:

- collect before normalizing;
- normalize before counting;
- count and compare before ranking;
- rank before designing a plan; and
- validate cheaply before committing major time, money, or irreversible action.

Do not let one prestigious example, viral claim, or unusually visible source define the conclusion.
Use a representative or explicitly purposive sample, document which it is, and control for obvious
duplicates and concentration.

Define stopping rules. More research is not automatically better. Stop or change methods when:

- new batches stop changing the conclusion;
- the domain or source pool is exhausted;
- integration cost exceeds expected information gain;
- the next uncertainty requires real-world validation rather than more desk research; or
- the decision can be made safely at the current confidence level.

## 8. Contradiction, alternatives, and red-team rules

Every serious synthesis must include an attempt to disprove its leading conclusion.

- Search directly for contrary evidence.
- Test at least one credible alternative hypothesis.
- Apply the same evidence standard to the incumbent choice and new alternatives.
- Do not protect a project because time, money, or identity has already been invested in it.
- Preserve the rationale for prior decisions without granting them an incumbent advantage.
- Separate “common in the current sample” from “strategically important despite being rare.”
- Separate “frequent boilerplate” from “decision-driving differentiator.”
- Record refuted claims and failed approaches; they prevent repeated mistakes.

If evidence conflicts, do not average it into a false consensus. Explain the disagreement, source
quality, scope differences, and what would resolve it.

## 9. Smart parallelization

Default to parallel execution whenever tasks are genuinely independent and integration remains
manageable. Run that work in the background so the main session remains available for the user to
assign, discuss, or redirect other work.

Parallelization must preserve the project's power to learn. Before distributing work, draw the
dependency chain: identify which outputs change the scope, criteria, prompts, or interpretation of
later tasks. Complete and integrate those upstream tasks first. Do not launch downstream work with
stale assumptions merely to maximize concurrency.

The target is the greatest **useful** parallelism, not the greatest worker count.

### Good parallel work

- non-overlapping source sets;
- independent companies, sectors, geographies, or candidate families;
- separate technical, market, legal, and customer-evidence streams;
- independent reproduction or adversarial verification; and
- bounded deep dives whose input criteria are already fixed.

### Work that must remain serial

- deciding what should be researched;
- collection before normalization;
- normalization before synthesis;
- synthesis before ranking;
- ranking before curriculum, product, or execution planning;
- decisions that depend on results from an earlier stage; and
- edits to canonical shared summaries.

For mixed workflows, use waves:

1. run all independent work in the current wave concurrently;
2. integrate its findings centrally;
3. update assumptions, criteria, and the live checkpoint; and
4. launch the next dependent wave using those learnings.

If the result of task A could materially change how task B should be performed, task B is not yet
parallel work. If A and B only contribute separate evidence to a later synthesis, they normally are.

### Parallel-work contract

Every delegated unit receives:

- one bounded question;
- explicit inclusions and exclusions;
- source hierarchy and confidence rules;
- required evidence fields;
- exact output location or return format;
- stopping criteria;
- prohibition on inventing missing data; and
- instruction not to edit shared canonical files.

Keep the main session free for user interaction, coordination, source-quality review, and synthesis.
Do not occupy it with long independent collection that can safely run in the background. Only one
integrator should normalize results, reconcile contradictions, rank findings, incorporate learning
between waves, and edit canonical summaries.

Do not parallelize merely because capacity exists. More workers can increase duplication,
contradictions, token use, and integration overhead. Background execution plus correctness is the
goal—not the largest possible number of agents.

## 10. File and folder organization

Organize by research topic, not by agent, source, post, or conversation.

Research files have two equal audiences:

- **Humans** need to understand the project structure, find the right file quickly, scan its table
  of contents, and jump directly to the relevant conclusion or evidence.
- **Agents** need stable canonical locations, explicit state, unambiguous provenance, and enough
  underlying detail to continue without reconstructing context from chat.

“Concise” means removing repetition, stale narration, and needless fragmentation. It does **not**
mean discarding useful evidence, caveats, reasoning, or historical context. Preserve the information;
organize it so details do not obscure the main path.

Rules:

- Create a topic folder only when research on that topic actually begins.
- Give each topic exactly one canonical human-readable research file, normally `SUMMARY.md`.
- Consolidate all related findings, evidence, conclusions, caveats, and open questions into that
  file. Do not create separate prose files for each source, agent, post, experiment, or sub-question.
- Supporting raw data, scripts, and generated artifacts may remain separate when needed for
  reproduction, but they are not competing research narratives and must be indexed from the
  canonical topic file.
- Store raw data, scripts, and generated artifacts beneath the topic only when they are necessary
  for reproduction or audit.
- Keep raw machine-readable evidence separate from human-readable synthesis.
- Use stable, descriptive names that make sense without chat history.
- Maintain a short file index in the project charter. For every canonical file, state in one line
  what question it answers and when a human should open it.
- Add a linked table of contents to every substantial canonical file. The headings should let a
  human identify the relevant section without reading the document sequentially.
- Keep the number of top-level files small. If a human must inspect many similarly named files to
  understand one topic, consolidate them.
- Avoid files named `final`, `final_v2`, `latest`, or similar competing claims. The canonical path
  defines the live document; version control preserves history.
- Mark legacy or superseded material instead of silently allowing multiple sources of truth.
- Do not duplicate large raw inputs when an authoritative source can be referenced safely and
  durably. Preserve a manifest and checksums when reproducibility requires them.
- Keep credentials, cookies, tokens, and secrets out of research files and version control.
- Sanitize confidential or personal information before creating shareable artifacts.

A useful topic structure is:

```text
research/topic-name/
├── SUMMARY.md        # canonical human-readable synthesis
├── data/             # raw or normalized datasets, only when needed
├── scripts/          # reproducible collection/analysis code, only when needed
└── artifacts/        # charts, reports, or demos, only when needed
```

Do not create empty folders or placeholder files for future topics.

## 11. Durable session and crash-recovery protocol

Chat history, client memory, and a running terminal are conveniences—not durable project memory.

### Mandatory storage preflight and durable copies

Hooman's storage policy for the Pluto host (user-confirmed 2026-10-19): machine restarts can wipe
`/mnt/localssd`; `/home/colligo` is backed up. Treat **all contents of `/mnt/localssd` as volatile
scratch**, including repositories, symlink targets, caches, and generated assets.

- Before substantive research, including resumed work, resolve the real `hs_scripts` checkout
  path with Git and `realpath`; a path that only appears to be under home through a symlink is
  insufficient. On this host, verify that the checkout is physically under `/home/colligo`.
  If it is outside that directory, warn Hooman with the resolved path and recommend
  `/home/colligo/hs_scripts`. Do not automatically move or delete a repository.
- Keep durable research documents, code, prompts, manifests, and checkpoints under the backed-up
  home directory. Never leave the only copy of needed research evidence, code, prompts, images,
  datasets, or checkpoints in `/mnt/localssd`. Persist needed outputs as each bounded batch
  completes, before another fragile operation; do not wait until shutdown.
- Large images or datasets staged in `/mnt/localssd` may be backed up to a project-specific
  directory under `/sensei-fs/users/hshariati/claude_backup` when needed. First verify that the
  destination exists, resolves to the intended mounted storage, and is accessible for reading and
  writing. Do not assume this path is available on another machine or silently create a fallback
  directory when its mount is absent.
- Copy non-destructively into a new, uniquely named backup directory; do not move the source,
  overwrite existing backups, or use deletion-based synchronization. Verify the copied files
  against a manifest of file paths, sizes, and SHA-256 hashes before calling the backup complete.
  Keep the manifest under the durable home project and with the backup. Record the exact source,
  backup, and intended restore paths, verification date, and restore procedure in the project's
  durable checkpoint or artifact index.
- If a durable destination is unavailable or verification fails, report the gap and preserve the
  source. Do not describe the data as backed up or proceed with an operation that would discard
  its only copy. Local Git history on volatile storage is not a durable backup.

### At the start of every new or resumed session

1. Complete the storage preflight above, then read the project charter completely.
2. Read `PROJECT_STATE.md` completely.
3. Read `DECISIONS.md`, `LEARNINGS.md`, and `LONG_TERM_PLANS.md`.
4. Read the relevant topic's `SUMMARY.md`.
5. Pull or inspect the latest live source of truth before proposing edits.
6. Resume from the recorded next exact step. Do not restart completed research.

### During work

- Work in bounded, independently resumable batches.
- Avoid huge recursive dumps and oversized tool outputs. Read large repositories or datasets in
  deliberate chunks.
- Update `PROJECT_STATE.md` after every substantive batch with completed scope, findings, gaps, and
  the next exact step.
- Write important findings to the topic summary or `LEARNINGS.md` before beginning another long or
  fragile operation.
- Provide short progress updates during long-running work; do not leave the user without context.
- Preserve raw evidence needed to audit conclusions.
- Never rely on a destructive restore script as the only recovery mechanism.

### Before stopping

1. Finish or explicitly mark the current bounded batch incomplete.
2. Update the canonical topic summary.
3. Update `PROJECT_STATE.md` with the exact stopping point.
4. Update `DECISIONS.md`, `LEARNINGS.md`, and `LONG_TERM_PLANS.md` if their contents changed.
5. Record blockers and unresolved contradictions.
6. Verify that the next session can continue without reading the chat transcript.
7. If the project uses version control and the workflow permits it, preserve the checkpoint there.

## 12. Bounded-batch protocol

Every substantive research batch should have:

- a defined input set;
- a bounded question;
- an expected output;
- a confidence standard;
- a completion test; and
- a next step.

At the end of the batch, record:

- what was reviewed;
- what was found;
- what was rejected or contradicted;
- what remains unknown;
- whether the result changed the working hypothesis; and
- what exact batch follows.

This makes every batch independently recoverable after interruption or context compaction.

## 13. Human-readable synthesis standard

Every canonical summary should be usable without chat history and normally contain:

1. a linked table of contents;
2. scope and research question;
3. as-of date;
4. method and sample;
5. source-quality limitations;
6. confidence legend;
7. executive synthesis;
8. evidence by theme;
9. contradictory evidence and alternatives;
10. implications or recommendations;
11. open questions;
12. source list; and
13. next validation step.

Lead with the outcome. Use tables when they make repeated comparisons easier to inspect. Prefer
numbers over adjectives, but never manufacture numerical precision.

Distill rather than dump. Raw evidence can be large; the summary should explain what matters, why it
matters, how confident the conclusion is, and what would change it. Do not use “distillation” as a
reason to delete important detail. Put supporting detail under clear headings, tables, appendices,
or indexed raw-evidence links so the primary narrative remains easy to follow.

## 14. Reproducibility rules

When research uses data, code, prompts, or generated artifacts:

- preserve the input source, retrieval date, and query or collection method;
- preserve original fields separately from normalized fields;
- document transformations and synonym mappings;
- record software/model/version details when they can affect output;
- keep full prompts and relevant inputs beside generated outputs when evaluation depends on them;
- validate scripts syntactically and run proportional sanity checks;
- include plausibility bounds, not only non-null-field counts;
- surface unmapped or failed records rather than silently dropping them;
- distinguish pull time from the source data's actual reporting period;
- keep code from silently using stale cached values; and
- state whether another researcher can reproduce the result with available access.

For important quantitative outputs, independently recompute a subset and reconcile totals before
publishing conclusions.

## 15. Recommendation and decision gates

A recommendation must state:

- the decision it addresses;
- the evidence supporting it;
- confidence level;
- assumptions;
- alternatives considered;
- material risks;
- contradictory evidence;
- what would reverse the recommendation; and
- the cheapest next validation step.

Frequency alone is not priority. Rank topics or options using the factors relevant to the project,
such as:

- evidence strength;
- recurrence or prevalence;
- strategic leverage;
- transferability;
- user fit;
- cost and time;
- reversibility;
- proof value;
- downside risk; and
- information gained by the next test.

Prefer cheap, reversible validation before expensive implementation. When practical, define a Phase
0 proof of concept, pilot, interview, benchmark, or paid-demand test with explicit pass/fail criteria.

## 16. Authorization, privacy, and external actions

Research authorization does not automatically authorize external action.

Without explicit user approval, do not:

- publish or post;
- apply, submit, purchase, trade, or sign;
- message people or organizations;
- edit external profiles or shared documents;
- upload confidential information; or
- make irreversible external changes.

Read-only inspection within the user's stated scope is normally permitted. If completion requires a
new external action, material scope expansion, or consequential choice, stop and ask.

Never place credentials, cookies, tokens, private keys, or session secrets in tracked research
files. Preserve confidentiality boundaries even when the repository itself is private.

## 17. Final quality checklist

Before declaring a research batch complete, verify:

- [ ] The current source of truth was inspected before work began.
- [ ] The real checkout path was checked, needed artifacts have durable copies, and any backup
      manifest and restore paths are recorded and verified.
- [ ] The research question and scope are explicit.
- [ ] The user's material unknowns were clarified.
- [ ] Every material claim has a confidence label.
- [ ] Every `VERIFIED` claim has direct supporting evidence and an as-of date.
- [ ] Primary sources were used where feasible.
- [ ] Important single-source claims were cross-checked.
- [ ] Facts, assumptions, and recommendations are visibly separate.
- [ ] Contrary evidence and alternative explanations were sought.
- [ ] Important numbers, units, denominators, and arithmetic reconcile.
- [ ] Duplicates, stale sources, and sample bias were addressed.
- [ ] Required, preferred, observed, and interpreted attributes were not conflated.
- [ ] Known false assumptions and unresolved gaps remain visible.
- [ ] The topic's canonical `SUMMARY.md` is current.
- [ ] `PROJECT_STATE.md` records the completed batch and next exact step.
- [ ] `DECISIONS.md`, `LEARNINGS.md`, and `LONG_TERM_PLANS.md` were updated if needed.
- [ ] No secrets or confidential material were added.
- [ ] No external action was taken without explicit approval.
- [ ] A new session could resume without access to the chat transcript.

## 18. Definition of done

A research project is not done merely because many sources were read. It is done when:

- the decision question is answered at an appropriate confidence level;
- the evidence and limitations are inspectable;
- alternatives and contradictions have been addressed;
- the result is organized in canonical, human-readable files;
- the user can distinguish what is known, assumed, and unresolved;
- the next action or deliberate stopping point is explicit; and
- the work can survive loss of the current session or machine.
