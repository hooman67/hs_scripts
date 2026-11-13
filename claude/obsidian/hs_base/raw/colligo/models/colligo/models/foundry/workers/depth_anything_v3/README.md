# Depth Anything V3 Worker

Depth estimation using [DA3-LARGE-1.1](https://huggingface.co/depth-anything/DA3-LARGE-1.1) (0.35B params, Apache 2.0).

- **Endpoint**: `v1/depth-anything-v3` (sync)
- **Input**: `image` (single, backward compatible) **or** `images` (1–16 views, same order as outputs). Optional `pointCloudStride` (default `2`): sample every Nth pixel when building point clouds (`1` = full resolution; larger values shrink artifacts). Optional `includeSceneExports` (default **`false`**): set **`true`** to build merged and per-view colored PLY (`scenePointCloud`, `framePointCloud`); otherwise those fields are omitted. Depth, cameras, numpy point clouds, and `consolidatedPointCloud` are always returned when applicable. Presigned GETs use `Content-Disposition` with `{storageId}.{ext}`; no separate filename hints are returned in the JSON.
- **Output**:
  - `outputs` — one object per input (same order as `images` / `image`), each with:
    - `inputImageId` — storage id of that input when the request used temp-storage ids
    - `previewImage` — 8-bit grayscale PNG depth preview (min–max normalized, quick sanity / viz)
    - `rawDepth` — float32 per-pixel depth `(H, W)` as a NumPy `.npy` blob (`numpy.load`)
    - `confidenceInDepth` — optional float32 `(H, W)` confidence; same tensor as the model’s `depth_conf` head, which upstream exposes on `Prediction.conf` in `specs.py` (not present if the head omits confidence)
    - `cameraExtrinsic` — float32 `(4, 4)` world-to-camera extrinsics (homogeneous), consistent with DA3’s decoder
    - `cameraIntrinsic` — float32 `(3, 3)` intrinsics at the processed resolution
    - `pointCloudWorld` — float32 `(P, 3)` per-view world points (`unproject_depth` + cameras; optional stride)
    - `framePointCloud` — optional per-view colored **PLY** for DCC / viewer workflows (same coordinate frame as `scenePointCloud`; binary PLY only)
  - `consolidatedPointCloud` — float32 `(P_total, 3)` concatenation of every view’s `pointCloudWorld` (same stride; multi-view fusion in numpy)
  - `scenePointCloud` — optional merged colored **PLY** for visualization (only when `includeSceneExports` is true; binary PLY only)
- **GPU**: 80 GB (H100) (it is actually much less, model is less than 1B params, we set for 80GB to get development started).
- **Multi-image**: More views in one request use more GPU memory (and CPU for PNG encoding). If you hit OOM, reduce `images` length or resolution; the hard cap is `MAX_DEPTH_INPUT_IMAGES` (16) in `types.py`.
- **API**: Typical integration: `rawDepth`, `cameraExtrinsic`, `cameraIntrinsic`, per-view `pointCloudWorld`, plus `consolidatedPointCloud`. For **PLY** point clouds (visualization, mesh tools, multi-view review), set **`includeSceneExports`: true** to get `scenePointCloud` / `framePointCloud`. Optional `confidenceInDepth` when the model exposes confidence. **Note:** optional PLY fields are standalone binary downloads; merged and per-view clouds use the same aligned coordinate frame when both are returned.

### Sample response

Shape-only example (placeholder storage ids and presigned URLs). `confidenceInDepth` is omitted when the model has no confidence head. `framePointCloud` and `scenePointCloud` appear only when `includeSceneExports` is true and export succeeds (each is a `PublicBinary` like the fields below). The canonical string `SAMPLE_RESPONSE_JSON` lives in `endpoints/depth_v3_endpoint.py`.

```json
{
  "outputs": [
    {
      "inputImageId": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
      "previewImage": {
        "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
        "presignedUrl": "https://storage.example.invalid/presigned/bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
      },
      "rawDepth": {
        "id": "cccccccc-cccc-4ccc-8ccc-cccccccccccc",
        "presignedUrl": "https://storage.example.invalid/presigned/cccccccc-cccc-4ccc-8ccc-cccccccccccc"
      },
      "confidenceInDepth": {
        "id": "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
        "presignedUrl": "https://storage.example.invalid/presigned/dddddddd-dddd-4ddd-8ddd-dddddddddddd"
      },
      "cameraExtrinsic": {
        "id": "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee",
        "presignedUrl": "https://storage.example.invalid/presigned/eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee"
      },
      "cameraIntrinsic": {
        "id": "ffffffff-ffff-4fff-8fff-ffffffffffff",
        "presignedUrl": "https://storage.example.invalid/presigned/ffffffff-ffff-4fff-8fff-ffffffffffff"
      },
      "pointCloudWorld": {
        "id": "11111111-1111-4111-8111-111111111111",
        "presignedUrl": "https://storage.example.invalid/presigned/11111111-1111-4111-8111-111111111111"
      }
    }
  ],
  "consolidatedPointCloud": {
    "id": "22222222-2222-4222-8222-222222222222",
    "presignedUrl": "https://storage.example.invalid/presigned/22222222-2222-4222-8222-222222222222"
  }
}
```

## Model Source

- **Code**: vendored from [ByteDance-Seed/depth-anything-3](https://github.com/ByteDance-Seed/depth-anything-3) (Apache 2.0) into `src/depth_anything_3/`
- **Checkpoint**: [depth-anything/DA3-LARGE-1.1](https://huggingface.co/depth-anything/DA3-LARGE-1.1) on HuggingFace, uploaded to S3 via `./m deps.upload_artifact`
- **Config**: `configs/da3-large.yaml` derived from the HF [config.json](https://huggingface.co/depth-anything/DA3-LARGE-1.1/blob/main/config.json), with `__object__` paths rewritten to colligo namespace
- **Model cards**: see the [full model card table](https://github.com/ByteDance-Seed/depth-anything-3?tab=readme-ov-file#%EF%B8%8F-model-cards) for all available DA3 variants and benchmarks

## Setup

Run from the colligo repo root:

```bash
./m sys.setup       # Configure IMS credentials (requires OKTA — run manually in terminal)
./m deps.sync       # Sync submodules + download LFS binaries (including test images)
./m deps.create     # Create unified dev environment
```

## Local Testing

Both options require configuring `colligo.dev.yaml` so the worker loads locally
instead of routing to a remote endpoint that doesn't have it.

Edit `colligo.dev.yaml` — set **both** `remote_deploy` (used by NativeClient / worker_e2e.py)
and `remote_deploy_per_spec.foundry` (used by dev_supervisor):

```yaml
remote_deploy:
  local_deploys: [depth_anything_v3]
  remote_deploys: []
  endpoint: https://gen-foundry-dev.ethos851-stage-or2.ethos.adobe.net/

remote_deploy_per_spec:
  foundry:
    local_deploys: [depth_anything_v3]
    remote_deploys: []
    endpoint: https://gen-foundry-dev.ethos851-stage-or2.ethos.adobe.net/
```

### Option 1: worker_e2e.py (direct worker validation)

Loads the worker via `NativeClient`, uploads a test image to temp storage, runs inference, and saves the output.

```bash
source .venvs/dev/bin/activate
python models/colligo/models/foundry/workers/depth_anything_v3/scripts/worker_e2e.py
```

Outputs are saved to `scripts/outputs/GasStation_depth_preview.png` and `GasStation_depth_raw.npy`.

### Benchmark: max batch size (HTTP + GPU)

With **dev_supervisor** running (`python -m colligo.rhode.commands.dev_supervisor --spec foundry`), use the endpoint benchmark (uploads once, then calls ``v1/depth-anything-v3`` with ``N`` repeated image ids and polls ``nvidia-smi`` during each request):

```bash
source .venvs/dev/bin/activate
pip install httpx   # if needed
python models/colligo/models/foundry/workers/depth_anything_v3/scripts/benchmark_depth_endpoint.py \
  --base-url http://localhost:8000 \
  --image models/colligo/models/foundry/workers/depth_anything_v3/scripts/inputs/GasStation.png \
  --max-n 16
```

Set ``COLLIGO_API_KEY`` / ``COLLIGO_BEARER_TOKEN`` if your deployment requires auth. GPU metrics reflect the machine where the script runs — use localhost or run on the worker host.

Use ``--synthetic-size 1000 1000`` to generate a 1k×1k PNG in memory (no fixture file) and sweep ``--max-n`` until HTTP errors to estimate how many 1k inputs fit per request.

For a **standalone** in-process probe (loads the checkpoint directly, no HTTP), see ``scripts/benchmark_max_batch.py``.

### Option 2: dev_supervisor (full HTTP service)

1. Start the service:

```bash
source .venvs/dev/bin/activate
python -m colligo.rhode.commands.dev_supervisor --spec foundry
```

2. Send a request (after uploading an image to get a `PublicBinary` id):

```bash
curl -X POST http://localhost:8000/v1/depth-anything-v3 \
  -H "Content-Type: application/json" \
  -d '{"image": {"id": "<uploaded-image-uuid>"}}'
```

## Test Inputs

Test images are stored as binaries via `./m lfs.sync`. On fresh checkout, run `./m deps.sync` to download them.

To add a new test image:
1. Place the file in `scripts/inputs/`
2. Run `./m lfs.sync models/colligo/models/foundry/workers/depth_anything_v3/scripts/inputs`
3. Commit the updated `scripts/inputs/.gitignore` (the manifest)
