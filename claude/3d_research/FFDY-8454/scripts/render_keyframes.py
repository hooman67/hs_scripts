#!/usr/bin/env python3
"""Render representative rig states from the already-open .blend file."""

from pathlib import Path
import bpy


ROOT = Path("/home/colligo/hs_scripts/claude/3d_research/FFDY-8454")
OUT = ROOT / "renders" / "keyframes"
OUT.mkdir(parents=True, exist_ok=True)

scene = bpy.context.scene
scene.render.image_settings.file_format = "PNG"
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100

frames = {
    1: "shot05_start_end_panel_raised",
    36: "shot05_mid_lowering",
    60: "shot05_end_panel_seated",
    90: "shot06_start_closed",
    108: "shot06_small_top_spread",
    132: "shot06_bottom_piece_inserted",
    156: "shot06_sides_closed",
    180: "shot07_start",
    198: "shot07_top_spread_bottom_fixed",
    224: "shot07_lock_piece_dropped",
    248: "shot07_locked_closed",
}

for frame, label in frames.items():
    scene.frame_set(frame)
    scene.render.filepath = str(OUT / f"f{frame:03d}_{label}.png")
    bpy.ops.render.render(write_still=True)
    print(scene.render.filepath)

