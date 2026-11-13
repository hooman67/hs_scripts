#!/usr/bin/env python3
"""Create a native-Blender, components-only copy with useful edge origins.

No control objects or drivers are added. Each component remains an ordinary mesh.
The only changes are its object origin and locked scale axes.
"""

from pathlib import Path
import json

import bpy
from mathutils import Vector


ROOT = Path("/home/colligo/hs_scripts/claude/3d_research/FFDY-8454")
source_has_legs = "with_legs" in Path(bpy.data.filepath).stem
if source_has_legs:
    OUT = ROOT / "blender" / "laundry_sink_components_only_v3_with_legs_rigid_edges.blend"
    REPORT = ROOT / "validation" / "rig_validation_v3_with_legs_rigid_edges.json"
else:
    OUT = ROOT / "blender" / "laundry_sink_components_only_v3_rigid_edges.blend"
    REPORT = ROOT / "validation" / "rig_validation_v3_rigid_edges.json"

scene = bpy.context.scene
components = {
    o.name: o for o in bpy.data.collections["CABINET_COMPONENTS_DIRECT"].objects
}


def world_bounds(obj):
    points = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    return {
        "min_x": min(p.x for p in points), "max_x": max(p.x for p in points),
        "min_y": min(p.y for p in points), "max_y": max(p.y for p in points),
        "min_z": min(p.z for p in points), "max_z": max(p.z for p in points),
    }


before = {name: world_bounds(obj) for name, obj in components.items()}

# Pivot descriptions use current flat-layout world coordinates. Each point lies at
# the center of a practical floor-contact edge.
bounds = before
pivots = {
    # Near long edge; R X 90 lifts the frame from the floor.
    "CABINET_01_FRONT_FRAME_DOORS": (
        (bounds["CABINET_01_FRONT_FRAME_DOORS"]["min_x"] +
         bounds["CABINET_01_FRONT_FRAME_DOORS"]["max_x"]) / 2,
        bounds["CABINET_01_FRONT_FRAME_DOORS"]["min_y"],
        bounds["CABINET_01_FRONT_FRAME_DOORS"]["min_z"],
    ),
    # Inner long edge; R Y 90 lifts the left side.
    "CABINET_02_LEFT_SIDE": (
        bounds["CABINET_02_LEFT_SIDE"]["max_x"],
        (bounds["CABINET_02_LEFT_SIDE"]["min_y"] +
         bounds["CABINET_02_LEFT_SIDE"]["max_y"]) / 2,
        bounds["CABINET_02_LEFT_SIDE"]["min_z"],
    ),
    # Inner long edge; R Y -90 lifts the right side.
    "CABINET_03_RIGHT_SIDE": (
        bounds["CABINET_03_RIGHT_SIDE"]["min_x"],
        (bounds["CABINET_03_RIGHT_SIDE"]["min_y"] +
         bounds["CABINET_03_RIGHT_SIDE"]["max_y"]) / 2,
        bounds["CABINET_03_RIGHT_SIDE"]["min_z"],
    ),
    # Near long edge; R X 90 lifts the bottom panel rigidly onto that edge.
    "CABINET_04_BOTTOM_PANEL": (
        (bounds["CABINET_04_BOTTOM_PANEL"]["min_x"] +
         bounds["CABINET_04_BOTTOM_PANEL"]["max_x"]) / 2,
        bounds["CABINET_04_BOTTOM_PANEL"]["min_y"],
        bounds["CABINET_04_BOTTOM_PANEL"]["min_z"],
    ),
    # Inner long edges for the two rails.
    "CABINET_05_WIDE_RAIL": (
        bounds["CABINET_05_WIDE_RAIL"]["min_x"],
        (bounds["CABINET_05_WIDE_RAIL"]["min_y"] +
         bounds["CABINET_05_WIDE_RAIL"]["max_y"]) / 2,
        bounds["CABINET_05_WIDE_RAIL"]["min_z"],
    ),
    "CABINET_06_NARROW_RAIL": (
        bounds["CABINET_06_NARROW_RAIL"]["min_x"],
        (bounds["CABINET_06_NARROW_RAIL"]["min_y"] +
         bounds["CABINET_06_NARROW_RAIL"]["max_y"]) / 2,
        bounds["CABINET_06_NARROW_RAIL"]["min_z"],
    ),
}

for name, obj in components.items():
    scene.cursor.location = pivots[name]
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR", center="MEDIAN")

    # Rigid authoring guardrails in Object Mode.
    obj.scale = (1.0, 1.0, 1.0)
    obj.lock_scale = (True, True, True)
    obj.animation_data_clear()
    for constraint in list(obj.constraints):
        obj.constraints.remove(constraint)

scene.cursor.location = (0, 0, 0)
scene.frame_set(1)
after = {name: world_bounds(obj) for name, obj in components.items()}


def max_bound_delta(a, b):
    return max(abs(a[key] - b[key]) for key in a)


checks = {
    "exactly_six_mesh_components": len(components) == 6,
    "no_control_empties": not any(o.type == "EMPTY" for o in bpy.data.objects),
    "world_geometry_unchanged_by_origin_move": all(
        max_bound_delta(before[name], after[name]) < 1e-6 for name in components
    ),
    "scale_is_one": all(tuple(round(v, 6) for v in o.scale) == (1.0, 1.0, 1.0)
                        for o in components.values()),
    "scale_is_locked": all(all(o.lock_scale) for o in components.values()),
    "no_animation_or_constraints": all(
        o.animation_data is None and len(o.constraints) == 0 for o in components.values()
    ),
}

scene["version"] = "v3 components only with native rigid edge origins"
scene["rigid_editing_rule"] = "Use Object Mode; Edit Mode changes mesh geometry"

bpy.ops.object.select_all(action="DESELECT")
bottom = components["CABINET_04_BOTTOM_PANEL"]
bottom.select_set(True)
bpy.context.view_layer.objects.active = bottom

OUT.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))

report = {
    "experiment": "FFDY-8454",
    "file": str(OUT),
    "pass": all(checks.values()),
    "checks": checks,
    "pivot_world_positions": {name: [round(v, 6) for v in pivot]
                              for name, pivot in pivots.items()},
    "bottom_panel_lift": "Object Mode: R, X, 90",
    "warning": "Edit Mode vertex/edge movement deforms geometry and is not rigid motion",
}
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
if not report["pass"]:
    raise SystemExit(1)
