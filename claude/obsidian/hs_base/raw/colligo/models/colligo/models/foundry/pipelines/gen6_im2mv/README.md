# Im2Mv Pipeline

Image-to-multiview generation pipeline. Generates 8 multiview images from 1-4 input images using a Shape3D diffusion model, suitable for downstream mesh reconstruction.

## Architecture

```
gen6_im2mv/                          # Pipeline package
├── Im2MvPipeline.py                 # Orchestrator (ColligoPipeline)
├── types/
│   ├── im2mv_types.py              # Im2MvPipelineRequest, Im2MvPipelineResponse
│   └── config.py                    # Im2MvPipelineConfig (BaseWorkerConfig)
├── adapters/
│   └── im2mv_adapters.py           # HTTP endpoint definition (IM2MV_ENDPOINT)
└── utils/
    └── camera_conditioning.py       # Lat-long spherical map generation

models/foundry/workers/im2mv/        # Standalone worker package
├── Im2MvWorker.py                   # Multi-GPU worker (ColligoMLModel)
├── api_adapters.py                  # API types → InferenceInput tensor conversion
├── torch_mp/
│   ├── __init__.py                  # InferenceInput dataclass
│   ├── inference.py                 # Shape3D diffusion loop (load model, run_inference)
│   └── worker.py                    # InferenceWorkerPool (torch.multiprocessing)
├── types/
│   ├── worker_api.py               # Im2MvInput, Im2MvWorkerOutput, Im2MvAdvancedParams
│   ├── config.py                    # Im2MvConfig (default_num_latents, default_shifting_factor)
│   └── endpoints.py                # Worker endpoint registration
├── checkpoints/                     # S3 artifact manifests (im2mv_v3_no_vsa.json)
├── build.py                         # deploy_worker configuration
└── colligo.yaml                     # custom_pyenv: foundry_mesh3d
```

## Pipeline Stages

### Stage 1: Preprocessing (`_preprocess_images`)

For each conditioning image (images 1-3):
1. Load bytes from storage via `load_encoded_image_from_storage_item`
2. Composite RGBA onto white background (transparent pixels become white)
3. Convert to RGB
4. Apply adaptive padding: detect non-white bounding box, crop, center on square canvas sized so the object occupies `adaptive_padding_ratio` of the canvas (default 0.8)
5. Resize to target resolution (1024x1024 for "1K") using LANCZOS interpolation

The 4th image (camera map) bypasses this pipeline — it's loaded raw at native resolution.

### Stage 2: Worker Call (`_run_multiview_generation`)

1. Primary image (image 1) → `Im2MvInput.input_image`
2. Reference images (images 2-3) → `Im2MvInput.reference_images` (max 2)
3. Camera map (image 4, if present) → `Im2MvInput.camera_map` (native resolution)
4. Prompt has `" # with camera guidance"` appended when camera map is present
5. Worker call wrapped in `asyncio.wait_for` with configurable timeout (default 600s)

### Stage 3: Output Encoding

Worker returns `[N, H, W, 3]` uint8 tensor → each view saved as RGB PNG → persisted to temp storage with presigned URLs.

## Worker Inference Pipeline

The worker runs on 2 GPUs using `torch.multiprocessing` with the `spawn` start method:

1. **Image encoding**: `api_adapters.py` converts PublicBinary → `[3, H, W]` tensor in [-1,1] range (RGBA → composite on white → normalize)
2. **Conversation building**: Primary image + references + camera map assembled as `RawImageAsset` objects in a conditional conversation
3. **VLM encoding**: Qwen VLM encoder processes text + image tokens (on GPU)
4. **VAE encoding**: Images encoded to latent space (on GPU, then offloaded)
5. **Diffusion denoising**: DiT denoiser runs `num_inference_steps` steps with Ulysses sequence parallelism across GPUs
6. **VAE decoding**: Latents decoded back to pixel space → 8-frame video tensor `[3, 8, H, W]`
7. **Output extraction**: Video frames extracted as `[N, H, W, 3]` uint8

Memory management: VLM, VAE encoder, VAE decoder, and denoiser are offloaded to CPU when not in use to fit within GPU memory.

