#!/usr/bin/env python3
"""Render an 8-fps review sequence sampled from the 24-fps v2 timeline."""

from pathlib import Path
import bpy


ROOT = Path("/home/colligo/hs_scripts/claude/3d_research/FFDY-8454")
OUT = ROOT / "renders" / "v2_preview_frames"
OUT.mkdir(parents=True, exist_ok=True)

scene = bpy.context.scene
scene.render.resolution_x = 480
scene.render.resolution_y = 270
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"

# Every third 24-fps timeline frame gives a 15-second preview at 8 fps.
for output_number, source_frame in enumerate(range(1, 361, 3), 1):
    scene.frame_set(source_frame)
    scene.render.filepath = str(OUT / f"f_{output_number:04d}.png")
    bpy.ops.render.render(write_still=True)
print(OUT)
