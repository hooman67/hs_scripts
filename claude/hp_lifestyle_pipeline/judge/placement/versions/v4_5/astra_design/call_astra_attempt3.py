#!/usr/bin/env python3
"""Final bounded Astra V4.5 design request: six raw scenes only."""

from __future__ import annotations

import base64
import json
import mimetypes
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

import foundry_aws_gateway.llm


HERE = Path(__file__).resolve().parent
OUT = HERE / "attempt_3_six_raw_scenes"


def image_content(path: Path) -> dict:
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii"),
            "detail": "high",
        },
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    prompt = (OUT / "astra_task.md").read_text(encoding="utf-8")
    manifest = json.loads((OUT / "request_manifest.json").read_text())
    content: list[dict] = [{"type": "text", "text": prompt}]
    for asset in manifest["image_assets"]:
        content.append(
            {
                "type": "text",
                "text": f"RAW_SCENE for frozen visual case {asset['record_id']} — authoritative generated pixels.",
            }
        )
        content.append(image_content(Path(asset["transport_path"])))

    client = foundry_aws_gateway.llm.get_openai().with_options(max_retries=0, timeout=900.0)
    started_at = datetime.now(timezone.utc).isoformat()
    clock = perf_counter()
    response = client.chat.completions.create(
        model="gpt-6-astra",
        messages=[{"role": "user", "content": content}],
        reasoning_effort="high",
        max_completion_tokens=16000,
    )
    latency_ms = round((perf_counter() - clock) * 1000, 3)
    choice = response.choices[0]
    text = choice.message.content or ""
    (OUT / "astra_output.md").write_text(text, encoding="utf-8")
    usage = getattr(response, "usage", None)
    completion_details = getattr(usage, "completion_tokens_details", None)
    metadata = {
        "submission_attempt": 3,
        "request_started_at": started_at,
        "response_finished_at": datetime.now(timezone.utc).isoformat(),
        "latency_ms": latency_ms,
        "response_id": getattr(response, "id", None),
        "model": response.model,
        "finish_reason": choice.finish_reason,
        "prompt_tokens": getattr(usage, "prompt_tokens", None),
        "completion_tokens": getattr(usage, "completion_tokens", None),
        "reasoning_tokens": getattr(completion_details, "reasoning_tokens", None),
        "total_tokens": getattr(usage, "total_tokens", None),
        "content_bytes": len(text.encode()),
        "refusal": getattr(choice.message, "refusal", None),
        "image_count": len(manifest["image_assets"]),
        "task_sha256": manifest["task_sha256"],
        "sdk_max_retries": 0,
    }
    (OUT / "response_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    if not text or choice.finish_reason != "stop" or metadata["refusal"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
