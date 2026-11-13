"""Publish complete P1 revision comparisons in the user's unchanged image gallery."""

import argparse
import html
import json
import re
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

import complete

HERE = Path(__file__).resolve().parent
OLD = complete.module("previous_astra_report", complete.PREVIOUS / "update.py")
STYLE = (
    OLD.STYLE.replace("repeat(13,auto)", "repeat(10,auto)")
    .replace("span 13", "span 10")
    .replace(
        "</style>",
        ".astra-previous{align-self:start;min-width:0;font-size:12px}"
        ".astra-previous>summary{cursor:pointer}"
        ".astra-previous .astra-result{margin-top:8px}</style>",
    )
)


def original_layer(source):
    return OLD.ADDED.sub("", source)


def render(source, records, filename, previous_filename):
    base = original_layer(source)
    slots = OLD.LEGACY.GalleryParser(base).slots
    by_url = {record["image_url"]: record for record in records}
    if len(by_url) != len(records) or {slot["url"] for slot in slots} != set(by_url):
        raise ValueError("Original image columns and results differ")
    insertions = []
    for slot in slots:
        record = by_url[slot["url"]]
        if record["source_row_id"] != slot["source_row_id"]:
            raise ValueError("Result belongs to another original row")
        for version in OLD.REVISIONS:
            value = record["results"][version]["p1"]
            if value is None or value["status"] != "complete":
                raise ValueError("All four selected P1 judgments must be complete")
        primary = "".join(
            OLD.panel(
                version,
                "p1",
                record["results"][version]["p1"],
                filename,
                record["image_sha256"],
            )
            for version in OLD.REVISIONS
        )
        previous = (
            '<details class="astra-previous"><summary>Other architecture: P2 '
            "(existing results only; not a repeat pass)</summary>"
            + "".join(
                OLD.panel(
                    version,
                    "p2",
                    record["results"][version]["p2"],
                    filename,
                    record["image_sha256"],
                )
                for version in OLD.REVISIONS
            )
            + "</details>"
        )
        insertions.append((slot["insert_at"], OLD.START + primary + previous + OLD.END))
    note = (
        '<p class="astra-note"><b>Astra P1: all four revisions now evaluated '
        "on every one of the128 images.</b> P1 and P2 are different judge architectures, "
        "not repeat passes; P1 is used consistently, without choosing by score. "
        "Existing P2 results remain in the collapsed Other architecture panel. "
        "R1/R2 use the earlier material-geometry policy; R3/R4 use the later "
        "appearance-sensitive policy. None is promoted; known failed calibration "
        "criteria remain explicit. These are development/E2E comparisons, not held-out "
        "accuracy or automatic acceptance.366 new judgments; no new images or prompt changes. "
        f'<a href="{html.escape(filename, quote=True)}">Download current results/provenance</a>. '
        f'<a href="{html.escape(previous_filename, quote=True)}">Previous Astra snapshot</a>.</p>'
    )
    insertions += [
        (base.rindex("</style>") + len("</style>"), OLD.START + STYLE + OLD.END),
        (base.index("<section"), OLD.START + note + OLD.END),
    ]
    result = base
    for offset, text in sorted(insertions, reverse=True):
        result = result[:offset] + text + result[offset:]
    if original_layer(result) != original_layer(source):
        raise AssertionError("Original images/old judges changed")
    return result


def verify_acquisitions(result):
    sys.path.insert(0, str(complete.VERSIONS / "v3_2"))
    import common

    for stage in result["stages"].values():
        value = complete.load(stage["path"])
        acquisition = value.get("visual_acquisition")
        if acquisition is None:
            continue
        if complete.sha(acquisition["path"]) != acquisition["sha256"]:
            raise ValueError("Actual acquisition evidence changed")
        actual = complete.load(acquisition["path"])
        if actual["observation"]["record"] != acquisition["record"]:
            raise ValueError("Acquisition record differs from actual result")
        if complete.sha(actual["chunks_path"]) != actual["chunks_sha256"]:
            raise ValueError("Acquisition raw stream changed")
        collector = common.Collector()
        with Path(actual["chunks_path"]).open() as stream:
            for line in stream:
                collector.feed(json.loads(line))
        if collector.result() != actual["observation"]:
            raise ValueError("Acquisition record differs from actual model stream")


