"""Freeze and publish an image-only human review; never call a judge or generator."""

import argparse
import base64
import hashlib
import importlib.util
import io
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlencode

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
FULL = PROJECT / "eval_sets/hp_lifestyle_v6_4_full160_pr4523_20261110"
SMALL = "eval_sets/hp_lifestyle_v6_4_pr4523_30_20261110/fe/"
COMPARISON = "eval_sets/hp_lifestyle_v6_3_full160_pr4523_pr4417_20261110/fe/"
BUCKET = "foundry-hp-enterprise-adobe-assets"
BASE = "https://foundry-aws-corp.adobe.io/asset/" + BUCKET + "/"
PREFIX = "judge_evals/hp_placement_blind_review_20261111/fe/"
TITLE = "HP V6.4 / PR4523 - blind placement appearance review"
SEED = "hp-blind-placement-20261111-v1"
VENDOR = Path.home() / ".claude/scripts/fe_html"
AUDIT = PROJECT / "judge/placement/versions/v3_2_r4/astra_exemplar_audit/analysis.json"
DEVELOPMENT = [
    PROJECT / "judge/placement/versions/v3_1/evaluation/inventory.json",
    PROJECT / "judge/placement/versions/v3_2_r2/evaluation/refiner/corpus.json",
    PROJECT / "judge/placement/versions/v3_2/astra_appearance_revision/corpus.json",
    PROJECT / "judge/placement/versions/v3_2_r4/astra_exemplar_audit/input.json",
]


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
            json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False) + "\n"
        ).encode()
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != body:
            raise ValueError("Refusing to overwrite frozen evidence: " + str(path))
    else:
        with path.open("xb") as stream:
            stream.write(body)


def client():
    import foundry_aws_gateway

    result = foundry_aws_gateway.maybe_s3_client(BUCKET)
    if result is None:
        raise RuntimeError("Authenticated Foundry S3 access is unavailable")
    return result


def get(s3, key):
    response = s3.get_object(Bucket=BUCKET, Key=key)
    try:
        body = response["Body"].read()
    finally:
        response["Body"].close()
    return body, response


def rank(label, value):
    return digest((SEED + "/" + label + "/" + str(value)).encode())


def identity(row):
    return " / ".join(map(str, row["key"]))


def select(rows, excluded_keys, excluded_hashes, excluded_prompts):
    eligible = [
        row
        for row in rows
        if identity(row) not in excluded_keys
        and row["output"]["image_sha256"] not in excluded_hashes
        and row["prompt"]["text_sha256"] not in excluded_prompts
        and row["output"]["reuse_status"] == "new"
    ]
    selected, used_hashes, used_prompts = [], set(), set()
    for device, count in (
        ("cashmere", 8),
        ("elitebook", 8),
        ("magic", 7),
        ("tassel", 7),
    ):
        cameras = sorted(
            {row["key"][1] for row in eligible if row["key"][0] == device},
            key=lambda camera: rank("camera", device + camera),
        )
        if len(cameras) != 4:
            raise ValueError("Expected four eligible cameras per product")
        for index in range(count):
            camera = cameras[index % len(cameras)]
            candidates = sorted(
                (row for row in eligible if row["key"][:2] == [device, camera]),
                key=lambda row: rank("selection", identity(row)),
            )
            chosen = next(
                (
                    row
                    for row in candidates
                    if row["output"]["image_sha256"] not in used_hashes
                    and row["prompt"]["text_sha256"] not in used_prompts
                ),
                None,
            )
            if chosen is None:
                raise ValueError("Insufficient independent eligible scene groups")
            selected.append(chosen)
            used_hashes.add(chosen["output"]["image_sha256"])
            used_prompts.add(chosen["prompt"]["text_sha256"])
    partitions = {
        identity(row): "calibration" if index < 20 else "held_out"
        for index, row in enumerate(
            sorted(selected, key=lambda row: rank("partition", identity(row)))
        )
    }
    return (
        sorted(selected, key=lambda row: rank("display", identity(row))),
        partitions,
        len(eligible),
    )


