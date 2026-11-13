#!/usr/bin/env python3
"""Convert the frozen comparison using the official FE contract and viewer."""

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
from urllib.parse import urljoin

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
PUBLIC = STUDY / "public"
PREFIX = "eval_sets/" + STUDY.name
BUCKET = "foundry-hp-enterprise-adobe-assets"
BASE = "https://foundry-aws-corp.adobe.io/asset/" + BUCKET + "/" + PREFIX + "/"
SOURCE_URL = BASE + "gallery/index.html"
VIEWER_URL = BASE + "fe/viewer.html?ldap=hshariati"
TITLE = "HP V6.2 vs V6.3 prompts - PR4417 vs PR4523 (30 rank-paired cases)"
VENDOR = Path.home() / ".claude/scripts/fe_html"
SOURCE_FILES = ("gallery/index.html", "gallery/main.js", "data/comparison.json")
CELLS = (
    ("v6_2_pr4417", "V6.2 / PR4417 - V15.6"),
    ("v6_2_pr4523", "V6.2 / PR4523 - V15.7 shapes"),
    ("v6_3_pr4417", "V6.3 / PR4417 - V15.6"),
    ("v6_3_pr4523", "V6.3 / PR4523 - V15.7 shapes"),
)
COMMITS = {
    "pr4417": "1f66c0b68c5ecdc7bee8ace9fa247ee72e04e6dc",
    "pr4523": "d1e5ae5323dedebc3b06ed173a3731307bd0623a",
}
HISTORICAL_JUDGE = (
    "https://foundry-aws-corp.adobe.io/asset/" + BUCKET
    + "/hp-data-artifacts/hp-3p-gpt25/"
    "hp16-v6prompt-v156-vs-v164-vs-v166-vs-v166noguide-v2-e2e32-20261106T181903Z/viewer.html"
)


def digest(body):
    return hashlib.sha256(body).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n")


def load_vendor():
    sys.path.insert(0, str(VENDOR))
    import parquet_to_fe_html

    return parquet_to_fe_html


def media_url(value):
    if not isinstance(value, str) or not value:
        raise ValueError("missing source asset URL")
    absolute = urljoin(SOURCE_URL, value)
    if not absolute.startswith(BASE):
        raise ValueError("source media or record escapes the frozen study prefix")
    return absolute


def image(src, label, model_input=False, meta=None):
    return {
        "kind": "image", "src": media_url(src), "label": label,
        "model_input": model_input, "meta": meta or {},
    }


def text(content, label):
    if not isinstance(content, str) or not content:
        raise ValueError(f"missing original text: {label}")
    return {"kind": "text", "content": content, "label": label}


