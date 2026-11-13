"""Render fixed-camera evidence frames from an open laundry-sink Blender file.

Usage:
  blender FILE.blend --background --python render_v5_geometry_evidence.py -- OUTPUT_DIR LABEL
"""

from pathlib import Path
import sys

import bpy


FRAMES = (1, 192, 216, 240, 264, 278, 324, 348)


def main():
    if "--" not in sys.argv:
        raise SystemExit("Expected OUTPUT_DIR and LABEL after --")
    args = sys.argv[sys.argv.index("--") + 1 :]
    if len(args) != 2:
        raise SystemExit("Expected exactly OUTPUT_DIR and LABEL")
    output = Path(args[0])
    label = args[1]
    output.mkdir(parents=True, exist_ok=False)

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.display.shading.light = "STUDIO"
    scene.display.shading.studio_light = "paint.sl"
    scene.display.shading.color_type = "MATERIAL"
    scene.display.shading.show_shadows = True
    scene.display.shading.show_cavity = True
    # A wider fixed lens keeps the assembled cabinet visible after stand-up and
    # is identical for old and new renders.
    scene.camera.data.lens = 35

    for frame in FRAMES:
        scene.frame_set(frame)
        scene.render.filepath = str(output / f"{label}_frame_{frame:04d}.png")
        bpy.ops.render.render(write_still=True)
        print(f"RENDERED {scene.render.filepath}")


if __name__ == "__main__":
    main()
