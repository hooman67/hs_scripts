---
type: source
title: Mori docs — AI Platform V3 portal
tags: [mori, docs, v3-portal, source]
created: 2026-07-05
updated: 2026-07-05
raw: "[[raw/mori-docs.md]]"
sources: ["[[raw/mori-docs.md]]"]
---

# Mori docs — AI Platform V3 portal

Summary of the official [[wiki/entities/mori|Mori]] documentation on the AI Platform **V3** docs portal, fetched 2026-07-05. This is where the in-repo `contrib/Mori/aidoc/*` move-notices point. Raw capture: [[raw/mori-docs.md]].

## Location & structure

Under `https://docs.ai.corp.adobe.com/v3/frameworks/training/mori/aidoc/`. Sibling training framework: **data_chef** ("Data Routing"). Pages: overview, contribution, tooling, parallelism, profiler, profiler_processing (trace analysis), dependency_management, s3_checkpointing, open_telemetry, release, blog (postmortems), internal.

## What each page gave us

| Page | Feeds wiki page |
|---|---|
| overview | [[wiki/entities/mori]], [[wiki/concepts/mori-architecture]], [[wiki/concepts/mori-training-workflow]] |
| parallelism | [[wiki/concepts/mori-parallelism]] (FSDP2, context parallelism, distributed attention; pipeline=no, tensor=WIP) |
| s3_checkpointing | [[wiki/concepts/mori-checkpointing]] (EXP_MANAGER, `--resume`, s5cmd, HSDP broadcast, throttling) |
| profiler + open_telemetry + tooling | [[wiki/concepts/mori-observability]] |
| internal/pluto_agent | [[wiki/concepts/mori-pluto-agent]] (HTTP-in-separate-process, REST endpoints, sync/async) |
| dependency_management | [[wiki/concepts/mori-dependency-management]] (requirements.yaml/lock.yaml, torch/cuda groups, S3-materialized) |
| contribution | WIP ("To be updated") — only "sharing a model" guidance |

## Fetch results

Fetched OK (HTML→markdown): README landing, overview, parallelism, internal/pluto_agent, s3_checkpointing, tooling, profiler, dependency_management, contribution. Not individually fetched: `profiler_processing`, `open_telemetry` (covered via overview/README references), `release`, `blog/index`, `internal/index`. No 404s encountered on the pages tried.

## Related
- [[wiki/entities/mori]]
- [[wiki/sources/mori-repo]]
- [[wiki/concepts/mori-parallelism]] · [[wiki/concepts/mori-checkpointing]] · [[wiki/concepts/mori-pluto-agent]] · [[wiki/concepts/mori-observability]] · [[wiki/concepts/mori-dependency-management]]
- [[wiki/sources/pluto-docs]]
