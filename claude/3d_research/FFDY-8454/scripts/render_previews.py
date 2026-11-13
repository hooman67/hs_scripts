#!/usr/bin/env python3
"""Render lightweight PNG sequences for later MP4 encoding with system FFmpeg."""

from pathlib import Path
import bpy


ROOT = Path("/home/colligo/hs_scripts/claude/3d_research/FFDY-8454")
OUT = ROOT / "renders" / "previews"
OUT.mkdir(parents=True, exist_ok=True)

scene = bpy.context.scene
scene.render.resolution_x = 480
scene.render.resolution_y = 270
scene.render.resolution_percentage = 100
scene.render.fps = 24
scene.render.image_settings.file_format = "PNG"

segments = (
    ("shot05_end_panel_insert", 1, 72),
    ("shot06_open_insert_close", 90, 162),
    ("shot07_spread_drop_lock", 180, 252),
)

for name, first, last in segments:
    segment_dir = OUT / (name + "_frames")
    segment_dir.mkdir(parents=True, exist_ok=True)
    scene.frame_start = first
    scene.frame_end = last
    scene.render.filepath = str(segment_dir / "f_")
    bpy.ops.render.render(animation=True)
    print(segment_dir)
