# Compute Jobs

Foundry uses the [Compute Platform (Pluto)](https://ai.corp.adobe.com/) for training, data processing, and demo jobs. All jobs run under the [Foundry Initiative (GAI-415)](https://ai.corp.adobe.com/compute/initiatives/d54f60e2-523d-4314-a8dc-885f091183f6).

<!--TOC-->

- [1. For Engineers](#1-for-engineers)
  - [1.1 Get Access to the Right Project](#11-get-access-to-the-right-project)
  - [1.2 Submit a Job](#12-submit-a-job)
  - [1.3 Choosing the Right Priority](#13-choosing-the-right-priority)
  - [1.4 Viewing Running Jobs](#14-viewing-running-jobs)
- [2. For Admins](#2-for-admins)
  - [2.1 Quota and Node Movement](#21-quota-and-node-movement)
  - [2.2 How to Visualize All Jobs](#22-how-to-visualize-all-jobs)
  - [2.3 Utilization Dashboards](#23-utilization-dashboards)
  - [2.4 Negotiating and Enforcing Allocation](#24-negotiating-and-enforcing-allocation)
  - [2.5 Computing UA for NBCU](#25-computing-ua-for-nbcu)
  - [2.6 Computing Initiative Allocation by Project](#26-computing-initiative-allocation-by-project)

<!--TOC-->

> [!IMPORTANT]
> **Shared pool — effective March 27, 2026.** All Foundry projects now share a single compute pool via initiative-level quota. Per-project node movement is no longer needed. The "Foundry Unified Compute" project holds the aggregate quota; individual projects will show zero quota — that is expected.

---

## 1. For Engineers

### 1.1 Get Access to the Right Project

Every job must be submitted from its associated project. Submitting from the wrong project has financial reporting consequences.

If you do not have access to a project, ask an initiative admin on the [Foundry Initiative page](https://ai.corp.adobe.com/compute/initiatives/d54f60e2-523d-4314-a8dc-885f091183f6).

### 1.2 Submit a Job

Use any of these tools to create and submit jobs:

- **[Pluto UI](https://ai.corp.adobe.com/)** — web interface for creating and managing jobs.
- **Pluto CLI (`aip`)** — command-line interface. See [CLI docs](https://docs.ai.corp.adobe.com/pylibs/colligo/pluto/aidoc/cli-jobs.html).
- **`morictl`** — Foundry's training launcher in [foundation_exploration](https://github.com/Adobe-Firefly/colligo/tree/main/contrib/Mori/collections/foundation_exploration). See [`docs/training.md`](training.md).

Always submit from the correct project.

### 1.3 Choosing the Right Priority

Set the job's [allocation mode](https://docs.ai.corp.adobe.com/pylibs/colligo/pluto/aidoc/jobs.html#allocation-mode) based on how critical it is. **Default to P1** unless you have a specific reason not to.

| Priority | When to Use | Job Types | Notes |
|---|---|---|---|
| **P0 — Guaranteed** | Critical work that must not be interrupted. Use sparingly. | Training | Resources guaranteed within quota. Cannot be preempted. |
| **P1 — Reclaimable** | **Default.** Standard submission mode. Only P0 can preempt. | Training, Interactive, Data | Quota-charged. Set up [graceful shutdown](https://docs.ai.corp.adobe.com/pylibs/colligo/pluto/aidoc/jobs.html#graceful-shutdown) to handle preemption. |
| **P2 — Spare Capacity** | Work that tolerates eviction, or data processing with bursty compute needs. | Data, Training | Quota-free, lowest priority (P0 and P1 can preempt). Supports [elastic resource allocation](https://docs.ai.corp.adobe.com/pylibs/colligo/pluto/aidoc/jobs.html#elastic-resource-allocation) — set max pods > min pods to auto-scale with available capacity. |
| **Limited-time access** | Short interactive sessions for debugging or quick iterations. | Interactive | Guaranteed 4-hour runtime, max 2 sessions / 3 GPUs per user. No quota charged. |

**With `morictl` — set priority in your config** (`launch.job_priority`, [example](https://github.com/Adobe-Firefly/colligo/blob/main/contrib/Mori/collections/foundation_exploration/configs/foundry/nbcu/gen45_inf_i2v_sample.yaml#L11)):

> [!TIP]
> Use `in-quota-preemptible` (P1) for all jobs — these run within Foundry quota and are the recommended default. Reserve `guaranteed` (P0) sparingly for work that absolutely must not be interrupted.

```yaml
launch:
  job_priority: in-quota-preemptible  # guaranteed | in-quota-preemptible | preemptible
```

**With Pluto CLI (`aip`):**

- P1: `aip job create --name my-job --in-quota-preemptible ...`
- P2: `aip job create --name my-job --preemptible ...`
- Limited-time: `aip job create --name my-job --limited-time-access ...`

### 1.4 Viewing Running Jobs

See [§2.2 How to Visualize All Jobs](#22-how-to-visualize-all-jobs) below. The same dashboards are available to all Foundry members, not just admins.

---

## 2. For Admins

### 2.1 Quota and Node Movement

Node movement between projects is no longer needed. All projects share a single compute pool under initiative-level quota.

- The **Foundry Unified Compute** project holds the aggregate quota.
- Individual project quotas show zero — that is expected.
- To adjust capacity allocation between projects, see [§2.4 Negotiating and Enforcing Allocation](#24-negotiating-and-enforcing-allocation).

### 2.2 How to Visualize All Jobs

The [Foundry Jobs Agent](../modeling/compute/job_agent/README.md) provides a unified view of all running jobs across Foundry projects, via an MCP server for Claude Code and Cursor.

Install it:

```bash
curl -s https://dit-scale-up.s3.us-west-2.amazonaws.com/foundry-jobs/latest/install.py | bash
```

Then open Claude Code or Cursor and ask:

```
> show me the jobs
> what's running?
```

This opens a live browser dashboard that auto-reloads every 10 seconds. You can also generate a [shareable snapshot](https://dit-scale-up.s3.us-west-2.amazonaws.com/foundry-jobs/reports/v1/b9f52c6ad92d.html) by asking:

```
> save this view
```

See the [Foundry Jobs Agent README](../modeling/compute/job_agent/README.md) for full usage and customization.

### 2.3 Utilization Dashboards

Three Grafana dashboards track Foundry compute usage:

| Dashboard | What It Shows | Link |
|---|---|---|
| UA Quota | Weekly utilization by instance type (hours and instance count) | [UA Quota Dashboard](https://observability.ai.corp.adobe.com/d/ua_quota_dashboard_prod/ua-quota-dashboard?orgId=1&from=now-30d&to=now&timezone=utc&var-initiative_key=GAI-415%20Foundry&var-adobe_week_key=$__all&var-job_size_category=$__all&var-instance_type=$__all) |
| HFU Weekly | Weekly GPU HFU utilization | [HFU Dashboard](https://observability.ai.corp.adobe.com/d/hfu_weekly_dashboard_prod/hfu-dashboard-weekly?orgId=1&from=now-30d&to=now&timezone=utc&var-initiative_key=GAI-415-Foundry&var-adobe_week_key=$__all&var-job_size_category=$__all&var-instance_type=$__all) |
| Cost / Spend | Weekly cost breakdown | [Cost Dashboard](https://observability.ai.corp.adobe.com/d/cost_spend_dashboard_prod/costs-spend-dashboard?orgId=1&from=now-6h&to=now&timezone=browser&var-adobe_week_key=$__all&var-category=$__all&var-expense_type=$__all&var-account_name=$__all) (select filters manually) |

You can also query these through the Foundry Jobs Agent:

```
> show me utilization for Foundry Unified Compute
> show me HFU for all Foundry
> show me cost dashboard
```

### 2.4 Negotiating and Enforcing Allocation

All projects share the same compute pool — there are no hard per-project quotas to enforce. Instead, squad admins agree on usage guidelines at a regular cadence (e.g., weekly).

**Rules** are maintained as bullet points in **[GitHub issue #728](https://github.com/Adobe-Firefly/foundry/issues/728)**. Admins update the issue body whenever allocation changes. example:

```
- NBCU has priority over N nodes this week.
- Certain jobs should be P0; others must be P1 or P2.
- A specific project should not exceed X GPUs.
```

**Checking and enforcing.** Ask Foundry Jobs Agent:

```
> check compliance       — reads #728 rules, compares against active jobs,
                           flags violators in red with ⚠ tooltips on the dashboard
> stop the violators     — confirms each stop, then notifies owners via Slack
```

### 2.5 Computing UA for NBCU

NBCU purchased a specific number of P5-equivalent nodes and we report their utilization periodically.

> [!NOTE]
> There is a known bug with the platform dashboard that affects recent weeks' data — see [FFP-81614](https://jira.corp.adobe.com/browse/FFP-81614). Until resolved, data for the most recent weeks may be unavailable.

**How to calculate:**

1. Open the [UA Quota Dashboard](https://observability.ai.corp.adobe.com/d/ua_quota_dashboard_prod/ua-quota-dashboard?orgId=1&var-initiative_key=GAI-415%20Foundry&var-project_key=Foundry%20NBCU&var-instance_type=$__all&timezone=utc), select the relevant weeks, and read GPU hours per instance type (P5, P5e, P6, P4de) from the bar chart:

   ![UA Quota Dashboard — sum the usage hours in the bar chart](https://github.com/user-attachments/assets/75207a4f-99e3-486b-809c-088188290616)

2. Enter the values into the **"NBCU UA Tracker"** sheet of the [UA Calculator spreadsheet](https://adobe.sharepoint.com/:x:/r/sites/FoundryPunchlist/Shared%20Documents/12%20Foundry%20Model%20Engineering/Foundry%20Pluto%20Utilization.xlsx?d=w6ed65a750c144702963a5db5fd5dd3db&csf=1&web=1&e=KFt0H0). The sheet computes utilization automatically:

   | Start Date | End Date | P5-eq Nodes Promised | P5 Hours | P5e Hours | P6 Hours | P4de Hours | Days | Promised P5-eq Hours | Used P5-eq Hours | % Utilization |
   |---|---|---|---|---|---|---|---|---|---|---|
   | (you enter) | (you enter) | (based on deal) | *(from dashboard)* | *(from dashboard)* | *(from dashboard)* | *(from dashboard)* | *auto* | *auto* | *auto* | *auto* |

3. The sheet converts non-P5 hours to P5-equivalent using fixed conversion factors (configured at the top of the sheet), then computes: **Utilization % = Used P5-eq Hours / Promised P5-eq Hours**.

### 2.6 Computing Initiative Allocation by Project

To report how Foundry's total compute is distributed across customer projects (for finance):

> [!NOTE]
> This also depends on the UA Quota Dashboard and is affected by the same bug — see [FFP-81614](https://jira.corp.adobe.com/browse/FFP-81614).

1. Open the [UA Quota Dashboard](https://observability.ai.corp.adobe.com/d/ua_quota_dashboard_prod/ua-quota-dashboard?orgId=1&var-initiative_key=GAI-415%20Foundry&var-instance_type=$__all&timezone=utc) at the **initiative level** (all projects), and read GPU hours per project per instance type.

2. Enter the values into the **"Initiative Allocation"** sheet of the [UA Calculator spreadsheet](https://adobe.sharepoint.com/:x:/r/sites/FoundryPunchlist/Shared%20Documents/12%20Foundry%20Model%20Engineering/Foundry%20Pluto%20Utilization.xlsx?d=w6ed65a750c144702963a5db5fd5dd3db&csf=1&web=1&e=KFt0H0). The sheet computes each project's share automatically:

   | Project | P5 Hours | P5e Hours | P6 Hours | P4de Hours | P5 % | P5e % | P6 % | P4de % | P5 Nodes | P5e Nodes | P6 Nodes | P4de Nodes |
   |---|---|---|---|---|---|---|---|---|---|---|---|---|
   | NBCU | *(from dashboard)* | *(from dashboard)* | *(from dashboard)* | *(from dashboard)* | *auto* | *auto* | *auto* | *auto* | *auto* | *auto* | *auto* | *auto* |
   | THD | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

3. Enter total nodes per instance type at the top of the sheet. The sheet computes: **Project % = project hours / total hours**, and **Project Nodes = % × total nodes**.

> [!TIP]
> For a new reporting period, copy the entire block (rows 3–18, which includes total nodes config + project table) and paste it below. Update the period label, total nodes, and project hours. You will also need to fix the formula references: replace `$5` with the new config row and `$18` with the new total row.
