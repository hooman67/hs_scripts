# HP lifestyle writer V4.1 — C-Tech reference proximity

As of 2026-10-26. **Text pilot ready for Hooman's review; no V4.1 image generation authorized.** V1 remains the selected baseline. V2, V3 and V4 runtime artifacts are preserved.

## What changed

V4.1 starts with a successful C-Tech scene and makes the smallest camera-compatible adaptation. It retains familiar rooms, furniture, props and natural light. Source messaging may choose ordinary visible details; it must not create invented places such as a “policy deployment counter,” or turn “lived-in” into elaborate wear, stains, scratches and document-routing stories. Diversity may depart from source messaging but must retain this writing style.

The reference library contains **18 distinct normalized environment cores**: the original ten October examples and eight unique additions from Hooman. All 18 occurrences supplied in chat are preserved separately, including repeats. Normalization removes target-device mentions, no-hardware clauses and blue-control clauses under the previously approved writer boundary. Minimal blue in the references is not a new color-control feature.

Priority: fixed camera/device rules, then C-Tech style and detail, then natural source cues, then diversity within that style. The six environments are Home, Office, Education, Gaming, Café and Creative Studio. Education has no direct C-Tech example and remains a labeled category extension.

## Runtime contract and exact tested artifacts

Input: JSON with `source_messaging` and `camera_tag` (`ProductType_CameraName`). No product names, smart briefs or runtime image analysis. Output: 30 prompt candidates plus source evidence, KSP mappings, camera metadata, and reference/source explanations. Ranking is descending C-Tech reference score, then source-relevance score; both are rubric annotations, not calibrated probabilities.

System prompt:
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v4.1/system_prompt.md`

SHA-256: `986957bcc1a5e218daea3594c037036b9d6d25af79847efbe0a95c849591fb04`.

Schema:
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v4.1/output.schema.json`

SHA-256: `03dba20d426fe151a0723a176858092101f4b0d05cd48fafcc9b4f7975d38a11`.

The version directory also contains the template, reference library, original supplied examples, pinned camera profiles, compiler and deterministic finalizer. The finalizer corrects evidence-path/arithmetic/registry metadata where mechanically verifiable and reranks the bank; it does not edit scene text.

Tested API settings: deployment `gpt-5.5`, returned model `gpt-5.5-2026-04-24`, medium reasoning, strict JSON Schema response, `max_completion_tokens=24000`, no explicit temperature, at most two concurrent calls. Transient transport errors use bounded retry/backoff (maximum100); semantic failure does not trigger indefinite retries.

## Pilot result and limits

Two production sources × close/wide = four banks /120 prompts. This is deliberately smaller than the full nine-source540-text evaluation.

| Stage | Result |
|---|---|
| First draw under the frozen prompt | Four model responses; all four banks had validation errors (48 total) |
| One bounded targeted GPT-5.5 correction per bank | Four responses, no transport retries; all four banks passed automated checks |
| Reviewed publication | Small editorial scene edits to8/120 candidates, plus explicit metadata corrections; all120 pass checks |

**This is a reviewed pilot, not evidence of single-call reliability.** Before/after edits and raw responses are retained. The root prose edits remove awkward noun stacking or workflow qualifiers without adding objects. Metadata edits correct reference relationships, claimed lighting and literal inventories. Earlier prompt revisions and repeated sampling attempts are retained as superseded experiments and are not mixed into the reported first-draw sample.

The fixed laptop close-up allows zero props/background objects; printer close-up allows one prop and zero background objects. Both wide presets allow three local props and two background fixtures. A shelf explicitly holding its ordinary contents counts as one background fixture. Independent objects remain separately counted. Numeric camera limits were not changed to improve acceptance.

## Review and reproduction

Canonical summary:
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/ctech_v4_1/SUMMARY.md`

Pilot inputs, outputs, model records, patch logs and report source:
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026`

Prompt download:
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/pilot_prompts.json`

Compile verification and deterministic replay of the reviewed export (no API calls):

```bash
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v4.1/scripts/build_system_prompt.py --check
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/integrate_reviewed_pilot.py
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/export_prompts.py
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1/build_analysis.py
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1/validate_analysis.py
```

The report needs the cached pinned `sentence-transformers/all-MiniLM-L6-v2` model, NumPy, PyTorch, transformers and scikit-learn. Its source manifest records their versions and input hashes. Run browser validation with `uv run --with playwright python` and the report's `browser_validate.py`. The publisher is intentionally one-shot and refuses existing publication state or a nonempty S3 destination.

For a fresh model experiment, use a new eval directory/manifest rather than overwriting these records. `run_gpt55.py --all-authorized` is the first-draw runner; `run_repair.py` preserves one targeted correction response per bank and refuses to reuse its pass directory. Exact correction requests are saved under `repair_pass_01/<case_id>/request.json`. Do not run the original first-draw `--rebuild-only` over the final reviewed map: it deliberately reflects first-draw rejection, not editorial review.

Full540 texts or images require the next user review decision. No image-quality or downstream camera-preservation claim follows from text similarity.

Published review: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1/gallery/index.html

System prompt permalink: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1/downloads/system_prompt.md
