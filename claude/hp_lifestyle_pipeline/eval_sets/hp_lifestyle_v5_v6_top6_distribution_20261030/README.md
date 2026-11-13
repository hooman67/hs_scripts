# V5–V6 comparison and V6 prop audit

This report compares the frozen, source-ranked top six prompts from each of the same 16 device/camera banks in V5 and V6. It uses the frozen 18-reference C-Tech library and MiniLM revision from the established V4.1/V5 reports.

The published HTML separates this content into two tabs:

1. the like-for-like V5 versus V6 top-96 comparison; and
2. the V6 prop audit, which covers all 160 frozen V6 prompts upstream and the generated/re-written 96-row subset downstream.

The prop audit keeps three evidence layers separate:

1. exact approved prop IDs and input prose across all 160 V6 prompts;
2. exact entity labels emitted by the downstream Gemini 3.1 Pro rewrite for the 96 generated previews; and
3. approximate visual-image prevalence supplied in C-Tech feedback for those 96 previews.

The first two are reproducible text/debug counts. They are not computer-vision detections and do not prove that an object appears in the generated pixels. The compact, durable 96-row source snapshot is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v5_v6_top6_distribution_20261030/inputs/v6_preview_prop_records.json`

The manual row-level trace of objects explicitly introduced by the downstream rewrite is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v5_v6_top6_distribution_20261030/DOWNSTREAM_PROP_ADDITIONS_AUDIT.md`

Its complete machine-readable evidence, including original prompts, rewritten fields, assembled `usedPrompt` values, and generated-image URLs, is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v5_v6_top6_distribution_20261030/downstream_prop_additions_audit.json`

The corrected paper-stack audit counts 13 explicit V6 input prompts and 14 downstream rewrites among the 96 previews. The rewrite-only case is `cashmere__laptop_FrontCloseUp::p3`. The previous displayed zero came from a pattern that matched only the exact wording “stack of papers” and missed phrases such as “stack of plain papers.”

Build and validate:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
python eval_sets/hp_lifestyle_v5_v6_top6_distribution_20261030/build_analysis.py
python eval_sets/hp_lifestyle_v5_v6_top6_distribution_20261030/validate_analysis.py
```

The canonical V4.1 set contains 120 prompts from four 30-prompt banks. No arbitrary 96-row V4.1 subset is created; the report links to its existing canonical distribution instead.
