---
document_type: guide
children:
  - ./aidoc/video-tutorials.md
  - ./aidoc/development-guides.md
  - ./services/samples/README.md
  - ./aidoc/tenant-pages.md
  - [./private/README.md, "Internal"]
---

# Managed Services (v3)

```{admonition} **v3 is available as a release candidate!**
:class: important

**Release Candidate** — v3 Managed Services is available for early adoption. APIs and workflows may still change before GA. For stable production services, continue with the [v2 Inference Platform](../aidoc/inference-platform/index.md).

<div style="display:flex;gap:8px;margin:4px 0;justify-content:center">
<a href="https://docs.ai.corp.adobe.com/v3/frameworks/inference/serve/aidoc/index.html" style="background:#f0f0f0;color:#666;padding:4px 12px;border-radius:4px;font-size:0.85em;text-decoration:none">Framework</a>
<a href="https://docs.ai.corp.adobe.com/v3/platforms/inference/aidoc/index.html" style="background:#f0f0f0;color:#666;padding:4px 12px;border-radius:4px;font-size:0.85em;text-decoration:none">Platform</a>
<span style="background:#1a73e8;color:#fff;padding:4px 12px;border-radius:4px;font-size:0.85em"><b>Managed Services</b></span>
</div>
```

The Managed Services platform provides an opinionated workflow for developing and deploying inference services in the Colligo monorepo. You write workers, pipelines, and web apps; the platform handles building, packaging, and deploying them to Ethos clusters via Bazel and Argo CD.

## What Stays the Same

If you are coming from v2, the following remain unchanged:

- **Access** — Same access groups and permissions. See [AI Platform Access Control](/aidoc/access-control.md).
- **Support** — Same support channels, on-call rotation, and SLAs. See [Support](/aidoc/inference-platform/support/index.md).
- **Ethos Clusters** — Same dev/stage/prod Ethos environments for deployment.
- **Observability** — Same Grafana, Splunk, and NewRelic dashboards.

## What Changes

- **Worker API** — New worker and pipeline abstractions replace the v2 SDK. Learn more about v3 Worker API [v3 Worker API](https://docs.ai.corp.adobe.com/v3/frameworks/inference/serve/aidoc/api.html).
Inference SDK is no longer a part of the monorepo but is an external library.
This allows it to be yet another versioned dependency defined inside `managed_services/`.

- **Build system** — Bazel replaces the v2 monorepo build toolchain. Every worker, pipeline, and webapp has a generated Bazel target; CI runs `bazel test //...`.
- **Deployment** — No `colligo-deploy` and Helm chart anymore. 
Deployment configuration lives alongside serrvice code in `services/<team>/<project>/deploys/`. `inference_application(...)` + `ethos_deployment(...)` Bazel rules are responsible for generating the necessary Kubernetes manifests and Argo CD configurations, which are then automatically picked up and deployed by Argo CD.

- **Code location** — Services live in `managed_services/services/<team>/<project>/`, not in the v2 `models/` tree. 
We keep `managed_services/` inside the monorepo to keep the same access control, but it is detached from v2 and can have its own dependencies, build system, and release cadence.

- **Code owner groups and PR approvals** - we use new code owner setup in `managed_services/`.
See details in the [v3 Code Reviews](https://docs.ai.corp.adobe.com/v3/platforms/dev_tools/aidoc/code-review.html) section.
Slack review notifications are sent automatically when a PR is ready — all requested teams are
listed by name. To also ping a specific team member, enable **Review assignment** (load balance
or round robin) on the corresponding GitHub team — see [Code Review: Tutorials](/aidoc/code-review/tutorials.md).

## Getting Started

### Developement Guides Video Tutorials

- [Video Tutorials](./aidoc/video-tutorials.md) - step-by-step walkthroughs for environment setup, creating workers, pipelines, web apps, migrating from v2, and deployment to Ethos.
- [Development Guides](./aidoc/development-guides.md) — CLI and code reference for creating workers, adding deps, detached apps etc.

### Code Samples

The [sample projects](./services/samples/README.md) form a progressive learning path.

- [A. Worker in managed services](./services/samples/A/README.md): Writing a compute worker
- [B. Pipeline in managed services](./services/samples/B/README.md): Writing a pipeline worker
- [C. Web app in managed services](./services/samples/C/README.md): Writing a web application
- [D. Package & deploy](./services/samples/D/README.md): Packaging and deploying an application
- [E. Production service (FLUX)](./services/samples/E/README.md): A real-world service (text-to-image)
- [F. Quick deploy escape hatch](./services/samples/F/README.md): Custom/cutting-edge deps

## Code Structure

The managed services ecosystem follows a standardized structure:

```
managed_services/
├── MODULE.bazel           # Bazel module definition with platform dependency
├── BUILD                  # Root build file with linting/structure rules
├── requirements.in        # Python dependencies
├── requirements.*.txt     # Lock files (auto-generated)
├── services/              # User service code
│   ├── <team>/
│   │   └── <project>/
│   │       ├── workers/   # Compute workers
│   │       ├── pipelines/ # Pipeline workers
│   │       ├── webapps/   # Web applications
│   │       └── deploys/   # Deployment configurations
│   └── samples/           # Sample projects (tutorials)
└── cloud/                 # Generated Kubernetes manifests (do not edit)
```
