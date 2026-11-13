#!/usr/bin/env bash
set -uo pipefail
umask 077
project=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment
package=/home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25
uv run --python 3.12 \
  --with 'foundry-aws-gateway[llm]>=2.0.0' \
  --with 'numpy==2.5.3' \
  --with 'Pillow==12.3.0' \
  --with 'openai==3.14.1' \
  --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple' \
  env PYTHONPATH="$project:$package" python "$project/run_v22_smoke.py" \
  >"$project/logs/v22_smoke.stdout.log" 2>"$project/logs/v22_smoke.stderr.log"
status=$?
printf '%s\n' "$status" >"$project/logs/v22_smoke.exit"
exit "$status"
