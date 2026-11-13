---
type: concept
title: Pluto resource hierarchy
tags: [adobe-infra, compute, pluto]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/pluto-docs]]"]
---

# Pluto resource hierarchy

How [[wiki/entities/pluto|Pluto]] organizes work and hardware. Two parallel hierarchies — one
**organizational** (who owns the work), one **physical** (what it runs on).

## Organizational (ownership of work)

- **Initiative** — top-level entity grouping multiple projects, with a shared resource pool and
  administrative boundary. Typically a team or department. Initiative admins add projects and manage
  membership.
- **Project** — a subdivision within an initiative that groups related jobs and manages resources
  independently. Each project has its own [[wiki/concepts/quota-and-utilization|quota]] and can share
  idle resources when available.
- **Job** — a workload (batch training **or** interactive session) created within a project. The
  creator is the job **owner**. Every job has an [[wiki/concepts/allocation-priority-tiers|allocation
  mode]] setting its priority.
- **Snapshot** — a saved state of a job's container that can be restored to resume execution. Fuller
  treatment (what's captured, save/restore cost): [[wiki/concepts/pluto-job-lifecycle]] (Snapshots section).

`Initiative → Project → Job (→ Snapshot)`

## Physical (hardware)

- **Cluster** — a managed group of nodes across one or more node groups; restricted to a single
  **region** but spanning multiple availability zones.
- **Node group** — a managed collection of similar nodes.
- **Node** — a high-performance Amazon EC2 instance with one or more GPUs and/or CPUs, plus memory
  and storage.
- **Pod** — a Kubernetes abstraction of one or more containers scheduled onto a node.

`Cluster → Node group → Node → Pod`

## Related
- [[wiki/entities/pluto]]
- [[wiki/concepts/quota-and-utilization]]
- [[wiki/concepts/allocation-priority-tiers]]
