---
document_type: guide
children: 

- [/aidoc/inference-platform/framework/api.md, "Inference Platform API"]
- [/aidoc/inference-platform/framework/worker.md, "Inference Worker"]
- [/aidoc/inference-platform/framework/endpoints.md, "Inference Application Public Endpoints"]
- [/aidoc/inference-platform/framework/http_api.md, "Common Platform HTTP APIs"]
- [/aidoc/inference-platform/framework/gpu-based-overrides.md, "GPU based overrides"]
- [/pylibs/colligo/sdk/aidoc/index.md, "Inference SDK"]
- [/pylibs/colligo/rhode/aidoc/task_queue.md, "Worker Queues"]
- [/pylibs/colligo/rhode/aidoc/concurrency_rate_limiter.md, "Global Rate Limiter"]
- [/pylibs/colligo/rhode/aidoc/guest-fingerprint-check.md, "Guest Access Token Fingerprint Check"]
- [/pylibs/colligo/rhode/aidoc/backpressure.md, "Backpressure"]
- [/aidoc/inference-platform/framework/resilient-async-pipeline.md, "Resilient Async Pipelines"]
- [/pylibs/colligo/rhode/aidoc/multi_task_async_context.md, "Multi-Task Async Context"]
- [/pylibs/colligo/rhode/aidoc/worker_self_healing.md, "Worker Self-Healing"]
- [/aidoc/inference-platform/framework/block-upload.md, "Block Upload Support in Storage API"]
- [/aidoc/inference-platform/framework/debug-ui.md, "Debug UI"]
- [/aidoc/inference-platform/framework/distributed-tracing.md, "Distributed tracing"]
- [/aidoc/inference-platform/framework/external.md, "External services"]
- [/aidoc/inference-platform/framework/websocket.md, "WebSocket Streaming API"]
- [/aidoc/inference-platform/framework/sse.md, "SSE Streaming API"]
- [/aidoc/inference-platform/framework/featureflags.md, "Feature Flags"]

show_children: false
---

# Inference Framework

```{note}
**v3 is available as a release candidate.** The v3 worker and pipeline API is redesigned and ships as part of the [Managed Services (v3)](/managed_services/README.md) platform — a Bazel-based workflow that replaces this build system and deployment model. See [Managed Services (v3)](/managed_services/README.md) to get started.
```

The Inference Framework is the core developer-facing API for building, testing, and running inference workers. It provides the foundational abstractions, communication protocols, and utilities needed to serve ML models at scale.

```{seealso}
**Prerequisites**: Before reading this document, we highly suggest you have:
- Reviewed the [Inference Platform landing page](/aidoc/inference-platform/index.md)
- Got Access and set up your [development environment](/aidoc/monorepo/env-setup.md)
```

---

## Overview

An **inference worker** is an abstraction of a unit that can process requests, potentially calling other workers. Workers are organized into **applications** - collections of workers that can be deployed together.

```{figure} /aidoc/_assets/inference/inference-worker.png
:width: 80%
:align: center
*Components of an inference worker: API, implementation, and dependencies.*
```

Workers are roughly divided into two categories:

- **Pipeline workers**: Orchestration and I/O work
- **ML workers**: Heavy computation (mainly on GPU)

---

## Core Concepts and Features

### [Inference Platform API](/aidoc/inference-platform/framework/api.md)

API reference for defining workers, configuring deployments, and overriding worker configurations. Includes details on making public HTTP APIs and request/response types.

### [Inference Worker](/aidoc/inference-platform/framework/worker.md)

Guide to building inference workers with required components, configuration options, and best practices. Covers worker structure, using local files, `colligo.yaml` file specification, concurrency control, and multi-model deployment with GPU sharing.

### [Inference Application Public Endpoints](/aidoc/inference-platform/framework/endpoints.md)

Documentation on public HTTP endpoints exposed by inference applications, including endpoint configuration, request/response formats, and API conventions.

### [Common Platform HTTP APIs](/aidoc/inference-platform/framework/http_api.md)

Standard HTTP APIs automatically available in all deployed applications. Includes storage APIs for uploading assets, async job tracking, and health check endpoints.

### [Inference SDK](/pylibs/colligo/sdk/aidoc/index.md)

Python SDK for calling inference workers without full monorepo setup. Supports both HTTP clients for remote calls and native clients for local execution in Jupyter notebooks.

### [Worker Queues](/pylibs/colligo/rhode/aidoc/task_queue.md)

