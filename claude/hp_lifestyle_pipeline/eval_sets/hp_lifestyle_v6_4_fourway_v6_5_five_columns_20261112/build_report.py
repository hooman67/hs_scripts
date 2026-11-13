"""Append existing training-grounded V6.5 outputs to the supplied four-way review."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import copy
import importlib.util
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
V65 = HERE.parent / "hp_lifestyle_v6_5_training_full160_pr4523_20261112"
SNAPSHOT = Path(
    "/home/colligo/.copilot/session-state/33fb7963-1994-4350-aa19-187148b03e14"
    "/files/hp_five_column_source_20261112"
)
spec = importlib.util.spec_from_file_location("completed_v65_study", V65 / "study.py")
if spec is None or spec.loader is None:
    raise RuntimeError("Completed V6.5 helper is unavailable")
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)
PUBLIC = HERE / "public"
PREFIX = "hp-data-artifacts/hp-3p-gpt25/hp160-v64-fourway-v65-five-column-20261112"
BASE = study.GATEWAY + PREFIX + "/"
TITLE = "HP lifestyle - V6.4 four-way + V6.5 (160 matched rows)"
LABEL = "V6.5 / PR 4523 - V15.7 shapes"


def emit(path, value):
    body = value if isinstance(value, bytes) else (
        json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    ).encode()
    path = Path(path)
    if path.exists():
        if path.read_bytes() != body:
            raise ValueError(f"Preserved artifact differs: {path}")
    else:
        study.write(path, body)


def verify_originals(client, originals):
    for name in ("viewer.html", "data.json"):
        expected = originals[name]
        response = client.get_object(Bucket=study.BUCKET, Key=expected["key"])
        if (
            response["Body"].read() != (HERE / "source" / name).read_bytes()
            or response["ETag"] != expected["etag"]
            or response.get("VersionId") != expected["version_id"]
            or response["ContentType"] != expected["content_type"]
            or response.get("Metadata", {}) != expected["metadata"]
        ):
            raise ValueError("Original report changed; inspect the current source before proceeding")


def prepare():
    if (HERE / "source_manifest.json").exists():
        manifest = verify()
        verify_originals(study.s3_client(), manifest["originals"])
        return
    expected = study.load(SNAPSHOT / "source_metadata.json")
    client = study.s3_client()
    for name in ("viewer.html", "data.json"):
        response = client.get_object(Bucket=study.BUCKET, Key=expected[name]["key"])
        body = response["Body"].read()
        if body != (SNAPSHOT / name).read_bytes() or response["ETag"] != expected[name]["etag"]:
            raise ValueError("Supplied report changed after inspection; re-read it before merging")
        emit(HERE / "source" / name, body)
    frozen = [HERE / "source" / name for name in ("viewer.html", "data.json")]
    frozen += [
        V65 / "completion_receipt.json", V65 / "public/data/generation.json",
        V65 / "extension/full/fe/data.json",
        V65 / "extension/full/data/comparison_v6_5_training_160_20261112.json",
    ]
    emit(HERE / "source_manifest.json", {
        "at_utc": study.now(), "title": TITLE, "originals": expected,
        "frozen_files": {str(path): study.sha(path) for path in frozen},
        "authorization": "New report; all160 existing outputs; preserve original four; show both source prompts",
        "new_generation_or_judging_authorized": False,
    })
    verify_originals(client, expected)


def verify():
    manifest = study.load(HERE / "source_manifest.json")
    for name, digest in manifest["frozen_files"].items():
        if study.sha(Path(name)) != digest:
            raise ValueError(f"Frozen source changed: {name}")
    return manifest


def merge(original, generation, official, baseline):
    new = {row["prompt"]["prompt_key"]: row for row in generation["rows"]}
    assets = {row["meta_data"]["evalset_item_id"]: row["images"][-1] for row in official["rows"]}
    previous = {row["prompt_v6_4"]["prompt_key"]: row["prompt_v6_4"] for row in baseline["rows"]}
    if len(original["rows"]) != 160 or len(new) != 160 or len(assets) != 160:
        raise ValueError("Expected complete, unique160-row source sets")
    result = copy.deepcopy(original)
    used = set()
    mapping = []
    labels = [asset["meta_text"]["label"] for asset in original["rows"][0]["images"][:4]]
    for row in result["rows"]:
        metadata = row["meta_data"]
        match = re.fullmatch(r"(.+)__p([1-9]|10)", metadata["evalset_item_id"])
        if match is None:
            raise ValueError("Unrecognized original row identifier")
        group, rank = match.groups()
        key = group + "::p" + rank
        if key in used or key not in new or key not in assets or key not in previous:
            raise ValueError("Missing or duplicated device/camera/rank binding")
        if (
            metadata["key_val_informations"]["Input group"] != group
            or metadata["key_val_informations"]["Prompt rank"] != int(rank)
            or [asset["asset_type"] for asset in row["images"]] != ["image"] * 4 + ["text"]
            or [asset["meta_text"]["label"] for asset in row["images"][:4]] != labels
            or row["images"][4]["text_content"] != previous[key]["text"]
        ):
            raise ValueError("Original column/source-prompt/rank binding differs")
        candidate = new[key]
        image = copy.deepcopy(assets[key])
        if (
            candidate["output"]["status"] != "done"
            or image["image_src"] != candidate["output"]["image"]
            or image["meta_text"]["label"] != LABEL
        ):
            raise ValueError("V6.5 asset differs from the completed native output")
        image["is_model_input_or_output"] = "model_output"
        prompt = {
            "asset_type": "text", "text_content": candidate["prompt"]["text"],
            "meta_text": {"label": "Original V6.5 user prompt"},
        }
        row["images"].insert(4, image)
        row["images"].append(prompt)
        used.add(key)
        mapping.append({
            "source_row_id": metadata["evalset_item_id"], "v65_prompt_key": key,
            "v65_image": image["image_src"], "v65_image_sha256": candidate["output"]["image_sha256"],
        })
    if used != set(new) or used != set(assets):
        raise ValueError("The report omits completed V6.5 slots")
    result["meta_texts"][0] = TITLE
    review = result["meta_texts"][1][1]
    review["Layout"] = "160 device/camera/rank-matched rows; five images in fixed column order."
    review["Images"] = "All800 existing images referenced in place. No generation or pixel changes."
    review["Prompts"] = "Original V6.4 and V6.5 user prompts per row; no rewritten prompts or debug."
    review["V6.5"] = "Training-grounded replacement on PR4523/V15.7; not the rejected predecessor."
    review["Matching"] = "Device/camera/prompt rank, not identical scenes or paired random seeds."
    return result, mapping, labels + [LABEL]


def once(text, before, after):
    if text.count(before) != 1:
        raise ValueError(f"Viewer customization anchor is not unique: {before[:90]}")
    return text.replace(before, after, 1)


def customize_viewer(html, labels):
    match = re.search(r"const METHOD_RATING_DEFS = (\[[^\n]*\])\.map\(text => \(\{", html)
    if match is None or json.loads(match[1]) != labels[:4]:
        raise ValueError("Original four method-rating definitions differ")
    html = once(html, match[0], match[0].replace(match[1], json.dumps(labels)))
    html = once(html, "<title>fe-html viewer</title>", f"<title>{TITLE}</title>")
    html = once(html, "grid-template-columns: repeat(2, auto);",
                "grid-template-columns: repeat(5, auto);")
    html = once(html, "repeat(4,minmax(0,1fr))", "repeat(5,minmax(0,1fr))")
    html = once(html, "repeat(4,240px)", "repeat(5,240px)")
    summary = re.search(r'<details id="columnChangeSummary".*?</details>', html, re.S)
    if summary is None:
        raise ValueError("Original designer brief is missing")
    addition = (
        "<section><h3>Column 5 - Training-grounded V6.5</h3><ul>"
        "<li>New source prompts informed by actual HP training photographs.</li>"
        "<li>Familiar everyday props and lived-in relationships; no people.</li>"
        "<li>Same PR4523/V15.7 image pipeline as Column 1, not the PR4619 interventions.</li>"
        "<li>Both original V6.4 and V6.5 source prompts appear below the images.</li>"
        "</ul></section>"
    )
    html = once(html, summary[0], once(summary[0], "</div></details>", addition + "</div></details>"))
    html = once(html, "'Mark both methods '", "'Mark all five methods '")
    html = once(html, "'v64-method-ratings.json'", "'v64-v65-five-method-ratings.json'")
    return html


def build():
    manifest = verify()
    data, mapping, labels = merge(
        study.load(HERE / "source/data.json"), study.load(V65 / "public/data/generation.json"),
        study.load(V65 / "extension/full/fe/data.json"),
        study.load(V65 / "extension/full/data/comparison_v6_5_training_160_20261112.json"),
    )
    emit(PUBLIC / "data.json", data)
    emit(PUBLIC / "viewer.html", customize_viewer(
        (HERE / "source/viewer.html").read_text(), labels).encode())
    emit(PUBLIC / "provenance.json", {
        "title": TITLE, "original_source": study.GATEWAY + manifest["originals"]["viewer.html"]["key"],
        "original_objects": manifest["originals"], "row_mapping": mapping,
        "original_four_images_and_row_metadata_preserved": True,
        "existing_images": 800, "new_model_calls": 0, "source_report_modified": False,
        "matching": "device/camera/rank; only identifier suffix formatting is normalized",
        "viewer": "Derived from supplied custom review; vendored files and original viewer untouched",
        "review_storage": "Independent new-report scope; original browser ratings are not overwritten",
    })
    emit(HERE / "publication_manifest.json", {
        "prefix": PREFIX, "url": BASE + "viewer.html?q=W10%3D&ldap=hshariati",
        "files": {p.name: {"path": str(p), "sha256": study.sha(p), "bytes": p.stat().st_size}
                  for p in sorted(PUBLIC.iterdir()) if p.is_file()},
        "source_manifest_sha256": study.sha(HERE / "source_manifest.json"),
        "builder_sha256": study.sha(Path(__file__)),
    })
    print(json.dumps({"rows": 160, "image_columns": 5, "images": 800, "source_prompts": 320}))


def check_images():
    verify()
    data = study.load(PUBLIC / "data.json")
    expected = {item["v65_image"]: item["v65_image_sha256"]
                for item in study.load(PUBLIC / "provenance.json")["row_mapping"]}
    urls = {a["image_src"] for row in data["rows"] for a in row["images"] if a["asset_type"] == "image"}
    client = study.s3_client()

    def head(url):
        response = client.head_object(Bucket=study.BUCKET, Key=study.key_for(url))
        if response["ContentLength"] <= 0 or not response["ContentType"].startswith("image/"):
            raise ValueError(f"Source image is unavailable or has the wrong content type: {url}")
        if url in expected and response.get("Metadata", {}).get("sha256") != expected[url]:
            raise ValueError("Published V6.5 image metadata differs from its audited raw PNG")
        return url, {"etag": response["ETag"], "version_id": response.get("VersionId"),
                     "bytes": response["ContentLength"], "content_type": response["ContentType"]}

    with ThreadPoolExecutor(max_workers=8) as pool:
        images = dict(pool.map(head, sorted(urls)))
    emit(HERE / "image_head_audit.json", {
        "at_utc": study.now(), "image_bindings": 800, "unique_urls": len(urls),
        "v65_hash_metadata_matches": len(expected), "images": images,
    })
    print(json.dumps({"image_urls_available": len(images), "v65_hash_bindings": len(expected)}))


def publish():
    from botocore.exceptions import ClientError

    frozen = verify()
    manifest = study.load(HERE / "publication_manifest.json")
    proof = study.load(HERE / "browser_validation.json")
    if (
        not proof["passed"] or proof["publication_manifest_sha256"] != study.sha(HERE / "publication_manifest.json")
        or manifest["builder_sha256"] != study.sha(Path(__file__))
    ):
        raise ValueError("Exact built-report browser proof is required")
    client = study.s3_client()
    verify_originals(client, frozen["originals"])
    objects = {}
    for name, item in manifest["files"].items():
        path = Path(item["path"])
        if study.sha(path) != item["sha256"]:
            raise ValueError("Browser-verified report changed")
        kind = "text/html; charset=utf-8" if name.endswith(".html") else "application/json"
        key = PREFIX + "/" + name
        try:
            client.put_object(Bucket=study.BUCKET, Key=key, Body=path.read_bytes(), ContentType=kind,
                              CacheControl="no-cache", Metadata={"sha256": item["sha256"]}, IfNoneMatch="*")
        except ClientError as error:
            if error.response["Error"]["Code"] not in ("PreconditionFailed", "412"):
                raise
        response = client.get_object(Bucket=study.BUCKET, Key=key)
        if response["Body"].read() != path.read_bytes() or response["ContentType"] != kind:
            raise ValueError("Published report bytes/content type differ")
        objects[key] = {**item, "content_type": kind, "etag": response["ETag"],
                        "version_id": response.get("VersionId")}
    verify_originals(client, frozen["originals"])
    emit(HERE / "publication_receipt.json", {
        "at_utc": study.now(), "url": manifest["url"], "objects": objects,
        "original_viewer_data_metadata_and_versions_unchanged": True, "new_model_calls": 0,
        "verified_by_complete_download": True, "live_ims_and_annotation_writes_certified": False,
        "publication_manifest_sha256": study.sha(HERE / "publication_manifest.json"),
    })
    emit(HERE / "report_links.txt", (manifest["url"] + "\n").encode())
    print(manifest["url"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "build", "check_images", "publish"))
    globals()[parser.parse_args().command]()
