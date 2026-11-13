# Data Capture Guide

This guide explains how to capture worker request/response data for load testing.

## Overview

The data capture utility intercepts worker calls during pipeline execution and saves the request/response pairs to disk in `.pth` format using a **rolling file strategy**:

- **Accumulates entries in memory** and writes one `.pth` file per batch
- **Rolls over** to a new file every N entries (default 5000; set `COLLIGO_CAPTURE_MAX_ENTRIES_PER_FILE` to capture fewer per file)
- **Uploads to S3** after 2 minutes of no new requests
- **Writes to disk on shutdown** so files can be uploaded on next run
- **Cleans up local files** after successful upload to save disk space

Captured data is uploaded to S3 bucket `colligo-comparison-results` under `captured_data/{spec_name}/{session_id}/{worker_name}/`, where `spec_name` is the deploy name (e.g., `lego_v1`) and `session_id` is the value of `COLLIGO_CAPTURE_SESSION_ID` (you choose it when starting the pipeline, e.g., `my-session-20260227` or `20260228-1709123456`).

## Benefits

- **No GPU over-provisioning**: Test individual workers without running the entire pipeline
- **Realistic data**: Use actual production/test traffic patterns
- **Easy benchmarking**: Test any component independently
- **Automatic S3 backup**: No manual file management needed
- **Disk space efficient**: Files are automatically cleaned up after upload

## Usage Example: Lego-v1 Pipeline

### Step 1: Decorate the Pipeline

Add the `@setup_capturing()` decorator to your pipeline's `load()` method (e.g., `ImageV5Pipeline.py`):

```python
from colligo.models.firefly.load_testing.capture import setup_capturing

class ImageV5Pipeline(ColligoPipeline[ImageV5Config]):
    @setup_capturing()
    async def load(self) -> None:
        # ... existing initialization code ...
```

**This decorator is required** — without it, the capture script's env vars (`COLLIGO_CAPTURE_SESSION_ID`, etc.) have no effect and zero data is captured. The decorator is a no-op when `COLLIGO_CAPTURE_SESSION_ID` is not set, so it's safe to leave in production code.

The `@setup_capturing()` decorator handles:
- Resolving the spec name (e.g., `lego_v1`) from the pipeline class for the S3 path
- Checking the `COLLIGO_CAPTURE_SESSION_ID` environment variable (when set, capturing is enabled and the value is the session ID)
- Using `COLLIGO_CAPTURE_MAX_ENTRIES_PER_FILE` to control rollover (default 5000; use e.g. 100 to capture smaller batches)
- Setting up the `CapturingWorkerRegistry` wrapper with rolling file capture
- Using local directory `./captured_data` for temporary storage
- Starting background task that uploads to S3 after 2 minutes of idle
- Writing pending entries to disk on shutdown for later upload
- Logging the setup status

**Tip**: When the pipeline starts, search for the log message `"CapturingWorkerRegistry initialized:"` to see the exact S3 path. When data is uploaded to S3, look for the 📤 emoji in logs to confirm.

### Step 2: Start the Pipeline

Run your pipeline and enable capturing by setting `COLLIGO_CAPTURE_SESSION_ID` (the value becomes your session ID / captured data version):

```bash
export COLLIGO_CAPTURE_SESSION_ID=my-session-20260227

# Optional: capture smaller batches (default 5000). E.g. 100 entries per file = faster rollover to disk.
# Useful when you want a specific count without waiting for the default 5000.
export COLLIGO_CAPTURE_MAX_ENTRIES_PER_FILE=100

# Example: Run lego_v1 pipeline
python -m colligo.rhode.commands.dev_supervisor \
    --spec lego_v1
```

The pipeline will automatically capture all worker requests/responses and upload them to S3. Use the same session ID in `run_load_test.py` when running load tests.

### Step 3: Send Traffic

Send requests to the running pipeline (e.g., via curl or the example scripts in `tools/`).

### Step 4: Access Uploaded Data from S3

Files are automatically uploaded to S3 after 2 minutes of idle and/or when rolling over to a new file. Each capture session creates a unique directory using the user-specified session ID.

**S3 path is deterministic** when you set `COLLIGO_CAPTURE_SESSION_ID` before starting the pipeline. You don't need to search logs — use the same spec name and session ID in `run_load_test.py`:

```bash
python models/colligo/models/firefly/load_testing/tools/cli/run_load_test.py \
    --worker gen45_text_encoder_v1_1024 \
    --spec-name lego_v1 \
    --capture-session-id my-session-20260227
```

To confirm data was uploaded, search logs for 📤 emoji.

**Then access the data:**
```bash
# List all capture sessions for a spec
aws s3 ls s3://colligo-comparison-results/captured_data/lego_v1/ --profile firefly-s3-developer

# List captured files for a specific session and worker
aws s3 ls s3://colligo-comparison-results/captured_data/lego_v1/20260228-1709123456/image5_dit_instruct_mmd_aoti_fp8/ --profile firefly-s3-developer

# Download a specific capture file
aws s3 cp s3://colligo-comparison-results/captured_data/lego_v1/20260228-1709123456/image5_dit_instruct_mmd_aoti_fp8/capture_1709123456789.pth ./ --profile firefly-s3-developer

# Download all files for a specific session and worker
aws s3 sync s3://colligo-comparison-results/captured_data/lego_v1/20260228-1709123456/image5_dit_instruct_mmd_aoti_fp8/ ./local_data/ --profile firefly-s3-developer

# Download all files for a specific session (all workers)
aws s3 sync s3://colligo-comparison-results/captured_data/lego_v1/20260228-1709123456/ ./local_data/ --profile firefly-s3-developer
```

