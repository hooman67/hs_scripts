#!/usr/bin/env bash
set -euo pipefail
ROOT=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_5/astra_design
OUT="$ROOT/attempt_3_six_raw_scenes"
umask 077
date --iso-8601=seconds > "$OUT/started_at.txt"
set +e
uv run --python 3.12 \
  --with 'foundry-aws-gateway[llm]>=2.0.0' \
  --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple' \
  python "$ROOT/call_astra_attempt3.py" > "$OUT/stdout.log" 2> "$OUT/stderr.log"
code=$?
set -e
printf '%s\n' "$code" > "$OUT/exit_code.txt"
date --iso-8601=seconds > "$OUT/finished_at.txt"
exit "$code"
