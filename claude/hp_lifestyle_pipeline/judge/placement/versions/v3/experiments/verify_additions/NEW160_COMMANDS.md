# Reusable new-160 two-pass and verifier commands

The decision policy was developed posthoc on prior comment checks. The new-160 run is a frozen-protocol, unlabeled, new-image evaluation. Replace the uppercase placeholders with new, unused names and absolute paths.

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline

uv run --script judge/placement/versions/v3/experiments/two_pass/combine.py \
  --manifest /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3/data/new_v6_1_eval_20261105/manifest.json \
  --baseline-run /ABSOLUTE/V2_160_RUN \
  --compact-run /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3/runs/v6_1_compact_v3 \
  --run-name V6_1_TWO_PASS_NAME

CAMPAIGN=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3/experiments/verify_additions_v6_1
mkdir -p "$CAMPAIGN"
cp judge/placement/versions/v3/experiments/verify_additions/{build_triggers.py,run_verifier.py,run_batch.py,merge_verified.py,freeze.py,system_prompt.md} "$CAMPAIGN/"
cp judge/placement/versions/v3/experiments/verify_additions/merge_verified_v2_new160.py "$CAMPAIGN/merge_verified_v2.py"
cp judge/placement/versions/v3/experiments/verify_additions/selected_protocol_v2.json "$CAMPAIGN/"
cp judge/placement/versions/v3/experiments/verify_additions/protocol_snapshots/policy_v2_new160/snapshot_manifest.json "$CAMPAIGN/selected_protocol_snapshot_manifest.json"

python "$CAMPAIGN/build_triggers.py" \
  --source-run "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3/experiments/two_pass/runs/V6_1_TWO_PASS_NAME" \
  --output "$CAMPAIGN/triggers.json"

python "$CAMPAIGN/freeze.py"
uv run --script "$CAMPAIGN/run_batch.py" --run-name VERIFIER_RUN_NAME --workers 3 --model gpt-5.5

python "$CAMPAIGN/merge_verified_v2.py" \
  --source-run "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3/experiments/two_pass/runs/V6_1_TWO_PASS_NAME" \
  --verifier-run "$CAMPAIGN/runs/VERIFIER_RUN_NAME" \
  --run-name VERIFIED_ENVELOPE_NAME \
  --development-status frozen_protocol_unlabeled_new_image_evaluation
```

Before each model call, inspect `triggers.json`, confirm its exact case/component counts and absence of comment/expectation keys, then preserve `freeze.json`. Never reuse a run name or overwrite a prior campaign.
