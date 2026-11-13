---
type: entity
title: Seedance (via fal.ai)
tags: [seedance, fal, video-generation, foundry, thd, third-party-models]
created: 2026-09-14
updated: 2026-09-14
sources: ["[[raw/thd-seedance-video-pipeline-learnings-2026-09]]"]
---

# Seedance (via fal.ai)

**Seedance** is ByteDance's reference-to-video generation model, consumed by Foundry as a **third-party
model hosted on fal.ai** — our pipeline builds the request; fal runs the model. It is the generator
behind the [[wiki/entities/thd-video|THD Video]] app.

## Versions & routing
- **Seedance 2.5** — `bytedance/seedance-2.5/reference-to-video` on fal. The default path (text +
  reference images, plus motion-bank clips).
- **Seedance 2.0** — `fal-ai/seedance-2/enterprise/reference-to-video`. Used **only** when the caller
  supplies a reference *video* (laxer content policy; duration cap 15s). Motion-bank **clips** stay on
  2.5; only a caller-supplied input video forces 2.0.

## Request surface (fal)
- `duration`: `"auto"` or an int **4–30s**. Per fal docs, **`"auto"` = the model sizes the clip to the
  prompt** (default). This matters a lot — see [[wiki/concepts/seedance-prompting|the rewriter/duration
  notes]]: our historical 10s cap was self-imposed, not fal's.
- `task` (reference/editing/extension), `resolution` (480p/720p/1080p), `aspect_ratio`
  (auto/21:9/16:9/4:3/1:1/3:4/9:16), `generate_audio`, `image_urls` (≤30), `video_urls` (≤10),
  `audio_urls` (≤10), `seed` (output-only).
- Endpoints/keys live in `seedance/config.py`; fal is reached with a direct `Authorization: Key <key>`
  header (a real external vendor, no Foundry gateway in front).

## Content policy
- Strict. On a policy rejection the pipeline retries with a declutter/paint-out edit
  (`DECLUTTER_EDIT_PROMPT`), then raises `SeedanceContentPolicyError` (whose `detail` may be a list).

## Related
- [[wiki/entities/thd-video]] — the app that drives Seedance
- [[wiki/concepts/seedance-prompting]] — the structured rewriter, roles & duration control
- [[wiki/concepts/foundry-third-party-models]] — how Foundry onboards 3P models
- [[wiki/entities/foundry]] · [[wiki/entities/foundry-studio]]
