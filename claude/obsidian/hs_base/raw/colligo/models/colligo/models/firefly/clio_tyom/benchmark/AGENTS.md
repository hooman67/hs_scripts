# Benchmark CLI - Architecture Guidelines

## Purpose

Benchmarks Colligo pipeline endpoints by running test scenarios, collecting timing metrics, and generating HTML comparison reports. This is a generic benchmarking tool - all configuration parameters are required (no use-case-specific defaults).

## Commands

| Command | Purpose |
|---------|---------|
| `run` | Full local benchmark: starts app in tmux, runs scenarios for multiple endpoints, generates per-result + comparison reports |
| `run-distributed` | Distributed benchmark: spawns Pluto GPU jobs, polls for completion, generates per-result + comparison reports on sensei-fs |
| `execute` | Single endpoint: runs scenarios, collects artifacts, and generates a per-result report |
| `compare` | Create a comparison from existing result directories |
| `report` | Generates report from existing run directories |
| `dashboard` | FastAPI web UI for viewing, labeling, comparing, and deleting benchmark results |

## Module Structure

```
models/colligo/models/firefly/clio_tyom/benchmark/
├── __main__.py              # CLI entry point (no use-case-specific defaults)
├── orchestrator.py          # BenchmarkOrchestrator: local benchmark execution
├── distributed_orchestrator.py # DistributedBenchmarkOrchestrator: Pluto job execution
├── executor.py              # ScenarioExecutor: manages app lifecycle + scenario execution
├── pluto_job_manager.py     # PlutoJobManager: wraps aip CLI for Pluto job lifecycle
├── api_client.py            # APIClient: async HTTP client with IMS auth support
├── scenario_loader.py       # ScenarioLoader: parses YAML scenario files
├── report_generator.py      # HTMLReportGenerator: creates comparison reports
├── log_parser.py            # Parses timing data from application logs
├── logging_utils.py         # Dual-output logging (console + file) for orchestrators
├── ims_auth.py              # IMS token acquisition
├── models.py                # Dataclasses: configs, results (no use-case defaults)
├── scenarios/               # Benchmark scenario YAML files
│   ├── cm_analyze/          # CM Analyze specific scenarios
│   │   ├── benchmark_scenarios.yaml           # Full benchmark scenarios
│   │   ├── benchmark_test_scenario.yaml       # Quick validation scenarios
│   │   └── benchmark_scenarios_caption_compare.yaml
│   ├── README.md            # Generic scenario format docs
│   └── example_scenario.yaml # Template for new scenarios
├── pluto_scripts/           # Shell scripts for Pluto job execution
│   ├── init_script.sh       # Environment setup (git clone, deps)
│   └── main_script.sh       # Benchmark execution in Pluto job
├── templates/
│   └── artifactory_env.template
├── compare_report_generator/ # Pluggable compare report generators
│   ├── types.py             # CompareReportGenerator protocol
│   └── cm_analyze.py        # CM Analyze implementation
├── dashboard/               # FastAPI web UI for results + comparisons
│   ├── __main__.py          # Dashboard entry point
│   └── server.py            # BenchmarkDashboard: list/label/compare/delete REST API + SPA
└── deprecated/              # Legacy scripts (superseded by modular CLI)
```

## Key Classes

- **BenchmarkOrchestrator**: Runs `ScenarioExecutor` for each endpoint locally, then generates report
- **DistributedBenchmarkOrchestrator**: Submits Pluto jobs, polls for completion, generates report directly on sensei-fs
- **PlutoJobManager**: Wraps aip CLI for job create/start/status/stop operations
- **ScenarioExecutor**: Starts app in tmux, waits for ready, executes scenarios via `APIClient`, collects artifacts
- **AppProcessManager**: Manages tmux session lifecycle, monitors log for ready message
- **APIClient**: Submits async requests, polls `/jobs/result/{job_id}` for completion
- **HTMLReportGenerator**: Loads `run_status.json` from each run, parses logs for component times, builds HTML

## Data Flow

