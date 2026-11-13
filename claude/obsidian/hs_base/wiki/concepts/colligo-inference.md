---
type: concept
title: Colligo Inference Platform
tags: [colligo, inference, serving, rhode, workers, ethos, firefly]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/colligo/aidoc/inference-platform/index.md]]", "[[raw/colligo/aidoc/inference-platform/framework/index.md]]", "[[raw/colligo/aidoc/inference-platform/framework/worker.md]]", "[[raw/colligo/aidoc/inference-platform/framework/endpoints.md]]"]
---

# Colligo Inference Platform

The [[wiki/entities/colligo|Colligo]] subsystem for **serving ML models and AI applications** at scale — from local experimentation to production services on Ethos Kubernetes clusters. This page covers the **V2 (stable)** platform; the newer Bazel-based V3 is [[wiki/concepts/colligo-managed-services|Managed Services]].

## Three product areas

1. **Inference Framework** — the developer-facing API for building/testing/running workers (`pylibs/colligo/rhode/` internals). Worker API + orchestration, worker-to-worker queues (FIFO / sticky / priority), resilient durable async queues with retries, temporary asset storage, distributed rate limiting + backpressure, profiling/logging/metrics, local dev + debug UI, and integrations with Adobe services (IMS, CAI, ACP, ACMP).
2. **Inference Infrastructure** — deployment to **Ethos** clusters (dev/stage/prod), S3 + Azure storage, multi-tenant metadata in Redis/MemoryDB, autoscaling, observability (Grafana, Splunk, Prometheus, NewRelic).
3. **Monorepo Developer Experience** — the Inference Platform team is the main tenant/maintainer of the monorepo tooling: build system, dependency management, CLI, static analysis, testing, CI, code ownership, versioning/release. See [[wiki/concepts/colligo-dev-workflow]].

## Workers and applications

An **inference worker** is a unit that processes requests and can call other workers. Two categories:

- **Pipeline workers** — orchestration and I/O.
- **ML workers** — heavy (usually GPU) compute; extend `ColligoMLModel`.

A collection of interdependent workers deployable together is an **application**. The infra serves *applications*, not individual workers. Apps are registered in `models/build/apps/app_*.py` via `build.application(...)` (e.g. `app_firefly.py`); passing a set of workers pulls them and their deps into the app.

**Required components of a worker** (all workers live under `models/colligo/`):
- Request/response types (`types.py`)
- Worker-specific config type
- The worker class defining `handle_request`, coupled to its config, e.g. `T5Model(ColligoMLModel[T5Config])`
- A `build.py` declaring request/response types, code+data deps, and the worker via `build.deploy_worker(...)`
- A `colligo.yaml` declaring deps and an optional `public` sub-package (see [[wiki/concepts/colligo-architecture]])

**Worker guidelines:** do pre/post-processing on pipeline workers (not GPU ML workers) to save bandwidth and GPU cycles; attach image ranges to tensors via `.with_image_range(...)`; workers should load only the data they need (>10 GB is a red flag — often an untrimmed checkpoint).

## Concurrency model (narrow → broad)

- **ML thread pool** — `concurrent_ml_threads` (default 1) per ML worker; increase only if thread-safe. Bypassed if you override `handle_request` (call `self.ml_executor.run_in_bg(...)` explicitly).
- **Worker replicas** — `workers_per_replica` (default 1; frontend/CPU workers default 4): number of worker processes per pod, each fully consuming the configured resources.
- **Pod replicas** — `replicas`: number of k8s pods (each an identical app).

## Multi-model deployment & GPU sharing

Multiple ML models can co-locate in one pod, each a **separate Python subprocess** under the **Rhode Supervisor** (process isolation, independent scaling, shared metrics/logging). GPU memory is bin-packed (largest first) and enforced via `torch.cuda.set_per_process_memory_fraction()` plus per-subprocess `CUDA_VISIBLE_DEVICES` isolation (the "nuclear option" for libs like vLLM that grab all GPUs). Configured via `GpuInfo(memory_gb=..., count=...)` in `build.py`, `additional_workers` for co-location, and `fill_with_model` / `ReplicaCount` to soak up remaining GPU capacity. Caveats: soft memory enforcement, no CUDA MPS (time-share not true share), static startup allocation, autoscaling gets confused by mixed-latency co-tenants (often disable it).

## Public HTTP endpoints

By default workers only expose **internal** endpoints callable via the [[wiki/concepts/colligo-inference-sdk|Inference SDK]]. **Public HTTP endpoints** (JS-friendly, with backward-compat promises) are opt-in via `PublicEndpoint(...)` passed to `build.deploy_worker`, with `to_request`/`from_response` adapters converting between HTTP and pipeline types.

- **Sync** endpoints (`is_async=False`): return directly, hard **60s gateway timeout** (`504` otherwise) — for tasks under ~60s.
- **Async** endpoints (`is_async=True`): return poll/cancel URLs immediately (v2 or v3 links inferred from path version); timeout via `initial_session_ttl_s`. Not retried unless made a **resilient async pipeline**.
- **PublicBinary** type carries images/video/3D across ACP file ids, presigned URLs, multipart form, or S3.
- **Streaming**: WebSocket (`enable_streaming=True`, signed short-lived URL via Cluster Gateway) and SSE (`is_sse=True` + `enable_sse=True`) over a single HTTP POST.

## Related framework features

Worker queues (Redis lists / sticky streams / priority), global concurrency rate limiter, backpressure, resilient async pipelines (durable job persistence + retry + heartbeat), multi-task async context, worker self-healing (`request_worker_restart()`, e.g. vLLM dead-engine recovery), block/stream upload, distributed tracing (Perfetto), feature flags, guest-token fingerprint checks. Most live under `pylibs/colligo/rhode/aidoc/`.

## Related

- [[wiki/entities/colligo]]
- [[wiki/concepts/colligo-inference-sdk]]
- [[wiki/concepts/colligo-managed-services]]
- [[wiki/concepts/colligo-architecture]]
- [[wiki/entities/pluto]] — GPU compute for local dev / interactive sessions
- [[wiki/sources/colligo-inference-framework]]
