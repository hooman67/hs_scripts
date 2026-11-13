#!/usr/bin/env python3
"""Build the FFDY-8454 storyboard-derived laundry cabinet motion rig.

Run with Blender, not system Python:
  blender --background --python build_laundry_sink_rig.py

This is a motion-control proxy, not a dimensionally accurate product model.
"""

from pathlib import Path
import math

import bpy
from mathutils import Vector


ROOT = Path("/home/colligo/hs_scripts/claude/3d_research/FFDY-8454")
BLEND_PATH = ROOT / "blender" / "laundry_sink_motion_rig_v1.blend"

W = 1.20
D = 0.68
H = 0.78
T = 0.035
BASE_TOP = 0.06


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials,
                       bpy.data.cameras, bpy.data.lights):
        for block in list(datablocks):
            if block.users == 0:
                datablocks.remove(block)


def collection(name):
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col


def move_to_collection(obj, col):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    col.objects.link(obj)


def material(name, rgba):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = rgba
    return mat


def cube(name, dims, loc=(0, 0, 0), mat=None, col=None, parent=None,
         bevel=0.012):
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if parent:
        obj.parent = parent
        obj.location = loc
    else:
        obj.location = loc
    if mat:
        obj.data.materials.append(mat)
        obj.color = mat.diffuse_color
    if bevel:
        mod = obj.modifiers.new("Soft_Edges", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    if col:
        move_to_collection(obj, col)
    return obj


def cylinder(name, radius, depth, loc=(0, 0, 0), mat=None, col=None,
             parent=None, rotation=(0, 0, 0), vertices=24):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius,
                                       depth=depth, location=(0, 0, 0),
                                       rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    if parent:
        obj.parent = parent
        obj.location = loc
    else:
        obj.location = loc
    if mat:
        obj.data.materials.append(mat)
        obj.color = mat.diffuse_color
    if col:
        move_to_collection(obj, col)
    return obj


def empty(name, loc=(0, 0, 0), col=None, display="ARROWS", size=0.13):
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_type = display
    obj.empty_display_size = size
    obj.location = loc
    (col or bpy.context.scene.collection).objects.link(obj)
    return obj


def text_label(name, body, loc, size, mat, col, rotation=(0, 0, 0)):
    curve = bpy.data.curves.new(name + "_Curve", "FONT")
    curve.body = body
    curve.align_x = "CENTER"
    curve.size = size
    curve.extrude = 0.002
    obj = bpy.data.objects.new(name, curve)
    obj.location = loc
    obj.rotation_euler = rotation
    curve.materials.append(mat)
    col.objects.link(obj)
    return obj


def add_prop(obj, name, default, description):
    obj[name] = default
    obj.id_properties_ui(name).update(
        min=0.0, max=1.0, soft_min=0.0, soft_max=1.0,
        description=description,
    )


def add_driver(obj, data_path, index, expression, variables):
    fcurve = obj.driver_add(data_path, index)
    drv = fcurve.driver
    drv.type = "SCRIPTED"
    drv.expression = expression
    for var_name, owner, prop_name in variables:
        var = drv.variables.new()
        var.name = var_name
        var.type = "SINGLE_PROP"
        var.targets[0].id = owner
        var.targets[0].data_path = f'["{prop_name}"]'
    return fcurve


def set_prop_key(master, frame, **values):
    for name, value in values.items():
        master[name] = value
        master.keyframe_insert(data_path=f'["{name}"]', frame=frame)


def set_transform_key(obj, frame, location=None, rotation=None):
    if location is not None:
        obj.location = location
        obj.keyframe_insert(data_path="location", frame=frame)
    if rotation is not None:
        obj.rotation_euler = rotation
        obj.keyframe_insert(data_path="rotation_euler", frame=frame)


def set_render_visibility_key(obj, frame, hidden):
    """Hide inactive proxy pieces in previews without hiding them in the viewport."""
    obj.hide_render = hidden
    obj.keyframe_insert(data_path="hide_render", frame=frame)


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def add_camera(name, loc, target, lens, col):
    data = bpy.data.cameras.new(name + "_Data")
    data.lens = lens
    data.sensor_width = 36
    cam = bpy.data.objects.new(name, data)
    cam.location = loc
    look_at(cam, target)
    col.objects.link(cam)
    return cam


def add_hand(name, ctrl, side, skin, accent, col):
    palm = cube(name + "_Palm", (0.105, 0.05, 0.13), (0, 0, 0), skin,
                col, ctrl, bevel=0.025)
    palm.rotation_euler[1] = math.radians(-10 if side == "L" else 10)
    x0 = -0.037
    for i in range(4):
        finger = cylinder(
            f"{name}_Finger_{i+1}", 0.011, 0.095,
            (x0 + i * 0.024, -0.006, -0.098), skin, col, ctrl,
            rotation=(0, 0, 0), vertices=16,
        )
        finger.rotation_euler[0] = math.radians(4 * (i - 1.5))
    thumb = cylinder(name + "_Thumb", 0.014, 0.075,
                     ((-0.065 if side == "L" else 0.065), 0, -0.02),
                     skin, col, ctrl,
                     rotation=(0, math.radians(68 if side == "L" else -68), 0),
                     vertices=16)
    cuff = cube(name + "_Cuff", (0.12, 0.065, 0.055), (0, 0, 0.09),
                accent, col, ctrl, bevel=0.015)
    return palm


def add_reference_empty(name, filepath, loc, scale, col):
    path = Path(filepath)
    if not path.exists():
        return None
    img = bpy.data.images.load(str(path), check_existing=True)
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_type = "IMAGE"
    obj.data = img
    obj.empty_display_size = scale
    obj.color[3] = 0.85
    obj.location = loc
    obj.rotation_euler = (math.radians(90), 0, 0)
    obj.hide_render = True
    obj["source_path"] = str(path)
    col.objects.link(obj)
    return obj


clear_scene()
scene = bpy.context.scene
scene.name = "FFDY_8454_Laundry_Sink_Motion_Rig"
scene.unit_settings.system = "METRIC"
scene.unit_settings.length_unit = "METERS"
scene.render.engine = "BLENDER_WORKBENCH"
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 252
scene.display.shading.light = "STUDIO"
scene.display.shading.studio_light = "paint.sl"
scene.display.shading.color_type = "MATERIAL"
scene.display.shading.show_shadows = True
scene.display.shading.show_cavity = True
scene.display.shading.cavity_type = "BOTH"
scene.display.shading.background_type = "VIEWPORT"
scene.display.shading.background_color = (0.055, 0.065, 0.085)
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = False

rig_col = collection("RIG_PRODUCT")
ctrl_col = collection("CONTROLS")
hands_col = collection("HANDS_OPTIONAL")
env_col = collection("ENVIRONMENT")
ref_col = collection("REFERENCES_STORYBOARD")
ref_col.hide_render = True

white = material("Cabinet_White", (0.88, 0.90, 0.92, 1))
left_mat = material("Left_Side_Blue", (0.28, 0.55, 0.92, 1))
right_mat = material("Right_Side_Cyan", (0.24, 0.78, 0.82, 1))
end_mat = material("End_Panel_Gold", (0.95, 0.66, 0.20, 1))
bottom_mat = material("Bottom_Piece_Purple", (0.66, 0.42, 0.92, 1))
rail_mat = material("Lock_Rail_Green", (0.30, 0.82, 0.46, 1))
orange = material("CLICKREADY_Orange", (1.0, 0.25, 0.035, 1))
metal = material("Sink_Metal", (0.48, 0.53, 0.58, 1))
dark = material("Dark_Labels", (0.025, 0.03, 0.04, 1))
skin = material("Hands_Skin", (0.64, 0.38, 0.26, 1))
sleeve = material("Hands_Sleeve", (0.34, 0.55, 0.78, 1))
mat_floor = material("Work_Mat", (0.12, 0.18, 0.24, 1))

floor = cube("Work_Mat", (3.7, 2.8, 0.025), (0, 0, -0.025), mat_floor,
             env_col, bevel=0.025)

master = empty("CTRL_Master_Select_Me", (0, 0, 0.04), ctrl_col, "CIRCLE", 0.25)
master.show_name = True
add_prop(master, "left_side_lift", 1.0,
         "0 = laid out flat, 1 = upright")
add_prop(master, "right_side_lift", 1.0,
         "0 = laid out flat, 1 = upright")
add_prop(master, "end_panel_insert", 0.0,
         "Shot 5: 0 = raised, 1 = seated")
add_prop(master, "side_top_spread", 0.0,
         "Shots 6/7: spreads only the top edges; lower pivots remain fixed")
add_prop(master, "bottom_piece_insert", 0.0,
         "Shot 6: 0 = outside, 1 = centered between side walls")
add_prop(master, "lock_rail_drop", 0.0,
         "Shot 7: 0 = raised, 1 = dropped straight down into place")
master["motion_proxy_notice"] = "Approximate storyboard-derived geometry; not CAD"
master["maximum_side_spread_degrees"] = 6.0

# Door/front frame lies on the mat while the RTA cabinet is assembled.
base = cube("Door_Frame_Base_FIXED", (W, D, BASE_TOP), (0, 0, BASE_TOP / 2),
            white, rig_col, bevel=0.018)
door_gap = 0.018
door_w = (W - 0.09 - door_gap) / 2
for idx, x in enumerate((-door_w / 2 - door_gap / 2, door_w / 2 + door_gap / 2), 1):
    cube(f"Door_{idx}_Outline", (door_w, D - 0.07, 0.012),
         (x, 0, BASE_TOP + 0.008), dark, rig_col, bevel=0.009)
    cube(f"Door_{idx}_Face", (door_w - 0.018, D - 0.088, 0.014),
         (x, 0, BASE_TOP + 0.017), white, rig_col, bevel=0.009)

for x in (-W * 0.36, W * 0.36):
    for y in (-D * 0.27, D * 0.27):
        cylinder("Hinge", 0.018, 0.055, (x, y, BASE_TOP + 0.045), metal,
                 rig_col, rotation=(0, math.radians(90), 0), vertices=16)

# Long side walls hinge around fixed lower edges.
left_pivot = empty("CTRL_LeftSide_FIXED_LOWER_PIVOT", (-W / 2, 0, BASE_TOP),
                   ctrl_col, "ARROWS", 0.16)
right_pivot = empty("CTRL_RightSide_FIXED_LOWER_PIVOT", (W / 2, 0, BASE_TOP),
                    ctrl_col, "ARROWS", 0.16)
left_side = cube("Panel_Long_Left", (T, D, H), (-T / 2, 0, H / 2),
                 left_mat, rig_col, left_pivot, bevel=0.014)
right_side = cube("Panel_Long_Right", (T, D, H), (T / 2, 0, H / 2),
                  right_mat, rig_col, right_pivot, bevel=0.014)

add_driver(left_pivot, "rotation_euler", 1,
           "-1.570796*(1-L)-0.104720*S",
           [("L", master, "left_side_lift"),
            ("S", master, "side_top_spread")])
add_driver(right_pivot, "rotation_euler", 1,
           "1.570796*(1-R)+0.104720*S",
           [("R", master, "right_side_lift"),
            ("S", master, "side_top_spread")])

# Orange click connectors are children of the side panels.
for side_name, parent, local_x in (("L", left_side, 0.025),
                                    ("R", right_side, -0.025)):
    for i, y in enumerate((-D * 0.30, D * 0.30), 1):
        cube(f"Connector_{side_name}_{i}", (0.024, 0.085, 0.075),
             (local_x, y, H * 0.13), orange, rig_col, parent, bevel=0.007)

# Shot 5: only this perpendicular end panel translates vertically.
end_ctrl = empty("CTRL_Shot05_EndPanel_Vertical", (0, D / 2 - T / 2, BASE_TOP),
                 ctrl_col, "SINGLE_ARROW", 0.20)
end_panel = cube("Panel_Perpendicular_End_SHOT05", (W - 2 * T, T, H),
                 (0, 0, H / 2), end_mat, rig_col, end_ctrl, bevel=0.014)
add_driver(end_ctrl, "location", 2, "(1-E)*0.42",
           [("E", master, "end_panel_insert")])

# Shot 6: a separate proxy for the named "bottom piece," sliding into the middle.
bottom_ctrl = empty("CTRL_Shot06_BottomPiece_Slide", (0, 0, BASE_TOP + 0.06),
                    ctrl_col, "SINGLE_ARROW", 0.20)
bottom_piece = cube("Bottom_Piece_SHOT06", (W - 0.10, D * 0.72, 0.028),
                    (0, 0, 0), bottom_mat, rig_col, bottom_ctrl, bevel=0.012)
add_driver(bottom_ctrl, "location", 1, "-0.62*(1-B)",
           [("B", master, "bottom_piece_insert")])

# Shot 7: narrow cross-piece drops vertically while lower side pivots remain fixed.
rail_ctrl = empty("CTRL_Shot07_LockRail_Vertical", (0, -D / 2 + T / 2, BASE_TOP),
                  ctrl_col, "SINGLE_ARROW", 0.20)
lock_rail = cube("Top_Locking_Piece_SHOT07", (W - 2 * T, T, 0.16),
                 (0, 0, H - 0.08), rail_mat, rig_col, rail_ctrl, bevel=0.012)
add_driver(rail_ctrl, "location", 2, "0.30*(1-D)",
           [("D", master, "lock_rail_drop")])

# A few loose context pieces from storyboard 1A. These do not drive the motion.
cube("Loose_ToeKick_REFERENCE", (0.82, 0.09, 0.025), (0.95, -0.86, 0.03),
     white, env_col, bevel=0.009)
cube("Loose_Trim_REFERENCE", (0.66, 0.07, 0.025), (0.96, -1.00, 0.03),
     white, env_col, bevel=0.009)
sink = cube("Sink_Basin_REFERENCE", (0.88, 0.54, 0.10), (-1.20, 0.60, 0.08),
            metal, env_col, bevel=0.07)
cube("Sink_Opening", (0.65, 0.34, 0.025), (-1.20, 0.60, 0.14), dark,
     env_col, bevel=0.05)

# Optional low-detail hand controls. They are deliberately independent so a user can edit them.
hand_l_ctrl = empty("CTRL_Hand_Left", (-0.38, 0.30, 1.18), ctrl_col,
                    "SPHERE", 0.06)
hand_r_ctrl = empty("CTRL_Hand_Right", (0.38, 0.30, 1.18), ctrl_col,
                    "SPHERE", 0.06)
add_hand("Hand_Left", hand_l_ctrl, "L", skin, sleeve, hands_col)
add_hand("Hand_Right", hand_r_ctrl, "R", skin, sleeve, hands_col)

# Simple color legend in the work area.
text_label("Title", "FFDY-8454  EDITABLE MOTION RIG", (0, 1.08, 0.03), 0.11,
           white, env_col, rotation=(0, 0, 0))
legend = "BLUE/CYAN: fixed-bottom side walls   GOLD: shot 5   PURPLE: shot 6   GREEN: shot 7"
text_label("Legend", legend, (0, -1.22, 0.03), 0.052, white, env_col,
           rotation=(0, 0, 0))

# Cameras and shot bindings.
camera_col = collection("CAMERAS")
overview = add_camera("CAM_Overview", (2.15, -2.35, 2.18), (0, 0, 0.36),
                      52, camera_col)
closeup = add_camera("CAM_Shot07_Closeup", (1.33, -1.33, 1.25),
                     (0, -D / 2 + 0.03, 0.74), 63, camera_col)
scene.camera = overview
for name, frame, cam in (("SHOT_05_END_PANEL", 1, overview),
                         ("SHOT_06_OPEN_INSERT_CLOSE", 90, overview),
                         ("SHOT_07_TOP_SPREAD_DROP_LOCK", 180, closeup)):
    marker = scene.timeline_markers.new(name, frame=frame)
    marker.camera = cam

# Each shot is self-contained on the timeline. The gaps make the shot boundaries obvious.
common = dict(left_side_lift=1.0, right_side_lift=1.0)
set_prop_key(master, 1, **common, end_panel_insert=0.0,
             side_top_spread=0.0, bottom_piece_insert=0.0, lock_rail_drop=0.0)
set_prop_key(master, 12, end_panel_insert=0.0)
set_prop_key(master, 60, end_panel_insert=1.0)
set_prop_key(master, 72, end_panel_insert=1.0)

set_prop_key(master, 89, **common, end_panel_insert=1.0,
             side_top_spread=0.0, bottom_piece_insert=0.0, lock_rail_drop=0.0)
set_prop_key(master, 90, side_top_spread=0.0, bottom_piece_insert=0.0)
set_prop_key(master, 108, side_top_spread=0.65, bottom_piece_insert=0.0)
set_prop_key(master, 132, side_top_spread=0.65, bottom_piece_insert=1.0)
set_prop_key(master, 156, side_top_spread=0.0, bottom_piece_insert=1.0)
set_prop_key(master, 162, side_top_spread=0.0, bottom_piece_insert=1.0)

set_prop_key(master, 179, **common, end_panel_insert=1.0,
             side_top_spread=0.0, bottom_piece_insert=1.0, lock_rail_drop=0.0)
set_prop_key(master, 180, side_top_spread=0.0, lock_rail_drop=0.0)
set_prop_key(master, 198, side_top_spread=1.0, lock_rail_drop=0.0)
set_prop_key(master, 224, side_top_spread=1.0, lock_rail_drop=1.0)
set_prop_key(master, 248, side_top_spread=0.0, lock_rail_drop=1.0)
set_prop_key(master, 252, side_top_spread=0.0, lock_rail_drop=1.0)

# Preview clarity: reveal each special-purpose proxy only in its relevant shot.
set_render_visibility_key(bottom_piece, 1, True)
set_render_visibility_key(bottom_piece, 89, True)
set_render_visibility_key(bottom_piece, 90, False)
set_render_visibility_key(lock_rail, 1, True)
set_render_visibility_key(lock_rail, 179, True)
set_render_visibility_key(lock_rail, 180, False)

# Hand proxy keys: editable guides, not physically solved hand animation.
set_transform_key(hand_l_ctrl, 1, (-0.38, D / 2 - 0.06, 1.18))
set_transform_key(hand_r_ctrl, 1, (0.38, D / 2 - 0.06, 1.18))
set_transform_key(hand_l_ctrl, 60, (-0.38, D / 2 - 0.06, 0.78))
set_transform_key(hand_r_ctrl, 60, (0.38, D / 2 - 0.06, 0.78))
set_transform_key(hand_l_ctrl, 90, (-W / 2 + 0.02, -0.15, 0.74))
set_transform_key(hand_r_ctrl, 90, (W / 2 - 0.02, -0.15, 0.74))
set_transform_key(hand_l_ctrl, 162, (-W / 2 + 0.02, -0.15, 0.74))
set_transform_key(hand_r_ctrl, 162, (W / 2 - 0.02, -0.15, 0.74))
set_transform_key(hand_l_ctrl, 180, (-W / 2 + 0.01, -D / 2 + 0.05, 0.76))
set_transform_key(hand_r_ctrl, 180, (W / 2 - 0.01, -D / 2 + 0.05, 0.76))
set_transform_key(hand_l_ctrl, 252, (-W / 2 + 0.01, -D / 2 + 0.05, 0.76))
set_transform_key(hand_r_ctrl, 252, (W / 2 - 0.01, -D / 2 + 0.05, 0.76))

# Blender 5.2 stores newly keyed properties in layered/slotted Actions. Their
# default Bezier interpolation is sufficient here; the drivers enforce the
# hard motion limits regardless of interpolation representation.

# Storyboard/sketch planes live in a separate, non-rendering collection.
reference_paths = [
    ROOT / "references" / "storyboard_all_pieces_image7.jpeg",
    ROOT / "references" / "storyboard_box_image11.jpeg",
    ROOT / "references" / "shot6_keyframe_1.png",
    ROOT / "references" / "shot6_keyframe_2.png",
    ROOT / "references" / "shot6_keyframe_3.png",
    ROOT / "references" / "shot7_motion_annotation.png",
]
for i, path in enumerate(reference_paths):
    add_reference_empty(f"REF_{i+1:02d}_{path.stem}", path,
                        (-3.1 + i * 1.22, 2.4, 1.0), 1.0, ref_col)

# Embed operational notes inside the .blend as a text block.
notes = bpy.data.texts.new("FFDY-8454_README")
notes.write("""FFDY-8454 Laundry Sink Motion Rig v1\n\n"
"Purpose: test whether explicit 3D articulation can communicate the failed shot 5/6/7 motions.\n"
"Geometry: approximate proxy inferred from storyboard and saved annotations; not CAD.\n\n"
"Select CTRL_Master_Select_Me and edit Custom Properties:\n"
"- end_panel_insert: shot 5 vertical end-panel placement\n"
"- side_top_spread: small top-only widening; lower pivots stay fixed\n"
"- bottom_piece_insert: shot 6 panel slides into the middle\n"
"- lock_rail_drop: shot 7 piece drops straight down\n"
"- left_side_lift/right_side_lift: optional earlier assembly exploration\n\n"
"Timeline markers:\n"
"- frames 1-72: shot 5\n"
"- frames 90-162: shot 6\n"
"- frames 180-252: shot 7\n"
"HANDS_OPTIONAL is independent and can be hidden or re-keyed.\n"
"REFERENCES_STORYBOARD is viewport-only.\n""")

scene["experiment"] = "FFDY-8454"
scene["source_ticket"] = "FFDY-7304"
scene["rig_version"] = "v1"
scene["geometry_confidence"] = "low-to-medium: storyboard-derived proxy"
scene["motion_constraints_confidence"] = "high: explicit saved prompts/annotations"
scene["source_root"] = "/home/colligo/hs_scripts/claude/thd/FFDY-7304"

scene.frame_set(1)
BLEND_PATH.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
print(f"Saved {BLEND_PATH}")
