# Agent Instructions: Pluto

<!-- AGENTS:JUDGE:context START -->
## Context

- **Purpose:** Platform layer of the Colligo AI Platform monorepo — GPU/CPU job scheduling, quotas, and training observability. Python 3.12, async-first, PostgreSQL-backed, with a self-contained `./pluto` toolchain. Ships a control-plane service (workers run by a supervisor), two distributable wheels (`adobe-aip-pluto-agent`, `adobe-aip-compute`), an MCP package, container images, and a React/Vite dashboard.
- **Architecture (one sentence):** A supervisor (`service/commands/pluto_supervisor.py` in prod, `dev/dev_supervisor.py` in dev) launches per-concern worker processes from `service/workers/<name>_worker.py`; each worker is a thin entry point that calls into a sibling `service/<name>/` directory holding the actual logic, with state persisted in PostgreSQL (via `ecs/`) and Redis. The two wheels (`agent/` runs inside user training jobs, `sdk/` provides the user-facing `aip` CLI) and the React dashboard (`dashboard/`) are independent dialects that consume the control plane.
- **Key Files:**
  - `pluto` — bash entry point; `source pluto` activates the dev venv
  - `pyproject.toml` — root project config (deps, ruff, mypy, pytest)
  - `service/commands/pluto_supervisor.py` — production worker supervisor
  - `dev/dev_supervisor.py` — local dev worker supervisor
  - `proto_defs/` — source `.proto` files; regenerated via `./pluto build-proto`
- **Sub-package context (Claude Code auto-loads each via its `CLAUDE.md` → `@AGENTS.md`):**
  - `service/AGENTS.md` — dual-supervisor pattern, `workers/` convention, worker→service pairings
  - `ecs/AGENTS.md` — entity/component data layer, `ECSSession`, task affinity, event roles
  - `sdk/AGENTS.md`, `dashboard/AGENTS.md` — the two distributable dialects
  - `containers/AGENTS.md` — index of per-container build recipes; each container has its own AGENTS.md too
<!-- AGENTS:JUDGE:context END -->

<!-- AGENTS:JUDGE:technical_rules START -->
## Technical Rules

