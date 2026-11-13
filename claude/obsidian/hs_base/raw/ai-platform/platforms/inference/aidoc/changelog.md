---
sectnum: false
---

# Changelog

Notable changes to `frameworks.inference` (Python wheel) and the Inference Platform (Helm chart).
Follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Both artifacts share a single version, released together via `release/inference/vX.Y.Z` tags.

## [v0.5.11] - 2026-06-26

### Added
- LangGraph agent deployments now emit structured Splunk logs automatically.
  `LangGraphAgentValues.logging` accepts an optional `LoggingConfig`; when omitted the
  renderer auto-derives the config from the Ethos environment (`nfp_nonprod` for dev/stage,
  `nfp_prod` for prod/prerelease, source type `v3-<deployment_name>-<env>`).
  `create_default_logging_config_from_env` is now re-exported from the agent renderer API
  for callers that need to build the config explicitly.

### Fixed
- LangGraph agent deployments: `.private.adobe.io` custom ingress hosts now correctly get
  ingress class `contour-internal` (was `contour-corp`), TLS secret
  `cluster-ssl-x-private-adobe-io` (was missing the `-x-`), and a DNS CNAME pointing at
  the internal load balancer (`ethos.int.<cluster>.ethos.adobe.net`, was `ethos.pub.*`).
  All three were bugs in the LangGraph renderer's local duplicates of inference-renderer
  logic; the duplicates have been removed and the shared `infer_tls_secret` and
  `generate_dns_record` helpers (now public) are used instead.
- LangGraph agent deployments: requests to `.private.adobe.io` custom ingress hosts no
  longer return 403. The IP allowlist applied to the shared base-route HTTPProxy
  (corp gateway IPs) blocked traffic arriving directly at the `contour-internal` load
  balancer with a `10.x.x.x` source address. Internal virtual hosts now get a separate
  unfiltered base route — the `contour-internal` LB is already network-restricted to
  Adobe's internal network, so route-level IP filtering is redundant and harmful.
- `infer_tls_secret` and `generate_dns_record` in the inference renderer ingress module
  are now public (previously `_infer_tls_secret` / `_generate_dns_record`) so the agent
  renderer can reuse them without duplication.

## [v0.5.10] - 2026-06-26

### Added
- GPU deployments now automatically mount a memory-backed `/dev/shm` volume sized at 3 GiB per GPU (e.g. 24 GiB for 8-GPU pods). vLLM, PyTorch multiprocessing, and NCCL use `/dev/shm` for inter-process communication; Kubernetes defaults it to 64 MiB which caused mysterious failures (bus errors, NCCL hangs) that were hard to diagnose. This is a safe no-op for workloads that don't use shared memory. ([FFP-98330](https://jira.corp.adobe.com/browse/FFP-98330), [#2497](https://github.com/Adobe-Firefly/ai-platform/pull/2497))

## [v0.5.9] - 2026-06-25

### Changed
- Synced the vendored Colligo code with the latest `main`, bringing in the latest CAI and ACMP fixes.

## [v0.5.8] - 2026-06-24

