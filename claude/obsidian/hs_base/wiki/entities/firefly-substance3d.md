---
type: entity
title: Substance 3D & Foundry 3D models
tags: [colligo, models, 3d, substance3d, foundry, mesh, texture]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/colligo/models/foundry/pipelines/gen6_mv2mesh/README.md]]", "[[raw/colligo/models/foundry/workers/AGENTS.md]]"]
---

# Substance 3D & Foundry 3D models

Colligo's **3D generation** model packages — creating meshes, textures, and materials from images or
multiview inputs. Two related package groups under `models/colligo/models/`:

## substance3d
The Substance 3D suite:
- **MeshLRM** / **MinLRM** — Large Reconstruction Models for mesh generation (with matching pipelines).
- **Materia Carbon** — texture generation.
- **material_super_resolution** — upscaling material maps.
- **ibl_post_process**, **lagrange_meshing** — IBL post-processing and meshing utilities.

## foundry (3D workers/pipelines)
Gen6 3D pipelines for Foundry Studio:
- **im2mv** — image-to-multiview.
- **mv2mesh** — multiview-to-mesh (4-6 RGBA views → GLB) using **TripoSG** (DiT denoiser + TripoSG VAE +
  DINOv3), with generation and SD-Edit-style refinement modes; async endpoint `v1/mv2mesh/generate-async`;
  `custom_pyenv: foundry_mesh3d`.
- **mesh2tex** — mesh-to-texture.
- **gen6_im2mv** / **gen6_mv2mesh** / **gen6_mesh2tex** pipelines chain these into full image→3D flows.

Sibling: **filix3/img23d** provides image-to-3D via the Filix3 stack, and
**spatial_generation/generation_3d** does gen6 3D image generation.

Foundry generative 3D pipelines must attach `FoundryGenerationMetadata` on ACP upload (see the Foundry
workers convention in [[wiki/concepts/colligo-models]]).

## Related
- [[wiki/concepts/colligo-models]] — the catalog this belongs to.
- [[wiki/concepts/colligo-inference]] · [[wiki/entities/colligo]]
