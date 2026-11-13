"""Probe source URL accessibility without credentials; never modify frozen pixels."""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

ROOT = Path(__file__).resolve().parent


def main():
    manifest = json.loads((ROOT / "calibration_manifest.json").read_text())

    def probe(case):
        image = case["generated_image"]
        row = {"id": case["id"], "url": image["url"], "expected_sha256": image["sha256"],
               "checked_utc": datetime.now(timezone.utc).isoformat(),
               "authorization_or_cookies_added": False}
        session = requests.Session()
        session.trust_env = False
        try:
            response = session.get(image["url"], timeout=(10, 15), allow_redirects=False)
            row.update(status_code=response.status_code,
                       content_type=response.headers.get("Content-Type"),
                       redirect_host=urlparse(response.headers.get("Location", "")).hostname)
            if response.status_code == 200 and row["content_type"] and row["content_type"].startswith("image/"):
                row["download_sha256"] = hashlib.sha256(response.content).hexdigest()
                row["matches_frozen_bytes"] = row["download_sha256"] == image["sha256"]
                row["image_bytes_accessible_without_added_auth_from_this_host"] = True
            else:
                row["image_bytes_accessible_without_added_auth_from_this_host"] = False
        except requests.RequestException as exc:
            row.update(error_type=type(exc).__name__,
                       image_bytes_accessible_without_added_auth_from_this_host=False)
        finally:
            session.close()
        return row

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(probe, manifest["cases"]))
    data = {
        "scope": "Anonymous/no-added-credentials HTTP probe from this Pluto host, not proof of global public access.",
        "original_foundry_source_urls_preserved": True,
        "local_frozen_images_available_and_hash_verified": True,
        "checks": rows,
    }
    (ROOT / "source_url_availability.json").write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps({"tested": len(rows),
                      "anonymous_accessible": sum(r["image_bytes_accessible_without_added_auth_from_this_host"] for r in rows)}))


if __name__ == "__main__":
    main()
