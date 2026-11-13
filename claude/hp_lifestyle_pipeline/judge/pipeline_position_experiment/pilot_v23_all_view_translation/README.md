# V23 all-view translation pilot package

Prepared offline on 2026-11-06. It has **not** launched an endpoint or made any model or generation call.

This package freezes the final V23 Foundry treatment and exactly four rank-1 V6.1 rows:

- Cashmere laptop, `Front_CloseUp`
- Cashmere laptop, `Front_Wide`
- Tassel printer, `Front_CloseUp`
- Tassel printer, `Front_Wide`

The endpoint and runner use one immutable outer job per row, process rows serially, hash-audit every terminal artifact, stop after the first failure, and preserve its status, provenance, artifacts, progress, and logs. The runner does not silently retry a failed row.

The package is isolated at:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/pilot_v23_all_view_translation`

The frozen Foundry checkout is read directly from:

`/home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25`

Run the offline gate:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/pilot_v23_all_view_translation
PYTHONPATH="$PWD" python preflight.py
```

Only after accepting the freeze and preflight, launch the detached endpoint and runner with:

```bash
/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/pilot_v23_all_view_translation/launch_tmux.sh
```

Runtime state will be preserved under the package's `run/` and `logs/` directories. A failed row records `first_failure` in `run/progress.json`; inspect it before any manual restart.
