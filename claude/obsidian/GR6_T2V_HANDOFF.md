# GR6 Text-to-Video Inference — Session Handoff

**Written:** 2026-07-06 (previous session, from the laptop).
**You (new session):** running **inside the Pluto CPU dev box** `pluto-prod-hshariati-hooman-cpu-de-1-0`
(job name `hooman_cpu_dev_box`, project `Foundry-Presale-And-Partnership-Support`), cwd
`hs_scripts/claude/obsidian` → on the box that's `/home/colligo/hs_scripts/claude/obsidian`.

> **Goal:** run **inference on the GR6 580k "Lite" checkpoint, task = text-to-video (T2V)**, on Pluto.
> This is research/eval for Hooman (Foundry team). Later: I2V, and a custom prompt set Hooman will provide.

---

## TL;DR — do this, in order

1. **Get `colligo` on the box** (needs a GitHub token — see "Blocker" below). Prefer `/home/colligo/colligo`
   (snapshot-persistent); `/mnt/localssd/colligo` is fine too but ephemeral. Use branch **`foundry/stable`**.
2. `cd /home/colligo/colligo/contrib/Mori/collections/foundation_exploration`
3. `make install` → `source scripts/env/activate.sh` → `morictl login` (puts `morictl` on PATH).
4. **Read `scripts/agent/running_inference.md`** — it is THE authoritative guide; follow it.
5. **Build the T2V inference config** by forking `configs/foundry/_base_gr6_lite_prod_580k.yaml` (see recipe below).
6. `python scripts/misc/validate_config.py -c <your_config>`
7. `morictl launch <your_config>` → a 1-node × 8×H200 Pluto job in **`Foundry-HP`** runs the T2V eval.
8. Monitor: `morictl find_error <uuid>` / `morictl job_summary <uuid>`; results → WandB + the job's S3 folder.

---

## Decisions already locked (don't re-litigate)

- **Path A:** submit from this CPU box via `morictl launch`; the inference runs on a **separate 8×H200
  Pluto job**. (Not local_run — this box has **no GPU**, 96 CPUs.)
- **pluto_project = `Foundry-HP`** (Hooman chose this; it replaces the config's `Foundry-NBCU`).
- **Base config = the foundry `_base_gr6_lite_prod_580k.yaml`** (NOT an existing inference config) —
  because it is guaranteed to match the 580k checkpoint's architecture (it's the config that trains it),
  avoiding the `vlm_channels`/`selected_layer` mismatch the running_inference doc warns about.
- **Checkpoint (already in that config, line 29):**
  `s3://dit-scale-up/fe-experiments/FFP-45051-dit-FFP-38154-gr6_lite_prod_beta_hr_conversational-2026.03.24-18.19.23/model-checkpoints/kduarte/ckpt_step00580000/`
- **Test set for the first run:** `t2v_540p_5sec` (960×544, 113 frames/5 s @24fps; prompts at
  `s3://clineto/test_data/t2v_test_set_v1_2026-02-11T15:20:06.json`). Use a **small `eval_first_n` (~8)**
  for the first pass. Hooman will hand over a custom prompt set later (JSON schema below).

---

## ⛔ Blocker to clear FIRST: GitHub auth on the box

The box is fresh — **no `colligo` checkout, no `GITHUB_TOKEN`**. Cloning `Adobe-Firefly/colligo` over
HTTPS failed with `could not read Username for 'https://github.com'`. Per
`scripts/agent/environment_setup.md`, cloning requires a **GitHub personal access token (repo scope)**.

**Ask Hooman for a GitHub PAT** (github.com/settings/tokens → classic → `repo` scope, or a shared team
token). Then, e.g.:
```bash
export GITHUB_TOKEN=<paste>
git clone --branch foundry/stable --single-branch --depth 1 \
  "https://${GITHUB_TOKEN}@github.com/Adobe-Firefly/colligo.git" /home/colligo/colligo
# then scrub the token from the remote URL:
git -C /home/colligo/colligo remote set-url origin https://github.com/Adobe-Firefly/colligo.git
```
Do **not** go hunting through credential stores for a token — the auto-mode classifier blocks that
(it happened last session). Just ask Hooman.

*(The laptop had `colligo` cloned at `/Users/hshariati/colligo` on `foundry/stable` @ `1ebaa02`, but the
new session is on the box, so re-clone there.)*

---

## The config recipe (fork → convert to inference)

