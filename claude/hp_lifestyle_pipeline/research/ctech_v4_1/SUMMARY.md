# V4.1 C-Tech proximity pilot

## Image phase — 2026-10-27 (active)

USER-CONFIRMED: generate all120 reviewed pilot prompts using the newly corrected white-gallery renders. Four tags match uniquely; all inputs are2368×1776 RGB PNG and requests preserve4:3. Text/source/camera-tag fields remain unchanged; the offline density budgets are not retroactively retuned. No miniPC. The separate image manifest authorizes this phase; the October26 text-only status below is historical.

VERIFIED integration: all four smoke images completed. Input SHA/blob binding, frozen prompt=request=returned rawPrompt, seed42 and2368×1776 output dimensions matched for every view. Root visually inspected all four composites: expected devices and approximate close/wide framing are present, without a measured pixel-fidelity or user-quality claim. The remaining116 are now in the resumable eight-worker run. Initial continuing snapshot:4 completed,8 further submitted,108 waiting; no failures/ambiguous submissions. Publisher refreshes every120seconds and stops at120 terminal rows.

OBSERVED downstream changes: the laptop close-up gained a mug/notebook/pen and background fixtures despite requesting none; the printer close-up gained a succulent and room detail; the printer-wide rewrite introduced a credenza/cool grade. These additions appear in saved `usedPrompt` and output images; they are not mutations to the frozen pilot prompts. Evidence: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/smoke_review.json`.

Runner integrity improvements: HTTP5xx submissions are held as ambiguous instead of assumed safe retries; missing/mismatched returned rawPrompt becomes a durable integrity failure; smoke exit status uses the selected four rows while retaining116 unsubmitted rows for resume. Twelve offline regression tests passed. The client/gallery use identical corrected PNG bytes with per-upload hash binding.

Live gallery: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/generated_v4_1/gallery/index.html

Reproduction and resume: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/generation/README.md`.


As of 2026-10-26, Pacific. **The120-text review pilot is complete; image generation remains stopped.** The report compares the reviewed pilot against the same120 V4 cases and18 reference environment cores. This is a controlled text comparison, not a visual-quality evaluation.

## Contents

