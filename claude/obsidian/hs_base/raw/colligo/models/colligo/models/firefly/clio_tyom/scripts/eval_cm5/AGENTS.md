# eval_cm5 — Bulk CM5 Training Evaluation Pipeline

Self-contained orchestration script for uploading datasets, running CM5
analysis (or populating from pre-generated parquet data), cloning Training Set
libraries, creating Custom Model libraries, invoking CM5 training, and polling
results.

## Directory layout

```
eval_cm5/
├── main.py                       # CLI entry-point and phase orchestrator
├── config.py                     # Environment, URL routing, IMS token, header helpers
├── cm_golden_datasets.yaml       # Dataset definitions (input paths, training modes)
├── training_config.yaml          # Per-dataset training payload & debug header overrides
├── results.json                  # Persisted pipeline state (upserted by dataset_id)
├── analyze_output/               # JSON + parquet outputs from the analyze phase
├── __main__.py                   # Allows `python -m eval_cm5`
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
├── .env                          # Local env vars (git-ignored); see .env.example
├── .env.example                  # Template for local environment variables
├── .env.example-quick-clone      # Minimal template for quick clone mode
├── QUICK_CLONE_USAGE.md          # Quick clone mode documentation
└── .gitignore
```

## Running the script

Run as a Python module from the repo root (after activating the dev
environment with `. m`):

```bash
. m

# Full pipeline (upload → analyze → clone → create-cm → train → poll), dry run:
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 --dry-run

# Upload + analyze only:
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 --phases upload,analyze --datasets maggie

# Upload images from parquet + populate_asml from pre-generated parquets:
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 --phases upload_asml,populate_asml --datasets yellow_girl_sally

# Upload from folder + populate_asml from pre-generated parquets (substitute for analyze):
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 --phases upload,populate_asml --datasets yellow_girl_sally

# Full pipeline using upload_asml + populate_asml instead of upload + analyze:
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 --phases upload_asml,populate_asml,clone,create-cm,train,poll

# Full pipeline using populate_asml instead of analyze:
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 --phases upload,populate_asml,clone,create-cm,train,poll

# Clone from previous upload/analyze results, then train:
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 --results results.json --phases clone,create-cm,train,poll

# Train + poll concurrently (sliding window, max 10 at a time):
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 --phases train,poll --concurrent 10

# Train + poll concurrently (unlimited, all at once — original behaviour):
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 --phases train,poll --concurrent

# Quick clone: clone datasets and create CM libraries for experimentation:
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 --quick-clone --datasets maggie

# Quick clone with dry run:
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 --quick-clone --datasets maggie --dry-run

# Use --work-dir to point at a single directory containing all config files:
python -m colligo.models.firefly.clio_tyom.scripts.eval_cm5 --work-dir /sensei-fs-3/users/afratila/SCAP/datasets/v6_analyze/results_colligo_analyze_experiment_2026_03_10 --quick-clone --datasets maggie
```

File-path defaults (`--training-config`, `--output`, `--golden-datasets`,
`--analyze-output`) all resolve relative to the script directory, so they
work regardless of CWD.  Use `--work-dir` to point at a single directory
containing `cm_golden_datasets.yaml`, `results.json`, and
`training_config.yaml` — all file-path arguments are then resolved
relative to that directory.

### Key CLI arguments

CLI arguments override the corresponding environment variable when both are
set.  Arguments without an env-var equivalent are CLI-only.

