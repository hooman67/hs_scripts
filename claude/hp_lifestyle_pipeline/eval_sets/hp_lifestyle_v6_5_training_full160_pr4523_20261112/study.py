"""Extend the training-grounded V6.5 to160 images without redrawing its30 outputs."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import sys
from urllib.parse import urljoin, urlsplit

import httpx

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
PRIOR = HERE.parent / "hp_lifestyle_v6_5_training_pr4523_30_20261111"
COMPARISON = HERE.parent / "hp_lifestyle_v6_3_full160_pr4523_pr4417_20261110"
GROUPED = HERE.parent / "hp_lifestyle_grouped_diversity_20261111"
LEGACY = HERE.parent / "hp_lifestyle_v6_4_full160_pr4523_20261110"
ENDPOINT = HERE / "endpoint_pr4523"
SOURCE = HERE / "source/prompts_for_runner_160.json"
PREFIX = "eval_sets/" + HERE.name
BUCKET = "foundry-hp-enterprise-adobe-assets"
GATEWAY = f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/"
TITLE = "V6.5 / PR 4523 - V15.7 shapes"
COMMIT = "d1e5ae5323dedebc3b06ed173a3731307bd0623a"
RUNNER = PROJECT / "eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/run_generation.py"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ValueError(f"helper unavailable: {path}")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def load(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = value if isinstance(value, bytes) else (
        json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    ).encode()
    with path.open("xb") as stream:
        stream.write(body)


def s3_client():
    import foundry_aws_gateway

    client = foundry_aws_gateway.maybe_s3_client(BUCKET)
    if client is None:
        raise RuntimeError("Managed Foundry S3 authentication is unavailable")
    return client


def image_runner():
    return module("v65_full160_native_runner", RUNNER)


def row_for(prompt):
    return {
        "row_id": prompt["prompt_key"],
        "row_slug": image_runner().slug(prompt["prompt_key"]),
        "prompt_sha256": prompt["text_sha256"],
    }


def partition(prompts, reused):
    return module("v65_full160_partition", LEGACY / "study.py").partition(prompts, reused)


def verify():
    manifest = load(HERE / "study_manifest.json")
    for path, digest in manifest["frozen_files"].items():
        if sha(path) != digest:
            raise ValueError(f"frozen source/reuse/pipeline changed: {path}")
    return manifest


def endpoint_url():
    return load(HERE / "study_manifest.json")["endpoint_base_url"]


def legacy():
    helper = module("v65_full160_unchanged_orchestration", LEGACY / "study.py")
    for name in (
        "HERE", "PROJECT", "PRIOR", "COMPARISON", "ENDPOINT", "SOURCE",
        "PREFIX", "BUCKET", "TITLE", "COMMIT", "RUNNER",
    ):
        setattr(helper, name, globals()[name])
    helper.BASE_URL = endpoint_url()
    helper.verify = verify
    helper.s3_client = s3_client
    return helper


class Links(HTMLParser):
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


def key_for(url):
    parsed = urlsplit(url)
    prefix = f"/asset/{BUCKET}/"
    if (
        parsed.scheme != "https" or parsed.netloc != "foundry-aws-corp.adobe.io"
        or not parsed.path.startswith(prefix) or parsed.query or parsed.fragment
    ):
        raise ValueError(f"asset escapes the authenticated HP bucket: {url}")
    return parsed.path[len(prefix):]


def annotations(client):
    prefix = "eval_sets/" + COMPARISON.name + "/fe/annotations/"
    found = {}
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix):
        for item in page.get("Contents", []):
            if item["Key"].endswith(".json"):
                response = client.get_object(Bucket=BUCKET, Key=item["Key"])
                body = response["Body"].read()
                found[item["Key"]] = {
                    "etag": response["ETag"], "version_id": response.get("VersionId"),
                    "sha256": hashlib.sha256(body).hexdigest(),
                }
                path = HERE / "baseline_live/annotations" / item["Key"].removeprefix(prefix)
                if path.exists():
                    if path.read_bytes() != body:
                        raise ValueError("published annotations changed")
                else:
                    write(path, body)
    return found


def prepare():
    if (HERE / "study_manifest.json").exists():
        raise FileExistsError("full160 study already frozen")
    prior = module("v65_full160_prior", PRIOR / "study.py")
    original = prior.verify()
    if prior.counts() != {"expected": 30, "done": 30, "failed": 0, "pending": 0}:
        raise ValueError("all thirty original outputs must be valid before reuse")
    completion = load(PRIOR / "completion_receipt.json")
    for name, digest in completion["evidence_sha256"].items():
        if sha(PRIOR / name) != digest:
            raise ValueError(f"original completion evidence changed: {name}")
    write(SOURCE, (PRIOR / "source/prompts_for_runner_160.json").read_bytes())
    document = load(SOURCE)
    if document["prompts"] != load(prior.TEXT)["prompts"]:
        raise ValueError("runner adapter changed an actual accepted prompt")
    runner = image_runner()
    runner.validate_prompt_document(document, SOURCE, sha(SOURCE))
    reused = []
    pinned = [Path(__file__), RUNNER, LEGACY / "study.py", LEGACY / "report.py",
              PRIOR / "study.py", PRIOR / "study_manifest.json",
              PRIOR / "completion_receipt.json", prior.TEXT, prior.TEXT.with_suffix(".txt"),
              SOURCE, HERE / "selection/remaining130.json"]
    for prompt in load(PRIOR / "selection/selected_v6_5_30.json")["prompts"]:
        row = row_for(prompt)
        record = runner.valid_completed_record(PRIOR / "run", row)
        paths = runner.paths(PRIOR / "run", row)
        if record is None or record["lineage"]["source_commit"] != COMMIT:
            raise ValueError("invalid original image or pipeline")
        audit = PRIOR / "input_audit" / (row["row_slug"] + ".json")
        reused.append({
            "prompt_key": prompt["prompt_key"], "job_id": record["job_id"],
            "image_sha256": record["image_sha256"],
            **{name + "_path": str(paths[name]) for name in ("record", "image", "job", "status")},
            "audit_path": str(audit),
        })
        pinned.extend(paths[name] for name in ("record", "image", "job", "status"))
        pinned.append(audit)
    fresh = partition(document["prompts"], [row["prompt_key"] for row in reused])
    write(HERE / "selection/remaining130.json", {
        "source_prompts_sha256": sha(SOURCE), "row_ids": fresh,
        "rows": [p for p in document["prompts"] if p["prompt_key"] in set(fresh)],
    })
    copied = []
    for path, digest in original["frozen_files"].items():
        path = Path(path)
        if path.is_relative_to(prior.ENDPOINT):
            if sha(path) != digest:
                raise ValueError("native endpoint source changed")
            target = ENDPOINT / path.relative_to(prior.ENDPOINT)
            write(target, path.read_bytes())
            copied.append(target)
    if len(copied) != 70:
        raise ValueError("expected exactly seventy unchanged endpoint files")
    pinned.extend(copied)
    client = s3_client()
    objects = {}

    def fetch(relative, key):
        response = client.get_object(Bucket=BUCKET, Key=key)
        body = response["Body"].read()
        path = HERE / "baseline_live" / relative
        write(path, body)
        objects[relative] = {
            "key": key, "sha256": hashlib.sha256(body).hexdigest(),
            "etag": response["ETag"], "version_id": response.get("VersionId"),
            "content_type": response["ContentType"], "metadata": response.get("Metadata", {}),
        }
        pinned.append(path)
        return body

    for label, root in (("full", COMPARISON), ("grouped", GROUPED), ("prior30", PRIOR)):
        base = GATEWAY + "eval_sets/" + root.name + "/gallery/index.html"
        html = fetch(label + "/gallery/index.html", key_for(base))
        links = Links()
        links.feed(html.decode())
        mains = [p for p in links.scripts if Path(urlsplit(p).path).name.startswith("main")]
        auths = [p for p in links.scripts if Path(urlsplit(p).path).name == "imsauth.js"]
        if len(mains) != 1 or len(auths) != 1 or len(links.styles) != 1:
            raise ValueError("live report script/style/auth identity is ambiguous")
        javascript = fetch(label + "/gallery/main.js", key_for(urljoin(base, mains[0])))
        fetch(label + "/gallery/imsauth.js", key_for(urljoin(base, auths[0])))
        fetch(label + "/gallery/style.css", key_for(urljoin(base, links.styles[0])))
        data_urls = re.findall(r'fetch\(["\']([^"\']+\.json)["\']', javascript.decode())
        if len(data_urls) != 1:
            raise ValueError("live report must identify exactly one current data object")
        fetch(label + "/data.json", key_for(urljoin(base, data_urls[0])))
    for name in ("viewer.html", "data.json"):
        fetch("full/fe/" + name, "eval_sets/" + COMPARISON.name + "/fe/" + name)
    old = load(HERE / "baseline_live/full/data.json")
    grouped = load(HERE / "baseline_live/grouped/data.json")
    if (
        len(old["rows"]) != 160 or len(old["cells"]) != 3
        or grouped["group_count"] != 16 or grouped["experiment_count"] != 3
        or grouped["image_count"] != 480
    ):
        raise ValueError("expected live three-experiment full160 and grouped reports")
    if {tuple(row["key"]) for row in old["rows"]} != {
        (p["device_id"], p["camera_tag"], p["bank_rank"]) for p in document["prompts"]
    }:
        raise ValueError("full160 slots do not match")
    published_annotations = annotations(client)
    pinned.extend(p for p in (HERE / "baseline_live/annotations").rglob("*") if p.is_file())
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    write(HERE / "study_manifest.json", {
        "version": "hp-v6.5-training-full160-pr4523-v1", "frozen_at_utc": now(),
        "title": TITLE, "source_export": str(prior.TEXT), "source_export_sha256": sha(prior.TEXT),
        "source_commit": COMMIT, "endpoint_base_url": f"http://127.0.0.1:{port}",
        "reused": reused, "new_row_ids": fresh, "authorized_primary_submissions": 130,
        "failure_policy": "User authorizes operational retries until generated; preserve attempts; "
                          "never redraw successes or duplicate unresolved ambiguous submissions.",
        "new_text_calls": 0, "new_judge_calls": 0, "workers": 4,
        "targets": "new V6.4/V6.5-only grouped report; fourth experiment in existing grouped, detailed and FE reports",
        "baseline_live_objects": objects, "baseline_annotations": published_annotations,
        "disk_free_at_freeze": shutil.disk_usage(HERE).free,
        "frozen_files": {str(path): sha(path) for path in pinned},
    })
    probe = json.dumps({"study": PREFIX, "manifest_sha256": sha(HERE / "study_manifest.json")}).encode()
    key = PREFIX + "/preflight/s3_access_probe.json"
    client.put_object(Bucket=BUCKET, Key=key, Body=probe, ContentType="application/json", IfNoneMatch="*")
    if client.get_object(Bucket=BUCKET, Key=key)["Body"].read() != probe:
        raise ValueError("conditional S3 write/read preflight failed")
    write(HERE / "s3_preflight.json", {"passed": True, "at_utc": now(), "key": key})
    print(json.dumps({"reused": 30, "remaining": 130, "endpoint_files": 70, "port": port,
                      "live_source_objects": len(objects), "annotations": len(published_annotations)}))


def counts():
    return legacy().counts()


def preflight():
    legacy().preflight()


def generate(authorized):
    manifest = verify()
    if not authorized:
        raise PermissionError("paid calls require explicit authorization")
    if shutil.disk_usage(HERE).free < 6 * 1024**3:
        raise RuntimeError("less than6GiB free before the130-image batch")
    gate = load(HERE / "endpoint_preflight.json")
    response = httpx.get(endpoint_url() + "/health", timeout=30)
    response.raise_for_status()
    if response.json()["instanceId"] != gate["health"]["instanceId"]:
        raise ValueError("owned endpoint instance changed")
    helper = legacy()
    command = helper.runner_command()
    write(HERE / "generation_launch.json", {
        "at_utc": now(), "row_ids": manifest["new_row_ids"], "command": command,
        "recorded_before_process_start": True, "study_manifest_sha256": sha(HERE / "study_manifest.json"),
    })
    with (HERE / "generation_execution.log").open("x") as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    terminal = counts()
    write(HERE / "generation_terminal.json", {
        "at_utc": now(), "process_exit_code": result.returncode, "counts": terminal,
    })
    print(json.dumps(terminal), flush=True)
    if result.returncode or terminal["done"] != 160 or terminal["failed"] or terminal["pending"]:
        raise RuntimeError("preserved incomplete first pass; inspect actual jobs before operational recovery")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "verify", "preflight", "generate", "counts"))
    parser.add_argument("--paid-calls-authorized", action="store_true")
    args = parser.parse_args()
    if args.command == "generate":
        generate(args.paid_calls_authorized)
    else:
        value = globals()[args.command]()
        if args.command == "counts":
            print(json.dumps(value))
