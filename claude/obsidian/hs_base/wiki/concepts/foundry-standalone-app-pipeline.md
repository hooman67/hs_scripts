---
type: concept
title: Foundry standalone-app pipeline (how to build one)
tags: [foundry, pipeline, inference, envelope, sam3, thd, v3]
created: 2026-09-14
updated: 2026-09-14
sources: ["[[raw/thd-seedance-video-pipeline-learnings-2026-09]]"]
---

# Foundry standalone-app pipeline (how to build one)

The shape of a Foundry **standalone app** that orchestrates a generation model, learned from
[[wiki/entities/thd-video|THD Video]]. Standalone apps are detached from the main Bazel build (own
Dockerfile + pyproject + Makefile) and consume monorepo libs as a wheel — see
[[wiki/concepts/colligo-managed-services|managed_services]].

## Structure (actors / http_api / helpers)
- **`actors/`** — the stateful bind targets: the **WebApp** (HTTP boundary), the **Pipeline** (CPU
  orchestrator), and **Workers**. Each has its own `.bind()`.
- **`http_api/`** — all FastAPI-facing pydantic types (the request/response **envelope**).
- Pure helpers at app root (`adapter_utils.py`, etc.); config via `inference.initialize(configs=…)`,
  never `os.environ` for secrets.

## The orchestrator pattern
`ThdVideoPipeline.execute` runs the stages in order: **SKU search → GPT rewriter → IP Guard → image
preprocessing → generation (Seedance via fal)**. The pipeline takes/returns encoded bytes
(`inference.Binary`); the **webapp** owns remote I/O (download at the endpoint, upload in
`on_store_result`). No ACP/presigned knowledge inside the pipeline.

## Unified inference envelope + async job model
- Speaks the shared Foundry **unified envelope** (`libs/foundry_http_envelope`): `input` (text + role-
  tagged image/video/audio refs), `controls` (resolution / aspectRatio / durationSeconds),
  `options` (promptRewrite mode, `debug` flags).
- **Async:** submit `POST /v2/video/generate` → `{jobId, links.result.href}` → poll until
  `succeeded|partial|failed`. References are uploaded first via `POST /v2/storage/image` (→ id) and
  passed as a `tempStorage` source. Made async precisely because synchronous multi-minute responses
  504 behind the customer gateway's 60s proxy timeout.
- **Per-image role** rides on `inference.Binary.metadata["role"]` — the webapp sets it from the request
  (`metadata={**meta, "role": item.role}`); the pipeline reads it. This is the production contract, and
  the exact seam eval drivers reuse (see [[wiki/concepts/foundry-eval-workflow]]).

## Product / motion bank
- SKU search resolves products in the prompt to bank entries and attaches a reference: a **grid**
  (Seedance 2.5, bound `@ImageN`) by default, or a **clip** (`@VideoN`) when `pickMotionVideo` is
  enabled (gated by a server allow-flag).

## SAM3 anonymize (image preprocessing)
- Preprocessing has two methods: **`remove`** (Nano-Banana paint-out; the deploy default) and
  **`anonymize`** (`Sam3Anonymizer`, SAM3 blur-in-place).
- `Sam3Anonymizer` (`image_preprocessing/anonymize.py`) calls the deployed **`sam2_image`** service:
  `POST /v2/storage/image` (upload) + `POST /v1/masking/sam3` (text prompts person/face/hand) → mask
  PNGs → local Gaussian blur composited over the plate.
- **Auth nuance (important):** use the **ethos-direct** host
  `https://sam2-image-dev.ethos851-stage-or2.ethos.adobe.net` with `x-api-key = foundry-services`
  (the IMS client_id) + a `foundry-services` IMS bearer. The `.private.adobe.io` **edge** rejects that —
  it needs a registered edge api-key (the reference `naou_image/sam3_client.py` uses `clio-playground-web`
  as the edge key plus a separate IMS identity). Wire the SAM3 host in the deploy runtime_config,
  modeled on the sibling `ip_guard` block.

## Related
- [[wiki/entities/thd-video]] · [[wiki/entities/seedance]]
- [[wiki/concepts/seedance-prompting]] — the rewriter stage
- [[wiki/concepts/foundry-dev-deploy]] — shipping it to dev
- [[wiki/concepts/colligo-managed-services]] · [[wiki/concepts/v3-inference-framework]]
- [[wiki/concepts/foundry-inference-auth-tokens]] · [[wiki/entities/foundry-gateway]]
