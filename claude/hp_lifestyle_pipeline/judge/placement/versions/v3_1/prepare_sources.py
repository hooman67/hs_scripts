"""Retrieve the supplied viewer and only its three C-Tech anchors plus twins."""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[3]
BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = ("hp-data-artifacts/hp-3p-gpt25/"
          "hp16-v6prompt-v156-vs-v164-vs-v166-vs-v166noguide-v2-e2e32-20261106T181903Z")
BASE = f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/{PREFIX}/"
SOURCE = ROOT / "sources"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    SOURCE.mkdir(exist_ok=True)
    if (SOURCE / "manifest.json").exists():
        raise SystemExit("Source manifest exists; do not overwrite frozen evidence.")
    attempts = []
    try:
        response = requests.get(BASE + "viewer.html", timeout=20)
        response.raise_for_status()
        viewer = response.content
        attempts.append({"route": "https", "status": response.status_code})
    except requests.RequestException as exc:
        attempts.append({"route": "https", "error_type": type(exc).__name__})
        viewer = None
    (SOURCE / "retrieval_attempts.json").write_text(json.dumps(attempts, indent=2))

    # Invoke the shared workflow without changing any shared credential file.
    command = ["uv", "run", "--script",
               str(Path.home() / ".claude/scripts/foundry_aws_creds.py"), "--no-write"]
    result = subprocess.run(command, capture_output=True, text=True, timeout=100)
    try:
        broker = json.loads(result.stdout)
    except ValueError:
        broker = {}
    attempts.append({"route": "aws-creds --no-write",
                     "returncode": result.returncode, "ok": broker.get("ok", False),
                     "shared_credential_files_modified": False})
    (SOURCE / "retrieval_attempts.json").write_text(json.dumps(attempts, indent=2))

    import foundry_aws_gateway
    s3 = foundry_aws_gateway.maybe_s3_client(BUCKET)
    if s3 is None:
        raise RuntimeError("Approved gateway S3 client unavailable")
    attempts.append({"route": "documented_gateway_maybe_s3_client",
                     "credentials": "memory/cache only; never included in artifacts"})

    assets = []

    def fetch(relative, existing=None):
        key = f"{PREFIX}/{relative}"
        obj = s3.get_object(Bucket=BUCKET, Key=key)
        data = obj["Body"].read()
        if existing is not None and existing != data:
            raise RuntimeError("HTTPS and S3 live viewer bytes differ")
        destination = SOURCE / relative
        destination.parent.mkdir(exist_ok=True, parents=True)
        destination.write_bytes(data)
        entry = {
            "url": urljoin(BASE, relative), "s3_uri": f"s3://{BUCKET}/{key}",
            "local_path": str(destination), "sha256": digest(data), "bytes": len(data),
            "etag": obj.get("ETag"), "last_modified": obj["LastModified"].isoformat(),
            "content_type": obj.get("ContentType"),
        }
        assets.append(entry)
        return data, entry

    viewer, viewer_entry = fetch("viewer.html", viewer)
    soup = BeautifulSoup(viewer, "html.parser")
    rows = {section.find("h2").get_text(" ", strip=True): section
            for section in soup.find_all("section") if section.find("h2")}
    cases = []
    for row_id, indices in (
        ("07_cashmere_x_Front_Wide", [0, 3]),
        ("13_elitebook_13_Front_Left_Medium", [3]),
    ):
        section = rows[row_id]
        figures = section.find("div", class_="row").find_all("figure", recursive=False)
        if len(figures) != 4:
            raise ValueError(f"{row_id}: expected four ordered variants")
        twin_href = section.find("details", class_="in").find("a", href=True)["href"]
        twin_rel = urlparse(urljoin(BASE, twin_href)).path.split(f"/{PREFIX}/", 1)[1]
        _, twin = fetch(twin_rel)
        prompt = section.find("p", class_="req").get_text(" ", strip=True)
        if not prompt.startswith("User request:"):
            raise ValueError("Missing original user request")
        for index in indices:
            figure = figures[index]
            href = figure.find("a", href=True)["href"]
            relative = urlparse(urljoin(BASE, href)).path.split(f"/{PREFIX}/", 1)[1]
            _, image = fetch(relative)
            cases.append({
                "id": Path(relative).stem,
                "source_row": row_id,
                "variant": figure.find("figcaption").get_text(" ", strip=True),
                "column_index_0based": index,
                "generated_image": image, "twin_image": twin,
                "scene_prompt": prompt.removeprefix("User request:").strip(),
                "product_type": "laptop", "source_image_stage": "e2e_comparison_output",
                "claim_boundary": "Development anchor; out-of-domain for scene-stage V3.",
            })
    manifest = {
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "viewer": viewer_entry, "assets": assets, "cases": cases,
        "rightmost_resolution": "Fourth direct child figure in live row 13; caption and href preserved.",
    }
    (SOURCE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (SOURCE / "retrieval_attempts.json").write_text(json.dumps(attempts, indent=2))
    print(json.dumps({"cases": [{"id": c["id"], "variant": c["variant"],
                                "url": c["generated_image"]["url"]} for c in cases]}))


if __name__ == "__main__":
    main()