- **Stack:** Python 3.12, async-first, PostgreSQL, Redis. Standalone toolchain via `./pluto` (independent of the Colligo monorepo's `./m`). Pinned UV binary for reproducible envs; mise for tool versions; deptry for external-dep validation; Click for the CLI.
- **Supported hosts:** Linux or macOS only, on `x86_64` or `arm64`/`aarch64`. Windows is unsupported (the setup tooling enforces this).
- **Required env vars before any `./pluto env *` command:** `ARTIFACTORY_UW2_USER` (your LDAP) and `ARTIFACTORY_UW2_API_TOKEN` (Artifactory API key — get it at <https://artifactory-uw2.adobeitc.com> via SAML SSO, then profile → Generate API Key). Persist them in `~/.zshrc` / `~/.bashrc`.
- **Imports:** Absolute only — `from colligo.pluto.* import ...`. No relative imports.
- **Proto imports:** One level deep — `from colligo.pluto.proto.ecs import ...`. Not `from colligo.pluto.proto.model.entities_pb2 import ...`.
- **Type annotations:** Required on all public functions; mypy is part of `./pluto lint`.
- **Copyright header:** Adobe Confidential block at the top of every source file.
- **Lint / format:** Ruff (line length 120) + mypy via `./pluto lint`.
- **Tests:** `test_*.py` files in `tests/` dirs alongside code; require a local PostgreSQL via `PostgresLauncher` (in `conftest.py`).
- **Retry loops:** Use `DefaultJitterRetryScope("pluto_<name>")` instead of hand-coded retries.
- **Wheels:** `agent/` and `sdk/` have their own `pyproject.toml`. Internal `colligo.pluto.*` deps are auto-bundled by AST scanning (`tools/_deps.py`); imports guarded by `try/except ImportError` are treated as optional.
<!-- AGENTS:JUDGE:technical_rules END -->

<!-- AGENTS:JUDGE:common_commands START -->
## Common Commands

- **First-time setup:** `./pluto env setup` (installs `jf`, mise tools, Artifactory creds; pulls vault creds)
- **Activate env:** `source pluto` (sourced, not executed — also activates mise-managed tools)
- **Sync env:** `./pluto env sync` (re-run any time `uv.lock` or `pyproject.toml` change)
- **Verify env health:** `./pluto env check`
- **Lint:** `./pluto lint` (add `--check` for read-only)
- **Build proto:** `./pluto build-proto` (regenerates `proto/` and `proto_models/`)
- **Tests:** `pytest <path> -v` (120s timeout per test). Single test: `pytest path/to/test_x.py::test_name -v`. Single test class: `pytest path/to/test_x.py::TestClass -v`.
- **Run all workers (dev):** `python -m colligo.pluto.dev.dev_supervisor --run-pluto-http --run-scheduler ...`
- **Run a single worker:** `python -m colligo.pluto.service.workers.<name>_worker ...`
- **Build / release wheels:** `./pluto sdk build`, `./pluto agent build`, `./pluto <sdk|agent> release <major|minor|patch>`
- **Build container image:** `./pluto image build [--push]`
- **Manage AGENTS.md:** Don't hand-create them — use the CLI:
  - `./pluto agents-md init <path>` — create a new AGENTS.md in that directory (errors if one already exists)
  - `./pluto agents-md fill <path>` — create or refresh; auto-detects key files, commands, and entry points
  - `./pluto agents-md refresh <path>` — re-render an existing AGENTS.md, preserving your hand-written sections
  - `./pluto agents-md scan` — list which directories are in the default scope and which have an AGENTS.md
  - `./pluto agents-md migrate <path>` — convert an un-marked legacy AGENTS.md into the marker format
- **Env validation at Claude Code startup:** `.claude/scripts/check-env.sh` is wired as a SessionStart hook in `.claude/settings.json`. It silently passes when the venv + Artifactory creds are loaded; otherwise it tells you to run `./claude` or `source ./pluto`.
<!-- AGENTS:JUDGE:common_commands END -->

## Agentic Setup

Agent-agnostic tooling (MCP servers, skills) lives in `.agents/`. See [`.agents/README.md`](.agents/README.md) for the full layout and philosophy.

- **MCP servers:** configured in `.mcp.json`. To add a new server or understand the wrapper pattern, see [`.agents/mcp-servers/README.md`](.agents/mcp-servers/README.md).
- **Skills:** reusable guides in `.agents/skills/`, surfaced in Claude Code via `.claude/skills → ../.agents/skills`. See [`.agents/skills/README.md`](.agents/skills/README.md) to add one.
- **MCP credentials:** use the `setup-mcp-credentials` skill (say "set up mcp credentials" in Claude Code).
- **Agent-specific config** (hooks, permissions, settings) stays in `.claude/` (Claude Code), `.cursor/`, `.codex/`, etc. — not in `.agents/`.

<!-- AGENTS:JUDGE:dos_donts START -->
## Do's and Don'ts

- **DO:** use `./pluto`, not compound shell commands. Don't `cd` between dirs or activate other envs inline.
- **DO:** add the Adobe copyright header to every new source file.
- **DO:** add long-running processes as `service/workers/<name>_worker.py` and select via `--run-<name>`.
- **DO:** if a shell reports `command not found` for `npm` / `go` / other mise-managed tools, the venv was activated directly bypassing mise — run `deactivate && source pluto` and retry.
- **DON'T:** edit generated code (`proto/`, `proto_models/`).
- **DON'T:** edit `uv.lock` manually — regenerate with `./pluto env lock`.
- **DON'T:** edit a wheel's `[tool.setuptools.packages.find]` block by hand — `./pluto <sdk|agent> validate-deps --fix` regenerates it.
- **DON'T:** use `~` or relative paths in `pluto.dev.yaml`'s `default_k8s_cluster.auth.path` — they're not expanded. Always use fully-qualified absolute paths.
<!-- AGENTS:JUDGE:dos_donts END -->
