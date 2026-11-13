# Decisions

## 2026-09-24 — Approved final shot sequence

Status: `[USER-CONFIRMED]`

Decision: Use the exact 11-shot sequence recorded in
`/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/final_cuts/final_cut_shot_by_shot_v1.inputs.json`
for the shot-by-shot final cut. The accepted blockout-guided assembly shots are Shot 4 Event Script
v2, Shot 6 Event Script v2, Shot 7A Event Script v2, Shot 7B v4C.2 narrower strip, and the isolated
Shot 8 call.

## 2026-09-24 — Customer-workflow demo behavior

Status: `[USER-CONFIRMED]`

Decision: The prototype begins with a planned graph and no generated results. First generation
simulates four minutes and populates parallel outputs only from 03:45–04:00. The user then selects
Shot 02, requests a manually editable 3D motion input, plays the Blender-edit walkthrough, selects
Shots 4–8 for intelligent motion propagation, and regenerates. The second final output is the
approved shot-by-shot cut. Preserve the approved backup documented in the FFDY-8454 handoff.

## 2026-09-24 — Result-gallery preservation and provenance

Status: `[USER-CONFIRMED]`

Decision: Never delete or overwrite content in result HTMLs unless Hooman explicitly requests it.
Each result card must show only the inputs actually sent to the model, along with the full prompt,
parameters, payload, and output. Diagnostic contact sheets must not be presented as inputs.

## 2026-09-24 — Shot 7B accepted result

Status: `[USER-CONFIRMED]`

Decision: Use `shot07B_identity_v4c_narrow_v2` for the final thin-strip installation. Preserve the
failed `shot07B_broad_face_v5` files for research history, but omit its card from the public gallery
as explicitly requested.

## 2026-09-22 — Research-only phase

Status: `[USER-CONFIRMED]`

Decision: Understand the proposal first, then jointly design experiments, run them gradually, and
only later consider adoption or integration. Production implementation is out of scope during the
research phase.

## 2026-09-22 — Paid generation gate

Status: `[USER-CONFIRMED]`

Decision: Do not run paid Seedance generations unless Hooman explicitly asks for a specific run.

## 2026-09-22 — Incumbent baseline

Status: `[USER-CONFIRMED]`

Decision: Use the 2026-09-12 kitchen expanded-text-elements motion-bank result linked in `README.md`
as the current quality baseline. Seek a workflow that improves accuracy while being easier for a
non-technical customer than curating a motion bank.

## 2026-09-22 — Initial articulated-product scope

Status: `[USER-CONFIRMED]`

Decision: For proof of concept, Hooman is the user and may work directly in Blender if that is the
fastest route. Motion authoring should be visual rather than textual. Begin from the finite current
motion-bank catalog, use CAD and manufacturer specifications as the geometry and kinematic source
of truth, and initially control the product rig plus hands. Customer-facing tooling can be
considered after feasibility is established.

Correction: the current V2 bank contains six product families, not the five initially assumed.

## 2026-09-22 — First product family

Status: `[USER-CONFIRMED]`

Decision: Start input collection with the sliding compound miter-saw family because it is the
suggested high-coverage candidate. PBT01B is currently only a high-confidence visual identification,
not a verified exact bank SKU.

## 2026-09-22 — FFDY-8454 experiment boundary

Status: `[USER-CONFIRMED]`

Decision: Keep all laundry-sink rig visual assets and experiment-specific notes under
`/home/colligo/hs_scripts/claude/3d_research/FFDY-8454`. Treat
`/home/colligo/hs_scripts/claude/thd/FFDY-7304` as read-only source evidence.

## 2026-09-23 — Full-assembly authoring authority

Status: `[USER-CONFIRMED]`

Decision: Limit the current rig to the six cabinet components. The user, not the customer video or
the rig, controls assembly order, timing, pickup path, and intermediate rotations. Defer hands until
the cabinet-authoring interaction is validated.
