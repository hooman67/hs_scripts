# eval_cm5 — Bulk CM5 Training Evaluation Pipeline

Self-contained orchestration script for uploading golden datasets, running
CM5 analysis (or populating from pre-generated parquet data), cloning
Training Set (TS) libraries, creating Custom Model (CM) libraries, invoking
CM5 training, and polling results.

## Prerequisites

- Python 3.10+
- Colligo dev environment activated (`. m` from the repo root)
- A valid IMS bearer token

## Quick start

1. Activate the dev environment:

```bash
. m
```

2. Create a `.env` file inside `eval_cm5/` (git-ignored) with your token
   and working directory:

```
IMS_TOKEN=ey...
CM_WORK_DIR=/sensei-fs-3/users/afratila/SCAP/datasets/v6_analyze
```

See `.env.example` for all supported variables.

3. Run from the repo root:

```bash
# Dry-run the full pipeline (no API calls):
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 --dry-run

# Run for real:
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5
```

The script automatically loads the `.env` file from its own directory on
startup via `python-dotenv`, so there is no need to source it manually.
To use a custom env file, set `ENV_FILE=/path/to/your.env` before running
the script (the path is resolved relative to the script directory). When
`ENV_FILE` is not set, the script defaults to reading `.env` in the
`eval_cm5/` directory. Shell environment variables always take precedence
over values loaded from the env file.

### Working directory

Use `CM_WORK_DIR` (or `--work-dir`) to point at a single directory
containing the files the pipeline needs. All file-path arguments
(`--golden-datasets`, `--results`, `--output`, `--training-config`,
`--analyze-output`) are resolved relative to this directory, replacing the
need for individual path variables.

For an **end-to-end flow**, the working directory should contain:

| File                        | Purpose                                              |
|-----------------------------|------------------------------------------------------|
| `cm_golden_datasets.yaml`   | Dataset definitions (input paths, training modes)    |
| `training_config.yaml`      | Per-dataset training payload & debug header overrides |
| `results.json`              | Pipeline state — created automatically on first run  |

A sample working directory you can copy as a starting point:

```
/sensei-fs-3/users/afratila/SCAP/datasets/v6_analyze/cm5_eval_app_wd_sample
```

Copy it to your own location and adjust the `.env` to point at it:

```bash
cp -r /sensei-fs-3/users/afratila/SCAP/datasets/v6_analyze/cm5_eval_app_wd_sample /path/to/my_experiment
```

```
CM_WORK_DIR=/path/to/my_experiment
```

### Concurrency setup

When using `CM_MAX_CONCURRENT` (or `--concurrent N`), align the value with
the number of CM5 training worker replicas in your deployment. Setting it
higher than the available workers will not improve throughput and may cause
queuing or throttling.

## Pipeline phases

The pipeline has nine phases, individually selectable with `--phases`:

| Phase           | Description                                                    |
|-----------------|----------------------------------------------------------------|
| `upload`        | Create TS libraries and upload images from golden datasets     |
| `upload_asml`   | Alternative to `upload`: upload images from parquet `image_path` column |
| `analyze`       | Run CM5 analyze on uploaded TS libraries; saves JSON + parquet to `--analyze-output` |
| `populate_asml` | Alternative to `analyze`: write pre-generated SCAP captions from parquet to TS libraries |
| `delete`        | Delete all existing libraries from the target project          |
| `clone`         | Duplicate analyzed TS libraries into the target CC project     |
| `create-cm`     | Create a Custom Model for each cloned TS                       |
| `train`         | Invoke the CM training endpoint for each CM                    |
| `poll`          | Poll training jobs until completion or timeout                 |

Default phases: `upload,analyze,delete,clone,create-cm,train,poll`.
The `upload_asml` and `populate_asml` phases must be requested explicitly.

### Data flow

```
Upload         -> creates TS libraries from input_path dirs -> results["upload"]
   OR
Upload ASML    -> creates TS libraries from parquet image_path -> results["upload"]
Analyze        -> analyzes uploaded TSes -> results["analyze"] + JSON/parquet
   OR
Populate ASML  -> writes parquet captions to TSes -> results["analyze"]
Delete         -> removes existing libraries from target project -> results["delete"]
Clone          -> uses analyze results as clone source -> results["clone"]
Create CM      -> creates CM for each clone -> results["cm"]
Train          -> invokes training per CM -> results["train"]
Poll           -> polls each training job -> results["poll"]
```

## Quick clone mode

The `--quick-clone` flag provides a lightweight mode for teammates to
quickly clone datasets and create CM libraries for experimentation.

**No access to `CM_SOURCE_PROJECT` is needed.** The script re-clones from
libraries already in `CM_TARGET_PROJECT` (using prior clone results). It
does **not** write to `results.json`.

