# Refraction prompt research

LATEST UPDATE — 2026-10-20: the single-drink orange run `v3fal_new_orange_ribbon` was replaced because it used the same rejected tilted source as seven group outputs. The current run uses `/home/colligo/mixology_data/refraction_research_2026-10-19/assets/ref_inputs/TCCC–Crafted-Sept-2026.png`, unchanged system V3, `Add refractions.`, style image 003 and FAL high/auto. Output is 896×1200. Direct review finds strong upright identity/crop preservation, but dense caustic mesh remains (advisory refraction 3/5, vein_like=true). The old run is recoverable in the replacement archive; 19 active refraction outputs remain. The older paragraphs below describe the pre-replacement batches. Combined composition/refraction is now tested separately in a third tab; source V3 stays frozen.

As of 2026-10-19. USER-CONFIRMED: keep system V3 unchanged and rerun overhead/group refraction from corrected inputs. Both new outputs are generated using clean inputs derived from 013/027. The prior twelve refraction outputs remain intact pending review of their replacements. Input-preparation experiments are removed from the main gallery narrative, not from stored provenance. No acceptance of the new refraction outputs is inferred.

COMPLETED FAL BATCH (2026-10-20 UTC): all five cream-topped drink inputs were processed with unchanged V3, excluding cap and empty cup. User authorized fal while new-cluster allowlisting was pending. All five use requested Astra through `openrouter/router/vision`, followed by exact endpoint `openai/gpt-image-2.5/sunburst/edit`, high/auto/PNG, original target plus style image 003 in that order. All outputs are 848 × 1264; observed image-stage durations range 35.95–48.61 seconds including queue/poll time. All five advisory critiques and direct visual reviews are complete. The previous fourteen results remain intact, for 19 refraction outputs total. The later ingress repair does not alter these results; the Foundry Azure resource still lacks a Sunburst deployment.

OBSERVED: target colors, major ice/syrup details and cream remain recognizable, with strong drink-colored projections. Fine mesh, long crossing rays and point-like bright intersections persist. Several images reduce or shift the subject despite matching canvas dimensions; the orange rim/base viewpoint also shifts somewhat. This is not strict composition or pixel preservation. Advisory refraction scores are 3/5 for four images and 4/5 for cola; advisory identity is 5/5 throughout, which should not be read as exact fidelity. Keep V3 unchanged per user instruction; no new refraction system iteration was made.

Four separate group-composition outputs (V1/V2 × lineup/staggered) are documented at `/home/colligo/hs_scripts/claude/mixology/research/group-composition/SUMMARY.md` and in the separate gallery tab. Do not confuse them with refraction edits or a merged system. Exact fal records are under `/home/colligo/mixology_data/refraction_research_2026-10-19/runs/v3fal_*`; no secret values are stored there. Astra's first `reasoning=false` request was rejected before image submission; its retained retry uses mandatory `reasoning=true`. Reasoning effort and backend snapshot are not exposed by fal, so this is a distinct provider batch, not a controlled prompt/provider benchmark.

HISTORICAL preparation delivery: before fal execution, the composition tab contained two not-generated cases and the 176-file package passed S3 readback. That checkpoint is superseded by the nine-image fal batch above; latest publication/browser verification is in `/home/colligo/hs_scripts/claude/mixology/PROJECT_STATE.md` and `/home/colligo/mixology_data/refraction_research_2026-10-19/_review`.

VERIFIED restart recovery: all 157 published files were restored from S3 and byte-checked under `/home/colligo/mixology_data/refraction_research_2026-10-19`; the older SSD run path below is now a compatibility symlink to that durable root. The supplied source tree is copied and hash-verified at `/home/colligo/mixology_data/source_restored_2026-10-19`. Use `/home/colligo/.venvs/mixology/bin/python`. Original `_review` reports were lost during the wipe; references below describe historical checks. Fresh recovery evidence is `/home/colligo/hs_scripts/claude/mixology/research/refraction-prompts/data/recovery_manifest_2026-10-19.json` and the durable run's `_review/before_new_inputs_manifest.json`.

## Contents

