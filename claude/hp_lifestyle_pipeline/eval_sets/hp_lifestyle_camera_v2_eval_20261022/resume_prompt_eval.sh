#!/usr/bin/env bash
set -uo pipefail

EVAL_ROOT="/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_camera_v2_eval_20261022"
WATCH_PID="${1:-}"

cd "$EVAL_ROOT" || exit 1
if [[ -n "$WATCH_PID" ]]; then
  echo "watching foreground prompt PID $WATCH_PID"
  while kill -0 "$WATCH_PID" 2>/dev/null; do
    sleep 10
  done
fi

echo "starting resumable prompt pass"
while true; do
  PYTHONDONTWRITEBYTECODE=1 uv run --script run_prompt_eval.py \
    --concurrency 2 --max-attempts 100
  status=$?
  if [[ $status -eq 0 ]]; then
    echo "resumable prompt pass complete"
    exit 0
  fi
  echo "prompt pass exited $status; retrying preserved state in 30 seconds"
  sleep 30
done
