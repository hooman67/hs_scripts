# Gen Upsampler Inference

## Setup

Uses the colligo dev venv which has most dependencies (torch, xformers, etc.) installed.
The inference script uses full `colligo.models.di_imaging.gen_upscaler.foundation_exploration.*`
imports, so the `models/` package root must be on PYTHONPATH. The `inference/` directory is
needed for local utility modules (`inference_utils.py`, `cliosr_utils.py`).

All `clio.*` dependencies have been migrated into `foundation_exploration/clio_core/`, a local
fork of the relevant cliocore packages. This avoids production import conflicts where `clio.*`
would resolve to the shared `contrib/AdobeDiffusion/cliocore/` instead of the gen_upscaler fork.

YAML config `target:` strings are patched at runtime in two places:

1. **`inference/inference_app.py`** — patches the main config YAML: rewrites `foundation_playground.*` to the colligo namespace and `clio.*` to `clio_core`
2. **`models/vae.py`** — patches the VAE arch config YAML loaded from disk (`config_path`), same rewrites

## Run

```bash
REPO=/home/colligo/colligo
FE=$REPO/models/colligo/models/di_imaging/gen_upscaler/foundation_exploration

export PYTHONPATH=$REPO/models:$FE/inference

$REPO/.venvs/dev/bin/python $FE/inference/inference_app.py \
    --config $FE/configs/f32_config_patch1_8node_mixres_tile_filtered_x8_masked_8k_compact_sr_upscale.yaml \
    --denoiser_pt /sensei-fs/users/abhinavve/zipir/denoiser/denoiser.pt \
    --images /sensei-fs/users/cobarnes/zipir/input_images/tier1/ \
    --out_dir /sensei-fs/users/abhinavve/zipir/inference-outputs/ \
    --resize_image --tile_inference --color_correction --steps 8
```

## PYTHONPATH breakdown

| Entry | Purpose |
|-------|---------|
| `$REPO/models` | `colligo.models.*` namespace (foundation_exploration + service code) |
| `$FE/inference` | Local modules: `inference_utils`, `cliosr_utils` |

Previously `cliocore/` subdirectories were needed on PYTHONPATH to provide `clio.*` packages.
These have been migrated to `clio_core/` under the colligo namespace, so only the two entries
above are required now.
