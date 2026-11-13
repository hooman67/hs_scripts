# HP Lifestyle Prompt × Digital Twin Eval v1

This eval set pairs every generated source-messaging prompt with every available digital twin in the same device category.

- Laptop: 6 prompts × 24 twins = 144 rows
- Printer: 8 prompts × 6 twins = 48 rows
- Total: 14 prompts, 30 used twins, 192 rows

The 12 desktop and monitor twins remain in the source digital-twin manifest but are excluded because the current production prompt set has no desktop or monitor source product.

## Build

```bash
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/build_eval_set.py
```

The build writes `gallery/data.js` and `manifest.json`. Digital-twin image binaries stay outside Git and are published to the eval set's S3 `assets/digital_twins/` prefix.

## S3 destination

```text
s3://foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/
```

The HTML gallery follows the Foundry HTML gateway pattern and uses IMS authentication plus relative image paths.
