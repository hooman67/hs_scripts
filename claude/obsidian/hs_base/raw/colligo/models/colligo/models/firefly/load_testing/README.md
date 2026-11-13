# Worker-Level Load Testing Framework

This framework enables **worker-level load testing** for Colligo pipelines without requiring full pipeline deployment.

## Purpose

Current load testing in Colligo requires deploying entire pipelines with all workers, which is resource-intensive and complex when we are trying to benchmark a single worker. For example, we need to over-provision the other workers in order to provide saturating traffic to the worker under testing. This framework solves that by:

1. **Capturing** real request/response data for individual workers
2. **Replaying** that data against individual workers running in isolation
3. **Measuring** performance metrics (latency, throughput, error rates) for specific workers

## Benefits

✅ **No GPU Over-provisioning**: Test individual workers without running the entire pipeline  
✅ **Easy Benchmarking and Isolated Testing**: Test any component independently

## Quick Start

### 1. Capture Data

Use the automated capture script to start the pipeline, generate traffic via Locust, and upload captured data to S3 — all in one command:

```bash
# Full automated capture (starts server, runs Locust headless for 1 hour, uploads to S3)
# --remote-endpoint is auto-discovered from colligo.dev.yaml
python models/colligo/models/firefly/load_testing/tools/cli/capture_pipeline_traffic.py \
    --spec lego_v1 \
    --api-path v1/images/generate-async

# Custom parameters (explicit run type, shorter duration)
python models/colligo/models/firefly/load_testing/tools/cli/capture_pipeline_traffic.py \
    --spec lego_v1 \
    --api-path v1/images/generate-async \
    --run-type imageV5_t2i_load_4MP_speed \
    --users 1 \
    --run-time 3600

# Traffic only (if you already started the server with capturing enabled)
python models/colligo/models/firefly/load_testing/tools/cli/capture_pipeline_traffic.py \
    --spec lego_v1 \
    --api-path v1/images/generate-async \
    --traffic-only --run-time 600
```

Data is automatically uploaded to S3. The S3 path is deterministic: `captured_data/{spec_name}/{session_id}/{worker_name}/`.

<details>
<summary>Manual capture (alternative)</summary>

You can also capture manually by setting the env var and starting the server yourself:

```bash
export COLLIGO_CAPTURE_SESSION_ID=my-session-20260227
python -m colligo.rhode.commands.dev_supervisor --spec lego_v1 --locust
# Then open Locust UI at http://localhost:8004 and start a swarm
```
</details>

### 2. Run Load Test

Use the captured data to load test workers. The tool starts the pipeline, waits for ready, warms up, sends traffic, and tears down automatically.

```bash
# Single worker — full lifecycle:
python models/colligo/models/firefly/load_testing/tools/cli/run_load_test.py \
    --combo gen45_text_encoder_v1_1024:1 \
    --spec-name lego_v1 \
    --capture-session-id lego-v1-captured-locust-2026-03-03 \
    --total-requests 100 \
    --concurrency 10

# Multiple workers packed on one GPU:
python models/colligo/models/firefly/load_testing/tools/cli/run_load_test.py \
    --combo gen45_text_encoder_v1_1024:1,nsfw_adobe_one:1 \
    --spec-name lego_v1 \
    --capture-session-id lego-v1-captured-locust-2026-03-03 \
    --total-requests 50 \
    --concurrency 5

# Traffic-only (workers already running, skip pipeline start/stop):
python models/colligo/models/firefly/load_testing/tools/cli/run_load_test.py \
    --combo gen45_text_encoder_v1_1024:1 \
    --spec-name lego_v1 \
    --capture-session-id lego-v1-captured-locust-2026-03-03 \
    --traffic-only \
    --total-requests 100 \
    --concurrency 10
```

### 3. Virtual-User Pipeline Mode

`--virtual-users` drives a **serialized per-user pipeline** against already-deployed workers, so you can measure end-to-end pipeline throughput while preserving per-user call order and multiplicity. `--pipeline worker_a:N,worker_b:M` defines the ordered call shape per user.

This is the right mode when you want to model how packing two models affects the full pipeline throughput, because a single virtual user can only invoke one worker at a time, so a slower worker naturally back-pressures the others.

