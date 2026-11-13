#!/usr/bin/env python3
"""Render v2 layout, pickup midpoint, and installation endpoints."""

from pathlib import Path
import bpy


ROOT = Path("/home/colligo/hs_scripts/claude/3d_research/FFDY-8454")
OUT = ROOT / "renders" / "v2_keyframes"
OUT.mkdir(parents=True, exist_ok=True)

scene = bpy.context.scene
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"

frames = {
    1: "all_six_pieces_flat",
    30: "front_frame_pickup",
    48: "front_frame_placed",
    84: "left_side_pickup",
    108: "left_side_installed",
    144: "right_side_pickup",
    168: "right_side_installed",
    204: "bottom_panel_pickup",
    228: "bottom_panel_installed",
    264: "wide_rail_pickup",
    288: "wide_rail_installed",
    324: "narrow_rail_pickup",
    348: "all_six_installed",
}
for frame, label in frames.items():
    scene.frame_set(frame)
    scene.render.filepath = str(OUT / f"f{frame:03d}_{label}.png")
    bpy.ops.render.render(write_still=True)
    print(scene.render.filepath)
