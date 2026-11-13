---
document_type: landing
children:
    - ./deployment/index.md
    - ./changelog.md
    - [../README.md, "Internal"]
---

# Inference Platform

```{note}
<div style="display:flex;gap:8px;margin:4px 0;justify-content:center">
<a href="https://docs.ai.corp.adobe.com/v3/frameworks/inference/serve/aidoc/index.html" style="background:#f0f0f0;color:#666;padding:4px 12px;border-radius:4px;font-size:0.85em;text-decoration:none">Framework</a>
<span style="background:#1a73e8;color:#fff;padding:4px 12px;border-radius:4px;font-size:0.85em"><b>Platform</b></span>
<a href="https://docs.ai.corp.adobe.com/managed_services/README.html" style="background:#f0f0f0;color:#666;padding:4px 12px;border-radius:4px;font-size:0.85em;text-decoration:none">Managed Services</a>
</div>

Start here for the big picture: architecture overview, deployment paths, sample progression, and v2 → v3 migration status.
Build inference services with the [Inference Framework](/frameworks/inference/serve/aidoc/index.md). Develop and deploy through [Managed Services](https://docs.ai.corp.adobe.com/managed_services/README.html).
Many topics are still in the [v2 docs](https://docs.ai.corp.adobe.com/aidoc/inference-platform/index.html) — see {ref}`v2 → v3 status <v2-bridge>` below.
```

The Inference Platform provides a complete solution for deploying machine learning inference services at Adobe. It includes Bazel-based build infrastructure, Kubernetes deployment automation, and integration with the [Inference Framework](/frameworks/inference/serve/aidoc/index.md).

## Architecture

### Layers

The inference stack has three layers. Your code sits on top; how you deploy is your choice.

```{figure} ./svg/layers.svg
:width: 60%
:align: center
```

### Runtime communication

Regardless of deployment path, the runtime architecture looks the same. Workers communicate via Redis task queues:

```{figure} ./svg/runtime.svg
:width: 70%
:align: center
```

```{note}
**Topology is flexible:** For GPU efficiency, multiple workers can share a single pod (multi-process). On Pluto, everything runs on a single node. Pipeline workers can be collocated with compute workers. The user's code stays the same regardless of topology.
```

## Deployment Paths

The framework is a standalone wheel — how you deploy is your choice.