```bash
# Single loaded run with 4 virtual users.
# Each user calls prompt_forge twice, then nsfw once, in sequence.
python models/colligo/models/firefly/load_testing/tools/cli/run_load_test.py \
    --combo prompt_forge_v2_1:1,nsfw_adobe_one:1 \
    --spec-name lego_v1 \
    --capture-session-id lego-v1-captured-locust-2026-03-03 \
    --virtual-users 4 \
    --pipeline prompt_forge_v2_1:2,nsfw_adobe_one:1 \
    --duration 60
```

#### Sweep several virtual-user values in one run

`--virtual-users` also accepts a **comma-separated list**. Each value is run in sequence against the same warmed-up pipeline, so:

- `V=1` gives you a **clean service-time reference** (no queueing, so latency ≈ true service time)
- `V=N` (e.g. 4) gives you **throughput under load**
- `V=1,2,4,8` gives you a **saturation curve** to find the knee

Warmup is shared across all values in the list, so the pipeline only starts once.

```bash
# Reference (V=1) + loaded (V=4) in a single command:
python models/colligo/models/firefly/load_testing/tools/cli/run_load_test.py \
    --combo prompt_forge_v2_1:1,nsfw_adobe_one:1 \
    --spec-name lego_v1 \
    --capture-session-id lego-v1-captured-locust-2026-03-03 \
    --virtual-users 1,4 \
    --pipeline prompt_forge_v2_1:2,nsfw_adobe_one:1 \
    --duration 60

# Saturation sweep — find where iter/s plateaus:
python models/colligo/models/firefly/load_testing/tools/cli/run_load_test.py \
    --combo prompt_forge_v2_1:1,nsfw_adobe_one:1 \
    --spec-name lego_v1 \
    --capture-session-id lego-v1-captured-locust-2026-03-03 \
    --virtual-users 1,2,4,8 \
    --pipeline prompt_forge_v2_1:2,nsfw_adobe_one:1 \
    --duration 60
```

> **Interpreting the results.** For `V>1` the per-worker `latency` fields include queue wait behind other virtual users, so they are higher than the true service time. For clean service-time numbers, always include `V=1` in the list. Use `iter/s` (or `iter/min`) as the apples-to-apples throughput metric across all values of `N`.

### 4. Pipeline E2E mode (`--pipeline-e2e`)

`--pipeline-e2e` runs a **client-side end-to-end load test** against a deployed async pipeline endpoint. It POSTs to the endpoint, polls the result URL until each job reaches a terminal `x-task-status`, and reports per-request E2E latency with P50/P95/P99 — directly comparable to the Locust `ASYNC_E2E` row but with raw samples (so percentiles are exact).

This is the analog of `clineto/tests/load/loadtest.py`'s POST + poll workflow, but generalized: any spec whose `compare.py` defines `generate_inputs(context)` is supported via `--run-type`.

```bash
# Hit a deployed lego_v1 endpoint, measure E2E async latency
python models/colligo/models/firefly/load_testing/tools/cli/run_load_test.py \
    --pipeline-e2e \
    --base-url https://lego-v1-dev.ethos851-stage-or2.ethos.adobe.net \
    --run-type imageV5_t2i_load_4MP_speed \
    --total-requests 100 --concurrency 4 \
    --request-timeout 600

# Shorthand for dev/stg (requires --spec-name)
python models/colligo/models/firefly/load_testing/tools/cli/run_load_test.py \
    --pipeline-e2e \
    --env stg --spec-name lego_v1 \
    --run-type mask_samples \
    --total-requests 5 --concurrency 1 --debug-token
# Prints Gallery report: file://.../report.html at end (use --no-report to skip)

# Same gallery against a deployed endpoint via profile_pipeline_e2e (no local dev_supervisor)
python models/colligo/models/firefly/load_testing/tools/profiling/profile_pipeline_e2e.py \
    --env dev --spec lego_v1 --run-type mask_samples \
    --total-requests 5 --concurrency 1

# Auth via env vars (preferred for ethos endpoints)
export COLLIGO_IMS_TOKEN="$(get-ims-token)"
export COLLIGO_X_API_KEY="colligo_testing"
python models/colligo/models/firefly/load_testing/tools/cli/run_load_test.py \
    --pipeline-e2e \
    --base-url https://lego-v1-stage.ethos851-stage-or2.ethos.adobe.net \
    --run-type imageV5_t2i_load_1MP_speed \
    --total-requests 50 --concurrency 2 --warmup-requests 5

# Duration-based (sustained throughput / soak)
python models/colligo/models/firefly/load_testing/tools/cli/run_load_test.py \
    --pipeline-e2e \
    --base-url http://localhost:8000 \
    --run-type imageV5_ie_load_1MP_speed \
    --duration 600 --concurrency 8
```

