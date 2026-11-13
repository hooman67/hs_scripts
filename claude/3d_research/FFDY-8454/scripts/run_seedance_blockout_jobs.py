"""Submit and monitor the FFDY-8454 blockout experiments.

Dry-run is the default. Pass --submit to spend. Every request, provider response,
and downloaded result is stored under the experiment folder.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib.util
import json
from pathlib import Path
import subprocess
import time
import urllib.request

from seedance_blockout_jobs import ALL_JOBS, ROOT


SKILL_CLIENT = Path("/home/colligo/.claude/scripts/seedance_video.py")
RESULTS = ROOT / "seedance_results" / "blockout_v1"
MAX_ESTIMATED_TOTAL_USD = 30.0


def load_client():
    spec = importlib.util.spec_from_file_location("seedance_skill_client", SKILL_CLIENT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def video_duration(path):
    output = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ], text=True)
    return float(output.strip())


def preflight(jobs):
    problems = []
    total_estimate = 0.0
    summaries = []
    for job in jobs:
        missing = [str(p) for p in job["images"] + job["videos"] if not Path(p).is_file()]
        if missing:
            problems.append(f"{job['id']}: missing {missing}")
            continue
        duration = int(job["duration"])
        if not 4 <= duration <= 30:
            problems.append(f"{job['id']}: output duration {duration} is outside 4..30")
        durations = [video_duration(p) for p in job["videos"]]
        if any(d < 1.8 or d > 30.2 for d in durations):
            problems.append(f"{job['id']}: video duration outside 1.8..30.2: {durations}")
        if len(job["videos"]) > 10 or sum(durations) > 30.2:
            problems.append(f"{job['id']}: video refs exceed limits: n={len(durations)}, sum={sum(durations):.2f}")
        if len(job["images"]) > 30:
            problems.append(f"{job['id']}: more than 30 images")
        # Measured THD estimate: ~$0.46 per 720p second, input+output billed,
        # multiplied by 0.6 when a video reference is supplied.
        estimate = 0.46 * (sum(durations) + duration) * 0.6
        total_estimate += estimate
        summaries.append({
            "id": job["id"], "output_seconds": duration,
            "input_video_seconds": round(sum(durations), 3),
            "estimated_usd": round(estimate, 2),
        })
    if total_estimate > MAX_ESTIMATED_TOTAL_USD:
        problems.append(
            f"estimated total ${total_estimate:.2f} exceeds safety cap ${MAX_ESTIMATED_TOTAL_USD:.2f}"
        )
    return problems, summaries, total_estimate


def submit_one(client, key, job):
    out = RESULTS / job["id"]
    out.mkdir(parents=True, exist_ok=True)
    video_path = out / f"{job['id']}.mp4"
    if video_path.exists() and video_path.stat().st_size:
        return job["id"], "skip-existing", str(video_path)

    local_request = {
        "id": job["id"], "endpoint": client.MODELS["ref"],
        "duration": str(job["duration"]), "resolution": "720p",
        "aspect_ratio": "16:9", "generate_audio": False,
        "images": [str(p) for p in job["images"]],
        "videos": [str(p) for p in job["videos"]],
        "prompt": job["prompt"],
    }
    (out / "request.local.json").write_text(json.dumps(local_request, indent=2))
    (out / "prompt.txt").write_text(job["prompt"])

    image_urls = [client.upload(key, str(p)) for p in job["images"]]
    video_urls = [client.upload(key, str(p)) for p in job["videos"]]
    payload = {
        "prompt": job["prompt"], "resolution": "720p",
        "duration": str(job["duration"]), "generate_audio": False,
        "aspect_ratio": "16:9", "image_urls": image_urls,
        "video_urls": video_urls,
    }
    debug = {"payload": payload, "submit": None, "status": [], "result": None}
    (out / "request.submitted.json").write_text(json.dumps(payload, indent=2))

    code, body = client._req(key, client.QUEUE + client.MODELS["ref"], payload)
    debug["submit"] = {"http": code, "body": body}
    (out / "debug.json").write_text(json.dumps(debug, indent=2))
    if code not in (200, 201, 202):
        return job["id"], f"submit-{code}", str(body)[:300]

    status_url, response_url = body.get("status_url"), body.get("response_url")
    if not status_url or not response_url:
        return job["id"], "missing-queue-urls", str(body)[:300]

    deadline = time.time() + 2400
    while time.time() < deadline:
        time.sleep(10)
        sc, sb = client._req(key, status_url)
        debug["status"].append({"http": sc, "body": sb})
        (out / "debug.json").write_text(json.dumps(debug, indent=2))
        state = sb.get("status")
        if state == "COMPLETED":
            break
        if state in ("FAILED", "ERROR"):
            return job["id"], state, str(sb)[:500]
    else:
        return job["id"], "timeout", str(out / "debug.json")

    rc, rb = client._req(key, response_url)
    debug["result"] = {"http": rc, "body": rb}
    (out / "debug.json").write_text(json.dumps(debug, indent=2))
    url = (rb.get("video") or {}).get("url") or (rb.get("videos") or [{}])[0].get("url")
    if not url:
        return job["id"], "no-video-url", str(rb)[:500]
    with urllib.request.urlopen(url, timeout=600) as response, video_path.open("wb") as handle:
        handle.write(response.read())
    metadata = {"job": local_request, "response": rb, "output": str(video_path)}
    (out / "result.json").write_text(json.dumps(metadata, indent=2))
    return job["id"], "ok", str(video_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument(
        "--job", action="append", default=[],
        help="Run only the named job id; repeat to select multiple jobs.",
    )
    args = parser.parse_args()

    jobs = ALL_JOBS
    if args.job:
        requested = set(args.job)
        jobs = [job for job in ALL_JOBS if job["id"] in requested]
        missing = sorted(requested - {job["id"] for job in jobs})
        if missing:
            raise SystemExit(f"unknown job ids: {', '.join(missing)}")

    problems, summaries, estimate = preflight(jobs)
    print(json.dumps({"jobs": summaries, "estimated_total_usd": round(estimate, 2),
                      "problems": problems}, indent=2), flush=True)
    if problems:
        raise SystemExit(2)
    if not args.submit:
        print("DRY_RUN_OK: pass --submit to spend", flush=True)
        return

    client = load_client()
    key = client.resolve_key()
    RESULTS.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(submit_one, client, key, job): job["id"] for job in jobs}
        for future in as_completed(futures):
            print("RESULT", *future.result(), flush=True)


if __name__ == "__main__":
    main()
