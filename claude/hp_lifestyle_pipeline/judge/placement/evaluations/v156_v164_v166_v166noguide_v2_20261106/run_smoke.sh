#!/usr/bin/env bash
set -euo pipefail

ROOT=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
HERE="$ROOT/judge/placement/evaluations/v156_v164_v166_v166noguide_v2_20261106"
MANIFEST="$HERE/manifest.json"

cd "$ROOT"
mkdir -p "$HERE/logs"

(
  uv run --script judge/placement/versions/v2/run_batch.py \
    --manifest "$MANIFEST" \
    --run-name v156-v164-v166-v166noguide-v2-smoke-r2-v2 \
    --limit 1 --workers 1 --model gpt-5.5 --visual-anchors \
    >"$HERE/logs/smoke_r2_v2.stdout.log" 2>"$HERE/logs/smoke_r2_v2.stderr.log"
) &
v2_pid=$!

(
  uv run --script judge/placement/versions/v3/run_batch.py \
    --manifest "$MANIFEST" \
    --run-name v156-v164-v166-v166noguide-v2-smoke-r2-v3 \
    --limit 1 --workers 1 --model gpt-5.5 \
    >"$HERE/logs/smoke_r2_v3.stdout.log" 2>"$HERE/logs/smoke_r2_v3.stderr.log"
) &
v3_pid=$!

set +e
wait "$v2_pid"; v2_status=$?
wait "$v3_pid"; v3_status=$?
set -e

printf '%s\n' "$v2_status" >"$HERE/logs/smoke_r2_v2.exit.txt"
printf '%s\n' "$v3_status" >"$HERE/logs/smoke_r2_v3.exit.txt"
test "$v2_status" -eq 0
test "$v3_status" -eq 0