1. YAML scenarios → `ScenarioLoader` → request payloads
2. `AppProcessManager` starts app in tmux, waits for ready pattern in log
3. `APIClient` submits requests, polls for completion
4. `ArtifactCollector` saves logs, bg_monitor data, `run_status.json`
5. `HTMLReportGenerator` aggregates results, produces `benchmark_report.html`

## Configuration

All configuration parameters are **required** - the CLI has no use-case-specific defaults.

Defined in `models.py`:
- **ExecutorConfig**: shell_command, scenarios_file, endpoint (all required), plus timeouts, paths, max_retries
- **BenchmarkConfig**: scenarios_file, endpoints, colligo_app (all required), plus output_dir, max_retries
- **IMSConfig**: optional IMS authentication credentials
- **DistributedBenchmarkConfig**: pluto_config, git_branch, sensei_output_path, scenarios_file, endpoints (all required), plus spec or command (at least one)

### Required Parameters for `run-distributed`

| Parameter | Description |
|-----------|-------------|
| `--branch` | Git branch to clone in Pluto jobs |
| `--colligo-app` | Colligo app name for dev_supervisor (e.g., `firefly_tyom_v2_training`). Required unless `--command` is provided. |
| `--command` | Custom shell command to start the app (overrides `--colligo-app`). Use for extra flags like `--replicas`. |
| `--scenarios` | Path to scenarios YAML file |
| `--endpoints` | Endpoints to benchmark (format: `name:path` or `name:path:branch`) |
| `--sensei-output` | sensei-fs path for results upload |
| `--colligo-dev-yaml` | Path to colligo.dev.yaml file on sensei-fs |

At least one of `--colligo-app` or `--command` must be provided. When `--command` is given, it is passed directly to the Pluto job and used as the `--command` argument for the `benchmark execute` call, bypassing the default `dev_supervisor --spec` template.

### Retry Configuration
Failed scenarios are automatically retried up to `max_retries` attempts (default: 3). The retry count is tracked in `ScenarioStatus.attempts` and included in `run_status.json` output.

## Important Patterns

- App runs in tmux session (attach with `tmux attach -t <session>` for debugging)
- Ready detection: scans log file for pattern `"[dev_supervisor] Local service is Ready!"`
- Async jobs: POST returns `job_id`, poll GET until `X-Task-Status` != `IN_PROGRESS`
- Component times extracted from logs using `session_id` for per-request filtering
- **Debug headers**: Scenarios can declare a `debug_headers` dict (next to `debug`) inside `base_recipe`, `warmup`, or any variation's `recipe`. `ScenarioLoader` deep-merges them across layers and `APIClient.submit_request` serialises the result as JSON into the `x-colligo-debug-input` request header on the POST (never added to the poll GET). Any key the server recognises on that header is allowed; keep `debug_headers` absent when no debug header is needed.
- **Graceful shutdown**: SIGINT/SIGTERM are caught by `DistributedBenchmarkOrchestrator`. On first signal, stop commands are emitted for all active Pluto jobs (fire-and-forget, no polling for confirmation), then `KeyboardInterrupt` is raised. A second signal forces immediate exit via `SystemExit(128 + signum)`.

## Output Structure

Both `run` and `run-distributed` write directly into a flat `results/` + `comparisons/` layout under the benchmark root (local: `--output-dir`, distributed: `--sensei-output`). There is **no** top-level `{run_id}/` folder — each run produces one per-endpoint result entity plus, for multi-endpoint runs only, a comparison entity. This matches what `dashboard/server.py` and `compare` expect.

```
{BENCHMARK_ROOT}/
├── results/
│   ├── 20260127_143052_v3/           # {run_id}_{endpoint.name}
│   │   ├── run_status.json
│   │   ├── executor.log
│   │   ├── logs/                     # Application logs
│   │   ├── bg_monitor/               # Memory profiler data
│   │   ├── label.json                # Endpoint name
│   │   ├── orchestrator.log          # Always lives here, duplicated across results
│   │   └── report/                   # Single-column per-result HTML report
│   │       ├── benchmark_report.html
│   │       ├── benchmark_results.json
│   │       └── images/
│   └── 20260127_143052_v1/
│       └── ...                       # Same structure, with its own orchestrator.log copy
└── comparisons/                      # Multi-endpoint runs only
    └── 20260127_143052/              # Run ID (auto-generated timestamp or custom)
        ├── comparison.json
        ├── label.json                # Optional, set via --comparison-label
        └── report/                   # Multi-column comparison HTML report
            ├── benchmark_report.html
            ├── benchmark_results.json
            └── images/
```

