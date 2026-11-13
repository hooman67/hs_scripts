---
type: entity
title: Pluto
tags: [adobe-infra, compute, gpu, foundry]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/pluto-docs]]", "[[raw/pluto-skill]]"]
---

# Pluto

**Pluto** is Adobe's **compute platform** — the codename for the Compute Platform that provides a
graphical interface to manage training ML models on GPU and CPU compute instances in the Adobe
cloud. It's a foundational building block of the Adobe AI infrastructure: where training and
interactive GPU workloads run. Web UI: https://ai.corp.adobe.com/.

## What it does

Manages **jobs** (batch training or interactive sessions) on pools of GPU/CPU **nodes**, organized
by [[wiki/concepts/pluto-resource-hierarchy|initiatives → projects → jobs]] and governed by
[[wiki/concepts/quota-and-utilization|quota]] and [[wiki/concepts/allocation-priority-tiers|priority
tiers]]. Runs on Kubernetes over Amazon EC2 GPU instances.

## UI sections

- **Dashboard** — GPU usage and capacity charts, platform-wide and per instance type.
- **Jobs** — personal, project, and archived (deleted) jobs.
- **Projects** / **Initiatives** — manage the org/resource hierarchy.
- **Clusters** — view node clusters.

## GPU landscape

Instance types are grouped by GPU tier: **B200 → H200 → H100 → A100 → CPU** (e.g. `p5en.48xlarge`
carries H200). Monitored via **UA** (utilization of allocated quota) and **HFU** (hardware FLOPs
utilization). See [[wiki/concepts/quota-and-utilization]].

## How Hooman interacts with it

Via the [[wiki/sources/pluto-skill|/pluto skill]], which wraps the **foundry-pluto MCP** (scoped to
Foundry initiatives): `render_dashboard`, `list_jobs`, `get_quota`, `stop_job`, `login`,
`generate_report`. Day-to-day work runs through the [[wiki/concepts/pluto-console|web console]], the
[[wiki/concepts/pluto-cli-sdk|`aip` CLI / SDK]], and the [[wiki/concepts/pluto-job-lifecycle|job
lifecycle]]. A [[wiki/concepts/pluto-operations|governance/operations layer]] (allocation checks,
node-violation detection, utilization canvas) sits on top of the job & quota data.

## Ecosystem

Part of the Adobe AI platform alongside inference platforms, the **[[wiki/entities/mori|Mori]]**
training framework, the **[[wiki/entities/genie|Genie]]** and **[[wiki/entities/glimmer|Glimmer]]**
data frameworks, and agent frameworks — all in the same docs portal. Within
[[wiki/entities/foundry|Foundry]], Pluto is the compute layer initiatives run on. Pluto's own SDK/CLI
(`colligo.pluto`) is built and shipped from the **[[wiki/entities/colligo|Colligo]]** monorepo — see
[[wiki/concepts/colligo-pluto-sdk]].

## Related
- [[wiki/concepts/pluto-resource-hierarchy]]
- [[wiki/concepts/allocation-priority-tiers]]
- [[wiki/concepts/quota-and-utilization]]
- [[wiki/concepts/pluto-job-lifecycle]]
- [[wiki/concepts/pluto-console]]
- [[wiki/concepts/pluto-cli-sdk]]
- [[wiki/concepts/pluto-storage]]
- [[wiki/concepts/pluto-secrets]]
- [[wiki/concepts/pluto-docker-images]]
- [[wiki/concepts/pluto-jupyter]]
- [[wiki/concepts/pluto-policy]]
- [[wiki/concepts/pluto-troubleshooting]]
- [[wiki/concepts/pluto-operations]]
- [[wiki/entities/colligo]]
- [[wiki/concepts/colligo-pluto-sdk]]
- [[wiki/entities/mori]] · [[wiki/concepts/mori-pluto-agent]]
- [[wiki/concepts/ai-platform-overview]]
- [[wiki/entities/ai-platform-repo]] — Pluto's code lives here (`platforms/pluto/`); Pluto is a [[wiki/concepts/v3-deployment|V3]] deploy target
- [[wiki/entities/foundry]] · [[wiki/concepts/foundry-compute]] · [[wiki/concepts/foundry-aws-access]] — Foundry runs on Pluto; its AWS broker consumes the Pluto machine token
- [[wiki/sources/pluto-docs]]
- [[wiki/sources/pluto-docs-operations]]
- [[wiki/sources/pluto-docs-extras]]
- [[wiki/sources/pluto-skill]]
- [[wiki/sources/pluto-governance-skills]]
