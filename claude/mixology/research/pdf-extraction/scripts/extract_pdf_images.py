"""Extract native PDF image streams and restore their soft masks losslessly."""
from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
from collections import defaultdict
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw, ImageFont


PDF = Path("/mnt/localssd/mixology/260605_Mixology_AI_Art_Direction_Process.pdf")
OUT = Path("/mnt/localssd/mixology/extracted_from_pdf")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_link(source: Path, destination: Path) -> None:
    try:
        os.link(source, destination)
    except OSError:
        shutil.copy2(source, destination)


def image_extension(ext: str) -> str:
    return ".jpg" if ext.lower() in {"jpg", "jpeg"} else f".{ext.lower()}"


def main() -> None:
    if not PDF.is_file():
        raise SystemExit(f"PDF not found: {PDF}")
    if OUT.exists():
        raise SystemExit(f"Refusing to overwrite existing extraction: {OUT}")

    os.umask(0o022)
    native_dir = OUT / "native_original_streams"
    rgba_dir = OUT / "png_with_transparency"
    placement_dir = OUT / "all_page_placements"
    review_dir = OUT / "_review"
    for directory in (native_dir, rgba_dir, placement_dir, review_dir):
        directory.mkdir(parents=True)

    doc = pymupdf.open(PDF)
    first_seen: dict[int, tuple[int, int]] = {}
    image_info: dict[int, tuple] = {}
    placements: list[dict] = []
    placement_counts: dict[int, int] = defaultdict(int)

    for page_index, page in enumerate(doc):
        page_number = page_index + 1
        images = page.get_images(full=True)
        for page_image_number, item in enumerate(images, start=1):
            xref, smask, width, height, bpc, colorspace, alt, name, pdf_filter, referencer = item
            first_seen.setdefault(xref, (page_number, page_image_number))
            image_info.setdefault(xref, item)
            placement_counts[xref] += 1
            placements.append(
                {
                    "page": page_number,
                    "page_image_number": page_image_number,
                    "xref": xref,
                    "smask_xref": smask,
                    "width": width,
                    "height": height,
                    "bits_per_component": bpc,
                    "colorspace": colorspace,
                    "pdf_filter": pdf_filter,
                    "pdf_resource_name": name,
                }
            )

    unique_records: list[dict] = []
    output_by_xref: dict[int, Path] = {}
    for sequence, xref in enumerate(sorted(image_info, key=lambda value: first_seen[value]), start=1):
        item = image_info[xref]
        smask, width, height, bpc, colorspace, name, pdf_filter = (
            item[1], item[2], item[3], item[4], item[5], item[7], item[8]
        )
        first_page, first_page_image = first_seen[xref]
        stem = f"image_{sequence:03d}_p{first_page:02d}_xref{xref}"

        extracted = doc.extract_image(xref)
        native_path = native_dir / f"{stem}{image_extension(extracted['ext'])}"
        native_path.write_bytes(extracted["image"])

        base = pymupdf.Pixmap(doc, xref)
        if base.colorspace is None:
            raise RuntimeError(f"Image xref {xref} has no colorspace")
        if base.n - base.alpha > 3:
            base = pymupdf.Pixmap(pymupdf.csRGB, base)
        alpha_restored = bool(smask)
        if smask:
            mask = pymupdf.Pixmap(doc, smask)
            if mask.width != base.width or mask.height != base.height:
                raise RuntimeError(
                    f"Mask dimensions differ for xref {xref}: "
                    f"image={base.width}x{base.height}, mask={mask.width}x{mask.height}"
                )
            composed = pymupdf.Pixmap(base, mask)
        else:
            composed = base
        rgba_path = rgba_dir / f"{stem}.png"
        composed.save(rgba_path)
        output_by_xref[xref] = rgba_path

        with Image.open(rgba_path) as check:
            check.load()
            png_mode = check.mode
            alpha_extrema = check.getchannel("A").getextrema() if "A" in check.getbands() else None

        unique_records.append(
            {
                "sequence": sequence,
                "xref": xref,
                "smask_xref": smask,
                "first_page": first_page,
                "first_page_image_number": first_page_image,
                "placement_count": placement_counts[xref],
                "width": width,
                "height": height,
                "bits_per_component": bpc,
                "colorspace": colorspace,
                "pdf_filter": pdf_filter,
                "native_file": str(native_path.relative_to(OUT)),
                "native_format": extracted["ext"],
                "native_bytes": native_path.stat().st_size,
                "native_sha256": sha256(native_path),
                "png_file": str(rgba_path.relative_to(OUT)),
                "png_mode": png_mode,
                "png_bytes": rgba_path.stat().st_size,
                "png_sha256": sha256(rgba_path),
                "alpha_restored": alpha_restored,
                "alpha_extrema": list(alpha_extrema) if alpha_extrema else None,
            }
        )

    # Materialize one full-resolution PNG for every page image placement. Reused
    # objects are hard-linked where possible, so their page order remains obvious
    # without needless storage duplication.
    for placement in placements:
        xref = placement["xref"]
        filename = (
            f"page_{placement['page']:02d}_image_{placement['page_image_number']:02d}"
            f"_xref{xref}.png"
        )
        destination = placement_dir / filename
        safe_link(output_by_xref[xref], destination)
        placement["file"] = str(destination.relative_to(OUT))
        placement["sha256"] = sha256(destination)

    with (OUT / "unique_images.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=unique_records[0].keys())
        writer.writeheader()
        writer.writerows(unique_records)
    with (OUT / "placements.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=placements[0].keys())
        writer.writeheader()
        writer.writerows(placements)

    manifest = {
        "source_pdf": str(PDF),
        "source_pdf_sha256": sha256(PDF),
        "page_count": doc.page_count,
        "unique_image_count": len(unique_records),
        "page_placement_count": len(placements),
        "method": (
            "Native image streams extracted without transcoding; PDF soft masks "
            "restored into full-resolution RGBA PNGs. Reused page placements are "
            "materialized as hard links when supported."
        ),
        "unique_images": unique_records,
        "placements": placements,
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    # Derived contact sheet is explicitly isolated from the extracted deliverables.
    thumbs: list[tuple[Image.Image, str]] = []
    for record in unique_records:
        path = OUT / record["png_file"]
        with Image.open(path) as image:
            preview = Image.new("RGB", image.size, "white")
            if "A" in image.getbands():
                preview.paste(image.convert("RGBA"), mask=image.getchannel("A"))
            else:
                preview.paste(image.convert("RGB"))
            preview.thumbnail((300, 220), Image.Resampling.LANCZOS)
            thumbs.append((preview.copy(), f"{record['sequence']:03d}  p{record['first_page']:02d}  {record['width']}×{record['height']}"))
    cols = 4
    cell_w, cell_h = 330, 270
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "#eeeeee")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for index, (preview, label) in enumerate(thumbs):
        x = (index % cols) * cell_w
        y = (index // cols) * cell_h
        px = x + (cell_w - preview.width) // 2
        py = y + 8 + (220 - preview.height) // 2
        sheet.paste(preview, (px, py))
        draw.text((x + 12, y + 238), label, fill="black", font=font)
    sheet.save(review_dir / "contact_sheet_unique_images.jpg", quality=92, subsampling=0)

    readme = f"""# PDF image extraction

Source: `{PDF}`

- Pages: {doc.page_count}
- Distinct embedded image objects: {len(unique_records)}
- Image placements across all pages: {len(placements)}

`native_original_streams/` contains the original compressed image streams with no transcoding.
`png_with_transparency/` contains full-resolution PNGs with each PDF soft mask restored.
`all_page_placements/` contains one restored PNG per page placement, including repeated uses.
`manifest.json`, `unique_images.csv`, and `placements.csv` record provenance, dimensions, hashes, and reuse.
`_review/contact_sheet_unique_images.jpg` is a derived review aid and is not an extracted source image.
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")
    print(json.dumps({key: manifest[key] for key in ("page_count", "unique_image_count", "page_placement_count")}, indent=2))


if __name__ == "__main__":
    main()
