# gr6_conv_pano — Text-to-Panorama Foundry Pipeline

End-to-end text-to-equirectangular-panorama pipeline built on
`Gen6ConvDiTWorker.GR6_CONV_PANO_DIT_WORKER` (deploy `gr6_conv_pano_dit_worker`). Accepts a text prompt and returns a
PNG-encoded panoramic image (default 1024 × 512, 2:1 equirectangular).

---

## Architecture

```
Gr6ConvPanoPipeline (ColligoPipeline)
  │
  ├── [parallel] QwenWorker          gr6_conv_qwen_worker       
  │               Qwen3-VL-8B text encoder
  │               encode_conversational([[RawTextAsset(prompt)]]) → PipelineEncodedTextAsset
  │
  ├── GR6_CONV_PANO_DIT_WORKER       (foundry DiT deploy, same model as gen6_conv pano)   
  │               DiffusionTransformerModel (ConversationalGen6Model)
  │               DiffusionTransformerRequest → DiffusionTransformerResponse
  │
  └── MoriVAEWorker                  gr6_conv_mori_vae_worker   
                  MoriVAE 3DVAE f16t4c48_wan decoder
                  PipelineEncodedImageAsset [48,1,H_lat,W_lat] → Tensor [3,H,W]
```

### Data flow

1. **QwenWorker** (×2 in parallel): encodes `prompt` and `negative_prompt`
   using `QwenVLEncoder.encode_conversational()` with the `text_to_image`
   system prompt from `pano_specialist.yaml`.
2. **`build_empty_image_slot()`**: creates an unnoised zero latent slot
   (`[48, 1, H//16, W//16]`, `is_equirectangular=True`, `diffusible=True`).
3. **`build_diffusion_request()`**: wraps the two text assets and the image slot
   into a `DiffusionTransformerRequest`.
4. **`DiffusionTransformerExecutor`**: calls the existing
   ``Gen6ConvDiTWorker.GR6_CONV_PANO_DIT_WORKER`` 
5. **`extract_image_latent()`**: pulls the denoised `PipelineEncodedImageAsset`
   from the last position in the output conversation.
6. **MoriVAEWorker**: reshapes latent to `(1, 1, 48, H_lat, W_lat)` and calls
   `MoriVAE.decode(apply_mean_std=True)` → `[3, H, W]` pixels in `[0, 1]`.
7. **NSFW check** (`check_image_nsfw`) → PNG encode → `Gr6ConvPanoResponse`.

---

## GPU requirements

| Worker | Model | GPU memory |
|--------|-------|-----------|
| `gr6_conv_qwen_worker` | Qwen3-VL-8B | ~20 GB |
| `gr6_conv_pano_dit_worker` | ConversationalGen6Model DiT (foundry deploy) | ~80 GB |
| `gr6_conv_mori_vae_worker` | MoriVAE 3DVAE f16t4c48_wan | ~10 GB |

---

## Key files

| File | Purpose |
|------|---------|
| `build.py` | Deploy all workers + pipeline |
| `gr6_conv/configs/pano_specialist.yaml` | Foundry-owned DiT training YAML (align with firefly `gen6_conv` copy when it changes) |
| `colligo.yaml` | Package deps (pyenv: `foundry_gr6_conv`) |
| `QwenWorker.py` | Qwen3-VL-8B text encoder worker |
| `MoriVAEWorker.py` | MoriVAE decoder worker |
| `Gr6ConvPanoPipeline.py` | Pipeline orchestration |
| `api_adapters.py` | Image slot construction + request/response helpers |
| `types/worker_api.py` | All request/response/config/executor types |
| `checkpoints/gr6_conv_pano_v1.json` | Checkpoint manifest placeholder |

---

## Latent format

- Latent channels: **48** (`DEFAULT_MODEL_CHANNELS_LATENT` from `gen6_conv/types/__init__.py`)
- Spatial factor: **16** (f16 VAE)
- Default output: **1024 × 512** pixels → **64 × 32** latent grid
- `is_equirectangular=True` triggers equirectangular RoPE in the DiT

---

## Checkpoint preparation (before deployment)

The Qwen and MoriVAE checkpoints are currently referenced as training-path
S3 placeholders in `build.py`. Before deploying to production:

1. **Qwen3-VL-8B**: Materialise from
   `s3://dit-scale-up/frozen-models/model_weights/qwen_3_vl_8b/...` and
   upload as a zip archive to `s3://colligo-dev-artifacts/artifacts-v1/gen6_conv_pano/`.

2. **MoriVAE**: Materialise from
   `s3://dit-scale-up/sensei-fs/users/zzhang/.../ckpt_step00513000/` and
   upload similarly (must include `configs/vae/inference_3dvae_f16t4c48_wan.yaml`).

3. Update `build.py` `QWEN_DIR` and `MORI_VAE_DIR` with the correct `key`,
   `version_id`, and `sha256`.

---

## Running tests

```bash
pytest models/colligo/models/foundry/workers/gr6_conv_pano/tests/

# Lint
./m lint --paths models/colligo/models/foundry/workers/gr6_conv_pano/
```
