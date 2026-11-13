---
type: concept
title: Mori Observability (Profiler & OpenTelemetry)
tags: [mori, profiler, opentelemetry, tracing, pytorch-profiler, observability]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/mori-docs.md]]"]
---

# Mori Observability (Profiler & OpenTelemetry)

Performance and telemetry tooling in [[wiki/entities/mori|Mori]]: an on-demand profiler for hot loops plus OpenTelemetry instrumentation.

## On-demand profiler

Dynamic performance tracing built on **PyTorch Profiler** + `torch.cuda.memory`, capturing execution traces and memory use for specific training-loop sections.

**Enable** (env vars before training starts):
```bash
export USE_PROFILER=true
export PLUTO_NODE_RANK=${RANK}
export PROFILER_PORT=8003     # optional, avoids port conflicts
```
Foundation-Exploration models also set `enable_profiler` in the model config.

**Trigger tracing:**
- CLI (recommended): `aip job run-tracing <JOB-NAME> --project <PROJECT> --iteration 3`
- curl from the pod: `curl -X POST "http://localhost:8003/run_job/start_tracing" -d '{"iteration":"2","enable_cpp_memory":"false"}'`
- Params: `iteration` (1-5 recommended), `sample_total` (#ranks), memory toggles.

**Auto-activation:** large jobs (128+ GPUs, 1000+ iterations) auto-trace at iteration 1000 to catch bottlenecks without manual intervention.

The `aip job run-tracing` / curl path works through the in-job [[wiki/concepts/mori-pluto-agent|Pluto Agent SDK]] HTTP service.

**Output & viewing:** traces go to S3 + local. View via **TensorBoard** (in VS Code), **Perfetto/Chrome tracing** (upload `.json.gz` to perfetto.dev), or the **PyTorch Memory Visualizer** (`.pickle` snapshots). A trace-analysis tool (`profiler_processing`) supports post-processing.

## OpenTelemetry

Mori is instrumented with **OpenTelemetry** for training-job telemetry (one of the documented framework features; page under `mori/aidoc/open_telemetry.html`). Used alongside the profiler and [[wiki/entities/pluto|Pluto]]'s job observability.

## Related
- [[wiki/entities/mori]]
- [[wiki/concepts/mori-pluto-agent]]
- [[wiki/concepts/mori-training-workflow]]
- [[wiki/concepts/pluto-cli-sdk]] · [[wiki/entities/pluto]]
