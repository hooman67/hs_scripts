---
type: source
title: "Source: Colligo Dependency Management & Build System"
tags: [colligo, source, dependencies, build-system, uv, colligo-yaml]
created: 2026-07-04
updated: 2026-07-04
ingested: 2026-07-04
raw: "[[raw/colligo/aidoc/dependency-management/overview.md]]"
sources: ["[[raw/colligo/aidoc/dependency-management/overview.md]]", "[[raw/colligo/aidoc/dependency-management/build-system.md]]"]
---

# Source: Colligo Dependency Management & Build System

Distilled from `aidoc/dependency-management/overview.md` and `build-system.md`. Synthesis in [[wiki/concepts/colligo-architecture]] and [[wiki/concepts/colligo-dev-workflow]].

## Overview doc

- Splits by lifecycle (see [[wiki/concepts/colligo-philosophy]]): short-lived code → published pip package (`pip install colligo[models,inference,train,...]`); long-lived code → in-monorepo with heavy tooling.
- **Five dependency types:** (1) monorepo tenants — checked-in code (1.1) and large binaries via checked-in manifests (1.2); (2) internal Adobe deps as subtrees; (3) external deps — as-is via pip (3.1), custom-built no-source-change (3.2), source-modified subtrees (3.3); (4) containerized system deps (CUDA/OS from the official dev Docker image, kept few); (5) host system deps (GPU drivers, managed by the [[wiki/entities/pluto|Pluto]] compute team).
- **Single version per dependency** monorepo-wide — deliberate trade-off for testability + low operational overhead. Platform team drives upgrades; owners must maintain tests. If your untested/passing workflow breaks after an upgrade, it's your responsibility to fix.

## Build-system doc

- The Python build system registers modules, collects/locks fixed versions into one UV lock file, and builds one dev virtualenv.
- Controlled by: root `pyproject.toml` (`tool.colligo.repo`), `envs/dev/requirements.lock.txt`, `envs/dev/known-packages.txt`, `envs/dev/constraints.txt`, `envs/common/{overrides,constraints-darwin-exclusions}.txt`, per-package `colligo.yaml` (under `models/`+`pylibs/`), plain `pyproject.toml` only for `contrib/`+`third_party/`, and the `./m` dispatcher.
- Commands: `./m lint` (dep checks), `./m deps.lock` (regenerate lock, run on Linux for CUDA/GPU; `deps.lock.docker` for macOS), `./m deps.sync` (env + proto gen), `source m`, `./m package.rhode` / `./m package.pluto`.
- **Frozen environments** (`envs/frozen/*.lock.txt`) support staged migrations (e.g. Torch 2.1→2.3); only one supported at a time.

## Related

- [[wiki/concepts/colligo-architecture]]
- [[wiki/concepts/colligo-dev-workflow]]
- [[wiki/concepts/colligo-philosophy]]
- [[wiki/entities/colligo]]
