#!/usr/bin/env python3
"""Extract the Makita storyboard PDF: text/guidance -> repo (FFDY-7309/text), page renders + embedded
images -> media dir (THD_makita_storyboard). Reuses the FFDY-7304 approach."""
import os, json, pymupdf
PDF="/home/colligo/THD_makita_storyboard/Makita_Brand CPT_Storyboards_072425_THD Preread-1.pdf"
REPO="/home/colligo/hs_scripts/claude/thd/FFDY-7309"
MEDIA="/home/colligo/THD_makita_storyboard"
TXT=os.path.join(REPO,"text"); PAGES=os.path.join(MEDIA,"pages"); IMGS=os.path.join(MEDIA,"images")
for d in (TXT,PAGES,IMGS): os.makedirs(d,exist_ok=True)
doc=pymupdf.open(PDF); combined=[]; index=[]
for i,page in enumerate(doc):
    n=i+1; text=page.get_text("text").strip()
    open(os.path.join(TXT,f"page_{n:02d}.txt"),"w").write(text)
    combined.append(f"\n\n===== PAGE {n:02d} =====\n{text or '(no text)'}")
    page.get_pixmap(matrix=pymupdf.Matrix(2,2)).save(os.path.join(PAGES,f"page_{n:02d}.png"))
    imgs=[]
    for k,img in enumerate(page.get_images(full=True)):
        try: info=doc.extract_image(img[0])
        except: continue
        w,h=info.get("width"),info.get("height")
        if (w or 0)*(h or 0) < 200*200: continue
        fn=f"page_{n:02d}_img_{k+1:02d}.{info.get('ext','png')}"
        open(os.path.join(IMGS,fn),"wb").write(info["image"]); imgs.append(fn)
    index.append({"page":n,"text_chars":len(text),"n_images":len(imgs),"images":imgs})
    print(f"page {n:02d}: {len(text):4d} chars, {len(imgs)} imgs")
open(os.path.join(REPO,"storyboard_text.md"),"w").write("# Makita storyboard — extracted text\n"+"".join(combined))
json.dump(index,open(os.path.join(REPO,"extract_index.json"),"w"),indent=1)
print("DONE", len(doc),"pages")