def convert(document):
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
        for name, label in CELLS:
            output = row["outputs"][name]
            if output["status"] != "done":
                raise ValueError(f"incomplete output: {key} {name}")
            if output["lineage"]["source_commit"] != COMMITS[name.rsplit("_", 1)[1]]:
                raise ValueError(f"wrong pinned pipeline: {key} {name}")
            assets.append(image(output["image"], label, meta={
                "Job": output["job_id"], "Image SHA256": output["image_sha256"],
                "Source commit": output["lineage"]["source_commit"],
                "Pipeline": output["lineage"]["pipelineVersion"],
                "Generation record": media_url(output["record_url"]),
                "Input audit": media_url(output["inputs"]["audit_url"]),
                "Judge": output["judgment"],
            }))
        historical = row["historical"]
        if historical["status"] != "done":
            raise ValueError("missing preserved historical reference")
        assets.append(image(
            historical["image"], "Historical V6.2: PR4349 + local V20 shape patch (NOT PR4523)",
            meta={"Generation record": media_url(historical["record_url"]),
                  "Image SHA256": historical["image_sha256"]},
        ))
        assets.append(image(row["twin"], "Frozen source digital twin", model_input=True))
        for name, label in CELLS:
            inputs = row["outputs"][name]["inputs"]
            for field, role in (
                ("geometry_guide", "actual sole image-generation input: geometry guide"),
                ("product", "actual planning/writing input: prepared product"),
                ("reference", "actual Astra planning/writing input: style reference"),
            ):
                assets.append(image(inputs[field], label + " - " + role, model_input=True))
        for writer in ("v6_2", "v6_3"):
            prompt = row["prompts"][writer]
            binding = (prompt["device_id"], prompt["camera_tag"], prompt["bank_rank"])
            if binding != key or digest(prompt["text"].encode()) != prompt["text_sha256"]:
                raise ValueError("source prompt text/hash/bank binding changed")
            assets.append(text(prompt["text"], writer.replace("_", ".").upper() + " user prompt"))
        for field in ("smart_brief", "source_messaging"):
            assets.append(text(row["source_input"][field], "Original " + field.replace("_", " ")))
        for name, label in CELLS:
            assets.append(text(row["outputs"][name]["scene_debug"]["finalPrompt"],
                               label + " - exact image-model prompt"))
        rows.append({
            "row_idx": index + 1,
            "evalset_item_id": " / ".join(map(str, key)),
            "meta": {
                "Device": row["device"], "Camera": row["camera"], "Bank rank": row["rank"],
                "V6.2 environment": row["prompts"]["v6_2"]["environment"],
                "V6.3 environment": row["prompts"]["v6_3"]["environment"],
                "Complete original row JSON": json.dumps(row, ensure_ascii=False),
            },
            "assets": assets,
        })
    manifest = {"rows": rows}
    data = load_vendor().manifest_to_data_json(manifest, is_secure=True, title=TITLE)
    for original, converted in zip(rows, data["rows"]):
        for asset, rendered in zip(original["assets"], converted["images"]):
            rendered["meta_text"].update(asset.get("meta", {}))
            if asset.get("model_input"):
                rendered["is_model_input_or_output"] = "model_input"
    data["meta_texts"].append(["Comparison scope", {
        "Matching": document["manifest"]["matching"],
        "Outputs": "Four exact writer/pipeline columns,120 new images; no judgments for these images.",
        "Historical reference": document["manifest"]["historical_lineage"],
        "Inputs": "Inputs toggles the frozen twin and actual model-input images; "
                  "all four comparison columns remain visible.",
        "Evidence limits": "Style references and stochastic outputs are not pair-controlled. "
                           "Remote inputs are API artifacts, not equivalent raw model-request hashes.",
        "Historical judges": "Separate32-row dataset; both V3.1 candidates remain unpromoted. "
                             "The original gallery now includes both candidates beneath stored V3 results.",
    }])
    downloads = (
        ("V6.3 all160 JSON", "prompts_all_v6_3_160.json"),
        ("V6.3 all160 TXT", "prompts_all_v6_3_160.txt"),
        ("V6.3 selected30 JSON", "selected_v6_3_30.json"),
        ("V6.3 selected30 TXT", "selected_v6_3_30.txt"),
        ("V6.2 matched30 JSON", "selected_v6_2_30.json"),
        ("V6.2 matched30 TXT", "selected_v6_2_30.txt"),
        ("Selection audit", "selection_report.json"),
        ("Immutable study lineage", "study_manifest.json"),
        ("Complete original comparison data", "comparison.json"),
    )
    data["links"] = [{"label": label, "url": BASE + "data/" + name}
                     for label, name in downloads] + [
        {"label": "Original comparison HTML", "url": SOURCE_URL},
        {"label": "Original historical gallery + V3 / V3.1 r1 / V3.1 r2", "url": HISTORICAL_JUDGE},
        {"label": "Original asset checksums", "url": BASE + "asset_manifest.json"},
    ]
    return manifest, data


