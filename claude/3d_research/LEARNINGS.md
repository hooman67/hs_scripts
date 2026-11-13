# Learnings

## Confidence legend

- `VERIFIED` — directly supported by a current primary source or independent confirmation.
- `ASSUMED` — transparent working interpretation requiring validation.
- `UNVERIFIED` — plausible claim without sufficient direct support.
- `USER-CONFIRMED` — supplied by Hooman; authoritative for preference or decision.

## 2026-09-24 — Selective 3D motion control POC

`VERIFIED` for the laundry-sink task — Storyboard-derived Blender blockouts materially improved
Seedance adherence on cabinet assembly motions that prior sketches, annotations, and text prompting
had not preserved. The accepted final sequence uses blockout-guided outputs for multiple difficult
assembly stages.

`ASSUMED` beyond this task — The result supports selective 3D control as a promising escalation path,
not a universal default. It has not been repeated across products or compared to the motion-bank
incumbent using a matched accuracy-and-effort rubric.

Sources:

- `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/HANDOFF.md`
- `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/final_cuts/final_cut_shot_by_shot_v1.inputs.json`
- `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/seedance_results/blockout_v1`

## 2026-09-24 — Seedance motion-prompt behavior

`VERIFIED` for the sampled retries — Short Event Script changes that assign continuous human
support and make `@Video1` authoritative for geometry/trajectory reduced autonomous “flying board”
motion and improved the cabinet footprint and insertion trajectory.

`VERIFIED` for the sampled Shot 7B retry — More descriptive wording introduced a new failure. The
phrase emphasizing the component's “largest broad rectangular face” corrected seating orientation
but changed the thin strip into a full-width lid-like panel. Small positive relative-identity wording
performed better than negative or size-superlative wording.

Limitation: most variants are `n=1`; these are task-local observations, not general model laws.

## 2026-09-24 — Combined call versus isolated shots

`VERIFIED` for this experiment — The combined Seedance call inferred eight visual shots and seven
cuts without supplied boundary timestamps, demonstrating useful automatic decomposition. It also
showed topology drift and temporary extra panels. Isolated shot calls were easier to diagnose,
prompt, and curate into the approved final cut.

## 2026-09-24 — Workflow product hypothesis

`USER-CONFIRMED` — The desired experience begins with automatic storyboard understanding and a
reviewable shot graph, then lets the user selectively request a 3D motion input for a difficult shot,
author the motion visually, propagate it to related shots, and regenerate.

`ASSUMED` — This selective-escalation design may reduce customer effort compared with requiring a
fully curated motion bank or a Blender blockout for every shot. It remains a mockup; no usability
study or production backend exists.

## 2026-09-24 — Share-page validation boundary

`VERIFIED` — The dedicated demo page contains a fast-start H.264/AAC MP4, 1200×420 poster, and Open
Graph image/video metadata, and the uploaded S3 object sizes/content types matched the local files
immediately after publication.

`UNVERIFIED` — Actual Slack unfurl behavior could not be tested from the host because the corporate
Foundry endpoint timed out for a Slackbot-style HTTP request.

## 2026-09-22 — Evaluation objective

`USER-CONFIRMED` — The desired workflow must beat the current best THD result on accuracy and be
easier for a non-technical customer. Motion-bank curation is a material usability burden.

Source: Hooman in the current research session.

## 2026-09-22 — Existing THD control findings

`VERIFIED` for the recorded THD experiment scope — Positional reference roles, ordered keyframes,
reference framing, and small prompt deltas have materially affected Seedance adherence in prior THD
experiments. These findings do not by themselves validate Blender blockouts.

Sources:

- `/home/colligo/hs_scripts/claude/dotclaude/memory/project_thd_video_rewriter.md`
- `/home/colligo/hs_scripts/claude/dotclaude/memory/feedback_lighter_touch_prompts.md`

## 2026-09-22 — Blockout proposal headline

`VERIFIED`, narrowly scoped — A synthetic Blender video reference can exert strong visible control
over Seedance camera, staging, broad action, and timing in the sampled deployed clips.

`UNVERIFIED` as a general accuracy result — The reported camera 2.97/3 and
blocking/action/timing 3.00/3 measure similarity to the blockout, not correctness, product fidelity,
or publishability. The 19 outputs cover seven scene types and the raw judgment records are not in
the durable repository or deployed docroot.

`UNVERIFIED` as an end-to-end speed comparison — Astra's 9m08s covered only the Blender scene block,
while additional prompt mapping and integration work occurred outside the harness. It remains a
credible existence proof that Astra can operate the established rig.

Source retrieved 2026-09-22:
`/tmp/thd-proj-everbilt-render/docs/blockout/REPRODUCE.md`, commit
`b4b684f268e49bf38a6a7c0fa70b4a7a6244d878`.

## 2026-09-22 — Blockout as an intermediate representation

