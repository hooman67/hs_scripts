#!/usr/bin/env bash
set -euo pipefail

# Deliberately not invoked during preparation. Run only after the V22.3.3 gate
# is accepted. Two durable sessions keep the endpoint and serial runner alive
# after SSH disconnects.
root=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_3_3
endpoint_session=hp-v2233-full160-endpoint
runner_session=hp-v2233-full160-runner

PYTHONPATH="$root" python "$root/preflight.py" --allow-progress
if tmux has-session -t "$endpoint_session" 2>/dev/null; then
  printf 'Refusing: tmux session already exists: %s\n' "$endpoint_session" >&2
  exit 1
fi
if tmux has-session -t "$runner_session" 2>/dev/null; then
  printf 'Refusing: tmux session already exists: %s\n' "$runner_session" >&2
  exit 1
fi
tmux new-session -d -s "$endpoint_session" "$root/run_endpoint.sh"

for _ in $(seq 1 120); do
  if curl -fsS http://127.0.0.1:8127/health >/dev/null; then
    tmux new-session -d -s "$runner_session" "$root/run_full160.sh"
    printf 'Started %s and %s\n' "$endpoint_session" "$runner_session"
    exit 0
  fi
  sleep 1
done

printf 'Endpoint did not become healthy; runner was not launched.\n' >&2
exit 1

