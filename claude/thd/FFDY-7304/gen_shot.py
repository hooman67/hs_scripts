#!/usr/bin/env python3
"""Storyboard-driven shot generator (stills -> video).

The laundry-sink deck gives us STILLS, not a source video, so we can't use rewriter_pipeline's
frame-extraction path. This driver takes a small per-shot JSON and calls Seedance directly:
  - mode "i2v" : one still as the first frame + a motion prompt (best for product macros)
  - mode "ref" : ordered still keyframes (@Image1..N) + prompt
Face-free product macros need no R3 handling; person beats will pre-process the still (cover_body /
paint-out) before landing here.

Config schema (see shots/*.json):
  { id, mode, images:[<file in the media images dir OR abs path>], prompt, duration, resolution,
    end_image? }

Usage: python3 gen_shot.py shots/3A_click_v1.json
"""
import os, sys, json
sys.path.insert(0, os.path.expanduser("~/.claude/scripts"))
import seedance_video as sv

MEDIA_IMAGES = "/home/colligo/THD_laundry_sink_storyboard/images"
GEN_DIR      = "/home/colligo/THD_laundry_sink_storyboard/gen"   # videos stay out of git


def resolve(p):
    return p if os.path.isabs(p) else os.path.join(MEDIA_IMAGES, p)


def run(cfg_path):
    cfg = json.load(open(cfg_path))
    key = sv.resolve_key(key_file=os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"))
    imgs = [resolve(p) for p in cfg.get("images", [])]
    out = os.path.join(GEN_DIR, cfg["id"])
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "prompt.txt"), "w").write(cfg["prompt"])
    end_img = resolve(cfg["end_image"]) if cfg.get("end_image") else None
    print(f"[{cfg['id']}] mode={cfg['mode']} dur={cfg.get('duration','4')} imgs={[os.path.basename(i) for i in imgs]}")
    res = sv.generate(key, name=cfg["id"], mode=cfg["mode"], prompt=cfg["prompt"],
                      out_dir=out, images=imgs, duration=str(cfg.get("duration", "4")),
                      resolution=cfg.get("resolution", "1080p"), audio=False,
                      aspect=cfg.get("aspect", "16:9"), end_image=end_img,
                      on_status=lambda st, s: print(f"  {st} ({s}s)", flush=True))
    print("RESULT:", res)
    return res


if __name__ == "__main__":
    run(sys.argv[1])
