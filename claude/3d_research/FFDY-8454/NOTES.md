# FFDY-8454 Experiment Notes

## 2026-09-22 — v1 assumptions

- The storyboard is sufficient to build a motion proxy, but not a faithful product model.
- The cabinet is represented in its on-the-mat assembly orientation.
- The two long side walls have fixed lower-edge pivots.
- The maximum authored top spread is deliberately small: 6 degrees per side at full control value.
- Shot 5, shot 6, and shot 7 use separate insertion controls so we can test each motion independently.
- Hands are editable visual guides and do not use inverse kinematics in v1.

## Evidence-backed motion interpretation

- Shot 5: both long side walls remain fixed; only the shorter perpendicular end panel lowers and seats.
- Shot 6: the long side walls open only slightly, the bottom piece enters the middle, and the walls close again.
- Shot 7: lower side-wall endpoints stay stationary, upper endpoints widen slightly, the locking piece drops straight down, and the upper endpoints close.

## Known uncertainties

- Exact panel dimensions and joinery locations are not available in the storyboard.
- The storyboard terminology for “bottom piece” and “top piece” is ambiguous relative to the cabinet's temporary assembly orientation.
- v1 prioritizes distinct motion constraints over exact visual identity.

## 2026-09-22 — v1 result

- Blender 5.2.2 built the rig successfully.
- Eleven representative key states rendered successfully.
- Three H.264 preview clips were encoded at 480×270 and 24 fps.
- Automated checks pass for fixed lower pivots, shot-5 vertical displacement, shot-6 insertion and re-closing, and shot-7 6-degree spread/drop/re-close behavior.
- Visual inspection confirms that inactive shot-specific pieces are omitted from earlier renders for clarity.
- The rig supports deterministic slider/timeline editing. The v1 controls are not yet direct-manipulation viewport gizmos.

## Decision gate before generation

Hooman should confirm that the gold shot-5 panel, purple shot-6 bottom proxy, and green shot-7 locking piece correspond to the intended physical parts. If they do, the next experiment can render a reference blockout and submit it to a video model. If not, revise topology before any paid generation.

## 2026-09-23 — v2 full-assembly rig

- Scope narrowed to exactly six cabinet components; sink, faucet, hardware, and hands are excluded.
- The six inferred components are the front frame/doors, two side panels, bottom panel, wide rail, and narrow rail.
- Every component has its own constrained progress channel, visible free-transform handle, and independent animation Action.
- The progress channel supplies layout and installed endpoints. The direct handle adds arbitrary user-authored translation and rotation.
- The included 360-frame order is explicitly an example. A separate blank template has no animation keys and begins with all pieces flat.
- The v2 validation passes all eleven checks, including exactly six component roots and one-component-only control isolation.
- The full demonstration preview is 15 seconds, H.264, 480×270 at 8 fps.

## 2026-09-23 — v3 components-only baseline

- Created a clean native-Blender baseline with exactly six directly selectable mesh components.
- Joined doors, hinges, and connector details into their corresponding physical component.
- Removed all custom progress controls, transform handles, drivers, constraints, pose guides, animation keys, labels, and imposed order.
- Retained only an optional floor and overview camera for orientation.
- Validation passes all six stripping checks.

## 2026-09-23 — Native rigid edge-pivot variant

- Edit Mode edge translation was identified as mesh deformation, not rigid rotation.
- Created a separate components-only copy whose ordinary object origins lie on practical floor-contact edges.
- Locked object scale to `(1,1,1)` without adding handles, drivers, or constraints.
- Verified that `CABINET_04_BOTTOM_PANEL` rotates upright with `R X 90` while its near long edge remains planted.
- Validation confirms that repositioning the origins did not change any component's world-space geometry.

## 2026-09-23 — Bottom-panel leg correction

- Superseded and incorrect. Legs were initially added to the wrong component.

## 2026-09-23 — Image-7-only component correction

