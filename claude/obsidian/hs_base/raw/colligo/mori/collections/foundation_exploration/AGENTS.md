# AI Agent Workflows

## Environment Setup

**When to use:** If you encounter `ModuleNotFoundError` for `torch` or any other Python package, activate the environment first.

This virtual environment is automatically activated when using `source scripts/env/activate.sh` on GPU machines.

**IMPORTANT for agents:** `source scripts/env/activate.sh` must be run from the workspace
root directory. If `which morictl` returns empty after sourcing, verify your working
directory is correct.

**Common issues:**
- `ModuleNotFoundError: No module named 'torch'` → Run the activation command above
- `pytest` or other tools fail with import errors → Activate the environment first
- Tests cannot import `foundation_exploration.*` modules → Activate the environment
- `LDAP not set` from `morictl find_error` → Run `export LDAP=<user_ldap>` (not set by `activate.sh`)
- `rg: command not found` → Use `grep` instead; ripgrep is not installed on all GPU machines

## Branch And PR Conventions

- Prefix agent-created branch names with the current user's LDAP, for example `seethara/<topic>`.
- When the LDAP is known from the user or environment, use that LDAP as the branch prefix instead of a generic name.
- Start PR titles with `[FE]` for Foundation Exploration changes unless the work is specifically Gen6-focused.
- Start PR titles with `[Gen6]` for Gen6-specific changes such as Gen6 configs, training flows, or Gen6-only infrastructure.

## MCP Tools (morictl)

When the `morictl` MCP server is connected (configured in `.claude/settings.json`), prefer
calling these tools over reading `scripts/local/main.py` or running CLI commands manually:

| Tool | What it does |
|---|---|
| `mcp__morictl__extract_job_id` | Normalize a job URL or UUID to just the UUID |
| `mcp__morictl__resolve_job_run_dir` | Resolve job ID → `/logging-fs/.../run-N` log path |
| `mcp__morictl__get_latest_run_number` | Find the latest run-N in a log directory |
| `mcp__morictl__list_pods` | List pod directories (rank + path) in a run |
| `mcp__morictl__search_logs` | Regex search across job logs (ripgrep/grep) |
| `mcp__morictl__find_errors` | Find tracebacks, segfaults, OOM, NCCL errors |
| `mcp__morictl__job_summary` | Return the job summary HTML URL |

These wrap the same functions in `scripts/local/main.py` — no duplication, no code reading needed.

## Available Workflows

**Launch and Debug Training Jobs** → `scripts/agent/debug_training_crashes.md`
- Use when: User provides a config and asks to launch/debug training
- Covers: `morictl launch`, `morictl find_error`, job monitoring, common errors
- Key insight: Heartbeat warnings during data loading are NORMAL - don't terminate early!

**Debugging Distributed Training Hangs** → `scripts/agent/debugging_distributed_training_hangs.md`
- Use when: Training hangs, NCCL timeouts, no progress for extended period
- Knowledge base: `scripts/agent/common_root_causes.md`

**Debugging Training Crashes** → `scripts/agent/debug_training_crashes.md`
- Use when: Training starts but crashes during forward/backward pass
- Key insight: Check ALL pods for errors - the first crash may not be on pod-0!

**Environment Setup** → `scripts/agent/environment_setup.md`
- Use when: New user needs to set up development environment
- Covers: Environment variables, morictl installation, interactive vs GPU setup, common issues
- Key insight: Choose Path A (interactive) for new users, Path B for direct GPU training

**Updating Dependencies** → `scripts/agent/updating_dependencies.md`
- Use when: User needs to add/update Python packages or Model Hub models
- Covers: Editing requirements.yaml, running make lock, testing changes, common scenarios
- Key insight: Always commit both requirements.yaml AND lock.yaml together

**Fine-Tuning with Custom Data** → `scripts/agent/finetuning_with_custom_data.md`
- Use when: User wants to fine-tune the prod model on a specific data shard or custom dataset
- Covers: Creating data configs, forking prod training configs, local validation, cluster launch, common errors
- Key insight: Always validate locally with `--mutate-config` before launching on the cluster

