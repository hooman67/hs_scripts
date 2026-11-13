"""Publish a presentation-only, input-banked view of the existing three experiments."""
from __future__ import annotations

import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit

HERE = Path(__file__).resolve().parent
PUBLIC = HERE / "public"
BUCKET = "foundry-hp-enterprise-adobe-assets"
GATEWAY = f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/"
PREFIX = "eval_sets/" + HERE.name
SOURCE_PREFIX = "eval_sets/hp_lifestyle_v6_3_full160_pr4523_pr4417_20261110"
SOURCE_URL = GATEWAY + SOURCE_PREFIX + "/gallery/index.html"
VIEWER_URL = GATEWAY + PREFIX + "/gallery/index.html"
TITLE = "HP lifestyle diversity - 16 inputs x 10 prompts x 3 experiments"
EXPERIMENTS = (
    ("v6_3_pr4417", "V6.3 / PR 4417 - V15.6", "prompt", "source_input"),
    ("v6_3_pr4523", "V6.3 / PR 4523 - V15.7 shapes", "prompt", "source_input"),
    ("v6_4_pr4523", "V6.4 / PR 4523 - V15.7 shapes", "prompt_v6_4", "source_input_v6_4"),
)


def load(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def emit(path, value):
    body = value if isinstance(value, bytes) else (
        json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode()
    path = Path(path)
    if path.exists():
        if path.read_bytes() != body:
            raise ValueError(f"refusing to overwrite saved evidence: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body)


def s3_client():
    helper = HERE.parent / "hp_lifestyle_v6_3_full160_pr4523_pr4417_20261110/s3_access.py"
    spec = importlib.util.spec_from_file_location("hp_grouped_s3_access", helper)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.s3_client()


def asset_key(url):
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or parsed.netloc != "foundry-aws-corp.adobe.io"
            or parsed.query or parsed.fragment or not parsed.path.startswith(f"/asset/{BUCKET}/")):
        raise ValueError("asset must be a same-origin HP gateway URL without tokens")
    return parsed.path.removeprefix(f"/asset/{BUCKET}/")


def relative_asset(value):
    import posixpath

    url = urljoin(SOURCE_URL, value)
    key = asset_key(url)
    return posixpath.relpath(key, PREFIX + "/gallery")


class SourceLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts = []
        self.styles = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "script" and attrs.get("src"):
            self.scripts.append(attrs["src"])
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.styles.append(attrs["href"])


def prepare():
    client = s3_client()
    objects = {}

    def fetch(relative, key):
        response = client.get_object(Bucket=BUCKET, Key=key)
        body = response["Body"].read()
        emit(HERE / "source" / relative, body)
        objects[relative] = {
            "key": key, "sha256": hashlib.sha256(body).hexdigest(),
            "etag": response["ETag"], "version_id": response.get("VersionId"),
            "content_type": response["ContentType"],
        }
        return body

    html = fetch("index.html", SOURCE_PREFIX + "/gallery/index.html")
    links = SourceLinks()
    links.feed(html.decode())
    main = [value for value in links.scripts if Path(urlsplit(value).path).name.startswith("main")]
    auth = [value for value in links.scripts if Path(urlsplit(value).path).name == "imsauth.js"]
    if len(main) != 1 or len(auth) != 1 or len(links.styles) != 1:
        raise ValueError("live gallery's script/auth/style identity is ambiguous")
    javascript = fetch("main.js", asset_key(urljoin(SOURCE_URL, main[0])))
    fetch("imsauth.js", asset_key(urljoin(SOURCE_URL, auth[0])))
    fetch("style.css", asset_key(urljoin(SOURCE_URL, links.styles[0])))
    data_urls = re.findall(r'fetch\(["\']([^"\']+\.json)["\']', javascript.decode())
    if len(data_urls) != 1:
        raise ValueError("live gallery must identify exactly one current data object")
    raw = fetch("comparison.json", asset_key(urljoin(SOURCE_URL, data_urls[0])))
    grouped = group_data(json.loads(raw))
    if len(grouped["groups"]) != 16:
        raise ValueError("expected exactly sixteen complete inputs")
    from botocore.exceptions import ClientError
    probe_key = PREFIX + "/preflight/source_sha256.txt"
    probe = objects["comparison.json"]["sha256"].encode()
    try:
        client.put_object(Bucket=BUCKET, Key=probe_key, Body=probe,
                          ContentType="text/plain", IfNoneMatch="*")
    except ClientError as error:
        if error.response["Error"]["Code"] not in ("PreconditionFailed", "412"):
            raise
    if client.get_object(Bucket=BUCKET, Key=probe_key)["Body"].read() != probe:
        raise ValueError("conditional S3 write/read preflight failed")
    emit(HERE / "source_manifest.json", {
        "source_url": SOURCE_URL, "objects": objects, "groups": 16,
        "experiments": 3, "images": 480, "ranks_per_group": 10,
        "new_model_calls": 0, "source_and_original_reports_must_remain_unchanged": True,
        "credential_route": "Standard broker lacks local Pluto token; user-approved refreshed temporary-file parser.",
        "scope": "New single non-FE gallery; sixteen inputs, three ten-image grids each; prompts collapsed; shared source documents expandable.",
    })
    print("Frozen live source and conditional access preflight: 16 inputs, 480 existing images.")


def group_data(source):
    if (source.get("status") != "complete" or len(source["rows"]) != 160
            or set(source["cells"]) != {item[0] for item in EXPERIMENTS}):
        raise ValueError("expected the complete three-experiment160-row source")
    groups = defaultdict(list)
    seen = set()
    for row in source["rows"]:
        slot = tuple(row["key"])
        if slot in seen:
            raise ValueError("duplicate device/camera/rank slot")
        seen.add(slot)
        if len(slot) != 3:
            raise ValueError("invalid input/rank slot")
        groups[slot[:2]].append(row)
    if len(groups) != 16:
        raise ValueError("expected sixteen device-camera inputs")
    result = []
    for (device_id, camera_tag), rows in sorted(groups.items()):
        rows.sort(key=lambda row: row["key"][2])
        if [row["key"][2] for row in rows] != list(range(1, 11)):
            raise ValueError("each input needs all ten distinct bank ranks")
        experiments = []
        for cell, label, prompt_field, input_field in EXPERIMENTS:
            context = rows[0][input_field]
            camera = rows[0][prompt_field]["source_camera_name"]
            bank = rows[0][prompt_field]["bank_debug_ref"]
            cards = []
            for row in rows:
                prompt, output = row[prompt_field], row["outputs"][cell]
                rank = row["key"][2]
                if (prompt["device_id"] != device_id or prompt["camera_tag"] != camera_tag
                        or prompt["bank_rank"] != rank or prompt["source_camera_name"] != camera
                        or prompt["bank_debug_ref"] != bank or row[input_field] != context
                        or context["camera_tag"] != camera_tag):
                    raise ValueError("input bank mixes sources, cameras or ranks")
                if output["status"] != "done" or not prompt["text"].strip():
                    raise ValueError("every card needs its actual successful image and original prompt")
                if hashlib.sha256(prompt["text"].encode()).hexdigest() != prompt["text_sha256"]:
                    raise ValueError("original writer prompt hash differs")
                cards.append({
                    "rank": rank, "prompt_key": prompt["prompt_key"],
                    "prompt": prompt["text"], "environment": prompt["environment"],
                    "image": relative_asset(output["image"]), "image_sha256": output["image_sha256"],
                })
            experiments.append({"id": cell, "label": label, "cards": cards})
        if experiments[0]["cards"][0]["prompt"] != experiments[1]["cards"][0]["prompt"]:
            raise ValueError("the two V6.3 pipelines must share original writer prompts")
        result.append({
            "id": device_id + "__" + camera_tag, "device": rows[0]["device"],
            "device_id": device_id, "camera": rows[0]["camera"], "camera_tag": camera_tag,
            "contexts": [
                {"label": "V6.3 - both pipelines", "input": rows[0]["source_input"]},
                {"label": "V6.4 - structured customer sources", "input": rows[0]["source_input_v6_4"]},
            ],
            "experiments": experiments,
        })
    return {"title": TITLE, "source_url": SOURCE_URL, "group_count": 16,
            "experiment_count": 3, "image_count": 480, "groups": result}


def build():
    frozen = load(HERE / "source_manifest.json")
    for name, expected in frozen["objects"].items():
        if sha(HERE / "source" / name) != expected["sha256"]:
            raise ValueError("frozen live source changed")
    emit(PUBLIC / "gallery/data.json", group_data(load(HERE / "source/comparison.json")))
    emit(PUBLIC / "gallery/imsauth.js", (HERE / "source/imsauth.js").read_bytes())
    names = ("index.html", "main.js", "style.css", "data.json", "imsauth.js")
    emit(HERE / "build_manifest.json", {
        "source_manifest_sha256": sha(HERE / "source_manifest.json"),
        "assets": {"gallery/" + name: {"sha256": sha(PUBLIC / "gallery" / name),
                   "bytes": (PUBLIC / "gallery" / name).stat().st_size} for name in names},
        "groups": 16, "images": 480, "new_image_uploads": 0,
    })
    print("Built one grouped gallery: 16 inputs x 3 experiments x 10 images.")


def verify_live(client):
    for expected in load(HERE / "source_manifest.json")["objects"].values():
        response = client.get_object(Bucket=BUCKET, Key=expected["key"])
        if (response["ETag"] != expected["etag"]
                or response.get("VersionId") != expected["version_id"]
                or hashlib.sha256(response["Body"].read()).hexdigest() != expected["sha256"]):
            raise ValueError("live source changed; re-read and merge instead of publishing a stale grouping")


def publish():
    from botocore.exceptions import ClientError
    client = s3_client()
    manifest = load(HERE / "build_manifest.json")
    proof = load(HERE / "browser_validation.json")
    if proof["status"] != "passed" or proof["build_manifest_sha256"] != sha(HERE / "build_manifest.json"):
        raise ValueError("exact browser validation is required")
    if manifest["source_manifest_sha256"] != sha(HERE / "source_manifest.json"):
        raise ValueError("source manifest changed")
    verify_live(client)
    types = {".html": "text/html; charset=utf-8", ".js": "application/javascript",
             ".css": "text/css", ".json": "application/json"}

    def upload(item):
        name, expected = item
        path = PUBLIC / name
        body = path.read_bytes()
        if hashlib.sha256(body).hexdigest() != expected["sha256"] or len(body) != expected["bytes"]:
            raise ValueError("browser-verified public file changed")
        key, content_type = PREFIX + "/" + name, types[path.suffix]
        try:
            client.put_object(Bucket=BUCKET, Key=key, Body=body, ContentType=content_type,
                              CacheControl="no-cache", Metadata={"sha256": expected["sha256"]},
                              IfNoneMatch="*")
        except ClientError as error:
            if error.response["Error"]["Code"] not in ("PreconditionFailed", "412"):
                raise
        response = client.get_object(Bucket=BUCKET, Key=key)
        if response["Body"].read() != body or response["ContentType"] != content_type:
            raise ValueError("published grouped report bytes/type differ")
        return key, {"sha256": expected["sha256"], "etag": response["ETag"],
                     "version_id": response.get("VersionId"), "bytes": len(body),
                     "content_type": content_type}

    with ThreadPoolExecutor(max_workers=5) as pool:
        objects = dict(pool.map(upload, manifest["assets"].items()))
    verify_live(client)
    emit(HERE / "publication_receipt.json", {
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "viewer_url": VIEWER_URL, "groups": 16, "experiments": 3, "images": 480,
        "objects": objects, "original_comparison_unchanged": True,
        "new_model_calls": 0, "image_uploads": 0, "build_manifest_sha256": sha(HERE / "build_manifest.json"),
        "network_boundary": "S3 byte/type verification and exact local browser rendering; IMS mocked in local check.",
    })
    emit(HERE / "report_links.txt", (VIEWER_URL + "\n").encode())
    print(VIEWER_URL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "build", "publish"))
    command = parser.parse_args().command
    {"prepare": prepare, "build": build, "publish": publish}[command]()
