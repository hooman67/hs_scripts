#!/usr/bin/env python3
"""Add compact V3.1 results without replacing the original gallery or judges."""

import argparse
import hashlib
import html
from html.parser import HTMLParser
import importlib.util
import json
import math
from pathlib import Path
import re
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
START = "<!-- hp-v31-added:start -->"
END = "<!-- hp-v31-added:end -->"
ADDED = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
STYLE = """<style>
.row{grid-template-rows:repeat(5,auto)}
.row>figure{display:grid;grid-template-rows:subgrid;grid-row:span 5;min-width:0}
.row>figure>a,.row>figure>.placement-judge{align-self:start}
.row>figure>.placement-judge{margin-top:0}
.v31-result{border:1px solid #ccd5e0;border-left-width:4px;border-radius:6px;padding:8px;background:#f8fafc;align-self:start}
.v31-pass{border-left-color:#176b32}.v31-review{border-left-color:#8a5c00}
.v31-fail,.v31-error{border-left-color:#a12622}
.v31-title{font-weight:700}.v31-reason{font-size:12px;line-height:1.4;margin:5px 0 0;overflow-wrap:anywhere}
.v31-note{padding:9px 12px;border:1px solid #e3c858;background:#fff8db;border-radius:6px}
</style>"""


def digest(body):
    return hashlib.sha256(body).hexdigest()


def load(path):
    return json.loads(path.read_text())


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n")


