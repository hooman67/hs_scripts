# Provenance — raw/colligo/mori

Immutable copies of in-repo Mori documentation, ingested 2026-07-05.

- **Source repo:** `/Users/hshariati/colligo` (Colligo monorepo), path `contrib/Mori/`
- **Commit:** `8f0cef36dc [FFP-97711] CD ConfigMap StateStore (#27861)` (branch `main`, READ-ONLY)
- **What was copied:** the `contrib/Mori/` READMEs and `aidoc/` pages, plus the highest-signal
  collection docs (foundation_exploration + genai_foundation) that still contain real content.

## Notes
- All of `contrib/Mori/aidoc/*.md` are now **move-notices** — the Training Framework docs
  migrated to the AI Platform V3 portal (`https://docs.ai.corp.adobe.com/v3/frameworks/training/`).
  They are copied here for the record; the actual content is in `raw/mori-docs.md`.
- `contrib/Mori` in the monorepo mostly holds **collections** (per-project training folders that
  use the Mori library) + a shared `mori_training_env`. The core `mori.training` / `morix`
  library is developed in a separate standalone `ai-platform` repo and installed as a package.
- Not copied (skimmed only, large / code-heavy): the full `collections/**` trees
  (`clio4`, `cliocore`, `vae_core`, `validate_mori_release`, `tutorials`) and the many
  `scripts/agent/*.md` runbooks under foundation_exploration.

## Files
- `README.md` — top-level Mori README (framework definition + quick tips)
- `aidoc/` — landing index + move-notices (overview, contribution, parallelism, profiler,
  dependency_management, open_telemetry, release, internal/pluto_agent)
- `collections/genai_foundation/README.md` — Run.ai job submission for DiT T2I/T2V training
- `collections/foundation_exploration/README.md` + `AGENTS.md` — the active Gen6 collection,
  its agent workflows, and `morictl` tooling
- `collections/foundation_exploration/docs/training_config_setup.md` — sequence balancer /
  KnapFormer / data layout config guidance
- `collections/foundation_exploration/scripts/agent/config_system.md` — config validation workflow
- `mori_training_env/requirements.yaml` — shared training env deps
