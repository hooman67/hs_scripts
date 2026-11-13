#!/usr/bin/env bash
set -euo pipefail

SHAPE_ROOT=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/local_scene_endpoint
SESSION_NAME=${1:-hp-v62-shape-endpoint}
PORT=${2:-8137}
GENERATION_ENABLED=${3:-0}

if [[ ! "$SESSION_NAME" =~ ^[a-zA-Z0-9._-]+$ ]]; then
  echo "invalid tmux session name" >&2
  exit 2
fi
if [[ ! "$PORT" =~ ^[0-9]+$ ]] || (( PORT < 1024 || PORT > 65535 )); then
  echo "invalid port" >&2
  exit 2
fi
if [[ "$GENERATION_ENABLED" != "0" && "$GENERATION_ENABLED" != "1" ]]; then
  echo "generation flag must be 0 or 1" >&2
  exit 2
fi
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  echo "tmux session already exists: $SESSION_NAME" >&2
  exit 1
fi
if ss -ltn | awk '{print $4}' | grep -Eq "(^|:)$PORT$"; then
  echo "port is already in use: $PORT" >&2
  exit 1
fi

COMMAND="cd '$SHAPE_ROOT' && exec env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 HP_SHAPE_HOST=127.0.0.1 HP_SHAPE_PORT='$PORT' HP_SHAPE_PUBLIC_BASE_URL='http://127.0.0.1:$PORT' HP_SHAPE_GENERATION_ENABLED='$GENERATION_ENABLED' HP_SHAPE_MAX_WORKERS=4 uv run --python 3.12 --with-requirements endpoint-requirements.txt --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple' python endpoint.py"
tmux new-session -d -s "$SESSION_NAME" "$COMMAND"

echo "session=$SESSION_NAME"
echo "base_url=http://127.0.0.1:$PORT"
echo "generation_enabled=$GENERATION_ENABLED"