A `comparisons/{run_id}/` entity is only produced when the run has **more than one endpoint**. For single-endpoint runs the per-result HTML report (`results/{run_id}_{endpoint}/report/benchmark_report.html`) is what the dashboard previews.

`orchestrator.log` is **always** stored in each result directory — never in the comparison entity. During the run it's written live to the first endpoint's result dir, and when the run finishes it's copied into every other result dir as well.

The path helpers on the config objects are:

- `config.results_dir` — `{BENCHMARK_ROOT}/results`
- `config.comparisons_dir` — `{BENCHMARK_ROOT}/comparisons`
- `config.comparison_dir` — `{BENCHMARK_ROOT}/comparisons/{run_id}`
- `config.result_dir(endpoint_name)` — `{BENCHMARK_ROOT}/results/{run_id}_{endpoint_name}`

**Log files:**

- `results/{run_id}_{endpoint}/orchestrator.log` — Orchestration history (run config, endpoint progress, job polling, report generation). Written live to the first endpoint's result dir, then copied into the other result dirs at the end of the run.
- `results/{run_id}_{endpoint}/executor.log` — Per-endpoint execution (app startup, ready detection, scenario runs, artifact collection).

**Distributed mode (Pluto jobs):** Pluto pods write their artifacts to `/mnt/localssd/benchmark_output` and then `cp -r` them into the final `results/{run_id}_{endpoint}/` path on sensei-fs (`BENCHMARK_OUTPUT_PATH` is set to that flat location by the orchestrator). No staging `{run_id}/` directory is ever created at the sensei-fs root.

**Legacy migration:** `migrate.py` converts older `{BENCHMARK_ROOT}/{run_id}/{endpoint}/` trees (produced before this refactor) into the current layout. New runs never need it.

## Benchmark Annotations

The benchmark system uses `benchmark_id` args in zone annotations for component discovery. This eliminates hardcoded mappings and makes the system fully generic - any endpoint with proper annotations can be benchmarked.

### Annotation Convention

**Entry Points** - mark with `benchmark_root: True` and `benchmark_id`:

```python
@annotate.func(
    log_code=LogCode.PERF_ZONE,
    backends=[CustomHandlerType.BG_MONITOR],
    args={"benchmark_id": "handle_request", "benchmark_root": True},
)
async def handle_request(self, request):
```

**Components** - mark with `benchmark_id`:

```python
@annotate.func(args={"benchmark_id": "category_detection"})
async def process(self, context):
```

**Grouped Components** - mark with `benchmark_id` and `benchmark_parent`:

```python
@annotate.func(args={"benchmark_id": "media_type_detection", "benchmark_parent": "cm_analysis"})
async def process(self, context):
```

**Code Block Zones** - use `annotate.zone()` for wrapping inline sections:

```python
with annotate.zone(zone="load_data", args={"benchmark_id": "load_data", "benchmark_parent": "handle_request"}):
    library_metadata = await connector.load_metadata()
    training_set = await connector.get_training_images_data()
```

### Hierarchical Grouping

Components can declare a parent via `benchmark_parent` to create a tree in the benchmark report. The `benchmark_parent` value must be another `benchmark_id` string. Components without `benchmark_parent` render at the top level.

Current CM5 hierarchy:

```
handle_request_validation          (top-level, runs before handle_request)
handle_request                     (root)
+-- load_data                      (ACP reads: metadata + training images)
+-- cm5_analysis                   (pipeline process())
|   +-- content_type_detection
|   +-- image_safety_validation
|   +-- media_type_detection
|   +-- background_consistency
|   +-- backing_shape_consistency
|   +-- class_descriptor_generation
|   +-- class_descriptor_validation
|   +-- scap_caption_generation
|   +-- caption_validation
|   +-- scap_caption_editing
|   +-- aggregate_library_changes
|   +-- custom_safety_controls
+-- store_results                  (ACP writes: metadata + images + safety controls)
|   +-- update_manifest
+-- embedding_computation          (training workflow only)
```

