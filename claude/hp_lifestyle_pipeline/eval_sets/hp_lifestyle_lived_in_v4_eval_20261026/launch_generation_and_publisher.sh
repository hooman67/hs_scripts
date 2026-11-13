#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
EVAL_ROOT=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026
RUN_ROOT=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_lived_in_v4_eval_20261026
RUNNER="$EVAL_ROOT/generation/run_generation.py"
GENERATION_SUPERVISOR="$EVAL_ROOT/generation/supervise_generation.py"
PUBLISHER="$EVAL_ROOT/publication/supervise_publication.py"
VALIDATOR="$EVAL_ROOT/validate_gallery.py"
AWS_ENV=/home/colligo/.claude/hshariati/aws_creds.env
GEN_SESSION=hp_v4_generation_20261026
PUB_SESSION=hp_v4_publisher_20261026
GEN_LOG="$RUN_ROOT/launch/generation.log"
PUB_LOG="$EVAL_ROOT/publication/publisher.log"
SELF=$(readlink -f "$0")

generation_running() {
  pgrep -f "$GENERATION_SUPERVISOR.*--run-dir" >/dev/null 2>&1 || \
    pgrep -f "$RUNNER.*--all" >/dev/null 2>&1
}

publisher_running() {
  pgrep -f "$PUBLISHER.*--poll-seconds" >/dev/null 2>&1
}

local_preflight() {
  cd "$PROJECT_ROOT"
  uv run --script "$VALIDATOR"
  uv run --script "$RUNNER" --run-dir "$RUN_ROOT" --validate-only
}

run_generation() {
  umask 077
  mkdir -p "$RUN_ROOT/launch"
  cd "$PROJECT_ROOT"
  exec env \
    -u OPENAI_API_KEY -u AZURE_OPENAI_API_KEY -u AZURE_OPENAI_ENDPOINT \
    -u AWS_ACCESS_KEY_ID -u AWS_SECRET_ACCESS_KEY -u AWS_SESSION_TOKEN \
    uv run --script "$GENERATION_SUPERVISOR" \
      --run-dir "$RUN_ROOT" \
      --poll-window-seconds 1800 \
      --max-invocations 12 >> "$GEN_LOG" 2>&1
}

run_publisher() {
  umask 077
  mkdir -p "$EVAL_ROOT/publication"
  cd "$PROJECT_ROOT"
  exec env \
    -u OPENAI_API_KEY -u AZURE_OPENAI_API_KEY -u AZURE_OPENAI_ENDPOINT \
    -u AWS_ACCESS_KEY_ID -u AWS_SECRET_ACCESS_KEY -u AWS_SESSION_TOKEN \
    -u AWS_DEFAULT_REGION -u AWS_REGION \
    python3 "$PUBLISHER" --poll-seconds 120 >> "$PUB_LOG" 2>&1
}

start_services() {
  command -v tmux >/dev/null
  test -s "$AWS_ENV"
  local_preflight
  mkdir -p "$RUN_ROOT/launch" "$EVAL_ROOT/publication"

  if tmux has-session -t "$PUB_SESSION" 2>/dev/null || publisher_running; then
    echo "V4 publisher is already running; leaving it unchanged."
  else
    tmux new-session -d -s "$PUB_SESSION" "$SELF _run_publisher"
    echo "Started progressive publisher in tmux session $PUB_SESSION"
  fi

  if tmux has-session -t "$GEN_SESSION" 2>/dev/null || generation_running; then
    echo "V4 generation is already running; refusing a duplicate runner."
  else
    tmux new-session -d -s "$GEN_SESSION" "$SELF _run_generation"
    echo "Started resumable 108-row generation in tmux session $GEN_SESSION"
  fi
}

status() {
  if tmux has-session -t "$GEN_SESSION" 2>/dev/null; then
    echo "generation tmux: running ($GEN_SESSION)"
  else
    echo "generation tmux: absent"
  fi
  if generation_running; then
    echo "generation process: running"
  else
    echo "generation process: absent"
  fi
  if tmux has-session -t "$PUB_SESSION" 2>/dev/null; then
    echo "publisher tmux: running ($PUB_SESSION)"
  else
    echo "publisher tmux: absent"
  fi
  if publisher_running; then
    echo "publisher process: running"
  else
    echo "publisher process: absent"
  fi
  if [[ -f "$RUN_ROOT/summary.json" ]]; then
    python3 - "$RUN_ROOT/summary.json" <<'PY'
import json
import sys
from pathlib import Path

summary = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print("generation summary:", json.dumps({
    "record_status_counts": summary.get("record_status_counts"),
    "pending_job_count": summary.get("pending_job_count"),
    "selected_missing_record_count": summary.get("selected_missing_record_count"),
    "ambiguous_submission_count": summary.get("ambiguous_submission_count"),
}, sort_keys=True))
PY
  fi
  if [[ -f "$RUN_ROOT/launch/generation_supervisor_state.json" ]]; then
    python3 - "$RUN_ROOT/launch/generation_supervisor_state.json" <<'PY'
import json
import sys
from pathlib import Path

state = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print("generation supervisor:", json.dumps({
    "status": state.get("status"),
    "invocation_count": state.get("invocation_count"),
    "lifetime_invocation_count": state.get("lifetime_invocation_count"),
    "decision": state.get("decision"),
}, sort_keys=True))
PY
  fi
}

case "${1:-}" in
  preflight) local_preflight ;;
  start|resume) start_services ;;
  status) status ;;
  _run_generation) run_generation ;;
  _run_publisher) run_publisher ;;
  *)
    echo "usage: $0 {preflight|start|resume|status}" >&2
    exit 2
    ;;
esac
