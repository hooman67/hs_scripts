#!/usr/bin/env python3
"""Validate six-piece independence, endpoints, and direct-control behavior in rig v2."""

from pathlib import Path
import json
import math

import bpy
from mathutils import Vector


ROOT = Path("/home/colligo/hs_scripts/claude/3d_research/FFDY-8454")
OUT = ROOT / "validation" / "rig_validation_v2.json"

scene = bpy.context.scene
part_roots = sorted(
    [o for o in bpy.data.objects if o.name.startswith("PART_")],
    key=lambda o: o.name,
)
channels = sorted(
    [o for o in bpy.data.objects if o.name.startswith("PROGRESS_")],
    key=lambda o: o.name,
)
directs = sorted(
    [o for o in bpy.data.objects if o.name.startswith("MOVE_ROTATE_")],
    key=lambda o: o.name,
)


def world_loc(obj):
    bpy.context.view_layer.update()
    return Vector(obj.matrix_world.translation)


scene.frame_set(1)
layout_locations = {o.name: list(world_loc(o)) for o in part_roots}
layout_z = [world_loc(o).z for o in part_roots]

scene.frame_set(360)
installed_locations = {o.name: list(world_loc(o)) for o in part_roots}

channel_actions_ok = all(
    c.animation_data is not None and c.animation_data.action is not None for c in channels
)
direct_actions_ok = all(
    c.animation_data is not None and c.animation_data.action is not None for c in directs
)

# Independence check: temporarily detach one channel's example Action so its frame-1
# key does not overwrite the value used by this manual dependency probe.
scene.frame_set(1)
probe_channel = channels[3]
probe_channel.animation_data_clear()
probe_channel["install_progress"] = 0.0
probe_channel.update_tag(refresh={"OBJECT"})
scene.frame_set(2)
scene.frame_set(1)
bpy.context.view_layer.update()
before = {o.name: world_loc(o).copy() for o in part_roots}
probe_channel["install_progress"] = 1.0
probe_channel.update_tag(refresh={"OBJECT"})
scene.frame_set(2)
scene.frame_set(1)
bpy.context.view_layer.update()
after = {o.name: world_loc(o).copy() for o in part_roots}
moved = [name for name in before if (after[name] - before[name]).length > 1e-5]
probe_channel["install_progress"] = 0.0

# Direct handle must add motion without altering another component.
target_direct = directs[2]
scene.frame_set(1)
target_name = target_direct.name.replace("MOVE_ROTATE_", "PART_")
target_part = bpy.data.objects[target_name]
target_before = world_loc(target_part).copy()
other_before = {o.name: world_loc(o).copy() for o in part_roots if o != target_part}
target_direct.location.z += 0.125
bpy.context.view_layer.update()
target_after = world_loc(target_part).copy()
other_after = {o.name: world_loc(o).copy() for o in part_roots if o != target_part}
direct_delta = (target_after - target_before).length
others_still = all((other_after[n] - other_before[n]).length < 1e-5 for n in other_before)

checks = {
    "exactly_six_component_roots": len(part_roots) == 6,
    "six_independent_progress_channels": len(channels) == 6,
    "six_visible_direct_handles": len(directs) == 6 and all(o.show_in_front for o in directs),
    "every_channel_has_constrained_progress": all(
        "install_progress" in c and
        c.id_properties_ui("install_progress").as_dict().get("min") == 0.0 and
        c.id_properties_ui("install_progress").as_dict().get("max") == 1.0
        for c in channels
    ),
    "every_channel_has_own_action": channel_actions_ok,
    "every_direct_handle_has_own_action": direct_actions_ok,
    "all_parts_start_flat_or_thin_to_mat": max(layout_z) < 0.05,
    "one_progress_channel_moves_only_its_part": len(moved) == 1,
    "direct_handle_moves_target": abs(direct_delta - 0.125) < 1e-4,
    "direct_handle_does_not_move_other_parts": others_still,
    "installed_pose_differs_from_layout_for_five_or_more_parts": sum(
        (Vector(installed_locations[n]) - Vector(layout_locations[n])).length > 0.05
        for n in layout_locations
    ) >= 5,
}

report = {
    "experiment": "FFDY-8454",
    "rig": str(ROOT / "blender" / "laundry_sink_full_assembly_rig_v2.blend"),
    "blender_version": bpy.app.version_string,
    "pass": all(checks.values()),
    "checks": checks,
    "component_roots": [o.name for o in part_roots],
    "progress_channels": [o.name for o in channels],
    "direct_handles": [o.name for o in directs],
    "independence_probe_moved": moved,
    "layout_locations": layout_locations,
    "installed_locations": installed_locations,
    "scope": "cabinet only; exactly six storyboard-inferred components",
    "caveat": "component dimensions and exact joinery are not CAD-derived",
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"pass": report["pass"], "checks": checks}, indent=2))
if not report["pass"]:
    raise SystemExit(1)