class GalleryParser(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.source = source
        self.lines = [0] + [match.end() for match in re.finditer("\n", source)]
        self.figure = None
        self.row_id = None
        self.heading = None
        self.slots = []
        self.feed(source)
        self.close()

    def source_offset(self):
        line, column = self.getpos()
        return self.lines[line - 1] + column

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h2":
            self.heading = []
        if tag == "figure":
            if self.figure is not None:
                raise ValueError("nested source figures are unsupported")
            self.figure = {"source_row_id": self.row_id, "images": [], "judge_depth": 0}
        if self.figure is None:
            return
        if tag == "img":
            self.figure["images"].append(attrs["src"])
        if tag == "details":
            if "placement-judge" in attrs.get("class", "").split():
                if "judge_start" in self.figure:
                    raise ValueError("multiple original judges in one image column")
                self.figure["judge_start"] = self.source_offset()
                self.figure["judge_depth"] = 1
            elif self.figure["judge_depth"]:
                self.figure["judge_depth"] += 1

    def handle_data(self, data):
        if self.heading is not None:
            self.heading.append(data)

    def handle_endtag(self, tag):
        if tag == "h2" and self.heading is not None:
            self.row_id = "".join(self.heading).strip()
            self.heading = None
        if self.figure is None:
            return
        if tag == "details" and self.figure["judge_depth"]:
            self.figure["judge_depth"] -= 1
            if self.figure["judge_depth"] == 0:
                self.figure["judge_end"] = self.source.index(">", self.source_offset()) + 1
        if tag == "figure":
            if "judge_start" in self.figure:
                if len(self.figure["images"]) != 1 or "judge_end" not in self.figure:
                    raise ValueError("source judge is not bound to exactly one image")
                slot = self.figure
                slot["url"] = slot["images"][0]
                slot["insert_at"] = self.source_offset()
                slot["original_judge"] = self.source[slot["judge_start"]:slot["judge_end"]]
                self.slots.append(slot)
            self.figure = None


def result_html(version, value):
    status = value["status"]
    if status == "complete":
        verdict, score, reason = value["verdict"], value["score"], value["short_reason"]
        if (verdict not in {"pass", "review", "fail"} or type(score) not in (int, float)
                or not math.isfinite(score) or not 0 <= score <= 100
                or not isinstance(reason, str) or not reason.strip()):
            raise ValueError("invalid completed V3.1 result")
        title = f"V3.1 {version}: {verdict.title()} | {score:g}/100"
        css = verdict
    elif status == "error":
        if any(value[field] is not None for field in ("verdict", "score", "short_reason")) or not value.get("error"):
            raise ValueError("failed V3.1 result must be explicit, not a fallback verdict")
        title, reason, css = f"V3.1 {version}: ERROR | no score", "Judging failed; see the result export for the recorded error.", "error"
    else:
        raise ValueError(f"V3.1 result is not terminal: {status}")
    return (
        f'<div class="v31-result v31-{css}" data-v31-version="{version}">'
        f'<div class="v31-title">{html.escape(title)}</div>'
        f'<p class="v31-reason">{html.escape(" ".join(reason.split()))}</p></div>'
    )


def render(source, records, result_filename):
    if START in source:
        raise ValueError("source already contains an added V3.1 layer; refusing duplicate insertion")
    slots = GalleryParser(source).slots
    slots_by_url = {slot["url"]: slot for slot in slots}
    records_by_url = {record["generated_image"]["url"]: record for record in records}
    if len(slots_by_url) != len(slots) or len(records_by_url) != len(records):
        raise ValueError("duplicate source/result image URL")
    if set(slots_by_url) != set(records_by_url):
        raise ValueError("source image columns and V3.1 result URLs differ")
    insertions = []
    for url, slot in slots_by_url.items():
        record = records_by_url[url]
        if record["source_row_id"] != slot["source_row_id"]:
            raise ValueError("judge source row differs from the original image column")
        added = result_html("r1", record["r1"]) + result_html("r2", record["r2"])
        insertions.append((slot["insert_at"], START + added + END))
    note = (
        '<p class="v31-note">Added experimental <b>V3.1 r1</b> and <b>r2</b> results below the '
        'unchanged original V3 results, aligned to the same image columns. Neither candidate is '
        'validated/promoted; known calibration misses remain. '
        f'<a href="{html.escape(result_filename, quote=True)}">Download both V3.1 result sets</a>.</p>'
    )
    insertions.extend([
        (source.index("</style>") + len("</style>"), START + STYLE + END),
        (source.index("<section"), START + note + END),
    ])
    updated = source
    for offset, added in sorted(insertions, reverse=True):
        updated = updated[:offset] + added + updated[offset:]
    if ADDED.sub("", updated) != source:
        raise AssertionError("insertion changed original HTML bytes")
    after = GalleryParser(updated).slots
    if [(slot["url"], slot["original_judge"]) for slot in after] != [
            (slot["url"], slot["original_judge"]) for slot in slots]:
        raise AssertionError("original judge/image columns changed")
    return updated, slots


def build(results_path):
    source_body = (HERE / "source/viewer.html").read_bytes()
    source_meta = load(HERE / "source/object.json")
    results_body = results_path.read_bytes()
    document = json.loads(results_body)
    if digest(source_body) != source_meta["sha256"] or document["source_html_sha256"] != source_meta["sha256"]:
        raise ValueError("source snapshot and evaluation source hashes differ")
    records = document["records"]
    counts = {version: {state: sum(row[version]["status"] == state for row in records)
                        for state in ("complete", "error")} for version in ("r1", "r2")}
    if len(records) != 128 or any(sum(states.values()) != 128 for states in counts.values()):
        raise ValueError("both candidates must have exactly128 terminal image results")
    if (sum(row["r1"]["reused"] is True for row in records) != 128
            or sum(row["r2"]["reused"] is True for row in records) != 6):
        raise ValueError("reuse differs from the authorized128 r1 plus six r2 results")
    filename = "judge_v31_" + digest(results_body)[:16] + ".json"
    updated, slots = render(source_body.decode("utf-8"), records, filename)
    rows = {slot["source_row_id"] for slot in slots}
    if len(rows) != 32 or any(sum(slot["source_row_id"] == row for slot in slots) != 4 for row in rows):
        raise ValueError("expected32 original rows and four judged image columns per row")
    output = HERE / "gallery"
    output.mkdir(exist_ok=True)
    (output / "viewer.html").write_bytes(updated.encode("utf-8"))
    (output / filename).write_bytes(results_body)
    audit = {
        "source_sha256": digest(source_body), "source_etag": source_meta["ETag"],
        "source_version_id": source_meta["VersionId"], "source_rows": 32, "image_columns": 128,
        "original_html_recovered_exactly": True, "original_judges_unchanged": 128,
        "counts": counts, "r1_reused": 128, "r2_reused": 6, "r2_new": 122,
        "results_filename": filename, "results_sha256": digest(results_body),
        "html_sha256": digest(updated.encode("utf-8")),
    }
    write_json(HERE / "build_audit.json", audit)
    print(json.dumps(audit))


def client_for(credentials_file):
    spec = importlib.util.spec_from_file_location(
        "hp_prior_report", PROJECT / "eval_sets/hp_lifestyle_v6_2_v6_3_pr4523_pr4417_20261109/report.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.s3_client(credentials_file)


def get_bytes(client, bucket, key):
    response = client.get_object(Bucket=bucket, Key=key)
    try:
        return response["Body"].read(), response
    finally:
        response["Body"].close()


def publish(client):
    audit = load(HERE / "build_audit.json")
    source = load(HERE / "source/object.json")
    bucket, key = source["bucket"], source["key"]
    updated = (HERE / "gallery/viewer.html").read_bytes()
    results = (HERE / "gallery" / audit["results_filename"]).read_bytes()
    if digest(updated) != audit["html_sha256"] or digest(results) != audit["results_sha256"]:
        raise ValueError("gallery changed after its build audit")
    put_fields = client.meta.service_model.operation_model("PutObject").input_shape.members
    if not {"IfMatch", "IfNoneMatch"} <= set(put_fields):
        raise RuntimeError("installed S3 SDK does not support safe conditional publication")
    current, current_meta = get_bytes(client, bucket, key)
    if digest(current) == audit["html_sha256"]:
        return verify_publication(client, bucket, key, audit, source)
    if current_meta["ETag"] != source["ETag"] or digest(current) != source["sha256"]:
        raise ValueError("live gallery changed; re-read and merge it before publishing")
    prefix = key.rsplit("/", 1)[0]
    backup_key = prefix + "/judge_v31_backups/" + source["sha256"][:16] + "/viewer.html"
    result_key = prefix + "/" + audit["results_filename"]
    from botocore.exceptions import ClientError

    for object_key, body, content_type in (
        (backup_key, current, source["ContentType"]),
        (result_key, results, "application/json; charset=utf-8"),
    ):
        try:
            client.put_object(
                Bucket=bucket, Key=object_key, Body=body, IfNoneMatch="*", ContentType=content_type,
                Metadata={"sha256": digest(body), "hp-v31-source-sha256": source["sha256"]},
            )
        except ClientError as error:
            if error.response["Error"]["Code"] not in {"PreconditionFailed", "412"}:
                raise
        copied, _ = get_bytes(client, bucket, object_key)
        if copied != body:
            raise ValueError(f"existing backup/results object differs; refusing overwrite: {object_key}")
    metadata = {**source["Metadata"], "sha256": audit["html_sha256"], "hp-v31-source-sha256": source["sha256"]}
    client.put_object(
        Bucket=bucket, Key=key, Body=updated, IfMatch=source["ETag"],
        ContentType=source["ContentType"], CacheControl="no-cache", Metadata=metadata,
    )
    return verify_publication(client, bucket, key, audit, source)


def verify_publication(client, bucket, key, audit, source):
    html_body, metadata = get_bytes(client, bucket, key)
    result_key = key.rsplit("/", 1)[0] + "/" + audit["results_filename"]
    results_body, results_meta = get_bytes(client, bucket, result_key)
    backup_key = key.rsplit("/", 1)[0] + "/judge_v31_backups/" + source["sha256"][:16] + "/viewer.html"
    backup, _ = get_bytes(client, bucket, backup_key)
    if (digest(html_body) != audit["html_sha256"] or digest(results_body) != audit["results_sha256"]
            or digest(backup) != source["sha256"] or metadata["ContentType"] != source["ContentType"]
            or results_meta["ContentType"] != "application/json; charset=utf-8"):
        raise ValueError("published gallery, backup or result bytes differ from their audit")
    receipt = {
        **audit, "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "url": "https://foundry-aws-corp.adobe.io/asset/" + bucket + "/" + key,
        "published_version_id": metadata.get("VersionId"), "published_etag": metadata["ETag"],
        "backup_key": backup_key, "results_key": result_key, "verification": "downloaded_sha256",
    }
    write_json(HERE / "publication_receipt.json", receipt)
    print(json.dumps(receipt))
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "publish"))
    parser.add_argument("--results", type=Path, default=HERE / "evaluation/gallery_results.json")
    parser.add_argument("--credentials-file", type=Path)
    args = parser.parse_args()
    if args.command == "build":
        build(args.results)
    else:
        if args.credentials_file is None:
            parser.error("--credentials-file is required")
        publish(client_for(args.credentials_file))
