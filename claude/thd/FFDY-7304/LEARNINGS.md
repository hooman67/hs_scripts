# FFDY-7304 — Storyboard → Video: Learnings (what worked, what didn't)

Turning the Glacier Bay laundry-sink storyboard into a generated ~:60 spot with Seedance 2.5 +
nano-banana on fal.ai. Distilled from the full build. Companion to `STORYBOARD_OVERVIEW.md`,
`COMPARISON.md`, and the memory `project_ffdy7304_laundry_sink`.

---

## The hard constraint: R3 (Seedance's people filter)
- **Any photoreal human in an image reference → 422 `content_policy_violation` (partner_validation).**
  This is true even for a **synthetic couple we generated** (nano-swapped) — Seedance can't tell it's not a
  real person and rejects it. Confirmed by direct test.
- **R3 also catches:** partial people at frame edges, and **reflections of people** in glass/metal (washer
  doors). Always paint those out too.
- **What passes R3 as a reference:** person-free plates, hands/forearms only, and **sketches of people**
  (line art carries no likeness). Seedance will *generate* photoreal people fine — the block is only on
  photoreal people in the *input*.
- **BIG exception found late (2026-08-25):** the **video-edit route does NOT trip R3** even with our photoreal
  couple in the clip (see "Video-edit" below). **⚠️ REVERSED 2026-08-28:** this no longer holds — fal tightened
  the policy. The video-edit route (`reference-to-video` + `video_urls`) now **rejects ANY source clip
  containing a human likeness — including Seedance's own generated characters** — with
  `content_policy_violation` on `video_urls`. The block is on the INPUT, so it fires regardless of whether you
  change the character or only an object (4/4 people-clips blocked, incl. overhead/small-face shots). It still
  works on **person-free** clips (confirmed: white→navy cabinet recolor on the establishing shot). **BUT the
  Seedance 2.0 video-edit endpoint (`bytedance/seedance-2.0/reference-to-video` + `video_urls`) does NOT block
  people** — tested 2026-08-28: it did a full character swap AND a people-preserving object recolor on a
  couple clip. So the overlay-cleanup / character-change workflow on finished people footage still exists —
  just move it to the **2.0** endpoint (2.0 = slightly softer fidelity than 2.5). Test report:
  `s3://…/video_rewriter/compare/videoedit_test/gallery/index.html`; code `model_comparison/test_videoedit.py`
  (`VE_MODEL=sd20`).

## Techniques that WORKED
- **Person-free plate + generated couple (ref mode).** nano-banana paints the real talent out → clean scene
  plate; ref-mode generates OUR invented couple from a fixed **couple bible** (verbatim description reused
  every shot). Couple stayed impressively consistent across ~8 person shots. This is the workhorse for
  person beats.
- **i2v single still + motion prompt** for face-free product macros (click connector, faucet, hardware,
  hinge, doors). Fast, no R3, clean.
- **"Locked-off tripod, camera does NOT move"** for establishing/beauty shots — otherwise a generic
  "push-in" over-zooms into a tight CU and loses the framing.
- **nano recolor for color variants** — recolor only the finish (white → White Oak wood grain), keep
  everything else, then the same locked-off establishing recipe.
- **Ordered keyframes for a progression** (vendor `@Image1..N` "first/second/last frame" directives). Used
  for the flat-lay → lifting → standing panel sequence.
