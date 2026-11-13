# HP source messaging → lifestyle prompts

Research charter, 2026-10-13. Owner: Hooman Shariati.

Create and test a self-contained GPT-5.5 system prompt that receives one production source-messaging JSON object and returns structured JSON containing at least one lifestyle environment prompt plus a debug section with KSP mappings and concise explanations. These environment prompts feed a downstream rewriter together with a digital-twin render; this project does not generate the final image-model prompt.

## Confirmed scope

- Six V4/V4.1/V5 environments: Home, Office, Education, Gaming, Café, Creative Studio. Historical project scope was nine SKUs.
- V5 uses smart brief and source messaging together; this supersedes the source-only boundary for V5. Earlier versions remain unchanged.
- Prioritize the October 2026 mAIstro guidance, then compatible supplied prompt examples. Read only column A of the lifestyle-photography workbook.
- Match the examples' style and compatible scene descriptions, not their empirical scene frequencies.
- People, activities, and ordinary props are allowed. Omit the target device, including generic laptop/printer references, from prompt text. Do not automatically add no-device clauses. Cafés and creative studios remain canonical Office subsettings in the frozen writer, while V3 result galleries expose them as separate display categories (approved 2026-10-23).
- Invent plausible scene details when source messaging is weak. Do not fabricate evidence or product claims.
- V1/V2: at least one output; additional outputs require useful KSPs. V3 supersedes this cap with30 ranked candidates per source/tag, fixed0–100 relevance and labeled creative departures.
- Product v1 is frozen and selected. Current v2 accepts source messaging and a fixed ProductType_CameraName tag, e.g. miniPC_FrontRightMedium. There are no product-name inputs or runtime images. Offline notes adapt scene density and elevation compatibility to the type-camera pair. Color control is outside this revision.
- Test all distinct supplied source examples on actual GPT-5.5. Initial acceptance is text review; Hooman handles subsequent image evaluation.

## Method and boundaries

Follow `/home/colligo/.codex/RESEARCH_RULES.md`. Inspect current local sources, preserve provenance and checksums, deduplicate exact content, record contradictions, and distinguish VERIFIED evidence from ASSUMED interpretation and USER-CONFIRMED decisions. Keep credentials out of artifacts. GPT calls through the approved Foundry helper are authorized. Review HTML follows Hooman’s standing instruction to publish to the appropriate Foundry S3 bucket; no external messages are part of this workflow. Hooman subsequently authorized the current-camera image evaluation while text review proceeds.

## Current version

V6 is the accepted integration handoff. It receives Smart Brief + source messaging + camera tag and returns ten source-ranked prompts with separate C-Tech scores. Its frozen application contract includes 237 approved props, 122 qualitative camera profiles, 18 C-Tech references, strict schema validation, application-owned scoring/sorting, and one bounded complete-bank repair. The accepted text evaluation has 16 actual GPT-5.5 banks and 160 prompts; the top-six preview evaluation generated 96/96 images with corrected product/view renders. Runtime and reproduction: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6/README.md`. Integration handoff: `/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/hp_image/prompt_rewrite/source_message_to_user_prompt/v6`.

V1–V5 remain frozen historical versions. Their descriptions below document the progression and do not override V6.

The current isolated writer-development candidate is a **replacement V6.5 grounded in actual HP training photographs, minus people**. Its160 actual prompts and160 matched PR4523 images are complete and published for human review:30 reused images plus130 new, organized into16 groups of10 alongside V6.4. V6.5 is also the fourth experiment in the existing grouped, full160 detailed and clean FE comparisons; original columns/cards/annotation IDs are preserved. The separate30-image report retains48 actual training references and the original30 C-Tech comments. Actual Astra/medium authored the complete design; the680-entry catalogue allows realistic reuse of familiar props while retaining no-people/no-extra-electronics constraints and the structured-source API/mappings/scoring. Native text0/16 and bounded-recovery14/2 remain explicit alongside the final recognition-only completion. The expansion's native primary pass was128 successful/2 failed; two preserved pre-image failures were operationally replaced unchanged, with no successful-image resampling. All160 final native input/output bindings pass,1011 published objects were fully read back, and the owned endpoint was stopped. The previously published richer-prop V6.5 remains explicitly user-rejected. No visual acceptance, live-SSO certification or promotion is implied. Scope, raw provenance and review links: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_5/SUMMARY.md`.

