---
type: source
title: ai-platform repo docs (V3)
tags: [ai-platform, v3, inference, deployment, source, firefly]
created: 2026-07-05
updated: 2026-07-05
raw: "[[raw/ai-platform/_provenance.md]]"
sources: ["[[raw/ai-platform/_provenance.md]]"]
---

# ai-platform repo docs (V3)

Distilled summary of the documentation ingested from the **ai-platform** repo
(`github.com/Adobe-Firefly/ai-platform`, branch `main`, commit `127e0a0e4a`, copied 2026-07-05) —
Firefly's standalone AI-platform repo, the **"V3"** model-deployment stack. Raw copies live under
`raw/ai-platform/` (see [[raw/ai-platform/_provenance.md|provenance]]). Repo scale: ~7,322 files,
**539** docs; 24 V3-deployment-focused docs copied.

## What the sources cover

- **Root** (`README.md`, `AGENTS.md`, `platforms/dev_tools/aidoc/code-structure.md`) — repo is a set
  of self-contained "virtual repos"; docs are the only shared root artifact (Sphinx via `./gtools docs
  build`); the models/frameworks/platforms layering convention.
- **Inference platform** (`platforms/inference/`) — the `@platforms_inference` Bazel module.
  `aidoc/index.md` is the big-picture V3 overview (three layers, three deployment paths, sample
  progression 1–10, "why v3", v2→v3 status). `aidoc/deployment/*` documents `inference_application` /
  `ethos_deployment`, the GitOps flow, runtime envs, and the `ai-inference-chart` values reference
  (worker/http/watchdog deployments, GPU hardware, Oshiya/KEDA autoscaling, ingress).
  `aidoc/internal/dev-workflows.md` has the `release/inference/vX.Y.Z` release + versioning process,
  editable-install-from-source, and test-env-branch pre-merge testing. `bazel_101.md` is a primer.
- **Inference framework** (`frameworks/inference/serve/`) — `aidoc/index.md` (building blocks),
  `aidoc/api.md` (the full public API: Worker/WebApp/ServeConfig/depends_on/Binary/Tensor/run modes/
  config), samples (a_basic, flux), `migration/README.md` (temporary Adobe-service wrappers).
- **Model hub** (`models/`) — `aidoc/index.md`, `hub/README.md` (packaging `models.<name>`;
  CI currently disabled).

## Key facts extracted

- V3 = **framework (wheel) + platform (Bazel build/deploy) separated**; user services + deploy config
  live in **colligo/managed_services**, which consumes `@platforms_inference` via a
  `release/inference/vX.Y.Z` git tag. So the "V3 stack" spans two repos.
- Deploy flow: BUILD (`inference_application` + `ethos_deployment`) → `smake lint/argo-sync` renders
  `k8s_manifest.yaml` → `argo_sync` copies to `cloud/` → merge → CI syncs to `colligo-v3-deploy` →
  **Argo CD** applies to **Ethos**. Renders in 1–2 s; manifests reviewable in the PR diff.
- Runtime is unchanged from V2 in spirit: workers over Redis queues, per-process GPU isolation; V3
  vendors V2 internals behind a shim layer.
- Status: **pre-1.0** (shared framework+chart **v0.5.11**, 2026-06-26). V2 still the stable path.
- Pluto code physically lives here (`platforms/pluto/`) but is covered by the Pluto pages.

## Synthesized into

- [[wiki/entities/ai-platform-repo]] — the hub entity
- [[wiki/concepts/v3-inference-framework]]
- [[wiki/concepts/v3-deployment]]
- [[wiki/concepts/v3-models-hub]]
- [[wiki/concepts/v3-vs-v2]]

## Related

- [[wiki/concepts/colligo-managed-services]] · [[wiki/concepts/colligo-inference]] · [[wiki/concepts/colligo-inference-infra]]
- [[wiki/entities/colligo]] · [[wiki/entities/pluto]]
- [[wiki/concepts/ai-platform-overview]]
- [[wiki/sources/ai-platform-docs]] — the earlier (colligo-side) portal source
