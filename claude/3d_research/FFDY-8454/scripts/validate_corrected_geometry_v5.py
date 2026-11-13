"""Validate the corrected, simplified v5 Blender file currently open."""

from pathlib import Path
import json

import bpy
from mathutils import Vector


ROOT = Path("/home/colligo/hs_scripts/claude/3d_research/FFDY-8454")
EXPECTED = ROOT / "blender" / "laundry_sink_components_v5_corrected_geometry_simplified_motion.blend"
SOURCE_STATES = ROOT / "validation" / "hooman_motion_source_animation.json"
REPORT = ROOT / "validation" / "rig_validation_v5_corrected_geometry.json"
COMPONENTS = [
    "CABINET_01_FRONT_FRAME_DOORS_WITH_TWO_LEGS",
    "CABINET_02_SIDE_PANEL_TOP",
    "CABINET_03_SIDE_PANEL_BOTTOM",
    "CABINET_04_TOP_WALL",
    "CABINET_05_RIGHT_BOARD_LARGE",
    "CABINET_06_RIGHT_BOARD_SMALL",
]


def action_fcurves(obj):
    action = obj.animation_data.action if obj.animation_data else None
    if action is None:
        return []
    if hasattr(action, "fcurves"):
        return list(action.fcurves)
    slot = obj.animation_data.action_slot
    return [
        curve
        for layer in action.layers
        for strip in layer.strips
        for bag in strip.channelbags
        if slot is None or bag.slot == slot
        for curve in bag.fcurves
    ]


def bounds(obj, frame):
    bpy.context.scene.frame_set(frame)
    evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    points = [evaluated.matrix_world @ Vector(corner) for corner in evaluated.bound_box]
    return {
        "min": [min(point[i] for point in points) for i in range(3)],
        "max": [max(point[i] for point in points) for i in range(3)],
    }


def close_bounds(a, b, tolerance=2e-5):
    return all(
        abs(float(left) - float(right)) <= tolerance
        for key in ("min", "max")
        for left, right in zip(a[key], b[key])
    )


def curve_values(obj, path, index):
    for curve in action_fcurves(obj):
        if curve.data_path == path and curve.array_index == index:
            return [(round(point.co.x), float(point.co.y)) for point in curve.keyframe_points]
    return []


def local_state(obj, frame):
    bpy.context.scene.frame_set(frame)
    return {
        "location": tuple(round(float(value), 6) for value in obj.location),
        "rotation": tuple(round(float(value), 6) for value in obj.rotation_euler),
        "scale": tuple(round(float(value), 6) for value in obj.scale),
    }


def main():
    if Path(bpy.data.filepath).resolve() != EXPECTED.resolve():
        raise RuntimeError(f"Open expected v5 file first: {EXPECTED}")
    source = json.loads(SOURCE_STATES.read_text(encoding="utf-8"))
    objects = [bpy.data.objects[name] for name in COMPONENTS]

    scale_curves = [
        curve
        for obj in objects
        for curve in action_fcurves(obj)
        if curve.data_path == "scale"
    ]
    all_scale_keys_one = all(
        abs(point.co.y - 1.0) < 1e-7
        for curve in scale_curves
        for point in curve.keyframe_points
    )

    exact_final_bounds = {}
    for frame in (324, 348):
        exact_final_bounds[str(frame)] = {
            name: close_bounds(
                bounds(bpy.data.objects[name], frame),
                source["objects"][name]["states"][str(frame)]["world_bounds"],
            )
            for name in COMPONENTS
        }

    large = bpy.data.objects["CABINET_05_RIGHT_BOARD_LARGE"]
    top_wall = bpy.data.objects["CABINET_04_TOP_WALL"]
    large_x_rotation = curve_values(large, "rotation_euler", 0)
    checks = {
        "new_file_is_distinct_from_source": str(EXPECTED) != source["source"],
        "exactly_six_named_components_present": len(objects) == 6,
        "all_object_scale_key_values_are_one": all_scale_keys_one,
        "all_component_scales_locked": all(all(obj.lock_scale) for obj in objects),
        "large_board_has_no_x_rotation": all(
            abs(value) < 1e-7 for _, value in large_x_rotation
        ),
        "top_wall_is_stable_after_installation": all(
            local_state(top_wall, frame) == local_state(top_wall, 192)
            for frame in (216, 240, 264, 278, 300, 324)
        ),
        "large_board_is_stable_after_installation": all(
            local_state(large, frame) == local_state(large, 264)
            for frame in (278, 300, 324)
        ),
        "source_and_v5_match_all_component_bounds_at_frame_324": all(
            exact_final_bounds["324"].values()
        ),
        "source_and_v5_match_all_component_bounds_at_frame_348": all(
            exact_final_bounds["348"].values()
        ),
        "all_initial_parts_rest_on_or_above_mat": all(
            bounds(obj, 1)["min"][2] >= -1e-5 for obj in objects
        ),
    }
    report = {
        "file": str(EXPECTED),
        "pass": all(checks.values()),
        "checks": checks,
        "final_bound_matches_by_component": exact_final_bounds,
        "large_board_x_rotation_key_values": large_x_rotation,
        "tested_with": bpy.app.version_string,
        "evidence_as_of": "2026-09-23",
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if not report["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
