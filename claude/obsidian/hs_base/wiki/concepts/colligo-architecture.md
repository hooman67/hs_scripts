---
type: concept
title: Colligo Architecture & Package Layout
tags: [colligo, architecture, monorepo, packaging, colligo-yaml]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/colligo/AGENTS.md]]", "[[raw/colligo/aidoc/monorepo/index.md]]", "[[raw/colligo/aidoc/dependency-management/build-system.md]]", "[[raw/colligo/pylibs/AGENTS.md]]", "[[raw/colligo/models/AGENTS.md]]"]
---

# Colligo Architecture & Package Layout

How [[wiki/entities/colligo|Colligo]] is organized: many independent Python packages under a few top-level roots, glued by a custom build system that reads per-package `colligo.yaml` files and produces a single locked environment.

## Top-level roots and their boundaries

- **`pylibs/`** — shared libraries in the `colligo.*` namespace. **Not one package**: `pluto`, `rhode`, `base`, `sdk`, `fastapi`, `repo`, `image`, `ci`, `doc_gen`, `external_services`, etc. each follow their own workflow. Work package-by-package; the nearest `colligo.yaml` (not `pylibs/pyproject.toml`) is the source of truth for deps, visibility, and env selection. Notable: `pylibs/colligo/pluto/dashboard` is a **frontend** (its own `package.json` — use `dev`/`test`/`lint`/`build`, don't hand-edit `_generated/`).
- **`models/`** — ML model packages (~50 top-level: `firefly`, `flux`, `di_imaging`, `substance3d`, `video`, `audio`, `masking`, `cai`, `common`, `template`, ...). Treat as many independent package roots, each with its own `colligo.yaml`, `build.py`, and co-located `tests/`. Some use `custom_pyenv` — check before changing deps.
- **`managed_services/`** — Inference V3, a **separate Bazel workspace** with its own deps, build system, release cadence, and code owners. Detached from V2 but kept in-repo for shared access control. See [[wiki/concepts/colligo-managed-services]].
- **`contrib/`** — research/training codebases that live in-repo but keep independent workflows (Mori, AdobeDiffusion, eval_science, autoX, ...). Configured via plain `pyproject.toml`, not full monorepo tooling. Excluded from repo-wide pytest.
- **`third_party/`** — vendored external + Adobe deps as **subtrees** (`third_party/adobe/*`, `third_party/external/*` — torch, vllm, diffusers, transformers, flash_attn, ffmpeg, ...). NEVER modify. Also uses plain `pyproject.toml`.
- **`aidoc/`, `tools/`, `envs/`, `docker/`, `data/`, `registry/`** — docs, the `./m` CLI + build scripts, UV env configs, container images, LFS test fixtures, and generated registry (do not modify).

## The `colligo.yaml` package model

Each in-repo Python package (under `models/` and `pylibs/`) carries a `colligo.yaml` that declares dependencies with less boilerplate than native `pyproject.toml`. It specifies:

1. **`deps:`** — Python deps for all the package's code.
2. **`public:`** — an optional public sub-package: `public.files` (files/dirs another package needs to *call* this worker, e.g. `types.py`) and `public.deps` (their deps). A dependency on just the public part uses the `[public]` suffix, e.g. `colligo.models.prompty_v2[public]`. This lets a caller pull in a worker's request/response types without dragging in all its heavy code at deployment. Required whenever the package defines a worker (has a `build.py`).
3. **`exclude:`** — files/dirs excluded from packaging + dependency scanning. `tests/` and `build.py` are excluded by default; append defaults with `...`.

Static analysis (`./m lint`) auto-populates and validates these files. `contrib/` and `third_party/` are exempt (they keep `pyproject.toml`).

## Build system & dependency locking

The build system (see [[wiki/concepts/colligo-dev-workflow]] and [[wiki/sources/colligo-dependency-management]]):

- Registers Python modules, collects/locks **fixed** dependency versions into a single UV lock file, and creates one dev virtualenv.
- Key files: root `pyproject.toml` (`tool.colligo.repo` section), `envs/dev/requirements.lock.txt` (all versions), `envs/dev/known-packages.txt` (import→package map for static analysis), `envs/dev/constraints.txt` (lock inputs), `envs/common/overrides.txt`.
- **Single version of each dependency** across the whole monorepo — a deliberate trade-off (less flexibility, far less operational overhead; everything is testable together). The platform team drives version upgrades; owners must maintain tests. "Frozen environments" (e.g. `envs/frozen/torch-2.1.0.lock.txt`) exist only for staged migrations, and only one is supported at a time.

## Five kinds of dependency

The dependency taxonomy that the architecture is built around:

1. **Monorepo tenants** — code checked in (1.1) or large binaries via a checked-in manifest (1.2, e.g. model weights via LFS/tooling).
2. **Internal Adobe deps** — other teams' code pulled in as subtrees (e.g. Lagrange).
3. **External deps** — as-is (3.1, pip), custom-built no-source-change (3.2), or source-modified subtrees (3.3).
4. **Containerized system deps** — CUDA, OS, provided by the official dev Docker image (kept very few).
5. **Host system deps** — GPU drivers etc., managed by the [[wiki/entities/pluto|Pluto]] compute-platform team.

## Related

- [[wiki/entities/colligo]]
- [[wiki/concepts/colligo-dev-workflow]]
- [[wiki/concepts/colligo-inference]]
- [[wiki/concepts/colligo-managed-services]]
- [[wiki/concepts/colligo-philosophy]]
- [[wiki/sources/colligo-dependency-management]]