| Argument             | Env override           | Description                                                        |
|----------------------|------------------------|--------------------------------------------------------------------|
| `--work-dir`         | `CM_WORK_DIR`          | Working directory; resolves `--golden-datasets`, `--results`, `--output`, `--training-config`, `--analyze-output` relative to this directory |
| `--source-project`   | `CM_SOURCE_PROJECT`    | CC Project URN where TS libraries are created during upload        |
| `--golden-datasets`  | `CM_GOLDEN_DATASETS`   | Path to `cm_golden_datasets.yaml`                                  |
| `--results`          | `CM_RESULTS_PATH`      | Path to previous `results.json` to resume from                    |
| `--training-config`  | `CM_TRAINING_CONFIG`   | YAML with per-dataset training overrides                           |
| `--project-urn`      | `CM_TARGET_PROJECT`    | Target CC Project URN                                              |
| `--analyze-output`   | `CM_ANALYZE_OUTPUT`    | Directory for analyze JSON + parquet outputs                       |
| `--output`           | `CM_OUTPUT_PATH`       | Output path for results JSON                                       |
| `--poll-interval`    | `CM_POLL_INTERVAL`     | Seconds between training poll requests                             |
| `--poll-timeout`     | `CM_POLL_TIMEOUT`      | Max seconds to poll each training job                              |
| `--phases`           | —                      | Comma-separated phases (see below). Default excludes `upload_asml` and `populate_asml`. |
| `--datasets`         | —                      | Comma-separated list of exact dataset names to process             |
| `--filter`           | —                      | Glob pattern to filter dataset names (e.g. `maggie*`)              |
| `--git-commit`       | —                      | Git commit hash to embed in parquet output (optional)              |
| `--dry-run`          | —                      | Simulate only — no API calls                                      |
| `--force-analyze`    | —                      | Force re-analyze/re-populate all datasets, ignoring prior successes |
| `--force-train`      | —                      | Force re-training all datasets, ignoring prior successful results  |
| `--concurrent [N]`   | `CM_MAX_CONCURRENT`    | Run training+polling concurrently. Optional *N* = max parallel jobs (sliding window). Align *N* with the number of CM5 training worker replicas. Without a value: unlimited. When both train and poll phases are active, each dataset is trained then polled as a single unit; as one finishes, the next starts. |
| `--quick-clone`      | —                      | Quick clone mode: clone datasets into `CM_TARGET_PROJECT` and create CM libraries. Does **not** write to `results.json`. Uses prior clone results (no `CM_SOURCE_PROJECT` access needed). See [QUICK_CLONE_USAGE.md](QUICK_CLONE_USAGE.md). |

## Pipeline phases

