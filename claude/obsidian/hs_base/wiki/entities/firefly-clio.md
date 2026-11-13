---
type: entity
title: Firefly Clio (image generation)
tags: [colligo, models, firefly, clio, image-generation, diffusion, flagship]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/colligo/models/firefly/README.md]]", "[[raw/colligo/models/firefly/clio_tyom/README.md]]", "[[raw/colligo/models/firefly/sglang_diffusion/README.md]]", "[[raw/colligo/models/firefly/minimal_inference/README.md]]"]
---

# Firefly Clio (image generation)

The flagship Firefly **text-to-image / image-to-image** model family, served from
`models/colligo/models/firefly/` in [[wiki/entities/colligo|Colligo]]. "Clio" is the image diffusion
pipeline (text-to-image, image-to-image, text effects); the underlying generations are versioned as the
**CM / Clio / Gen** model line (`clio1..4`, `gen45`, `gr6`, `image5`, `cm5`).

## What it is

Per the package's own README, the three core pieces are:
- **clio** — the pipeline for image-based diffusion workflows (image-to-image, text-to-image, text effects).
- **diffusion** — the diffusion process itself (the DiT/UNet denoiser).
- **t5** — the T5 text encoder.

Around that core, `firefly/` hosts the full serving stack for a generation: text encoders
(`t5`, `gen45_text_encoder`), diffusion denoisers (`diffusion/clio1..4`, `diffusion/gen45`,
`diffusion/gr6`, `diffusion/image5`, `diffusion/lego`), VAEs and image-coding workers (`imcoding/*`,
`cmgan`), priors, identity encoders, upsamplers, and safety (`nsfw`, `nsfw_adobe_one`). Pipelines are
assembled under `firefly/pipelines/` (`imaging_v3`, `imaging_v4`, `cm5`, `upsampler`, `vision_sdk`).

## Serving & optimization

- Diffusion denoisers ship in multiple execution backends under `diffusion/eps/` — `torch`, `aot`,
  `aoti` (ahead-of-time inductor), and `trt` (TensorRT) — plus **FP8 quantization** via the AOTI
  framework with input-range calibration (see `clio_tyom`).
- **`sglang_diffusion`** serves OSS DiTs (FLUX.1-dev 12B, Qwen-Image 20B) through SGLang 0.5.9 with a
  single worker hosting text-encoder + DiT + VAE; weights are S3-staged via `hf_hub` stubs.
- **`minimal_inference`** is a linear, PyTorch-native prototyping harness with 100% component parity to
  the production pipeline — the recommended path for researchers to hand a model to the Clineto/Clio
  integration team (a merged minimal-inference PR + quality/latency baseline).

## Custom Models (clio_tyom / "Train Your Own Model")

`firefly/clio_tyom` is the "Firefly Custom Models" subtree — fine-tuning (DreamBooth, LoRA) on the CM3/
CM4/CM5 model line, plus inference optimizations (FP8 quantization + calibration via AOTI). It has an
extensive training/eval scripts tree (`training/`, `finetuning/`, `end2end_eval/`, `benchmark/`).

## Related
- [[wiki/concepts/colligo-models]] — the catalog this belongs to.
- [[wiki/entities/firefly-clineto]] — the video sibling (shares T5, VAE, NSFW workers).
- [[wiki/entities/flux]] — FLUX image DiT, also served via `sglang_diffusion`.
- [[wiki/entities/di-imaging]] — editing/DI stack that consumes Firefly generations.
- [[wiki/concepts/colligo-inference]] · [[wiki/concepts/colligo-training]] · [[wiki/entities/colligo]]
