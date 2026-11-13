# GR6 Video Inference Skill — Quick Reference

The `/gr6-video-inference` Claude Code skill automates GR6 T2V inference launches on Pluto with all 4 blockers fixed.

## What you need

1. **Credentials in `~/.claude/hshariati/credentials.yaml`** — or set env vars:
   ```yaml
   wandb:
     api_key: "your-wandb-api-key"
   slack:
     member_id: "D06340Q0EG3"  # Your Slack member ID
   ldap: "hshariati"
   kinetobot_github:
     api_token: "github_pat_..."  # GitHub PAT for Adobe-Firefly/colligo
   ```

2. **Colligo repo** at `/home/colligo/colligo` on branch `foundry/stable` (or use `--colligo /path`)

3. **Config YAML** — default is `hshariati_gr6_lite_580k_t2v_infer.yaml` (or pass `--config /path`)

## Quick commands

```bash
# Launch with defaults (8 T2V samples, 5-sec clips)
/gr6-video-inference

# Custom config
/gr6-video-inference --config /path/to/my_config.yaml

# Show last job status (no new launch)
/gr6-video-inference --status

# Dry-run to see what would execute
/gr6-video-inference --dry-run
```

## After launch

The skill prints monitoring hints. Common commands:

```bash
# Get job status
morictl job status <JOB_NAME>

# View recent logs
morictl job logs <JOB_NAME>

# Find errors
morictl find_error <UUID>

# Full summary (once done)
morictl job_summary <UUID>
```

## The 4 blockers (auto-fixed)

| # | Issue | Fix |
|----|-------|-----|
| 1 | morictl requires `WANDB_API_KEY` + `SLACK_MEMBER_ID` | Skill prompts for these, injects into launch env |
| 2 | Box static AWS keys → `AccessDenied` on `s3://dit-scale-up` | Skill unsets `AWS_*` keys, uses instance role |
| 3 | `pluto_main.tmp.sh` has expired GitHub token → exit 128 | Skill patches file with `KINETOBOT_GITHUB_API_TOKEN` |
| 4 | `balance_gpu_specs` missing `symm_mem` key | Skill validates config, warns if missing |

## Config forking recipe

Start with `configs/foundry/_base_gr6_lite_prod_580k.yaml`:

1. Set `inference_mode: true`
2. Change `num_nodes: 64 → 1` (keep `num_gpus: 8`)
3. Scale GPU-count params to 8: `vae_balance_gpu_count`, `vlm_encoder...balance_gpu_count`, `balance_gpu_specs`
4. Update `balance_gpu_specs` to:
   ```
   ring=none,ulysses=8,bags=1,inner=ulysses,symm_mem=false
   ```
5. Trim `inference_mapping` to your task (T2V, I2V, etc.)
6. Set `inference.inference_mapping[].dataset_params.eval_first_n: 8` (small test set)
7. Validate: `python scripts/misc/validate_config.py -c <your_config>`

## WandB results

- **Project:** `foundry`
- **Run name:** `inference-gr6_lite_580k_t2v_infer-<suffix>-<timestamp>`
- **Video results:** Under the run's `media` tab

## S3 results

Job outputs stored under:
```
s3://dit-scale-up/.../<JOB_UUID>/...
```

Path shown in `morictl job_summary <UUID>` output.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `WANDB_API_KEY not found` | Add to credentials.yaml or set `WANDB_API_KEY` env var |
| `KINETOBOT_GITHUB_API_TOKEN not found` | Add to credentials.yaml or set env var |
| Device-flow login times out | Run `morictl login` manually, authenticate at login.microsoft.com/device |
| Job fails exit 128 (token error) | GitHub token in pluto_main.tmp.sh stale — skill patches this automatically |
| `balance_gpu_specs missing symm_mem` | Update config with value above |

## See also

- Full docs: `~/.claude/commands/gr6_video_inference.md`
- Session handoff: `hs_scripts/claude/obsidian/GR6_T2V_HANDOFF.md`
- Legacy status helper: `hs_scripts/claude/obsidian/gr6_status.sh`
- In-repo guide: `colligo/contrib/Mori/collections/foundation_exploration/scripts/agent/running_inference.md`

## Script files

- **Main script:** `~/.claude/scripts/gr6_video_inference.py`
- **Command registration:** `~/.claude/commands/gr6_video_inference` (symlink)
- **Command docs:** `~/.claude/commands/gr6_video_inference.md`
- **Git backup:** All above symlinked from `hs_scripts/claude/dotclaude/`

---

**Git commit these files to sync across machines:**
```bash
cd ~/hs_scripts && git add claude/dotclaude/scripts/gr6_video_inference.py \
  claude/dotclaude/commands/gr6_video_inference.md && git commit -m "Add gr6-video-inference skill"
```
