# Pluto — official documentation (raw)

> Source: Adobe AI Platform docs. Fetched 2026-07-04. Immutable.
> - Index: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/index.html
> - Key concepts: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/concepts.html
> Content below is extracted/condensed from those pages (not necessarily byte-verbatim).

## index.html — Overview

The Compute Platform, codenamed **Pluto**, provides "a graphical interface to manage training ML
models on GPU and CPU compute instances in the Adobe cloud." Accessible at https://ai.corp.adobe.com/.

**Main UI sections (sidebar):**
- **Dashboard** — default landing page; GPU usage metrics and capacity charts across the platform
  and by instance type.
- **Jobs** — personal jobs, project-related jobs, and archived (deleted) jobs.
- **Projects** — view and manage platform projects.
- **Initiatives** — create and modify initiatives.
- **Clusters** — view node clusters.

**Administrative features:** role-based access — initiative admins can add projects and manage
project membership; debug panel for authorized users (beta features, debugging); global
configuration settings for platform policy.

**Reporting / monitoring:**
- **Weekly UA (Utilization of Allocated quota)** — measures GPU capacity utilization.
- **Weekly HFU (Hardware FLOPs Utilization)** — measures GPU computational efficiency.

**Ecosystem integration:** Pluto integrates with broader Adobe AI infrastructure — inference
platforms, training frameworks (**Mori**), data frameworks (**Genie**, **Glimmer**), and agent
frameworks, all documented within the same portal.

## concepts.html — Key concepts

### Platform organization
- **Initiative** — top-level entity grouping multiple projects with a shared resource pool and
  administrative boundary; typically a team or department.
- **Project** — subdivision within an initiative grouping related jobs and managing resources
  independently. Projects have their own quota and can share idle resources when available.
- **Job** — a workload (batch training or interactive session) created within a project. The creator
  becomes the job owner. Every job has an allocation mode determining resource priority.
- **Snapshot** — "a saved state of a job's container that can be restored to resume execution."

### Resource management
- **Quota** — "the number of nodes of each CPU instance type or GPU instance type guaranteed to be
  available to the project's non-preemptible jobs."
- **Allocation Mode (priority tiers):**
  - **P0** — Guaranteed resources within project quota; **non-preemptible**.
  - **P1** — Uses specified resources if available; **preemptible by P0** jobs.
  - **P2** — No quota consumption; runs on spare capacity at lowest priority; **preemptible**.
  - **Limited-time access** — interactive sessions only; four-hour guarantee; max two concurrent
    jobs and three GPUs per user; preemptible after four hours.
- **Current capacity** — resources available within project quota. **Unallocated capacity** —
  currently unused quota.

### Infrastructure
- **Cluster** — a managed group of nodes within one or more node groups; restricted to a single
  region but spanning multiple availability zones.
- **Node group** — a managed collection of similar nodes.
- **Node** — "a high-performance Amazon EC2 instance equipped with one or more GPUs and/or CPUs, as
  well as memory and storage systems."
- **Pod** — a Kubernetes abstraction representing one or more containers scheduled onto a node.
