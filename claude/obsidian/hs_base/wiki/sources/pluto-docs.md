---
type: source
title: "Pluto documentation"
raw: "[[raw/pluto-docs]]"
created: 2026-07-04
updated: 2026-07-04
ingested: 2026-07-04
tags: [adobe-infra, compute, pluto]
---

# Pluto documentation

The official Adobe AI Platform docs for [[wiki/entities/pluto|Pluto]] — the index/overview page and
the Key Concepts page. Source: [[raw/pluto-docs]]
(https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/).

## Key claims

- Pluto = the **Compute Platform** — a GUI to manage training ML models on GPU/CPU instances in the
  Adobe cloud; UI at ai.corp.adobe.com. Sections: Dashboard, Jobs, Projects, Initiatives, Clusters.
- **Organizational hierarchy:** [[wiki/concepts/pluto-resource-hierarchy|Initiative → Project → Job]]
  (+ Snapshot). **Physical hierarchy:** Cluster → Node group → Node → Pod (Kubernetes on EC2).
- **Quota** = guaranteed nodes per instance type for a project's non-preemptible jobs;
  current vs. unallocated capacity. See [[wiki/concepts/quota-and-utilization]].
- **Allocation modes / priority tiers:** P0 (guaranteed, non-preemptible), P1 (preemptible by P0),
  P2 (spare, no quota), Limited-time access (4h interactive). See
  [[wiki/concepts/allocation-priority-tiers]].
- **Efficiency metrics:** weekly **UA** (utilization of allocated quota) and **HFU** (hardware FLOPs
  utilization).
- **Ecosystem:** integrates with inference platforms, **[[wiki/entities/mori|Mori]]** (training), **[[wiki/entities/genie|
  Genie]]** / **[[wiki/entities/glimmer|Glimmer]]** (data), and agent frameworks.

## Notes
- Not byte-verbatim — condensed from the rendered pages. Sub-pages (Dashboard/Jobs/Projects/etc.)
  exist and can be ingested later for deeper detail.

## Related
- [[wiki/entities/pluto]]
- [[wiki/sources/pluto-skill]]
