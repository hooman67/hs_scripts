---
name: project_thd_video_rewriter
description: "THD article→video rewriter experiments (Seedance): recreating how-to shots; the person-free PLATE technique + R3 boundary"
metadata: 
  node_type: memory
  type: project
  originSessionId: 988e6174-d494-4ea5-a025-8678b58141b2
  modified: 2026-08-24T17:15:52.647Z
---

Goal (started 2026-08-22): build an LLM rewriter agent that turns a THD how-to **article** into a
video, using the [[reference_seedance_video_skill]] (`/generate-video-fal-seedance`).

**Project code now lives in the repo: `hs_scripts/claude/thd/`** (git-tracked; README.md there). Media
(source/generated videos + images) stays OUT of git in `/home/colligo/THD_How_to_Install_a_Door_Lock/`;
`thd/.gitignore` excludes creds.txt + media. Layout: `pipeline/` (engine + PIPELINE.md + configs),
`gallery/` (build_gallery.py + manifest.json = full round-by-round record + imsauth.js), `experiments/`
(the round drivers). The skill code is in `../dotclaude/scripts/seedance_video.py` (+ command), and these
memories are in `../dotclaude/memory/` (symlinked from ~/.claude, so in-repo).

**Pipeline (backlog b) STARTED — `pipeline/rewriter_pipeline.py` + `PIPELINE.md`.** Config-driven (one
JSON per shot): source shot → extract beat keyframes → `person_mode=cover_body` (nano-banana removes
head+torso, keeps real hands+tool, strips step/TIP graphics) → `compose_prompt()` (vendor @ImageN ordered
keyframes IN the THD register) → generate (ref mode, ~5s/beat). Ran end-to-end on shot 0007 (remove the
doorknob, blue screwdriver, 2 beats): action-faithful + R3-clean, BUT came out HANDS-ONLY — the
body-covered keyframes weren't re-expanded into the full man. Refinement (same as shot-3 tight→wide):
stronger "full person visible" framing or a wide person plate. Still TODO for (b): auto-decompose the
ARTICLE into a shot list + auto-pick beat timestamps (LLM), and multi-shot assembly + continuity lock. Working test
case = "How to Install a Door Lock". Assets on the colligo box under
`/home/colligo/THD_How_to_Install_a_Door_Lock/`: `ORIGINAL_*.mp4` (full human video), `brightcove-article/shots/`
(29 segmented shots + `metadata/*.parquet`), `work/` (frames, plates, gen rounds), `gallery/`
(self-contained HTML: `manifest.json` + `build_gallery.py` → `index.html`; re-run build to append rounds).

Fidelity bar set by Hooman: **match composition** (camera angle, framing, door layout, action) — identity aside.

Key measured findings (recreating shot 0003 = measuring the lock backset):
- **R3 is stricter than the skill said.** ANY real person in a reference → `422 content_policy_violation`
  (partner_validation) — a visible face AND a back-of-head/face-hidden frame both rejected. BUT
  disembodied **hands are tolerated** (a crop with only hands+tape rendered fine).
- **The unlock for person-shots = person-free PLATE.** Paint the person out of a source frame with
  `fal-ai/nano-banana-pro/edit` (`work/paint_out.py`), then ref-mode that plate. It carries BOTH the
  real hardware/room fidelity AND the original camera/composition (R2 works FOR us). This beat
  everything: cropping the person out FIGHTS composition (tight crop → wrong camera); pure t2v can't
  reproduce a specific camera (asked for hinge-side back view, got face-side). Winner so far = round2 G1.
- **Which plate you reference sets the camera.** Plate from the source shot → original camera; plate
  from the article still → front-profile.
- Watch-outs: ungrounded text on clothing invents a garbled wordmark (brand-safety fail) — fix with a
  "plain shirt, no text/logo" negative (worked in round 3).
