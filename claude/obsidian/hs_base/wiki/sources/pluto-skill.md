---
type: source
title: "/pluto skill + foundry-pluto MCP"
raw: "[[raw/pluto-skill]]"
created: 2026-07-04
updated: 2026-07-04
ingested: 2026-07-04
tags: [adobe-infra, compute, pluto, tooling]
---

# /pluto skill + foundry-pluto MCP

How Hooman operates [[wiki/entities/pluto|Pluto]] from Claude Code: the `/pluto` skill wrapping the
**foundry-pluto** MCP server (scoped to Foundry initiatives). Source: [[raw/pluto-skill]].

## Capabilities (MCP tools)

- `render_dashboard` — open an auto-refreshing browser dashboard (the **default** way to "show jobs").
- `list_jobs` — job list for small/specific queries, formatted as a markdown table.
- `get_quota` — per-project capacity (see [[wiki/concepts/quota-and-utilization]]).
- `stop_job` — stop by job ID (then refresh dashboard; offer to Slack the owner).
- `login` — device-code auth.
- `generate_report` — upload a static HTML snapshot to S3 to share a view.

## Display conventions

- Group by instance type; sort by GPU tier **B200 → H200 → H100 → A100 → CPU**, then size desc.
- Columns: job name, project, owner, priority, nodes, GPUs/node, type, age, status. Age as relative
  time. Default to **active jobs only**.

## Priority labels

The skill and MCP use display strings that differ from the docs' wording — see the flagged
contradiction in [[wiki/concepts/allocation-priority-tiers]]. Skill: "P0 Guaranteed / P1 Reclaimable
/ P2 Spare Capacity". MCP: "P0 Critical / P1 Normal / Limited-time access / P2 Spare Capacity".

## Related
- [[wiki/entities/pluto]]
- [[wiki/sources/pluto-docs]]
