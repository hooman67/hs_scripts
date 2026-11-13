# V3 prompt diversity analysis

This report measures categorical breadth, lexical repetition, semantic similarity within the 540-prompt V3 corpus, and proximity to the ten sample prompts in the authoritative October C-Tech DOCX. It does not use generated images and does not claim visual diversity.

## Sources

- V3 prompts: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/generation_prompts.json`, SHA-256 `3db71a433357edcc2fd0ef0804c9584355ff3e13d6eff98afc983f57a7138cc1`.
- Authoritative DOCX: `/mnt/localssd/HP_scenes/input_output_hp_rewriter/example_prompts/HP - mAIstro Prompt Guidance (Oct 2026).docx`, SHA-256 `1f1605f034f581e03679d101fddd9cd52f00601b75ba2a9ec64783206fb78293`.
- Durable identical DOCX: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/example_prompts/HP - mAIstro Prompt Guidance (Oct 2026).docx`, same SHA-256.
- Raw extraction: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/diversity_aware/data/october_guidance_raw_extraction.json`.
- Mechanical lexical audit: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/diversity_aware/data/v3_generation_prompt_stats.json`.
- Accepted display-environment taxonomy audit: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/diversity_aware/data/v3_display_environment_taxonomy_audit.json`. It is bound to the exact 540-row prompt export SHA-256 and candidate-key set.

The ten comparison prompts are DOCX paragraphs 6, 7, 8, 10, 11, 12, 14, 15, 17 and 18. Headings, the reusable template and the blue-control instruction are not treated as sample prompts.

## Comparison contract

The primary C-Tech comparison is scope-adjusted. It removes the `Laptop:`/`Printer:` prefix, trailing blue-control clauses, and explicit no-hardware clauses because those are intentionally outside the approved V3 contract. The report also preserves original text and a device-prefix-normalized full-reference semantic score.

Semantic similarity uses `sentence-transformers/all-MiniLM-L6-v2` at frozen revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, attention-mask mean pooling and cosine similarity. Lexical similarity uses TF-IDF word unigrams and bigrams. The map is PCA over all 540 prompt embeddings plus ten adjusted reference embeddings. These are descriptive metrics without a calibrated pass threshold.

The primary distribution uses six deterministic display categories: Office, Café, Creative Studio, Home, Education and Gaming. The taxonomy preserves the model-authored canonical `environment` on every row. Non-Office families remain unchanged; only canonical Office rows with an explicit café setting or explicit physical creative-studio setting are relabeled for display. `display_environment` and `display_environment_rule` are included in the analysis JSON, map points and 540-row CSV. Canonical family counts and canonical-family grouped similarity remain in the JSON as provenance. The rendered report copies the accepted audit verbatim to `downloads/display_environment_taxonomy.json` and exposes it in the download navigation.

## Reproduce

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/diversity_aware/data/scripts/audit_generation_prompt_diversity.py
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/diversity_analysis/build_analysis.py
```

An independent rebuild produced byte-identical analysis JSON, CSV, reference JSON and gallery files. The build refuses a taxonomy whose recorded prompt SHA, byte count, 540 candidate keys or candidate identity fields differ from the frozen prompt export. The Hugging Face cache may live in volatile `/mnt/localssd`; the model ID and exact revision are durable, so the cache is reproducible.

## Outputs

Rendered local report:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/reports/hp_lifestyle_diversity_v3_eval_20261023/diversity_analysis_v1`

Published report:

https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/diversity_analysis_v1/gallery/index.html

The display-taxonomy revision was published in place on2026-10-24 UTC after every existing remote object matched either its recorded prior SHA-256 or the exact target SHA-256. All ten final objects were GET/HEAD verified and the final key list matched the explicit allowlist. Publication evidence is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/diversity_analysis/publication.json`; the prior record is retained in `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/diversity_analysis/publication_history.jsonl`. The update touched only the sibling `diversity_analysis_v1` prefix, not the active `generated_v3` image gallery. JavaScript passes V8 compile-only validation. No authenticated browser rendering was performed.

## Important limits

- The ten October references cover Office, Home, Coffee Shop and Creative Studio, with no Education or Gaming examples.
- Close-up V3 prompts deliberately describe a local surface/light region; October references are usually longer room-level scenes.
- Textual uniqueness and embedding spread do not establish visible image diversity. Use the bounded 108-image eval for that conclusion.
- Display environment is a conservative lexical presentation taxonomy, not a semantic classifier or a replacement for the canonical environment field.
