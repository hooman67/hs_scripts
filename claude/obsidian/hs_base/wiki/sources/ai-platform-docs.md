---
type: source
title: AI Platform Docs Portal (docs.ai.corp.adobe.com)
tags: [ai-platform, docs-portal, inference, infra, source]
created: 2026-07-05
updated: 2026-07-05
raw: "[[raw/ai-platform-docs]]"
sources: ["[[raw/ai-platform-docs]]"]
---

# AI Platform Docs Portal (docs.ai.corp.adobe.com)

Distilled summary of the **official Adobe AI Platform documentation portal**
(`https://docs.ai.corp.adobe.com/`), ingested 2026-07-05. Scope of this ingest: the **general
platform overview** and the **inference-platform infrastructure** — the "how inference actually runs"
layer that the V2/V3 framework pages don't fully cover. Raw capture: [[raw/ai-platform-docs]].

## What this source is

The portal is compiled from the co-located `aidoc/` folders across the [[wiki/entities/colligo|Colligo]]
monorepo, so its URL tree mirrors the repo. Top-level sections: Philosophy, Compute Platform (Pluto),
Training Framework (Mori), Inference Platform, Data Platform, Monorepo, Capability Registry, Access
Control, an engineering-practices band, and Models & Services.

## Pages I ingested (all OK unless noted)

- `/` (portal map) and `aidoc/philosophy.html` → [[wiki/concepts/ai-platform-overview]]
- `aidoc/inference-platform/index.html` (nav + product areas)
- `aidoc/inference-platform/infra/index.html`, `.../infra/compute.html` (Ethos clusters, gateway,
  compute, state)
- `.../infra/observability.html` (Grafana / New Relic / Splunk)
- `.../infra/auto-scaling.html` (Oshiya / QBS / KEDA scale-to-zero)
- `.../infra/slo-framework.html` (firefly-sla, error budgets, burn-rate alerting, ORR)
- `.../infra/colligo-deploy/index.html` (Ethos Flex Helm, worker groups, crossfade)
- `.../infra/deployment-automation.html` (ArgoCD, Argo Analysis canary, PR-comment triggers)
- `aidoc/inference-platform/capability-registry.html` (capability catalog)

All of the above feed [[wiki/concepts/colligo-inference-infra]].

**404/blocked:** `.../infra/colligo-deploy/targeted-rollouts.html` returned HTTP 403 — skipped
(crossfade/targeted-rollout detail was recovered from the colligo-deploy index instead).

## Deliberately left to siblings / not ingested

- **Pluto** (`pylibs/colligo/pluto/aidoc/`) — already covered by [[wiki/entities/pluto]] and its
  concept pages; not re-fetched.
- **Training / Mori** (`contrib/Mori/aidoc/`) — sibling-owned; see [[wiki/concepts/colligo-training]].
- **Models catalog** (`models/**/aidoc/`, Flux/Florence/IP-Guard/Adobe-Research, Firefly Foundry
  Services) — sibling-owned.
- **Data Platform** (`aidoc/data-platform/`) — noted in the map only; belongs with
  [[wiki/entities/genie]] / [[wiki/entities/glimmer]].
- **Inference *framework*** internals (task queues, rate limiter, backpressure, streaming, etc.) —
  already summarized in [[wiki/concepts/colligo-inference]]; this ingest focused on infra, not the
  framework API.
- Engineering-practices band (testing, CI, static analysis, code review) and caplan/support
  (postmortems, newsletters, release notes) — not fetched.

## Related

- [[wiki/concepts/ai-platform-overview]]
- [[wiki/concepts/colligo-inference-infra]]
- [[wiki/concepts/colligo-inference]] · [[wiki/concepts/colligo-managed-services]]
- [[wiki/entities/colligo]] · [[wiki/entities/pluto]]
- [[raw/ai-platform-docs]]
