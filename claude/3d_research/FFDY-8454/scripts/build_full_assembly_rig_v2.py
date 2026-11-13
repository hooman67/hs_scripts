#!/usr/bin/env python3
"""Build the six-piece, user-authorable FFDY-8454 cabinet assembly rig v2.

The rig combines:
  1. an independent 0-1 layout-to-installed baseline per component; and
  2. a visible, freely keyframeable transform handle for arbitrary pickup paths.

The included order and timing are examples only. They are intentionally stored on
separate objects/actions so the user can reorder and retime every component.
"""

from pathlib import Path
import math

import bpy
from mathutils import Vector


ROOT = Path("/home/colligo/hs_scripts/claude/3d_research/FFDY-8454")
OUT = ROOT / "blender" / "laundry_sink_full_assembly_rig_v2.blend"

# Approximate cabinet proportions, inferred from storyboard photographs.
W = 1.20                  # cabinet width
H = 0.82                  # cabinet height; lies along Y during on-mat assembly
D = 0.62                  # cabinet depth; rises along Z during on-mat assembly
T = 0.035                 # proxy panel thickness


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


def relink(obj, col):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    col.objects.link(obj)


def mat(name, color):
    value = bpy.data.materials.new(name)
    value.diffuse_color = color
    return value


def cube(name, dims, loc=(0, 0, 0), material=None, col=None, parent=None,
         rot=(0, 0, 0), bevel=0.01):
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if parent:
        obj.parent = parent
    obj.location = loc
    obj.rotation_euler = rot
    if material:
        obj.data.materials.append(material)
        obj.color = material.diffuse_color
    if bevel:
        mod = obj.modifiers.new("Soft_Edges", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    if col:
        relink(obj, col)
    return obj


def cylinder(name, radius, depth, loc, material, col, parent=None,
             rot=(0, 0, 0), vertices=16):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius,
                                       depth=depth, location=(0, 0, 0))
    obj = bpy.context.object
    obj.name = name
    if parent:
        obj.parent = parent
    obj.location = loc
    obj.rotation_euler = rot
    obj.data.materials.append(material)
    obj.color = material.diffuse_color
    relink(obj, col)
    return obj


def empty(name, loc=(0, 0, 0), col=None, style="ARROWS", size=0.1,
          color=(1, 1, 1, 1), show_name=False):
    obj = bpy.data.objects.new(name, None)
    obj.location = loc
    obj.empty_display_type = style
    obj.empty_display_size = size
    obj.color = color
    obj.show_name = show_name
    obj.show_in_front = True
    (col or bpy.context.scene.collection).objects.link(obj)
    return obj


def label(name, body, loc, size, material, col, rot=(0, 0, 0), align="CENTER"):
    curve = bpy.data.curves.new(name + "_Curve", "FONT")
    curve.body = body
    curve.size = size
    curve.align_x = align
    curve.extrude = 0.0015
    curve.materials.append(material)
    obj = bpy.data.objects.new(name, curve)
    obj.location = loc
    obj.rotation_euler = rot
    col.objects.link(obj)
    return obj


def add_progress_prop(channel, part_number, label_text):
    channel["install_progress"] = 0.0
    channel.id_properties_ui("install_progress").update(
        min=0.0, max=1.0, soft_min=0.0, soft_max=1.0,
        description="0 = layout pose; 1 = installed pose",
    )
    channel["part_number"] = part_number
    channel["component"] = label_text
    channel["timing_authority"] = "USER — included keys are an editable example only"


def property_driver(obj, data_path, index, expression, channel):
    fc = obj.driver_add(data_path, index)
    driver = fc.driver
    driver.type = "SCRIPTED"
    driver.expression = expression
    var = driver.variables.new()
    var.name = "P"
    var.type = "SINGLE_PROP"
    var.targets[0].id = channel
    var.targets[0].data_path = '["install_progress"]'


def key_progress(channel, frame, value):
    channel["install_progress"] = value
    channel.keyframe_insert(data_path='["install_progress"]', frame=frame)


def key_direct(ctrl, frame, loc=(0, 0, 0), rot=(0, 0, 0)):
    ctrl.location = loc
    ctrl.rotation_euler = rot
    ctrl.keyframe_insert(data_path="location", frame=frame)
    ctrl.keyframe_insert(data_path="rotation_euler", frame=frame)


