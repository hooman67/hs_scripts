#!/usr/bin/env python3
"""Build three labeled contact sheets covering all 15 scene/twin pairs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
IMAGE_MANIFEST = HERE / "evidence" / "image_payload_manifest.json"
OUTPUT_DIR = HERE / "contact_sheets"
OUTPUT_MANIFEST = HERE / "evidence" / "contact_sheet_manifest.json"
ROWS_PER_SHEET = 5
PANEL_WIDTH = 520
PANEL_HEIGHT = 390
HEADER_HEIGHT = 52
ROW_GAP = 10
MARGIN = 18


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contain(path: Path) -> Image.Image:
    with Image.open(path) as opened:
        image = opened.convert("RGB")
        image.thumbnail((PANEL_WIDTH, PANEL_HEIGHT), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (PANEL_WIDTH, PANEL_HEIGHT), "white")
    canvas.paste(image, ((PANEL_WIDTH - image.width) // 2, (PANEL_HEIGHT - image.height) // 2))
    return canvas


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
    source = json.loads(IMAGE_MANIFEST.read_text(encoding="utf-8"))
    pairs = source["pairs"]
    font = ImageFont.load_default()
    sheets = []
    for start in range(0, len(pairs), ROWS_PER_SHEET):
        batch = pairs[start : start + ROWS_PER_SHEET]
        width = MARGIN * 2 + PANEL_WIDTH * 2 + ROW_GAP
        row_height = HEADER_HEIGHT + PANEL_HEIGHT + ROW_GAP
        height = MARGIN * 2 + row_height * len(batch)
        sheet = Image.new("RGB", (width, height), "#20242a")
        draw = ImageDraw.Draw(sheet)
        covered = []
        for index, pair in enumerate(batch):
            top = MARGIN + index * row_height
            record_id = pair["record_id"]
            draw.text((MARGIN, top + 4), f"{record_id}  |  GENERATED SCENE (left)  |  ORIGINAL TWIN (right)", fill="white", font=font)
            image_top = top + HEADER_HEIGHT
            generated = contain(Path(pair["generated_scene"]["derivative_path"]))
            twin = contain(Path(pair["digital_twin"]["derivative_path"]))
            sheet.paste(generated, (MARGIN, image_top))
            sheet.paste(twin, (MARGIN + PANEL_WIDTH + ROW_GAP, image_top))
            covered.append(record_id)
        sheet_index = start // ROWS_PER_SHEET + 1
        output = OUTPUT_DIR / f"contact_sheet_{sheet_index:02d}.jpg"
        sheet.save(output, format="JPEG", quality=88, optimize=True, progressive=True, exif=b"")
        sheets.append(
            {
                "path": str(output),
                "sha256": sha256(output),
                "bytes": output.stat().st_size,
                "width": width,
                "height": height,
                "record_ids": covered,
            }
        )
    covered_ids = [record_id for sheet in sheets for record_id in sheet["record_ids"]]
    expected_ids = [pair["record_id"] for pair in pairs]
    if covered_ids != expected_ids or len(sheets) > 5:
        raise RuntimeError("Contact-sheet coverage/order check failed")
    manifest = {
        "schema_version": "hp-placement-astra-contact-sheets-v1",
        "source_image_payload_manifest_sha256": sha256(IMAGE_MANIFEST),
        "sheet_count": len(sheets),
        "pair_count": len(covered_ids),
        "all_pairs_covered_once": len(covered_ids) == len(set(covered_ids)) == 15,
        "total_bytes": sum(sheet["bytes"] for sheet in sheets),
        "sheets": sheets,
    }
    temporary = OUTPUT_MANIFEST.with_suffix(".tmp")
    temporary.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    temporary.replace(OUTPUT_MANIFEST)
    print(json.dumps({"manifest": str(OUTPUT_MANIFEST), "sheets": len(sheets), "pairs": len(covered_ids), "bytes": manifest["total_bytes"], "sha256": sha256(OUTPUT_MANIFEST)}))


if __name__ == "__main__":
    main()
