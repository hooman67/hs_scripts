"""Create a non-destructive v5 of Hooman's authored laundry-sink motion.

The source file must already be open in Blender. This script:

* bakes the final assembled scale corrections into mesh geometry, so each part is
  rigid and has its corrected dimensions from the first frame;
* moves late post-install fit nudges to the actual installation endpoints; and
* removes the 180-degree X flip from the large narrow board, treating its two
  broad faces as motion-equivalent and compensating Z to preserve its assembled
  occupancy.

It intentionally preserves the separately-authored front-frame rotation during
the whole-cabinet stand-up. That rotation may encode which door face is outward
and is not the same correction as the large-board pre-stand-up flip.

The output is append-only: this script refuses to overwrite an existing file.
"""

from pathlib import Path
import json
import math

import bpy


ROOT = Path("/home/colligo/hs_scripts/claude/3d_research/FFDY-8454")
SOURCE = ROOT / "blender" / "laundry_sink_components_v4_image7_corrected_hooman_added_motion.blend"
OUTPUT = ROOT / "blender" / "laundry_sink_components_v5_corrected_geometry_simplified_motion.blend"
REPORT = ROOT / "validation" / "rig_validation_v5_corrected_geometry.json"

FINAL_ASSEMBLED_FRAME = 324
TOP_WALL_INSTALLED_FRAME = 192
LARGE_BOARD_PICKUP_FRAME = 240
LARGE_BOARD_INSTALLED_FRAME = 264

CORRECTED_SCALES = {
    "CABINET_04_TOP_WALL": (0.92, 1.08, 1.0),
    "CABINET_05_RIGHT_BOARD_LARGE": (1.0, 1.18, 1.0),
    "CABINET_06_RIGHT_BOARD_SMALL": (1.0, 1.25, 1.0),
}


def action_fcurves(obj):
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


def curve(obj, data_path, array_index):
    for fcurve in action_fcurves(obj):
        if fcurve.data_path == data_path and fcurve.array_index == array_index:
            return fcurve
    raise RuntimeError(f"Missing {obj.name} {data_path}[{array_index}]")


def set_point_values(fcurve, value, min_frame=None):
    changed = []
    for point in fcurve.keyframe_points:
        if min_frame is None or point.co.x >= min_frame:
            point.co.y = value
            changed.append(int(round(point.co.x)))
    fcurve.update()
    return changed


def set_frame_and_later(obj, data_path, index, frame, value):
    fcurve = curve(obj, data_path, index)
    changed = False
    for point in fcurve.keyframe_points:
        if point.co.x >= frame:
            point.co.y = value
            changed = True
    if not changed:
        raise RuntimeError(f"No key at/after frame {frame} for {obj.name}")
    fcurve.update()


def evaluated_transform(obj, frame):
    bpy.context.scene.frame_set(frame)
    return {
        "location": tuple(float(value) for value in obj.location),
        "rotation": tuple(float(value) for value in obj.rotation_euler),
        "scale": tuple(float(value) for value in obj.scale),
    }


def bake_scale_into_mesh(obj, scale):
    if obj.data.users != 1:
        obj.data = obj.data.copy()
    for vertex in obj.data.vertices:
        vertex.co.x *= scale[0]
        vertex.co.y *= scale[1]
        vertex.co.z *= scale[2]
    obj.data.update()
    for index in range(3):
        set_point_values(curve(obj, "scale", index), 1.0)
    obj.scale = (1.0, 1.0, 1.0)
    obj.lock_scale = (True, True, True)


