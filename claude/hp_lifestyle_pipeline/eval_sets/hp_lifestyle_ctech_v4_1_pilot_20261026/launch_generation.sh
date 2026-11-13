#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
EVAL_ROOT="$PROJECT_ROOT/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026"
RUN_ROOT="$PROJECT_ROOT/local_data/generation_runs/hp_lifestyle_ctech_v4_1_pilot_20261026_corrected_twins_20261027"
RUNNER="$EVAL_ROOT/generation/run_generation.py"
SUPERVISOR="$EVAL_ROOT/generation/supervise_generation.py"
SESSION=hp_ctech_v4_1_generation_20261027
SMOKE_SESSION=hp_ctech_v4_1_smoke_20261027
LOG="$RUN_ROOT/launch/generation.log"
SMOKE_LOG="$RUN_ROOT/launch/smoke.log"
SELF=$(readlink -f "$0")

generation_running() {
  pgrep -f "$SUPERVISOR.*--run-dir" >/dev/null 2>&1 || \
    pgrep -f "$RUNNER.*--all" >/dev/null 2>&1 || \
    pgrep -f "$RUNNER.*--row-id" >/dev/null 2>&1
}

local_validate() {
  cd "$PROJECT_ROOT"
  uv run --script "$RUNNER" --run-dir "$RUN_ROOT" --validate-only
}

preflight() {
  local_validate
  cd "$PROJECT_ROOT"
  uv run --script "$RUNNER" --run-dir "$RUN_ROOT" --preflight-only
}

run_all() {
  umask 077
  mkdir -p "$RUN_ROOT/launch"
  cd "$PROJECT_ROOT"
  exec env \
    -u OPENAI_API_KEY -u AZURE_OPENAI_API_KEY -u AZURE_OPENAI_ENDPOINT \
    -u AWS_ACCESS_KEY_ID -u AWS_SECRET_ACCESS_KEY -u AWS_SESSION_TOKEN \
    uv run --script "$SUPERVISOR" --run-dir "$RUN_ROOT" \
      --poll-window-seconds 1800 --max-invocations 12 >>"$LOG" 2>&1
}

run_smoke() {
  umask 077
  mkdir -p "$RUN_ROOT/launch"
  cd "$PROJECT_ROOT"
  mapfile -t smoke_rows < <(
    uv run --script "$RUNNER" --run-dir "$RUN_ROOT" --list-smoke-candidates |
      python3 -c 'import json,sys; print("\n".join(json.load(sys.stdin)["row_ids"]))'
  )
  if [[ ${#smoke_rows[@]} -ne 4 ]]; then
    echo "expected exactly four smoke rows" >&2
    exit 2
  fi
  args=()
  for row_id in "${smoke_rows[@]}"; do args+=(--row-id "$row_id"); done
  exec env \
    -u OPENAI_API_KEY -u AZURE_OPENAI_API_KEY -u AZURE_OPENAI_ENDPOINT \
    -u AWS_ACCESS_KEY_ID -u AWS_SECRET_ACCESS_KEY -u AWS_SESSION_TOKEN \
    uv run --script "$RUNNER" --run-dir "$RUN_ROOT" \
      "${args[@]}" --workers 4 --upload-workers 2 \
      --poll-window-seconds 1800 >>"$SMOKE_LOG" 2>&1
}

start_all() {
  command -v tmux >/dev/null
  preflight
  mkdir -p "$RUN_ROOT/launch"
  if tmux has-session -t "$SESSION" 2>/dev/null || generation_running; then
    echo "V4.1 generation is already running; refusing a duplicate runner."
    exit 2
  fi
  tmux new-session -d -s "$SESSION" "$SELF _run_all"
  echo "Started resumable 120-row V4.1 generation in tmux session $SESSION"
}

start_smoke() {
  command -v tmux >/dev/null
  preflight
  mkdir -p "$RUN_ROOT/launch"
  if tmux has-session -t "$SMOKE_SESSION" 2>/dev/null || generation_running; then
    echo "V4.1 generation is already running; refusing a duplicate smoke runner."
    exit 2
  fi
  tmux new-session -d -s "$SMOKE_SESSION" "$SELF _run_smoke"
  echo "Started controlled four-row V4.1 smoke in tmux session $SMOKE_SESSION"
}

status() {
  generation_running && echo "generation process: running" || echo "generation process: absent"
  for session in "$SESSION" "$SMOKE_SESSION"; do
    tmux has-session -t "$session" 2>/dev/null && echo "tmux: running ($session)" || echo "tmux: absent ($session)"
  done
  if [[ -f "$RUN_ROOT/summary.json" ]]; then
    python3 - "$RUN_ROOT/summary.json" <<'PY'
import json, sys
from pathlib import Path
s = json.loads(Path(sys.argv[1]).read_text())
print(json.dumps({k: s.get(k) for k in (
    "record_status_counts", "selected_missing_record_count", "pending_job_count",
    "ambiguous_submission_count", "safe_retry_job_count")}, sort_keys=True))
PY
  fi
}

case "${1:-}" in
  validate) local_validate ;;
  preflight) preflight ;;
  smoke) start_smoke ;;
  start|resume) start_all ;;
  status) status ;;
  _run_all) run_all ;;
  _run_smoke) run_smoke ;;
  *) echo "usage: $0 {validate|preflight|smoke|start|resume|status}" >&2; exit 2 ;;
esac
