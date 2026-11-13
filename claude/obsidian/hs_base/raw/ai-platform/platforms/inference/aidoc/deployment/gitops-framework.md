---
sectnum: false
---

# GitOps Framework

These are **Bazel** APIs within your **BUILD** files, relevant to using the "managed inference platform". For getting started with the managed services ecosystem, see the [Managed Services README](https://docs.ai.corp.adobe.com/managed_services/README.html) in the colligo repository.

This replaces the [colligo-deploy](https://github.com/Adobe-Firefly/colligo/tree/main/managed_services/services/firefly/foundry/deploys) rendering pipeline — no more nesting values files in specific folder hierarchies to control inheritance. Bazel rules declare the composition explicitly (which chart, which values, which runtime env). Renders in 1–2 seconds (vs 30–60s), and the rendered manifests are visible in PR diffs before merge.

## Package an application

Load from: `load("@platforms_inference//:defs.bzl", ...)`

```{colligo_bazel_docs} /platforms/inference/bazel_infra/package/package.bzl:inference_application
:toc:
```

## Generate Deployment

Load from: `load("@platforms_inference//:defs.bzl", ...)`

`ethos_deployment(...)` is the main way to **deploy anything to Ethos**. You give it some
charts (Helm or Python) and/or raw Kubernetes YAML, pick a target cluster, and it produces
one Argo CD application. It is not specific to inference — you can use it to ship a plain
Helm chart, some CRDs, or an Argo workflow just as easily as an inference service.

**What one call does.** One `ethos_deployment(...)` target takes everything you pass in
(charts, chart values, raw YAMLs) plus the defaults from the runtime env (image pull secrets,
IAM role, cluster-specific endpoints like Redis, default RBAC) and renders them into a single
`k8s_manifest.yaml`. That file gets copied into the repo's `cloud/` folder by the
`argo_sync(...)` rule. Argo CD watches `cloud/` and deploys whatever it finds. So: merge a
PR → `cloud/` updates → your app updates in Kubernetes. No `kubectl` needed.

**Where to put it.** The conventional layout in `managed_services` is one `BUILD` per
environment (dev / stage / prod). Most apps have exactly one `ethos_deployment(...)` call
inside each environment's `BUILD`, targeting that environment's cluster:

```
services/samples/E/deploys/imaging/
├── BUILD                         # inference_application(...) — builds the Docker image
├── dev/
│   ├── BUILD                     # one ethos_deployment for the dev cluster
│   └── values.inference.yaml
└── stage/
    ├── BUILD                     # one ethos_deployment for the stage cluster
    └── values.inference.yaml
```

**Multiple deployments in one `BUILD`.** Sometimes a single environment spans more than
one cluster — for example, dev in `ethos851-dev-or2` *and* `ethos851-dev-va7`. In that
case you just add **a second `ethos_deployment(...)` call in the same `dev/BUILD`**,
pointing at the other cluster;

```python
# dev/BUILD — one ethos_deployment per dev cluster.

ethos_deployment(
    name = "imaging_dev_or2",
    ethos_runtime_env = "@platforms_inference//:ethos851-dev-or2",
    python_charts = ["@platforms_inference//:ai-inference-chart"],
    chart_values = [":inference-chart-values"],
)

ethos_deployment(
    name = "imaging_dev_va7",
    ethos_runtime_env = "@platforms_inference//:ethos851-dev-va7",
    python_charts = ["@platforms_inference//:ai-inference-chart"],
    chart_values = [":inference-chart-values"],
)
```

**One thing not to forget.** Every `ethos_deployment(...)` target has to be listed in the
repo's `argo_sync(...)` rule (in the root `BUILD`) so that Argo actually sees it. `smake lint`
adds it for you thanks to the `# gazelle:argo_sync_rule` directive. If you skip lint, the
target builds fine but nothing ever syncs to the cluster, which is a confusing first-time
failure mode.

```{colligo_bazel_docs} /platforms/inference/bazel_infra/gitops/ethos_deployment.bzl:ethos_deployment_rule
:toc:
```

Note: Use `ethos_deployment(...)` instead of `ethos_deployment_rule`. We have a bug in the docs that show the wrong name.

Load from: `load("@platforms_inference//:defs.bzl", ...)`

```{colligo_bazel_docs} /platforms/inference/bazel_infra/gitops/k8s_raw_objects.bzl:k8s_raw_objects
:toc:
```

```{colligo_bazel_docs} /platforms/inference/bazel_infra/gitops/k8s_helm_chart.bzl:k8s_remote_helm_chart,k8s_local_helm_chart,k8s_alias_helm_chart
:toc:
```

```{colligo_bazel_docs} /platforms/inference/bazel_infra/gitops/k8s_py_chart.bzl:k8s_local_python_chart,k8s_remote_python_chart
:toc:
```

```{colligo_bazel_docs} /platforms/inference/bazel_infra/gitops/k8s_values.bzl:k8s_global_values,k8s_chart_values
:toc:
```

```{colligo_bazel_docs} /platforms/inference/bazel_infra/gitops/rbac_groups.bzl:rbac_groups
:toc:
```

### Available runtime envs

The `ethos_runtime_env` you pass to `ethos_deployment(...)` picks the **cluster + environment + infrastructure defaults** your app is deployed into. Reference them as `@platforms_inference//:<name>`.

```{admonition} Source of truth — this table may be stale
:class: important

The table below is a snapshot and may drift as new clusters are added or old ones are retired. The authoritative list is always the BUILD file that defines them: [platforms/inference/ethos/runtime_envs/BUILD](/platforms/inference/ethos/runtime_envs/BUILD). Every target declared with ``ethos_runtime_env(name = "...")`` in that file is an available runtime env;
```

If you need a new runtime env that does not exist yet, open a PR or ping the AI Platform team.

| Label | Environment | Region | Backing cluster | RBAC group |
|---|---|---|---|---|
| `ethos851-dev-or2` | dev | or2 | `ethos851-stage-or2` (shared with stage) | `firefly_dev_rbac` |
| `ethos851-stage-or2` | stage | or2 | `ethos851-stage-or2` | `firefly_dev_rbac` |
| `ethos851-prod-or2` | prod | or2 | `ethos851-prod-or2` | `firefly_prod_rbac` |
| `ethos852-prod-or2` | prod | or2 | `ethos852-prod-or2` | `firefly_prod_rbac` |
| `ethos853-prod-or2` | prod | or2 | `ethos853-prod-or2` | `firefly_prod_rbac` |
| `ethos854-prod-or2` | prod | or2 | `ethos854-prod-or2` | `firefly_prod_rbac` |
| `ethos851-prod-va6` | prod | va6 | `ethos851-prod-va6` | `firefly_prod_rbac` |
| `ethos852-prod-va6` | prod | va6 | `ethos852-prod-va6` | `firefly_prod_rbac` |
| `ethos853-prod-va6` | prod | va6 | `ethos853-prod-va6` | `firefly_prod_rbac` |
| `ethos-hub` | — | — | — | `firefly_dev_rbac` |

Two things worth knowing when picking one:

- **Dev shares a cluster with stage.** `ethos851-dev-or2` and `ethos851-stage-or2` both resolve to the same physical cluster; the difference is the namespace/env labels and which chart values are injected. You do not get a separate "dev cluster" — treat it accordingly for resource limits and noisy-neighbor sensitivity.
- **To run in prod in both regions, add one `ethos_deployment(...)` per runtime env.** There is no wildcard — e.g. shipping to all four or2 prod clusters + all three va6 prod clusters means seven `ethos_deployment(...)` targets. See the "Multiple deployments in one BUILD" note above.

Each runtime env also ships a bundle of chart-value defaults (image pull secrets, IAM role, redis host, S3/Splunk secret references, etc.) so you don't have to repeat infra wiring in every tenant's `values.inference.yaml`. See [Runtime configuration — `ethos_runtime_env`-provided defaults](./inference-chart.md#runtime-configuration) for the merge order.

## Ethos environment management (platform internal)


Load from: `load("@platforms_inference//gitops:defs.bzl", ...)`


```{colligo_bazel_docs} /platforms/inference/bazel_infra/gitops/ethos_env.bzl:ethos_env
:toc:
```

```{colligo_bazel_docs} /platforms/inference/bazel_infra/gitops/ethos_runtime_env.bzl:ethos_runtime_env
:toc:
```

```{colligo_bazel_docs} /platforms/inference/bazel_infra/gitops/ethos_cluster.bzl:ethos_cluster
:toc:
```

```{colligo_bazel_docs} /platforms/inference/bazel_infra/gitops/ethos_region.bzl:ethos_region
:toc:
```

## Binary management

```{colligo_bazel_docs} /platforms/inference/bazel_infra/binary_group/binary_group.bzl:binary_group
:toc:
```
