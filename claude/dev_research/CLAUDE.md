# Career Readiness — Project State & Operating Manual

**This is the stable source of truth for the project.** `PROJECT_STATE.md` contains the
live stopping point and current work.

Owner: Hooman Shariati. Created: 2026-09-15.

## Contents

- [1. Goal](#1-goal)
- [2. Target profile](#2-target-profile)
- [3. Known career thesis](#3-known-career-thesis)
- [4. Source hierarchy](#4-source-hierarchy)
- [5. Working rules](#5-working-rules)
- [6. File organization](#6-file-organization)
- [7. Definition of success](#7-definition-of-success)

## 1. Goal

Prepare Hooman for an accepted offer within approximately two months from November 9, 2026.
Cover essential interview breadth in the first month and deepen assessed gaps and company-specific
requirements in the second. The user has increased study effort; the previous 5–6-hour cap and
non-urgent readiness framing are superseded. Give an efficient sequence, not a rigid timetable.

The current outputs are one shared Senior/Staff/Principal IC curriculum; focused study packets and
performance evidence; an accurate career inventory; ready-to-paste LinkedIn and related-material
updates; and an application workflow to activate when Hooman requests it. An offer is the target,
not an outcome the curriculum can guarantee. Do not infer that an organizational cut has occurred.

## 2. Target profile

### Primary target

Senior IC and Staff/Principal AI infrastructure/inference roles. The historical research emphasized
well-compensated roles; no new salary floor has been confirmed for the accelerated search. Core areas:

1. AI platform and ML infrastructure;
2. inference, serving, runtime, performance, and optimization;
3. applied AI / AI engineering that delivers end-to-end business workflows;
4. ML systems spanning models, data, evaluation, deployment, and production operations.

### Supporting breadth

Model behavior, practical fine-tuning, evaluation and customer workflows support the infrastructure
and inference target. Pure model research, applied-scientist and management roles are not separate
active search or learning tracks in the accelerated plan.

### Excluded track

Engineering-manager roles are excluded by Hooman's November 9 instruction. Leadership remains
relevant evidence of IC scope and influence. Modeling/customer AI is supporting technical breadth;
do not build a second specialist curriculum before the core.

### Geography and current employment

Hooman lives in **San Jose, California**, remains employed at **Adobe — Machine Learning Engineer,
ASML**, and says no sponsorship is needed for applying (November 9). Do not infer permanent
residency, citizenship, a visa category or answers to differently worded future-sponsorship questions.
Remote work was previously preferred; actual role location and work arrangement need live checks.
Historical Canadian job locations remain historical facts.

## 3. Known career thesis

Hooman's strongest plausible positioning is not “pure model researcher” or “generic engineering
manager.” It is a senior technical leader who can connect models to reliable, valuable products:

- research/model integration and technical transfer;
- production pipelines, deployment, data preparation, and support;
- inference/platform systems and optimization;
- evaluation and workflow design;
- customer-domain discovery and end-to-end AI product delivery;
- Staff-level technical leadership across teams and stakeholders.

This is a hypothesis to validate against the market, not a conclusion to protect.

## 4. Source hierarchy

1. Primary evidence: employer job pages, official documentation, papers, repositories,
   benchmarks, filings, and direct work artifacts that Hooman is allowed to use.
2. Strong secondary evidence: reputable engineering blogs, conference talks, compensation
   datasets with stated methods, and corroborated practitioner material.
3. Discovery-only evidence: LinkedIn listings, recruiter posts, X posts, newsletters, and
   aggregators. Use them to find leads and hypotheses, then verify.
4. Personal evidence: résumé, check-ins, work summaries, public artifacts, and Hooman's direct
   recollection. Record the source class; do not inflate wording or impact.

## 5. Working rules

- Persist research to disk as it is completed; chat history is not durable memory.
- Maintain four living records: state, decisions, learnings, and long-term plans.
- Use explicit confidence labels and source/as-of dates.
- Separate job-market requirements from our interpretation of why they matter.
- Count repeated requirements across a representative sample; do not build a curriculum from
  one prestigious posting or a viral thread.
- Use equal skepticism on the preferred inference thesis and the modeling alternative.
- Prefer primary sources and reproducible analysis. Cross-check decision-driving claims.
- Teach unfamiliar topics in this order: big-picture design and diagrams; normal flow and main
  components; concrete implementations/examples; problems and constraints with motivated fixes
  and alternatives. Define terms at first use. Name practical services and explain what we build.
  Keep interview presentation advice separate. Early lessons may be long enough to lay foundations;
  shorten them as Hooman becomes familiar. Allow learning before unaided attempts; do not require
  guessing unfamiliar terminology. This is Hooman's explicit November 10 teaching preference.
- Convert learning into demonstrations: code, benchmarks, architecture work, technical writing,
  and interview explanations. Course completion alone is not proof of skill.
- For every technical learning topic, inspect relevant Adobe implementations, AIDocs, wikis, and
  the local monorepo at `/home/colligo/colligo` when access permits. Use them to connect public
  concepts to production practice, but distinguish current code, documentation, experiments, and
  historical patterns; do not assume an internal implementation is best or current without checking.
- Proactively explain security implications when a topic introduces a trust boundary, credential,
  network listener, untrusted artifact or code, user data, persistence, tool execution, or external
  side effect. State the threat, practical safe default, and what production controls are still
  missing.
- Keep Adobe/customer information private and sanitized. Never copy internal code, data,
  architectures, or confidential customer details into public artifacts.
- Treat team outcomes achieved under Hooman's leadership as part of his career impact. Preserve
  enough role, scope, metric, and confidentiality context to express that impact strongly.
- Make no external edits or communications without explicit approval.
- Whenever mentioning a file to Hooman, use its full absolute filesystem path. Never use a
  relative file path in a response.
- In responses, render local file paths as plain text or inline code, not Markdown file links; the
  client may shorten linked labels into relative paths even when their targets are absolute.

## 6. File organization

Root: `/home/colligo/hs_scripts/claude/dev_research`. Start with this charter, then the exact live
handoff at `/home/colligo/hs_scripts/claude/dev_research/PROJECT_STATE.md`. Read the decisions,
learnings and roadmap required by `/home/colligo/hs_scripts/claude/dev_research/AGENTS.md`; open
only the relevant topic after that. There is one current curriculum and one positioning plan.

| Open when you need… | Canonical location |
|---|---|
| Study sequence, gates and model/delegation contract | `/home/colligo/hs_scripts/claude/dev_research/learning/LEARNING_PLAN.md` |
| The current first exercise | `/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/STUDY_GUIDE.md` |
| Concept-first tutorial; interview rehearsal in a separate section | `/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/REVIEW_GUIDE.md` |
| Lesson 2: ML/inference explanation, worked memory estimate and closed answer key | `/Users/ana.rodrigues/Desktop/hooman/hs_scripts/claude/dev_research/learning/first-pass/ML_INFERENCE_GUIDE.md` |
| Lesson 2: local tensor, evaluation, memory and supplied-trace assignment | `/Users/ana.rodrigues/Desktop/hooman/hs_scripts/claude/dev_research/learning/first-pass/ML_INFERENCE_EXERCISE.md` |
| HTTP connections, polling, SSE, WebSockets and webhooks; six local Python examples | `/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/http_protocol.md` |
| LinkedIn copy, profile corrections and application handoff | `/home/colligo/hs_scripts/claude/dev_research/positioning/POSITIONING.md` |
| Current résumé | `/home/colligo/hs_scripts/claude/dev_research/positioning/HOOMAN_SHARIATI_RESUME.md` |
| Career claims and their evidence | `/home/colligo/hs_scripts/claude/dev_research/career/CAREER_EVIDENCE.md` |
| Serving reference notes, baseline lab and quiz | `/home/colligo/hs_scripts/claude/dev_research/learning/inference-baseline.md` |
| Attention reference | `/home/colligo/hs_scripts/claude/dev_research/learning/attention.md` |
| LoRA reference, primarily diffusion examples | `/home/colligo/hs_scripts/claude/dev_research/learning/lora.md` |
| Historical job-market evidence and limitations | `/home/colligo/hs_scripts/claude/dev_research/research/job-market/SUMMARY.md` |
| Original posting descriptions, not current vacancies | `/home/colligo/hs_scripts/claude/dev_research/research/job-market/postings.jsonl` |
| Bookmark-derived sources and discovery rationale | `/home/colligo/hs_scripts/claude/dev_research/research/x-bookmarks/SUMMARY.md` |
| Friend-plan comparison and retained audit links | `/home/colligo/hs_scripts/claude/dev_research/research/plan-comparison/SUMMARY.md` |
| Current job-search/md-viewer source review, Mac preferences and implementation handoff | `/Users/ana.rodrigues/Desktop/hooman/hs_scripts/claude/dev_research/research/job-search-tooling/SUMMARY.md` |
| Research method and evidence rules | `/home/colligo/hs_scripts/claude/dev_research/research-plan.md` |

The small JSON audit files and validator beneath the comparison topic support its historical
claims. Keep them even while the raw friend archive is unavailable. Source-manifest paths/hashes
are historical evidence and must not be rewritten merely to match the current layout.

The old remote-browser launcher and duplicate research overview were removed on November 9.
The previous cycle/week inference packet is consolidated into the topic reference above. Removed
originals are recoverable from Git; the cleanup record is in the live handoff. Do not recreate
obsolete browser tooling or a second study schedule during routine resume.

Add folders only for active topics. Keep each study packet focused, with the exercise separate
from its teaching/review guide. Length follows the learner's familiarity, not a fixed brevity rule.
Reference material is indexed by topic, and supporting data stays beside its canonical summary.

## 7. Definition of success

Hooman can solve unfamiliar coding problems, design and defend distributed/ML systems, explain
inference mechanics and measurements, and present accurate evidence of technical scope. The first
month establishes breadth and assessed gaps; the second targets those gaps and actual interviews.
Profile and résumé preparation overlap learning. Applications and external edits require the
user's authorization; the current instruction prepares them rather than submitting them.

Use `gpt-5.6-sol` at `xhigh` for bounded execution when available, as requested. Keep planning,
ambiguous judgments, shared-file integration and review centralized. Follow the task contract in
`/home/colligo/hs_scripts/claude/dev_research/learning/LEARNING_PLAN.md`; quality is checked through
sources, tests and independent performance, not assumed from a model name.
