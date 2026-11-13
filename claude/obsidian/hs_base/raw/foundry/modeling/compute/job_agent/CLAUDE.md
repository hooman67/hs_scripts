# Foundry Job Agent — Development Guide

## 1. The Sync Contract

This is an **AI-native development** project:

- **`design/`** is the source of truth. The human reviews only this.
- **`src/`** is derived. The agent keeps it in sync with `design/`.
- **`plans/`** contains development plans. Changes always start with a new plan.

When modifying the app, edit `design/` files first, then update `src/` to match. Never modify `src/` without a corresponding `design/` change.

**IMPORTANT — Order of operations for every change:**

1. Identify which `design/` file(s) are affected (app.md, runtime-context.md, layouts/*.md).
2. Update `design/` first with the new behavior/spec.
3. Then update `src/` to implement what `design/` now says.
4. If a change is purely internal (refactor, bug fix, no behavior change), `src/`-only is OK — but add a comment in the commit explaining why no design change was needed.

**Before pushing:**
- Run `uv run pytest` and ensure all tests pass.
- If you changed template context, render logic, or layout files: render the dashboard with **every** available layout (shipped + runtime) to verify none are broken. A layout that worked before must not break due to a context change (e.g. adding/renaming a field).

## 2. Directory Structure

```
job_agent/
  scripts/             # Tooling scripts (release, etc.)
    release.py         # Release automation (full + dev)
  plans/               # Development plans (one per effort)
  design/
    app.md             # App spec: what it does, initiatives, workflows, architecture
    runtime-context.md # MCP instructions loaded for installed users
    layouts/           # Natural-language layout specs → agent syncs to src/layouts/
  src/
    foundry_jobs/
      server.py        # MCP server (tools + instructions from runtime-context.md)
      client.py        # Pluto SDK wrapper (FoundryJobsClient)
      render.py        # Jinja rendering: container + layout → HTML file
      s3.py            # S3 upload helper
    container.jinja.html    # Shared HTML shell (styles, header, auto-reload)
    layouts/                # Jinja layouts (one per design/layouts/*.md). Sacred at runtime.
    runtime_layouts/        # User-created layouts (modifiable at runtime)
```

## 3. Release Process
All release logic lives in `scripts/release.py`. Uses anonymous S3 access (`--no-sign-request`) to the `dit-scale-up` public bucket.

```bash
python3 scripts/release.py -m "User-facing change description"   # Full release with curated changelog
python3 scripts/release.py                                       # Full release (changelog auto-generated from git log)
python3 scripts/release.py --dev                                 # Dev release: quick upload for testing, no changelog
```

**Changelog convention:** Always use `-m` with a user-facing summary. The changelog is for end users — only include visible behavior changes (new features, UI changes, bug fixes), not internal refactors, doc updates, or file moves. If `-m` is omitted, the script falls back to raw git log which includes noise.

**What `scripts/release.py` does:**
- Sets `pyproject.toml` version to the release version (e.g. `"2026.03.24"`) — this is the single source of truth read by `get_version` at runtime
- Vendors the `adobe-aip` wheel into `vendor/` (so users don't need Artifactory/.netrc)
- Patches `pyproject.toml` to remove the Artifactory index
- Uploads code + vendored wheel to S3
- `install.py` uses `uv sync --find-links vendor/` to resolve `adobe-aip` locally
- Commits `CHANGELOG.md` and `pyproject.toml` version bump, then uploads to S3

The source `pyproject.toml` in git keeps the Artifactory index for development — only the S3 copy has it removed.

## 4. Development Setup

### 4.1 Install dependencies

```bash
cd modeling/compute/job_agent
uv sync
```

### 4.2 Register MCP server

Open Claude Code from `modeling/compute/job_agent/`. The `.mcp.json` auto-registers the `foundry-pluto` MCP server.

### 4.3 Authentication

Use the `login` MCP tool, or run `uv run aip login`. Tokens cached at `~/.colligo/pluto_cli/msal-pluto-auth.secret`.

## 5. Pluto SDK Reference

### 4.1 Core calls

```python
from colligo.pluto.sdk.internal.cli_context import CLIContext
ctx = CLIContext()
client = await ctx.get_client()  # → PlutoClient

from colligo.pluto.sdk.job.command_utils.list_util import get_filtered_jobs
jobs = await get_filtered_jobs(client, initiatives=["GAI-415 Foundry"], return_job_details=False)
```

### 4.2 Entity component system

Pluto uses an entity-component system. Use `ComponentModels.*.get(entity)` for protobuf components, not `get_state()`.

**Key gotcha:** `job_type` and `preemption_policy` live on `ComponentModels.job.get(entity)`, not on `get_state()`. The `PlutoJob.job_type` and `PlutoJob.preemption_policy` from `get_filtered_jobs()` are always 0 — must fetch `JOB_COMPONENT` separately. Use `jc.exec_spec.preemption_policy` for the real priority.

### 4.2b Preemption policy mapping

The `PreemptionPolicy` enum maps to platform priority labels as follows:

| Enum | Value | Platform label | Quota-charged? |
|------|-------|----------------|----------------|
| `NON_PREEMPTABLE` | 0 | P0 Guaranteed | Yes |
| `IN_QUOTA_PREEMPTABLE` | 4 | P1 Reclaimable | Yes |
| `PREEMPTABLE` | 1 | P2 Spare Capacity | No |
| `ELASTIC_PREEMPTABLE` | 3 | P2 Spare Capacity | No |
| `LIMITED_TIME_ACCESS` | 2 | Limited-time access | No |

P0 and P1 are quota-charged (guaranteed section). P2, LTA are quota-free (preemptible section). `host_spec.cpu_cores` gives the actual CPU allocation for CPU jobs (varies per job, not fixed per instance type).

```python
from colligo.pluto.proto import ComponentType
from colligo.pluto.client.entity_defs import ComponentModels

entities = await client.get_entities(
    entity_ids=["<uuid>"],
    component_types=[ComponentType.JOB_COMPONENT],
)
jc = ComponentModels.job.get(entity)  # → JobComponent protobuf
jc.job_type  # 1=interactive, 2=training
```

### 4.3 Finding more

The Pluto dashboard code at `pylibs/colligo/pluto/dashboard/` in [Adobe-Firefly/colligo](https://github.com/Adobe-Firefly/colligo) is the best reference for discovering components and fields. Key files:
- `src/store/EntityModels.ts` — component types per entity
- `src/store/PlutoJobEntity.ts` — job computed properties
- `src/store/PlutoEntity.ts` — base entity accessors

Clone for reference: `git clone --single-branch --depth 1 https://github.com/Adobe-Firefly/colligo.git .worktrees/colligo`

### 4.4 Instance types

| Instance | GPU | GPUs/Node |
|----------|-----|-----------|
| `p6-b200.48xlarge` | B200 | 8 |
| `p5en.48xlarge` | H200 | 8 |
| `p5.48xlarge` | H100 | 8 |
| `p4de.24xlarge` | A100 | 8 |
| `c6id.24xlarge` | CPU | 0 |

### 4.5 Auth internals

```python
from colligo.pluto.sdk.internal.cli_context import ConsoleAccessTokenProvider
provider = ConsoleAccessTokenProvider()
token = await provider.get_access_token()       # cached token
await provider.initiate_device_flow(callback)    # device code flow
```

### 4.6 Quota

`capacity_usage.quota_usage.xpu_counters` on `PlutoProject` — per-instance-type GPU quotas. No node counters; derive by dividing GPUs by GPUs-per-node.
