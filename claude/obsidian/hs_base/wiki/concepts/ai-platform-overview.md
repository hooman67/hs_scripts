---
type: concept
title: Adobe AI Platform — Portal Overview
tags: [ai-platform, adobe, firefly, colligo, pluto, inference, training, data, docs-portal]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/ai-platform-docs]]"]
---

# Adobe AI Platform — Portal Overview

The **Adobe AI Platform** is the end-to-end stack for "delivering delightful AI experiences to
Adobe's users" — spanning **compute, training, inference, and data processing**. Its documentation
portal is `https://docs.ai.corp.adobe.com/`, compiled from the co-located `aidoc/` folders of the
[[wiki/entities/colligo|Colligo]] monorepo. This page maps the whole portal and how the pieces fit;
each piece links to its dedicated wiki page.

The platform's founding idea (see [[wiki/concepts/colligo-philosophy]]): unify three historically
separate efforts — Firefly inference tech, training-data processing, and AI compute infra — behind
one monorepo with shared tooling, so maintenance overhead grows *sublinearly* as code and teams
scale past ~200 developers.

## The pieces and how they fit

An AI experience flows through the platform roughly left-to-right: **data → training → a model →
inference serving**, all running on the shared **compute** substrate and governed by common
engineering practices.

| Piece | What it is | Docs path | Wiki page |
|---|---|---|---|
| **Compute Platform (Pluto)** | GPU/CPU job scheduling, quotas, training observability — the substrate training and interactive jobs run on. | `pylibs/colligo/pluto/aidoc/` | [[wiki/entities/pluto]] |
| **Training Framework (Mori)** | 2nd-gen imaging/video GenAI training framework; runs on Pluto. | `contrib/Mori/aidoc/` | [[wiki/concepts/colligo-training]] · [[wiki/entities/mori]] |
| **Inference Platform** | Managed platform for serving ML models & AI apps at scale (V2 + V3). | `aidoc/inference-platform/` | [[wiki/concepts/colligo-inference]] · [[wiki/concepts/colligo-inference-infra]] · [[wiki/concepts/colligo-managed-services]] |
| **Data Platform** | Training-data pipelines. | `aidoc/data-platform/` | [[wiki/entities/genie]] · [[wiki/entities/glimmer]] |
| **Capability Registry** | Browsable catalog of registered inference apps + their declared capabilities (workflow/model/modality/dimensions); powers discovery and routing. | `aidoc/inference-platform/capability-registry.html` | [[wiki/concepts/colligo-inference-infra]] |
| **Monorepo & Access Control** | The single codebase and its access model. | `aidoc/monorepo/`, `aidoc/access-control.html` | [[wiki/concepts/colligo-architecture]] |

All of it lives in one repo — the [[wiki/entities/colligo|Colligo]] monorepo — which is why the docs
portal, the platform code, and the tenant/model code share a URL tree.

## Engineering practices (cross-cutting)

The portal dedicates a whole band to shared practices, all owned/maintained largely by the Inference
Platform team as the monorepo's main tenant (see [[wiki/concepts/colligo-dev-workflow]]):
Documentation, Code Review, Source Control, Testing, Dependency Management, Continuous Integration,
Static Analysis, and Docker Containers.

## Two code lifecycles

The platform is explicitly designed for two audiences (see [[wiki/concepts/colligo-philosophy]]):

- **Short-lived code** — research/prototyping; shipped as installable pip packages (`adobe-aip` /
  `colligo[...]`) so users consume platform capabilities without cloning the repo (e.g. the
  [[wiki/concepts/colligo-inference-sdk|Inference SDK]] and [[wiki/concepts/pluto-cli-sdk|Pluto SDK]]).
- **Long-lived code** — production; lives in the monorepo with heavy tooling investment.

## Scope note

This page is a map, synthesized from the portal's own navigation. Depth on the serving
infrastructure is in [[wiki/concepts/colligo-inference-infra]]. Depth on Pluto, the models catalog,
and training/Mori lives in their own pages (owned separately).

## Related

- [[wiki/entities/colligo]] — the monorepo everything ships from
- [[wiki/concepts/colligo-philosophy]]
- [[wiki/concepts/colligo-inference]] · [[wiki/concepts/colligo-inference-infra]] · [[wiki/concepts/colligo-managed-services]]
- [[wiki/entities/pluto]] · [[wiki/concepts/colligo-training]]
- [[wiki/entities/genie]] · [[wiki/entities/glimmer]] · [[wiki/entities/mori]]
- [[wiki/sources/ai-platform-docs]]