1. **Upload** — Create TS libraries (with timestamp-suffixed names) and upload images from golden dataset `input_path` directories.
2. **Upload ASML** *(alternative to Upload)* — Create TS libraries and upload images referenced in the `image_path` column of the `asml_parquet_path` parquet file. Datasets without an `asml_parquet_path` are skipped. Not included in the default `--phases`; use `--phases upload_asml,...` explicitly.
3. **Analyze** — Run CM5 analyze on the freshly uploaded TS libraries (source of truth). Saves raw JSON + per-image parquet to `--analyze-output`. After each successful analyze, fetches the `cm5-ts-metadata` ACP component to include `backingShapeConsistency` and `backgroundConsistency` in the output parquet (these fields are stored by the CM5 pipeline in a separate component, not in the analyze response's `libraryUpdate`). Supports delta detection (skips datasets already successful in `results.json`) and retries up to 3 times on API/poll failure. Use `--force-analyze` to bypass delta detection.
4. **Populate ASML** *(alternative to Analyze)* — Write pre-generated SCAP captions from parquet files directly to the TS library elements and library-level metadata. Datasets must have an `asml_parquet_path` defined in `cm_golden_datasets.yaml`. Produces results in the same format as Analyze so downstream phases work interchangeably. Not included in the default `--phases`; use `--phases upload_asml,populate_asml,...` explicitly.
5. **Delete** — Delete all existing libraries from the target project. Optional; include in `--phases` when you want a clean slate before cloning.
6. **Clone** — Duplicate analyzed/populated TS libraries into the target project (requires analyze or populate_asml results).
7. **Create CM** — Create a Custom Model for each cloned TS, patching CM5 fields.
8. **Train** — Invoke the CM training endpoint for each CM.
9. **Poll** — Poll training jobs until completion or timeout.

### Data flow

```
Upload         → creates TS libraries from input_path dirs → URNs stored in results["upload"]
   OR
Upload ASML    → creates TS libraries from parquet image_path → URNs stored in results["upload"]
Analyze        → analyzes uploaded TSes → results["analyze"] + JSON/parquet in analyze_output/
                  (parquet includes backing_shape_consistency/background_consistency from cm5-ts-metadata)
   OR
Populate ASML  → writes parquet captions to TSes → results["analyze"] (same key as Analyze)
Delete         → removes existing libraries from target project → results["delete"]
Clone          → uses analyze/populate_asml results as clone source → results["clone"]
Create CM      → creates CM for each clone → results["cm"]
Train          → invokes training per CM → results["train"]
Poll           → polls each training job → results["poll"]
```

### Populate ASML phase details

The **populate_asml** phase reads pre-generated SCAP captioning parquet files
(one per dataset) and writes the data to the TS library via Melville API and
ACP content storage:

- **Per-element metadata**: Sets `firefly#cme.userData.caption`,
  `firefly#cme.userData.previousCaption`, and
  `firefly#cme.trainingData.caption` from the parquet `caption_scap` column.
  Elements are matched by image filename.

- **Library-level metadata**: Sets `classDescriptors` (derived from
  the `superclass` column), `trainingMode`, `contentType`, `conceptId`,
  and `schemaVersion` via the Melville API.  `backgroundConsistency` and
  `backingShapeConsistency` are excluded from `firefly#cme` (matching
  production CM5 behaviour) and stored in the component below instead.

- **CM5 Training Set Metadata component** (`cm5-ts-metadata`): Uploads a
  JSON component to ACP content storage containing `scapCaptions`
  (per-element structured SCAP caption dicts parsed from the parquet
  `caption_scap` column), `backingShapeConsistency`, and
  `backgroundConsistency`.  The component is registered in the library
  manifest.  This matches the storage pattern used by the production CM5
  analyze pipeline and is required for the CM5 training workflow to read
  back the metadata at train time.

Parquet files are referenced via the `asml_parquet_path` field in
`cm_golden_datasets.yaml`, pointing to files in
`/sensei-fs-3/users/afratila/SCAP/datasets/v6/`.  Datasets without an
`asml_parquet_path` are skipped with a warning.

The populate_asml phase shares delta detection and `--force-analyze` behavior
with the analyze phase.

### Upload ASML phase details

The **upload_asml** phase is an alternative to the standard **upload** phase.
Instead of scanning an `input_path` directory for images, it reads the
`image_path` column from the `asml_parquet_path` parquet file and uploads
those specific images to ACP storage.

For each dataset with an `asml_parquet_path`:
1. Loads the parquet and extracts `image_path` values (filters to `.jpg`,
   `.jpeg`, `.png`).
2. Creates a TS library in the source project.
3. Uploads each image individually to ACP storage.
4. Registers uploaded images as library elements via batch PATCH.

Results are stored under the `upload` key in `results.json`, the same as the
regular upload phase.  Downstream phases (analyze, populate_asml, clone, etc.)
consume them interchangeably.

### Quick clone mode

The ``--quick-clone`` flag provides a lightweight mode for teammates to
quickly generate CM libraries for experimentation.  It runs only two
phases — **clone** and **create-cm** — using ``CM_TARGET_PROJECT`` as
the destination.

Key differences from the full pipeline:
- Does **not** write any output to ``results.json``.
- Uses only ``CM_TARGET_PROJECT`` — no access to ``CM_SOURCE_PROJECT``
  is needed.  Clone sources are resolved from prior clone results
  (already in the target project) first, falling back to analyze results
  only if no clone results exist.
- Requires a ``--results`` file with prior clone or analyze data.
- Compatible with ``--datasets``, ``--filter``, and ``--dry-run``.

See [QUICK_CLONE_USAGE.md](QUICK_CLONE_USAGE.md) for step-by-step
usage instructions.

### Concurrent sliding-window (train + poll)

When `--concurrent N` is used and both **Train** and **Poll** phases are
active, the pipeline runs them as a single combined step.  Each dataset
goes through *train → poll* as one unit.  At most *N* datasets are
in-flight at any time.  As soon as one dataset's poll completes (or
fails), the next dataset begins training — keeping the concurrency slots
full.

Results are saved incrementally after each dataset finishes, so progress
is not lost if the process is interrupted.

When `--concurrent` is passed without a value (or `CM_MAX_CONCURRENT=0`),
all datasets run at once with no limit — equivalent to the previous
behaviour.

If only one of **Train** or **Poll** is in `--phases`, a standard
semaphore-limited concurrency is used (no combined sliding window).

### Analyze delta detection & retry

The analyze phase checks existing results (loaded from `--results`) for
datasets that already have `status: "ok"`.  Those datasets are skipped
and their previous results are carried forward.  Use `--force-analyze` to
re-analyze all datasets regardless of prior results.

Each analyze invocation (API call + polling) is retried up to 3 times on
failure, with exponential back-off between attempts (5s, 10s, 15s).

### Clone source resolution

The clone phase requires analyze or populate_asml results (from the current run
or a previous `--results` file). It uses the successfully analyzed/populated
TS library URNs as the source for cloning — no fuzzy name matching is needed
since the pipeline controls the full lifecycle from upload through
analyze/populate_asml.

## cm_golden_datasets.yaml

Dataset definitions include an optional `asml_parquet_path` field for the
upload_asml and populate_asml phases:

