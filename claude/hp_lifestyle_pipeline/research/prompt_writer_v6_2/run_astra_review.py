#!/usr/bin/env python3
"""Submit the durable V6.2/V4 review prompt to Direct OpenAI Astra."""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import foundry_aws_gateway.llm


PROMPT = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/"
    "research/prompt_writer_v6_2/astra_v6_2_and_judge_v4_task.md"
)
OUT = PROMPT.with_name("astra_v6_2_and_judge_v4_response.md")
META = PROMPT.with_name("astra_v6_2_and_judge_v4_run.log")


def main() -> None:
    started = dt.datetime.now(dt.timezone.utc)
    prompt = PROMPT.read_text(encoding="utf-8")
    client = foundry_aws_gateway.llm.get_openai().with_options(
        max_retries=8,
        timeout=600.0,
    )
    response = client.chat.completions.create(
        model="gpt-6-astra",
        messages=[{"role": "user", "content": prompt}],
        reasoning_effort="high",
        max_completion_tokens=16384,
    )
    choice = response.choices[0]
    content = choice.message.content or ""
    OUT.write_text(content + "\n", encoding="utf-8")
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
