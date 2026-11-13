#!/usr/bin/env python3
"""Build one hi-res per-model gallery + stitch, same tabs as the 2.5 gallery.
Usage: build_hires_gallery.py <variant> <config_suffix> <gen_subdir> <title>
  e.g. build_hires_gallery.py sd20_1080 _sd20_1080 sd20_1080 "Seedance 2.0 (1080p)"
"""
import os, sys, json, shutil, subprocess
ROOT="/home/colligo/hs_scripts/claude/thd/model_comparison"
GC="/home/colligo/THD_laundry_sink_storyboard/gen_compare"
CO="/home/colligo/THD_laundry_sink_storyboard/compare_out"
SRCGAL="/home/colligo/THD_laundry_sink_storyboard/gallery"
SHOTCFG=f"{ROOT}/shots"
ORDER=[("S01","Shot 1 · Establishing hero"),("S02_1A","Shot 2 · Couple assembling the cabinet"),
 ("S03_3A","Shot 3 · CLICKREADY connector (macro)"),("S04_opp","Shot 4 · Opposite side connected"),
 ("S05_perp","Shot 5 · Perpendicular side / box takes shape"),("S06_box","Shot 6 · Box completion — push sides together"),
 ("S07_boxfin","Shot 7 · Box finalize (zoom-in)"),("S08_4A","Shot 8 · Standing the cabinet up"),
 ("S09_4B","Shot 9 · Placing the sink basin"),("S10_8A","Shot 10 · Turning on the faucet"),
 ("S11_8B","Shot 11 · Hero / couple admiring")]

def stitch(gensub, outp):
    ins=[f"{GC}/{gensub}/{s}/{s}.mp4" for s,_ in ORDER if os.path.exists(f"{GC}/{gensub}/{s}/{s}.mp4")]
    cmd=["ffmpeg","-nostdin","-y","-loglevel","error"]
    for p in ins: cmd+=["-i",p]
    n=len(ins)
    fc="".join(f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v{i}];" for i in range(n))
    fc+="".join(f"[v{i}]" for i in range(n))+f"concat=n={n}:v=1:a=0[o]"
    cmd+=["-filter_complex",fc,"-map","[o]","-c:v","libx264","-pix_fmt","yuv420p","-crf","18",outp]
    subprocess.run(cmd,check=True); return n

def build(variant, suffix, gensub, title):
    cfgs={}
    for fn in os.listdir(SHOTCFG):
        if fn.endswith(f"{suffix}.json"):
            c=json.load(open(f"{SHOTCFG}/{fn}")); cfgs[c["id"]]=c
    gdir=f"{CO}/gallery_{variant}"; adir=f"{gdir}/assets"; os.makedirs(adir,exist_ok=True)
    st=f"{CO}/stitch_{variant}.mp4"; n=stitch(gensub, st); shutil.copy(st,f"{adir}/stitch.mp4")
    secs=[{"kind":"divider","id":"shot0000_stitch_divider","label":f"0000 · FINAL STITCH — {title}",
        "note":f"All {n} shots concatenated in narrative order (straight cuts, no VO/SUPERs). Same customer storyboard inputs and same prompts as the matching lower-res run — only the resolution changed."},
      {"kind":"target","id":"final_stitch","label":f"Stitched cut — {title}",
        "note":"Watch for: couple consistency, motion correctness, and whether the higher resolution actually improves detail/sharpness vs the lower-res run.",
        "video":"assets/stitch.mp4"}]
    for i,(sid,label) in enumerate(ORDER):
        c=cfgs.get(sid); v=f"{GC}/{gensub}/{sid}/{sid}.mp4"; num=i+1
        secs.append({"kind":"divider","id":f"shot{num:04d}_div","label":label})
        frames=[]
        if c:
            for j,ip in enumerate(c.get("images",[])):
                if os.path.exists(ip):
                    ext=os.path.splitext(ip)[1]; dst=f"{sid}_in{j}{ext}"
                    shutil.copy(ip,f"{adir}/{dst}"); frames.append(f"assets/{dst}")
        secs.append({"kind":"target","id":f"{sid}_input",
            "label":f"INPUT — reference image(s) passed to {title}",
            "note":f"mode: {c.get('mode') if c else '?'} · resolution: {c.get('resolution') if c else '?'} · best-effort prep from the customer storyboard.",
            "frames":frames})
        exp={"id":sid,"approach":f"{title} · {c.get('mode') if c else ''} · {c.get('resolution','') if c else ''}",
             "status":"ok" if os.path.exists(v) else "rejected"}
        if os.path.exists(v): shutil.copy(v,f"{adir}/{sid}.mp4"); exp["video"]=f"assets/{sid}.mp4"
        else: exp["error"]="no output (still rendering or failed)"
        if c: exp["prompt"]=c.get("prompt","")
        secs.append({"kind":"round","id":f"{sid}_result","label":f"{title} — result","experiments":[exp]})
    manifest={"title":f"Laundry-sink spot — {title}",
        "subtitle":"Model comparison (higher-res) · same customer storyboard inputs, same prompts as the lower-res run · shots 1–11.",
        "sections":secs}
    json.dump(manifest,open(f"{gdir}/manifest.json","w"),indent=1)
    shutil.copy(f"{SRCGAL}/build_gallery.py",f"{gdir}/build_gallery.py")
    shutil.copy(f"{SRCGAL}/imsauth.js",f"{gdir}/imsauth.js")
    subprocess.run(["python3","build_gallery.py"],cwd=gdir,check=True)
    print("built",gdir,f"({n} shots)")

if __name__=="__main__":
    build(sys.argv[1],sys.argv[2],sys.argv[3]," ".join(sys.argv[4:]))
