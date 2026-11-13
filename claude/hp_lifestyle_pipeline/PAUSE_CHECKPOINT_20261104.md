# Pause checkpoint — V6.1 frozen before judge work

Date: 2026-11-04

## Current decision

V6.1 prompt-writer work is paused temporarily while the project detours into building a judge for generated images. The judge is a separate evaluation component, not V6.2 and not a modification of the frozen V6.1 writer.

Do not change the accepted V6.1 prompt set, runtime, catalogue, scores, or published report while developing the judge. When prompt-writer work resumes, continue from the frozen V6.1 state described below.

## Frozen V6.1 state

- Contract: Smart Brief + source messaging + camera tag produce ten source-ranked prompts.
- Coverage: four devices × four views × ten prompts = 160 unique prompts in 16 banks.
- Accepted revision: `v6.1-expanded-20261103-r6`.
- Prompt export SHA-256: `adcb9edb2643e45acb0cb882cdc4d65b8c256a52d58ad4a44ddd9c235287b3cd`.
- Runtime catalogue: 261 approved entries and 158 visual families.
- Final set: 130 approved prop IDs, 473 assignments, and 100 visual families.
- Validation: 229 offline tests pass; all 16 accepted banks revalidate through the frozen runtime.
- Provenance: five banks passed the initial GPT-5.5 response and eleven passed one bounded automatic repair. No scene text or creative field was manually edited.
- C-Tech constraints enforced: no repeated registered visual or semantic phrase family within a bank; selected shelves and pegboards are populated; printers use appropriate equipment-scale tables/worktables rather than occupied desks or personal workstations.
- No V6.1 images or downstream Gemini rewrites have been generated.

## Published artifacts

- Prompt JSON: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/data/prompts_all_160.json
- Distribution and all-160 prop audit: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_v6_1_distribution_prop_audit_20261103/gallery/index.html

## Canonical local artifacts

- Runtime: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_1`
- Approved props: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/approved_props_v6_1/PROPS_FOR_REVIEW.md`
- Evaluation workflow: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103`
- Accepted export: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/revisions/v6.1-expanded-20261103-r6/exports/final/prompts_all_160.json`
- Report workflow: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_1_distribution_prop_audit_20261103`

## Resume instructions

1. Read this checkpoint and the first checkpoint in `PROJECT_STATE.md`.
2. Verify the accepted export hash before using it.
3. Treat V6.1 as frozen. Create a new evaluated revision for any prompt, catalogue, camera, validation, or reference change.
4. The next V6.1 project action is image generation only after Hooman explicitly requests it.
5. Preserve the V6.1 prompt-to-source, camera-tag, device, score, prop-ID, and validation metadata because the judge may later consume these as evaluation context.

## Temporary judge detour

The next project activity is to design a judge that evaluates generated images across multiple dimensions. Its rubric, inputs, output schema, model, calibration set, and acceptance thresholds have not yet been decided. Store judge work separately from the writer versions so experiments cannot mutate the frozen V6.1 artifacts. No judge implementation has started at this checkpoint.
