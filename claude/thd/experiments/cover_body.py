#!/usr/bin/env python3
"""Cover the person's head+torso (keep real arms/hands) — test on one beat, then all if good."""
import os, sys, time, json, urllib.request
sys.path.insert(0, os.path.expanduser("~/.claude/scripts"))
import seedance_video as sv
KEY = sv.resolve_key(key_file=os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"))
MODEL = "fal-ai/nano-banana-pro/edit"
OUT = "/home/colligo/THD_How_to_Install_a_Door_Lock/work/plates"

PROMPT = (
 "Edit this image. KEEP the man's arms, forearms, hands and the yellow tape measure EXACTLY as they "
 "are — identical pixels, the same natural length and position; do NOT stretch, lengthen, move or "
 "redraw the arms or hands. Replace ONLY his head, face, hair, neck and torso/upper body with the "
 "plain background that belongs behind him (white wall, window frame, and green plant). Also remove the "
 "orange round 'TIP' lightbulb graphic and the 'Some locks have an adjustable backset' caption text, "
 "replacing them with the plain door and wall behind. Keep the white door, the stainless steel deadbolt "
 "and knob, the door edge and latch, the frosted glass panel with blinds, the plant and the lighting "
 "unchanged. The result: natural forearms and hands holding the tape at the lock, with no head, face or "
 "torso and no on-screen graphics. Photoreal. No text, no logos.")

def edit(name, src):
    url = sv.upload(KEY, src)
    code, body = sv._req(KEY, sv.QUEUE + MODEL, {"prompt": PROMPT, "image_urls": [url],
                                                 "num_images": 1, "resolution": "2K"})
    if code not in (200, 201, 202):
        print("submit", code, str(body)[:300]); return
    surl, rurl = body["status_url"], body["response_url"]; t = time.time()
    while time.time() - t < 300:
        time.sleep(5); sc, sb = sv._req(KEY, surl); st = sb.get("status")
        print("  ", name, st, round(time.time()-t), flush=True)
        if st == "COMPLETED": break
        if st in ("FAILED", "ERROR"): print("FAILED", str(sb)[:200]); return
    rc, rb = sv._req(KEY, rurl); imgs = rb.get("images") or []
    if not imgs: print("no image", str(rb)[:200]); return
    dst = os.path.join(OUT, name + ".png")
    with urllib.request.urlopen(imgs[0]["url"], timeout=180) as r, open(dst, "wb") as f:
        f.write(r.read())
    print("ok ->", dst)

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "beat1"
    srcs = {"beat1": "wbeat1_v2", "beat2": "wbeat2_v2", "beat3": "wbeat3_v2"}
    edit(srcs[which], f"/home/colligo/THD_How_to_Install_a_Door_Lock/work/shot3_hs_refs/{which}.png")
