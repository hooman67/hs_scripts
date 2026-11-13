#!/usr/bin/env python3
"""Publish four minimal FE reports and remove clutter from the existing report."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil

import convert as original

WORK = original.HERE / "clean"
REPORTS = (("combined", None), *((name, name) for name, _ in original.CELLS))


def report_url(name):
    directory = "" if name == "combined" else name + "/"
    return original.BASE + "fe/" + directory + "viewer.html?ldap=hshariati"


def convert(document, cell=None):
    choices = [(name, label) for name, label in original.CELLS if cell is None or name == cell]
    if not choices:
        raise ValueError("unknown comparison column")
    if document["status"] != "complete" or len(document["rows"]) != 30:
        raise ValueError("expected the completed30-row comparison")
    rows = []
    seen = set()
    for index, row in enumerate(document["rows"]):
        key = tuple(row["key"])
        if key in seen:
            raise ValueError("duplicate comparison row")
        seen.add(key)
        assets = []
        for name, label in choices:
            output = row["outputs"][name]
            if output["status"] != "done":
                raise ValueError("incomplete comparison image")
            if output["lineage"]["source_commit"] != original.COMMITS[name.rsplit("_", 1)[1]]:
                raise ValueError("wrong pinned pipeline")
            assets.append({"kind": "image", "src": original.media_url(output["image"]), "label": label})
        rows.append({
            "row_idx": index + 1, "evalset_item_id": " / ".join(map(str, key)), "assets": assets,
        })
    title = original.TITLE if cell is None else (
        "HP " + choices[0][1] + " (30 rank-paired cases)"
    )
    return original.load_vendor().manifest_to_data_json({"rows": rows}, is_secure=True, title=title)


def preflight(client):
    sources = original.verify_live_source(client)
    previous = json.loads((original.HERE / "publication_receipt.json").read_text())
    targets = {}
    for name, expected in previous["objects"].items():
        body, metadata = original.get_bytes(client, expected["key"])
        if original.digest(body) != expected["sha256"]:
            raise ValueError("existing FE report changed; re-read and merge before replacing it")
        targets[name] = {
            "key": expected["key"], "sha256": original.digest(body),
            "etag": metadata["ETag"], "version_id": metadata.get("VersionId"),
        }
    original.write_json(WORK / "preflight.json", {"source": sources, "previous_combined": targets})


def build():
    preflight = json.loads((WORK / "preflight.json").read_text())
    for name, identity in preflight["source"].items():
        if original.digest((original.PUBLIC / name).read_bytes()) != identity["sha256"]:
            raise ValueError("source changed after preflight")
    source = json.loads((original.PUBLIC / "data/comparison.json").read_text())
    reports = {}
    for name, cell in REPORTS:
        data = convert(source, cell)
        destination = WORK / "reports" / name
        original.write_json(destination / "data.json", data)
        shutil.copyfile(original.VENDOR / "annotation_viewer.html", destination / "viewer.html")
        reports[name] = {
            "url": report_url(name), "rows": 30, "images_per_row": 4 if cell is None else 1,
            "files": {filename: original.digest((destination / filename).read_bytes())
                      for filename in ("data.json", "viewer.html")},
        }
    original.write_json(WORK / "build_audit.json", {"reports": reports, **preflight})
    print(json.dumps({name: report["url"] for name, report in reports.items()}))


def publish(client):
    from botocore.exceptions import ClientError

    audit = json.loads((WORK / "build_audit.json").read_text())
    browser = json.loads((WORK / "browser_validation.json").read_text())
    expected_files = {name: report["files"] for name, report in audit["reports"].items()}
    if browser["status"] != "passed" or browser["files"] != expected_files:
        raise ValueError("browser validation must match all exact report files")
    if original.verify_live_source(client) != audit["source"]:
        raise ValueError("live comparison source changed")
    verified = {}
    for name, report in audit["reports"].items():
        for filename, expected in report["files"].items():
            body = (WORK / "reports" / name / filename).read_bytes()
            if original.digest(body) != expected:
                raise ValueError("report changed after browser verification")
            directory = "" if name == "combined" else name + "/"
            key = original.PREFIX + "/fe/" + directory + filename
            current, metadata = None, None
            try:
                current, metadata = original.get_bytes(client, key)
            except ClientError as error:
                if error.response["Error"]["Code"] not in {"NoSuchKey", "404"}:
                    raise
            content_type = "application/json" if filename.endswith(".json") else "text/html; charset=utf-8"
            if current != body:
                if name == "combined":
                    previous = audit["previous_combined"][filename]
                    if metadata is None or original.digest(current) != previous["sha256"]:
                        raise ValueError("live FE report changed; refusing overwrite")
                    condition = {"IfMatch": previous["etag"]}
                else:
                    if current is not None:
                        raise ValueError("separate FE report already exists with different content")
                    condition = {"IfNoneMatch": "*"}
                client.put_object(
                    Bucket=original.BUCKET, Key=key, Body=body, ContentType=content_type,
                    CacheControl="no-cache", Metadata={"sha256": expected}, **condition,
                )
            downloaded, metadata = original.get_bytes(client, key)
            if downloaded != body or metadata["ContentType"] != content_type:
                raise ValueError("published FE object differs: " + key)
            verified[key] = {
                "sha256": original.digest(downloaded), "bytes": len(downloaded),
                "content_type": metadata["ContentType"], "etag": metadata["ETag"],
                "version_id": metadata.get("VersionId"),
            }
    original.write_json(WORK / "publication_receipt.json", {
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "verification": "downloaded_sha256", "objects": verified,
        "separate_report_urls": [report_url(name) for name, cell in REPORTS if cell is not None],
        "existing_combined_report_cleaned": True,
    })
    for name, cell in REPORTS:
        if cell is not None:
            print(report_url(name))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("preflight", "build", "publish"))
    parser.add_argument("--credentials-file", type=Path)
    args = parser.parse_args()
    if args.command == "build":
        build()
    else:
        if args.credentials_file is None:
            parser.error("--credentials-file is required")
        client = original.client_for(args.credentials_file)
        if args.command == "preflight":
            preflight(client)
        else:
            publish(client)