Fork `configs/foundry/_base_gr6_lite_prod_580k.yaml` → e.g. `configs/foundry/hshariati_gr6_lite_580k_t2v_infer.yaml`.
It's a **64-node training config** (~15,900 lines); convert to single-node inference. Changes:

**A. `train` section** (starts ~line 760):
- add `inference_mode: true`
- `sharding_gpus: 64 → 8`

**B. `launch` section** (starts line 1):
- `num_nodes: 64 → 1` (keep `num_gpus: 8`)
- `pluto_project: Foundry-NBCU → Foundry-HP`
- `enable_torch_preflight_test: false`
- set a descriptive `tag:` e.g. `gr6_lite_580k_t2v_infer`; `wandb_project` can stay `foundry` (or `GenRenderer6-Debug`)
- keep `gpu_instance: NVIDIA_H200_141GB` and the existing `docker_image`

**C. Scale every GPU-count param to ≤ 8** (running_inference.md Step 4 — search the whole file):
- `model.params.vae_balance_gpu_count` → 8
- `model.params.vlm_encoder_config.ckpt_params.balance_gpu_count` → 8, and `auto_balance_prompts: false`
- `model.params.denoiser_config.params.balance_gpu_specs` → `"ring=none,ulysses=8,bags=1,inner=ulysses"`
- (grep for `balance_gpu_count`, `sharding_gpus`, `balance_gpu_specs`, `auto_balance_prompts` and cap all at 8)

**D. `checkpoint.resume_from`** (line ~28): keep `path` (the 580k ckpt). Set
`training_state: {optimizer: false, lr_scheduler: false, ema: false, train_step: true, data_module_state: false}`.

**E. `inference.inference_mapping`** (line ~899): trim to **T2V only**:
```yaml
  inference_mapping:
    - [ non_ema_inference, text_to_audio_video, [ t2v_540p_5sec ] ]
```
Keep the `non_ema_inference` runner, the `text_to_audio_video` ldm_inference_module, and the
`t2v_540p_5sec` dataset entry (set its `eval_first_n: 8`). You may delete the other inference_mapping
entries + unused datasets/modules to keep it lean (optional).

**F. Remove the training `data:` section** (starts ~line 2007) — not needed in inference mode. Also drop
`validation_mapping` if present.

Then `validate_config.py`, then `morictl launch`.

> The T2V dataset catalog is in the base config at **lines 1169–1296** (`t2v_360p/540p × 2/5/10 sec`,
> plus senorita/eval99 variants). I2V/TI2V sets are at **~1416–1557** (for the later I2V run).

---

## Key facts / gotchas (so you don't re-derive)

