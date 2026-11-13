# HP lifestyle prompt writer V6.2 text evaluation

This evaluation freezes the V6.2 runtime, approved catalogue, and the same 16 device/view inputs used for V6.1. It supports a bounded four-bank pilot followed by the complete 16-bank, 160-prompt text evaluation. It does not authorize image generation.

The runner copies every runtime and input byte into an immutable revision, records pre-call and post-call journals, permits only GPT-5.5, limits concurrency to two, and allows the writer's one initial call plus at most one semantic repair per bank. A complete export contains all 160 prompts and the source-ranked top 96.

Runtime source:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_2`

Runner:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/run_eval.py`

Offline verification:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
PYTHONDONTWRITEBYTECODE=1 python -m pytest \
  eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/test_run_eval.py -q
```

No revision is considered frozen until all selected banks succeed without manual prose edits and the snapshot verifier passes.

## Frozen R3 text pilot

The four-bank R3 pilot passed the snapshot verifier and contains 40 prompts without manual prose edits:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/revisions/v6.2-pilot-20261106-r3`

The FE review payload is built reproducibly by:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/build_pilot_report.py`

Its durable local output is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/reports/v6.2-pilot-20261106-r3`

Published review:

`https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_spatial_composition_v6_2_pilot_20261106/gallery/viewer.html`

Published prompt JSON:

`https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_spatial_composition_v6_2_pilot_20261106/gallery/prompts_pilot_40.json`

All four uploaded report files checked byte-for-byte against their local sources through S3. The Foundry gateway itself timed out from the Pluto host during publication verification on 2026-11-06; this is recorded rather than treated as an HTTP verification success.

## Frozen 160-prompt replay and V3 placement-judge report

Hooman subsequently authorized the complete V6.2 image replay. The frozen prompt export is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/revisions/v6.2-full160-20261107-r5-validated-composite/exports/final/prompts_all_160.json`

The replay used the same 8016 scene-only endpoint contract, four digital twins, sixteen device/view banks, and Latin-square queue ordering as the V6.1 comparison. All 160 endpoint records completed successfully and passed image hash, 2368×1776 dimension, prompt identity, and `generationMode=sceneOnly` checks. The complete local run is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/generation_gpt_image2_scene_v1/run`

The exact V3 consensus-v2 placement judge produced 160 complete results with five disputed component checks: two confirmed by both verification passes and three rejected. The requested grouped FE report contains sixteen source-input groups with ten prompts per group:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3/fe_reports/v6_2_consensus_v2_grouped_20261107`

Intended publication URL:

`https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp_natural_placement_judge_v3_v6_2_20261107/consensus_v2/grouped_by_source_input/viewer.html?ldap=hshariati`

As of 2026-11-07, local generation, judging, report construction, and publication planning are complete. Publication is pending because the Foundry AWS credential broker hosts time out from this Pluto machine and the prior temporary AWS credentials have expired.