- **Sketch method for photos/screenshots (the unlock for shots 6/7):** sketchify a source frame (nano: "draw
  ONLY the cabinet + hands, omit text/UI/chrome") → ordered **sketch** keyframes for structure/pose + a
  **prior generated frame as the photoreal style reference** (our couple, room, materials). Solves R3 +
  wrong-couple-likeness + baked-in SUPER text all at once. Sketch = geometry/pose; style ref = appearance.
- **"Use @Image1 as the LAST frame"** — the tested directive to pin an end state (vs vague "target scene").
- **Precise per-hand motion prompting** — "his LEFT hand on the LEFT side, RIGHT hand on the RIGHT side",
  "the two long sides stay FIXED", "a very small gap then close". Specificity fixed motion that generic
  wording got wrong.
- **Video-edit to clean cosmetic defects (KEY, Hooman's idea).** A generation with the right motion but a
  stray overlay (rendered annotation marks) was fixed by passing the mp4 as **`video_urls`** to
  `bytedance/seedance-2.5/reference-to-video` with "remove X, keep everything else identical". Preserved
  couple + motion, erased the marks, and **did not trip R3**. Use for stray marks/text/wrong logos instead
  of re-rolling. (`seedance_video.generate()` doesn't expose `video_urls` — build the payload directly with
  `sv.upload` + `sv._req`.)

## Techniques that DIDN'T work (and the fix)
- **Feeding a synthetic couple to i2v** → R3 rejected. Fix: paint-out + generate the couple from text.
- **"Use @Image1 as the target scene"** → Seedance has no notion of "target scene"; didn't pin the end
  state. Fix: literal "Use @Image1 as the LAST frame ... the video ENDS on @Image1".
- **"Ignore the colored marks / don't draw them"** on an annotated sketch → the model still **rendered** the
  green arrows/red circles into the video. Emphasizing the marks made it draw them. Fix: keep the ref sketch
  **clean** and put the motion in **prose**; OR generate then **video-edit** the marks out (what we did).
- **Generic "push the side walls together"** → exaggerated expand-and-collapse of the whole box. Fix: name
  which pieces are fixed vs moving, and constrain the magnitude ("very slight, no exaggerated movement").
- **Single-keyframe end-state (ref mode)** end-state control is *soft* — lands close, not exact. The hard
  lock is i2v `end_image_url` (needs a first frame too).
- **nano "paint out the person" hallucinating assembly** — it "helpfully" completed flat panels into a built
  box, or **laid a held/raised panel flat**. Fix: explicit "keep pieces FLAT and SEPARATE / keep the raised
  panel UP; do NOT assemble, connect, or lay anything down". **Always eyeball the plate before generating.**
- **Person-dominated close-ups** (a CU that's mostly the person) don't survive paint-out into a usable
  person-free keyframe — you're left with empty room. Use the sketch route or a wider frame instead.
- **Our extracted video frames ≠ the customer's chosen screenshots** — re-timing guesses missed their exact
  beat. When the customer points at specific frames, use *those* (sketchify them).

## Gotchas / ops
- **fal was congested the whole session (~15–25 min per generation)** vs the usual ~3. Batch parallel
  variants; don't serialize.
- **Subagents dispatched for gens ORPHANED** the work (set it up, ended before the ~18-min render). Poll from
  the main session, or give the subagent a hard "do not exit until the mp4 exists".
- **macOS screenshot filenames use a narrow no-break space (U+202F) before AM/PM** — exact-string paths fail
  (`test -f` says missing while `ls` shows it). Resolve via `glob` instead of typing the spaces.
- **Foundry S3 token expires (~a few hours)** and its **format flip-flops** between `export AWS_...="..."`
  and lowercase `aws_...=...` in creds.txt — source robustly (`eval "$(grep '^export AWS_' creds.txt)"` for
  the export form). The gateway role is **upload-only** (no `s3:DeleteObject`) — de-referenced assets linger
  but don't render.
- **Background `for..& done` without `wait`** returns exit 0 while children still run — check disk or use a
  waiter.

## Process rules (from Hooman)
1. **WIP-first.** Post keyframes + prompt to a single top **"WIP" tab** and wait for "go" before generating
   any shot. Overwrite that one WIP tab each time.
2. **Always ADD** new shot results to the HTML — never delete/replace prior versions. Keep the history; mark
   the chosen one ★.
3. **Fan out** generations to the background and poll; keep the main session free.
4. **Don't use target-video frames as generation inputs** (cheating) *unless the customer authorizes it* for a
   beat they didn't storyboard — then sketchify / paint-out those frames.
5. **Precise, honest reporting** — flag defects (rendered marks, drift, wrong motion) rather than claiming success.

## Tooling built (this experiment)
- `extract_pptx.py` — PPTX → slide text (repo) + embedded photos (media).
- `gen_shot.py` — stills→video driver (i2v single first-frame, or ref ordered keyframes); config-per-shot.
- `nano.py` — nano-banana helpers: `swap_couple`, `paint_out`, generic `_edit` (sketchify, recolor,
  keep-raised-panel, keep-flat-panels, remove-people+reflections).
- `couple_bible.md` — the fixed couple description (reused verbatim for consistency).
- `assemble.py` / `assemble_v2.py` / `assemble_stitch.py` — concat/recut in shot order.
- `gallery/build_gallery.py` + `manifest.json` — self-contained tabbed review gallery (IMS auth), uploaded to
  `s3://foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/`.

## Net result
Assembly + product beats built shot-by-shot from **storyboard/customer assets only** (target video used
just for comparison, and — with permission — as sketch structure for the box-completion beats). Couple stays
consistent across the person shots. A 42s review stitch confirms harmony; the two skip-seams (assemble→stand-up,
basin→hero) are the candidates for bridging B-rolls.
