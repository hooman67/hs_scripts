---
type: source
title: Mori in-repo docs (contrib/Mori)
tags: [mori, colligo, contrib, source]
created: 2026-07-05
updated: 2026-07-05
raw: "[[raw/colligo/mori/_provenance.md]]"
sources: ["[[raw/colligo/mori/README.md]]", "[[raw/colligo/mori/collections/foundation_exploration/README.md]]", "[[raw/colligo/mori/collections/foundation_exploration/AGENTS.md]]", "[[raw/colligo/mori/collections/genai_foundation/README.md]]"]
---

# Mori in-repo docs (contrib/Mori)

Summary of the [[wiki/entities/mori|Mori]] documentation that lives in the [[wiki/entities/colligo|Colligo]] monorepo at `contrib/Mori/` — captured 2026-07-05 from commit `8f0cef36dc` (READ-ONLY). Raw copies in `raw/colligo/mori/**`.

## What's there

- **`README.md`** — the canonical one-paragraph definition of Mori: a PyTorch-native training framework with the MoriX accelerator (FSDP/FSDP2), optimized attention (FA2/FA3, context parallelism, distributed attention), and tools (S3, viz, profiling). Lists the component table and the "functional components, not a mega-Trainer" + Strategy-Pattern philosophy. Quick tips: bump Genie version, `killall -9 /opt/venv/bin/python` to evict stuck processes.
- **`aidoc/`** — the framework's doc tree, now **move-notices** pointing to the V3 portal (see [[wiki/sources/mori-docs-portal]]). Landing `index.md` still lists the topic outline (overview, contribution, parallelism, profiler, dependency management, OpenTelemetry, release, internal/pluto_agent).
- **`collections/`** — the real code: per-project training folders (`clio4`, `cliocore`, `foundation_exploration`, `genai_foundation`, `vae_core`, `validate_mori_release`, `tutorials`).
  - **`foundation_exploration/`** — the active **Gen6** collection. Its `AGENTS.md` documents the `morictl` CLI/MCP, launch/debug workflows, branch/PR conventions (`[FE]`/`[Gen6]`), and a large set of `scripts/agent/*.md` runbooks. `docs/training_config_setup.md` + `scripts/agent/config_system.md` are the source for [[wiki/concepts/mori-config]].
  - **`genai_foundation/`** — DiT T2I/T2V training; README documents the **Run.ai** submission flow (legacy scheduler, pre-Pluto) with a `MONITOR_JOBS` watchdog.
- **`mori_training_env/`** — shared training env (`requirements.yaml`, `lock.yaml`, Makefile) — deps materialized with editable installs of the collections.

## Key point

`contrib/Mori/` is mostly **collections + env**; the **core `mori.training` / MoriX library is a separate `ai-platform` repo** installed as a package. See [[wiki/concepts/mori-architecture]].

## Related
- [[wiki/entities/mori]]
- [[wiki/sources/mori-docs-portal]]
- [[wiki/concepts/mori-architecture]] · [[wiki/concepts/mori-config]] · [[wiki/concepts/mori-training-workflow]]
- [[wiki/concepts/colligo-training]] · [[wiki/entities/colligo]]