## Request Parameters

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `images` | `list[PublicBinary]` | required (1-4) | Input images. First 3 = conditioning, 4th = camera map |
| `resolution` | `"512" \| "1K"` | `"1K"` | Output resolution (512px or 1024px) |
| `seed` | `int \| None` | `None` | Random seed. Auto-generated if None |
| `prompt` | `str \| None` | `None` | Text conditioning. Worker defaults to "high quality 3D asset" |
| `adaptive_padding_ratio` | `float [0,1]` | `0.8` | Object-to-canvas ratio. 0 = disabled |
| `camera_conditioning_enabled` | `bool` | `True` | When 4 images provided, use 4th as camera map |
| `num_inference_steps` | `int [1,100]` | `50` | Diffusion denoising steps |
| `guidance_scale` | `float [0,20]` | `7.0` | Classifier-free guidance scale |
| `enable_cutout` | `bool` | `True` | Apply DI cutout (not yet wired) |
| `save_debug_intermediates` | `bool` | `False` | Persist camera map to response for debugging |

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `view_images` | `list[PublicBinary]` | 8 generated view images as PNG |
| `view_names` | `list[str]` | Canonical name for each view index |
| `seed_used` | `int` | Actual seed used |
| `inference_time_s` | `float` | Total wall-clock time |
| `orchestration_notes` | `dict[str, str]` | Execution metadata |
| `debug_camera_map` | `PublicBinary \| None` | Camera map (when debug enabled) |

## Input Modes

### 1 image
Single image → worker generates 8 multiview outputs. The image is preprocessed (padded, resized to 1024x1024) then sent as the primary input.

### 2-3 images
Image 1 = primary, images 2-3 = reference images for multi-view conditioning. Reference images go through the same preprocessing and are passed as additional `RawImageAsset` tokens in the model's conditional conversation.

### 4 images (camera conditioning)
Images 1-3 = conditioning (as above). Image 4 = camera conditioning map. The camera map is a pre-rendered lat-long spherical image (typically 128x256 RGB) encoding camera positions as colored caps. It is:
- Loaded at native resolution (no padding, no resize, no white-compositing)
- Normalized to [-1,1] and passed as a `RawImageAsset` to the model
- Encoded by the VAE at its native resolution (producing fewer latent tokens than the 1024x1024 images)
- The prompt automatically gets `" # with camera guidance"` appended

## Camera Conditioning Map Format

The map is a lat-long projection of a sphere where each pixel represents a direction. Camera views are rendered as colored Gaussian spherical caps:
- White = anchor/primary view
- Red = 2nd view
- Green = 3rd view
- Blue = 4th view

Training uses 128x256 resolution with `cap_deg=80.0` and `sigma_deg=15.0`. The `utils/camera_conditioning.py` module provides `generate_camera_map_from_images()` for generating these maps from view names, though the pipeline currently expects the map to be pre-rendered by the client.

## Output Views

8 views following the model's training convention:

| Index | View | Used |
|-------|------|------|
| 0 | top | yes |
| 1 | — | no |
| 2 | back | yes |
| 3 | left | yes |
| 4 | front | yes |
| 5 | right | yes |
| 6 | — | no |
| 7 | bottom | yes |

## Configuration

### Pipeline Config (`Im2MvPipelineConfig`)

| Field | Default | Description |
|-------|---------|-------------|
| `mock_worker` | `False` | Return empty outputs without calling model |
| `default_resolution` | `"1K"` | Fallback resolution |
| `max_inference_time_s` | `600.0` | Timeout for worker call |

### Worker Config (`Im2MvConfig`)

| Field | Default | Description |
|-------|---------|-------------|
| `do_not_load_any_model` | `False` | Skip model loading (for debugging) |
| `default_num_latents` | `2048` | Latent token count for diffusion |
| `default_shifting_factor` | `7.0` | Noise schedule shifting factor |

## Environment

Both pipeline and worker use `custom_pyenv: foundry_mesh3d` defined at `envs/foundry/mesh3d/`. Key dependencies include `mori`, `foundry_vendored_im2gs`, `torch`, `diffusers`, `transformers`.

## Deployment

The worker is deployed with:
- 2 GPUs (78GB each) — sequence-parallel denoiser + offloaded VLM/VAE
- `concurrent_ml_threads: 1` — one request at a time
- `is_async: True` with `initial_session_ttl_s: 600`
- Model bundle: `checkpoints/im2mv_v3_no_vsa.json` (S3 fileset)

## Endpoint

- Path: `v1/im2mv/generate`
- Method: Async (poll for result)
- Operation ID: `generateIm2Mv`
- Tags: `Public`, `V2`
