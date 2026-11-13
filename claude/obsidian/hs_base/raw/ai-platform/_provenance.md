---
type: provenance
title: ai-platform raw sources — provenance
created: 2026-07-05
---

# ai-platform — raw source provenance

Immutable snapshot of documentation copied from the **ai-platform** repo (Adobe Firefly's
standalone AI-platform repo, aka **"V3"** — the current model-deployment stack).

- **Repo:** https://github.com/Adobe-Firefly/ai-platform
- **Branch:** `main`
- **Commit:** `127e0a0e4a38d4ea89854721c849af6841a5dcae`
  (`chore(pluto): bump dev2 image tag to 1.5.0-c9e0972b (#2590)`)
- **Cloned / copied:** 2026-07-05
- **Scope of copy:** documentation only (`.md`), focused on the V3 inference /
  model-deployment story (`frameworks/inference/`, `platforms/inference/`, `models/`).
  Code was read for shape but not copied.
- **Repo scale at this commit:** ~7,322 tracked files; **539** markdown/README/AGENTS docs.

These files are a point-in-time copy and are treated as **immutable**. The wiki pages
under `wiki/` synthesize from them. Re-clone the repo to refresh.

## Files copied (24)

Top-level: `README.md`, `AGENTS.md`, `platforms/dev_tools/aidoc/code-structure.md`

Inference **platform** (`platforms/inference/`): `README.md`, `AGENTS.md`,
`aidoc/index.md`, `aidoc/bazel_101.md`, `aidoc/changelog.md`,
`aidoc/deployment/{index,gitops-framework,inference-chart}.md`,
`aidoc/internal/dev-workflows.md`.

Inference **framework** (`frameworks/inference/`): `README.md`, `serve/README.md`,
`serve/AGENTS.md`, `serve/aidoc/{index,api}.md`, `serve/aidoc/samples/index.md`,
`serve/migration/README.md`, `serve/samples/a_basic/README.md`,
`serve/samples/a_basic/scripts/C_cloud_run.md`, `serve/samples/flux/README.md`.

Model hub (`models/`): `aidoc/index.md`, `hub/README.md`.
