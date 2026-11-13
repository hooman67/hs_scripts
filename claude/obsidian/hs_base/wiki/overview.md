---
type: overview
title: Overview
tags: [meta]
created: 2026-07-04
updated: 2026-09-14
---

# Overview

This is Hooman's personal LLM-maintained knowledge base — a persistent, interlinked wiki that the
LLM builds and keeps current from raw sources, rather than re-deriving answers from scratch on every
query. See [[wiki/concepts/llm-wiki-pattern|the LLM-Wiki pattern]] for the idea and
[[wiki/concepts/three-layer-architecture|the architecture]] for how it's laid out.

## How it works here

- **Raw sources** live in `raw/` — including Hooman's technical notes symlinked at `raw/docs/`
  (asml_notes, glimmer, colligo, foundry, guides, …) and the founding
  [[wiki/sources/llm-wiki|Karpathy idea file]].
- **The wiki** (this folder) is LLM-owned synthesis: concepts, entities, source summaries, and
  analyses — all cataloged in [[index]].
- **Navigation** via [[index]] (catalog) and [[log]] (timeline); conventions in [[WIKI_SCHEMA]].
- **Operations** via skills: `/obs-ingest`, `/obs-query`, `/obs-search`, `/obs-lint`, `/obs-index`.

## Current state

Seeded 2026-07-04 with the LLM-Wiki pattern itself. Hooman's `docs/` notes are wired in as raw
sources and are being ingested topic-by-topic.

**Adobe AI infrastructure** — the first real domain. See [[wiki/concepts/ai-platform-overview|the
platform map]] for how the pieces fit. Foundational building blocks ingested so far:
- **[[wiki/entities/pluto|Pluto]]** — the compute platform. Covered in depth: the
  [[wiki/concepts/pluto-resource-hierarchy|resource hierarchy]],
  [[wiki/concepts/allocation-priority-tiers|priority tiers]] &
  [[wiki/concepts/quota-and-utilization|quota/utilization]], the
  [[wiki/concepts/pluto-job-lifecycle|job lifecycle]], [[wiki/concepts/pluto-console|console]] &
  [[wiki/concepts/pluto-cli-sdk|CLI/SDK]], [[wiki/concepts/pluto-storage|storage]],
  [[wiki/concepts/pluto-secrets|secrets]], [[wiki/concepts/pluto-docker-images|images]],
  [[wiki/concepts/pluto-jupyter|Jupyter]], [[wiki/concepts/pluto-policy|policy]] &
  [[wiki/concepts/pluto-troubleshooting|troubleshooting]], and the
  [[wiki/concepts/pluto-operations|governance/operations layer]].
- **[[wiki/entities/colligo|Colligo]]** — Firefly's AI-platform monorepo for training & inference (it
  ships Pluto's SDK). Covered: [[wiki/concepts/colligo-architecture|architecture]],
  [[wiki/concepts/colligo-inference|inference]] (V2 + [[wiki/concepts/colligo-managed-services|V3]] +
  [[wiki/concepts/colligo-inference-infra|infra]]), the
  [[wiki/concepts/colligo-models|models catalog]] (~52 packages, incl. flagship
  [[wiki/entities/firefly-clio|Clio]] / [[wiki/entities/firefly-clineto|Clineto]] /
  [[wiki/entities/di-imaging|DI Imaging]]), [[wiki/concepts/colligo-training|training]], the
  [[wiki/concepts/colligo-pluto-sdk|Pluto SDK]], [[wiki/concepts/colligo-dev-workflow|dev workflow]]
  & [[wiki/concepts/colligo-philosophy|philosophy]].
- **[[wiki/entities/mori|Mori]]** — Firefly's PyTorch-native training framework (MoriX accelerator),
  runs on Pluto. Covered: [[wiki/concepts/mori-architecture|architecture]],
  [[wiki/concepts/mori-training-workflow|training workflow]],
  [[wiki/concepts/mori-parallelism|parallelism]], [[wiki/concepts/mori-config|config]],
  [[wiki/concepts/mori-checkpointing|checkpointing]], [[wiki/concepts/mori-observability|observability]],
  [[wiki/concepts/mori-pluto-agent|Pluto Agent]] & [[wiki/concepts/mori-dependency-management|deps]].
- **[[wiki/entities/ai-platform-repo|ai-platform repo (V3)]]** — the current model-deployment stack:
  the [[wiki/concepts/v3-inference-framework|inference framework]] wheel +
  [[wiki/concepts/v3-deployment|Bazel→ArgoCD→Ethos deploy]] machinery +
  [[wiki/concepts/v3-models-hub|models hub]]; [[wiki/concepts/v3-vs-v2|V3 vs V2]] spans ai-platform + Colligo.
- **[[wiki/entities/foundry|Foundry]]** — Hooman's own team & monorepo (customer/partner generative
  models). Covered: [[wiki/concepts/foundry-modeling|modeling]] (the priority),
  [[wiki/concepts/foundry-compute|compute]] (job_agent/job_police),
  [[wiki/concepts/foundry-terraform|terraform]] & per-customer storage,
  [[wiki/concepts/foundry-third-party-models|3P-models process]],
  [[wiki/concepts/foundry-dev-workflow|dev workflow]], the
  [[wiki/entities/foundry-gateway|access gateway]] & [[wiki/concepts/foundry-aws-access|AWS-access model]],
  plus [[wiki/entities/foundry-studio|Studio]] and [[wiki/entities/media-intelligence|Media Intelligence]],
  including the MI [[wiki/concepts/media-intelligence-ingestion|ingestion workflow]] and
  [[wiki/concepts/media-intelligence-gap-analysis|corpus gap-analysis loop]]. A worked example of a
  Foundry customer app: **[[wiki/entities/thd-video|THD Video]]** (reference-to-video via
  [[wiki/entities/seedance|Seedance]]/fal) — covering [[wiki/concepts/seedance-prompting|prompting &
  the structured rewriter]], the [[wiki/concepts/foundry-standalone-app-pipeline|standalone-app
  pipeline]] (+ SAM3 anonymize), [[wiki/concepts/foundry-dev-deploy|dev deploy]],
  [[wiki/concepts/foundry-local-debugging|local debugging]], and the
  [[wiki/concepts/foundry-eval-workflow|eval workflow]] + [[wiki/concepts/foundry-eval-html-reports|
  result HTMLs]].

Neighbouring systems referenced but not yet ingested: [[wiki/entities/genie|Genie]],
[[wiki/entities/glimmer|Glimmer]].

## Related
- [[wiki/entities/pluto]]
- [[wiki/entities/colligo]]
- [[wiki/concepts/rag-vs-persistent-wiki]]
- [[wiki/concepts/index-and-log]]
- [[wiki/entities/obsidian]]
