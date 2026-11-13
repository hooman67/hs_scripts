#!/usr/bin/env bash
set -euo pipefail
ROOT=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_5/root_probe
RUN="$ROOT/runs/dev6_once_gpt55"
mkdir -p "$RUN"
date -u +%FT%TZ > "$RUN/started_at.txt"
set +e
/home/colligo/.venvs/mixology/bin/python "$ROOT/run_probe.py" > "$RUN/stdout.log" 2> "$RUN/stderr.log"
code=$?
set -e
printf '%s\n' "$code" > "$RUN/exit_code.txt"
date -u +%FT%TZ > "$RUN/finished_at.txt"
exit "$code"