def main():
    if Path(bpy.data.filepath).resolve() != SOURCE.resolve():
        raise RuntimeError(f"Open the expected source first: {SOURCE}")
    if OUTPUT.exists():
        raise RuntimeError(f"Refusing to overwrite existing result: {OUTPUT}")

    scene = bpy.context.scene
    scene.frame_set(FINAL_ASSEMBLED_FRAME)
    final_states = {
        name: evaluated_transform(bpy.data.objects[name], FINAL_ASSEMBLED_FRAME)
        for name in CORRECTED_SCALES
    }

    # Apply corrected dimensions at mesh level, then eliminate all animated scale.
    for name, scale in CORRECTED_SCALES.items():
        bake_scale_into_mesh(bpy.data.objects[name], scale)

    # The end wall was already installed at frame 192. Move its later fit nudge
    # back to that endpoint so it does not drift while another part is handled.
    top_wall = bpy.data.objects["CABINET_04_TOP_WALL"]
    top_final = final_states[top_wall.name]["location"]
    for index, value in enumerate(top_final):
        set_frame_and_later(
            top_wall, "location", index, TOP_WALL_INSTALLED_FRAME, value
        )

    # The larger narrow board is front/back motion-equivalent. The old 180° X
    # roll only changed which broad face was up. Remove that roll. Because this
    # object's origin lies on a face, lower its post-pickup Z by its local depth
    # to keep the installed world-space slab in the same vertical interval.
    large = bpy.data.objects["CABINET_05_RIGHT_BOARD_LARGE"]
    set_point_values(curve(large, "rotation_euler", 0), 0.0)
    local_max_z = max(vertex.co.z for vertex in large.data.vertices)
    old_pickup = evaluated_transform(large, LARGE_BOARD_PICKUP_FRAME)["location"]
    large_final = final_states[large.name]["location"]

    # Retain the authored pickup waypoint, with only the no-flip Z compensation.
    pickup_target = (old_pickup[0], old_pickup[1], old_pickup[2] - local_max_z)
    for index, value in enumerate(pickup_target):
        fcurve = curve(large, "location", index)
        for point in fcurve.keyframe_points:
            if int(round(point.co.x)) == LARGE_BOARD_PICKUP_FRAME:
                point.co.y = value
        fcurve.update()

    installed_target = (
        large_final[0],
        large_final[1],
        large_final[2] - local_max_z,
    )
    for index, value in enumerate(installed_target):
        set_frame_and_later(
            large, "location", index, LARGE_BOARD_INSTALLED_FRAME, value
        )

    scene["experiment"] = "FFDY-8454"
    scene["version"] = "v5 corrected geometry and simplified motion"
    scene["source_file"] = str(SOURCE)
    scene["authoritative_assembled_frame"] = FINAL_ASSEMBLED_FRAME
    scene["geometry_corrections"] = json.dumps(CORRECTED_SCALES)
    scene["motion_simplifications"] = (
        "top-wall fit correction ends at f192; large-board fit correction ends "
        "at f264; large-board 180-degree X flip removed"
    )
    scene["preserved_uncertainty"] = (
        "front-frame relative 180-degree rotation during f324-f348 stand-up was "
        "preserved because it may encode the outward door face"
    )

    scene.frame_set(1)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT))

    report = {
        "source": str(SOURCE),
        "output": str(OUTPUT),
        "authoritative_assembled_frame": FINAL_ASSEMBLED_FRAME,
        "baked_scale_corrections": {
            name: list(values) for name, values in CORRECTED_SCALES.items()
        },
        "top_wall_corrected_install_endpoint": TOP_WALL_INSTALLED_FRAME,
        "large_board_corrected_install_endpoint": LARGE_BOARD_INSTALLED_FRAME,
        "large_board_removed_rotation_degrees": 180,
        "large_board_z_compensation": float(local_max_z),
        "front_frame_standup_rotation_preserved": True,
        "confidence": {
            "dimension_corrections": "VERIFIED from final pre-stand-up authored state at frame 324",
            "late_nudges_as_fit_corrections": "ASSUMED from timing after each part was already installed",
            "large_board_front_back_equivalence": "USER-CONFIRMED",
            "front_frame_rotation_semantics": "UNRESOLVED; preserved conservatively",
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
