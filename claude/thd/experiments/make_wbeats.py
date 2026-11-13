#!/usr/bin/env python3
"""Exp2: remove person (head/face/torso) from 3 wide beat frames, keep hands+tape -> wide keyframes."""
import os, sys, time, json, urllib.request
sys.path.insert(0, os.path.expanduser("~/.claude/scripts"))
import seedance_video as sv

KEY = sv.resolve_key(key_file=os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"))
MODEL = "fal-ai/nano-banana-pro/edit"
SRC_DIR = "/home/colligo/THD_How_to_Install_a_Door_Lock/work/shot3_hs_refs"
OUT = "/home/colligo/THD_How_to_Install_a_Door_Lock/work/plates"

PROMPT = (
    "Remove the man's head, face, hair, neck and torso/upper body from this image completely. "
    "KEEP his forearms, hands and the yellow tape measure exactly where they are, still held "
    "against the door lockset — it should look like forearms and hands reaching in from the left "
    "edge of frame to hold the tape. Keep the white door, the stainless steel deadbolt and knob, "
    "the door edge and latch, the frosted glass panel with blinds, the green plant, the walls, "
    "the window and the natural daylight EXACTLY as they are, unchanged. No head, no face, no "
    "torso anywhere. Photoreal. Do not add any text or logo.")

def edit_one(src, dst, prompt):
    url = sv.upload(KEY, src)
    payload = {"prompt": prompt, "image_urls": [url], "num_images": 1, "resolution": "2K"}
    code, body = sv._req(KEY, sv.QUEUE + MODEL, payload)
    if code not in (200, 201, 202):
        print("submit", code, str(body)[:300]); return False
    surl, rurl = body["status_url"], body["response_url"]
    t = time.time()
    while time.time() - t < 300:
        time.sleep(5)
        sc, sb = sv._req(KEY, surl); st = sb.get("status")
        print("  ", os.path.basename(dst), st, round(time.time()-t), "s", flush=True)
        if st == "COMPLETED": break
        if st in ("FAILED", "ERROR"): print("FAILED", str(sb)[:200]); return False
    rc, rb = sv._req(KEY, rurl)
    imgs = rb.get("images") or []
    if not imgs: print("no image", str(rb)[:250]); return False
    with urllib.request.urlopen(imgs[0]["url"], timeout=180) as r, open(dst, "wb") as f:
        f.write(r.read())
    json.dump({"src": src, "model": MODEL, "prompt": prompt, "response": rb},
              open(dst.replace(".png", ".json"), "w"), indent=1)
    print("ok ->", dst, flush=True)
    return True

def main():
    which = sys.argv[1:] if len(sys.argv) > 1 else ["1", "2", "3"]
    ok = True
    for n in which:
        src = os.path.join(SRC_DIR, f"beat{n}.png")
        dst = os.path.join(OUT, f"wbeat{n}.png")
        prompt = PROMPT
        if len(sys.argv) > 2 and sys.argv[1] == "custom":
            break
        ok = edit_one(src, dst, prompt) and ok
    print("DONE", ok)

if __name__ == "__main__":
    main()
