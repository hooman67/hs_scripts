# V22.4.3 full-160 candidate package

This isolated package is prepared for the exact frozen 160 V6.1 rows. It has not been launched.

V22.4.3 changes only product-guard dispatch for fixed-position RGBA inputs. When a fitted affine has structurally insufficient evidence—too few inliers or inadequate source landmark spread, quadrant coverage, or hull coverage—the guard preserves the affine metrics and reasons, then lets the already-frozen alpha-mask fallback decide. Reliable dense affine failures, including scale, rotation, shear, and excess translation, remain affine-only failures.

No prompt, geometry policy, model-call policy, threshold, retry count, selection rule, or alpha-fallback implementation changed. Both system prompts are byte-identical to V22.4.2.

The local wrapper retains the corrected standard Stage-B artifact contract from V22.4.2.1:

- every Stage-B attempt requires its request and response artifact;
- a two-call Stage-B fallback additionally requires the raw second response;
- every image attempt requires its image request, raw image, and invariant audit;
- every provenance artifact is hash- and size-verified;
- `ours.png` must equal the guard-selected raw attempt; and
- planning artifacts are not required when `reference_blue=None`.

## Isolation

- Package: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_3`
- Run root: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_3/run`
- Local endpoint: `127.0.0.1:8131`
- tmux sessions: `hp-v2243-full160-endpoint`, `hp-v2243-full160-runner`

## Offline verification

```bash
root=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_3
PYTHONPATH="$root" python "$root/freeze_inputs.py" --verify-only
PYTHONPATH="$root" python "$root/preflight.py"
PYTHONPATH="$root" python -m pytest "$root/tests" -q -p no:cacheprovider
```

The freeze contains 160 rows in 16 banks of 10, exact record and prompt-export hashes, V22.4.3 pipeline hashes, and standard-wrapper source hashes.

## Deliberate launch command

Do not launch until the V22.4.3 replay evidence is accepted. The prepared command is:

```bash
/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_3/launch_tmux.sh
```

The runner is serial and fail-fast. It preserves the first error and never silently continues.
