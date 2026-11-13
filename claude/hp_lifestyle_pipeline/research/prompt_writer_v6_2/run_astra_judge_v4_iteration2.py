#!/usr/bin/env python3
"""Submit the durable V4 calibration redesign task to Direct OpenAI Astra."""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import foundry_aws_gateway.llm


ROOT = Path(__file__).resolve().parent
PROMPT = ROOT / "astra_judge_v4_iteration2_task.md"
OUT = ROOT / "astra_judge_v4_iteration2_response.md"
META = ROOT / "astra_judge_v4_iteration2_run.log"


def main() -> None:
    started = dt.datetime.now(dt.timezone.utc)
    client = foundry_aws_gateway.llm.get_openai().with_options(
        max_retries=8,
        timeout=600.0,
    )
    response = client.chat.completions.create(
        model="gpt-6-astra",
        messages=[{"role": "user", "content": PROMPT.read_text(encoding="utf-8")}],
        reasoning_effort="high",
        max_completion_tokens=12288,
    )
    choice = response.choices[0]
    OUT.write_text((choice.message.content or "") + "\n", encoding="utf-8")
    finished = dt.datetime.now(dt.timezone.utc)
    META.write_text(
        "\n".join(
            [
                f"started_utc={started.isoformat()}",
                f"finished_utc={finished.isoformat()}",
                f"model={response.model}",
                f"finish_reason={choice.finish_reason}",
                f"total_tokens={getattr(response.usage, 'total_tokens', None)}",
                f"response_path={OUT}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        raise
