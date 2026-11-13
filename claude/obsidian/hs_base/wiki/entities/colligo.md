---
type: entity
title: Colligo (AI Platform Monorepo)
tags: [colligo, firefly, ai-platform, monorepo, inference, training, adobe]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/colligo/AGENTS.md]]", "[[raw/colligo/README.md]]", "[[raw/colligo/aidoc/root.md]]", "[[raw/colligo/aidoc/philosophy.md]]", "[[raw/colligo/aidoc/monorepo/index.md]]"]
---

# Colligo (AI Platform Monorepo)

Adobe Firefly's **AI Platform monorepo** ("V2") — a single unified codebase for the end-to-end lifecycle of generative-AI experiences: model **inference/serving**, **training**, **data processing**, shared Python libraries, and the developer tooling that holds it all together. Also referred to internally simply as "the AI Platform monorepo."

Colligo is the largest and most important code block in the Firefly AI stack. It hosts both the **platform code** (inference framework, compute-platform SDK, build system) and the **user/tenant code** (models, pipelines, services) in one repo, so ~200 developers can build, test, and deploy against shared infrastructure.

## Why a monorepo

The platform serves two very different code lifecycles (see [[wiki/concepts/colligo-philosophy]]):

- **Short-lived code** (research/prototyping): shipped as an installable `pip` package (`adobe-aip` / `colligo[...]` extras) so users can consume platform capabilities without cloning the repo.
- **Long-lived code** (production): lives in the monorepo with heavy tooling investment, so collective maintenance overhead grows *sublinearly* as code and teams scale. A monorepo with proper tooling lets all teams share build/test/lint and test everything together, avoiding "dependency hell" across sibling repos.

## Repo layout

```
pylibs/            # shared Python libraries (colligo.* namespace)
  colligo/pluto/   #   Compute Platform (Pluto) — GPU/CPU job scheduling, quotas, training observability
  colligo/rhode/   #   Inference Framework internals (workers, queues, supervisor)
  colligo/sdk/     #   Inference SDK (call/run workers from a pip package or notebook)
  colligo/base/    #   core types, config, exceptions (validation_assert/runtime_assert)
models/            # ML model packages (Firefly, Flux, di_imaging, ...) — each its own package
managed_services/  # Inference "V3" — separate Bazel workspace, own AGENTS.md and deps
contrib/           # research/training codebases (Mori, AdobeDiffusion, eval_science, ...)
  Mori/            #   Training Framework (2nd-gen imaging/video GenAI training)
third_party/       # vendored deps as subtrees (adobe/* and external/*) — NEVER modify
docker/            # container images
tools/             # build/lint scripts, tasks.py (the ./m CLI)
envs/              # Python environment configs (UV lock files, constraints)
aidoc/             # platform docs (compiled to docs.ai.corp.adobe.com); aidoc/root.md is the topic index
data/              # test fixtures (Git LFS)
registry/          # generated — do not modify
```

Docs are **co-located** with code in per-directory `aidoc/` folders, and most subdirectories carry their own `AGENTS.md`/`CLAUDE.md` with package-specific guidance (84 `AGENTS.md`, 58 `CLAUDE.md` across the repo). The published docs site is `https://docs.ai.corp.adobe.com`.

## The major subsystems

| Subsystem | Where | Wiki page |
|---|---|---|
| Inference Platform (serving) | `aidoc/inference-platform/`, `pylibs/colligo/rhode/`, `models/` | [[wiki/concepts/colligo-inference]] |
| Inference SDK | `pylibs/colligo/sdk/` | [[wiki/concepts/colligo-inference-sdk]] |
| Managed Services (Inference V3, Bazel) | `managed_services/` | [[wiki/concepts/colligo-managed-services]] |
| Compute Platform (Pluto) SDK | `pylibs/colligo/pluto/` | [[wiki/concepts/colligo-pluto-sdk]] |
| Training Framework (Mori) | `contrib/Mori/` | [[wiki/concepts/colligo-training]] |
| Architecture & boundaries | whole repo | [[wiki/concepts/colligo-architecture]] |
| Dev workflow (build/lint/test/CI) | `tools/`, `envs/`, `aidoc/` | [[wiki/concepts/colligo-dev-workflow]] |

## Relationship to Pluto and Firefly

