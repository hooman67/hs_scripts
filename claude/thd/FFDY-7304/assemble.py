#!/usr/bin/env python3
"""Assemble the generated shots into the full spot, in storyboard order.

Concatenates each shot's mp4 (normalized to 1920x1080 / 30fps) into one file. No audio (VO is added
later). Order follows the storyboard VO sequence. Writes to the media gen dir (not git).
"""
import os, subprocess

GEN = "/home/colligo/THD_laundry_sink_storyboard/gen"
OUT = os.path.join(GEN, "final_spot.mp4")

# (shot, gen-subdir) in storyboard / VO order
ORDER = [
    ("1A", "1A_assemble_v2"),
    ("2A", "2A_click_v1"),
    ("3A", "3A_click_v1"),
    ("4A", "4A_standup_v1"),
    ("4B", "4B_basin_v1"),
    ("5A", "5A_faucet_v1"),
    ("6A", "6A_hardware_v1"),
    ("7A", "7A_doors_v1"),
    ("7B", "7B_hinge_v1"),
    ("8A", "8A_faucet_v1"),
    ("8B", "8B_hero_v1"),
]

paths = []
for shot, sub in ORDER:
    p = os.path.join(GEN, sub, sub + ".mp4")
    if not os.path.exists(p):
        raise SystemExit(f"missing shot {shot}: {p}")
    paths.append(p)

# normalize each input then concat via filter_complex (handles differing fps/timebase)
cmd = ["ffmpeg", "-nostdin", "-y", "-loglevel", "error"]
for p in paths:
    cmd += ["-i", p]
n = len(paths)
fc = "".join(f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=decrease,"
             f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v{i}];" for i in range(n))
fc += "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[out]"
cmd += ["-filter_complex", fc, "-map", "[out]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", OUT]

print(f"assembling {n} shots ->", OUT)
subprocess.run(cmd, check=True)
dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "default=noprint_wrappers=1:nokey=1", OUT],
                     capture_output=True, text=True).stdout.strip()
print(f"DONE. duration = {dur}s, order = {[s for s,_ in ORDER]}")
