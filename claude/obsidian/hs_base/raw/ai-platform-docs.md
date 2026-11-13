---
type: raw
title: "AI Platform Docs Portal — Overview & Inference Infrastructure (fetched)"
source: https://docs.ai.corp.adobe.com/
fetched: 2026-07-05
immutable: true
---

# AI Platform Docs Portal — raw capture (2026-07-05)

Provenance: fetched via WebFetch from `https://docs.ai.corp.adobe.com/` and sub-pages on
2026-07-05 by the AI-platform-docs ingest agent. This file is an **immutable** source capture.
Content is summarized/condensed by the fetch model (not byte-for-byte HTML). Sibling agents own
Pluto, the models catalog, and training/Mori; those pages were deliberately NOT captured here.

URLs fetched:
- `https://docs.ai.corp.adobe.com/` — OK (portal map)
- `aidoc/philosophy.html` — OK
- `aidoc/inference-platform/index.html` — OK
- `aidoc/inference-platform/infra/index.html` — OK
- `aidoc/inference-platform/infra/compute.html` — OK
- `aidoc/inference-platform/infra/observability.html` — OK
- `aidoc/inference-platform/infra/auto-scaling.html` — OK
- `aidoc/inference-platform/infra/slo-framework.html` — OK
- `aidoc/inference-platform/infra/colligo-deploy/index.html` — OK
- `aidoc/inference-platform/infra/deployment-automation.html` — OK
- `aidoc/inference-platform/capability-registry.html` — OK
- `aidoc/inference-platform/infra/colligo-deploy/targeted-rollouts.html` — HTTP 403 (skipped)

---

## 1. Portal map (root index)

Platform mission: "facilitate the end-to-end lifecycle of delivering delightful AI experiences to
Adobe's users" — inference, training, and data processing. Platform and components live in the
**Colligo monorepo**.

Top-level sections:
- **Philosophy** — `aidoc/philosophy.html`
- **Compute Platform (Pluto)** — `pylibs/colligo/pluto/aidoc/index.html` (SIBLING/done)
- **Training Framework (Mori)** — `contrib/Mori/aidoc/index.html` (SIBLING)
- **Inference Platform** — `aidoc/inference-platform/index.html` (THIS AGENT)
- **Data Platform** — `aidoc/data-platform/index.html`
- **Monorepo** — `aidoc/monorepo/index.html`
- **Capability Registry** — `aidoc/inference-platform/capability-registry.html`
- **Access Control** — `aidoc/access-control.html`

Engineering practices: Documentation, Code Review, Source Control, Testing, Dependency Management,
Continuous Integration, Static Analysis, Docker Containers (`docker/aidoc/index.html`).

Models & Services: Adobe Research (`models/colligo/models/adobe_research/aidoc/index.html`),
Firefly Foundry Services (`managed_services/services/firefly/foundry/README.html`), specialized
model docs (Florence 2.0, Flux, IP Guard, etc.) — SIBLING owns the models catalog.

## 2. Philosophy

Integrates three historically separate efforts: inference technology (Firefly), data processing for
training, and AI compute infrastructure. Unified components: Compute Platform (Pluto), Training
Framework (Mori), Inference Platform, Data Platform.

Dual code strategy:
- **Short-lived code** (research/prototyping, days–months): lightweight practices, shipped as
  installable packages (pip).
- **Long-lived code** (production): robust SW engineering. Principle: "as the amount of code
  increases, the collective code maintenance overhead should increase sublinearly."

Monorepo rationale: cross-team changes manageable with unified tooling; test all code together to
catch breaking changes (avoid "dependency hell"); uniform build/test/quality standards. Scales
beyond 200 concurrent developers.

## 3. Inference Platform — overview & nav

"A managed platform for serving machine learning models and AI applications efficiently and at
scale." Covers local development → production operations.

Three product areas:
1. **Inference Framework** — worker API, orchestration, queues (FIFO/sticky/priority), durable async
   processing, rate limiting, backpressure, profiling, logging, metrics, service integrations.
