# V23.1 all-view translation eight-row pilot

This is a fresh, isolated package for the V23.1 strong-low-inlier invariant guard. Preparation does not launch the endpoint or make model or generation calls.

Package:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/pilot_v23_1_all_view_translation`

Frozen Foundry source:

`/home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25`

## Cohorts

The first four rows are the original rank-1 V6.1 representative rows:

- Cashmere laptop `Front_CloseUp`
- Cashmere laptop `Front_Wide`
- Tassel printer `Front_CloseUp`
- Tassel printer `Front_Wide`

The final four rows are movement-demand diagnostics using existing audited prompts and the corresponding frozen V6.1 product, Stage-A, style-reference and geometry-guide inputs:

- Cashmere laptop `Front_CloseUp`
- Cashmere laptop `Front_Wide`
- Magic printer `Front_CloseUp`
- Magic printer `Front_Wide`

The diagnostic prompt source is frozen and mechanically compared with:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/run_v22_smoke.py`

## Execution policy

Rows run serially with exactly one immutable outer job each. Every terminal artifact is hash-audited. The runner stops after the first terminal failure and preserves the failure status, provenance, raw artifacts, progress and logs. There is no silent outer retry.

Run the offline gate:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/pilot_v23_1_all_view_translation
PYTHONPATH="$PWD" python preflight.py
```

The detached launch command is prepared for later authorization:

```bash
/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/pilot_v23_1_all_view_translation/launch_tmux.sh
```

It was not invoked during package preparation.

## FE review report

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/pilot_v23_1_all_view_translation/build_fe_report.py`

is completion-gated. It refuses to build unless all eight rows are successful and then validates every frozen row, runtime input, raw image attempt, selected output, status, provenance record, and artifact hash. Its report includes the two cohorts, scene prompt, digital twin, geometry guide, every raw attempt, selected output, guard/localization metrics, Stage-B rewrite, executable prompt, and collapsible row-level provenance/debug information.

After the pilot completes, build locally with:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/pilot_v23_1_all_view_translation
PYTHONPATH="$PWD" python build_fe_report.py
```

The prepared builder performs no upload. Its immutable eventual destination is:

`s3://foundry-hp-enterprise-adobe-assets/hp_position_flex_v23_1_pilot_20261106/review/`

The report URL carries one `Pass / Fail / Borderline` placement question with a per-question comment field.
