#!/usr/bin/env python3
"""Per-model review galleries (sd25 720p / sd20 / h3), same tab structure as the 2.5 gallery.
Reuses gallery/build_gallery.py verbatim by writing a manifest.json into each model's dir."""
import os, json, shutil, subprocess
ROOT="/home/colligo/hs_scripts/claude/thd/model_comparison"
GC="/home/colligo/THD_laundry_sink_storyboard/gen_compare"
CO="/home/colligo/THD_laundry_sink_storyboard/compare_out"
SRCGAL="/home/colligo/THD_laundry_sink_storyboard/gallery"
SHOTCFG=f"{ROOT}/shots"
MODELS={"sd25":"Seedance 2.5 (720p)","sd20":"Seedance 2.0 (720p)","h3":"MiniMax Hailuo 3 (768P)"}
ORDER=[("S01","Shot 1 · Establishing hero"),("S02_1A","Shot 2 · Couple assembling the cabinet"),
 ("S03_3A","Shot 3 · CLICKREADY connector (macro)"),("S04_opp","Shot 4 · Opposite side connected"),
 ("S05_perp","Shot 5 · Perpendicular side / box takes shape"),("S06_box","Shot 6 · Box completion — push sides together"),
 ("S07_boxfin","Shot 7 · Box finalize (zoom-in)"),("S08_4A","Shot 8 · Standing the cabinet up"),
 ("S09_4B","Shot 9 · Placing the sink basin"),("S10_8A","Shot 10 · Turning on the faucet"),
 ("S11_8B","Shot 11 · Hero / couple admiring")]

# index configs by (id, model)
cfgs={}
for fn in os.listdir(SHOTCFG):
    if fn.endswith(".json"):
        c=json.load(open(f"{SHOTCFG}/{fn}"))
        cfgs[(c["id"],c["model"])]=c

def build(model):
    gdir=f"{CO}/gallery_{model}"; adir=f"{gdir}/assets"
    os.makedirs(adir,exist_ok=True)
    secs=[]
    # FINAL STITCH
    stitch=f"{CO}/stitch_{model}.mp4"
    if os.path.exists(stitch):
        shutil.copy(stitch,f"{adir}/stitch.mp4")
        secs.append({"kind":"divider","id":"shot0000_stitch_divider",
            "label":f"0000 · FINAL STITCH — {MODELS[model]}",
            "note":"All 11 shots concatenated in narrative order (straight cuts, no VO/SUPERs). Same shot list and same customer storyboard inputs as the other two models; prompts tuned per model."})
        secs.append({"kind":"target","id":"final_stitch","label":f"Stitched cut — {MODELS[model]}",
            "note":"Watch for: couple consistency across the person shots (2,4,5,6,7,8,9,11), motion correctness, and overall coherence vs the other models.",
            "video":"assets/stitch.mp4"})
    for i,(sid,label) in enumerate(ORDER):
        c=cfgs.get((sid,model))
        v=f"{GC}/{model}/{sid}/{sid}.mp4"
        num=i+1
        secs.append({"kind":"divider","id":f"shot{num:04d}_div","label":label})
        # input references
        frames=[]
        if c:
            for j,ip in enumerate(c.get("images",[])):
                if os.path.exists(ip):
                    ext=os.path.splitext(ip)[1]; dst=f"{sid}_in{j}{ext}"
                    shutil.copy(ip,f"{adir}/{dst}"); frames.append(f"assets/{dst}")
        secs.append({"kind":"target","id":f"{sid}_input",
            "label":f"INPUT — reference image(s) passed to {MODELS[model]}",
            "note":f"mode: {c.get('mode') if c else '?'} · best-effort prep from the customer storyboard for this model.",
            "frames":frames})
        # result
        exp={"id":sid,"approach":f"{MODELS[model]} · {c.get('mode') if c else ''} · {c.get('resolution','') if c else ''}",
             "status":"ok" if os.path.exists(v) else "rejected"}
        if os.path.exists(v):
            shutil.copy(v,f"{adir}/{sid}.mp4"); exp["video"]=f"assets/{sid}.mp4"
        else:
            exp["error"]="no output"
        if c: exp["prompt"]=c.get("prompt","")
        secs.append({"kind":"round","id":f"{sid}_result","label":f"{MODELS[model]} — result","experiments":[exp]})
    manifest={"title":f"Laundry-sink spot — {MODELS[model]}",
        "subtitle":"Model comparison · same customer storyboard inputs, best-effort prep per model, ~720p · shots 1–11.",
        "sections":secs}
    json.dump(manifest,open(f"{gdir}/manifest.json","w"),indent=1)
    shutil.copy(f"{SRCGAL}/build_gallery.py",f"{gdir}/build_gallery.py")
    shutil.copy(f"{SRCGAL}/imsauth.js",f"{gdir}/imsauth.js")
    subprocess.run(["python3","build_gallery.py"],cwd=gdir,check=True)
    print("built",gdir)

if __name__=="__main__":
    for m in MODELS: build(m)
