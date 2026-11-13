---
type: concept
title: V3 Deployment (Bazel → Argo CD → Ethos)
tags: [ai-platform, v3, deployment, bazel, argocd, ethos, gitops, autoscaling, firefly]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/ai-platform/platforms/inference/aidoc/deployment/index.md]]", "[[raw/ai-platform/platforms/inference/aidoc/deployment/gitops-framework.md]]", "[[raw/ai-platform/platforms/inference/aidoc/deployment/inference-chart.md]]", "[[raw/ai-platform/platforms/inference/aidoc/internal/dev-workflows.md]]", "[[raw/ai-platform/platforms/inference/aidoc/bazel_101.md]]", "[[raw/ai-platform/frameworks/inference/serve/samples/a_basic/scripts/C_cloud_run.md]]"]
---

# V3 Deployment (Bazel → Argo CD → Ethos)

How a [[wiki/entities/ai-platform-repo|V3]] model goes from code to a live endpoint. The deployment
machinery is the `@platforms_inference` **Bazel module** built from `platforms/inference/`; users
drive it from **`colligo/managed_services`** (see [[wiki/concepts/colligo-managed-services]]). It
replaces the V2 `colligo-deploy` + Helm rendering pipeline: composition is declared explicitly in
BUILD files, renders in **1–2 s** (vs 30–60 s), and the rendered k8s manifests are **visible in the
PR diff before merge**.

## Deployment paths (pick one)

| Path | What you get | When |
|---|---|---|
| **Managed Services** (recommended) | CI/CD, Bazel builds, Docker packaging, Argo k8s deploy, autoscaling, observability, platform GPU capacity planning | production services |
| **Self-managed k8s** | full control, you own all cloud components (Ethos for customer traffic) | special infra needs |
| **[[wiki/entities/pluto|Pluto]]** | quick GPU access, no deploy overhead | demos, sharing an endpoint for hours/days, single-node prototyping |

Regardless of path the **runtime is identical**: workers talk over Redis task queues; a web server
fronts pipeline workers; topology (which workers share a pod) is flexible and does not change user
code. Deploying yourself means manually running the pod entrypoints (`python -m frameworks.inference
webapps/workers/watchdog/dashboard --config …`) + a Redis cluster + an ingress; managed services does
all of it.

## The two Bazel rules

Load both from `@platforms_inference//:defs.bzl`.

1. **`inference_application(name, roots=[…], deps=[…])`** — packages an app: builds the Docker image,
   walks the worker/webapp dependency graph from `roots` (worker/webapp refs, incl. builtin webapps),
   and emits a metadata JSON. Lives in the app's `BUILD`.
2. **`ethos_deployment(name, ethos_runtime_env, python_charts=[…], chart_values=[…])`** — the main way
   to deploy *anything* to Ethos (not inference-specific). Takes charts (Helm/Python) and/or raw YAML
   + the runtime-env defaults (image-pull secrets, IAM role, Redis host, RBAC) and renders them into a
   single `k8s_manifest.yaml`.

**Conventional layout** — one BUILD per environment, one `ethos_deployment` per target cluster:

```
services/samples/E/deploys/imaging/
├── BUILD                       # inference_application(...) — builds the image
├── dev/{BUILD, values.inference.yaml}     # one ethos_deployment for the dev cluster
└── stage/{BUILD, values.inference.yaml}
```

There is **no wildcard**: shipping to N prod clusters = N `ethos_deployment` calls. Every
`ethos_deployment` must be registered in the root **`argo_sync(...)`** rule — `smake lint` does this
via the `# gazelle:argo_sync_rule` directive; forget it and the target builds but never syncs (a
classic first-time failure).

## The GitOps flow (code → endpoint)

```
edit code → smake lint/argo-sync renders k8s_manifest.yaml
   → argo_sync(...) copies it into the repo's cloud/ folder
   → merge PR to managed_services main
   → CI syncs cloud/ manifests to the deploy repo (colligo-v3-deploy)
   → Argo CD watches cloud/ and applies → app updates in Kubernetes (no kubectl)
```

