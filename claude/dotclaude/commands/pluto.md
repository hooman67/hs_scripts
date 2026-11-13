Interact with the Foundry Pluto compute platform — list jobs, check quota, stop jobs, open dashboard, and generate reports.

## Available Actions

This skill wraps the `foundry-pluto` MCP server tools. Use the appropriate MCP tool based on what the user asks:

### Show Jobs / Dashboard
- **"show me the jobs"**, **"what's running"**, **"open dashboard"** → Use `mcp__foundry-pluto__render_dashboard` to open an auto-refreshing HTML dashboard in the browser.
- For small/specific queries (e.g., "largest job", "who owns the most H200s") → Use `mcp__foundry-pluto__list_jobs` and format as a markdown table.
- Default to **active jobs only** (running, queued, starting, stopping). Only include stopped/archived if explicitly asked.

### Check Quota
- **"show quota"**, **"how much capacity"** → Use `mcp__foundry-pluto__get_quota`.
- Display per-project capacity: instance type, GPU type, total GPUs, used GPUs, utilization %.

### Stop a Job
- **"stop job X"** → Use `mcp__foundry-pluto__stop_job` with the job ID.
- After stopping, always call `render_dashboard` to refresh the view.
- Ask if the user wants to notify the owner via Slack (use `/slack-write` skill).

### Login
- **"login"** → Use `mcp__foundry-pluto__login` for first-time device-code authentication.

### Generate Shareable Report
- **"save this view"**, **"share this"** → Use `mcp__foundry-pluto__generate_report` to upload a static HTML snapshot to S3.

## Display Conventions
- Group by instance type (showing GPU: B200, H200, H100, A100)
- Sort by GPU tier (B200 first), then by job size descending
- Show age as relative time: "2h 15m", "3d 1h"
- Priority labels: P0 Guaranteed, P1 Reclaimable, P2 Spare Capacity

## Parameters
- `project`: Filter to a specific project name
- `initiative`: Filter to a specific Foundry initiative
- `status_filter`: "active" (default), "running", "pending", "stopped", "all"

## Examples
```
/pluto show me the jobs
/pluto show quota for foundry-tccc
/pluto stop job 725b295b-ac38-40fc-8c25-52159202b778
/pluto login
```
