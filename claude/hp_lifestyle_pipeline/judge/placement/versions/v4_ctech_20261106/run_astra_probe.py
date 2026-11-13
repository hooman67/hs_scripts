#!/usr/bin/env python3
"""Run the evidence-first V4 observation contract on Astra for model ablation."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
from pathlib import Path

import foundry_aws_gateway.llm

from run_judge import WIRE_SCHEMA
from scoring import aggregate_observation


ROOT = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest = json.loads((ROOT / "evidence/calibration_manifest.json").read_text())
    record = next(item for item in manifest["records"] if item["id"] == args.record_id)
    content: list[dict] = [
        {
            "type": "text",
            "text": json.dumps(
                {
                    "product_type": record["device_type"],
                    "scene_prompt": record["scene_prompt"],
                    "image_stage": record["image_stage"],
                }
            ),
        }
    ]
    for label, key in (
        ("A — scene-generation image to evaluate", "generated_image"),
        ("B — original digital-twin render for identity/orientation reference", "twin_image"),
    ):
        path = Path(record[key]["local_path"])
        mime = mimetypes.guess_type(path.name)[0]
        content.extend(
            [
                {"type": "text", "text": label},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode(),
                        "detail": "high",
                    },
                },
            ]
        )

    client = foundry_aws_gateway.llm.get_openai().with_options(max_retries=8, timeout=600.0)
    response = client.chat.completions.create(
        model="gpt-6-astra",
        messages=[
            {"role": "system", "content": (ROOT / "system_prompt.md").read_text(encoding="utf-8")},
            {"role": "user", "content": content},
        ],
        reasoning_effort="high",
        max_completion_tokens=12000,
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "placement_observation", "strict": True, "schema": WIRE_SCHEMA},
        },
    )
    choice = response.choices[0]
    observation = json.loads(choice.message.content)
    payload = {
        "record_id": args.record_id,
        "model": response.model,
        "finish_reason": choice.finish_reason,
        "usage": response.model_dump(mode="json").get("usage"),
        "judgment": aggregate_observation(observation),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"record_id": args.record_id, "model": response.model, "verdict": payload["judgment"]["verdict"], "output": str(args.output)}))


if __name__ == "__main__":
    main()
