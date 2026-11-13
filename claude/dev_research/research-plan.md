# Research Plan — Job Market to Skills to Learning

## Contents

- [1. Research question](#1-research-question)
- [2. Confidence and claim classification](#2-confidence-and-claim-classification)
- [3. Job-posting evidence schema](#3-job-posting-evidence-schema)
- [4. Initial market sample](#4-initial-market-sample)
- [5. Anti-hallucination and quality gates](#5-anti-hallucination-and-quality-gates)
- [6. Skill synthesis](#6-skill-synthesis)
- [7. Curriculum gate](#7-curriculum-gate)
- [8. Parallel execution](#8-parallel-execution)
- [9. Record keeping](#9-record-keeping)

## 1. Research question

For well-compensated Senior IC and Staff/Principal roles near AI platform, inference, ML systems, applied AI,
and production-oriented modeling:

1. Which role families are genuinely available?
2. Which skills are required, preferred, or differentiating?
3. Which expectations are common across employers versus stack-specific?
4. What evidence do senior candidates need to demonstrate?
5. Which gaps belong in the first-month breadth pass and which should drive second-month depth?

The September 15 sample remains historical skill evidence. The November 9 goal is an accepted
offer within two months. When Hooman requests applications, refresh a bounded set of live employer
roles; do not treat old postings as active or restart the full market collection by default.

## 2. Confidence and claim classification

- **VERIFIED:** directly supported by a current primary source, or independently confirmed by
  multiple reliable sources. Include URL/source, retrieval date, and applicable scope.
- **ASSUMED:** a transparent interpretation or planning estimate. State what would verify it.
- **UNVERIFIED:** plausible but materially unsupported. It cannot drive a curriculum or résumé
  claim until resolved.
- **USER-CONFIRMED:** a decision, preference, or recollection explicitly provided by Hooman.
  This is authoritative for preferences but not independent proof of business impact.

For career accomplishments, use source-specific labels in `career/CAREER_EVIDENCE.md` rather
than silently upgrading a résumé statement or recollection to independently verified fact.

## 3. Job-posting evidence schema

For every sampled role record:

- company, title, level, location, and remote status;
- employer career-page URL and retrieval date;
- posted compensation and whether it is base, bonus, equity, or total compensation;
- role family and product/system context;
- required skills exactly as listed;
- preferred skills exactly as listed;
- years/seniority expectations;
- responsibility and scope signals;
- interview or hiring-process evidence, if sourced;
- notes and confidence; and
- duplicate/repost relationship.

Normalize synonyms only in a separate analysis column. Preserve the employer's original words.

## 4. Initial market sample

Sample across these families:

1. inference/serving/runtime/performance;
2. AI platform/ML infrastructure/MLOps;
3. applied AI/product workflow/agents;
4. ML systems spanning data, evaluation, and production;
5. applied scientist/modeling roles with production ownership.

Favor roles whose posted range crosses $200K or whose credible total compensation is well above
$200K. Record base and total compensation separately. Include a limited lower-compensation sample
only when it supplies important skill evidence, such as Canadian or internal Adobe roles.

Use employer career pages as the canonical listing. LinkedIn and other boards are discovery
surfaces. De-duplicate reposts and staffing copies. Do not infer demand from raw listing counts
without controlling for duplicates, geography, and company hiring volume.

## 5. Anti-hallucination and quality gates

1. Every material claim gets a source and as-of date.
2. A viral post or one prestigious employer cannot define the curriculum.
3. Distinguish “required,” “preferred,” and our interpretation.
4. Separate current market frequency from strategic future importance.
5. Cross-check compensation, role level, and technical claims when they drive prioritization.
6. Treat expired postings as historical evidence and label them.
7. Record access limitations; blocked pages do not prove absence.
8. Search for contradictory evidence and alternative role families.
9. Re-run a subset later to test whether findings are stable or momentary.
10. Never invent impact metrics. Team outcomes are valid evidence when Hooman led or materially
    drove them; capture enough context to select the strongest accurate leadership or execution verb.
11. For each technical learning topic, inspect applicable Adobe code and internal documentation
    when accessible. Label whether a finding comes from current code, documentation, an experiment,
    or historical practice; internal use is practical evidence, not automatic proof of best practice.
12. Include a security pass whenever the topic crosses a network, credential, data, model-artifact,
    persistence, tool-execution, or authorization boundary. State threats, safe defaults, and
    controls that a production design would still require.

## 6. Skill synthesis

Create a skills matrix with:

- frequency across all roles and within each family;
- required versus preferred frequency;
- seniority leverage: baseline, Staff differentiator, or specialist differentiator;
- transferability across employers/stacks;
- Hooman's evidence level: demonstrated, historical/stale, exposure-only, or absent;
- confidence in that assessment;
- time to close the gap;
- best proof artifact; and
- priority score.

Do not prioritize by frequency alone. A skill can be rare but decisive for the target niche;
another can be common boilerplate with little interview leverage.

## 7. Curriculum gate

A topic enters the learning plan only when at least one applies:

- it recurs materially across the market sample;
- it is a high-leverage differentiator in the chosen role family;
- it closes a verified weakness in Hooman's current evidence;
- it enables multiple other skills or proof artifacts; or
- it is required for credible Staff-level systems reasoning.

Each module needs a learning objective, primary resources, hands-on work, an assessment, a public-
safe artifact where appropriate, an ordered scope and a stop condition. The accelerated plan does
not require fixed hour estimates. Reassess rather than extending
a module indefinitely.

## 8. Parallel execution

Use background agents for independent employer sets or role families when authorized. Each writes
to its own raw-data area and reports sources. Keep the main session free for coordination. Serialize:

1. evidence collection before normalization;
2. normalization before skills synthesis;
3. synthesis before gap ranking; and
4. gap ranking before curriculum design.

Only one owner edits canonical summaries and shared matrices. More agents are useful only when the
work is independent and the integration cost stays low.

## 9. Record keeping

After every substantive batch:

- update `PROJECT_STATE.md` with completed scope and the next exact step;
- add durable findings to `LEARNINGS.md`;
- record accepted choices in `DECISIONS.md`;
- update the relevant topic's canonical summary;
- keep raw inputs beneath that topic rather than at repository root; and
- check whether the long-term roadmap changed.
