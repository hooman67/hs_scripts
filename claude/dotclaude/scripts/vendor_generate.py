# /// script
# requires-python = ">=3.10"
# dependencies = ["boto3", "requests"]
# ///
"""Submit each row of a Foundry viz HTML to the Deccan Media Studio API
and produce a new viz HTML with the generated outputs added as a column.

Pipeline per row:
  1. Read source image URL + prompt from the HTML's `const DATA = [...]` array
  2. Presign the source S3 URL (vendor can't read foundry-aws-corp URLs)
  3. POST /v1/jobs  — submit one job, get job_id back
  4. Poll GET /v1/jobs/{id} until terminal status
  5. Download result_url, store on our S3 alongside the source HTML
  6. Record row state to state.jsonl (resumable)

After all rows finish, write a new HTML with thead extended by 'Generated'
and a `g` field on each row pointing at the new output image.

Usage:
    uv run --script vendor_generate.py <html_url_or_s3> <model_id> [options]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import boto3
import requests

FOUNDRY_PREFIX = "https://foundry-aws-corp.adobe.io/asset/"
DEFAULT_BASE_URL = "https://media-studio-core.platform.deccan.ai"
TERMINAL_STATUSES = frozenset({"complete", "failed", "cancelled"})


# ── URL helpers ──────────────────────────────────────────────────────────────


def url_to_s3(url: str) -> str:
    if url.startswith("s3://"):
        return url
    if url.startswith(FOUNDRY_PREFIX):
        return "s3://" + url[len(FOUNDRY_PREFIX):]
    raise ValueError(f"Unrecognized URL: {url}")


def parse_s3_uri(uri: str) -> tuple[str, str]:
    p = urlparse(uri)
    if p.scheme != "s3":
        raise ValueError(f"Not an s3:// URI: {uri}")
    return p.netloc, p.path.lstrip("/")


def s3_to_foundry(s3_uri: str) -> str:
    bucket, key = parse_s3_uri(s3_uri)
    return f"{FOUNDRY_PREFIX}{bucket}/{key}"


# ── HTML parsing ─────────────────────────────────────────────────────────────


def extract_data_array(html: str) -> tuple[list[dict], int, int]:
    """Return (data, start_index, end_index) of the JSON array literal."""
    m = re.search(r"const\s+DATA\s*=\s*", html)
    if not m:
        raise ValueError("Could not find `const DATA =` in HTML")
    start = m.end()
    data, consumed = json.JSONDecoder().raw_decode(html[start:])
    if not isinstance(data, list):
        raise ValueError("`const DATA` is not a JSON array")
    return data, start, start + consumed


def detect_keys(html: str) -> tuple[str, str]:
    """Auto-detect (image_key, prompt_key) by scanning JS `d.X` references."""
    image_key = None
    prompt_key = None
    for m in re.finditer(r"(\.src|\.textContent|\.innerText|\.innerHTML)\s*=\s*d\.(\w+)", html):
        attr, key = m.group(1), m.group(2)
        if attr == ".src" and image_key is None:
            image_key = key
        elif attr != ".src" and prompt_key is None:
            prompt_key = key
    if not image_key or not prompt_key:
        raise ValueError(f"Could not auto-detect keys (image={image_key}, prompt={prompt_key})")
    return image_key, prompt_key


def detect_output_key(html: str) -> str | None:
    """Find a `d.X` on .src that isn't the first image (i.e. the 'generated' slot)."""
    image_keys = []
    for m in re.finditer(r"\.src\s*=\s*d\.(\w+)", html):
        if m.group(1) not in image_keys:
            image_keys.append(m.group(1))
    return image_keys[1] if len(image_keys) >= 2 else None


# ── Deccan API ───────────────────────────────────────────────────────────────


@dataclass
class JobResult:
    row_idx: int
    source_url: str
    prompt: str
    status: str  # complete | failed | cancelled | submit_error
    job_id: str | None = None
    result_url: str | None = None  # vendor-side signed URL
    output_url: str | None = None  # our S3 (foundry-aws-corp URL)
    error: str | None = None
    cost_usd: float | None = None


def submit_job(session: requests.Session, base_url: str, modality: str,
               model_id: str, prompt: str, image_url: str, image_field: str) -> str:
    body = {
        "modality": modality,
        "model_ids": [model_id],
        "inputs": {"prompt": prompt, image_field: image_url},
    }
    r = session.post(f"{base_url}/v1/jobs", json=body, timeout=60)
    r.raise_for_status()
    return r.json()[0]["id"]


