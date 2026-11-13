#!/usr/bin/env python3
"""Build the all-shot laundry-sink review cut used by the gallery.

This preserves the FINAL v2 target-order trims, inserts the gallery's chosen
Shot 6 and Shot 7 results between Shot 5 and Shot 8, and writes a versioned
output without replacing any prior edit.
"""

import json
import os
import subprocess


GEN = "/home/colligo/THD_laundry_sink_storyboard/gen"
OUT = os.path.join(GEN, "final_spot_all_shots_v3.mp4")
MANIFEST = os.path.join(GEN, "final_spot_all_shots_v3.inputs.json")

# (label, subdirectory, filename, start offset, duration)
# None means use the rest of the source. Shot 6 is already the user-chosen
# trim, so it and Shot 7 are included in full.
SEQ = [
    ("Shot 1 / S01 establishing", "S01_establish_v2", "S01_establish_v2.mp4", 0.3, 5.0),
    ("Shot 2 / 1A assembly", "1A_assemble_v5", "1A_assemble_v5.mp4", 0.3, 6.0),
    ("Shot 3 / 3A connector macro", "3A_click_v1", "3A_click_v1.mp4", 0.5, 2.5),
    ("Shot 4 / opposite side", "newshot4_oppside", "newshot4_oppside.mp4", 0.5, 4.0),
    ("Shot 5 / perpendicular wall", "newshot5_perp", "newshot5_perp.mp4", 0.5, 4.0),
    ("Shot 6 / box completion", "shot6a_sketch", "shot6a_prev_trim.mp4", 0.0, None),
    ("Shot 7 / box completion close-up", "shot7_v3edit", "shot7_v3edit.mp4", 0.0, None),
    ("Shot 8 / 4A stand cabinet", "4A_standup_v1", "4A_standup_v1.mp4", 1.0, 2.5),
    ("Shot 9 / 4B place basin", "4B_basin_v1", "4B_basin_v1.mp4", 1.0, 3.0),
    ("5A pull-down faucet", "5A_faucet_v1", "5A_faucet_v1.mp4", 0.8, 2.5),
    ("S17 drain macro", "S17_drain_v1", "S17_drain_v1.mp4", 0.5, 2.0),
    ("S18 White Oak variant", "S18_whiteoak_v1", "S18_whiteoak_v1.mp4", 0.3, 4.0),
    ("6A brushed-nickel hardware", "6A_hardware_v1", "6A_hardware_v1.mp4", 0.5, 2.5),
    ("7A doors closing", "7A_doors_v1", "7A_doors_v1.mp4", 0.5, 2.0),
    ("7B soft-close hinge", "7B_hinge_v1", "7B_hinge_v1.mp4", 0.5, 2.0),
    ("Shot 10 / 8A faucet on", "8A_faucet_v1", "8A_faucet_v1.mp4", 1.0, 3.0),
    ("Shot 11 / 8B couple hero", "8B_hero_v1", "8B_hero_v1.mp4", 1.0, 4.5),
    ("Final product hero hold", "S01_establish_v2", "S01_establish_v2.mp4", 0.3, 3.0),
]


def probe_duration(path):
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", path,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


inputs = []
cmd = ["ffmpeg", "-nostdin", "-y", "-loglevel", "error"]
for label, subdir, filename, start, duration in SEQ:
    path = os.path.join(GEN, subdir, filename)
    if not os.path.exists(path):
        raise SystemExit(f"missing {label}: {path}")
    source_duration = probe_duration(path)
    used_duration = duration if duration is not None else source_duration - start
    cmd += ["-ss", str(start), "-t", str(used_duration), "-i", path]
    inputs.append(
        {
            "label": label,
            "path": path,
            "source_duration_seconds": source_duration,
            "start_seconds": start,
            "used_duration_seconds": used_duration,
        }
    )

n = len(inputs)
filters = "".join(
    f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=decrease,"
    f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v{i}];"
    for i in range(n)
)
filters += "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[out]"
cmd += [
    "-filter_complex", filters,
    "-map", "[out]",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-crf", "18",
    "-preset", "medium",
    "-movflags", "+faststart",
    OUT,
]

print(f"assembling {n} ordered segments -> {OUT}")
subprocess.run(cmd, check=True)
output_duration = probe_duration(OUT)

with open(MANIFEST, "w", encoding="utf-8") as handle:
    json.dump(
        {
            "output": OUT,
            "output_duration_seconds": output_duration,
            "method": "ffmpeg filter_complex; normalize each segment to padded 1920x1080, 30 fps; straight-cut concat; H.264 CRF 18; no audio",
            "inputs": inputs,
        },
        handle,
        indent=2,
    )
    handle.write("\n")

print(f"DONE: {output_duration:.3f}s")
print(f"INPUT MANIFEST: {MANIFEST}")
