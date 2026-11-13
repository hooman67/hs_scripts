#!/usr/bin/env bash
set -uo pipefail
umask 077
run_root=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_1
run_name=development-15-v4-1-anchored-astra
log_path="$run_root/runs/$run_name.batch.log"
exit_path="$run_root/runs/$run_name.exit.txt"
started_path="$run_root/runs/$run_name.started.txt"
finished_path="$run_root/runs/$run_name.finished.txt"
mkdir -p "$run_root/runs"
date --iso-8601=seconds > "$started_path"
cd "$run_root"
uv run \
  --python 3.12 \
  --with jsonschema \
  --with openai \
  --with tomli \
  --with pyyaml \
  --with requests \
  --with 'foundry-aws-gateway[llm]>=2.0.0' \
  --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple' \
  run_batch.py \
  --manifest "$run_root/data/development_15_manifest.json" \
  --run-name "$run_name" \
  --workers 1 \
  --model gpt-6-astra \
  > "$log_path" 2>&1
status=$?
printf '%s\n' "$status" > "$exit_path"
date --iso-8601=seconds > "$finished_path"
exit "$status"
