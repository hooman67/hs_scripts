#!/usr/bin/env python3
"""Add the two photographed corner legs to the current v3 bottom-panel mesh."""

from pathlib import Path
import json

import bpy
from mathutils import Vector


ROOT = Path("/home/colligo/hs_scripts/claude/3d_research/FFDY-8454")
OUT = ROOT / "blender" / "laundry_sink_components_only_v3_with_legs.blend"
REPORT = ROOT / "validation" / "rig_validation_v3_with_legs.json"

bottom = bpy.data.objects["CABINET_04_BOTTOM_PANEL"]
original_world = bottom.matrix_world.copy()
original_scale = tuple(bottom.scale)
original_animation = bottom.animation_data

local_points = [Vector(corner) for corner in bottom.bound_box]
min_x = min(p.x for p in local_points)
max_x = max(p.x for p in local_points)
min_y = min(p.y for p in local_points)
max_y = max(p.y for p in local_points)
max_z = max(p.z for p in local_points)

leg_width = 0.075
leg_extension = 0.075
panel_thickness = min(0.035, max_y - min_y)
material = bottom.data.materials[0] if bottom.data.materials else None
legs = []

for side, x in (("LEFT", min_x + leg_width / 2),
                ("RIGHT", max_x - leg_width / 2)):
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    leg = bpy.context.object
    leg.name = f"BOTTOM_PANEL_{side}_LEG"
    leg.dimensions = (leg_width, panel_thickness, leg_extension)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        leg.data.materials.append(material)
        leg.color = material.diffuse_color
    bevel = leg.modifiers.new("Soft_Edges", "BEVEL")
    bevel.width = 0.008
    bevel.segments = 2
    leg.parent = bottom
    leg.location = (x, 0, max_z + leg_extension / 2)
    legs.append(leg)

# Apply bevels, detach in place, and join into the existing rigid component.
for leg in legs:
    bpy.ops.object.select_all(action="DESELECT")
    leg.select_set(True)
    bpy.context.view_layer.objects.active = leg
    bpy.ops.object.modifier_apply(modifier="Soft_Edges")
    world = leg.matrix_world.copy()
    leg.parent = None
    leg.matrix_world = world

bpy.ops.object.select_all(action="DESELECT")
bottom.select_set(True)
for leg in legs:
    leg.select_set(True)
bpy.context.view_layer.objects.active = bottom
bpy.ops.object.join()
bottom.name = "CABINET_04_BOTTOM_PANEL"

# Preserve all current user-authored object state while only changing mesh topology.
bottom.matrix_world = original_world
bottom.scale = original_scale
if original_animation is None:
    bottom.animation_data_clear()

updated_points = [Vector(corner) for corner in bottom.bound_box]
updated_max_z = max(p.z for p in updated_points)
updated_min_x = min(p.x for p in updated_points)
updated_max_x = max(p.x for p in updated_points)

components = list(bpy.data.collections["CABINET_COMPONENTS_DIRECT"].objects)
checks = {
    "exactly_six_components": len(components) == 6,
    "bottom_panel_remains_one_mesh": bottom.type == "MESH" and
                                      bottom.name == "CABINET_04_BOTTOM_PANEL",
    "two_corner_extensions_added": updated_max_z >= max_z + leg_extension - 1e-5,
    "full_width_preserved": abs(updated_min_x - min_x) < 1e-5 and
                            abs(updated_max_x - max_x) < 1e-5,
    "object_transform_preserved": all(
        abs(bottom.matrix_world[i][j] - original_world[i][j]) < 1e-6
        for i in range(4) for j in range(4)
    ),
    "scale_preserved": tuple(bottom.scale) == original_scale,
}

scene = bpy.context.scene
scene["bottom_panel_geometry"] = "rectangular panel plus two photographed corner legs"
bpy.ops.object.select_all(action="DESELECT")
bottom.select_set(True)
bpy.context.view_layer.objects.active = bottom

OUT.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))

report = {
    "experiment": "FFDY-8454",
    "file": str(OUT),
    "pass": all(checks.values()),
    "checks": checks,
    "leg_width_proxy_m": leg_width,
    "leg_extension_proxy_m": leg_extension,
    "evidence": [
        "/home/colligo/THD_laundry_sink_storyboard/images/image8.jpeg",
        "/home/colligo/THD_laundry_sink_storyboard/images/image11.jpeg"
    ],
    "confidence": "high that two corner extensions exist; approximate dimensions",
}
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
if not report["pass"]:
    raise SystemExit(1)
