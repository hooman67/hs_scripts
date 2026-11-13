#!/usr/bin/env bash
set -uo pipefail
umask 077

run_dir=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/astra/all_view_translation_compact_v2
prompt_path="$run_dir/request.md"

date -u +%Y-%m-%dT%H:%M:%SZ > "$run_dir/started_at_utc.txt"
uv run \
  --python 3.12 \
  --with 'foundry-aws-gateway[llm]>=2.0.0' \
  --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple' \
  python - "$prompt_path" > "$run_dir/response.md" 2> "$run_dir/stderr.log" <<'PY'
from pathlib import Path
import sys

import foundry_aws_gateway.llm

prompt = Path(sys.argv[1]).read_text(encoding="utf-8")
client = foundry_aws_gateway.llm.get_openai().with_options(
    max_retries=8,
    timeout=600.0,
)
response = client.chat.completions.create(
    model="gpt-6-astra",
    messages=[{"role": "user", "content": prompt}],
    reasoning_effort="high",
    max_completion_tokens=32768,
)
choice = response.choices[0]
print(choice.message.content or "")
print(
    f"[model={response.model} finish={choice.finish_reason} "
    f"total_tokens={getattr(response.usage, 'total_tokens', None)}]",
    file=sys.stderr,
)
PY
status=$?
printf '%s\n' "$status" > "$run_dir/exit_code.txt"
date -u +%Y-%m-%dT%H:%M:%SZ > "$run_dir/finished_at_utc.txt"
exit "$status"
