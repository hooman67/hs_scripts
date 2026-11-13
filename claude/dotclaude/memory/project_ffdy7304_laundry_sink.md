---
name: project_ffdy7304_laundry_sink
description: "FFDY-7304: Glacier Bay laundry-sink storyboard → generated ~:60 video (customer stills, not sketches)"
metadata: 
  node_type: memory
  type: project
  originSessionId: d24f6783-62e3-43e4-9386-81e8e1cd0c68
  modified: 2026-08-28T17:12:08.793Z
---

Experiment **FFDY-7304** (started 2026-08-24): turn a Home Depot customer storyboard into a generated
~:60 promotional video, reusing the door-lock rewriter techniques ([[project_thd_video_rewriter]]).

**Product/deck:** Glacier Bay Drop-In Laundry Sink + RTA Cabinet with **CLICKREADY** tool-free assembly
(orange cam-lock connectors; 9-in/9-gal stainless basin; pull-down faucet; brushed-nickel hardware;
soft-close doors; 5 finishes; HD exclusive). Source = a **PPTX** of real shoot **stills** (a couple
assembling it), 8 slides, 12 shot series **1A–8B**. One continuous VO. NOT sketches, NOT a video.

**Locations (git rules):** code+text in repo `hs_scripts/claude/thd/FFDY-7304/` (`extract_pptx.py`,
`build_index.py`, `gen_shot.py`, `storyboard.json`=shot index+VO+specs, `storyboard_text.md`, `text/`,
`STORYBOARD_OVERVIEW.md`, `gallery/`); media (PPTX, `images/` stills, `gen/` videos, `gallery/assets/`)
in `/home/colligo/THD_laundry_sink_storyboard/` (NOT git). (An earlier Makita PDF was placed here by
mistake and removed.)

**Decisions (from Hooman):**
- Use the **customer stills directly** (i2v / cover_body / paint-out), NOT the sketch route — customer can
  supply either; here they gave photos. Sketchify only if ever needed.
- **Talent = an invented but CONSISTENT couple** (need not be real people, must stay consistent shot-to-shot).
- **Do the face-free product macros first** (3A click connectors, 5A faucet, 6A hardware, 7B hinge) — no R3.
- Source is **stills only, no video** → can't use rewriter_pipeline's frame-extraction; wrote `gen_shot.py`
  (stills→video: i2v single first frame + motion prompt, or ref ordered keyframes).