- Hooman specified `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/references/storyboard_all_pieces_image7.jpeg` as the sole reference.
- The central front-frame assembly has the two legs, two doors, four hinges, small rectangle, and orange areas along its top and bottom edges.
- One side panel lies above the center, another below, two unequal boards lie at right, and the plain top wall lies at upper left.
- Rebuilt all six components and their layout from scratch instead of patching the incorrect v3 topology.
- V4 passes all eight structural checks. Exact dimensions remain approximate because the single image is not CAD.

## 2026-09-23 — Seedance blockout review publication

- Eight Seedance 2.5 jobs completed: seven isolated assembly actions and one combined auto-edit.
- The combined output inferred eight visual segments separated by seven cuts in the intended action order.
- Added a `BLENDER BLOCKOUT — motion → Seedance` tab to the existing laundry-sink gallery.
- Each isolated result is presented beside its exact Blender motion-reference clip; the tab also contains the combined video and diagnostic contact sheets.
- Review URL: `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/index.html`
- Hooman prefers generated video/image results to be published in reviewable HTML galleries by default rather than shared only as filesystem links.

## 2026-09-23 — Combined-call provenance gallery

- Replaced the detailed blockout content in the original laundry-sink gallery with a link to a dedicated report.
- Dedicated report: `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/3d_blockout_combined_v1/index.html`
- The overview contains all eight ordered video inputs, all six ordered image inputs, the complete submitted prompt, model parameters, raw local/submitted request JSON, result metadata, and the complete 22.04-second output.
- Eight stage tabs compare the primary motion reference with the output segment extracted at the detected cuts.
- The seven isolated generation cards likewise include their complete input sets, prompts, parameters, submitted payloads, and outputs.
- The stage mappings are labeled as analysis of one combined model call; they are not misrepresented as eight independent calls.

## 2026-09-23 — Shot 2 / 1A Event Script retry

- Preserved the complete v1 prompt and replaced only `【Event Script】` with Hooman's supplied wording.
- Submitted additive job `shot02_1A_event_script_v2` with the same blockout video, appearance image, endpoint, 4-second duration, 720p resolution, 16:9 aspect ratio, and audio disabled.
- Estimated incremental cost: $1.66.
- Visual review: the extra 180-degree panel flip is no longer visible; the lift is direct. The retry changes framing somewhat by moving higher and admitting the sink at frame left.
- Appended the retry beneath the original Stage 1 card with full request provenance; the original card and assets remain unchanged.

## 2026-09-23 — Shot 4 Event Script retry

- Preserved the complete Shot 4 v1 prompt and replaced only `【Event Script】`, adapting the successful Shot 2 wording to the correct Shot 4 starting state.
- Submitted additive job `shot04_event_script_v2` with the same blockout video, appearance image, endpoint, 4-second duration, 720p resolution, 16:9 aspect ratio, and audio disabled.
- Estimated incremental cost: $1.67.
- Visual review: the opposite panel now follows one clean edge lift into its upright position without v1's awkward intermediate handling. The retry uses a tighter, lower framing and crops more of the couple.
- Appended the retry beneath the original Stage 3 card with full request provenance; the original card and assets remain unchanged.

## 2026-09-23 — Customer workflow mockup v1

- Created a standalone screen-recording prototype inspired by the supplied Runway workflow screenshot.
- The left panel presents the storyboard upload and agent conversation; the main workspace presents a 12-shot laundry-sink graph using real project thumbnails.
- Image, prompt, inferred-motion, shared-context, video-output, and final-timeline nodes use distinct shapes and colors.
- The graph supports pan, zoom, fit, node inspection, chat input, upload selection, a simulated generation sequence, and demo reset.
- Published without modifying any existing result gallery at `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/workflow_mock_v1/index.html`.

## 2026-09-23 — Seedance physics and proportion retries for Shots 5–7B

