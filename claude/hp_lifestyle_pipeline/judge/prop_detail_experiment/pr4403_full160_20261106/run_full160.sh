#!/usr/bin/env bash
set -euo pipefail
root=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/prop_detail_experiment/pr4403_full160_20261106
cd "$root"
exec uv run --python 3.12 --with boto3 python run_full160.py \
  >"$root/logs/runner.stdout.log" 2>"$root/logs/runner.stderr.log"
