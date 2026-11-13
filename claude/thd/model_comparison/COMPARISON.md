# Model comparison — Seedance 2.5 vs Seedance 2.0 vs MiniMax Hailuo 3

Laundry-sink spot (FFDY-7304), shots 1–11. **Same customer storyboard as the fixed input**; each
model got a **best-effort prep** of those source images (no artificial restrictions) so the test is
"what is the best each model can do with reasonable effort." All three at **~720p** (Seedance 720p,
H3 native 768P) — H3 has no 1080p tier, so 720p is the only fair common resolution; the existing
1080p Seedance-2.5 gallery stays separate, and this set adds a matched 720p 2.5 run.

## Deliverables (S3, IMS-gated gateway)
- **SIDE-BY-SIDE (all 3 per shot + 3 stitches on top)** — the decision view:
  https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/compare/sidebyside/gallery/index.html
- Seedance 2.5 (720p): …/video_rewriter/compare/sd25_720/gallery/index.html
- Seedance 2.0 (720p): …/video_rewriter/compare/sd20/gallery/index.html
- MiniMax H3 (768P): …/video_rewriter/compare/h3/gallery/index.html

Each per-model gallery mirrors the 2.5 gallery tabs: **FINAL STITCH** + Shot 1…11, each shot showing
the **input reference(s) passed to that model** and the **result + exact prompt**.

## How each model was prompted (learned this pass)
- **Seedance 2.5 / 2.0** — same family: `@Image1..N` ordered-keyframe directives, "Use @ImageN as the
  LAST frame" end-state pin, ref-mode people-injection from a person-free plate + the couple bible.
  2.0 endpoint adds `generate_audio=false`; otherwise identical payloads.
- **MiniMax H3** (`minimax/h3/image-to-video`) — **only 2 frames** (image_url + optional end_image_url),
  no `@Image` directives → prompts rewritten as **natural-language motion** ("the couple kneels and
  presses the panels together…"). `duration>=5` (rejects 4), native **768P**, `prompt_expansion_mode=
  balanced`, `enable_safety_checker=true`. **H3 i2v DOES inject prompt-described people** from a
  person-free plate — same trick as Seedance ref-mode works here.

## Frame-level observations (temporal/motion quality must be judged in the galleries)
- **Establishing (S01), product-only:** effectively identical across all three — a wash.
- **Person injection & couple consistency:** all three reproduce the couple bible (dark-haired woman /
  cream sweater; grey-haired man / light-blue polo) consistently across the person shots. This closes
  the earlier open question — H3 injects people as reliably as Seedance ref-mode.
- **Hero (S11):** H3 frames were the **sharpest/cleanest**; 2.0 had the warmest composition (couple
  embracing); 2.5 solid but framing slightly awkward.
- **Box completion (S06), complex motion:** 2.5 and 2.0 both give the wide two-person assembly read;
  **H3 tended to zoom tighter** onto the cam-lock hardware (hands/forearms only) — a different, more
  macro interpretation of the same prompt.
- **Framing interpretation differs per model** even from the same input — H3 crops tighter more often.

## Reliability notes
- **Seedance 2.5** has a stochastic **post-generation output filter** on person shots (rejected S10/S11
  once each; re-ran clean). 2.0 and H3 did not exhibit this.
- **H3** rejects `duration<5`. Transient "Downstream service unavailable" hit 2.0 once (re-ran).
- fal was congested (~15–25 min/gen) all session for every model.

## Recommendation
Judge **motion** in the side-by-side (frames can't). On stills, **H3 is the cleanest/sharpest and
injects people just as well** while being the cheapest to prompt (plain motion language, no keyframe
grammar) and without the 2.5 post-filter rejections — a strong default for these person+assembly spots.
**Seedance 2.5/2.0** keep the edge where you need **precise multi-keyframe control** (`@Image` ordered
progressions, hard LAST-frame end-state) and the **video-edit overlay-cleanup** route, which H3's 2-frame
API can't express. Pick per shot: H3 for clean single-motion beats, Seedance for choreographed
multi-keyframe ones.
