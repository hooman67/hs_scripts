# Gen4.5 Conversational Worker — Multi-Reference Image Generation

Foundry worker for multi-reference image-to-image generation using the
Gen4.5 Conversational model (11.2B parameter DiT). Given a text prompt and
one or more reference images, generates a new image conditioned on both.

## Architecture

```
MultirefImageInput
    │
    ▼
api_adapters.build_inference_sample()
    │  - resize references to target area (preserving aspect ratio)
    │  - normalize to [-1, 1]
    │  - build conversation: [system_prompt, user_prompt, refs..., target]
    ▼
LDMInference (DiT + VAE + T5 + scheduler)
    │  - encode conversation (VAE + T5)
    │  - diffusion core loop (50 steps, EGG guidance)
    │  - decode output (VAE)
    ▼
api_adapters.create_worker_output()
    │  - extract generated images
    │  - encode to PNG
    ▼
MultirefWorkerOutput
```

### Components

- **Gen45ConvWorker.py** — Worker entry point. Loads the model, builds
  DiffusionParameters, runs inference.
- **api_adapters.py** — Converts between API types (`MultirefImageInput`)
  and inference types (`InferenceSample`). Handles image loading, resize,
  and normalization.
- **types/** — Pydantic models for the API, config, and endpoint definitions.
- **build.py** — Foundry deployment config (GPU, checkpoint). Worker is internal-only;
  a separate CPU pipeline will expose public HTTP endpoints.

### Parallel CFG (2-GPU)

When `parallel_cfg=True` in `Gen45ConvConfig`, the worker loads two copies of
the DiT — one on `cuda:0` (conditional) and one on `cuda:1` (unconditional) —
and runs them concurrently via `ConvCFGManager`. This is enabled by
monkey-patching `get_velocity_predictions` on the `ldm_inference` module so
positive and unconditional passes are dispatched to separate GPUs and joined
before the guidance step. Requires a 2-GPU instance (e.g. 2x A100-80G).

### Model

The model is assembled manually from four components:

1. **DiT** (11.2B params) — `ConversationalGen45Model`, loaded from sharded
   safetensors exported from DCP training checkpoints.
2. **VAE** — Encodes/decodes images to/from latent space (spatial downsample 16x).
3. **T5** — Text encoder for prompts and system prompts.
4. **Scheduler** — DDIM-based solver with per-asset timestep scheduling.

### Checkpoints

Four model variants are deployed, each as a separate worker:

| Worker name | Checkpoint file | Weights | Steps | Notes |
|---|---|---|---|---|
| `GEN45_CONV_TCCC_MULTIREF` | `gen45conv_tccc_step1089000_nonema.json` | non-EMA step 1089000 | 50 | 2-GPU parallel CFG |
| `GEN45_CONV_HUMAIN_T2I` | `gen45conv_humain_step1026000_dynamic_neg.json` | non-EMA step 1026000 | 50 | Dynamic negative prompt, 2-GPU |
| `GEN45_CONV_THD` | `gen45conv_thd_step1088000_nonema.json` | non-EMA step 1088000 | 50 | T2I + gen_edit, 2-GPU |
| `GEN45_CONV_VMM_8STEP` | `gen45conv_vmm_8step_glow_worm.json` | EMA step 1084600 | 8 | Distilled, public HTTP endpoint |

Non-EMA weights (`model.denoiser.*`) are exported by default. EMA weights use
`--use-ema` which targets `ema.*` only.

## API

### Endpoint

The worker is internal-only (no public HTTP endpoints). Will be integrated into Lego
Pipeline later.

### Request

```json
{
    "prompt": "Replace the bottle in the scene with...",
    "neg_prompt": "<instruction> Generate a different, low-quality...",
    "reference_images": [{"id": "uuid-1"}, {"id": "uuid-2"}],
    "width": 1024,
    "height": 1024,
    "seed": 333,
    "num_assets": 2,
    "num_inference_steps": 50,
    "cfg_scale": 5.0
}
```

- `width`/`height`: Output dimensions. Must account for aspect ratio — the
  training pipeline uses `round_size_with_aspect_ratio(1024, 1024, ar)` to
  compute actual dimensions from a base 1024x1024 and per-item aspect ratio.
- `num_assets`: Number of images to generate (different seeds). Note: batch
  size affects DiT sequence balancing, so `num_assets=2, seed=333` produces
  different results than `num_assets=1, seed=334`.

### Response

```json
{
    "generations": [
        {"seed": 333, "asset": {"id": "..."}, "width": 1024, "height": 1024},
        {"seed": 334, "asset": {"id": "..."}, "width": 1024, "height": 1024}
    ]
}
```

## Scripts

| Script | Level | Purpose |
|--------|-------|---------|
| `scripts/compare_utils.py` | shared | Tensor/conversation diff helpers; training YAML param loader |
| `scripts/verify_model.py` | 1 — model | Direct inference (no SDK); `--compare` for training-path parity |
| `scripts/verify_worker.py` | 2 — worker | NativeClient SDK test; any worker via `--worker-name` |
| `scripts/verify_endpoint.py` | 3 — endpoint | HTTP generate-async test; any model via `--foundry-model-id` |
| `scripts/package.py` | — | Export/materialize/upload subcommands (individual steps) |
| `scripts/package_workflow.py` | — | Full packaging orchestration: export → materialize → upload |

### Packaging a new checkpoint

`package_workflow.py` runs the full pipeline in one command. It handles credential
isolation automatically: training-bucket credentials (`AWS_ACCESS_KEY_ID` etc.) are
used for the export step, then stripped before materialize and upload so the default
IAM role (dit-scale-up) takes over.

```bash
source .venvs/foundry_gen45_conv/bin/activate

# Get temporary credentials from https://foundry-aws-corp.adobe.io/
export AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=... AWS_SESSION_TOKEN=...

python scripts/package_workflow.py \
    --checkpoint s3://<bucket>/.../<ckpt_step0XXXXXXX>/ \
    --config <path/to/training_config.yaml> \
    --output /mnt/localssd/<output_dir> \
    --name <checkpoint_name> \
    [--use-ema]            # add only for distilled/VMM checkpoints; non-EMA is the default
```

After completion:
1. Manifest is written to `scripts/outputs/<name>/artifacts.json`
2. Copy it to `checkpoints/<name>.json`
3. Add a `_deploy_gen45_conv_worker(...)` entry in `build.py`

Use `--skip-export` or `--skip-materialize` to resume a partial run without re-doing
completed steps. Run with `--help` for all options.

**EMA vs non-EMA:** Non-EMA is the default and correct for most production checkpoints
(TCCC, THD, HuMAIn). Pass `--use-ema` only for distilled checkpoints (e.g. VMM 8-step).

## Development

```bash
# Activate the foundry_gen45_conv environment
source .venvs/foundry_gen45_conv/bin/activate

# Level 1 — direct model inference (requires model on disk)
python scripts/verify_model.py \
    --model-path /mnt/localssd/gen45conv_export/<name> \
    --prompt "..." --ref-images img1.jpg img2.jpg

# Level 1 — with training-path parity check
python scripts/verify_model.py \
    --model-path /mnt/localssd/gen45conv_export/<name> \
    --config path/to/training_config.yaml \
    --prompt "..." --ref-images img1.jpg img2.jpg --compare

# Level 2 — NativeClient worker test
python scripts/verify_worker.py \
    --worker-name gen45_conv_tccc_multiref_worker \
    --prompt "..." --ref-images img1.jpg img2.jpg

# Level 3 — HTTP endpoint test (local service must be running)
python scripts/verify_endpoint.py \
    --token <x-user-token> --foundry-model-id thd \
    --eval-json /mnt/localssd/thd_multiref_eval_1024px.json

# Run via dev_supervisor
python -m colligo.rhode.commands.dev_supervisor --spec foundry  # with dev env activated
```

See [NOTES.md](NOTES.md) for technical details on inference parameters,
image preprocessing, and bit-identical verification.

Historical docs (may be out of date) are in [`docs/`](docs/).