def questions():
    needs = load(AUDIT)["human_reviewed_evidence_still_needed"]
    appearance = {
        "key": "custom",
        "name": "Appearance",
        "options": [
            {"value": value, "label": label, "tone": tone}
            for value, label, tone in [
                ("acceptable", "Acceptable", "good"),
                ("minor", "Mildly awkward - minor concern", "neutral"),
                ("material", "Material concern", "bad"),
                ("unresolved", "Unresolved / disputed", "skip"),
                ("not_visible", "Not visible / not applicable", "skip"),
            ]
        ],
    }
    result = [
        {
            "text": item["boundary"],
            "rubric": appearance,
            "comment_box": True,
            "hard_check": False,
        }
        for item in needs["priority_contrasts"]
    ]
    result.append(
        {
            "text": "Physical feasibility (separate from appearance).",
            "rubric": {
                "key": "custom",
                "name": "Physical feasibility",
                "options": [
                    {"value": value, "label": label, "tone": tone}
                    for value, label, tone in [
                        ("feasible", "Appears feasible", "good"),
                        ("infeasible", "Appears infeasible", "bad"),
                        ("unresolved", "Unresolved / disputed", "skip"),
                        ("not_applicable", "Not applicable", "skip"),
                    ]
                ],
            },
            "comment_box": True,
            "hard_check": False,
        }
    )
    return result


