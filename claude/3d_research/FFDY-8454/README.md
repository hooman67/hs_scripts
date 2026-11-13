# FFDY-8454 — Laundry Sink 3D Motion-Rig Experiment

This folder contains the visual assets, editable Blender rig, previews, validation, and notes for the laundry-sink cabinet motion experiment.

For the complete current state, approved shot sequence, published URLs, workflow-demo behavior, and
resume instructions, read
`/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/HANDOFF.md`.

## Research question

Can a simple articulated 3D proxy express the cabinet assembly motions that image/video prompting failed to preserve in shots 5, 6, and 7?

## Scope

- Motion-authoring proof of concept, not a photoreal asset.
- Geometry reconstructed from storyboard evidence; it is not CAD and is not dimensionally authoritative.
- Product parts and low-detail hand guides are included.
- No paid video-generation call is part of this stage.

## Source evidence

Primary source folder: `/home/colligo/hs_scripts/claude/thd/FFDY-7304`

The strongest motion evidence is in:

- `/home/colligo/hs_scripts/claude/thd/FFDY-7304/shots/newshot5_perp_v2.json`
- `/home/colligo/hs_scripts/claude/thd/FFDY-7304/shots/shot6a_v2.json`
- `/home/colligo/hs_scripts/claude/thd/FFDY-7304/shots/shot6b_v2.json`
- `/home/colligo/hs_scripts/claude/thd/FFDY-7304/shots/shot7_v3.json`

## Historical v1 rig controls

The v1 experiment used `CTRL_Master_Select_Me` with these custom properties:

- `end_panel_insert`: shot 5, perpendicular end panel moves vertically into place.
- `side_top_spread`: shots 6/7, upper edges widen by at most 6 degrees while lower pivots stay fixed.
- `bottom_piece_insert`: shot 6, the proxy bottom piece slides into the middle.
- `lock_rail_drop`: shot 7, locking piece drops vertically.
- `left_side_lift`, `right_side_lift`: optional earlier assembly exploration.

Timeline ranges are 1–72 (shot 5), 90–162 (shot 6), and 180–252 (shot 7).

The old v1 `.blend` is no longer present in the current `blender` directory. Its validation report,
editing guide, renders, and this control record remain for history. Use the V4/V5 assets below for
current work.

## Outputs

- Canonical experiment handoff: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/HANDOFF.md`
- Hooman-authored V4 animation: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/blender/laundry_sink_components_v4_image7_corrected_hooman_added_motion.blend`
- Corrected-dimensions/simplified-motion V5 derived from Hooman's animation: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/blender/laundry_sink_components_v5_corrected_geometry_simplified_motion.blend`
- V5 exact changes, evidence, and uncertainty: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/V5_CORRECTED_GEOMETRY.md`
- Recommended image-7-only corrected file: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/blender/laundry_sink_components_v4_image7_corrected.blend`
- V4 component map and editing notes: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/V4_IMAGE7_COMPONENTS.md`
- V4 validation: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/validation/rig_validation_v4_image7_corrected.json`
- Components-only instructions: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/V3_COMPONENTS_ONLY.md`
- Rigid edge-rotation instructions: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/V3_RIGID_EDGE_EDITING.md`
- Components-only validation: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/validation/rig_validation_v3_components_only.json`
- Full-assembly preview: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/renders/full_cabinet_assembly_v2.mp4`
- V2 editing guide: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/V2_HOW_TO_EDIT.md`
- V2 validation: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/validation/rig_validation_v2.json`
- Local review page: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/index.html`
- Key-state contact sheet: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/renders/keyframes_contact_sheet.png`
- Shot previews: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/renders/previews`
- Machine-readable validation: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/validation/rig_validation_v1.json`
- Editing guide: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/HOW_TO_EDIT.md`
- Approved shot-by-shot final cut: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/final_cuts/final_cut_shot_by_shot_v1.mp4`
- Final-cut reproduction script: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/scripts/assemble_final_cut_shot_by_shot.py`
- Complete generation/provenance gallery source: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/gallery_combined_breakdown/index.html`
- Interactive workflow-demo source: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/mockups/workflow_graph_v1/index.html`
- Preserved approved demo backup: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/mockups/workflow_graph_v1_backup_2026-09-24_perfect`
- Slack/Open Graph demo share page: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/share/workflow_demo_slack/index.html`

## Status

The POC is complete through the approved final cut, interactive workflow mockup, and recorded demo.
V4 is the authoritative Hooman-authored motion source. V5 is the recommended corrected/simplified
successor for further Blender work. Earlier V3 leg variants placed the two legs on a non-central
component and are superseded. The historical V1, V2, and V3 `.blend` files referenced in older chat
or notes are no longer present in the current folder; their documentation, validations, and renders
remain. Production integration and a matched benchmark against the incumbent remain future
research, not completed work.
