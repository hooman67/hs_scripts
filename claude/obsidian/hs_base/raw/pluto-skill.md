# Pluto — /pluto skill + foundry-pluto MCP (raw)

> Source: Hooman's `/pluto` Claude Code skill (`~/.claude/commands/pluto.md`) and the
> `foundry-pluto` MCP server's runtime instructions. Captured to raw on 2026-07-04. Immutable.

## /pluto skill

Interact with the Foundry Pluto compute platform — list jobs, check quota, stop jobs, open
dashboard, and generate reports. Wraps the `foundry-pluto` MCP server tools.

### Actions
- **Show jobs / dashboard**: "show me the jobs", "what's running", "open dashboard" →
  `render_dashboard` opens an auto-refreshing HTML dashboard in the browser. For small/specific
  queries (largest job, who owns the most H200s) → `list_jobs` formatted as a markdown table.
  Default to **active jobs only** (running, queued, starting, stopping); include stopped/archived
  only if explicitly asked.
- **Check quota**: "show quota", "how much capacity" → `get_quota`. Show per-project: instance
  type, GPU type, total GPUs, used GPUs, utilization %.
- **Stop a job**: "stop job X" → `stop_job` with the job ID; then `render_dashboard` to refresh.
  Offer to notify the owner via Slack (`/slack-write`).
- **Login**: "login" → `mcp__foundry-pluto__login` for first-time device-code auth.
- **Generate shareable report**: "save this view" / "share this" → `generate_report` uploads a
  static HTML snapshot to S3.

### Display conventions
- Group by instance type (showing GPU: B200, H200, H100, A100).
- Sort by GPU tier (B200 first), then job size descending.
- Age as relative time ("2h 15m", "3d 1h").
- Priority labels (as written in the skill): **P0 Guaranteed, P1 Reclaimable, P2 Spare Capacity**.

### Parameters
- `project` (filter to a project), `initiative` (filter to a Foundry initiative),
  `status_filter`: "active" (default), "running", "pending", "stopped", "all".

## foundry-pluto MCP server (runtime context)

Scope: specifically **Foundry** initiatives on Pluto (not general Pluto). Tools: `render_dashboard`,
`list_jobs`, `get_quota`, `stop_job`, `login`, `generate_report`, `get_version`.

### Display conventions (MCP)
- Default grouping: instance type (name + GPU, e.g. "p5en.48xlarge H200").
- Default columns: job name, project, owner, priority, nodes, GPUs/node, type, age, status.
- Default sort: GPU tier (B200 → H200 → H100 → A100 → CPU), then job size descending.
- GPU short names: B200, H200, H100, A100.
- Priority labels (as written in the MCP): **P0 Critical, P1 Normal, Limited-time access,
  P2 Spare Capacity**.

### Workflow guidance
- "show me the jobs" / "list jobs" → prefer the **browser dashboard** (`render_dashboard`) by
  default. Use a markdown table (`list_jobs`) only for specific small queries.
- Default to **active jobs only** (status_filter="active"). "all jobs" → status_filter="all".
- Never pull stopped/archived/succeeded by default.
