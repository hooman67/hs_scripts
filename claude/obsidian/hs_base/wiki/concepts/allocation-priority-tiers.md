---
type: concept
title: Allocation priority tiers
tags: [adobe-infra, compute, pluto, scheduling]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/pluto-docs]]", "[[raw/pluto-skill]]"]
---

# Allocation priority tiers

Every [[wiki/entities/pluto|Pluto]] job has an **allocation mode** that determines its resource
priority and whether it can be **preempted** (evicted so a higher-priority job can run). This is how
Pluto shares finite GPUs across [[wiki/concepts/pluto-resource-hierarchy|projects]].

## The tiers (per the official docs)

| Tier | Quota | Preemption | Meaning |
|---|---|---|---|
| **P0** | Within project [[wiki/concepts/quota-and-utilization\|quota]] | **Non-preemptible** | Guaranteed resources for the project's committed work. |
| **P1** | Uses specified resources if available | **Preemptible by P0** | Runs when capacity exists; yields to P0. |
| **P2** | **No quota consumption** | Preemptible (lowest priority) | Opportunistic — runs on spare capacity only. |
| **Limited-time access** | — | Preemptible **after 4h** | Interactive only; 4-hour guarantee; max **2 concurrent jobs** and **3 GPUs** per user. |

Higher tier = stronger guarantee. Preemption cascades downward: P0 can evict P1/P2; P2 gets whatever
is left over.

## Terminology differs by source — RESOLVED

> [!note] Resolved (2026-07-04)
> The tiers are the same everywhere; only the display labels differed. The later CLI/SDK ingest
> settles it: the **canonical names are the `aip job create` allocation-mode flags** (see
> [[wiki/concepts/pluto-cli-sdk]]):
> - `--guaranteed` → **P0 Guaranteed** (non-preemptible)
> - `--quota-charged-reclaimable` → **P1 Reclaimable** (preemptible by P0)
> - `--quota-free` → **P2 Spare Capacity** (no quota consumption)
> - `--limited-time-access` → **Limited-time access** (4h interactive)
>
> Against that canon:
> - **Docs** ([[wiki/sources/pluto-docs]], [[wiki/sources/pluto-docs-operations]]) — correct
>   (guaranteed / reclaimable / spare semantics).
> - **/pluto skill** ([[wiki/sources/pluto-skill]]): "P0 Guaranteed / P1 **Reclaimable** / P2 Spare
>   Capacity" — **correct** (matches the CLI flags).
> - **foundry-pluto MCP** ([[wiki/sources/pluto-skill]]): "P0 **Critical** / P1 **Normal** /
>   Limited-time access / P2 Spare Capacity" — the **outlier**. "Critical"/"Normal" are the only
>   labels that don't match; they should read **Guaranteed** / **Reclaimable**.
>
> This is **cosmetic only** — the MCP's "Critical/Normal" are dashboard *display strings*; the
> underlying preemption policy (and therefore [[wiki/concepts/pluto-job-lifecycle|scheduling/preemption
> behavior]]) is unaffected. Not a functional problem: we know P0 Critical = Guaranteed and
> P1 Normal = Reclaimable. Fix is to correct the MCP's two display strings when convenient.

## Related
- [[wiki/entities/pluto]]
- [[wiki/concepts/quota-and-utilization]]
- [[wiki/concepts/pluto-resource-hierarchy]]
- [[wiki/concepts/pluto-cli-sdk]]
- [[wiki/concepts/pluto-job-lifecycle]]