All analysis components (including common ones like `class_descriptor_validation` and `ux_data_generation`) use `benchmark_parent: "cm_analysis"` so they appear under the pipeline in both CM4 and CM5 benchmarks.

### Cross-Endpoint Comparison

Equivalent operations across different endpoints are compared automatically when they use the **same** `benchmark_id` value. The benchmark system discovers components dynamically by scanning log entries for `benchmark_id` args - no hardcoded mappings required.

To find all annotated components, search the codebase for `benchmark_id`.

## Distributed Mode (Pluto Jobs)

The `run-distributed` command offloads benchmark workloads to Pluto GPU jobs, allowing the orchestrator to run on CPU-only compute.

### Architecture

```
┌─────────────────────────────────┐
│  CPU Orchestrator (local/CI)    │
│  DistributedBenchmarkOrchestrator│
│    └─ PlutoJobManager           │
│        └─ aip CLI calls         │
└──────┬─────────────────────┬────┘
       │ submit jobs         │ generate report + orchestrator.log
       ▼                     │
┌─────────────────────────┐  │
│     Pluto GPU Jobs      │  │
│  ┌────────┐ ┌────────┐  │  │
│  │ v3 job │ │ v1 job │  │  │
│  └───┬────┘ └───┬────┘  │  │
└──────┼──────────┼───────┘  │
       │ upload   │          │
       ▼          ▼          ▼
┌─────────────────────────────────────────┐
│  sensei-fs shared storage               │
│  /sensei-fs/users/.../benchmark         │
│    ├─ results/                          │
│    │   ├─ {run_id}_v3/                  │
│    │   │   ├─ run_status.json           │
│    │   │   └─ orchestrator.log          │
│    │   └─ {run_id}_v1/                  │
│    │       ├─ run_status.json           │
│    │       └─ orchestrator.log          │
│    └─ comparisons/{run_id}/report/      │
│      (multi-endpoint runs only)         │
└─────────────────────────────────────────┘
```

### Usage

```bash
# CM Analyze: Compare V3 vs V1 using unified endpoint with config overrides
# V1/V3 selection is controlled by worker config via --endpoint-config
python -m colligo.models.firefly.clio_tyom.benchmark run-distributed \
  --branch main \
  --colligo-app firefly_tyom_v2_training \
  --scenarios ./models/colligo/models/firefly/clio_tyom/benchmark/scenarios/cm_analyze/benchmark_scenarios.yaml \
  --endpoints "v3:/v2/images/cm_analyze" "v1:/v2/images/cm_analyze" \
  --endpoint-config 'v3={"deployment_config": {"cm_preprocessor_v1": {"impl_model_config_dict": {"use_v3_pipeline": true}}}}' \
  --endpoint-config 'v1={"deployment_config": {"cm_preprocessor_v1": {"impl_model_config_dict": {"use_v3_pipeline": false}}}}' \
  --sensei-output /sensei-fs/users/$USER/benchmark \
  --colligo-dev-yaml /sensei-fs/users/$USER/colligo.dev.yaml \
  --pluto-project "FFP CM Services"
```

### Key Options

