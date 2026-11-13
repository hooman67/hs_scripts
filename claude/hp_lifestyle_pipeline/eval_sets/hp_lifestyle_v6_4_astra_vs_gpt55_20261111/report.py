"""Grouped GPT-5.5/Astra writer comparison, with actual scene inputs and failures."""

from __future__ import annotations

import hashlib
import json
import posixpath
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import audit_image
import image_study as study
import text_study

HERE = study.HERE
PUBLIC = HERE / "public"
BUCKET = study.BUCKET
PREFIX = study.PREFIX
GATEWAY = f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/"
VIEWER_URL = GATEWAY + PREFIX + "/gallery/index.html"
TITLE = "HP V6.4 prompt writers - GPT-5.5 vs Astra"


def relative(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != "foundry-aws-corp.adobe.io":
        raise ValueError("Expected a Foundry asset URL")
    prefix = "/asset/" + BUCKET + "/"
    if not parsed.path.startswith(prefix) or parsed.query or parsed.fragment:
        raise ValueError("Expected an HP asset without credentials/query parameters")
    return posixpath.relpath(parsed.path.removeprefix(prefix), PREFIX + "/gallery")


def copy_asset(source: Path, name: str, expected: str | None = None) -> str:
    data = source.read_bytes()
    if expected and hashlib.sha256(data).hexdigest() != expected:
        raise ValueError("Public asset source hash changed")
    text_study.write(PUBLIC / name, data)
    return relative(GATEWAY + PREFIX + "/" + name)


def details(output: dict[str, Any]) -> dict[str, Any]:
    return {
        "scene_prompt": output["scene_debug"]["finalPrompt"],
        "inputs": {role: relative(output["inputs"][role]) for role in ("product", "reference", "geometry_guide")},
        "lineage": output["lineage"],
        "image_settings": {
            "model": "gpt-image-2.5-sunburst-2026-09-08",
            "size": "2368x1776",
            "quality": "high",
            "image_calls": 1,
            "mask": None,
        },
    }


def card(prompt: dict[str, Any], output: dict[str, Any]) -> dict[str, Any]:
    return {
        "rank": prompt["bank_rank"],
        "prompt_key": prompt["prompt_key"],
        "prompt": prompt["text"],
        "environment": prompt["environment"],
        "status": output["status"],
        "image": relative(output["image"]) if output.get("image") else None,
        "image_sha256": output.get("image_sha256"),
        "error": output.get("error"),
        "details": details(output) if output["status"] == "done" else None,
        "source_relevance_score": prompt["source_relevance_score"],
        "ctech_reference_score": prompt["ctech_reference_score"],
        "prop_ids": prompt["prop_ids"],
        "primary_support": prompt["primary_support"],
    }


def build() -> None:
    study.verify()
    astra = text_study.load(study.SOURCE)
    baseline = text_study.load(HERE / "baseline/live/generation.json")
    before = {row["prompt"]["prompt_key"]: row for row in baseline["rows"]}
    after = {prompt["prompt_key"]: prompt for prompt in astra["prompts"]}
    twins = {
        (entry["digital_twin_id"], entry["camera_id"]): entry
        for entry in text_study.load(study.ENDPOINT / "input_bundle/manifest.json")["entries"]
    }
    output_by_key: dict[str, dict[str, Any]] = {}
    models = Counter()
    for prompt in astra["prompts"]:
        row = study.row_for(prompt)
        paths = study.image_runner().paths(study.RUN, row)
        record = text_study.load(paths["record"])
        if record["status"] != "done":
            output_by_key[prompt["prompt_key"]] = {"status": "image_failed", "error": record["error"]}
            continue
        audit = audit_image.audit_one(prompt, twins, False)
        models.update(audit["models"])
        image = copy_asset(paths["image"], "assets/outputs/" + row["row_slug"] + ".png", record["image_sha256"])
        inputs = {
            role: GATEWAY + PREFIX + "/" + "assets/inputs/" + audit[role]["sha256"] + "." + audit[role]["suffix"]
            for role in ("product", "reference", "geometry_guide")
        }
        for role in ("product", "reference", "geometry_guide"):
            path = PUBLIC / "assets/inputs" / (audit[role]["sha256"] + "." + audit[role]["suffix"])
            if not path.exists():
                copy_asset(Path(audit[role]["path"]), str(path.relative_to(PUBLIC)), audit[role]["sha256"])
        copy_asset(paths["record"], "data/records/" + paths["record"].name)
        output_by_key[prompt["prompt_key"]] = {
            "status": "done",
            "error": None,
            "image": GATEWAY + PREFIX + "/" + "assets/outputs/" + row["row_slug"] + ".png",
            "image_sha256": record["image_sha256"],
            "inputs": inputs,
            "scene_debug": record["scene_debug"],
            "lineage": record["lineage"],
        }
        if relative(output_by_key[prompt["prompt_key"]]["image"]) != image:
            raise ValueError("Image URL binding changed")
    groups: list[dict[str, Any]] = []
    for case in text_study.load(HERE / "banks.json")["cases"]:
        bank_id = case["bank_id"]
        result = astra["bank_audit"][bank_id]["result"]
        copy_asset(HERE / "text/results" / f"{bank_id}.json", "data/banks/" + bank_id + ".json")
        prior_cards, new_cards = [], []
        for rank in range(1, 11):
            key = bank_id + f"::p{rank}"
            prior_cards.append(card(before[key]["prompt"], before[key]["output"]))
            if key in after:
                new_cards.append(card(after[key], output_by_key[key]))
            else:
                new_cards.append(
                    {
                        "rank": rank,
                        "prompt_key": key,
                        "prompt": None,
                        "environment": None,
                        "status": "writer_failed",
                        "image": None,
                        "image_sha256": None,
                        "error": result["error"]["message"],
                        "details": None,
                    }
                )
        groups.append(
            {
                "id": bank_id,
                "device": before[bank_id + "::p1"]["prompt"]["device_display_name"],
                "device_id": case["device_id"],
                "camera": before[bank_id + "::p1"]["prompt"]["source_camera_name"],
                "camera_tag": case["camera_tag"],
                "contexts": [
                    {"label": "Identical V6.4 input for both writers", "input": text_study.load(HERE / case["input"])}
                ],
                "experiments": [
                    {"id": "gpt55", "label": "GPT-5.5 / medium / 16k - frozen baseline", "cards": prior_cards},
                    {
                        "id": "astra",
                        "label": "Astra / high / 32k - new best-effort writer",
                        "cards": new_cards,
                        "writer_status": result["status"],
                        "bank_result_url": "../data/banks/" + bank_id + ".json",
                        "terminal_error": result.get("error"),
                        "warnings": result.get("debug", {}).get("service", {}).get("validation_warnings", []),
                    },
                ],
            }
        )
    if len(groups) != 16 or any(len(group["experiments"]) != 2 for group in groups):
        raise ValueError("Comparison does not contain sixteen model-matched input banks")
    done = sum(
        card["image"] is not None
        for group in groups
        for experiment in group["experiments"]
        for card in experiment["cards"]
    )
    dataset = {
        "title": TITLE,
        "source_url": GATEWAY + text_study.BASELINE_KEY,
        "groups": groups,
        "group_count": 16,
        "experiment_count": 2,
        "planned_slots": 320,
        "image_count": done,
        "astra_text": text_study.load(HERE / "text/terminal.json"),
        "astra_images": text_study.load(HERE / "image_terminal.json"),
        "successful_native_models": dict(models),
    }
    text_study.write(PUBLIC / "gallery/data.json", dataset)
    copy_asset(study.SOURCE, "data/prompts_all_astra.json")
    copy_asset(HERE / "text/exports/prompts_all.txt", "data/prompts_all_astra.txt")
    copy_asset(HERE / "baseline/outputs/all_160/prompts_all_160.json", "data/prompts_all_gpt55.json")
    files = {
        str(path.relative_to(PUBLIC)): {"sha256": text_study.sha(path), "bytes": path.stat().st_size}
        for path in sorted(PUBLIC.rglob("*"))
        if path.is_file()
    }
    text_study.write(
        HERE / "build_manifest.json",
        {
            "assets": files,
            "images": done,
            "groups": 16,
            "study_manifest_sha256": text_study.sha(HERE / "study_manifest.json"),
        },
    )
    print(json.dumps({"built_groups": 16, "actual_images": done}), flush=True)


def verify_live(client: Any) -> None:
    for expected in text_study.load(HERE / "writer_snapshot_manifest.json")["baseline_live"].values():
        response = client.get_object(Bucket=BUCKET, Key=expected["key"])
        if (
            response["ETag"] != expected["etag"]
            or hashlib.sha256(response["Body"].read()).hexdigest() != expected["sha256"]
        ):
            raise ValueError("Live baseline changed; do not publish stale comparison bindings")


def publish() -> None:
    from botocore.exceptions import ClientError

    manifest = text_study.load(HERE / "build_manifest.json")
    proof = text_study.load(HERE / "browser_validation.json")
    if proof["status"] != "passed" or proof["build_manifest_sha256"] != text_study.sha(HERE / "build_manifest.json"):
        raise ValueError("Exact browser validation is required")
    client = text_study.s3_client()
    verify_live(client)
    types = {
        ".html": "text/html; charset=utf-8",
        ".js": "application/javascript",
        ".css": "text/css",
        ".json": "application/json",
        ".png": "image/png",
        ".webp": "image/webp",
        ".jpg": "image/jpeg",
        ".txt": "text/plain; charset=utf-8",
    }

    def upload(item: tuple[str, dict[str, Any]]) -> tuple[str, Any]:
        name, expected = item
        data = (PUBLIC / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != expected["sha256"]:
            raise ValueError("Verified public asset changed")
        key = PREFIX + "/" + name
        kind = types[Path(name).suffix]
        try:
            client.put_object(
                Bucket=BUCKET,
                Key=key,
                Body=data,
                ContentType=kind,
                Metadata={"sha256": expected["sha256"]},
                IfNoneMatch="*",
            )
        except ClientError as error:
            if error.response["Error"]["Code"] not in ("PreconditionFailed", "412"):
                raise
        response = client.get_object(Bucket=BUCKET, Key=key)
        if response["Body"].read() != data or response["ContentType"] != kind:
            raise ValueError("Published object bytes/type differ")
        return key, {"sha256": expected["sha256"], "etag": response["ETag"], "bytes": len(data)}

    with ThreadPoolExecutor(max_workers=8) as workers:
        objects = dict(workers.map(upload, manifest["assets"].items()))
    verify_live(client)
    text_study.write(HERE / "publication_receipt.json", {"objects": objects, "viewer_url": VIEWER_URL})
    text_study.write(HERE / "report_links.txt", (VIEWER_URL + "\n").encode())
    text_study.write(
        HERE / "completion_receipt.json",
        {
            "status": "complete" if manifest["images"] == 320 else "complete_with_errors",
            "viewer_url": VIEWER_URL,
            "images": manifest["images"],
            "publication_receipt_sha256": text_study.sha(HERE / "publication_receipt.json"),
        },
    )
    print(json.dumps({"published": VIEWER_URL, "objects": len(objects)}), flush=True)