**LoRA Fine-Tuning** → `configs/genrender6/lora/LORA_CONFIG_TUTORIAL.md` (tutorial), `docs/lora/lora_design.md` (design)
- Use when: User wants to set up or debug LoRA (Low-Rank Adaptation) fine-tuning on a pre-trained base model
- Covers: Base checkpoint loading, freezing base model, LoRA config (rank/alpha/strategy/targets), EMA, GPU scaling, checkpoint resume
- Key insight: EMA must be disabled (`ema_start_step: 999999999`) — it clones the entire denoiser, doubling memory and risking FSDP2 DTensor corruption
- Key insight: LoRA bank must be FSDP-sharded BEFORE the main model; `reset_parameters()` must be called after `apply_sharding()`

**Config System (Gen6-focused)** → `scripts/agent/config_system.md`
- Use when: User is editing training configs, especially Gen6 experiment configs
- Covers: Config section coupling rules, validation sequence, and common config failures
- Key insight: Run `python scripts/misc/validate_config.py -c configs/genrender6/prod/<config>.yaml` before launch

**Running Inference Jobs** → `scripts/agent/running_inference.md`
- Use when: User wants to run inference/generation with a checkpoint without training
- Covers: Forking prod config, setting inference_mode, scaling GPU counts, configuring datasets and samplers
- Key insight: Set `train.inference_mode: true` and adjust all `balance_gpu_count` / `sharding_gpus` to match your node count

**V2V / GenProp → SSR Evaluation Pipeline** → `scripts/agent/v2v_ssr_eval_pipeline.md`
- Use when: User wants to launch a V2V or GenProp inference job, build an SSR eval set from the results, and run SSR inference
- Covers: Launching source inference, locating data.json, running ssr_update_config.py, updating SSR config, launching SSR inference
- Key insight: All eval set JSONs use V2 format (ConversationalBuilderDataset). The mode (--v2v vs --genprop) determines the SSR builder and conditioning fields.
- Key insight: `gen6_ssr_student.yaml` enables **both** V2V and GenProp SSR datasets in `inference_mapping` by default. Before launching SSR, comment out the non-requested mode so only one dataset runs (see Step 6c in the pipeline doc).

**Converting V1 JSON to V2 JSON** → `scripts/agent/converting_v1_to_v2_json.md`
- Use when: User has an X2XDataset JSON (V1) and wants to convert it to ConversationalBuilderDataset format (V2)
- Covers: Running the converter script, manual conversion for unsupported tasks, creating the YAML dataset snippet
- Key insight: V1 uses positional `media[]` with meaning from `task`; V2 uses named conditioning fields matching the builder's `Conditioning` Pydantic model

**Creating Agent-Friendly Design Docs** → `scripts/agent/creating_design_docs.md`
- Use when: Writing architecture docs, design specs, or technical documentation
- Covers: Quick Reference structure, Table of Contents, Implementation Notes, before/after examples
- Key insight: Front-load critical info in first 60 lines - agents get 80% of context in 7% of document

**Creating a New Training Recipe** → `scripts/agent/benchmark_inference_step.md`
- Use when: User wants to create a new morictl-launchable recipe (custom trainer, benchmark, evaluation, etc.)
- Covers: Recipe interface, required YAML stubs, loading the denoiser with FSDP2, common pitfalls
- Key insight: `train:` and `checkpoint.cleanup` stubs are always required; use `${oc.env:S3_EXPERIMENT_FOLDER}/model-checkpoints/` for prefix, not `null`

**Optimizing Data Layouts** → `scripts/agent/optimizing_data_layouts.md`
- Use when: User provides a training run log path and wants to balance `data.layout` or reduce VAE/balancer load imbalance
- Covers: Parsing ORI_LOADS and REDIST_LOADS from `pod-*/main_scripts/1/current`, mapping layout to ranks, minimizing max REDIST_LOAD across pods
- Key insight: Minimize max REDIST_LOAD across all pods; use max ORI_LOAD over the run (~4 logs) to estimate cost per dataloader slot

