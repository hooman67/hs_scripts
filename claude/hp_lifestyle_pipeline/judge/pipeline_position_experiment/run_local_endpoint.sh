#!/usr/bin/env bash
set -euo pipefail
umask 077

project=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment
package=/home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25
exec env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$project:$package" \
  uv run --python 3.12 \
    --with 'foundry-aws-gateway[llm]>=2.0.0' \
    --with 'numpy==2.5.3' \
    --with 'Pillow==12.3.0' \
    --with 'openai==3.14.1' \
    --with 'fastapi>=0.115,<1' \
    --with 'uvicorn>=0.34,<1' \
    --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple' \
    uvicorn local_endpoint:app --host 127.0.0.1 --port 8126 \
    >"$project/logs/local_endpoint.stdout.log" 2>"$project/logs/local_endpoint.stderr.log"
