#!/usr/bin/env bash
set -euo pipefail
umask 077

root=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_1
mkdir -p "$root/logs"
set +e
PYTHONPATH="$root" python "$root/run_full160.py" \
  >"$root/logs/full160.stdout.log" 2>"$root/logs/full160.stderr.log"
code=$?
set -e
tmp="$root/logs/full160.exit.tmp.$$"
printf '%s\n' "$code" >"$tmp"
mv "$tmp" "$root/logs/full160.exit"
exit "$code"

