"""Preserve original failure evidence and CAS-publish the completed comparison."""

from __future__ import annotations

import argparse
import copy
import hashlib
import mimetypes
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from botocore.exceptions import ClientError

import report as original_report
import text_study
from recovery.complete160 import audit_native, image_recovery

HERE = image_recovery.HERE
ROOT = image_recovery.ROOT
PUBLIC = HERE / "public"
NEW = "completion_20261112"
DATA_NAME = "gallery/completed_data_20261112.json"
MAIN_NAME = "gallery/completed_main_20261112.js"
PREFIX = original_report.PREFIX
BUCKET = original_report.BUCKET
load, sha, write = text_study.load, text_study.sha, text_study.write
SOURCE_NAMES = ("gallery/index.html", "gallery/main.js", "gallery/style.css", "gallery/imsauth.js", "gallery/data.json")


def prepare() -> None:
    client = text_study.s3_client()
    files = {}
    for name in SOURCE_NAMES:
        response = client.get_object(Bucket=BUCKET, Key=PREFIX + "/" + name)
        body = response["Body"].read()
        if body != (ROOT / "public" / name).read_bytes():
            raise ValueError("Current published report differs from the original verified local report")
        write(HERE / "source" / name, body)
        files[name] = {
            "sha256": hashlib.sha256(body).hexdigest(),
            "etag": response["ETag"],
            "content_type": response["ContentType"],
            "metadata": response.get("Metadata", {}),
            "headers": {
                key: response[key]
                for key in ("CacheControl", "ContentDisposition", "ContentEncoding")
                if key in response
            },
        }
    original_report.verify_live(client)
    probe = b"Authorized Astra completion publication preflight"
    key = PREFIX + "/" + NEW + "/preflight.txt"
    client.put_object(Bucket=BUCKET, Key=key, Body=probe, ContentType="text/plain", IfNoneMatch="*")
    if client.get_object(Bucket=BUCKET, Key=key)["Body"].read() != probe:
        raise ValueError("Completion publication preflight failed")
    write(
        HERE / "source_manifest.json",
        {
            "files": files,
            "prepared_utc": datetime.now(UTC).isoformat(),
            "recovery_code": {
                name: sha(HERE / name) for name in ("completed_report.py", "audit_native.py", "verify_browser.py")
            },
        },
    )


def verify_source() -> None:
    manifest = load(HERE / "source_manifest.json")
    for name, digest in manifest["recovery_code"].items():
        if sha(HERE / name) != digest:
            raise ValueError("Frozen completion report code changed")
    for name, identity in manifest["files"].items():
        if sha(HERE / "source" / name) != identity["sha256"]:
            raise ValueError("Frozen publication source changed")


def asset(source: Path, name: str, expected: str | None = None) -> str:
    body = source.read_bytes()
    if expected is not None and hashlib.sha256(body).hexdigest() != expected:
        raise ValueError("New public asset differs from its audited source")
    destination = PUBLIC / name
    if destination.exists():
        if destination.read_bytes() != body:
            raise ValueError("New public asset collision")
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        os.link(source, destination)
    return original_report.relative(original_report.GATEWAY + PREFIX + "/" + name)


def merge_data(before: dict[str, Any], document: dict[str, Any], replacements: dict[str, Any]) -> dict[str, Any]:
    data = copy.deepcopy(before)
    prompts = {prompt["prompt_key"]: prompt for prompt in document["prompts"]}
    used = set()
    for group in data["groups"]:
        experiment = group["experiments"][1]
        for index, card in enumerate(experiment["cards"]):
            key = card["prompt_key"]
            if card["status"] == "done":
                if key in replacements or card["prompt"] != prompts[key]["text"]:
                    raise ValueError("Recovery would replace a successful original")
                continue
            if key not in replacements:
                raise ValueError("A failed image/writer slot has no recovery result")
            experiment["cards"][index] = replacements[key]
            used.add(key)
        experiment["writer_status"] = "ok"
        experiment["terminal_error"] = None
        if "original_result" in document["bank_audit"][group["id"]]:
            experiment["bank_result_url"] = "../" + NEW + "/data/banks/" + group["id"] + ".json"
    if used != set(replacements) or len(used) != 81:
        raise ValueError("Recovery must replace exactly81 previously failed slots")
    data["original_astra_text"] = data["astra_text"]
    data["original_astra_images"] = data["astra_images"]
    data["astra_text"] = {
        "accepted_prompts": 160,
        "accepted_banks": 16,
        "failed_banks": [],
        "status": "complete",
        "original_accepted_prompts": 80,
        "recovered_prompts": 80,
    }
    data["astra_images"] = {"done": 160, "failed": 0, "preserved": 79, "recovered": 81}
    data["original_successful_native_models"] = data["successful_native_models"]
    data["successful_native_models"] = {"gpt-6-astra": 480, "gpt-image-2.5-sunburst-2026-09-08": 160}
    data["successful_native_models_scope"] = "Successful Astra-arm images only; failed-attempt calls are separate."
    data["image_count"] = 320
    data["recovery_note"] = "Authorized continuation/repairs; not a new unedited reliability trial."
    return data


