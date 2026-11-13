"""Append existing Astra results to the user's original gallery without new judgments."""

import argparse
import hashlib
import html
import importlib.util
import json
import re
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLACEMENT = HERE.parent
VERSIONS = PLACEMENT / "versions"
BUCKET = "foundry-hp-enterprise-adobe-assets"
BASE = "https://foundry-aws-corp.adobe.io/asset/" + BUCKET + "/"
REVISIONS = ("v3_2", "v3_2_r2", "v3_2_r3", "v3_2_r4")
START = "<!-- hp-astra-added:start -->"
END = "<!-- hp-astra-added:end -->"
ADDED = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
STYLE = """<style>
.row{grid-template-rows:repeat(13,auto)}
.row>figure{grid-row:span 13}
.astra-result{border:1px solid #ccd5e0;border-left:4px solid #6b7280;border-radius:6px;padding:8px;background:#f8fafc;align-self:start;min-width:0;overflow-wrap:anywhere}
.astra-result.pass{border-left-color:#176b32}
.astra-result.review{border-left-color:#8a5c00}
.astra-result.fail,.astra-result.error{border-left-color:#a12622}
.astra-result.not-evaluated{padding:6px 8px;color:#666;background:#fafafa;font-size:12px}
.astra-result p{font-size:12px;line-height:1.4;margin:6px 0}
.astra-result pre{font-size:12px;max-height:420px;overflow:auto}
.astra-result details{margin-top:7px}.astra-result summary{cursor:pointer}
.astra-result .failed-check{color:#8b1e1e}
.astra-note{padding:10px 12px;border:1px solid #e3c858;background:#fff8db;border-radius:6px}
</style>"""


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


LEGACY = module(
    "original_gallery_v31",
    VERSIONS / "v3_1/original_gallery_update_20261110/gallery_update.py",
)