### Added
- `ethos_deployment(service_descriptor = …)` — optional per-deploy label binding the app's service descriptor (e.g. `service_descriptor = "//services/team/app:descriptor"`, the same label across dev/stage/prod). A declaration of operational facts the control plane consumes (service identity, capacity-planning info, CD/rollout policy) — not pod runtime config. Surfaced into each deployment's `argo_info.yaml` as `service_descriptor`; parsed in the control plane, not by Bazel. Optional for now — primarily the opt-in gate for CD. ([#2432](https://github.com/Adobe-Firefly/ai-platform/pull/2432))

## [v0.5.7] - 2026-06-24

### Changed
- Synced the vendored colligo code with latest main. Notably, `migration.acp.patch_acp_application_metadata` no longer performs a `GET` → `PATCH` sequence with `If-Match` optimistic locking; it now writes the JSON Patch `add` operation directly.

## [v0.5.6] - 2026-06-23

### Fixed
- Resilient (background) async jobs now report the real request path in the `colligo_resilient_queue_request_time` metric instead of the `v3_background` placeholder. `BackgroundJobExecutor` labels the metric with the original request endpoint (restored from the job's `RequestContext`), matching the v2 rhode path — so the NewRelic "API request latency [async][resilient]" dashboard (faceted by `path`, filtered on `/v./.*`) shows v3 deployments.

## [v0.5.5] - 2026-06-19

### Fixed
- `inference.serve()` now respects `ServeConfig.num_processes` when launching worker subprocesses.
  `python -m frameworks.inference workers ...` also respects `ServeConfig.num_processes`; passing the
  same worker ref more than once now fails fast instead of hanging during supervisor startup.
  ([FFP-97287](https://jira.corp.adobe.com/browse/FFP-97287), [#2315](https://github.com/Adobe-Firefly/ai-platform/pull/2315))

## [v0.5.4] - 2026-06-19

### Fixed
- Added the missing `generation_metrics.py` to the `migration.metrics` namespace in the published wheel. It was absent in v0.5.0–v0.5.3 (the serve wheel's `include` allowlist dropped it), so `from frameworks.inference.migration.metrics import generations` raised `ImportError` and the pre-registered generation metrics were unusable. ([FFP-95352](https://jira.corp.adobe.com/browse/FFP-95352))

## [v0.5.3] - 2026-06-19

### Changed
- `ScaleToZeroConfig` KEDA defaults updated: `server_address` now points at per-namespace Query (`http://app-promoperator-prometheus.ns-team-firefly-enm.svc.cluster.local:9090`) instead of the Thanos (`thanos-query.ns-team-firefly-enm.svc.cluster.local:10902`).

## [v0.5.2] - 2026-06-18

### Fixed
- `argo_sync` no longer wipes committed meta files in `cloud/<env>/` subdirectories. The cloud-folder scrub previously `rmtree`'d each env directory wholesale, honoring the keep-list (`.ethos.yaml`, `.gitignore`, `OWNERS`, `README.md`) only at the `cloud/` root; it now preserves those names at any depth via the new `utils.rmtree_except`, while still regenerating the per-chart `cloud/<env>/<chart>/` subdirs. This lets committed code-review policy (e.g. SRE `OWNERS` on `cloud/stage`, `cloud/prod`, `cloud/prerelease`) survive manifest regeneration, unblocking the downstream colligo code-review parity change. ([FFP-89989](https://jira.corp.adobe.com/browse/FFP-89989), [#1667](https://github.com/Adobe-Firefly/ai-platform/pull/1667))

## [v0.5.1] - 2026-06-16

### Added
Added KEDA `activationThreshold` - It defines the minimum metric value required to activate the scaler and scale up from 0 to minReplicaCount. 
The trigger is activated only when metric (or warm up) > activationThreshold. Default is 0. ([FFP-95555](https://jira.corp.adobe.com/browse/FFP-95555))

## [v0.5.0] - 2026-06-11

### Added
- `migration.metrics` module — exposes the multi-backend metrics factory (`METRICS_FACTORY`, `ColligoMetric`, `SettableMetric`, `MetricBackendName`, `with_active_metrics_backends`) for registering custom metrics against Prometheus, NewRelic, and S3 backends. ([FFP-95352](https://jira.corp.adobe.com/browse/FFP-95352))
- `migration.metrics.generation_metrics` — pre-registered generation metrics (image, video, audio, prompt-rewrite, LLM tokens) identical to colligo v2; required for finance-tracked NewRelic and Prometheus dashboards. ([FFP-95352](https://jira.corp.adobe.com/browse/FFP-95352))
- Metrics registration guide and full generation metrics reference in [migration/metrics docs](/frameworks/inference/serve/migration/metrics/aidoc/metrics.md). ([FFP-95352](https://jira.corp.adobe.com/browse/FFP-95352))

## [v0.4.5] - 2026-06-11

### Added
- Runtime weight download now reads `s3_bucket` from manifests (added in [platforms.dev_tools.binaries v3.3](/platforms/dev_tools/aidoc/changes.md)) and resolves credentials per bucket. Services with weights in custom buckets (e.g. vendor-specific) can download them at startup — configure the bucket's S3 profile in [`InferenceFrameworkConfig.S3`](https://docs.ai.corp.adobe.com/v3/frameworks/inference/serve/aidoc/api.html#api-doc-s3). ([FFP-95251](https://jira.corp.adobe.com/browse/FFP-95251))

## [v0.4.4] - 2026-06-10

### Added
- `binary_group()` guardrail: rejects manifests with a custom `s3_bucket` field (added in [platforms.dev_tools v3.3](/platforms/dev_tools/aidoc/changes.md)) at build time with a clear error that `binary_group()` and custom buckets are not a valid combination. ([FFP-95251](https://jira.corp.adobe.com/browse/FFP-95251))
- `binary_group()` documented in the GitOps Framework API page.

### Changed
- `ScaleToZeroConfig` KEDA defaults updated: `server_address` now points at Thanos Query (`http://thanos-query.ns-team-firefly-enm.svc.cluster.local:10902`) instead of the per-namespace Prometheus (`app-promoperator-prometheus…:9090`), and the `threshold` default changed from `'1'` to `'5'`. `threshold` is the KEDA target value used to size replicas (`desiredReplicas = ceil(metricValue / threshold)`) and does not affect scale-from-zero behavior — clarifying/superseding the `'1'` warm-trigger rationale from v0.3.14.
- Upgrade Bazel stack: Bazel `8.5.0` → `9.1.0`, `rules_python` `1.8.0` → `2.0.1`, `rules_img` `0.3.3` → `0.3.11`, `rules_mypy` `0.40.0` → `0.41.0`, `gazelle` `0.47.0` → `0.51.0`, `rules_go` `0.59.0` → `0.60.0`, `rules_shell` `0.6.1` → `0.8.0`, `rules_cc` `0.2.16` → `0.2.18`, `buildifier_prebuilt` `8.2.1` → `8.5.1.2`. ([FFP-89335](https://jira.corp.adobe.com/browse/FFP-89335), [#1402](https://github.com/Adobe-Firefly/ai-platform/pull/1402))

## [v0.4.1] - 2026-06-05

### Added
- LangGraph agent ingress can now be locked to a CIDR allowlist. Setting `ingress.custom_ingress[].allowed_ip_groups` (predefined groups like `corp`, `laser_dev`) and/or `allowed_ip_ranges` (literal CIDRs) makes the renderer attach Adobe CGW's `envoy.filters.http.ip_allow_deny` filter to every rendered HTTPProxy route, so a public agent endpoint (e.g. `chiron-webhook.adobe.io`) only accepts the listed networks. Public webhook paths are now fully configurable via `ingress.custom_ingress[].public_paths`: each listed prefix is cloned into an unfiltered route so endpoints delivered from un-allowlistable IP pools stay reachable (e.g. Slack's Events API `/events/slack`, interactivity `/slack/interactions`, and slash commands `/slack/commands`, all HMAC-verified). Nothing is exempt unless listed, so a deploy must enumerate every public webhook path. No-op when no allowlist is configured. ([FFP-94722](https://jira.corp.adobe.com/browse/FFP-94722), [#1921](https://github.com/Adobe-Firefly/ai-platform/pull/1921))

## [v0.4.0] - 2026-06-08

### Added
- Exposed all prod `runtime_env` aliases in `@platforms_inference` — `ethos851`–`ethos855-prod-or2` and `ethos851`–`ethos853-prod-va6` — so v3 managed-service consumers can reference prod clusters without importing the internal `//ethos/runtime_envs` target directly. Also added the missing `ethos855-prod-or2` runtime env definition (cluster and chart values already existed). ([FFP-95025](https://jira.corp.adobe.com/browse/FFP-95025))

## [v0.3.29] - 2026-06-08

### Fixed
- HTTP-server pods now serve `GET /status` (the Contour HTTPProxy `healthCheckPolicy` target on the app port). `mount_http_server_extras` registers the ingress-liveness route before the `StaticFiles("/")` catch-all mount, so it returns `200` instead of falling through to a `404`. Previously every Contour health check (per route, per pod) hit the catch-all and 404'd — flooding pod logs with ERROR-level noise and pushing Envoy into panic mode, which silently disabled health-based draining (traffic was routed to all backends regardless of health).

## [v0.3.28] - 2026-06-04

### Added
- `JobResult.intermediate_results: dict[str, Any] | None` — background workers can now report structured mid-execution data alongside the float `progress`. `DistributedExecuteKit` persists it to the `$intermediate_results` session key; `LocalExecuteKit` passes it through in-process. The built-in `default_jobs_app` surfaces it on `IN_PROGRESS` poll responses (`exclude_none` keeps responses that omit it byte-identical to before). New writer: `ExecuteKit.set_background_intermediate_results(dict)`. ([FFP-93371](https://jira.corp.adobe.com/browse/FFP-93371), [#1863](https://github.com/Adobe-Firefly/ai-platform/pull/1863))

## [v0.3.27] - 2026-06-04

### Added
- NewRelic metrics reporting is now configured by default for inference apps via each environment's `env_specific` globals. Every pod gets the `NEWRELIC_API_KEY` secret injected as a `secretKeyRef` from vault (`dme_spl/services/firefly/common/NEWRELIC_API_KEY`, field `prod`/`nonprod` by environment tier), and the runtime config's `newrelic.app_name` is set to a globally-unique `<gitOrg>--<gitRepo>-<serviceEnvironment>-<application_name>` (e.g. `firefly--ai-platform-Dev-my-app`) so metrics from different repos/envs/apps don't collide. 
- The framework's metrics backend reads the key from the runtime config and reports to NewRelic. A product opts out by overriding the value (e.g. setting the key to `None`) in its chart.

## [v0.3.26] - 2026-06-03

### Fixed
- Fix LangGraph Contour ingress 503: `flex-langgraph-standalone-deployment` ingress template hardcodes `langgraph-cloud-api-server` as the HTTPProxy backend, but `fullnameOverride: {deployment_name}` causes the actual service to be named `{deployment_name}-api-server`. The renderer now post-processes rendered HTTPProxy specs and patches the wrong service name ([#1841](https://github.com/Adobe-Firefly/ai-platform/pull/1841)).

## [v0.3.25] - 2026-06-03

- Add missing `health_check_path` config to the `ai-ingress-chart`: [FFP-92957](https://jira.corp.adobe.com/browse/FFP-92957), [#1832](https://github.com/Adobe-Firefly/ai-platform/pull/1832)
- Fix `bazel test ...` failures in managed services in MacOS due to file system case insensitivity [#1834](https://github.com/Adobe-Firefly/ai-platform/pull/1834).
- Fix `bazel test ...` failures in managed services due to inference framework trying to read into readonly paths under Bazel sandbox: [FFP-94085](https://jira.corp.adobe.com/browse/FFP-94085), [#1831](https://github.com/Adobe-Firefly/ai-platform/pull/1831).

## [v0.3.24] - 2026-06-03

### Fixed
- LangGraph chart resource names (`Deployment`, `Service`, `ServiceAccount`, `StatefulSet`, `HPA`, `VaultSecret`, `ConfigMap`) are now fully scoped to `deployment_name`, making it safe to deploy multiple LangGraph agents to the same namespace ([#1828](https://github.com/Adobe-Firefly/ai-platform/pull/1828)):
  - `fullnameOverride` on the `langgraph-cloud` subchart now uses `deployment_name` instead of the hardcoded `langgraph-cloud` prefix
  - `config.existingSecretName` (LangSmith credentials) now `{deployment_name}-secrets`
  - Postgres and Redis `existingSecretName` now `{deployment_name}-postgres` / `{deployment_name}-redis`
  - `env_vars.secrets` VaultSecrets now named `{deployment_name}-{path-suffix}-secrets` instead of `agent-{path-suffix}-secrets`
  - Registry auth VaultSecret now `{deployment_name}-registry-secret`; the chart's hardcoded generic `registry-secret` and empty `flex-langgraph-standalone-deployment-cm` ConfigMap are filtered from the rendered manifest

## [v0.3.23] - 2026-06-03

### Added
- `ai-ingress-chart` (`@platforms_inference//:ai-ingress-chart`) — standalone Python chart for adding ingress (Service, HTTPProxy, RequestProcessing, DNSRecord) to any ethos-deployed service without the full inference chart. Supports `EthosTarget` (auto-expand binding from ethos globals) and `AbsoluteTarget` (raw binding selector). ([FFP-92957](https://jira.corp.adobe.com/browse/FFP-92957), [#1797](https://github.com/Adobe-Firefly/ai-platform/pull/1797))
- `enable_multi_task_async_context` exposed in `frameworks.inference` default config — allows enabling multi-task async context for the runtime ([FFP-93577](https://jira.corp.adobe.com/browse/FFP-93577), [#1795](https://github.com/Adobe-Firefly/ai-platform/pull/1795))
- Chart env_specific values now set IMS config, temp storage bucket, and S3 Transfer Acceleration by default — apps no longer need to configure these manually ([FFP-93184](https://jira.corp.adobe.com/browse/FFP-93184), [#1768](https://github.com/Adobe-Firefly/ai-platform/pull/1768))

### Fixed
- Fix development environment issues: `.vscode/launch.py` paths, `binary_group` gazelle plugin, `setup-auth.py` credential setup, and requirements lock files updated for latest toolchain ([FFP-85691](https://jira.corp.adobe.com/browse/FFP-85691), [#1796](https://github.com/Adobe-Firefly/ai-platform/pull/1796))

## [v0.3.22] - 2026-06-01

### Fixed
- `k8s_alias_helm_chart` now works with `ethos_deployment`: the same Helm chart can be included multiple times (e.g. two CGW `HTTPProxy` instances with different `customDomains`/`clusterGateway.endpoints`) without the render failing with `found in Chart.yaml, but missing in charts/ directory`. The renderer now derives the Helm dependency name from the chart's on-disk name (the tar's `Chart.yaml`) and emits Helm's two-instance `name`+`alias` pattern, extracting the shared sub-chart once. Alias dependencies also pin the chart's real version instead of `*`, which previously dropped alias instances of pre-release charts (e.g. `1.17.0-beta.2`) ([FFP-91264](https://jira.corp.adobe.com/browse/FFP-91264), [#1757](https://github.com/Adobe-Firefly/ai-platform/pull/1757))

## [v0.3.21] - 2026-06-01

### Fixed
- Update AWS secrets to new vault paths for all environments

## [v0.3.20] - 2026-05-29

### Added
- `langgraph-chart` (`@platforms_inference//:langgraph-chart`) — explicit Bazel target for LangGraph self-hosted platform deployments (apiServer + queue + Postgres + Redis via `flex-langgraph-standalone-deployment`). Previously the unified `agent-chart` target heuristically dispatched on `langsmith_project`; the two paths are now separate binaries with separate public targets.
- `AgentSecret` and `AgentEnvVars` types in `bazel_infra.gitops.agent_renderer.api`. `AgentSecret` extends `Secret` with an optional `secret_name` field (K8s Secret name override); `AgentEnvVars` is the env-vars model for both agent chart types.
- Agent deployment docs reorganised under `platforms/inference/aidoc/deployment/agents/`: `deployment/agents/claude-agent-sdk.md` for the single-pod shape and `deployment/agents/langgraph.md` for the LangGraph shape.

### Changed
- `agent-chart` renamed to `claude-agent-sdk-chart`; `agent-renderer` renamed to `claude-agent-sdk-renderer`. Update `@platforms_inference//:agent-chart` references to `@platforms_inference//:claude-agent-sdk-chart`.
- `secret_name` field removed from `inference_renderer.api.Secret` — it was agent-renderer-only and now lives on `agent_renderer.api.AgentSecret`. Inference chart consumers are unaffected (the field was never rendered by the inference chart).
- `AgentValues.env_vars` and `LangGraphAgentValues.env_vars` type changed from `EnvVars` to `AgentEnvVars` (structurally identical except `secrets` map uses `AgentSecret` instead of `Secret`).

## [v0.3.19] - 2026-05-29

### Fixed
- `async_endpoint_url` config injection now respects `global_config.url_prefix` instead of always using the default `v3-{application_name}` — fixes job polling 404s when a custom url_prefix is set ([FFP-93178](https://jira.corp.adobe.com/browse/FFP-93178))

## [v0.3.18] - 2026-05-29

### Fixed
- `PUT /jobs/cancel/{id}` is now idempotent: a second cancel on a job already in `CANCEL_PENDING`, `CANCELED`, or `WATCHDOG_CANCELLED` state returns HTTP 200 instead of 404 `unknown_job_id`. The previous code conflated "no state change" with "job not found". ([FFP-93091](https://jira.corp.adobe.com/browse/FFP-93091))
- `GET /jobs/result/{id}` now returns 410 `job_canceled` immediately after a successful cancel, instead of continuing to report the job as `IN_PROGRESS` while cancellation was pending. ([FFP-93091](https://jira.corp.adobe.com/browse/FFP-93091))

## [v0.3.17] - 2026-05-29

### Fixed
- Async ingress in dev/stage now gets default corp+laser IP allowlisting (was open to internet), DNS records pointed to wrong target for public ingress, and custom ingress class inference for ethos wildcard domains was incorrect ([FFP-92939](https://jira.corp.adobe.com/browse/FFP-92939), [FFP-91070](https://jira.corp.adobe.com/browse/FFP-91070))

### Changed
- `PUT` added to default `allowed_methods` for all ingress types (previously only async had it) ([FFP-92939](https://jira.corp.adobe.com/browse/FFP-92939))

## [v0.3.16] - 2026-05-29

### Fixed
- `create_dns: true` now generates correct DNSRecord CNAME target based on ingress class: `contour-internal` → `ethos.int.*`, `contour-corp` → `ethos.corp.*` (was always `ethos.pub.*`) ([FFP-91070](https://jira.corp.adobe.com/browse/FFP-91070))
- `public_async_ingress` FQDN now includes `-async` suffix to avoid collision with `development_ingress`, and always uses `contour-public` ([FFP-92939](https://jira.corp.adobe.com/browse/FFP-92939))
- `_infer_ingress_class` and `_infer_tls_secret` now support Ethos wildcard domains (`.corp.*`, `.int.*`, `.*ethos.adobe.net`) ([FFP-91070](https://jira.corp.adobe.com/browse/FFP-91070))
- `prerelease` environment now gets `contour-public` ingress class for `public_ingress` (was `contour-corp` when no CIDRs) ([FFP-91070](https://jira.corp.adobe.com/browse/FFP-91070))

### Changed
- `CustomIngressConfig.ingress_class` no longer accepts arbitrary strings — must be a valid `IngressClass` enum value (`"contour-public"`, `"contour-corp"`, `"contour-internal"`)
- `custom_ingress` field changed from a list to a dict keyed by logical name, enabling clean overlay merging without repeating all entries ([FFP-92938](https://jira.corp.adobe.com/browse/FFP-92938))

## [v0.3.15] - 2026-05-28

### Reverted
- Revert `x-gw-ims-*` header stripping on HTTPProxy routes (v0.3.13) — the `requestHeadersPolicy.remove` runs after contour injects identity headers, stripping them before they reach the app and breaking all authz on internal (`.private.adobe.io`) ingresses. [FFP-92153](https://jira.corp.adobe.com/browse/FFP-92153) remains open to explore a proper anti-spoofing solution. ([#1681](https://github.com/Adobe-Firefly/ai-platform/pull/1681))

## [v0.3.14] - 2026-05-28
### Fixed
- `ScaleToZeroConfig.threshold` default changed from `'5'` to `'1'` so the warm trigger signal (`colligo_worker_warm_trigger = 1.0`) reliably causes KEDA to scale up from zero; previously a threshold of 5 meant the warm trigger was silently ignored and workers never pre-warmed ([FFP-89295](https://jira.corp.adobe.com/browse/FFP-89295))

## [v0.3.13] - 2026-05-27

### Added
- Strip all `x-gw-ims-*` headers on every HTTPProxy route so client-supplied values cannot be spoofed alongside CGW-injected ones; covers 31 headers across OAuth token, profile, and multi-token flows ([FFP-92153](https://jira.corp.adobe.com/browse/FFP-92153), [#1602](https://github.com/Adobe-Firefly/ai-platform/pull/1602))

## [v0.3.12] - 2026-05-21

### Added
- `/mnt/localssd` ephemeral PVC volume (storageClass: `local-ssd`) now mounted by default for GPU deployments; prevents model weight downloads from consuming ephemeral-storage and triggering kubelet eviction. CPU deployments are unaffected (opt-in with `localssd: true`). Set `localssd: false` to disable. ([FFP-91269](https://jira.corp.adobe.com/browse/FFP-91269), [#1502](https://github.com/Adobe-Firefly/ai-platform/pull/1502))

## [v0.3.11] - 2026-05-20

### Added
- `ACPConfig` in `MigrationConfig` — exposes `enable_inputs`, `enable_components_inputs`, `enable_outputs`, and `api_key` for ACP file storage; wired through the config shim to v2 `creative_cloud_storage` ([FFP-90726](https://jira.corp.adobe.com/browse/FFP-90726), [#1441](https://github.com/Adobe-Firefly/ai-platform/pull/1441))
- `migration.acp` module — public surface for ACP download (`get_data_from_acp_file_asset`, `get_data_from_acp_component`), upload (`upload_acp_file_asset`), metadata (`patch_acp_application_metadata`, `fetch_direct_download_url`), and HTTP client (`AsyncClientWithStats`) ([#1441](https://github.com/Adobe-Firefly/ai-platform/pull/1441))
- ACP section in the [Migration API docs](/frameworks/inference/serve/aidoc/api.md) ([#1441](https://github.com/Adobe-Firefly/ai-platform/pull/1441))

## [v0.3.10] - 2026-05-20

### Added
- Changelog for `frameworks.inference` and the Inference Platform, seeded with full history from v0.2.11 ([FFP-90183](https://jira.corp.adobe.com/browse/FFP-90183), [#1435](https://github.com/Adobe-Firefly/ai-platform/pull/1435))
- `./make release VERSION` — validates the changelog entry then creates and pushes the release tag ([#1435](https://github.com/Adobe-Firefly/ai-platform/pull/1435))
- `./make check-changelog VERSION` — standalone changelog validation, also called by CI on tag push ([#1435](https://github.com/Adobe-Firefly/ai-platform/pull/1435))

## [v0.3.9] - 2026-05-19

### Added
- New `cpu-xlarge` hardware tier for agent deployments (4 cpu req / 16 cpu limit, 8 GiB / 32 GiB on `c5.12xlarge` nodes) ([#1413](https://github.com/Adobe-Firefly/ai-platform/pull/1413))

### Fixed
- Agent chart shipped in v0.3.8 hardcoded container resources, dropped Splunk log routing, and omitted dashboard ingress; all three now flow through the same renderer helpers as the inference chart ([FFP-88192](https://jira.corp.adobe.com/browse/FFP-88192), [#1413](https://github.com/Adobe-Firefly/ai-platform/pull/1413))

## [v0.3.8] - 2026-05-19

### Added
- Agent renderer (`platforms/inference/bazel_infra/gitops/agent_renderer`) moved into the Inference Platform with K8s manifest generation (ConfigMap, PodMonitor, secret vars) and new [Agent Deployment docs](/platforms/inference/aidoc/deployment/agents/claude-agent-sdk.md) ([FFP-88192](https://jira.corp.adobe.com/browse/FFP-88192), [#1393](https://github.com/Adobe-Firefly/ai-platform/pull/1393))

## [v0.3.7] - 2026-05-18

### Fixed
- `download_binary_manifests` now acquires an `fcntl` exclusive lock per file before the cache check and before the check-then-symlink phase, preventing corruption and deadlocks when concurrent pods race on the same cache entry; duplicate file entries across manifest keys are also deduplicated to avoid same-thread deadlock ([FFP-89687](https://jira.corp.adobe.com/browse/FFP-89687), [#1354](https://github.com/Adobe-Firefly/ai-platform/pull/1354))

## [v0.3.6] - 2026-05-18

### Added
- Five `ethos85{1..5}-prerelease-or2` runtime environments backed by the prod-or2 cluster in `ns-team-colligov2-prod-prerelease`; `default_namespace` is now mandatory and flows through the full render chain ([FFP-90182](https://jira.corp.adobe.com/browse/FFP-90182), [#1388](https://github.com/Adobe-Firefly/ai-platform/pull/1388))
- `XDG_CACHE_HOME=/mnt/localssd/.cache` set globally for all inference chart deployments, routing model/weight downloads to local SSD instead of EBS-backed `/workspace/.cache/` ([FFP-89672](https://jira.corp.adobe.com/browse/FFP-89672), [#1367](https://github.com/Adobe-Firefly/ai-platform/pull/1367))

### Changed
- `{_env: VAR}` config resolution no longer requires inheriting from `BaseConfig`; a new `resolve_env_vars()` helper replaces `{_env: VAR}` with `os.getenv(VAR)` in any config dict before Pydantic validation ([FFP-89128](https://jira.corp.adobe.com/browse/FFP-89128), [#1369](https://github.com/Adobe-Firefly/ai-platform/pull/1369))

### Fixed
- `setup-auth` script broken by a `uv`/Artifactory behavior change ([#1384](https://github.com/Adobe-Firefly/ai-platform/pull/1384))

## [v0.3.5] - 2026-05-15

### Fixed
- `url_prefix` now works correctly for dev deployments ([FFP-89587](https://jira.corp.adobe.com/browse/FFP-89587), [#1330](https://github.com/Adobe-Firefly/ai-platform/pull/1330))

### Added
- Startup probe, rollout strategy, and extra tolerations support in the inference chart ([FFP-89529](https://jira.corp.adobe.com/browse/FFP-89529), [#1330](https://github.com/Adobe-Firefly/ai-platform/pull/1330))

## [v0.3.4] - 2026-05-14

### Added
- v2-style endpoints and responses for background jobs ([FFP-8716](https://jira.corp.adobe.com/browse/FFP-8716), [#1298](https://github.com/Adobe-Firefly/ai-platform/pull/1298))

## [v0.3.3] - 2026-05-13

### Fixed
- `pillow` added as a declared dependency of `frameworks.inference[migration]` ([FFP-87760](https://jira.corp.adobe.com/browse/FFP-87760), [#1299](https://github.com/Adobe-Firefly/ai-platform/pull/1299))

## [v0.3.2] - 2026-05-12

### Added
- ACP helpers exposed under `migration.acp` ([FFP-87002](https://jira.corp.adobe.com/browse/FFP-87002), [#1275](https://github.com/Adobe-Firefly/ai-platform/pull/1275))

## [v0.3.1] - 2026-05-12

### Changed
- `platforms_inference` pip hub upgraded to Python 3.13 ([FFP-87760](https://jira.corp.adobe.com/browse/FFP-87760), [#1276](https://github.com/Adobe-Firefly/ai-platform/pull/1276))

## [v0.3.0] - 2026-05-12

### Changed
- Managed Services upgraded to Colligo 2.0 stack: CUDA 13, Python 3.13 ([FFP-87760](https://jira.corp.adobe.com/browse/FFP-87760), [#1225](https://github.com/Adobe-Firefly/ai-platform/pull/1225))

## [v0.2.99] - 2026-05-11

### Added
- `return_stack_trace` option in v3 runtime config ([FFP-87582](https://jira.corp.adobe.com/browse/FFP-87582), [#1081](https://github.com/Adobe-Firefly/ai-platform/pull/1081))

## [v0.2.98] - 2026-05-11

### Added
- More flexible ingress configuration ([FFP-86592](https://jira.corp.adobe.com/browse/FFP-86592), [#1073](https://github.com/Adobe-Firefly/ai-platform/pull/1073))

## [v0.2.97] - 2026-04-29

### Added
- Debug traces and CORS configurable under `values.inference.yaml`; scale-to-zero re-enabled ([FFP-76564](https://jira.corp.adobe.com/browse/FFP-76564), [#936](https://github.com/Adobe-Firefly/ai-platform/pull/936))

## [v0.2.96] - 2026-04-28

### Fixed
- Default async allowed URL paths ([#1056](https://github.com/Adobe-Firefly/ai-platform/pull/1056))

## [v0.2.95] - 2026-04-28

### Changed
- Scale-to-zero disabled until fully functional ([FFP-85808](https://jira.corp.adobe.com/browse/FFP-85808), [#1055](https://github.com/Adobe-Firefly/ai-platform/pull/1055))
- OWNERS access rehaul: team aliases and ownership rules ([FFP-85082](https://jira.corp.adobe.com/browse/FFP-85082), [#1034](https://github.com/Adobe-Firefly/ai-platform/pull/1034))

## [v0.2.94] - 2026-04-22

### Fixed
- Public ingress prefix override ([#1008](https://github.com/Adobe-Firefly/ai-platform/pull/1008))

## [v0.2.93] - 2026-04-21

### Added
- Custom structured logger for better Splunk trace visibility ([FFP-65251](https://jira.corp.adobe.com/browse/FFP-65251), [#1002](https://github.com/Adobe-Firefly/ai-platform/pull/1002))

## [v0.2.92] - 2026-04-20

### Fixed
- Traces not showing in Splunk ([FFP-65251](https://jira.corp.adobe.com/browse/FFP-65251), [#1004](https://github.com/Adobe-Firefly/ai-platform/pull/1004))

## [v0.2.91] - 2026-04-17

### Added
- Session support in local single-process mode ([FFP-83304](https://jira.corp.adobe.com/browse/FFP-83304), [#998](https://github.com/Adobe-Firefly/ai-platform/pull/998))

## [v0.2.90] - 2026-04-13

### Fixed
- Cross-platform argo-sync for k8s_raw_objects ([#995](https://github.com/Adobe-Firefly/ai-platform/pull/995))

## [v0.2.89] - 2026-04-09

### Added
- Public async and custom ingress support ([FFP-70639](https://jira.corp.adobe.com/browse/FFP-70639), [#987](https://github.com/Adobe-Firefly/ai-platform/pull/987))

## [v0.2.88] - 2026-04-08

### Changed
- Inference chart input fields renamed to snake_case ([FFP-78962](https://jira.corp.adobe.com/browse/FFP-78962), [#971](https://github.com/Adobe-Firefly/ai-platform/pull/971))

## [v0.2.87] - 2026-04-03

### Fixed
- Explicit node affinity set when `preferred_family` is used for hardware selection ([FFP-80818](https://jira.corp.adobe.com/browse/FFP-80818), [#972](https://github.com/Adobe-Firefly/ai-platform/pull/972))

## [v0.2.86] - 2026-04-02

### Changed
- Consistent worker naming across deployments ([FFP-76471](https://jira.corp.adobe.com/browse/FFP-76471), [#927](https://github.com/Adobe-Firefly/ai-platform/pull/927))

## [v0.2.85] - 2026-04-01

### Fixed
- KEDA not enabled by default for GPU workers using `preferred_family` ([FFP-80587](https://jira.corp.adobe.com/browse/FFP-80587), [#969](https://github.com/Adobe-Firefly/ai-platform/pull/969))

## [v0.2.84] - 2026-03-25

### Added
- Public API paths supported in deployment chart ([FFP-78867](https://jira.corp.adobe.com/browse/FFP-78867), [#964](https://github.com/Adobe-Firefly/ai-platform/pull/964))

### Removed
- Default BKS IMS client ([#948](https://github.com/Adobe-Firefly/ai-platform/pull/948))

## [v0.2.83] - 2026-03-18

### Added
- Background job progress API ([FFP-76368](https://jira.corp.adobe.com/browse/FFP-76368), [#945](https://github.com/Adobe-Firefly/ai-platform/pull/945))
- `WatchdogDeployment` for automatic restart on failure ([FFP-76369](https://jira.corp.adobe.com/browse/FFP-76369), [#934](https://github.com/Adobe-Firefly/ai-platform/pull/934))

### Fixed
- Clear renderer error when deployment image is unresolved ([#942](https://github.com/Adobe-Firefly/ai-platform/pull/942))

## [v0.2.82] - 2026-03-12

### Added
- Concurrency limiter ([FFP-74504](https://jira.corp.adobe.com/browse/FFP-74504), [#920](https://github.com/Adobe-Firefly/ai-platform/pull/920))
- Backpressure support ([FFP-74505](https://jira.corp.adobe.com/browse/FFP-74505), [#924](https://github.com/Adobe-Firefly/ai-platform/pull/924))
- Autoscaler parity between platform and framework ([FFP-71618](https://jira.corp.adobe.com/browse/FFP-71618), [#866](https://github.com/Adobe-Firefly/ai-platform/pull/866))
- Platform-owned external services exposed from the framework ([FFP-73642](https://jira.corp.adobe.com/browse/FFP-73642), [#891](https://github.com/Adobe-Firefly/ai-platform/pull/891))

## [v0.2.81] - 2026-03-03

### Added
- Async request API ([FFP-63093](https://jira.corp.adobe.com/browse/FFP-63093), [#903](https://github.com/Adobe-Firefly/ai-platform/pull/903))

## [v0.2.80] - 2026-03-02

### Added
- Multi-GPU worker support ([FFP-65783](https://jira.corp.adobe.com/browse/FFP-65783), [#906](https://github.com/Adobe-Firefly/ai-platform/pull/906))
- Bazel sandbox support for worker tests ([FFP-69356](https://jira.corp.adobe.com/browse/FFP-69356), [#911](https://github.com/Adobe-Firefly/ai-platform/pull/911))

### Fixed
- Metrics not cleaned up correctly in distributed mode ([FFP-75702](https://jira.corp.adobe.com/browse/FFP-75702), [#907](https://github.com/Adobe-Firefly/ai-platform/pull/907))
- Local distributed mode ignored remote execution config ([FFP-74595](https://jira.corp.adobe.com/browse/FFP-74595), [#900](https://github.com/Adobe-Firefly/ai-platform/pull/900))

## [v0.2.79] - 2026-02-19

### Added
- Both sync and async handler functions now supported ([FFP-73416](https://jira.corp.adobe.com/browse/FFP-73416), [#889](https://github.com/Adobe-Firefly/ai-platform/pull/889))

### Fixed
- Editable install and Debug UI regression ([FFP-74586](https://jira.corp.adobe.com/browse/FFP-74586), [#892](https://github.com/Adobe-Firefly/ai-platform/pull/892))

## [v0.2.78] - 2026-02-17

### Added
- Metrics support via PodMonitor ([FFP-71613](https://jira.corp.adobe.com/browse/FFP-71613), [#872](https://github.com/Adobe-Firefly/ai-platform/pull/872))

### Fixed
- Dependency versions updated to allow using the framework from editable install ([#890](https://github.com/Adobe-Firefly/ai-platform/pull/890))

## [v0.2.77] - 2026-02-09

### Changed
- Switched to new Artifactory container registry ([FFP-67768](https://jira.corp.adobe.com/browse/FFP-67768), [#875](https://github.com/Adobe-Firefly/ai-platform/pull/875))

## [v0.2.76] - 2026-02-02

### Added
- Ingress unit tests ([FFP-67282](https://jira.corp.adobe.com/browse/FFP-67282), [#833](https://github.com/Adobe-Firefly/ai-platform/pull/833))

### Changed
- Cluster renamed from `ethoshub` to `ethos-hub`; cleanup of services files ([FFP-67832](https://jira.corp.adobe.com/browse/FFP-67832), [#843](https://github.com/Adobe-Firefly/ai-platform/pull/843), [#847](https://github.com/Adobe-Firefly/ai-platform/pull/847), [#848](https://github.com/Adobe-Firefly/ai-platform/pull/848))

## [v0.2.75] - 2026-01-20

### Fixed
- Docker image building regression ([#837](https://github.com/Adobe-Firefly/ai-platform/pull/837))

## [v0.2.74] - 2026-01-20

### Added
- Ingress throttling ([FFP-67280](https://jira.corp.adobe.com/browse/FFP-67280), [#760](https://github.com/Adobe-Firefly/ai-platform/pull/760))

### Removed
- Circular dependency: inference chart no longer depends on inference framework ([FFP-69076](https://jira.corp.adobe.com/browse/FFP-69076), [#831](https://github.com/Adobe-Firefly/ai-platform/pull/831))

## [v0.2.73] - 2026-01-19

### Changed
- `platforms/inference` and services ecosystem decoupled ([FFP-69724](https://jira.corp.adobe.com/browse/FFP-69724), [#828](https://github.com/Adobe-Firefly/ai-platform/pull/828))

## [v0.2.71] - 2026-01-16

### Fixed
- Misleading frontend component name ([#809](https://github.com/Adobe-Firefly/ai-platform/pull/809))

## [v0.2.70] - 2026-01-15

### Changed
- Nginx proxy removed from CI; `rules_python` and `rules_oci` updated ([#799](https://github.com/Adobe-Firefly/ai-platform/pull/799), [#801](https://github.com/Adobe-Firefly/ai-platform/pull/801), [#807](https://github.com/Adobe-Firefly/ai-platform/pull/807))
- `./bazel` binary decoupled from gtools ([FFP-69724](https://jira.corp.adobe.com/browse/FFP-69724), [#806](https://github.com/Adobe-Firefly/ai-platform/pull/806))

## [v0.2.69] - 2026-01-09

### Changed
- `rules_python` updated ([FFP-65851](https://jira.corp.adobe.com/browse/FFP-65851), [#796](https://github.com/Adobe-Firefly/ai-platform/pull/796))

## [v0.2.68] - 2026-01-07

### Removed
- Cyclic dependency between `platform/make` and managed services ([FFP-65851](https://jira.corp.adobe.com/browse/FFP-65851), [#786](https://github.com/Adobe-Firefly/ai-platform/pull/786))

## [v0.2.67] - 2026-01-06

### Added
- Improved Python debugging experience ([FFP-69075](https://jira.corp.adobe.com/browse/FFP-69075), [#769](https://github.com/Adobe-Firefly/ai-platform/pull/769))

## [v0.2.66] - 2025-12-17

### Changed
- GHA actions updated to be usable by external repos ([FFP-68343](https://jira.corp.adobe.com/browse/FFP-68343), [#753](https://github.com/Adobe-Firefly/ai-platform/pull/753))

## [v0.2.65] - 2025-12-16

### Added
- v3 ingress support ([FFP-67046](https://jira.corp.adobe.com/browse/FFP-67046), [#741](https://github.com/Adobe-Firefly/ai-platform/pull/741))

### Fixed
- Bloated (2×) Docker images ([FFP-56304](https://jira.corp.adobe.com/browse/FFP-56304), [#725](https://github.com/Adobe-Firefly/ai-platform/pull/725))

## [v0.2.63] - 2025-12-05

### Removed
- All references to custom `py_binary` ([FFP-56304](https://jira.corp.adobe.com/browse/FFP-56304), [#723](https://github.com/Adobe-Firefly/ai-platform/pull/723))

## [v0.2.62] - 2025-12-05

### Changed
- Switched to `rules_python`'s modern executable approach ([FFP-56304](https://jira.corp.adobe.com/browse/FFP-56304), [#718](https://github.com/Adobe-Firefly/ai-platform/pull/718))

## [v0.2.60] - 2025-12-05

### Fixed
- Inference framework incompatibility with Sample E ([FFP-63554](https://jira.corp.adobe.com/browse/FFP-63554), [#720](https://github.com/Adobe-Firefly/ai-platform/pull/720))
- Duplicate dependency versions reduced ([FFP-66091](https://jira.corp.adobe.com/browse/FFP-66091), [#708](https://github.com/Adobe-Firefly/ai-platform/pull/708))

## [v0.2.59] - 2025-12-02

### Added
- Sample E can now run locally on macOS ([FFP-59510](https://jira.corp.adobe.com/browse/FFP-59510), [#634](https://github.com/Adobe-Firefly/ai-platform/pull/634))

### Fixed
- Nginx cache pull failure in CI ([#710](https://github.com/Adobe-Firefly/ai-platform/pull/710))

## [v0.2.58] - 2025-12-02

### Fixed
- `.ethos.yaml` validity ([FFP-66092](https://jira.corp.adobe.com/browse/FFP-66092), [#707](https://github.com/Adobe-Firefly/ai-platform/pull/707))

## [v0.2.57] - 2025-12-01

### Fixed
- S3 auth in HTTP server ([FFP-65229](https://jira.corp.adobe.com/browse/FFP-65229), [#701](https://github.com/Adobe-Firefly/ai-platform/pull/701))

## [v0.2.56] - 2025-11-27

### Added
- Tensor serialization/deserialization between worker calls ([FFP-65230](https://jira.corp.adobe.com/browse/FFP-65230), [#695](https://github.com/Adobe-Firefly/ai-platform/pull/695))

## [v0.2.55] - 2025-11-25

### Fixed
- `.so` loading for Docker image entrypoints ([FFP-64904](https://jira.corp.adobe.com/browse/FFP-64904), [#676](https://github.com/Adobe-Firefly/ai-platform/pull/676))
- `s5cmd` now included in editable install ([FFP-64901](https://jira.corp.adobe.com/browse/FFP-64901), [#677](https://github.com/Adobe-Firefly/ai-platform/pull/677))
- Binary metadata mismatch between refs and tarballs ([FFP-63992](https://jira.corp.adobe.com/browse/FFP-63992), [#639](https://github.com/Adobe-Firefly/ai-platform/pull/639))

## [v0.2.54] - 2025-11-12

### Added
- Hardware specification API ([FFP-60595](https://jira.corp.adobe.com/browse/FFP-60595), [#511](https://github.com/Adobe-Firefly/ai-platform/pull/511))

## [v0.2.53] - 2025-11-04

### Fixed
- Inference application base image layer ([FFP-58623](https://jira.corp.adobe.com/browse/FFP-58623), [#570](https://github.com/Adobe-Firefly/ai-platform/pull/570))

## [v0.2.52] - 2025-11-03

### Changed
- `ethos.yaml` generation simplified; comments preserved ([FFP-60592](https://jira.corp.adobe.com/browse/FFP-60592), [#581](https://github.com/Adobe-Firefly/ai-platform/pull/581))

## [v0.2.51] - 2025-10-29

### Added
- Test environment for integration testing ([FFP-60592](https://jira.corp.adobe.com/browse/FFP-60592), [#505](https://github.com/Adobe-Firefly/ai-platform/pull/505))

### Changed
- `frameworks/inference` restructured as a folder-of-folders ([FFP-61744](https://jira.corp.adobe.com/browse/FFP-61744), [#585](https://github.com/Adobe-Firefly/ai-platform/pull/585))

### Fixed
- NGINX startup transient failure ([FFP-61562](https://jira.corp.adobe.com/browse/FFP-61562), [#528](https://github.com/Adobe-Firefly/ai-platform/pull/528))
- Symlink regression from restructure ([FFP-61744](https://jira.corp.adobe.com/browse/FFP-61744), [#589](https://github.com/Adobe-Firefly/ai-platform/pull/589))

## [v0.2.50] - 2025-10-16

### Fixed
- Race condition in binary cache download ([FFP-61352](https://jira.corp.adobe.com/browse/FFP-61352), [#521](https://github.com/Adobe-Firefly/ai-platform/pull/521))

## [v0.2.49] - 2025-10-16

### Fixed
- `binary_group()` targets not getting Bazel cache hits ([FFP-61352](https://jira.corp.adobe.com/browse/FFP-61352), [#520](https://github.com/Adobe-Firefly/ai-platform/pull/520))

## [v0.2.47] - 2025-10-16

### Fixed
- Bazel no longer reads `ARTIFACTORY_*`/`XDG_CACHE_HOME` env vars, improving remote cache hit rate ([FFP-60965](https://jira.corp.adobe.com/browse/FFP-60965), [#517](https://github.com/Adobe-Firefly/ai-platform/pull/517))

## [v0.2.44] - 2025-10-16

### Added
- Bazel remote cache support ([FFP-60967](https://jira.corp.adobe.com/browse/FFP-60967), [#514](https://github.com/Adobe-Firefly/ai-platform/pull/514))
- Remote Redis instance used instead of local workaround ([FFP-58623](https://jira.corp.adobe.com/browse/FFP-58623), [#456](https://github.com/Adobe-Firefly/ai-platform/pull/456))

## [v0.2.43] - 2025-10-14

### Changed
- RBAC groups moved to separate files ([FFP-54971](https://jira.corp.adobe.com/browse/FFP-54971), [#465](https://github.com/Adobe-Firefly/ai-platform/pull/465))

## [v0.2.41] - 2025-10-03

### Added
- Worker templates for services using model hub ([FFP-59248](https://jira.corp.adobe.com/browse/FFP-59248), [#475](https://github.com/Adobe-Firefly/ai-platform/pull/475))

## [v0.2.40] - 2025-09-30

### Added
- Updated torch support ([FFP-58555](https://jira.corp.adobe.com/browse/FFP-58555), [#454](https://github.com/Adobe-Firefly/ai-platform/pull/454))
- Improved VSCode/Jupyter development experience ([FFP-58554](https://jira.corp.adobe.com/browse/FFP-58554), [#462](https://github.com/Adobe-Firefly/ai-platform/pull/462))

## [v0.2.39] - 2025-09-30

### Removed
- LDAP groups moved out of infra/gitops to break cyclic dependency ([FFP-58343](https://jira.corp.adobe.com/browse/FFP-58343), [#445](https://github.com/Adobe-Firefly/ai-platform/pull/445))

## [v0.2.37] - 2025-09-29

### Added
- Colligo v2 namespace deployment support ([FFP-58416](https://jira.corp.adobe.com/browse/FFP-58416), [#442](https://github.com/Adobe-Firefly/ai-platform/pull/442))

### Changed
- Switched to new S3 credentials ([FFP-58599](https://jira.corp.adobe.com/browse/FFP-58599), [#452](https://github.com/Adobe-Firefly/ai-platform/pull/452))

## [v0.2.35] - 2025-09-29

### Added
- Model hub support in the inference ecosystem ([FFP-55786](https://jira.corp.adobe.com/browse/FFP-55786), [#439](https://github.com/Adobe-Firefly/ai-platform/pull/439))

## [v0.2.34] - 2025-09-23

### Added
- Splunk logging enabled ([FFP-54970](https://jira.corp.adobe.com/browse/FFP-54970), [#428](https://github.com/Adobe-Firefly/ai-platform/pull/428))

## [v0.2.32] - 2025-09-17

### Added
- Chart version freezing support ([FFP-49271](https://jira.corp.adobe.com/browse/FFP-49271), [#402](https://github.com/Adobe-Firefly/ai-platform/pull/402))
- Hook JSON support ([FFP-50478](https://jira.corp.adobe.com/browse/FFP-50478), [#382](https://github.com/Adobe-Firefly/ai-platform/pull/382))

## [v0.2.31] - 2025-09-11

### Added
- Platform code propagated to services ecosystem ([FFP-54964](https://jira.corp.adobe.com/browse/FFP-54964), [#376](https://github.com/Adobe-Firefly/ai-platform/pull/376))
- Metadata JSON uploaded to Artifactory ([FFP-50454](https://jira.corp.adobe.com/browse/FFP-50454), [#351](https://github.com/Adobe-Firefly/ai-platform/pull/351))

## [v0.2.29] - 2025-09-03

### Added
- Config map redeployment triggered on update ([FFP-54963](https://jira.corp.adobe.com/browse/FFP-54963), [#369](https://github.com/Adobe-Firefly/ai-platform/pull/369))
- Dict-style deployment definitions ([FFP-54965](https://jira.corp.adobe.com/browse/FFP-54965), [#370](https://github.com/Adobe-Firefly/ai-platform/pull/370))
- Corp HTTP ingress for inference services ([FFP-51708](https://jira.corp.adobe.com/browse/FFP-51708), [#372](https://github.com/Adobe-Firefly/ai-platform/pull/372))
- Auto-complete for `values.inference.yaml` ([FFP-54964](https://jira.corp.adobe.com/browse/FFP-54964), [#371](https://github.com/Adobe-Firefly/ai-platform/pull/371))

## [v0.2.26] - 2025-09-01

### Fixed
- Argo-sync logic ([FFP-54613](https://jira.corp.adobe.com/browse/FFP-54613), [#367](https://github.com/Adobe-Firefly/ai-platform/pull/367))

## [v0.2.25] - 2025-08-29

### Added
- Redis cluster with Vault secret injection ([FFP-53664](https://jira.corp.adobe.com/browse/FFP-53664), [#337](https://github.com/Adobe-Firefly/ai-platform/pull/337)–[#350](https://github.com/Adobe-Firefly/ai-platform/pull/350))
- ConfigMap generation ([FFP-50251](https://jira.corp.adobe.com/browse/FFP-50251), [#333](https://github.com/Adobe-Firefly/ai-platform/pull/333))
- Deployment env var overrides ([FFP-51705](https://jira.corp.adobe.com/browse/FFP-51705), [#320](https://github.com/Adobe-Firefly/ai-platform/pull/320))
- `inference_application()` JSON metadata output ([FFP-50454](https://jira.corp.adobe.com/browse/FFP-50454), [#310](https://github.com/Adobe-Firefly/ai-platform/pull/310))

## [v0.2.22] - 2025-08-20

### Added
- Docker image URL and entry point wired into the inference chart ([FFP-50249](https://jira.corp.adobe.com/browse/FFP-50249), [#321](https://github.com/Adobe-Firefly/ai-platform/pull/321), [#322](https://github.com/Adobe-Firefly/ai-platform/pull/322))

## [v0.2.21] - 2025-08-19

### Changed
- YAML spec comparison and copy now run in the `./bazel test` step ([FFP-50457](https://jira.corp.adobe.com/browse/FFP-50457), [#311](https://github.com/Adobe-Firefly/ai-platform/pull/311))

## [v0.2.20] - 2025-08-18

### Changed
- Platform changes propagated to service ecosystem ([FFP-49581](https://jira.corp.adobe.com/browse/FFP-49581), [#308](https://github.com/Adobe-Firefly/ai-platform/pull/308))

## [v0.2.19] - 2025-08-18

### Changed
- API moved to `__init__.py` for cleaner imports ([FFP-52974](https://jira.corp.adobe.com/browse/FFP-52974), [#299](https://github.com/Adobe-Firefly/ai-platform/pull/299))

### Fixed
- Inference chart YAML trailing-space formatting ([FFP-52976](https://jira.corp.adobe.com/browse/FFP-52976), [#296](https://github.com/Adobe-Firefly/ai-platform/pull/296))

## [v0.2.18] - 2025-08-16

### Added
- Service ecosystem updated with binary management support ([FFP-48323](https://jira.corp.adobe.com/browse/FFP-48323), [#293](https://github.com/Adobe-Firefly/ai-platform/pull/293))

## [v0.2.15] - 2025-08-15

### Fixed
- Worker and webapps chart templates ([FFP-48323](https://jira.corp.adobe.com/browse/FFP-48323), [#292](https://github.com/Adobe-Firefly/ai-platform/pull/292))

## [v0.2.14] - 2025-08-15

### Added
- Binary management infrastructure ([FFP-48323](https://jira.corp.adobe.com/browse/FFP-48323), [#291](https://github.com/Adobe-Firefly/ai-platform/pull/291))
- Pre-merge check to ensure YAML specs are up to date ([FFP-46398](https://jira.corp.adobe.com/browse/FFP-46398), [#225](https://github.com/Adobe-Firefly/ai-platform/pull/225))

## [v0.2.13] - 2025-08-14

### Added
- K8s specs generated per pod worker separately ([FFP-50468](https://jira.corp.adobe.com/browse/FFP-50468), [#257](https://github.com/Adobe-Firefly/ai-platform/pull/257))

### Changed
- `inference_renderer` simplified ([FFP-50452](https://jira.corp.adobe.com/browse/FFP-50452), [#224](https://github.com/Adobe-Firefly/ai-platform/pull/224))
- Build output path normalized to remove OS-specific parts ([FFP-48776](https://jira.corp.adobe.com/browse/FFP-48776), [#284](https://github.com/Adobe-Firefly/ai-platform/pull/284))

## [v0.2.12] - 2025-07-29

### Changed
- `python_chart/inference` migrated into `inference_renderer` ([FFP-50452](https://jira.corp.adobe.com/browse/FFP-50452), [#211](https://github.com/Adobe-Firefly/ai-platform/pull/211))

## [v0.2.11] - 2025-07-29

### Added
- Editable install and release process established ([FFP-47801](https://jira.corp.adobe.com/browse/FFP-47801), [#206](https://github.com/Adobe-Firefly/ai-platform/pull/206))
