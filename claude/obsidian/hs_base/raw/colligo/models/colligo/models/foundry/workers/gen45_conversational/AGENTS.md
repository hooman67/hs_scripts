# ADOBE CONFIDENTIAL
# ___________________
#
#  Copyright 2026 Adobe
#  All Rights Reserved.
#
# NOTICE: All information contained herein is, and remains
# the property of Adobe and its suppliers, if any. The intellectual
# and technical concepts contained herein are proprietary to Adobe
# and its suppliers and are protected by all applicable intellectual
# property laws, including trade secret and copyright laws.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from Adobe.

# Gen4.5 Conversational Worker — Agent Onboarding Guide

This document is the authoritative checklist for deploying a new Gen45Conv model
(new customer, new checkpoint, or new workflow variant). Follow the phases in order.

---

## Concepts

**Gen45ConvWorker** runs a 11.2B-parameter Diffusion Transformer conditioned on text
+ reference images. Each customer deployment ("worker") is a separate process with its
own checkpoint and `Gen45ConvConfig`.

**Pipeline routing** (`FoundryGen45ConvFlows.py`) decides, per incoming API request,
which worker to call. It lives in the `lego_v1` pipeline, not in this package.

---

## Phase 1 — Package the Checkpoint

The packaging script handles export → materialize → upload in one invocation.

**Prerequisites:**
- Training S3 credentials for the export step (set as env vars below)
- Default IAM role has access to `s3://colligo-dev-artifacts/`
- Active virtualenv: `source .venvs/foundry_gen45_conv/bin/activate`

**Run:**
```bash
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...

python models/colligo/models/foundry/workers/gen45_conversational/scripts/package_workflow.py \
    --checkpoint s3://<training-bucket>/<run>/checkpoints/ckpt_step<N>/ \
    --config <path-to-training-config.yaml> \
    --output /mnt/localssd/gen45conv_export/<customer>_step<N> \
    --name <customer>_step<N> \
    [--use-ema]    # add only for distilled/VMM checkpoints; non-EMA is the default
```

**EMA vs non-EMA:** non-EMA (`model.denoiser.*`) is the default. Pass `--use-ema`
only for distilled/student checkpoints (e.g. VMM 8-step) where EMA weights are preferred.

**Output:** `scripts/outputs/<name>/artifacts.json` — the manifest that describes the
S3 bundle locations.

---

## Phase 2 — Read EGG Parameters from Training Config

Open the training config YAML passed to the packaging script above and locate the
`ldm_inference_modules` section. Example:

```yaml
ldm_inference_modules:
  - name: image_to_image
    params:
      cfg_scale: 'lambda t: torch.full_like(t, 5.0)'
      eta: 'lambda t: torch.where(t > 200, 1.0, 0.0)'
      num_inference_steps: 50
      egg_min_cfg: 5.0
      egg_guidance_shifting: 13.0
      egg_energy_annealing: 0.4
      egg_match_energy: true
      egg_use_global_norm: true
```

Map these fields directly to `Gen45ConvConfig` fields (same names). Use the
training config as the single source of truth — do not guess or reuse another
customer's values.

---

## Phase 3 — Register the Worker

### 3a. Copy the manifest

```bash
cp scripts/outputs/<name>/artifacts.json \
   models/colligo/models/foundry/workers/gen45_conversational/checkpoints/<name>.json
```

### 3b. Add an enum variant — `types/__init__.py`

```python
class Gen45ConvWorkerName(str, Enum):
    ...
    GEN45_CONV_<CUSTOMER> = "gen45_conv_<customer>_worker"  # ADD
```

The string value must be globally unique across all workers in the repo.

### 3c. Add a worker deployment — `build.py`

```python
_deploy_gen45_conv_worker(
    Gen45ConvWorkerName.GEN45_CONV_<CUSTOMER>,
    artifact="checkpoints/<name>.json",
    worker_config=Gen45ConvConfig(
        parallel_cfg=True,                         # set False for 1-GPU deployments
        allowed_system_prompt_keys=["<key>"],      # see §System Prompt Keys below
        default_system_prompt_key="<key>",
        default_neg_prompt="...",                  # customer-specific negative prompt
        egg_min_cfg=<from training config>,
        egg_guidance_shifting=<from training config>,
        egg_energy_annealing=<from training config>,
        egg_match_energy=<from training config>,
        egg_use_global_norm=<from training config>,
        eta="lambda t: 1.0 if t > 200 else 0.0",  # match eta from training config
        default_num_inference_steps=<from training config>,
        default_cfg_scale=<cfg_scale constant from training config>,
    ),
    gpu_count=2,   # 2 required when parallel_cfg=True
)
```

**System Prompt Keys** — valid values trained into the model:

| Key | Workflow |
|-----|----------|
| `text_to_image` | T2I, no reference images |
| `gen_edit` | Instruct edit with reference images |
| `image_to_image_multiref` | Multi-reference image-to-image |

List only the keys this checkpoint was trained on in `allowed_system_prompt_keys`.

---

## Phase 4 — Wire Pipeline Routing

Pipeline routing lives in the `lego_v1` pipeline package, not here.

### 4a. Add to FOUNDRY_WORKERS — `lego_v1/build.py`

Add the new worker name to `FOUNDRY_WORKERS` in
`models/colligo/models/firefly/pipelines/lego_v1/build.py`:

```python
FOUNDRY_WORKERS: set[str] = {
    ...
    Gen45ConvWorkerName.GEN45_CONV_<CUSTOMER>,   # ADD
}
```

