#!/usr/bin/env python3
"""Submit the final text-only V4.5 Astra audit."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

import foundry_aws_gateway.llm


HERE = Path(__file__).resolve().parent
OUT = HERE / "attempt_4_text_only_review"


def main() -> None:
    prompt = (OUT / "astra_task.md").read_text(encoding="utf-8")
    manifest = json.loads((OUT / "request_manifest.json").read_text())
    client = foundry_aws_gateway.llm.get_openai().with_options(max_retries=2, timeout=600.0)
    started_at = datetime.now(timezone.utc).isoformat()
    clock = perf_counter()
    response = client.chat.completions.create(
        model="gpt-6-astra",
        messages=[{"role": "user", "content": prompt}],
        reasoning_effort="high",
        max_completion_tokens=12000,
    )
    choice = response.choices[0]
    text = choice.message.content or ""
    usage = getattr(response, "usage", None)
    details = getattr(usage, "completion_tokens_details", None)
    metadata = {
        "request_started_at": started_at,
        "response_finished_at": datetime.now(timezone.utc).isoformat(),
        "latency_ms": round((perf_counter() - clock) * 1000, 3),
        "response_id": getattr(response, "id", None),
        "model_requested": "gpt-6-astra",
        "model_returned": response.model,
        "finish_reason": choice.finish_reason,
        "prompt_tokens": getattr(usage, "prompt_tokens", None),
        "completion_tokens": getattr(usage, "completion_tokens", None),
        "reasoning_tokens": getattr(details, "reasoning_tokens", None),
        "total_tokens": getattr(usage, "total_tokens", None),
        "content_bytes": len(text.encode()),
        "refusal": getattr(choice.message, "refusal", None),
        "task_sha256": manifest["task_sha256"],
        "images_attached": 0,
    }
    (OUT / "astra_output.md").write_text(text, encoding="utf-8")
    (OUT / "response_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    if not text or choice.finish_reason != "stop" or metadata["refusal"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
