#!/usr/bin/env bash
set -uo pipefail
umask 077

run_dir=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4/astra
stdout_path="$run_dir/astra_output.md"
stderr_path="$run_dir/astra_stderr.log"
exit_path="$run_dir/astra_exit_code.txt"
started_path="$run_dir/astra_started_at.txt"
finished_path="$run_dir/astra_finished_at.txt"

date --iso-8601=seconds > "$started_path"
uv run \
  --python 3.12 \
  --with 'foundry-aws-gateway[llm]>=2.0.0' \
  --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple' \
  "$run_dir/call_astra.py" \
  > "$stdout_path" 2> "$stderr_path"
status=$?
printf '%s\n' "$status" > "$exit_path"
date --iso-8601=seconds > "$finished_path"
exit "$status"
