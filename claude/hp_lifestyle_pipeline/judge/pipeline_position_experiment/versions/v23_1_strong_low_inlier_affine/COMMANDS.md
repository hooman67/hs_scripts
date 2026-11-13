# Exact commands

```bash
CAND=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_1_strong_low_inlier_affine
SRC=/home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25/hp3p/invariants.py
RUN="$CAND/calibration/run_1"

sha256sum "$SRC" > "$RUN/FOUNDRY_GUARD_SHA256_BEFORE.txt"
sha256sum "$CAND/candidate_invariants.py" > "$RUN/CANDIDATE_GUARD_SHA256_BEFORE.txt"

python -m pytest -q "$CAND/test_candidate_invariants.py"
python -m py_compile "$CAND/candidate_invariants.py" "$CAND/calibration/replay_v23_1_calibration.py"

V23_CALIBRATION_OUT="$RUN" \
  python "$CAND/calibration/replay_v23_1_calibration.py" \
  > "$RUN/replay.stdout" 2> "$RUN/replay.stderr"

python "$CAND/replay_tassel_pilot.py" \
  > "$RUN/tassel_pilot_replay.stdout"
python "$CAND/compare_run3.py" \
  > "$RUN/comparison_to_v23_run3.stdout"

sha256sum "$SRC" > "$RUN/FOUNDRY_GUARD_SHA256_AFTER.txt"
sha256sum "$CAND/candidate_invariants.py" > "$RUN/CANDIDATE_GUARD_SHA256_AFTER.txt"
diff -u "$RUN/FOUNDRY_GUARD_SHA256_BEFORE.txt" "$RUN/FOUNDRY_GUARD_SHA256_AFTER.txt"
diff -u "$RUN/CANDIDATE_GUARD_SHA256_BEFORE.txt" "$RUN/CANDIDATE_GUARD_SHA256_AFTER.txt"
```
