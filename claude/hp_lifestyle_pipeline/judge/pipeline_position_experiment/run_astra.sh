#!/usr/bin/env bash
set -uo pipefail
umask 077

experiment_dir=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment
prompt_path="$experiment_dir/astra/prompt.md"
output_path="$experiment_dir/astra/output.md"
stderr_path="$experiment_dir/logs/astra.stderr.log"
exit_path="$experiment_dir/logs/astra.exit"

rm -f "$exit_path"
uv run \
  --python 3.12 \
  --with 'foundry-aws-gateway[llm]>=2.0.0' \
  --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple' \
  python - "$prompt_path" >"$output_path" 2>"$stderr_path" <<'PY'
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
    reasoning_effort="medium",
    max_completion_tokens=24000,
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
printf '%s\n' "$status" >"$exit_path"
exit "$status"
