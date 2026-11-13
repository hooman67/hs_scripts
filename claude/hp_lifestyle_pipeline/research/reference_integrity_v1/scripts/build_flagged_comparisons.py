#!/usr/bin/env python3
"""Build compact displayed-twin/output comparisons for the three flagged rows."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CASES = (
    ("ee810cf51bb82bb4__p1__baseline-0016", "09_baseline-0016.jpg"),
    ("ee810cf51bb82bb4__p1__baseline-0018", "11_baseline-0018.jpg"),
    ("160db92655412f4d__p1__baseline-0016", "09_baseline-0016.jpg"),
)


def fit(image: Image.Image, width: int, height: int) -> Image.Image:
    copy = image.copy()
    copy.thumbnail((width, height), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (width, height), "white")
    canvas.paste(copy, ((width - copy.width) // 2, (height - copy.height) // 2))
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default(size=24)
    small = ImageFont.load_default(size=18)
    for safe_row_id, twin_filename in CASES:
        twin = Image.open(args.artifact_dir / twin_filename).convert("RGB")
        output = Image.open(args.artifact_dir / f"{safe_row_id}.png").convert("RGB")
        canvas = Image.new("RGB", (1640, 720), "white")
        draw = ImageDraw.Draw(canvas)
        draw.text((20, 14), safe_row_id, fill="black", font=font)
        draw.text((20, 52), f"Displayed twin: {twin_filename}", fill="black", font=small)
        draw.text((830, 52), "Generated output", fill="black", font=small)
        canvas.paste(fit(twin, 790, 630), (20, 82))
        canvas.paste(fit(output, 790, 630), (830, 82))
        canvas.save(args.output_dir / f"{safe_row_id}__comparison.jpg", quality=92)


if __name__ == "__main__":
    main()
