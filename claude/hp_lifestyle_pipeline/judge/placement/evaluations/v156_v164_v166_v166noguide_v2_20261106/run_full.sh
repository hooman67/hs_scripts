#!/usr/bin/env bash
set -euo pipefail

ROOT=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
HERE="$ROOT/judge/placement/evaluations/v156_v164_v166_v166noguide_v2_20261106"
MANIFEST="$HERE/manifest.json"
V2_RUN=v156-v164-v166-v166noguide-v2-full-v2
V3_RUN=v156-v164-v166-v166noguide-v2-full-v3
TWO_PASS_RUN=v156-v164-v166-v166noguide-v2-two-pass
CONSENSUS_RUN=v156-v164-v166-v166noguide-v2-consensus-v1
PROP="$ROOT/judge/placement/versions/v3/experiments/verify_additions_v156_v164_v166_v166noguide_v2"
NAMES="$ROOT/judge/placement/versions/v3/experiments/independent_component_check_v156_v164_v166_v166noguide_v2"
TWO_PASS="$ROOT/judge/placement/versions/v3/experiments/two_pass/runs/$TWO_PASS_RUN"

cd "$ROOT"
mkdir -p "$HERE/logs"
date --iso-8601=seconds >"$HERE/logs/full.started.txt"

(
  uv run --script judge/placement/versions/v2/run_batch.py \
    --manifest "$MANIFEST" --run-name "$V2_RUN" --workers 2 \
    --model gpt-5.5 --visual-anchors \
    >"$HERE/logs/full_v2.stdout.log" 2>"$HERE/logs/full_v2.stderr.log"
) &
v2_pid=$!

(
  uv run --script judge/placement/versions/v3/run_batch.py \
    --manifest "$MANIFEST" --run-name "$V3_RUN" --workers 2 \
    --model gpt-5.5 \
    >"$HERE/logs/full_v3.stdout.log" 2>"$HERE/logs/full_v3.stderr.log"
) &
v3_pid=$!

set +e
wait "$v2_pid"; v2_status=$?
wait "$v3_pid"; v3_status=$?
set -e
printf '%s\n' "$v2_status" >"$HERE/logs/full_v2.exit.txt"
printf '%s\n' "$v3_status" >"$HERE/logs/full_v3.exit.txt"
test "$v2_status" -eq 0
test "$v3_status" -eq 0

uv run --script judge/placement/versions/v3/experiments/two_pass/combine.py \
  --manifest "$MANIFEST" \
  --baseline-run "$ROOT/judge/placement/versions/v2/runs/$V2_RUN" \
  --compact-run "$ROOT/judge/placement/versions/v3/runs/$V3_RUN" \
  --run-name "$TWO_PASS_RUN" \
  >"$HERE/logs/two_pass.stdout.log" 2>"$HERE/logs/two_pass.stderr.log"

python "$PROP/build_triggers.py" \
  --source-run "$TWO_PASS" --output "$PROP/triggers.json" \
  >"$HERE/logs/build_triggers.stdout.log" 2>"$HERE/logs/build_triggers.stderr.log"
python "$PROP/freeze.py" \
  >"$HERE/logs/freeze_proposal.stdout.log" 2>"$HERE/logs/freeze_proposal.stderr.log"
uv run --script "$PROP/run_batch.py" --run-name proposal-aware-v1 --workers 3 --model gpt-5.5 \
  >"$HERE/logs/proposal.stdout.log" 2>"$HERE/logs/proposal.stderr.log"

python "$NAMES/build_manifest.py" --triggers "$PROP/triggers.json" --output "$NAMES/input_manifest.json" \
  >"$HERE/logs/build_names.stdout.log" 2>"$HERE/logs/build_names.stderr.log"
python "$NAMES/freeze.py" \
  >"$HERE/logs/freeze_names.stdout.log" 2>"$HERE/logs/freeze_names.stderr.log"
uv run --script "$NAMES/run_batch.py" --run-name names-only-v1 --workers 3 --model gpt-5.5 \
  >"$HERE/logs/names.stdout.log" 2>"$HERE/logs/names.stderr.log"

python judge/placement/versions/v3/experiments/consensus_policy/merge_consensus_v2.py \
  --source-run "$TWO_PASS" \
  --proposal-aware-run "$PROP/runs/proposal-aware-v1" \
  --names-only-run "$NAMES/runs/names-only-v1" \
  --trigger-manifest "$PROP/triggers.json" \
  --run-name "$CONSENSUS_RUN" \
  >"$HERE/logs/consensus.stdout.log" 2>"$HERE/logs/consensus.stderr.log"

date --iso-8601=seconds >"$HERE/logs/full.finished.txt"
printf '0\n' >"$HERE/logs/full.exit.txt"
