#!/usr/bin/env python3
"""
Build data.js for the Sprite HTML gallery.

Groups files by a human-readable folder label. Paths point to the JPEG thumbnails
in html_gallery/ relative to the gallery's index.html (which sits in
html_gallery/gallery/).
"""
import json
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "sprite_image_manifest.json")
OUT = os.path.join(ROOT, "sprite_gallery", "data.js")


def folder_label(dam_path: str) -> str:
    """Map a DAM asset path to a gallery group label."""
    rel = dam_path.replace("/content/dam/tccc/", "")
    parts = rel.split("/")
    # parts[0] = products|marketing
    if parts[0] == "products" and len(parts) >= 3:
        country = parts[1].upper()
        brand = parts[2]
        return f"products / {country} / {brand}"
    if parts[0] == "marketing" and len(parts) >= 3:
        # /marketing/sprite/<campaign>/...
        if parts[1] in ("sprite", "sprite-zero-diet-light", "absolut-vodka---sprite"):
            campaign = parts[2] if len(parts) >= 3 else parts[1]
            return f"marketing / {parts[1]} / {campaign}"
        return f"marketing / {parts[1]}"
    return parts[0] if parts else "(root)"


def thumb_path(dam_path: str) -> str:
    """Path of the JPEG thumb relative to html_gallery/ (i.e., '../html_gallery/' from gallery/)."""
    rel = dam_path.replace("/content/dam/", "")  # e.g. tccc/products/us/sprite/.../foo.png
    base, _ = os.path.splitext(rel)
    return base + ".jpg"


def main():
    manifest = json.load(open(MANIFEST))
    grouped = defaultdict(list)
    for a in manifest:
        label = folder_label(a["damPath"])
        # `p` is path relative to the prefix the gallery sits in (html_gallery/).
        # gallery/index.html → ../<thumb_path>  → s3://bucket/.../html_gallery/<thumb_path>
        grouped[label].append({
            "n": a["name"],
            "s": int(a.get("size", 0) or 0),
            "p": thumb_path(a["damPath"]),
        })
    # Sort each group's items by name
    for k in grouped:
        grouped[k].sort(key=lambda x: x["n"].lower())
    # Sort groups by label
    out = {k: grouped[k] for k in sorted(grouped.keys())}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        f.write("const GALLERY_DATA = ")
        json.dump(out, f, separators=(",", ":"))
        f.write(";\n")
    n = sum(len(v) for v in out.values())
    print(f"Wrote {OUT}: {len(out)} groups, {n} items")


if __name__ == "__main__":
    main()