def poll_job(session: requests.Session, base_url: str, job_id: str,
             poll_interval: float, timeout: float) -> dict:
    deadline = time.time() + timeout
    while True:
        r = session.get(f"{base_url}/v1/jobs/{job_id}", timeout=30)
        r.raise_for_status()
        j = r.json()
        if j.get("status") in TERMINAL_STATUSES:
            return j
        if time.time() >= deadline:
            j["status"] = "failed"
            j["error_message"] = f"Client timeout after {timeout:.0f}s"
            return j
        time.sleep(poll_interval)


# ── Per-row worker ───────────────────────────────────────────────────────────


def process_row(
    row_idx: int,
    row: dict,
    image_key: str,
    prompt_key: str,
    *,
    session: requests.Session,
    s3,
    base_url: str,
    modality: str,
    model_id: str,
    image_field: str,
    output_bucket: str,
    output_prefix: str,
    presign_expiry: int,
    poll_interval: float,
    job_timeout: float,
) -> JobResult:
    src_url = row[image_key]
    prompt = row[prompt_key]
    rec = JobResult(row_idx=row_idx, source_url=src_url, prompt=prompt, status="failed")

    try:
        s3_uri = url_to_s3(src_url)
        bucket, key = parse_s3_uri(s3_uri)
        presigned = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=presign_expiry,
        )
    except Exception as e:
        rec.status = "submit_error"
        rec.error = f"presign failed: {e}"
        return rec

    try:
        job_id = submit_job(session, base_url, modality, model_id, prompt, presigned, image_field)
        rec.job_id = job_id
    except Exception as e:
        rec.status = "submit_error"
        rec.error = f"submit failed: {e}"
        return rec

    try:
        j = poll_job(session, base_url, job_id, poll_interval, job_timeout)
    except Exception as e:
        rec.status = "failed"
        rec.error = f"poll failed: {e}"
        return rec

    rec.status = j.get("status", "failed")
    rec.error = j.get("error_message")
    rec.cost_usd = j.get("total_cost")
    rec.result_url = j.get("result_url")

    if rec.status != "complete" or not rec.result_url:
        return rec

    # Download and store on our S3
    try:
        rr = requests.get(rec.result_url, timeout=120)
        rr.raise_for_status()
        ct = rr.headers.get("content-type", "image/png")
        ext = "jpg" if ("jpeg" in ct or "jpg" in ct) else ("mp4" if "mp4" in ct else "png")
        dest_key = f"{output_prefix}/outputs/{row_idx:06d}__{job_id}.{ext}"
        s3.put_object(Bucket=output_bucket, Key=dest_key, Body=rr.content, ContentType=ct)
        rec.output_url = s3_to_foundry(f"s3://{output_bucket}/{dest_key}")
    except Exception as e:
        rec.error = f"download/copy failed: {e}"
        rec.status = "failed"

    return rec


# ── State file ───────────────────────────────────────────────────────────────


class StateLog:
    def __init__(self, path: Path):
        self.path = path
        self._lock = threading.Lock()
        self._completed: dict[int, JobResult] = {}
        if path.exists():
            for line in path.read_text().splitlines():
                if not line.strip():
                    continue
                try:
                    d = json.loads(line)
                    self._completed[d["row_idx"]] = JobResult(**d)
                except Exception:
                    pass

    def has(self, row_idx: int) -> bool:
        return row_idx in self._completed

    def get(self, row_idx: int) -> JobResult | None:
        return self._completed.get(row_idx)

    def append(self, rec: JobResult) -> None:
        with self._lock:
            self._completed[rec.row_idx] = rec
            with self.path.open("a") as f:
                f.write(json.dumps(asdict(rec)) + "\n")


# ── Output HTML ──────────────────────────────────────────────────────────────


def build_output_html(src_html: str, data: list[dict], data_start: int, data_end: int,
                       output_col_label: str, output_key: str) -> str:
    """Return new HTML with thead extended, renderPage fixed, and DATA replaced."""
    new_data_js = json.dumps(data, separators=(",", ":"))
    out = src_html[:data_start] + new_data_js + src_html[data_end:]

    def add_th_to_thead(m: re.Match) -> str:
        thead_open, thead_inner, thead_close = m.group(1), m.group(2), m.group(3)
        new_inner = re.sub(r'(</tr>\s*)$', f'<th>{output_col_label}</th>\\1', thead_inner)
        if new_inner == thead_inner:
            new_inner = thead_inner + f'<th>{output_col_label}</th>'
        return thead_open + new_inner + thead_close

    out = re.sub(
        r'(<thead[^>]*>)(.*?)(</thead>)',
        add_th_to_thead,
        out,
        count=1,
        flags=re.DOTALL,
    )

    out = re.sub(
        r'(td3\.appendChild\([^)]+\);\s*)(tbody\.appendChild\(tr\);)',
        r'\1tr.appendChild(td3); \2',
        out,
    )

    return out


