#!/usr/bin/env bash
set -euo pipefail
umask 077
project=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment
package=/home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25
version="$project/versions/v22_4"
exec env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$project:$package" \
  uv run --python 3.12 \
    --with 'foundry-aws-gateway[llm]>=2.0.0' \
    --with 'numpy==2.5.3' \
    --with 'opencv-python-headless==4.10.0.84' \
    --with 'Pillow==12.3.0' \
    --with 'openai==3.14.1' \
    --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple' \
    python "$version/run_v22_4_1_guard_smoke.py"
