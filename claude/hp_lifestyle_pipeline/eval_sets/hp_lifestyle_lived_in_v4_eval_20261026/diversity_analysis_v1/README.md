# V4 prompt distribution and reference-proximity analysis

This isolated report measures exact categorical distributions, source-relevance scores, lexical
repetition, semantic proximity within the final accepted 540-prompt V4 corpus, and proximity to
the ten sample prompts in the authoritative October C-Tech DOCX. It does not use generated images
and does not claim visual diversity or image quality.

## Frozen inputs

- Prompt export: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/generation_prompts.json`.
- Accepted map: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/accepted_prompt_cases.json`, SHA-256 `d247ca2bbae1f1a0ad460476c1277cb42e12b26d2ec0ea0fd16da0a03802fcd8`.
- Approved selection: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/selection_manifest.json`, SHA-256 `2c9f23f5fc6bed0d802198b1a793e3099761e69d156e63846deed2b43cf87f1e`.
- Durable V4 lexical audit: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/lived_in_v4/data/v4_generation_prompt_stats.json`. Its input record is byte- and SHA-bound to the V4 prompt export (`ae881cccb9eecb434b500dac2314401a6de921298cc7b7084267e8fbe01f7c6b`, 929990 bytes). Its internal `v3-generation-prompt-stats-v1` version string names the shared mechanical formula implementation; the input path, export version, date, bytes and SHA identify this artifact as the V4 run.
- Raw October reference extraction: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/diversity_aware/data/october_guidance_raw_extraction.json`.

The builder refuses prompt exports that are not bound to the current accepted and selection
hashes. It requires exactly 540 unique candidates and the exact native V4 environment set: Home,
Office, Education, Gaming, Café and Creative Studio. `display_environment` remains in the JSON and
CSV only as a compatibility alias for the established V3 gallery code; it equals the native
`environment` value on every row and no taxonomy remapping occurs.

## Methodology

Exact distributions and relevance histograms are direct counts over exported fields. The lexical
audit applies the established mechanical formulas to the V4 prompt export: normalized text
duplicates, word-bigram and character-trigram Jaccard proximity, and recurring 3–6-word phrase
document frequency.

Semantic similarity uses the locally cached `sentence-transformers/all-MiniLM-L6-v2` model at
frozen revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, attention-mask mean pooling, L2
normalization and cosine similarity. The build runs with `TRANSFORMERS_OFFLINE=1`; it makes no
remote model, text-generation, image-generation or publication call. PCA is a descriptive 2-D
projection of the 540 prompt and ten scope-adjusted reference embeddings.

The ten references are paragraphs 6, 7, 8, 10, 11, 12, 14, 15, 17 and 18. The primary comparison
removes the device prefix, blue-control clauses and explicit no-hardware clauses because those are
outside the V4 environment-writer contract. Original reference text and full-reference similarity
remain in the analysis output. Education and Gaming have no matching October reference; proximity
has no calibrated pass threshold and does not measure visual quality.

## Local build

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
TRANSFORMERS_OFFLINE=1 python3 /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/diversity_analysis_v1/build_analysis.py
```

Output:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/reports/hp_lifestyle_lived_in_v4_eval_20261026/diversity_analysis_v1`

The one-shot publisher targets only the isolated sibling prefix:

`s3://foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/diversity_analysis_v1/`

It refuses a nonempty prefix and is not run by the build.

## Published report

Gallery:

https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/diversity_analysis_v1/gallery/index.html

The one-shot publisher was run on 2026-10-26 after confirming the target prefix was empty. It uploaded exactly ten allowlisted objects and verified each by GET SHA-256 plus HEAD size, content type and SHA metadata. The final remote key list matched the allowlist. Publication evidence is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/diversity_analysis_v1/publication.json`. The `local_validation.json` record validates the frozen local artifacts and, when the publication record exists, its exact allowlist, hashes and isolation evidence without making another publication call.
