#!/usr/bin/env python3
"""Integrate finished pipeline shots into the gallery: per shot, add a divider + TARGET + result
section (same format as shot 0007), staging assets. Central step (avoids manifest races from the
batch subagents). Usage: python3 pipeline/integrate_shots.py 0008 0009 0010 ..."""
import os, sys, json, subprocess, glob

BASE = "/home/colligo/THD_How_to_Install_a_Door_Lock"
CONF = os.path.join(BASE, "pipeline", "configs")
ASSETS = os.path.join(BASE, "gallery", "assets")
MAN = os.path.join(BASE, "gallery", "manifest.json")


def dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=noprint_wrappers=1:nokey=1", path],
                         capture_output=True, text=True).stdout.strip()
    try: return float(out)
    except: return 0.0


def frame(src, t, dst):
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-ss", str(t), "-i", src,
                    "-frames:v", "1", "-q:v", "3", dst, "-y"], check=True)


def compress(src, dst):
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", src, "-vf", "scale=1280:-2",
                    "-c:v", "libx264", "-crf", "30", "-preset", "veryfast", "-an", dst, "-y"], check=True)


def integrate(nn, M):
    sid = f"shot{nn}"
    if any(s["id"] == f"{sid}_divider" for s in M["sections"]):
        return f"{sid}: already present, skip"
    cfgp = os.path.join(CONF, f"{sid}.json")
    if not os.path.exists(cfgp):
        return f"{sid}: NO CONFIG, skip"
    cfg = json.load(open(cfgp))
    src = cfg["source"]
    wd = cfg["work_dir"]
    mp4 = os.path.join(wd, "gen", f"{sid}_v1.mp4")
    beats = cfg.get("beats", [])
    subject = cfg.get("subject", "").rstrip(";, ")

    # TARGET assets: compressed source + up to 3 frames at beat timestamps (or evenly)
    compress(src, os.path.join(ASSETS, f"target_{sid}.mp4"))
    D = dur(src)
    ts = [b["t"] for b in beats][:3] or [D * x for x in (0.15, 0.5, 0.85)]
    tframes = []
    for i, t in enumerate(ts):
        fn = f"target{nn}_f{i}.jpg"; frame(src, t, os.path.join(ASSETS, fn)); tframes.append("assets/" + fn)

    M["sections"].append({"id": f"{sid}_divider", "kind": "divider",
        "label": f"SHOT {nn} — {subject[:70]}",
        "note": f"Generated with the rewriter pipeline (configs/{sid}.json). TARGET then pipeline result."})
    M["sections"].append({"id": f"target{nn}", "kind": "target",
        "label": f"TARGET — original human shot {nn}",
        "note": f"{subject}. {round(D,1)}s source. Beats: " +
                " → ".join(b["desc"][:60] for b in beats) if beats else subject,
        "video": f"assets/target_{sid}.mp4", "frames": tframes})

    if not (os.path.exists(mp4) and os.path.getsize(mp4) > 0):
        M["sections"].append({"id": f"{sid}_pipeline", "label": f"PIPELINE RESULT — shot {nn}",
            "params": "SKIPPED / not generated",
            "experiments": [{"id": f"{sid}_v1", "approach": "pipeline",
                "status": "rejected", "error": "no output mp4 (skipped or failed)", "refs": []}]})
        return f"{sid}: target added, NO RESULT mp4"

    # result assets
    import shutil
    shutil.copy(mp4, os.path.join(ASSETS, f"{sid}_result.mp4"))
    kfs = sorted(glob.glob(os.path.join(wd, "kf*.png")))
    refs = []
    for i, k in enumerate(kfs):
        fn = f"{sid}_kf{i+1}.png"; shutil.copy(k, os.path.join(ASSETS, fn)); refs.append("assets/" + fn)
    Dr = dur(mp4)
    rframes = []
    for i, t in enumerate([Dr * x for x in (0.05, 0.3, 0.5, 0.7, 0.92)]):
        fn = f"{sid}_result_f{i}.jpg"; frame(mp4, t, os.path.join(ASSETS, fn)); rframes.append("assets/" + fn)
    prompt = ""
    pp = os.path.join(wd, "prompt.txt")
    if os.path.exists(pp): prompt = open(pp).read()

    M["sections"].append({"id": f"{sid}_pipeline", "label": f"PIPELINE RESULT — shot {nn} (v1)",
        "params": f"{round(Dr)}s · 720p · 16:9 · person_mode={cfg.get('person_mode')} · "
                  f"{len(beats)} keyframe(s) · auto-built by rewriter_pipeline.py",
        "shared_prompt_note": "End-to-end pipeline: auto-extracted beat frames, R3-safe keyframes, "
                              "vendor @Image keyframe prompt in the THD register, ~5s/beat.",
        "experiments": [{"id": f"{sid}_v1",
            "approach": f"{cfg.get('person_mode')} keyframes ({len(beats)} beat(s)) — {cfg.get('tool','')}",
            "status": "ok", "note": subject,
            "refs": refs, "video": f"assets/{sid}_result.mp4", "frames": rframes, "prompt": prompt}]})
    return f"{sid}: integrated ({len(kfs)} kf, {round(Dr)}s)"


if __name__ == "__main__":
    M = json.load(open(MAN))
    for nn in sys.argv[1:]:
        print(integrate(nn, M))
    json.dump(M, open(MAN, "w"), indent=2, ensure_ascii=False)
    print("manifest written")