- [Decision and scope](#decision-and-scope)
- [Findings and contrary evidence](#findings-and-contrary-evidence)
- [Evidence and reproducibility](#evidence-and-reproducibility)
- [Next gate](#next-gate)

## Decision and scope

USER-CONFIRMED: preserve C-Tech's everyday settings, familiar objects, natural light and broad lived-in detail. Avoid invented administrative furniture names and recurring microscopic wear stories. Diversity can reduce source relevance, but not abandon C-Tech style. Keep all six environments, tag-only camera input, device exclusion and30 candidates per bank. Review a small pilot and its distribution before images.

The pilot uses one laptop source and one printer source, each on FrontRightCloseUp and FrontRightWide. It covers120 texts, not the full540. All inputs are production source-messaging JSON; smart briefs are excluded. The references consist of ten original October cores plus eight distinct additions. The18 chat occurrences are preserved, including repeated references, without treating repeats as independent reference types.

## Findings and contrary evidence

VERIFIED, this finite pilot: the latest simplified system produced four first-draw responses. All four banks failed automated checks (48 errors total), mostly camera inventories and reference/debug consistency. One bounded targeted GPT-5.5 correction per bank reduced automated errors to zero. Independent prose review still identified awkward phrasing and metadata inaccuracies; root made explicit scene edits to8/120 candidates and factual metadata corrections. All original outputs and before/after patches remain available. The published pilot is **reviewed output**, not an unedited model-success sample.

RESEARCHER INTERPRETATION: ordinary named places and reference-level detail are substantially clearer than the V4 examples supplied as negative feedback. The old policy of converting source operations into furniture names and using wear to imply activity was removed. The prompt now begins from the nearest C-Tech scene. Familiar crumbs, half-finished coffee and broad “subtle imperfections” remain allowed when present in reference style; arbitrary damage and backstories are not required.

VERIFIED text proximity: median nearest-reference cosine similarity is0.863561, compared with0.504219 for the same120 V4 cases (+0.359342). The same18 normalized reference cores and pinned MiniLM model are used on both corpora. The lexical feedback indicators affect41/120 V4 prompts for unnatural framing/place phrases and66/120 for microscopic wear/story markers; both are0/120 in the reviewed V4.1 pilot. These indicators are not a complete style judgment. There are no exact or canonical duplicate groups in this pilot.

VERIFIED distribution: Office31, Home24, Café19, Creative Studio17, Education16, Gaming13. Reference relationships after review:38 minimal camera edits,66 close adaptations,16 category extensions. These are annotations, not objective quality labels. Embedding/lexical comparisons in the report are independent descriptive metrics and do not imply image quality.

Contrary evidence / limits:

- The frozen system alone is not yet demonstrated to be production-reliable. A correction pass and editorial review were needed.
- A zero-prop laptop close-up cannot retain the C-Tech room inventories. Its candidates necessarily emphasize surfaces, ordinary settings and lighting, reducing visible diversity.
- Fixed wide-view budgets still delete some furniture and accessories from the full references. Whether the resulting amount of detail satisfies C-Tech requires user/image review.
- Education has no direct C-Tech reference. All16 Education texts are explicit category extensions, rather than falsely claimed verbatim examples.
- Source scores describe retained cues; an office with papers is broad support, not proof of a specific administrative workflow.
- The earlier elaborate prompt and repeatedly selected attempts are superseded, retained and excluded from current first-draw reporting.
- A runner integrity audit found one historical path/hash inconsistency. The cited response hash survives at another saved path; no missing response bytes were established. The current runner uses exclusive record allocation and immutable raw-response capture.

## Evidence and reproducibility

Confidence terminology: VERIFIED means directly checked local artifacts for the stated scope; USER-CONFIRMED describes Hooman's preferences; RESEARCHER INTERPRETATION is an assessment, not measured model quality. Downstream visual diversity and camera fidelity are UNVERIFIED for V4.1.

All durable artifacts reside in the real checkout under backed-up `/home/colligo/hs_scripts`. Scratch caches under `/mnt/localssd` are not the sole copies of prompts, source evidence or results.

| Evidence | Absolute path |
|---|---|
| Tested system and reproduction guide | `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v4.1/README.md` |
| Full original18 user examples | `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v4.1/user_reference_additions.txt` |
| Authoritative original October source | `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/example_prompts/HP - mAIstro Prompt Guidance (Oct 2026).docx` |
| Source/camera manifest | `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/manifest.json` |
| First-draw accounting | `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/run_accounting_prompt_986957bcc1a5_20261026.json` |
| Correction accounting | `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/repair_pass_01/accounting.json` |
| Final reviewed prompts and per-row edits | `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/pilot_prompts.json` |
| Explicit review limitations | `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/final_text_review.json` |

System SHA-256: `986957bcc1a5e218daea3594c037036b9d6d25af79847efbe0a95c849591fb04`. API: GPT-5.5 (`gpt-5.5-2026-04-24` returned), medium reasoning, strict schema,24000 max completion tokens. Replaying the deterministic finalizer+explicit editorial patches regenerates the review corpus without model calls. Fresh sampling is nondeterministic and must retain a new run identity.

## Next gate

Hooman reviews the distribution, full prompts and reference comparisons. Do not generate V4.1 images or silently expand to540 until that review determines the next step. V2/V3/V4 image runs and the cancelled eval-hub upload remain stopped. Publication verified:13 S3 objects match local SHA-256, content types and exact allowlist. Local browser checks passed with zero JavaScript/request errors; IMS was mocked only in the local browser test, not in published files.

Review: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1/gallery/index.html

Prompts text: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1/downloads/pilot_prompts.txt

Full prompt JSON: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1/downloads/pilot_prompts.json

System prompt: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1/downloads/system_prompt.md

Publication record: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1/publication.json`.
