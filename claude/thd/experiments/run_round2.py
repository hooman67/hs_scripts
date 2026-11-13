#!/usr/bin/env python3
"""Round 2 — person-free plates + corrected short-backset prompt. Prompts pulled from manifest."""
import os, sys, json, concurrent.futures as cf
sys.path.insert(0, os.path.expanduser("~/.claude/scripts"))
import seedance_video as sv

BASE = "/home/colligo/THD_How_to_Install_a_Door_Lock"
OUT = os.path.join(BASE, "work", "gen_round2")
PLATES = os.path.join(BASE, "work", "plates")
KEY = sv.resolve_key(key_file=os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"))

man = json.load(open(os.path.join(BASE, "gallery", "manifest.json")))
r2 = next(s for s in man["sections"] if s["id"] == "round2_inputs")
PROMPTS = {e["id"]: e["prompt"] for e in r2["experiments"]}

# id -> (mode, image path or None)
REFMAP = {
    "G1": ("ref", os.path.join(PLATES, "plate_paint_shot.png")),
    "G2": ("ref", os.path.join(PLATES, "plate_paint_article.png")),
    "G3": ("ref", os.path.join(PLATES, "plate_crop.jpg")),
    "G4": ("t2v", None),
}

def run(item):
    gid, (mode, img) = item
    return sv.generate(KEY, name=gid, mode=mode, prompt=PROMPTS[gid], out_dir=OUT,
                       images=[img] if img else [], duration="8", resolution="720p",
                       audio=False, aspect="16:9",
                       on_status=lambda st, s: print(f"    [{gid}] {st} ({s}s)", flush=True))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(f"key ...{KEY[-4:]}  ->  {OUT}", flush=True)
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        for name, status, secs, size in ex.map(run, REFMAP.items()):
            print(f"==> [{status[:44]:<44}] {name:<6} {secs:>4}s {size//1024:>7} KB", flush=True)
    print("DONE", flush=True)
