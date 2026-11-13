---
type: concept
title: Pluto job lifecycle
tags: [adobe-infra, compute, pluto, jobs, scheduling]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/pluto-docs-operations]]"]
---

# Pluto job lifecycle

A [[wiki/entities/pluto|Pluto]] job is either an **interactive session** or a **training job**, and it moves through a fixed set of lifecycle states from Draft to a terminal state.

## Two job types

| Type | Purpose | Ends when |
|---|---|---|
| **Interactive Session** | Interactive development/testing you connect to via Visual Studio (browser VS Code) or a Bash shell. | Persists until you **explicitly stop** it. |
| **Training Job** | Batch execution of scripts. | Scripts exit (unless **"Keep Failed Pods Running"** overrides). |

## Job states

Jobs progress through these states (exact names from the docs):

| State | Meaning |
|---|---|
| **Draft** | Created but not yet started. |
| **Pending** | Scheduled, awaiting resource/quota allocation. |
| **Starting** | Resources allocated; pods initializing. |
| **Queued** | Insufficient resources to begin. |
| **Running** | Accessible and executing. |
| **Running Unstable** | Some pods running while others failed. |
| **Failed** | At least one pod failed or returned a non-zero exit. |
| **Succeeded** | All pods completed successfully. |
| **Stopping** | Terminating, not accessible. |
| **Stopped** | Terminated, not accessible. |

Jobs left more than **two weeks** in Succeeded / Stopped / Failed face **archival**.

## Submitting a job

Both flows start from the Jobs page → **+ Create Job** (see [[wiki/concepts/pluto-console|the console]]). Every job needs a **name** (unique), a **project ID** (you must be a [[wiki/concepts/pluto-resource-hierarchy|project]] member), a **host type** (GPU/CPU) + instance type + count, a **Docker image**, and an **[[wiki/concepts/allocation-priority-tiers|allocation mode]]**.

**Interactive session (batch=no):** Create Job → *Interactive Session* → name → project → host type → instance type + count → image → **Create & Start**. Once Running, open **Run Details → Open VS Code** for a browser IDE. New users can use the **"Platform Guest (Platform)"** project with **Limited Time Access** (≤2 concurrent sessions, 3 GPUs total).

**Training job (batch):** Create Job (*Training Job* is the default) → name → project → **Create** (lands in Draft) → edit compute type / instance type / add scripts → **Start**.

Scripts must be **Bash**. Init scripts run first; "If an init script fails, the remaining init scripts and all main scripts are not executed." For graceful preemption, handle **SIGTERM** within a **30-second** window.

For the CLI/SDK equivalents (`aip job create/start/...`), see [[wiki/concepts/pluto-cli-sdk]].

## Snapshots

A **snapshot** preserves "the current root file system state" — the contents of the root disk (`/home/colligo`) stored off the running node to a central location. It **excludes** `/mnt/localssd` and GitHub code distributions. Cost: ~**1.5–2 s/GB** to create/save, ~**2–3 s/GB** to restore. Snapshots apply to **interactive sessions**, so work survives a stop without recreating it.

Two actions appear as buttons on the job detail page:
- **Save** — creates a snapshot of the root filesystem and stores it off-node while the job **keeps running**.
- **Pause** — saves the filesystem state **and** simultaneously terminates the job.

On resume, a restarted interactive session automatically "restarts from the last snapshot you saved." To start clean instead, **remove the Snapshot ID** so it boots from the plain Docker image. Back local-SSD work up to the root filesystem or S3 *before* snapshotting (local SSD is not captured — see [[wiki/concepts/pluto-storage]]).

Snapshot is the fourth level of the [[wiki/concepts/pluto-resource-hierarchy|resource hierarchy]] (initiative → project → job → snapshot). Source: [[wiki/sources/pluto-docs-extras]] (snapshot announcement blog).

## Scheduling & preemption

The scheduler evaluates jobs strictly in priority order — P0 (guaranteed) → P1 (reclaimable) → P2 (spare) — so higher-priority work is always considered first. P2 jobs are checked in randomized order and re-evaluated roughly every second when capacity changes. Preemption cascades: P2 preempted first, P1 only if P0 needs room, **P0 never preempted**. Within a tier, selection is "non-deterministic." Quota is normally **project-based**, but an initiative can opt into **initiative-based** quota that aggregates usage across its projects. See [[wiki/concepts/allocation-priority-tiers]] and [[wiki/concepts/quota-and-utilization]].

## Platform-managed environment & URLs

Pluto injects env vars into every pod — `JOB_NAME`, `JOB_UUID`, `RANK`, `NUM_OF_GPUS`, `NUM_OF_CPUS`, `PLUTO_AUTH_TOKEN`, `PLUTO_JOB_RUN_ID`, `POD_UUID`, `NODE_NAME`, `PLUTO_LOCAL_USER_ID` (1000), `PLUTO_LOCAL_GROUP_ID` (100) — **do not override them**. Jobs get persistent URLs `https://$HOSTNAME-<PORT>.jobs.colligo.dev` (hostname `pluto-prod-<LDAP_ID>-<JOB_NAME>-<RANK>-PORT`); ports 8000–8006 serve apps, VS Code uses 20000.

## Related
- [[wiki/entities/pluto]]
- [[wiki/concepts/pluto-console]]
- [[wiki/concepts/pluto-cli-sdk]]
- [[wiki/concepts/allocation-priority-tiers]]
- [[wiki/concepts/pluto-resource-hierarchy]]
- [[wiki/concepts/quota-and-utilization]]
- [[wiki/sources/pluto-docs-operations]]
