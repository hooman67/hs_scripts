#!/usr/bin/env python3
"""Make an empty-bore plate: remove the knob from the front plate, leaving a clean round bore hole."""
import os, sys, time, json, urllib.request
sys.path.insert(0, os.path.expanduser("~/.claude/scripts"))
import seedance_video as sv

KEY = sv.resolve_key(key_file=os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"))
MODEL = "fal-ai/nano-banana-pro/edit"
OUT = "/home/colligo/THD_How_to_Install_a_Door_Lock/work/plates"
SRC = os.path.join(OUT, "plate_paint_article.png")

PROMPT = (
    "Remove the lower door knob and its round metal rose completely. In its place show a clean, "
    "empty, round bore hole cut straight through the white door where the knob used to be, about two "
    "inches across, with the plain white door visible through and around it. Keep everything else "
    "exactly the same: the stainless steel deadbolt above, the door edge and latch plate, the tall "
    "frosted glass panel with white blinds, the green fiddle-leaf fig plant, the walls, the window "
    "and the natural daylight. Photoreal, no people, no hands, no tools, no text.")

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
    dst = os.path.join(OUT, "plate_bore_article.png")
    with urllib.request.urlopen(imgs[0]["url"], timeout=180) as r, open(dst, "wb") as f:
        f.write(r.read())
    json.dump({"src": SRC, "model": MODEL, "prompt": PROMPT, "response": rb},
              open(os.path.join(OUT, "plate_bore_article.json"), "w"), indent=1)
    print("ok ->", dst)

if __name__ == "__main__":
    main()
