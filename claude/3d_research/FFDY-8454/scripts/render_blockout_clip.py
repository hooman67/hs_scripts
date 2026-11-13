"""Render one frame range from an already-open Blender file as an H.264 blockout.

Usage:
  blender --background file.blend --python render_blockout_clip.py -- \
      START END /absolute/output/frames_directory [CAMERA_LENS_MM]

The source .blend is never saved by this script.
"""

from pathlib import Path
import sys

import bpy


args = sys.argv[sys.argv.index("--") + 1:]
if len(args) not in (3, 4):
    raise SystemExit("expected: START END /absolute/output/frames_directory [CAMERA_LENS_MM]")

start, end = int(args[0]), int(args[1])
output = Path(args[2]).resolve()
output.mkdir(parents=True, exist_ok=True)
if len(args) == 4:
    bpy.context.scene.camera.data.lens = float(args[3])

scene = bpy.context.scene
scene.frame_start = start
scene.frame_end = end
scene.render.fps = 24
scene.render.engine = "BLENDER_WORKBENCH"
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(output / "frame_")

bpy.ops.render.render(animation=True)
print(f"RENDERED_BLOCKOUT_FRAMES {output}")
