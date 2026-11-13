#!/usr/bin/env python3
"""Build and optionally upload the incremental PR 4403 control/treatment gallery."""

from __future__ import annotations

import argparse
import html
import json
import shutil
from pathlib import Path

import boto3

from common import atomic_json, sha256_file
from config import BUCKET, CONTROL_IMAGES, GATEWAY, JOB_ROOT, PREFIX, PROGRESS, RECORDS, REGION, REPORT_ROOT


def build() -> dict:
    progress = json.loads(PROGRESS.read_text()) if PROGRESS.is_file() else {"done": [], "total": 160}
    rows = []
    assets = REPORT_ROOT / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    for slug in progress.get("done", []):
        record = json.loads((RECORDS / f"{slug}.json").read_text())
        result = json.loads((JOB_ROOT / slug / "result.json").read_text())
        prop_details = json.loads((JOB_ROOT / slug / "prop_details.json").read_text())
        targets = {
            "control": (CONTROL_IMAGES / record["image_filename"], assets / f"{slug}__control.png"),
            "treatment": (JOB_ROOT / slug / "output.png", assets / f"{slug}__treatment.png"),
            "guide": (JOB_ROOT / slug / "guide.png", assets / f"{slug}__guide.png"),
        }
        for source, target in targets.values():
            if not target.is_file() or sha256_file(target) != sha256_file(source):
                shutil.copy2(source, target)
        rows.append({
            "slug": slug, "device": record["device_id"], "type": record["device_type"],
            "camera": record["camera_id"], "rank": record["bank_rank"], "environment": record["environment"],
            "prompt": record["prompt"], "final_prompt": result["prompt"],
            "prop_details": prop_details.get("generated", []),
            "control": f"assets/{slug}__control.png", "treatment": f"assets/{slug}__treatment.png",
            "guide": f"assets/{slug}__guide.png",
        })
    cards = []
    for row in rows:
        details = html.escape(json.dumps(row["prop_details"], indent=2, ensure_ascii=False))
        cards.append(f'''<article><h2>{html.escape(row['device'])} · {html.escape(row['camera'])} · rank {row['rank']}</h2>
<p><b>{html.escape(row['environment'])}</b> · <code>{html.escape(row['slug'])}</code></p>
<p class="prompt">{html.escape(row['prompt'])}</p>
<div class="images"><figure><img src="{row['control']}" loading="lazy"><figcaption>V6.1 control</figcaption></figure>
<figure><img src="{row['treatment']}" loading="lazy"><figcaption>PR 4403</figcaption></figure>
<figure><img src="{row['guide']}" loading="lazy"><figcaption>Frozen geometry guide</figcaption></figure></div>
<details><summary>Astra prop details</summary><pre>{details}</pre></details>
<details><summary>Final image prompt</summary><pre>{html.escape(row['final_prompt'])}</pre></details></article>''')
    document = f'''<!doctype html><meta charset="utf-8"><title>HP V6.1 · PR 4403 dynamic prop details</title>
<style>body{{font:15px system-ui;margin:24px;background:#f4f5f7;color:#18212f}}header,article{{background:white;border-radius:12px;padding:18px;margin:0 0 18px;box-shadow:0 1px 5px #0002}}h1{{margin:.2em 0}}h2{{margin:0 0 6px}}.images{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}figure{{margin:0}}img{{width:100%;border-radius:8px;background:#eee}}figcaption{{font-weight:700;margin-top:4px}}.prompt{{font-size:16px;line-height:1.45}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#f6f7f8;padding:12px;border-radius:8px}}@media(max-width:900px){{.images{{grid-template-columns:1fr}}}}</style>
<header><h1>HP V6.1 · PR 4403 dynamic prop details</h1><p>{len(rows)} / {progress.get('total',160)} generated. Frozen V6.1 control is shown beside the PR 4403 treatment. Rows are generated in device/view-interleaved order.</p></header>
{''.join(cards)}'''
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    (REPORT_ROOT / "index.html").write_text(document)
    atomic_json(REPORT_ROOT / "data.json", {"progress": progress, "rows": rows})
    summary = {"rows": len(rows), "total": progress.get("total", 160), "url": f"{GATEWAY}/gallery/index.html"}
    atomic_json(REPORT_ROOT / "build_summary.json", summary)
    return summary


def upload() -> None:
    client = boto3.client("s3", region_name=REGION)
    for path in sorted(REPORT_ROOT.rglob("*")):
        if path.is_file():
            key = f"{PREFIX}/gallery/{path.relative_to(REPORT_ROOT).as_posix()}"
            content_type = "text/html" if path.suffix == ".html" else "application/json" if path.suffix == ".json" else "image/png"
            client.upload_file(str(path), BUCKET, key, ExtraArgs={"ContentType": content_type})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upload", action="store_true")
    args = parser.parse_args()
    summary = build()
    if args.upload:
        upload()
        summary["uploaded"] = True
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
