# V6.2 writer and natural-placement judge V4 status

Date: 2026-11-06

## Prompt writer V6.2

V6.2 is implemented as an isolated successor to V6.1 at:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_2`

It adds laptop support-shape diversity, coherent populated walls, camera-aware spatial composition, prop placement rules, and printer-specific equipment-table placement. V6.1 is unchanged.

The frozen R3 GPT-5.5 text pilot contains four representative banks and 40 prompts. All four banks passed after the one allowed automatic repair; no prompt was manually edited. The prompt export and FE report are:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/revisions/v6.2-pilot-20261106-r3/pilot_export/prompts_pilot_40.json`

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/reports/v6.2-pilot-20261106-r3`

Review URL:

`https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_spatial_composition_v6_2_pilot_20261106/gallery/viewer.html`

The next gate is human text review. A complete 16-bank/160-prompt export and image generation have not been started.

## Natural-placement judge V4

The clean V4 calibration candidate is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_ctech_20261106`

It is preserved as a failed research candidate and is not promoted over V3. Results:

- full 35-case development set: V4 16/35 versus V3 15/35;
- focused 10-case gate: V4 2/10 versus V3 4/10;
- five known failures in the focused gate were all passed;
- C-Tech-specific visual anchors still passed the first three known failures at 100;
- one high-effort Astra vision probe also missed a known missing-support defect.

The evidence indicates a perception failure for subtle furniture geometry and load paths. A future judge should add geometric measurements or segmentation and be evaluated as a new version on held-out human annotations. Further rubric-only iteration is not supported by the results.

## Reproduction checks

- V6.2 writer tests: 231 passed.
- Immutable evaluation-runner tests: 6 passed.
- V4 deterministic scoring tests: 9 passed.
- Published FE payload files match the local report byte-for-byte through S3.
- The Foundry gateway timed out from this Pluto host during HTTP verification; no HTTP success is claimed.
