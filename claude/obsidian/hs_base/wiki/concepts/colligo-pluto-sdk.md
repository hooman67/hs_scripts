---
type: concept
title: Colligo Pluto SDK (colligo.pluto)
tags: [colligo, pluto, compute, sdk, cli, aip]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/colligo/pylibs/colligo/pluto/sdk/AGENTS.md]]", "[[raw/colligo/pylibs/colligo/pluto/AGENTS.md]]", "[[raw/colligo/aidoc/monorepo/index.md]]"]
---

# Colligo Pluto SDK (`colligo.pluto`)

The **Compute Platform (Pluto)** code that ships from inside [[wiki/entities/colligo|Colligo]] at `pylibs/colligo/pluto/`. Colligo is where Pluto's SDK, CLI, services, containers, dashboard, and agent live in source; the running platform is [[wiki/entities/pluto|Pluto]] itself.

This is the crucial link between the two: **the `aip` CLI Hooman uses (`python -m colligo.pluto.sdk.cli`) is exactly this Colligo-shipped Pluto SDK.** See [[wiki/concepts/pluto-cli-sdk]] for CLI usage and [[wiki/concepts/pluto-job-lifecycle]] for job semantics.

## What lives under `pylibs/colligo/pluto/`

- **`sdk/`** — the public, distributable **wheel** (its own `pyproject.toml`, entrypoint `cli.py`). Internal `colligo.pluto.*` deps are auto-bundled by `./pluto sdk validate-deps`. Public API imports come from `colligo.pluto.sdk` (never `_core`). Build with `./pluto sdk build`; release with `./pluto sdk release <major|minor|patch>`.
- **`service/`, `ecs/`, `agent/`** — the compute-API service, ECS deployment, and the on-node Pluto agent.
- **`containers/`** — the sidecar/init containers Pluto runs on nodes: `aggregator`, `bindfs`, `cache`, `job_init`, `log_server`, `nfs_mount`, `otel_collector`, `pluto_hardware_fault_detector`, `preflight_tests`, `prometheus_push_gateway`, `common`.
- **`dashboard/`** — a **frontend** package with its own `package.json` (`dev`/`test`/`lint`/`build:proto:dev`/`build`); use those scripts, regenerate proto/types via the package (don't hand-edit `_generated/`).

## Package-level rules

- Python **3.12** for Pluto code (note: the wider monorepo baseline is 3.10+), absolute imports, ruff, mypy, Adobe copyright header.
- The SDK is a **separate wheel**: guard optional deps with `try/except ImportError` so the dep scanner skips them; run `./pluto sdk validate-deps --fix` after changing internal imports; update `pyproject.toml` before adding an external PyPI dep and re-validate.
- Uses a dedicated `./pluto` command dispatcher (distinct from the repo-wide `./m`), and `./m package.pluto` packages Pluto release candidates.

> [!note] Docs migrated
> Most Pluto user/internal docs (CLI, jobs, clusters, quotas, scheduler, secrets, s3-access, deployment, caplan, etc.) were migrated out of the monorepo `aidoc/` to `https://docs.ai.corp.adobe.com/v3/platforms/pluto/` (redirects listed in `aidoc/root.md`). Source code stays in `pylibs/colligo/pluto/`.

## What Pluto provides

GPU/CPU job scheduling, quota management, interactive development sessions, training-job monitoring/observability, and host-level system deps (GPU drivers) for both training and inference dev. It is dependency-type 5 ("host system deps") in Colligo's [[wiki/concepts/colligo-architecture|dependency taxonomy]].

## Related

- [[wiki/entities/pluto]]
- [[wiki/concepts/pluto-cli-sdk]]
- [[wiki/concepts/pluto-job-lifecycle]]
- [[wiki/entities/colligo]]
- [[wiki/concepts/colligo-training]]
- [[wiki/concepts/colligo-architecture]]