**Parameter Search** → `scripts/agent/parameter_search.md`
- Use when: User wants to sweep/search over training parameters by running multiple configs and comparing metrics
- Covers: Auto-diffing config variants, launching sequential sweeps, collecting wandb metrics, generating comparison reports
- Key insight: User provides config YAML paths + wandb project; tool auto-detects varying parameters and runs overnight unattended

**FE Logging System** → `scripts/agent/logging_system.md`
- Use when: Editing training logs, adding `[fe-log]` lines, or debugging with `felogs`
- Covers: Curated vs raw logs, `felogs`, and which lines should be marked `[fe-log]`
- Key insight: Important, stable, grepable user-facing lines should be prepended with `[fe-log]`

**Stop Job After N Steps** — inline workflow (no external doc)
- Use when: User wants to automatically stop a running Pluto job after it reaches a target training step
- Input: One or more job UUIDs and a target step count (e.g., "stop after 200 steps")
- Procedure:
  1. Resolve each job's log directory using `morictl job_summary` (which prints the log path) or by listing `/logging-fs/logs/pluto/jobs/<ldap>/`
  2. Resolve each job's name using `$PLUTO_CLI job list` and matching the UUID
  3. Find the training log at `<logdir>/run-<N>/pod-0-*/main_scripts/1/current`
  4. Poll the log every 30 seconds, extracting the latest step from lines matching `[fe-log] [train] step=<N>`
  5. When a job's step >= target, stop it with `$PLUTO_CLI job stop <job-uuid>`
  6. Report each stop event and exit once all monitored jobs are stopped
- Key insight: Jobs may take a while to start producing `[fe-log] [train]` lines (compilation/warmup phase shows step=0). Do not treat step=0 as "done" — keep polling until real training steps appear and reach the target.

**Orion/Styx Services Image, Export & Deployment** → `scripts/agent/orion_services_image_and_deployment.md`
- **Naming:** "Orion" is the old name; "Styx" is the current name — they refer to the same inference serving platform. Both names appear in configs, CLI flags, S3 buckets, and docs.
- Use when: Building the inference Docker image, exporting a model checkpoint for Orion/Styx, creating/updating a deployment, checking build/deployment status, or testing a pipeline locally with `orion run`
- Covers: Getting a bearer token from FEDemo, `make services-environment`, checking build status, `orion deploy create`, verifying startup logs, local testing with `orion run`, and Styx deployment
- Key insight: Always start by asking the user to run `copy(adobeIMS.getAccessToken().token)` in the FEDemo browser console to get a fresh `ORION_API_TOKEN`; tokens expire after 24 hours

# Coding Style

**Detailed coding guidelines** → `scripts/agent/code_style.md`

Before commit and push, run `make lint` and `make type-check`. Activate mori-venv by `source scripts/env/activate.sh` before type-check.

Key highlights from the style guide:
- **Strong typing always** — All function arguments and return values must be typed
- **Early returns** — Prefer early exits over nested conditionals
- **No `elif`** — Use `match`/`case` or early returns instead
- **Functional patterns** — Pure functions for logic; side effects at the edges
- **No nested functions** — Extract to module-level functions with explicit arguments
- **Prefer Pydantic over dicts** — Use typed models for structured data

For full details on architecture, control flow, typing, error handling, and more, see `scripts/agent/code_style.md`.

## Distributed Training - Barrier Rules

**NEVER create conditional barriers based on process-divergent state.**

When using `torch.distributed.barrier()` or any collective operation, ALL ranks must call the same barriers in the same order. Conditional barriers based on local state (e.g., "files exist on this node") cause **barrier mismatch** bugs that are extremely difficult to debug.

