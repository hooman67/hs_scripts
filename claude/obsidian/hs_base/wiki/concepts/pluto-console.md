---
type: concept
title: Pluto console operations
tags: [adobe-infra, compute, pluto, ui, admin]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/pluto-docs-operations]]"]
---

# Pluto console operations

The operational specifics of the [[wiki/entities/pluto|Pluto]] web console (ai.corp.adobe.com) — editing jobs, administering projects, requesting capacity, and the SRE-only clusters view — beyond the structural overview in [[wiki/concepts/pluto-resource-hierarchy]].

## Onboarding & access

To use the platform you must be in an LDAP group (`CT_SENSEI_*` or `CLOUDTECH_SENSEI_*`, requested via the Adobe IAM portal), then wait ~2 hours for LDAP sync. Verify with `ldapsearch ... cn=<LDAP_USERNAME> memberOf`. The console lives at **https://ai.corp.adobe.com/** and requires the Adobe network / VPN. New users without a project can use the **"Platform Guest (Platform)"** project for time-limited preemptible experimentation.

## Editing a job

Click a job, then the **Edit** button at the top-right of each section. Editability depends on job state and permissions (a disabled/absent Edit button = missing permission or the job is still running; locked fields show a lock icon).

**Editable while running:**
- Job name & description
- Tags (for categorization/filtering)
- Notification recipients (Slack channels)
- Resource Access Roles (**must be added before starting** the job)

**Requires stopping the job first:**
- **Scheduling Spec** — GPU/CPU instance type & count; [[wiki/concepts/allocation-priority-tiers|allocation mode]]; elastic min/max pods; auto-requeue on preemption (P2); exclusive GPU node access
- **Content Spec** — Docker image URL; snapshot ID; GitHub code distribution; init & main scripts
- **Runtime Config** — log collection & verbose logging; Docker enablement; Burstable QoS; Vault secrets
- **Auto Recovery** — enable/disable Auto Recovery V2; pod restart behavior; incidents-per-hour limit

**Never editable:** Job Overview settings (**job type, status, project**) are fixed at creation.

## Project administration

Projects live inside [[wiki/concepts/pluto-resource-hierarchy|initiatives]] ("high-level strategic objectives defined by the Adobe CTO committee") and are the grouping unit for job submission and quota. Users must be **project members** to submit jobs or use quota.

- **Create project** (initiative admins): Initiatives page → select initiative → Projects → *Create Project* → details (architecture, modality, business goal, customer info, lifecycle stage).
- **Edit project** (initiative/project admins): project detail page → *Edit* a section.
- **Manage members**: Members section; add/remove, single or bulk via *Enable multiselect*.
- **Delete/archive project**: initiative admins only; warns if active jobs exist.
- **Resource access roles**: project admins request roles so "jobs created in the project will have access to that resource" (e.g. S3 buckets); the role owner must approve.

## Quota & capacity operations

- **View quota**: each project shows GPU & CPU quota; hover blue values for node counts and availability %. See [[wiki/concepts/quota-and-utilization]].
- **Transfer capacity** (initiative & platform admins): pick source project/initiative → node type + new quota → destination initiative/project → justification (optional Jira ref). "The quota transfer will happen immediately once you click **Confirm Transfer**."
- **Request more capacity**: initiative admins distribute quota per Adobe's "quarterly prioritization process." Notably, "The AI Platform support team cannot get you any additional capacity" — only initiative admins and leadership can approve capacity. Non-funded collaborators ask a funded initiative's admin; unfunded teams escalate through leadership.

## Clusters view (SRE only)

The **Clusters** page is for "platform developers and SREs"; regular users cannot modify cluster settings. It lists all clusters; clicking one shows its EKS **node groups** ("Jobs can only run on a single node group"; "The nodes in a node group are homogeneous"). To **cordon a node**: node group → **VIEW** → **EDIT** → set a **Cordon rank** → **CORDON NODE** → **Save**. The docs flag this section as "_MORE DETAILS TBD_" (capacity/utilization metrics and full admin ops are not yet documented).

## Debugging & telemetry

- **Logs**: job details → **Run Details** → **Browse logs** (running) or **(Download)** (stopped).
- **Telemetry**: **Job Telemetry Dashboard** (resource graphs) and **Open Node Telemetry Dashboard** (Grafana).
- **Pod status colors**: Green = running, Red = error, Yellow = stopped.

## Related
- [[wiki/entities/pluto]]
- [[wiki/concepts/pluto-job-lifecycle]]
- [[wiki/concepts/pluto-resource-hierarchy]]
- [[wiki/concepts/quota-and-utilization]]
- [[wiki/concepts/allocation-priority-tiers]]
- [[wiki/concepts/pluto-cli-sdk]]
- [[wiki/sources/pluto-docs-operations]]
