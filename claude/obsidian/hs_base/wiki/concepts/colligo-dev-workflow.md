---
type: concept
title: Colligo Dev Workflow (m CLI, lint, test, deps)
tags: [colligo, dev-workflow, tooling, uv, ruff, mypy, pytest, ci]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/colligo/AGENTS.md]]", "[[raw/colligo/aidoc/dependency-management/build-system.md]]", "[[raw/colligo/aidoc/monorepo/index.md]]", "[[raw/colligo/pylibs/AGENTS.md]]", "[[raw/colligo/models/AGENTS.md]]"]
---

# Colligo Dev Workflow (`./m` CLI, lint, test, deps)

The day-to-day developer loop in [[wiki/entities/colligo|Colligo]], driven by the **`./m` command dispatcher** (`tools/tasks.py`) over a **UV**-managed single environment.

## The `./m` CLI

```bash
./m deps.create              # create the dev environment (UV)
source m                     # activate the dev environment
./m deps.sync                # sync submodules + python deps; runs proto (.proto) generation
./m deps.lock                # regenerate envs/dev/requirements.lock.txt (run on Linux for CUDA/GPU)
./m deps.lock.docker         # (experimental) lock inside a linux/amd64 container (for macOS)
./m lint                     # auto-fix lint + format (ruff) + mypy + colligo.yaml dep checks
./m lint --check             # check only, no fixes
./m lint --paths "p1 p2"     # lint specific paths (recommended — mypy over the whole repo is slow)
./m package.rhode            # package an inference (Rhode) release candidate
./m package.pluto            # package a compute-platform (Pluto) release candidate
pytest path/to/test_file.py  # run tests
```

## Environments (UV)

One dev virtualenv with **fixed, locked** dependency versions — the monorepo supports a **single version of each dependency**. Key files (see [[wiki/sources/colligo-dependency-management]] and [[wiki/concepts/colligo-architecture]]):

- `envs/dev/requirements.lock.txt` — all locked versions
- `envs/dev/constraints.txt` — inputs to the lock
- `envs/dev/known-packages.txt` — import→package-name map for static analysis
- `envs/common/overrides.txt`, `constraints-darwin-exclusions.txt`
- Root `pyproject.toml` `tool.colligo.repo` — general build config
- `envs/frozen/*.lock.txt` — staged-migration frozen envs (only one supported at a time)

`./m deps.lock` should be re-run and checked in whenever deps/constraints change.

## Coding standards (enforced)

- Python **3.10+** (Pluto code is 3.12), strict type annotations on all public functions.
- **Absolute imports only** (`from colligo.base.x import y`) — no relative imports.
- No plain `assert` in production code — use `validation_assert(cond, details)` (→ HTTP 422) or `runtime_assert(cond, details)` (→ HTTP 500) from `colligo.base.exceptions`.
- Adobe copyright header on every source file; Google-style docstrings on public functions.
- Package deps declared in per-package `colligo.yaml` (auto-maintained by `./m lint`), **not** hand-edited `pyproject.toml` (except `contrib/`, `third_party/`).

## Testing

- `pytest` per file/path. Directories **excluded** from repo-wide pytest: `contrib/`, `third_party/`, `managed_services/`, `vendor/`, `_build/`.
- CPU and GPU unit testing with code coverage; a separate integration-testing framework and CI pipelines run affected-package tests. Full CI/testing docs live under `aidoc/continuous-integration/` and `aidoc/testing/` (not yet ingested in depth).

## Boundaries & PR rules

- NEVER modify `third_party/`, `uv.lock`, `*.lock`, or generated files (`*_pb2*.py(i)`, `registry/applications.yaml`).
- Work **package by package** — `pylibs/` and `models/` are many independent packages, each with its own `colligo.yaml` + co-located `tests/`; some use `custom_pyenv`. Keep metadata, code, worker/endpoint registration, and tests aligned in one change.
- PR titles need a JIRA prefix in brackets (`[FFP-123] ...` / `[NOJIRA] ...`); PR body must follow `.github/PULL_REQUEST_TEMPLATE.md`.

## Related

- [[wiki/entities/colligo]]
- [[wiki/concepts/colligo-architecture]]
- [[wiki/sources/colligo-dependency-management]]
- [[wiki/concepts/colligo-managed-services]] — V3 uses Bazel instead of `./m`
- [[wiki/sources/colligo-agents]]
