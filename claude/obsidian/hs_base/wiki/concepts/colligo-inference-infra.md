---
type: concept
title: Colligo Inference Infrastructure (serving infra)
tags: [colligo, inference, infra, ethos, kubernetes, autoscaling, slo, argocd, observability, deployment, firefly]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/ai-platform-docs]]"]
---

# Colligo Inference Infrastructure (serving infra)

**How inference actually runs in production** — the Ethos Kubernetes substrate, cluster gateway/
routing, autoscaling, deployment/rollout, SLOs, and observability behind the
[[wiki/concepts/colligo-inference|V2 Inference Platform]] and
[[wiki/concepts/colligo-managed-services|V3 Managed Services]]. Where those pages cover the
*developer-facing framework/API*, this page covers the **`aidoc/inference-platform/infra/`** layer:
the operational plumbing an app rides once it's built.

## Ethos clusters and compute

Serving runs on **Ethos** — Adobe's Kubernetes-based orchestration platform — across three tiers
(dev, staging, production). Concrete cluster inventory:

- **Dev/Stage:** `ethos851-stage-or2` (US West / Oregon, GA); `ethos851-stage-deu6` (Germany, Azure,
  limited availability).
- **Prod (US West / Oregon):** `ethos851-prod-or2` … `ethos855-prod-or2` — six GA clusters.
- **Prod (US East / Virginia):** `ethos851-prod-va6` … `ethos853-prod-va6` — three GA clusters.
- Additional limited-availability prod clusters in Ohio and Germany for regional needs.

**Compute:** CPU nodes host frontend/orchestration/I/O/preprocessing workers; GPUs are NVIDIA **A10**
(24GB, cheap moderate-res, wide availability), **A100** (80GB, large/multi-GPU), and **H100** (80GB,
latest gen, limited availability). Note the docs' V2 infra GPU list (A10/A100/H100) sits below the
newer [[wiki/entities/pluto|Pluto]] *training* GPU tiers (B200/H200/H100/A100) — inference and
training draw from different fleets.

## Gateway, routing, and state

Public requests enter through a **Cluster Gateway** that performs initial routing to worker instances
based on service requirements and load distribution; **ingress** configs (per-app) govern traffic and
network policies. The gateway also mints the signed short-lived WebSocket URLs the
[[wiki/concepts/colligo-inference|V2 framework]] uses for streaming.

Distributed state is split by durability:
- **Redis / MemoryDB** — task queues, worker registry, request caching, session state, rate limiting.
- **S3 + Azure Storage** — content persistence, worker results, pipeline outputs.

