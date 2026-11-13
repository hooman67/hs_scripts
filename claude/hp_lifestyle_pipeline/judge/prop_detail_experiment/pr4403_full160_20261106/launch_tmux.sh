#!/usr/bin/env bash
set -euo pipefail
root=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/prop_detail_experiment/pr4403_full160_20261106
endpoint_session=hp-pr4403-props-endpoint
runner_session=hp-pr4403-props-runner
mkdir -p "$root/logs"
source <(sed -n '/^export AWS_/p' /mnt/localssd/temp_creds.txt)
PYTHONPATH="$root:/home/colligo/foundry-pr4403-prop-exp/experimental/adarabi/hp-3p-gpt25" python "$root/preflight.py"
tmux has-session -t "$endpoint_session" 2>/dev/null && { echo "session exists: $endpoint_session" >&2; exit 1; }
tmux has-session -t "$runner_session" 2>/dev/null && { echo "session exists: $runner_session" >&2; exit 1; }
tmux new-session -d -s "$endpoint_session" "source <(sed -n '/^export AWS_/p' /mnt/localssd/temp_creds.txt); exec '$root/run_endpoint.sh'"
for _ in $(seq 1 180); do
  if curl -fsS http://127.0.0.1:8135/health >/dev/null; then
    tmux new-session -d -s "$runner_session" "source <(sed -n '/^export AWS_/p' /mnt/localssd/temp_creds.txt); exec '$root/run_full160.sh'"
    echo "started $endpoint_session and $runner_session"
    exit 0
  fi
  sleep 1
done
echo "endpoint failed health check" >&2
exit 1
