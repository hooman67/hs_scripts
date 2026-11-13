#!/usr/bin/env bash
set -euo pipefail
umask 077

if [[ $# -lt 2 ]]; then
  echo "usage: $0 SESSION [run_generation.py flags...]" >&2
  exit 2
fi

session=$1
shift
root=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108
run_dir=
previous=
for argument in "$@"; do
  if [[ $previous == --run-dir ]]; then
    run_dir=$argument
    break
  fi
  previous=$argument
done
if [[ -z $run_dir ]]; then
  echo "--run-dir is required" >&2
  exit 2
fi
if tmux has-session -t "$session" 2>/dev/null; then
  echo "tmux session already exists: $session" >&2
  exit 2
fi

mkdir -p "$run_dir/journals"
runner=(
  uv run --python 3.12
  --with 'foundry-aws-gateway>=2.0.0'
  --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple'
  "$root/run_generation.py" "$@"
)
printf -v runner_q '%q ' "${runner[@]}"
printf -v log_q '%q' "$run_dir/journals/tmux.stdout.log"
printf -v exit_q '%q' "$run_dir/journals/tmux.exit.txt"
printf -v started_q '%q' "$run_dir/journals/tmux.started.txt"
printf -v finished_q '%q' "$run_dir/journals/tmux.finished.txt"
command="date --iso-8601=seconds > $started_q; set -o pipefail; $runner_q 2>&1 | tee -a $log_q; status=\${PIPESTATUS[0]}; printf '%s\\n' \"\$status\" > $exit_q; date --iso-8601=seconds > $finished_q; exit \"\$status\""
tmux new-session -d -s "$session" "bash -lc $(printf '%q' "$command")"
echo "launched $session"
echo "log: $run_dir/journals/tmux.stdout.log"

