# Project State

## Status

Dataset discovery and the expanded GPT Image 2.5 POC batch are complete as of 2026-10-07. The current gallery has
22 generated lifestyle assets across three product families, with explicit provenance labels for every comparison image.

## Inputs reviewed

- User-provided ticket text and scrape summary.
- Research operating playbook.
- THD image/video generation context and managed-services architecture.
- Top-level S3 inventory for `scraped_from_kdp_website/`.
- All three canonical CSVs and the 34-page supplied PDF.
- All 170 curated pair assets, all 86 reference instances, and all non-video focus-SKU assets.
- Manual contact-sheet review of all 44 paired product/color variants.
- Official OpenAI GPT Image 2.5 model and image-generation documentation.
- Existing Foundry `naou_image` GPT Image 2.5 Sunburst transport implementation.

## Confirmed inventory snapshot

- `1_lifestyle/`: 3,139 objects, 447,064,702 bytes.
- `2_reference/`: 86 objects, 19,530,089 bytes.
- `3_pairs/`: 170 objects, 50,971,292 bytes.
- `4_index/`: 914 objects, 7,234,949 bytes.
- `focus_skus/`: 204 objects, 187,310,217 bytes.

These object totals include non-image files such as `.DS_Store` and must be normalized before comparison.

## Completed batch

- Reconciled the ticket counts and S3 object structure.
- Identified and documented label inflation in the curated pair set.
- Assessed both ticket SKUs.
- Ranked initial POC candidates.
- Built a 52-image local candidate gallery with manual accept/proxy/exclude labels and exact S3 URIs.
- Published the candidate gallery to Foundry S3 with IMS authentication.
- Verified `foundry-aws-gateway 2.0.0` can retrieve direct OpenAI credentials from this Pluto VM.
- Generated and visually compared the first K-Express Sunburst lifestyle output.
- Expanded the POC to six Sunburst/high outputs across K-Express Black, Mini Mate Plus Warm Stone, and K-Supreme
  Gen 2 Black, including two human/button-interaction scenes.
- Updated the same IMS-authenticated comparison gallery with five clean generation inputs, six generated outputs,
  six exact-SKU held-out real lifestyle images, one labeled cross-color proxy, and all six full prompts.
- Validated all 18 referenced S3 image objects and the gallery HTML/JavaScript/CSS content types.
- Expanded the displayed POC to 22 generated lifestyle assets: seven K-Express Black, five Mini Mate Plus Warm
  Stone, five Mini Mate Plus Matte Black, and five K-Supreme Gen 2 Black outputs.
- Added more human interactions and materially different environments, including text-only red/pink scene matches.
- Removed the Mini Mate synthetic-black-reference experiment from the displayed gallery after confirming a genuine
  clean Matte Black reference for SKU `5000390176`.
- Added five Matte Black lifestyles made only from that genuine reference: botanical sunroom, lavender studio,
  yellow/cobalt tabletop, lavender mug placement, and yellow/cobalt button press.
- Published the 22-output revision to the existing Foundry S3 URL. Validated all 37 unique image references, all
  22 full prompt blocks, absence of the synthetic-reference artifact from the HTML, and correct HTML/JavaScript/CSS
  content types.
- Consolidated the dataset, generation procedure, credentials flow, prompts/outputs, published gallery URLs,
  findings, limitations, and evaluation rules into `PROJECT_NOTES.md` and durable shared memory.
- Verified from source that `fe-html` supports one-image custom classification, reviewer-attributed publishing,
  CSV export, and aggregate summaries, but its default path/filename labels and sorted order are not blind-safe.
- Built and published a stock `fe-html` blind pilot with 14 opaque normalized candidates, balanced 7 real / 7
  generated within SKU. Each row includes the clean SKU reference image(s); the private truth map was not uploaded.

## Current assumptions

- `[USER-CONFIRMED]` “Other selected SKUs” means the evidence-ranked K-Express Black, Mini Mate Plus Warm Stone,
  and, if bounded generation permits, K-Supreme Gen 2 Black.
- `[ASSUMED]` Real lifestyle images should remain evaluation holdouts and must not be passed to the generation
  model. This preserves a clean real-versus-generated comparison and is falsified only if Hooman explicitly asks
  to use them as style references.
- `[ASSUMED]` A small matrix of distinct scene archetypes is the cheapest next validation; breadth is more useful
  now than many seeds of the same prompt.
- `[USER-CONFIRMED]` Human interaction should include believable product use, such as pressing a control.
- `[USER-CONFIRMED]` The next batch should increase environment and interaction diversity for all three active
  SKUs and improve on the AI-looking hand in the first K-Express interaction output.
- `[ASSUMED]` Textually describing the red/pink visual setting without sending the lifestyle pixels to the model
  satisfies the requested scene-matching experiment. Because those images informed prompt design, they are labeled
  prompt-inspired comparisons rather than pristine blind-test holdouts for that scene.

## Corrected assumptions

- `[VERIFIED]` A clean real Mini Mate Plus Matte Black reference already exists for SKU `5000390176`; the initial
  premise that a synthetic black reference was needed is false. The user subsequently removed that experiment from
  the displayed gallery in favor of genuine-reference Matte Black generations.

## Blockers and limitations

- Standard brokered AWS credentials were unavailable because the machine lacks a configured Pluto token.
  Hooman explicitly supplied temporary Klam credentials at an external untracked path; values were not printed.
- The local `managed_services` checkout is 367 commits behind `origin/main` and contains pre-existing edits.
- The original `foundry_aws_gateway` preflight used version 1.6.0 and returned HTTP 403. An isolated Python 3.12
  environment with version 2.0.0 sends the required policy acknowledgement and successfully obtains a direct
  OpenAI client from the Pluto-injected token. No user-supplied OpenAI credential is required.
- The first K-Express Sunburst smoke output completed with strong scene realism and promising preservation of the
  supplied brewer, controls, reservoir, cup, wordmark, and overall geometry. Subtle SKU-level review remains.

## Next exact step

Have the C-Tech reviewer complete and publish the 14-row pilot, then compare their answers with the private truth
map and report accuracy, uncertainty if collected, and errors by SKU/scene.
