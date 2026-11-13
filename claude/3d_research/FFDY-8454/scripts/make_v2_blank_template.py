#!/usr/bin/env python3
"""Turn the loaded v2 example rig into a clean, six-piece authoring template."""

from pathlib import Path
import json

import bpy


ROOT = Path("/home/colligo/hs_scripts/claude/3d_research/FFDY-8454")
OUT = ROOT / "blender" / "laundry_sink_full_assembly_rig_v2_blank.blend"
REPORT = ROOT / "validation" / "rig_validation_v2_blank.json"

scene = bpy.context.scene
channels = [o for o in bpy.data.objects if o.name.startswith("PROGRESS_")]
directs = [o for o in bpy.data.objects if o.name.startswith("MOVE_ROTATE_")]

for channel in channels:
    channel.animation_data_clear()
    channel["install_progress"] = 0.0
for ctrl in directs:
    ctrl.animation_data_clear()
    ctrl.location = (0, 0, 0)
    ctrl.rotation_euler = (0, 0, 0)

for marker in list(scene.timeline_markers):
    scene.timeline_markers.remove(marker)

scene.frame_start = 1
scene.frame_end = 240
scene.frame_set(1)
bpy.context.view_layer.update()
scene["template"] = "blank user-authoring template"
scene["order_authority"] = "user"
scene["timing_authority"] = "user"

bpy.ops.object.select_all(action="DESELECT")
for ctrl in directs:
    ctrl.select_set(True)
bpy.context.view_layer.objects.active = sorted(directs, key=lambda o: o.name)[0]

bpy.ops.wm.save_as_mainfile(filepath=str(OUT))

checks = {
    "six_progress_channels": len(channels) == 6,
    "six_direct_handles": len(directs) == 6,
    "all_progress_zero": all(float(c["install_progress"]) == 0.0 for c in channels),
    "no_progress_actions": all(c.animation_data is None for c in channels),
    "no_direct_actions": all(c.animation_data is None for c in directs),
    "no_timeline_markers": len(scene.timeline_markers) == 0,
}
report = {
    "experiment": "FFDY-8454",
    "template": str(OUT),
    "pass": all(checks.values()),
    "checks": checks,
}
REPORT.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
if not report["pass"]:
    raise SystemExit(1)