The [[wiki/concepts/colligo-inference|framework's]] queues, global rate limiter, and backpressure are
implemented on top of this Redis/MemoryDB layer.

## Capability Registry

A browsable catalog of registered apps and their declared **capabilities**, declared in
`build.application()` (`display_name`, `description`, `capabilities`). Each capability records a
workflow type (e.g. "Text2Image", "GenExtend Video"), the model (e.g. "Clio 4.0 Ultra", "Filix3"),
modality (image/video/audio/text/3D), and dimension bounds (resolution 512–4096, frame rates,
duration 1.0–5.0s, token/sample limits). Filterable by workflow/model/modality/app — powers discovery
and intelligent routing.

## Autoscaling

Autoscaling is primarily a **cost-saving** mechanism; the system tracks traffic across apps/workers
and tunes replica counts against latency and request parallelism. Three strategies:

1. **Prediction-based GPU autoscaling ("Oshiya")** — default for GPU workers on Helm chart ≥
   1.4.825. Forecasts optimal cluster-wide replica counts from historical traffic, favoring
   higher-value apps under contention. Enable `autoScaler: oshiya`; params `minReplicas`/
   `maxReplicas`/`bufferReplicas`. Per-cluster UI e.g.
   `https://oshiya.corp.ethos851-prod-or2.ethos.adobe.net/ui`. Needs ~20 min of observed traffic →
   poor for sudden spikes; high latency variance degrades it.
2. **Queue-Based Scaling (QBS)** — scales on request queue length. Primary for CPU workers
   (`autoScaler: prometheus_rule`), emergency fallback for GPU (opt-in). WebSocket slot utilization =
   `ceil((1 - available_slots/max_slots) * 100)`. Not recommended as the primary GPU strategy
   (single-worker view, ignores cluster-wide allocation).
3. **KEDA scale-to-zero (experimental)** — scales idle workers to zero. Dev/stage available; prod
   needs Init script ≥ 1.16.0 and Rhode Helm chart ≥ 1.4.1925. Enable `autoScaler: oshiya` +
   `kedaEnabled: true`, plus `check_worker_before_call: false`. Prometheus triggers (poll ~10s,
   cooldown ~3600s).

**Cold start:** KEDA workers report phases — 0% init → 20% model loading → 80% warmup → 100% ready;
pipeline workers scale sequentially (~10 min full deploy). The **Warm API** pre-scales and confirms
readiness before prod traffic. Savings are "mostly unrealized" until freed nodes return to shared
pools; early onboarders saw ~25% replica reductions. Key signals:
`usm_object_colligo_queue_requests_in_progress`, `usm_object_colligo_ws_utilization`, CPU/mem,
parallel-request capacity.

## Deployment & rollout

**V2 path — colligo-deploy:** built on **Ethos Flex Helm**. The `colligo-deploy` Git repo (out of the
monorepo, `git.corp.adobe.com/firefly/colligo-deploy`) holds app configs + Helm templates. Flow: YAML
config → Helm render/validate → automation across clusters → rollout. **Worker Groups** logically
cluster compute; per-worker **config hashing** enables targeted/incremental rollouts; **crossfade**
replaces workers with zero service interruption.

**Deployment automation:** triggered by a **comment on the Git PR** (not webhooks; comment format per
app). Promotion dev → staging (`ns-team-colligov2-stage`) → prod (`ns-team-colligov2-prod`).
**ArgoCD** manages declarative app state (GitOps); **Argo Analysis** runs automated **canary**
analysis over progressive traffic steps (typically 25%→50%→75%→100%, ~10-min waits) against YAML
thresholds (error rate, latency, queue depth), auto-aborting/rolling back on violation; **Argo
Workflows** orchestrate.

> [!note] V2 vs V3 deployment
> This ArgoCD/Argo-Analysis/colligo-deploy machinery is the **V2** operational path.
> [[wiki/concepts/colligo-managed-services|Managed Services (V3)]] replaces `colligo-deploy` + Helm
> with in-repo Bazel rules (`inference_application` / `ethos_deployment`) that generate manifests +
> Argo CD config synced automatically — same Ethos clusters, different authoring. Both ultimately
> land on Argo CD.

## SLO framework

Reliability is standardized in the **Adobe-Firefly/firefly-sla** repo — "what 99.x looks like" per
service, measured over 30-day rolling windows. Three numbers: **Compliance** (rolling % meeting
target), **Error Budget Remaining**, **Burn Rate** (× steady-state). Per-endpoint SLIs: Availability
(tiered 99.9/99.5/99% for tier-1/2/3), optional P95 latency, optional 5XX error rate. Error budget =
`(1 - target) × requests` over 30 days; a 2× burn empties the budget in 15 days.

Burn-rate-driven escalation: ≤1× none · >1×–2× ticket · >2× sustained Sev-3 · >6× Sev-2 (block
non-hotfix deploys) · >14× (1h)+>1× (24h) Sev-1 page. Dashboard `firefly-sla.corp.adobe.com`, weekly
owner report, metrics from Prometheus/Cortex + New Relic, GitHub Actions + Nexus alerting. **ORR**
gates: new services / major rewrites must onboard SLOs (self-serve PR, `sla.py validate`) before
taking customer traffic.

## Observability

- **Grafana** — main dashboards: "Colligo V2 Service Metrics" (RPS, error rate, queue length,
  per-worker latency, worker counts, throttling, backpressure), queue-metrics, GPU/CPU/RAM, and "HPA
  & Oshiya" autoscaling. Custom dashboards → **firefly-monitoring** repo; editing needs
  `GRP-FIREFLY-GRAFANA-EDITOR`.
- **New Relic** — supplementary nonprod/prod dashboards; some apps use
  **neuralfiltersplatform/alerting-newrelic**.
- **Splunk** — log aggregation, filter by source, separate nonprod/prod indices.

Custom metrics via the `colligo.base` metrics module. Engineers get default view access; sensitive
data gated by Adobe groups.

## Related

- [[wiki/concepts/colligo-inference]] — the V2 developer-facing framework this infra serves
- [[wiki/concepts/colligo-managed-services]] — V3 (Bazel + Argo CD) deployment authoring
- [[wiki/concepts/colligo-inference-sdk]] — how clients call served workers
- [[wiki/concepts/ai-platform-overview]] — where inference sits in the whole platform
- [[wiki/entities/colligo]] · [[wiki/concepts/colligo-dev-workflow]]
- [[wiki/entities/pluto]] — the training/compute substrate (distinct fleet)
- [[wiki/sources/ai-platform-docs]]
