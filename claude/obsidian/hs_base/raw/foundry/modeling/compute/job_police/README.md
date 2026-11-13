# Foundry Job Police

Automated GPU allocation enforcer. Reads allocation rules from GitHub issue [Adobe-Firefly/foundry#728](https://github.com/Adobe-Firefly/foundry/issues/728), compares against live Pluto jobs, and alerts or kills violating jobs.

## 1. How It Works

```
┌─────────┐     ┌───────────┐     ┌─────────────┐
│ run.py  │────▶│ Claude CLI │────▶│ skill.md    │
│ (loop)  │     │ (per cycle)│     │ (playbook)  │
└─────────┘     └───────────┘     └─────────────┘
                      │
         ┌────────────┼────────────┐
         ▼            ▼            ▼
   ┌──────────┐ ┌──────────┐ ┌──────────────┐
   │ Pluto MCP│ │ gh       │ │ slack_post.py│
   │ list/stop│ │ issue#728│ │ #ersin-eng   │
   └──────────┘ └──────────┘ └──────────────┘
```

1. `run.py` fetches Slack token from Vault, gets GitHub token from `gh auth`.
2. Each cycle invokes Claude Code (Opus via Bedrock) with `skill.md`.
3. Claude fetches allocation rules from GitHub issue #728, lists jobs via MCP, finds violations.
4. Violators are @-mentioned in `#foundry-ersin-eng-team` (one thread per day).
5. Repeat offenders (count >= threshold) get their jobs killed.

## 2. Running Locally

```bash
# Prerequisites (one-time)
gh auth login                         # GitHub auth
uv run --script login.py              # Pluto auth (only needed for --submit-to-pluto)

# Single dry-run (test without posting to Slack or killing)
uv run --script run.py --once --dry-run

# Production loop (every 15 minutes)
uv run --script run.py

# Custom interval and threshold
uv run --script run.py --interval 5 --kill-threshold 2
```

## 3. Running on Pluto

```bash
uv run --script run.py --submit-to-pluto --interval 15
```

This creates a CPU job on Pluto (project: Foundry-Presale-And-Partnership-Support) that:
- Installs uv, gh, foundry-pluto MCP, Claude CLI + Bedrock creds
- Clones this repo branch
- Runs the enforcement loop

Secrets are gathered locally and forwarded as env vars — no interactive auth needed on the node.

## 4. CLI Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--interval` | 15 | Minutes between enforcement cycles |
| `--kill-threshold` | 3 | Alert count before job is killed |
| `--dry-run` | off | Log violations but don't act |
| `--once` | off | Single cycle then exit |
| `--submit-to-pluto` | off | Submit as Pluto CPU job |

## 5. Prerequisites

**Local run:**
- `gh` CLI authenticated (`gh auth login`)
- `foundry-pluto` MCP server installed (`~/.foundry-jobs/`)
- Vault access (for Slack token)

**Pluto submission (additional):**
- `~/.netrc` with Artifactory credentials
- `aip` CLI logged in (`uv run --script login.py`)

If prerequisites aren't met, the script gives clear error messages with fix instructions.

## 6. State

Stored in `$XDG_CACHE_HOME/foundry_job_police_state/` (default `~/.cache/foundry_job_police_state/`):

- `alerts.json` — per-job alert counters and metadata
- `daily_thread.json` — today's Slack thread timestamp

State is ephemeral. If lost, counters reset (violators get fresh warnings before kill).

## 7. Files

| File | Purpose |
|------|---------|
| `run.py` | Main launcher — config, secrets, sleep loop, Claude invocation |
| `skill.md` | Enforcement playbook — Claude follows this each cycle |
| `slack_post.py` | Slack posting helper (click CLI) |
| `pluto_main.sh` | Startup script for Pluto jobs |
| `setup_pluto.py` | Restores aip auth + installs Claude CLI on Pluto |
| `login.py` | Helper for interactive `aip login` |