- **Separate gallery** from the door-lock one (don't pollute it). New S3 prefix
  `video_rewriter/laundry_sink/gallery/` (door-lock stays at `.../door_lock/gallery/`).

**Progress (2026-08-24): ALL 11 SHOTS DONE + assembled into a ~51s spot.** Gallery LIVE (35 sections,
tabbed, FINAL cut on top).
- **Face-free product macros (i2v, one still + motion prompt):** 3A click connector, 5A pull-down faucet
  (hand only), 6A brushed-nickel hardware, 7B soft-close hinge, 7A doors closing. All clean, no R3.
- **Person beats (the couple):** 1A assemble, 2A click panels, 4A stand up, 4B place basin, 8A woman turns
  on faucet, 8B hero. The invented couple (couple_bible.md) stays impressively CONSISTENT across all beats.
- **Final assembly:** `assemble.py` concats in VO order 1A→2A→3A→4A→4B→5A→6A→7A→7B→8A→8B → `final_spot.mp4`
  (1080p ~51s, no VO/audio yet — post).

**KEY FINDING — R3 blocks ALL photoreal humans in refs, even SYNTHETIC ones.** Feeding a nano-swapped
invented couple to Seedance i2v → content_policy_violation. So person beats use: **nano paint the real
talent OUT → person-free plate → ref-mode GENERATE our couple from the continuity text** (couple_bible.md).
R3-safe; identity rides on the reused description (holds up well across beats).

**New code (FFDY-7304):** `gen_shot.py` (stills→video i2v/ref), `nano.py` (swap_couple / paint_out),
`couple_bible.md`, `assemble.py`, `build_index.py`/`storyboard.json`, `extract_pptx.py`, `gallery/`.
Media (plates, gen videos, assets) in /home/colligo/THD_laundry_sink_storyboard/ (prep/, gen/, gallery/).
Skipped: **1B** 5-color b-roll (deck only had one hero still; needs the 5 finishes synthesized).

**REFERENCE — the ACTUAL THD-produced spot (found 2026-08-25).** Brightcove video **6384961806112**
(account 66036796001, "Glacier Bay Drop-In Laundry Sink...CLICKREADY", **67s**). NOT in any S3 dataset
(searched product_video_mapping 38k, pairs_index 14.5k, master table 588k, the full shot-segmentation
corpus of 29,740 videos, downloaded_videos) — it's a new SKU postdating those corpora. Got the HLS URL from
Hooman (DevTools) and pulled it via ffmpeg. Saved: local `THD_laundry_sink_storyboard/reference/
thd_produced_67s.mp4`; S3 backup `video_rewriter/laundry_sink/reference/thd_produced_67s.mp4`. To re-pull a
brightcove product video: get its HLS master.m3u8 (+fastly_token) from the page and `ffmpeg -i <url> -c copy`.
LEARNINGS from the real spot: (1) production RECAST the talent (red-haired woman + younger dark-haired man,
NOT the storyboard couple) → our invented couple is fine; (2) fast-cut ~22-shot montage (intro/title 0-12s,
assembly 12-37s, feature CUs 37-55s, hero+endcard 55-67s) — quicker than our ~5s/shot; (3) SUPERs + title
overlay + GLACIER BAY/CLICKREADY end-card baked in (post layer); (4) same set as the stills. Added to gallery
as the top "REFERENCE" tab for side-by-side.

**Sketch route for annotated screenshots (shots 6/7):** customer had no storyboard frames for box-completion,
so gave screenshots from the target video. Recipe: **sketchify the screenshot** (nano, "draw only the
cabinet+hands, omit text/UI/chrome") → ordered sketch keyframes + a prior generated frame as the photoreal
**style ref** (our couple). R3-safe; drops the wrong-couple likeness + baked-in SUPER. Passing an ANNOTATED
sketch (colored motion arrows) made Seedance RENDER the marks into the video ("honor but don't draw" still
drew them) → describe motion in PROSE, keep the ref sketch clean.

**Seedance VIDEO-EDIT to clean overlays (KEY capability, found 2026-08-25 via Hooman's idea):** generation had
right motion but rendered marks → don't re-roll; run the mp4 through `bytedance/seedance-2.5/reference-to-video`
with **`video_urls`:[uploaded mp4]** + "remove X, keep everything else identical (same people/motion/room)".
Cleaned the green/red marks out while preserving couple+motion. seedance_video.generate() doesn't expose
video_urls — build the payload directly with sv.upload + sv._req to the ref endpoint.
**⚠️ REVERSED 2026-08-28 (tested):** the video-edit route NOW trips the people filter — fal tightened the
policy. It rejects ANY source clip with a human likeness (incl. Seedance's OWN generated characters) with
content_policy_violation on video_urls; the block is on the INPUT so it fires whether you change the character
OR only an object (4/4 people-clips blocked incl. overhead/small-face; both edit types). Still works on
PERSON-FREE clips (confirmed white→navy cabinet recolor on the establishing shot). **WORKAROUND: the Seedance
2.0 video-edit endpoint (bytedance/seedance-2.0/reference-to-video + video_urls) does NOT block people** (tested
2026-08-28: full character swap + people-preserving object recolor on a couple clip both rendered). So editing
finished people footage (char swap, overlay cleanup) still works — just use the 2.0 endpoint (softer fidelity
than 2.5). Report: s3 …/video_rewriter/compare/videoedit_test/gallery/index.html.
Test code: model_comparison/test_videoedit.py (VE_MODEL=sd20) + build_videoedit_report.py.

**Process rules from Hooman:** (1) WIP-first — post keyframes+prompt to a top "WIP" tab, wait for "go" before
generating; overwrite that one WIP tab each time. (2) ALWAYS ADD new shot results to the HTML, never
delete/replace prior versions (keep history; mark chosen ★). (3) fan out gens to background + poll (fal ~15-20
min/gen all session). (4) don't use target-video frames as inputs unless the customer authorizes it for a
missing beat — then sketchify/paint-out them.

Gallery: https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/index.html
