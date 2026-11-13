# CM5 Batch Dataset Pipeline

Batch tooling for uploading evaluation datasets to Melville and running CM5 analyze to produce parquet outputs. This is the ML-side evaluation harness — it drives the services-side CM5 analyze endpoint externally.

## Architecture

```
batch_analyze.py          Orchestrator: reads datasets.yaml, detects deltas via manifest, runs upload+analyze
├── upload_asml_dataset.py   Reads a .snappy/.parquet file or image folder and delegates to create_dataset_upload_images
│   └── utils/api_helper.py  All Melville API operations (TyomApiHelper + create_dataset_upload_images)
│       └── utils/http.py    Low-level HTTP with retry (urllib-based, used by all Melville calls)
│       └── utils/config.py  TyomConfig singleton: URL routing per environment/service
├── run_cm5_analyze.py       Calls the /v2/images/cm_analyze endpoint (httpx-based), polls async result, writes parquet
├── compare_outputs.py       Standalone: comparison engine (compare_dataset, format_report, format_summary)
└── compare_runs.py          Standalone: compares models-team parquets (from datasets.yaml) vs pipeline parquets (from manifest.json)
```

## Pipeline Flow

### 1. Delta Detection
`batch_analyze.py` loads `datasets.yaml` and a persistent `manifest.json` from the output directory. For each dataset it computes an `Action`:

| Condition | Action | Behavior |
|---|---|---|
| No manifest entry | `CREATE` | Upload + analyze |
| Config hash changed | `UPDATE` | Delete old library, re-upload + analyze |
| `--force` flag | `UPDATE`/`CREATE` | Force re-processing |
| Status `failed` | `RETRY` | Delete old library, re-upload + analyze |
| Status `uploaded` | `ANALYZE_ONLY` | Skip upload, run analyze only |
| Status `completed` | `SKIP` | No-op |

### 2. Upload (CREATE / UPDATE / RETRY)
`upload_asml_dataset.upload_dataset()` → `api_helper.create_dataset_upload_images()`:
0. If `input_path` is a directory, scans for image files (`.png`, `.jpg`, `.jpeg`, `.webp`) and builds a DataFrame; otherwise reads the parquet/snappy file
1. Resolves or creates a Melville **project** via `TyomApiHelper.get_or_create_project()`
2. Creates a **training set** (library) via `create_training_set()` — returns a `library_urn`
3. For each image in the parquet DataFrame:
   - Uploads image binary to cloud storage via `upload_image()` (uses block upload for files > 10 MB)
   - Adds image to training set via `add_image_to_training_set()` (PATCH with element metadata)
4. Fetches final training set metadata to build `image_path_to_image_id` mapping
5. Returns `dataset_info` dict: `{dataset_library_name, dataset_urn, n_images, image_path_to_image_id}`

If image uploads fail partway, `DatasetUploadError` is raised with partial `dataset_info` (including the library URN) so the manifest can track the created library for later cleanup.

### 3. Analyze
`run_cm5_analyze.run_analyze()`:
1. Builds payload with `modelUrn` = dataset_urn and debug flags (training mode, content type, deterministic)
2. POSTs to `/v2/images/cm_analyze` on the Tyom host — returns an async job
3. Polls the async result link every 5s until `links` key disappears from the response
4. Parses `libraryUpdate` (class descriptors, background/backing shape consistency) and `imageUpdates` (per-image SCAP captions)
5. Writes output to `<dataset_name>.parquet`

### 4. Manifest Update
After each step (upload, analyze), `batch_analyze.py` updates `manifest.json` with:
- `status`: `uploaded` → `completed` (or `failed` on error)
- `dataset_urn`, `dataset_name`, `dataset_info`, `config_hash`, timestamps
- `output_parquet_path` after successful analyze

## HTTP Layers

There are **two separate HTTP stacks**:

### urllib (Melville APIs) — `utils/http.py`
- `make_http_request()` handles all Melville calls: training set CRUD, image upload, project management
- Returns `HttpResponse(status_code, text, headers)` — does **not** raise on HTTP errors
- Callers must check `status_code` and raise explicitly on failure
- Retries 3x with exponential backoff (1s, 2s, 4s) on transient errors (429, 500, 502, 503, 504) and connection failures