```bash
# Quick clone specific datasets:
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 \
    --quick-clone --datasets maggie

# Quick clone using a specific experiment directory:
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 \
    --quick-clone --datasets maggie \
    --work-dir /sensei-fs-3/users/afratila/SCAP/datasets/v6_analyze

# Dry run:
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 \
    --quick-clone --datasets maggie --dry-run
```

See [QUICK_CLONE_USAGE.md](QUICK_CLONE_USAGE.md) for detailed setup and
usage instructions, and `.env.example-quick-clone` for a minimal env
template.

## CLI arguments

| Argument             | Env override           | Description                                                         |
|----------------------|------------------------|---------------------------------------------------------------------|
| `--work-dir`         | `CM_WORK_DIR`          | Working directory; resolves all file paths relative to this directory |
| `--source-project`   | `CM_SOURCE_PROJECT`    | CC Project URN where TS libraries are created during upload         |
| `--project-urn`      | `CM_TARGET_PROJECT`    | Target CC Project URN                                               |
| `--golden-datasets`  | `CM_GOLDEN_DATASETS`   | Path to `cm_golden_datasets.yaml`                                   |
| `--results`          | `CM_RESULTS_PATH`      | Path to a previous `results.json` to resume from                    |
| `--training-config`  | `CM_TRAINING_CONFIG`   | YAML with per-dataset training overrides                            |
| `--analyze-output`   | `CM_ANALYZE_OUTPUT`    | Directory for analyze JSON + parquet outputs                        |
| `--output`           | `CM_OUTPUT_PATH`       | Output path for results JSON                                        |
| `--phases`           | —                      | Comma-separated phases to run (default: all except `upload_asml`, `populate_asml`) |
| `--datasets`         | —                      | Comma-separated list of exact dataset names to process              |
| `--filter`           | —                      | Glob pattern to filter dataset names (e.g. `maggie*`)               |
| `--git-commit`       | —                      | Git commit hash to embed in parquet output (optional)               |
| `--dry-run`          | —                      | Simulate only — no API calls                                        |
| `--force-analyze`    | —                      | Force re-analyze/re-populate all datasets, ignoring prior successes |
| `--force-train`      | —                      | Force re-training all datasets, ignoring prior successful results   |
| `--quick-clone`      | —                      | Quick clone mode (see above)                                        |
| `--concurrent [N]`   | `CM_MAX_CONCURRENT`    | Run training+polling concurrently (optional max parallel jobs). Align N with the number of CM5 training worker replicas. |
| `--poll-interval`    | `CM_POLL_INTERVAL`     | Seconds between poll requests (default: 30)                         |
| `--poll-timeout`     | `CM_POLL_TIMEOUT`      | Max seconds to poll each job (default: 7200)                        |

## Usage examples

```bash
# Full pipeline, dry run:
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 --dry-run

# Upload + analyze for a single dataset:
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 \
    --phases upload,analyze --datasets maggie

# Upload from parquet + populate from parquet (ASML alternative):
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 \
    --phases upload_asml,populate_asml --datasets yellow_girl_sally

# Clone from previous analyze results, then train:
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 \
    --phases clone,create-cm,train,poll

# Train concurrently (sliding window, max 10 -- align with worker replicas):
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 \
    --phases train,poll --concurrent 10

# Use --work-dir to point at an experiment directory:
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 \
    --work-dir /sensei-fs-3/users/afratila/SCAP/datasets/v6_analyze/results_colligo_analyze_experiment_2026_03_10 \
    --phases train,poll --concurrent 10
```

## Environment variables

All variables can be set in the `.env` file inside `eval_cm5/` or exported
in the shell. The `.env` file is loaded automatically on startup; shell
exports take precedence. To load a different env file, set `ENV_FILE` before
running the script (e.g. `ENV_FILE=.env.prod python -m ...`). The path is
resolved relative to the script directory. When `ENV_FILE` is not set, the
script defaults to `.env`.

