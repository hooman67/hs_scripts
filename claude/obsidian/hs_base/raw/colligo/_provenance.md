---
type: source
title: Colligo Raw Docs Provenance
tags: [colligo, provenance, raw]
created: 2026-07-04
updated: 2026-07-04
---

# Colligo Raw Docs Provenance

Immutable raw documentation harvested from the Colligo (AI Platform) monorepo.

- **Source repo:** https://github.com/Adobe-Firefly/colligo
- **Branch:** `main`
- **Commit:** `8f0cef36dc2cadbf8cdc17c38934c82c4263aee5` (`[FFP-97711] CD ConfigMap StateStore (#27861)`)
- **Copied:** 2026-07-04
- **Local clone:** `/Users/hshariati/colligo`

## Immutability

These files are a point-in-time copy of the repo's instructional/doc markdown. **Do not edit them.** Wiki pages under `wiki/*colligo*` synthesize from these; if the repo changes, re-harvest rather than editing here.

## Scale of the source corpus

The repo contains ~1,741 `.md` files, including 84 `AGENTS.md` and 58 `CLAUDE.md` files (per-directory agent guidance), 586 README-ish files, and a large `aidoc/` documentation tree that is compiled and published to `https://docs.ai.corp.adobe.com`. Only a curated core set (26 files) was copied here — the top-level agent/onboarding docs plus the key inference/monorepo/dependency/training landing pages. A future ingest can widen coverage (see the Colligo entity page's "Uncovered" section).

## Files copied (relative paths preserved)

- `AGENTS.md`, `CLAUDE.md`, `README.md` — root (AGENTS.md and CLAUDE.md are identical)
- `aidoc/root.md`, `aidoc/philosophy.md`, `aidoc/AGENTS.md`
- `aidoc/inference-platform/index.md` + `framework/{index,worker,endpoints}.md`
- `aidoc/monorepo/index.md`
- `aidoc/dependency-management/{overview,build-system}.md`
- `pylibs/colligo/sdk/aidoc/index.md` — Inference SDK
- `pylibs/AGENTS.md`, `models/AGENTS.md`, `pylibs/colligo/pluto/{AGENTS.md,sdk/AGENTS.md}`
- `contrib/Mori/aidoc/{index,overview}.md` — Training Framework (Mori)
- `managed_services/{README.md,AGENTS.md,CLAUDE.md}` — Inference v3
- `tools/AGENTS.md`, `envs/AGENTS.md`, `docker/AGENTS.md`

## Related

- [[wiki/entities/colligo]]
