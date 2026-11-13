# Benchmark CLI

A tool for benchmarking Colligo pipeline endpoints, collecting timing metrics, and generating HTML comparison reports.

## Quick Start

### CM Analyze Example

```bash
# Compare V3 vs V1
python -m colligo.models.firefly.clio_tyom.benchmark run-distributed \
  --branch main \
  --colligo-app firefly_tyom_v2_training \
  --scenarios ./models/colligo/models/firefly/clio_tyom/benchmark/scenarios/cm_analyze/benchmark_scenarios.yaml \
  --endpoints "v3:/v2/images/cm_analyze_v3" "v1:/v2/images/cm_analyze" \
  --sensei-output /sensei-fs/users/$USER/benchmark \
  --colligo-dev-yaml /sensei-fs/users/$USER/colligo.dev.yaml

# Single endpoint (V3 only)
python -m colligo.models.firefly.clio_tyom.benchmark run-distributed \
  --branch main \
  --colligo-app firefly_tyom_v2_training \
  --scenarios ./models/colligo/models/firefly/clio_tyom/benchmark/scenarios/cm_analyze/benchmark_scenarios.yaml \
  --endpoints "v3:/v2/images/cm_analyze_v3" \
  --sensei-output /sensei-fs/users/$USER/benchmark \
  --colligo-dev-yaml /sensei-fs/users/$USER/colligo.dev.yaml
```

## Commands

| Command | Description |
|---------|-------------|
| `run-distributed` | Distributed benchmark: spawns Pluto GPU jobs, polls for completion, generates report on sensei-fs |
| `run` | Local benchmark: starts app locally, runs scenarios, generates report |
| `execute` | Single endpoint: runs scenarios for one endpoint only |
| `report` | Generates report from existing run directories |
| `dashboard` | Launch web UI for viewing and labeling benchmark results |

---

## Required Configuration

### AIP CLI Installation (Required for Distributed Benchmarks)

The `run-distributed` command requires the AIP CLI tool to manage Pluto jobs. Install it in the conda environment:

```bash
# Source Artifactory credentials
source ./models/colligo/models/firefly/clio_tyom/benchmark/templates/artifactory_env.template

# Install adobe-aip in conda
/opt/conda/bin/pip install "adobe-aip[compute]" --extra-index-url=$EXTRA_INDEX_URL
```

> **Note:** This is a one-time setup. The AIP CLI will be available for all future benchmark runs.

### Required Parameters

All benchmark commands require explicit configuration (no defaults):

| Parameter | Description |
|-----------|-------------|
| `--branch` | Git branch to clone in Pluto jobs |
| `--colligo-app` | Colligo app name for dev_supervisor (e.g., `firefly_tyom_v2_training`) |
| `--scenarios` | Path to scenarios YAML file |
| `--endpoints` | Endpoints to benchmark (format: `name:path` or `name:path:branch`) |
| `--sensei-output` | sensei-fs path for results upload (for `run-distributed`) |
| `--colligo-dev-yaml` | Path to colligo.dev.yaml file on sensei-fs |

### colligo.dev.yaml (Required for Distributed Benchmarks)

Pluto jobs require a `colligo.dev.yaml` file with specific configurations for logging and memory profiling.

**Required configurations:**

```yaml
# Logging - enables log file output for timing extraction
logging:
  dev_log_file: .logs/colligo.log
  log_to_console: false

# Tracing - enables bg_monitor for memory profiling
tracing:
  extra_backends_factory: colligo.models.firefly.clio_tyom.benchmark.profiling.handlers.extraHandlerFactoryCreator
  enabled_backends: ["log", "tracing", "bg_monitor"]
  default_backends: ["log", "tracing", "bg_monitor"]
```

**Setup steps:**

1. Create or update your `colligo.dev.yaml` with the required sections above
2. Copy to sensei-fs: `cp colligo.dev.yaml /sensei-fs/users/<your-username>/colligo.dev.yaml`
3. Pass to CLI: `--colligo-dev-yaml /sensei-fs/users/<your-username>/colligo.dev.yaml`

> **Important:** The log file path in `colligo.dev.yaml` (`logging.dev_log_file`) must match the `--app-log-file` CLI argument (default: `.logs/colligo.log`).

### Artifactory Credentials (Optional)

Pluto jobs use Artifactory credentials to install Python dependencies. **By default, the benchmark uses the shared `cliobot` service account** from the repo template, so no setup is required.

If you need to use your own credentials:

1. Copy the template: `cp templates/artifactory_env.template /sensei-fs/users/<your-username>/.artifactory_env`
2. Edit with your credentials (generate a token at [Artifactory User Profile](https://artifactory-uw2.adobeitc.com/ui/admin/artifactory/user_profile))
3. Pass to CLI: `--artifactory-env /sensei-fs/users/<your-username>/.artifactory_env`

---

## Usage Examples

### 1. Distributed Benchmark (CM Analyze)

Run benchmarks on Pluto GPU infrastructure:

```bash
python -m colligo.models.firefly.clio_tyom.benchmark run-distributed \
  --branch main \
  --colligo-app firefly_tyom_v2_training \
  --scenarios ./models/colligo/models/firefly/clio_tyom/benchmark/scenarios/cm_analyze/benchmark_scenarios.yaml \
  --endpoints "v3:/v2/images/cm_analyze_v3" "v1:/v2/images/cm_analyze" \
  --sensei-output /sensei-fs/users/$USER/benchmark \
  --colligo-dev-yaml /sensei-fs/users/$USER/colligo.dev.yaml \
  --pluto-project "FFP CM Services"
```

### 2. Per-Endpoint Branches

Compare a feature branch against main:

```bash
python -m colligo.models.firefly.clio_tyom.benchmark run-distributed \
  --branch main \
  --colligo-app firefly_tyom_v2_training \
  --scenarios ./models/colligo/models/firefly/clio_tyom/benchmark/scenarios/cm_analyze/benchmark_scenarios.yaml \
  --endpoints "v3:/v2/images/cm_analyze_v3:my/feature-branch" "v1:/v2/images/cm_analyze" \
  --sensei-output /sensei-fs/users/$USER/benchmark \
  --colligo-dev-yaml /sensei-fs/users/$USER/colligo.dev.yaml
```

### 3. Per-Endpoint Config Overrides

Use `--endpoint-config` to override worker configuration per endpoint. This allows you to override settings from `colligo.dev.yaml` at runtime, enabling A/B comparisons with different worker configurations on the same endpoint.

The format is `NAME=JSON` where `NAME` matches an endpoint name from `--endpoints` and `JSON` is the configuration to merge into the worker config.

```bash
# Compare V3 vs V1 pipeline on the SAME endpoint by toggling a config flag
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

The `--endpoint-config` JSON structure follows the same format as `colligo.dev.yaml`. For example, to override a worker's `impl_model_config_dict` settings, use:

```json
{
  "deployment_config": {
    "<worker_name>": {
      "impl_model_config_dict": {
        "<setting>": <value>
      }
    }
  }
}
```

This is useful when:
- Comparing different algorithm versions controlled by a feature flag
- Testing different model configurations without modifying `colligo.dev.yaml`
- Running A/B benchmarks where only a config parameter differs between endpoints

### 4. With Compare Generator

Enable side-by-side comparison of endpoint outputs:

```bash
python -m colligo.models.firefly.clio_tyom.benchmark run-distributed \
  --branch main \
  --colligo-app firefly_tyom_v2_training \
  --scenarios ./models/colligo/models/firefly/clio_tyom/benchmark/scenarios/cm_analyze/benchmark_scenarios.yaml \
  --endpoints "v3:/v2/images/cm_analyze_v3" "v1:/v2/images/cm_analyze" \
  --sensei-output /sensei-fs/users/$USER/benchmark \
  --colligo-dev-yaml /sensei-fs/users/$USER/colligo.dev.yaml \
  --compare-generator cm_analyze.CMAnalyzeCompareReportGenerator
```

### 5. Generate Report Only

Generate a comparison report from existing benchmark runs:

```bash
python -m colligo.models.firefly.clio_tyom.benchmark report \
  --input ./data/benchmark/20260127_143052/v3 ./data/benchmark/20260127_143052/v1 \
  --output ./data/benchmark/20260127_143052/report \
  --title "V3 vs V1 Performance Comparison"
```

### 6. Dashboard

Launch the web UI for viewing and labeling benchmark results:

```bash
# View distributed benchmark results on sensei-fs
python -m colligo.models.firefly.clio_tyom.benchmark.dashboard \
  --benchmark-dir /sensei-fs/users/$USER/benchmark \
  --port 8080

# View local benchmark results
python -m colligo.models.firefly.clio_tyom.benchmark.dashboard \
  --benchmark-dir ./data/benchmark \
  --port 8080
```

---

## Endpoint Format

The `--endpoints` argument requires explicit paths:

| Format | Description |
|--------|-------------|
| `name:path` | Endpoint name and API path (required) |
| `name:path:branch` | Endpoint with explicit git branch |

Examples:
- `v3:/v2/images/cm_analyze_v3` → explicit path, branch from `--branch`
- `v3:/v2/images/cm_analyze_v3:feature/new` → explicit path and branch

---

## Scenario Files

Scenario files are organized by use case in `scenarios/`:

```
scenarios/
├── cm_analyze/              # CM Analyze specific scenarios
│   ├── benchmark_scenarios.yaml
│   └── benchmark_test_scenario.yaml
├── README.md                # Scenario format documentation
└── example_scenario.yaml    # Template for new scenarios
```

See [scenarios/README.md](scenarios/README.md) for scenario format details.

---

## Output Structure

### Local mode (`run`)

Each benchmark run creates a timestamped folder under `data/benchmark/`:

```
data/benchmark/
└── 20260127_143052/              # Run ID (auto-generated or custom)
    ├── orchestrator.log
    ├── v3/
    │   ├── run_status.json       # Execution metadata + scenario results
    │   ├── logs/                 # Application logs
    │   └── bg_monitor/           # Memory profiler data
    ├── v1/
    │   └── ...
    └── report/
        ├── benchmark_report.html # Interactive comparison report
        ├── benchmark_results.json
        └── images/
```

### Distributed mode (`run-distributed`)

All output is written directly to sensei-fs (no local copy):

```
{sensei_output}/
└── 20260127_143052/              # Run ID (auto-generated or custom)
    ├── orchestrator.log
    ├── v3/                       # Uploaded by Pluto job
    │   ├── run_status.json
    │   ├── logs/
    │   └── bg_monitor/
    ├── v1/                       # Uploaded by Pluto job
    │   └── ...
    └── report/                   # Generated directly on sensei-fs
        ├── benchmark_report.html
        ├── benchmark_results.json
        └── images/
```

---

## Parameter Reference

### `run-distributed` Command

#### Required Parameters

| Parameter | Description |
|-----------|-------------|
| `--branch` | Git branch to clone in Pluto jobs |
| `--colligo-app` | Colligo app name for dev_supervisor (e.g., `firefly_tyom_v2_training`) |
| `--scenarios`, `-s` | Path to scenarios YAML file (relative to repo root) |
| `--endpoints`, `-e` | Endpoints to benchmark (format: `name:path` or `name:path:branch`) |
| `--sensei-output` | sensei-fs path for results upload from Pluto jobs |
| `--colligo-dev-yaml` | Path to colligo.dev.yaml file on sensei-fs |

#### Optional Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--run-id` | Auto-generated | Unique run identifier (e.g., `20260127_143052`) |
| `--artifactory-env` | Repo template | Path to artifactory_env file |
| `--endpoint-config` | None | Per-endpoint worker config overrides as JSON (format: `NAME=JSON`). Overrides settings from `colligo.dev.yaml`. Can be specified multiple times for different endpoints. |
| `--compare-generator` | None | Compare generator class path |

#### Pluto Job Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--pluto-snapshot-id` | None | Pluto snapshot ID with pre-configured environment |
| `--pluto-project` | `FFP CM Services` | Pluto project name |
| `--pluto-gpu-instance-type` | `p5.48xlarge` | GPU instance type for Pluto jobs |
| `--pluto-xpus-per-pod` | `4` | Number of XPUs (GPUs) per pod |
| `--pluto-max-retries` | `3` | Maximum retries for failed or preempted Pluto jobs |
| `--pluto-poll-interval` | `60.0` | Interval in seconds for polling Pluto job status |
| `--pluto-timeout` | `18000.0` | Maximum total time in seconds to wait (5 hours) |

#### IMS Authentication (Optional)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--ims-user-email` | None | User email for IMS authentication |
| `--ims-user-password` | None | User password for IMS authentication |
| `--ims-user-type` | None | User type: `T1`, `T2`, `T3`, or `T2E` |
| `--ims-org-id` | None | Organization ID for EOA token (required for T2E) |
| `--ims-client-id` | None | IMS client ID |
| `--ims-client-secret` | None | IMS client secret |
| `--ims-host` | `https://ims-na1-stg1.adobelogin.com` | IMS host URL |

### `report` Command

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--input`, `-i` | *Required* | Input directories containing run data |
| `--output`, `-o` | `benchmark_results/report` | Output directory for report |
| `--title`, `-t` | `Benchmark Report` | Report title |
| `--compare-generator` | None | Compare generator class path |

### `dashboard` Command

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--benchmark-dir` | `data/benchmark` | Path to benchmark output folder |
| `--port` | `8501` | Server port |
| `--host` | `0.0.0.0` | Server host |

---

## Compare Report Generator

The benchmark report includes an optional "Compare" tab for side-by-side comparison of endpoint outputs.

### Available Compare Generators

| Generator | Description |
|-----------|-------------|
| `cm_analyze.CMAnalyzeCompareReportGenerator` | Compares CM Analyze outputs: captions (with diff highlighting), image analysis sizes, aspect ratios |

### Creating Custom Compare Generators

1. Create a new module in `benchmark/compare_report_generator/`
2. Implement a class with the `generate_html()` method:

```python
from colligo.models.firefly.clio_tyom.benchmark.log_parser import LogParser
from colligo.models.firefly.clio_tyom.benchmark.report_generator import ScenarioResult

class MyCompareReportGenerator:
    def generate_html(
        self,
        scenarios: dict[str, dict[str, ScenarioResult]],
        run_ids: list[str],
    ) -> str:
        return "<div>My comparison content</div>"
```

3. Use with: `--compare-generator my_compare.MyCompareReportGenerator`