### httpx (Analyze API) — `run_cm5_analyze.py`
- `call_cm5_analyze()` POSTs to the analyze endpoint with retry (3x, exponential backoff)
- `poll_async_result()` polls via `_poll_request_with_retry()` — each individual poll has its own retry loop
- Uses `raise_for_status()` — raises `httpx.HTTPStatusError` on non-retryable failures

## Configuration

### TyomConfig (`utils/config.py`)
Singleton with URL mappings per service and environment:

| Service | Purpose |
|---|---|
| `melvilleTrainingSet` | Training set (library) CRUD — `/api/v1/libraries` |
| `melvilleCustomModel` | Custom model CRUD — `/api/v1/custom-models` |
| `storage` | Cloud storage — `platform-cs-edge-{region}.adobe.io` (region-templated) |
| `projects` | CC Projects API — `/api/v3/projects` |
| `external` / `corp` | Tyom service endpoints (auto-detected via `ENDPOINT_TYPE` env var) |

### Environment Variables
| Variable | Required | Purpose |
|---|---|---|
| `IMS_TOKEN` | Yes | Adobe IMS bearer token for all API calls |
| `ENDPOINT_TYPE` | No | `external` (Pluto/GitHub Actions) or `corp` (VPN); auto-detected if unset |
| `CUSTOM_BASE_URL` | No | Override all URL selection logic |

### datasets.yaml Schema
```yaml
datasets:
  <name>:
    type: Subject | Style | Icon
    sub_type: Photorealistic | Illustration
    input_path: /path/to/dataset.snappy   # or /path/to/image/folder
    input_source: parquet | folder         # optional, default "parquet"
    upload_training_mode: subject | style | iconography
    analyze_training_mode: subject | style | iconography
    content_type: photo | illustration | vector
    concept_id: <uuid>  # required for subject mode
```

When `input_source` is `folder`, `input_path` points to a directory on sensei-fs containing image files (`.png`, `.jpg`, `.jpeg`, `.webp`). The upload pipeline scans the folder and builds the image list automatically instead of reading from a parquet.

## Key Conventions

### Error Handling
- `make_http_request` does NOT raise — always check `response.status_code` before accessing response fields
- `DatasetUploadError` carries partial `dataset_info` with the library URN for manifest tracking
- `batch_analyze.run_batch()` catches all exceptions per-dataset and continues to the next; failures are logged and written to the manifest

### Training Mode Mapping
Upload and analyze both use the training mode as-is — no remapping is performed:
- **Iconography**: passed directly to Melville as `iconography`
- **Subject**: requires `concept_id` (validated in `create_training_set`)
- **Style**: `concept_id` is cleared to empty string

### Image Upload
- Max 40 images per dataset (hard limit in `create_dataset_upload_images`)
- Images must be `.png`, `.jpg`, `.jpeg`, or `.webp`
- Large files (> 10 MB) use 3-step block upload: init → transfer chunks to S3 → finalize
- Images exceeding `MAX_IMAGE_SIZE_BYTES` (10 MB) are resized via PIL before upload
- **Actual image metadata** (content type, width, height, content length) is read via PIL and passed to both the storage upload and the training set element registration. Content type is auto-detected from the file extension (see `CONTENT_TYPES` mapping). This matches the approach in `cm-agentic-automated-tests/tools/api/upload_images.py`.

### CLI
```bash
# Batch analyze
python -m colligo.models.firefly.clio_tyom.scripts.cm5.batch_analyze \
    --datasets /path/to/datasets.yaml \
    --output-dir /path/to/output \
    [--parent-project-name cm5-datasets] \
    [--environment stage] \
    [--dry-run] \
    [--force] \
    [--filter 'maggie*'] \
    [--deterministic]

# Compare models-team parquets vs pipeline analyze parquets
python -m colligo.models.firefly.clio_tyom.scripts.cm5.compare_runs \
    --datasets /path/to/datasets.yaml \
    --output-dir /path/to/batch_analyze_output \
    [--filter 'baptist*'] \
    [--report-dir ./comparison_reports] \
    [--verbose] \
    [--max-mismatches 5]
```
