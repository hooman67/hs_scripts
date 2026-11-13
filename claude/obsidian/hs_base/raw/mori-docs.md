# Mori — AI Platform V3 portal docs (raw capture)

> **Provenance.** Fetched 2026-07-05 from the AI Platform V3 docs portal, Training Frameworks
> section: `https://docs.ai.corp.adobe.com/v3/frameworks/training/`. Content converted from HTML
> to markdown by the fetch tool and lightly condensed. **Immutable** — do not edit; re-fetch to
> refresh. Some pages were "To be updated" stubs at capture time (noted inline).

## Landing: Training Frameworks

Mori is Adobe's distributed training framework for the AI Platform. Sibling framework listed:
**data_chef** ("Data Routing"). Mori doc pages (all under `.../training/mori/aidoc/`):

| Topic | URL |
|---|---|
| Getting started (overview) | `mori/aidoc/overview.html` |
| Contribution guide | `mori/aidoc/contribution.html` |
| Tooling | `mori/aidoc/tooling.html` |
| Parallelism strategies | `mori/aidoc/parallelism.html` |
| On-demand profiler | `mori/aidoc/profiler.html` |
| Trace analysis tool | `mori/aidoc/profiler_processing.html` |
| Dependency management | `mori/aidoc/dependency_management.html` |
| S3 Checkpointing | `mori/aidoc/s3_checkpointing.html` |
| OpenTelemetry | `mori/aidoc/open_telemetry.html` |
| Install and release | `mori/aidoc/release.html` |
| Postmortems / blog | `mori/aidoc/blog/index.html` |
| Internal documents | `mori/aidoc/internal/index.html` |

## overview.html — Getting started

Mori is a distributed training library within Adobe's AI Platform, integrated into the
**Foundation Exploration** codebase but also usable as a standalone package.

Components: `mori.training` (core distributed training), `morix` (training accelerator /
utilities), Tools & Models, and **Collections** (organized project structures, e.g.
foundation_exploration).

Install paths:
- **Foundation Exploration users (recommended):** clone the colligo repo, follow FE setup, then
  `pip install --no-deps -e <mori_repo_root>` (editable).
- **Standalone lib dev:** clone the **ai-platform** repo, run `make install`
  (torch/cuda variants via `make install-<env>`), then `source <mori_repo_root>/.venv/bin/activate`.
- Verify: `pip list | grep mori` shows the editable path.

Dev workflow: editable install lets you set breakpoints in Mori; change deps in `pyproject.toml`
then `make lock`; **always commit the updated lock files** (`uv.lock` / `lock.yaml`).
To test local changes elsewhere: release a dev version of Mori, point the target env at it, launch.
Entry point `train.sh` launches distributed training via `torchrun` or the custom
`mori.training.distributed.torchrun_handler`. Mori integrates closely with the Compute Platform
(**Pluto**) for job scheduling/execution.

## parallelism.html — MoriX parallelism strategies

- **FSDP2 (primary/recommended):** shards params + gradients across devices to cut communication
  overhead; configured via `FSDP2ShardingConfig`; impl `mori.training._dev.plugin.fsdp2_plugin.FSDP2Plugin`.
  (FSDP v1 is deprecated.)
- **Context Parallelism (aka sequence parallelism):** partitions inputs across devices, each GPU
  handles a portion; for very long inputs (high-res images / video). Set `sp_size` (degree) and
  `token_budget` (max seq length).
- **Distributed Attention (in-house):** evenly shards input across all GPUs within a single node so
  each GPU processes equal-length input; supported, still evolving.
- **Pipeline parallelism:** not supported. **Tensor parallelism:** in progress.
- New strategies plug in via the **Strategy Pattern** — implement a new `Plugin`.

## internal/pluto_agent.html — Pluto Agent SDK

Lets a training framework running inside a Pluto job talk to the Pluto platform with minimal
impact. Runs an **HTTP service in a separate process** (Python multiprocessing) to avoid GIL
interference with training. Communication = multiprocessing queues + HTTP REST + JSON payloads.

Training-framework side:
- `agent.start_pluto_agent(port_number)`
- register sync/async handlers per task type
- call `agent.run_pluto_agent_handlers()` each iteration to process queued tasks
- report async results via `agent.send_pluto_agent_result()`

