#!/usr/bin/env bash
set -euo pipefail
umask 077

root=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_3_3
package=/home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25
mkdir -p "$root/logs"
cd "$root"
exec env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$root:$package" \
  uv run --python 3.12 \
    --with 'foundry-aws-gateway[llm]>=2.0.0' \
    --with 'numpy==2.5.3' \
    --with 'opencv-python-headless==4.10.0.84' \
    --with 'Pillow==12.3.0' \
    --with 'openai==3.14.1' \
    --with 'fastapi>=0.115,<1' \
    --with 'uvicorn>=0.34,<1' \
    --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple' \
    uvicorn endpoint:app --host 127.0.0.1 --port 8127 \
    >"$root/logs/endpoint.stdout.log" 2>"$root/logs/endpoint.stderr.log"

