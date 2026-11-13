# Inference Platform Tools

The inference offering has three layers:

1. **Inference Framework** (`pip install frameworks.inference`) — standalone Python library for workers, pipelines, web apps. Lives at `../../frameworks/inference/serve/`.
2. **Inference Platform** (this folder) — Bazel build rules, k8s deployment automation, capacity planning. Produces the `@platforms_inference` Bazel module.
3. **Managed Services** — opinionated user-facing ecosystem that consumes both: https://github.com/Adobe-Firefly/colligo/tree/main/managed_services

Documentation convention:
- `README.md` here is the **user-facing entry point** (big picture, architecture, deployment paths).
- `aidoc/internal/` is for **internal platform developers** only.

This folder contains all inference platform tools, libraries, and services needed for the managed services ecosystem.

## Some important notes

- One deliverable from this folder is a Bazel module that can be used by a downstream managed services repository.
- Anything exported from this module should either be at the root BUILD or defs.bzl (depending on if it is a label or macro/rule).
- To ensure everything works, we need to pass `./bazel test ...` in this folder.
- If you modify BUILD files, requirements.in, or change `ethos_deployment(...)` charts, bazel test can fail due to out of date auto-generated files or unformatted files. `make lint` tries to fix those.
    + `make lint` also tries to fix any file formatting.

## Documentation

- Documentation uses sphinx, you can look at .md files directly, or use "./gtools docs build" to render the final sphinx doc (more info at in the AGENTS.md at the root of the repo). When reading a page, also pay attention to its child pages.
- The user facing documentation is at: @./README.md
- The internal documentation is at: @./aidoc/internal/index.md

## Pre-PR checklist

- `make lint` passes
- `./bazel test ...` passes
- If you modified `bazel_infra/gitops/inference_renderer/api.py` or `bazel_infra/gitops/agent_renderer/api.py`, run the `api-docs` skill to regenerate API documentation.

## End user of this product

- The managed services folder that consumes most of the deliverables of this repo is at https://github.com/Adobe-Firefly/colligo/tree/main/managed_services