| Option | Description | Required |
|--------|-------------|----------|
| `--branch` | Git branch for Pluto jobs | Yes |
| `--colligo-app` | Colligo app name for dev_supervisor | Yes (unless `--command`) |
| `--command` | Custom shell command to start the app (overrides `--colligo-app`) | No |
| `--scenarios` | Path to scenarios YAML file | Yes |
| `--endpoints` | Endpoints to benchmark (format: `name:path` or `name:path:branch`) | Yes |
| `--sensei-output` | sensei-fs path for results | Yes |
| `--colligo-dev-yaml` | Path to colligo.dev.yaml file on sensei-fs | Yes |
| `--custom-pyenvs` | Space-separated list of custom pyenvs to set up via `./m deps.enable/create/sync` in each Pluto job (e.g., `vllm_0_11_0 cm_5_0_0`). Omit for apps that need no custom pyenv. | No |
| `--endpoint-config` | Per-endpoint worker config overrides as JSON (format: `NAME=JSON`) | No |
| `--artifactory-env` | Path to artifactory_env file (default: repo template) | No |
| `--pluto-snapshot-id` | Pluto snapshot with pre-configured environment | No |
| `--pluto-project` | Pluto project name (default: `FFP CM Services`) | No |
| `--pluto-gpu-instance-type` | GPU instance type (default: `p5.48xlarge`) | No |
| `--pluto-max-retries` | Maximum retries for failed/preempted jobs (default: `3`) | No |
| `--pluto-poll-interval` | Job status polling interval in seconds (default: `60.0`) | No |
| `--pluto-timeout` | Maximum wait time for all jobs in seconds (default: `18000.0`) | No |
| `--aip-python-path` | Python with adobe-aip installed (default: `/opt/conda/bin/python3`). Do not use colligo dev venv. | No |

### Per-Endpoint Branch Format

The `--endpoints` argument requires explicit paths:

- `name:path` - Endpoint name and API path (required)
- `name:path:branch` - Explicit path and git branch

### Job Lifecycle

1. **Submit**: Creates Pluto job with `--init-script` and `--main-script`
2. **Init Script**: Clones colligo repo, runs `deps.sync`, and iterates `BENCHMARK_CUSTOM_PYENVS` (from `--custom-pyenvs`) to run `./m deps.enable/create/sync` for each listed pyenv. Skipped entirely when the list is empty.
3. **Main Script**: Runs `benchmark execute` for single endpoint, copies results to sensei-fs
4. **Poll**: Orchestrator polls `aip job status` every 60s
5. **Retry**: On `Stopped` (preemption) or `Failed`, resubmit up to max_retries
6. **Report**: Generate HTML comparison report directly on sensei-fs

### Graceful Shutdown (Signal Handling)

`DistributedBenchmarkOrchestrator` installs SIGINT/SIGTERM handlers during `run_full_benchmark`:

- **First signal**: Sets a shutdown event, which interrupts the polling sleep immediately. All active (non-terminal) Pluto jobs receive a stop command (fire-and-forget via `PlutoJobManager.stop_job` — no polling for confirmation). The orchestrator logs a job summary and raises `KeyboardInterrupt`, skipping report generation.
- **Second signal**: Forces immediate exit via `SystemExit(128 + signum)`.
- Signal handlers are installed at the start of `run_full_benchmark` and removed in a `finally` block, so they don't leak beyond the orchestrator's lifetime.
- The polling loop uses `asyncio.wait_for(shutdown_event.wait(), timeout=poll_interval)` instead of `asyncio.sleep`, allowing instant interruption when a signal arrives mid-sleep.

### Configuration Classes

- **PlutoJobConfig**: snapshot_id, project, gpu_instance_type, max_retries (job retries), poll_interval (job status), job_timeout (total)
- **DistributedBenchmarkConfig**: pluto_config, git_branch, sensei_output_path, scenarios_file, endpoints (all required), plus spec or command (at least one)

## Extending

- **Add new use case**: Create scenarios in `scenarios/your_use_case/`
- **Add new endpoints**: Use `--endpoints name:path:branch` with explicit paths
- **Per-endpoint branches**: Use format `name:path:branch` to test different code versions per endpoint
- **Add new components to benchmark**: Add `args={"benchmark_id": "component_name"}` to the zone annotation
- **Add new entry points**: Add `args={"benchmark_id": "handle_request", "benchmark_root": True}` to the entry point annotation
- **Custom scenarios**: Copy `scenarios/example_scenario.yaml` and customize

## Compare Report Generator

Optional "Compare" tab for side-by-side comparison of endpoint outputs using pluggable generators.

### Key Files
- **compare_report_generator/types.py**: `CompareReportGenerator` protocol definition
- **compare_report_generator/cm_analyze.py**: CM Analyze implementation (captions + image sizes)

