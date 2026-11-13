#!/usr/bin/env python3
"""Extract the laundry-sink storyboard PPTX into reviewable assets.

Per the experiment's git rules:
  - TEXT / guidance  -> the repo dir (FFDY-7304/text/, git-tracked)
  - IMAGES (embedded slide photos) -> the media dir (NOT git)

python-pptx gives us shape geometry, so we recover reading order (top->bottom, left->right) and
pair each caption/text block with the photo it sits under on the same slide.

Usage: python3 extract_pptx.py
"""
import os, json, zipfile
from pptx import Presentation
from pptx.util import Emu

PPTX  = "/home/colligo/THD_laundry_sink_storyboard/Storyboard ClickReady 10_1_25 v2a-FINALBOARDS CLEAN.pptx"
REPO  = "/home/colligo/hs_scripts/claude/thd/FFDY-7304"
MEDIA = "/home/colligo/THD_laundry_sink_storyboard"

TXT_DIR  = os.path.join(REPO, "text")
IMGS_DIR = os.path.join(MEDIA, "images")
for d in (TXT_DIR, IMGS_DIR):
    os.makedirs(d, exist_ok=True)


def emu_in(v):
    return round(Emu(v).inches, 2) if v is not None else None


# --- 1) dump the embedded media straight from the zip (originals, full res) ---
zf = zipfile.ZipFile(PPTX)
media_map = {}   # ppt/media/imageN.ext -> saved filename
for n in sorted(zf.namelist()):
    if n.startswith("ppt/media/") and n.rsplit(".", 1)[-1].lower() in ("jpeg", "jpg", "png"):
        base = os.path.basename(n)
        out = os.path.join(IMGS_DIR, base)
        open(out, "wb").write(zf.read(n))
        media_map[base] = base

# --- 2) walk slides for text + picture geometry (to recover reading order + caption pairing) ---
prs = Presentation(PPTX)
combined = ["# Laundry-sink storyboard (PPTX) — extracted text (all slides)\n"]
index = []

for si, slide in enumerate(prs.slides, 1):
    texts, pics = [], []
    for sh in slide.shapes:
        geom = {"top": emu_in(sh.top), "left": emu_in(sh.left),
                "w": emu_in(sh.width), "h": emu_in(sh.height)}
        if sh.has_text_frame and sh.text_frame.text.strip():
            texts.append({**geom, "text": sh.text_frame.text.strip()})
        if sh.shape_type == 13 or sh.name.lower().startswith("picture"):  # 13 = PICTURE
            fn = None
            try:
                fn = os.path.basename(sh.image.filename or "") or f"slide{si}_pic"
                blob_name = sh.image.blob  # noqa (ensures it's a real picture)
            except Exception:
                fn = None
            pics.append({**geom, "name": sh.name, "media": fn})

    # reading order: top band then left
    texts.sort(key=lambda t: (round((t["top"] or 0) * 2) / 2, t["left"] or 0))
    body = "\n".join(t["text"] for t in texts)
    open(os.path.join(TXT_DIR, f"slide_{si:02d}.txt"), "w").write(body)
    combined.append(f"\n\n===== SLIDE {si:02d} =====\n{body or '(no text)'}")

    index.append({"slide": si, "n_text_blocks": len(texts), "n_pictures": len(pics),
                  "texts": texts, "pictures": pics})
    print(f"slide {si:02d}: {len(texts)} text blocks, {len(pics)} pictures")

open(os.path.join(REPO, "storyboard_text.md"), "w").write("".join(combined))
json.dump(index, open(os.path.join(REPO, "extract_index.json"), "w"), indent=1)
print(f"\nDONE. {len(prs.slides._sldIdLst)} slides, {len(media_map)} media images.")
print(f"text -> {TXT_DIR}, images -> {IMGS_DIR}")
