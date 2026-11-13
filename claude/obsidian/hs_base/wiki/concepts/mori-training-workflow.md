---
type: concept
title: Mori Training Workflow
tags: [mori, training, workflow, morictl, torchrun, pluto]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/mori-docs.md]]", "[[raw/colligo/mori/collections/foundation_exploration/README.md]]", "[[raw/colligo/mori/collections/foundation_exploration/AGENTS.md]]", "[[raw/colligo/mori/collections/genai_foundation/README.md]]"]
---

# Mori Training Workflow

The end-to-end path from a training script to a monitored run on [[wiki/entities/pluto|Pluto]] with [[wiki/entities/mori|Mori]].

## 1. Install / set up the environment

- **Foundation Exploration (recommended path):** clone the Colligo repo, follow FE setup, then editable-install Mori: `pip install --no-deps -e <mori_repo_root>`. On GPU machines, `source scripts/env/activate.sh` (from the workspace root) activates the venv and puts `morictl` on `PATH`.
- **Standalone library dev:** clone the `ai-platform` repo → `make install` (torch/cuda variant via `make install-<env>`) → `source <mori_repo_root>/.venv/bin/activate`.
- Common gotcha: `ModuleNotFoundError: No module named 'torch'` → the env isn't activated.

## 2. Pick / edit a config

Training is config-driven (YAML per experiment). Before spending cluster GPUs, **validate**:

```bash
python scripts/misc/validate_config.py -c configs/genrender6/prod/<config>.yaml
morictl local_run --mutate-config configs/genrender6/prod/<config>.yaml   # local sanity
```

Config coupling and the sequence balancer are the top sources of failure — see [[wiki/concepts/mori-config]]. Use `--limit-samples 3` on all debug/validation/profiling runs to save time.

## 3. Launch

- **Direct / low-level:** `train.sh` → `torchrun` (or `mori.training.distributed.torchrun_handler`), e.g. `torchrun --nnodes=1 --nproc_per_node=2 train_morix.py ...`.
- **Collection CLI (`morictl`, foundation_exploration):** `morictl launch configs/.../<config>.yaml` (optionally `--limit-samples`). `morictl` also does `local_run`, `find_error`, and job-log helpers (exposed as a `morictl` MCP server too: `resolve_job_run_dir`, `search_logs`, `find_errors`, `job_summary`).
- **Older Run.ai path (legacy collections):** `genai_foundation` still documents Run.ai submission (`scripts/submit_runai.sh`, `submit-pytorch`, node pools, jack id) with an optional `MONITOR_JOBS` auto-resubmit watchdog.

> [!note] Run.ai vs Pluto
> Some collection READMEs pre-date the [[wiki/entities/pluto|Pluto]] migration and reference **Run.ai**. New work runs on Pluto; treat Run.ai instructions as legacy.

## 4. Checkpoints, monitoring, recovery

- Checkpoints stream to **S3** via the experiment manager; resume with `--resume s3://.../ckpt_step*.pth`, or rely on auto-recovery from the latest checkpoint in the log dir. See [[wiki/concepts/mori-checkpointing]].
- Profile hot loops on demand and via auto-tracing on large jobs; telemetry via OpenTelemetry. See [[wiki/concepts/mori-observability]].
- Debugging runbooks (FE): distributed hangs / NCCL timeouts, crashes (check **all** pods, not just pod-0), heartbeat warnings during data loading are **normal**. Evict stuck processes with `killall -9 /opt/venv/bin/python` and confirm GPUs are clear via `nvidia-smi`.

## Related
- [[wiki/entities/mori]]
- [[wiki/concepts/mori-config]]
- [[wiki/concepts/mori-checkpointing]]
- [[wiki/concepts/mori-parallelism]]
- [[wiki/concepts/mori-observability]]
- [[wiki/concepts/mori-pluto-agent]]
- [[wiki/concepts/pluto-job-lifecycle]] · [[wiki/concepts/pluto-cli-sdk]]
