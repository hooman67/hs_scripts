#!/usr/bin/env python3
"""Prep a tiny test set for eval_hub upload.

Parses the Humain prompts gallery HTML, takes the first N prompts and the first
K variations per prompt, downloads the images, and writes them to
Humain/inference/assets/ as row{i}_img{j}.png plus a prompts file.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import boto3

HERE = Path(__file__).parent
HTML_PATH = Path("/tmp/eval_hub_index.html")
S3_BUCKET = "foundry-humain-default-adobe-assets"
S3_PREFIX = "experiments/h06/colligo/22-apr/humain_prompts/"
CREDS_PATH = Path("/Users/hshariati/Downloads/creds.txt")
PROMPTS_OUT = HERE / "Humain" / "humain_eval_set.txt"
ASSETS_DIR = HERE / "Humain" / "inference" / "assets"


def load_creds() -> dict:
    out = {}
    for line in CREDS_PATH.read_text().splitlines():
        if "=" in line:
            k, _, v = line.partition("=")
            out[k.strip()] = v.strip()
    return out


def make_s3_client():
    c = load_creds()
    return boto3.client(
        "s3",
        aws_access_key_id=c["aws_access_key_id"],
        aws_secret_access_key=c["aws_secret_access_key"],
        aws_session_token=c.get("aws_session_token"),
        region_name="us-west-2",
    )

NUM_PROMPTS = int(sys.argv[1]) if len(sys.argv) > 1 else 3
NUM_VARIATIONS = int(sys.argv[2]) if len(sys.argv) > 2 else 2


def parse_rows(html: str):
    rows = []
    tr_re = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
    prompt_re = re.compile(r'<td class="prompt">(.*?)</td>', re.S)
    img_re = re.compile(r'<img src="([^"]+\.png)"', re.S)
    for tr in tr_re.findall(html):
        pm = prompt_re.search(tr)
        if not pm:
            continue
        prompt = re.sub(r"\s+", " ", pm.group(1)).strip()
        filenames = img_re.findall(tr)
        if not filenames:
            continue
        rows.append((prompt, filenames))
    return rows


def main() -> None:
    html = HTML_PATH.read_text()
    rows = parse_rows(html)
    print(f"Parsed {len(rows)} rows from HTML.")

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    PROMPTS_OUT.parent.mkdir(parents=True, exist_ok=True)
    s3 = make_s3_client()

    selected_prompts = []
    for i in range(min(NUM_PROMPTS, len(rows))):
        prompt, filenames = rows[i]
        selected_prompts.append(prompt)
        for j in range(min(NUM_VARIATIONS, len(filenames))):
            key = S3_PREFIX + filenames[j]
            dest = ASSETS_DIR / f"row{i}_img{j}.png"
            print(f"  row {i} var {j}: s3://{S3_BUCKET}/{key} -> {dest.name}")
            s3.download_file(S3_BUCKET, key, str(dest))

    PROMPTS_OUT.write_text("\n".join(selected_prompts) + "\n")
    print(f"\nWrote {len(selected_prompts)} prompts to {PROMPTS_OUT}")
    print(f"Asset files in {ASSETS_DIR}:")
    for p in sorted(ASSETS_DIR.iterdir()):
        print(" ", p.name, p.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
