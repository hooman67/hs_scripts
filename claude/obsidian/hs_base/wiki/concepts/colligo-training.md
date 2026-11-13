---
type: concept
title: Colligo Training (Mori & training codebases)
tags: [colligo, training, mori, adobediffusion, genai, firefly]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/colligo/contrib/Mori/aidoc/index.md]]", "[[raw/colligo/contrib/Mori/aidoc/overview.md]]", "[[raw/colligo/aidoc/monorepo/index.md]]"]
---

# Colligo Training (Mori & training codebases)

The model-**training** side of [[wiki/entities/colligo|Colligo]]. Training code lives under `contrib/` — research/training codebases that reside in the monorepo but keep **independent workflows** (contact the owners directly rather than assuming platform conventions).

> [!note] Docs moved to V3
> The **Training Framework (Mori)** documentation has moved out of the in-repo `aidoc/` to the AI Platform V3 docs site: `https://docs.ai.corp.adobe.com/v3/frameworks/training/`. The in-repo `contrib/Mori/aidoc/*.md` pages are now just move-notices, so the detail below is the topic outline they used to cover — go to the V3 site for specifics.

## Training codebases in `contrib/`

- **`contrib/Mori/`** — the **Training Framework** ("MoriX"): second-generation imaging and video GenAI models and training code. Topic areas: getting started, contribution guide, **parallelism strategies**, an **on-demand profiler**, dependency management (contrib packages use plain `pyproject.toml`), **OpenTelemetry** instrumentation, and install/release.
- **`contrib/AdobeDiffusion/`** — first-generation imaging and video GenAI models and training code.
- **`contrib/eval_science/`** — Evaluation Science model-evaluation frameworks (@bylinski's team).
- Other contrib training/research: `autoX`, `autogen`, `image_model_metrics`, `vbench`, `whispurr`, `kaizen`, etc.

## Where training runs

Training code is not yet a first-class monorepo "tenant" the way inference workers are (single-version dependency policy has historically bent for training vs inference). The heavy lifting runs on **[[wiki/entities/pluto|Pluto]]**, the compute platform: Pluto handles GPU/CPU job scheduling, quotas, interactive sessions, and training-job observability, and it manages host-level system deps (GPU drivers). Mori integrates with Pluto via a Pluto Agent SDK. See [[wiki/concepts/pluto-job-lifecycle]] for how those jobs schedule and run, and [[wiki/concepts/colligo-pluto-sdk]] for the SDK/CLI shipped from Colligo.

Related training model packages also appear under `models/colligo/models/firefly/` (e.g. `brewmaster`, `clio_tyom`), each with their own AGENTS guidance.

## Related

- [[wiki/entities/colligo]]
- [[wiki/entities/pluto]]
- [[wiki/concepts/colligo-pluto-sdk]]
- [[wiki/concepts/pluto-job-lifecycle]]
- [[wiki/concepts/colligo-architecture]]
- [[wiki/concepts/colligo-inference]] — the serving counterpart