| Variable                    | Required | Description                                        |
|-----------------------------|----------|----------------------------------------------------|
| `CM_WORK_DIR`               | No       | Working directory; all file paths resolve relative to it |
| `IMS_TOKEN`                 | Yes      | Pre-generated IMS bearer token                     |
| `CM_API_KEY`                | No       | `x-api-key` header value (default: `clio-playground-web`) |
| `CM_ENV`                    | No       | `stage` or `prod` (default: `stage`)               |
| `CM_FIREFLY_CME_URL`        | No       | Override the Firefly CME base URL                  |
| `CM_SOURCE_PROJECT`         | No       | CC Project URN for upload phase                    |
| `CM_TARGET_PROJECT`         | No       | Target CC Project URN for clone/delete/create-cm   |
| `CM_MAX_CONCURRENT`         | No       | Max concurrent train+poll jobs (unset=sequential, `0`=unlimited, N=sliding window). Align with CM5 training worker replicas. |
| `CM_LIBRARY_NAME_PREFIX`    | No       | Prefix prepended to TS library names during upload |
| `CM_POLL_INTERVAL`          | No       | Seconds between poll requests (default: `30`)      |
| `CM_POLL_TIMEOUT`           | No       | Max seconds to poll each job (default: `7200`)     |
| `CM_DELAY_BETWEEN_REQUESTS` | No       | Delay in seconds between API requests (default: `2`) |
| `CM_DELAY_BETWEEN_CLONES`   | No       | Delay in seconds between clone operations (default: `5`) |
| `CM_ANALYZE_MAX_RETRIES`    | No       | Max retry attempts per analyze invocation (default: `3`) |
| `CM_ANALYZE_RETRY_DELAY`    | No       | Base delay for analyze retry back-off (default: `5`) |
| `ENV_FILE`                  | No       | Custom `.env` file path (relative to script dir)   |

## Training configuration

Training parameters and debug headers are configured per dataset in
`training_config.yaml`. The file uses a `defaults` section plus per-dataset
overrides under `datasets`:

```yaml
defaults:
  payload:
    modelUrn: "urn:aaid:sc:..."
    debug:
      batchSize: 4
      steps: 1000
  debug_header:
    sweep_config:
      batch_size: 4
      num_training_steps: 1000

datasets:
  maggie:
    payload:
      trainingMode: subject
    debug_header:
      sweep_config:
        experiment_name: cm5_maggie
```

Per-dataset values are deep-merged over the defaults. Every dataset that
reaches the training phase **must** have an explicit entry under `datasets`.

## Results file and automatic resumption

Pipeline output is written to `results.json` (resolved via `CM_WORK_DIR`
or `--output`). Each section (`upload`, `analyze`, `clone`, `cm`, `train`,
`poll`) is a list of entries keyed by `dataset_id`.

The `results.json` file acts as **persistent state** across runs. When you
re-run the pipeline, it automatically detects which datasets succeeded in
previous runs and skips them — only datasets that failed or were not yet
processed are retried. This means you can safely re-run the same command
after a partial failure and the pipeline will pick up where it left off.

When a phase re-runs for a dataset that already has results, the previous
entry is moved into a `_history` array on the new entry with a
`_replaced_at` ISO timestamp, so no data is lost.

### Re-running with `--force-analyze` and `--force-train`

By default the pipeline skips datasets that already have successful results.
To override this behavior:

- `--force-analyze` — re-analyze (or re-populate) all datasets, even those
  that previously succeeded in the analyze/populate_asml phase.
- `--force-train` — re-train all datasets, even those that previously
  completed training successfully.

**Recommendation:** prefer creating a new working directory for a fresh
experiment rather than using `--force-*` flags to overwrite previous results.
This keeps prior experiment data intact and makes comparison easier. Only
use `--force-analyze` / `--force-train` when you intentionally want to
re-run specific phases within the same experiment (e.g. after changing
training parameters in `training_config.yaml`).

## Directory layout

```
eval_cm5/
├── __init__.py                   # Package marker
├── __main__.py                   # Enables `python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5`
├── main.py                       # CLI entry-point and phase orchestrator
├── config.py                     # Environment, URL routing, IMS token, header helpers
├── cm_golden_datasets.yaml       # Dataset definitions (input paths, training modes)
├── training_config.yaml          # Per-dataset training payload & debug header overrides
├── results.json                  # Persisted pipeline state (upserted by dataset_id)
├── tools/                        # One module per API operation
│   ├── __init__.py               # Package marker (no re-exports)
│   ├── create_ts.py              # create_ts_library()
│   ├── upload_images.py          # upload_images(), upload_single_image()
│   ├── update_images_metadata.py # update_images_metadata()
│   ├── analyze.py                # invoke_analyze()
│   ├── populate_from_parquet.py  # populate_ts_from_parquet()
│   ├── clone.py                  # clone_library()
│   ├── create_cm.py              # create_cm_for_ts()
│   ├── delete.py                 # delete_library()
│   ├── list_libraries.py         # list_project_libraries()
│   ├── metadata.py               # fetch/extract/patch library metadata
│   ├── train.py                  # invoke_train()
│   └── poll.py                   # check_job_status(), poll_job_status()
├── .env.example                  # Template for local environment variables
├── .env.example-quick-clone      # Minimal template for quick clone mode
├── QUICK_CLONE_USAGE.md          # Quick clone mode documentation
└── .gitignore
```