def look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def create_camera(name, loc, target, lens, col):
    data = bpy.data.cameras.new(name + "_Data")
    data.lens = lens
    cam = bpy.data.objects.new(name, data)
    cam.location = loc
    look_at(cam, target)
    col.objects.link(cam)
    return cam


clear_scene()
scene = bpy.context.scene
scene.name = "FFDY_8454_Full_Cabinet_Assembly_Rig_v2"
scene.unit_settings.system = "METRIC"
scene.unit_settings.length_unit = "METERS"
scene.frame_start = 1
scene.frame_end = 360
scene.render.fps = 24
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
scene.display.shading.background_color = (0.04, 0.05, 0.07)

parts_col = new_collection("PARTS_EXACTLY_SIX")
details_col = new_collection("PART_DETAILS")
channels_col = new_collection("CONTROLS_01_PROGRESS_CHANNELS")
direct_col = new_collection("CONTROLS_02_DIRECT_HANDLES")
internal_col = new_collection("RIG_INTERNALS")
guides_col = new_collection("POSE_GUIDES_INSTALLED")
environment_col = new_collection("ENVIRONMENT")
camera_col = new_collection("CAMERAS")

white = mat("Front_Frame_White", (0.91, 0.92, 0.93, 1))
colors = {
    "front": mat("01_Front_Frame", (0.89, 0.90, 0.93, 1)),
    "left": mat("02_Left_Side", (0.25, 0.56, 0.96, 1)),
    "right": mat("03_Right_Side", (0.20, 0.78, 0.82, 1)),
    "bottom": mat("04_Bottom_Panel", (0.96, 0.65, 0.20, 1)),
    "wide": mat("05_Wide_Rail", (0.68, 0.43, 0.94, 1)),
    "narrow": mat("06_Narrow_Rail", (0.33, 0.85, 0.47, 1)),
}
orange = mat("CLICKREADY_Orange", (1.0, 0.24, 0.025, 1))
metal = mat("Hinge_Metal", (0.35, 0.39, 0.44, 1))
ink = mat("Text", (0.92, 0.95, 1.0, 1))
floor_mat = mat("Assembly_Mat", (0.12, 0.17, 0.23, 1))
ghost_mat = mat("Installed_Ghost", (0.28, 0.32, 0.38, 1))

cube("Assembly_Mat", (4.25, 3.30, 0.025), (0, 0, -0.025), floor_mat,
     environment_col, bevel=0.025)
label("Title", "FFDY-8454  SIX-PIECE USER-AUTHORED CABINET ASSEMBLY",
      (0, 1.53, 0.02), 0.075, ink, environment_col)
label("Subtitle", "EXAMPLE ORDER ONLY — MOVE EACH PART'S KEYS TO DEFINE YOUR OWN ORDER AND TIMING",
      (0, -1.52, 0.02), 0.042, ink, environment_col)

# Layout mimics the storyboard parts sheet; installed pose is cabinet-on-front, open side up.
specs = [
    {
        "id": "01_FRONT_FRAME_DOORS", "label": "Front frame + doors",
        "dims": (W, H, T), "color": colors["front"],
        "layout_loc": (0.00, -0.15, T / 2), "layout_rot": (0, 0, 0),
        "installed_loc": (0, 0, T / 2), "installed_rot": (0, 0, 0),
        "start": 12, "end": 48, "lift": 0.16,
    },
    {
        "id": "02_LEFT_SIDE", "label": "Left side panel",
        "dims": (T, H, D), "color": colors["left"],
        "layout_loc": (-1.05, 0.22, T / 2), "layout_rot": (0, -math.pi / 2, 0),
        "installed_loc": (-W / 2 + T / 2, 0, T + D / 2), "installed_rot": (0, 0, 0),
        "start": 60, "end": 108, "lift": 0.24,
    },
    {
        "id": "03_RIGHT_SIDE", "label": "Right side panel",
        "dims": (T, H, D), "color": colors["right"],
        "layout_loc": (1.05, 0.22, T / 2), "layout_rot": (0, math.pi / 2, 0),
        "installed_loc": (W / 2 - T / 2, 0, T + D / 2), "installed_rot": (0, 0, 0),
        "start": 120, "end": 168, "lift": 0.24,
    },
    {
        "id": "04_BOTTOM_PANEL", "label": "Bottom panel",
        "dims": (W - 2 * T, T, D - 0.05), "color": colors["bottom"],
        "layout_loc": (0, 1.04, T / 2), "layout_rot": (math.pi / 2, 0, 0),
        "installed_loc": (0, -H / 2 + T / 2, T + (D - 0.05) / 2),
        "installed_rot": (0, 0, 0),
        "start": 180, "end": 228, "lift": 0.23,
    },
    {
        "id": "05_WIDE_RAIL", "label": "Wide rail",
        "dims": (W - 2 * T, T, 0.18), "color": colors["wide"],
        "layout_loc": (1.33, -0.72, T / 2),
        "layout_rot": (math.pi / 2, 0, math.pi / 2),
        "installed_loc": (0, H / 2 - T / 2, D - 0.10), "installed_rot": (0, 0, 0),
        "start": 240, "end": 288, "lift": 0.20,
    },
    {
        "id": "06_NARROW_RAIL", "label": "Narrow rail",
        "dims": (W - 2 * T, T, 0.075), "color": colors["narrow"],
        "layout_loc": (1.58, -0.72, T / 2),
        "layout_rot": (math.pi / 2, 0, math.pi / 2),
        "installed_loc": (0, H / 2 - T / 2, 0.13), "installed_rot": (0, 0, 0),
        "start": 300, "end": 348, "lift": 0.18,
    },
]