`ASSUMED` — The customer-friendly opportunity is to treat a blockout as a model-generated,
validated intermediate representation. A non-technical customer should provide intent and approve
a cheap preview; an agent should own Blender, rig code, geometry checks, and semantic mapping.

Verification path: measure full human intervention and correction time across repeated Astra runs
on diverse tasks.

## 2026-09-22 — Incumbent evidence footprint

`VERIFIED` from the user-selected HTML — The incumbent report contains 54 shots (52 succeeded), 147
ordinary reference images, 74 storyboard images, 211 processed images, and 14 motion clips. The
report says the run uses person-gated sketch-Nano, not SAM3 anonymization despite the legacy
filename.

Source: S3 object linked in `/home/colligo/hs_scripts/claude/3d_research/README.md`, retrieved
2026-09-22 through the Foundry S3 gateway.

## 2026-09-22 — Reusable articulated-product hypothesis

`USER-CONFIRMED` objective — Instead of authoring an unconstrained blockout from scratch for every
shot, build each known SKU once from CAD as a component-aware articulated rig. Encode allowable
translations/rotations and let a product-knowledgeable human visually keyframe the desired motion.
Begin with product parts and hands; add workpiece, camera, effects, and richer physical interaction
only after the core idea is validated.

`ASSUMED` — This could amortize expert product knowledge more effectively than a fixed motion bank:
one rig could express many motion variants rather than requiring one curated source clip per
variant. It still requires validation that Seedance follows the rendered mechanical motion and
does not inherit blockout appearance or lose product identity.

## 2026-09-22 — First SKU and geometry search

`VERIFIED` — The live V2 bank contains six families. `ryobi_miter_saw` has 18 labels over 17 unique
clips, the largest label count and tied with the jigsaw on unique clip count.

`ASSUMED` — The incumbent reference image is the RYOBI PBT01B. It is a strong visual match to the
manufacturer imagery, but the bank does not record exact SKU provenance.

`VERIFIED` for the bounded search — No authoritative, exact, downloadable PBT01B CAD was found.
Two CC BY Sketchfab alternatives exist, but one is crude and one appears scan-derived; neither has
been downloaded or validated as componentized geometry.

## 2026-09-22 — Blender and Astra readiness

`VERIFIED` — Blender 5.2.2 LTS is installed and passes headless startup, proposal-script loading,
geometry validation, still render, and H.264 smoke tests. The host is CPU-only and lacks an active
visual desktop.

`VERIFIED` — GPT-6 Astra is selectable in this Codex environment; a parallel task executed with it.
No Hooman-provided API key is needed through this route. Official model documentation lists text
and image inputs, not native video input.

## 2026-09-22 — Storyboard-derived laundry cabinet rig v1

`VERIFIED` — The saved FFDY-7304 prompts and annotations are sufficient to encode deterministic
motion constraints for shots 5–7: a single end-panel descent, a small top-only wall spread with
fixed lower pivots, a middle-piece insertion, and a vertical lock-piece drop followed by closure.
The Blender validation suite passes all nine programmed checks.

`ASSUMED` — Storyboards alone are sufficient for the proxy topology. They are not sufficient to
claim exact panel identity, dimensions, or joinery. The shot-6 “bottom piece” remains the most
important human-review ambiguity before using the blockout as video-model conditioning.

Artifacts: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454`.

## 2026-09-23 — Full-assembly authoring control

`USER-CONFIRMED` — The current scope is exactly the six cabinet pieces. The user must control the
assembly order and all timing. The workflow should expose as much spatial control as practical
rather than reduce each motion to an opaque automatic pickup.

`VERIFIED` for the v2 proxy — A two-layer control design works in Blender: an independent 0–1
layout/installed baseline per component plus an additive visible handle for arbitrary translation
and rotation keys. The six channels do not move one another, and the six direct handles are also
isolated. All eleven v2 validation checks pass.

`ASSUMED` — The storyboard's six cabinet pieces are front frame/doors, left side, right side,
bottom panel, wide rail, and narrow rail. This is sufficient to test interaction but not to claim
manufacturer-accurate part identity or assembly geometry.

## 2026-09-23 — Rigid motion versus Edit Mode deformation

`VERIFIED` — Translating a selected edge in Blender Edit Mode changes mesh vertex positions and can
change component dimensions. A rigid panel lift should instead rotate the entire object in Object
Mode around an origin or temporary 3D Cursor placed on the contact edge. Moving each v3 component's
origin to a useful edge preserved its world geometry exactly; locking scale at `(1,1,1)` prevents
Object Mode scaling but cannot prevent deliberate mesh edits in Edit Mode.

`USER-CONFIRMED` and visually verified from storyboard image 7 — The two legs belong to the central
front-frame/door assembly, not the upper-left wall panel. The central assembly also contains two
doors, four visible hinges, a smaller rectangular section, and orange connector areas. The other
five pieces are two side panels, a plain upper-left top wall, and two unequal narrow boards at right.
Dimensions remain approximate without CAD or a dimensioned drawing.
