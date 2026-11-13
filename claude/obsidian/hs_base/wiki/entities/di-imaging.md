---
type: entity
title: DI Imaging (Digital Imaging)
tags: [colligo, models, digital-imaging, editing, masking, multiedit, flagship]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/colligo/models/di_imaging/README.md]]", "[[raw/colligo/models/di_imaging/multiedit/aidoc/README.md]]", "[[raw/colligo/models/foundry/workers/AGENTS.md]]"]
---

# DI Imaging (Digital Imaging)

The **Digital Imaging** model suite — Firefly's image *editing* stack (as distinct from pure
generation) — served from `models/colligo/models/di_imaging/` in [[wiki/entities/colligo|Colligo]],
owned by the co-di team.

## What it serves

A broad collection of editing, masking, and enhancement workers:

- **MultiEdit** (`multiedit/`) — the generative editing pipelines: **MultiDiffusion**, **Object
  Stitch**, **Generative Erase**, **Generative Expand**, plus envirofill. Built from adobeone
  autoencoder/autodecoder, a diffusion denoiser, T5, and a refiner.
- **gen_upscaler** — generative upscaling (caption + CLIP + T5 + tile models).
- **GR6 / lightshop** (`gr6/`) — relighting and interactive "lightshop" rendering (DiT + light encoder
  + VAE decoder + VLM encoder).
- **harmonization** / **parametric_harmonization** — compositing harmonization.
- **Masking & selection** — `sam2`, `select_subject_v4`, `material_selection`, `supermasking`,
  `mfm_masking`/`mfm_backbone`/`mfm_task` (multi-function masking), `generic_segformer`,
  `portrait_segformer`, `florence2`, `gem_vlm`.
- **matting / trimap**, **depth_estimation**, **esrgan** (super-res), **cmgan**, **clio_erase**,
  **body_parser**, **svd**, **urm**, **refine_bundle**, **nsfw**.

The public customer-facing endpoints for many of these live in the `compare/` v1/v2/v3 endpoint layer
(`images/fill`, `expand`, `harmonize`, `masking/*`, `structure/depth|edge`, etc.).

## Related packages
- **ffent** — Firefly Enterprise MultiEdit, the enterprise variant of the multiedit stack (pixelperfect,
  objectcomposite, objectstitch).
- **recolor**, **masking**, **text_effects**, **ff_image_ops** — sibling image-editing packages.

## Related
- [[wiki/concepts/colligo-models]] — the catalog this belongs to.
- [[wiki/entities/firefly-clio]] — the generation stack DI edits build on.
- [[wiki/concepts/colligo-inference]] · [[wiki/entities/colligo]]
