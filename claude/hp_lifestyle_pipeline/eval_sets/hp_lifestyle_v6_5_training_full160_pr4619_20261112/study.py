"""Freeze and inspect the authorized, pinned V6.5/V15.8 image experiment."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import uuid
from urllib.parse import urljoin, urlsplit

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / "hp_lifestyle_v6_5_training_full160_pr4523_20261112"
NATIVE = HERE / "native/experimental/adarabi/hp-3p-gpt25"
COMMIT = "db074bd9ab8f832712aa45415435dfa647e51ced"
BUCKET = "foundry-hp-enterprise-adobe-assets"
GATEWAY = f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/"
PREFIX = "eval_sets/" + HERE.name
FE_PREFIX = "hp-data-artifacts/hp-3p-gpt25/hp160-v64-fourway-v65-five-column-20261112"
GROUP_PREFIX = "eval_sets/" + PRIOR.name + "/gallery"
BASELINE = "hp-data-artifacts/hp-3p-gpt25/hp160-v64-native-pr4619-20261111T201255Z"
LABEL = "V6.5 / PR 4619 - V15.8 stats in rewriter + strong lighting"
BACKUP = Path("/sensei-fs/users/hshariati/claude_backup")


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(body):
    return hashlib.sha256(body).hexdigest()


def sha(path):
    return digest(Path(path).read_bytes())


def load(path):
    return json.loads(Path(path).read_text())


def emit(path, value):
    path = Path(path)
    body = value if isinstance(value, bytes) else (
        json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    ).encode()
    if path.exists():
        if path.read_bytes() != body:
            raise ValueError(f"Existing immutable artifact differs: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(body)


def client():
    import foundry_aws_gateway

    result = foundry_aws_gateway.maybe_s3_client(BUCKET)
    if result is None:
        raise RuntimeError("Managed Foundry HP S3 authentication is unavailable")
    return result


def key_for(url):
    parsed = urlsplit(url)
    prefix = f"/asset/{BUCKET}/"
    if (parsed.scheme != "https" or parsed.netloc != "foundry-aws-corp.adobe.io"
            or not parsed.path.startswith(prefix) or parsed.query or parsed.fragment):
        raise ValueError(f"Asset is not a plain authenticated HP object: {url}")
    return parsed.path[len(prefix):]


def prompt_key(row):
    metadata = row["meta_data"]
    match = re.fullmatch(r"(.+)__p([1-9]|10)", metadata["evalset_item_id"])
    if match is None:
        raise ValueError("Unexpected external device/camera/rank identifier")
    group, rank = match.groups()
    values = metadata["key_val_informations"]
    if values["Input group"] != group or values["Prompt rank"] != int(rank):
        raise ValueError("External input-group/rank metadata disagrees with identifier")
    return group + "::p" + rank


class Dependencies(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "script" and attrs.get("src"):
            self.urls.append(attrs["src"])
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.urls.append(attrs["href"])


def prepare():
    if (HERE / "source_manifest.json").exists():
        verify()
        raise FileExistsError("Source is already frozen; do not silently refresh this experiment")
    if not os.path.ismount("/sensei-fs") or not BACKUP.is_dir():
        raise RuntimeError("Approved durable Sensei mount is unavailable; no fallback is permitted")
    if (HERE / "storage.json").exists():
        storage = load(HERE / "storage.json")
        artifacts = Path(storage["artifact_root"])
        if artifacts.parent != BACKUP or not artifacts.is_dir():
            raise ValueError("Existing storage identity does not name this approved mounted directory")
    else:
        artifacts = BACKUP / (HERE.name + "_" + uuid.uuid4().hex[:12])
        artifacts.mkdir()
        probe = b"HP V6.5 pinned V15.8 durable storage verification\n"
        emit(artifacts / "storage_probe.txt", probe)
        if (artifacts / "storage_probe.txt").read_bytes() != probe:
            raise RuntimeError("Durable mounted-storage write/read verification failed")
        storage = {
            "at_utc": now(), "artifact_root": str(artifacts),
            "code_and_checkpoint_root": str(HERE),
            "storage_policy": "Write new large artifacts directly to approved durable mounted storage.",
            "old_studies_deleted_or_moved": False,
        }
        emit(HERE / "storage.json", storage)
        emit(artifacts / "storage.json", storage)
    c = client()
    objects = {}

    def fetch(relative, key):
        response = c.get_object(Bucket=BUCKET, Key=key)
        body = response["Body"].read()
        path = HERE / "source" / relative
        emit(path, body)
        objects[relative] = {
            "key": key, "sha256": digest(body), "bytes": len(body),
            "etag": response["ETag"], "version_id": response.get("VersionId"),
            "content_type": response["ContentType"], "metadata": response.get("Metadata", {}),
        }
        return body

    for name in ("viewer.html", "data.json", "provenance.json"):
        fetch("fe/" + name, FE_PREFIX + "/" + name)
    index = fetch("grouped/index.html", GROUP_PREFIX + "/index.html")
    dependencies = Dependencies()
    dependencies.feed(index.decode())
    for url in dependencies.urls:
        resolved = urljoin(GATEWAY + GROUP_PREFIX + "/index.html", url)
        if resolved.startswith(GATEWAY + GROUP_PREFIX + "/"):
            key = key_for(resolved)
            fetch("grouped/" + key.removeprefix(GROUP_PREFIX + "/"), key)
    fetch("grouped/data.json", GROUP_PREFIX + "/data.json")
    for name in ("manifest.json", "cases.json", "profiles.json", "generation_summary.json",
                 "validation.json", "results.json"):
        fetch("baseline/" + name, BASELINE + "/" + name)
    annotations = {}
    for page in c.get_paginator("list_objects_v2").paginate(
        Bucket=BUCKET, Prefix=FE_PREFIX + "/annotations/"
    ):
        for item in page.get("Contents", []):
            if item["Key"].endswith(".json"):
                name = item["Key"].removeprefix(FE_PREFIX + "/")
                fetch("fe/" + name, item["Key"])
                annotations[name] = objects["fe/" + name]
    original_prompts = PRIOR / "source/prompts_for_runner_160.json"
    emit(HERE / "source/prompts_for_runner_160.json", original_prompts.read_bytes())
    frozen = [HERE / "source" / name for name in objects]
    frozen += [HERE / "source/prompts_for_runner_160.json", HERE / "storage.json"]
    frozen += [p for p in NATIVE.rglob("*")
               if p.is_file() and "__pycache__" not in p.parts]
    manifest = {
        "at_utc": now(), "commit": COMMIT, "size": [1216, 912],
        "label": LABEL, "storage": storage, "objects": objects, "annotations": annotations,
        "frozen_files": {str(p): sha(p) for p in sorted(frozen)},
        "authorization": {
            "frozen_v65_prompts": 160, "new_images": 160,
            "native_scap_and_realism": True, "extra_color_or_wall_interventions": False,
            "explicitly_labeled_no_statistics_cases": True,
            "recover_genuine_failures_without_resampling_successes": True,
            "new_grouped_view": "One paired16-bank comparison, ten images per method.",
            "new_writer_or_judge_calls": False,
        },
    }
    emit(HERE / "source_manifest.json", manifest)
    emit(artifacts / "source_manifest.json", manifest)
    print(json.dumps({
        "artifact_root": str(artifacts), "live_objects": len(objects),
        "annotation_documents": len(annotations), "native_files": len(frozen) - len(objects) - 2,
        "source_prompts": len(load(original_prompts)["prompts"]),
        "baseline_manifest_fields": list(load(HERE / "source/baseline/manifest.json")),
    }, indent=2))


def verify():
    manifest = load(HERE / "source_manifest.json")
    if manifest["commit"] != COMMIT:
        raise ValueError("Pinned native source identity differs")
    for path, expected in manifest["frozen_files"].items():
        if sha(path) != expected:
            raise ValueError(f"Frozen source changed: {path}")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "verify"])
    command = parser.parse_args().command
    if command == "prepare":
        prepare()
    else:
        verify()
        print("Frozen native source, original prompts, live snapshots and storage identity verified.")
