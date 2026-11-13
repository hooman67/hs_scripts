# vLLM-Omni Pipeline (vllm_omni_v1)

## Overview

Generic image-to-image editing pipeline backed by vLLM-Omni 0.16.0. The pipeline dispatches to a configurable worker — by default **Qwen-Image-Edit-2509-Lightning** — with optional LoRA support. Adding a new model requires no new Python files; only entries in `build.py`.

## Architecture

```
vllm_omni_pipeline (ColligoPipeline)
  └── <worker_name> (VLLMOmniBaseWorker)       ← configured via colligo.dev.yaml
        └── AsyncOmni (vLLM-Omni diffusion engine)
              ├── Text encoder stage
              ├── Transformer stage  (LoRA injected here)
              └── VAE decode stage
```

Registered workers:

| Worker name | Model |
|---|---|
| `qwen_image_edit_2509_lightning` | `AdobeInternal/Qwen-Image-Edit-2509-Lightning-8steps-bf16-Merged` |
| `qwen_image_edit_2511` | `Qwen/Qwen-Image-Edit-2511` |

## Running Locally

### Start the service

```bash
. m
python -m colligo.rhode.commands.dev_supervisor --spec vllm_omni_v1
```

Or from Cursor: run the `dev_supervisor` launch configuration.

The service starts on **`http://localhost:8000`**. First startup takes ~2–3 minutes (model load + CUDA kernel compilation).

### Choose which worker to run

By default all workers in the spec start. To bring up only one worker, use `--default-replica 0` and selectively enable what you need:

```bash
python -m colligo.rhode.commands.dev_supervisor \
  --spec vllm_omni_v1 \
  --default-replica 0 \
  --replicas vllm_omni_pipeline 1 \
  --replicas qwen_image_edit_2509_lightning 1
```

### Switch the pipeline to a different worker

Add a `deployment_config` block to `colligo.dev.yaml` at the repo root:

```yaml
deployment_config:
  vllm_omni_pipeline:
    impl_model_config_dict:
      worker_name: qwen_image_edit_2511
```

Then start only that worker:

```bash
python -m colligo.rhode.commands.dev_supervisor \
  --spec vllm_omni_v1 \
  --default-replica 0 \
  --replicas vllm_omni_pipeline 1 \
  --replicas qwen_image_edit_2511 1
```

No code changes needed — as long as the worker is registered in `vllm_omni/build.py`, the pipeline routes to it automatically.

### Upload an image

```bash
IMAGE_ID=$(curl -s -X POST http://localhost:8000/v2/storage/image \
  -H "Content-Type: image/jpeg" \
  --data-binary "@input.jpg" | python3 -c "import sys,json; print(json.load(sys.stdin)['images'][0]['id'])")
```

### Send a request

```bash
curl -s -X POST http://localhost:8000/v1/vllm-omni/image-edit \
  -H "Content-Type: application/json" \
  -d "{
    \"request\": {
      \"prompt\": \"Move the camera left.\",
      \"image\": {\"id\": \"$IMAGE_ID\"},
      \"seed\": 42,
      \"height\": 1024,
      \"width\": 1024,
      \"numInferenceSteps\": 10,
      \"guidanceScale\": 7.5
    }
  }"
```

With LoRA, add `"loraName": "<adapter-name>"` to the request body (must match a key in `lora_modules` in `vllm_omni/build.py`).

### Poll for result

The endpoint is async. Grab the job ID from the response and poll:

```bash
JOB_ID="<from links.result.href>"
curl -s http://localhost:8000/jobs/result/$JOB_ID
```

`"status": "succeeded"` means done. The response contains a `presignedUrl` to download the output image.

## Request Parameters

| Field | Type | Default | Description |
|---|---|---|---|
| `prompt` | string | required | Natural language edit instruction |
| `image` | `{"id": "<uuid>"}` | required | Input image uploaded via `/v2/storage/image` |
| `seed` | int | 0 | Generation seed |
| `height` | int | 1024 | Output height |
| `width` | int | 1024 | Output width |
| `numInferenceSteps` | int | 40 | Diffusion steps — use 10 for fast iteration |
| `guidanceScale` | float | 1.0 | Classifier-free guidance scale |
| `trueCfgScale` | float | null | True CFG scale (optional) |
| `negativePrompt` | string | null | Negative prompt (optional) |
| `loraName` | string | null | LoRA adapter name |
| `loraScale` | float | 1.0 | LoRA weight scale |

## Adding a New Model

No new Python files needed. Two steps:

**1. Register the worker in `vllm_omni/build.py`:**

```python
register_vllm_omni_worker(
    name="my_new_model",
    hf_model_id="org/my-new-model",
    lora_modules={"my-lora": "org/my-lora"},  # optional
    endpoint_path="v1/vllm_omni/my_new_model",
    endpoint_operation_id="my_new_model_operation",
)
```

**2. Add it to the app in `app_vllm_omni.py`:**

```python
build.application(
    name="vllm_omni_v1",
    deployments=[..., "my_new_model"],
)
```

Then select it via `colligo.dev.yaml` as shown above.

## LoRA Setup

The **lightning LoRA** is pre-fused into the 2509 base model offline — no runtime loading needed.

Runtime LoRAs (e.g. angles LoRA `dx8152/Qwen-Edit-2509-Multiple-angles`) are served dynamically by vLLM-Omni. Keys must be converted for compatibility:
- `attn.to_out.0` → `attn.to_out` (Qwen vllm_omni uses `RowParallelLinear`, not a `ModuleList`)
- Drop `img_mod.1` / `txt_mod.1` (target `nn.Linear` which vllm_omni cannot wrap with LoRA)
- Strip `.default.` from key names (diffusers vs vllm PEFT format)

The LoRA int ID uses `stable_lora_int_id(path)` (SHA256-based) so the pre-loaded adapter is reused on every request without re-loading from disk.

## Troubleshooting

**LoRA request hangs** — the LoRA name in the request must match exactly what's in `build.py` `lora_modules`.

**Image response is empty `{}`** — the worker must upload output bytes via `save_binary_to_temp_storage_item`. Setting `PublicBinary._source` directly is not sufficient for JSON responses.

**DiffusionWorker crashes on startup (EOFError)** — LoRA safetensors contains incompatible key names. Re-run the conversion script.

**OOM** — lower `memory_gb` or `gpu_memory_utilization` in `vllm_omni/build.py`.

**Slow first request** — first inference triggers JIT compilation. Use `numInferenceSteps: 10` during development.
