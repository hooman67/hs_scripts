# Failed mechanical smoke: pre-contract-fix prompt

This attempt is excluded from the four-fixture treatment. It is retained as failure evidence, not selected output.

- The first fixture completed one Astra writing call and one GPT Image call.
- The second fixture stopped before its GPT Image call because Stage B emitted `Follow the reference tabletop`.
- `_check_image_prompt` correctly rejected that unseen-image wording.
- No manual output repair occurred.
- The remaining fixtures were not run.
- The source prompt was revised to use `baseline layout/geometry` instead of `reference` in all translation-policy language that Stage B could copy.
- A focused regression assertion now rejects the standalone word `reference` in the assembled image prompt and the translation-policy prefix.
- The entire treatment directory and logs were archived before a fresh run with new prompt-source hashes.

Archived treatment:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/smoke/archived/treatment_pre_contract_fix_20261106T023241Z`

The failing source result is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/smoke/archived/treatment_pre_contract_fix_20261106T023241Z/cashmere__laptop_FrontWide__p1/run/rows/cashmere__laptop_FrontWide__p1/result.json`
