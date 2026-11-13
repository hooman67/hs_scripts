#!/usr/bin/env python3
"""Re-cut the spot in the TARGET's shot order + fast-cut pacing.

Each entry: (gen-subdir, start_offset_s, take_duration_s). We trim a punchy window from each generated
shot so the whole thing reads at the real spot's montage tempo (~60s) instead of our slow 5s beats.
No new generations — reuses existing shot mp4s (incl. S01/S17/S18). No audio (VO/SUPERs are post).
"""
import os, subprocess
GEN = "/home/colligo/THD_laundry_sink_storyboard/gen"
OUT = os.path.join(GEN, "final_spot_v2.mp4")

# (subdir, start, dur) in target order
SEQ = [
    ("S01_establish_v2", 0.3, 5.0),   # establishing hero (hold)
    ("1A_assemble_v5",   0.3, 6.0),   # couple begin assembly
    ("3A_click_v1",      0.5, 2.5),   # connector ECU
    ("newshot4_oppside", 0.5, 4.0),   # opposite side connected
    ("newshot5_perp",    0.5, 4.0),   # perpendicular side / box takes shape
    ("4A_standup_v1",    1.0, 2.5),   # stand cabinet up
    ("4B_basin_v1",      1.0, 3.0),   # place basin
    ("5A_faucet_v1",     0.8, 2.5),   # pull-down faucet
    ("S17_drain_v1",     0.5, 2.0),   # drain strainer macro
    ("S18_whiteoak_v1",  0.3, 4.0),   # White Oak color variant (hold)
    ("6A_hardware_v1",   0.5, 2.5),   # brushed-nickel hardware
    ("7A_doors_v1",      0.5, 2.0),   # doors closing
    ("7B_hinge_v1",      0.5, 2.0),   # soft-close hinge
    ("8A_faucet_v1",     1.0, 3.0),   # woman turns on faucet
    ("8B_hero_v1",       1.0, 4.5),   # couple hero
    ("S01_establish_v2", 0.3, 3.0),   # final hero hold (end-card is post)
]

cmd = ["ffmpeg", "-nostdin", "-y", "-loglevel", "error"]
for sub, ss, d in SEQ:
    p = os.path.join(GEN, sub, sub + ".mp4")
    if not os.path.exists(p):
        raise SystemExit(f"missing {p}")
    cmd += ["-ss", str(ss), "-t", str(d), "-i", p]
n = len(SEQ)
fc = "".join(f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=decrease,"
             f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v{i}];" for i in range(n))
fc += "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[out]"
cmd += ["-filter_complex", fc, "-map", "[out]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", OUT]
print("assembling v2 (target order + fast cut) ...")
subprocess.run(cmd, check=True)
dur = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                      "-of","default=noprint_wrappers=1:nokey=1",OUT],capture_output=True,text=True).stdout.strip()
print(f"DONE -> {OUT}  ({dur}s, {n} shots)")
