# Inference Overview

The big picture for Foundry inference: what we serve, how it's structured, and the v2/v3 split. Once you know which slice of the system you care about, use the router at the bottom to land in the right detail doc.

> [!TIP]
> **Related docs — inference:**
> | When you need... | See |
> |---|---|
> | Build a new service (v3 / managed services / standalone apps) | [Inference Services — v3 (in colligo)](https://github.com/Adobe-Firefly/colligo/blob/main/managed_services/services/firefly/foundry/aidoc/inference-services-v3.md) |
> | Operate or change the v2 service (gen-foundry) | [Inference Services — v2](inference-services-v2.md) |
> | Day-to-day ops, alerts, deployment steps for gen-foundry | [Gen-Foundry Runbook](gen-foundry-runbook.md) |
> | API auth layers and customer allowlisting | [Gen-Foundry Auth & Allowlisting](gen-foundry-auth-allowlisting.md) |
>
> **Related docs — cross-cutting:**
> | When you need... | See |
> |---|---|
> | Cloud credentials, S3 bucket setup, auth | [Cloud Resources and Access](project-setup-and-access.md) |
> | Compute (training, data processing) jobs, priority, quota | [Compute Jobs](compute-jobs.md) |

<!--TOC-->

- [1. What Foundry inference is](#1-what-foundry-inference-is)
- [2. Architecture](#2-architecture)
- [3. v2 vs v3 — which to use](#3-v2-vs-v3--which-to-use)
- [4. Customer-facing endpoints](#4-customer-facing-endpoints)
- [5. Models and customers at a glance](#5-models-and-customers-at-a-glance)
- [6. For leads and PgMs](#6-for-leads-and-pgms)
- [7. Third-party model private buckets](#7-third-party-model-private-buckets)
- [8. Where to go next](#8-where-to-go-next)

<!--TOC-->

---

## 1. What Foundry inference is

Foundry serves fine-tuned model endpoints to enterprise customers (NBCU Gabby's Dollhouse, NBCU DreamWorks Animation, TCCC, WDI, THD) and to internal Studio surfaces. Traffic is sporadic — typically 0 requests, then a burst of 1–4 concurrent requests, then back to 0 — which shapes most of our environment and capacity choices.

Two backends co-exist today:

- **v2 — `gen-foundry`** ([details](inference-services-v2.md)). A single service on the Colligo v2 Inference Platform that hosts most production models.
- **v3 — managed services / standalone apps** ([details in colligo](https://github.com/Adobe-Firefly/colligo/blob/main/managed_services/services/firefly/foundry/aidoc/inference-services-v3.md)). The newer platform where new services are built. Each app is self-contained (own deps, own Dockerfile, own deploy).

> [!NOTE]
> "v3 is the new way" — but v2 still serves most production traffic. We migrate models out of gen-foundry one at a time. NBCU DWA (image and video) are the first to land on v3; the rest follow.

---

## 2. Architecture

At the customer edge, a single FastAPI **customer gateway** is the external front door for all v3 Foundry inference. It looks at the request path plus an `x-foundry-model-id` header and 307-redirects to the right backend. (v2 traffic still flows through gen-foundry's own ingress — `gen-foundry.ff.adobe.io` — and will eventually consolidate behind the gateway as models migrate.)

![v3 end-state — apps, gateway, vllm_serve](svg/v3-end-state.svg)

A second shared backend, **`vllm_serve`**, hosts LLMs that multiple apps need (e.g. prompt rewrite). Apps that need an LLM call `vllm_serve` over in-cluster DNS instead of embedding their own engine. One image, one deploy per model variant.

![Customer gateway routing](svg/customer-gateway.svg)

So the production path on v3 looks like:

```
customer ──▶ customer gateway ──307──▶ standalone app (webapp → pipeline → workers)
                                            │
                                            └──in-cluster──▶ vllm_serve (shared LLM)
```

For the architecture inside a v3 app (worker / pipeline / web app split), see the upstream [framework reference](https://docs.ai.corp.adobe.com/v3/frameworks/inference/serve/aidoc/index.html). For the v2 architecture (one service, mixed shared and per-deal workers), see [`inference-services-v2.md` §9.1](inference-services-v2.md#91-architecture-single-service-with-shared-and-deal-specific-workers).

---

## 3. v2 vs v3 — which to use

| | **v2 (gen-foundry)** | **v3 (managed services / standalone apps)** |
|---|---|---|
| Use for | Existing production models that haven't migrated | All new services |
| Code lives in | `colligo/models/colligo/models/foundry/` | `colligo/managed_services/services/firefly/foundry/standalone_apps/<app>/` |
| Deploy config in | `colligo-deploy` (separate repo) | Same repo as code (`deploys/<app>/`) |
| Worker SDK | `inference` (monorepo) | `frameworks.inference` (external, versioned pip) |
| Build / inner loop | `./m package.rhode` + Bazel | `make` + `uv` (app is detached from Bazel) |
| Environments | dev, prerelease | dev, prerelease |
| Detail doc | [`inference-services-v2.md`](inference-services-v2.md) | [colligo `aidoc/inference-services-v3.md`](https://github.com/Adobe-Firefly/colligo/blob/main/managed_services/services/firefly/foundry/aidoc/inference-services-v3.md) |

What stays the same across v2 and v3: access groups, support channels and on-call, the Ethos clusters we run on, and observability (Grafana, Splunk, NewRelic).

> [!TIP]
> Migrating an existing v2 app to v3? Run `/migrate-v2-app-to-v3` in Claude Code, and use the already-migrated apps as worked references — `nbcu_dwa_image` and `nbcu_dwa_video` under `services/firefly/foundry/standalone_apps/`.

---

## 4. Customer-facing endpoints

| FQDN | Backend | Access | Auth |
|---|---|---|---|
| `gen-foundry.ff.adobe.io` | v2 (gen-foundry, prerelease) | public (customer-facing) | IMS token required |
| `foundry-inference.adobe.io` | v3 (customer gateway, prerelease) | public (customer-facing) | IMS token required; only `/v1/`, `/v2/` |
| `foundry-inference-prerelease.adobe.io` | v3 (customer gateway, prerelease) | corp + Pluto (IP-filtered) | none |
| `foundry-inference-dev.adobe.io` | v3 (customer gateway, dev) | corp + Pluto (IP-filtered) | none |

When you ship a new v3 app or endpoint, add a route entry (`{path, model_id?, backend}`) to the customer gateway config so customers can reach it. The backend still validates the forwarded `Authorization` token itself — the gateway's public-endpoint auth is just a first line of defense. See [Gen-Foundry Auth & Allowlisting](gen-foundry-auth-allowlisting.md) for the full auth picture.

---

## 5. Models and customers at a glance

Quick summary — which model serves which customer, and which backend it lives on today. For the complete v2 endpoint table (paths, `foundry_model_id` values, notes), see [`inference-services-v2.md` §10](inference-services-v2.md#10-on-models-and-endpoints). For v3 app inventories, see each app's README under `standalone_apps/`.

| Model | Customers | Backend today |
|---|---|---|
| Image Gen5 ("lego") | NBCU Gabby, TCCC, WDI, THD | v2 |
| Gen6 (GR6) — image | NBCU Gabby | v2 |
| Gen6 (GR6) — video | NBCU Gabby | v2 |
| Gen6 Prompt Rewrite | supports Gen6 | v2 |
| Clineto / Filix | NBCU Gabby | v2 |
| Depth / Edge | Studio | v2 |
| Whisper | Studio | v2 |
| WAN 2.2 Lucy | Studio | v2 |
| NBCU DWA image | NBCU DreamWorks Animation | v3 (`nbcu_dwa_image`) |
| NBCU DWA video | NBCU DreamWorks Animation | v3 (`nbcu_dwa_video`) |

---

## 6. Capacity and Environments

A quick view of the operational shape. Most of what's below applies to **both v2 and v3** — the deep-link in each row points at the source-of-truth for that topic (the platform docs where the topic is general, the v2 or v3 doc where it diverges).

**Environments.** The platform offers four (dev, stage, prerelease, prod); Foundry uses only **dev** and **prerelease** on both v2 and v3. Stage is for high-traffic shared use; prod requires a >99% SLA, on-call rotation, and finance reporting on downtime — overkill for our sporadic 0→4→0 traffic pattern. Prerelease gives us production-like behavior without those obligations. Platform-wide environment definitions: [Clusters and Compute](https://docs.ai.corp.adobe.com/aidoc/inference-platform/infra/compute.html). Per-app environment differences on v3 (auth bypass, scale-to-zero, secrets, gateways): [colligo v3 doc §3](https://github.com/Adobe-Firefly/colligo/blob/main/managed_services/services/firefly/foundry/aidoc/inference-services-v3.md#3-deploying-dev-vs-prerelease).

*Constant high-traffic (left) vs. Foundry's sporadic spike pattern (right):*

![Traffic pattern comparison](svg/traffic-pattern-comparison.svg)

**Deploy checklists.** Standard flow is dev first, smoke-test, then promote to prerelease. v2 checklist: [`inference-services-v2.md` §4](inference-services-v2.md#4-checklists). v3 (standalone apps): [colligo `aidoc/inference-services-v3.md` §3](https://github.com/Adobe-Firefly/colligo/blob/main/managed_services/services/firefly/foundry/aidoc/inference-services-v3.md#3-deploying-dev-vs-prerelease). Legal / non-beta readiness applies to both and is still TBD — current notes in [`inference-services-v2.md` §4.3](inference-services-v2.md#43-legal--non-beta-readiness).

**Capacity (applies equally to v2 and v3).** Foundry runs from a **fixed pool** of P5/P5en nodes shuffled across three categories: Pluto, the stage cluster's Foundry-dedicated pool, and the prod cluster's Foundry-dedicated pool. Both stage and prod have dedicated Karpenter nodepools with bidirectional isolation and a small overprovisioner kept warm — see the [Foundry deploy pool doc in colligo](https://github.com/Adobe-Firefly/colligo/blob/main/managed_services/services/firefly/foundry/aidoc/foundry-deploy-pool.md) for the pool structure, opt-in toleration, and SRE-side detail. **We do not borrow from the inference cluster buffer** — capacity growth means moving nodes within the pool, tracked via Jira tickets on the [book keeping wiki](https://wiki.corp.adobe.com/x/RWZF4Q). Stage and prerelease usage must stay ≤ allocation; the [capacity Excel](https://adobe-my.sharepoint.com/:x:/p/shantanupal/IQA6a83zT61XT4WlIr4PmXhSAVDShPKyaLc4Iv1P5UJ6KwY) is the source-of-truth for the per-category limits. Current usage: [Oshiya stage](https://oshiya-stage.corp.ethos851-stage-or2.ethos.adobe.net/ui/?) · [Oshiya prod](https://oshiya.corp.ethos855-prod-or2.ethos.adobe.net/ui/?namespace=ns-team-colligov2-prod&app=gen-foundry). v2 service-side specifics (gen-foundry single-service architecture, burst-traffic scaling): [`inference-services-v2.md` §9](inference-services-v2.md#9-capacity-management).

Before any deploy that changes GPU replicas or autoscaling envelopes, run **`/check-deploy-capacity`** on the PR — it computes Before/After GPU usage and flags any envelope that would exceed allocation. **Required for prerelease** (replicas stay warm and land on the prod-cluster pool); **also useful for dev when the change touches a sizable GPU worker** (e.g. an x8 stage worker, where the dedicated pool is small). Applies to v2 (`colligo-deploy`) and v3 (`managed_services`).

---

## 7. Third-party model private buckets

Some third-party model assets cannot use the shared inference-platform bucket for base or derived weights. Start with [Third-Party Models](third-party-models.md) for the Adobe engineering process, inventory, repo conventions, and access controls.

For V3 service implementation details, see the Colligo [private bucket weights guide](https://docs.ai.corp.adobe.com/managed_services/services/firefly/foundry/aidoc/private-bucket-weights.html).

---

## 8. Where to go next

| If you want to... | Go to |
|---|---|
| Build a new service | [colligo `aidoc/inference-services-v3.md`](https://github.com/Adobe-Firefly/colligo/blob/main/managed_services/services/firefly/foundry/aidoc/inference-services-v3.md) |
| Operate / change gen-foundry | [`inference-services-v2.md`](inference-services-v2.md) |
| Handle a gen-foundry alert / page | [`gen-foundry-runbook.md`](gen-foundry-runbook.md) |
| Understand v2/v3 customer auth, allowlist a new tenant | [`gen-foundry-auth-allowlisting.md`](gen-foundry-auth-allowlisting.md) |
| Share an endpoint with users via Firefly Boards | [`experimental/shared/boards/README.md`](../experimental/shared/boards/README.md) |
