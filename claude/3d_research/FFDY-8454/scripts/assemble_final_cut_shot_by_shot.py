#!/usr/bin/env python3
"""Assemble the approved laundry-sink clips in the exact user-specified order."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path("/home/colligo/hs_scripts/claude/3d_research/FFDY-8454")
OUTPUT_DIR = ROOT / "final_cuts"
OUTPUT = OUTPUT_DIR / "final_cut_shot_by_shot_v1.mp4"
MANIFEST = OUTPUT_DIR / "final_cut_shot_by_shot_v1.inputs.json"

GALLERY_ASSETS = Path("/home/colligo/THD_laundry_sink_storyboard/gallery/assets")
BLOCKOUT_ASSETS = ROOT / "gallery_combined_breakdown/assets"

SHOTS = [
    {
        "name": "1. S01 — establishing hero (storyboard image1)",
        "path": GALLERY_ASSETS / "S01.mp4",
        "url": "https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/assets/S01.mp4",
    },
    {
        "name": "2. ORDERED KEYFRAMES image7(flat) → image5(lifted) → image6(standing) — approved",
        "path": GALLERY_ASSETS / "1A.mp4",
        "url": "https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/assets/1A.mp4",
    },
    {
        "name": "3. i2v from image13 (connector + peg + hole clearly visible) — BEST",
        "path": GALLERY_ASSETS / "3A_v1.mp4",
        "url": "https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/assets/3A_v1.mp4",
    },
    {
        "name": "4. RETRY v2 — simplified Event Script",
        "path": BLOCKOUT_ASSETS / "shot04_event_script_v2_output.mp4",
        "url": "https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/3d_blockout_combined_v1/assets/shot04_event_script_v2_output.mp4",
    },
    {
        "name": "5. RETRY v2 — explicit rectangular footprint and supported motion",
        "path": BLOCKOUT_ASSETS / "shot06_event_script_v2_output.mp4",
        "url": "https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/3d_blockout_combined_v1/assets/shot06_event_script_v2_output.mp4",
    },
    {
        "name": "6. RETRY v2 — blockout-authoritative proportions and trajectory",
        "path": BLOCKOUT_ASSETS / "shot07A_event_script_v2_output.mp4",
        "url": "https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/3d_blockout_combined_v1/assets/shot07A_event_script_v2_output.mp4",
    },
    {
        "name": "7. RETRY v4C.2 — narrower exact moving strip",
        "path": BLOCKOUT_ASSETS / "shot07B_identity_v4c_narrow_v2_output.mp4",
        "url": "https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/3d_blockout_combined_v1/assets/shot07B_identity_v4c_narrow_v2_output.mp4",
    },
    {
        "name": "8. Isolated-shot call — exact fal / Seedance inputs",
        "path": BLOCKOUT_ASSETS / "shot08_blockout_v1_output.mp4",
        "url": "https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/3d_blockout_combined_v1/assets/shot08_blockout_v1_output.mp4",
    },
    {
        "name": "9. ROUND 1 — 4A (paint-out plate + generated couple)",
        "path": GALLERY_ASSETS / "4A.mp4",
        "url": "https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/assets/4A.mp4",
    },
    {
        "name": "10. ROUND 1 — 4B (paint-out plate + generated couple)",
        "path": GALLERY_ASSETS / "4B.mp4",
        "url": "https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/assets/4B.mp4",
    },
    {
        "name": "11. ROUND 1 — 8B (paint-out plate + generated couple)",
        "path": GALLERY_ASSETS / "8B.mp4",
        "url": "https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/assets/8B.mp4",
    },
]


def duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def main() -> None:
    missing = [str(shot["path"]) for shot in SHOTS if not shot["path"].is_file()]
    if missing:
        raise FileNotFoundError("Missing inputs:\n" + "\n".join(missing))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ffdy8454_final_cut_") as tmp:
        tmpdir = Path(tmp)
        normalized = []
        for index, shot in enumerate(SHOTS, 1):
            target = tmpdir / f"{index:02d}.mp4"
            subprocess.run(
                [
                    "ffmpeg",
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    "-y",
                    "-i",
                    str(shot["path"]),
                    "-map",
                    "0:v:0",
                    "-vf",
                    "scale=1920:1080:force_original_aspect_ratio=decrease,"
                    "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,"
                    "fps=24,setsar=1,format=yuv420p",
                    "-an",
                    "-c:v",
                    "libx264",
                    "-preset",
                    "medium",
                    "-crf",
                    "18",
                    "-movflags",
                    "+faststart",
                    str(target),
                ],
                check=True,
            )
            normalized.append(target)

        concat_file = tmpdir / "concat.txt"
        concat_file.write_text(
            "".join(f"file '{path.as_posix()}'\n" for path in normalized)
        )
        subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-c",
                "copy",
                "-movflags",
                "+faststart",
                str(OUTPUT),
            ],
            check=True,
        )

    records = []
    for shot in SHOTS:
        records.append(
            {
                "name": shot["name"],
                "path": str(shot["path"]),
                "url": shot["url"],
                "input_duration_seconds": round(duration(shot["path"]), 3),
            }
        )
    manifest = {
        "method": "Full-clip straight cuts in the user-specified order; normalized to H.264 1920x1080 24fps, yuv420p, CRF 18, no audio.",
        "output": str(OUTPUT),
        "output_duration_seconds": round(duration(OUTPUT), 3),
        "shots": records,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