Distributed task queue implementations for worker-to-worker communication. Covers Redis Lists (FIFO), Sticky Streams (cache-aware routing), and Priority Queues (user prioritization).

### [Global Rate Limiter](/pylibs/colligo/rhode/aidoc/concurrency_rate_limiter.md)

Distributed rate limiting and concurrency control to protect services from overload. Supports per-endpoint rate limits, global concurrency caps, and graceful degradation.

### [Guest Access Token Fingerprint Check](/pylibs/colligo/rhode/aidoc/guest-fingerprint-check.md)

Opt-in middleware check that rejects guest access tokens (`atp=guest`) missing a fingerprint device ID (`fdi` claim). Enabled per-deployment with a single config flag; supports a client-ID allowlist for escape hatches. Replaces ad-hoc per-pipeline implementations.

### [Backpressure](/pylibs/colligo/rhode/aidoc/backpressure.md)

Backpressure mechanisms that signal when workers are overwhelmed, preventing queue overflow and cascading failures. Includes queue depth monitoring and automatic throttling.

### [Resilient Async Pipelines](/aidoc/inference-platform/framework/resilient-async-pipeline.md)

Durable async pipeline with job persistence, automatic retry, and worker heartbeat monitoring. Designed for long-running tasks with configurable timeouts and failure recovery.

### [Multi-Task Async Context](/pylibs/colligo/rhode/aidoc/multi_task_async_context.md)

Guide to running multiple concurrent tasks for the same session on a single worker. Includes feature flag setup, `task_id` usage via `RequestHints`, fanout and deduplication patterns, and per-instance deduplication constraints.

### [Worker Self-Healing](/pylibs/colligo/rhode/aidoc/worker_self_healing.md)

First-class API for a worker to request its own subprocess restart after the current request completes. Designed for vllm dead engine detection and other corrupted-state recovery scenarios. Covers `request_worker_restart()` usage, response strategies, drain guarantees, and the `enable_worker_restart_on_request` flag.

### [Block Upload Support in Storage API](/aidoc/inference-platform/framework/block-upload.md)

Chunked upload support for large assets with parallel transfer, resume capability, and improved performance. Enabled by default in experimental mode.

### [Debug UI](/aidoc/inference-platform/framework/debug-ui.md)

Web-based debug interface for request inspection, authentication token management, and service status monitoring. Accessible at port 8000 during local development.

### [Distributed Tracing](/aidoc/inference-platform/framework/distributed-tracing.md)

End-to-end request tracing across workers using in-house profiling tools. Traces can be visualized in Perfetto for performance analysis and debugging.

### [WebSocket Streaming API](/aidoc/inference-platform/framework/websocket.md)

A WebSocket API for securely streaming real-time ML requests and responses directly from Colligo worker pods.

### [SSE Streaming API](/aidoc/inference-platform/framework/sse.md)

Server-Sent Events (SSE) for pushing a sequence of typed events from a worker to a client over a single HTTP POST connection.

### [Feature Flags](/aidoc/inference-platform/framework/featureflags.md)

Dynamic feature toggles for enabling/disabling features, controlling configuration values, and implementing circuit breakers at runtime.

---

## Experimental Features

```{seealso}
See our [guide](/aidoc/inference-platform/user-guides/how-to-experimental-features.md) on how to use experimental features.
```

The following features are available but not yet recommended for production use without consultation:

| Feature | Description | Status | How to Enable |
|---------|-------------|--------|---------------|
| **Block Upload** | See [detailed guide](/aidoc/inference-platform/framework/block-upload.md) | 🎓  Flag moved to Common Config | `enable_block_upload: true` |
| **Stream Upload** | Parallel/streaming upload for storage API | ⚠️ Experimental | `enable_stream_upload: true` |
| **Buffer Request Body** | Buffer multipart form and JSON in frontend | 🎓  Flag is moved to Requestconfig. ExperimentConfig to be deprecated  | `buffer_request_body: true` |
| **CAI Claim 2.2** | Content Authenticity Initiative v2.2 | ⚠️ Experimental | `cai_claim_version: 2` |
| **Azure Assets Mirroring** | Copy files from presigned URLs to Azure blob Storage. See [guide](/pylibs/colligo/external_services/azure_assets_sync/aidoc/index.md) | ⚠️ Experimental | Use `AzureAssetsSyncClient` |

**Resources**:

- [Experimental config reference](/pylibs/colligo/base/config.py)

---

## External Services

Integration clients for Adobe and third-party services used by inference workers.

[**See supported External Services list →**](/aidoc/inference-platform/framework/external.md)
