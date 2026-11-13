#!/usr/bin/env python3
"""Call Direct OpenAI Astra with exact comment evidence and associated images."""

from __future__ import annotations

import hashlib
import json
import base64
import sys
from datetime import datetime, timezone
from pathlib import Path

import foundry_aws_gateway.llm


HERE = Path(__file__).resolve().parent
TASK = HERE / "astra_task.md"
EVIDENCE = HERE / "evidence" / "joined_feedback_context.json"
IMAGE_MANIFEST = HERE / "evidence" / "image_payload_manifest.json"
MANIFEST = HERE / "request_manifest.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_json(path: Path, value) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    task = TASK.read_text(encoding="utf-8")
    evidence_text = EVIDENCE.read_text(encoding="utf-8")
    evidence = json.loads(evidence_text)
    image_manifest = json.loads(IMAGE_MANIFEST.read_text(encoding="utf-8"))
    if evidence.get("comment_count") != 15:
        raise RuntimeError("Expected exactly 15 joined feedback records")

    content: list[dict] = [
        {
            "type": "text",
            "text": task + "\n\n```json\n" + evidence_text + "```\n",
        }
    ]
    if image_manifest.get("pair_count") != 15:
        raise RuntimeError("Expected exactly 15 prepared image pairs")
    pairs = {pair["record_id"]: pair for pair in image_manifest["pairs"]}
    image_sequence = []
    for record in evidence["records"]:
        record_id = record["record_id"]
        pair = pairs[record_id]
        generated_bytes = Path(pair["generated_scene"]["derivative_path"]).read_bytes()
        twin_bytes = Path(pair["digital_twin"]["derivative_path"]).read_bytes()
        generated_data_url = "data:image/jpeg;base64," + base64.b64encode(generated_bytes).decode("ascii")
        twin_data_url = "data:image/jpeg;base64," + base64.b64encode(twin_bytes).decode("ascii")
        content.extend(
            [
                {
                    "type": "text",
                    "text": f"IMAGE PAIR FOR {record_id}: generated scene first, original digital twin second.",
                },
                {"type": "image_url", "image_url": {"url": generated_data_url, "detail": "high"}},
                {"type": "image_url", "image_url": {"url": twin_data_url, "detail": "high"}},
            ]
        )
        image_sequence.append(
            {
                "record_id": record_id,
                "generated_image_url": record["input"]["generated_image_url"],
                "generated_image_sha256": record["input"]["generated_image_sha256"],
                "generated_derivative_sha256": pair["generated_scene"]["derivative_sha256"],
                "generated_derivative_bytes": pair["generated_scene"]["derivative_bytes"],
                "twin_image_url": record["input"]["twin_image_url"],
                "twin_image_sha256": record["input"]["twin_image_sha256"],
                "twin_derivative_sha256": pair["digital_twin"]["derivative_sha256"],
                "twin_derivative_bytes": pair["digital_twin"]["derivative_bytes"],
            }
        )

    request_manifest = {
        "schema_version": "hp-placement-astra-request-manifest-v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "route": "foundry_aws_gateway.llm.get_openai direct OpenAI",
        "model_requested": "gpt-6-astra",
        "reasoning_effort": "high",
        "max_completion_tokens": 16384,
        "max_retries": 8,
        "timeout_seconds": 600.0,
        "concurrency": 1,
        "task_path": str(TASK),
        "task_sha256": sha256(TASK),
        "evidence_path": str(EVIDENCE),
        "evidence_sha256": sha256(EVIDENCE),
        "image_payload_manifest_path": str(IMAGE_MANIFEST),
        "image_payload_manifest_sha256": sha256(IMAGE_MANIFEST),
        "image_transport": "base64 data URLs of bounded JPEG derivatives",
        "image_pair_count": image_manifest["pair_count"],
        "image_unique_count": image_manifest["unique_image_count"],
        "image_derivative_bytes_in_sequence": image_manifest["derivative_bytes_in_sequence"],
        "image_unique_derivative_bytes": image_manifest["unique_derivative_bytes"],
        "annotation_sha256": evidence["annotation_source"]["sha256"],
        "image_pairs": image_sequence,
        "credentials_recorded": False,
    }
    atomic_json(MANIFEST, request_manifest)

    client = foundry_aws_gateway.llm.get_openai().with_options(
        max_retries=8,
        timeout=600.0,
    )
    response = client.chat.completions.create(
        model="gpt-6-astra",
        messages=[{"role": "user", "content": content}],
        reasoning_effort="high",
        max_completion_tokens=16384,
    )
    choice = response.choices[0]
    print(choice.message.content or "")
    print(
        json.dumps(
            {
                "model": response.model,
                "finish_reason": choice.finish_reason,
                "total_tokens": getattr(response.usage, "total_tokens", None),
            }
        ),
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