- All four retries changed only `【Event Script】`; video references, image references, endpoint, duration, resolution, aspect ratio, and audio settings were preserved.
- Shot 5 / Stage 4 (`shot05_event_script_v2`, estimated $2.22): continuous two-hand wall support removed the autonomous flying-board failure. The man's narrow-board displacement is subtle.
- Shot 6 / Stage 5 (`shot06_event_script_v2`, estimated $1.68): explicit hand ownership improved physical causality, but the cabinet remained closer to square than the Blender reference. This is a partial prompt-only proportion failure.
- Shot 7A / Stage 6 (`shot07A_event_script_v2`, estimated $1.83): assigning exact geometry, proportions, orientation, camera, and trajectory to `@Video1`, with `@Image1` restricted to materials and room appearance, produced a wide laid-flat cabinet and direct two-hand board installation without a flip.
- Shot 7B / Stage 7 (`shot07B_event_script_v2`, estimated $1.64): repeating that role separation preserved the wide laid-flat cabinet, direct final-board motion, continuous two-hand support, and visible cabinet stabilization.
- Total estimated incremental cost for these four retries: $7.37. This is a planning estimate, not a fal invoice.
- The result gallery remains append-only: each retry was added beneath its corresponding original card with the exact prompt, input video, image, payload, output, and contact sheet.

## 2026-09-23 — Blender V5 corrected geometry

- Created append-only successor `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/blender/laundry_sink_components_v5_corrected_geometry_simplified_motion.blend`.
- Baked the final top-wall and narrow-board dimensions into mesh geometry from frame 1; animated scale values are now all 1.
- Moved late fit corrections to installation endpoints and removed the large-board 180-degree X flip with installed-height compensation.
- Preserved final assembly bounds at frames 324 and 348 within 0.00002 units and retained the front-frame/master stand-up orientation change.
- Published visual review at `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/blender_v5_review/index.html`.

## 2026-09-24 — Shot 7B thin-strip identity wording test

- Ran three additive Seedance 2.5 reference-to-video variations with the exact same `shot07B.mp4` motion reference, `S6a_box_plate.png` appearance reference, v3 prompt structure, 4-second duration, 720p resolution, 16:9 aspect ratio, and audio disabled.
- The only experimental variable was `【Event Script】` wording. Each call had an estimated incremental cost of $1.64; the preflight total was $4.93. These are planning estimates, not a fal invoice.
- `shot07B_identity_v4a`: **best of this three-sample batch**. The moving component remains visibly thinner than the already installed wider board and the direct installation motion is preserved. It is closest to the far-right strip in `storyboard_all_pieces_image7.jpeg`; exact one-third width remains visually unverified.
- `shot07B_identity_v4b`: motion remains direct, but the generated moving component reads as a substantially wider plank than the target strip.
- `shot07B_identity_v4c`: motion remains direct, but the generated moving component again reads as a broad plank rather than the thinnest component.
- Conclusion at low confidence (`n=1` per wording): the positive relative-width wording in A performed better than B's negative `do not substitute or widen it` wording and C's `exact loose strip` wording. This does not establish a general Seedance rule.
- Private diagnostic contact sheets remain beside each local result under its `review/` directory. They were intentionally not copied into the public gallery.
- Appended all three cards after v3 with only the actual submitted video/image inputs, prompt, settings, payload, result metadata, and generated output; no prior card or asset was deleted or replaced.

## 2026-09-24 — Shot 7B broad-face orientation retry

- Submitted additive job `shot07B_broad_face_v5` using the exact v4A structure, blockout video, appearance image, 4-second duration, 720p resolution, 16:9 aspect ratio, and disabled audio.
- Changed only `【Event Script】` to preserve the thinnest-strip identity while requiring its largest broad rectangular face to stay horizontal and seat against the cabinet instead of its thin edge.
- Estimated incremental cost: $1.64. This is a planning estimate, not a fal invoice.
- **Failed combined requirement:** the generated action seats a component horizontally on a broad face, but the component becomes a full-width lid-like panel. The prompt corrected the face orientation while destroying v4A's successful thin-strip identity.
- Interpretation at low confidence (`n=1`): the phrase `largest broad rectangular face` likely shifted model attention from part identity toward a broad panel prior. A future retry should avoid size-superlative wording and may require a dedicated appearance reference of the isolated strip rather than more text.
- The private diagnostic contact sheet remains under the local result's `review/` directory and is not displayed in the gallery.
- Appended the failed v5 result after v4A/B/C with its exact submitted inputs, prompt, settings, payload, metadata, and output. All prior cards and assets remain present.