```yaml
datasets:
  yellow_girl_sally:
    type: Subject
    sub_type: Illustration
    input_source: folder
    input_path: /sensei-fs-3/.../raw_datasets/ASML - YellowGirlSally
    upload_training_mode: subject
    analyze_training_mode: subject
    content_type: illustration
    concept_id: sally
    asml_parquet_path: /sensei-fs-3/users/afratila/SCAP/datasets/v6/yellow_girl_sally_captioned.parquet
```

The parquet files contain columns: `image_path`, `superclass`, `caption_scap`,
`backing_shape_consistency`, `background_consistency`, `git_commit_hash`.

## results.json structure

Each section (`upload`, `analyze`, `clone`, `cm`, `train`, `poll`) is a
list of entries keyed by `dataset_id` (the golden dataset name).
The populate_asml phase writes its results under the `analyze` key so that
downstream phases consume them identically.

When a phase re-runs for a dataset that already has results, the previous
entry is moved into a `_history` array on the new entry (with a
`_replaced_at` ISO timestamp), so no data is lost.

## Environment variables

All configurable constants, file paths, and tuning parameters are set via
environment variables (loaded from `.env` by `python-dotenv`).  CLI arguments
still exist as overrides — when both are set, the CLI value takes precedence.
See `.env.example` for a complete template.

| Variable                    | Required | Description                                                        |
|-----------------------------|----------|--------------------------------------------------------------------|
| `CM_WORK_DIR`               | No       | Working directory; all file paths resolve relative to it when set   |
| `IMS_TOKEN`                 | Yes      | Pre-generated IMS bearer token                                     |
| `CM_API_KEY`                | No       | `x-api-key` header value (default: `clio-playground-web`)          |
| `CM_ENV`                    | No       | `stage` or `prod` (default: `stage`)                               |
| `CM_FIREFLY_CME_URL`        | No       | Override the Firefly CME base URL                                  |
| `CM_SOURCE_PROJECT`         | No       | CC Project URN for upload phase                                    |
| `CM_TARGET_PROJECT`         | No       | Target CC Project URN for clone/delete/create-cm                   |
| `CM_GOLDEN_DATASETS`        | No       | Path to `cm_golden_datasets.yaml`                                  |
| `CM_TRAINING_CONFIG`        | No       | Path to `training_config.yaml` (default: script dir)               |
| `CM_RESULTS_PATH`           | No       | Path to previous `results.json` to resume from                     |
| `CM_OUTPUT_PATH`            | No       | Output path for the results JSON (default: `results.json` in script dir) |
| `CM_ANALYZE_OUTPUT`         | No       | Directory for analyze JSON + parquet outputs                       |
| `CM_POLL_INTERVAL`          | No       | Seconds between training poll requests (default: `30`)             |
| `CM_POLL_TIMEOUT`           | No       | Max seconds to poll each training job (default: `7200`)            |
| `CM_MAX_CONCURRENT`         | No       | Max concurrent train+poll jobs. Unset = sequential, `0` = unlimited, positive int = sliding-window size |
| `CM_LIBRARY_NAME_PREFIX`    | No       | Prefix prepended to TS library names during upload (e.g. `v6`, `scap_test`). Empty = no prefix |
| `CM_DELAY_BETWEEN_REQUESTS` | No       | Delay in seconds between sequential API requests (default: `2`)    |
| `CM_DELAY_BETWEEN_CLONES`   | No       | Delay in seconds between clone operations (default: `5`)           |
| `CM_ANALYZE_MAX_RETRIES`    | No       | Max retry attempts per analyze invocation (default: `3`)           |
| `CM_ANALYZE_RETRY_DELAY`    | No       | Base delay in seconds for analyze retry back-off (default: `5`)    |

## Imports

All modules use fully-qualified absolute imports with the full package path
(e.g. `from colligo.models.firefly.clio_tyom.scripts.eval_cm5.config import get_token`,
`from colligo.models.firefly.clio_tyom.scripts.eval_cm5.tools.analyze import invoke_analyze`).
The `tools/__init__.py` is kept empty — no re-exports.

## Coding conventions

- Python 3.10+, strict type annotations on public functions.
- Async HTTP via `aiohttp`.
- No relative imports — all imports are absolute.
- Each `tools/*.py` module is self-contained and handles a single API operation.
- `training_config.yaml` uses a `defaults` + per-`datasets` override structure.
- Every dataset that reaches the training phase **must** have an explicit entry under the `datasets` key in `training_config.yaml`. The pipeline raises `ValueError` and aborts before any training API call if a dataset is missing its configuration.
- NEVER modify `results.json` by hand during a run; the script manages upserts.
