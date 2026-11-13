# V22.4.3-R1 preparation audit

## Scope

A new qualitative-assembly wrapper was created at:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_3_r1`

No V22.4.3 pipeline, prompt, geometry, guard, or threshold file changed. The new wrapper permits at most one fresh outer endpoint job after an exact terminal product-invariant guard rejection and selects the first passing job.

## Isolation

- Endpoint port: `8132`
- Endpoint tmux session: `hp-v2243r1-full160-endpoint`
- Runner tmux session: `hp-v2243r1-full160-runner`
- Experiment ID: `hp-position-flex-v22.4.3-r1-qualitative-assembly-v6.1-full160`
- S3 prefix: `s3://foundry-hp-enterprise-adobe-assets/hp_position_flex_v22_4_3_r1_qualitative_assembly_v6_1_20261106/grouped/`
- Run root: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_3_r1/run`

The prior V22.4.3 tree was verified byte-for-byte against the 58-file preparation manifest after this work.

## Audit contract

Each job preserves `submission_request.json`, immutable terminal `status.json`, and either `provenance.json` or `failure_provenance.json`. Both success and failure provenance include row/job identity, outer-attempt number, request hash, wrapper/pipeline identity, source hashes, model-call audit when available, and a recursive artifact manifest with hashes and byte sizes. Progress records the status and provenance hashes for every attempted outer job.

## Verification

- 13 wrapper contract tests passed.
- Frozen 160-row / 16-bank / 10-rank source contract passed.
- Freeze verification passed.
- Local preflight passed.
- Grouped-report input validation passed.
- No run or log directory exists.
- No endpoint, runner, or model call was launched.

## Methodological note

A bounded outer retry is acceptable for producing a reviewable qualitative set only when it is explicit and fully audited. It changes the unit from one native pipeline job to “up to two independent jobs, first passing job selected.” Therefore the report must expose first-job pass, recovered-on-retry, and terminal-failure rates, and must never present the selected 160 as V22.4.3's native reliability. The preserved initial failures remain evidence and cannot be discarded or overwritten.

## Evidence

- Exact wrapper diff: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_3_r1/WRAPPER_DIFF_FROM_V22_4_3.patch`
- Frozen package hashes: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_3_r1/V22_4_3_R1_PACKAGE_SHA256.txt`
- Pipeline source identity: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_3_r1/PIPELINE_SOURCE_IDENTITY.json`
- Preserved base-tree hashes: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_3_r1/PREPARATION_BASE_TREE_SHA256.txt`