- **Tape-measure prior (round 3):** Seedance ALWAYS renders the tape blade fully extended (~a foot),
  regardless of a requested short span (2-3/8" backset, hole diameter). Text can't shorten it.
  Hypothesis to try: crop the plate to a MACRO of the feature (door-edge+knob, or bore hole) so the
  over-extended blade falls out of frame (R2: framing follows the reference). Door THICKNESS is the
  hardest measurement — model runs the tape vertically down the edge instead of across the slab depth.
- **Tape fix (round 5, THE breakthrough):** don't ask Seedance to CREATE a short measurement (rounds
  3-4 proved macro-crop and plain i2v both fail — it always re-extends the blade). Instead build a
  reference plate (nano-banana edit) that ALREADY shows a correctly-placed SHORT tape at the feature
  (hook at door edge → across to knob for backset; across the bore hole for diameter), then generate
  with a "hold steady, almost no motion" prompt. The short tape then persists the whole clip. Works in
  ref and i2v; **i2v (plate as first frame) is the most faithful.** Still can't render legible numerals
  up close (keep tape mid-distance; add the real number as a post graphic).
- i2v first-frame lock (round 4B) only HOLDS when frame 0 has no person to contradict (bore plate held,
  knob plate didn't) — good for clean opening shots.
- **"Hold steady" was WRONG (round 5 critique):** the shot is motion-through-beats, not a frozen tape.
  Reproduce motion with MULTIPLE KEYFRAMES, per the vendor guide's "Controlling the Order of Multiple
  Keyframes" (docs/prompting/vendor/sd25-pe.SKILL.md, §Keyframe Anchors). Method: pass keyframes as
  ordinary reference images in `image_urls` (order = @Image1, @Image2, …) and declare roles VERBATIM in
  the prompt: "Use @Image1 through @ImageN as keyframes in that order." / "Use @Image1 as the first
  frame." / "@Image2 defines the second keyframe: <state>." / "Use @ImageN as the last frame." Each real
  beat frame already shows the correctly-short tape, so keyframes ALSO fix the over-extension. Native
  i2v also supports first+last positional frames via `image_url` + `end_image_url` (added to
  seedance_video.generate as `end_image=`). We had NOT been using @ImageN roles at all — that was the gap.
- **Sketch-driven shots (rounds 14-15): you can drive a shot from SKETCHES + one photoreal ref, no
  source footage.** Convert beat frames to line sketches (nano-banana) for the tape/hand geometry, add a
  photoreal person-free plate for appearance. CRITICAL ordering (same lesson as round 10): the SKETCHES
  must be the ORDERED KEYFRAMES (@Image1..N) and the plate a trailing APPEARANCE ref (@Image4, "render
  photoreal, do not adopt the sketch look"). Round 14 put the plate as @Image1 first-frame → it dominated,
  sketches ignored, tape over-extended. Round 15 V_sb (sketches as keyframes + plate @Image4) → tape
  honors the sketch positions (short, no over-extension) AND fully photoreal. Gets ~80-85% of round 13
  with zero exact frames; per-beat geometry looser (may need longer duration for 3 distinct beats).
- The vendor guide (sd25-pe) is the authority for HOW to reference assets: every reference image needs an
  explicit `@ImageN` role line; unused assets go in 【Unused Assets】; up to 50 refs; also covers
  storyboard grids and coarse/fine blockout videos. Read it before designing any multi-asset shot.
- **VERIFIED (round 6): fal's reference-to-video HONORS the vendor @ImageN ordered-keyframe directives.**
  Pass real beat frames as image_urls=[kf1,kf2,kf3] (order = @Image1..3) + verbatim "Use @Image1 as the
  first frame / @Image2 defines the second keyframe / Use @Image3 as the last frame / Use @Image1 through
  @Image3 as keyframes in that order" → clip opens on kf1, passes through kf2, ends on kf3 with REAL hand
  MOTION, and the tape stays correctly short (the MIDDLE keyframe anchors it and kills over-extension).
  This is THE recipe for beat-based action + correct measurement. i2v first+last only (kf1→kf3, no middle)
  FAILS — unconstrained midpoint hallucinates the over-extension. Face-free crops (hands+tape+lockset,
  no head) keep keyframes R3-safe. Winner = round6 K1.
- **VERIFIED (round 8): split-role references give a WIDE shot with a correct tight action.** Assign
  different roles to different refs (vendor §Reference Asset Roles): @Image1 = a wide person-free PLATE
  for composition/camera ("Use @Image1 as the first frame … keep this framing/scene"); @Image2 = a tight
  CROP used ONLY for the tape+hand pose ("Use @Image2 for the position and pose … without changing the
  composition of @Image1"); insert the person via the prompt. Seedance scales the tight tape pose into
  the wide frame with NO over-extension. This is the general recipe: one ref for framing, another for a
  detailed action/prop pose, person from text. W1=front plate (clearest measurement), W2=hinge plate
  (closest to original camera). Both in gallery round 8.
- **FINAL shot 0003 recipe (round 9): 1 wide plate + N ordered beat crops = wide framing + beat motion +
  correct action.** image_urls=[wide_plate, kf1, kf2, kf3]: @Image1 = wide plate as first frame for
  camera/composition (framing LOCKED all clip, "do not zoom in"); @Image2..@Image4 = the beat crops used
  ONLY for the tape/hand pose per beat "without changing @Image1's framing". Gives the 3-beat measuring
  motion in the wide camera, tape stays short. Winner = round9 F_hinge (hinge/back-angled plate HOLDS the
  wide frame). CAVEAT: the FRONT wide plate tends to COLLAPSE to a close-up mid-clip AND can surface a
  legible tape brand logo (STANLEY) — prefer the hinge/back-angled wide plate. Residual: prompted
  door-swing motion stays subtle.
- **Role rule (round 10): to get a WIDE shot, the wide plate MUST be @Image1 (the first frame).** A
  trailing "@Image4 defines the wider framing, render the whole shot at this scale" override is IGNORED —
  the model locks to whatever the FIRST frame's scale is. So: wide plate = @Image1 first frame → holds
  wide framing + person + motion (round10 Va), BUT tight beat keyframes then get down-weighted (beats
  blur into one). Crops-as-first-frames → distinct beats but stays close-crop (round10 Vb). Open tension:
  wide-first-frame vs tight beat-keyframes (scale mismatch) — a wide first frame dilutes tight beat
  crops. Likely real fix = beat keyframes AT the wide scale (composite hands+tape into the wide plate at
  each beat) rather than tight crops. Demoting keyframes to loose "pose refs" (round 9) breaks the beat
  sequence entirely — always use the vendor ordered-keyframe directives.
- **WIDE beat keyframes (round 11, the wide fix): cover the person's body, KEEP the real hands.** To make
  wide keyframes from source frames that contain a person, nano-banana-edit each frame to replace ONLY
  the head+face+torso with background while keeping the real forearms+hands+tool UNCHANGED ("do not
  stretch/lengthen/redraw the arms"). Removing the arms too makes nano-banana regrow long unnatural hands
  (bad). These 3 body-covered wide beat frames, used as ordered keyframes (no separate plate), give a
  WIDE held frame + full generated person + natural hands + real motion (round11 exp2b — best wide take).
  Same edit also removes on-screen graphics (the TIP overlay). Alt idea (untried): stylize to a sketch to
  dodge R3 — not needed; cover-body worked and preserves door fidelity.
- **Shot 0003 has THREE distinct measurements (corrected — an earlier note wrongly said one).** beat1 =
  tape horizontal across the round KNOB PLATE (plate/hole width); beat2 = tape from the DOOR EDGE to the
  knob plate (edge-to-plate); beat3 = tape across the door's NARROW EDGE (the strip where the latch bolt
  sits) = THICKNESS. The differences are subtle/all in the lockset region. Round 7 v2 (A2_door_motion_v2,
  tight, 3 crops as ordered keyframes) captures all three because the tight scale makes them legible; the
  WIDE version (exp2b) at 8s BLENDED them and dropped the thickness beat. FIX CONFIRMED (round 12 exp2c):
  same wide beat keyframes + LONGER duration (16s, Seedance allows 4-22s) + explicit per-beat directives
  ("settle briefly on each") recovered ALL THREE in the held wide frame (across-plate -> edge-to-plate ->
  thickness-at-edge). Lesson: for N distinct beats give ~5s each; 8s is too short for 3 subtle beats.
  Shot 0003 packs all 3 measurements into ONE shot, so one wide 3-beat shot is the faithful target (my
  "3 separate shots" suggestion was based on the misread and does not apply here).
- THD team's OWN composer (mechanism.html / shotlist.py) gets motion from TEXT instead: a "In order: A;
  then B; then C" beats line + an ENTRY_LINE timing table (mid_action / full_arc / hand_absent_both_ends /
  from_still) + generic single reference — NO @ImageN, NO keyframes (their §14 gap). Best practice =
  COMBINE: vendor visual keyframes inside the THD 5-line register (subject+beats / shot+camera / talent+
  entry / look+neg). shotlist.py IS a prototype of the rewriter (tables + compose() for fixed domains);
  the rewriter generalizes those tables from an arbitrary article. Continuity lock (verbatim room/light/
  wardrobe clause + one shared room reference on every shot) is the mechanism for multi-shot sequences.
- **✅ SHOT 0003 IS DONE (approved 2026-08-24). Final winner = `sketch_Vsb_16s_light`** (Round 17, in the
  gallery Shot 0003 tab): the sketch-driven method (thin sketches sk1/2/3 as @Image1-3 ordered keyframes +
  photoreal person-free plate @Image4), beat2 wording fixed ("tape hook at door edge, blade STOPS at the
  near rim of the knob plate, not into the middle"), at 16s, with ONE light clause to curb the between-beat
  tape retract. **Key lesson — LIGHTER TOUCH WINS ([[feedback_lighter_touch_prompts]]):** a heavy all-caps
  multi-clause "anti-retract" paragraph AND thicker sketch lines BOTH made the result visibly WORSE than the
  plain beat2fix; the fix was to keep the good prompt verbatim and append a single short sentence ("the hand
  keeps the tape out and slides it between measurements rather than winding it back in"). Thick vs thin
  sketches = no meaningful difference (line weight is not a lever). Over-engineering the prompt degrades
  Seedance output — reach for the smallest delta first.
- **cover_body mangles BUSY two-handed source frames → re-time the beats (shot 0008).** On shot 0008 the
  cover_body nano edit dropped the knob in kf1 and hallucinated a hand screwing the latch plate in kf2
  (wrong beat), because the chosen timestamps landed on cluttered/ambiguous frames. Fix: pick beat
  timestamps on CLEAN, unambiguous moments (re-timed 0.98s/3.8s → 0.5s/2.9s) so the cover_body edit and the
  ordered keyframes come out correct. Approved result. When a cover_body keyframe looks wrong, re-time the
  beat before touching the prompt.
- Gallery is LIVE on S3 (creds now in thd/creds.txt, valid ~24h): rebuild `gallery/` then upload to
  `s3://foundry-thd-enterprise-adobe-assets/video_rewriter/door_lock/gallery/` (index.html text/html,
  imsauth.js application/javascript, assets by ext). View:
  https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/door_lock/gallery/index.html

Blocker: this box has NO Foundry token (no credentials.yaml / ~/Downloads/creds.txt) and the AWS
broker endpoint times out, so `/render-s3-gallery` + `/aws-creds` don't work here. View the gallery by
local-serve (`python3 -m http.server` in `gallery/`, open the box's `*.od1.colligo.dev` URL) unless a
token is provided. See [[reference_dotclaude_backup]].
