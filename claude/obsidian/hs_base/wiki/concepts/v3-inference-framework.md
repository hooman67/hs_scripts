---
type: concept
title: V3 Inference Framework (frameworks.inference)
tags: [ai-platform, v3, inference, framework, workers, pipelines, webapps, firefly]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/ai-platform/frameworks/inference/serve/aidoc/index.md]]", "[[raw/ai-platform/frameworks/inference/serve/aidoc/api.md]]", "[[raw/ai-platform/frameworks/inference/serve/README.md]]", "[[raw/ai-platform/frameworks/inference/serve/samples/a_basic/README.md]]", "[[raw/ai-platform/frameworks/inference/serve/samples/flux/README.md]]", "[[raw/ai-platform/frameworks/inference/serve/migration/README.md]]"]
---

# V3 Inference Framework (frameworks.inference)

The developer-facing programming model of [[wiki/entities/ai-platform-repo|V3]] — a **standalone
Python wheel** (`pip install frameworks.inference`) for building inference services out of three
building blocks: **compute workers**, **pipeline workers**, and **web apps**. The defining V3 change
vs [[wiki/concepts/colligo-inference|V2]] is that the framework has **no dependency on the monorepo
or the deployment system** — you can run the whole stack on your laptop, a Pluto node, or anywhere
Python runs, and *how* you deploy is a separate choice ([[wiki/concepts/v3-deployment]]).

## The building blocks

An **inference application** = a web server → one or more **pipeline workers** → one or more
**compute workers** (which may be called `remote` over a queue or `collocated` in the same pod).

- **`inference.Worker`** — the smallest deployable unit: takes a typed `Input`, runs user code in
  `execute(input, kit)`, returns a typed `Output`. Optional `load(params)` for model loading.
  Subclasses redefine `Input` / `Output` / `Config`; the class is turned into a servable instance
  with **`bind(config=…, serve_config=…, binary_groups=…)`**. Convention: a stub class declares the
  API and points `ImplRef = ".impl.MyWorkerImpl"` at the heavy implementation (keeps API modules
  importable without torch).
  - *Compute workers* do the heavy (usually GPU) work.
  - *Pipeline workers* orchestrate — call other workers, do pre/post-processing (keep this off the
    GPU workers to save bandwidth/GPU cycles).
- **`inference.WebApp`** — defines the public HTTP surface via FastAPI-style decorators
  (`inference.post/get/put/delete(path, …)`). Endpoints are always `async`.
- **Builtin web apps** — mount `frameworks.inference.builtin_webapps.jobs_app` (background-job
  poll/cancel: `GET /jobs/result/{id}`, `PUT /jobs/cancel/{id}`) and `storage_app`
  (`POST /v2/storage/{image,document,video,audio,block/*}` uploads returning UUIDs) for free.

## Declaring dependencies between workers

A worker/webapp declares a handle **as a class attribute**:
`nsfw = inference.depends_on.worker_handle(nsfw_v1)`. The framework then guarantees the dependency is
deployed, gives typed `self.nsfw.api.Input/Output`, and handles network/serialization/retries. Call it
with **`submit(...)`** from a regular `def execute` or **`submit_from_el(...)`** (awaited) from an
`async def execute` or any webapp endpoint. Two modes: **`immediate`** (wait for the answer) or
**`background`** (returns a `BackgroundJob` immediately; long jobs; supports `on_complete=` and
`on_store_result=` callbacks — the latter useful to push big binaries to S3 and store only a URL).

## Typed request/response

- **`inference.Binary`** — for any field holding raw bytes (image/audio/PDF/weights). Sent
  **side-by-side with the JSON** as multipart (like a file upload) instead of base64-in-JSON,
  avoiding ~33% inflation + encode/decode cost. Fields: `value: bytes`, `metadata: dict`.
- **`inference.Tensor`** — alias for `torch.Tensor` when torch is installed; a stub otherwise, so API
  modules import cleanly without the ~1 GB torch dependency. Torch is only needed on the pod that
  actually runs the worker.