This is required for the lego pipeline to declare the worker as a dependency so
Rhode's worker registry can route calls to it.

**File:** `models/colligo/models/firefly/pipelines/lego_v1/utils/FoundryGen45ConvFlows.py`

### 4b. Add a flow constant

```python
_<CUSTOMER>_FLOW = Gen45ConvFlow(
    workflow_tag="<customer>_<variant>",           # short tag for logs/debug_data
    worker_name=Gen45ConvWorkerName.GEN45_CONV_<CUSTOMER>,
    system_prompt_key="<key>",
    uses_reference_images=<True|False>,
    rewriter=<CustomerRewriter() | None>,          # None = pass prompt verbatim
)
```

`rewriter=None` is acceptable when no prompt rewrite is needed. The prompt
rewriter implementation is a separate concern; assume it is provided by the
team owning that customer's skill bundle.

### 4c. Add a routing condition in `gen45conv_flow_for()`

```python
def gen45conv_flow_for(foundry_model_id: str, num_reference_images: int) -> Gen45ConvFlow | None:
    ...
    if foundry_model_id == "<customer_model_id>":
        return _<CUSTOMER>_FLOW
    if foundry_model_id == "<customer_model_id>" and num_reference_images > 1:
        return _<CUSTOMER>_MULTIREF_FLOW
    ...
```

The `foundry_model_id` string must match the value set in `SUPPORTED_FOUNDRY_WORKFLOWS`
in `FoundryWorkflow.py` (see §FoundryWorkflow registration below).

### 4d. Add to FoundryWorkflow registration — `FoundryWorkflow.py`

For **Gen45Conv-only models** (no DIT fallback), add to `SUPPORTED_FOUNDRY_WORKFLOWS`:

```python
SUPPORTED_FOUNDRY_WORKFLOWS["<customer_model_id>"] = {"t2i"}       # T2I only
# or
SUPPORTED_FOUNDRY_WORKFLOWS["<customer_model_id>"] = {"t2i", "ie"} # T2I + IE
```

For models that use the DIT pipeline for single-ref and Gen45Conv for multi-ref
(e.g. THD, TCCC), also add an entry to `FOUNDRY_MODEL_MAPPING` and
`FOUNDRY_PROMPT_SUFFIX_MAPPING` in `FoundryWorkflow.py`.

---

## Phase 5 — Validate

Validation is currently manual. Two checks are required before marking the
deployment complete:

**Check 1 — Inference result matches training path (model level):**

```bash
python scripts/verify_model.py \
    --model-path /mnt/localssd/gen45conv_export/<name> \
    --config <path-to-training-config.yaml> \
    --prompt "..." \
    --ref-images /path/ref1.jpg /path/ref2.jpg \
    --compare
```

Pass `--compare` to run both the training inference path and the packaged model
and verify pixel-level outputs are identical.

**Check 2 — Local worker matches model output (worker level):**

```bash
python scripts/verify_worker.py \
    --worker-name <Gen45ConvWorkerName value> \
    --prompt "..." \
    --ref-images /path/ref1.jpg /path/ref2.jpg
```

**Check 3 — Deployed endpoint matches local worker (endpoint level):**

```bash
python scripts/verify_endpoint.py \
    --token <x-user-token> \
    --foundry-model-id <customer_model_id> \
    --ref-images /path/ref1.jpg /path/ref2.jpg \
    --prompt "..."
# or with an eval JSON:
python scripts/verify_endpoint.py \
    --token <x-user-token> \
    --foundry-model-id <customer_model_id> \
    --eval-json /path/to/eval.json
```

All three checks must pass before the PR is merged.

---

## File Map

| File | What to change |
|------|----------------|
| `checkpoints/<name>.json` | Copy manifest from packaging output |
| `types/__init__.py` | Add `Gen45ConvWorkerName` enum variant |
| `build.py` | Add `_deploy_gen45_conv_worker()` call |
| `lego_v1/build.py` | Add worker name to `FOUNDRY_WORKERS` set |
| `lego_v1/utils/FoundryGen45ConvFlows.py` | Add flow constant + routing condition |
| `lego_v1/FoundryWorkflow.py` | Add to `SUPPORTED_FOUNDRY_WORKFLOWS` (and `FOUNDRY_MODEL_MAPPING` if DIT path also needed) |

## Export Utilities

`scripts/export_utils.py` is a **local copy** of `gr6_uber/scripts/export_utils.py`,
intentionally kept separate. Do not replace it with an import from gr6_uber.

**Why:** `gr6_uber`'s version tracks GR6-specific model changes (e.g. `sparse_attention`
injection for `ConversationalGR6Model`) that are incompatible with
`ConversationalGen45Model.Config`. Importing from gr6_uber will silently break on any
upstream GR6 model update that adds new denoiser params.

If you need to sync an upstream fix from gr6_uber's `export_utils.py`, copy the relevant
change here manually and verify it doesn't introduce GR6-specific denoiser param handling.

## Test Scripts

| Script | Level | What it tests |
|--------|-------|---------------|
| `scripts/compare_utils.py` | shared | Tensor/conversation diff helpers; YAML param loader |
| `scripts/verify_model.py` | 1 — model | Direct model load + inference; `--compare` for training-path parity |
| `scripts/verify_worker.py` | 2 — worker | NativeClient SDK; any worker via `--worker-name` |
| `scripts/verify_endpoint.py` | 3 — endpoint | HTTP generate-async against local service; any model via `--foundry-model-id` |
