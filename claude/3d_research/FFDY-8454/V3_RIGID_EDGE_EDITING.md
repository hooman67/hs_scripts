# Native Rigid Edge Rotation

> Superseded: this document describes the earlier incorrect component mapping. Use `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/V4_IMAGE7_COMPONENTS.md` and `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/blender/laundry_sink_components_v4_image7_corrected.blend` instead.

Use `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/blender/laundry_sink_components_only_v3_with_legs_rigid_edges.blend`.

This remains a components-only Blender file. There are no custom handles, sliders, drivers, guides, or constraints. Each component's ordinary Blender object origin has simply been moved onto a useful floor-contact edge, and object scaling has been locked.

The bottom panel includes the two short corner-leg extensions visible in the storyboard photographs. Their presence is high-confidence; their exact dimensions are approximate because this remains a photo-derived proxy.

## Lift the bottom panel onto its edge

1. Stay in **Object Mode**.
2. Select `CABINET_04_BOTTOM_PANEL`.
3. Go to the desired starting frame and press `I` → `Location & Rotation`.
4. Move to the desired ending frame.
5. Press `R`, then `X`, type `90`, and press Enter.
6. Press `I` → `Location & Rotation` again.

The near long edge remains at the pivot while the complete rigid panel rotates upward.

## Suggested edge rotations

- Front frame: `R`, `X`, `90`.
- Left side: `R`, `Y`, `90`.
- Right side: `R`, `Y`, `-90`.
- Bottom panel: `R`, `X`, `90`.
- Wide and narrow rails: begin with `R`, `Y`, `-90`, then reposition as needed.

## Why Edit Mode behaved differently

Edit Mode transforms vertices and edges inside a mesh. Moving one selected edge changes edge lengths, face angles, dimensions, and proportions. It does not rotate the complete rigid object.

Object Mode transforms the complete mesh without changing the distances between its vertices. Rotation around an edge is achieved by placing the object origin—or the temporary 3D Cursor pivot—on that edge.

## Dimensions versus scale

Scale is locked at `(1, 1, 1)`. The actual mesh geometry remains fixed during Object Mode movement and rotation.

Blender's displayed `Dimensions` values are the object's axis-aligned bounding box. Those numbers may swap or change as a rigid rectangular panel rotates, even though its physical side lengths and proportions have not changed. This is expected. The important invariant is that Scale remains `(1, 1, 1)` and the mesh is not edited.

## Use a different edge temporarily

1. Enter Edit Mode only long enough to select the desired edge.
2. Press `Shift+S` → `Cursor to Selected`.
3. Return immediately to Object Mode without moving the edge.
4. Set the pivot mode to `3D Cursor` using the `.` pivot menu.
5. Rotate the whole object and keyframe both Location and Rotation.
6. Restore the pivot mode to `Median Point` afterward.

Selecting an edge in Edit Mode is safe; moving that edge in Edit Mode is what deforms the object.