### Creating Custom Generators
1. Create module in `benchmark/compare_report_generator/`
2. Implement class with `generate_html(scenarios, run_ids) -> str`
3. Access data via `result.response_data` or `LogParser.parse_benchmark_metadata()`

### Logging Custom Benchmark Metadata
Log with `benchmark_id` in `extra` for compare generators to extract:

```python
logger.info("msg", extra={"benchmark_id": "my_id", "field": value})
```

See README.md for CLI usage examples.

## Dashboard

The `dashboard` command launches a FastAPI server (`dashboard/server.py`) that exposes a single-page UI for browsing the benchmark output tree. It operates on the `results/` + `comparisons/` directory layout under `--benchmark-dir`.

### Entities

- **Result**: A single endpoint run, stored at `{benchmark_dir}/results/{result_id}/` (contains `run_status.json`, logs, `bg_monitor/`, optional `label.json`, and `report/benchmark_report.html` — a single-column HTML report inspectable directly from the dashboard).
- **Comparison**: A report generated from 2+ results, stored at `{benchmark_dir}/comparisons/{comparison_id}/` (contains `comparison.json`, `report/benchmark_report.html`, optional `label.json`).

### Per-Result Reports

Every result directory gets its own single-column HTML report at `results/{result_id}/report/benchmark_report.html` so a single endpoint run can be inspected directly from the dashboard without first creating a comparison. Reports are produced in two places:

1. **At run time** — `BenchmarkOrchestrator`, `DistributedBenchmarkOrchestrator`, and the standalone `execute` command call `generate_result_report(result_dir)` after each endpoint completes.
2. **Lazily, on first dashboard view** — `GET /api/results/{id}/report` generates the report on demand if it is missing, so historical results without a pre-built report still render in the UI.

### REST API

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/api/results` | List all results |
| `GET` | `/api/results/{id}` | Get single result metadata (includes `has_report` flag) |
| `GET` | `/api/results/{id}/report` | Serve `report/benchmark_report.html` (generated lazily if missing) |
| `GET` | `/api/results/{id}/images/{name}` | Serve images embedded in the per-result report |
| `PUT` | `/api/results/{id}/label` | Set label |
| `DELETE` | `/api/results/{id}/label` | Clear label |
| `DELETE` | `/api/results/{id}` | Delete the result directory from disk |
| `GET` | `/api/comparisons` | List all comparisons |
| `GET` | `/api/comparisons/{id}` | Get single comparison metadata |
| `POST` | `/api/comparisons` | Create a new comparison from selected results |
| `GET` | `/api/comparisons/{id}/report` | Serve `benchmark_report.html` |
| `GET` | `/api/comparisons/{id}/images/{name}` | Serve report images |
| `PUT` | `/api/comparisons/{id}/label` | Set label |
| `DELETE` | `/api/comparisons/{id}/label` | Clear label |
| `DELETE` | `/api/comparisons/{id}` | Delete the comparison directory from disk |

### Deletion Semantics

Deleting a result or comparison from the UI must remove the corresponding directory from the source filesystem (i.e., `shutil.rmtree` on `{benchmark_dir}/results/{id}` or `{benchmark_dir}/comparisons/{id}`). There is no soft-delete or trash — the action is destructive and irreversible.

Requirements for the `DELETE /api/results/{id}` and `DELETE /api/comparisons/{id}` endpoints:

- Return `404` if the target directory does not exist.
- Reject any `id` containing path separators or `..` (defense-in-depth against path traversal); only accept IDs that resolve to a direct child of `results_dir` / `comparisons_dir`.
- Remove the entire directory tree, including logs, `bg_monitor/` data, `run_status.json`, labels, reports, and images.
- Return `{"id": <id>, "deleted": true}` on success.
- The UI must prompt for confirmation before issuing the request and refresh the list after a successful deletion. The currently selected entity should be cleared if it was the one deleted.

Deleting a result does **not** cascade into comparisons that reference it; comparisons keep their generated reports and remain viewable. The listing simply shows the missing `result_id` by its label without linking back to a live result.
