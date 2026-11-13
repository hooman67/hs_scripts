# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx", "boto3", "tqdm"]
# ///
"""Run a text-to-image generation eval against a customer endpoint.

Usage:
  uv run run_generation.py \
    --customer humain_t2i \
    --prompts-csv /tmp/humain_prompts.csv \
    --token-file /tmp/auth_token.txt \
    --seeds 333,777 \
    --limit 5 \
    --run-name smoke5 \
    [--no-upload]
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import importlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import httpx
from tqdm import tqdm

POLL_INTERVAL_S = 4
POLL_TIMEOUT_S = 600  # 10 min per job
MAX_WORKERS = 8

# Error codes worth retrying. prompt_unsafe / http_4xx are NOT retryable.
RETRYABLE_ERROR_CODES = {
    "submit_error", "poll_exception", "download_error",
    "job_canceled", "job_timeout", "runtime_error", "timeout",
    "worker_exception",
}
# Default in-task retries on top of the first attempt
DEFAULT_TASK_RETRIES = 2
TASK_RETRY_BACKOFF_S = 8

# S3 upload retries (sync is idempotent so safe to loop)
S3_UPLOAD_ATTEMPTS = 5
S3_UPLOAD_BACKOFF_S = 6

# ---------- prompt CSV loading ----------

def check_token_expiry(token: str, token_file: str) -> None:
    """Decode JWT payload and abort if the token is already expired.

    The Adobe token's `created_at` is in milliseconds and `expires_in` is also in milliseconds
    (e.g. 86400000 = 24h). We add a small safety margin.
    """
    import base64
    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        claims = json.loads(base64.urlsafe_b64decode(payload))
        created_ms = int(claims.get("created_at", 0))
        expires_in_ms = int(claims.get("expires_in", 0))
        if not created_ms or not expires_in_ms:
            return  # unknown format, let the endpoint judge
        expires_at = (created_ms + expires_in_ms) / 1000
        now = time.time()
        if expires_at < now + 60:  # 60s safety margin
            expired_iso = dt.datetime.fromtimestamp(expires_at).isoformat()
            raise SystemExit(
                f"\nERROR: Bearer token in {token_file} expired at {expired_iso}.\n"
                f"Refresh it (paste a fresh 'authorization: Bearer ...' from a working browser request) and retry.\n"
            )
    except SystemExit:
        raise
    except Exception:
        # Token didn't decode as expected JWT — don't block, let the endpoint judge.
        return


def load_prompts(csv_path: str) -> list[dict]:
    """Return list of {id, category, prompt, aspect_ratio} rows."""
    rows: list[dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                "id": r.get("id") or r.get("ID") or r.get("Id"),
                "category": r.get("Category") or r.get("category") or "",
                "prompt": r.get("Prompt") or r.get("prompt") or "",
                "aspect_ratio": r.get("Aspect Ratio") or r.get("aspect_ratio") or "1:1",
            })
    return rows


# ---------- endpoint client ----------

class AuthError(Exception):
    """Raised on 401/403 from the generate endpoint. Never retried."""


class Client:
    def __init__(self, token: str, customer_mod):
        self.token = token.strip()
        self.cm = customer_mod
        self.client = httpx.Client(
            timeout=httpx.Timeout(60.0, connect=10.0),
            headers={
                "authorization": f"Bearer {self.token}",
                "x-api-key": customer_mod.X_API_KEY,
                "content-type": "application/json",
            },
        )

    def submit(self, payload: dict) -> str:
        r = self.client.post(self.cm.ENDPOINT_URL, json=payload)
        if r.status_code in (401, 403):
            # auth_failed is intentionally NOT in RETRYABLE_ERROR_CODES — fail fast
            raise AuthError(f"HTTP {r.status_code} from generate endpoint: {(r.text or '')[:200]}")
        r.raise_for_status()
        href = r.json()["links"]["result"]["href"]
        m = re.search(r"/result/([^/?]+)", href)
        if not m:
            raise ValueError(f"can't parse job id from {href!r}")
        return m.group(1)

    def poll_once(self, job_id: str) -> dict:
        r = self.client.get(self.cm.RESULT_URL_TEMPLATE.format(job_id=job_id))
        # Non-2xx may carry a JSON error body (e.g. 451 for prompt_unsafe).
        # Try to parse it; if that fails, surface a structured error.
        try:
            body = r.json()
        except Exception:
            body = None
        if r.status_code >= 400:
            if isinstance(body, dict) and ("error_code" in body or "message" in body):
                return body
            return {"error_code": f"http_{r.status_code}", "message": (r.text or "")[:500]}
        return body if body is not None else {}

    def wait_for(self, job_id: str, timeout_s: int = POLL_TIMEOUT_S) -> dict:
        t0 = time.time()
        while True:
            try:
                resp = self.poll_once(job_id)
            except Exception as e:
                return {"status": "failed", "error_code": "poll_exception", "error_message": str(e)[:500],
                        "model_seed": None, "presigned_url": None, "image_id": None,
                        "rewritten_prompt": None, "rewritten_negative_prompt": None}
            parsed = self.cm.parse_result(resp)
            if parsed["status"] in ("done", "failed"):
                return parsed
            if time.time() - t0 > timeout_s:
                return {"status": "failed", "error_code": "timeout", "error_message": f"poll timeout after {timeout_s}s",
                        "model_seed": None, "presigned_url": None, "image_id": None,
                        "rewritten_prompt": None, "rewritten_negative_prompt": None}
            time.sleep(POLL_INTERVAL_S)

    def close(self):
        self.client.close()


# ---------- per-task worker ----------

def _run_one_attempt(client: Client, prompt_row: dict, seed: int, images_dir: Path) -> dict:
    """Single attempt at a (prompt, seed) generation. Returns CSV-ready row."""
    payload = client.cm.build_payload(
        prompt=prompt_row["prompt"],
        seed=seed,
        aspect_ratio=prompt_row["aspect_ratio"],
    )

    row = {
        "prompt_id": prompt_row["id"],
        "category": prompt_row["category"],
        "aspect_ratio": prompt_row["aspect_ratio"],
        "original_prompt": prompt_row["prompt"],
        "input_seed": seed,
        "model_seed": "",
        "image_filename": "",
        "s3_image_uri": "",
        "rewritten_prompt": "",
        "rewritten_negative_prompt": "",
        "status": "",
        "error_code": "",
        "error_message": "",
    }

    try:
        job_id = client.submit(payload)
    except AuthError as e:
        row["status"] = "failed"
        row["error_code"] = "auth_failed"
        row["error_message"] = str(e)[:500]
        return row
    except Exception as e:
        row["status"] = "failed"
        row["error_code"] = "submit_error"
        row["error_message"] = str(e)[:500]
        return row

    parsed = client.wait_for(job_id)
    row["status"] = parsed["status"]
    if parsed["status"] != "done":
        row["error_code"] = parsed.get("error_code") or ""
        row["error_message"] = (parsed.get("error_message") or "")[:500]
        return row

    model_seed = parsed["model_seed"]
    row["model_seed"] = model_seed
    row["rewritten_prompt"] = parsed.get("rewritten_prompt") or ""
    row["rewritten_negative_prompt"] = parsed.get("rewritten_negative_prompt") or ""

    fname = f"prompt{prompt_row['id']}_seed{model_seed}.png"
    row["image_filename"] = fname
    local_path = images_dir / fname

    try:
        with httpx.Client(timeout=60, headers={"user-agent": "Mozilla/5.0"}) as c:
            with c.stream("GET", parsed["presigned_url"]) as resp:
                resp.raise_for_status()
                with open(local_path, "wb") as f:
                    for chunk in resp.iter_bytes(64 * 1024):
                        f.write(chunk)
    except Exception as e:
        row["status"] = "failed"
        row["error_code"] = "download_error"
        row["error_message"] = str(e)[:500]
        return row

    return row


def run_one(client: Client, prompt_row: dict, seed: int, images_dir: Path,
            max_retries: int = DEFAULT_TASK_RETRIES) -> dict:
    """Run one task with retries on transient errors. Never retries prompt_unsafe / http_4xx."""
    last_row = None
    for attempt in range(max_retries + 1):
        row = _run_one_attempt(client, prompt_row, seed, images_dir)
        last_row = row
        if row["status"] == "done":
            return row
        if row.get("error_code") not in RETRYABLE_ERROR_CODES:
            return row
        if attempt < max_retries:
            time.sleep(TASK_RETRY_BACKOFF_S * (attempt + 1))
    return last_row


# ---------- S3 upload ----------

def aws_env() -> dict:
    """Load creds from ~/Downloads/creds.txt (key=value format)."""
    creds_path = Path.home() / "Downloads" / "creds.txt"
    if not creds_path.exists():
        raise FileNotFoundError(f"Missing {creds_path}. Refresh at https://foundry-aws-corp.adobe.io/")
    env = os.environ.copy()
    for line in creds_path.read_text().splitlines():
        line = line.strip()
        if not line or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.upper()] = v.strip()
    return env


def s3_upload_dir(local_dir: Path, s3_uri: str, region: str) -> None:
    """aws s3 sync local_dir -> s3_uri, retrying on transient failures.

    sync is idempotent (it skips already-present matching files), so it is safe
    to loop until all files are uploaded.
    """
    env = aws_env()
    env["AWS_MAX_ATTEMPTS"] = "10"
    env["AWS_RETRY_MODE"] = "adaptive"
    last_err = None
    for attempt in range(1, S3_UPLOAD_ATTEMPTS + 1):
        r = subprocess.run(
            ["aws", "s3", "sync", str(local_dir), s3_uri, "--region", region,
             "--cli-read-timeout", "300", "--cli-connect-timeout", "30",
             "--no-progress"],
            env=env, capture_output=True, text=True,
        )
        if r.returncode == 0 and "upload failed" not in r.stderr:
            return
        last_err = (r.stderr or "")[-1000:]
        if attempt < S3_UPLOAD_ATTEMPTS:
            print(f"  [s3 sync attempt {attempt} had failures, retrying in {S3_UPLOAD_BACKOFF_S * attempt}s]")
            time.sleep(S3_UPLOAD_BACKOFF_S * attempt)
    raise RuntimeError(f"aws s3 sync failed after {S3_UPLOAD_ATTEMPTS} attempts. Last stderr:\n{last_err}")


def s3_upload_file(local_path: Path, s3_uri: str, region: str, content_type: str | None = None) -> None:
    env = aws_env()
    env["AWS_MAX_ATTEMPTS"] = "10"
    env["AWS_RETRY_MODE"] = "adaptive"
    cmd = ["aws", "s3", "cp", str(local_path), s3_uri, "--region", region,
           "--cli-read-timeout", "300", "--cli-connect-timeout", "30"]
    if content_type:
        cmd += ["--content-type", content_type]
    last_err = None
    for attempt in range(1, S3_UPLOAD_ATTEMPTS + 1):
        r = subprocess.run(cmd, env=env, capture_output=True, text=True)
        if r.returncode == 0:
            return
        last_err = (r.stderr or "")[-500:]
        if attempt < S3_UPLOAD_ATTEMPTS:
            time.sleep(S3_UPLOAD_BACKOFF_S * attempt)
    raise RuntimeError(f"aws s3 cp {local_path} failed after {S3_UPLOAD_ATTEMPTS} attempts. Last stderr:\n{last_err}")


def s3_download_file(s3_uri: str, local_path: Path, region: str) -> None:
    env = aws_env()
    env["AWS_MAX_ATTEMPTS"] = "10"
    env["AWS_RETRY_MODE"] = "adaptive"
    subprocess.run(
        ["aws", "s3", "cp", s3_uri, str(local_path), "--region", region,
         "--cli-read-timeout", "300", "--cli-connect-timeout", "30"],
        env=env, check=True, capture_output=True, text=True,
    )


# ---------- HTML gallery (IMS-auth, dark theme, multi-file) ----------

GALLERY_TEMPLATE_DIR = Path(__file__).parent / "gallery_template"


def write_gallery(gallery_dir: Path, rows: list[dict], title: str, subtitle: str) -> None:
    """Stage the 5-file IMS gallery in gallery_dir.

    Static files (index.html, imsauth.js, style.css, main.js) come verbatim from
    gallery_template/. The data.js is generated per-run from rows.
    """
    gallery_dir.mkdir(parents=True, exist_ok=True)

    # Copy static files
    for name in ("imsauth.js", "style.css", "main.js"):
        shutil.copy2(GALLERY_TEMPLATE_DIR / name, gallery_dir / name)

    # index.html with title/subtitle baked in
    html = (GALLERY_TEMPLATE_DIR / "index.html").read_text()
    html = html.replace("__TITLE__", _esc(title)).replace("__SUBTITLE__", _esc(subtitle))
    (gallery_dir / "index.html").write_text(html)

    # Group rows by prompt_id for data.js
    by_prompt: dict[str, list[dict]] = {}
    for r in rows:
        by_prompt.setdefault(str(r["prompt_id"]), []).append(r)

    prompts_payload = []
    for pid, items in sorted(by_prompt.items(), key=lambda kv: int(kv[0]) if str(kv[0]).isdigit() else 0):
        prompts_payload.append({
            "pid": pid,
            "category": items[0]["category"],
            "ar": items[0]["aspect_ratio"],
            "original_prompt": items[0]["original_prompt"],
            "rows": [{
                "input_seed": r["input_seed"],
                "model_seed": r["model_seed"],
                "image_filename": r["image_filename"],
                "rewritten_prompt": r["rewritten_prompt"] or "",
                "rewritten_negative_prompt": r["rewritten_negative_prompt"] or "",
                "status": r["status"],
                "error_code": r["error_code"] or "",
                "error_message": r["error_message"] or "",
            } for r in sorted(items, key=lambda x: int(x["input_seed"]))],
        })

    n_done = sum(1 for r in rows if r["status"] == "done")
    payload = {
        "meta": {
            "title": title,
            "subtitle": subtitle,
            "total_rows": len(rows),
            "n_done": n_done,
            "n_failed": len(rows) - n_done,
        },
        "prompts": prompts_payload,
    }
    (gallery_dir / "data.js").write_text(
        "const GALLERY_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n"
    )


def _esc(s: str) -> str:
    if s is None:
        return ""
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&#39;"))


# ---------- main ----------

CSV_FIELDNAMES = ["prompt_id", "category", "aspect_ratio", "original_prompt",
                  "input_seed", "model_seed", "image_filename", "s3_image_uri",
                  "rewritten_prompt", "rewritten_negative_prompt",
                  "status", "error_code", "error_message"]


def load_results_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_results_csv(path: Path, rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        w.writeheader()
        for r in rows:
            w.writerow({k: str(r.get(k, "")) for k in CSV_FIELDNAMES})


def execute_tasks(tasks: list[tuple], client: Client, images_dir: Path,
                  workers: int, max_retries: int, desc: str) -> list[dict]:
    """Run (prompt_row, seed) tasks in parallel. Returns list of row dicts."""
    rows: list[dict] = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(run_one, client, p, s, images_dir, max_retries): (p, s) for (p, s) in tasks}
        for f in tqdm(as_completed(futs), total=len(futs), desc=desc):
            p, s = futs[f]
            try:
                rows.append(f.result())
            except Exception as e:
                rows.append({
                    "prompt_id": p["id"], "category": p["category"], "aspect_ratio": p["aspect_ratio"],
                    "original_prompt": p["prompt"], "input_seed": s,
                    "model_seed": "", "image_filename": "", "s3_image_uri": "",
                    "rewritten_prompt": "", "rewritten_negative_prompt": "",
                    "status": "failed", "error_code": "worker_exception",
                    "error_message": str(e)[:500],
                })
    return rows


def write_run_info(info_path: Path, *, customer: str, prompt_set: str, prompts_csv: str,
                   seeds: list[int], n_prompts: int, rows: list[dict],
                   endpoint: str, folder: str, s3_uri_root: str,
                   extra_lines: list[str] | None = None) -> None:
    n_done = sum(1 for r in rows if r["status"] == "done")
    body = [
        f"customer:      {customer}",
        f"prompt_set:    {prompt_set}",
        f"prompts_csv:   {prompts_csv}",
        f"seeds:         {seeds}",
        f"n_prompts:     {n_prompts}",
        f"n_generations: {len(rows)}",
        f"n_done:        {n_done}",
        f"n_failed:      {len(rows) - n_done}",
        f"endpoint:      {endpoint}",
        f"timestamp_utc: {dt.datetime.utcnow().isoformat()}Z",
        f"run_folder:    {folder}",
        f"s3_uri_root:   {s3_uri_root}",
    ]
    if extra_lines:
        body.extend(extra_lines)
    info_path.write_text("\n".join(body) + "\n")


def upload_run_to_s3(out_dir: Path, s3_uri_root: str, region: str) -> None:
    images_dir = out_dir / "images"
    gallery_dir = out_dir / "gallery"
    csv_path = out_dir / "results.csv"
    info_path = out_dir / "run_info.txt"
    print(f"  syncing images -> {s3_uri_root}/images/ ...")
    s3_upload_dir(images_dir, f"{s3_uri_root}/images/", region)
    print(f"  uploading csv + run_info + gallery ...")
    s3_upload_file(csv_path,  f"{s3_uri_root}/results.csv",  region, "text/csv")
    s3_upload_file(info_path, f"{s3_uri_root}/run_info.txt", region, "text/plain")
    s3_upload_file(gallery_dir / "index.html", f"{s3_uri_root}/gallery/index.html", region, "text/html")
    s3_upload_file(gallery_dir / "style.css",  f"{s3_uri_root}/gallery/style.css",  region, "text/css")
    s3_upload_file(gallery_dir / "imsauth.js", f"{s3_uri_root}/gallery/imsauth.js", region, "application/javascript")
    s3_upload_file(gallery_dir / "main.js",    f"{s3_uri_root}/gallery/main.js",    region, "application/javascript")
    s3_upload_file(gallery_dir / "data.js",    f"{s3_uri_root}/gallery/data.js",    region, "application/javascript")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--customer", required=True, help="Customer module name in customers/ (e.g. humain_t2i)")
    ap.add_argument("--prompts-csv", default="", help="Required for a fresh run. Optional for --retry-failed-from.")
    ap.add_argument("--token-file", default="/tmp/auth_token.txt")
    ap.add_argument("--seeds", default="333,777")
    ap.add_argument("--limit", type=int, default=0, help="0 = no limit")
    ap.add_argument("--skip-ids", default="", help="Comma-separated prompt IDs to skip")
    ap.add_argument("--ids", default="", help="Comma-separated prompt IDs to include (overrides --limit)")
    ap.add_argument("--run-name", default="", help="Optional suffix in the run folder name")
    ap.add_argument("--prompt-set-name", default="", help="Defaults to CSV stem")
    ap.add_argument("--out-dir", default="", help="Local output dir; default: ./runs/<folder>")
    ap.add_argument("--no-upload", action="store_true", help="Skip S3 upload")
    ap.add_argument("--workers", type=int, default=MAX_WORKERS)
    ap.add_argument("--retries", type=int, default=DEFAULT_TASK_RETRIES,
                    help="Per-task retry attempts on transient errors (default 2 = up to 3 total tries)")
    ap.add_argument("--retry-failed-from", default="",
                    help="Path to a previous run dir (or its results.csv). Re-runs only retryable failures, "
                         "merges results back, and re-uploads to the same S3 prefix.")
    args = ap.parse_args()

    sys.path.insert(0, str(Path(__file__).parent))
    customer_mod = importlib.import_module(f"customers.{args.customer}")

    token = Path(args.token_file).read_text().strip()
    if token.lower().startswith("bearer "):
        token = token[7:].strip()

    check_token_expiry(token, args.token_file)

    if args.retry_failed_from:
        return _main_retry(args, customer_mod, token)

    if not args.prompts_csv:
        raise SystemExit("--prompts-csv is required for a fresh run")

    prompts = load_prompts(args.prompts_csv)
    if args.ids:
        wanted = [x.strip() for x in args.ids.split(",") if x.strip()]
        by_id = {str(p["id"]): p for p in prompts}
        missing = [i for i in wanted if i not in by_id]
        if missing:
            raise SystemExit(f"unknown prompt ids: {missing}")
        prompts = [by_id[i] for i in wanted]
    else:
        skip = {x.strip() for x in args.skip_ids.split(",") if x.strip()}
        if skip:
            prompts = [p for p in prompts if str(p["id"]) not in skip]
        if args.limit:
            prompts = prompts[: args.limit]

    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]

    prompt_set = args.prompt_set_name or Path(args.prompts_csv).stem
    today = dt.date.today().isoformat()
    folder = f"{today}_{prompt_set}"
    if args.run_name:
        folder += f"_{args.run_name}"

    out_dir = Path(args.out_dir) if args.out_dir else Path(__file__).parent / "runs" / folder
    images_dir = out_dir / "images"
    gallery_dir = out_dir / "gallery"
    out_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)
    gallery_dir.mkdir(parents=True, exist_ok=True)

    print(f"out_dir = {out_dir}")
    print(f"prompts = {len(prompts)}  seeds = {seeds}  -> {len(prompts)*len(seeds)} generations")
    print(f"per-task retries on transient errors: {args.retries}")

    tasks = [(p, s) for p in prompts for s in seeds]

    client = Client(token, customer_mod)
    try:
        rows = execute_tasks(tasks, client, images_dir, args.workers, args.retries, "generating")
    finally:
        client.close()

    rows.sort(key=lambda r: (int(r["prompt_id"]) if str(r["prompt_id"]).isdigit() else 0, int(r["input_seed"])))

    s3_prefix = f"{customer_mod.S3_ROOT_PREFIX}/{folder}"
    s3_bucket = customer_mod.S3_BUCKET
    s3_uri_root = f"s3://{s3_bucket}/{s3_prefix}"

    for r in rows:
        if r["status"] == "done":
            r["s3_image_uri"] = f"{s3_uri_root}/images/{r['image_filename']}"

    csv_path = out_dir / "results.csv"
    write_results_csv(csv_path, rows)

    info_path = out_dir / "run_info.txt"
    write_run_info(info_path, customer=args.customer, prompt_set=prompt_set,
                   prompts_csv=args.prompts_csv, seeds=seeds, n_prompts=len(prompts),
                   rows=rows, endpoint=customer_mod.ENDPOINT_URL, folder=folder,
                   s3_uri_root=s3_uri_root)

    n_done = sum(1 for r in rows if r["status"] == "done")
    title = f"{prompt_set} — {folder}"
    subtitle = f"{s3_bucket} / {s3_prefix}  •  {n_done}/{len(rows)} done"
    write_gallery(gallery_dir, rows, title=title, subtitle=subtitle)

    print(f"local: {out_dir}")
    print(f"  CSV:     {csv_path}")
    print(f"  images:  {images_dir} ({len(list(images_dir.glob('*.png')))} files)")
    print(f"  gallery: {gallery_dir}/index.html")
    print(f"  info:    {info_path}")

    if args.no_upload:
        print("[--no-upload] skipping S3 upload")
        return

    print(f"\nuploading to {s3_uri_root}/ ...")
    upload_run_to_s3(out_dir, s3_uri_root, customer_mod.AWS_REGION)

    gallery_url = f"https://foundry-aws-corp.adobe.io/asset/{s3_bucket}/{s3_prefix}/gallery/index.html"
    print(f"\nDone. Gallery: {gallery_url}")
    print(f"     S3 root: {s3_uri_root}/")


# ---------- retry-failed mode ----------

def _resolve_retry_target(target: str) -> tuple[Path, Path]:
    """Accept either a run dir or its results.csv. Returns (out_dir, csv_path)."""
    p = Path(target)
    if p.is_dir():
        csv_path = p / "results.csv"
    elif p.is_file() and p.name == "results.csv":
        csv_path = p
        p = p.parent
    else:
        raise SystemExit(f"--retry-failed-from must be a run dir or its results.csv. Got: {target}")
    if not csv_path.exists():
        raise SystemExit(f"no results.csv found at {csv_path}")
    return p, csv_path


def _main_retry(args, customer_mod, token: str) -> None:
    out_dir, csv_path = _resolve_retry_target(args.retry_failed_from)
    images_dir = out_dir / "images"
    gallery_dir = out_dir / "gallery"
    images_dir.mkdir(parents=True, exist_ok=True)
    gallery_dir.mkdir(parents=True, exist_ok=True)

    prev_rows = load_results_csv(csv_path)
    if not prev_rows:
        raise SystemExit(f"results.csv is empty at {csv_path}")

    # Index previous rows by (prompt_id, input_seed) for merge
    prev_index = {(r["prompt_id"], str(r["input_seed"])): r for r in prev_rows}

    retry_tasks: list[tuple[dict, int]] = []
    for r in prev_rows:
        if r["status"] == "done":
            continue
        ec = r.get("error_code") or ""
        if ec not in RETRYABLE_ERROR_CODES:
            continue  # e.g. prompt_unsafe — permanent
        prompt_row = {
            "id": r["prompt_id"],
            "category": r.get("category", ""),
            "prompt": r["original_prompt"],
            "aspect_ratio": r.get("aspect_ratio") or "1:1",
        }
        try:
            seed = int(r["input_seed"])
        except (TypeError, ValueError):
            continue
        retry_tasks.append((prompt_row, seed))

    if not retry_tasks:
        print(f"No retryable failures found in {csv_path}. Nothing to do.")
        return

    folder = out_dir.name
    s3_prefix = f"{customer_mod.S3_ROOT_PREFIX}/{folder}"
    s3_bucket = customer_mod.S3_BUCKET
    s3_uri_root = f"s3://{s3_bucket}/{s3_prefix}"

    print(f"retry mode: {csv_path}")
    print(f"  out_dir   = {out_dir}")
    print(f"  retrying  = {len(retry_tasks)} task(s)  (of {len(prev_rows)} total rows)")
    print(f"  s3 prefix = {s3_uri_root}")
    print(f"  per-task retries on transient errors: {args.retries}")

    client = Client(token, customer_mod)
    try:
        new_rows = execute_tasks(retry_tasks, client, images_dir, args.workers, args.retries, "retrying")
    finally:
        client.close()

    # Merge new_rows into prev_rows by (prompt_id, input_seed)
    n_recovered = 0
    for nr in new_rows:
        key = (str(nr["prompt_id"]), str(nr["input_seed"]))
        if key not in prev_index:
            continue
        old = prev_index[key]
        # Preserve category/aspect_ratio/original_prompt from the previous row
        # (they should match, but the previous row is authoritative).
        nr["category"] = old.get("category", nr.get("category", ""))
        nr["aspect_ratio"] = old.get("aspect_ratio", nr.get("aspect_ratio", ""))
        nr["original_prompt"] = old.get("original_prompt", nr.get("original_prompt", ""))
        if nr["status"] == "done":
            nr["s3_image_uri"] = f"{s3_uri_root}/images/{nr['image_filename']}"
            n_recovered += 1
        # Replace the row in prev_index (we'll rebuild the full list at the end)
        prev_index[key] = nr

    # Rebuild ordered rows preserving original order
    merged_rows = [prev_index[(r["prompt_id"], str(r["input_seed"]))] for r in prev_rows]

    # Persist
    write_results_csv(csv_path, merged_rows)

    seeds_sorted = sorted({int(r["input_seed"]) for r in merged_rows if str(r.get("input_seed", "")).lstrip("-").isdigit()})
    n_prompts = len({r["prompt_id"] for r in merged_rows})
    n_done = sum(1 for r in merged_rows if r["status"] == "done")

    info_path = out_dir / "run_info.txt"
    write_run_info(
        info_path,
        customer=args.customer,
        prompt_set=folder,  # folder name carries the prompt_set; preserve it
        prompts_csv=str(csv_path),
        seeds=seeds_sorted,
        n_prompts=n_prompts,
        rows=merged_rows,
        endpoint=customer_mod.ENDPOINT_URL,
        folder=folder,
        s3_uri_root=s3_uri_root,
        extra_lines=[
            f"retry_at_utc:  {dt.datetime.utcnow().isoformat()}Z",
            f"retried_tasks: {len(retry_tasks)}",
            f"recovered:     {n_recovered}",
        ],
    )

    title = f"{folder} — retry"
    subtitle = f"{s3_bucket} / {s3_prefix}  •  {n_done}/{len(merged_rows)} done  •  retry recovered +{n_recovered}"
    write_gallery(gallery_dir, merged_rows, title=title, subtitle=subtitle)

    print(f"\nmerged: {n_recovered} previously-failed tasks now done.")
    print(f"  total: {n_done}/{len(merged_rows)} done")
    print(f"  CSV:   {csv_path}")

    if args.no_upload:
        print("[--no-upload] skipping S3 upload")
        return

    print(f"\nuploading to {s3_uri_root}/ ...")
    upload_run_to_s3(out_dir, s3_uri_root, customer_mod.AWS_REGION)

    gallery_url = f"https://foundry-aws-corp.adobe.io/asset/{s3_bucket}/{s3_prefix}/gallery/index.html"
    print(f"\nDone. Gallery: {gallery_url}")
    print(f"     S3 root: {s3_uri_root}/")


if __name__ == "__main__":
    main()