rig_records = []
for number, spec in enumerate(specs, 1):
    rgba = spec["color"].diffuse_color
    channel = empty(
        f"PROGRESS_{spec['id']}", (-1.95, 1.28 - (number - 1) * 0.25, 0.08),
        channels_col, "CIRCLE", 0.09, rgba, True,
    )
    add_progress_prop(channel, number, spec["label"])
    channel["example_start_frame"] = spec["start"]
    channel["example_end_frame"] = spec["end"]

    base = empty(f"INTERNAL_BASE_LOCATION_{spec['id']}", (0, 0, 0),
                 internal_col, "PLAIN_AXES", 0.018, rgba, False)
    direct = empty(f"MOVE_ROTATE_{spec['id']}", (0, 0, 0), direct_col,
                   "CUBE", 0.105, rgba, True)
    direct.parent = base
    autorot = empty(f"INTERNAL_AUTO_ROTATION_{spec['id']}", (0, 0, 0),
                    internal_col, "PLAIN_AXES", 0.018, rgba, False)
    autorot.parent = direct

    p = "min(max(P,0.0),1.0)"
    for axis in range(3):
        a = spec["layout_loc"][axis]
        b = spec["installed_loc"][axis]
        property_driver(base, "location", axis, f"({a})+(({b})-({a}))*{p}", channel)
        ra = spec["layout_rot"][axis]
        rb = spec["installed_rot"][axis]
        property_driver(autorot, "rotation_euler", axis,
                        f"({ra})+(({rb})-({ra}))*{p}", channel)

    component = cube(f"PART_{spec['id']}", spec["dims"], (0, 0, 0),
                     spec["color"], parts_col, autorot, bevel=0.013)
    component["component_number"] = number
    component["component_label"] = spec["label"]
    component["geometry_notice"] = "Approximate storyboard-derived proxy; not CAD"

    # Installed-pose wire guide: visible in viewport, excluded from renders.
    ghost = cube(f"GUIDE_INSTALLED_{spec['id']}", spec["dims"],
                 spec["installed_loc"], ghost_mat, guides_col,
                 rot=spec["installed_rot"], bevel=0)
    ghost.display_type = "WIRE"
    ghost.show_in_front = True
    ghost.hide_render = True

    # Independent example track: user can shift/reorder these keys per component.
    key_progress(channel, 1, 0.0)
    key_progress(channel, spec["start"], 0.0)
    key_progress(channel, spec["end"], 1.0)
    key_progress(channel, 360, 1.0)
    mid = round((spec["start"] + spec["end"]) / 2)
    key_direct(direct, spec["start"], (0, 0, 0), (0, 0, 0))
    key_direct(direct, mid, (0, 0, spec["lift"]), (0, 0, 0))
    key_direct(direct, spec["end"], (0, 0, 0), (0, 0, 0))

    marker = scene.timeline_markers.new(
        f"EXAMPLE_{number:02d}_{spec['label'].upper().replace(' ', '_')}",
        frame=spec["start"],
    )
    rig_records.append((spec, channel, base, direct, autorot, component))

