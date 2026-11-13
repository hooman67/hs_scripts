#!/usr/bin/env python3
"""Deterministic SIFT/RANSAC diagnostics and comparison contact sheets for position smoke runs."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

PROJECT=Path('/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment')

def analyze(root: Path):
    rows=[]
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        p=d/'run/rows'/d.name
        if not (p/'ours.png').exists(): continue
        result=json.loads((p/'result.json').read_text())
        x0,y0,x1,y1=result['guide_info']['product_bounds_px']
        src=cv2.imread(str(p/'geometry_guide.png'),cv2.IMREAD_GRAYSCALE)
        dst=cv2.imread(str(p/'ours.png'),cv2.IMREAD_GRAYSCALE)
        mask=np.zeros_like(src);mask[y0:y1,x0:x1]=255
        sift=cv2.SIFT_create()
        k1,d1=sift.detectAndCompute(src,mask);k2,d2=sift.detectAndCompute(dst,None)
        pairs=cv2.BFMatcher().knnMatch(d1,d2,k=2)
        good=[a for a,b in pairs if a.distance < .65*b.distance]
        q=np.float32([k1[m.queryIdx].pt for m in good]);t=np.float32([k2[m.trainIdx].pt for m in good])
        cv2.setRNGSeed(42)
        M,inliers=cv2.estimateAffinePartial2D(q,t,method=cv2.RANSAC,ransacReprojThreshold=3.6,
                                              maxIters=2000,confidence=.99,refineIters=10)
        scale=float(math.hypot(M[0,0],M[1,0]));rotation=float(math.degrees(math.atan2(M[1,0],M[0,0])))
        rows.append({'slug':d.name,'density_class':result.get('guide_density_class'),'matches':len(good),
                     'inliers':int(inliers.sum()),'scale':scale,'rotation_deg':rotation,
                     'translation_x_px':float(M[0,2]),'translation_y_px':float(M[1,2]),
                     'bounds':result['guide_info']['product_bounds_px']})
    return rows

def write(root, rows):
    (root/'affine_metrics.json').write_text(json.dumps(rows,indent=2))
    lines=[]
    for r in rows:
        lines.append(f"{r['slug']} class {r['density_class']} matches {r['matches']} inliers {r['inliers']} "
                     f"scale {r['scale']:.4f} rotation {r['rotation_deg']:.3f} "
                     f"tx {r['translation_x_px']:.1f} ty {r['translation_y_px']:.1f}")
    (root/'affine_metrics.txt').write_text('\n'.join(lines)+'\n')

def contact(base_slug, versions):
    modes=[mode for mode in ('retained_control','relocation_demand')
           if (versions[-1][1]/f'{base_slug}__{mode}').exists()]
    cell=(720,540); head=42
    sheet=Image.new('RGB',(cell[0]*len(versions), (cell[1]+head)*len(modes)), 'white');draw=ImageDraw.Draw(sheet);font=ImageFont.load_default(size=18)
    for row,mode in enumerate(modes):
        for col,(label,root) in enumerate(versions):
            d=root/f'{base_slug}__{mode}'; p=d/'run/rows'/d.name
            f=p/('geometry_guide.png' if label=='guide' else 'ours.png')
            im=Image.open(f).convert('RGB');im.thumbnail(cell)
            x=col*cell[0]+(cell[0]-im.width)//2;y=row*(cell[1]+head)+head+(cell[1]-im.height)//2
            sheet.paste(im,(x,y));draw.text((col*cell[0]+8,row*(cell[1]+head)+8),f'{mode} | {label}',font=font,fill='black')
    return sheet

def main():
    ap=argparse.ArgumentParser();ap.add_argument('versions',nargs='+');args=ap.parse_args()
    roots=[]
    for v in args.versions:
        root=PROJECT/'smoke'/v;rows=analyze(root);write(root,rows);roots.append((v,root))
    if len(roots)>=2:
        latest=roots[-1][1]
        bases=['cashmere__laptop_FrontCloseUp__p1','cashmere__laptop_FrontWide__p1','magic__printer_FrontCloseUp__p1','magic__printer_FrontWide__p1']
        for b in bases:
            # v22 guide is byte-identical for every version.
            guide_root=roots[0][1]
            contact(b,[('guide',guide_root),*roots]).save(latest/f'{b}_comparison_contact.jpg',quality=92)

if __name__=='__main__': main()
