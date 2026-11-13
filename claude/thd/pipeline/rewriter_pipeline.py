#!/usr/bin/env python3
"""THD article -> video REWRITER pipeline (backlog b).

Encodes the recipe validated on shot 0003 (rounds 1-13). One source how-to SHOT in, one
Seedance recreation out. A shot is described by a CONFIG (below); the pipeline does the mechanics:

  1. extract N beat keyframes from the source shot at chosen timestamps
  2. make them R3-safe:
       person_mode="cover_body"  -> nano-banana removes head+face+torso, KEEPS real hands+tool
                                    (keeps natural hands; also strips baked-in step/TIP graphics)
       person_mode="crop"        -> tight face-free crop (hands+tool only)  [not implemented here]
       person_mode="none"        -> use frames as-is (hands-only / no person source)
  3. compose the prompt: vendor ordered-keyframe directives (@Image1..N) IN the THD 5-line register
  4. generate: reference-to-video, ordered keyframes, duration ~= secs_per_beat * n_beats (>=4, <=22)

WHY each choice (measured on shot 0003):
  - R3: any real person's face/head/torso in a reference -> 422; hands/forearms are OK.
  - The wide/medium frame must come from the KEYFRAMES themselves (consistent scale) — mixing a wide
    plate @Image1 with tight beat crops makes the beats blur or the frame collapse.
  - Give ~5 s per beat; 8 s was too short for 3 subtle beats (they blended).
  - Keyframes drive the visual; text can't override a pose the keyframe doesn't show, BUT a per-beat
    text constraint DOES rein in drift when the keyframe is right (e.g. tape not past the plate edge).
  - Negatives (no on-screen text/logos) are per the THD brief; plain clothing avoids invented wordmarks.

Shot-analysis (which beats, what they show) is currently filled into the CONFIG by a human/LLM
looking at the shot; automating that from the article is the remaining piece of (b). See PIPELINE.md.
"""
import os, sys, time, json, urllib.request, subprocess
sys.path.insert(0, os.path.expanduser("~/.claude/scripts"))
import seedance_video as sv

NANO = "fal-ai/nano-banana-pro/edit"
LOOK = ("Photoreal Home Depot how-to footage, bright natural daylight, clean and crisp.")
NEG = ("No on-screen text, no captions, no step labels, no watermarks, no added logos, "
       "no competitor brands.")


def key():
    return sv.resolve_key(key_file=os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"))


def probe_dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=noprint_wrappers=1:nokey=1", path],
                         capture_output=True, text=True).stdout.strip()
    try: return float(out)
    except: return 0.0


def extract_keyframes(source, timestamps, out_dir, stem="kf"):
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for i, t in enumerate(timestamps):
        p = os.path.join(out_dir, f"{stem}{i+1}.jpg")
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-ss", str(t),
                        "-i", source, "-frames:v", "1", "-q:v", "2", p, "-y"], check=True)
        paths.append(p)
    return paths


def cover_body(k, src, out_path, tool="tool"):
    """nano-banana: remove head+face+torso, keep real hands/forearms + the tool + scene. R3-safe."""
    prompt = (
        "Edit this image. KEEP the person's forearms, hands and the " + tool + " EXACTLY as they are — "
        "identical pixels, same natural length and position; do NOT stretch, lengthen, move or redraw "
        "the arms or hands. Replace ONLY the head, face, hair, neck and torso/upper body with the plain "
        "background that belongs behind them. Also remove any on-screen graphics, step labels or caption "
        "text, replacing them with the plain scene behind. Keep the door, hardware, tools and the whole "
        "background scene otherwise unchanged. The result: natural forearms and hands using the " + tool +
        ", with no head, face or torso and no on-screen graphics. Photoreal. No text, no logos.")
    url = sv.upload(k, src)
    code, body = sv._req(k, sv.QUEUE + NANO, {"prompt": prompt, "image_urls": [url],
                                              "num_images": 1, "resolution": "2K"})
    if code not in (200, 201, 202):
        raise RuntimeError(f"cover_body submit {code}: {str(body)[:200]}")
    surl, rurl = body["status_url"], body["response_url"]; t = time.time()
    while time.time() - t < 300:
        time.sleep(5); sc, sb = sv._req(k, surl)
        if sb.get("status") == "COMPLETED": break
        if sb.get("status") in ("FAILED", "ERROR"): raise RuntimeError(f"cover_body failed {sb}")
    rc, rb = sv._req(k, rurl); imgs = rb.get("images") or []
    if not imgs: raise RuntimeError(f"cover_body no image {str(rb)[:200]}")
    with urllib.request.urlopen(imgs[0]["url"], timeout=180) as r, open(out_path, "wb") as f:
        f.write(r.read())
    return out_path


