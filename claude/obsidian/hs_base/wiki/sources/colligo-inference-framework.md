---
type: source
title: "Source: Colligo Inference Framework docs"
tags: [colligo, source, inference, framework, workers]
created: 2026-07-04
updated: 2026-07-04
ingested: 2026-07-04
raw: "[[raw/colligo/aidoc/inference-platform/framework/index.md]]"
sources: ["[[raw/colligo/aidoc/inference-platform/index.md]]", "[[raw/colligo/aidoc/inference-platform/framework/index.md]]", "[[raw/colligo/aidoc/inference-platform/framework/worker.md]]", "[[raw/colligo/aidoc/inference-platform/framework/endpoints.md]]"]
---

# Source: Colligo Inference Framework docs

Distilled from the V2 Inference Platform docs: the landing page, framework index, worker guide, and public-endpoints guide. Full synthesis in [[wiki/concepts/colligo-inference]].

## What these docs cover

- **Landing (`inference-platform/index.md`):** three product areas — Inference Framework, Inference Infrastructure (Ethos, storage, Redis/MemoryDB, autoscaling, observability), and Monorepo Dev Experience. Quick-start path: get access → env setup → build a worker → deploy to Ethos → Operational Readiness Review. Support via `#firefly-colligo` / `#firefly-sre-devops` Slack, Jira intake, shared on-call. Banner: **V3 is a release candidate**.
- **Framework index:** catalog of features, each with its own doc — API, worker, endpoints, HTTP APIs, GPU overrides, SDK, worker queues (FIFO/sticky/priority), global rate limiter, backpressure, resilient async pipelines, multi-task async context, worker self-healing, block upload, debug UI, distributed tracing, WebSocket/SSE streaming, feature flags, external-service clients. Most internals live in `pylibs/colligo/rhode/`.
- **Worker guide:** worker = unit doing compute (called by another worker or an HTTP endpoint); apps = deployable worker collections registered in `models/build/apps/app_*.py`. Required files per worker (`types.py`, config, model class extending `ColligoMLModel[Config]`, `build.py`, `colligo.yaml`). Concurrency: ML thread pool → workers-per-replica → pod replicas. Multi-model GPU sharing via Rhode Supervisor subprocesses + bin-packing + `CUDA_VISIBLE_DEVICES` isolation.
- **Endpoints guide:** opt-in `PublicEndpoint` (JS-friendly, backward-compat), sync (60s gateway timeout) vs async (poll/cancel URLs, v2/v3), `PublicBinary`, multipart encoding, WebSocket + SSE streaming.

## Key facts worth remembering

- Sync public endpoints have a hard **60-second gateway timeout** (`504` otherwise).
- ML pre/post-processing belongs on **pipeline** workers, not GPU ML workers.
- vLLM-style libs need `CUDA_VISIBLE_DEVICES` isolation because they ignore `set_current_device()`.

## Related

- [[wiki/concepts/colligo-inference]]
- [[wiki/concepts/colligo-inference-sdk]]
- [[wiki/entities/colligo]]
