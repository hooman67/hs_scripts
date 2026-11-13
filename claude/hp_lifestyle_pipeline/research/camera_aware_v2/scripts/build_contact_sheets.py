#!/usr/bin/env python3
"""Build local, labeled review sheets for ZIP camera views and PDF pages.

PDF rendering uses PyMuPDF (import name ``fitz``); the image sheets use Pillow.
Outputs stay below local_data/HP_scenes/review and are intentionally Git-ignored.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont, ImageOps


PROJECT_ROOT = Path(__file__).resolve().parents[3]
LOCAL_ROOT = PROJECT_ROOT / "local_data" / "HP_scenes"
SHARED = LOCAL_ROOT / "extracted" / "Shared"
REVIEW = LOCAL_ROOT / "review"
DATA = PROJECT_ROOT / "research" / "camera_aware" / "data"


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = Path("/usr/share/fonts/truetype/dejavu") / name
    if path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def fit_image(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    rgba = image.convert("RGBA")
    background = Image.new("RGBA", rgba.size, "#d8d8d8")
    background.alpha_composite(rgba)
    result = ImageOps.contain(background.convert("RGB"), size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, "#d8d8d8")
    canvas.paste(result, ((size[0] - result.width) // 2, (size[1] - result.height) // 2))
    return canvas


def build_device_sheet(device: dict, assets: list[dict]) -> Path:
    columns = 5
    image_size = (240, 135)
    tile = (260, 190)
    header = 74
    rows = math.ceil(len(assets) / columns)
    sheet = Image.new("RGB", (columns * tile[0], header + rows * tile[1]), "#eeeeee")
    draw = ImageDraw.Draw(sheet)
    title = device["device_asset_name_from_folder"]
    draw.text((16, 10), title, fill="black", font=font(22, True))
    type_label = (
        f"effective type {device['effective_device_type']} · "
        f"source-declared {device['source_declared_device_type']}"
    )
    if device.get("device_type_correction_id"):
        type_label += f" · USER-CONFIRMED correction {device['device_type_correction_id']}"
    draw.text(
        (16, 41),
        f"{type_label} · {len(assets)} camera files",
        fill="#333333",
        font=font(13),
    )
    for index, asset in enumerate(assets):
        row, col = divmod(index, columns)
        x, y = col * tile[0], header + row * tile[1]
        with Image.open(asset["extracted_absolute_path"]) as source:
            thumb = fit_image(source, image_size)
        sheet.paste(thumb, (x + 10, y + 4))
        label = asset["camera_name_exact"]
        label_font = font(13, True)
        if draw.textlength(label, font=label_font) > 242:
            label_font = font(11, True)
        draw.text((x + 10, y + 144), label, fill="black", font=label_font)
        draw.text(
            (x + 10, y + 164),
            f"{asset['width_px']}×{asset['height_px']} · mask {asset.get('alpha_nonzero_occupancy_fraction', 0):.1%}",
            fill="#444444",
            font=font(10),
        )
    output = REVIEW / "camera_views" / f"{device['device_id']}.contact_sheet.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, optimize=True)
    return output


def build_device_index(sheet_paths: list[Path]) -> Path:
    columns = 2
    tile = (720, 950)
    rows = math.ceil(len(sheet_paths) / columns)
    canvas = Image.new("RGB", (columns * tile[0], rows * tile[1]), "#d8d8d8")
    for index, path in enumerate(sheet_paths):
        with Image.open(path) as source:
            preview = fit_image(source, (700, 930))
        row, col = divmod(index, columns)
        canvas.paste(preview, (col * tile[0] + 10, row * tile[1] + 10))
    output = REVIEW / "camera_views_all_devices_index.png"
    canvas.save(output, optimize=True)
    return output


def render_pdf_pages(catalog: dict) -> tuple[list[Path], Path]:
    rendered: list[tuple[Path, str]] = []
    page_dir = REVIEW / "pdf_pages"
    page_dir.mkdir(parents=True, exist_ok=True)
    for report in catalog["pdf_reports"]:
        source_id = report["source_id"]
        document = fitz.open(report["pdf_absolute_path"])
        for page_index, page in enumerate(document):
            pixmap = page.get_pixmap(matrix=fitz.Matrix(0.45, 0.45), alpha=False)
            image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
            page_record = report["pages"][page_index]
            output = page_dir / f"{source_id}.page_{page_index + 1:02d}.png"
            image.save(output, optimize=True)
            rendered.append(
                (
                    output,
                    f"{source_id} · p.{page_index + 1} · {page_record['page_device_asset_name_exact']}",
                )
            )
        document.close()

    columns = 2
    tile = (920, 670)
    rows = math.ceil(len(rendered) / columns)
    canvas = Image.new("RGB", (columns * tile[0], rows * tile[1]), "#d8d8d8")
    draw = ImageDraw.Draw(canvas)
    for index, (path, label) in enumerate(rendered):
        row, col = divmod(index, columns)
        x, y = col * tile[0], row * tile[1]
        with Image.open(path) as source:
            preview = fit_image(source, (900, 620))
        canvas.paste(preview, (x + 10, y + 40))
        display = label if len(label) <= 104 else label[:101] + "..."
        draw.text((x + 10, y + 10), display, fill="black", font=font(14, True))
    contact = REVIEW / "pdf_pages_contact_sheet.png"
    canvas.save(contact, optimize=True)
    return [item[0] for item in rendered], contact


def main() -> None:
    catalog = json.loads((DATA / "camera_catalog.json").read_text(encoding="utf-8"))
    mask_metrics = json.loads(
        (DATA / "camera_alpha_mask_metrics.json").read_text(encoding="utf-8")
    )
    metrics_by_zip = {item["zip_filename"]: item for item in mask_metrics["assets"]}
    for asset in catalog["high_resolution_assets"]:
        asset.update(metrics_by_zip[asset["zip_filename"]])
    assets_by_device: dict[str, list[dict]] = {}
    for asset in catalog["high_resolution_assets"]:
        assets_by_device.setdefault(asset["device_id"], []).append(asset)
    sheets = []
    for device in catalog["devices"]:
        assets = sorted(
            assets_by_device[device["device_id"]], key=lambda item: item["camera_name_exact"]
        )
        sheets.append(build_device_sheet(device, assets))
    device_index = build_device_index(sheets)
    pdf_pages, pdf_contact = render_pdf_pages(catalog)
    index = {
        "camera_device_contact_sheets": [str(path) for path in sheets],
        "camera_all_devices_index": str(device_index),
        "pdf_page_renders": [str(path) for path in pdf_pages],
        "pdf_pages_contact_sheet": str(pdf_contact),
    }
    (REVIEW / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(index, indent=2))


if __name__ == "__main__":
    main()
