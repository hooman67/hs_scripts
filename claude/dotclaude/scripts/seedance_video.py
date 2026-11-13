#!/usr/bin/env python3
"""Generate video with Seedance 2.5 via fal.ai — text / image / reference to video.

Self-contained CLI distilled from Adobe-Firefly/THD_Proj scripts/brand_video/fal_gen.py
(the seedance-video skill). Keeps the hard-won API constraints that cost real money to learn:

  R1  duration is 'auto' or an integer 4..22 AS A STRING. There is no 3s. An illegal
      duration is accepted into the queue (HTTP 200) and only rejected on result fetch.
      -> we preflight it before submitting.
  R2  the seed/reference image's framing beats the prompt. Want a close-up? supply a close ref.
  R3  any reference carrying a real person's likeness -> 422 content_policy_violation (any modality).
  R4  image-to-video silently ignores aspect_ratio (returns the seed's aspect). We don't send it on i2v.

Cost (720p): ~$0.46 per second of output. 1080p is 2.25x for no measured quality gain.
A video reference cuts the rate to 0.6x. Keep clips short and trim in post.

Key resolution order (never printed, never logged):
  1. --key on the command line (discouraged; shows in shell history)
  2. FAL_KEY env var
  3. file named by FAL_ENV_FILE  (FAL_KEY=... / fal_api_key: ... / bare key)
  4. --key-file PATH             (same formats)
  5. ~/.claude/hshariati/credentials.yaml  (fal_api_key: ...)
  6. ~/hs_scripts/claude/thd/creds.txt     (fal_api_key: ...)
"""
import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request

QUEUE = "https://queue.fal.run/"
UPLOAD_INIT = "https://rest.alpha.fal.ai/storage/upload/initiate"
MODELS = {
    "t2v": "bytedance/seedance-2.5/text-to-video",
    "i2v": "bytedance/seedance-2.5/image-to-video",
    "ref": "bytedance/seedance-2.5/reference-to-video",
}
ALLOWED_DURATIONS = {"auto"} | {str(n) for n in range(4, 23)}
RESOLUTIONS = ("480p", "720p", "1080p")

_KEY_PREFIXES = ("FAL_KEY=", "FAL_KEY:", "fal_api_key:", "fal_api_key=", "fal_key:", "fal_key=")
_DEFAULT_KEY_FILES = (
    os.path.expanduser("~/.claude/hshariati/credentials.yaml"),
    os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"),
)


def _scan_key_file(path):
    if not path or not os.path.exists(path):
        return None
    for line in open(path):
        s = line.strip()
        if s.startswith("export "):
            s = s[len("export "):]
        for pref in _KEY_PREFIXES:
            if s.startswith(pref):
                return s[len(pref):].strip().strip("'\"") or None
    return None


def resolve_key(cli_key=None, key_file=None):
    if cli_key:
        return cli_key
    if os.environ.get("FAL_KEY"):
        return os.environ["FAL_KEY"]
    for p in (os.environ.get("FAL_ENV_FILE"), key_file, *_DEFAULT_KEY_FILES):
        k = _scan_key_file(p)
        if k:
            return k
    raise SystemExit(
        "No fal key found. Set FAL_KEY, or point --key-file / FAL_ENV_FILE at a file "
        "containing `fal_api_key: <key>` (or `FAL_KEY=<key>`).")


def _req(key, url, data=None, method=None, timeout=180):
    h = {"Authorization": f"Key {key}"}
    if data is not None:
        h["Content-Type"] = "application/json"
        data = json.dumps(data).encode()
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            body = resp.read()
            return resp.status, (json.loads(body) if body else {})
    except urllib.error.HTTPError as e:
        return e.code, {"_error": e.read().decode("utf-8", "replace")[:600]}


def upload(key, path):
    """Put a local file in fal storage; fall back to a data URI if storage is unavailable."""
    if path.startswith(("http://", "https://", "data:")):
        return path
    ct = mimetypes.guess_type(path)[0] or "image/jpeg"
    code, body = _req(key, UPLOAD_INIT,
                      {"content_type": ct, "file_name": os.path.basename(path)})
    if code == 200 and body.get("upload_url"):
        put = urllib.request.Request(body["upload_url"], data=open(path, "rb").read(),
                                     headers={"Content-Type": ct}, method="PUT")
        with urllib.request.urlopen(put, timeout=300):
            pass
        return body.get("file_url") or body.get("public_url")
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    return f"data:{ct};base64,{b64}"


def preflight(mode, duration, resolution, images):
    bad = []
    if str(duration) not in ALLOWED_DURATIONS:
        bad.append(f"duration {duration!r} must be 'auto' or an integer 4..22 (R1)")
    if resolution not in RESOLUTIONS:
        bad.append(f"resolution {resolution!r} must be one of {RESOLUTIONS}")
    if mode in ("i2v", "ref") and not images:
        bad.append(f"mode {mode!r} needs at least one --image")
    for p in images or []:
        if not p.startswith(("http://", "https://", "data:")) and not os.path.exists(p):
            bad.append(f"reference file missing on disk: {p}")
    return bad


