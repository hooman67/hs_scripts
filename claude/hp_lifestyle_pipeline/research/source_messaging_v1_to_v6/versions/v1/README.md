# HP lifestyle source-messaging rewriter v1

This directory freezes the first product release of the source-messaging-to-environment-prompt rewriter. The files here are immutable release inputs; the unversioned files at `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/system_prompt.md` and `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/output.schema.json` remain compatibility copies.

## Frozen contract

- System prompt: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v1/system_prompt.md`
- Strict JSON schema: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v1/output.schema.json`
- Release metadata and checksums: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v1/release.json`
- Git tag: `hp-lifestyle-rewriter-v1`

The runtime user message is one complete source-messaging JSON object. The response is strict JSON with one or more environment prompts plus traceability/debug data. Smart briefs are excluded. Prompt text may contain people, activities, ordinary props, and any of the Home, Office, Education, or Gaming environment families. It omits the target device, including generic laptop, printer, computer, monitor, device, and hardware wording.

## Text reproduction

The release was tested with deployment `gpt-5.5`, medium reasoning, `max_completion_tokens=8000`, no explicit temperature, and strict structured output. The returned model was `gpt-5.5-2026-04-24` during the recorded runs.

```bash
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/scripts/run_gpt55.py \
  --system /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v1/system_prompt.md \
  --schema /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v1/output.schema.json \
  --manifest /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/data/source_manifest.json \
  --output-dir /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/runs/reproduced_v1_production
```

The accepted release candidate is preserved in `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/runs/v2_production` and `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/runs/v2_edges`. Those directory names refer to the second internal prompt candidate; the product release name is v1. The combined accepted validation is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/runs/v2_validation.json`.

## Image-eval reproduction

The first image eval paired all prompts with every available digital twin in the same workbook category: 6 laptop prompts × 24 laptop twins plus 8 printer prompts × 6 printer twins, producing 192 rows. The versioned prompt output, source messaging, matching rules, endpoint runner, gallery builder, and FE-input builder are retained in the repository. Generated pixels and sanitized endpoint results remain outside Git under `/mnt/localssd/hp_lifestyle_pipeline/generation_runs/hp_lifestyle_prompt_digital_twin_eval_v1_generated_v1` and in the Foundry S3 report locations documented in `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/README.md`.

The image request used 2368×1776, `n=1`, prompt rewrite enabled, `gemini-3.1-pro`, and 50 inference steps. All 192 rows completed. This establishes reproducibility and mechanical completion; visual quality remains subject to Hooman's review.