# ── Main ─────────────────────────────────────────────────────────────────────


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("html", help="Foundry viz HTML URL or s3:// URI")
    ap.add_argument("model_id", help="Vendor model_id (UUID or slug)")
    ap.add_argument("--modality", default="image_editing")
    ap.add_argument("--image-field", default="image_url",
                    help="Vendor input field name for the source image (default: image_url)")
    ap.add_argument("--api-key", default=None,
                    help="Media Studio API key (default: read from ~/Downloads/creds.txt)")
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--output-bucket", default=None,
                    help="Destination S3 bucket (default: source bucket)")
    ap.add_argument("--output-prefix", default=None,
                    help="Destination S3 prefix (default: alongside source HTML)")
    ap.add_argument("--output-html-name", default=None,
                    help="Output HTML key/name (default: <stem>__<model_id>.html)")
    ap.add_argument("--limit", type=int, default=None, help="Run only first N rows")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--poll-interval", type=float, default=5.0)
    ap.add_argument("--job-timeout", type=float, default=600.0)
    ap.add_argument("--presign-expiry", type=int, default=86400, help="Seconds (default: 24h)")
    ap.add_argument("--region", default="us-west-2")
    ap.add_argument("--image-key", default=None, help="Override auto-detected image key")
    ap.add_argument("--prompt-key", default=None, help="Override auto-detected prompt key")
    ap.add_argument("--output-key", default="g", help="Field name for the new output URL in DATA")
    ap.add_argument("--output-col-label", default="Generated")
    ap.add_argument("--resume", action="store_true",
                    help="Skip rows already in state.jsonl")
    ap.add_argument("--retry-failed", action="store_true",
                    help="Re-run rows previously marked failed/submit_error")
    ap.add_argument("--dry-run", action="store_true",
                    help="Plan only — list rows + paths, submit nothing")
    args = ap.parse_args()

    # ── Resolve API key ────────────────────────────────────────────────────
    api_key = args.api_key
    if not api_key:
        creds_path = Path.home() / "Downloads" / "creds.txt"
        if creds_path.exists():
            for line in creds_path.read_text().splitlines():
                m = re.match(r'\s*API_key\s*=\s*(\S+)', line)
                if m:
                    api_key = m.group(1)
                    break
    if not api_key:
        print("ERROR: --api-key not provided and not found in ~/Downloads/creds.txt", file=sys.stderr)
        return 2

    # ── Fetch source HTML ──────────────────────────────────────────────────
    s3 = boto3.client("s3", region_name=args.region)
    src_uri = url_to_s3(args.html)
    src_bucket, src_key = parse_s3_uri(src_uri)
    print(f"Reading {src_uri}", file=sys.stderr)
    body = s3.get_object(Bucket=src_bucket, Key=src_key)["Body"].read()
    src_html = body.decode("utf-8")
    src_stem = Path(src_key).stem

    # ── Parse ──────────────────────────────────────────────────────────────
    data, data_start, data_end = extract_data_array(src_html)
    image_key = args.image_key or detect_keys(src_html)[0]
    prompt_key = args.prompt_key or detect_keys(src_html)[1]
    output_key = args.output_key
    print(f"Rows: {len(data)}", file=sys.stderr)
    print(f"Image key:  {image_key!r}", file=sys.stderr)
    print(f"Prompt key: {prompt_key!r}", file=sys.stderr)
    print(f"Output key: {output_key!r}", file=sys.stderr)

    # ── Resolve output destination ─────────────────────────────────────────
    out_bucket = args.output_bucket or src_bucket
    if args.output_prefix:
        out_prefix = args.output_prefix.rstrip("/")
    else:
        # Place alongside source: <html_dir>/<stem>__<model>
        src_dir = str(Path(src_key).parent).replace("\\", "/")
        if src_dir == ".":
            src_dir = ""
        out_prefix = f"{src_dir}/{src_stem}__{args.model_id}".lstrip("/")
    out_html_key = (
        args.output_html_name
        if args.output_html_name
        else f"{out_prefix}.html"
    )
    state_key = f"{out_prefix}/state.jsonl"
    print(f"Output bucket: {out_bucket}", file=sys.stderr)
    print(f"Output prefix: {out_prefix}", file=sys.stderr)
    print(f"Output HTML:   s3://{out_bucket}/{out_html_key}", file=sys.stderr)
    print(f"State file:    s3://{out_bucket}/{state_key}", file=sys.stderr)

    # ── Limit + state ──────────────────────────────────────────────────────
    if args.limit is not None:
        data = data[: args.limit]
        print(f"--limit {args.limit}: processing {len(data)} rows", file=sys.stderr)

    state_local = Path(f"/tmp/{src_stem}__{args.model_id}_state.jsonl")
    # Pull existing state from S3 if --resume
    if args.resume or args.retry_failed:
        try:
            obj = s3.get_object(Bucket=out_bucket, Key=state_key)
            state_local.write_bytes(obj["Body"].read())
            print(f"Resumed state from s3://{out_bucket}/{state_key}", file=sys.stderr)
        except s3.exceptions.NoSuchKey:
            print(f"No prior state file — starting fresh", file=sys.stderr)
        except Exception as e:
            print(f"Could not load prior state ({e}); starting fresh", file=sys.stderr)
    elif state_local.exists():
        state_local.unlink()
    state = StateLog(state_local)

    # ── Decide which rows to run ───────────────────────────────────────────
    todo: list[int] = []
    skipped_complete = 0
    skipped_failed = 0
    for i in range(len(data)):
        prior = state.get(i)
        if prior is None:
            todo.append(i)
        elif prior.status == "complete":
            if args.retry_failed:
                # complete is good, keep it
                skipped_complete += 1
            elif args.resume:
                skipped_complete += 1
            else:
                todo.append(i)
        else:  # failed / submit_error / etc.
            if args.retry_failed:
                todo.append(i)
            elif args.resume:
                skipped_failed += 1  # still skip on plain --resume
            else:
                todo.append(i)
    print(f"To process: {len(todo)}  (skipped complete={skipped_complete}, "
          f"prior failed={skipped_failed})", file=sys.stderr)

    # ── Dry run ────────────────────────────────────────────────────────────
    if args.dry_run:
        print("\n--- DRY RUN (first 3 rows) ---", file=sys.stderr)
        for i in todo[:3]:
            print(f"  row {i}: src={data[i][image_key][:80]}  prompt={data[i][prompt_key][:80]}", file=sys.stderr)
        return 0

    # ── Run ────────────────────────────────────────────────────────────────
    session = requests.Session()
    session.headers.update({"X-API-Key": api_key, "Content-Type": "application/json"})

    started = time.time()
    done = 0
    failed = 0

    def run_one(i: int) -> JobResult:
        return process_row(
            i, data[i], image_key, prompt_key,
            session=session, s3=s3, base_url=args.base_url,
            modality=args.modality, model_id=args.model_id,
            image_field=args.image_field,
            output_bucket=out_bucket, output_prefix=out_prefix,
            presign_expiry=args.presign_expiry,
            poll_interval=args.poll_interval, job_timeout=args.job_timeout,
        )

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_one, i): i for i in todo}
        for fut in as_completed(futs):
            i = futs[fut]
            try:
                rec = fut.result()
            except Exception as e:
                rec = JobResult(row_idx=i, source_url=data[i].get(image_key, ""),
                                prompt=data[i].get(prompt_key, ""),
                                status="failed", error=f"unhandled: {e}")
            state.append(rec)
            done += 1
            if rec.status != "complete":
                failed += 1
            if done % 10 == 0 or done == len(todo):
                elapsed = time.time() - started
                rate = done / max(elapsed, 1)
                eta = (len(todo) - done) / max(rate, 0.001)
                print(f"  [{done}/{len(todo)}] failed={failed}  "
                      f"rate={rate:.2f}/s  eta={eta:.0f}s", file=sys.stderr)

    # ── Upload state file to S3 ────────────────────────────────────────────
    if state_local.exists():
        s3.upload_file(str(state_local), out_bucket, state_key,
                       ExtraArgs={"ContentType": "application/x-ndjson"})
        print(f"Uploaded state → s3://{out_bucket}/{state_key}", file=sys.stderr)

    # ── Build output HTML ──────────────────────────────────────────────────
    output_data = []
    for i, row in enumerate(data):
        rec = state.get(i)
        new_row = dict(row)
        if rec and rec.output_url:
            new_row[output_key] = rec.output_url
        output_data.append(new_row)

    out_html = build_output_html(
        src_html, output_data, data_start, data_end,
        args.output_col_label, output_key,
    )

    s3.put_object(Bucket=out_bucket, Key=out_html_key,
                  Body=out_html.encode("utf-8"), ContentType="text/html")
    print(f"\nUploaded HTML → s3://{out_bucket}/{out_html_key}", file=sys.stderr)
    print(f"View at: {FOUNDRY_PREFIX}{out_bucket}/{out_html_key}", file=sys.stderr)
    print(f"\nSummary: {done - failed}/{len(todo)} complete, {failed} failed", file=sys.stderr)

    print(f"{FOUNDRY_PREFIX}{out_bucket}/{out_html_key}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