2. **Inference Infrastructure** — deployment to Ethos clusters (dev/stage/prod), cloud storage,
   Redis metadata, autoscaling, observability.
3. **Monorepo Developer Experience** — build system, deps, CLI, static analysis, testing, CI.

Full sub-nav:

Inference Framework (`framework/`): API reference, Worker design, Public endpoints, HTTP APIs, GPU
overrides, SDK, Task queues, Global rate limiter, Guest fingerprint checks, Backpressure, Resilient
async pipelines, Multi-task async context, Worker self-healing, Block upload support, Debug UI,
Distributed tracing, External services, WebSocket streaming, SSE streaming, Feature flags.

Inference Infrastructure (`infra/`): Clusters and compute (`compute.html`), Observability
(`observability.html`), SLO framework (`slo-framework.html`), Auto-scaling (`auto-scaling.html`),
Scale-to-zero FAQ (`scale-to-zero-faq.html`), IAM users (`iam_users.html`), IMS client IDs
(`ims-client-ids.html`), Deployments (`colligo-deploy/index.html` + sub-guides: repository access,
code structure, application onboarding, worker groups, PR contributions, Helm chart linting, ingress
configurations, targeted rollouts, crossfade worker replacement), Deployment automation
(`deployment-automation.html`).

Managed Services v3 (`../../managed_services/`): video tutorials, dev guides, sample projects A–G,
tenant pages.

User Guides (`user-guides/`): tutorials (video setup, inference applications, general apps, serving,
vLLM), integration testing, Ethos troubleshooting, alert configuration, Operational Readiness Review
(ORR, automated & manual), capabilities taxonomy, service accounts and IRSA, experimental features,
HX00 timeslicing, corp access, migration guides, ACMP onboarding.

Capacity Planning (`caplan/`): prerequisites, timeline, GPU request process, FAQs, app rightsizing,
Grafana troubleshooting.

Support (`support/`): blog posts and postmortems, newsletter archive, release notes.

## 4. Clusters and Compute (`infra/compute.html` + infra index)

**Ethos** = Adobe's Kubernetes-based orchestration platform hosting inference workloads across
distributed cloud environments. Three environment tiers: dev, staging, production.

Cluster inventory (from compute.html):
- **Dev/Stage:** `ethos851-stage-or2` (US West / Oregon, GA); `ethos851-stage-deu6` (Europe /
  Germany, Azure-based, limited availability).
- **Production (US West / Oregon):** `ethos851-prod-or2` through `ethos855-prod-or2` (six clusters,
  all GA).
- **Production (US East / Virginia):** `ethos851-prod-va6` through `ethos853-prod-va6` (three
  clusters, all GA).
- Additional limited-availability prod clusters in Ohio and Germany for regional needs.

Request flow: requests traverse a **Cluster Gateway** component that performs initial routing,
directing traffic to appropriate worker instances based on service requirements and load
distribution. (The Cluster Gateway also mints signed short-lived WebSocket URLs — cross-ref V2
inference framework.) Ingress configs control traffic routing with network policies.

Compute resources:
- **CPU nodes** — frontend workers, orchestration, I/O, preprocessing.
- **GPU options:** NVIDIA A10 (24GB, cost-effective moderate-res, wide availability); NVIDIA A100
  (80GB, large models / multi-GPU); NVIDIA H100 (80GB, latest gen, limited availability).

Data infrastructure:
- **Redis / MemoryDB** — task queues, worker registry, request caching, session state, rate
  limiting.
- **S3 and Azure Storage** — content persistence, worker results, pipeline outputs.
- Multi-region deployment capability.

## 5. Observability (`infra/observability.html`)

Three primary tools:
- **Grafana** — main dashboards. Standard dashboards: "Colligo V2 Service Metrics" (RPS, error
  rates, queue length, latency per worker, worker counts, throttling, backpressure); dedicated queue
  metrics dashboard; GPU/CPU/RAM usage dashboards; "HPA & Oshiya" autoscaling dashboard. Teams
  contribute custom dashboards to the **firefly-monitoring** repo. Editing requires the
  `GRP-FIREFLY-GRAFANA-EDITOR` group.
