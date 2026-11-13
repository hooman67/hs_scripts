---
name: project_gr6_t2v_inference
description: "GR6 580k Lite T2V inference on Pluto — working config, launch recipe, and the 4 non-obvious blockers/fixes"
metadata: 
  node_type: memory
  type: project
  originSessionId: b8832f62-30e8-4425-b7ca-05fc12b73f85
---

GR6 580k "Lite" text-to-video **inference works end-to-end on Pluto** (first run 2026-07-07: all 8 ranks
`return_code=0`, videos synced to WandB). Done from *inside* the Pluto CPU dev box, cwd
`/home/colligo/hs_scripts/claude/obsidian`; colligo checked out at `/home/colligo/colligo` on `foundry/stable`.

- **Config:** `contrib/Mori/collections/foundation_exploration/configs/foundry/hshariati_gr6_lite_580k_t2v_infer.yaml`
  (fork of `_base_gr6_lite_prod_580k.yaml`: `inference_mode: true`, 1 node × 8 H200, all GPU-count params → 8,
  `pluto_project: Foundry-HP`, `inference_mapping` trimmed to `[non_ema_inference, text_to_audio_video, [t2v_540p_5sec]]`,
  `eval_first_n: 8`, training `data:` section dropped).
- **Launch/monitor:** helper `hs_scripts/claude/obsidian/gr6_status.sh {status|logs|find_error}`.
  Results → WandB `foundry` project, run `inference-gr6_lite_580k_t2v_infer-…`; job-summary HTML under the
  job's S3 `logs/<uuid>/…/index.html`. Denoising ≈9 s/step × 50 steps ≈ 8 min per 5-s clip.

**Four blockers NOT in the in-repo docs (fix on every rerun):**
1. `morictl launch` hard-asserts `WANDB_API_KEY` + `SLACK_MEMBER_ID` env vars; runs `aip login` first →
   **device flow** (browser code at login.microsoft.com/device), token caches to `~/.colligo/pluto_cli/`.
   No `make install`/GPU venv needed — launch loads config from FE source via its own uv venv.
2. Box injects static AWS keys for IAM user `foundry-bedrock-prod` that **can't PutObject to `s3://dit-scale-up`**.
   Prefix launch with `env -u AWS_ACCESS_KEY_ID -u AWS_SECRET_ACCESS_KEY -u AWS_SESSION_TOKEN` so it uses the
   box **instance role** (`colligo-laser01-od-ng-role-uw2`), which can write.
3. `scripts/local/pluto_main.tmp.sh` hardcodes an **expired** `cliobot_adobe` GitHub token → compute pod dies
   exit 128 `Invalid username or token`. Replace with the box's working `$KINETOBOT_GITHUB_API_TOKEN`.
4. `balance_gpu_specs` now needs a `symm_mem` key (parser: `extended_knapformer.py`). Use
   `ring=none,ulysses=8,bags=1,inner=ulysses,symm_mem=false` (base config + running_inference.md are stale).

Full detail + exact commands: `hs_scripts/claude/obsidian/GR6_T2V_HANDOFF.md`. Next: I2V run, Hooman's custom
prompt set, and an Obsidian hs_base `gr6-inference` how-to page. See [[project_obsidian_llm_wiki]], [[reference_obsidian_mcp]].
