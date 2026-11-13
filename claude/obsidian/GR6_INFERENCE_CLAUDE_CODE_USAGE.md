# Using `/gr6-video-inference` in Claude Code

The GR6 video inference skill is now available as a slash command in Claude Code. Use it to launch T2V/I2V inference jobs on Pluto directly from the CLI.

## Basic usage in Claude Code

### Launch a default T2V job

```
/gr6-video-inference
```

This:
1. Validates the default config (`hshariati_gr6_lite_580k_t2v_infer.yaml`)
2. Prompts for or loads: `WANDB_API_KEY`, `SLACK_MEMBER_ID`, `LDAP`, `KINETOBOT_GITHUB_API_TOKEN`
3. Unsets static AWS keys (blocker #2 fix)
4. Patches `pluto_main.tmp.sh` with the working GitHub token (blocker #3 fix)
5. Runs `morictl launch` from the FE directory
6. Saves job state and prints monitoring hints

### Launch with a custom config

```
/gr6-video-inference --config /path/to/my_config.yaml
```

Useful for I2V, custom prompt sets, or different model checkpoints.

### Dry-run (inspect without launching)

```
/gr6-video-inference --dry-run
```

Shows the exact `morictl launch` command and env vars that would be used — great for testing config changes or credential setup.

### Check last job status

```
/gr6-video-inference --status
```

Shows the most recent job name, UUID, and monitoring commands. Does not launch a new job.

### Show help

```
/gr6-video-inference --help
```

## Before you use it

### 1. Set up credentials

Add to `~/.claude/hshariati/credentials.yaml`:

```yaml
wandb:
  api_key: "<your-wandb-api-key>"

slack:
  member_id: "<your-slack-member-id>"  # e.g., D06340Q0EG3

ldap: "hshariati"

kinetobot_github:
  api_token: "<github-pat-..."  # GitHub PAT for Adobe-Firefly/colligo
```

Or set env vars in your shell:
```bash
export WANDB_API_KEY="..."
export SLACK_MEMBER_ID="..."
export LDAP="hshariati"
export KINETOBOT_GITHUB_API_TOKEN="..."
```

### 2. Ensure colligo is checked out

Default location: `/home/colligo/colligo` on branch `foundry/stable`.

To use a different path:
```
/gr6-video-inference --colligo /path/to/colligo
```

### 3. Prepare (or use default) config

The default config is:
```
/home/colligo/colligo/contrib/Mori/collections/foundation_exploration/configs/foundry/hshariati_gr6_lite_580k_t2v_infer.yaml
```

To fork for a custom config:
1. Start with `configs/foundry/_base_gr6_lite_prod_580k.yaml`
2. Set `inference_mode: true`, `num_nodes: 1`
3. Scale GPU-count params to 8
4. Add `symm_mem=false` to `balance_gpu_specs`
5. Trim `inference_mapping` to your task
6. Validate: `python scripts/misc/validate_config.py -c <your_config>`

## What happens during launch

### Pre-flight

- Validates config (checks for `train`, `launch`, `inference_mapping`, `symm_mem`)
- Resolves credentials (env → credentials.yaml → prompt)
- Patches `pluto_main.tmp.sh` to inject `KINETOBOT_GITHUB_API_TOKEN`
- Unsets `AWS_*` env vars (so instance role is used)
- Triggers device-flow login if needed (browser auth at login.microsoft.com/device)

### Launch

- Activates FE environment (`source scripts/env/activate.sh`)
- Runs `morictl launch <config>` with cleaned env
- Captures job name and UUID
- Saves state to `~/.claude/hshariati/.gr6_last_job`

### Post-launch

Prints:
- Job name and UUID
- Monitoring command templates
- Expected duration (~8 min per 5-sec video)
- WandB project and run name format
- S3 results path info

## Monitoring in progress

After launch, use the printed commands to monitor:

```bash
# Job status
morictl job status <JOB_NAME>

# Recent logs (last 80 lines)
morictl job logs <JOB_NAME>

# Find errors
morictl find_error <UUID>

# Full summary (once complete)
morictl job_summary <UUID>
```

Or use the skill again:
```
/gr6-video-inference --status
```

## Results

### WandB

- **Project:** `foundry`
- **Run name:** `inference-gr6_lite_580k_t2v_infer-<suffix>-<timestamp>`
- **Media:** Videos appear in the run's media tab

### S3

Job outputs under:
```
s3://dit-scale-up/.../<JOB_UUID>/...
```

Full path shown in `morictl job_summary` output.

## Common commands

| Task | Command |
|------|---------|
| Launch default T2V | `/gr6-video-inference` |
| Launch custom config | `/gr6-video-inference --config /path/to/config.yaml` |
| Show last job status | `/gr6-video-inference --status` |
| Dry-run (inspect) | `/gr6-video-inference --dry-run` |
| Get full help | `/gr6-video-inference --help` |
| Show config validation errors | `morictl validate_config <config.yaml>` (from FE dir) |
| Monitor in-flight job | `morictl find_error <UUID>` or `morictl job logs <JOB>` |

## Troubleshooting

### "WANDB_API_KEY not found"

Add to credentials.yaml or set env var:
```bash
export WANDB_API_KEY="..."
/gr6-video-inference
```

### "KINETOBOT_GITHUB_API_TOKEN not found"

Get a valid GitHub PAT from Adobe-Firefly admins, add to credentials.yaml:
```yaml
kinetobot_github:
  api_token: "github_pat_..."
```

### "Colligo root not found"

Ensure `/home/colligo/colligo` exists on branch `foundry/stable`, or use:
```
/gr6-video-inference --colligo /path/to/colligo
```

### "Config not found"

Provide full path:
```
/gr6-video-inference --config /full/path/to/config.yaml
```

### Job fails with exit 128 (token error)

The GitHub token in `pluto_main.tmp.sh` has expired. The skill patches this automatically, but if you see exit 128:
1. Verify `KINETOBOT_GITHUB_API_TOKEN` is valid
2. The skill should have injected it; if not, manually patch and relaunch

### Device-flow login times out

If the browser auth times out:
1. Manually run `morictl login` from the FE directory
2. Complete the device flow auth at login.microsoft.com/device
3. Re-run `/gr6-video-inference`

### "balance_gpu_specs missing symm_mem"

The script warns about this. Update your config:

From:
```yaml
balance_gpu_specs: "ring=none,ulysses=8,bags=1,inner=ulysses"
```

To:
```yaml
balance_gpu_specs: "ring=none,ulysses=8,bags=1,inner=ulysses,symm_mem=false"
```

## Behind the scenes: the 4 blockers

The skill automates fixes for 4 non-obvious issues:

| # | Problem | Symptom | Fix |
|----|---------|---------|-----|
| 1 | `morictl` hard-asserts `WANDB_API_KEY` + `SLACK_MEMBER_ID` | Launch fails with `AssertionError` | Script prompts for these, injects into env |
| 2 | Box static AWS keys can't write to `s3://dit-scale-up` | `AccessDenied` on training-code upload | Script unsets `AWS_*`, uses instance role |
| 3 | `pluto_main.tmp.sh` has expired GitHub token | Pod fails exit 128: `Invalid username or token` | Script patches with `KINETOBOT_GITHUB_API_TOKEN` |
| 4 | `balance_gpu_specs` missing `symm_mem` key | Config parse fails: `Missing required key 'symm_mem'` | Script validates and warns; you update config |

See `GR6_T2V_HANDOFF.md` for full technical details.

## File locations

- **Script source:** `~/.claude/scripts/gr6_video_inference.py`
- **Command registration:** `~/.claude/commands/gr6_video_inference` (symlink to script)
- **Command docs:** `~/.claude/commands/gr6_video_inference.md`
- **Git backup:** All above under `hs_scripts/claude/dotclaude/`
- **Job state cache:** `~/.claude/hshariati/.gr6_last_job` (JSON)

## See also

- **Quick reference:** `hs_scripts/claude/obsidian/GR6_INFERENCE_SKILL.md`
- **Full command docs:** `~/.claude/commands/gr6_video_inference.md`
- **Session handoff:** `hs_scripts/claude/obsidian/GR6_T2V_HANDOFF.md`
- **In-repo guide:** `colligo/contrib/Mori/collections/foundation_exploration/scripts/agent/running_inference.md`

---

**Ready to go!** Run:
```
/gr6-video-inference --dry-run
```

to test your setup, or:
```
/gr6-video-inference
```

to launch a real T2V job.
