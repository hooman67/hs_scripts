---
type: concept
title: Mori Architecture
tags: [mori, architecture, morix, collections, pytorch, training]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/colligo/mori/README.md]]", "[[raw/mori-docs.md]]", "[[raw/colligo/mori/_provenance.md]]"]
---

# Mori Architecture

How [[wiki/entities/mori|Mori]] is put together: a small core library, a pluggable accelerator, and many per-project "collections" that consume it.

## Layered structure

1. **Core library** (`mori.training`, `mori.training.morix`, `mori.training.tools`, `mori.models`) — the framework itself, developed in a **standalone `ai-platform` repo** and installed as an editable/pip package (`pip install mori[torch271-cu128]` or `pip install --no-deps -e <mori_repo_root>`).
2. **Collections** (`contrib/Mori/collections/**` in the [[wiki/entities/colligo|Colligo]] monorepo) — per-project training folders that import the core library and implement concrete training logic. Each has clear ownership so teams don't block each other; experimental features are proven in a collection before **upstreaming** to `mori.training` / `mori.models`.

This is why `contrib/Mori/` in the monorepo is mostly collections + a shared `mori_training_env`, not the core code.

## MoriX = accelerator + Strategy Pattern

**MoriX** (`mori.training.morix`) is a lightweight accelerator that exposes a **common interface across training strategies**. New strategies (parallelism schemes, etc.) are added by implementing a new **`Plugin`** — e.g. `FSDP2Plugin` at `mori.training._dev.plugin.fsdp2_plugin.FSDP2Plugin`. This Strategy-Pattern design is deliberate: GenAI moves fast, so the framework absorbs new training algorithms without rewriting workflows. See [[wiki/concepts/mori-parallelism]].

## Design philosophy — functional components, not a mega-trainer

Mori's building blocks are **re-usable functional components**, not one giant `Trainer` class. You can take an ordinary PyTorch training script and add FSDP + S3 checkpointing with a few lines. Entry point `train.sh` launches distributed training via `torchrun` or the custom `mori.training.distributed.torchrun_handler`.

## Collections in the monorepo

`contrib/Mori/collections/`: `clio4`, `cliocore`, `foundation_exploration` (the active **Gen6** collection), `genai_foundation`, `vae_core`, `validate_mori_release`, `tutorials`, `scripts`. `cliocore` further breaks into `core_models/` (autoencoders, cldm, encoders, latent_upsampler, prior, unets), `ait_models/` (DiT, unets), `diffusion_core`, `nas`, etc. Configs are YAML files per experiment (e.g. `configs/genrender6/prod/<config>.yaml`, `filix2_*`). Each collection commonly ships its own `AGENTS.md`/`CLAUDE.md`, `Makefile`, `pyproject.toml`, and lock files.

## Related
- [[wiki/entities/mori]]
- [[wiki/concepts/mori-parallelism]]
- [[wiki/concepts/mori-config]]
- [[wiki/concepts/mori-training-workflow]]
- [[wiki/concepts/mori-dependency-management]]
- [[wiki/concepts/colligo-training]] · [[wiki/entities/colligo]]
