---
type: concept
title: Pluto operations
tags: [adobe-infra, compute, pluto, governance, foundry]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/pluto-governance-skills]]"]
---

# Pluto operations

The governance layer on top of [[wiki/entities/pluto|Pluto]]: three of Hooman's skills that read
Pluto quota/job data and two Slack canvases to catch over-allocation, flag node-allocation
violations, and log daily compute utilization.

Where [[wiki/concepts/quota-and-utilization|quota and utilization]] defines *what a project is
entitled to* and [[wiki/concepts/allocation-priority-tiers|priority tiers]] define *who wins when
GPUs are scarce*, **Pluto operations** is the ongoing enforcement: is what's actually **running**
consistent with what was **approved** and **quota'd**, and where is the waste? All three skills run
off the [[wiki/sources/pluto-skill|foundry-pluto MCP]] (`get_quota`, `list_jobs`) plus Slack
canvases read with `slack.user_token`. Full operational detail: [[wiki/sources/pluto-governance-skills]].

## Two governance canvases

- **Weekly Thu→Thu node request and allocation** (`F0BCU4W3KU6`) — the weekly request/approval
  table (requester, node count, GPU type, description, Status). ✅/`:greencheck:` = approved;
  red/blank = not approved. This is the **approval contract** the first two skills check running
  jobs against.

> [!note] Node-allocation canvas is in flux — no dedicated page yet
> The node-allocation process is **new and still settling**. There are currently **two candidate
> canvases** — `F0BCU4W3KU6` (the weekly request/approval table) and `F0AQ1PFGE5U` (the daily
> utilization log) — and the team hasn't decided which is canonical. For now the practice is that
> **Hooman posts the relevant canvas link at runtime** when he runs these skills, rather than the
> skills hard-coding one. Once the team **consolidates to a single canvas**, this is worth its own
> page; until then, deliberately not documented as a fixed concept.
- **Foundry Node Utilization** (`F0AQ1PFGE5U`) — a shared **daily-summary log**, split between
  Hooman's squad (TCCC, THD, Humain) and another squad (NBCU, Lionsgate, Paramount, WDI, GW).

## The three operations

### 1. Allocation check — approved vs. runnable capacity (mutating: DMs Slack)

`allocation_check` builds one table by GPU type (H200 / B200 / Total):
**Available (fleet) · Approved ✅ · Not approved ❌ · Running now**, then DMs it to Hooman.

- **Available (fleet)** comes from `get_quota` — the central capacity pool, `total_xpus ÷ 8`
  nodes per instance type (`p5en.48xlarge`→H200, `p6-b200.48xlarge`→B200). See
  [[wiki/concepts/quota-and-utilization]].
- **Approved / Not approved** come from the weekly canvas.
- **Running now** comes from `list_jobs` (active): `num_nodes × gpus_per_node ÷ 8` for `Running`
  jobs, by `gpu_type`.
- **Free = fleet − running.** If ≤ 0 it reports "overcommitted / no free" — because the quota fleet
  figure can be overcommitted/stale, so "0 free" means *no headroom*, not an exact number. This is
  the operational face of low [[wiki/concepts/quota-and-utilization|unallocated capacity]].

Read-only against Pluto; the only side effect is the Slack DM (`--dry-run` suppresses it).

### 2. Node-violation detection & kill candidates (read-only, advisory)

`find_node_violation` cross-references `Running` jobs against the weekly canvas and ranks **kill
candidates** in three tiers, plus the queued demand a kill would unblock:

1. **Running work the canvas REJECTED** (❌) — clearest violation. Matched by keyword (job **name**
   vs. rejected-row descriptions; jobs also matching an approved row are excluded), so treat as
   "review these," not gospel.
2. **Dev boxes over the 2-GPU limit** — deterministic dev-box rule (name matches `dev` and
   > 2 GPU). Distinct from the [[wiki/concepts/allocation-priority-tiers|Limited-time access]]
   interactive cap (3 GPUs / 2 concurrent).
3. **Demos not declared on the canvas** — deterministic.

It **never stops a job** — stopping is the separate `mcp__foundry-pluto__stop_job` action, done
explicitly by the user afterward. This is the enforcement counterpart to allocation_check's "who
has headroom" table: it names *which running jobs* are eating capacity they weren't granted.

### 3. Node-utilization canvas / daily summaries (mutating: edits shared canvas)

`update-node-utilization-canvas` reads `list_jobs` (all) filtered to `Foundry-TCCC`,
`Foundry-THD`, `Foundry-Humain`, researches unclear job names (FFP- tickets via `/jira-get`, squad
Slack, owner mapping), and writes executive-level **daily compute summaries** into the shared
Foundry Node Utilization canvas. It merges into existing date sections (`insert_after`) or inserts
new ones (`insert_before`), newest-first, and **never touches the other squad's content**. This is
the reporting/utilization-narrative half of governance — the human-readable record of how
[[wiki/concepts/quota-and-utilization|UA/HFU]]-relevant compute was actually spent per customer.

## Read-only vs. mutating

| Skill | Reads | Mutates | Canvas |
|---|---|---|---|
| `allocation_check` | quota, active jobs, canvas | **DMs Hooman** (unless `--dry-run`) | F0BCU4W3KU6 (read) |
| `find_node_violation` | active jobs, canvas | **nothing — advisory only** | F0BCU4W3KU6 (read) |
| `update-node-utilization-canvas` | all jobs, canvas, Jira, Slack | **edits the shared canvas** | F0AQ1PFGE5U (read+write) |

None stop jobs; killing is always a deliberate follow-up via `stop_job`.

## Related
- [[wiki/entities/pluto]]
- [[wiki/concepts/quota-and-utilization]]
- [[wiki/concepts/allocation-priority-tiers]]
- [[wiki/concepts/pluto-resource-hierarchy]]
- [[wiki/sources/pluto-governance-skills]]
- [[wiki/sources/pluto-skill]]
