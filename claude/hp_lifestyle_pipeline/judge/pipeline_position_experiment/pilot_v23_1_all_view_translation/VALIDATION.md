# Offline validation

Validated on 2026-11-06 without launching the endpoint or making model or generation calls.

- Freeze verification: passed for 8 rows in two explicit 4-row cohorts.
- Offline preflight: passed against Foundry HEAD `8c358bc7989cb0e137e89db0fd325168249e2a22`.
- Diagnostic prompts: exact AST-derived equality with the existing audited `RELOCATION_PROMPTS` fixture source.
- Pilot contract tests: 6 passed.
- Frozen Foundry production tests: 180 passed.
- Python compilation: passed.
- Shell syntax: passed.
- Ruff `F`, `E9`, and import-order checks: passed.
- Runtime directories: absent; the endpoint and pilot were not launched.

Frozen manifest:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/pilot_v23_1_all_view_translation/freeze.json`

Freeze SHA-256: `ee4a8462249ca133549afe0d48087b0ad6c7513e55fc88bd7b53b4a1ca755279`.

Frozen V23.1 source SHA-256 values include:

- `hp3p/pipeline.py`: `ef1158a882dca0c8a85d01e3ed427d036282b29341fa5beeb88c9d4db39d9137`
- `hp3p/invariants.py`: `808bde48be35ba6093dc01d0cc23808f0c7f4509b62e79dce64d1033674c19a6`
- `hp3p/prompts/system_3p.txt`: `324ce0e449804bc0d17ac0cf5ed10587716bc9d7e6ef72b9a91e439745b6aaec`
- `hp3p/prompts/system_3p_fixed_position.txt`: `67e4d817a5a203912116bb99afbd6c4511d9a5c537b241cc6e980e34e75b1118`
