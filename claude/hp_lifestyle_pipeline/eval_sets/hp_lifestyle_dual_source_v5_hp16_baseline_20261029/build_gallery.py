#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["boto3>=1.34"]
# ///
"""Build and optionally upload the HP16 V5 baseline review gallery."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import boto3


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
DEFAULT_STATE = PROJECT / "local_data/generation_runs/hp_lifestyle_dual_source_v5_hp16_baseline_20261029"
BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = "eval_sets/hp_lifestyle_dual_source_v5_hp16_baseline_20261029"
ASSET_BASE = f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/{PREFIX}"


def e(value: object) -> str:
    return html.escape(str(value), quote=True)


def asset_url(record: dict, name: str) -> str | None:
    info = record.get("artifacts", {}).get(name, {})
    uri = info.get("publication", {}).get("s3_uri")
    if not isinstance(uri, str):
        return None
    prefix = f"s3://{BUCKET}/"
    return f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/{uri.removeprefix(prefix)}"


def image_cell(url: str | None, label: str) -> str:
    if not url:
        return '<div class="missing">Not available</div>'
    return f'<a href="{e(url)}" target="_blank"><img loading="lazy" src="{e(url)}" alt="{e(label)}"></a>'


def detail(title: str, value: object) -> str:
    content = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)
    return f"<details><summary>{e(title)}</summary><pre>{e(content)}</pre></details>"


def build(records: list[dict], summary: dict) -> str:
    rows = []
    for record in records:
        task = record["task"]
        v5 = task["v5"]
        hero = asset_url(record, "1_hero_white.png")
        final = asset_url(record, "6_relight_3d.png")
        stage_links = []
        for name in record.get("artifacts", {}):
            url = asset_url(record, name)
            if url:
                stage_links.append(f'<a href="{e(url)}" target="_blank">{e(name)}</a>')
        metadata = (
            f"<div><strong>{e(v5['device_display_name'])}</strong></div>"
            f"<div>{e(task['digitalTwinId'])} · {e(task['cameraId'])}</div>"
            f"<div>rank {e(v5['rank'])} · {e(v5['environment'])}</div>"
            f"<div>source {e(v5['source_relevance_score'])} · C-Tech {e(v5['ctech_reference_score'])}</div>"
            f"<div class=\"status {e(record['status'])}\">{e(record['status'])}</div>"
        )
        prompt = f"<div class=\"prompt\">{e(task['prompt'])}</div>"
        debug = (
            detail("Prompt explanation", v5.get("explanation", ""))
            + detail("Smart brief", task["source_input"].get("smart_brief", ""))
            + detail("Source messaging", task["source_input"].get("source_messaging", ""))
            + detail("V5 prompt metadata", v5)
            + detail("HP16 request", record.get("request"))
            + detail("HP16 job manifest / debug", record.get("manifest"))
            + detail("Artifact hashes and publication", record.get("artifacts"))
            + (f'<div class="links">{" · ".join(stage_links)}</div>' if stage_links else "")
        )
        rows.append(
            "<tr>"
            f"<td>{metadata}</td>"
            f"<td>{image_cell(hero, 'digital twin')}</td>"
            f"<td>{prompt}</td>"
            f"<td>{image_cell(final, 'final relit generation')}</td>"
            f"<td>{debug}</td>"
            "</tr>"
        )
    status_text = ", ".join(f"{key}: {value}" for key, value in sorted(summary["status_counts"].items()))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>V5 top-96 · HP16 baseline</title>
<style>
:root{{--bg:#11151b;--panel:#18202a;--line:#334155;--text:#e5e7eb;--muted:#a7b0bf;--accent:#65a8ff}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--text);font:14px/1.45 system-ui,sans-serif}}
header{{position:sticky;top:0;z-index:3;background:#11151bf2;border-bottom:1px solid var(--line);padding:16px 20px}}
h1{{margin:0 0 5px;font-size:21px}} .meta{{color:var(--muted)}} .wrap{{padding:16px;overflow:auto}}
table{{border-collapse:separate;border-spacing:0;width:100%;min-width:1450px}} th{{position:sticky;top:82px;z-index:2;background:#202a36;text-align:left;padding:11px;border:1px solid var(--line)}}
td{{vertical-align:top;width:18%;padding:12px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);background:var(--panel)}}
td:first-child{{width:12%}} td:nth-child(3){{width:24%}} td:last-child{{width:28%}}
img{{display:block;width:100%;max-height:320px;object-fit:contain;background:#fff;border-radius:6px}} .prompt{{font-size:15px;white-space:pre-wrap}}
details{{border-top:1px solid var(--line);padding:7px 0}} summary{{cursor:pointer;color:var(--accent)}} pre{{white-space:pre-wrap;word-break:break-word;max-height:380px;overflow:auto;color:#d1d5db}}
.status{{margin-top:7px;display:inline-block;padding:2px 7px;border-radius:999px;background:#374151}} .status.complete{{background:#17613a}} .missing{{padding:30px;color:var(--muted)}}
.links{{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}} a{{color:var(--accent)}}
</style></head><body>
<header><h1>V5 top-96 · HP16 five-stage baseline</h1>
<div class="meta">{e(summary['tasks'])} frozen prompts · {e(status_text)} · endpoint rewriter: {e(summary['endpoint_catalog'].get('rewriterVersion'))} · generator: {e(summary['endpoint_catalog'].get('generator'))}</div></header>
<div class="wrap"><table><thead><tr><th>Device / view</th><th>Digital twin</th><th>Frozen V5 prompt</th><th>Final relit output</th><th>Inputs and debug</th></tr></thead><tbody>
{''.join(rows)}
</tbody></table></div></body></html>"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-root", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--no-upload", action="store_true")
    args = parser.parse_args()
    paths = sorted((args.state_root / "records").glob("*.json"))
    records = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    if not records:
        raise SystemExit("No generation records found")
    summary_path = args.state_root / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    statuses = Counter(record.get("status", "unknown") for record in records)
    summary["status_counts"] = dict(sorted(statuses.items()))
    output = HERE / "generated/gallery/index.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    content = build(records, summary)
    output.write_text(content, encoding="utf-8")
    manifest = {
        "as_of_utc": datetime.now(timezone.utc).isoformat(),
        "rows": len(records),
        "status_counts": dict(sorted(statuses.items())),
        "html_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "gallery_url": f"{ASSET_BASE}/gallery/index.html",
    }
    manifest_path = HERE / "generated/gallery_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    if not args.no_upload:
        client = boto3.client("s3", region_name="us-west-2")
        client.upload_file(str(output), BUCKET, f"{PREFIX}/gallery/index.html", ExtraArgs={"ContentType": "text/html"})
        client.upload_file(str(manifest_path), BUCKET, f"{PREFIX}/gallery_manifest.json", ExtraArgs={"ContentType": "application/json"})
        head = client.head_object(Bucket=BUCKET, Key=f"{PREFIX}/gallery/index.html")
        if head["ContentLength"] != output.stat().st_size:
            raise RuntimeError("gallery upload byte count mismatch")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
