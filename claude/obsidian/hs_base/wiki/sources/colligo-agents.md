---
type: source
title: "Source: Colligo root AGENTS.md / CLAUDE.md"
tags: [colligo, source, agents, conventions]
created: 2026-07-04
updated: 2026-07-04
ingested: 2026-07-04
raw: "[[raw/colligo/AGENTS.md]]"
sources: ["[[raw/colligo/AGENTS.md]]", "[[raw/colligo/CLAUDE.md]]", "[[raw/colligo/README.md]]"]
---

# Source: Colligo root AGENTS.md / CLAUDE.md

Distilled summary of [[wiki/entities/colligo|Colligo]]'s top-level agent guidance. The root `AGENTS.md` and `CLAUDE.md` are **byte-identical**; `README.md` is a one-liner pointing to `docs.ai.corp.adobe.com`.

## Key content

- **Identity:** "AI Platform monorepo ('V2'): shared Python libraries, ML models, inference services, and build tooling."
- **Boundaries:** never modify `third_party/`, `uv.lock`/`*.lock`, or generated files (`*_pb2*.py(i)`, `registry/applications.yaml`); never use plain `assert` in production (use `validation_assert`/`runtime_assert` from `colligo.base.exceptions`).
- **Repo map:** `pylibs/` (colligo.* libs, incl. `pluto/` compute + `rhode/` inference internals), `models/`, `managed_services/` (V3, separate Bazel), `contrib/Mori/` (training), `docker/`, `tools/` (`./m`), `envs/`, `aidoc/`, `data/`, `registry/`. Docs are co-located in `aidoc/` dirs; `aidoc/root.md` is the topic index.
- **Doc routing table:** Inference → `aidoc/inference-platform/index.md`; Compute/Pluto → `pylibs/colligo/pluto/aidoc/index.md`; Managed Services → `managed_services/README.md`; Deployment → `colligo-deploy` (separate repo `git.corp.adobe.com/firefly/colligo-deploy`, holds Helm + Ethos Flex values Argo CD syncs).
- **Commands:** the `./m` CLI (`deps.create`, `source m`, `deps.sync`, `lint [--check|--paths]`) + `pytest`.
- **Coding standards:** Python 3.10+, strict types, absolute imports only, Adobe copyright header, Google-style docstrings; pytest excludes `contrib/`, `third_party/`, `managed_services/`, `vendor/`, `_build/`.
- **PR format:** JIRA prefix in brackets (`[FFP-123]` / `[NOJIRA]`); body follows `.github/PULL_REQUEST_TEMPLATE.md`.

## Related

- [[wiki/entities/colligo]]
- [[wiki/concepts/colligo-architecture]]
- [[wiki/concepts/colligo-dev-workflow]]
