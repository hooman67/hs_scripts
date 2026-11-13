---
sectnum: false
---

# Inference Chart

Available as `@platforms_inference//:ai-inference-chart`, and can be used with the `ethos_deployment()` and `k8s_values()` APIs.

This is a successor to the [rhode](https://git.corp.adobe.com/firefly/colligo-deploy/tree/main/charts/rhode) chart, and can create multiple deployments and other required resources.

## Values API

(api-doc-inferencevalues)=
[**`InferenceValues`**](api-doc-inferencevalues)

Parameters specific to the inference renderer chart.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `json_spec` | str \\| None | `None` | Artifactory path to the JSON metadata file |
| `application_name` | `str` | *required* | The name of the application. Must start/end with alphanumeric, contain only ``[a-zA-Z0-9_.-]``, max 63 chars. |
| `image` | `str` | `''` | Link to the docker image of the application |
| `image_pull_secrets` | `ImagePullSecrets` | *required* | Secrets for pulling images from a private registry. |
| `deployments` | dict[str, WorkerDeployment \\| HttpServerDeployment \\| WatchdogDeployment] | `{}` | Dictionary mapping pod names to deployment configurations. The pod name (deployment key) is arbitrary and does not need to match a worker ref. The actual workers each pod runs are specified in ``processes`` (defaults to one process for the worker ref matching the pod name). Conventionally, pod names are set to the worker ref so that the process name inherits it — but for GPU-sharing scenarios where one pod runs multiple workers, a custom name is used. The last segment of each worker ref is used as the Redis queue name, K8s label, and metric label and must be unique across all workers in the application. |
| `env_vars` | `EnvVars` | `EnvVars()` | Global environment variables for the application. |
| `runtime_config` | `RuntimeCofigs` | `RuntimeCofigs()` | Runtime configuration that the entry point of each pod will read. |
| `iam_role` | str \\| None | `None` | The iam role to associate with the pods |
| `logging` | LoggingConfig \| None | `None` | Logging configuration for the application |
| `enable_metrics` | `bool` | `True` | Whether to enable metrics for the application |

(api-doc-basedeployment)=
[**`BaseDeployment`**](api-doc-basedeployment)

Shared attributes of a deployment

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `replicas` | int \\| None | `None` | The number of replicas for the deployment. Cannot be set when autoscaling is configured (mutually exclusive). If not specified and no autoscaling is configured, defaults to 0 (deployment is skipped). |
| `env_vars` | `EnvVars` | `EnvVars()` | Environment variables for the deployment. |
| `image` | str \\| None | `None` | Optional override for the docker image of this deployment. |
| `iam_role` | str \\| None | `None` | The iam role to associate with the pods. Overrides application iam role. |
| `runtime_config` | `RuntimeCofigs` | `RuntimeCofigs()` | Runtime configuration that this pod will read. This will merge with the application.runtime_config. |
| `hardware` | CpuHardware \\| GpuHardware \\| None | `None` | Hardware specification for the deployment (user override). This takes precendence over preferred_hardware |
| `preferred_hardware` | WorkerCpuPreference \\| WorkerGpuPreference \\| None | `None` | Worker preferred hardware from ServeConfig. |
| `ingress` | Ingress \| None | `None` | Optional ingress configuration |
| `autoscaling` | AutoScalingConfig \\| None | `None` | Autoscaler configuration. Behavior depends on deployment type and environment. Cannot be set when replicas is explicitly configured (mutually exclusive). |
| `startup_probe` | ProbeConfig \\| None | `None` | Override startup probe timing. |
| `liveness_probe` | ProbeConfig \\| None | `None` | Override liveness probe timing. |
| `readiness_probe` | ProbeConfig \\| None | `None` | Override readiness probe timing. |
| `rollout` | `RollingRollout` | `RollingRollout()` | Rollout strategy. Defaults: maxSurge 100%, maxUnavailable 20%. |
| `localssd` | bool \\| None | `None` | Mount node-local NVMe SSD at /mnt/localssd via an ephemeral PVC (storageClassName: local-ssd). Defaults to true for GPU deployments, false for CPU. Set explicitly to override. |

(api-doc-workerdeployment)=
[**`WorkerDeployment`**](api-doc-workerdeployment)

Deployment of an inference worker.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `replicas` | int \\| None | `None` | The number of replicas for the deployment. Cannot be set when autoscaling is configured (mutually exclusive). If not specified and no autoscaling is configured, defaults to 0 (deployment is skipped). |
| `env_vars` | `EnvVars` | `EnvVars()` | Environment variables for the deployment. |
| `image` | str \\| None | `None` | Optional override for the docker image of this deployment. |
| `iam_role` | str \\| None | `None` | The iam role to associate with the pods. Overrides application iam role. |
| `runtime_config` | `RuntimeCofigs` | `RuntimeCofigs()` | Runtime configuration that this pod will read. This will merge with the application.runtime_config. |
| `hardware` | CpuHardware \\| GpuHardware \\| None | `None` | Hardware specification for the deployment (user override). This takes precendence over preferred_hardware |
| `preferred_hardware` | WorkerCpuPreference \\| WorkerGpuPreference \\| None | `None` | Worker preferred hardware from ServeConfig. |
| `ingress` | Ingress \| None | `None` | Optional ingress configuration |
| `autoscaling` | AutoScalingConfig \\| None | `None` | Autoscaler configuration. Behavior depends on deployment type and environment. Cannot be set when replicas is explicitly configured (mutually exclusive). |
| `startup_probe` | ProbeConfig \\| None | `None` | Override startup probe timing. |
| `liveness_probe` | ProbeConfig \\| None | `None` | Override liveness probe timing. |
| `readiness_probe` | ProbeConfig \\| None | `None` | Override readiness probe timing. |
| `rollout` | `RollingRollout` | `RollingRollout()` | Rollout strategy. Defaults: maxSurge 100%, maxUnavailable 20%. |
| `localssd` | bool \\| None | `None` | Mount node-local NVMe SSD at /mnt/localssd via an ephemeral PVC (storageClassName: local-ssd). Defaults to true for GPU deployments, false for CPU. Set explicitly to override. |
| `type` | `Literal['worker']` | `'worker'` |  |
| `processes` | `dict[str, int]` | `{}` | Mapping of worker reference to number of processes to launch for the worker. The default value is `{<name>: 1}` (i.e. assuming this deployment maps to a worker with the same name, and deploys a single instance of it). At render time, each worker ref is passed once to `python -m frameworks.inference workers`, and the count is injected into this deployment's runtime config as `<worker_ref>.serve_config.num_processes`. |
| `extra_tolerations` | list[Toleration] \\| None | `None` | Additional tolerations appended to auto-generated ones. |

(api-doc-httpserverdeployment)=
[**`HttpServerDeployment`**](api-doc-httpserverdeployment)

Deployment of an http server (that serves the web apps).

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `replicas` | int \\| None | `None` | The number of replicas for the deployment. Cannot be set when autoscaling is configured (mutually exclusive). If not specified and no autoscaling is configured, defaults to 0 (deployment is skipped). |
| `env_vars` | `EnvVars` | `EnvVars()` | Environment variables for the deployment. |
| `image` | str \\| None | `None` | Optional override for the docker image of this deployment. |
| `iam_role` | str \\| None | `None` | The iam role to associate with the pods. Overrides application iam role. |
| `runtime_config` | `RuntimeCofigs` | `RuntimeCofigs()` | Runtime configuration that this pod will read. This will merge with the application.runtime_config. |
| `hardware` | CpuHardware \\| GpuHardware \\| None | `None` | Hardware specification for the deployment (user override). This takes precendence over preferred_hardware |
| `preferred_hardware` | WorkerCpuPreference \\| WorkerGpuPreference \\| None | `None` | Worker preferred hardware from ServeConfig. |
| `ingress` | Ingress \| None | `None` | Optional ingress configuration |
| `autoscaling` | AutoScalingConfig \\| None | `None` | Autoscaler configuration. Behavior depends on deployment type and environment. Cannot be set when replicas is explicitly configured (mutually exclusive). |
| `startup_probe` | ProbeConfig \\| None | `None` | Override startup probe timing. |
| `liveness_probe` | ProbeConfig \\| None | `None` | Override liveness probe timing. |
| `readiness_probe` | ProbeConfig \\| None | `None` | Override readiness probe timing. |
| `rollout` | `RollingRollout` | `RollingRollout()` | Rollout strategy. Defaults: maxSurge 100%, maxUnavailable 20%. |
| `localssd` | bool \\| None | `None` | Mount node-local NVMe SSD at /mnt/localssd via an ephemeral PVC (storageClassName: local-ssd). Defaults to true for GPU deployments, false for CPU. Set explicitly to override. |
| `type` | `Literal['http_server']` | `'http_server'` |  |
| `serves` | `list[str]` | *required* | References of all the web apps that should be included in this HTTP server. (min length: 1) |
| `port` | `int` | `8000` | The port to expose the http server. |

(api-doc-watchdogdeployment)=
[**`WatchdogDeployment`**](api-doc-watchdogdeployment)

Deployment of the job watchdog process that monitors background job queues.

The watchdog detects abandoned or timed-out jobs and restarts them.
Only one watchdog is needed per application. It always runs on CPU (small)
with no autoscaling or ingress.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `replicas` | `Literal[1]` | `1` | Number of replicas. Always 1 (singleton watchdog). |
| `env_vars` | `EnvVars` | `EnvVars()` | Environment variables for the deployment. |
| `image` | str \\| None | `None` | Optional override for the docker image of this deployment. |
| `iam_role` | str \\| None | `None` | The iam role to associate with the pods. Overrides application iam role. |
| `runtime_config` | `RuntimeCofigs` | `RuntimeCofigs()` | Runtime configuration that this pod will read. This will merge with the application.runtime_config. |
| `hardware` | `CpuHardware` | `CpuHardware()` | Hardware specification. Always CPU; defaults to CPU (small). |
| `preferred_hardware` | WorkerCpuPreference \\| WorkerGpuPreference \\| None | `None` | Worker preferred hardware from ServeConfig. |
| `ingress` | `None` | `None` | Ingress is not supported for watchdog deployments. |
| `autoscaling` | `None` | `None` | Autoscaling is not supported for watchdog deployments. |
| `startup_probe` | ProbeConfig \\| None | `None` | Override startup probe timing. |
| `liveness_probe` | ProbeConfig \\| None | `None` | Override liveness probe timing. |
| `readiness_probe` | ProbeConfig \\| None | `None` | Override readiness probe timing. |
| `rollout` | `RollingRollout` | `RollingRollout()` | Rollout strategy. Defaults: maxSurge 100%, maxUnavailable 20%. |
| `localssd` | bool \\| None | `None` | Mount node-local NVMe SSD at /mnt/localssd via an ephemeral PVC (storageClassName: local-ssd). Defaults to true for GPU deployments, false for CPU. Set explicitly to override. |
| `type` | `Literal['watchdog']` | `'watchdog'` |  |
| `queues` | `list[str]` | *required* | Worker refs whose queues the watchdog should monitor. |

(api-doc-cpuhardware)=
[**`CpuHardware`**](api-doc-cpuhardware)

CPU hardware specification.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `xpu` | `Literal['cpu']` | `'cpu'` |  |
| `size` | `Literal['small', 'medium', 'large', 'xlarge']` | `'small'` | CPU tier size. Options: small, medium, large, xlarge |

(api-doc-gpuhardware)=
[**`GpuHardware`**](api-doc-gpuhardware)

GPU hardware specification for direct user specification in inference values.

This allows users to directly specify concrete GPU types and counts.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `xpu` | `Literal['ampere_40gb', 'ampere_80gb', 'hopper_80gb', 'hopper_140gb']` | *required* | GPU type. Options: ampere_40gb, ampere_80gb, hopper_80gb, hopper_140gb |
| `num_gpus` | `Literal[1, 2, 4, 8]` | `1` | Number of GPUs. Options: 1, 2, 4, 8 |

```{note}
GPU deployments automatically mount a memory-backed `/dev/shm` volume sized at **3 GiB per GPU** (e.g. 24 GiB for an 8-GPU pod). This is required by vLLM, PyTorch multiprocessing, and NCCL for inter-process communication — Kubernetes' default 64 MiB `/dev/shm` is too small.
```

(api-doc-workercpupreference)=
[**`WorkerCpuPreference`**](api-doc-workercpupreference)

Worker CPU preference from ServeConfig.

This matches the CpuRequirement type from frameworks.inference ServeConfig.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `xpu` | `Literal['cpu']` | `'cpu'` |  |
| `size` | `Literal['small', 'medium', 'large', 'xlarge']` | `'small'` |  |

(api-doc-workergpupreference)=
[**`WorkerGpuPreference`**](api-doc-workergpupreference)

Worker GPU preference from ServeConfig.

This matches the GpuRequirement type from frameworks.inference ServeConfig.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `xpu` | `Literal['gpu']` | `'gpu'` |  |
| `num` | `int` | `1` |  |
| `memory` | float \\| None | `None` | GPU memory requirement in GB. If None, allows any GPU. |
| `preferred_family` | `Literal['ampere', 'hopper', 'blackwell', None]` | `None` | Preferred GPU family. If not specified, will pick based on memory requirement. |

(api-doc-imagepullsecrets)=
[**`ImagePullSecrets`**](api-doc-imagepullsecrets)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `secret_ref` | str \\| None | `None` |  |
| `username_field_name` | `str` | *required* |  |
| `password_field_name` | `str` | *required* |  |

(api-doc-envvars)=
[**`EnvVars`**](api-doc-envvars)

Environment variable configuration for a deployment.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `non_secrets` | dict[str, EnvVar] \\| None | `None` | Non-secret environment variables. |
| `secrets` | dict[str, Secret] \\| None | `None` | Secret environment variables. |

(api-doc-secret)=
[**`Secret`**](api-doc-secret)

A secret environment variable sourced from a secret store.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `secret_ref_path` | `str` | *required* | Path to the secret in the secret store. |
| `field` | `str` | *required* | Field name within the secret. |
| `secret_store_ref` | str \\| None | `None` | Optional reference to a specific secret store. |

(api-doc-loggingconfig)=
[**`LoggingConfig`**](api-doc-loggingconfig)

Configuration for logging capture in ethos deployments.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `index` | `str` | *required* | The logging index to use for log aggregation |
| `source_type` | `str` | *required* | The source type for log classification |

(api-doc-autoscalingconfig)=
[**`AutoScalingConfig`**](api-doc-autoscalingconfig)

Autoscaling configuration.

Choose cpu_scaling OR gpu_scaling based on worker hardware type.
Exactly one of cpu_scaling or gpu_scaling must be set.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `cpu_scaling` | CPUScalingConfig \\| None | `None` | CPU worker autoscaling configuration. |
| `gpu_scaling` | GPUScalingConfig \\| None | `None` | GPU worker autoscaling configuration. |

(api-doc-cpuscalingconfig)=
[**`CPUScalingConfig`**](api-doc-cpuscalingconfig)

CPU worker autoscaling configuration.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `min_replicas` | int \\| None | `None` | Minimum number of replicas. Defaults to deployment.replicas if not set. |
| `max_replicas` | int \\| None | `None` | Maximum number of replicas. When None and queue_based_scaling is enabled, calculated using formula: min_replicas^0.75 + min_replicas + 5. |
| `queue_based_scaling` | bool \\| QueueBasedScalingConfig \\| None | `False` | Queue-based HPA scaling using Prometheus metrics. Set to true to use defaults, or provide config. |

(api-doc-gpuscalingconfig)=
[**`GPUScalingConfig`**](api-doc-gpuscalingconfig)

GPU worker autoscaling configuration.

Supports Oshiya prediction-based scaling (enabled by default),
optionally extended with queue-based HPA and event-driven KEDA.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `min_replicas` | int \\| None | `None` | Minimum number of replicas. Defaults to deployment.replicas if not set. |
| `max_replicas` | int \\| None | `None` | Maximum number of replicas. When None: if scale_to_zero (KEDA) enabled, defaults to deployment.replicas; else if queue_based_scaling enabled, uses formula min_replicas^0.75 + min_replicas + 5; else omitted (Oshiya calculates it). |
| `prediction_based_scaling` | bool \\| PredictionBasedScalingConfig | `True` | Oshiya prediction-based scaling. Set to true for defaults (default), false to disable, or provide custom config. |
| `queue_based_scaling` | bool \\| QueueBasedScalingConfig \\| None | `None` | Queue-based HPA scaling. Set to true for defaults, or provide custom config. Requires prediction_based_scaling enabled. |
| `scale_to_zero` | bool \\| ScaleToZeroConfig \\| None | `None` | KEDA event-driven scaling with scale-to-zero. Set to true for defaults, or provide custom config. Requires prediction_based_scaling enabled. |

(api-doc-queuebasedscalingconfig)=
[**`QueueBasedScalingConfig`**](api-doc-queuebasedscalingconfig)

Configuration for queue-based HPA autoscaling using Prometheus metrics.

Creates HorizontalPodAutoscaler for scaling based on queue length, CPU, and memory.
Supported by both CPU and GPU workers.
On GPU workers, the HPA is created dynamically at runtime by Oshiya, it will not be seen in the deployment spec.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | `bool` | `True` | Enable/disable queue-based scaling. Default is true when configured. |
| `queue_name` | str \\| None | `None` | Queue name to monitor for scaling. Defaults to worker name. Should not include ':internal' suffix. |
| `metric_name` | `str` | `'usm_object_colligo_queue_requests_in_progress'` | Prometheus metric name to use for scaling decisions. For the dev environment, the default metric becomes usm_object_colligo_queue_requests_in_progress_dev. |
| `average_value` | `int` | `5` | Target average value of the metric per replica. Scaling occurs when actual value exceeds this. |
| `average_value_format` | Literal['default', 'MI'] \\| None | `None` | Format for average_value. Use 'MI' to support fractional target values (e.g., average_value=1500 with MI means 1.5). |
| `average_cpu_utilization` | `int` | `90` | Target average CPU utilization percentage across all pods. |
| `average_memory_utilization` | `int` | `80` | Target average memory utilization percentage across all pods. |
| `scale_down` | ScalePolicy \\| None | `None` | Policy for scaling down. If not set, uses default values. |
| `scale_up` | ScalePolicy \\| None | `None` | Policy for scaling up. If not set, uses default values. |

(api-doc-predictionbasedscalingconfig)=
[**`PredictionBasedScalingConfig`**](api-doc-predictionbasedscalingconfig)

Configuration for Oshiya GPU prediction-based autoscaling.

Uses historical traffic data to predict optimal replica counts.
Only supported for GPU workers.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | `bool` | `True` | Enable/disable prediction-based scaling. Default is true when configured. |
| `buffer_replicas` | `int` | `0` | Extra replicas to add on top of min_replicas when capacity is available. Allows faster scale-up. |
| `boost_factor` | `float` | `1.0` | Factor to make this worker more preferable for scaling up. Higher values = more priority. |

(api-doc-scaletozeroconfig)=
[**`ScaleToZeroConfig`**](api-doc-scaletozeroconfig)

Configuration for KEDA event-driven autoscaling with scale-to-zero support.

KEDA requirements:
- Only supported for GPU workers
- Requires prediction_based_scaling to be enabled
- Requires `check_worker_before_call: false` and `enable_worker_warming: true` in the runtimeconfig to work correctly

Architecture doc: https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=GenAI&title=FFP-62810+-+Scale-to-Zero+API+and+UX

| Field                  | Type | Default                                                             | Description |
|------------------------|------|---------------------------------------------------------------------|-------------|
| `enabled`              | `bool` | `True`                                                              | Enable/disable KEDA scaling. Default is true when configured. |
| `idle_replica_count`   | `int` | `0`                                                                 | Replicas when idle (0 = scale-to-zero). |
| `polling_interval`     | `int` | `10`                                                                | How often KEDA checks metrics (seconds). |
| `cooldown_period`      | `int` | `600`                                                               | Wait time before scaling to zero after last trigger (seconds). Maximum 4 hours (14400 seconds). (≤ 14400) |
| `server_address`       | `str` | `'http://app-promoperator-prometheus.ns-team-firefly-enm.svc.cluster.local:9090'` | Prometheus server address for KEDA queries. |
| `metric_name`          | `str` | `'usm_object_colligo_queue_requests_in_progress'`                   | Prometheus metric name to monitor. Your application must write this metric. For the dev environment, the default metric is usm_object_colligo_queue_requests_in_progress_dev.The usm_object... metric is created by a prometheus record rule, not by the code itself https://git.corp.adobe.com/firefly/firefly-monitoring/blob/main/charts/enm-base/templates/general/prometheus-rules-stage.yaml |
| `threshold`            | `str` | `'5'`                                                               | Threshold value as string (e.g., '1', '5', '3.5'). Used by KEDA to calculate the desired number of replicas: desiredReplicas = ceil(metricValue / threshold). Does not affect scale-from-zero behavior. |
| `activation_threshold` | `str` | `'0'`                                                               | It defines the minimum metric value required to activate the scaler and scale up from 0 to minReplicaCount. The trigger is activated only when metric (or warm up) > activationThreshold. |
| `scale_down`           | ScalePolicy \\| None | `None`                                                              | Policy for scaling down. |
| `scale_up`             | ScalePolicy \\| None | `None`                                                              | Policy for scaling up. |

(api-doc-scalepolicy)=
[**`ScalePolicy`**](api-doc-scalepolicy)

Policy for controlling how fast scaling happens.

Used to configure both scale_up and scale_down behavior in HPA.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `period_seconds` | `int` | `300` | How often (in seconds) the scaling policy is evaluated. |
| `stabilization_window_seconds` | `int` | `900` | Time window (in seconds) to look back at metrics before making a scaling decision. |
| `pods` | `int` | `1` | Number of pods to add/remove per evaluation period. |
| `select_policy` | `Literal['Min', 'Max']` | `'Min'` | Policy for selecting which scaling recommendation to use when multiple are available. |

(api-doc-probeconfig)=
[**`ProbeConfig`**](api-doc-probeconfig)

Override timing for a k8s probe. Path and port are fixed by the framework.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `timeout` | int \\| None | `None` | Probe timeout in seconds. |
| `period_seconds` | int \\| None | `None` | How often to perform the probe. |
| `failure_threshold` | int \\| None | `None` | Number of consecutive failures before action. |

(api-doc-toleration)=
[**`Toleration`**](api-doc-toleration)

K8s toleration for scheduling on tainted nodes.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `key` | `str` | *required* | Taint key to tolerate. |
| `value` | `str` | *required* | Taint value to match. |
| `effect` | `Literal['NoSchedule']` | `'NoSchedule'` | Taint effect. |
| `operator` | `Literal['Equal']` | `'Equal'` | Match operator. |

(api-doc-ingress)=
[**`Ingress`**](api-doc-ingress)

Configuration for adding ingress(es) to send traffic to a deployment.

Global settings defined at this level are inherited by all specific ingress types
(public_ingress, dev_ingress, etc.) but can be overridden per-ingress.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `global_config` | `IngressBaseConfig` | `IngressBaseConfig()` | Global configuration for all ingresses. |
| `public_ingress` | bool \\| IngressBaseConfig \\| None | `None` | Public internet-facing ingress on .ff.adobe.io. DNS must be set up manually by SRE. For auto DNS, use custom_ingress with dns: true. |
| `development_ingress` | bool \\| IngressBaseConfig \\| None | `None` | Development ingress for debugging. Restricted to corp + Laser + Ethos cluster IPs. Defaults: all paths with disabled_auth, all HTTP methods, dev client IDs. |
| `public_async_ingress` | bool \\| IngressBaseConfig \\| None | `None` | Public async ingress for background job polling. Uses Ethos cluster wildcard DNS. Defaults: /jobs/ path (matches the framework Jobs webapp); GET/POST/OPTIONS/PUT/DELETE; auth enabled. Auto-injects async_endpoint_url into runtime config when configured. |
| `custom_ingress` | `dict[str, CustomIngressConfig]` | `{}` | Custom ingress with user-defined domains, keyed by a logical name. Set dns: true to auto-create DNS records for .adobe.io or .private.adobe.io domains. |
| `port` | `int` | `8000` | The port to expose from the deployment. |

For details on `IngressBaseConfig`, `CustomIngressConfig`, and related types, see the [Ingress](#ingress) section below.


(api-doc-envvar)=
[**`EnvVar`**](api-doc-envvar)

A single environment variable entry (used in lists within `EnvVars`).

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | *required* | Environment variable name. |
| `value` | `str` | *required* | Environment variable value. |

## Using the Metadata

When using `managed_services`, set `json_spec` in `values.inference.yaml` to point to the metadata JSON file generated at build time:

```yaml
# values.inference.yaml
json_spec: https://artifactory.example.com/.../metadata.json
```

The use of metadata is completely optional, but it comes with some advantages. The chart uses it for two things:

**1. Catch invalid inputs at render time**

If you reference a worker that does not exist, the chart fails immediately when you render it — not later when the pod starts up and crashes.

```yaml
deployments:
  my_worker:
    processes:
      svc.workers.nsfw.I_DONT_EXIST: 1   # fails at chart render ✗
```

**2. Auto-generate deployment defaults**

Worker names and hardware requirements are already declared in your `BUILD` files and Python `ServeConfig`. The chart reads the metadata and creates default deployment entries for you, so you do not have to repeat that information:

| Auto-generated entry | Type | What it does |
|---|---|---|
| `image` | — | Populated from the metadata file if not set in `values.inference.yaml` |
| One entry per worker ref | `WorkerDeployment` | `replicas: 1`, `processes: {<worker_ref>: 1}`, hardware from `ServeConfig` |
| `http_server` | `HttpServerDeployment` | `replicas: 1`, `serves` set to all webapp refs, `development_ingress: true` |
| `job_watchdog` | `WatchdogDeployment` | `replicas: 1`, monitors all worker queues |

So if your metadata contains workers `svc.workers.nsfw.nsfw_v2` and `svc.workers.clip.clip_v1`, you get this for free without writing anything in `values.inference.yaml`:

```yaml
# auto-generated — you don't write this
image: docker.example.com/myapp:abc123   # pulled from metadata
deployments:
  svc.workers.nsfw.nsfw_v2:
    type: worker
    replicas: 1
    processes:
      svc.workers.nsfw.nsfw_v2: 1
  svc.workers.clip.clip_v1:
    type: worker
    replicas: 1
    processes:
      svc.workers.clip.clip_v1: 1
  http_server:
    type: http_server
    replicas: 1
    serves:
      - svc.webapps.app.my_app
    ingress:
      development_ingress: true
  job_watchdog:
    type: watchdog
    replicas: 1
```

**How to get a metadata file** - see the [Package an application](./gitops-framework.md#package-an-application) section

**Example metadata file**

```json
{
  "workers": [
    "svc.workers.nsfw.nsfw_v2",
    "svc.workers.clip.clip_v1"
  ],
  "webapps": [
    "svc.webapps.app.my_app"
  ],
  "image": "docker.example.com/myapp:abc123",
  "preferred_hardware": {
    "svc.workers.nsfw.nsfw_v2": {
      "xpu": "gpu",
      "num": 1,
      "memory": 40,
      "preferred_family": "ampere"
    },
    "svc.workers.clip.clip_v1": {
      "xpu": "cpu",
      "size": "medium"
    }
  }
}
```

The `preferred_hardware` values come from the `ServeConfig` you set in Python and are used as defaults when auto-generating worker deployments. You can always override them in `values.inference.yaml`.

**Overriding a default** — any key you write in `values.inference.yaml` merges with the auto-generated entry of the same name. For example, to scale up a worker:

```yaml
deployments:
  svc.workers.nsfw.nsfw_v2:
    replicas: 5   # override; everything else stays as auto-generated
```

**Disabling a default** — set `replicas: 0`. This also applies when you want to rename an auto-generated entry: disable the original and create a new one under your preferred name:

```yaml
deployments:
  job_watchdog:
    replicas: 0              # disable the auto-generated watchdog
  my_watchdog:               # create a new one under a different name
    type: watchdog
    replicas: 1
```

**Development ingress** — the auto-generated `http_server` also gets a development ingress enabled by default (`development_ingress: true`). You can override it by merging into the `http_server` key or replace it entirely by disabling and recreating as above.

**Running multiple workers on the same pod while using the metadata**

By default each worker gets its own pod. When GPU time-slicing is unavailable and hardware is tight, you can run multiple worker processes on the same pod by setting `processes` to a map of full refs to process counts. Independent per-worker scaling does not work in this mode — use it only as a last resort.

`processes` remains a map of worker ref to process count. At render time, each worker ref is passed
once to `python -m frameworks.inference workers`, and the count is injected into that pod's runtime
config as `<worker_ref>.serve_config.num_processes`. The override is pod-local, so two deployments can
run the same worker ref with different process counts.

To do this, set the metadata auto-generated single-worker deployments to `replicas: 0` and create a new deployment that lists all workers in `processes`:

```yaml
deployments:
  svc.workers.nsfw.nsfw_v2:
    replicas: 0                    # disable auto-generated single-worker pod
  svc.workers.nsfw.nsfw_v4:
    replicas: 0                    # disable auto-generated single-worker pod
  merged_nsfw:
    type: worker
    replicas: 1
    processes:
      svc.workers.nsfw.nsfw_v2: 1  # worker ref → number of processes to start
      svc.workers.nsfw.nsfw_v4: 2  # starts 2 nsfw_v4 processes on the same pod
```

## Runtime configuration

Every pod reads a **runtime config** at startup — a dictionary that is rendered into the pod spec
and exposed to the inference framework. You can set it at two levels:

- **Application-wide** (global) — `runtime_config:` at the top of `values.inference.yaml`.
  Applied to every deployment in the application.
- **Per deployment / per worker** — `deployments.<name>.runtime_config:`.
  Applied only to that deployment and **deep-merged on top of** the application-level config:
  dict/list keys are merged recursively; scalar values at the deployment level override the
  application-level value for the same key.

```yaml
# values.inference.yaml
runtime_config:
  frameworks.inference.default_config:
    logging:
      level: INFO
  my_app.feature_flags:
    enable_foo: true

deployments:
  svc.workers.nsfw.nsfw_v2:
    runtime_config:
      frameworks.inference.default_config:
        logging:
          level: DEBUG          # overrides INFO for this deployment only
      my_app.worker_settings:
        batch_size: 8           # only injected into this worker's pod
```

### Referencing secrets with `{_env: ...}`

Secrets injected via `env_vars.secrets` can be referenced in `runtime_config` using
`{_env: ENV_VAR_NAME}`. At pod startup, the framework resolves these to the actual
env var value before Pydantic validation. See
[Environment variable substitution in config](/frameworks/inference/serve/aidoc/api.md#environment-variable-substitution-in-config)
for full details.

```yaml
runtime_config:
  my_app.default_config:
    api_key: {_env: MY_API_KEY}       # resolved from env var at startup
    azure_endpoint: {_env: AZURE_EP}
```

### Platform-provided defaults

Defaults are merged from three layers before your `values.inference.yaml` is applied. You can override any key by setting it yourself.

**Merge order** (last wins): runtime-env values → chart-provided defaults → your `values.inference.yaml`.

#### `frameworks.inference.default_config`

| Key | Source | Notes |
|---|---|---|
| `redis.host` | cluster-specific | MemoryDB endpoint for the cluster |
| `redis.port`, `redis.username`, `redis.password` | env-specific | Credentials via Vault |
| `redis.namespace` | chart-injected | Set to `application_name` (scopes queues per app) |
| `s3.*` | env-specific | Default profile credentials + bucket with `use_accelerate_endpoint: true` |
| `logging.formatter` | env-specific | `json` |
| `metrics.app_name` | chart-injected | Set to `application_name` |
| `experimental_config.enable_queue_length_metrics_reporter` | chart-injected | Always `true` (required for queue-based autoscaling) |
| `background.watchdog_queues` | chart-injected | Only on `WatchdogDeployment`s — list of monitored worker names |
| `async_endpoint_url` | chart-injected | Only when `public_async_ingress` is configured |
| `experimental_config.enable_worker_warming` | chart-injected | `true` on KEDA `scaleToZero` deployments + their `http_server` |

#### `frameworks.inference.migration.default_config`

| Key | Source | Notes |
|---|---|---|
| `ims.*` | env-specific | IMS endpoint (`env`, `enabled`, `host`) — stage vs prod |
| `temp_storage.bucket` | env-specific | Pre-signed URL bucket for the environment |

#### Other runtime-env defaults (non-`runtime_config`)

| Key | Source |
|---|---|
| `image_pull_secrets` | env-specific — shared Artifactory credentials |
| `iam_role` | env-specific — AWS IAM role for Vault/S3 access |
| `env_vars.secrets` (Redis, S3 credentials) | env-specific — Vault secret references |
| `env_vars.non_secrets.XDG_CACHE_HOME` | global — redirects model downloads to local SSD |

### Config hash and pod recreation

The fully-merged runtime config (application defaults + chart-provided defaults + deployment
overrides) is serialized to canonical JSON and hashed with SHA-256. The hash is written onto
the pod template as a `rhode.confighash` annotation.

Because the annotation is part of the pod template, **any change to the runtime config — at
either the global or per-deployment level — changes the hash, which changes the pod template,
which causes Kubernetes to roll the deployment and recreate the pods.** Pods that did not see a
config change keep the same hash and are not restarted. This is how a change to
`values.inference.yaml` propagates to the running fleet.

## Hardware Specification

### GPU workloads


**`WorkerGpuPreference`**

Worker GPU preference from ServeConfig.

This matches the GpuRequirement type from frameworks.inference ServeConfig.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `xpu` | `Literal['gpu']` | `'gpu'` |  |
| `num` | `int` | `1` |  |
| `memory` | float \| None | `None` | GPU memory requirement in GB. If None, allows any GPU. |
| `preferred_family` | `Literal['ampere', 'hopper', 'blackwell', None]` | `None` | Preferred GPU family. If not specified, will pick based on memory requirement. |

**`GpuHardware`**

GPU hardware specification for direct user specification in inference values.

This allows users to directly specify concrete GPU types and counts.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `xpu` | `Literal['ampere_40gb', 'ampere_80gb', 'hopper_80gb', 'hopper_140gb']` | *required* | GPU type. Options: ampere_40gb, ampere_80gb, hopper_80gb, hopper_140gb |
| `num_gpus` | `Literal[1, 2, 4, 8]` | `1` | Number of GPUs. Options: 1, 2, 4, 8 |


The preferred hardware spec for the workers can be set in the worker' ServeConfig, which is later added as default in the deployment values by the inference JSON metadata.

```python
from frameworks.inference import serve

serve_config = serve.ServeConfig(
    xpu_requirement=serve.GpuRequirement(
        memory=40,  # minimum VRAM in GB required for the model
        preferred_family="ampere",
        num=1, # number of GPUs
    )
)
```

Available families:
- `ampere`: A100 (40GB), A100 (80GB)
- `hopper`: H100 (80GB), H200 (140GB)
- `blackwell`: coming soon

Override in `values.inference.yaml` to pin exact hardware:

```python
deployments:
  my_worker:
    hardware:
      xpu: ampere_80gb  # only A100 (80GB)
      num_gpus: 2
```

### CPU workloads

The preferred hardware spec for the workers can be set in the worker' ServeConfig, which is later added as default in the deployment values by the inference JSON metadata.


**`WorkerCpuPreference`**

Worker CPU preference from ServeConfig.

This matches the CpuRequirement type from frameworks.inference ServeConfig.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `xpu` | `Literal['cpu']` | `'cpu'` |  |
| `size` | `Literal['small', 'medium', 'large', 'xlarge']` | `'small'` |  |

**`CpuHardware`**

CPU hardware specification.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `xpu` | `Literal['cpu']` | `'cpu'` |  |
| `size` | `Literal['small', 'medium', 'large', 'xlarge']` | `'small'` | CPU tier size. Options: small, medium, large, xlarge |


Override in `values.inference.yaml` to pin exact hardware:

```python
deployments:
  my_worker:
    hardware:
      xpu: cpu
      size: large
```

CPU sizes set the request; the chart applies a 4× multiplier for the limit, so a pod
can burst up to 4× its baseline as long as the node has spare capacity:

| `size`    | CPU request | Memory request | CPU limit (4×) | Memory limit (4×) |
|-----------|-------------|----------------|----------------|-------------------|
| `small`   | 1           | 2 GB           | 4              | 8 GB              |
| `medium`  | 1           | 3 GB           | 4              | 12 GB             |
| `large`   | 2           | 4 GB           | 8              | 16 GB             |
| `xlarge`  | 4           | 8 GB           | 16             | 32 GB             |

All sizes target the same `c5.12xlarge` workload pool — the pin guarantees a known
instance shape and per-pod ephemeral storage budget.

## Local NVMe SSD (`localssd`)

Set `localssd: true` on a deployment to mount node-local NVMe at `/mnt/localssd`
via an ephemeral PVC (storageClassName `local-ssd`). Useful for staging large
model weights or scratch I/O without paying EBS latency.

```yaml
deployments:
  my_worker:
    hardware:
      xpu: cpu
      size: large
    localssd: true
```

Defaults: **GPU** deployments get `localssd: true` (GPU pools have NVMe and the
storage class is bound there). **CPU** deployments default to `false` and only
provision the volume when explicitly requested.

When `localssd: true` is set on a CPU deployment, scheduling switches from the
plain `c5.12xlarge` pool to the **`c5dssd` workload pool** (a c5d-family pool
where the `local-ssd` storage class actually provisions PVs). The renderer
swaps both `nodeAffinity` and the matching toleration; if the swap did not
happen, the PVC would never bind and the pod would stay `Pending`.

## Logging configuration

Applications automatically configure appropriate Splunk routing based on deployment environment:

| Environment | Splunk Index | Source Type                 |
|-------------|--------------|-----------------------------|
| **dev**     | `nfp_nonprod`| `v3-{app_name}-{env}`       |
| **stage**   | `nfp_nonprod`| `v3-{app_name}-{env}`       |
| **prod**    | `nfp_prod`   | `v3-{app_name}-{env}`       |

The logging formatter defaults to `"default"` and must be explicitly configured by the user if a different format is desired.


## Autoscaling

Autoscaling is configured per deployment under `deployments.<name>.autoscaling`.

Pick the config that matches the worker hardware:

- **CPU workers / HTTP servers**: `cpuScaling` (HPA rendered in the chart output)
- **GPU workers**: `gpuScaling` (WorkerConfig rendered; Oshiya handles scaling)

Most nested fields accept a shorthand:

- `true`: enable with defaults
- `false`: disable
- an object: enable with custom settings

**Defaults today:**

- **CPU**: no autoscaling unless you set it
- **stage/prod/prerelease**: no autoscaling unless you set it
- **dev + GPU workers**: scale to zero and worker warmup are enabled by default for workers when the specific GPU is supported by KEDA

### Config reference


**`AutoScalingConfig`**

Autoscaling configuration.

Choose cpu_scaling OR gpu_scaling based on worker hardware type.
Exactly one of cpu_scaling or gpu_scaling must be set.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `cpu_scaling` | CPUScalingConfig \| None | `None` | CPU worker autoscaling configuration. |
| `gpu_scaling` | GPUScalingConfig \| None | `None` | GPU worker autoscaling configuration. |

**`CPUScalingConfig`**

CPU worker autoscaling configuration.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `min_replicas` | int \| None | `None` | Minimum number of replicas. Defaults to deployment.replicas if not set. |
| `max_replicas` | int \| None | `None` | Maximum number of replicas. When None and queue_based_scaling is enabled, calculated using formula: min_replicas^0.75 + min_replicas + 5. |
| `queue_based_scaling` | bool \| QueueBasedScalingConfig \| None | `False` | Queue-based HPA scaling using Prometheus metrics. Set to true to use defaults, or provide config. |

**`GPUScalingConfig`**

GPU worker autoscaling configuration.

Supports Oshiya prediction-based scaling (enabled by default),
optionally extended with queue-based HPA and event-driven KEDA.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `min_replicas` | int \| None | `None` | Minimum number of replicas. Defaults to deployment.replicas if not set. |
| `max_replicas` | int \| None | `None` | Maximum number of replicas. When None: if scale_to_zero (KEDA) enabled, defaults to deployment.replicas; else if queue_based_scaling enabled, uses formula min_replicas^0.75 + min_replicas + 5; else omitted (Oshiya calculates it). |
| `prediction_based_scaling` | bool \| PredictionBasedScalingConfig | `True` | Oshiya prediction-based scaling. Set to true for defaults (default), false to disable, or provide custom config. |
| `queue_based_scaling` | bool \| QueueBasedScalingConfig \| None | `None` | Queue-based HPA scaling. Set to true for defaults, or provide custom config. Requires prediction_based_scaling enabled. |
| `scale_to_zero` | bool \| ScaleToZeroConfig \| None | `None` | KEDA event-driven scaling with scale-to-zero. Set to true for defaults, or provide custom config. Requires prediction_based_scaling enabled. |

**`QueueBasedScalingConfig`**

Configuration for queue-based HPA autoscaling using Prometheus metrics.

Creates HorizontalPodAutoscaler for scaling based on queue length, CPU, and memory.
Supported by both CPU and GPU workers.
On GPU workers, the HPA is created dynamically at runtime by Oshiya, it will not be seen in the deployment spec.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | `bool` | `True` | Enable/disable queue-based scaling. Default is true when configured. |
| `queue_name` | str \| None | `None` | Queue name to monitor for scaling. Defaults to worker name. Should not include ':internal' suffix. |
| `metric_name` | `str` | `'usm_object_colligo_queue_requests_in_progress'` | Prometheus metric name to use for scaling decisions. For the dev environment, the default metric becomes usm_object_colligo_queue_requests_in_progress_dev. |
| `average_value` | `int` | `5` | Target average value of the metric per replica. Scaling occurs when actual value exceeds this. |
| `average_value_format` | Literal['default', 'MI'] \| None | `None` | Format for average_value. Use 'MI' to support fractional target values (e.g., average_value=1500 with MI means 1.5). |
| `average_cpu_utilization` | `int` | `90` | Target average CPU utilization percentage across all pods. |
| `average_memory_utilization` | `int` | `80` | Target average memory utilization percentage across all pods. |
| `scale_down` | ScalePolicy \| None | `None` | Policy for scaling down. If not set, uses default values. |
| `scale_up` | ScalePolicy \| None | `None` | Policy for scaling up. If not set, uses default values. |

**`PredictionBasedScalingConfig`**

Configuration for Oshiya GPU prediction-based autoscaling.

Uses historical traffic data to predict optimal replica counts.
Only supported for GPU workers.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | `bool` | `True` | Enable/disable prediction-based scaling. Default is true when configured. |
| `buffer_replicas` | `int` | `0` | Extra replicas to add on top of min_replicas when capacity is available. Allows faster scale-up. |
| `boost_factor` | `float` | `1.0` | Factor to make this worker more preferable for scaling up. Higher values = more priority. |

**`ScaleToZeroConfig`**

Configuration for KEDA event-driven autoscaling with scale-to-zero support.

KEDA requirements:
- Only supported for GPU workers
- Requires prediction_based_scaling to be enabled
- Requires `check_worker_before_call: false` and `enable_worker_warming: true` in the runtimeconfig to work correctly

| Field | Type | Default | Description |
|-------|------|-------|-------------|
| `enabled` | `bool` | `True` | Enable/disable KEDA scaling. Default is true when configured. |
| `idle_replica_count` | `int` | `0` | Replicas when idle (0 = scale-to-zero). |
| `polling_interval` | `int` | `10` | How often KEDA checks metrics (seconds). |
| `cooldown_period` | `int` | `600` | Wait time before scaling to zero after last trigger (seconds). Maximum 4 hours (14400 seconds). (≤ 14400) |
| `server_address` | `str` | `'http://app-promoperator-prometheus.ns-team-firefly-enm.svc.cluster.local:9090'` | Prometheus server address for KEDA queries. |
| `metric_name` | `str` | `'usm_object_colligo_queue_requests_in_progress'` | Prometheus metric name to monitor. |
| `threshold` | `str` | `'5'` | Threshold value as string (e.g., '1', '5', '3.5'). KEDA target value used to size replicas (desiredReplicas = ceil(metricValue / threshold)). Does not affect scale-from-zero behavior. |
| `activation_threshold` | `str` | `'0'` | It defines the minimum metric value required to activate the scaler and scale up from 0 to minReplicaCount. The trigger is activated only when metric (or warm up) > activationThreshold. |
| `scale_down` | ScalePolicy \| None | `None` | Policy for scaling down. |
| `scale_up` | ScalePolicy \| None | `None` | Policy for scaling up. |

**`ScalePolicy`**

Policy for controlling how fast scaling happens.

Used to configure both scale_up and scale_down behavior in HPA.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `period_seconds` | `int` | `300` | How often (in seconds) the scaling policy is evaluated. |
| `stabilization_window_seconds` | `int` | `900` | Time window (in seconds) to look back at metrics before making a scaling decision. |
| `pods` | `int` | `1` | Number of pods to add/remove per evaluation period. |
| `select_policy` | `Literal['Min', 'Max']` | `'Min'` | Policy for selecting which scaling recommendation to use when multiple are available. |


### CPU autoscaling

This creates an HPA that scales on a Prometheus queue metric, and optionally CPU/memory.

**Queue-based**

```yaml
deployments:
  my_cpu_worker:
    type: worker
    hardware:
      xpu: cpu
    autoscaling:
      cpuScaling:
        minReplicas: 2
        maxReplicas: 20
        queueBasedScaling: true
```

**Queue-based + custom tuning**

```yaml
deployments:
  my_cpu_worker:
    type: worker
    hardware:
      xpu: cpu
    autoscaling:
      cpuScaling:
        minReplicas: 2
        maxReplicas: 20
        queueBasedScaling:
          queueName: "my_cpu_worker"
          averageValue: 5
          scaleDown:
            periodSeconds: 900
            pods: 1
          scaleUp:
            periodSeconds: 240
            pods: 3
```

### GPU autoscaling

`predictionBasedScaling` is enabled by default for `gpuScaling`. You can still override it.


**Prediction-based**

```yaml
deployments:
  my_gpu_worker:
    type: worker
    hardware:
      xpu: hopper_80gb
    autoscaling:
      gpuScaling:
        minReplicas: 2
        maxReplicas: 15
        predictionBasedScaling: true # can be omitted, true by default
```

**Prediction-based + custom tuning**

```yaml
deployments:
  my_gpu_worker:
    type: worker
    hardware:
      xpu: hopper_80gb
    autoscaling:
      gpuScaling:
        minReplicas: 2
        maxReplicas: 15
        predictionBasedScaling:
          bufferReplicas: 2
          boostFactor: 1.5
```

**Prediction-based + queue-based**

```yaml
deployments:
  my_gpu_worker:
    type: worker
    hardware:
      xpu: hopper_80gb
    autoscaling:
      gpuScaling:
        minReplicas: 3
        maxReplicas: 25
        predictionBasedScaling: true # can be omitted, true by default
        queueBasedScaling: true
```

**Prediction-based + queue-based + fine-tuning**

```yaml
deployments:
  my_gpu_worker:
    type: worker
    hardware:
      xpu: hopper_80gb
    autoscaling:
      gpuScaling:
        minReplicas: 3
        maxReplicas: 25
        predictionBasedScaling:
          bufferReplicas: 2
          boostFactor: 1.5
        queueBasedScaling:
          queueName: "my_gpu_worker"
          averageValue: 5
          scaleDown:
            periodSeconds: 900
            pods: 1
          scaleUp:
            periodSeconds: 240
            pods: 3
```

**Prediction-based + queue-based + scale-to-zero**

```yaml
deployments:
  my_gpu_worker:
    type: worker
    hardware:
      xpu: hopper_80gb
    autoscaling:
      gpuScaling:
        minReplicas: 0
        maxReplicas: 10
        predictionBasedScaling: true # can be omitted, true by default
        queueBasedScaling: true
        scaleToZero: true
```

**Prediction-based + queue-based + scale-to-zero + fine-tuning**

```yaml
deployments:
  my_gpu_worker:
    type: worker
    hardware:
      xpu: hopper_80gb
    autoscaling:
      gpuScaling:
        minReplicas: 0
        maxReplicas: 10
        predictionBasedScaling: true # can be omitted, true by default
        queueBasedScaling: true
        scaleToZero:
          idleReplicaCount: 0
          pollingInterval: 30
          cooldownPeriod: 600
          metricName: "usm_object_colligo_queue_requests_in_progress"
          threshold: "5"
          activationThreshold: "0"
```

### Validation Rules

- ❌ set both `cpuScaling` and `gpuScaling`
- ❌ use `cpuScaling` on GPU workers
- ❌ use `gpuScaling` on CPU workers
- ❌ set `queueBasedScaling` or `scaleToZero` on GPU while `predictionBasedScaling` is disabled
- ℹ️ `scaleToZero` (KEDA) automatically sets `enable_worker_warming: true` in the runtime config of the worker itself, and also of the chart's `http_server` deployment.
Note: `check_worker_before_call` is always `false` in inference v3
- ✅ CPU: `cpuScaling.queueBasedScaling`
- ✅ GPU: `gpuScaling` (prediction only, or prediction + queue-based, or prediction + KEDA, or all of them)


## Ingress

Ingress is configured per deployment under `deployments.<name>.ingress`. The inference chart provides several built-in ingress types that auto-configure FQDN, DNS, and access policies. For the full configuration reference (`IngressBaseConfig`, `CustomIngressConfig`, throttling, DNS, access restrictions), see the [Ingress Chart](./ingress-chart.md) docs — the API and behavior are identical.

### Overview

The `url_prefix` defaults to `v3-{application_name}` and is used in the FQDN for all ingress types except `custom_ingress` (which uses the explicit `host` field).

| Ingress type | FQDN pattern (prod) | FQDN pattern (non-prod) | DNS |
|---|---|---|---|
| `development_ingress` | `<url_prefix>-<env>.{cluster}.ethos.adobe.net` | same | Ethos wildcard (automatic) |
| `public_ingress` | `<url_prefix>.ff.adobe.io` | `<url_prefix>-<env>.ff.adobe.io` | Manual (SRE team) |
| `public_async_ingress` | `<url_prefix>-<env>-async.{cluster}.ethos.adobe.net` | same | Ethos wildcard (automatic) |
| `custom_ingress` | user-defined `host` field | user-defined `host` field | `create_dns: true` creates a DNSRecord CRD, or manual |

All ingress types except `custom_ingress` accept `true` (use defaults) or an `IngressBaseConfig` (customize). `custom_ingress` is a dict of `CustomIngressConfig` entries keyed by a logical name.

### Development ingress

Creates an endpoint restricted to Adobe corp network, Laser clusters, and Ethos cluster egress IPs for debugging. DNS is provided by the Ethos cluster wildcard — no setup needed.

Defaults: all paths (`/`) with `disabled_auth=true`, client IDs `colligo-developer`/`colligov2_platform`/`colligo_testing`, all HTTP methods.

### Public async ingress

For multi-cluster services where background job status/result URLs must route back to the originating cluster. DNS is provided by the Ethos cluster wildcard — no setup needed.

Defaults when `public_async_ingress: true`:
- **Paths**: `/jobs/`
- **Methods**: GET, POST, OPTIONS, PUT, DELETE
- **Auth**: Enabled
- **Ingress class**: always `contour-public`
- **Exposed headers**: `x-task-status`, `x-request-id`, `x-session-id`, `retry-after`

**`async_endpoint_url` auto-injection**: When `public_async_ingress` is configured, the chart auto-injects `frameworks.inference.default_config.async_endpoint_url` into the runtime config, pointing to the public async FQDN.

```yaml
deployments:
  http_server:
    type: http_server
    serves:
      - svc.webapps.app.my_app
      - frameworks.inference.builtin_webapps.jobs_app
    ingress:
      public_async_ingress: true
      development_ingress: true
```

### Public ingress

For production API traffic:

1. **`public_ingress`** — uses `<url_prefix>.ff.adobe.io` (prod) or `<url_prefix>-<env>.ff.adobe.io` (non-prod). DNS must be set up by the SRE team.
2. **`custom_ingress`** with a `.adobe.io` domain and `create_dns: true` — provides automatic DNS resolution via the Ethos `DNSRecord` CRD.

### Custom ingress

For user-defined domains. Each entry specifies a `host` and optionally `create_dns: true`. TLS secret and ingress class are auto-inferred from the domain suffix. See [Ingress Chart](./ingress-chart.md) for DNS and constraints.

```yaml
    ingress:
      custom_ingress:
        public:
          host: "gabby-gen6-ff.adobe.io"
          create_dns: true
          allowed_url_paths:
            - prefix: "/v1/"
        internal:
          host: "my-service.private.adobe.io"
          create_dns: true
          allowed_url_paths:
            - prefix: "/api/"
```