def development_exclusions():
    hashes, prompts = set(), set()

    def walk(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "scene_prompt" and isinstance(child, str):
                    prompts.add(digest(child.encode()))
                if "sha256" in key and isinstance(child, str) and len(child) == 64:
                    hashes.add(child)
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    for path in DEVELOPMENT:
        walk(load(path))
    return hashes, prompts


def annotation_exclusions(document, source):
    if len({row["meta_data"]["row_idx"] for row in source["rows"]}) != len(
        source["rows"]
    ):
        raise ValueError("Ambiguous annotation row indices")
    mapping = {str(row["meta_data"]["row_idx"]): row for row in source["rows"]}
    excluded = set()
    for annotation in document["rows"]:
        if not (
            annotation.get("answers")
            or annotation.get("comment")
            or annotation.get("question_comments")
        ):
            continue
        row = mapping[str(annotation["row_idx"])]
        if annotation["key"] != row["meta_data"]["evalset_item_id"]:
            raise ValueError("Published annotation/source identity mismatch")
        excluded.add(annotation["key"])
    return excluded


def prepare():
    if (HERE / "freeze.json").exists():
        verify()
        print("Existing frozen review verified; no selection redrawn.")
        return
    s3 = client()
    snapshots = []

    def snapshot(key):
        body, response = get(s3, key)
        path = HERE / "source" / key
        emit(path, body)
        snapshots.append(
            {
                "key": key,
                "path": str(path),
                "sha256": digest(body),
                "etag": response["ETag"],
                "content_type": response["ContentType"],
            }
        )
        return json.loads(body)

    generation = snapshot("eval_sets/" + FULL.name + "/data/generation.json")
    if generation != load(FULL / "public/data/generation.json"):
        raise ValueError("Live full160 source differs from the native audited source")
    reviewed = snapshot(SMALL + "data_source_prompts_20261110.json")
    comparison = snapshot(COMPARISON + "data.json")
    excluded_keys = {row["meta_data"]["evalset_item_id"] for row in reviewed["rows"]}
    if len(generation["rows"]) != 160 or len(excluded_keys) != 30:
        raise ValueError(
            "Expected160 existing images and30 known reviewed source slots"
        )
    listing = []
    for prefix, source in ((SMALL, reviewed), (COMPARISON, comparison)):
        keys = sorted(
            item["Key"]
            for page in s3.get_paginator("list_objects_v2").paginate(
                Bucket=BUCKET, Prefix=prefix + "annotations/"
            )
            for item in page.get("Contents", [])
            if item["Key"].endswith(".json")
        )
        listing.append({"prefix": prefix + "annotations/", "keys": keys})
        for key in keys:
            excluded_keys.update(annotation_exclusions(snapshot(key), source))
    hashes, prompts = development_exclusions()
    selected, partitions, eligible_count = select(
        generation["rows"], excluded_keys, hashes, prompts
    )
    private, public_rows = [], []
    for index, row in enumerate(selected, 1):
        output = row["output"]
        if output["status"] != "done" or output["error"] is not None:
            raise ValueError("Selected output is not a successful generation")
        if (
            output["lineage"]["source_commit"]
            != "d1e5ae5323dedebc3b06ed173a3731307bd0623a"
        ):
            raise ValueError("Selected output is not the pinned PR4523 pipeline")
        key = output["image"].removeprefix(BASE)
        if BASE + key != output["image"] or not key.startswith(
            "eval_sets/" + FULL.name + "/"
        ):
            raise ValueError("Image escaped the approved original study")
        path = FULL / "public" / key.split(FULL.name + "/", 1)[1]
        body, response = get(s3, key)
        if digest(body) != output["image_sha256"] or body != path.read_bytes():
            raise ValueError("Live image differs from the native output")
        from PIL import Image

        with Image.open(io.BytesIO(body)) as image:
            if image.size != (2368, 1776) or image.format != "PNG":
                raise ValueError("Unexpected original image dimensions or format")
            image.verify()
        record = FULL / "public/data/records" / Path(output["record_url"]).name
        if digest(record.read_bytes()) != output["record_sha256"]:
            raise ValueError("Native record changed")
        native = load(record)
        if (
            native["image_sha256"] != digest(body)
            or native["prompt_sha256"] != row["prompt"]["text_sha256"]
            or native["prompt"] != row["prompt"]["text"]
            or native["job_id"] != output["job_id"]
        ):
            raise ValueError("Image, prompt and native job binding differ")
        review_id = "R" + str(index).zfill(3)
        private.append(
            {
                "review_id": review_id,
                "source_key": identity(row),
                "partition": partitions[identity(row)],
                "source_row": row["key"],
                "prompt_sha256": row["prompt"]["text_sha256"],
                "image_sha256": digest(body),
                "image_url": output["image"],
                "image_path": str(path),
                "image_etag": response["ETag"],
                "record_path": str(record),
                "record_sha256": digest(record.read_bytes()),
            }
        )
        public_rows.append(
            {
                "row_idx": index,
                "evalset_item_id": review_id,
                "meta": {},
                "assets": [{"kind": "image", "src": output["image"], "label": "Scene"}],
            }
        )
        print(f"Verified original image {index}/30", flush=True)
    spec = importlib.util.spec_from_file_location(
        "official_fe", VENDOR / "parquet_to_fe_html.py"
    )
    fe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fe)
    emit(
        HERE / "public/data.json",
        fe.manifest_to_data_json({"rows": public_rows}, is_secure=True, title=TITLE),
    )
    emit(HERE / "public/viewer.html", (VENDOR / "annotation_viewer.html").read_bytes())
    questionnaire = questions()
    encoded = base64.b64encode(
        json.dumps(questionnaire, separators=(",", ":")).encode()
    ).decode()
    url = (
        BASE + PREFIX + "viewer.html?" + urlencode({"ldap": "hshariati", "q": encoded})
    )
    emit(HERE / "review_url.txt", (url + "\n").encode())
    emit(HERE / "questionnaire.json", questionnaire)
    emit(
        HERE / "manifest.json",
        {
            "title": TITLE,
            "seed": SEED,
            "selected": private,
            "eligible_count": eligible_count,
            "excluded_source_keys": sorted(excluded_keys),
            "annotation_listing": listing,
            "snapshots": snapshots,
            "strata": dict(Counter(row["source_row"][0] for row in private)),
            "method": "Hash-rank within product/camera; unique source-slot/prompt/pixels; independent display and partition ranks.",
            "partition_policy": "20 calibration/10 held-out source slots; all version variants inherit the slot partition.",
            "limits": [
                "Previously unused in recorded judge development, not proof nobody has viewed the public originals.",
                "Shared briefs, product families and cameras are not document-disjoint holdout.",
                "Blind to judge results, labels and partition; original asset URLs and confirmed title reveal generation provenance.",
                "No guarantee all rare registration/contour contrasts occur; only human review can establish them.",
                "No automatic overall FAIL follows from a minor appearance concern.",
                "Held-out labels must remain outside Astra design; all30 are not development examples.",
            ],
            "question_source": str(AUDIT),
            "question_source_sha256": digest(AUDIT.read_bytes()),
            "new_generation_calls": 0,
            "new_judge_calls": 0,
            "new_astra_calls": 0,
        },
    )
    frozen_paths = [
        HERE / "manifest.json",
        HERE / "questionnaire.json",
        HERE / "review_url.txt",
        HERE / "public/data.json",
        HERE / "public/viewer.html",
        Path(__file__),
        AUDIT,
        VENDOR / "annotation_viewer.html",
        VENDOR / "parquet_to_fe_html.py",
        *DEVELOPMENT,
    ]
    emit(
        HERE / "freeze.json",
        {
            "frozen_at_utc": datetime.now(UTC).isoformat(),
            "files": {str(path): digest(path.read_bytes()) for path in frozen_paths},
            "publication_prefix": PREFIX,
        },
    )
    verify()
    print(
        json.dumps(
            {
                "frozen": 30,
                "eligible": eligible_count,
                "partition": {"calibration": 20, "held_out": 10},
            }
        )
    )