def build():
    plan = complete.verify_plan()
    existing, sources = OLD.actual_results()
    import build_review

    indexes = {}
    files = {
        str(HERE / "plan.json"): complete.sha(HERE / "plan.json"),
        str(Path(__file__)): complete.sha(__file__),
    }
    for version in OLD.REVISIONS:
        path = HERE / "evaluation" / version / "summary.json"
        summary = complete.load(path)
        if (
            summary["protocol_freeze_sha256"]
            != plan["versions"][version]["protocol_freeze_sha256"]
            or not summary["complete"]
            or summary["expected"] != 128
            or any(row["candidate"] != "p1" for row in summary["records"])
        ):
            raise ValueError("Every revision needs128 actual completed P1 results")
        indexes[version] = build_review.indexed(summary)
        sources.append(
            {
                "version": version,
                "architecture": "p1",
                "summary_sha256": complete.sha(path),
                "protocol_freeze_sha256": summary["protocol_freeze_sha256"],
            }
        )
        files[str(path)] = complete.sha(path)
    records, counts = [], Counter()
    for case in plan["cases"]:
        results = {}
        for version in OLD.REVISIONS:
            row = indexes[version][(case["id"], "p1")]
            complete.validate_reuse(
                row, case, plan["versions"][version]["protocol_freeze_sha256"]
            )
            verify_acquisitions(complete.load(row["result_path"]))
            prior = existing[version].get((case["id"], "p1"))
            if prior is not None and any(
                row[key] != prior[key]
                for key in (
                    "result_path",
                    "result_sha256",
                    "observation",
                    "score",
                    "verdict",
                    "checks",
                )
            ):
                raise ValueError("Existing completed P1 judgment was changed/redrawn")
            files[row["result_path"]] = row["result_sha256"]
            results[version] = {
                "p1": row,
                "p2": existing[version].get((case["id"], "p2")),
            }
            for candidate, value in results[version].items():
                counts[
                    f"{version}/{candidate}/"
                    + (value["status"] if value else "not_evaluated")
                ] += 1
        records.append(
            {
                "id": case["id"],
                "source_row_id": case["source_row_id"],
                "image_url": case["generated_image"]["url"],
                "image_sha256": case["generated_image"]["sha256"],
                "image_path": case["generated_image"]["local_path"],
                "results": results,
            }
        )
    source = (HERE / "source/viewer.html").read_bytes()
    object_info = complete.load(HERE / "source/object.json")
    current, metadata = OLD.get(OLD.client(), object_info["key"])
    if current != source or metadata["ETag"] != object_info["etag"]:
        raise ValueError(
            "Live report changed since preparation; inspect/merge before publishing"
        )
    previous_names = set(
        re.findall(r"judge_astra_existing_[a-f0-9]+\.json", source.decode())
    )
    if len(previous_names) != 1:
        raise ValueError("Expected one exact previous Astra result export")
    previous_name = previous_names.pop()
    previous_key = object_info["key"].rsplit("/", 1)[0] + "/" + previous_name
    previous_body, _ = OLD.get(OLD.client(), previous_key)
    if previous_body != (complete.PREVIOUS / "gallery" / previous_name).read_bytes():
        raise ValueError("Previous live result export changed")
    complete.immutable(HERE / "source" / previous_name, previous_body)
    old_v31_name = "judge_v31_65e32394a80098e3.json"
    complete.immutable(
        HERE / "source" / old_v31_name,
        (complete.PREVIOUS / "source" / old_v31_name).read_bytes(),
    )
    document = {
        "source_html_sha256": complete.sha(HERE / "source/viewer.html"),
        "model": "gpt-6-astra",
        "reasoning_effort": "high",
        "selected_architecture": "p1",
        "promoted": False,
        "new_judgments": plan["expected_new"],
        "new_images": 0,
        "plan_sha256": complete.sha(HERE / "plan.json"),
        "sources": sources,
        "counts": dict(counts),
        "records": records,
        "transport_policy": plan["transport_policy"],
        "scope": "Development comparison, not held-out accuracy or promotion.",
    }
    results_body = (json.dumps(document, indent=2, ensure_ascii=False) + "\n").encode()
    filename = "judge_astra_all_p1_" + OLD.digest(results_body)[:16] + ".json"
    updated = render(source.decode(), records, filename, previous_name).encode()
    complete.immutable(HERE / "gallery" / filename, results_body)
    complete.immutable(HERE / "gallery/viewer.html", updated)
    complete.immutable(
        HERE / "build_audit.json",
        {
            "source_sha256": OLD.digest(source),
            "html_sha256": OLD.digest(updated),
            "results_sha256": OLD.digest(results_body),
            "results_filename": filename,
            "previous_results_filename": previous_name,
            "source_rows": 32,
            "image_columns": 128,
            "complete_p1": 512,
            "new_p1": 366,
            "reused_p1": 146,
            "retained_p2_complete": 144,
            "retained_p2_errors": 2,
            "unrun_p2": 366,
            "counts": dict(counts),
            "local_files": files,
            "original_non_astra_bytes_preserved": True,
        },
    )
    print(
        json.dumps(
            {"complete_p1": 512, "new_judgments": 366, "existing_p2_preserved": 146}
        ),
        flush=True,
    )


