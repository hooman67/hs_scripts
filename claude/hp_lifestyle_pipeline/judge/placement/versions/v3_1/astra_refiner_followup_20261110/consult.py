"""Bounded Astra image consultation; retrieval and artifact work remain local."""

import argparse
import base64
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import time

import foundry_aws_gateway.llm

from prepare import ROOT, R1, sha, write_json

CONTRACTS = [
    R1 / "prompts/baseline.md", R1 / "prompts/compact.md",
    R1 / "prompts/proposal.md", R1 / "prompts/independent.md",
    R1 / "observation_schema.json", R1 / "r2/prompts/compact.md",
    R1.parent / "v3/experiments/consensus_policy/policy.json",
]


def prepare_batches():
    manifest = json.loads((ROOT / "evidence_manifest.json").read_text())
    contracts = []
    for path in CONTRACTS:
        contracts.append({"path": str(path), "sha256": sha(path), "text": path.read_text()})
    for index in range(4):
        cases = manifest["cases"][index * 16:(index + 1) * 16]
        case_inputs = []
        media = {}

        def register(image, path_field="review_path", hash_field="review_sha256"):
            path = Path(image[path_field])
            expected = image[hash_field]
            if sha(path) != expected:
                raise ValueError("review/source image changed")
            media_id = "image_" + expected[:16]
            media[media_id] = {
                "id": media_id, "path": str(path), "sha256": expected,
                "bytes": path.stat().st_size,
                "transform": image.get("transformation", "none; exact original source JPEG"),
            }
            return media_id

        for case in cases:
            case_inputs.append({
                "case_id": case["id"], "human_feedback": case["reviewer_feedback"],
                "images": {role: register(item) for role, item in case["images"].items()},
                "refiner_execution_status_not_quality": case["status"],
                "refiner_scope_not_judge_policy": case["refiner_scope_text"],
                "refiner_plan_not_visual_truth": case["result"]["plan"],
                "prior_qualitative_review_not_gold": manifest["review_notes"]["notes"].get(case["id"]),
            })
        anchors = []
        if index == 0:
            for case in manifest["historical_annotated_examples_and_controls"]:
                anchors.append({
                    "case_id": case["id"], "role": case["role"],
                    "criterion_expectation": case["expectation"],
                    "scene_prompt": case["scene_prompt"],
                    "images": {role: register(case[role], "local_path", "sha256")
                               for role in ("generated_image", "twin_image")},
                })
        content = {
            "batch_id": index + 1, "source_html_sha256": manifest["source"]["sha256"],
            "case_inputs": case_inputs, "historical_examples": anchors,
            "frozen_contracts": contracts, "image_inventory": list(media.values()),
        }
        directory = ROOT / "batches" / f"batch{index + 1}"
        write_json(directory / "input.json", content)
        estimated_bytes = sum(item["bytes"] * 4 // 3 + 4 for item in media.values())
        if estimated_bytes > 45_000_000:
            raise ValueError("batch payload exceeds the preselected45MB image budget")
        print(json.dumps({"batch": index + 1, "cases": len(cases), "images": len(media),
                          "estimated_base64_image_bytes": estimated_bytes}))


def run(batch_number):
    directory = ROOT / "batches" / f"batch{batch_number}"
    if (directory / "config.json").exists():
        raise ValueError("batch already attempted; inspect preserved evidence, do not resample")
    package = json.loads((directory / "input.json").read_text())
    prompt = (ROOT / "brief.txt").read_text()
    content = [{"type": "text", "text": json.dumps(package, ensure_ascii=False)}]
    for media in package["image_inventory"]:
        path = Path(media["path"])
        if sha(path) != media["sha256"]:
            raise ValueError("frozen package media changed")
        content.extend([
            {"type": "text", "text": "ACTUAL IMAGE " + media["id"] + "; " + media["transform"]},
            {"type": "image_url", "image_url": {
                "url": "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode(),
                "detail": "high",
            }},
        ])
    config = {
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "route": "foundry_aws_gateway.llm.get_openai", "model": "gpt-6-astra",
        "reasoning_effort": "high", "max_completion_tokens": 24000,
        "timeout_seconds": 600, "transport_max_retries": 8, "concurrency": 1,
        "semantic_resampling": False, "input_sha256": sha(directory / "input.json"),
        "brief_sha256": sha(ROOT / "brief.txt"), "case_ids": [
            row["case_id"] for row in package["case_inputs"]],
        "images": package["image_inventory"],
        "sdk_versions": {name: version(name) for name in ("openai", "foundry-aws-gateway")},
    }
    write_json(directory / "config.json", config)
    started = time.monotonic()
    try:
        response = foundry_aws_gateway.llm.get_openai().with_options(
            max_retries=8, timeout=600,
        ).chat.completions.create(
            model="gpt-6-astra", reasoning_effort="high", max_completion_tokens=24000,
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": content}],
        )
        (directory / "response.json").write_text(response.model_dump_json(indent=2) + "\n")
        choice = response.choices[0]
        body = choice.message.content or ""
        (directory / "output.txt").write_text(body)
        receipt = {
            "completed_at_utc": datetime.now(timezone.utc).isoformat(),
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "model_returned": response.model, "finish_reason": choice.finish_reason,
            "usage": response.usage.model_dump() if response.usage else None,
            "response_sha256": sha(directory / "response.json"),
        }
        write_json(directory / "receipt.json", receipt)
        if response.model != "gpt-6-astra" or choice.finish_reason != "stop" or not body:
            raise ValueError("incomplete or unexpected-model Astra response")
        result = json.loads(body)
        expected = set(config["case_ids"])
        actual = [row["case_id"] for row in result["case_reviews"]]
        if len(actual) != 16 or set(actual) != expected or result["batch_id"] != batch_number:
            raise ValueError("Astra omitted, duplicated or rebound case reviews")
        anchor_ids = [row["case_id"] for row in result["anchor_reviews"]]
        if set(anchor_ids) != {row["case_id"] for row in package["historical_examples"]}:
            raise ValueError("Astra historical-example coverage differs")
        write_json(directory / "analysis.json", result)
        print(json.dumps({"batch": batch_number, "status": "complete", **receipt}), flush=True)
    except Exception as error:
        write_json(directory / "error.json", {
            "error_type": type(error).__name__, "http_status": getattr(error, "status_code", None),
            "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        })
        raise SystemExit(type(error).__name__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "run"))
    parser.add_argument("--batch", type=int, choices=range(1, 5))
    args = parser.parse_args()
    if args.command == "prepare":
        prepare_batches()
    elif args.batch is None:
        parser.error("--batch is required for run")
    else:
        run(args.batch)
