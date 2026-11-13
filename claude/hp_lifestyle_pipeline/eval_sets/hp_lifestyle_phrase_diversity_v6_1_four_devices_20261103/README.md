# V6.1 four-device, four-view text evaluation

This evaluation exercises the V6.1 writer on Cashmere and EliteBook laptops plus Tassel and Magic printers. Each device uses four fixed camera tags and each bank returns ten source-ranked prompts: 4 devices × 4 views × 10 prompts = 160 prompts.

## Accepted result

Final runtime snapshot:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/revisions/v6.1-expanded-20261103-r6`

Accepted export:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/revisions/v6.1-expanded-20261103-r6/exports/final/prompts_all_160.json`

SHA-256: `adcb9edb2643e45acb0cb882cdc4d65b8c256a52d58ad4a44ddd9c235287b3cd`

The export contains 160 unique texts in 16 complete banks. Environment counts are Office 51, Home 35, Creative Studio 31, Education 24, Café 11, and Gaming 8. Source relevance ranges from 0–95 with mean 46.12; declared C-Tech score ranges from 60–86 with mean 73.08.

All banks pass the final r6 runtime. Five passed the initial model call and eleven passed after the single allowed complete-bank repair. The accepted sources total 27 semantic/transport calls, all returned `gpt-5.5-2026-04-24`. No scene text or creative field was manually edited; deterministic evidence normalization removed three invalid citations and records each change.

R4 accepted 15 banks but exposed a validator recognition defect for “substantial office side table.” A later independent audit found unresolved `or` choices in three banks. The final r6 system requires one concrete visible variant, preserves safety exclusions such as “without text or faces,” and accepts the natural side-table phrase. The three affected banks were rerun through the normal bounded-repair path. `composite_source_map.json` records the 13 r4 and three r6 sources, and `assemble_validated_composite.py` revalidates all sixteen through the frozen r6 runtime before export.

## Commands

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
PYTHONDONTWRITEBYTECODE=1 python -m pytest \
  research/source_messaging_v1_to_v6/versions/v6_1/tests \
  eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/test_run_eval.py -q

PYTHONDONTWRITEBYTECODE=1 python \
  eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/run_eval.py verify \
  --revision v6.1-expanded-20261103-r6
```

The `revisions/` directory is durable evidence under backed-up `/home/colligo` but is excluded from Git because it contains complete source documents, raw model responses, and redundant frozen runtime copies. The final JSON and distribution report are also published to Foundry S3 with recorded SHA-256 hashes.

No V6.1 images have been generated. The distribution/prop audit therefore covers upstream prompt text and declared props only; downstream Gemini rewrite and output-pixel audits begin after image generation.

Published prompt JSON:

`https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/data/prompts_all_160.json`

Published distribution and declared-prop audit:

`https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_v6_1_distribution_prop_audit_20261103/gallery/index.html`