def _nano_edit(k, src, prompt, out_path, tries=4):
    """One nano-banana image edit, with retries (fal storage/queue occasionally 500s)."""
    last = None
    for attempt in range(tries):
        try:
            url = sv.upload(k, src)
            code, body = sv._req(k, sv.QUEUE + NANO, {"prompt": prompt, "image_urls": [url],
                                                      "num_images": 1, "resolution": "2K"})
            if code not in (200, 201, 202):
                raise RuntimeError(f"nano submit {code}: {str(body)[:200]}")
            surl, rurl = body["status_url"], body["response_url"]; t = time.time()
            while time.time() - t < 300:
                time.sleep(5); sc, sb = sv._req(k, surl)
                if sb.get("status") == "COMPLETED": break
                if sb.get("status") in ("FAILED", "ERROR"): raise RuntimeError(f"nano failed {sb}")
            rc, rb = sv._req(k, rurl); imgs = rb.get("images") or []
            if not imgs: raise RuntimeError(f"nano no image {str(rb)[:200]}")
            with urllib.request.urlopen(imgs[0]["url"], timeout=180) as r, open(out_path, "wb") as f:
                f.write(r.read())
            return out_path
        except Exception as e:
            last = e; print(f"    nano retry {attempt+1}/{tries} after: {str(e)[:120]}", flush=True)
            time.sleep(8)
    raise last


def sketchify(k, src, out_path):
    """Convert a beat frame to a clean line SKETCH (line-art keyframe; R3-safe, no real likeness)."""
    return _nano_edit(k, src,
        "Convert this photo into a CLEAN, BOLD, high-contrast black-and-white LINE DRAWING on pure white "
        "paper: crisp clear outlines only of the person, the hands, the tool and the hardware/door. Keep "
        "the EXACT composition, poses and tool position. No color, no shading fills, no photoreal texture, "
        "no text. Pure line art.", out_path)


def paint_out_person(k, src, out_path):
    """Paint the person (and tool) fully out of a frame -> a photoreal person-free style/appearance plate."""
    return _nano_edit(k, src,
        "Remove the person entirely (head, face, hair, body, arms, hands) and any hand-held tool from this "
        "image; fill the vacated area with the plausible continuation of the scene behind. Keep the door, "
        "the hardware and the whole background exactly as they are, and keep any on-screen graphics OUT. "
        "Photoreal, no people, no tools, no text.", out_path)


def compose_prompt_sketch(cfg):
    """Sketch method: sketches are the ordered keyframes; a trailing plate supplies photoreal appearance."""
    beats = cfg["beats"]; n = len(beats)
    L = [f"Use @Image1 through @Image{n} as keyframes in that order. @Image1"
         + (f"-@Image{n}" if n > 1 else "") + " are line-drawing SKETCHES that define the exact composition "
         "and the exact hand-and-tool geometry at each beat — reproduce each precisely, keep the tool the "
         "SHORT length shown and do not extend it beyond the sketch."]
    for i, b in enumerate(beats):
        if i == 0:
            s = f"Use @Image1 as the first frame — BEAT 1: {b['desc']}"
        elif i == n - 1:
            s = f"Use @Image{n} as the last frame — BEAT {n}: {b['desc']}"
        else:
            s = f"@Image{i+1} defines keyframe {i+1} — BEAT {i+1}: {b['desc']}"
        if b.get("constraint"):
            s += ". " + b["constraint"]
        L.append(s.rstrip(".") + ".")
    L.append(f"@Image{n+1} is a PHOTOREAL appearance reference: render the ENTIRE video photorealistically "
             "in its style, lighting and materials; do NOT adopt the line-drawing/sketch look of the "
             "keyframes — they are only structure/position guides.")
    L.append(f"The shot moves through the {n} beats in order, settling briefly on each. Between beats the "
             "hand and tool move smoothly and directly from one position to the next, with NO extra "
             "back-and-forth, resetting, or retracting motions.")
    cl = cfg.get("clothing", "work shirt").rstrip(". ")
    L.append(cfg["subject"] + f" is FULLY VISIBLE in frame — head, face, {cl.lower()} torso and both arms — "
             "performing the beats, not just hands.")
    keep = " Keep " + cfg["scene_keep"] + " consistent and photoreal." if cfg.get("scene_keep") else ""
    L.append(f"{LOOK}{keep} {cl} with no text or logo. {NEG}")
    return "\n".join(L)


