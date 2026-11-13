---
type: entity
title: FLUX (Colligo model package)
tags: [colligo, models, flux, image-generation, diffusion, oss-model]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/colligo/models/flux/colligo.yaml]]", "[[raw/colligo/models/firefly/sglang_diffusion/README.md]]"]
---

# FLUX (Colligo model package)

Support for **Black Forest Labs' FLUX** image diffusion transformer inside
[[wiki/entities/colligo|Colligo]]. The top-level `models/colligo/models/flux/` package is thin — a
public `types.py` and the core deps (`torch`, `transformers`, `safetensors`, `einops`,
`invisible-watermark`) — providing the FLUX model plumbing/weights used by other packages.

## How FLUX is served
- **`firefly/sglang_diffusion`** serves `black-forest-labs/FLUX.1-dev` (a 12B image DiT) via SGLang
  0.5.9 through `POST /v1/sglang_diffusion/black-forest-labs/FLUX.1-dev`. Weights are S3-staged (not
  pulled from HuggingFace at runtime) via an auto-generated `hf_hub` stub pinning `version_id` + SHA-256
  for deterministic, license-once, rate-limit-free cold starts.
- **`adobe_research/flux2_klein`** is a research package building on FLUX2 (Klein).

FLUX is the primary example of Colligo serving a third-party open-source foundation model alongside
Adobe's own [[wiki/entities/firefly-clio|Clio/Firefly]] models — useful for benchmarking and as a
3P option surfaced through the [[wiki/entities/firefly-firefall|Firefall]] gateway / auto-model-selector.

## Related
- [[wiki/concepts/colligo-models]] — the catalog this belongs to.
- [[wiki/entities/firefly-clio]] — Adobe's first-party image model family.
- [[wiki/entities/firefly-firefall]] — the 3P model gateway/router.
- [[wiki/concepts/colligo-inference]] · [[wiki/entities/colligo]]
