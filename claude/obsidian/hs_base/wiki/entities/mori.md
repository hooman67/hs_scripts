---
type: entity
title: Mori (Training Framework)
tags: [colligo, training, mori, morix, firefly, genai, pytorch, adobe]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/colligo/mori/README.md]]", "[[raw/mori-docs.md]]", "[[raw/colligo/mori/collections/foundation_exploration/README.md]]"]
---

# Mori (Training Framework)

**Mori** is Adobe Firefly's **PyTorch-native distributed training framework** — the second-generation training platform for large-scale imaging and video GenAI foundation models (DiT text-to-image / text-to-video, VAEs, etc.). It is the "Training Framework" referenced by [[wiki/concepts/colligo-training|Colligo training]] and runs its jobs on [[wiki/entities/pluto|Pluto]].

Mori aims to be *simple to use yet powerful*: instead of one giant `Trainer` class, it gives you **re-usable functional components** so you can take a PyTorch-101 training script and add FSDP, sequence balancing, S3 checkpointing, and profiling with a few lines. Its accelerator, **MoriX**, uses the **Strategy Pattern** so new parallelism/training strategies plug in as `Plugin`s without rewriting workflows.

## Components

| Component | Description |
|---|---|
| `mori.training` | Core distributed-training package. |
| `mori.training.morix` (**MoriX**) | Lightweight training accelerator with a common interface across training strategies; new strategies = new `Plugin`. Currently supports FSDP and FSDP2. |
| `mori.training.tools` | Common tools for training jobs — HTML/report creation, S3 storage/checkpointing. |
| `mori.models` | Firefly, research, and common third-party models with configurable optimization. |
| `collections/` | Per-project training folders that *use* `mori.training`; each has clear ownership. Experimental features are proven here before upstreaming into `mori.training` / `mori.models`. |

See [[wiki/concepts/mori-architecture]] for the repo shape and where the core library vs. the collections live.

## What it provides

- **Parallelism** — FSDP / FSDP2, context (sequence) parallelism, and in-house distributed attention, plus optimized attention (FA2/FA3, Context Parallelism). See [[wiki/concepts/mori-parallelism]].
- **Sequence balancing** — the KnapFormer-based balancer that redistributes variable-length sequences across GPUs to minimize imbalance. See [[wiki/concepts/mori-config]].
- **S3 checkpointing** — save/resume checkpoints on S3 via an experiment manager. See [[wiki/concepts/mori-checkpointing]].
- **On-demand profiler + OpenTelemetry** — dynamic PyTorch/CUDA-memory tracing and telemetry. See [[wiki/concepts/mori-observability]].
- **Pluto integration** — a [[wiki/concepts/mori-pluto-agent|Pluto Agent SDK]] lets the in-job framework talk to the platform (backs `aip job run-tracing`, snapshots, etc.).
- **Dependency management** — pre-compiled, version-locked deps materialized to S3. See [[wiki/concepts/mori-dependency-management]].

## Training workflow (high level)

Write/adapt a training script → pick a config (YAML) → validate locally → launch on Pluto (`torchrun` / `train.sh` / a collection CLI like `morictl`) → checkpoints stream to S3 → monitor + profile. Full detail in [[wiki/concepts/mori-training-workflow]].

## Relationship to Colligo, contrib, and Pluto

- Mori lives in the [[wiki/entities/colligo|Colligo]] monorepo under **`contrib/`** (`contrib/Mori/`), which is where research/training codebases keep **independent workflows** — see [[wiki/concepts/colligo-training]]. In the monorepo, `contrib/Mori/` mostly holds the **collections** + a shared `mori_training_env`; the **core `mori.training` / MoriX library is developed in a separate standalone `ai-platform` repo** and installed as an editable/pip package.
- The heavy training runs on **[[wiki/entities/pluto|Pluto]]** (GPU scheduling, quotas, storage, observability). Mori talks back to Pluto via the [[wiki/concepts/mori-pluto-agent|Pluto Agent SDK]]; the [[wiki/concepts/pluto-job-lifecycle|Pluto job lifecycle]] governs how jobs schedule/run and the [[wiki/concepts/pluto-cli-sdk|`aip` CLI]] triggers in-job actions.
- Predecessor: `contrib/AdobeDiffusion/` (first-generation training). Some collection READMEs still reference **Run.ai** submission (the older scheduler) alongside newer Pluto/`morictl` flows.

> [!note] Docs live on the V3 portal
> The in-repo `contrib/Mori/aidoc/*.md` pages are now just **move-notices**. The real docs are at
> `https://docs.ai.corp.adobe.com/v3/frameworks/training/mori/aidoc/` (captured in [[raw/mori-docs.md]]).

## Related
- [[wiki/concepts/mori-architecture]]
- [[wiki/concepts/mori-training-workflow]]
- [[wiki/concepts/mori-parallelism]]
- [[wiki/concepts/mori-config]]
- [[wiki/concepts/mori-checkpointing]]
- [[wiki/concepts/mori-observability]]
- [[wiki/concepts/mori-pluto-agent]]
- [[wiki/concepts/mori-dependency-management]]
- [[wiki/concepts/colligo-training]] · [[wiki/entities/colligo]] · [[wiki/entities/pluto]]
- [[wiki/sources/mori-repo]] · [[wiki/sources/mori-docs-portal]]