def digest(body):
    return hashlib.sha256(body).hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def emit(path, value):
    path = Path(path)
    body = (
        value
        if isinstance(value, bytes)
        else (
            json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
        ).encode()
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != body:
            raise ValueError("Existing evidence differs: " + str(path))
    else:
        with path.open("xb") as stream:
            stream.write(body)


def client():
    import foundry_aws_gateway

    s3 = foundry_aws_gateway.maybe_s3_client(BUCKET)
    if s3 is None:
        raise RuntimeError("Authenticated Foundry S3 access is unavailable")
    return s3


def get(s3, key):
    response = s3.get_object(Bucket=BUCKET, Key=key)
    try:
        return response["Body"].read(), response
    finally:
        response["Body"].close()


def label(version, candidate):
    return f"Astra {candidate.upper()} / R{REVISIONS.index(version) + 1} ({version})"


def panel(version, candidate, value, filename, image_sha):
    title = label(version, candidate)
    if value is None:
        state = "not-evaluated"
        content = f"<strong>{title}: NOT EVALUATED | no score</strong>"
    elif value["status"] == "error":
        if any(value[key] is not None for key in ("score", "verdict", "observation")):
            raise ValueError("A failed judgment cannot have a score or verdict")
        state = "error"
        content = (
            f"<strong>{title}: ERROR | no score</strong><p>"
            + html.escape(value["error_type"] + ": " + value["error"])
            + "</p>"
        )
    elif value["status"] == "complete":
        if value["verdict"] not in ("pass", "fail", "review"):
            raise ValueError("Invalid completed verdict")
        score = value["score"]
        if type(score) not in (int, float) or not 0 <= score <= 100:
            raise ValueError("Invalid completed score")
        state = value["verdict"]
        content = (
            f"<strong>{title}: {state.upper()} | {score:g}/100</strong><p>"
            + html.escape(value["observation"]["summary"])
            + "</p>"
        )
        failed = [
            key for key, matched in (value.get("checks") or {}).items() if not matched
        ]
        if failed:
            content += (
                '<p class="failed-check">Calibration criterion not met: '
                + html.escape("; ".join(failed))
                + "</p>"
            )
        content += (
            "<details><summary>Component evidence</summary><pre>"
            + html.escape(
                json.dumps(
                    value["observation"]["components"], indent=2, ensure_ascii=False
                )
            )
            + "</pre></details>"
        )
    else:
        raise ValueError("Only terminal actual judgments may be rendered")
    if value is not None:
        content += (
            f'<p><a href="{html.escape(filename, quote=True)}" download>'
            "All existing Astra results / provenance</a></p>"
        )
    return (
        f'<div class="astra-result {state}" data-astra-version="{version}" '
        f'data-astra-candidate="{candidate}" data-image-sha256="{image_sha}">'
        + content
        + "</div>"
    )


def render(source, records, filename):
    if START in source:
        raise ValueError(
            "Source already contains the Astra layer; refusing duplicate insertion"
        )
    slots = LEGACY.GalleryParser(source).slots
    by_url = {record["image_url"]: record for record in records}
    if len(by_url) != len(records) or len({slot["url"] for slot in slots}) != len(
        slots
    ):
        raise ValueError("Duplicate image identity")
    if set(by_url) != {slot["url"] for slot in slots}:
        raise ValueError("Results and original image columns differ")
    insertions = []
    for slot in slots:
        record = by_url[slot["url"]]
        if record["source_row_id"] != slot["source_row_id"]:
            raise ValueError("Result belongs to another source row")
        content = "".join(
            panel(
                version,
                candidate,
                record["results"][version][candidate],
                filename,
                record["image_sha256"],
            )
            for version in REVISIONS
            for candidate in ("p1", "p2")
        )
        insertions.append((slot["insert_at"], START + content + END))
    note = (
        '<p class="astra-note"><b>Added Astra P1/P2 candidates, R1-R4, below all existing judges.</b> '
        "Each result is bound to the exact image above it. R2 covers all128 images (two P2 errors); "
        "R1, R3 and R4 cover only six calibration images each. "
        "<b>NOT EVALUATED means no judgment was run, not a pass.</b> "
        "R1/R2 use the earlier material-geometry policy; R3/R4 use the later appearance-sensitive policy. "
        "None is promoted; known calibration misses and operational errors remain explicit. "
        "These are development/E2E diagnostics, not held-out accuracy or automatic acceptance. "
        f'<a href="{html.escape(filename, quote=True)}">Download actual results and provenance</a>. '
        "No new judgments or images were generated.</p>"
    )
    insertions += [
        (source.rindex("</style>") + len("</style>"), START + STYLE + END),
        (source.index("<section"), START + note + END),
    ]
    updated = source
    for offset, text in sorted(insertions, reverse=True):
        updated = updated[:offset] + text + updated[offset:]
    if ADDED.sub("", updated) != source:
        raise AssertionError("Original HTML bytes changed")
    return updated, slots


def actual_results():
    sys.path.insert(0, str(VERSIONS / "v3_2"))
    import build_review

    indexed, sources = {}, []
    for version in REVISIONS:
        root = VERSIONS / version
        freeze_path = root / "protocol_freeze.json"
        frozen = load(freeze_path)
        for item in frozen["files"]:
            if digest(Path(item["path"]).read_bytes()) != item["sha256"]:
                raise ValueError("Frozen judge dependency changed: " + item["path"])
        relative = (
            "evaluation/historical/summary.json"
            if version == "v3_2_r2"
            else "evaluation/calibration/summary.json"
        )
        path = root / relative
        summary = load(path)
        if summary["protocol_freeze_sha256"] != digest(freeze_path.read_bytes()):
            raise ValueError("Summary belongs to another frozen policy")
        indexed[version] = build_review.indexed(summary)
        sources.append(
            {
                "version": version,
                "summary_sha256": digest(path.read_bytes()),
                "protocol_freeze_sha256": summary["protocol_freeze_sha256"],
                "records": len(indexed[version]),
            }
        )
    return indexed, sources


def build():
    source_body = (HERE / "source/viewer.html").read_bytes()
    source_object = load(HERE / "source/object.json")
    if digest(source_body) != source_object["sha256"]:
        raise ValueError("Source snapshot changed")
    inventory = load(VERSIONS / "v3_1/evaluation/inventory.json")
    cases = {case["generated_image"]["url"]: case for case in inventory["records"]}
    slots = LEGACY.GalleryParser(source_body.decode()).slots
    if len(slots) != 128 or len({slot["source_row_id"] for slot in slots}) != 32:
        raise ValueError("Expected32 rows of four image columns")
    indexed, sources = actual_results()
    records, counts, local_files = [], Counter(), {}
    for slot in slots:
        case = cases[slot["url"]]
        if case["source_row_id"] != slot["source_row_id"]:
            raise ValueError("Original image/source-row binding changed")
        image = case["generated_image"]
        if digest(Path(image["local_path"]).read_bytes()) != image["sha256"]:
            raise ValueError("Original source image changed")
        results = {}
        for version in REVISIONS:
            results[version] = {}
            for candidate in ("p1", "p2"):
                value = indexed[version].get((case["id"], candidate))
                if value is not None:
                    if (
                        value["source_row_id"] != case["source_row_id"]
                        or value["generated_image"]["url"] != image["url"]
                        or value["generated_image"]["sha256"] != image["sha256"]
                        or value["twin_image"]["sha256"] != case["twin_image"]["sha256"]
                    ):
                        raise ValueError(
                            "Judge record belongs to another image or source"
                        )
                    if value["status"] == "error":
                        assessment = (
                            VERSIONS
                            / version
                            / "evaluation/historical"
                            / candidate
                            / case["id"]
                            / "assessment.json"
                        )
                        if load(assessment) != value:
                            raise ValueError(
                                "Error assessment differs from actual preserved failure"
                            )
                        evidence = (
                            assessment.parent / "p2_reconcile/attempt01/error.json"
                        )
                        if not evidence.is_file():
                            raise ValueError("Actual failed stage evidence is missing")
                        local_files[str(evidence)] = digest(evidence.read_bytes())
                        local_files[str(assessment)] = digest(assessment.read_bytes())
                    else:
                        local_files[value["result_path"]] = value["result_sha256"]
                results[version][candidate] = value
                counts[
                    version
                    + "/"
                    + candidate
                    + "/"
                    + (value["status"] if value else "not_evaluated")
                ] += 1
        records.append(
            {
                "id": case["id"],
                "source_row_id": case["source_row_id"],
                "image_url": image["url"],
                "image_sha256": image["sha256"],
                "image_path": image["local_path"],
                "results": results,
            }
        )
    document = {
        "source_html_sha256": digest(source_body),
        "model": "gpt-6-astra",
        "reasoning_effort": "high",
        "promoted": False,
        "new_judgments": 0,
        "new_images": 0,
        "sources": sources,
        "counts": dict(counts),
        "records": records,
        "scope": "Actual existing development judgments on E2E comparison images; R3/R4 appearance policy is prospective, not retrospective recovery.",
    }
    results_body = (
        json.dumps(document, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    ).encode()
    filename = "judge_astra_existing_" + digest(results_body)[:16] + ".json"
    updated, _ = render(source_body.decode(), records, filename)
    emit(HERE / "gallery" / filename, results_body)
    emit(HERE / "gallery/viewer.html", updated.encode())
    local_files.update(
        {
            str(HERE / "source/viewer.html"): digest(source_body),
            str(HERE / "source/object.json"): digest(
                (HERE / "source/object.json").read_bytes()
            ),
            str(Path(__file__)): digest(Path(__file__).read_bytes()),
            str(VERSIONS / "v3_1/evaluation/inventory.json"): digest(
                (VERSIONS / "v3_1/evaluation/inventory.json").read_bytes()
            ),
        }
    )
    emit(
        HERE / "build_audit.json",
        {
            "source_sha256": digest(source_body),
            "html_sha256": digest(updated.encode()),
            "results_sha256": digest(results_body),
            "results_filename": filename,
            "source_rows": 32,
            "image_columns": 128,
            "original_html_recovered_exactly": True,
            "added_actual_judgments": 292,
            "completed_judgments": 290,
            "explicit_errors": 2,
            "not_evaluated_panels": 732,
            "counts": dict(counts),
            "local_files": local_files,
        },
    )
    print(
        json.dumps(
            {"actual_judgments": 292, "errors": 2, "not_evaluated": 732, "new_calls": 0}
        )
    )


def verify_build():
    audit = load(HERE / "build_audit.json")
    for name, expected in audit["local_files"].items():
        if digest(Path(name).read_bytes()) != expected:
            raise ValueError("Build input changed: " + name)
    for name, expected in (
        ("viewer.html", audit["html_sha256"]),
        (audit["results_filename"], audit["results_sha256"]),
    ):
        if digest((HERE / "gallery" / name).read_bytes()) != expected:
            raise ValueError("Built report changed")
    return audit


def publish(s3):
    from botocore.exceptions import ClientError

    audit = verify_build()
    browser = load(HERE / "browser_validation.json")
    if not browser["passed"] or browser["html_sha256"] != audit["html_sha256"]:
        raise ValueError("Exact built report needs passing browser verification")
    source = load(HERE / "source/object.json")
    key = source["key"]
    current, metadata = get(s3, key)
    if digest(current) not in (source["sha256"], audit["html_sha256"]):
        raise ValueError(
            "Live gallery changed; preserve and merge current edits before publication"
        )
    if digest(current) == source["sha256"] and metadata["ETag"] != source["etag"]:
        raise ValueError("Live source metadata changed; refresh before publication")
    prefix = key.rsplit("/", 1)[0]
    backup_key = (
        prefix + "/judge_astra_backups/" + source["sha256"][:16] + "/viewer.html"
    )
    exports = [
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
    ]
    for export_key, body, content_type in exports:
        try:
            s3.put_object(
                Bucket=BUCKET,
                Key=export_key,
                Body=body,
                ContentType=content_type,
                IfNoneMatch="*",
                Metadata={"sha256": digest(body)},
            )
        except ClientError as error:
            if error.response["Error"]["Code"] not in ("PreconditionFailed", "412"):
                raise
        actual, response = get(s3, export_key)
        if actual != body or response["ContentType"] != content_type:
            raise ValueError("Existing backup/export differs; refusing overwrite")
    if digest(current) != audit["html_sha256"]:
        s3.put_object(
            Bucket=BUCKET,
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
    actual, response = get(s3, key)
    if (
        digest(actual) != audit["html_sha256"]
        or response["ContentType"] != source["content_type"]
    ):
        raise ValueError("Published original viewer differs from the verified build")
    if (
        ADDED.sub("", actual.decode()).encode()
        != (HERE / "source/viewer.html").read_bytes()
    ):
        raise ValueError("Published gallery did not preserve original bytes")
    emit(
        HERE / "publication_receipt.json",
        {
            "verified_at_utc": datetime.now(UTC).isoformat(),
            "url": BASE + key,
            "html_sha256": digest(actual),
            "etag": response["ETag"],
            "version_id": response.get("VersionId"),
            "backup_key": backup_key,
            "results_key": prefix + "/" + audit["results_filename"],
            "original_bytes_preserved": True,
            "content_types_verified": True,
            "new_judgments": 0,
            "new_images": 0,
        },
    )
    print(
        "Updated the exact original HTML; backup, results and HTML byte/type verified."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "verify", "publish"))
    args = parser.parse_args()
    if args.command == "build":
        build()
    elif args.command == "verify":
        verify_build()
    else:
        publish(client())