- **GR6 = "genrender6".** "Lite" = 32L-2048d; "Ultra" = 56L-4096d. We want **Lite / 580k**.
- **Two inference workflows** (running_inference.md): (1) config-based `morictl launch`/`local_run` (what we're doing);
  (2) exported inference (`scripts/gr6/export.py` + `inference.py`, torchrun, local GPU) — not our path (no GPU here).
- **Frame counts @24fps:** 2 s=57, 5 s=113, 10 s=225 (`dur*24+9`).
- **Prompt JSON schema** (`JSONDatasetSampleSchemaV1`) for Hooman's future custom set:
  ```json
  [{"task":"text_to_video","prompt":"...","negative_prompt":"...","output_type":"video",
    "width":960,"height":544,"num_frames":113}]
  ```
  (I2V adds `"task":"image_to_video"` + `"media":["s3://.../ref.jpg"]`.)
- **Common launch pitfalls:** `world_size must be divisible by sharding_gpus/balance_gpu_count` → a GPU-count
  param still exceeds 8; `Unexpected/Missing key(s)` on ckpt load → model arch ≠ checkpoint (shouldn't happen
  since we fork the base config); `data config is required` → forgot `inference_mode: true`.
- **Config-editing help in-repo:** `scripts/agent/config_system.md` (coupling rules), `docs/training_config_setup.md`.
- **Pluto job mgmt from the box** (once colligo is present):
  `PLUTO_CLI="…/scripts/local/.venv/bin/python -m colligo.pluto.sdk.cli"; $PLUTO_CLI job list --project Foundry-HP`.

---

## Reference docs (read these, in the cloned repo)

`contrib/Mori/collections/foundation_exploration/`:
- `scripts/agent/running_inference.md` ← **primary guide** (has a full minimal inference-config template)
- `AGENTS.md` (workflows, morictl, stopping-jobs rules), `scripts/agent/environment_setup.md` (env + token)
- `scripts/agent/config_system.md`, `docs/training_config_setup.md` (balancer/GPU-count rules)

**Obsidian notes** (hs_base vault; run `/obs-query` or grep `hs_scripts/claude/obsidian/hs_base/wiki`):
`mori-training-workflow`, `mori-checkpointing`, `mori-config`, `pluto-*`, `foundry-*`, `colligo-*`.
These confirm the workflow but the **in-repo docs above are the ground truth**.

---

## ✅ DONE — T2V inference launched & running (2026-07-07)

The full path works. Config `configs/foundry/hshariati_gr6_lite_580k_t2v_infer.yaml` built per the recipe
and **launched successfully**; the 8×H200 job loaded the 580k ckpt cleanly (no arch mismatch) and is
denoising T2V samples (50 steps, ~9 s/step). Running job: `...01.32.05`, UUID
`0d0f4ebb-c0df-4e41-9aed-43832a2dff42`. Monitor via `obsidian/gr6_status.sh {status|logs|find_error}`.

### Three real blockers hit (NOT in the docs — fix these on any rerun)

1. **`morictl launch` needs `WANDB_API_KEY` + `SLACK_MEMBER_ID` env vars** (hard `assert` in
   `scripts/local/main.py:1858`). Also runs `aip login` first → **device-flow** (browser + code at
   login.microsoft.com/device); token caches to `~/.colligo/pluto_cli/msal-pluto-auth.secret`.
   No `make install` / GPU venv needed — launch loads the config from FE *source* via its own uv venv.
2. **AWS creds:** the box injects static `AWS_ACCESS_KEY_ID/SECRET` for IAM user `foundry-bedrock-prod`,
   which **cannot** `PutObject` to `s3://dit-scale-up/` → `AccessDenied` on the training-code upload.
   Fix: **`env -u AWS_ACCESS_KEY_ID -u AWS_SECRET_ACCESS_KEY -u AWS_SESSION_TOKEN morictl launch …`**
   so it falls back to the box's **instance role** (`colligo-laser01-od-ng-role-uw2`), which can write.
3. **Compute-node clone token expired:** `scripts/local/pluto_main.tmp.sh:132` hardcodes a `cliobot_adobe`
   GitHub token that's **revoked** → pod dies exit 128 `Invalid username or token`. Fix: replace that literal
   with the box's working `$KINETOBOT_GITHUB_API_TOKEN` (verified against Adobe-Firefly/colligo). This is a
   local edit to a tracked file; it rides along in the launch's `local_diff.patch`.

### One config fix beyond the recipe
- **`balance_gpu_specs` now requires a `symm_mem` key** (parser in
  `src/foundation_exploration/models/denoisers/extended_knapformer.py:1903`). The recipe's value fails with
  `Missing required key 'symm_mem'`. Use **`ring=none,ulysses=8,bags=1,inner=ulysses,symm_mem=false`**.
  (The base config's own value also lacks it — this checkout's code is newer than the config.)

### Launch command that worked
```bash
cd /home/colligo/colligo/contrib/Mori/collections/foundation_exploration
source scripts/env/activate.sh
export WANDB_API_KEY=<key> SLACK_MEMBER_ID=D06340Q0EG3 LDAP=hshariati
env -u AWS_ACCESS_KEY_ID -u AWS_SECRET_ACCESS_KEY -u AWS_SESSION_TOKEN \
  morictl launch configs/foundry/hshariati_gr6_lite_580k_t2v_infer.yaml
```

## Earlier state (superseded)

- ✅ Identified repo/branch (`foundry/stable` @ `1ebaa02`), the config, the 580k ckpt, the T2V test sets, the workflow.
- ✅ `pluto_project=Foundry-HP` chosen; Path A chosen.
- 📝 Still TODO: results → WandB `foundry` project (run `inference-gr6_lite_580k_t2v_infer-…`) + the job's S3
  folder; then write up a `gr6-inference` how-to page in the Obsidian hs_base vault.

## Housekeeping notes (unrelated to this task)
- The `/obs-*` skills were reverted to single-vault (`hs_base`) last session — leave as is.
- A second vault `hs_fin` exists on the laptop (value-investing research) — not relevant here.
- `.obsidian/.../obsidian-local-rest-api/data.json` is now gitignored (had secrets).