**Note**:
- The S3 bucket `colligo-comparison-results` is the same bucket used by the PIPA comparison tool, so everyone with PIPA access can access the load testing data.
- Use `--profile firefly-s3-developer` to authenticate with the correct AWS credentials.

## Data Format

Each `.pth` file contains a **list** of captured request/response pairs:
```python
[
    {
        "pipeline_name": str,         # Spec name for S3 path (e.g., "lego_v1")
        "worker_name": str,           # Worker deployment name
        "request": BaseModel,         # Pydantic model object (preserves Tensors)
        "response": BaseModel,        # Pydantic model object (preserves Tensors)
        "request_type": str,          # Fully qualified request class name
        "response_type": str,         # Fully qualified response class name
        "timestamp": int,             # Unix timestamp in milliseconds
        "request_id": str             # Unique request identifier
    },
    # ... more entries appended to the same file
]
```

**File Rotation**: A new file is created every 5000 entries, or after 2 minutes of idle.

## S3 Structure

```
s3://colligo-comparison-results/
└── captured_data/
    └── {spec_name}/                 # e.g., lego_v1 (deploy/spec name)
        └── {session_id}/             # Value of COLLIGO_CAPTURE_SESSION_ID
            └── {worker_name}/        # e.g., image5_dit_instruct_mmd_aoti_fp8
                ├── capture_1709123456789.pth
                └── ...
```

**Example**:
```
s3://colligo-comparison-results/captured_data/lego_v1/{session_id}/{worker_name}/capture_1709123456789.pth
```

This structure organizes data by both pipeline and worker, preventing collisions when multiple workers run in the same pipeline.

## Onboarding a New Service for Traffic Capture

The capture script uses [Locust](https://locust.io/) to generate traffic through the pipeline.  Locust supports **any pipeline registered in `gold_standards.yaml`** — currently ~105 pipelines across v1/v2/v3 (images, audio, video, 3D, masking, etc.).  The `--pipeline` arg in `ColligoLoadTest.py` is dynamically populated from that YAML, so there's no hardcoded list.

A pipeline becomes Locust-compatible (and therefore capturable) when it has a `compare_info` object **and** the `@setup_capturing()` decorator on its `load()` method.  The steps:

### 0. Decorate the pipeline's `load()` method

Add `@setup_capturing()` to the pipeline class (see Step 1 above).  Without this, the capture script sets env vars but the `CapturingWorkerRegistry` is never installed — traffic flows through but nothing is captured.

```python
from colligo.models.firefly.load_testing.capture import setup_capturing

class MyPipeline(ColligoPipeline[MyConfig]):
    @setup_capturing()
    async def load(self) -> None:
        ...
```

### 1. Create the compare module

Create `models/colligo/models/compare/{api_path}/compare.py` with:

```python
from colligo.models.compare.common.request import CompareInfo

compare_info = CompareInfo(
    generate_inputs=...,    # async fn -> list[CompareInput] (test payloads)
    convert_response=...,   # async fn -> CompareOutput (parse API response)
    compare_outputs=...,    # fn -> ComparisonResult (diff baseline vs actual)
    load_outputs=...,       # fn -> CompareOutput (load saved outputs from disk)
)
```

### 2. Add test input YAML

Create the request YAML files that `generate_inputs()` loads (or generate programmatically like the `imageV5_t2i_load_*` patterns that produce 10k synthetic requests from `ResolutionLevel` x `PromptReasoner` combinations).

### 3. Register in `gold_standards.yaml`

Add an entry in `models/colligo/models/compare/common/gold_standards.yaml` with the pipeline path.  This is what makes it show up in Locust's `--pipeline` choices:

```yaml
- pipeline: v1/your-service/your-endpoint
  latest_run: some_run_id
```

### 4. (Optional) Custom Locust class

If the default `ColligoLoadTest` flow (POST -> poll for async, or POST -> check response for sync) doesn't match your service, set `load_test_module` in `CompareInfo` to point to a custom Locust class:

```python
compare_info = CompareInfo(
    load_test_module="colligo.models.compare.v1.your_service.load_test",
    generate_inputs=...,
    convert_response=...,
    compare_outputs=...,
    load_outputs=...,
)
```

### 5. Update capture script config

After completing steps 1-3, run `--refresh-config` to pick up the new spec's run types automatically:

```bash
python models/colligo/models/firefly/load_testing/tools/cli/capture_pipeline_traffic.py \
    --refresh-config
```

This parses the new `compare.py`'s `generate_inputs()` match/case block via AST and adds all discovered run types to `spec_config.yaml`.

### Key files

| File | Purpose |
|------|---------|
| `models/colligo/models/compare/locust/ColligoLoadTest.py` | Default Locust test class |
| `models/colligo/models/compare/common/gold_standards.yaml` | Pipeline registry (populates `--pipeline` choices) |
| `models/colligo/models/compare/common/request.py` | `CompareInfo` type definition |
| `models/colligo/models/compare/{api_path}/compare.py` | Per-pipeline test input generation + comparison logic |