def client_for(credentials_file):
    spec = importlib.util.spec_from_file_location("hp_comparison_report", STUDY / "report.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.s3_client(credentials_file)


def get_bytes(client, key):
    response = client.get_object(Bucket=BUCKET, Key=key)
    try:
        return response["Body"].read(), response
    finally:
        response["Body"].close()


def verify_live_source(client):
    sources = {}
    for name in SOURCE_FILES:
        body, metadata = get_bytes(client, PREFIX + "/" + name)
        if body != (PUBLIC / name).read_bytes():
            raise ValueError(f"live source changed; re-read and merge before conversion: {name}")
        sources[name] = {
            "sha256": digest(body), "bytes": len(body), "etag": metadata["ETag"],
            "version_id": metadata.get("VersionId"),
        }
    return sources


def build():
    sources = json.loads((HERE / "source_receipt.json").read_text())
    for name, identity in sources.items():
        if digest((PUBLIC / name).read_bytes()) != identity["sha256"]:
            raise ValueError("source changed after live verification")
    manifest, data = convert(json.loads((PUBLIC / "data/comparison.json").read_text()))
    write_json(HERE / "manifest.json", manifest)
    write_json(HERE / "report/data.json", data)
    shutil.copyfile(VENDOR / "annotation_viewer.html", HERE / "report/viewer.html")
    audit = {
        "title": TITLE, "source": sources, "rows": len(data["rows"]),
        "comparison_outputs": 120, "historical_references": 30, "input_images": 390,
        "viewer_url": VIEWER_URL,
        "files": {name: digest((HERE / "report" / name).read_bytes())
                  for name in ("data.json", "viewer.html")},
        "vendor_converter_sha256": digest((VENDOR / "parquet_to_fe_html.py").read_bytes()),
        "vendor_viewer_sha256": digest((VENDOR / "annotation_viewer.html").read_bytes()),
    }
    write_json(HERE / "build_audit.json", audit)
    print(json.dumps({key: value for key, value in audit.items() if key != "source"}))


def publish(client):
    from botocore.exceptions import ClientError

    audit = json.loads((HERE / "build_audit.json").read_text())
    browser = json.loads((HERE / "browser_validation.json").read_text())
    if browser["files"] != audit["files"] or browser["status"] != "passed":
        raise ValueError("browser validation must match the exact report files")
    if verify_live_source(client) != audit["source"]:
        raise ValueError("source version changed after conversion")
    objects = {}
    for name, expected in audit["files"].items():
        body = (HERE / "report" / name).read_bytes()
        if digest(body) != expected:
            raise ValueError("report changed after build/browser verification")
        key = PREFIX + "/fe/" + name
        content_type = "application/json" if name.endswith(".json") else "text/html; charset=utf-8"
        try:
            client.put_object(
                Bucket=BUCKET, Key=key, Body=body, ContentType=content_type,
                IfNoneMatch="*", CacheControl="no-cache", Metadata={"sha256": expected},
            )
        except ClientError as error:
            if error.response["Error"]["Code"] not in {"PreconditionFailed", "412"}:
                raise
        downloaded, metadata = get_bytes(client, key)
        if downloaded != body or metadata["ContentType"] != content_type:
            raise ValueError("existing or published FE object differs; refusing overwrite: " + key)
        objects[name] = {
            "key": key, "sha256": digest(downloaded), "bytes": len(downloaded),
            "content_type": metadata["ContentType"], "etag": metadata["ETag"],
            "version_id": metadata.get("VersionId"),
        }
    write_json(HERE / "publication_receipt.json", {
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "viewer_url": VIEWER_URL, "verification": "downloaded_sha256", "objects": objects,
    })
    print(VIEWER_URL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("source", "build", "publish"))
    parser.add_argument("--credentials-file", type=Path)
    args = parser.parse_args()
    if args.command == "build":
        build()
    else:
        if args.credentials_file is None:
            parser.error("--credentials-file is required")
        client = client_for(args.credentials_file)
        if args.command == "source":
            write_json(HERE / "source_receipt.json", verify_live_source(client))
            print("Live source bytes match the frozen comparison.")
        else:
            publish(client)