V6.4 is the completed structured-source compatibility baseline on the unchanged V6.3 scene/prop/scoring contract. Its160 distinct actual GPT-5.5 texts are complete:40 per device across the same sixteen camera banks, with source pairs assigned by device category and relative printer size. Its full160 exact Adobe-Firefly/foundry#4523 image study is also complete:30 reused images plus130 new, with no failures or replacements. V6.4 is the third column of both existing full160 V6.3 reports, preserving the original columns and annotation IDs. The separate matched30 study remains published as `V6.4 / PR 4523 - V15.7 shapes`, with clean image-only and source-prompt FE variants; its five-column V6.2/V6.3/V6.4 comparison is unchanged by the expansion. All studies use the original device/camera/bank-rank slots and normal native reference selection. Links, audit evidence and the host's live-gateway access limitation are indexed in the V6.4 summary. V6.3 remains frozen, with HP product/environment associations, six newly approved prop entries and no paperweights or loose decorative stones. Its160 actual texts and matched30-row subsets are complete; the smaller comparison preserves120 V6.2/V6.3 outputs on exact Adobe-Firefly/foundry#4417 and Adobe-Firefly/foundry#4523, adds30 V6.4/PR4523 outputs, and retains30 explicitly historical references. Actual model-input images and source/debug provenance remain in the detailed galleries. The separate historical V3.1 judge candidate is **not promoted**: its bounded calibration still misses required alignment and geometry failures. No production deployment or image-quality acceptance is implied; V6 remains the accepted integration handoff.

The same160 training-grounded V6.5 texts also have160 new native2368x1776 outputs on exact Adobe-Firefly/foundry#4619 commit `db074bd9ab8f832712aa45415435dfa647e51ced` (V15.8, statistics plus strong lighting). Six explicitly labeled no-statistics cases retain lighting. The requested grouped report now has three experiments; the supplied five-column FE now has six, preserving original images/review IDs. Separate two-column and paired groups-of-ten V6.4/V6.5 V15.8 reports are published. All622 new/updated/backup objects were fully read back;168 native attempts (152/8 primary, eight unchanged successful recoveries),816 Astra responses and160 image edits remain auditable. This is comparison availability, not image-quality acceptance or promotion.

## File map

- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_5_training_full160_pr4619_20261112/report_links.txt`: all four published V15.8 comparison URLs; adjacent execution manifest and completion receipt bind exact native settings,160 raw outputs,622-object publication, preserved reviews and all failed attempts.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_4_fourway_v6_5_five_columns_20261112/report_links.txt`: original five-column creation receipt, preserving four supplied V6.4 experiments and adding training-grounded V6.5; that viewer is now extended to six columns by the V15.8 study above. The original four-column source remains untouched.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_4_astra_vs_gpt55_20261111/SUMMARY.md`: completed actual-Astra/high/32000 versus frozen GPT-5.5 comparison,160 Astra prompts/160 Astra images and320 total images. The80 missing prompts/81 images were recovered without changing original successes or validation policy; original80/79 outcome and all attempts remain preserved. Safe gallery switch,336-object read-back, actual320-image browser proof and service cleanup are under `recovery/complete160`.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_5/SUMMARY.md`: actual Astra/medium analysis of48 training examples and30 C-Tech reviews,680-entry replacement, explicit native/recovery accounting,160 texts/160 images and four-view publication/cleanup evidence; rejected predecessor preserved separately.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_5_training_full160_pr4523_20261112/report_links.txt`: current V6.4/V6.5 groups-of-ten gallery, extended four-experiment grouped/detailed/FE views and160 prompt downloads; adjacent completion receipt binds the full1011-object publication and owned-service cleanup.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_5_training_pr4523_30_20261111/report_links.txt`: preserved30-image training-grounded V6.4/replacement-V6.5 comparison,48 training references, original C-Tech comments and160 prompt downloads.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_5_pr4523_30_20261111/report_links.txt`: historical user-rejected richer-prop V6.5 comparison/download URLs, not the current replacement.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_grouped_diversity_20261111`: original diversity-review gallery, now extended to four ten-image experiments per input bank by the isolated V6.5 full160 study; all original three-experiment cards and source contexts are preserved.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_4/SUMMARY.md`: new JSON document comparison, approved compatibility implementation, size/context pair assignments,160 texts and completed30/full160 PR4523 images; V6.3 unchanged.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_4_full160_pr4523_20261110`: frozen30/130 partition, complete160-output native audit, third-column extensions to both full160 reports, all copyable links and final publication/cleanup receipts.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_4_pr4523_30_20261110`: frozen rank-matched30 selection, isolated exact-PR4523 generation, both report formats, copyable links and complete publication/cleanup evidence.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_4/README.md`: isolated structured-source runtime, unchanged V6.3 catalogue identity, focused guards and reproduction commands.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_2_v6_3_pr4523_pr4417_20261109`:160-text V6.3 evaluation, matched30-row selection, exact-PR2x2 image study and unified publication.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_2_v6_3_pr4523_pr4417_20261109/add_v6_4_20261110`: live-source snapshots, preservation checks and conditional publication adding the completed V6.4 images as the fifth comparison column; original source data and FE reports unchanged.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_3/SUMMARY.md`: C-Tech product/environment evidence, approved prompt/prop delta, paperweight removal and V6.3 implementation status.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_3/README.md`: isolated V6.3 runtime, 265-entry approved catalogue, unchanged contracts, provenance and offline reproduction.

- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_2/surface_diversity_20261108/SUMMARY.md`: current V6.2 surface-diversity160 text set, published review/distribution, rectangle-guide evidence, isolated candidate and pending image-pipeline decision.

- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/ctech_v4_1/SUMMARY.md`: current V4.1 C-Tech proximity pilot,120 reviewed prompts and explicit model/editorial limitations.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v4.1/README.md`: V4.1 system prompt,18 reference cores, runtime contract and exact replay procedure.

- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v3/README.md`: V3 runtime prompt, schemas, required finalizer and frozen model settings.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/README.md`:540-candidate/108-image bounded V3 eval, frozen artifacts, reproduction and gallery.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/diversity_analysis/README.md`: distribution graphs and comparison of all540 prompts with the ten October C-Tech sample prompts.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/diversity_aware_v3/SUMMARY.md`: V3 diversity design, source-relevance rubric, and bounded108-image evaluation.

- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/camera_aware_v2/SUMMARY.md`: camera evidence, type-camera profiles, design tradeoffs, and V2 text evaluation.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/reference_integrity_v1/SUMMARY.md`: confirmed eight-row reference-upload error, other framing drift, evidence, and exclusions.

- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/PROJECT_STATE.md`: current checkpoint and next exact action.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/DECISIONS.md`: confirmed and proposed decisions.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/LEARNINGS.md`: durable verified findings and limitations.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/LONG_TERM_PLANS.md`: later image evaluation and deferred choices.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research-plan.md`: bounded source analysis and evaluation protocol.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/SUMMARY.md`: canonical evidence, recommendations, and evaluation findings once analysis begins.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/pipeline.md`: pre-existing broader pipeline proposal; background context, not this stage's specification.

## Success