def generate(key, name, mode, prompt, out_dir, images=None, duration="5",
             resolution="720p", audio=False, aspect="16:9", poll=10, timeout_s=1800,
             on_status=None, end_image=None):
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, name + ".mp4")

    problems = preflight(mode, duration, resolution, images)
    if problems:
        return name, "preflight: " + "; ".join(problems), 0, 0

    payload = {"prompt": prompt, "resolution": resolution, "duration": str(duration),
               "generate_audio": bool(audio)}
    if mode != "i2v" and aspect:   # R4: i2v ignores aspect_ratio, so don't send it
        payload["aspect_ratio"] = aspect
    imgs = [upload(key, p) for p in (images or [])]
    if mode == "i2v":
        payload["image_url"] = imgs[0]
    elif mode == "ref":
        payload["image_urls"] = imgs
    # i2v only: an optional last frame; Seedance interpolates first->end (see skill §6).
    if end_image and mode == "i2v":
        payload["end_image_url"] = upload(key, end_image)

    t = time.time()
    code, body = _req(key, QUEUE + MODELS[mode], payload)
    if code not in (200, 201, 202):
        return name, f"submit {code}: {str(body.get('_error'))[:300]}", 0, 0
    status_url = body.get("status_url")
    resp_url = body.get("response_url")
    if not status_url:
        return name, f"no status_url: {str(body)[:200]}", 0, 0

    dbg = {"submit": body, "payload_keys": sorted(payload), "status": [], "result": None}
    dbg_p = os.path.join(out_dir, name + ".debug.json")

    while time.time() - t < timeout_s:
        time.sleep(poll)
        sc, sb = _req(key, status_url)
        st = sb.get("status")
        dbg["status"].append({"http": sc, "status": st})
        if on_status:
            on_status(st, round(time.time() - t))
        if st == "COMPLETED":
            break
        if st in ("FAILED", "ERROR"):
            json.dump(dbg, open(dbg_p, "w"), indent=1)
            return name, f"FAILED (see {name}.debug.json): {str(sb)[:200]}", round(time.time() - t), 0
    else:
        json.dump(dbg, open(dbg_p, "w"), indent=1)
        return name, "timeout", round(time.time() - t), 0

    rc, rb = _req(key, resp_url)
    dbg["result"] = {"http": rc, "body": rb}
    json.dump(dbg, open(dbg_p, "w"), indent=1)
    vid = (rb.get("video") or {}).get("url") or (rb.get("videos") or [{}])[0].get("url")
    if not vid:
        return name, f"no video url: {str(rb)[:250]}", round(time.time() - t), 0
    with urllib.request.urlopen(vid, timeout=600) as r, open(dst, "wb") as f:
        f.write(r.read())
    json.dump({"name": name, "mode": mode, "prompt": prompt,
               "images": [os.path.basename(p) for p in (images or [])],
               "duration": str(duration), "resolution": resolution, "audio": bool(audio),
               "aspect": aspect, "response": rb},
              open(os.path.join(out_dir, name + ".json"), "w"), indent=1)
    return name, "ok", round(time.time() - t), os.path.getsize(dst)


def main():
    ap = argparse.ArgumentParser(
        description="Generate a video with Seedance 2.5 via fal.ai.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--prompt", help="prompt text (or use --prompt-file)")
    ap.add_argument("--prompt-file", help="read prompt from this file")
    ap.add_argument("--mode", choices=["t2v", "i2v", "ref"], default="t2v",
                    help="t2v=text only, i2v=one first-frame image, ref=1-2 reference images")
    ap.add_argument("--image", action="append", dest="images", default=[],
                    help="reference image path/URL (repeatable; i2v uses the first)")
    ap.add_argument("--duration", default="5", help="'auto' or integer 4..22 as string (R1)")
    ap.add_argument("--resolution", default="720p", choices=list(RESOLUTIONS))
    ap.add_argument("--aspect", default="16:9", help="ignored for i2v (R4)")
    ap.add_argument("--audio", dest="audio", action="store_true", default=True)
    ap.add_argument("--no-audio", dest="audio", action="store_false")
    ap.add_argument("--name", default="seedance", help="output filename stem (must be unique)")
    ap.add_argument("--out", default=os.path.expanduser("~/seedance_out"),
                    help="output directory")
    ap.add_argument("--key", help="fal key (discouraged: shows in shell history)")
    ap.add_argument("--key-file", help="file containing fal_api_key: / FAL_KEY=")
    ap.add_argument("--check", action="store_true",
                    help="verify credential is resolvable, spend nothing")
    a = ap.parse_args()

    key = resolve_key(a.key, a.key_file)
    if a.check:
        print(f"credential OK: {len(key)} chars, ends {key[-4:]}  <- compare this, never the key")
        return 0

    prompt = a.prompt
    if a.prompt_file:
        prompt = open(a.prompt_file).read()
    if not prompt:
        ap.error("need --prompt or --prompt-file")

    print(f"[seedance] mode={a.mode} {a.duration}s {a.resolution} audio={a.audio} -> {a.out}",
          flush=True)
    name, status, secs, size = generate(
        key, name=a.name, mode=a.mode, prompt=prompt, out_dir=a.out,
        images=a.images, duration=a.duration, resolution=a.resolution,
        audio=a.audio, aspect=a.aspect,
        on_status=lambda st, s: print(f"    ... {st} ({s}s)", flush=True))
    print(f"[{status}] {name}  {secs}s  {size // 1024} KB")
    if status == "ok":
        print(f"  video:  {os.path.join(a.out, name + '.mp4')}")
        print(f"  prompt: {os.path.join(a.out, name + '.json')}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
