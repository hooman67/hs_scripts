#!/usr/bin/env python3
"""Strip the loaded v2 blank rig down to six directly editable mesh components."""

from pathlib import Path
import json

import bpy


ROOT = Path("/home/colligo/hs_scripts/claude/3d_research/FFDY-8454")
OUT = ROOT / "blender" / "laundry_sink_components_only_v3.blend"
REPORT = ROOT / "validation" / "rig_validation_v3_components_only.json"

scene = bpy.context.scene
scene.frame_set(1)
bpy.context.view_layer.update()

component_ids = [
    "01_FRONT_FRAME_DOORS",
    "02_LEFT_SIDE",
    "03_RIGHT_SIDE",
    "04_BOTTOM_PANEL",
    "05_WIDE_RAIL",
    "06_NARROW_RAIL",
]


def descendants(root):
    result = []
    stack = list(root.children)
    while stack:
        obj = stack.pop()
        result.append(obj)
        stack.extend(list(obj.children))
    return result


def apply_modifiers(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    for modifier in list(obj.modifiers):
        try:
            bpy.ops.object.modifier_apply(modifier=modifier.name)
        except RuntimeError:
            pass


joined_components = []
for component_id in component_ids:
    main = bpy.data.objects[f"PART_{component_id}"]
    auto = bpy.data.objects[f"INTERNAL_AUTO_ROTATION_{component_id}"]
    geometry = [o for o in [auto] + descendants(auto) if o.type == "MESH"]

    # Preserve evaluated layout transforms, then detach geometry from the rig.
    for obj in geometry:
        apply_modifiers(obj)
        world = obj.matrix_world.copy()
        obj.parent = None
        obj.matrix_world = world
        obj.animation_data_clear()
        for constraint in list(obj.constraints):
            obj.constraints.remove(constraint)

    # Join details such as doors, hinges, and orange connectors into their component.
    bpy.ops.object.select_all(action="DESELECT")
    for obj in geometry:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = main
    if len(geometry) > 1:
        bpy.ops.object.join()
    main.name = f"CABINET_{component_id}"
    main.animation_data_clear()
    main.lock_location = (False, False, False)
    main.lock_rotation = (False, False, False)
    main.lock_scale = (False, False, False)
    for key in list(main.keys()):
        del main[key]
    joined_components.append(main)

# Keep only the six components, an optional floor, and the overview camera.
keep = set(joined_components)
floor = bpy.data.objects.get("Assembly_Mat")
camera = bpy.data.objects.get("CAM_Assembly_Overview")
if floor:
    keep.add(floor)
if camera:
    keep.add(camera)

for obj in list(bpy.data.objects):
    if obj not in keep:
        bpy.data.objects.remove(obj, do_unlink=True)

# Replace the rig collections with a small, explicit scene organization.
for col in list(bpy.data.collections):
    bpy.data.collections.remove(col)

component_col = bpy.data.collections.new("CABINET_COMPONENTS_DIRECT")
scene.collection.children.link(component_col)
for obj in joined_components:
    component_col.objects.link(obj)

if floor:
    environment_col = bpy.data.collections.new("ENVIRONMENT_OPTIONAL")
    scene.collection.children.link(environment_col)
    environment_col.objects.link(floor)
if camera:
    camera_col = bpy.data.collections.new("CAMERAS_OPTIONAL")
    scene.collection.children.link(camera_col)
    camera_col.objects.link(camera)
    scene.camera = camera

scene.frame_start = 1
scene.frame_end = 240
scene.frame_set(1)
scene["experiment"] = "FFDY-8454"
scene["version"] = "v3 components only"
scene["scope"] = "six directly editable cabinet mesh objects"
scene["controls"] = "none beyond native Blender transforms and keyframes"

# Select all six components when the file opens.
bpy.ops.object.select_all(action="DESELECT")
for obj in joined_components:
    obj.select_set(True)
bpy.context.view_layer.objects.active = joined_components[0]

OUT.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))

component_meshes = list(component_col.objects)
checks = {
    "exactly_six_component_meshes": len(component_meshes) == 6,
    "no_empties": not any(o.type == "EMPTY" for o in bpy.data.objects),
    "no_component_animation": all(o.animation_data is None for o in component_meshes),
    "no_component_constraints": all(len(o.constraints) == 0 for o in component_meshes),
    "no_locked_transforms": all(
        not any(o.lock_location) and not any(o.lock_rotation) and not any(o.lock_scale)
        for o in component_meshes
    ),
    "no_custom_component_controls": all(len(o.keys()) == 0 for o in component_meshes),
}
report = {
    "experiment": "FFDY-8454",
    "file": str(OUT),
    "pass": all(checks.values()),
    "checks": checks,
    "components": sorted(o.name for o in component_meshes),
}
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
if not report["pass"]:
    raise SystemExit(1)

