---
type: concept
title: Quota and utilization
tags: [adobe-infra, compute, pluto, capacity]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/pluto-docs]]", "[[raw/pluto-skill]]"]
---

# Quota and utilization

How [[wiki/entities/pluto|Pluto]] measures what a [[wiki/concepts/pluto-resource-hierarchy|project]]
is entitled to and how well that entitlement is used.

## Quota

**Quota** = the number of nodes of each CPU or GPU instance type **guaranteed** to be available to a
project's **non-preemptible** ([[wiki/concepts/allocation-priority-tiers|P0]]) jobs. Each project has
its own quota and can share idle resources when available.

- **Current capacity** — resources available within project quota.
- **Unallocated capacity** — quota that is currently unused.

Checked via the [[wiki/sources/pluto-skill|/pluto skill]] `get_quota` (per-project: instance type,
GPU type, total GPUs, used GPUs, utilization %).

## Utilization metrics

Two weekly efficiency metrics (dashboard reporting):

- **UA — Utilization of Allocated quota** — how much of the *allocated* GPU capacity is actually
  being used. Answers "are we using what we reserved?"
- **HFU — Hardware FLOPs Utilization** — how efficiently the GPUs *compute* while in use. Answers
  "are the GPUs we're using doing real work, or idling/stalling?"

UA is about **occupancy**; HFU is about **compute efficiency** of that occupancy. Both matter: high
UA with low HFU means nodes are held but under-driven.

> [!note] Governance tie-in
> Hooman's `allocation_check`, `find_node_violation`, and `update-node-utilization-canvas` skills
> operate on this quota/utilization data to catch over-allocation and node-canvas violations.

## Related
- [[wiki/entities/pluto]]
- [[wiki/concepts/allocation-priority-tiers]]
- [[wiki/concepts/pluto-resource-hierarchy]]
