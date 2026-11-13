#!/usr/bin/env python3
"""Build the six cabinet components using only storyboard_all_pieces_image7.jpeg.

This supersedes the incorrect v3 part mapping. The two legs belong to the central
front-frame/door assembly, not to the upper-left top-wall panel.
"""

from pathlib import Path
import json

import bpy
from mathutils import Vector


ROOT = Path("/home/colligo/hs_scripts/claude/3d_research/FFDY-8454")
OUT = ROOT / "blender" / "laundry_sink_components_v4_image7_corrected.blend"
REPORT = ROOT / "validation" / "rig_validation_v4_image7_corrected.json"


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for blocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials,
                   bpy.data.cameras, bpy.data.lights):
        for block in list(blocks):
            if block.users == 0:
                blocks.remove(block)


def new_collection(name):
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col


def material(name, rgba):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = rgba
    return mat


def relink(obj, col):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    col.objects.link(obj)


def box(name, dims, loc, mat, col, bevel=0.008):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    obj.color = mat.diffuse_color
    if bevel:
        mod = obj.modifiers.new("Soft_Edges", "BEVEL")
        mod.width = bevel
        mod.segments = 2
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
    relink(obj, col)
    return obj


def join_component(name, objects, col):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    if len(objects) > 1:
        bpy.ops.object.join()
    result = objects[0]
    result.name = name
    relink(result, col)
    result.animation_data_clear()
    result.scale = (1, 1, 1)
    result.lock_scale = (True, True, True)
    result.lock_location = (False, False, False)
    result.lock_rotation = (False, False, False)
    return result


def set_origin_world(obj, point):
    scene.cursor.location = point
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR", center="MEDIAN")


def bounds_world(obj):
    pts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    return {
        "min_x": min(p.x for p in pts), "max_x": max(p.x for p in pts),
        "min_y": min(p.y for p in pts), "max_y": max(p.y for p in pts),
        "min_z": min(p.z for p in pts), "max_z": max(p.z for p in pts),
    }


def camera(name, loc, target, lens, col):
    data = bpy.data.cameras.new(name + "_Data")
    data.lens = lens
    obj = bpy.data.objects.new(name, data)
    obj.location = loc
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()
    col.objects.link(obj)
    return obj


clear_scene()
scene = bpy.context.scene
scene.name = "FFDY_8454_Image7_Corrected_Components"
scene.render.engine = "BLENDER_WORKBENCH"
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.display.shading.light = "STUDIO"
scene.display.shading.studio_light = "paint.sl"
scene.display.shading.color_type = "MATERIAL"
scene.display.shading.show_shadows = True
scene.display.shading.show_cavity = True
scene.display.shading.cavity_type = "BOTH"
scene.display.shading.background_type = "VIEWPORT"
scene.display.shading.background_color = (0.045, 0.055, 0.075)
scene.frame_start = 1
scene.frame_end = 240
scene.render.fps = 24

components_col = new_collection("CABINET_COMPONENTS_DIRECT")
environment_col = new_collection("ENVIRONMENT_OPTIONAL")
camera_col = new_collection("CAMERAS_OPTIONAL")
build_col = new_collection("TEMP_BUILD")

white = material("Cabinet_White", (0.90, 0.91, 0.92, 1))
white_face = material("Door_Face_White", (0.84, 0.86, 0.88, 1))
orange = material("Orange_Connector_Areas", (1.0, 0.24, 0.025, 1))
metal = material("Hinge_Metal", (0.34, 0.37, 0.40, 1))
floor_mat = material("Dark_Assembly_Mat", (0.11, 0.15, 0.21, 1))

box("Assembly_Mat", (3.25, 2.75, 0.025), (0, 0, -0.025),
    floor_mat, environment_col, bevel=0.02)

# Approximate dimensions inferred only from relative proportions in image 7.
frame_w = 1.20
frame_h = 0.82
t = 0.035
leg_extension = 0.12
leg_height = 0.10

# 01 — central front frame: two doors, four hinges, small rectangle, two legs.
front_pieces = [
    box("Front_Frame_Base", (frame_w, frame_h, t), (0, 0, t / 2), white, build_col),
]

# Small tall rectangle at the left of the photographed layout.
small_w = 0.18
margin = 0.055
front_pieces.append(box(
    "Front_Frame_Small_Rectangle", (small_w, frame_h - 2 * margin, 0.012),
    (-frame_w / 2 + margin + small_w / 2, 0, t + 0.006), white_face, build_col,
    bevel=0.004,
))

