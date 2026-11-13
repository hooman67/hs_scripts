#!/usr/bin/env bash
set -euo pipefail

# Prepared but deliberately not invoked. The runner is serial and stops after
# preserving the first terminal failure. Detached sessions survive SSH logout.
root=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/pilot_v23_1_all_view_translation
endpoint_session=hp-v231-pilot-endpoint
runner_session=hp-v231-pilot-runner

PYTHONPATH="$root" python "$root/preflight.py" --allow-progress
for session in "$endpoint_session" "$runner_session"; do
  if tmux has-session -t "$session" 2>/dev/null; then
    printf 'Refusing: tmux session already exists: %s\n' "$session" >&2
    exit 1
  fi
done

tmux new-session -d -s "$endpoint_session" "$root/run_endpoint.sh"
for _ in $(seq 1 120); do
  if curl -fsS http://127.0.0.1:8134/health >/dev/null; then
    tmux new-session -d -s "$runner_session" "$root/run_pilot.sh"
    printf 'Started %s and %s\n' "$endpoint_session" "$runner_session"
    exit 0
  fi
  sleep 1
done

printf 'Endpoint did not become healthy; runner was not launched. Endpoint logs were preserved.\n' >&2
exit 1
