# GR6 Text-to-Video Inference on Pluto

Unified launcher for GR6 580k Lite text-to-video inference on Pluto. Automates all setup, env-var injection, and the 4 known blockers.

**Usage:** `/gr6-video-inference [--config PATH] [--colligo PATH] [--dry-run] [--status]`

## Quick start

```bash
# Launch with default config (hshariati_gr6_lite_580k_t2v_infer.yaml)
/gr6-video-inference

# Launch with a custom config
/gr6-video-inference --config /path/to/custom_config.yaml

# Show status of last launched job
/gr6-video-inference --status

# Dry-run: show command and env without launching
/gr6-video-inference --dry-run
```

## What it does

1. **Validates config** — checks for required sections (train, launch, inference_mapping) and `symm_mem` in `balance_gpu_specs`
2. **Resolves credentials** — fetches `WANDB_API_KEY`, `SLACK_MEMBER_ID`, `LDAP`, `KINETOBOT_GITHUB_API_TOKEN` from:
   - Environment variables (highest priority)
   - `~/.claude/hshariati/credentials.yaml`
   - Interactive prompts (fallback)
3. **Patches GitHub token** — injects `KINETOBOT_GITHUB_API_TOKEN` into `scripts/local/pluto_main.tmp.sh` to replace the hardcoded expired token
4. **Unsets static AWS keys** — removes `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN` so the instance role is used (can write to `s3://dit-scale-up`)
5. **Handles device-flow login** — runs `morictl login` if needed (caches token to `~/.colligo/pluto_cli/msal-pluto-auth.secret`)
6. **Launches job** — runs `morictl launch <config>` and captures job name + UUID
7. **Saves job state** — persists last job info to `~/.claude/hshariati/.gr6_last_job` for monitoring
8. **Shows monitoring hints** — prints command templates for status, logs, and error checking

## Prerequisites

- **colligo checkout** at `/home/colligo/colligo` on branch `foundry/stable` (default) or `--colligo /path/to/colligo`
- **Credentials in `~/.claude/hshariati/credentials.yaml`** (or env vars):
  ```yaml
  wandb:
    api_key: "..."
  slack:
    member_id: "D06340Q0EG3"  # or your SLACK_MEMBER_ID
  ldap: "hshariati"
  kinetobot_github:
    api_token: "github_pat_..."
  ```
- **GitHub PAT** for Adobe-Firefly/colligo (needed to clone/update the repo)

## Options

| Option | Description |
|--------|-------------|
| `--config PATH` | Config YAML path. Default: `{colligo}/contrib/Mori/collections/foundation_exploration/configs/foundry/hshariati_gr6_lite_580k_t2v_infer.yaml` |
| `--colligo PATH` | Colligo repo root. Default: `/home/colligo/colligo` |
| `--dry-run` | Show command and env without launching. Useful for testing. |
| `--status` | Show status of last launched job (no new launch). |
| `-v, --verbose` | Verbose output. |
| `--help` | Show this help. |

## The 4 blockers (automatically fixed)

### 1. morictl requires WANDB_API_KEY + SLACK_MEMBER_ID
`morictl launch` hard-asserts these env vars and runs `aip login` first (device-flow browser auth).

**Fix:** Script prompts for these and injects them into the launch env.

### 2. Box injects static AWS keys → AccessDenied on s3://dit-scale-up
The CPU box's environment sets `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN` for IAM user `foundry-bedrock-prod`, which **cannot** write to `s3://dit-scale-up/` (training code upload fails).

**Fix:** Script unsets all three so the launch falls back to the box's instance role (`colligo-laser01-od-ng-role-uw2`), which can write.

### 3. Hardcoded GitHub token in pluto_main.tmp.sh is expired
`scripts/local/pluto_main.tmp.sh:132` contains a revoked `cliobot_adobe` token → compute pod dies with exit 128 `Invalid username or token`.

**Fix:** Script patches the file to inject `KINETOBOT_GITHUB_API_TOKEN` (a working token verified against Adobe-Firefly/colligo). This rides along in the launch's `local_diff.patch`.

### 4. balance_gpu_specs missing symm_mem key
The denoiser config parser now requires `symm_mem` in `balance_gpu_specs` (newer code than the base config).

**Fix:** Script validates the config and warns if `symm_mem` is missing. Recommended value:
```
ring=none,ulysses=8,bags=1,inner=ulysses,symm_mem=false
```

## Monitoring

### After launch