Merge a PR → `cloud/` updates → Argo CD reconciles → your app updates. Platform developers can
short-circuit this for pre-merge testing via **test-environment branches** in `.ethos.yaml` (the
Ethos provisioner watches a `chart_path` on a branch), pushing manually built/pushed images + rendered
manifests to e.g. the `test_env` branch.

## Runtime envs (cluster + env + infra defaults)

`ethos_runtime_env` selects the cluster + environment + baked-in infra defaults, referenced as
`@platforms_inference//:<name>` (e.g. `ethos851-dev-or2`, `ethos851-prod-or2`, `ethos852-prod-va6`).
The authoritative list is `platforms/inference/ethos/runtime_envs/BUILD`. Notable: **dev shares a
physical cluster with stage** (`ethos851-dev-or2` == `ethos851-stage-or2`, differing only by
namespace/env labels). RBAC groups: `firefly_dev_rbac` (dev/stage) / `firefly_prod_rbac` (prod).

## The inference chart (`ai-inference-chart`)

Successor to the V2 **rhode** chart. Its `InferenceValues` (`values.inference.yaml`) drives one app
into multiple k8s deployments. Key deployment types keyed by arbitrary pod name in `deployments`:

- **`WorkerDeployment`** — GPU/CPU pods running compute/pipeline workers. `processes: {worker_ref: n}`
  injects `num_processes` per worker; one pod can run multiple workers (GPU sharing) via a custom
  pod name.
- **`HttpServerDeployment`** — CPU pods serving web apps (`serves: [webapp refs]`, port 8000).
- **`WatchdogDeployment`** — singleton CPU pod monitoring background-job queues (restarts
  abandoned/timed-out jobs).

Hardware: CPU (`small/medium/large/xlarge`) or GPU (`ampere_40gb / ampere_80gb / hopper_80gb /
hopper_140gb`, 1/2/4/8 GPUs). GPU pods auto-mount a **3 GiB/GPU `/dev/shm`** (vLLM/NCCL/torch need it).

**Autoscaling** (GPU): **Oshiya** prediction-based scaling (on by default), optionally + queue-based
HPA (Prometheus queue-length metric) + **KEDA scale-to-zero** (needs `enable_worker_warming: true` +
`check_worker_before_call: false`; `idle_replica_count: 0`, cooldown ≤ 4 h). CPU workers: queue-based
HPA. `replicas` and autoscaling are mutually exclusive; unset + no autoscaling ⇒ 0 (deployment
skipped).

**Ingress:** `public_ingress` (.ff.adobe.io, manual SRE DNS), `development_ingress` (corp/Laser/Ethos
IPs, auth disabled), `public_async_ingress` (for `/jobs/` background polling; auto-injects
`async_endpoint_url`), `custom_ingress` (user domains, optional auto-DNS). Standalone
`ai-ingress-chart` also exists. Two **agent charts** (`claude-agent-sdk-chart` single-pod,
`langgraph-chart` apiServer+queue+Postgres+Redis) plug into `ethos_deployment` for `frameworks.agent`
LLM agents.

## Release / versioning

The framework wheel **and** the inference chart share **one version**, released together via a git
tag **`release/inference/vX.Y.Z`**. Pushing the tag makes CI publish the wheel + chart. To adopt a
version, `colligo/managed_services/MODULE.bazel` sets a `git_override(module_name =
"platforms_inference", tag = "release/inference/vX.Y.Z")` and `./make lint` re-locks
`requirements.*.txt` to the matching wheel. Dev charts can be published from a PR (label
`publish-inference-chart` → `0.dev<PR>+sha.<SHA>`). Latest at ingest: **v0.5.11 (2026-06-26)** — still
0.x / pre-1.0.

## Related

- [[wiki/entities/ai-platform-repo]] — where the `@platforms_inference` module is built
- [[wiki/concepts/v3-inference-framework]] — the app being deployed
- [[wiki/concepts/colligo-managed-services]] — the ecosystem (in colligo) that drives these rules
- [[wiki/concepts/colligo-inference-infra]] — V2 Ethos/gateway/autoscaling infra this succeeds
- [[wiki/concepts/v3-vs-v2]] — colligo-deploy → ethos_deployment mapping
- [[wiki/sources/ai-platform-repo-ingest]]
