# Mv2Mesh Pipeline

Multiview-to-mesh pipeline for generating 3D meshes from 4-6 RGBA view images using TripoSG.

## Features

- **Generation mode**: Create mesh from scratch from view images
- **Refinement mode**: Refine existing coarse mesh using view images (SD-Edit style)
- **Automatic view naming**: Default view names assigned based on image count
- **Flexible input**: 4-6 images with optional view labels

## Endpoint

**POST** `v1/mv2mesh/generate-async`

Async endpoint that returns immediately with a job ID. Poll for results.

## Request Format

```json
{
  "images": [<PublicBinary>, ...],  // 4-6 RGBA images
  "views": ["front", "right", ...],  // Optional view names
  "coarse_mesh_glb": <PublicBinary>,  // Optional for refinement
  "seed": 42,
  "num_inference_steps": 50,
  "do_classifier_free_guidance": true,
  "guidance_scale": 7.5
}
```

### View Name Defaults

When `views` is not provided, defaults are assigned based on image count:

- **4 images**: `[front, right, back, left]`
- **5 images**: `[front, right, back, left, top]`
- **6 images**: `[front, right, back, left, top, bottom]`

Valid view names: `front`, `right`, `back`, `left`, `top`, `bottom`

### Refinement Mode

To refine an existing coarse mesh:
1. Provide `coarse_mesh_glb` as a GLB binary
2. Worker samples the coarse surface and conditions diffusion on those points
3. Results in topology-preserving refinement of the input mesh

## Response Format

```json
{
  "mesh_glb": <PublicBinary>,
  "num_vertices": 123456,
  "num_faces": 234567,
  "refinement_mode": false,
  "seed": 42,
  "denoising_time_s": 12.3,
  "mesh_extraction_time_s": 3.4,
  "surface_sampling_time_s": 0.0
}
```

## Worker Configuration

Pipeline uses the `mv2mesh_v1` worker with:
- GPU: 1x A100 (78GB VRAM)
- Model: TripoSG (DiT denoiser + TripoSG VAE + DINOv3)
- Image size: 768x768
- Custom pyenv: `foundry_mesh3d`

## Example Usage

### Generation Mode (4 images, auto view names)

```python
from colligo.models.foundry.pipelines.gen6_mv2mesh.types import (
    Mv2MeshPipelineRequest,
)
from colligo.base.types.fastapi import PublicBinary

request = Mv2MeshPipelineRequest(
    images=[
        PublicBinary(name="file://front.png"),
        PublicBinary(name="file://right.png"),
        PublicBinary(name="file://back.png"),
        PublicBinary(name="file://left.png"),
    ],
    # views not provided - will use [front, right, back, left]
    seed=42,
    num_inference_steps=50,
)
```

### Refinement Mode (6 images with explicit views)

```python
request = Mv2MeshPipelineRequest(
    images=[...],  # 6 images
    views=["front", "right", "back", "left", "top", "bottom"],
    coarse_mesh_glb=PublicBinary(name="file://coarse.glb"),
    seed=42,
    num_inference_steps=30,  # Fewer steps for refinement
)
```

## Architecture

```
Mv2MeshPipeline
  ├─> Validates 4-6 images
  ├─> Assigns default view names if needed
  ├─> Validates view names (no duplicates, valid names)
  └─> Calls Mv2MeshWorker
        ├─> Loads & preprocesses images (resize to 768x768, RGBA split)
        ├─> [Optional] Loads & samples coarse mesh surface
        ├─> Encodes images with DINOv3 -> image embeddings
        ├─> [Optional] Samples coarse mesh -> point cloud conditioning
        ├─> Diffusion denoising with TripoSG DiT
        ├─> Decodes latents with TripoSG VAE -> triplane
        └─> Marching cubes extraction -> GLB mesh
```

## Related

- Worker: `models/colligo/models/foundry/workers/mv2mesh/`
- Model checkpoint: `triposg-dinov3-step80k` (S3)
- Custom pyenv: `envs/foundry_mesh3d.lock`

## Implementation Notes

This pipeline was migrated from `Gen6Shape3dPipeline` mesh refinement functionality. Key differences:
- Standalone pipeline (not part of shape3d package)
- Dedicated worker with `foundry_mesh3d` environment
- Simplified API focused on multiview-to-mesh use case
- Optional refinement mode vs. generation-only
