#!/usr/bin/env python3
"""nano-banana-pro/edit helper for FFDY-7304 (image prep for person beats).

Two ops we need for the laundry-sink person beats:
  swap_couple(src, out) : replace the REAL shoot talent with our invented consistent couple
                          (couple_bible.md) — makes an R3-safe synthetic reference we control.
  paint_out(src, out)   : remove the people entirely -> person-free scene plate (fallback route:
                          generate the couple from text on top of a clean plate).

Usage: python3 nano.py swap  images/image8.jpeg  <media>/prep/1A_couple.png
       python3 nano.py paint images/image8.jpeg  <media>/prep/1A_plate.png
"""
import os, sys, time, urllib.request
sys.path.insert(0, os.path.expanduser("~/.claude/scripts"))
import seedance_video as sv

NANO = "fal-ai/nano-banana-pro/edit"
IMAGES = "/home/colligo/THD_laundry_sink_storyboard/images"

COUPLE = (
 "a woman in her early 30s with warm light skin and shoulder-length straight dark-brown hair, wearing a "
 "plain oatmeal cream crew-neck knit sweater and slim mid-blue jeans, and a man in his early 50s with "
 "light skin, short neat salt-and-pepper grey hair, clean-shaven, wearing a plain light-blue short-sleeve "
 "polo shirt and medium-blue jeans")


def key():
    return sv.resolve_key(key_file=os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"))


def resolve(p):
    return p if os.path.isabs(p) else os.path.join(IMAGES, p)


def _edit(src, prompt, out_path, tries=4):
    k = key(); last = None
    for a in range(tries):
        try:
            url = sv.upload(k, resolve(src))
            code, body = sv._req(k, sv.QUEUE + NANO, {"prompt": prompt, "image_urls": [url],
                                                      "num_images": 1, "resolution": "2K"})
            if code not in (200, 201, 202):
                raise RuntimeError(f"submit {code}: {str(body)[:200]}")
            surl, rurl = body["status_url"], body["response_url"]; t = time.time()
            while time.time() - t < 300:
                time.sleep(5); _, sb = sv._req(k, surl)
                if sb.get("status") == "COMPLETED": break
                if sb.get("status") in ("FAILED", "ERROR"): raise RuntimeError(f"failed {sb}")
            _, rb = sv._req(k, rurl); imgs = rb.get("images") or []
            if not imgs: raise RuntimeError(f"no image {str(rb)[:200]}")
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with urllib.request.urlopen(imgs[0]["url"], timeout=180) as r, open(out_path, "wb") as f:
                f.write(r.read())
            print("wrote", out_path); return out_path
        except Exception as e:
            last = e; print(f"  nano retry {a+1}/{tries}: {str(e)[:120]}", flush=True); time.sleep(8)
    raise last


def swap_couple(src, out_path):
    return _edit(src,
        "Edit this photo. Replace the two people with " + COUPLE + ". Keep their body positions, poses, "
        "hands and the assembly action EXACTLY the same, and keep the whole background, cabinet parts, "
        "sink, floor and room identical. Natural, photoreal people; plain clothing with no text or logos. "
        "Only change who the people are — everything else stays the same.", out_path)


def paint_out(src, out_path):
    return _edit(src,
        "Remove the people entirely (all faces, bodies, arms and hands) from this photo and fill the "
        "vacated area with the plausible continuation of the laundry room and the cabinet/sink parts "
        "behind them. Keep the room, cabinet, sink, floor and background exactly as they are. Photoreal, "
        "no people, no text, no logos.", out_path)


if __name__ == "__main__":
    op, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
    (swap_couple if op == "swap" else paint_out)(src, out)
