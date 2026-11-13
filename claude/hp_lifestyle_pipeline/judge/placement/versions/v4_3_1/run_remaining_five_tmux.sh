#!/usr/bin/env bash
set -euo pipefail
ROOT=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_3_1
RUN="$ROOT/runs/remaining-five-v1-gpt55"
mkdir -p "$RUN"
date --iso-8601=seconds > "$RUN/started.txt"
umask 077
set +e
uv run \
  --python 3.12 \
  --with 'foundry-aws-gateway[llm]>=2.0.0' \
  --with 'jsonschema==4.25.1' \
  --with 'pillow==12.0.0' \
  --with 'opencv-python-headless==4.10.0.84' \
  --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple' \
  python "$ROOT/run_remaining_five.py" \
    --manifest "$ROOT/data/gate_6_manifest.json" \
    --output-dir "$RUN" \
    --model gpt-5.5 > "$RUN/batch.log" 2>&1
code=$?
set -e
printf '%s\n' "$code" > "$RUN/exit.txt"
date --iso-8601=seconds > "$RUN/finished.txt"
exit "$code"