def compose_prompt(cfg):
    """Vendor ordered-keyframe directives inside the THD register. Returns the prompt string."""
    beats = cfg["beats"]; n = len(beats); framing = cfg.get("framing", "medium")
    L = []
    if n > 1:
        L.append(f"Use @Image1 through @Image{n} as keyframes in that order.")
    L.append(f"Keep a fixed {framing} camera framing for the entire shot; do not zoom or pan.")
    for i, b in enumerate(beats):
        if i == 0:
            s = f"Use @Image1 as the first frame — {b['desc']}"
        elif i == n - 1:
            s = f"Use @Image{n} as the last frame — {b['desc']}"
        else:
            s = f"@Image{i+1} defines keyframe {i+1} — {b['desc']}"
        if b.get("constraint"):
            s += ". " + b["constraint"]
        L.append(s.rstrip(".") + ".")
    if n > 1:
        L.append(f"The shot moves through these {n} beats in order, settling briefly on each so each "
                 "reads distinctly, with continuous natural hand and arm motion.")
    # Full-person: the cover-body keyframes show only hands+tool, so instruct the model to render the
    # WHOLE man around them (otherwise it stays hands-only, as it did on the first batch).
    if cfg.get("person_mode") == "cover_body":
        cl = cfg.get("clothing", "work shirt").rstrip(". ")
        L.append(cfg["subject"] + " is FULLY VISIBLE in frame — his head and face, his " + cl.lower() +
                 " torso and both arms are all in shot as he works, not just his hands. The reference "
                 "keyframes show only his hands and the hardware; generate the rest of his body and head "
                 "naturally around them. Do not render disembodied hands.")
    else:
        L.append(cfg["subject"] + " works with both hands; movements are natural and unhurried.")
    keep = " Keep " + cfg["scene_keep"] + " exactly as in the reference frames." if cfg.get("scene_keep") else ""
    L.append(f"{LOOK}{keep} {cfg.get('clothing','Plain clothing')} with no text or logo. {NEG}")
    return "\n".join(L)


def run(cfg):
    """Full pipeline for one shot config. Returns (prompt, keyframe_paths, gen_result)."""
    k = key()
    work = cfg["work_dir"]; os.makedirs(work, exist_ok=True)
    raw = extract_keyframes(cfg["source"], [b["t"] for b in cfg["beats"]],
                            os.path.join(work, "raw"), stem="raw")
    # method selects how references are built (config-driven; user picks per shot):
    #   "sketch"     -> sketches as ordered keyframes + a photoreal person-free plate as appearance ref
    #   "cover_body" -> body-covered keyframes (head+torso removed, real hands+tool kept)  [default]
    #   "none"       -> raw frames as-is (hands/product only)
    method = cfg.get("method", cfg.get("person_mode", "cover_body"))
    refs = []
    if method == "sketch":
        for i, src in enumerate(raw):
            print(f"  sketchify sk{i+1} ...", flush=True)
            refs.append(sketchify(k, src, os.path.join(work, f"sk{i+1}.png")))
        print("  paint_out style plate ...", flush=True)
        refs.append(paint_out_person(k, raw[0], os.path.join(work, "style_plate.png")))
        prompt = compose_prompt_sketch(cfg)
    else:
        for i, src in enumerate(raw):
            if method == "cover_body":
                print(f"  cover_body kf{i+1} ...", flush=True)
                refs.append(cover_body(k, src, os.path.join(work, f"kf{i+1}.png"), tool=cfg.get("tool", "tool")))
            else:
                refs.append(src)
        prompt = compose_prompt(cfg)
    open(os.path.join(work, "prompt.txt"), "w").write(prompt)
    # Match the ORIGINAL shot's length (Seedance allows 4..22s), so pacing + trim match the source.
    dur = max(4, min(22, round(probe_dur(cfg["source"]))))
    print(f"  generating ({dur}s, {len(refs)} keyframes) ...", flush=True)
    res = sv.generate(k, name=cfg["id"], mode="ref", prompt=prompt,
                      out_dir=os.path.join(work, "gen"), images=refs,
                      duration=str(dur), resolution=cfg.get("resolution", "720p"),
                      audio=False, aspect="16:9",
                      on_status=lambda st, s: print(f"    {st} ({s}s)", flush=True))
    return prompt, refs, res


if __name__ == "__main__":
    cfg_path = sys.argv[1]
    cfg = json.load(open(cfg_path))
    prompt, refs, res = run(cfg)
    print("KEYFRAMES:", refs)
    print("RESULT:", res)
    print("DONE")
