# FFDY-8454 canonical handoff

As of: 2026-09-28

This is the durable technical and product-context handoff for the laundry-sink 3D-motion experiment.
It is intended to let a new agent continue without the prior chat transcript. Read the project-level
`/home/colligo/hs_scripts/claude/3d_research/README.md` and
`/home/colligo/hs_scripts/claude/3d_research/PROJECT_STATE.md` first.

## Contents

- [Outcome](#outcome)
- [User intent and boundaries](#user-intent-and-boundaries)
- [Shared vocabulary and Blender model](#shared-vocabulary-and-blender-model)
- [Durable working rules](#durable-working-rules)
- [Experiment history](#experiment-history)
- [Current Blender assets](#current-blender-assets)
- [Seedance results and approved final sequence](#seedance-results-and-approved-final-sequence)
- [Published galleries](#published-galleries)
- [Workflow demo behavior](#workflow-demo-behavior)
- [Recorded demo and Slack share page](#recorded-demo-and-slack-share-page)
- [Evidence-backed learnings](#evidence-backed-learnings)
- [Known limitations and contradictions](#known-limitations-and-contradictions)
- [Reproduction and checksums](#reproduction-and-checksums)
- [Exact resume instructions](#exact-resume-instructions)

## Outcome

`USER-CONFIRMED` — The proof of concept is successful enough that Hooman said the final workflow
demo was “perfect” and later “fantastic.” The project now has:

1. a user-authored Blender animation for the six cabinet components;
2. rendered blockout references for the difficult assembly motions;
3. Seedance retries that substantially improved motion adherence and physical plausibility;
4. an approved 11-shot final cut assembled from the best original and blockout-guided shots;
5. an interactive graph/chat workflow mockup showing how selective 3D motion authoring could fit a
   customer workflow; and
6. a recorded 4:53 walkthrough plus a dedicated share page.

This is still research and a mock prototype. It is not a production implementation, a measured
benchmark against the incumbent, or proof that the workflow generalizes to other products.

## User intent and boundaries

- `USER-CONFIRMED` — Research supports understanding, benchmarking, possible adoption, and possible
  integration, in that order and through gradual experiments.
- `USER-CONFIRMED` — Production implementation remains out of scope during research.
- `USER-CONFIRMED` — Never run paid Seedance calls unless Hooman explicitly requests the specific
  run. The calls recorded here were explicitly requested.
- `USER-CONFIRMED` — The current incumbent is the curated motion-bank HTML linked from
  `/home/colligo/hs_scripts/claude/3d_research/README.md`. A candidate must improve accuracy and be
  easier for a non-technical customer.
- `USER-CONFIRMED` — For the proof of concept, Hooman is the customer and direct Blender use is
  acceptable. The desired control is visual because text is poor at specifying precise motion.
- `USER-CONFIRMED` — The reusable-product hypothesis is a finite catalog of CAD/spec-derived rigs
  whose moving parts and constraints are set once, with a product-knowledgeable human supplying the
  desired animation.
- `USER-CONFIRMED` — The laundry-sink experiment is limited to the six cabinet components. The user,
  not the customer video or a preset rig, controls assembly order, timing, paths, and rotations.

## Shared vocabulary and Blender model

- A **blockout** is a deliberately low-detail 3D staging/animation that communicates camera,
  positions, timing, trajectories, and contact. It is a motion specification, not the final visual.
- Blender is a general 3D scene and animation application. A `.blend` stores meshes, object
  transforms, rigs/constraints, cameras, lights, materials, and timeline keyframes. It is not itself
  an MP4; Blender renders the animated scene to image frames or a video file.
- A mesh is an object's polygonal surface. A Gaussian splat is a learned point-like scene
  representation mainly suited to capturing/rendering appearance. A Blender scene can combine
  editable meshes with object hierarchy, pivots, constraints, animation, and cameras, which is why
  it was used for motion authoring here.
- In Blender, moving an edge in **Edit Mode** deforms mesh vertices. To preserve a rigid board's
  dimensions, move/rotate the whole object in **Object Mode**, keep scale at `(1,1,1)`, and place the
  object's origin or the 3D Cursor on the desired hinge/contact edge.
- An **Empty** is a non-rendering transform object. Parenting all assembled components to an Empty
  lets the user rotate the complete cabinet around the Empty's pivot without joining/deforming the
  pieces.
- Animation requires meaningful keys at both the starting and later frames. Key location and
  rotation for the selected object(s); copying a keyframe to a future frame is a valid way to hold
  the current pose before the next motion begins.

## Durable working rules

1. Result galleries are append-only unless Hooman explicitly requests a deletion or replacement.
   Do not silently delete or overwrite existing cards, tabs, outputs, or provenance.
2. Every generation card must show the exact prompt, every actual model input, parameters, payload,
   and output. Do not display diagnostic contact sheets as if they were model inputs.
3. Hooman prefers videos, images, and generation comparisons in reviewable HTML galleries, not only
   filesystem links.
4. Prompt tuning should be the smallest possible delta. Preserve a good prompt and change only the
   necessary Event Script language. Over-descriptive instructions repeatedly hurt Seedance.
5. When Hooman asks for work in the background, delegate the bounded task and leave the main session
   available. Canonical-file synthesis stays in the main session.
6. Use the mandatory research playbook at `/home/colligo/.codex/RESEARCH_RULES.md`.
7. Use `/aws-creds` for Foundry S3 access. Never write credentials into tracked files or ask Hooman
   to paste them. On 2026-09-28 the broker had no Pluto token and both
   `/home/colligo/.claude/hshariati/aws_creds.env` and `/mnt/localssd/tmp_creds.txt` were expired.
8. Preserve the workflow-demo backup at
   `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/mockups/workflow_graph_v1_backup_2026-09-24_perfect`.

## Experiment history

### Geometry and authoring

- V1 encoded narrow shot-specific controls for shots 5–7.
- V2 explored six components with one 0–1 layout/installed control and one additive transform
  handle per component.
- V3 removed all custom controls so Hooman could test native Blender editing.
- The initial V3 leg correction was wrong and is superseded. Hooman directed that only
  `storyboard_all_pieces_image7.jpeg` be used to correct component identity.
- V4 rebuilt the six components from image 7. The central front-frame/door assembly owns the two
  legs, two doors, hinges, small upper rectangle, and orange top/bottom regions.
- Hooman authored the actual assembly animation in the V4 file.
- V5 propagated final fitted dimensions and orientations back to the starting layout, baked scale
  into rigid geometry, and removed an avoidable 180-degree flip to simplify the reference motion.

### Generation and refinement

- One combined Seedance call used all blockout/reference inputs. It inferred eight visual segments
  and seven cuts without boundary timestamps. This was promising but exhibited topology drift and
  temporary extra panels.
- Isolated shot calls gave better control and made debugging easier.
- Shot 2 and Shot 4 retries removed unnecessary flips by using short Event Scripts that told the
  couple to follow `@Video1`.
- Shot 5–7 retries improved physical contact by explicitly assigning people to support the moving
  panel and restricting `@Video1` to geometry/trajectory while using the still image for appearance.
- Shot 7B required several identity tests. The accepted result is
  `shot07B_identity_v4c_narrow_v2`; it preserves v4C's smooth motion while making the strip narrower.
- The `shot07B_broad_face_v5` retry is a failed result: it corrected broad-face seating but changed
  the strip into a full-width lid. Hooman explicitly asked that this card be deleted from the public
  result HTML. The local files remain for research history.

## Current Blender assets

### Authoritative motion source

- Hooman-authored animation:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/blender/laundry_sink_components_v4_image7_corrected_hooman_added_motion.blend`
- SHA-256: `625958fc71592b4f9b747b54af51ab84d554d6738919085fe4f9f486b0f09275`

### Corrected successor

- Recommended simplified-geometry successor:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/blender/laundry_sink_components_v5_corrected_geometry_simplified_motion.blend`
- SHA-256: `7fcd3359daa065d37c9b4cca67a01b53b471b4ad3056734188a45a2c715c7c69`
- Change report:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/V5_CORRECTED_GEOMETRY.md`
- Validation:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/validation/rig_validation_v5_corrected_geometry.json`
- Visual evidence:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/renders/v5_geometry_evidence/old_new_contact_sheet.png`
- No-flip preview:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/renders/v5_geometry_evidence/v5_large_board_no_flip.mp4`

### Blockout references

- Rendered per-shot blockouts and review frames:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/renders/seedance_blockouts`
- Generation outputs and complete request provenance:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/seedance_results/blockout_v1`

## Seedance results and approved final sequence

`USER-CONFIRMED` — Hooman said “we have all the shots now” and supplied this exact sequence. The
final assembly uses each clip at full length with straight cuts:

1. `S01 — establishing hero`: `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/assets/S01.mp4`
2. `ORDERED KEYFRAMES image7 → image5 → image6`: `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/assets/1A.mp4`
3. `image13 connector macro`: `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/assets/3A_v1.mp4`
4. `Shot 4 Event Script v2`: `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/3d_blockout_combined_v1/assets/shot04_event_script_v2_output.mp4`
5. `Shot 6 Event Script v2`: `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/3d_blockout_combined_v1/assets/shot06_event_script_v2_output.mp4`
6. `Shot 7A Event Script v2`: `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/3d_blockout_combined_v1/assets/shot07A_event_script_v2_output.mp4`
7. `Shot 7B v4C.2 narrower strip`: `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/3d_blockout_combined_v1/assets/shot07B_identity_v4c_narrow_v2_output.mp4`
8. `Shot 8 isolated blockout`: `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/3d_blockout_combined_v1/assets/shot08_blockout_v1_output.mp4`
9. `4A paint-out plate + couple`: `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/assets/4A.mp4`
10. `4B paint-out plate + couple`: `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/assets/4B.mp4`
11. `8B paint-out plate + couple`: `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/assets/8B.mp4`

Final cut:

- Local video:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/final_cuts/final_cut_shot_by_shot_v1.mp4`
- Duration/format: 54.462 seconds, H.264, 1920×1080, 24 fps, yuv420p, no audio, fast-start.
- SHA-256: `39b4f818e6f5e3bb03156e9060ae6612747836f28e85c15bd80c2a3fb956d862`
- Reproduction script:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/scripts/assemble_final_cut_shot_by_shot.py`
- Exact input manifest:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/final_cuts/final_cut_shot_by_shot_v1.inputs.json`
- Published video:
  `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/3d_blockout_combined_v1/assets/final_cut_shot_by_shot_v1.mp4`

## Published galleries

- Original laundry-sink gallery:
  `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/index.html`
- Complete combined-call and per-shot provenance gallery:
  `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/3d_blockout_combined_v1/index.html`
- Local source for that gallery:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/gallery_combined_breakdown/index.html`
- Its tabs are: complete call, Stages 1–8, `Final Cut made shot by shot`, and `workflow demo`.
- Blender V5 review:
  `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/blender_v5_review/index.html`

The combined gallery was hash-verified against S3 immediately after the 2026-09-24 publish. Its
local SHA-256 is `2a517a15f6f707cd7960032482f87b1a214f74f84f4e5d48d042593e26a9e11a`.
Fresh S3 verification on 2026-09-28 was not possible because all available AWS credentials had
expired and the broker lacked a Pluto token.

## Workflow demo behavior

Live demo:
`https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/workflow_mock_v1/index.html`

Local source:
`/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/mockups/workflow_graph_v1/index.html`

The interaction Hooman approved is:

1. Fresh refresh shows the 12-shot plan, but no generated output thumbnails and no final video.
2. Normal click toggles shot selection; Shift is not required.
3. First `Generate video` simulates four minutes. The timer fast-forwards from 00:00 to 03:45 with
   no outputs, then all 12 shot thumbnails populate during the last 15 seconds to represent parallel
   generation.
4. The first Final Timeline video is
   `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/assets/final_spot_all_shots_v3.mp4`.
5. Select Shot 02 and type a message containing the intent “The motion is wrong, give me a 3D model
   of this so that I can input the motion manually.” The agent replaces the inferred-motion input
   with a 3D motion-edit node.
6. That node uses the first frame of Hooman's Blender-edit recording as its thumbnail. Clicking it
   opens a full-window in-app editor and plays `assets/blender_edit_video.mp4`; the full video is
   visible without lower-half cropping.
7. Select Shots 4, 5, 6, 7A, 7B, and 8 and ask to intelligently propagate the motion. Each selected
   shot receives a motion input with the relevant Blender blockout thumbnail.
8. The second generation repeats the four-minute simulation and changes the Final Timeline to the
   approved shot-by-shot cut:
   `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/3d_blockout_combined_v1/assets/final_cut_shot_by_shot_v1.mp4`.
9. The chat has its own vertical scrollbar and pinned composer. The Reset Demo button and editing
   tooltips are intentionally absent. The Final Timeline card was shifted right to avoid overlap.

The live local HTML SHA-256 is
`6ee08002f22103b6391dc1a24ab232a33417b1936e264cf3c560060317a8f812`. It was hash-verified against
S3 immediately after the 2026-09-24 publish.

Do not alter this backup unless Hooman explicitly asks:

- Local:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/mockups/workflow_graph_v1_backup_2026-09-24_perfect`
- Published:
  `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/workflow_mock_v1_backup_2026-09-24_perfect/index.html`

## Recorded demo and Slack share page

- Original recording from Hooman:
  `/home/colligo/3d_agent_graph_demo.mov`
- Original size: 962,993,237 bytes; duration 292.967 seconds; H.264/AAC; 3420×1196 at 60 fps.
- Original SHA-256: `cf6dadd9af28de77ed5f5f666ee905ea1523404839454fda3d71b239b1b948f7`
- The original was uploaded into the combined gallery and appears in the `workflow demo` tab:
  `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/3d_blockout_combined_v1/assets/3d_agent_graph_demo.mov`
- Dedicated Slack/Open Graph share page:
  `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/workflow_demo_share/index.html`
- Local share-page source:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/share/workflow_demo_slack/index.html`
- Fast-start MP4 used by the page:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/share/workflow_demo_slack/assets/3d_agent_graph_demo.mp4`
- Open Graph poster:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/share/workflow_demo_slack/assets/3d_agent_graph_demo_poster.jpg`

The share page includes `og:title`, `og:description`, `og:image`, `og:video`, video dimensions/type,
and Twitter summary-card metadata. S3 object sizes and content types were verified immediately after
publication on 2026-09-24. A Slackbot-style HTTP fetch could not be verified from this host because
`foundry-aws-corp.adobe.io:443` timed out; therefore the Open Graph metadata is verified in the
published object, while actual Slack unfurl behavior remains `UNVERIFIED`.

## Evidence-backed learnings

- `VERIFIED` for this task — A coarse Blender render can be a strong motion reference even when its
  appearance is intentionally crude. It materially improved difficult assembly trajectories that
  sketches, annotations, and prose had failed to preserve.
- `VERIFIED` for this task — Isolated per-shot reference-to-video calls were more controllable and
  auditable than asking one combined call to infer all boundaries and actions.
- `VERIFIED` for this task — Explicit hand ownership/support language fixed “flying board” physics
  failures in sampled retries.
- `VERIFIED` for this task — Assigning blockout geometry, proportions, camera, and trajectory to
  `@Video1`, while limiting the still to appearance, improved rectangular footprint and trajectory
  adherence in Shots 7A/7B.
- `VERIFIED` for this task — More description is not automatically better. Small Event Script edits
  were successful; broad-face superlative wording fixed orientation but destroyed thin-strip
  identity.
- `VERIFIED` for this task — Blender's Edit Mode moves vertices and can deform rigid parts. Rigid
  panels should be transformed in Object Mode around a useful origin/3D Cursor, with scale kept at
  `(1,1,1)`.
- `ASSUMED` — A reusable CAD-derived articulated rig could amortize expert product knowledge better
  than a curated motion bank, but the laundry-sink proxy does not yet measure rig-building cost or
  generalization.
- `ASSUMED` — The most promising product design is an agent-created plan with simple references by
  default and selective escalation to 3D authoring only for shots whose motion cannot be expressed
  reliably in text/images.

## Known limitations and contradictions

- The six cabinet components were reconstructed from storyboard image 7, not CAD. Dimensions,
  joinery, and exact topology are approximate.
- The final cut is user-approved as a demonstration sequence, but no blinded or rubric-based
  benchmark against the incumbent has been performed.
- Seedance conclusions are task-local and mostly `n=1` per prompt variation.
- The demo is scripted front-end behavior, not a working orchestration backend.
- The Open Graph share page has the correct metadata but actual Slack unfurl behavior was not
  observable from this machine.
- Current S3 state was last hash-verified on 2026-09-24. A 2026-09-28 refresh was blocked by expired
  credentials. Always fetch the live object before the next gallery edit.

## Reproduction and checksums

The most important reproducible files and hashes are listed above. Additional exact generation
prompts, input media, submitted fal payloads, results, and costs live under:

`/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/seedance_results/blockout_v1`

The combined gallery is itself the human-readable provenance record. The final-cut JSON manifest is
the machine-readable record for the 11 selected clips.

No credentials, fal keys, cookies, or tokens are stored in this handoff.

## Exact resume instructions

1. Read, in order:
   - `/home/colligo/hs_scripts/claude/3d_research/README.md`
   - `/home/colligo/hs_scripts/claude/3d_research/PROJECT_STATE.md`
   - `/home/colligo/hs_scripts/claude/3d_research/DECISIONS.md`
   - `/home/colligo/hs_scripts/claude/3d_research/LEARNINGS.md`
   - this file
2. Do not repeat completed Blender, generation, final-cut, or demo work.
3. Refresh Foundry credentials using `/aws-creds`. If the Pluto token is still absent, surface that
   blocker and do not claim the remote objects are current.
4. Before any HTML change, download the latest S3 object and merge on top of it. Preserve every
   existing card/tab unless Hooman explicitly requests removal or replacement.
5. There is no active generation or background job. The three prior subagents all completed.
6. The next research decision is not yet user-confirmed. The cheapest useful next step is to define
   a matched evaluation of accuracy **and authoring effort** for the 3D-assisted sequence versus the
   incumbent motion-bank workflow. Ask Hooman whether to begin that evaluation or pursue another
   idea; do not assume production integration is authorized.
