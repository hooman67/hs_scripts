#!/usr/bin/env bash
set -euo pipefail
umask 077

if [[ $# -lt 1 ]]; then
  echo "usage: $0 SESSION [run_generation.py flags, including optional --row-ids ...]" >&2
  exit 2
fi

session=$1
endpoint_base_url=http://127.0.0.1:8137
deployment_manifest_sha256=b2a852792ef8029e867fb37c3c21c394d6e47fed7e81dc103fbe726d0ec0604c
shift

for argument in "$@"; do
  case "$argument" in
    --prompts|--prompts=*|--prompts-sha256|--prompts-sha256=*|--run-dir|--run-dir=*|--prefix|--prefix=*|--bucket|--bucket=*|--endpoint-base-url|--endpoint-base-url=*|--expected-generator|--expected-generator=*|--expected-rewriter|--expected-rewriter=*|--expected-pipeline-version|--expected-pipeline-version=*|--lineage-label|--lineage-label=*|--lineage-source-commit|--lineage-source-commit=*|--lineage-patch-sha256|--lineage-patch-sha256=*|--lineage-runtime-tree-sha256|--lineage-runtime-tree-sha256=*|--lineage-source-manifest-sha256|--lineage-source-manifest-sha256=*|--lineage-deployment-manifest-sha256|--lineage-deployment-manifest-sha256=*|--lineage-candidate-config-sha256|--lineage-candidate-config-sha256=*)
      echo "candidate launcher owns immutable identity flag: $argument" >&2
      exit 2
      ;;
  esac
done

root=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108
prompts=$root/exports/v6.2-surfaces-20261109-r5-final/prompts_all_160.json
run_dir=$root/runs/generated_surface_shape_r1_env2
prefix=eval_sets/hp_lifestyle_surface_diversity_v6_2_gpt_image2_scene_20261108/generated_surface_shape_r1_env2
deployment_manifest=$root/local_scene_endpoint/deployment_manifest.json
if [[ ! -f $deployment_manifest ]] || [[ $(sha256sum "$deployment_manifest" | awk '{print $1}') != $deployment_manifest_sha256 ]]; then
  echo "candidate deployment manifest is missing or differs from the frozen SHA-256" >&2
  exit 2
fi

exec "$root/launch_tmux.sh" "$session" \
  --prompts "$prompts" \
  --prompts-sha256 e661123648d8b64bf37b462e482a8015fc8e9219cf3798781271719b99929500 \
  --run-dir "$run_dir" \
  --prefix "$prefix" \
  --endpoint-base-url "$endpoint_base_url" \
  --expected-generator 'GPT Image 2.5 / single reference / no grading' \
  --expected-rewriter 'Adobe-Firefly/foundry#4349 / 8c358bc7989c + surface-shape-r1 / unified-blue-scale-v20-surface-shape-r1' \
  --expected-pipeline-version unified-blue-scale-v20-surface-shape-r1 \
  --lineage-label hp-v6.2-surface-shape-r1 \
  --lineage-source-commit 8c358bc7989cb0e137e89db0fd325168249e2a22 \
  --lineage-patch-sha256 95ddc80d7d62e75c6f7461a45011a6412a35a4bc03a36fada517fdf5888a8843 \
  --lineage-runtime-tree-sha256 631fe047e7b82c6c690f038effda1155b0ffde5ecdbf8be745164db649a80de5 \
  --lineage-source-manifest-sha256 17346485b892b02714f52940b2bbd1806de99c06c8c23816b5c1b11a4564d172 \
  --lineage-deployment-manifest-sha256 "$deployment_manifest_sha256" \
  --lineage-candidate-config-sha256 9ae1f16c2ace027ad6da157356e5025c1ae06722f6c4cb2955b15f0a959b4b08 \
  "$@"