- [Question and evidence](#question-and-evidence)
- [Corrected-input reruns](#corrected-input-reruns)
- [V3 checkpoint and corrected overhead input](#v3-checkpoint-and-corrected-overhead-input)
- [Method](#method)
- [Results and recommendation](#results-and-recommendation)
- [Reproduction and limitations](#reproduction-and-limitations)
- [Current checkpoint](#current-checkpoint)

## Question and evidence

USER-CONFIRMED: build a GPT system prompt that turns a very short user request and a drink image into a GPT Image 2.5 edit with the preferred refractive-light appearance. Generate, judge, revise, and publish every generation with all inputs through render-s3-gallery.

The customer PDF is `/mnt/localssd/mixology/260605_Mixology_AI_Art_Direction_Process.pdf`. Curated native sources are in `/mnt/localssd/mixology/extracted_from_pdf/native_original_streams/refraction`.

USER-CONFIRMED examples: 023→027 is the strongest pair; 012→013 is another positive pair; 014→015 is a negative example because the caustics resemble veins. Image 003 is a good single berry-drink output, originating from the right-hand drink in 018; 002 is a good cola output with uncertain input. Image 029 is a good unpaired group output. Keep uncertain pairings explicit.

VERIFIED source reading: page 4 concerns base drink properties and angle variation; page 5 is refraction prompting; page 6 includes a later restrained-light prompt whose prohibitions partly conflict with the user's preferred branching-light treatment. Page 10 supplies a general refractive style paragraph and labels a subsequent Photoshop composition/upscale step. The page 5/10 prompt bodies are image descriptions, not a fully specified deployed system-message contract.

VERIFIED visual inspection: both positive pairs change crop/visible area compared with their inputs. Crop fidelity and style match therefore need separate evaluation. A clarification on default reframing is pending. Until answered, use input framing as the baseline; do not claim the positive pairs prove exact geometric preservation.

## V3 checkpoint and corrected overhead input

USER-CONFIRMED: leave system V3 as-is for now. The frozen prompt is `/home/colligo/hs_scripts/claude/mixology/research/refraction-prompts/prompts/system_v3.md`, SHA-256 `652fd8895c132e7cf6d311052f55a823dbe7ea09b749077a32d82faa6948eb9e`. The full review gallery remains at https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/mixology/refraction_research_2026-10-19/gallery/index.html . Subsequent corrected-input reruns reuse that exact V3; they are not V4 or prompt tuning.

USER-CONFIRMED correction: image 012 is unsuitable because of its crop. Preserve it as historical evidence, but use a new input derived from customer image 013 for future overhead work. Source: https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/mixology/refraction_research_2026-10-19/assets/image_013_p05_xref1594.jpg .

USER-APPROVED clean input: `/mnt/localssd/mixology/refraction_research_2026-10-19/assets/overhead_013_clean.png`. It is already beside the other inputs. The one-off cleanup section formerly shown in the gallery was removed at Hooman's request; cleanup artifacts and the record remain under `/mnt/localssd/mixology/refraction_research_2026-10-19/input_cleanup/overhead_from_013_v1`.

VERIFIED method: one direct `gpt-image-2.5-sunburst` edit (high/auto/PNG; observed CLI duration 23.4 seconds), using only customer image 013 and the exact prompt in `/home/colligo/hs_scripts/claude/mixology/research/refraction-prompts/prompts/clean_overhead_input_v1.txt`. The task removes external shadows, colored light pools and caustics, not the internal optical appearance of the drinks. The refraction rewriter/system V3 was not used for this inverse cleanup.

The raw edit slightly smoothed drink details. A conservative silhouette mask extracted from the shadow-free raw output restores source pixels in the cup interiors, with a narrow feathered boundary retaining the generated clean rim. Reproduction of this deterministic step: `/home/colligo/hs_scripts/claude/mixology/research/refraction-prompts/scripts/finish_clean_input.py`. All intermediates, the raw model output and the preservation mask are retained separately, not displayed in the main gallery narrative; the mask was NOT a model input.

VERIFIED checks: source and delivered output are both 1537 × 1023. All 498,696 fully protected pixels equal the source exactly (zero changed pixels). Among 1,002,357 checked background pixels away from cup boundaries, none has channel spread above 12 or a minimum RGB channel below 235; mean RGB is approximately (253.985, 253.952, 253.952). Direct visual review of raw and delivered outputs found the colored projections removed and the fruit, ice, foam, straws and cup placement retained, with no visible double edges or colored ghosting.

LIMITS: exact-pixel preservation is guaranteed only inside the saved opaque mask, not at generated rim/transition pixels. Image 013's existing slight top/right edge crops remain intentionally unchanged; no outpainting was requested. This is a derived clean input from a preferred output, not an independently acquired customer before/after pair or a held-out test. The `overhead_clean` case and preset point to this file; historical `overhead`/012 is marked deprecated for new generation.

## Corrected-input reruns

USER-CONFIRMED scope: the overhead correction looks good; use it for a replacement V3 output. Also replace cropped group input 023 by removing external shadows/refraction from customer output 027, preserving its complete-cup framing, and generate a V3 refraction result from that corrected input. Preserve old outputs until Hooman reviews the replacements. Do not include either one-off input-generation process in the HTML experiment narrative.

Execution: the user-requested three-way delegation and two compact-context worker retries returned no usable messages or artifacts before interruption. The parent completed the bounded work directly, overlapping model calls with gallery/documentation work. New IDs are `v3corrected_overhead_clean` and `v3corrected_group_clean`. Both use system V3 unchanged, user text `Add refractions.`, high/auto Sunburst, and the same style presets 013/027 as their earlier V3 counterparts. Input correction, rather than a new system version, is the intended change; stochastic rewrite/generation differences remain possible.

VERIFIED group input: `/mnt/localssd/mixology/refraction_research_2026-10-19/assets/group_027_clean.png`; one-off provenance is stored separately under `/mnt/localssd/mixology/refraction_research_2026-10-19/input_cleanup/group_from_027_v1`. One direct Sunburst edit (25.4 seconds, high/auto/PNG) removed external lighting. `/home/colligo/hs_scripts/claude/mixology/research/refraction-prompts/scripts/finish_group_input.py` then restored source interiors using an eroded/feathered silhouette mask. Source and result are 1402 × 1122; all 493,891 protected pixels match exactly. None of 1,021,269 checked background pixels has channel spread above 12 or minimum RGB below 235; mean RGB is (254.012, 253.953, 253.959). Root visual inspection confirmed white surroundings and complete bases with no visible colored shadow remnants. Exact preservation excludes generated edge transitions.

VERIFIED new generations: overhead output `/mnt/localssd/mixology/refraction_research_2026-10-19/runs/v3corrected_overhead_clean/output.png` is 1538 × 1023 (29.75 seconds); group output `/mnt/localssd/mixology/refraction_research_2026-10-19/runs/v3corrected_group_clean/output.png` is 1402 × 1122 (29.1 seconds). Astra rewrites were 123 and 119 words, respectively. The overhead auto-sized output adds one column relative to its 1537-pixel-wide input; neither output has a pixel-exact preservation guarantee.

OBSERVED by direct visual inspection: overhead preserves the wider three-cup layout and long lower-left pink/blue projections with bright branching centers. Group retains all bases, recognizable drink ingredients and straw assignments, with extended magenta/cyan/coral projections and bright branching concentrations. Fine connected mesh persists in both; the group side projections also diverge. These are new review candidates, not proven quality improvements or held-out transfer tests. Full prompts, actual input/style images, automatic critiques and separate agent notes accompany both gallery entries. No further generation is requested before user review.

ADVISORY model assessment: both new Astra critiques returned refraction 4/5, identity 5/5 and composition 5/5, with `vein_like=false` and verdict `promising`. Their explanations still flag dense secondary mesh; group highlights are excessively white in some concentrations. These subjective scores are not calibrated measures or user approval.

## Method

ASSUMED starting bounds: roughly 10–12 outputs in up to three iterative rounds, `gpt-image-2.5-sunburst`, quality high, original inputs reused independently per version. Stop earlier if a useful reviewed candidate is established; no endless generation loop. Use `gpt-6-astra` as the vision prompt rewriter and as a separate automatic critic, with direct human-agent visual review. Model judgments are advisory, not customer acceptance.

Initial cases: group (023), overhead (012), single dragonfruit cup (014). Start with a page-5 verbatim direct baseline on the overhead case, plus a v1 rewriter on all three. Read actual outputs before changing instructions. Add a bounded transfer case only after the main cases are understood.

Runtime user prompt: `Add refractions.` Image 1 supplies scene/drink truth. Initial runtime uses no stylistic image references; the system encodes the learned style. A later reference-conditioned variant may be compared if text-only conditioning is insufficient, with every extra model input clearly shown.

Judge appearance separately from preservation: branching-light hierarchy, luminous cores inside colored projections, coherent directional lighting, clean receiving surfaces; cup identity, ingredients, straw colors/count, camera/view, and composition. Distinguish uniform veins, generic glow, literal electricity, sparkle meshes, and unwarranted color/geometry changes. Compare the accepted examples and rejected example to calibrate judgment.

Preserve full system/user/generated prompts, all model input images and roles, model/settings, output files, hashes, errors, automatic critiques and agent assessments. There is no exposed seed in the bundled CLI. Single samples cannot isolate prompt effects from stochastic variation.

## Current checkpoint

All 14 refraction outputs and 14 automatic critiques are complete: the original twelve plus two corrected-input V3 reruns. All outputs were directly visually inspected. No additional inference is scheduled. Every run remains under `/mnt/localssd/mixology/refraction_research_2026-10-19/runs`.

VERIFIED updated delivery: the five-file IMS gallery and all assets/prompts/run evidence are uploaded. Authenticated S3 readback matched all 157 published files (approximately 49 MB), including required HTML/CSS/JavaScript MIME types. The gallery excludes both input-preparation experiments while retaining their stored files. Local Chromium loaded all 70 displayed images and validated 218 relative references; filters, prompt expansion, lightbox and mobile layout passed with no JavaScript errors. IMS code is byte-identical to the existing KDP template. Both corrected runs use the exact frozen V3 hash, and all twelve old output hashes match the pre-change manifest. Evidence: `/mnt/localssd/mixology/refraction_research_2026-10-19/_review/gallery_validation.json`, `/mnt/localssd/mixology/refraction_research_2026-10-19/_review/s3_verification.json`, and `/mnt/localssd/mixology/refraction_research_2026-10-19/_review/before_corrected_input_reruns_manifest.json`.

LIMITATION: the browser test mocked IMS only locally. A live request to the Foundry HTML gateway timed out from this compute host, consistent with its earlier corporate-documentation timeout. S3 publication is verified; a real signed-in end-to-end gateway session is not. The user-facing URL requires Adobe/Foundry access.

The corrected-input batch stopped with both results presented. Subsequent user direction authorizes the five-input batch and separate composition research above. Preserve every prior run ID; no historical deletion or refraction-system tuning is requested.

## Results and recommendation

CURRENT WORKING CONFIGURATION — USER SELECTED FOR NOW: concise V3 system prompt and one fixed view-appropriate lighting reference. End-user request remains `Add refractions.` The preset is supplied by the application, not by the user. Astra creates a short concrete edit prompt; Sunburst receives that prompt and BOTH the original target and the preset image. The observations below describe the original twelve-image batch, including its subsequently rejected cropped overhead input.

Canonical system prompt: `/home/colligo/hs_scripts/claude/mixology/research/refraction-prompts/prompts/system_v3.md`. Request contract and reproducible commands: `/home/colligo/hs_scripts/claude/mixology/research/refraction-prompts/USAGE.md`. Configuration: `/home/colligo/hs_scripts/claude/mixology/research/refraction-prompts/preset.json`.

OBSERVED, limited to these single samples: text-only prompts produced broad caustic webs and decorative sparkles more often. Adding a fixed customer lighting reference made the overhead fields more directional and localized, and moved the single-cup projection onto a backdrop like the preferred example. V3 shortened the rewrite from roughly 160–240 requested words to 80–130 with comparable observed style. This does not establish a statistical improvement over V2.

| Iteration | Outputs | Change | Visual finding |
| --- | ---: | --- | --- |
| Customer baseline | 1 | Page-5 prompt directly to Sunburst | Preserved overhead scene; broad cellular mesh and inconsistent projected directions |
| V1 | 3 | Astra system, target only | Identity broadly retained; repeated nets, rays and star intersections |
| V2 | 3 | Revised system plus fixed style image | More localized caustics and better overhead direction; some mesh persists |
| V2 text-only control | 1 | Same V2 system, no style image | Conspicuous stars on cup rims, fruit and straws |
| V3 | 3 | Concise system plus same style inputs | Useful overhead candidate; group and single still have overly connected secondary lines |
| V3 framing diagnostic | 1 | `Add refractions and show the full cups.` | Closest group-style match; all bases and longer light paths visible, but changes crop and invents previously unseen geometry |

HISTORICAL RECOMMENDATION, superseded for first review by the corrected-input results above: review `v3_overhead` beside `v2_overhead`, then `v3_single`, and `v3reframe_group` beside customer output 027. The last run was the strongest group match in the original batch but conditions on that same accepted image and explicitly allows a pullback. It is not proof of text-only learning, unseen-scene transfer, or pixel-exact preservation. Keep the default crop-preserving until a different user requirement is established.

Advisory Astra refraction scores were 3/5 for the baseline; 2.5–3/5 for V1; 3.5–4/5 for V2 with style; 3/5 for the V2 text-only control; and 4/5 for V3 and its framing diagnostic. These are one model's subjective assessments, not calibrated quality measurements. Agent visual notes remain separate in the gallery and `/home/colligo/hs_scripts/claude/mixology/research/refraction-prompts/review_notes.json`.

## Reproduction and limitations

- VERIFIED execution: all 14 refraction edits completed through `gpt-image-2.5-sunburst` using the unchanged bundled imagegen CLI, high quality, auto size, PNG. All 13 rewrites and 14 completed critiques used `gpt-6-astra` via Foundry's direct gateway credentials. Baseline has no rewriter. Two separate cleanup edits also used the unchanged CLI without Astra rewriting.
- Full system/user/generated prompts, ordered image roles and hashes, output dimensions/hashes, rewriter usage/IDs, image timing, sanitized CLI logs and automatic critiques are retained per run. Exported source and all prompt versions accompany the gallery.
- Three initial critic calls returned HTTP 400 because JSON mode required the word JSON in the input message. The harness was corrected and those evaluations rerun. No image-generation request failed. The exact failed-response payloads/IDs were not saved; this error note is reconstructed from observed tool results, not a complete provider failure log.
- Original customer assets and generated refraction outputs are unmodified in the gallery; no upscaling or post-generation retouching was applied to refraction results. The two newly derived clean inputs use the explicitly documented cleanup/compositing process above. Historical outputs still show their actual original inputs.
- Single samples, not a factorial study: wording, preset inclusion and stochastic generation may all contribute. The V2 text-only group control helps inspection but does not isolate a causal effect. No random seed is exposed by the bundled CLI.
- Group and overhead style presets depict the same scenes as the inputs. The single-cup preset is a different drink, but there is no held-out customer scene, repeated-sample robustness test, or automatic view-to-preset selector.
- Close crop and available receiving-surface area materially constrain the light layout. Automatic composition scores compare to the original crop, including for the explicitly reframed diagnostic.
- The system/preset configuration is a research artifact, not a deployed application. The single-cup mesh/star pattern remains unresolved. No statement here implies Hooman accepted a generation or a new default framing policy.

Published gallery: https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/mixology/refraction_research_2026-10-19/gallery/index.html . S3 prefix was verified empty before publication. TCCC bucket choice is a researcher assumption based on the PDF branding and existing customer bucket, not an answered user preference. `render-s3-gallery` determined the relative-asset layout and unchanged IMS authentication implementation; its missing original template was replaced by the existing KDP gallery template. Temporary AWS credentials came from the machine-token broker per the higher-priority global rule, not manually pasted credentials.