**BAD - Conditional barrier:**
```python
if files_exist_locally:
    pass  # No barrier - fast path
else:
    download_files()
    dist.barrier()  # Only called when files missing!
```

If some ranks have cached files and others don't, they call different numbers of barriers. Rank A's barrier N may match Rank B's barrier M, causing incorrect synchronization.

**GOOD - Unconditional barrier:**
```python
if not files_exist_locally:
    if local_rank == 0:
        download_files()

# Always synchronize - barrier count must be identical across all ranks
dist.barrier()
```

**Key principle:** The number and order of collective calls must be deterministic and identical across all ranks, regardless of local state differences.

# Knowledge Accumulation

When interacting with users, especially for debugging and developing new functionalities, it is helpful to record the thought process in a knowledge base. The knowledge base is located at `scripts/agent/`. When implementing new functionalities, put the design info in the knowledge base as a new file and update the ToC file `scripts/agent/toc.md` to index it.


# Important Info - Training Job Structure

## Finding Job Logs - ALWAYS START HERE

**Fastest path — use the `ls` command `morictl launch` prints.** Job names start with a
deterministic 12-char hex slug (`{slug}-{short_name}-{tag}-{timestamp}`), and Pluto reuses that
slug as the pod-name segment, so the log dir is uniquely globbable. `morictl launch` prints a
ready-to-run line like:
```bash
# (valid once a pod starts; LDAP must have been set at launch)
ls -dt /logging-fs/logs/pluto/jobs/<ldap>/pluto-prod-<ldap>-<slug>*/run-*/
```
If you have that line from the launch output, just run it. The methods below are for when you
only have a job UUID/URL.

**When the morictl MCP server is connected, use the MCP tools directly:**
- `mcp__morictl__find_errors` — searches all pods for tracebacks, segfaults, OOM, NCCL errors
- `mcp__morictl__resolve_job_run_dir` — resolves a job UUID/URL to its `/logging-fs/.../run-N` path

**Fallback (no MCP):** run the CLI manually:
```bash
cd /mnt/localssd/colligo/contrib/Mori/collections/foundation_exploration
source scripts/env/activate.sh
export LDAP=<user_ldap>   # REQUIRED — morictl find_error needs this
morictl find_error <job-uuid>
```

These find the log directory path (e.g., `/logging-fs/logs/pluto/jobs/<user>/<job-name>/`),
search for errors across all pods, and work with job UUIDs from ai.corp.adobe.com URLs.

**If `find_error` fails** (e.g. `IndexError: pop from empty list` for freshly launched jobs):

```bash
# Use Pluto CLI to get pod names directly
PLUTO_CLI="scripts/local/.venv/bin/aip"
$PLUTO_CLI job list-pods <job-uuid> --project asml-foundation
# Output: 0,pluto-prod-<user>-<truncated-name>-<hash>-0

# Derive log path: strip trailing "-N" from pod name
# Log dir: /logging-fs/logs/pluto/jobs/<LDAP>/<pod-name-without-rank-suffix>/run-N/
ls /logging-fs/logs/pluto/jobs/$LDAP/<pod-prefix>/
```

**Log search note:** `rg` (ripgrep) is **not installed** on all GPU machines. Always
fall back to `grep` for log searching in agent workflows.

## Job Summary URL (Experiment Manager Page)

**With MCP:** call `mcp__morictl__job_summary` with the job UUID or URL.

**Fallback (no MCP):**
```bash
morictl job_summary <job-uuid-or-url>
morictl job_summary <job-uuid> --run_number 2  # specific run
```

The URL format is: `https://dit-scale-up.s3.us-west-2.amazonaws.com/fe-experiments/<job-name>/logs/<uuid>/<run>/index.html`


## Job Log Structure

Jobs may have **multiple runs** (run-1, run-2, etc.) if they were restarted or auto-recovered. When analyzing logs:

1. First list available runs:
   ```bash
   ls <logdir>/
   ```