def build() -> None:
    verify_source()
    image_recovery.verify()
    document = load(HERE / "exports/prompts_all_160.json")
    prompts = {prompt["prompt_key"]: prompt for prompt in document["prompts"]}
    replacements = {}
    for row in image_recovery.selected_rows():
        key, slug = row["row_id"], row["row_slug"]
        result = load(HERE / "image_results" / (slug + ".json"))
        run = Path(result["run"])
        paths = image_recovery.scene_runner.paths(run, row)
        record = load(paths["record"])
        audit = audit_native.audit_one(prompts[key], run)
        asset(paths["image"], NEW + "/assets/outputs/" + slug + ".png", record["image_sha256"])
        inputs = {}
        for role in ("product", "reference", "geometry_guide"):
            part = audit[role]
            name = NEW + "/assets/inputs/" + part["sha256"] + "." + part["suffix"]
            asset(Path(part["path"]), name, part["sha256"])
            inputs[role] = original_report.GATEWAY + PREFIX + "/" + name
        asset(paths["record"], NEW + "/data/records/" + slug + ".json")
        output = {
            "status": "done",
            "image": original_report.GATEWAY + PREFIX + "/" + NEW + "/assets/outputs/" + slug + ".png",
            "image_sha256": record["image_sha256"],
            "inputs": inputs,
            "scene_debug": record["scene_debug"],
            "lineage": record["lineage"],
        }
        replacements[key] = original_report.card(prompts[key], output)
        replacements[key]["details"]["recovery"] = {
            "native_attempts": result["attempts"],
            "original_failure_preserved": True,
        }
    for bank, audit in document["bank_audit"].items():
        if "original_result" not in audit:
            continue
        evaluations = [load(path) for path in sorted((HERE / "journals" / bank).glob("attempt_*/evaluation.json"))]
        write(PUBLIC / NEW / "data/banks" / (bank + ".json"), {**audit, "all_recovery_attempts": evaluations})
    data = merge_data(load(HERE / "source/gallery/data.json"), document, replacements)
    write(PUBLIC / DATA_NAME, data)
    old_js = (HERE / "source/gallery/main.js").read_text()
    if old_js.count('"./data.json"') != 1:
        raise ValueError("Original gallery fetch path changed")
    write(PUBLIC / MAIN_NAME, old_js.replace('"./data.json"', '"./completed_data_20261112.json"').encode())
    old_html = (HERE / "source/gallery/index.html").read_text()
    write(PUBLIC / "gallery/original_run_20261112.html", old_html.encode())
    note = (
        "<p><strong>Completed with authorized recovery:</strong> 80 original accepted prompts and 79 images were preserved. "
        "Eight failed banks were continued/repaired and 81 missing image slots were generated. "
        "This is not a new first-draw reliability trial. "
        '<a href="./original_run_20261112.html">Original failure snapshot</a> | '
        f'<a href="../{NEW}/data/recovery_history.json">Recovery history</a> | '
        f'<a href="../{NEW}/data/prompts_all_160.json">All 160 Astra prompts (JSON)</a> | '
        f'<a href="../{NEW}/data/prompts_all_160.txt">All 160 Astra prompts (TXT)</a></p>'
    )
    if old_html.count("<header>") != 1:
        raise ValueError("Original report header changed")
    html = old_html.replace("<header>", "<header>\n" + note).replace(
        'src="./main.js"', 'src="./completed_main_20261112.js"'
    )
    html = html.replace(
        "Failures are shown, not resampled.", "Original failures and authorized recovery attempts are retained."
    )
    html = html.replace(
        "Only accepted Astra banks are rendered. Images therefore represent the validated subset;\n"
        "        failed banks have ten explicit error slots, not substitute prompts or images.",
        "All 160 Astra prompts now pass validation. Originally failed banks were continued or repaired under explicit "
        "authorization; all attempts and the original failure snapshot remain available.",
    )
    write(PUBLIC / "gallery/index.html", html.encode())
    asset(HERE / "exports/prompts_all_160.json", NEW + "/data/prompts_all_160.json")
    asset(HERE / "exports/prompts_all_160.txt", NEW + "/data/prompts_all_160.txt")
    write(
        PUBLIC / NEW / "data/recovery_history.json",
        {
            "authorization": load(HERE / "authorization.json"),
            "original_text": load(ROOT / "text/terminal.json"),
            "original_images": load(ROOT / "image_terminal.json"),
            "recovered_images": load(HERE / "image_terminal.json"),
            "all_image_attempt_records": [
                load(path) for path in sorted((HERE / "image_attempts").glob("*/attempt_*/records/*.json"))
            ],
            "writer_results": {
                bank: audit["result"]["audit"]
                for bank, audit in document["bank_audit"].items()
                if "original_result" in audit
            },
        },
    )
    for name in SOURCE_NAMES:
        asset(HERE / "source" / name, NEW + "/original_bytes/" + name)
    assets = {
        str(path.relative_to(PUBLIC)): {"sha256": sha(path), "bytes": path.stat().st_size}
        for path in sorted(PUBLIC.rglob("*"))
        if path.is_file()
    }
    write(
        HERE / "build_manifest.json",
        {
            "assets": assets,
            "actual_images": 320,
            "recovered_images": 81,
            "source_manifest_sha256": sha(HERE / "source_manifest.json"),
        },
    )


