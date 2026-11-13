#!/usr/bin/env python3
"""Submit the frozen V4.5 design task and case images through Direct OpenAI."""

from __future__ import annotations

import base64
import json
import mimetypes
from pathlib import Path

import foundry_aws_gateway.llm


HERE = Path(__file__).resolve().parent


def image_content(path: Path, detail: str) -> dict:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii"),
            "detail": detail,
        },
    }


def main() -> None:
    prompt = (HERE / "astra_task.md").read_text(encoding="utf-8")
    manifest = json.loads((HERE / "request_manifest.json").read_text())
    content: list[dict] = [{"type": "text", "text": prompt}]
    current = None
    for asset in manifest["image_assets"]:
        if asset["record_id"] != current:
            current = asset["record_id"]
            content.append(
                {
                    "type": "text",
                    "text": f"VISUAL CASE {current}. The human label is in the frozen evidence; inspect these pixels yourself.",
                }
            )
        role = asset["role"]
        content.append(
            {
                "type": "text",
                "text": {
                    "raw_scene": "RAW_SCENE — authoritative complete generated image",
                    "original_twin": "ORIGINAL_TWIN — identity and functional-front reference only",
                    "product_support_crop": "PRODUCT_SUPPORT_CROP — deterministic unwarped aid; raw scene controls",
                    "geometry_overlay": "GEOMETRY_OVERLAY — algorithmic edge aid; may contain false/missing lines; raw scene controls",
                }[role],
            }
        )
        detail = "high" if role in {"raw_scene", "product_support_crop", "geometry_overlay"} else "auto"
        content.append(image_content(Path(asset["transport_path"]), detail))

    client = foundry_aws_gateway.llm.get_openai().with_options(max_retries=8, timeout=600.0)
    response = client.chat.completions.create(
        model="gpt-6-astra",
        messages=[{"role": "user", "content": content}],
        reasoning_effort="high",
        max_completion_tokens=24000,
    )
    choice = response.choices[0]
    text = choice.message.content or ""
    (HERE / "astra_output.md").write_text(text, encoding="utf-8")
    usage = getattr(response, "usage", None)
    completion_details = getattr(usage, "completion_tokens_details", None)
    metadata = {
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
    }
    (HERE / "response_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    if not text or choice.finish_reason != "stop" or metadata["refusal"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