2. **Ask the user** if they want to analyze the latest run or a specific run number.

3. Each run has multiple pods with timestamps:
   ```bash
   ls <logdir>/run-1/
   ```

## Quick Commands

```bash

# Setup dependencies for the first time 
make install 
source scripts/env/activate.sh

# IMPORTANT: Refer to docs/training_config_setup.md before setting up training configs for training jobs!
# Misconfigured balancers can cause memory errors, reduce efficiency and waste GPU hours.

# Launch remote training on Pluto
cd /mnt/localssd/colligo/contrib/Mori/collections/foundation_exploration
morictl launch configs/path/to/config.yaml

# Launch with preemptible allocation (cheaper, can be terminated anytime)
# Can set in config (job_priority: preemptible) or override via CLI flag:
morictl launch configs/path/to/config.yaml --preemptible

# Launch preemptible with auto-requeue (auto-restarts if preempted)
morictl launch configs/path/to/config.yaml --preemptible --auto_requeue

# Pluto Resource Role(s) for S3 access are read from launch.roles in the YAML
# config (string or list of role names/UUIDs). Defaults to asml-data-access-role
# when unset. Example:
#   launch:
#     roles:
#       - asml-data-access-role
#       - adobe-soda-readonly

# IMPORTANT: When modifying configs for quick tests:
# - OK to reduce num_nodes, but NEVER below sharding_gpus or balance_gpu_count
# - NEVER modify sharding_gpus, sharding_num_gpus, or balance_gpu_count - models are sized for these
# - total GPUs (num_nodes * num_gpus) must be >= max(sharding_gpus, balance_gpu_count)
# - Look for these config keys: sharding_gpus, sharding_num_gpus, balance_gpu_count, auto_balance_prompts
# - Example: sharding_gpus: 64 means minimum 8 nodes with 8 GPUs each

# Default checkpoint config when NOT resuming from a checkpoint:
# checkpoint:
#   prefix: ${oc.env:S3_EXPERIMENT_FOLDER}/model-checkpoints/
#   resume_from:
#     path: null
#     strict: true
#     use_s5cmd_download: true
#     ema_backward_compatibility: "none"
#     training_state:
#       data_module_state: false
#       optimizer: true
#       lr_scheduler: true
#       ema: true
#       train_step: true
#   cleanup:
#     keep_ckpt_step_div_by: 5000

# launch local training
morictl local_run configs/path/to/config.yaml

# launch local training for debug a training config designed for remote
morictl local_run --mutate-config configs/path/to/config.yaml

# Find job logs - PREFERRED METHOD (get UUID from ai.corp.adobe.com URL or launch output)
morictl find_error <job-uuid>

# Job management - use the venv in scripts/local
# IMPORTANT: The CLI expects a job UUID, not the pluto-prod-* job name!
PLUTO_CLI="/mnt/localssd/colligo/contrib/Mori/collections/foundation_exploration/scripts/local/.venv/bin/aip"

# List YOUR jobs (defaults to current user)
$PLUTO_CLI job list --project <project-name>

# List ALL users' jobs in a project (requires --all flag with --project or --initiative)
$PLUTO_CLI job list --all --project <project-name>

# Filter jobs by status (running, stopped, failed, queued, etc.)
$PLUTO_CLI job list --all --project <project-name> --status running

# Filter jobs by specific owner
$PLUTO_CLI job list --owner user@adobe.com --project <project-name>

# Filter running jobs by node count (e.g., jobs with 8+ nodes)
# Save to temp file first, then filter with awk (column 5 is node count)
$PLUTO_CLI job list --all --project <project-name> --status running > /tmp/jobs.txt
awk -F',' '$5 >= 8' /tmp/jobs.txt  # Show jobs with 8+ nodes
awk -F',' '$5 == 8' /tmp/jobs.txt  # Show jobs with exactly 8 nodes

# List pods/nodes in a specific job
$PLUTO_CLI job list-pods <job-uuid-or-name> --project <project-name>

# Get job status by UUID
$PLUTO_CLI job status <job-uuid> --project <project-name>

# Stop a job by UUID (see "Stopping Jobs" section for rules!)
$PLUTO_CLI job stop <job-uuid> --project <project-name>

# Search for errors across ALL pods (adjust run-N as needed)
# NOTE: rg may not be installed on all machines — use grep as fallback
grep -E "Error during training|RuntimeError|ZeroDivision" /logging-fs/logs/pluto/jobs/<user>/<job>/run-1/pod-*/main_scripts/1/current

# Check training progress
grep -E "train step|train loss" /logging-fs/logs/pluto/jobs/<user>/<job>/run-1/pod-0-*/main_scripts/1/current | tail -10
```

