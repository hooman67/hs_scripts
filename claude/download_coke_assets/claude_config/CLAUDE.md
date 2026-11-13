# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## User Context

Hooman Shariati (hshariati@adobe.com), engineering manager at Adobe working on AI platform infrastructure, generative models (Firefly), and related tooling. LDAP / username everywhere: `hshariati`.

## Proactive Tool Usage

Use the skills and scripts automatically based on context — don't wait for the user to ask explicitly.

- **Jira ticket reference** (e.g., "FFP-123", "look at that ticket"): use `/jira-get`
- **Sprint / workload questions** ("check my sprint", "what's on my plate"): use `/jira-sprint`
- **Create/update/close tickets**: use `/jira-create`, `/jira-update`
- **Slack messages** ("send this to the team", "DM me"): use `/slack-post` (defaults to DMing Hooman)
- **Slack thread URL or channel ID**: use `/slack-read` to fetch and display it
- **Confluence / wiki page reference**: use `/wiki-read`
- **Create or update wiki pages**: use `/wiki-write`
- **Meeting transcript provided**: use `/meeting-to-jira` to extract action items and map to Jira tickets

## Skills (Slash Commands)

All skills live in `~/.claude/commands/` backed by Python scripts in `~/.claude/scripts/`. Scripts use `uv run --script` with inline PEP 723 deps (requests, pyyaml). Credentials at `~/.claude/hshariati/credentials.yaml`.

| Skill | Description |
|---|---|
| `/slack-post` | Post message to Slack. Defaults to DMing Hooman if no channel specified. |
| `/slack-read` | Read messages from a channel or thread. Requires channel ID (bot can't list channels). |
| `/jira-get` | Get ticket details |
| `/jira-create` | Create a ticket |
| `/jira-update` | Update ticket fields, transition status, add comments |
| `/jira-sprint` | Show current sprint tickets. Supports custom JQL. |
| `/wiki-read` | Read a Confluence page by ID or URL |
| `/wiki-write` | Create or update a Confluence page |
| `/meeting-to-jira` | Process meeting transcripts → extract action items → propose Jira updates |

### Slack Limitations

The Slack bot token does **not** support `search.messages` or `conversations.list`. Work only with channel IDs and thread timestamps provided by the user. Channel IDs can be extracted from Slack URLs: `app.slack.com/client/TEAM_ID/CHANNEL_ID`.

## Environment Overview

Home directory with multiple Adobe AI/ML projects.

### Key Projects

| Directory | Description | Stack |
|---|---|---|
| `colligo/` | AI Platform monorepo — model serving, training infra, platform libs | Python (ruff, mypy, pytest) |
| `foundry/` | Foundry monorepo — Foundry Studio, media intelligence, modeling | TS (pnpm, Lit, NestJS) + Python (uv, ruff) + Terraform |
| `genie/` | Dataloader for images, audio, video (Project Clineto) | Python (uv, black, ruff), Rust |
| `spl-web-client/` | SPL Web Client & CLIO Playground — graph-based task execution | TypeScript (pnpm, eslint, Prettier) |
| `hs_scripts/` | Personal utility scripts — evaluation, inference, data processing | Python |

### Shell Environment

- Conda (miniconda3), nvm, bun, uv, Google Cloud SDK
- `alias aip="python -m colligo.pluto.sdk.cli"` — Colligo CLI
- `alias ethos_dev` / `ethos_prod855` — kubectl context switching for Colligo k8s clusters

## Build & Development Commands

### Colligo (`colligo/`)
- Linting: `ruff check .` and `ruff format .` (config in root `pyproject.toml`, line-length=120, target py310)
- Type checking: `mypy` (strict mode, config in root `pyproject.toml`)
- Tests: `pytest` (import-mode=importlib, 120s timeout per test, `--log-cli-level=INFO`)
- Single test: `pytest path/to/test_file.py::test_name`
- Package discovery roots: `models/`, `pylibs/`, `contrib/`, `third_party/`

### Foundry (`foundry/`)
- Has its own `CLAUDE.md` → `AGENTS.md` system (two-level agent guidelines)
- TS projects: `pnpm install`, `pnpm lint`, `pnpm lint:fix`
- Python projects: `uv`, `ruff`
- Pre-commit: Husky + lint-staged (auto-setup on `pnpm install`)
- Git workflow: never commit to `main`, branch format `USER/<initiative>/<description>`, use `.worktrees/` for worktrees

### Genie (`genie/`)
- Setup: `make venv` (uses uv)
- Lint: `make lint` (black + ruff)
- Docker: `make build`, `make push`

### SPL Web Client (`spl-web-client/`)
- Setup: `./scripts/onetime-setup.sh` then `pnpm install`
- Build: `pnpm -w build` or `pnpm -w watch` (incremental)
- Tests: `pnpm -w test` (fast), `pnpm -w test/all` (incl. integration)
- Lint: `pnpm -w lint`, fix: `pnpm -w lint/fix`
- Dev server: `pnpm -w start`
- Test naming: files suffixed with `-test` (e.g. `feature-test.ts`)

## Architecture Notes

### Colligo
- Monorepo with shared linter config in root `pyproject.toml` (ruff, mypy, pytest all configured there)
- Libraries in `pylibs/`, models in `models/`, third-party in `third_party/`, contributions in `contrib/`
- `colligo.pluto` — the platform SDK/CLI
- Uses pydantic (v2) with mypy plugin; strict typing enforced
- Known first-party import: `colligo` (ruff isort config: `detect-same-package = false`)

### Foundry
- Catch-all monorepo for code not in Genie or Colligo
- `foundry-studio/` — NestJS backend + Lit/TypeScript frontend
- `media-intelligence/` — video understanding ML pipeline
- `experimental/` — prototypes and explorations

### SPL Web Client
- pnpm workspace monorepo with `@spl/` and `@adobe/` scoped packages
- Core packages: `@spl/client` (graph/session), `@spl/sensei` (Sensei endpoint tasks), `@spl/core` (types/utils)
- Artifactory-based npm registry for `@spl` scope; requires Node >=20.9.0
