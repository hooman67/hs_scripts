#!/usr/bin/env python3
"""Paint the person out of a frame with nano-banana-pro/edit on fal -> a clean person-free plate."""
import os, sys, time, json
sys.path.insert(0, os.path.expanduser("~/.claude/scripts"))
import seedance_video as sv

KEY = sv.resolve_key(key_file=os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"))
MODEL = "fal-ai/nano-banana-pro/edit"
OUT = "/home/colligo/THD_How_to_Install_a_Door_Lock/work/plates"

EDIT_PROMPT = (
    "Remove the man, his arms, both hands and the tape measure completely from this image. "
    "Keep everything else exactly as it is: the white door, the stainless steel deadbolt above the "
    "stainless steel door knob, the tall frosted glass panel with white blinds, the green fiddle-leaf "
    "fig plant, the white walls, the window and the natural daylight. Naturally fill the area where "
    "the person was with the plausible continuation of the room, wall and door. Photoreal, no people, "
    "no hands, no tools. Do not add any text.")

def edit(name, src):
    url = sv.upload(KEY, src)
    payload = {"prompt": EDIT_PROMPT, "image_urls": [url], "num_images": 1, "resolution": "2K"}
    code, body = sv._req(KEY, sv.QUEUE + MODEL, payload)
    if code not in (200, 201, 202):
        return name, f"submit {code}: {str(body.get('_error'))[:300]}"
    surl, rurl = body.get("status_url"), body.get("response_url")
    t = time.time()
    while time.time() - t < 300:
        time.sleep(5)
        sc, sb = sv._req(KEY, surl)
        st = sb.get("status")
        print(f"    [{name}] {st} ({round(time.time()-t)}s)", flush=True)
        if st == "COMPLETED":
            break
        if st in ("FAILED", "ERROR"):
            return name, f"FAILED: {str(sb)[:200]}"
    rc, rb = sv._req(KEY, rurl)
    imgs = rb.get("images") or []
    if not imgs:
        return name, f"no image: {str(rb)[:250]}"
    import urllib.request
    dst = os.path.join(OUT, name + ".png")
    with urllib.request.urlopen(imgs[0]["url"], timeout=180) as r, open(dst, "wb") as f:
        f.write(r.read())
    json.dump({"name": name, "src": src, "model": MODEL, "prompt": EDIT_PROMPT, "response": rb},
              open(os.path.join(OUT, name + ".json"), "w"), indent=1)
    return name, f"ok -> {dst}"

if __name__ == "__main__":
    for name, src in [
        ("plate_paint_shot",    os.path.join(OUT, "src_last.jpg")),
        ("plate_paint_article", "/home/colligo/THD_How_to_Install_a_Door_Lock/work/refs/article_step1.jpg"),
    ]:
        print(edit(name, src), flush=True)
