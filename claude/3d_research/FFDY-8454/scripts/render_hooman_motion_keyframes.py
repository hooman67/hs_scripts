"""Render review stills from Hooman's authored cabinet animation.

Run with Blender after opening the .blend on the command line. This script does
not save or modify the source .blend; it only changes in-memory render settings.
"""

from pathlib import Path

import bpy


ROOT = Path("/home/colligo/hs_scripts/claude/3d_research/FFDY-8454")
OUT = ROOT / "renders" / "hooman_motion_review" / "keyframes"
OUT.mkdir(parents=True, exist_ok=True)

scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = False

for frame in (1, 24, 48, 72, 96, 120, 144, 168, 192, 216,
              240, 264, 278, 300, 324, 348):
    scene.frame_set(frame)
    scene.render.filepath = str(OUT / f"frame_{frame:04d}.png")
    bpy.ops.render.render(write_still=True)
    print(f"RENDERED {scene.render.filepath}")