## 2026-09-24 — Superseding Shot 7B gallery decision and accepted retry

- Hooman explicitly requested removal of the failed `shot07B_broad_face_v5` card from the public
  result HTML. Its local generation files remain preserved for research history.
- Starting from the smoother v4C result, a minimal wording change produced
  `shot07B_identity_v4c_narrow_v2`, which reduced the moving strip's width while retaining the
  desired direct motion.
- Hooman accepted the available shots and selected v4C.2 for the final sequence.

## 2026-09-24 — Approved shot-by-shot final cut

- Assembled the exact 11-shot order supplied by Hooman, using full source durations and straight
  cuts.
- Output is 54.462 seconds, H.264, 1920×1080, 24 fps, yuv420p, no audio, and fast-start.
- Local output:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/final_cuts/final_cut_shot_by_shot_v1.mp4`
- Reproduction script:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/scripts/assemble_final_cut_shot_by_shot.py`
- Input manifest:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/final_cuts/final_cut_shot_by_shot_v1.inputs.json`
- Appended the `Final Cut made shot by shot` tab and its ordered source ledger to the complete
  provenance gallery.

## 2026-09-24 — Final workflow-demo interaction

- Fresh refresh intentionally shows no generated thumbnails and no final assembled video.
- First generation simulates 00:00–04:00; outputs remain empty through 03:45 and populate during the
  last 15 seconds to communicate parallel generation.
- Selecting Shot 02 and requesting manual 3D motion creates a motion-edit node. Its thumbnail is the
  first frame of Hooman's Blender-edit video; clicking opens a full-window player.
- Selecting Shots 4, 5, 6, 7A, 7B, and 8 and asking for intelligent propagation adds the appropriate
  per-shot blockout thumbnails.
- Second generation switches the Final Timeline to the approved shot-by-shot cut.
- Removed reset and editability tooltips, kept click-to-toggle selection, added an independent chat
  scrollbar, fixed the full-window video crop, and moved the final-timeline card to avoid overlap.
- Preserved the approved backup at
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/mockups/workflow_graph_v1_backup_2026-09-24_perfect`.

## 2026-09-24 — Recorded workflow demo and share page

- Hooman's 4:53 recording is `/home/colligo/3d_agent_graph_demo.mov` (962,993,237 bytes, H.264/AAC,
  3420×1196 at 60 fps).
- Added it to a new `workflow demo` tab in the combined provenance gallery.
- Created a fast-start MP4, a 1200×420 poster, and a dedicated Open Graph share page under
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/share/workflow_demo_slack`.
- Published share page:
  `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/workflow_demo_share/index.html`
- The S3 uploads and HTML hashes were verified immediately after publication. Actual Slack unfurl
  behavior remains unverified because this host could not connect to the corporate URL as Slackbot.

## 2026-09-28 — Durable handoff

- Consolidated the complete experiment state, decisions, paths, checksums, URLs, limitations, and
  exact resume instructions in
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/HANDOFF.md`.
- Updated project-level `PROJECT_STATE.md`, `DECISIONS.md`, `LEARNINGS.md`, and `LONG_TERM_PLANS.md`.
- All three prior subagents are complete; no background work is running.
- A fresh S3 read was attempted but blocked because the broker lacks a Pluto token and cached
  credentials are expired. The handoff distinguishes the 2026-09-24 verified publication state from
  the unavailable 2026-09-28 refresh.
