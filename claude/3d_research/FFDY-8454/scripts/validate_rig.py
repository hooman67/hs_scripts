#!/usr/bin/env python3
"""Validate the FFDY-8454 motion constraints and write machine-readable evidence."""

from pathlib import Path
import json
import math

import bpy


ROOT = Path("/home/colligo/hs_scripts/claude/3d_research/FFDY-8454")
OUT = ROOT / "validation" / "rig_validation_v1.json"

scene = bpy.context.scene
master = bpy.data.objects["CTRL_Master_Select_Me"]
left_pivot = bpy.data.objects["CTRL_LeftSide_FIXED_LOWER_PIVOT"]
right_pivot = bpy.data.objects["CTRL_RightSide_FIXED_LOWER_PIVOT"]
end_ctrl = bpy.data.objects["CTRL_Shot05_EndPanel_Vertical"]
bottom_ctrl = bpy.data.objects["CTRL_Shot06_BottomPiece_Slide"]
rail_ctrl = bpy.data.objects["CTRL_Shot07_LockRail_Vertical"]


def xyz(vec):
    return [round(float(v), 6) for v in vec]


def state(frame):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    return {
        "frame": frame,
        "properties": {
            key: round(float(master[key]), 6)
            for key in (
                "left_side_lift", "right_side_lift", "end_panel_insert",
                "side_top_spread", "bottom_piece_insert", "lock_rail_drop"
            )
        },
        "left_lower_pivot_world": xyz(left_pivot.matrix_world.translation),
        "right_lower_pivot_world": xyz(right_pivot.matrix_world.translation),
        "left_side_rotation_y_degrees": round(
            math.degrees(float(left_pivot.rotation_euler.y)), 6),
        "right_side_rotation_y_degrees": round(
            math.degrees(float(right_pivot.rotation_euler.y)), 6),
        "end_panel_control_world": xyz(end_ctrl.matrix_world.translation),
        "bottom_piece_control_world": xyz(bottom_ctrl.matrix_world.translation),
        "lock_rail_control_world": xyz(rail_ctrl.matrix_world.translation),
    }


frames = [1, 60, 90, 108, 132, 156, 180, 198, 224, 248]
states = {str(frame): state(frame) for frame in frames}


def delta(a, b, field, axis):
    return round(states[str(b)][field][axis] - states[str(a)][field][axis], 6)


left_positions = {tuple(states[str(f)]["left_lower_pivot_world"]) for f in frames}
right_positions = {tuple(states[str(f)]["right_lower_pivot_world"]) for f in frames}

checks = {
    "required_objects_exist": all(name in bpy.data.objects for name in (
        "Panel_Long_Left", "Panel_Long_Right", "Panel_Perpendicular_End_SHOT05",
        "Bottom_Piece_SHOT06", "Top_Locking_Piece_SHOT07",
        "CTRL_Master_Select_Me", "CTRL_Hand_Left", "CTRL_Hand_Right"
    )),
    "shot05_end_panel_moves_down_0_42m": abs(delta(1, 60, "end_panel_control_world", 2) + 0.42) < 1e-5,
    "shot05_side_lower_pivots_fixed": len(left_positions) == 1 and len(right_positions) == 1,
    "shot06_bottom_piece_moves_in_0_62m": abs(delta(90, 132, "bottom_piece_control_world", 1) - 0.62) < 1e-5,
    "shot06_spread_is_small": abs(states["108"]["left_side_rotation_y_degrees"]) <= 4.0,
    "shot06_sides_close_again": (
        abs(states["156"]["left_side_rotation_y_degrees"]) < 1e-5
        and abs(states["156"]["right_side_rotation_y_degrees"]) < 1e-5
    ),
    "shot07_max_spread_is_6deg_each": (
        abs(abs(states["198"]["left_side_rotation_y_degrees"]) - 6.0) < 1e-4
        and abs(abs(states["198"]["right_side_rotation_y_degrees"]) - 6.0) < 1e-4
    ),
    "shot07_lock_piece_moves_down_0_30m": abs(delta(180, 224, "lock_rail_control_world", 2) + 0.30) < 1e-5,
    "shot07_sides_close_after_drop": (
        abs(states["248"]["left_side_rotation_y_degrees"]) < 1e-5
        and abs(states["248"]["right_side_rotation_y_degrees"]) < 1e-5
    ),
}

report = {
    "experiment": "FFDY-8454",
    "rig": str(ROOT / "blender" / "laundry_sink_motion_rig_v1.blend"),
    "blender_version": bpy.app.version_string,
    "pass": all(checks.values()),
    "checks": checks,
    "sampled_states": states,
    "interpretation": {
        "geometry": "Approximate storyboard-derived proxy, not CAD",
        "motion_constraints": "Encoded from FFDY-7304 shot JSON and annotations",
        "hands": "Independent editable guides; no IK in v1",
    },
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"pass": report["pass"], "checks": checks}, indent=2))
if not report["pass"]:
    raise SystemExit(1)

