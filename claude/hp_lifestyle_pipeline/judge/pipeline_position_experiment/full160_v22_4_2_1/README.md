# V22.4.2.1 wrapper-only full-160 package

This package reruns the exact frozen 160 V6.1 rows with the unchanged V22.4.2 pipeline. V22.4.2.1 changes only the local execution/audit wrapper: its artifact contract now matches the standard `reference_blue=None` Stage-B branch used by this experiment.

## Contract correction

- `stage_b_attempt_<n>_request.json` and `stage_b_attempt_<n>_response.json` are required for every declared Stage-B attempt.
- `stage_b_attempt_2_raw_response.json` is additionally required for a two-call Stage-B fallback.
- Every declared image attempt requires its raw image, image request, and invariant result.
- Every artifact in provenance is hash- and size-verified, and `ours.png` must equal the guard-selected raw attempt.
- `planning_request.json` and `planning_response.json` are not required. Those belong to the separate reference-blue branch, while this frozen execution explicitly calls `run_row(..., reference_blue=None)`.

The pipeline source, both system prompts, thresholds, affine guard, model-call policy, and 160 frozen inputs are unchanged.

## Isolation and preservation

- Package: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2_1`
- Run root: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2_1/run`
- Local endpoint: `127.0.0.1:8130`
- tmux sessions: `hp-v22421-full160-endpoint`, `hp-v22421-full160-runner`
- The failed V22.4.2 package tree remains unchanged with tree digest `9dde0a63ddad1ec454f6a73fc00620097c279ef6c78b007252f9daa8bdeb5468` across 62 files.

## Frozen verification

```bash
root=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2_1
PYTHONPATH="$root" python "$root/freeze_inputs.py" --verify-only
PYTHONPATH="$root" python "$root/preflight.py" --allow-progress
PYTHONPATH="$root" python -m unittest discover -s "$root/tests" -v
```

The freeze contains 160 rows in 16 banks of 10, the exact record hashes, prompt-export hash, unchanged V22.4.2 pipeline source hashes, and hashes of the V22.4.2.1 wrapper sources.

## Launch

No endpoint, model call, image generation, or full-160 run has been launched from this package. After root review:

```bash
/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2_1/launch_tmux.sh
```

Monitor with:

```bash
tmux capture-pane -pt hp-v22421-full160-runner -S -60
tail -f /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2_1/logs/full160.stdout.log
```

The runner is serial and fail-fast. It preserves the first error and refuses to continue silently. The grouped report builder remains available after 160/160 completion.
