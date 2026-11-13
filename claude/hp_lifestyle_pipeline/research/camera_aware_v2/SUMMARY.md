# Camera-aware environment writer V2

As of 2026-10-22. **Draft ready for Hooman’s text review; V1 remains selected.** The new V2 changes scene scope to fit a fixed product-camera preset. It contains no blue-coverage policy.

## Contents

- [Decision and runtime contract](#decision-and-runtime-contract)
- [Evidence and offline interpretation](#evidence-and-offline-interpretation)
- [Design and alternatives](#design-and-alternatives)
- [Evaluation](#evaluation)
- [Reproduction and update procedure](#reproduction-and-update-procedure)
- [Limits and next decision](#limits-and-next-decision)

## Decision and runtime contract

**USER-CONFIRMED, latest decision:** V2 receives only source messaging and a type-qualified camera tag. There are **no product names**, SKU inputs, or runtime images. Named presets are fixed. Canonical examples are `miniPC_FrontRightMedium` and `laptop_BackLeftCloseUp`. Current types are `laptop`, `printer`, and `miniPC`; later types can be registered. This supersedes both the earlier required-product design and the subsequent optional-product suggestion.

```json
{
  "source_messaging": {"KSP1": {}, "ValueProposition": {}},
  "camera_tag": "miniPC_FrontRightMedium"
}
```

The type and compact camera name have one separating underscore. Case and surrounding whitespace normalize. Older type-qualified names with underscores inside the camera name are supported only through explicit aliases for known presets; unknown spelling is not guessed. A suffix such as `90` is a literal preset identifier, not a rotation command.

The output preserves V1's `prompts` and source-mapping `debug`, adding `debug.camera`: requested/resolved tag, effective device type, profile version, resolution status, framing/elevation and per-prompt omissions. No product-resolution fields remain. The supplied tag controls type even if marketing copy names a different device. Device/type/camera labels stay out of scene prose; exact source quotations may retain original marketing text.

**Implementation:** embed compact offline type-camera notes in the system prompt. No external lookup or image analysis is required at runtime. A deterministic resolver accompanies the draft for offline test validation only. Profiles conservatively cover the reviewed shapes for each type; there are no per-product runtime overrides.

## Evidence and offline interpretation

**VERIFIED, supplied finite corpus:** 243 named camera PNGs across six product folders in `Shared.zip`. There are 40 regular camera names. Magic and Messi also contain `CAM_review`; Viktor contains a review render too, but that laptop review tag is not part of the approved 40-name laptop list and is excluded from the draft runtime registry. Regular renders are 1024×576; review images may have different dimensions. The corrected registry has 40 laptop tags, 41 printer tags, and 41 miniPC tags: 122 type-camera profiles. The ZIP has four laptop products, one actual printer (Magic), and one miniPC (Messi). Another printer, Tassel, has PDF references rather than a matching high-resolution ZIP folder.

Source files were copied from volatile `/mnt/localssd/HP_scenes` to backed-up `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/originals`. All ten supplied files were verified by SHA-256. Large source data and review images are ignored by Git; compact manifests, notes, scripts, prompt text and evaluation records are durable within the checkout.

**USER-CORRECTED / VERIFIED SOURCE LABEL ERROR:** Messi is a miniPC, although its original folder and filenames falsely say printer. The approximately 46% Magic versus 3% Messi alpha coverage under `Back_CloseUp` is therefore a **cross-type** comparison. It does not support the earlier claim that printer models require product-specific runtime profiles. Original names remain unchanged as provenance; derived records explicitly separate source-declared and effective device types. A thin side silhouette can still have low pixel coverage while spanning most of the frame height, so occupancy alone is not enough even within one type.

The alpha metric counts nontransparent rendered pixels, including any shadow encoded in alpha. It is **not** a semantic product segmentation, an available-tabletop measurement, or a conversion formula for prop counts. The draft uses visual judgments about framing and view elevation, with counts as conservative design ceilings. Elevation labels are broad qualitative groups, not measured camera extrinsics.

| Offline pattern | Draft response |
|---|---|
| Tight near-level front/back views | Surface, soft light, neutral background tone; no named props or room fixtures. |
| Tight oblique views | At most one small detail; crop the detail if appropriate rather than expanding the scene. |
| Medium views | At most two local props and one subordinate background detail, if elevation permits. |
| Wide views | At most three local props and two background details; do not fill every allowance. |
| Top-oblique views | Local horizontal surface and flat details; no required visible walls, windows or distant room layers. |
| Low/level elevation | Avoid tabletop sprawl, foreground blockage, and demands to reveal top surfaces. |
| miniPC regular close views | Medium-density ceiling calibrated offline on the supplied miniPC; retain its scale. No people. Top-oblique restrictions still apply. |
| laptop_FrontRightCloseUp | Surface and light only, conservatively accommodating the tightest reviewed laptop framing without a SKU lookup. |

**Counterevidence and tradeoff:** broad margins around the supplied miniPC could tempt much richer scenes. The draft allows modest additional context but does not assume all transparent space is usable tabletop. Conversely, zero-prop tight scenes can lose visible differentiation between KSPs. The draft records that loss in debug instead of requiring all source details to appear.

Sources and audit artifacts:

- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/camera_aware_v2/data/device_type_corrections.json`: user-confirmed Messi miniPC correction, retained source identity, and provenance.

- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/camera_aware_v2/data/source_manifest.json`: originals, durable copies, hashes, and file sizes.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/camera_aware_v2/data/camera_catalog.json`: exact names and extracted render locations.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/camera_aware_v2/data/pdf_extraction.json`: PDF page/text provenance.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/camera_aware_v2/data/camera_alpha_mask_metrics.json`: alpha occupancy and bounding boxes, not inferred prop capacity.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/review`: product contact sheets and PDF previews used for offline inspection.

## Design and alternatives

The root research agent authored the system instructions; delegated GPT-5.6-sol high-effort agents handled extraction, cleanup, compiler/validation code, historical request tracing, and GPT-5.5 execution. No subagent authored the behavioral prompt.

The camera registry stores one profile per type-camera tag. Top-oblique geometry permits no named background details. Unknown types or cameras receive a minimal surface-and-light fallback with explicit unknown status. Registered aliases cannot cross device types. New types can be added to the registry without writing type-specific prompt or resolver branches.

| Approach | Benefit | Cost / limitation | Status |
|---|---|---|---|
| Infer everything from name words | Small prompt and minimal setup | Misses actual framing, misleading names and opaque review tags | Rejected as the primary method |
| Embed offline type-camera registry | Tag-only runtime; repeatable notes; no vision cost | Larger system prompt; model must select correct notes; defaults may simplify more than a specific product requires | Current V2 draft |
| Resolve the profile in application code | Smaller request context and deterministic lookup | Integration work; still no runtime vision | Compatible later optimization if embedded lookup proves unreliable |
| Analyze the actual image every request | Can detect changed assets or unexpected crop | Extra cost, latency, and interpretive variability | User deferred to V3 |

The output still follows V1's environment-only boundary and four families. There is no device mention, generic computing hardware, camera instruction, blue percentage, or automatic no-device clause. A useful KSP can survive as a material/activity cue: lesson preparation may become a worksheet edge rather than a classroom full of furniture. Additional prompts still require distinct useful KSP cues; camera adaptation does not multiply the prompt count.

The complete prompt embeds camera knowledge; product-name lookup tables were removed after the final user decision. Prompt length is an integration cost, not a latency measurement. Actual request latency and usage belong in the raw text-evaluation records. The local compiler creates one reproducible prompt from the template and registry; manual edits to the compiled output are not the source of truth.

## Evaluation

The first exploratory batch is preserved under `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/experiments/initial_mislabeled_messi`. It ran 22 actual GPT-5.5 requests covering all nine source JSONs and returned 35 prompts. All camera lookups and strict schemas passed, but only **19/22** passed every audit: one value-proposition quote cited under the wrong copy-variant path and two incorrect nested `_chatSession` ignored-field entries. Its taxonomy and runtime product-name contract were superseded by Hooman's correction. It is not accepted evidence for the final type-only V2.

The first type-only batch is separately preserved under `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/experiments/type_camera_r3`: 24 requests, 39 prompts, all type-camera lookups correct, and 23/24 complete audits passed. Its sole failure quoted text found in `ValueProposition.short_message` but cited `ValueProposition.long_message_best_sku`. The text was present in the source; its citation path was wrong.

The revised prompt explicitly requires short verbatim spans from one selected source field, checks within that field rather than across variants, and requires the top-level `_chatSession` ignored-field marker. The active revised 24-case batch covers all nine production inputs, compact tag spelling and explicit old aliases, laptop/printer/miniPC framing, source/type disagreement, sparse input and unregistered types. Inputs now contain only source messaging and camera tag. Full requests/responses and validation remain separate from the superseded run.

Acceptance requires valid output JSON, exact source-evidence quotes, correct mappings, correct type-camera resolution, no device/camera specifications in prose, and manual scene-scope review against the offline references. Text checks do not establish camera preservation in downstream images. The completed current batch used prompt SHA-256 `00912f74c3ef11dece81c7e3ba7792ffafdf9f3fb12a2330923dd16c75dbd65e` and returned `gpt-5.5-2026-04-24`. It covers all nine distinct production sources plus camera/control cases. **VERIFIED for these saved calls:** 24 selected cases, 39 prompts, 26 successful model responses, 27 transport attempts, and one transient retry. All 24 selected outputs passed automated checks and root scene review; no selected citation needed repair.

The two initial scene rejections are preserved: case07 requested three nearby objects under a two-prop profile, and case19 added a phone. Separate same-prompt retries passed review. Case07 also cited a valid value-proposition quote under the wrong copy-variant path. The initial 24 responses passed 22/24 raw automated audits; deterministic citation-path normalization raises that to 23/24, but does not fix the scene-density failure. The final 24 selected samples are therefore **not a claim of 100% first-call reliability**. The false positive for “wooden desktop” was corrected in the validator because it describes the support surface, not a computer.

A small deterministic guard checks citation paths against the original source JSON. It changes only a wrong field path when the unchanged quote matches exactly one field in the same intended KSP or value proposition. Missing, ambiguous, or wrong-scope evidence remains a failure. Raw model responses stay untouched; repairs have a separate audit. This is a recommended runtime integration guard, not an additional model call. Object counts still require semantic review.

Selected outputs consumed 391,195 reported tokens and 510.446 seconds of summed request latency. This is the sum across 24 selected calls, not wall-clock batch duration or an image-generation measurement. Most medium samples use their full two-prop/one-background ceiling; that may still be too demanding for some views and needs image testing.

Evidence: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/eval/current/accepted_samples.json`, `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/eval/current/accepted_validation.json`, `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/eval/current/manual_review.json`. The full review at `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/eval/current/review.html` includes all selected prompts, complete inputs, camera references, source debug, raw API records, and preserved rejected attempts. Its camera images are human-review references only; none were sent to GPT-5.5.

## Reproduction and update procedure

Draft files are under `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2`:

- `system_prompt.template.md`: root-authored behavioral instructions.
- `camera_profiles.json`: versioned type-camera limits, supported types and explicit camera aliases.
- `build_system_prompt.py`: deterministic compiler; `--check` verifies the compiled file is current.
- `system_prompt.md`: self-contained system message to send to GPT-5.5.
- `input.schema.json` and `output.schema.json`: input envelope and strict response contract.
- `camera_profile_resolver.py`: deterministic offline reference for test validation.
- `test_camera_profile_tools.py`: bounded registry/compiler checks.

```bash
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/build_system_prompt.py
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/build_system_prompt.py --check
python -m unittest discover -s /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2 -p test_camera_profile_tools.py
```

For a renamed camera with identical geometry, add an explicit alias to the existing canonical tag. For a new view, new device type, or changed reference render, inspect it offline, preserve its source hash, update the conservative type-camera profile, increment the registry version, compile, and run the affected text checks. Do not map a new view to the nearest name without review. Updating a preset image without updating its versioned notes is a known staleness risk.

The execution target remains the requested deployment `gpt-5.5`, medium reasoning, strict JSON Schema, 8000 maximum completion tokens, and no explicit temperature. Preserve the returned model identifier rather than assuming it equals the public default snapshot. Official model capability reference, retrieved 2026-10-22: https://developers.openai.com/api/docs/models/gpt-5.5 . The public page supports Chat Completions, structured outputs and medium reasoning; the authorized Azure deployment's actual response is the run-specific evidence.

## Limits and next decision

V2 is an environment writer, not a camera lock. The downstream rewriter also has to preserve the selected view. In the historical flagged `baseline-0018` output, the downstream rewrite asks for exact product scale while independently adding wide-angle/high-angle composition and several furnishings. That is a plausible conflict; the saved evidence does not isolate causation. The separate `baseline-0016` laptop/printer mismatch was a confirmed client upload/cache mistake affecting eight rows, not evidence against this framing hypothesis. See `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/reference_integrity_v1/SUMMARY.md`.

After text review, the cheapest informative image experiment holds the reference bytes, output dimensions, seed and downstream settings constant while comparing V1 and V2 environment text on tight, medium and wide presets. Keep the downstream rewritten prompt with each result. If the downstream rewriter reintroduces room inventories or changes angle despite simpler V2 input, compare a rewrite constrained to the selected camera separately before attributing improvements or failures to the environment writer. Hooman subsequently authorized the full current-render evaluation while text review proceeds. It is now running at https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_camera_v2_eval_20261022/generated_v2/gallery/index.html; scope and live status are recorded under `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_camera_v2_eval_20261022`. This has different references and aspect ratio from historical V1 and is not a controlled paired A/B.

A later V3 can compare runtime image analysis with the offline profiles. Camera names and approval status remain changeable; explicit aliases and registry versions support updates. The application must supply the correct device type: V2 has no image or product-name input with which to detect another upstream mislabel.

Published camera-V2 text review: [https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_camera_v2_text_review_20261022/gallery/index.html](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_camera_v2_text_review_20261022/gallery/index.html). New prefix; historical galleries unchanged. S3 byte/content-type verification is recorded at `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/eval/current/publication/publication.json`; authenticated browser rendering was not performed.

## Current image evaluation, authorized2026-10-22

Same nine production messages,202 current laptop/printer renders, no miniPC,369 distinct source/tag calls before exact reuse,729 source/render pairs before prompt multiplicity. All references preserve16:9, with2560×1440 outputs,50steps, seed42 and Gemini3.1Pro rewrite. Source/tag generation is reused across same-tag renders; exact prior accepted calls may be reused only with identical input/system/schema hashes.

VERIFIED smoke finding: the tight-printer environment prompt contains no props, but downstream usedPrompt explicitly adds a paper stack and succulent; both appear in the generated result. This directly demonstrates scene expansion in the downstream rewriter for that case. It does not prove resulting camera drift. The client binding and native image dimensions passed checks. Evidence and raw record links: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_camera_v2_eval_20261022/smoke_review.json`.

The new run is in progress, not accepted as a camera-fidelity result. Live gallery: [https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_camera_v2_eval_20261022/generated_v2/gallery/index.html](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_camera_v2_eval_20261022/generated_v2/gallery/index.html).
