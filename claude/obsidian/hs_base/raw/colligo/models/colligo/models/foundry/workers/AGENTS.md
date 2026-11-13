# Foundry Workers — Agent Notes

This file applies to all workers under `models/colligo/models/foundry/workers/`.

## ACP Metadata on Generative Pipelines

Any pipeline that generates content from a user prompt (text-to-video, image-to-video,
video-to-video, upsampling) **must** pass a `FoundryGenerationMetadata` object when
uploading to ACP. Missing metadata means Creative Cloud users see no generation context
on their assets (seed, prompt, model version, etc.).

**Rule:** if your pipeline calls `upload_video_to_acp()` or `upload_image_to_acp()` and
the request has a `prompt` and `seed`, always pass `generation_metadata=`.

```python
from colligo.models.foundry.metrics.utils import get_clean_application_version
from colligo.models.foundry.workers.common.acp_upload import FoundryGenerationMetadata, upload_video_to_acp

generation_metadata = FoundryGenerationMetadata(
    prompt=prompt,
    seed=seed,
    module="video_generation",       # "video_generation" | "video_upsampling" | "text2video"
    model_name="<your_model_name>",
    model_version=get_clean_application_version(),
    api_path="/v1/<your/endpoint>",
    width=width,
    height=height,
    duration=num_frames / fps,       # omit if not applicable
    fps=int(fps),                    # omit if not applicable
)
await upload_video_to_acp(
    video=video,
    creative_cloud_target=creative_cloud_target,
    workflow_name="<your_workflow>",
    generation_metadata=generation_metadata,
)
```

**Reference implementation:** `workers/gr6_uber/api_adapters.py` → `_encode_video_tensor()`

**Exempt pipelines** (post-processing, no prompt/seed): `depth_edge`, `video_concat`,
`video_composition`. These do not produce generative outputs so metadata does not apply.
