---
type: entity
title: ai-platform repo (V3)
tags: [ai-platform, v3, inference, deployment, bazel, firefly, adobe, colligo]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/ai-platform/README.md]]", "[[raw/ai-platform/AGENTS.md]]", "[[raw/ai-platform/platforms/dev_tools/aidoc/code-structure.md]]", "[[raw/ai-platform/platforms/inference/AGENTS.md]]", "[[raw/ai-platform/platforms/inference/aidoc/index.md]]"]
---

# ai-platform repo (V3)

Adobe Firefly's **standalone AI-Platform repo** (`github.com/Adobe-Firefly/ai-platform`) — the
codebase Hooman's team calls **"V3"**, the current/latest way of **deploying models**. It is the
successor path to the [[wiki/entities/colligo|Colligo]] "V2" serving stack
([[wiki/concepts/colligo-inference]]). It packages the **inference framework** as a standalone
Python wheel and the **deployment build infra** as a versioned Bazel module, so a model can go from
code → deployed Ethos endpoint without checking out the Colligo monorepo.

> The "V3 stack" spans **two repos**: this **ai-platform** repo (the framework + platform build
> infra + model hub) and **`colligo/managed_services`** (the opinionated user-facing services
> ecosystem that *consumes* this repo — see [[wiki/concepts/colligo-managed-services]]). This page
> covers the ai-platform repo; [[wiki/concepts/v3-deployment]] covers how the two fit together.

## What it is (self-description)

"The unified repository for AI Platform org products and their users." A collection of
**self-contained folders (virtual repos)** — any folder with a `.vscode/` at its root is a
standalone sub-repo with its own build/test. The only thing shared at the root is documentation
(all `README.md`/`*.md` feed a Sphinx docs site at `docs.ai.corp.adobe.com/v3/…`, built via
`./gtools docs build`). Repo scale at ingest: ~7,322 files, 539 doc files.

## Top-level layout

```
frameworks/     # AI-Platform product libraries (stable Python APIs users import)
  inference/serve/   # THE Inference Framework — pip install frameworks.inference (workers/pipelines/webapps)
  inference/aoti/    # ahead-of-time-inductor torch compilation/quantization helpers
  training/ data/ agent/   # sibling frameworks (training, dataloading, LLM agents)
models/         # the Model Hub — shareable, packaged model forward-execution (models.<name>)
  hub/          #   the hub SDK + hub.make dispatcher; per-model folders (t5_xxl, gen45_dit, …)
platforms/      # AI-Platform-team code that isn't a framework
  inference/    #   Bazel build/deploy infra → the @platforms_inference module (ethos_deployment, charts)
  pluto/        #   Pluto compute-platform code lives here (see note below)
  dev_tools/    #   repo-wide tooling, code-structure conventions, docs build
third_party/    # vendored deps (ffmpeg, flash-attn, redis, torch-torio)
aidoc/          # cross-cutting docs (data-ecosystem, feature-registry, genie, glimmer)
gtools          # root dispatcher (docs build, netrc, …)
```

The three-layer code convention (from `code-structure.md`): **cloud** (deploy manifests) on top,
then **models**, then **frameworks** (agent/training/data/inference), then **platforms**
(agent/dev_tools/compute/data/inference) as the base.

## The three inference layers

Per `platforms/inference/AGENTS.md`, the inference offering is three layers:

1. **Inference Framework** — `pip install frameworks.inference`, a standalone library for workers,
   pipelines, web apps. Lives at `frameworks/inference/serve/`. See
   [[wiki/concepts/v3-inference-framework]].
2. **Inference Platform** — `platforms/inference/`; Bazel build rules, k8s deployment automation,
   capacity planning. Produces the `@platforms_inference` Bazel module. See
   [[wiki/concepts/v3-deployment]].
3. **Managed Services** — the opinionated user ecosystem that consumes both; it lives in the
   **colligo** repo at `managed_services/`, not here. See [[wiki/concepts/colligo-managed-services]].

## Relationship to Colligo, Pluto, Firefly

- **Colligo (V2):** ai-platform *extracts and cleans up* Colligo's serving path. The framework still
  vendors proven V2 internals (multiprocess comms, Redis queues, logging) under
  `frameworks/inference/serve/_private/colligo/` behind a **shim layer** that bridges the clean V3
  config API to V2 implementation. External Adobe services (CAI/IMS/BKS/temp-storage/ACP) are wrapped
  in a temporary `frameworks.inference.migration.*` API whose implementation still lives in Colligo
  and must be **manually synced**. See [[wiki/concepts/v3-vs-v2]].
- **Pluto:** `platforms/pluto/` — the [[wiki/entities/pluto|Pluto]] compute-platform code physically
  lives in this repo (this is where the `pluto-*` release tags come from). Pluto is already covered by
  the Pluto pages; ai-platform treats Pluto as one of three **deployment targets** (quick GPU
  access / prototyping) alongside Managed Services and self-managed k8s.
- **Firefly:** the product family whose models (FLUX, gen45/gen6, filix3, Clineto, etc. — many under
  `models/`) are packaged and deployed through this stack.

## Related

- [[wiki/concepts/v3-inference-framework]] — the programming model (workers/pipelines/web apps)
- [[wiki/concepts/v3-deployment]] — Bazel → Argo CD → Ethos release pipeline
- [[wiki/concepts/v3-models-hub]] — model packaging / distribution
- [[wiki/concepts/v3-vs-v2]] — how V3 differs from Colligo V2 + migration path
- [[wiki/concepts/colligo-managed-services]] — the consuming user ecosystem (in colligo)
- [[wiki/concepts/colligo-inference]] — the V2 (Rhode) serving platform this succeeds
- [[wiki/entities/colligo]] · [[wiki/entities/pluto]]
- [[wiki/concepts/ai-platform-overview]] — the broader platform portal map
- [[wiki/sources/ai-platform-repo-ingest]] — the doc sources this synthesizes
