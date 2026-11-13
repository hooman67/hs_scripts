# Offline validation

Validated on 2026-11-06 without launching the endpoint or making model/generation calls.

- Freeze verification: passed, 4 rows.
- Offline preflight: passed against Foundry HEAD `8c358bc7989cb0e137e89db0fd325168249e2a22`.
- Pilot contract tests: 5 passed.
- Frozen Foundry focused tests (`test_invariants.py`, `test_pipeline.py`, `test_prompts.py`): 79 passed using the frozen `requirements.txt` environment.
- Python compilation: passed.
- Shell syntax: passed.
- Ruff `F`, `E9`, and import-order checks: passed.
- Runtime directories: absent; the endpoint and pilot were not launched.

The frozen manifest is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/pilot_v23_all_view_translation/freeze.json`

Its SHA-256 is `19cb1066741def4927f7d0465417dad3f2922a0dc637d2adedf9afb41cfb24aa`.
