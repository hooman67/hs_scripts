---
children:
    - ./aidoc/internal/dev-workflows.md
    - ./bazel_infra/README.md
---

# Internal

This section is for **internal platform developers** working on the inference platform itself.

If you are a user of the managed services platform looking to deploy inference services, see the [main documentation](./aidoc/index.md) and [Deployment API](./aidoc/deployment/index.md).

## Overview

The inference platform is built on several key components:

### Code Structure

- **[bazel_infra](./bazel_infra/README.md)**: Build utilities for managing the Bazel infrastructure (packaging, deployment) for managed user code. This results in a versioned Bazel module named `platforms_inference`.
- **[bazel_infra/gitops/agent_renderer/](./bazel_infra/gitops/agent_renderer/)**: The `claude-agent-sdk-chart` Python chart for LLM agents built with `frameworks.agent`. Renders the ethos-deployment chart with agent-specific defaults (CPU sizing, probes, pre-reserved metrics ports), emits the runtime ConfigMap and PodMonitor, and computes the pod's termination grace period from the agent's `session_timeout_seconds`. See [Agent Deployment aidoc](./aidoc/deployment/index.md#agent-charts).
- **[editable_install](./editable_install/)**: Shims for using the inference framework from source (for platform developers only).

### Ethos Infrastructure

The `ethos/` folder contains infrastructure registration using the GitOps API:

- **[Clusters](./ethos/clusters/BUILD)**: Registered Ethos clusters
- **[Envs](./ethos/envs/BUILD)**: Registered Ethos environments
- **[Regions](./ethos/regions/BUILD)**: Registered Ethos regions
- **[Runtime Envs](./ethos/runtime_envs/BUILD)**: Cluster + env combinations
- **[Shared Charts](./ethos/shared_charts/BUILD)**: Shared charts for all tenants

### Module Export

The platform module is exported as `@platforms_inference` and can be used in the managed services ecosystem. Public APIs are exposed in:

- [BUILD](./BUILD): For targets
- [defs.bzl](./defs.bzl): For macros and rules

## Using Platform from Source

See [Dev Workflows - Using inference platform and framework from source](./aidoc/internal/dev-workflows.md#using-inference-platform-and-framework-from-source-in-managed-services-ecosystem).

## Development Workflows

See [Dev Workflows](./aidoc/internal/dev-workflows.md) for debugging, publishing, and development processes.
