#!/usr/bin/env bash
set -uo pipefail
umask 077
run_dir=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_2/astra_redesign
date --iso-8601=seconds > "$run_dir/started_at.txt"
uv run --python 3.12 --with 'foundry-aws-gateway[llm]>=2.0.0' --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple' "$run_dir/call_astra.py" > "$run_dir/astra_output.md" 2> "$run_dir/astra_stderr.log"
status=$?
printf '%s\n' "$status" > "$run_dir/exit_code.txt"
date --iso-8601=seconds > "$run_dir/finished_at.txt"
exit "$status"
