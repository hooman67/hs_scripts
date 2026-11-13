# Material Selection

Interactive material-aware segmentation service using AdobeSAM. Supports two modes:

- **click** — point-prompted SAM segmentation returning sigmoid score masks
- **auto** — grid/blue-noise/image-aware point sampling returning a uint8 segment label map

Both modes support optional ViTMatte-B refinement for sharper hard binary masks.

## Workers

| Worker | Type | GPU |
|---|---|---|
| `material_selection_model_adobe_sam` | GPU | 30 GB |
| `material_selection_refinement_bundle` | GPU | 4 GB |
| `material_selection_pipeline_v1` | CPU | — |

## Endpoints

- `POST /v1/masking/material-selection/click`
- `POST /v1/masking/material-selection/auto`

Images and masks are passed by reference using the two-step upload API:
```json
{"image": {"source": {"id": "<upload-id>"}}}
```

## Ported from

`models/colligo/models/filix3/pipelines/material_selection/` (branch `jotran/material_selection`)
