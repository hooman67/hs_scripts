# V22.4.2 position-flex full-160 package

Status: **prepared and locally validated; no endpoint, model, image, or S3 call has been launched from this package.**

This package runs the exact 160 V6.1 prompt/device/camera rows through the frozen V22.4.2 treatment. It replays each row's original reference selection, Stage-A geometry, and byte-identical geometry guide. Stage B and image generation remain live. The only change from V22.4.1 is that a fixed-position `affine_fit_failed` result with an RGBA mask dispatches to the same frozen alpha fallback already used for no/too-few features.

## Safety and reproducibility contract

- `freeze.json` pins all 160 record files individually, the V6.1 prompt export, the Foundry PR commit, the V22.4.2 source files, the original control report, the original grouped judge report used to locate digital twins, and the canonical FE viewer.
- All outputs are isolated below `full160_v22_4_2/run/`; no V21, earlier smoke, or prior full-160 cache path is reused. The failed V22.3.3 and V22.4.1 trees are explicit forbidden output locations.
- The endpoint has one worker. The runner is serial and uses an exclusive file lock.
- Progress is replaced atomically after each fully validated row.
- A pipeline or guard failure is recorded as `first_error` and stops the run immediately. There is no runner retry. The sole permitted second attempt is V22.4.2's bounded in-pipeline fixed-position fallback.
- A completed row must retain the product input, alpha mask, style reference, geometry text/requests/responses/guide, planning request/response, all Stage-B audits, every raw image request/output, every invariant audit, all live-call audits, and the guard-selected output. The selected attempt must have `verdict: pass` and match the selected raw image byte-for-byte.
- Resume validates every already-completed row before moving forward.

## Preflight

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
PYTHONPATH=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2 \
  python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2/freeze_inputs.py --verify-only
PYTHONPATH=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2 \
  python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2/preflight.py --allow-progress
PYTHONPATH=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2 \
  python -m unittest discover -s /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2/tests -v
```

Do not launch if any command fails. A source hash failure means the treatment is no longer the frozen V22.4.2 implementation and must receive a new explicit version/freeze.

## Detached tmux runbook

Offline replay preserves all eight V22.4.1 smoke selections and now selects attempt 2 for the preserved V22.4.1 first-row failure. No V22.4.2 model call has been made. Launch remains a deliberate separate action:

```bash
/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2/launch_tmux.sh
```

Monitor without attaching:

```bash
tmux capture-pane -pt hp-v2242-full160-runner -S -60
tail -f /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2/logs/full160.stdout.log
```

The endpoint binds only to `127.0.0.1:8129`. The runner fails fast on the first bad row. If `run/progress.json` contains `first_error`, inspect the preserved row artifacts before any deliberate restart; the runner will refuse to silently continue past it.

## Grouped FE report

After 160/160 complete, build the 16-bank × 10-prompt report:

```bash
PYTHONPATH=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2 \
  python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2/build_grouped_report.py
```

After a new placement-judge report exists, rebuild and merge its text evidence:

```bash
PYTHONPATH=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2 \
  python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2/build_grouped_report.py \
  --judge-report /absolute/path/to/treatment/judge/data.json
```

The builder creates `report/viewer.html`, a root `data.json`, 16 linked per-bank reports, and local assets for selected treatment output, guide, and both raw attempts when fallback occurred. It performs no upload. `report/build_manifest.json` records the intended S3 destination and every group hash. Use `/aws-creds` before the later explicit S3 publication step.

