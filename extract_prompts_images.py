#!/usr/bin/env python3
import argparse
import csv
import os
import re
import sys
from typing import Dict, List, Optional, Tuple

from docx import Document  # type: ignore


PROMPT_PATTERN = re.compile(r"^\s*Prompt\s*:\s*(.*)$", re.IGNORECASE)


def safe_makedirs(path: str) -> None:
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


def guess_extension_from_content_type(content_type: str) -> str:
    mapping = {
        "image/jpeg": "jpg",
        "image/png": "png",
        "image/gif": "gif",
        "image/bmp": "bmp",
        "image/tiff": "tiff",
        "image/webp": "webp",
        "image/x-emf": "emf",
        "image/x-wmf": "wmf",
        "image/x-pcx": "pcx",
    }
    return mapping.get(content_type.lower(), "bin")


def iter_paragraph_images(document: Document, paragraph) -> List[Tuple[bytes, str]]:
    """
    Extract raw image blobs referenced within a paragraph (in order).
    Returns a list of tuples (blob, extension).
    """
    images: List[Tuple[bytes, str]] = []
    for run in paragraph.runs:
        # Find all blips (image references) within the run
        blips = run._element.xpath('.//a:blip')
        for blip in blips:
            rel_id = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
            if not rel_id:
                # Some images may be linked (r:link), ignore for now
                rel_id = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}link')
            if not rel_id:
                continue
            try:
                image_part = document.part.related_parts[rel_id]
            except KeyError:
                continue
            blob = image_part.blob
            content_type = getattr(image_part, 'content_type', 'application/octet-stream')
            ext = guess_extension_from_content_type(content_type)
            images.append((blob, ext))
    return images


def extract_prompts_and_images(docx_path: str, output_dir: str) -> str:
    document = Document(docx_path)

    csv_path = os.path.join(output_dir, 'prompts.csv')
    images_dir = os.path.join(output_dir, 'images')
    safe_makedirs(images_dir)

    prompts: List[str] = []
    per_prompt_image_count: Dict[int, int] = {}
    current_prompt_index: Optional[int] = None

    # Iterate through all paragraphs preserving document order
    for paragraph in document.paragraphs:
        text = paragraph.text or ""
        m = PROMPT_PATTERN.match(text)
        if m:
            prompt_text = m.group(1).strip()
            prompts.append(prompt_text)
            current_prompt_index = len(prompts)  # 1-based row index
            per_prompt_image_count.setdefault(current_prompt_index, 0)
            # Continue to next iteration to also capture any images within this Prompt paragraph
        # Save any images found in this paragraph and associate to the latest prompt (if any)
        images = iter_paragraph_images(document, paragraph)
        if images and current_prompt_index is not None:
            for blob, ext in images:
                per_prompt_image_count[current_prompt_index] += 1
                count = per_prompt_image_count[current_prompt_index]
                # If only one image for prompt, use plain index; if multiple, suffix with _n
                if count == 1:
                    filename = f"{current_prompt_index}.{ext}"
                else:
                    filename = f"{current_prompt_index}_{count}.{ext}"
                out_path = os.path.join(images_dir, filename)
                with open(out_path, 'wb') as f:
                    f.write(blob)

    # Write CSV with header 'prompts'
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["prompts"])  # header
        for prompt in prompts:
            writer.writerow([prompt])

    return csv_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract prompts and images from a DOCX file.")
    parser.add_argument('--docx', required=True, help='Path to input .docx file')
    parser.add_argument('--outdir', required=True, help='Directory to write prompts.csv and images/')
    args = parser.parse_args()

    docx_path = os.path.abspath(args.docx)
    out_dir = os.path.abspath(args.outdir)
    safe_makedirs(out_dir)

    if not os.path.isfile(docx_path):
        print(f"Input file not found: {docx_path}", file=sys.stderr)
        sys.exit(1)

    csv_path = extract_prompts_and_images(docx_path, out_dir)
    print(f"Wrote CSV: {csv_path}")
    print(f"Images directory: {os.path.join(out_dir, 'images')}")


if __name__ == '__main__':
    main()


