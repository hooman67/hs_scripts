# IE tensor-diff recording

Out-of-tree script that produces the golden tensors consumed by
`tests/test_cm5_dit_ie_tensor_diff.py`. Lives under `scripts/` (excluded from
this package's pyenv) because it imports `foundation_exploration` (Mori),
which doesn't belong in colligo's production dep tree.

## What it produces

Per resolution under `/tmp/ie_recording/<label>/`:

- `inputs.pt` — text embeddings (the actually-DiT-fed bf16 tensors,
  captured via a forward hook), `reference_latent`, `initial_latents`, and
  every hyper-parameter the test reconstructs (`seed`,
  `num_inference_steps`, `cfg_scale_src`, `eta_src`, `ie_layerwise_settings`,
  EGG knobs).
- `output.pt` — `{"x_t": Tensor}` containing Mori's final pre-VAE-decode
  `core_loop` output. The colligo test asserts its worker produces the same
  tensor at fp32 `assert_close` defaults.

The recording runs `LegoLDMInference` end-to-end and, on the first DiT
forward, snapshots the materialized `text_embeddings` / mask the cond and
uncond paths actually receive — Mori re-encodes prompts internally with
`prompt_suffix` per-prompt, producing bf16 tensors that differ slightly from
a separate batched encoder call. Replaying those exact tensors at test time
is what lets the test bit-match.

## What the recording must match

The colligo worker test loads:
- **base**: `base_ckpt_5.0.0` = `CKPT_GEN45_T2I` from `colligo-dev-artifacts`
  (registered in `models/colligo/models/firefly/clio_tyom/workers/inference/cm5/build.py`).
- **delta**: `weights_id=".tensor_diff_cm5_maggie_gw_v2_short_prompts_2026-01-22"`,
  `weights_type=DELTA`, `model_version=V5_0_0_LORA`. Resolves via
  `TYOM_CKPT_FALLBACK_LIST[V5_0_0_LORA]` to filename `clio_tyom_v5_lora.pt`
  under `s3://tyom-assets-dev/static-weights/<weights_id>/`.

The recording script applies the same LoRA delta to the same base
checkpoint, with the canonical Mori-recipe **fp32 LoRA merge** (matching
`LoRADeltaLinear.apply_delta`). Both sides cast the merged weight to bf16
at the very end.

## Prerequisites

1. **mori-venv built against afratila's branch worktree**:
   ```bash
   git worktree add /home/colligo/colligo-mihaib origin/mihaib/cm5-gw2-dataloader-update
   cd /home/colligo/colligo-mihaib/contrib/Mori/collections/foundation_exploration/training_env
   make env  # creates /mnt/localssd/mori-venv
   ```
2. **Frozen-model weights cached**:
   ```bash
   /mnt/localssd/mori-venv/bin/python \
     /home/colligo/colligo-mihaib/contrib/Mori/collections/foundation_exploration/src/foundation_exploration/utils/cache_utils.py \
     flan_t5 flan_t5_tokenizer
   ```
3. **AWS credentials** with read access to:
   - `s3://tyom-assets-dev/static-weights/...`  (LoRA delta)
   - `s3://dit-scale-up/frozen-models/...`  (T5 cache)

   The default IAM role on a Pluto laser instance has `dit-scale-up` access
   but **not** `tyom-assets-dev` — set `AWS_ACCESS_KEY_ID` /
   `AWS_SECRET_ACCESS_KEY` from `colligo.dev.yaml:s3_config.default_profile`
   to use colligo's worker credentials.
4. **Local IE base checkpoint**:
   `/sensei-fs-3/users/mihaib/_ckpts/alpha/ckpt_step01080000_consolidated_FFP-64025-lego-FFP-64335-glow_worm_editing_prod__v2_ema_bf16.pth`

## Running

```bash
cd /home/colligo/colligo-mihaib/contrib/Mori/collections/foundation_exploration
AWS_ACCESS_KEY_ID=… AWS_SECRET_ACCESS_KEY=… AWS_DEFAULT_REGION=us-west-2 \
  IE_RES_LABEL=all \
  /mnt/localssd/mori-venv/bin/python \
  /home/colligo/colligo/models/colligo/models/firefly/clio_tyom/workers/inference/cm5/scripts/record_ie_mori_tensors.py
```

`IE_RES_LABEL=1k_square` (or any label in `RESOLUTIONS`) records a single
resolution; `all` records every resolution. After the recording finishes,
upload the per-resolution `inputs.pt` / `output.pt` to
`s3://colligo-dev-artifacts/artifacts-v1/cm5/tensor_diff/ie/<label>/` and
update the `build.s3_source(...)` blocks in
`tests/test_cm5_dit_ie_tensor_diff.py` with the new `version_id` /
`sha256`.