- **New Relic** — supplementary nonprod & prod dashboards; some apps keep custom dashboards in the
  **neuralfiltersplatform/alerting-newrelic** repo.
- **Splunk** — aggregates inference logs across environments; filter by source to isolate apps/
  workers; separate indices for nonprod and prod.

Metrics: request throughput, error rates, queue behavior, latency distributions, resource
utilization (GPU/CPU/RAM), autoscaling decisions. Custom metrics via the `colligo.base` metrics
module. Engineers get default dashboard view access; sensitive data gated by Adobe access groups.

## 6. Auto-scaling (`infra/auto-scaling.html`)

Primarily a cost-saving mechanism. Tracks traffic across all apps/workers; analyzes latency and
request parallelism to optimize replica counts. Three approaches:

1. **GPU Worker Autoscaling (prediction-based, "Oshiya")** — default for GPU workers on chart
   version ≥ 1.4.825. Uses historical traffic to forecast optimal replica counts cluster-wide,
   favoring higher-value apps during contention. Enable via `autoScaler: oshiya`. Params:
   `minReplicas`, `maxReplicas`, `bufferReplicas`. Central "HPA & Oshiya Autoscaling Dashboard";
   per-cluster UI e.g. `https://oshiya.corp.ethos851-prod-or2.ethos.adobe.net/ui`. Needs ~20 min of
   traffic observation before accurate predictions; unsuitable for sudden spikes; high latency
   variance degrades decisions.

2. **Queue-Based Scaling (QBS)** — simpler; scales on request queue length. Primary for CPU workers,
   emergency fallback for GPU. CPU: enable `autoScaler: prometheus_rule`; monitors queue depth +
   resource utilization; WebSocket slot utilization = `ceil((1 - (available_slots / max_slots)) *
   100)`; configurable scale-up/down periods and stabilization windows. GPU: disabled by default,
   opt-in; runs alongside prediction-based as emergency scaling; not recommended as primary
   (single-worker focus, ignores cluster-wide allocation).

3. **KEDA-based (experimental scale-to-zero)** — scale to zero during idle. Dev/stage available;
   prod requires Init script ≥ 1.16.0 and Rhode Helm chart ≥ 1.4.1925. Enable `autoScaler: oshiya`
   + `kedaEnabled: true`; requires `check_worker_before_call: false` in config commons; Prometheus
   triggers, polling default 10s, cooldown default 3600s; custom metric queries for activation.

Metrics/signals: request latency & variance; queue depth (`usm_object_colligo_queue_requests_in_progress`);
WebSocket slot utilization (`usm_object_colligo_ws_utilization`); CPU/memory utilization; parallel
request capacity.

Cold start: KEDA workers report progress phases — 0% init, 20% model loading, 80% warmup, 100%
ready. Pipeline workers scale up sequentially (~10 min for full deploy). **Warm API** allows
proactive pre-scaling and readiness monitoring before directing prod traffic.

Cost impact: idle-period capacity reduced, but savings "mostly unrealized" until infra releases
unused nodes to other pools. Initial prod deployments hit ~25% replica-count reductions during
onboarding.

## 7. SLO Framework (`infra/slo-framework.html`)

Standardizes reliability measurement for Firefly inference services. Definitions of "what 99.x looks
like" live in a single repo: **Adobe-Firefly/firefly-sla**. Continuous measurement over 30-day
rolling windows.

Three primary numbers per service:
1. **Compliance** — rolling 30-day % of requests meeting SLO target (typically 99.9% for tier-1).
2. **Error Budget Remaining** — allowable "bad" behavior not yet consumed.
3. **Burn Rate** — how fast budget is consumed vs steady-state (multiples of 1×).

SLI/SLO dimensions per endpoint:
- **Availability** — primary target, tier-dependent: 99.9% (tier-1), 99.5% (tier-2), 99% (tier-3).
- **Latency** — optional P95 threshold (seconds).
- **Error Rate** — optional 5XX rate threshold.

Config: JSON templates specifying `service.tier`, endpoint paths, per-endpoint SLO targets. Error
budget = `(1 - target%) × measured_requests` over 30 days. Burn rate: 2× depletes 30-day budget in
15 days.