def content_type(name: str) -> str:
    return {
        ".html": "text/html; charset=utf-8",
        ".json": "application/json",
        ".js": "application/javascript",
        ".txt": "text/plain; charset=utf-8",
    }.get(Path(name).suffix, mimetypes.guess_type(name)[0] or "application/octet-stream")


def publish() -> None:
    verify_source()
    proof = load(HERE / "browser_validation.json")
    if proof["status"] != "passed" or proof["build_manifest_sha256"] != sha(HERE / "build_manifest.json"):
        raise ValueError("Completed actual-image browser validation is required")
    client = text_study.s3_client()
    source = load(HERE / "source_manifest.json")["files"]
    manifest = load(HERE / "build_manifest.json")["assets"]
    original_report.verify_live(client)

    def unchanged(name: str) -> None:
        expected = source[name]
        response = client.get_object(Bucket=BUCKET, Key=PREFIX + "/" + name)
        if (
            response["ETag"] != expected["etag"]
            or hashlib.sha256(response["Body"].read()).hexdigest() != expected["sha256"]
        ):
            raise ValueError("Concurrent report edit; stop and merge current source: " + name)

    for name in source:
        unchanged(name)
    objects = {}

    def upload(name: str) -> tuple[str, Any]:
        data = (PUBLIC / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != manifest[name]["sha256"]:
            raise ValueError("Verified public completion asset changed")
        key = PREFIX + "/" + name
        kind = content_type(name)
        metadata = {"sha256": manifest[name]["sha256"]}
        headers = {}
        archive = NEW + "/original_bytes/"
        if name.startswith(archive):
            previous = source[name.removeprefix(archive)]
            kind, metadata, headers = previous["content_type"], previous["metadata"], previous["headers"]
        try:
            client.put_object(
                Bucket=BUCKET, Key=key, Body=data, ContentType=kind, Metadata=metadata, IfNoneMatch="*", **headers
            )
        except ClientError as error:
            if error.response["Error"]["Code"] not in ("PreconditionFailed", "412"):
                raise
        response = client.get_object(Bucket=BUCKET, Key=key)
        if (
            response["Body"].read() != data
            or response["ContentType"] != kind
            or response.get("Metadata", {}) != metadata
        ):
            raise ValueError("Completion public bytes/type mismatch")
        return key, {"sha256": manifest[name]["sha256"], "etag": response["ETag"]}

    updates = ("gallery/index.html",)
    with ThreadPoolExecutor(max_workers=8) as workers:
        objects.update(workers.map(upload, [name for name in manifest if name not in updates]))
    for name in source:
        unchanged(name)
    for name in updates:
        data = (PUBLIC / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != manifest[name]["sha256"]:
            raise ValueError("Completion CAS body changed")
        client.put_object(
            Bucket=BUCKET,
            Key=PREFIX + "/" + name,
            Body=data,
            ContentType=source[name]["content_type"],
            IfMatch=source[name]["etag"],
            Metadata={**source[name]["metadata"], "sha256": manifest[name]["sha256"]},
            **source[name]["headers"],
        )
        response = client.get_object(Bucket=BUCKET, Key=PREFIX + "/" + name)
        if response["Body"].read() != data or response["ContentType"] != source[name]["content_type"]:
            raise ValueError("Completion CAS publication read-back mismatch")
        objects[PREFIX + "/" + name] = {"sha256": manifest[name]["sha256"], "etag": response["ETag"]}
        image_recovery.scene_runner.atomic_json(HERE / "partial_publication_receipt.json", {"objects": objects})
    for name in set(source) - set(updates):
        unchanged(name)
    original_report.verify_live(client)
    write(HERE / "publication_receipt.json", {"objects": objects, "viewer_url": original_report.VIEWER_URL})
    write(HERE / "report_links.txt", (original_report.VIEWER_URL + "\n").encode())
    write(
        HERE / "completion_receipt.json",
        {
            "status": "complete",
            "astra_prompts": 160,
            "astra_images": 160,
            "baseline_images": 160,
            "recovered_prompts": 80,
            "recovered_images": 81,
            "original_images_preserved": 79,
            "publication_receipt_sha256": sha(HERE / "publication_receipt.json"),
            "viewer_url": original_report.VIEWER_URL,
            "completed_utc": datetime.now(UTC).isoformat(),
        },
    )


def execute() -> None:
    build()
    from recovery.complete160 import verify_browser

    verify_browser.main()
    publish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "execute"))
    arguments = parser.parse_args()
    if arguments.command == "prepare":
        prepare()
    else:
        execute()
