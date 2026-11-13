---
type: entity
title: Firefly Clineto (video generation)
tags: [colligo, models, firefly, clineto, filix, video-generation, diffusion, flagship]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/colligo/models/firefly/pipelines/clineto/README.md]]", "[[raw/colligo/models/firefly/minimal_inference/README.md]]", "[[raw/colligo/models/firefly/brewmaster/README.md]]"]
---

# Firefly Clineto (video generation)

The production Firefly **video generation** pipeline — text-to-video (T2V), image-to-video (I2V), and
video-to-video (V2V) — served from `models/colligo/models/firefly/pipelines/clineto/` (with the DiT
workers under `firefly/diffusion/clineto/` and the Filix video stack in `models/colligo/models/filix3/`).
The core denoiser is the **Filix2** DiT (project name "Clineto" for the integrated client pipeline).

## The pipeline (V1.8/V1.9)

A single production pipeline handles T2V/I2V/V2V; conditions feed a shared **DiT core**:
- **Text condition** — Prompt Forge V2 → prompt processor → **T5 encoder**.
- **Image condition** — AdobeOne image encoder → image NSFW (V7) → Dentro pre-processing.
- **Video condition** — image NSFW → VideoDepthAnything + edge → spatial encoder.
- **Core** — the **Filix2 DiT** denoiser (e.g. `filix2_t2v_prod1_9_540p_1_student_opt`).
- **Decoding** — dual **VAE decoder** → image NSFW → Dentro post → optional **SSR** (spatial super-res)
  → final video.

Model versions are selected by DiT worker name: `filix2_t2v_prod1_8_540p`, `..._prod1_9_540p`
(student/teacher), V2V (`filix2_v2v_prod1_8_540p`), RGBA (`filix2_t2rgba_prod1_8_540p`), and a
motion-brush variant. Because GPUs can't hold multiple large DiTs, only one DiT worker loads per job;
config files list the default worker and other jobs **swap** it via `debug_overrides.dit_model_name`
(VAE, prompt-forge, NSFW, T5 workers stay constant).

## Related packages
- **filix3** — the next-gen Filix3 generation stack (images/video/img23d/mirai/rgbx/upscalegs).
- **video** — post/ops (avatar, lipsync, background removal, uprez super-res, mask propagation).
- **foundry/workers/wan22** — WAN 2.2 video generation (base, distilled for Foundry Studio depth
  control, NBCU VACE upsampler) — a separate video model line also under `models/`.
- **firefly/minimal_inference** — the linear prototyping harness (T2V/I2V/V2V scripts) used to hand
  models off to the Clineto integration group.
- **firefly/brewmaster** — the eval portal used to compare Clineto video model versions.

## Related
- [[wiki/concepts/colligo-models]] — the catalog this belongs to.
- [[wiki/entities/firefly-clio]] — the image sibling (shares T5/VAE/NSFW workers).
- [[wiki/concepts/colligo-inference]] — worker/pipeline serving model.
- [[wiki/concepts/colligo-training]] · [[wiki/entities/colligo]]
