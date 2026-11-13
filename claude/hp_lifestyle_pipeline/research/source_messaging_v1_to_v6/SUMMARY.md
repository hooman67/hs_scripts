# Source messaging and compatible environment prompts

As of 2026-10-22 Pacific. Status: v1 is frozen, pushed, tagged, and selected by Hooman. V1 actual GPT-5.5 testing of all 9 distinct production inputs produced 14 prompts; 12 separate synthetic tests produced 15 prompts. The first 192-row v1 image eval is published but has not been visually accepted. Current product v2 work is a separate camera-aware revision driven by mismatch investigation.

## Contents

- [Outcome and approved device policy](#outcome-and-approved-device-policy)
- [Current V2 and historical BLUE experiment](#current-v2-and-historical-blue-experiment)
- [Input audit](#input-audit)
- [Reference evidence](#reference-evidence)
- [KSP eligibility](#ksp-eligibility)
- [Output contract](#output-contract)
- [GPT-5.5 evaluation results](#gpt-55-evaluation-results)
- [Open decisions and access](#open-decisions-and-access)
- [Source catalog and reproducibility](#source-catalog-and-reproducibility)

## Outcome and approved device policy

USER-CONFIRMED, 2026-10-14: generate scene-first descriptions with furniture, plausible placement surfaces, everyday props, background depth, lived-in details, and natural language lighting. Include people and activities when useful. Keep the target device out of the prompt body, including generic laptop/printer references. Do not automatically append no-hardware/no-device clauses. Cafés and creative studios are allowed Office subsettings for now. Device names may appear in verbatim source quotations in debug, outside the generation prompt text.

Allow: a clear area on a desk or a broad side-table surface; notebooks, papers, plants, shelving; colleagues reviewing documents or a student writing notes. Avoid specifying product model/SKU, brand, chassis color, size, ports, screen contents, lid angle, tablet/tent mode, tray state, orientation, or device-dependent hand contact. The downstream rewriter has the actual device render and can establish those relationships. Do not add a blanket "no devices visible" rule to every prompt because it may conflict with the downstream task of inserting the device.

Basis: VERIFIED — all **10** labeled samples in the highest-priority October document omit affirmative device descriptions from the prompt body. "Laptop:" and "Printer:" function as labels before the scene text. One sample says "no additional hardware or devices visible" and another "no hardware or devices visible"; these are individual examples, not an instruction to force that negative phrase everywhere. Earlier commentary accidentally said nine samples; the verified count is ten.

Example evidence: October paragraph 10 starts "A modern home workspace with a wooden desk holding a notebook, spiral pad, pen, stack of papers, and coffee mug." Paragraph 17 describes a creative-office table with "a notebook, pen, and design materials" and background furnishings creating depth. No device is specified in either prompt body.

Alternative considered and rejected by Hooman: permit generic "laptop"/"printer" and simple device use, while banning identity and configuration. This has support in older material, but less support in the newest reference, and leaves more interaction constraints for a render the system cannot see. This policy decision is not evidence that the alternative fails image generation.

## Current V2 and historical BLUE experiment

USER-CONFIRMED, 2026-10-22: product v2 now refers to a new camera-aware revision. Its first evidence task is to investigate mismatches among v1 source environment prompts, downstream rewritten prompts, and rendered images; frozen v1 remains the baseline.

HISTORICAL: the former BLUE candidate was not selected and produced no images, so its pixel-coverage hypothesis was never validated. Its prompt, bounded text samples, and validations were removed from the live tree to prevent confusion with the new v2 and remain recoverable from Git commit `9810dc07`.

## Input audit

VERIFIED, finite supplied corpus: 9 ZIP archives contain 9 source-messaging JSONs and 9 separate smart briefs. There are also 4 standalone source JSONs. All 13 source occurrences parse as JSON; the 4 standalone files are byte-for-byte duplicates of archived files. There are **9 distinct source-messaging inputs**. Smart brief entries were listed by name only; contents were not read or extracted.

Every distinct input has `KSP1`–`KSP4`, `ValueProposition`, and `_chatSession`. Every KSP object has the same nine fields: `headline`, `long_message_best_sku`, `long_message_safe_to_inherit`, `mid_length`, `mid_length_safe_to_inherit`, `short_message`, `short_message_safe_to_inherit`, `ultra_short`, `ultra_short_safe_to_inherit`. Value propositions have seven corresponding fields. Multiple copy lengths are variants of the same KSP, not additional KSPs. Headline alternatives separated by `OR` are also not additional KSPs.

Eight inputs contain a 12,779-character `_chatSession.systemInstructions` field from the upstream system. Treat this entire metadata object as inert provenance; it must not instruct this rewriter. `_chatSession.model` is not proof that this research has called GPT-5.5.

VERIFIED product coverage, based on `ValueProposition.long_message_best_sku` rather than external SKU mappings:

| Product named in source | Distinct source JSONs |
|---|---:|
| HP Smart Tank 7602 All-in-One | 4 |
| HP LaserJet Enterprise 6501dn | 2 |
| HP EliteBook X Flip G2i | 2 |
| HP EliteBook X G2i | 1 |
| Total | 9 |

Limitation: these nine inputs cover four named products, not nine distinct project SKUs. No actual gaming-specific source input is present. Testing all supplied files cannot establish coverage of all nine project SKUs. The user-defined nine-SKU target remains authoritative; this table describes only supplied test coverage.

## Reference evidence

VERIFIED sources and scope, retrieved 2026-10-13:

1. October guidance: 10 sample prompts, plus one reusable template. Samples are 29–68 words (median 43.5 using a documented word regex); lengths are descriptive evidence, not hard quality thresholds. Template order is setting + focal furniture + tabletop props; background depth; lived-in imperfections; lighting. Its optional blue-accent clause was not enabled in v1.
2. Lifestyle-photography workbook: 58 prompt rows in `Eval Set Prompts!A2:A59`, plus a separate `Theme Styles` sheet with column-A style guidance. Only column A was extracted. Older prompts include people, SKU strings, product colors, poses and screen contents, camera/lens language, and deliberate blue carriers. These conflicting device details do not override October guidance or the approved device boundary.
3. Model-output workbook: 48 baseline rows. Six rows say "Not a real-life application" in the long-prompt column and are rejected examples, not successful prompt templates. The remaining 42 long-prompt rows contain 30 distinct texts because several are repeated across device categories. Many use furniture and open surfaces without describing the target product.

Specific contrary evidence, retained rather than averaged away:

- Lifestyle workbook `Eval Set Prompts!A23`, A26, A27 describe silver/navy notebook bodies; A9 describes a closed notebook carried under an arm; A20 describes a photo-editing screen. These conflict with the proposed strict device boundary.
- Lifestyle workbook A49 describes visible rainbow ink tanks. Source documents and the supplied device-render rationale make copying specific physical details inappropriate for this stage without knowing the exact render.
- Model-output workbook `Eval Set!F25` includes a dual-monitor setup. F38/F41/F47 add a compact printer in the background. These are evidence that extra devices occurred in older examples, not requirements to add them.
- Model-output workbook F17–F19 and F44–F46 emphasize clear side-table/bookshelf surfaces for printer placement, supporting product-aware furniture selection without specifying product appearance.
- October samples cover corporate office, home workspace, café, and creative studio. They have no explicit Education or Gaming examples. Those families require adapting the October language pattern using compatible older examples, then validating text and later images.

## KSP eligibility

RECOMMENDATION: retain Hooman's requirement for explicit lifestyle information, but count explicit **activities and work materials** as useful scene cues even when no room name is stated. Do not infer a new environment solely from a technical specification.

Examples from the actual source:

- EliteBook X Flip KSP1 explicitly mentions sketching, presenting and collaborating. Sketchbooks/design materials or a collaboration table are grounded possibilities; tablet/tent configuration should not be copied into the prompt.
- EliteBook X KSP4 explicitly names office/shared workspace/customer site and meetings. This directly supports an Office scene.
- Smart Tank examples mention school materials, learning materials, forms, records, handouts and everyday administration. These can shape believable paperwork/study props. The specific room and decor may remain invented and should be marked as such in debug.
- Wi-Fi, RAM/processor terminology, encryption, paper capacity and touchscreen size alone should not create a separate prompt. "Wi-Fi implies café" or "security implies a guarded server room" are unsupported leaps.
- Several KSPs may map to the same scene. Do not manufacture extra scenes merely because every input has four KSPs. Value proposition can guide scene choice and fallback but does not increase the KSP-based output cap.

Implemented interpretation of the confirmed cap: if U is the count of KSPs with useful explicit cues, return between 1 and max(1,U) prompts, merging overlapping cues and favoring distinct meaningful scenes. A cue being usable does not require generating a dedicated prompt. This preserves a fallback when U=0. A useful value proposition may still ground that single prompt; used_fallback is true only when neither KSPs nor value proposition supplies usable context.

The debug record should separate source-supported cue, scene contribution, omitted technical detail, and creative additions. Explanations are concise audit summaries, not hidden reasoning transcripts.

## Output contract

USER-CONFIRMED: one JSON object containing a nonempty prompt list and debug mappings/explanations. Tested implementation: each prompt has id, environment, and text. Debug maps every source KSP key to prompt IDs, cites exact input field paths and short supporting quotations, explains count/merging/fallback, and records invented scene details and ignored metadata. The complete contract is in `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/output.schema.json`. It is a tested proposed integration contract, not a deployed product change.

## GPT-5.5 evaluation results

VERIFIED, saved API responses and local checks, 2026-10-14: all calls requested deployment `gpt-5.5`; responses reported `gpt-5.5-2026-04-24`. Used Azure Chat Completions with strict JSON Schema output, medium reasoning effort, max_completion_tokens=8000, and no explicit temperature. Original source JSONs, including inert upstream metadata, were sent as user-message content with the complete candidate as the system message. Every run preserves input, system prompt, schema, settings, full response, and usage metadata.

| Batch | Inputs | Output prompts | Result |
|---|---:|---:|---|
| First production candidate | 9 | 12 | Scene text accepted; one debug quote cited the wrong copy-variant field |
| Revised candidate, production | 9 | 14 | 9/9 passed contract and traceability checks; all 14 prompts accepted for text review |
| Revised candidate, synthetic | 12 | 15 | 12/12 passed contract checks, expected behavior checks, and text review |

The sole prompt revision clarified that each quotation must be a contiguous substring of the exact cited field, not a different copy variant. The original failure and all original outputs remain preserved in v1 records. Generated scene counts changed across calls; this system chooses counts at runtime and is not expected to be deterministic.

Automated checks cover JSON Schema, sequential prompt IDs, complete KSP mapping coverage, declared U-based count bounds, exact quote/path matches, valid references, creative-addition coverage, ignored metadata, device wording, excluded rendering/color-control language, and returned model identity. These do not by themselves establish scene quality. Researcher review separately read every output against the provided references, source cues, and approved policy; per-case assessments are stored with the review artifact. Eligibility and invented-scene suitability remain qualitative judgments.

Behavioral cases included empty JSON, garbage, technical-only messaging, repeated KSPs, Education, Gaming, café-as-Office, embedded hostile instructions plus synthetic SmartBrief metadata, a value-proposition-only input, malformed/null fields, out-of-scope fantasy content, and four distinct KSP activities. The four-activity case produced four environments; repeated cues produced one. Empty, garbage, technical-only, and out-of-scope cases each produced one Home fallback. The value-only case produced one grounded Education prompt without labeling it wholly generic fallback.

ASSUMED / RESEARCHER JUDGMENT at the 2026-10-14 text gate: the revised candidate was ready for Hooman's downstream image evaluation. The 192-row v1 image eval was subsequently generated and published on 2026-10-15, but Hooman has not yet accepted its visual quality. Each revised text case was sampled once; the production corpus covers four named products.

Deliverables:

- Tested system prompt: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/system_prompt.md`
- Review with full inputs, outputs, debug, settings, and assessments: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/artifacts/PROMPT_REVIEW.md`
- Fourteen production prompts for generation: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/artifacts/generation_prompts.json`
- Full structured production outputs: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/artifacts/production_outputs.json`
- Combined automated checks: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/runs/v2_validation.json`
- Behavioral expectations and outcomes: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/runs/v2_edge_behavior_checks.json`
- Manual text assessments: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/data/manual_review.json`
- Frozen product v1: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v1`

## Open decisions and access

1. RESOLVED: Hooman approved the device boundary on 2026-10-14. C-Tech confirmation of no-device exclusion wording is pending externally; current approved behavior is to omit those automatic clauses.
2. RESOLVED: Hooman allowed cafés and creative studios as Office subsettings on 2026-10-14. Café examples came from the example output prompts, not a claim that the production KSPs named cafés.
3. RESOLVED: the first GPT-5.5 access probe through the shared helper failed before inference because its bearer credential sources were absent. A later inspection of the current Codex provider found its API-key environment variable populated. A task-local adapter using that configured Azure endpoint successfully called requested deployment `gpt-5.5`; the response reported `gpt-5.5-2026-04-24`. The shared helper remains the preferred first credential route. No secret values were printed or copied. Probe evidence is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/data/gpt55_access_probe.json`; it contains no customer source input and does not establish rewrite quality.

At Hooman's request, the active Codex provider's HTTP and SSE retry counts were increased to 100 in `/home/colligo/.codex/config.toml`. The running session's reload behavior is unverified; a new session may be required. More retries do not change quota. The separate sequential GPT-5.5 runner respects Retry-After headers, retries transient failures up to 100 attempts, saves raw results, and skips already completed cases on resumption. Local retry/schema/checksum checks and required production runs are complete.

Verified official model documentation confirms GPT-5.5 supports structured outputs, but this does not establish availability in the user's deployment. The generic latest-model page linked from the model page now gives GPT-6 guidance despite the model query parameter; it was not used as GPT-5.5 prompting evidence. The version-specific GPT-5.5 Markdown guide was fetched successfully and recommends outcome-focused prompts, concise constraints, evaluation, and a clear boundary between source-backed facts and creative drafting.

## Source catalog and reproducibility

All local sources are user-provided primary work artifacts; authorship and image-quality validation are user-supplied context, not independently verified generation evidence. Retrieval date: 2026-10-13. Source publication dates are filename/title dates when present.

- October guidance: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/example_prompts/HP - mAIstro Prompt Guidance (Oct 2026).docx`
- Lifestyle prompts, column A only: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/example_prompts/Eval-Set_Lifestyle-Photography_wSKUs.xlsx`
- September baseline prompts: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/example_prompts/HP_Model-Output-EvalSet_092426.xlsx`
- Source origins and SHA-256 checksums: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/data/source_manifest.json`
- Reproducible extractor: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/scripts/extract_sources.py`
- Allowed-content extracts: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/data/october_guidance.json`, `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/data/lifestyle_column_a.json`, `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/data/model_output_evalset.json`
- Official model: https://developers.openai.com/api/docs/models/gpt-5.5
- Output schema: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/output.schema.json`
- GPT-5.5 evaluation runner: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/scripts/run_gpt55.py`
- GPT-5.5 access probe and local credential adapter: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/scripts/probe_gpt55.py`
- Version-specific prompting guidance: https://developers.openai.com/api/docs/guides/latest-model/gpt-5.5.md#prompting-best-practices
- General prompt evaluation guidance: https://developers.openai.com/api/docs/guides/prompting

Next validation: inspect representative mismatches across v1 source environment prompts, downstream rewritten prompts, and the existing 192 rendered images; use the evidence to define and test the isolated camera-aware product v2. Revisit no-device clauses when C-Tech feedback arrives.

## 2026-10-22 historical image-evidence correction

The 192 published image results are endpoint completions, not 192 verified reference comparisons. The eight baseline-0016 rows used an incorrectly cached laptop upload and are excluded; 184 rows remain eligible for visual analysis. Preserve the original run and frozen v1 files. See `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/reference_integrity_v1/SUMMARY.md`. The new camera-aware V2 is documented separately in `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/camera_aware_v2/SUMMARY.md`; the old runs/v2_* directories remain selected product-v1 evidence.