# Two door faces stacked vertically in the photographed orientation.
door_left = -frame_w / 2 + margin + small_w + 0.035
door_right = frame_w / 2 - margin
door_w = door_right - door_left
door_gap = 0.018
door_h = (frame_h - 2 * margin - door_gap) / 2
door_x = (door_left + door_right) / 2
for index, y in enumerate((door_h / 2 + door_gap / 2,
                           -door_h / 2 - door_gap / 2), 1):
    front_pieces.append(box(
        f"Door_Face_{index}", (door_w, door_h, 0.012),
        (door_x, y, t + 0.006), white_face, build_col, bevel=0.005,
    ))

# Four visible hinge groups, matching their arrangement around the two doors.
for row, y in (("TOP", frame_h / 2 - 0.055),
               ("BOTTOM", -frame_h / 2 + 0.055)):
    for column, x in (("LEFT", door_left + door_w * 0.28),
                      ("RIGHT", door_left + door_w * 0.78)):
        front_pieces.append(box(
            f"Hinge_{row}_{column}", (0.075, 0.045, 0.025),
            (x, y, t + 0.020), metal, build_col, bevel=0.006,
        ))

# Correct two legs: both protrude from the right edge of the central assembly.
for side, y in (("TOP", frame_h / 2 - leg_height / 2),
                ("BOTTOM", -frame_h / 2 + leg_height / 2)):
    front_pieces.append(box(
        f"Front_Frame_Leg_{side}", (leg_extension, leg_height, t),
        (frame_w / 2 + leg_extension / 2, y, t / 2), white, build_col,
        bevel=0.006,
    ))

# Orange areas along the top and bottom edges, plus one at the right side.
for edge_y in (-frame_h / 2, frame_h / 2):
    for x in (-0.42, 0.0, 0.42):
        front_pieces.append(box(
            f"Front_Orange_{edge_y:+.2f}_{x:+.2f}", (0.065, 0.018, 0.012),
            (x, edge_y, t + 0.008), orange, build_col, bevel=0.003,
        ))
front_pieces.append(box(
    "Front_Orange_Right", (0.018, 0.065, 0.012),
    (frame_w / 2, 0, t + 0.008), orange, build_col, bevel=0.003,
))
front = join_component("CABINET_01_FRONT_FRAME_DOORS_WITH_TWO_LEGS",
                       front_pieces, components_col)


def panel_component(name, dims, loc, connector_edges):
    pieces = [box(name + "_Body", dims, (loc[0], loc[1], t / 2), white, build_col)]
    for n, (dx, dy) in enumerate(connector_edges, 1):
        pieces.append(box(
            f"{name}_Orange_{n}", (0.065, 0.018, 0.012),
            (loc[0] + dx, loc[1] + dy, t + 0.008), orange, build_col,
            bevel=0.003,
        ))
    return join_component(name, pieces, components_col)


# 02/03 — the two broad side panels immediately above and below the center.
side_w = 1.12
side_h = 0.45
top_side_y = frame_h / 2 + 0.08 + side_h / 2
bottom_side_y = -frame_h / 2 - 0.08 - side_h / 2
top_side = panel_component(
    "CABINET_02_SIDE_PANEL_TOP", (side_w, side_h, t), (0, top_side_y, 0),
    [(-0.42, side_h / 2), (-0.34, side_h / 2),
     (0.40, -side_h / 2), (0.48, -side_h / 2)],
)
bottom_side = panel_component(
    "CABINET_03_SIDE_PANEL_BOTTOM", (side_w, side_h, t), (0, bottom_side_y, 0),
    [(-0.42, side_h / 2), (-0.34, side_h / 2),
     (0.40, -side_h / 2), (0.48, -side_h / 2)],
)

# 04 — upper-left top wall, plain rectangular panel with edge connector marks.
top_wall_w = 0.52
top_wall_h = 0.76
top_wall_loc = (-0.95, 0.25, 0)
top_wall = panel_component(
    "CABINET_04_TOP_WALL", (top_wall_w, top_wall_h, t), top_wall_loc,
    [(-top_wall_w / 2, 0.24), (-top_wall_w / 2, -0.24),
     (top_wall_w / 2, 0.0)],
)

