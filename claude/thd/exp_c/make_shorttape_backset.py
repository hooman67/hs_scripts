#!/usr/bin/env python3
"""Exp C: add a SHORT tape measuring the backset (door edge -> knob center) to the paint plate."""
import os, sys, time, json, urllib.request
sys.path.insert(0, os.path.expanduser("~/.claude/scripts"))
import seedance_video as sv

KEY = sv.resolve_key(key_file=os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"))
MODEL = "fal-ai/nano-banana-pro/edit"
OUT = "/home/colligo/THD_How_to_Install_a_Door_Lock/work/plates"
SRC = os.path.join(OUT, sys.argv[2] if len(sys.argv) > 2 else "plate_paint_article.png")
DST = os.path.join(OUT, sys.argv[1] if len(sys.argv) > 1 else "plate_shorttape_backset.png")

PROMPT = os.environ.get("PROMPT") or (
    "Add a person's hand holding a yellow tape measure to measure the door-lock BACKSET. "
    "The metal hook catches on the vertical edge of the door right beside the latch, and the "
    "yellow blade extends only a SHORT distance, about two inches, horizontally to the centre of "
    "the stainless door knob. The tape's yellow-and-black case rests in the hand right at the knob. "
    "The tape is SHORT - the blade does NOT extend beyond the knob and does not run across the glass "
    "panel. Keep the white door, the stainless deadbolt, the knob, the frosted glass panel with "
    "blinds, the plant, the walls and the lighting exactly the same. Photoreal how-to footage, "
    "plain denim sleeve with no text or logo.")

def main():
    url = sv.upload(KEY, SRC)
    payload = {"prompt": PROMPT, "image_urls": [url], "num_images": 1, "resolution": "2K"}
    code, body = sv._req(KEY, sv.QUEUE + MODEL, payload)
    if code not in (200, 201, 202):
        print("submit", code, str(body)[:300]); return
    surl, rurl = body["status_url"], body["response_url"]
    t = time.time()
    while time.time() - t < 300:
        time.sleep(5)
        sc, sb = sv._req(KEY, surl); st = sb.get("status")
        print("  ", st, round(time.time()-t), "s", flush=True)
        if st == "COMPLETED": break
        if st in ("FAILED", "ERROR"): print("FAILED", str(sb)[:200]); return
    rc, rb = sv._req(KEY, rurl)
    imgs = rb.get("images") or []
    if not imgs: print("no image", str(rb)[:250]); return
    with urllib.request.urlopen(imgs[0]["url"], timeout=180) as r, open(DST, "wb") as f:
        f.write(r.read())
    json.dump({"src": SRC, "model": MODEL, "prompt": PROMPT, "response": rb},
              open(DST.replace(".png", ".json"), "w"), indent=1)
    print("ok ->", DST)

if __name__ == "__main__":
    main()
