#!/usr/bin/env bash
set -euo pipefail
umask 077

root=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/pilot_v23_all_view_translation
mkdir -p "$root/logs"
cd "$root"
set +e
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$root" \
  python "$root/run_pilot.py" \
  >"$root/logs/pilot.stdout.log" 2>"$root/logs/pilot.stderr.log"
status=$?
set -e
printf '%s\n' "$status" >"$root/logs/pilot.exit_code"
exit "$status"
