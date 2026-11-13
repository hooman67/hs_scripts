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
EVIDENCE = HERE / "evidence" / "compact_feedback_context.json"
IMAGE_MANIFEST = HERE / "evidence" / "contact_sheet_manifest.json"
SOURCE_MANIFEST = HERE / "evidence" / "source_manifest.json"
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
    source_manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    if evidence.get("record_count") != 15:
        raise RuntimeError("Expected exactly 15 joined feedback records")

    content: list[dict] = [
        {
            "type": "text",
            "text": task + "\n\n```json\n" + evidence_text + "```\n",
        }
    ]
    if image_manifest.get("pair_count") != 15 or image_manifest.get("sheet_count") > 5:
        raise RuntimeError("Expected 15 pairs represented in at most five contact sheets")
    if image_manifest.get("all_pairs_covered_once") is not True:
        raise RuntimeError("Contact-sheet coverage is not exact")
    image_sequence = []
    for index, sheet in enumerate(image_manifest["sheets"], start=1):
        sheet_bytes = Path(sheet["path"]).read_bytes()
        sheet_data_url = "data:image/jpeg;base64," + base64.b64encode(sheet_bytes).decode("ascii")
        content.extend(
            [
                {
                    "type": "text",
                    "text": f"CONTACT SHEET {index}: five labeled rows; generated scene left, original twin right. Record IDs: {', '.join(sheet['record_ids'])}",
                },
                {"type": "image_url", "image_url": {"url": sheet_data_url, "detail": "high"}},
            ]
        )
        image_sequence.append(
            {
                "contact_sheet_index": index,
                "record_ids": sheet["record_ids"],
                "sha256": sheet["sha256"],
                "bytes": sheet["bytes"],
                "width": sheet["width"],
                "height": sheet["height"],
            }
        )

    request_manifest = {
        "schema_version": "hp-placement-astra-request-manifest-v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "route": "foundry_aws_gateway.llm.get_openai direct OpenAI",
        "model_requested": "gpt-6-astra",
        "reasoning_effort": "medium",
        "max_completion_tokens": 24000,
        "max_retries": 2,
        "timeout_seconds": 600.0,
        "concurrency": 1,
        "task_path": str(TASK),
        "task_sha256": sha256(TASK),
        "evidence_path": str(EVIDENCE),
        "evidence_sha256": sha256(EVIDENCE),
        "image_payload_manifest_path": str(IMAGE_MANIFEST),
        "image_payload_manifest_sha256": sha256(IMAGE_MANIFEST),
        "image_transport": "base64 data URLs of three labeled JPEG contact sheets",
        "image_pair_count": image_manifest["pair_count"],
        "contact_sheet_count": image_manifest["sheet_count"],
        "contact_sheet_total_bytes": image_manifest["total_bytes"],
        "annotation_sha256": source_manifest["annotation"]["sha256"],
        "contact_sheets": image_sequence,
        "credentials_recorded": False,
    }
    atomic_json(MANIFEST, request_manifest)

    client = foundry_aws_gateway.llm.get_openai().with_options(
        max_retries=2,
        timeout=600.0,
    )
    response = client.chat.completions.create(
        model="gpt-6-astra",
        messages=[{"role": "user", "content": content}],
        reasoning_effort="medium",
        max_completion_tokens=24000,
    )
    choice = response.choices[0]
    answer = choice.message.content or ""
    print(answer)
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
    if not answer.strip():
        raise RuntimeError(f"Astra returned no visible answer; finish_reason={choice.finish_reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