# Door detail belongs to the front-frame component but is not an additional component.
front_autorot = rig_records[0][4]
door_w = (W - 0.09) / 2
for i, x in enumerate((-door_w / 2 - 0.008, door_w / 2 + 0.008), 1):
    cube(f"DETAIL_Door_{i}", (door_w - 0.018, H - 0.10, 0.012),
         (x, 0, T / 2 + 0.008), white, details_col, front_autorot, bevel=0.009)
    for y in (-H * 0.32, H * 0.32):
        cylinder(f"DETAIL_Hinge_{i}_{y:+.2f}", 0.014, 0.052,
                 (x + (-0.17 if i == 1 else 0.17), y, T / 2 + 0.035),
                 metal, details_col, front_autorot,
                 rot=(0, math.pi / 2, 0))

# Image 7 shows that the two short legs belong to the central front-frame/door
# assembly, protruding from one short edge in its photographed layout.
front_leg_extension = 0.12
front_leg_height = 0.10
for side, y in (("Top", H / 2 - front_leg_height / 2),
                ("Bottom", -H / 2 + front_leg_height / 2)):
    cube(f"DETAIL_FrontFrame_{side}_Leg",
         (front_leg_extension, front_leg_height, T),
         (W / 2 + front_leg_extension / 2, y, 0),
         colors["front"], details_col, front_autorot, bevel=0.008)

# Orange connector cues on panels; these are details, not separate cabinet pieces.
for spec, channel, base, direct, autorot, component in rig_records[1:4]:
    for x_sign in (-1, 1):
        cube(f"DETAIL_Connector_{spec['id']}_{x_sign:+d}",
             (0.045, 0.055, 0.025),
             (x_sign * spec["dims"][0] * 0.35, 0, spec["dims"][2] * 0.42),
             orange, details_col, autorot, bevel=0.005)

# Control-board labels are renderable so preview semantics remain clear.
label("Control_Header", "PROGRESS CHANNELS", (-1.93, 1.43, 0.02), 0.043,
      ink, environment_col)
for number, spec in enumerate(specs, 1):
    label(f"Control_Label_{number:02d}", f"{number}. {spec['label']}",
          (-1.82, 1.28 - (number - 1) * 0.25, 0.02), 0.038,
          spec["color"], environment_col, align="LEFT")

# Camera sees both the parts layout and the final assembly.
cam = create_camera("CAM_Assembly_Overview", (3.25, -3.70, 3.55),
                    (0, 0.02, 0.10), 53, camera_col)
scene.camera = cam

# Embed clear instructions in the Blender file.
notes = bpy.data.texts.new("START_HERE_FFDY_8454_V2")
notes.write(
    "FFDY-8454 full cabinet assembly rig v2\n\n"
    "There are exactly six cabinet component roots in PARTS_EXACTLY_SIX.\n"
    "The included order/timing is an editable example, not authoritative.\n\n"
    "For each component:\n"
    "1. Select PROGRESS_<part> and key install_progress (0=layout, 1=installed).\n"
    "2. Select the visible MOVE_ROTATE_<part> cube handle to add arbitrary pickup path, "
    "translation, or rotation keys.\n"
    "3. Move that component's independent keys to choose order and duration.\n\n"
    "POSE_GUIDES_INSTALLED contains non-rendering wire guides.\n"
    "Hands are intentionally excluded from v2; first validate cabinet authoring.\n"
)

scene["experiment"] = "FFDY-8454"
scene["rig_version"] = "v2"
scene["component_count"] = 6
scene["scope"] = "cabinet only; sink, faucet, hardware and hands excluded"
scene["order_authority"] = "user"
scene["timing_authority"] = "user"
scene["geometry_confidence"] = "medium topology, low dimensions; storyboard-derived"
scene["source_reference"] = str(ROOT / "references" / "storyboard_all_pieces_image7.jpeg")

# Start in the clean layout state with all six visible handles selected as a group.
scene.frame_set(1)
bpy.ops.object.select_all(action="DESELECT")
for _, _, _, direct, _, _ in rig_records:
    direct.select_set(True)
bpy.context.view_layer.objects.active = rig_records[0][3]

OUT.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
print(f"Saved {OUT}")
