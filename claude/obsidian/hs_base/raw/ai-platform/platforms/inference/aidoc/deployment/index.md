---
children:
    - ./gitops-framework.md
    - ./inference-chart.md
    - ./ingress-chart.md
    - ./agents/claude-agent-sdk.md
    - ./agents/langgraph.md
---

# Deployment API

The Deployment API provides Bazel rules and Python charts for deploying applications to Ethos clusters via GitOps (Argo CD).

## Overview

| Page | Description |
|------|-------------|
| [GitOps Framework](./gitops-framework.md) | Bazel rules for packaging and deploying: `ethos_deployment`, `k8s_chart_values`, runtime envs |
| [Inference Chart](./inference-chart.md) | `ai-inference-chart` values reference: hardware, autoscaling, ingress, logging, runtime config |
| [Ingress Chart](./ingress-chart.md) | `ai-ingress-chart` standalone ingress for any Ethos deployment |
| [Claude Agent SDK](./agents/claude-agent-sdk.md) | Single-pod agent chart: ConfigMap, PodMonitor, termination grace period |
| [LangGraph](./agents/langgraph.md) | Multi-pod agent chart: apiServer + queue + Postgres + Redis |

## Agent Charts

The inference platform exposes two Python charts for deploying LLM agents built with `frameworks.agent`. Both are available as public Bazel targets in `@platforms_inference` and plug into `ethos_deployment(...)` the same way.

| Chart | Target | Shape | When to use |
|---|---|---|---|
| **`claude-agent-sdk-chart`** | `@platforms_inference//:claude-agent-sdk-chart` | Single pod | Simple agents; Slack bots; CPU-only workloads where you don't need durable checkpointing |
| **`langgraph-chart`** | `@platforms_inference//:langgraph-chart` | apiServer + queue + Postgres + Redis | Agents that need durable state, LangSmith tracing, or horizontal queue scaling |
