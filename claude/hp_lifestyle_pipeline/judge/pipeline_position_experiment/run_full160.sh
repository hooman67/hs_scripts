#!/usr/bin/env bash
set -euo pipefail
umask 077
project=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment
set +e
python "$project/run_full160.py" >"$project/logs/full160.stdout.log" 2>"$project/logs/full160.stderr.log"
code=$?
set -e
printf '%s\n' "$code" >"$project/logs/full160.exit"
exit "$code"