**Auth resolution order (highest priority first)**
1. `--ims-token` / `--x-api-key` flags
2. `$COLLIGO_IMS_TOKEN` / `$COLLIGO_X_API_KEY` env vars
3. `--debug-token` (paste-once user token from the pipeline's `/debug/` page; cached under `~/.colligo/load_test_tokens/<host>.json` until ~5 min before JWT expiry; `--refresh-debug-token` forces a re-prompt). The `x-api-key` header is auto-derived from the JWT's `client_id` (typically `colligo_testing`). Use this when the gateway only allowlists *user* tokens — e.g. `lego-v1-stage` rejects the auto-minted `colligo-developer` service token.

   The `/debug/` page is only served on the **corp** host (e.g. `lego-v1-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net`), which is reachable from a laptop on Adobe VPN but **not** from a pluto pod. For pluto runs, mint the token on your laptop with the dedicated subcommand below and forward via env vars:

   ```bash
   # On your laptop (corp network):
   python models/colligo/models/firefly/load_testing/tools/cli/run_load_test.py \
       --mint-debug-token-only \
       --debug-token-url https://lego-v1-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/debug/

   # Prints (copy/paste these on the pluto pod):
   #   export COLLIGO_IMS_TOKEN=ey...
   #   export COLLIGO_X_API_KEY=colligo_testing

   # On the pluto pod, after exporting the env vars:
   python models/colligo/models/firefly/load_testing/tools/cli/run_load_test.py \
       --pipeline-e2e \
       --base-url https://lego-v1-stage.ethos851-stage-or2.ethos.adobe.net \
       --run-type mask_samples \
       --total-requests 10 --concurrency 4
   ```

   When `--debug-token` is used directly (laptop runs against a public gateway) and `--base-url` doesn't look corp-internal, the tool prints a warning and points you at this subcommand.
4. **Auto-mint from `dev_ims_credentials` in `colligo.dev.yaml`** (default — same path clineto's `loadtest.py --import-mode remote` uses; mints a service token for `client_id=colligo-developer`). Pass `--no-auto-ims-token` to disable.
5. No auth headers (works for fully local sandbox endpoints).

The minted `client_id` is printed in the run header so you can confirm what you're sending. If you see:
- `403 ErrMissingOauthToken` — `dev_ims_credentials` is unset in `colligo.dev.yaml` or auto-mint failed; populate it (`./m sys.setup` for Adobe internal) or pass `--ims-token`.
- `403 ErrInvalidClientIdOauthToken` — the gateway you're hitting doesn't allowlist the auto-minted `client_id` (e.g. `lego-v1-stage` only allowlists certain clients). The runner aborts after 3 consecutive auth failures and prints actionable hints. Either pass an externally minted token via `--ims-token`, run against a gateway that allowlists `colligo-developer` (e.g. `clineto-stage`), or ask the platform team to allowlist your client.

> Note: `inference_integration_testing_config.dev_ims_user_credentials` (`colligo-developer-client`) is **not** usable for auto-mint — it requires the `password` / `cluster_at_exchange` / `guest_token` grants (real human user / org context), not the `authorization_code` service grant. Use `--ims-token` if you want to drive a load test with a user-scoped token.

**Other notes**
- `--pipeline-e2e` is mutually exclusive with `--combo`, `--virtual-users`, `--capture-session-id`, `--s3-path`, and `--traffic-only` — it does not use captured worker data.
- By default, pipeline E2E runs write an HTML gallery (`report.html`) under the run output directory with prompt, input/mask thumbnails (for `mask_samples`), output images, and per-request latency. Pass `--no-report` to skip.
- `--env dev|stg` resolves the base URL from a small registry (currently `lego_v1` only). Use `--base-url` for other specs or custom hosts.
- Distributed tracing (chrome trace / zone tables) is only available in local `profile_pipeline_e2e.py` runs without `--env` / `--base-url`.
- `t_start` is captured **before** the POST is sent (clean E2E latency definition).
- The default `--poll-interval` is 1 s; that's the lower bound on measured latency. Lower it for short-running endpoints; servers can also override it via `Retry-After`.
- Results are printed to stdout and written to `<log-dir>/pipeline_e2e_<spec>_<run_type>_<timestamp>.json`.
- `--remote --pod ...` works with `--pipeline-e2e`: the script re-invokes itself on the pod with the same flags forwarded.

### 5. Remote execution and pod reuse

Add `--remote` to run the whole thing on an AIP GPU pod, or `--remote --pod POD_NAME` to **reuse an existing pod** (skips AIP job creation; the pod's repo is fetched/checked out to `--branch` and `./m deps.create` is run before the load test).

```bash
# Create a new pod and run remotely:
python models/colligo/models/firefly/load_testing/tools/cli/run_load_test.py \
    --remote --project "FF Product Eval & Optimization" \
    --gpu-instance-type p5.48xlarge \
    --combo prompt_forge_v2_1:1,nsfw_adobe_one:1 \
    --spec-name lego_v1 \
    --capture-session-id lego-v1-captured-locust-2026-03-03 \
    --virtual-users 1,4 \
    --pipeline prompt_forge_v2_1:2,nsfw_adobe_one:1 \
    --duration 60 \
    --keep-alive

# Reuse an existing pod (skip job creation):
python models/colligo/models/firefly/load_testing/tools/cli/run_load_test.py \
    --remote --pod pluto-prod-shawnliu-load-test-0416-0 \
    --combo prompt_forge_v2_1:1,nsfw_adobe_one:1 \
    --spec-name lego_v1 \
    --capture-session-id lego-v1-captured-locust-2026-03-03 \
    --virtual-users 1,4 \
    --pipeline prompt_forge_v2_1:2,nsfw_adobe_one:1 \
    --duration 60
```

## Reusing an existing Pluto pod with `colligo_pluto_launcher`

`colligo_pluto_launcher` is the companion CLI that provisions an AIP GPU pod with a full Colligo dev environment and (optionally) starts `dev_supervisor`. It supports **pod reuse** via `--pod`, so you can iterate on a branch without waiting 4+ minutes for a fresh pod to come up.

When `--pod POD_NAME` is passed, the launcher:

- skips AIP job submission, SSH configuration, and interactive project selection
- SSHes to the existing pod
- fetches and checks out `--branch` (works even for `--single-branch` clones)
- runs `./m deps.sync` to refresh the venv against the new branch
- launches the main command (`dev_supervisor` if `--spec` is provided, otherwise an interactive wait loop)

SSH access to the pod must already be configured. The easiest way is to reuse a pod from a previous launcher run or from `aip job configure ssh <job> --project <proj> --all-pods`.

```bash
# Fresh run — creates a pod, sets up env, starts dev_supervisor for lego_v1.
# --local-deploys / --remote-endpoint are auto-discovered from colligo.dev.yaml.
python models/colligo/models/firefly/load_testing/tools/cli/colligo_pluto_launcher.py \
    --name my-dev-job --project "FF Product Eval & Optimization" \
    --gpu-instance-type p5.48xlarge \
    --spec lego_v1

# Reuse the same pod to test a new branch — no new AIP job, no reprovisioning.
# The launcher fetches the branch and runs ./m deps.sync before dev_supervisor.
python models/colligo/models/firefly/load_testing/tools/cli/colligo_pluto_launcher.py \
    --pod pluto-prod-shawnliu-my-dev-job-0416-0 \
    --branch my-feature-branch \
    --spec lego_v1

# Reuse for interactive debugging — no --spec, so the pod just stays up.
# Use SSH to poke around, start dev_supervisor manually, run ad-hoc commands.
python models/colligo/models/firefly/load_testing/tools/cli/colligo_pluto_launcher.py \
    --pod pluto-prod-shawnliu-my-dev-job-0416-0 \
    --branch my-feature-branch
```

> **Tip.** `run_load_test.py --remote --pod POD_NAME` uses the same reuse machinery under the hood, so the same `POD_NAME` can be switched between the launcher (for interactive dev) and `run_load_test` (for load tests) without tearing the pod down.

## Run Types Reference

The `--run-type` parameter selects which set of test inputs Locust uses when generating traffic. Each pipeline endpoint defines its own run types in its `compare.py` module.

### How run_type works

The run type is passed to the pipeline's `compare_info.generate_inputs()` function, which selects the appropriate request YAML or generates synthetic inputs. The format is `{pipeline}_{workflow}_load_{resolution}_{reasoner}`.

### Lego V1 (`v1/images/generate-async`) run types

For text-to-image (T2I), the format is `imageV5_t2i_load_{resolution}_{reasoner}`:

| Run Type | Resolution | Prompt Reasoner | Description |
|---|---|---|---|
| `imageV5_t2i_load_1MP_speed` | 1MP (~1024x1024) | speed (Qwen3) | Fast T2I at standard resolution |
| `imageV5_t2i_load_1MP_quality` | 1MP | quality (GPT-5) | High-quality T2I at standard resolution |
| `imageV5_t2i_load_1MP_budget` | 1MP | budget (Qwen3) | Budget T2I at standard resolution |
| `imageV5_t2i_load_2.4MP_speed` | 2.4MP (~1536x1536) | speed | Fast T2I at high resolution |
| `imageV5_t2i_load_4MP_speed` | 4MP (~2048x2048) | speed | Fast T2I at max resolution |
| `imageV5_t2i_load_4MP_quality` | 4MP | quality | High-quality T2I at max resolution |

For instruct-edit (IE), the format is `imageV5_ie_load_{resolution}_{reasoner}`:

| Run Type | Resolution | Prompt Reasoner | Description |
|---|---|---|---|
| `imageV5_ie_load_1MP_speed` | 1MP | speed | Fast instruct edit |
| `imageV5_ie_load_4MP_speed` | 4MP | speed | Fast instruct edit at max resolution |

Other run types (non-load-test):

| Run Type | Description |
|---|---|
| `imageV5_generate` | Integration test requests (from YAML) |
| `imageV5_instruct_edit_external` | External instruct edit integration tests |
| `imageV5_instruct_edit_internal` | Internal instruct edit integration tests |

**Resolution levels**: `1MP` (1024x1024), `2.4MP` (1536x1536), `4MP` (2048x2048)
**Prompt reasoners**: `speed`/`budget` (Qwen3, local), `quality` (GPT-5, 3P gateway)

> To find run types for other pipelines, check the `compare.py` file in the pipeline's compare directory (e.g., `models/colligo/models/compare/{version}/{endpoint}/compare.py`). Look for the `generate_inputs()` function's `match context.run_type` block.

## Components

- **[Capture Traffic](./tools/cli/capture_pipeline_traffic.py)**: Automated end-to-end capture: start server, generate traffic, upload to S3
- **[Capture](./capture/README.md)**: Intercept and save worker requests/responses during pipeline execution
- **[Data Loading](./data/README.md)**: Load and sample captured data from S3 or local storage
- **[Execution](./execution/README.md)**: Replay captured requests against worker endpoints and collect metrics
- **[Load Test Tool](./tools/cli/run_load_test.py)**: CLI tool for running load tests against workers
- **[Combinatorial Load Test](./tools/cli/run_combinatorial_load_test.py)**: Sweep worker combinations, packing, and concurrency
- **[Analyze Combinatorial Results](./tools/analysis/analyze_combinatorial_results.py)**: ILP recommendations and per-worker vs ILP analysis

## Combinatorial Load Testing

Combinatorial load testing sweeps over **worker deployment combinations** (which workers to pack together on one GPU), **replica counts**, and **concurrency levels** to find optimal GPU packing. The `combined` traffic pattern sends traffic to all workers in a combo concurrently, modelling real mixed-workload pressure.

Configs live in `configs/` (e.g. `configs/image5_lego_v1.yaml`).

```bash
# Use default config (image5_lego_v1):
python models/colligo/models/firefly/load_testing/tools/cli/run_combinatorial_load_test.py

# Use a specific config:
python models/colligo/models/firefly/load_testing/tools/cli/run_combinatorial_load_test.py \
    --config models/colligo/models/firefly/load_testing/configs/image5_lego_v1.yaml

# Dry run (print planned combinations only):
python ... --config ... --dry-run

# Re-measure VRAM (ignores cache):
python ... --config ... --rediscover
```

To analyze results (ILP recommendations, per-worker vs ILP breakdown):

Recommendations are computed by an integer linear program: for each worker, select one combo that maximizes `RPS / log(P99+1)^\lambda`, subject to each worker appearing in exactly one selected combo. Use `--lambda` to tune (0 = throughput only, 1 = default, higher = penalize latency more).

```bash
python models/colligo/models/firefly/load_testing/tools/analysis/analyze_combinatorial_results.py \
    --results-dir load_testing_output/results/combinatorial/{app_name}
```

Example output (truncated):

```
ILP-selected combos (lambda=1.0):
┌──────────────────────────────────────────┬──────────────────────────────┬───────────┬──────────────┬────────────────────────────────────────────────────────┐
│ combo_key                                │ combo                        │ total_rps │ p99_at_best  │ rps_per_worker                                         │
├──────────────────────────────────────────┼──────────────────────────────┼───────────┼──────────────┼────────────────────────────────────────────────────────┤
│ gen45_text_encoder_v1_1024x1__nsfw_…x1   │ gen45_text_encoder…×1, nsfw… │ 4.821     │ 3241.2       │ gen45_text_encoder_v1_1024: 2.91; nsfw_adobe_one: 1.91 │
│ image5_dit_instruct_mmd_aoti_fp8x1       │ image5_dit_instruct…×1       │ 1.203     │ 8820.5       │ image5_dit_instruct_mmd_aoti_fp8: 1.20                 │
│ vae_f16_legox2                           │ vae_f16_lego×2               │ 6.102     │ 1450.1       │ vae_f16_lego: 3.05                                     │
└──────────────────────────────────────────┴──────────────────────────────┴───────────┴──────────────┴────────────────────────────────────────────────────────┘

Total RPS vs ILP combo (100% = at ILP):
┌──────────────┬──────────────────────┬────────────────────────┬──────────────┐
│ packing_type │ mean_rps_vs_best_pct │ median_rps_vs_best_pct │ n_worker_runs│
├──────────────┼──────────────────────┼────────────────────────┼──────────────┤
│ mixed        │ 94.3                 │ 96.1                   │ 48           │
│ same         │ 101.2                │ 100.8                  │ 36           │
└──────────────┴──────────────────────┴────────────────────────┴──────────────┘

P99 (max) vs ILP combo (1.0 = at ILP, >1 = worse):
┌──────────────┬──────────────────────┬────────────────────────┐
│ packing_type │ mean_p99_vs_best     │ median_p99_vs_best     │
├──────────────┼──────────────────────┼────────────────────────┤
│ mixed        │ 1.08                 │ 1.04                   │
│ same         │ 0.97                 │ 0.98                   │
└──────────────┴──────────────────────┴────────────────────────┘
```

The ILP-selected combos are the **recommended deployment**. For mixed-packing combos the `mean_rps_vs_best_pct` and `p99_vs_best_ratio` rows show how packed performance compares to each worker's singleton baseline, giving confidence that packing is safe without relying on an auto-scaler.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ 1. CAPTURE PHASE (Production/Test Pipeline)                │
│                                                             │
│  Pipeline → CapturingWorkerRegistry → Workers              │
│                      ↓                                      │
│              Save to .pth files                             │
│                      ↓                                      │
│              Upload to S3 (session-based)                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 2. LOAD TEST PHASE (Isolated Worker)                       │
│                                                             │
│  S3 → DataLoader → DataSampler → LoadTestRunner            │
│                                        ↓                    │
│                                  WorkerClient               │
│                                        ↓                    │
│                              Single Worker (localhost)      │
│                                        ↓                    │
│                                  Metrics & Results          │
└─────────────────────────────────────────────────────────────┘
```

## Use Cases

- **Performance Benchmarking**: Measure worker latency and throughput under load
- **Regression Testing**: Ensure new worker versions don't degrade performance
- **Capacity Planning**: Determine optimal worker scaling parameters
- **Optimization Validation**: Test performance improvements in isolation
- **Stress Testing**: Find breaking points and resource limits

## See Also

- [Capture Guide](./capture/README.md) - How to capture worker traffic
- [Execution Guide](./execution/README.md) - How to run load tests
- [Load Test Tool](./tools/cli/run_load_test.py) - CLI tool for running load tests