- Colligo **ships the [[wiki/entities/pluto|Pluto]] SDK/CLI** from `pylibs/colligo/pluto/`. Hooman's `aip` alias (`python -m colligo.pluto.sdk.cli`) is exactly this Colligo-shipped Pluto SDK — see [[wiki/concepts/pluto-cli-sdk]]. Pluto is the compute platform that runs Colligo's training jobs and interactive GPU sessions; its [[wiki/concepts/pluto-job-lifecycle|job lifecycle]] governs how those jobs schedule and run.
- **Firefly** is the product family (generative image/video/3D/audio) whose models and inference services are built and served out of Colligo. Model packages under `models/colligo/models/firefly/` (Clio, T5, diffusion, etc.) are the concrete tenants.
- Several platforms **moved out** of the monorepo and keep their own repos: the Data Platform, Lineage, the traditional Sensei Training Framework, and `colligo-deploy` (Helm charts + Ethos Flex config for V2 inference deployments, at `git.corp.adobe.com/firefly/colligo-deploy`).

## Hard boundaries (repo-wide rules)

- NEVER modify `third_party/`, `uv.lock`, or `*.lock` files.
- NEVER modify generated files: `*_pb2.py`, `*_pb2_grpc.py`, `*_pb2.pyi`, `registry/applications.yaml`.
- NEVER use plain `assert` in production code — use `validation_assert(cond, details)` (user-input errors → HTTP 422) or `runtime_assert(cond, details)` (internal invariants → HTTP 500) from `colligo.base.exceptions`.
- Python 3.10+, **absolute imports only** (`from colligo.base.x import y`), strict type annotations on public functions, Adobe copyright header on every source file, Google-style docstrings.
- PR titles need a JIRA prefix in brackets (`[FFP-123] ...` or `[NOJIRA] ...`) and must follow `.github/PULL_REQUEST_TEMPLATE.md`.

## Uncovered / future ingest

This ingest covered the core (architecture, inference, training, pluto-sdk, dev-workflow, managed-services). Not yet ingested and worth a follow-up pass:
- Inference infra deep-dives: `aidoc/inference-platform/infra/**` (auto-scaling, Ethos, colligo-deploy, SLO, observability), caplan (capacity planning), postmortems, newsletters.
- `pylibs/colligo/rhode/` internals in depth (task queues, rate limiter, backpressure, self-healing, supervisor) — only summarized here.
- The full `models/` catalog (Clio, Flux, di_imaging, substance3d, video, etc.) and per-model AGENTS.
- Managed Services V3 tutorials/samples A–F and Bazel rules in depth.
- CI (`aidoc/continuous-integration/`), testing (`aidoc/testing/`), static-analysis, code-review, and the announcements timeline.

## Related

- [[wiki/concepts/colligo-architecture]]
- [[wiki/concepts/colligo-inference]]
- [[wiki/concepts/colligo-inference-infra]]
- [[wiki/concepts/colligo-inference-sdk]]
- [[wiki/concepts/colligo-managed-services]]
- [[wiki/concepts/colligo-models]]
- [[wiki/concepts/colligo-training]]
- [[wiki/concepts/colligo-pluto-sdk]]
- [[wiki/concepts/colligo-dev-workflow]]
- [[wiki/concepts/colligo-philosophy]]
- [[wiki/concepts/ai-platform-overview]]
- [[wiki/entities/ai-platform-repo]] — the V3 framework + deploy infra extracted out; `managed_services` consumes it via `release/inference/v*` tags
- [[wiki/concepts/v3-deployment]] · [[wiki/concepts/v3-vs-v2]]
- [[wiki/entities/foundry]] — a tenant team (training in Colligo, inference via managed_services)
- [[wiki/entities/mori]] — the training framework it hosts in `contrib/`
- Flagship models: [[wiki/entities/firefly-clio]] · [[wiki/entities/firefly-clineto]] · [[wiki/entities/di-imaging]] · [[wiki/entities/flux]] · [[wiki/entities/firefly-substance3d]] · [[wiki/entities/firefly-firefall]]
- [[wiki/entities/pluto]] · [[wiki/concepts/pluto-cli-sdk]] · [[wiki/concepts/pluto-job-lifecycle]]
- [[wiki/sources/colligo-agents]]
