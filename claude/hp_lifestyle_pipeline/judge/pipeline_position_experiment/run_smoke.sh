#!/usr/bin/env bash
set -euo pipefail
umask 077

project=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment
worktree=/home/colligo/foundry-pr4349-position-exp
package="$worktree/experimental/adarabi/hp-3p-gpt25"
log_dir="$project/logs"
mkdir -p "$log_dir"

set +e
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$package" \
  uv run \
    --python 3.12 \
    --with 'foundry-aws-gateway[llm]>=2.0.0' \
    --with 'numpy==2.5.3' \
    --with 'Pillow==12.3.0' \
    --with 'openai==3.14.1' \
    --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple' \
    python "$project/run_smoke.py" \
    >"$log_dir/smoke.stdout.log" 2>"$log_dir/smoke.stderr.log"
code=$?
set -e
printf '%s\n' "$code" >"$log_dir/smoke.exit"
exit "$code"
