---
type: concept
title: GR6 Text-to-Video Inference
tags: [gr6, inference, t2v, mori, pluto, genrender6, morictl]
created: 2026-07-07
updated: 2026-07-07
sources: ["[[raw/hs_scripts/claude/obsidian/GR6_T2V_HANDOFF.md]]", "[[raw/colligo/mori/collections/foundation_exploration/scripts/agent/running_inference.md]]", "[[raw/colligo/mori/collections/foundation_exploration/scripts/agent/config_system.md]]", "[[raw/colligo/mori/collections/foundation_exploration/scripts/agent/environment_setup.md]]"]
---

# GR6 Text-to-Video Inference

Running inference on the GR6 580k "Lite" checkpoint for **text-to-video (T2V)** generation on [[wiki/entities/pluto|Pluto]]. This page is the canonical reference for submitting and monitoring GR6 T2V eval runs; supersedes the handoff document.

> [!note] Scope
> This covers config-based inference via `morictl launch` (from a CPU dev box or laptop), not exported inference (local GPU torchrun). For I2V (image-to-video), the config recipe is nearly identical; swap `t2v_*` dataset entries for `i2v_*` and add frame refs.

## Quick start (TL;DR)

1. **Clone colligo** (if not present): `export GITHUB_TOKEN=<PAT>; git clone --branch foundry/stable --single-branch --depth 1 "https://${GITHUB_TOKEN}@github.com/Adobe-Firefly/colligo.git" /home/colligo/colligo; cd /home/colligo/colligo && git remote set-url origin https://github.com/Adobe-Firefly/colligo.git`
2. **Activate env:** `cd /home/colligo/colligo/contrib/Mori/collections/foundation_exploration && source scripts/env/activate.sh`
3. **Build your config** by forking `configs/foundry/_base_gr6_lite_prod_580k.yaml` (see [[#Configuration recipe]] below).
4. **Validate:** `python scripts/misc/validate_config.py -c <your_config>`
5. **Launch:** `export WANDB_API_KEY=<key> SLACK_MEMBER_ID=<id> LDAP=hshariati && env -u AWS_ACCESS_KEY_ID -u AWS_SECRET_ACCESS_KEY -u AWS_SESSION_TOKEN morictl launch <your_config>`
6. **Monitor:** `morictl find_error <uuid>` or `morictl job_summary <uuid>` (once running, see [[#Monitoring]] for details).

## Setup & Prerequisites

### Repository & credentials

- **Colligo repo:** branch `foundry/stable` (canonical).
  - Path: `/home/colligo/colligo` (snapshot-persistent on Pluto dev boxes) or `/mnt/localssd/colligo` (ephemeral).
  - **First clone requires `GITHUB_TOKEN`** (personal access token, `repo` scope, or shared team token): pass it to the clone command via `https://${GITHUB_TOKEN}@github.com/...`, then scrub it from the remote with `git remote set-url origin https://github.com/Adobe-Firefly/colligo.git`.

### Environment activation

From the FE workspace root:
```bash
cd /home/colligo/colligo/contrib/Mori/collections/foundation_exploration
source scripts/env/activate.sh     # Activates venv, puts `morictl` on PATH
morictl login                      # Device-flow: opens browser, caches token to ~/.colligo/pluto_cli/msal-pluto-auth.secret
```

No GPU / `make install` needed — `morictl launch` submits via its own uv-managed venv.

### Environment variables for launch

**Before running `morictl launch`, set:**
- `WANDB_API_KEY=<your_weights_and_biases_api_key>` — required, hard assertion in `scripts/local/main.py:1858`.
- `SLACK_MEMBER_ID=<your_slack_user_id>` — required, same assertion.
- `LDAP=hshariati` (or your username) — optional but recommended for identification in logs.

**Example:**
```bash
export WANDB_API_KEY=<key>
export SLACK_MEMBER_ID=D06340Q0EG3    # or look up your own in Slack → Profile → Copy user ID
export LDAP=hshariati
```

### AWS credentials (Pluto dev boxes only)

Pluto dev boxes inject static AWS creds for IAM user `foundry-bedrock-prod`, which **cannot** write to `s3://dit-scale-up/`. When launching from a dev box, unset them so `morictl` falls back to the box's **instance role** (which can write):

```bash
env -u AWS_ACCESS_KEY_ID -u AWS_SECRET_ACCESS_KEY -u AWS_SESSION_TOKEN morictl launch ...
```

(On your laptop, you likely have broader S3 access; this is a Pluto-only gotcha.)

## Configuration recipe

### Starting point

Fork `configs/foundry/_base_gr6_lite_prod_580k.yaml` (the **training config** for the 580k checkpoint). This is essential: it guarantees the model architecture (layer count, hidden dims) matches the checkpoint, avoiding silent shape mismatches on load.

Example fork: `configs/foundry/hshariati_gr6_lite_580k_t2v_infer.yaml`

### Key edits

**A. Launch section** (top of the file, starts line ~1)

```yaml
launch:
  name: hooman_gr6_t2v_infer          # or your identifier
  num_nodes: 1                        # was 64 (training); inference is single-node
  num_gpus: 8                         # keep 8 (H200 per node)
  gpu_instance: NVIDIA_H200_141GB     # keep unchanged
  pluto_project: Foundry-HP           # not Foundry-NBCU
  enable_torch_preflight_test: false  # disable for inference
  tag: gr6_lite_580k_t2v_infer        # descriptive label
  wandb_project: foundry              # or GenRenderer6-Debug
  docker_image: <keep existing>       # no change needed
```

**B. Train section** (starts ~line 760)

```yaml
train:
  inference_mode: true                # CRITICAL: flips model to eval, disables training ops
  sharding_gpus: 8                    # was 64; match num_gpus
```

**C. GPU count scaling** (search entire file for these keys; cap all at 8)

```yaml
model:
  params:
    vae_balance_gpu_count: 8          # was higher
    
  params:
    vlm_encoder_config:
      ckpt_params:
        balance_gpu_count: 8          # was higher
        auto_balance_prompts: false   # important
    
    denoiser_config:
      params:
        balance_gpu_specs: "ring=none,ulysses=8,bags=1,inner=ulysses,symm_mem=false"
        # ^ includes symm_mem=false (required in newer builds; base config lacks it)
```

Use grep to find all `balance_gpu_count`, `sharding_gpus`, `balance_gpu_specs`, `auto_balance_prompts` and scale to ≤8.

**D. Checkpoint section** (line ~28)

Keep the `path` unchanged; edit only the `training_state`:
```yaml
checkpoint:
  resume_from:
    path: s3://dit-scale-up/fe-experiments/.../.../kduarte/ckpt_step00580000/  # unchanged
    training_state:
      optimizer: false
      lr_scheduler: false
      ema: false
      train_step: true
      data_module_state: false
```

**E. Inference mapping** (line ~899, the `inference:` section)

Trim to **T2V only**:
```yaml
inference:
  inference_mapping:
    - [non_ema_inference, text_to_audio_video, [t2v_540p_5sec]]
  
  # Delete or comment out other inference_mapping entries (i2v, ti2v, etc.).
  # You may also remove unused dataset entries and inference modules (optional, keeps file lean).
```

**F. Dataset config** (for `t2v_540p_5sec`, in the datasets section ~line 1169–1296)

Set a small `eval_first_n` for the first pass:
```yaml
# Within the t2v_540p_5sec dataset entry:
params:
  eval_first_n: 8                     # process only first 8 samples; remove/increase for full eval
  # other params unchanged
```

**G. Data section** (starts ~line 2007)

**Remove the entire `data:` section** (training dataloaders are not needed in inference mode).

**Optional:** remove `validation_mapping` if present (not used in inference).

### Validation before launch

```bash
python scripts/misc/validate_config.py -c configs/foundry/hshariati_gr6_lite_580k_t2v_infer.yaml
# If validation passes, you're ready to launch.
```

## The 4 non-obvious blockers (and fixes)

These do not appear in the official docs and will cause silent failures or cryptic errors on rerun. All are one-time fixes.

### 1. Missing `WANDB_API_KEY` and `SLACK_MEMBER_ID`

**Error:** `AssertionError` in `scripts/local/main.py:1858` before the job even submits.

**Fix:** Set both env vars before calling `morictl launch`:
```bash
export WANDB_API_KEY=<paste_your_wandb_api_key>
export SLACK_MEMBER_ID=<your_slack_user_id>  # find via Slack → Profile → Copy user ID
morictl launch ...
```

Both are **required** — `morictl` will hard-fail if either is missing.

### 2. Static AWS creds block S3 writes (Pluto dev boxes only)

**Error:** `AccessDenied` when training code tries to upload config to `s3://dit-scale-up/`.

**Cause:** Dev boxes inject static AWS creds for user `foundry-bedrock-prod`, which lacks `PutObject` permission on that bucket.

**Fix:** Unset the static creds so `morictl` uses the **instance role** (which has write access):
```bash
env -u AWS_ACCESS_KEY_ID -u AWS_SECRET_ACCESS_KEY -u AWS_SESSION_TOKEN morictl launch ...
```

(Not needed on your laptop — you likely have broader S3 permissions.)

### 3. Revoked GitHub token in compute-node clone script

**Error:** `exit 128` on compute pod startup; `Invalid username or token` in logs.

**Cause:** `scripts/local/pluto_main.tmp.sh:132` hardcodes a revoked `cliobot_adobe` GitHub token for checking out colligo on the compute nodes.

**Fix:** This is a **local file edit** (not a config change). Before launch, edit `scripts/local/pluto_main.tmp.sh` line 132:

Replace the hardcoded token with the box's working token:
```bash
# BEFORE (line 132):
export GITHUB_TOKEN="<hardcoded_revoked_token>"

# AFTER:
export GITHUB_TOKEN="${KINETOBOT_GITHUB_API_TOKEN:-<fallback_token>}"
```

The box's `$KINETOBOT_GITHUB_API_TOKEN` is valid and verified against Adobe-Firefly/colligo. This edit **rides along** in the `local_diff.patch` sent to compute pods; it does not require a commit.

### 4. Missing `symm_mem` in `balance_gpu_specs`

**Error:** `Missing required key 'symm_mem'` during config parsing (parser in `src/foundation_exploration/models/denoisers/extended_knapformer.py:1903`).

**Cause:** The base config's `balance_gpu_specs` value lacks `symm_mem`; this repository's code is newer than the config template.

**Fix:** Add `symm_mem=false` to `balance_gpu_specs`:
```yaml
# In model.params.denoiser_config.params:
balance_gpu_specs: "ring=none,ulysses=8,bags=1,inner=ulysses,symm_mem=false"
```

(See [[#Configuration recipe#C. GPU count scaling]] for full context.)

## Launch command

Once config is ready and all env vars are set:

```bash
cd /home/colligo/colligo/contrib/Mori/collections/foundation_exploration
source scripts/env/activate.sh

# Set env vars
export WANDB_API_KEY=<your_key>
export SLACK_MEMBER_ID=<your_id>
export LDAP=hshariati

# On Pluto dev boxes: unset static AWS creds
# (Safe to run on laptop too — no-op if already unset)
env -u AWS_ACCESS_KEY_ID -u AWS_SECRET_ACCESS_KEY -u AWS_SESSION_TOKEN \
  morictl launch configs/foundry/hshariati_gr6_lite_580k_t2v_infer.yaml
```

**Output:** UUID of the submitted job, e.g. `0d0f4ebb-c0df-4e41-9aed-43832a2dff42`.

Save this UUID for monitoring.

## Monitoring

### Job status & errors

Once the job is running on [[wiki/entities/pluto|Pluto]]:

```bash
# Quick check — is it running, failed, etc.?
morictl find_error <UUID>

# Full job summary (logs, metrics, end state)
morictl job_summary <UUID>

# List recent jobs
morictl job list --project Foundry-HP
```

### What to watch for

- **Startup (first ~2 min):** pod initializes, downloads the 580k checkpoint (~40 GB), compiles inference kernels. Initial `nvidia-smi` will show rapid GPU memory growth.
- **Denoising loop:** once running, the job will print per-step timings (target ~9 s/step for T2V @ 50 denoising steps, ~450 s per sample).
- **Data loading:** if samples are slow to appear, check that the dataset (e.g., `t2v_540p_5sec` @ `s3://clineto/test_data/...`) is readable and not too large.

### Common failure patterns

| Error | Cause | Fix |
|-------|-------|-----|
| `world_size must be divisible by ...` | GPU-count param still > 8 | Grep for `balance_gpu_count`, `sharding_gpus`, scale all to ≤8 |
| `Unexpected/Missing key(s) on checkpoint load` | Model architecture ≠ checkpoint | Use base config `_base_gr6_lite_prod_580k.yaml`; don't fork from old inference configs |
| `data config is required` | Forgot `inference_mode: true` | Add to `train:` section |
| `AccessDenied` on S3 write | Static AWS creds (Pluto box) | Use `env -u AWS_ACCESS_KEY_ID -u AWS_SECRET_ACCESS_KEY -u AWS_SESSION_TOKEN morictl launch ...` |
| `Invalid username or token` (pod exit 128) | Revoked GitHub token in compute script | Edit `scripts/local/pluto_main.tmp.sh:132` to use `$KINETOBOT_GITHUB_API_TOKEN` |
| `Missing required key 'symm_mem'` | Config lacks `symm_mem` in `balance_gpu_specs` | Append `,symm_mem=false` to the `balance_gpu_specs` value |

## Results & outputs

### WandB run

Results are logged to the [[wiki/entities/wandb|WandB]] project specified in your config (default: `foundry`). Run name pattern: `inference-gr6_lite_580k_t2v_infer-<timestamp>`.

Logged metrics:
- Per-sample denoising-step timings
- Generated video metadata (resolution, frame count, duration)
- Latency breakdowns (model forward, VAE decode, etc.)

### S3 outputs

The job's compute pod uploads generated videos to an S3 folder. Path available in job logs or via `morictl job_summary <UUID>` under "Output S3 Path" or similar. Pattern: `s3://dit-scale-up/experiments/<job_name>/<job_uuid>/outputs/`.

### Checkpoint & intermediate state

Checkpoints/snapshots are not saved during inference runs (inference_mode=true disables checkpointing). To preserve intermediate denoising steps or generated frames, configure the inference module to log them to S3 (check `scripts/agent/running_inference.md` for dataset-specific logging options).

## Next steps

### Image-to-video (I2V)

Repeat the config recipe, but:
1. Swap `t2v_*` datasets for `i2v_*` equivalents (catalog at ~line 1416–1557 in the base config).
2. Add reference image paths to the prompt JSON:
   ```json
   [{"task":"image_to_video","prompt":"...","media":["s3://.../ref.jpg"],"width":960,"height":544,...}]
   ```
3. All other config changes remain the same.

### Custom prompt sets

Hooman will provide a custom prompt JSON set. Schema: `JSONDatasetSampleSchemaV1`
```json
[
  {
    "task": "text_to_video",
    "prompt": "a waterfall in slow motion",
    "negative_prompt": "blurry, low quality",
    "output_type": "video",
    "width": 960,
    "height": 544,
    "num_frames": 113
  },
  ...
]
```

Save to S3 (e.g., `s3://dit-scale-up/experiments/hooman_custom_prompts_v1.json`), then create a dataset config entry in the inference mapping pointing to it.

### Longer videos, higher resolutions

Update dataset entries in the config to use e.g. `t2v_1080p_10sec` (10 s @ 1080p). Frame count = `duration_sec × 24 + 9` (e.g., 10 s = 249 frames). Monitor GPU memory; if OOM, reduce `eval_first_n` or batch size via the dataset's `batch_size` param.

### Troubleshooting & reference docs

- **In-repo canonical guides** (read these first):
  - `contrib/Mori/collections/foundation_exploration/scripts/agent/running_inference.md` — full minimal inference-config template and detailed troubleshooting.
  - `scripts/agent/config_system.md` — balancer rules & coupling.
  - `scripts/agent/environment_setup.md` — full setup flow.
- **Obsidian wiki pages:**
  - [[wiki/concepts/mori-training-workflow]] — general Mori workflow (training & inference).
  - [[wiki/concepts/mori-config]] — sequence balancer and config validation details.
  - [[wiki/concepts/pluto-job-lifecycle]] — Pluto job states and monitoring.
  - [[wiki/concepts/colligo-pluto-sdk]] — Pluto CLI/SDK reference.

## Related

- [[wiki/entities/mori]]
- [[wiki/entities/colligo]]
- [[wiki/entities/pluto]]
- [[wiki/concepts/mori-training-workflow]]
- [[wiki/concepts/mori-config]]
- [[wiki/concepts/pluto-job-lifecycle]]
- [[wiki/concepts/pluto-cli-sdk]]
- [[wiki/concepts/colligo-inference]]