The script prints monitoring command templates. Common uses:

```bash
# Job status
morictl job status <JOB_NAME>

# Recent logs (last 80 lines)
morictl job logs <JOB_NAME>

# Find errors
morictl find_error <UUID>

# Full job summary (once done; includes S3 results path)
morictl job_summary <UUID>
```

### Check last job

```bash
/gr6-video-inference --status
```

This shows the most recent job name, UUID, and monitoring commands.

## Results

- **WandB:** `foundry` project, run `inference-gr6_lite_580k_t2v_infer-<config_suffix>-<timestamp>`
- **S3 logs:** Job's output folder under `s3://dit-scale-up/...` (path shown in job_summary HTML)
- **Duration:** ~8 min per 5-sec video (9 s/denoising step × 50 steps)

## Credentials setup

Create or edit `~/.claude/hshariati/credentials.yaml`:

```yaml
wandb:
  api_key: "your-wandb-api-key"

slack:
  member_id: "your-slack-member-id"  # e.g., D06340Q0EG3

ldap: "hshariati"

kinetobot_github:
  api_token: "github_pat_..."  # GitHub PAT for Adobe-Firefly/colligo
```

Or set env vars:
```bash
export WANDB_API_KEY="..."
export SLACK_MEMBER_ID="..."
export LDAP="hshariati"
export KINETOBOT_GITHUB_API_TOKEN="github_pat_..."
```

## Config forking & customization

See `hs_scripts/claude/obsidian/GR6_T2V_HANDOFF.md` for the full config recipe:

1. Fork `configs/foundry/_base_gr6_lite_prod_580k.yaml`
2. Set `inference_mode: true` and `num_nodes: 1` (from 64)
3. Scale all GPU-count params to 8
4. Add `symm_mem=false` to `balance_gpu_specs`
5. Trim `inference_mapping` to your task (T2V, I2V, etc.)
6. Validate: `python scripts/misc/validate_config.py -c <your_config>`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `WANDB_API_KEY not found` | Add to `~/.claude/hshariati/credentials.yaml` or set `WANDB_API_KEY` env var. |
| `KINETOBOT_GITHUB_API_TOKEN not found` | Add valid GitHub PAT to credentials or `KINETOBOT_GITHUB_API_TOKEN` env var. |
| `Colligo root not found` | Use `--colligo /path/to/colligo` or clone to `/home/colligo/colligo`. |
| `Config not found` | Use `--config /absolute/path/to/config.yaml`. |
| `balance_gpu_specs missing symm_mem` | Update config: replace `balance_gpu_specs` value with `ring=none,ulysses=8,bags=1,inner=ulysses,symm_mem=false`. |
| Device-flow login timeout | Manually run `morictl login` and authenticate at login.microsoft.com/device. |
| `morictl: command not found` | Run `source scripts/env/activate.sh` in the FE directory first. |
| Job fails with exit 128 (token error) | GitHub token in pluto_main.tmp.sh may be stale; script patches this automatically. |

## See also

- `hs_scripts/claude/obsidian/GR6_T2V_HANDOFF.md` — full session notes, config recipe, blocker details
- `hs_scripts/claude/obsidian/gr6_status.sh` — legacy helper (now superseded by `--status`)
- In colligo repo:
  - `contrib/Mori/collections/foundation_exploration/scripts/agent/running_inference.md` — authoritative inference guide
  - `contrib/Mori/collections/foundation_exploration/scripts/agent/environment_setup.md` — env setup details
  - `contrib/Mori/collections/foundation_exploration/scripts/misc/validate_config.py` — config validator

## Examples

### Default T2V inference (8 samples)

```bash
/gr6-video-inference
# Launches with default config: hshariati_gr6_lite_580k_t2v_infer.yaml
# 1 node × 8 H200 GPUs, 5-sec clips, 8 samples
```

### Custom config for image-to-video

```bash
/gr6-video-inference --config /home/colligo/colligo/.../configs/foundry/my_i2v_config.yaml
# Launches custom I2V config
```

### Dry-run to inspect command

```bash
/gr6-video-inference --dry-run
# Prints the morictl launch command and env vars without executing
```

### Monitor an in-flight job

```bash
/gr6-video-inference --status
# Shows last job name, UUID, and monitoring commands
```

### Custom colligo path (e.g., ephemeral checkout)

```bash
/gr6-video-inference --colligo /mnt/localssd/colligo --config /mnt/localssd/colligo/.../my_config.yaml
```
