# Fast Turntable Checkpoint

## Status
Complete. The `im2mv_v3_fast.json` manifest points to the materialized Colligo artifact bundle.

## Source Checkpoint
```
s3://dit-scale-up/fe-experiments/FFP-87727-dit-FFP-87737-3d_gr6_distill_64gpus_with_discriminator_8steps_from_530400-2026.05.27-15.48.32/model-checkpoints/haitongt/ckpt_step00535000/student/
```

## Colligo Artifact Location
```
s3://colligo-dev-artifacts/artifacts-v1/gr6_im2gs/8v-step535000-fast/
```

## Bundle Contents
The uploaded bundle includes:

- Root config files: `config.yaml`, `inference_config.yaml`
- DiT inference files under `dit/`, including sharded safetensors
- Materialized VAE and Qwen VLM assets under `materialized/`
- VAE sub-config under `vae/`

## Packaging Notes
The originally requested `ckpt_step00532000` prefix was not present under the experiment checkpoint listing. The bundle was exported from `ckpt_step00535000/student/`, materialized locally, and uploaded to the Colligo artifact bucket.

The export command emitted a warning about unresolved `S3_EXPERIMENT_FOLDER`, but it still created the expected inference config files and completed successfully.

**Fixes Applied (2026-06-03):**
1. **VSA disabled**: The distillation checkpoint was trained with VSA (Video Sparse Attention) enabled, which caused worker processes to crash during model loading. Fixed by updating `dit/config.yaml` in S3 to set `sparse_attention_type: default` and `vsa_sparse_attention: null`. The manifest SHA256 was updated to match the corrected config.

2. **Inference steps**: The distilled checkpoint was trained for 8-step inference (vs 50 steps for standard). Updated `Gen6Shape3dPipeline.py` to automatically use `num_inference_steps=8` when `mode="fast"` is specified, matching the training config from `3d_gr6_distill_resume_530400_with_discriminator.yaml`.

## Testing
Test with:
```json
{
  "images": [...],
  "mode": "fast",
  "pipelineStepLabel": "multiview_only",
  "seeds": [0]
}
```

The pipeline should route to `im2mv_worker_fast` instead of the standard `im2mv_worker`.