# 05/06 — unequal boards immediately to the right of the center assembly.
large_board_w, large_board_h = 0.18, 0.70
small_board_w, small_board_h = 0.075, 0.65
large_loc = (0.84, 0.02, 0)
small_loc = (1.04, 0.02, 0)
large_board = panel_component(
    "CABINET_05_RIGHT_BOARD_LARGE",
    (large_board_w, large_board_h, t), large_loc,
    [(0, large_board_h / 2), (0.04, -large_board_h / 2)],
)
small_board = panel_component(
    "CABINET_06_RIGHT_BOARD_SMALL",
    (small_board_w, small_board_h, t), small_loc,
    [],
)

components = [front, top_side, bottom_side, top_wall, large_board, small_board]

# Native edge pivots only; no control objects. All scale axes are locked.
component_bounds = {obj.name: bounds_world(obj) for obj in components}
origins = {
    front.name: (component_bounds[front.name]["max_x"], 0,
                 component_bounds[front.name]["min_z"]),
    top_side.name: (0, component_bounds[top_side.name]["min_y"],
                    component_bounds[top_side.name]["min_z"]),
    bottom_side.name: (0, component_bounds[bottom_side.name]["max_y"],
                       component_bounds[bottom_side.name]["min_z"]),
    top_wall.name: (component_bounds[top_wall.name]["max_x"], top_wall_loc[1],
                    component_bounds[top_wall.name]["min_z"]),
    large_board.name: (component_bounds[large_board.name]["min_x"], large_loc[1],
                       component_bounds[large_board.name]["min_z"]),
    small_board.name: (component_bounds[small_board.name]["min_x"], small_loc[1],
                       component_bounds[small_board.name]["min_z"]),
}
for obj in components:
    set_origin_world(obj, origins[obj.name])
    obj.scale = (1, 1, 1)
    obj.lock_scale = (True, True, True)

scene.cursor.location = (0, 0, 0)
cam = camera("CAM_Image7_Layout", (2.45, -2.90, 3.10), (0, 0, 0), 55, camera_col)
scene.camera = cam

# Remove the now-empty temporary collection.
bpy.data.collections.remove(build_col)

scene["experiment"] = "FFDY-8454"
scene["version"] = "v4 image7-only corrected components"
scene["sole_geometry_reference"] = str(
    ROOT / "references" / "storyboard_all_pieces_image7.jpeg"
)
scene["component_count"] = 6
scene["controls"] = "none; native Blender mesh objects with edge origins"
scene["geometry_notice"] = "photo-derived relative proportions, not CAD"

bpy.ops.object.select_all(action="DESELECT")
front.select_set(True)
bpy.context.view_layer.objects.active = front

OUT.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))

# Validate the corrected topology and stripped interaction model.
front_bounds = bounds_world(front)
front_world_vertices = [front.matrix_world @ v.co for v in front.data.vertices]
right_leg_top = [v for v in front_world_vertices
                 if v.x > frame_w / 2 + 0.02 and v.y > frame_h / 2 - leg_height - 0.02]
right_leg_bottom = [v for v in front_world_vertices
                    if v.x > frame_w / 2 + 0.02 and v.y < -frame_h / 2 + leg_height + 0.02]

checks = {
    "exactly_six_direct_mesh_components": len(list(components_col.objects)) == 6,
    "no_control_empties": not any(o.type == "EMPTY" for o in bpy.data.objects),
    "front_frame_has_top_leg": len(right_leg_top) > 0,
    "front_frame_has_bottom_leg": len(right_leg_bottom) > 0,
    "front_legs_extend_beyond_frame": front_bounds["max_x"] > frame_w / 2 + 0.05,
    "top_wall_has_only_small_connector_protrusions": (
        component_bounds[top_wall.name]["max_x"] - component_bounds[top_wall.name]["min_x"]
        <= top_wall_w + 0.08
    ),
    "six_scales_locked_at_one": all(tuple(o.scale) == (1.0, 1.0, 1.0)
                                     and all(o.lock_scale) for o in components),
    "no_animation_or_constraints": all(o.animation_data is None and not o.constraints
                                        for o in components),
}
report = {
    "experiment": "FFDY-8454",
    "file": str(OUT),
    "pass": all(checks.values()),
    "checks": checks,
    "components": [o.name for o in components],
    "sole_reference": str(ROOT / "references" / "storyboard_all_pieces_image7.jpeg"),
    "confidence": "part identity/layout high from user correction; dimensions approximate",
}
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
if not report["pass"]:
    raise SystemExit(1)
