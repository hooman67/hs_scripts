---
name: project_thd_model_comparison
description: "THD laundry-sink model bake-off: Seedance 2.5 vs 2.0 vs MiniMax H3 — how to prompt each, findings, gallery links"
metadata: 
  node_type: memory
  type: project
  originSessionId: d24f6783-62e3-43e4-9386-81e8e1cd0c68
  modified: 2026-08-28T07:40:51.054Z
---

Model bake-off on the FFDY-7304 laundry-sink spot (shots 1–11), done 2026-08-28. Same customer
storyboard as fixed input; **best-effort prep per model** (Hooman: "the true test is the best each
model can do with reasonable effort"), all at **~720p** (Seedance 720p, H3 native 768P — H3 has NO
1080p, so 720p is the only fair common res). See [[project_ffdy7304_laundry_sink]], [[project_thd_video_rewriter]].

**Prompting per model (learned this pass):**
- Seedance 2.5 & 2.0 = same family: `@Image1..N` ordered keyframes, "Use @ImageN as the LAST frame"
  end-state pin, ref-mode people-injection from person-free plate + couple bible. 2.0 adds
  `generate_audio=false`.
- MiniMax H3 (`minimax/h3/image-to-video`): **only 2 frames** (image_url + optional end_image_url), NO
  @Image grammar → prompts must be **natural-language motion**. `duration>=5` (rejects 4), 768P native,
  `prompt_expansion_mode=balanced`, `enable_safety_checker=true`. **H3 i2v injects prompt-described
  people** from a person-free plate too (couple stayed consistent — cream sweater / blue polo / grey hair).

**Findings:** establishing/product-only shots = a wash. All 3 inject the couple consistently. On
stills H3 was sharpest/cleanest and cheapest to prompt, no post-filter rejections; Seedance 2.5 has a
stochastic post-gen output filter on person shots (re-run clears it). Seedance keeps the edge for
precise multi-keyframe control + the video-edit overlay-cleanup route (H3's 2-frame API can't express).
Motion quality must be judged in the galleries, not from frames.

**Code:** `hs_scripts/claude/thd/model_comparison/` — `gen_multimodel.py` (multi-model driver, `EP`
endpoint map), `shots/S*_{sd25,sd20,h3}.json` (per-shot configs), `comparison_build.py` (stitches +
side-by-side), `build_model_galleries.py` (per-model galleries reusing gallery/build_gallery.py),
`COMPARISON.md`. Outputs in `/home/colligo/THD_laundry_sink_storyboard/gen_compare/{sd25,sd20,h3}/` and
`compare_out/`.

**Galleries (S3, IMS gateway foundry-aws-corp.adobe.io, prefix video_rewriter/compare/):**
side-by-side = `.../compare/sidebyside/gallery/index.html`; per-model = `.../compare/{sd25_720,sd20,h3}/gallery/index.html`.
