---
type: concept
title: V3 vs V2 (inference) + migration
tags: [ai-platform, v3, v2, colligo, inference, migration, comparison, firefly]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/ai-platform/platforms/inference/aidoc/index.md]]", "[[raw/ai-platform/frameworks/inference/serve/README.md]]", "[[raw/ai-platform/frameworks/inference/serve/migration/README.md]]", "[[raw/ai-platform/platforms/inference/aidoc/internal/dev-workflows.md]]"]
---

# V3 vs V2 (inference) + migration

How the [[wiki/entities/ai-platform-repo|V3 stack]] differs from the [[wiki/concepts/colligo-inference|Colligo V2 (Rhode) serving platform]], and the migration path. The one-sentence framing from the docs: **framework and platform are now separated** — the framework is a standalone wheel, and "managed services" replaces the V2 pattern where framework, build system, and deployment were all intertwined in one repo (colligo + colligo-deploy).

## Why V3 (per the platform docs)

- **Use the framework without the monorepo.** V2 required checking out all of Colligo + its custom build system. V3 is `pip install frameworks.inference` — prototype on a laptop / Pluto node / anywhere.
- **Your code stays yours.** V2 mixed user code and platform code side by side. V3: your code lives in managed services; platform components are **versioned dependencies** you can't accidentally break (or be broken by).
- **One workflow for build + deploy.** V2 built in colligo and deployed in a separate repo (colligo-deploy) with its own tooling. V3: a single BUILD file defines the app *and* its deployment (`inference_application` + `ethos_deployment`).
- **Learn incrementally.** Start with just the framework (samples 1–4), add managed services when ready to deploy (samples 5–10).

## Concept mapping

| V2 (Colligo) | V3 (ai-platform) |
|---|---|
| `ColligoMLModel` worker + `build.deploy_worker(...)` | `inference.Worker` + `.bind()` ([[wiki/concepts/v3-inference-framework]]) |
| `build.application(...)` in `models/build/apps/` | `inference_application(roots=…)` Bazel rule |
| Custom `./m` monorepo build | **Bazel** (`@platforms_inference` module) |
| `colligo-deploy` + Helm rendering (rhode chart) | `ethos_deployment(...)` + `ai-inference-chart` ([[wiki/concepts/v3-deployment]]) |
| `DeployInfo` / `RhodeOptions` | `ServeConfig` (`xpu_requirement`, `num_processes`) |
| Inference SDK in `pylibs/colligo/sdk` | framework's own `WorkerHandle` / `HttpWorkerHandle`; migration wrappers |
| BKS/CAI/IMS/temp-storage via global config | `frameworks.inference.migration.*` (temporary clean wrappers) |
| user code in `models/` tree | user code in `colligo/managed_services/services/<team>/<project>/` |

## What is reused (V3 is built *on* V2 internals)

V3 is not a from-scratch rewrite of the runtime. The framework **vendors** proven V2 code
(multiprocess communication, Redis queues, logging formatters) under
`frameworks/inference/serve/_private/colligo/`, and a **shim layer** (`shims/config_shim.py`,
`task_executor.py`, `task_submitter.py`, `http_server.py`) bridges the clean V3 config to that V2
global state. Likewise the **migration API** wraps external Adobe services whose implementation still
lives in Colligo — changes there do **not** auto-propagate; a manual sync into the vendored tree is
required. So the same runtime architecture (workers over Redis queues, per-process GPU isolation) is
preserved; V3 mostly changes the *packaging, API surface, build, and deploy*.

## Migration status (the reconciliation)

The platform's own "v2 → v3 status" table says **v2 is the stable and recommended path; v3 is in
active development.** New in v3: worker/pipeline/webapp API, Bazel build, `ethos_deployment`. **Still
in v2 docs (fully apply):** autoscaling/scale-to-zero concepts, capacity management, observability
(Grafana/Splunk/Prometheus), alerts, troubleshooting, support channels. Not all v2 docs have been
migrated.

> [!note] Reconciliation with [[wiki/concepts/colligo-managed-services]]
> That page (ingested 2026-07-04 from the **colligo** repo) calls Inference V3 a **"release
> candidate."** The ai-platform docs (2026-07-05) are consistent: V3 is **pre-1.0 / in active
> development** (latest shared framework+chart version **v0.5.11**, 2026-06-26), with V2 still the
> stable production path. Within V3, *managed services* is the recommended deployment path — but V3
> overall has **not** replaced V2 or moved to GA yet. No contradiction; the two pages describe the
> same not-yet-GA status from the consuming (colligo) and producing (ai-platform) sides. Note the
> "V3 stack" now spans **two repos**: the framework + build infra live in **ai-platform**, while the
> `managed_services/` user ecosystem still lives in **colligo**.

## Related

- [[wiki/entities/ai-platform-repo]]
- [[wiki/concepts/v3-inference-framework]] · [[wiki/concepts/v3-deployment]] · [[wiki/concepts/v3-models-hub]]
- [[wiki/concepts/colligo-inference]] — V2 serving platform
- [[wiki/concepts/colligo-inference-infra]] — V2 Ethos/deploy infra
- [[wiki/concepts/colligo-managed-services]] — the managed-services ecosystem (colligo side)
- [[wiki/entities/colligo]] · [[wiki/entities/pluto]]
- [[wiki/sources/ai-platform-repo-ingest]]