A reviewable system prompt, output schema, reproducible GPT-5.5 runs covering all distinct production source examples, full inputs beside outputs, text-level assessment against supplied references, and an honest record of untested downstream image behavior. Do not claim completion before the device boundary is approved and required testing is complete.

## Tested deliverables (2026-10-14)

Product release v1 is the user-selected active rewriter. It is frozen under `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v1` and tagged `hp-lifestyle-rewriter-v1`. Its README records the exact prompt/schema checksums, GPT-5.5 settings, accepted evidence locations, reproduction command, and downstream image-eval settings. The existing unversioned prompt and schema remain compatibility copies of v1.

The tested system prompt is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/system_prompt.md`; its output contract is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/output.schema.json`. Send the full source JSON as the user message, using the system text as the system message and the schema as strict response_format. The tested settings are GPT-5.5, medium reasoning, max_completion_tokens=8000, and no explicit temperature.

Review all inputs and outputs at `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/artifacts/PROMPT_REVIEW.md`. The 14 production prompts are available for downstream generation at `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/artifacts/generation_prompts.json`. Actual revised-model testing passed all 9 production and 12 synthetic cases; image quality is still awaiting Hooman's evaluation.

## Current V2 work and historical BLUE experiment

The current product v2 is camera-aware and starts from mismatch investigation against the selected v1 pipeline. It is new work and does not reuse the former BLUE candidate. The unselected BLUE experiment was removed from the live tree on 2026-10-22; its prompt, bounded samples, and validations remain recoverable from Git commit `9810dc07`. No BLUE-candidate images were generated, and its pixel-coverage hypothesis was never validated.

## Digital-twin render inputs

The 42 first-column renderings from the supplied Foundry viewer are stored outside Git at `/mnt/localssd/hp_lifestyle_pipeline/digital_twin_renders_first_column`. Their Git-trackable provenance, filenames, dimensions, byte sizes, and checksums are in `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/digital_twin_assets/first_column_manifest.json`; the plain S3 list is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/digital_twin_assets/first_column_s3_paths.txt`.

## First prompt × digital-twin eval

The first eval matches each prompt to every twin in the same workbook-labeled device category: 6 laptop prompts × 24 laptop twins plus 8 printer prompts × 6 printer twins, for 192 rows. The reproducible builder, manifest, and gallery source are in `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1`.

Published gallery: `https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/gallery/index.html`

## Generated image eval

All 192 prompt/twin rows were generated through the supplied HP endpoint at 2368×1776 with prompt rewriting enabled, `gemini-3.1-pro`, 50 inference steps, and one output per row. The historical run has 192 endpoint-completed outputs and no endpoint failures. The 2026-10-22 audit found that all eight `baseline-0016` rows used a laptop upload while displaying a printer twin. Exclude those eight rows from image-model and camera-fidelity analysis; 184 rows remain eligible, without implying visual acceptance. The original publication remains historical evidence. See `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/reference_integrity_v1/SUMMARY.md`. The published gallery preserves the four input columns and appends Output, collapsed Rewritten prompt, and collapsed Generation debug columns.

Generated gallery: `https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/generated_v1/gallery/index.html`

FE viewer: `https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/generated_v1/fe_html/viewer.html`

Local outputs, sanitized results, and the FE input parquet are stored at `/mnt/localssd/hp_lifestyle_pipeline/generation_runs/hp_lifestyle_prompt_digital_twin_eval_v1_generated_v1`. Reproducible generation, gallery, and FE-input builder code is stored at `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/generation`.

Camera-aware V2 is ready for text review: 24 selected cases / 39 prompts covering all nine production inputs. Two rejected first attempts and their retries are retained. Runtime accepts only source messaging plus `ProductType_CameraName`. Open `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/README.md` for the system prompt, schemas, evidence and reproduction commands. V1 remains selected.

Current camera-V2 image evaluation: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_camera_v2_eval_20261022/README.md`. Same nine production sources, laptop/printer current renders only, native 16:9 aspect ratio; miniPC excluded by user.
