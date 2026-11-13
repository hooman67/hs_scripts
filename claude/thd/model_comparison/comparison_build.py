#!/usr/bin/env python3
"""Build the model-comparison deliverables from gen_compare/<model>/<shot>/<shot>.mp4:
 - stitch each model's 11 shots into one video (target narrative order)
 - a per-model gallery (same shot tabs) for sd25(720p) / sd20 / h3
 - a SIDE-BY-SIDE gallery (per shot: the 3 models next to each other; 3 stitches on top)
Uploads each to its own S3 prefix. Run after all 33 gens exist."""
import os, json, subprocess, html, shutil
GC="/home/colligo/THD_laundry_sink_storyboard/gen_compare"
OUT="/home/colligo/THD_laundry_sink_storyboard/compare_out"
MODELS=[("sd25","Seedance 2.5 (720p)"),("sd20","Seedance 2.0 (720p)"),("h3","MiniMax H3 (768P)")]
SHOTS=[  # (shot_id, tab label)
 ("S01","Shot 1 · Establishing hero"),("S02_1A","Shot 2 · Couple assembling"),
 ("S03_3A","Shot 3 · CLICKREADY connector"),("S04_opp","Shot 4 · Opposite side"),
 ("S05_perp","Shot 5 · Perpendicular side"),("S06_box","Shot 6 · Box push-sides"),
 ("S07_boxfin","Shot 7 · Box finalize (zoom)"),("S08_4A","Shot 8 · Stand cabinet up"),
 ("S09_4B","Shot 9 · Place sink basin"),("S10_8A","Shot 10 · Turn on faucet"),
 ("S11_8B","Shot 11 · Hero / couple"),]
os.makedirs(OUT,exist_ok=True)

def vid(m,s): return f"{GC}/{m}/{s}/{s}.mp4"

def stitch(m):
    ins=[vid(m,s) for s,_ in SHOTS if os.path.exists(vid(m,s))]
    outp=f"{OUT}/stitch_{m}.mp4"
    cmd=["ffmpeg","-nostdin","-y","-loglevel","error"]
    for p in ins: cmd+=["-i",p]
    n=len(ins)
    fc="".join(f"[{i}:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v{i}];" for i in range(n))
    fc+="".join(f"[v{i}]" for i in range(n))+f"concat=n={n}:v=1:a=0[o]"
    cmd+=["-filter_complex",fc,"-map","[o]","-c:v","libx264","-pix_fmt","yuv420p","-crf","20",outp]
    subprocess.run(cmd,check=True); return outp,n

CSS_PATH="/home/colligo/THD_laundry_sink_storyboard/gallery/build_gallery.py"  # reuse look via manifest+builder

def esc(s): return html.escape(s or "")

def build_side_by_side(assetdir):
    """returns HTML for the side-by-side page"""
    css="""*{box-sizing:border-box}body{margin:0;background:#0b0d10;color:#e6e6e6;font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif}
.wrap{max-width:1500px;margin:0 auto;padding:22px}h1{font-size:24px;margin:0 0 4px}.sub{color:#9aa4af;margin:0 0 18px}
.row{margin:26px 0;border-top:1px solid #232a31;padding-top:14px}.row h2{font-size:16px;margin:0 0 10px}
.cols{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}
.col h3{font-size:12px;color:#9fd0a0;margin:0 0 6px;letter-spacing:.4px}
video{width:100%;border-radius:8px;background:#000;border:1px solid #232a31}
.loading-screen{padding:48px;text-align:center;color:#9aa4af}.hidden{display:none}
#ims{padding:8px 12px;background:#0d1216;border-bottom:1px solid #232a31;font-size:12px;color:#9aa4af}"""
    def cell(m,s,mp4):
        return f'<div class="col"><h3>{esc(dict(MODELS)[m])}</h3>'+(f'<video controls preload="metadata" src="assets/{mp4}"></video>' if mp4 else '<div class="loading-screen">—</div>')+'</div>'
    rows=[]
    # top: the three stitches
    st="".join(cell(m,"stitch",f"stitch_{m}.mp4" if os.path.exists(f"{OUT}/stitch_{m}.mp4") else None) for m,_ in MODELS)
    rows.append(f'<div class="row"><h2>★ FINAL STITCH — full narrative, each model</h2><div class="cols">{st}</div></div>')
    for s,lbl in SHOTS:
        cols="".join(cell(m,s,f"{m}_{s}.mp4" if os.path.exists(f"{assetdir}/{m}_{s}.mp4") else None) for m,_ in MODELS)
        rows.append(f'<div class="row"><h2>{esc(lbl)}</h2><div class="cols">{cols}</div></div>')
    body=f'<div class="wrap"><h1>Model comparison — Seedance 2.5 vs 2.0 vs MiniMax H3</h1><p class="sub">Same customer storyboard inputs, best-effort prep per model, ~720p. Laundry-sink narrative, shots 1–11.</p>'+"".join(rows)+'</div>'
    scripts=('<script src="https://auth-stg1.services.adobe.com/imslib/imslib.js"></script><script src="./imsauth.js"></script>'
     '<script>function onAuthReady(){}document.addEventListener("DOMContentLoaded",function(){try{initializeIMS();}catch(e){}'
     'setTimeout(function(){var c=document.getElementById("content"),l=document.getElementById("loading");if(c&&c.classList.contains("hidden")){c.classList.remove("hidden");if(l)l.style.display="none";}},9000);});</script>')
    return (f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
      f'<title>Model comparison</title><style>{css}</style></head><body><div id="ims"></div>'
      f'<div id="loading" class="loading-screen">Loading…</div><div id="content" class="hidden">{body}</div>{scripts}</body></html>')

if __name__=="__main__":
    # 1) stitches
    for m,_ in MODELS:
        try: p,n=stitch(m); print("stitched",m,n,"shots")
        except Exception as e: print("stitch FAIL",m,e)
    # 2) side-by-side assets: copy each shot video per model into a flat assets dir
    sbs=f"{OUT}/sidebyside/assets"; os.makedirs(sbs,exist_ok=True)
    for m,_ in MODELS:
        for s,_ in SHOTS:
            v=vid(m,s)
            if os.path.exists(v): shutil.copy(v, f"{sbs}/{m}_{s}.mp4")
        st=f"{OUT}/stitch_{m}.mp4"
        if os.path.exists(st): shutil.copy(st, f"{sbs}/stitch_{m}.mp4")
    open(f"{OUT}/sidebyside/index.html","w").write(build_side_by_side(sbs))
    shutil.copy("/home/colligo/THD_laundry_sink_storyboard/gallery/imsauth.js", f"{OUT}/sidebyside/imsauth.js")
    print("built side-by-side ->", f"{OUT}/sidebyside/index.html")
