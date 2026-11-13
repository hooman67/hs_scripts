# /// script
# requires-python = ">=3.10"
# dependencies = ["boto3", "beautifulsoup4"]
# ///
"""
Convert a Foundry viz HTML into an Appen/Humain annotation CSV.

The script:
  1. Reads the HTML (from a foundry-aws-corp.adobe.io URL or an s3:// URI)
  2. Extracts the embedded `const DATA = [...]` array
  3. Auto-detects which fields are reference images, result images, and prompts
     using <th> column headers and the JS rendering code (`d.X` references)
  4. Copies every referenced image from its source bucket into
     s3://<dest-bucket>/<dest-prefix>/<html_stem>/{references,generated}/<basename>
  5. Writes a CSV with columns: asset_url, reference_url[_N], prompt
  6. Uploads the CSV next to the copied assets

Usage:
    uv run --script html_to_appen_csv.py <html_url_or_s3_uri> [options]
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

import boto3
from bs4 import BeautifulSoup

FOUNDRY_PREFIX = "https://foundry-aws-corp.adobe.io/asset/"


def url_to_s3(url: str) -> str:
    if url.startswith("s3://"):
        return url
    if url.startswith(FOUNDRY_PREFIX):
        return "s3://" + url[len(FOUNDRY_PREFIX):]
    raise ValueError(f"Unrecognized URL (expected s3:// or foundry-aws-corp URL): {url}")


def parse_s3_uri(uri: str) -> tuple[str, str]:
    p = urlparse(uri)
    if p.scheme != "s3":
        raise ValueError(f"Not an s3:// URI: {uri}")
    return p.netloc, p.path.lstrip("/")


def extract_data_array(html: str) -> list[dict]:
    m = re.search(r"const\s+DATA\s*=\s*", html)
    if not m:
        raise ValueError("Could not find `const DATA =` in HTML")
    start = m.end()
    data, _ = json.JSONDecoder().raw_decode(html[start:])
    if not isinstance(data, list):
        raise ValueError("`const DATA` is not a JSON array")
    return data


def extract_th_labels(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    return [th.get_text(strip=True) for th in soup.select("thead th")]


def detect_key_order(html: str) -> list[tuple[str, str]]:
    """Return [(key, type)] in JS appearance order. type ∈ {'image', 'text'}."""
    seen = []
    for m in re.finditer(r"(\.src|\.textContent|\.innerText|\.innerHTML)\s*=\s*d\.(\w+)", html):
        typ = "image" if m.group(1) == ".src" else "text"
        key = m.group(2)
        if (key, typ) not in seen:
            seen.append((key, typ))
    return seen


def classify_field(label: str, is_image: bool) -> str:
    l = label.lower()
    if is_image:
        if any(w in l for w in ("source", "input", "reference", "original", "before")):
            return "reference"
        if any(w in l for w in ("generated", "result", "output", "edited", "after", "ai")):
            return "result"
        return "reference"
    return "prompt"


def fetch_html(src: str, s3) -> tuple[str, str]:
    """Return (html_text, html_stem)."""
    if src.startswith(FOUNDRY_PREFIX) or src.startswith("s3://"):
        s3_uri = url_to_s3(src)
        bucket, key = parse_s3_uri(s3_uri)
        body = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
        return body.decode("utf-8"), Path(key).stem
    raise ValueError(f"Only s3:// and {FOUNDRY_PREFIX} URLs are supported; got {src}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("html", help="Foundry URL or s3:// URI for the viz HTML")
    ap.add_argument("--dest-bucket", default="foundry-appen-humain-enterprise")
    ap.add_argument("--dest-prefix", default="to_annotate")
    ap.add_argument("--local-out", default=None, help="Local path for the CSV")
    ap.add_argument("--region", default="us-west-2")
    ap.add_argument("--workers", type=int, default=16, help="Parallel S3 copy workers")
    ap.add_argument("--dry-run", action="store_true", help="Plan only; don't copy or write")
    ap.add_argument(
        "--reference-keys",
        default=None,
        help="Comma-separated DATA keys to treat as reference images (override auto-detect)",
    )
    ap.add_argument(
        "--result-key",
        default=None,
        help="DATA key to treat as the result/generated image (override auto-detect)",
    )
    ap.add_argument(
        "--prompt-keys",
        default=None,
        help="Comma-separated DATA keys to treat as prompt text (override auto-detect)",
    )
    args = ap.parse_args()

    s3 = boto3.client("s3", region_name=args.region)

    html, html_stem = fetch_html(args.html, s3)
    data = extract_data_array(html)
    th_labels = extract_th_labels(html)
    key_order = detect_key_order(html)

    print(f"HTML stem:    {html_stem}", file=sys.stderr)
    print(f"Rows:         {len(data)}", file=sys.stderr)
    print(f"TH labels:    {th_labels}", file=sys.stderr)
    print(f"Key order:    {key_order}", file=sys.stderr)

    # Auto-detect role per key using column header by position
    auto_ref: list[str] = []
    auto_result: list[str] = []
    auto_prompt: list[str] = []
    for i, (key, typ) in enumerate(key_order):
        label = th_labels[i] if i < len(th_labels) else key
        role = classify_field(label, typ == "image")
        if role == "reference":
            auto_ref.append(key)
        elif role == "result":
            auto_result.append(key)
        else:
            auto_prompt.append(key)

    # Apply CLI overrides
    ref_keys = args.reference_keys.split(",") if args.reference_keys else auto_ref
    result_keys = [args.result_key] if args.result_key else auto_result
    prompt_keys = args.prompt_keys.split(",") if args.prompt_keys else auto_prompt

    # If no result detected but multiple image keys, last image key → result
    if not result_keys:
        image_keys = [k for k, t in key_order if t == "image"]
        if len(image_keys) >= 2:
            result_keys = [image_keys[-1]]
            ref_keys = [k for k in image_keys[:-1] if k not in result_keys]
        elif len(image_keys) == 1:
            # Only one image — treat it as the result
            result_keys = image_keys
            ref_keys = []

    print(f"Reference:    {ref_keys}", file=sys.stderr)
    print(f"Result:       {result_keys}", file=sys.stderr)
    print(f"Prompt:       {prompt_keys}", file=sys.stderr)

    if not result_keys:
        print("ERROR: could not identify a result/asset image key", file=sys.stderr)
        return 2

    dest_base = f"{args.dest_prefix}/{html_stem}"
    copied: dict[str, str] = {}

    # Collect all (src_uri, role) pairs to copy, dedup by src_uri
    to_copy: dict[str, str] = {}  # s3_src -> role

    def queue(url: str, role: str):
        if not url:
            return
        s3_src = url_to_s3(url)
        to_copy.setdefault(s3_src, role)

    for row in data:
        for k in result_keys:
            if k in row:
                queue(row[k], "result")
        for k in ref_keys:
            if k in row:
                queue(row[k], "reference")

    print(f"Unique assets to copy: {len(to_copy)}", file=sys.stderr)

    def dest_uri_for(s3_src: str, role: str) -> str:
        _, src_key = parse_s3_uri(s3_src)
        folder = "references" if role == "reference" else "generated"
        dest_key = f"{dest_base}/{folder}/{os.path.basename(src_key)}"
        return f"s3://{args.dest_bucket}/{dest_key}"

    def do_copy(s3_src: str, role: str) -> tuple[str, str]:
        src_bucket, src_key = parse_s3_uri(s3_src)
        dest = dest_uri_for(s3_src, role)
        _, dest_key = parse_s3_uri(dest)
        s3.copy_object(
            CopySource={"Bucket": src_bucket, "Key": src_key},
            Bucket=args.dest_bucket,
            Key=dest_key,
        )
        return s3_src, dest

    if args.dry_run:
        for s3_src, role in to_copy.items():
            copied[s3_src] = dest_uri_for(s3_src, role)
    else:
        done = 0
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = [ex.submit(do_copy, s, r) for s, r in to_copy.items()]
            for fut in as_completed(futs):
                s3_src, dest = fut.result()
                copied[s3_src] = dest
                done += 1
                if done % 50 == 0 or done == len(to_copy):
                    print(f"  copied {done}/{len(to_copy)}", file=sys.stderr)

    # Build CSV
    num_refs = len(ref_keys)
    if num_refs == 0:
        ref_cols: list[str] = []
    elif num_refs == 1:
        ref_cols = ["reference_url"]
    else:
        ref_cols = [f"reference_url_{i+1}" for i in range(num_refs)]
    cols = ["asset_url"] + ref_cols + ["prompt"]

    rows_out = []
    for row in data:
        result_url = copied.get(url_to_s3(row[result_keys[0]]), "")
        ref_urls = [copied.get(url_to_s3(row[k]), "") for k in ref_keys]
        prompt = " | ".join(str(row[k]) for k in prompt_keys if k in row)
        rows_out.append([result_url] + ref_urls + [prompt])

    local_out = args.local_out or f"/tmp/{html_stem}_appen.csv"
    with open(local_out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(rows_out)

    print(f"\nLocal CSV:   {local_out}", file=sys.stderr)
    print(f"Dest folder: s3://{args.dest_bucket}/{dest_base}/", file=sys.stderr)

    if not args.dry_run:
        csv_key = f"{dest_base}/annotations.csv"
        s3.upload_file(local_out, args.dest_bucket, csv_key, ExtraArgs={"ContentType": "text/csv"})
        print(f"Uploaded CSV: s3://{args.dest_bucket}/{csv_key}", file=sys.stderr)

    print(local_out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