| Path | What you get | When to use |
|------|-------------|-------------|
| **Managed Services** (recommended) | CI/CD, Bazel builds, Docker packaging, k8s deployment via Argo, autoscaling, observability. Platform-managed GPU [capacity planning](https://docs.ai.corp.adobe.com/aidoc/inference-platform/caplan/index.html). | Production services. Abstracts away significant cloud and organizational complexity. |
| **Self-managed k8s** | Full control, no restrictions | You have specific infrastructure requirements that managed services cannot accommodate. You own all cloud components. Customer-facing services use [Ethos](https://devhome.corp.adobe.com/) clusters. |
| **Pluto** (compute platform) | Quick GPU access, no deployment overhead | Quick demos, sharing an endpoint with a PM for a few hours/days, prototyping when everything fits on one node. See [Pluto docs](https://docs.ai.corp.adobe.com/pylibs/colligo/pluto/aidoc/index.html). |

```{note}
**Self-managed k8s:** Kubernetes clusters that serve user traffic at Adobe are provisioned by [Ethos](https://devhome.corp.adobe.com/), with usage charged back to your org. High-end GPUs (Ampere 80 GB and above) require separate finance approval for your org's allocation. Both the inference platform ([capacity management](https://docs.ai.corp.adobe.com/aidoc/inference-platform/caplan/index.html)) and the compute platform / Pluto ([capacity management](https://docs.ai.corp.adobe.com/pylibs/colligo/pluto/aidoc/compute-cap.html)) handle GPU capacity planning at the platform level, which is more efficient than individual orgs negotiating their own allocations.
```

The managed services path also supports a **quick-deploy escape hatch** (Sample 10) for cutting-edge deps or rapid prototyping, where you skip Bazel/CI and bring your own Docker image.

## Sample Progression

A curated learning path from framework basics to production deployment. Samples 1–4 use the framework only and work with any deployment path. Samples 5–10 are specific to the managed services ecosystem.

| # | Name | Location | What you learn |
|---|------|----------|----------------|
| 1 | [Basic worker](https://docs.ai.corp.adobe.com/v3/frameworks/inference/serve/aidoc/samples/index.html) | Framework | Compute worker, sync execute, local run |
| 2 | [Async patterns](https://docs.ai.corp.adobe.com/v3/frameworks/inference/serve/aidoc/samples/index.html) | Framework | async def execute/load, sync/async calling matrix |
| 3 | [Background jobs](https://docs.ai.corp.adobe.com/v3/frameworks/inference/serve/aidoc/samples/index.html) | Framework | Resilient async, job status, cancellation |
| 4 | [Multi-GPU pipeline (FLUX)](https://docs.ai.corp.adobe.com/v3/frameworks/inference/serve/samples/flux/README.html) | Framework | Pipeline decomposition, num_processes, GPU placement |
| 5 | [Worker in managed services](https://docs.ai.corp.adobe.com/managed_services/services/samples/A/README.html) | Managed Services | stub/impl split, BUILD files, `smake worker`, bazel test |
| 6 | [Pipeline in managed services](https://docs.ai.corp.adobe.com/managed_services/services/samples/B/README.html) | Managed Services | Pipeline deps, visibility rules |
| 7 | [Web app in managed services](https://docs.ai.corp.adobe.com/managed_services/services/samples/C/README.html) | Managed Services | WebApp, FastAPI endpoints, `smake webapp` |
| 8 | [Package & deploy](https://docs.ai.corp.adobe.com/managed_services/services/samples/D/README.html) | Managed Services | `inference_application`, `ethos_deployment`, Argo CD, k8s |
| 9 | [Production service (FLUX)](https://docs.ai.corp.adobe.com/managed_services/services/samples/E/README.html) | Managed Services | Full FLUX in managed services, BKS, CAI, remote exec |
| 10 | [Quick deploy escape hatch](https://docs.ai.corp.adobe.com/managed_services/services/samples/F/README.html) | Managed Services | Detached app, custom deps, no CI |

## Deployment Types

The [Deployment API](./deployment/index.md) supports two main deployment types within an inference application:

- **Worker deployments** — GPU or CPU pods running compute/pipeline workers
- **HTTP server deployments** — CPU pods serving web applications (FastAPI)

See the [Deployment API](./deployment/index.md) for full configuration details including GPU options (Ampere/Hopper), autoscaling, and environment setup.

## Why v3?

- **Use the framework without the monorepo** — In v2, building an inference service required checking out the full colligo repo and using its custom build system. In v3, the framework is `pip install frameworks.inference` — you can prototype on your laptop, a Pluto node, or anywhere Python runs.
- **Your code stays yours** — In v2, user code and platform code lived side by side, making it hard to tell what you own vs what the platform manages. In v3, your code lives in managed services, platform components are consumed as versioned dependencies, and you can't accidentally break (or get broken by) platform internals.
- **One workflow for build and deploy** — In v2, building was in colligo and deploying was in a separate repo (colligo-deploy) with its own tooling. In v3, a single BUILD file defines your application and its deployment — `inference_application` + `ethos_deployment` in the same place.
- **Learn incrementally** — In v2, the learning curve was steep because everything was coupled. In v3, you can start with just the framework (samples 1–4), then add managed services when you're ready to deploy (samples 5–10).

(v2-bridge)=
## v2 → v3 Migration Status

v2 is the stable and recommended path. v3 is in active development. Many v2 docs still apply to v3, either fully or partially. Until v3 is the sole path, not all v2 documentation has been migrated.

Refer to the [v2 docs](https://docs.ai.corp.adobe.com/aidoc/inference-platform/index.html) for topics not yet covered here.

| Topic | Status in v3 |
|-------|-------------|
| Worker API, pipeline API, web app API | **New in v3** — see [framework docs](/frameworks/inference/serve/aidoc/index.md) |
| Build system (Bazel vs custom) | **New in v3** — see [managed services docs](https://docs.ai.corp.adobe.com/managed_services/README.html) |
| Deployment (ethos_deployment vs colligo-deploy) | **New in v3** — see [Deployment API](./deployment/index.md) |
| Autoscaling, scale-to-zero | **Still in v2 docs** — concepts apply |
| Capacity management | **Still in v2 docs** — fully applies |
| Observability (Grafana, Splunk, Prometheus) | **Still in v2 docs** — fully applies |
| Alerts, monitoring | **Still in v2 docs** — fully applies |
| Troubleshooting, support channels | **Still in v2 docs** — fully applies |

## FAQ

**Q: Do all workers run on one instance?**
No. By default, each worker runs as a separate pod in Kubernetes. They communicate via Redis task queues. The pipeline worker orchestrates calls to compute workers.

**Q: What does Bazel have to do with inference?**
Bazel is the build system for managed services only. It auto-generates BUILD files, builds Docker images, and packages deployments. The inference framework itself is just `pip install frameworks.inference`.

**Q: Can I use the framework without managed services?**
Yes. `pip install frameworks.inference`, build your own Docker image, deploy however you want. The framework does not depend on managed services. See the [framework docs](/frameworks/inference/serve/aidoc/index.md).

**Q: How is v3 different from v2?**
Framework and platform are now separated. The framework is a standalone wheel. Managed services replaces the v2 pattern where framework, build system, and deployment were all intertwined in the same repo (colligo + colligo-deploy).

**Q: Where are the v2 docs for topic X?**
Most v2 docs still apply. See the {ref}`v2 → v3 migration table <v2-bridge>` above.

## Quick Links

| Resource | Description |
|----------|-------------|
| [Managed Services README](https://docs.ai.corp.adobe.com/managed_services/README.html) | Getting started with managed services in colligo |
| [Deployment API](./deployment/index.md) | Bazel APIs for packaging and deploying applications |
| [Inference Framework](/frameworks/inference/serve/aidoc/index.md) | Python framework for workers and web apps |
| [Model Hub](/models/aidoc/index.md) | Model packaging and distribution |

## Support

Follow the same [support section in the v2 docs](https://docs.ai.corp.adobe.com/aidoc/inference-platform/support/index.html).