Pluto-platform side (REST):
- `GET /handlers` — list registered task types
- `POST /run_job/{handler_name}` — start a task (JSON payload)
- `GET /job_status/{task_id}` — check status
- `PUT /cancel/{task_id}` — cancel

Modes: **synchronous** (returns immediately) and **asynchronous** (returns task id; completion
reported later — e.g. snapshot creation). This is what backs `aip job run-tracing` and on-demand
profiling triggers.

## s3_checkpointing.html — S3 checkpointing

Save/load training checkpoints to/from S3 (default via AWS CLI; `s5cmd` optional via
`export USE_S5CMD=true`). Full access to allowlisted buckets like `s3://clio.corp.adobe.com`
needs no credentials.

- **Load / resume:** `torchrun ... train_morix.py --resume s3://clio.corp.adobe.com/<exp>/checkpoints/ckpt_step00000100.pth`.
  Auto-recovery: Mori auto-resumes from the latest checkpoint in the log dir.
- **Save:** set `export S3_BUCKET=...`, `export S3_PREFIX=...`, and `export EXP_MANAGER=true` in
  the Pluto script. The **experiment manager** watches the local checkpoint folder and uploads to
  S3 periodically (more robust than direct S3 writes; fresh checkpoints may lag).
- **Validate:** `python -m mori.training.utils.validate_checkpoint_integrity s3://.../path`.
- **S3 throttling at scale:** enable HSDP broadcasting (only rank 0 downloads, broadcasts to
  others); use pre-partitioned prefixes; enable checkpoint replicas across multiple prefixes.
- Support: `#mori-users` Slack (post job URL, error logs, log dir).

## tooling.html — Makefile / dev tooling

`make install` (venv + deps), `make lock` / `make lock-check` (uv.lock), `make lint`
(`ruff check . --fix` + format), `make lint-dev` (cross-platform, no fixes),
`make lint-check` (full type validation vs actual lib versions), `make test` (pytest),
`make build` (wheel), `make publish`, `make clean`. Strict type annotations enforced for new code.

## profiler.html — On-demand profiler

Dynamic performance tracing in MoriX using PyTorch Profiler + `torch.cuda.memory`.
Enable via env vars: `USE_PROFILER=true`, `PLUTO_NODE_RANK=${RANK}`, optional
`PROFILER_PORT=8003`. FE models also set `enable_profiler` in model config.
Trigger tracing:
- CLI (recommended): `aip job run-tracing <JOB-NAME> --project <PROJECT> --iteration 3`
- curl from pod: `curl -X POST "http://localhost:8003/run_job/start_tracing" -d '{"iteration":"2","enable_cpp_memory":"false"}'`
Params: iteration (1-5), sample_total (#ranks), memory toggles.
**Auto-activation:** large jobs (128+ GPUs, 1000+ iters) auto-trace at iteration 1000.
Output → S3 + local. View via TensorBoard (VS Code), Perfetto/Chrome tracing (`.json.gz` →
perfetto.dev), PyTorch Memory Visualizer (`.pickle` snapshots).

## dependency_management.html

Pre-compiled, version-locked deps: Python packages are built as artifacts and uploaded to S3
before training, decoupling deps from the Docker image.
- `requirements.yaml` — dependency constraints (source of version constraints).
- `lock.yaml` — materialized dep set: full transitive audit trail + CUDA/OS version constraints +
  S3 paths. "Makes dependencies part of the code" (diffable across git commits).
- Workflow: change deps → `make lock` → commit `lock.yaml`. At training startup `make env` creates
  a venv at `/mnt/localssd/mori-ven` and downloads pre-compiled deps from S3.
- **PyTorch/CUDA dependency groups** in `pyproject.toml`, e.g. `torch271-cu128` = PyTorch 2.7.1 +
  CUDA 12.8 (torch, flash-attn, flashattn-hopper, st_attn, deep-gemm, magi_attention, sageattention).
  Install: `pip install mori[torch271-cu128]`. Pin exact versions incl. build tags (`+cu128`).
- Rule: version constraints live in `requirements.yaml` (not `pyproject.toml`, except dep groups);
  deps + CUDA + OS versions are treated as code — use separate branches for different versions.

## contribution.html — (WIP at capture)

Mostly "To be updated". Only concrete guidance: sharing a model = PR implementing it under
`Mori/models`, clean up unused `use_xxx` variation flags, keep only necessary ones.