Alert routing by burn-rate threshold:
- ≤1× — no action.
- >1× and ≤2× — track/open ticket.
- >2× sustained — Sev-3, engage owner.
- >6× — Sev-2, block non-hotfix deploys.
- >14× (1h) AND >1× (24h) — Sev-1, page on-call.

Budget-driven and policy-scaled (distinct from symptom-driven alerts). ORR integration: new services
/ major rewrites must onboard to the SLO framework via self-serve PR before taking customer traffic;
ORR gates launch on SLO maturity. Live dashboard: `https://firefly-sla.corp.adobe.com/`. Weekly
automated report to owners (Monday AM). Metrics from Prometheus/Cortex + New Relic. GitHub Actions
power metric fetching + Nexus alerting. Onboarding: copy template, fill placeholders, validate with
`sla.py validate`, merge; appears in dashboard ~30 min post-merge.

## 8. Deployments — colligo-deploy (`infra/colligo-deploy/index.html`)

"Colligo deploy project is designed for easy deployment of Colligo applications, being built on top
of Ethos Flex helm deployment." Primary V2 deployment mechanism.

Elements:
- **Deployment repository** — the `colligo-deploy` Git repo holds all deployment configs + app
  specs. (Cross-ref: repo at `git.corp.adobe.com/firefly/colligo-deploy`, moved out of monorepo.)
- **Code organization** — structured folders for app configs + Helm chart templates.
- **Application deployment flow** — YAML config submission → Helm chart rendering & validation →
  deployment automation across cluster environments → rollout orchestration.
- **Worker management** — Worker Groups (logical clustering of compute); per-worker config hashing
  for targeted, incremental rollouts; **crossfade** rollout for worker replacement without service
  interruption.
- **Network configuration** — ingress configs control routing with network policies.

Sub-pages: repository access, code structure, application onboarding, worker group configuration,
Helm chart linting, ingress setup, advanced rollout strategies (targeted rollouts — 403 when
fetched), deployment automation.

## 9. Deployment Automation (`infra/deployment-automation.html`)

Two core functions: canary-analysis monitoring during rollout, and Git-based deployment triggering
via PR comments.

- **Triggering** — add a comment on the appropriate Git PR (comment format varies by app, documented
  in the Deployment Automation Commands wiki). Not webhook-based.
- **Promotion flow** — dev → staging → production. Namespaces: staging `ns-team-colligov2-stage`,
  production `ns-team-colligov2-prod`. Both environments visible in ArgoCD.
- **GitOps** — **ArgoCD** manages app deployment state; apps declaratively defined and synced;
  ArgoCD UI for inspection/status.
- **Config** — YAML app settings define metrics thresholds (error rates, latency, queue depth),
  canary traffic steps (typically 25% → 50% → 75% → 100%), analysis intervals (~10-min waits).
  "Define what 'healthy' means" → drives canary analysis + automatic rollback.
- **Automated canary analysis** — **Argo Analysis** runs during progressive rollout; threshold
  violations auto-abort/rollback without manual intervention. **Argo Workflows** orchestrate the
  process.

## 10. Capability Registry (`capability-registry.html`)

A browsable catalog of registered inference apps and their declared capabilities. A **capability** =
a specific task/service an app can perform (e.g. text-to-image, audio separation).

Declared via `build.application()` with `display_name`, `description`, `capabilities`. Each
capability declaration includes:
- **Workflow type** (e.g. "Text2Image", "GenExtend Video")
- **Model used** (e.g. "Clio 4.0 Ultra", "Filix3")
- **Modality** (image / video / audio / text / 3D)
- **Dimension details**: resolution bounds (e.g. 512–4096), frame rates (24, 30 FPS), duration
  limits (1.0–5.0s), token limits (text), sample rates (audio).

Registry supports filtering by workflow / model / modality / app name — taxonomy-driven discovery
(e.g. find all apps supporting "Text2Image" with "Clio 3"). Metadata facilitates intelligent routing
decisions and shows what's available with operational constraints.
