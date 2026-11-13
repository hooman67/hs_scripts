# V6.1 GPT Image 2.5 scene generation

This run sends the frozen V6.1 160-prompt export to the image-only HP endpoint
at `POST /api/generate`. It does not invoke IBL, backplate, recomposite, or
relight stages.

The queue uses a Latin-square device/view interleave. Each four-task wave
contains Cashmere, EliteBook, Tassel, and Magic, with view positions rotated
between devices. This gives the live gallery broad product and view coverage
before the complete run finishes.

The runner validates the frozen prompt hash, 16 ten-prompt banks, live twin and
camera mappings, endpoint generator identity, output dimensions, and skipped
downstream stages. Submissions are checkpointed before polling, so restarting
the same command resumes saved jobs without blind resubmission.

Source prompts:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/revisions/v6.1-expanded-20261103-r6/exports/final/prompts_all_160.json`

Live gallery:

https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_phrase_diversity_v6_1_gpt_image2_scene_20261105/gallery/index.html

Run or resume after refreshing and sourcing Foundry AWS credentials:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
source /home/colligo/.claude/hshariati/aws_creds.env
uv run --script \
  /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/generation_gpt_image2_scene_v1/run_generation.py \
  --workers 4
```

Runtime records and image bytes live in the ignored `run/` directory. Review
artifacts are uploaded incrementally under:

`s3://foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_phrase_diversity_v6_1_gpt_image2_scene_20261105/`