## The three run modes (same code, different topology)

| | `initialize()` — prototyping | `serve()` — cloud-like local | `python -m frameworks.inference` — prod pods |
|---|---|---|---|
| Where | laptop, 1 process | laptop, N processes | k8s cluster, N pods |
| Worker→worker | in-process function call | **Redis queue** | **Redis queue** |
| Webapp front door | FastAPI app you mount | real HTTP localhost | HTTP via k8s Service |
| Redis | none | local (managed) | managed Redis cluster |
| GPU isolation | shared CUDA context | per-process `CUDA_VISIBLE_DEVICES` | per-pod GPU |
| Restart on crash | no (all down) | yes (supervisor) | yes (k8s) |

`serve()` is the key middle rung: it exercises the **exact same runtime code path** as production
(real `RedisWorkerHandle`/`HttpWorkerHandle`, FastAPI, task submitter — not mocks), just on your
laptop. A **mixed** mode (`dev.remote_execution`) lets you run most of the graph locally while
delegating one heavy worker to a remote HTTP endpoint (`HttpWorkerHandle`, immediate mode only).

`python -m frameworks.inference` is also **how each container process boots in production** — the
subcommands `workers`, `webapps`, `watchdog`, `dashboard` are the pod entrypoints. `ServeConfig`
(`xpu_requirement`, `num_processes`) declares per-worker hardware and replica count; Redis queue
distribution load-balances across processes.

## Configuration

`InferenceFrameworkConfig` (pydantic) covers `Supervisor` (status port 8001 / metrics 8002),
`Redis`, `S3`, `Metrics`/`Newrelic`, `Background` (watchdog cadence, job config, concurrency limiter,
backpressure), `Logging` (default/json/splunk_text), plus `Development`/`Debug`/`Experimental`
(worker warming + KEDA scale-to-zero flags). Register per-module defaults via `RegisterDefaultConfig`.
Secrets use `{_env: VAR}` substitution in runtime config, resolved before pydantic validation.

## Migration API (temporary Adobe-service wrappers)

`frameworks.inference.migration.*` (install `frameworks.inference[migration]`) wraps external Adobe
services with a clean V3 API while the implementation still lives in Colligo V2 (vendored under
`_private/colligo/`, manually synced). Covers **CAI** (C2PA signing, Linux-only), **IMS** (auth),
**Business Kit** (authorization + credit metering), **Object Store** (session KV, memory/S3), **ACP**
(Creative Cloud assets), **Temp Storage** (S3/Azure blobs + presigned URLs + block upload),
**Metrics**. Explicitly unstable; graduates to `frameworks.inference.*` once stable.

## FLUX reference sample

Sample 4 decomposes FLUX.1-schnell into CLIP encoder (~1 GB), T5-XXL (~10 GB, `num_processes=2`),
denoiser (~25 GB), VAE (~1 GB), and a CPU pipeline that calls CLIP+T5 in parallel via
`asyncio.gather` + `submit_from_el`. Illustrates why you'd split a model that fits on one GPU:
**independent scaling, right-sized GPUs, no single bottleneck.** Run local via `run_local.py`,
distributed via `run_distributed.py` (Swagger at `localhost:8000/docs`).

## Related

- [[wiki/entities/ai-platform-repo]] — the repo this framework ships from
- [[wiki/concepts/v3-deployment]] — how a bound app becomes an Ethos deployment
- [[wiki/concepts/v3-vs-v2]] — mapping to the V2 worker/SDK API
- [[wiki/concepts/colligo-inference]] — the V2 (Rhode) framework, whose internals V3 vendors
- [[wiki/concepts/colligo-inference-sdk]] — V2 client SDK
- [[wiki/concepts/colligo-managed-services]] — the ecosystem where samples 5–10 add build/deploy
- [[wiki/sources/ai-platform-repo-ingest]]