def verify():
    freeze = load(HERE / "freeze.json")
    if freeze["publication_prefix"] != PREFIX:
        raise ValueError("Wrong publication prefix")
    for name, expected in freeze["files"].items():
        if digest(Path(name).read_bytes()) != expected:
            raise ValueError("Frozen review input changed: " + name)
    manifest = load(HERE / "manifest.json")
    data = load(HERE / "public/data.json")
    if len(data["rows"]) != 30 or len(manifest["selected"]) != 30:
        raise ValueError("Expected30 review rows")
    for item, row in zip(manifest["selected"], data["rows"], strict=True):
        if (
            row["meta_data"]["evalset_item_id"] != item["review_id"]
            or row["meta_data"]["key_val_informations"] is not None
            or len(row["images"]) != 1
            or row["images"][0]["asset_type"] != "image"
            or row["images"][0]["image_src"] != item["image_url"]
            or digest(Path(item["image_path"]).read_bytes()) != item["image_sha256"]
        ):
            raise ValueError("Blind row or actual image binding changed")
    return manifest


def publish():
    from botocore.exceptions import ClientError

    manifest = verify()
    validation = load(HERE / "browser_validation.json")
    if validation.get("passed") is not True or validation["freeze_sha256"] != digest(
        (HERE / "freeze.json").read_bytes()
    ):
        raise ValueError("A passing browser check for this exact freeze is required")
    s3 = client()
    for snapshot in manifest["snapshots"]:
        if digest(get(s3, snapshot["key"])[0]) != snapshot["sha256"]:
            raise ValueError("Live source/feedback changed before publication")
    for listing in manifest["annotation_listing"]:
        current = sorted(
            item["Key"]
            for page in s3.get_paginator("list_objects_v2").paginate(
                Bucket=BUCKET, Prefix=listing["prefix"]
            )
            for item in page.get("Contents", [])
            if item["Key"].endswith(".json")
        )
        if current != listing["keys"]:
            raise ValueError("New human annotations require a fresh exclusion review")
    written = []
    for name, content_type in (
        ("data.json", "application/json"),
        ("viewer.html", "text/html"),
    ):
        body = (HERE / "public" / name).read_bytes()
        try:
            s3.put_object(
                Bucket=BUCKET,
                Key=PREFIX + name,
                Body=body,
                ContentType=content_type,
                Metadata={"sha256": digest(body)},
                IfNoneMatch="*",
            )
        except ClientError as error:
            if error.response["ResponseMetadata"]["HTTPStatusCode"] != 412:
                raise
        actual, response = get(s3, PREFIX + name)
        if actual != body or response["ContentType"] != content_type:
            raise ValueError(
                "Published object differs; no existing object was overwritten"
            )
        written.append(
            {
                "key": PREFIX + name,
                "sha256": digest(body),
                "etag": response["ETag"],
                "bytes": len(body),
                "content_type": response["ContentType"],
            }
        )
    emit(
        HERE / "publication_receipt.json",
        {
            "verified": True,
            "objects": written,
            "freeze_sha256": digest((HERE / "freeze.json").read_bytes()),
            "shared_url": (HERE / "review_url.txt").read_text().strip(),
            "live_sso_and_annotation_writes_verified": False,
        },
    )
    print(
        "Published two byte/type-verified FE objects; original images referenced in place."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "verify", "publish"))
    args = parser.parse_args()
    {"prepare": prepare, "verify": verify, "publish": publish}[args.command]()
