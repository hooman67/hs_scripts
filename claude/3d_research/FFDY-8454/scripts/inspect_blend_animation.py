"""Export object animation, transforms, and evaluated bounds from an open Blender file.

Usage:
  blender SOURCE.blend --background --python inspect_blend_animation.py -- OUTPUT.json
"""

import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def rounded(values, digits=6):
    return [round(float(value), digits) for value in values]


def world_bounds(obj, depsgraph):
    evaluated = obj.evaluated_get(depsgraph)
    corners = [evaluated.matrix_world @ Vector(corner) for corner in evaluated.bound_box]
    mins = [min(corner[index] for corner in corners) for index in range(3)]
    maxs = [max(corner[index] for corner in corners) for index in range(3)]
    return {
        "min": rounded(mins),
        "max": rounded(maxs),
        "dimensions": rounded([maxs[index] - mins[index] for index in range(3)]),
    }


def action_fcurves(obj):
    """Return F-curves for both legacy and Blender 4.4+ layered Actions."""
    animation = obj.animation_data
    action = animation.action if animation else None
    if action is None:
        return []
    if hasattr(action, "fcurves"):
        return list(action.fcurves)
    slot = animation.action_slot
    curves = []
    for layer in action.layers:
        for strip in layer.strips:
            for channelbag in strip.channelbags:
                if slot is None or channelbag.slot == slot:
                    curves.extend(channelbag.fcurves)
    return curves


def keyframe_map(obj):
    action = obj.animation_data.action if obj.animation_data else None
    result = {}
    if action is None:
        return result
    for fcurve in action_fcurves(obj):
        label = f"{fcurve.data_path}[{fcurve.array_index}]"
        result[label] = [
            {
                "frame": round(float(point.co.x), 6),
                "value": round(float(point.co.y), 6),
                "interpolation": point.interpolation,
            }
            for point in fcurve.keyframe_points
        ]
    return result


def main():
    if "--" not in sys.argv:
        raise SystemExit("Expected output path after --")
    output = Path(sys.argv[sys.argv.index("--") + 1])
    scene = bpy.context.scene
    animated = [
        obj
        for obj in scene.objects
        if obj.animation_data and obj.animation_data.action
    ]
    frames = {int(scene.frame_start), int(scene.frame_end)}
    for obj in animated:
        for curve in action_fcurves(obj):
            frames.update(round(point.co.x) for point in curve.keyframe_points)
    frames = sorted(frames)

    report = {
        "source": bpy.data.filepath,
        "scene_frame_start": scene.frame_start,
        "scene_frame_end": scene.frame_end,
        "objects": {},
        "frames": frames,
    }
    for obj in sorted(scene.objects, key=lambda item: item.name):
        if obj.type not in {"MESH", "EMPTY"}:
            continue
        item = {
            "type": obj.type,
            "parent": obj.parent.name if obj.parent else None,
            "rotation_mode": obj.rotation_mode,
            "lock_scale": list(obj.lock_scale),
            "keyframes": keyframe_map(obj),
            "states": {},
        }
        for frame in frames:
            scene.frame_set(frame)
            state = {
                "location": rounded(obj.location),
                "rotation_euler_degrees": rounded(
                    [value * 180.0 / 3.141592653589793 for value in obj.rotation_euler]
                ),
                "scale": rounded(obj.scale),
                "matrix_world": [rounded(row) for row in obj.matrix_world],
            }
            if obj.type == "MESH":
                state["world_bounds"] = world_bounds(obj, bpy.context.evaluated_depsgraph_get())
            item["states"][str(frame)] = state
        report["objects"][obj.name] = item

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
