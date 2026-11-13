# How to Author the Full Six-Piece Assembly

## Choose a starting file

- Blank template: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/blender/laundry_sink_full_assembly_rig_v2_blank.blend`
- Working example: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/blender/laundry_sink_full_assembly_rig_v2.blend`

The blank template begins with all six components flat and contains no motion keys. The working example demonstrates all controls, but its order is not authoritative.

## The two controls on every component

Each component has:

1. `PROGRESS_<component>` — select it in the Outliner and edit `install_progress` under Object Properties → Custom Properties. `0` is the layout pose and `1` is the installed pose.
2. `MOVE_ROTATE_<component>` — a visible cube handle at the component. Select it in the 3D viewport and use Blender's standard move and rotate gizmos to add any pickup route or intermediate orientation.

The two layers are additive: progress provides known endpoints, while the cube handle provides user-authored motion between them.

## Author one component

1. Choose the frame when the component should start moving.
2. Select its `PROGRESS_...` object, set `install_progress` to `0`, hover the value, and press `I`.
3. Choose the frame when it should be installed, set the value to `1`, and press `I` again.
4. Scrub to any intermediate frame.
5. Select the component's `MOVE_ROTATE_...` cube in the viewport.
6. Use `G` to move it and `R` to rotate it. Press `I` and choose `Location & Rotation`.
7. Add as many intermediate keys as needed to express pickup height, clearance, pauses, or orientation changes.

Repeat this independently for the other five parts in whatever order and duration you choose.

## Change order or timing

Select a component's `PROGRESS_...` and `MOVE_ROTATE_...` objects, open the Dope Sheet, select their keys, and move them horizontally. No component depends on another component's timeline.

## Installed-pose guides

`POSE_GUIDES_INSTALLED` contains non-rendering wireframe targets. Toggle the collection in the Outliner when you need installation guidance.

## Hands

Hands are not included in v2. Automatic hand-following would attach a hand rig to the moving component; that would reduce your control and introduce a separate animation problem. Once cabinet authoring feels correct, hands can be added as independent handles using the same approach.
