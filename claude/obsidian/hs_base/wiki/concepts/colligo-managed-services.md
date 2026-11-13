---
type: concept
title: Colligo Managed Services (Inference V3)
tags: [colligo, inference, v3, bazel, managed-services, ethos, argocd]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/colligo/managed_services/README.md]]", "[[raw/colligo/managed_services/AGENTS.md]]", "[[raw/colligo/aidoc/inference-platform/index.md]]"]
---

# Colligo Managed Services (Inference V3)

The next-generation inference platform inside [[wiki/entities/colligo|Colligo]] — an **opinionated, Bazel-based workflow** for developing and deploying inference services. As of the ingested commit it is a **release candidate** (APIs may change; V2 [[wiki/concepts/colligo-inference|Inference Platform]] remains the stable production path).

You write workers, pipelines, and web apps; the platform handles building, packaging, and deploying them to Ethos clusters via Bazel + Argo CD.

## What stays the same as V2

- **Access** — same access groups/permissions.
- **Support** — same channels, on-call, SLAs.
- **Ethos clusters** — same dev/stage/prod environments.
- **Observability** — same Grafana/Splunk/NewRelic.

## What changes vs V2

- **Worker API** — new worker/pipeline abstractions replace the V2 SDK. The Inference SDK is no longer in the monorepo; it becomes an external, versioned dependency defined inside `managed_services/`.
- **Build system** — **Bazel** replaces the V2 `./m` monorepo toolchain. Every worker/pipeline/webapp gets a generated Bazel target; CI runs `bazel test //...`.
- **Deployment** — no more `colligo-deploy` + Helm. Deployment config lives beside service code in `services/<team>/<project>/deploys/`. `inference_application(...)` + `ethos_deployment(...)` Bazel rules generate the k8s manifests + Argo CD config, which Argo CD auto-syncs.
- **Code location** — services live in `managed_services/services/<team>/<project>/`, not the V2 `models/` tree. `managed_services/` is a separate Bazel workspace kept in-repo for shared access control but detached from V2, with its own deps, build system, and release cadence.
- **Code owners** — a new code-owner setup with automatic Slack review notifications.

## Structure

```
managed_services/
├── MODULE.bazel            # Bazel module (depends on the platform)
├── BUILD                   # root build + linting/structure rules
├── requirements.in         # Python deps  (requirements.*.txt are generated locks)
├── services/<team>/<project>/
│   ├── workers/            # compute workers
│   ├── pipelines/          # pipeline workers
│   ├── webapps/            # web applications
│   └── deploys/            # deployment configs
├── services/samples/       # progressive tutorial projects A–F
└── cloud/                  # generated k8s manifests (do not edit)
```

Sample learning path: **A** worker → **B** pipeline → **C** web app → **D** package & deploy → **E** real production service (FLUX text-to-image) → **F** quick-deploy escape hatch for custom/cutting-edge deps.

## Related

- [[wiki/concepts/colligo-inference]] — the stable V2 platform
- [[wiki/concepts/colligo-inference-sdk]]
- [[wiki/concepts/colligo-architecture]]
- [[wiki/concepts/foundry-endpoint-email-allowlist]] — allowlist a customer email on an endpoint via a deploy configmap
- [[wiki/entities/colligo]]