def verify_build():
    complete.verify_plan()
    audit = complete.load(HERE / "build_audit.json")
    for path, digest in audit["local_files"].items():
        if complete.sha(path) != digest:
            raise ValueError("Verified report dependency changed: " + path)
    for name, digest in (
        ("viewer.html", audit["html_sha256"]),
        (audit["results_filename"], audit["results_sha256"]),
    ):
        if complete.sha(HERE / "gallery" / name) != digest:
            raise ValueError("Built report changed")
    return audit


def publish(s3):
    from botocore.exceptions import ClientError

    audit = verify_build()
    browser = complete.load(HERE / "browser_validation.json")
    if not browser["passed"] or browser["html_sha256"] != audit["html_sha256"]:
        raise ValueError("Exact built report needs passing browser verification")
    source = complete.load(HERE / "source/object.json")
    key = source["key"]
    current, metadata = OLD.get(s3, key)
    if OLD.digest(current) not in (source["sha256"], audit["html_sha256"]):
        raise ValueError("Live gallery changed; preserve and merge current edits")
    if OLD.digest(current) == source["sha256"] and metadata["ETag"] != source["etag"]:
        raise ValueError("Live source metadata changed; refresh before publication")
    prefix = key.rsplit("/", 1)[0]
    backup_key = (
        prefix + "/judge_astra_backups/" + source["sha256"][:16] + "/viewer.html"
    )
    for export_key, body, content_type in (
        (
            backup_key,
            (HERE / "source/viewer.html").read_bytes(),
            source["content_type"],
        ),
        (
            prefix + "/" + audit["results_filename"],
            (HERE / "gallery" / audit["results_filename"]).read_bytes(),
            "application/json; charset=utf-8",
        ),
    ):
        try:
            s3.put_object(
                Bucket=OLD.BUCKET,
                Key=export_key,
                Body=body,
                ContentType=content_type,
                IfNoneMatch="*",
                Metadata={"sha256": OLD.digest(body)},
            )
        except ClientError as error:
            if error.response["Error"]["Code"] not in ("PreconditionFailed", "412"):
                raise
        actual, response = OLD.get(s3, export_key)
        if actual != body or response["ContentType"] != content_type:
            raise ValueError("Backup/export differs; refusing overwrite")
    if OLD.digest(current) != audit["html_sha256"]:
        s3.put_object(
            Bucket=OLD.BUCKET,
            Key=key,
            Body=(HERE / "gallery/viewer.html").read_bytes(),
            IfMatch=source["etag"],
            ContentType=source["content_type"],
            CacheControl="no-cache",
            Metadata={
                **source["metadata"],
                "sha256": audit["html_sha256"],
                "hp-astra-source-sha256": source["sha256"],
            },
        )
    actual, response = OLD.get(s3, key)
    if (
        OLD.digest(actual) != audit["html_sha256"]
        or response["ContentType"] != source["content_type"]
    ):
        raise ValueError("Published viewer differs from the verified build")
    if original_layer(actual.decode()) != original_layer(
        (HERE / "source/viewer.html").read_text()
    ):
        raise ValueError("Original non-Astra HTML bytes changed")
    complete.immutable(
        HERE / "publication_receipt.json",
        {
            "verified_at_utc": datetime.now(UTC).isoformat(),
            "url": OLD.BASE + key,
            "html_sha256": OLD.digest(actual),
            "etag": response["ETag"],
            "version_id": response.get("VersionId"),
            "backup_key": backup_key,
            "results_key": prefix + "/" + audit["results_filename"],
            "content_types_verified": True,
            "complete_p1": 512,
            "new_judgments": 366,
            "new_images": 0,
            "promoted": False,
            "original_non_astra_bytes_preserved": True,
            "existing_completed_p1_and_all_p2_preserved": True,
        },
    )
    print(json.dumps({"published": OLD.BASE + key, "complete_p1": 512}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "verify", "publish"))
    args = parser.parse_args()
    if args.command == "build":
        build()
    elif args.command == "verify":
        verify_build()
    else:
        publish(OLD.client())