## Stopping Jobs - IMPORTANT RULES

**Agents must follow these rules strictly when stopping jobs:**

1. **Jobs launched by the agent in current session:**
   - Can be stopped without asking when user has requested to "debug training" or similar
   - The debug workflow implicitly includes stopping failed/hung jobs to iterate
   - Keep track of launched job UUIDs so you can identify them later

2. **Jobs NOT launched by the agent** - Always double-check with user before stopping:
   - "I found job `<name>` (UUID: `<uuid>`). Are you sure you want me to stop it?"
   - Wait for explicit user confirmation before proceeding

3. **Never stop jobs based on assumption** - If unsure which job to stop, ask the user to clarify

**Example confirmation dialogue (for jobs not launched by agent):**
```
User: "stop the training"
Agent: "I see job FFP-64647-dit-...-2026.01.23 (UUID: 66b0f2e1-...) is running. 
        I did not launch this job in our current session. 
        Are you sure you want me to stop it? (yes/no)"
```

# S3 Credentials in training configs

The canonical contract for S3 credentials in training configs lives in
[`docs/s3_credentials.md`](docs/s3_credentials.md): the grouped
`launch.vault_secrets` shape and the `gateway_auth: <group>` alias that
morictl expands into the rendered genie config.

**Read that doc when:** the user reports an S3 403 from a training job; a
new data shard targets a Foundry/Styx/orion bucket; the user asks to
declare or change vault secrets; or you need to add `--vault-secret` flags
to an AIP CLI invocation. **Skip otherwise** — most prod buckets
(`dit-scale-up`, `genie-table`, `clineto`, `mldp-image`, ...) work via
ambient pod IAM creds with no `vault_secrets` block at all, and adding
one "just in case" slows job startup.

# ConversationBuilder Conditioning Version Policy

When modifying any `Conditioning` class on a `ConversationBuilder` implementation
(files under `src/foundation_exploration/services/conversation_builders/`), you **must**
bump the `version` class variable on the corresponding builder class.

## Versioning rules (semver)

| Change type | Version bump | Examples |
|---|---|---|
| Add an **optional** field (has a default) | **MINOR** (0.1.0 → 0.2.0) | Adding `style: str = "cinematic"` |
| Add a **required** field (no default) | **MAJOR** (0.1.0 → 1.0.0) | Adding `mask: Image` with no default |
| Remove a field | **MAJOR** | Removing `negative_prompt` |
| Rename a field | **MAJOR** | `first_frame` → `keyframe` |
| Change a field's type | **MAJOR** | `fps: float` → `fps: int` |
| Change a default value | **PATCH** (0.1.0 → 0.1.1) | `negative_prompt=""` → `negative_prompt="none"` |

## How to bump

1. Edit the `Conditioning` class fields as needed.
2. Update the `version = "X.Y.Z"` class variable on the **same builder class**.
3. Mention the version bump in your commit message.

If you are unsure whether a change is breaking, default to a **MAJOR** bump.

# Past Experiment Learnings

**Past Experiment Learnings** → `scripts/agent/past_experiment_learnings.md`
- Use when: Looking for insights from previous experiments
- Covers: Quality debugging strategies, task-specific findings, data mixing insights
