---
type: concept
title: Mori Dependency Management
tags: [mori, dependencies, uv, lock, cuda, pytorch, s3]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/mori-docs.md]]", "[[raw/colligo/mori/collections/foundation_exploration/AGENTS.md]]", "[[raw/colligo/mori/mori_training_env/requirements.yaml]]"]
---

# Mori Dependency Management

How [[wiki/entities/mori|Mori]] pins and ships Python dependencies — a **pre-compiled, version-locked** model that treats deps (and CUDA/OS versions) as code.

## Model: dependencies as code, materialized to S3

Packages are built as artifacts and **uploaded to S3 before training**, decoupling deps from the Docker image (consistency without bundling everything into the container).

- **`requirements.yaml`** — declares dependency **constraints** (the source of version constraints).
- **`lock.yaml`** — the materialized dep set: full transitive audit trail + CUDA version + OS version constraints + S3 path references. Being a file, it's **diffable across git commits** so regressions are detectable — "makes dependencies part of the code."

**Workflow:** change deps → `make lock` → commit `lock.yaml` (and `uv.lock` where present) — always commit lock files together with the change. At training startup, `make env` creates a venv at `/mnt/localssd/mori-ven` and downloads the pre-compiled deps from S3.

## PyTorch / CUDA dependency groups

Multiple torch/cuda combos are optional dependency groups in `pyproject.toml`, e.g. **`torch271-cu128`** = PyTorch 2.7.1 + CUDA 12.8 (torch, flash-attn, flashattn-hopper, st_attn, deep-gemm, magi_attention, sageattention). Install: `pip install mori[torch271-cu128]`. Pin exact versions incl. build tags (`+cu128`).

## Rules

- Version constraints go in `requirements.yaml`, **not** `pyproject.toml` (except the dependency groups).
- Deps, CUDA, and OS versions are treated as code — use **separate branches** for different versions.
- This differs from the monorepo-wide single-version policy: `contrib/` training codebases keep independent dep workflows (see [[wiki/concepts/colligo-training]]); contrib packages use plain `pyproject.toml`.

## Related
- [[wiki/entities/mori]]
- [[wiki/concepts/mori-architecture]]
- [[wiki/concepts/mori-training-workflow]]
- [[wiki/concepts/colligo-training]] · [[wiki/concepts/colligo-dev-workflow]]
