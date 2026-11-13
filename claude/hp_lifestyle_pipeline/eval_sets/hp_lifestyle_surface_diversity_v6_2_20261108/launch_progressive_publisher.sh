#!/usr/bin/env bash
set -euo pipefail
umask 077

session=${1:-hp-v62-surface-shape-publisher}
root=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108
run_dir=$root/runs/generated_surface_shape_r1_env2
if [[ ! -f $run_dir/run_manifest.json ]]; then
  echo "env2 run manifest does not exist yet: $run_dir/run_manifest.json" >&2
  exit 2
fi
if tmux has-session -t "$session" 2>/dev/null; then
  echo "tmux session already exists: $session" >&2
  exit 2
fi

mkdir -p "$run_dir/journals"
command=(
  uv run --python 3.12
  --with 'foundry-aws-gateway>=2.0.0'
  --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple'
  "$root/progressive_publish.py"
  --run-dir "$run_dir"
  --prompts "$root/exports/v6.2-surfaces-20261109-r5-final/prompts_all_160.json"
  --prompts-txt "$root/exports/v6.2-surfaces-20261109-r5-final/prompts_all_160.txt"
  --catalog /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/revisions/v6.2-surfaces-20261109-r5-recognition/runtime/v6_2/approved_catalog.json
  --title 'HP V6.2 Surface Diversity — shape-aware V20, 160 scenes'
  --interval-seconds 60
  --minimum-done 1
)
printf -v command_q '%q ' "${command[@]}"
printf -v log_q '%q' "$run_dir/journals/publisher.stdout.log"
printf -v exit_q '%q' "$run_dir/journals/publisher.exit.txt"
shell_command="set -o pipefail; $command_q 2>&1 | tee -a $log_q; status=\${PIPESTATUS[0]}; printf '%s\\n' \"\$status\" > $exit_q; exit \"\$status\""
tmux new-session -d -s "$session" "bash -lc $(printf '%q' "$shell_command")"
echo "launched $session"
echo "log: $run_dir/journals/publisher.stdout.log"
