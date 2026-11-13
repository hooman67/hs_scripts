# V6.3: HP product, environment, support and prop associations

As of 2026-11-10 UTC. **Isolated V6.3 implementation,160-text export and120-image exact-pipeline comparison are complete and published.** Frozen V6.2 runtime, prompts and historical images are unchanged. The original research rationale and proposed wording remain provenance; the current evaluation status below supersedes the earlier no-new-calls implementation checkpoint. Neither generation completion nor the unpromoted historical judge candidate establishes image-quality improvement.

## Contents

- [Implementation](#implementation)
- [Recommendation](#recommendation)
- [Confirmed boundaries](#confirmed-boundaries)
- [Evidence and limitations](#evidence-and-limitations)
- [Proposed prompt changes](#proposed-prompt-changes)
- [Props: reuse first, then a small approval list](#props-reuse-first-then-a-small-approval-list)
- [What not to import](#what-not-to-import)
- [Reproduction and next gate](#reproduction-and-next-gate)

## Implementation

**CURRENT EVALUATION:** Hooman authorized160 fresh V6.3 texts, a deterministic30-row coverage subset with rank-matched V6.2, and both writers on exact Adobe-Firefly/foundry#4523/#4417. The old V6.2 gallery is a V20/#4349 shape prototype, not current #4523; after that correction, the user authorized four fresh30-image cells (120 new), retaining old30 only as historical reference. Current study and executable orchestration: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_2_v6_3_pr4523_pr4417_20261109`.

The untouched r1 service completed15 successful banks and1 terminal false failure: "desk tray" was treated as a second desk/table, so the subsequent "the table" lost its primary-support exemption. R2 reuses the bounded accessory-suffix exclusion for antecedent detection while retaining checks on actual second tables/cabinets. All16 final actual responses now validate;195 affected tests and Ty pass. Original raw responses, automatic repair and failed service result remain preserved. No additional model calls or model-field edits were made for acceptance; this is not a fresh16/16 r2 deployment reliability trial.

**VERIFIED TEXT EXPORT:**160 unique prompts, SHA-256 `c0e7553848c3226a0bc3a83c24f161e6ff601ff76f8f0e0557f5bb5b317448c8`. Seed42 coverage selects30 across all16 banks and all6 environments, with exact V6.2 device/camera/rank counterparts. Full and selected JSON/TXT downloads, complete inputs and30 historical references are published at https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_v6_2_v6_3_pr4523_pr4417_20261109/gallery/index.html .

**VERIFIED IMAGE STUDY:** all four cells succeeded30/30, with120 unique known jobs/raw image hashes and zero failures. All120 actual prepared products, geometry guides and Astra style references are materialized and hash-bound. All60 remote product PNG bytes and productVersion values match the frozen local inputs. Native4523 request hashes bind its guide/reference bytes; the remote API exposes named input artifacts, not equivalent request-image hashes. No audit call invokes a model. Final publication verifies758 objects by downloaded SHA-256, bytes and content type. The sample is purposive and rank-paired, not semantically paired; style references and stochastic outputs are not pair-controlled. No comparative image-quality conclusion is claimed.

**JUDGE LIMITATION:** actual Astra-assisted V3.1 r1/r2 candidates remain unpromoted. The single six-case r2 calibration clears chair-offset placement but misses required laptop/table alignment and malformed-table failures; no full128 r2 run followed. The historical judge tab preserves128 frozen V3 results, six r2 results and122 explicitly blocked/null results, with the first candidate's separate full128 JSON also available. These are not judgments of the new120 images.

**USER-CONFIRMED 2026-11-09:** "This is good. Go ahead and execute the proposal." The user also requested removal of rock paperweights, permitting either proper replacements or complete omission. **IMPLEMENTATION DECISION:** omit all paperweights and loose decorative stones, not another decorative substitute. Approved stone coasters and furniture materials remain available.

**VERIFIED, offline scope:** runtime `v6.3-writer-runtime-r1-hp-associations` implements the compact device/environment guidance, explicit support/background relationships and no corpus-based source-score bonus. It preserves the input/output contracts, camera data, 18 C-Tech references, source scoring, bank-level diversity and bounded repair. There is no new runtime data source, model stage or input field.

The production catalogue is `hp-v6.3-approved-props-v1`, revision `v6.3-hp-associations-20261109-r1`: **265 entries = 260 baseline - one Office paperweight + six approved additions**. The Home stone arrangement was already absent from V6.2. All 259 retained entries are identical to the baseline.

| Approved ID | Environment | Concrete approval | Shared visual family |
| --- | --- | --- | --- |
| `V63-CAF-001` | Cafe | Closed unbranded bag or backpack | `laptop_bag` |
| `V63-EDU-001` | Education | Closed unbranded bag or backpack | `laptop_bag` |
| `V63-STU-001` | Creative Studio | Handmade ceramic cup/mug as studio work | `drinkware` |
| `V63-STU-002` | Creative Studio | Handmade ceramic bowl as studio work | `food_bowl` |
| `V63-STU-003` | Creative Studio | Handmade ceramic plate as studio work | `food_plate` |
| `V63-OFF-001` | Office | Unnumbered unbranded analog clock | `clock` |

Clock scope stays Office, bags stay Cafe/Education and vessels stay Creative Studio. The Office bag extension, calendars, electronics and broad "stock inventory" category were not added. The review CSV records both approvals and rejections. Removed paperweight/stone phrases remain recognizable without approval; catalogue loading also rejects attempts to reapprove them. The bag/clock treatment checks attach safeguards to their own noun rather than accepting a safeguard on a nearby book or other object. Printer support checks include pottery cups/bowls/plates.

Implementation paths:

- Runtime and usage: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_3/README.md`
- System prompt: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_3/system_prompt.md`
- Approved catalogue: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_3/approved-v6.3-20261109.catalog.json`
- Explicit decisions: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_3/approved_additions.csv`
- Reproducible builder: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_3/build_v63_catalog.py`
- Baseline/release hashes: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_3/assets_manifest.json`

Verification: **317 offline tests passed**. The affected runtime/CLI subset subsequently passed 38 tests after type-only annotations. Ruff correctness checks, Ty and the real catalogue-check CLI passed. All 28 frozen V6.2 source hashes match. The initial test run had 311 passes and one copied assertion expecting the old runtime suffix; the next had 314 passes and one new test expecting a shortened error code. Both assertions were corrected to the actual contract, with no production behavior weakened. The second run's failure record is preserved at `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_3/data/offline_tests_attempt2.xml`; the passing full run is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_3/data/offline_tests.xml`.

The default Python lacked Ruff and the gateway package; cached UV tooling supplied the existing dependencies. Initial Ty attempts could not discover UV-installed dependencies. Adding their actual installed source paths resolved import discovery; no type errors were suppressed. Two copied dynamic-call sites received proper dictionary annotations. These checks do **not** establish fresh GPT compliance or improved generated images. No deployment, publication, paid calls or changes to V6.2 outputs were made.

## Recommendation

**ORIGINAL RESEARCHER RECOMMENDATION, now approved:** make V6.3 an association-aware refinement, not a rewrite or a frequency-matching system. V6.2 already permits most of the useful furniture and objects in the report. Its main missing ingredient is explicit guidance connecting the device family, a recognizable subsetting, the main supporting furniture and a coherent choice of approved surrounding objects.

Add a short product/environment association section, keep all current safety/diversity/scoring controls, and seek approval for a few genuinely missing ordinary objects. Do not paste the raw SCAP captions into the prompt, automatically approve the report's inventory, or replace the 18 existing C-Tech prose references with caption-derived examples.

## Confirmed boundaries

**USER-CONFIRMED in the current thread:**

- V6.3 covers laptops and printers, not the other seven report device families.
- Use associations to enrich plausible choices, without matching observed frequencies.
- Recommend new ordinary props for explicit approval; hardware/competitor exclusions remain.
- Preserve the no-face boundary and conditional cropped hands/arms policy.
- Preserve V6.2's support-diversity floors: at least two round laptop tables per bank, every laptop Cafe candidate round, at least three printer support families and at least five non-table printer supports.
- The first step was reading/proposing only; subsequent explicit approval authorized implementation, as recorded above.

The existing ten-prompt contract, six environments, qualitative fixed-camera guidance, source-first ranking, independent C-Tech score, within-bank visual/phrase non-repetition, populated shelving, text safety and one complete-bank repair remain unchanged. No new product-name, image or user-history input is proposed.

## Evidence and limitations

**VERIFIED source retrieval:** the live index was retrieved through the Foundry gateway and matched the existing 1,940,512-byte local snapshot exactly: SHA-256 `0dd310ebd247626d36078abdad706ae8003afad75585d096d1bdee8c57e7349a`. The S3 object reports last modification `2026-11-07T05:23:28+00:00`. The standard credential helper had no Pluto token and the old AWS environment failed; the installed policy-aware Foundry gateway succeeded. No credential values are stored in these artifacts.

Primary supplied report:

https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/analysis/hp-lifestyle-statistics-all-devices-20261106/index.html

The original report and its downloadable extraction, statistics, placement audit, reconciliation, captions and relevant analysis source are preserved under this topic. All 150 laptop/printer device-profile and device/environment count comparisons were independently recomputed from the downloaded row records and matched the published statistics. This confirms aggregation consistency, **not caption accuracy or visible-image contents**.

| Report scope | Verified accounting | Implication |
| --- | --- | --- |
| Whole collection | 469 identities: 458 original no-person records plus 11 targeted original printer references | Not a random or independent population sample; do not use collection percentages as generation probabilities |
| Original cohort | 457 augmented images and one real image according to source metadata; existing Qwen captions with reviewed heuristic normalization | Not 458 independently visually validated original photographs |
| Laptop-containing scenes | 340: 337 original + 3 added; 319 primary/foreground, 12 mixed-focus, 9 secondary | Device-presence associations are broader than focal-laptop references |
| Printer-containing scenes | 25: 14 original + 11 added; 24 desktop-printer scenes and one industrial scene | Exclude the industrial machine when proposing desktop-printer supports |
| Printer roles | 14 primary, 9 secondary/background, 1 cropped secondary and 1 industrial | A background printer's room objects are not automatically props on its support |
| Added printer cohort | All 11 contain physical people, according to the report's fresh assistant visual inspection | Illustrates environments/relationships, not permission to add faces or people to our outputs |

**VERIFIED, caption-derived findings:** laptop environment labels include Home workspace 76/340, Office 72/340, Cafe 51/340, Library/shared study 9/340 and Pottery studio 8/340. These are normalized report categories, sometimes based on ambiguous caption alternatives, not newly verified physical locations.

Printer environment labels are Home workspace 13/25, Office 8/25, Library/shared study 2/25, Art/craft workspace 1/25 and Print workshop 1/25. The last is the industrial machine. The two library cases and one craft case are weak, small-sample inspiration, not strong general defaults.

**VERIFIED support relationships:** Home printer scenes use cabinet/console in 7/13 records. Across all printer-containing records, cabinet/console occurs in 8/25 and desk/worktable in 11/25. Removing the industrial scene leaves the same 8 and 11 counts among 24 desktop-printer scenes. The latter label merges ordinary desks and worktables: exact evidence includes occupied/shared desks, so it cannot justify relaxing our dedicated-support restriction. The report does not separately establish our fitted-counter or credenza diversity quotas.

The report's surrounding-object counts are image presence, not number of objects and not evidence that objects share the main support. Its material and support counts can be multi-label. "Not established" must remain unknown. Named product codes are not validated retail SKU identities, and a code in a printer-containing scene may identify its focal computer.

## Proposed prompt changes

### 1. Add compact, device-conditioned association guidance

**PROPOSAL:** add the following short section alongside the existing scene-planning instructions. The table below supplies its compact reference examples; it is not a new output schema or another model stage.

> Use the trusted HP product/environment associations to choose an ordinary subsetting, appropriate main supporting furniture, and a coherent selection of approved surrounding objects. Match the device family resolved from the camera tag; do not infer a product SKU from a caption code. Associations are descriptive options, not frequency targets, required bundles, approval grants, or source-score evidence. Preserve the existing environment labels and all support-diversity, camera, prop and phrase rules. Choose among compatible examples without reusing a reserved visual family. Borrow room character and useful object relationships, not every object, a caption's camera instructions, device configuration, people or color grade.

**PROPOSED compatible reference options:**

| Device and canonical environment | Subsetting/support options | Existing approved details to choose among | Evidence and qualification |
| --- | --- | --- | --- |
| Laptop / Home | Home study or work area; ordinary wood desk or suitable home table | Comfortable seating, populated bookcase, curtains, plants, unmarked paper material | Home workspace 76 records; desk 64/76; wood 58/76; shelving 39/76. Living-room references already exist, so no new sofa/pillow support permission is needed |
| Laptop / Office | Ordinary office or meeting area; desk or meeting table, including permitted round alternatives | Task seating, a safe-side drink, plain notebook, lamp or approved storage | Office 72 records; desk 61/72; separate meeting/conference category 8 records. These choices do not replace the round-table floor |
| Laptop / Cafe | Neighborhood cafe; required round table, with wood or another context-compatible material | Coffee cup, seating, plant, lamp or vase; select non-repeating approved families rather than requiring a cup in every cafe scene | Table 36/51; wood 36/51; cups 41/51; seating 38/51. Source counter examples do not override the round-Cafe rule |
| Laptop / Education | Library or study area; study table | Unmarked notebook, writing tool, populated bookcase or suitable chair | Library/shared study 9 records; table 8/9; notebook 8/9. Mapping to Education is our compatible taxonomy choice, not a claim that every reference is a classroom |
| Laptop / Creative Studio | Pottery or ordinary art/craft studio; suitable worktable | Approved palette/brushes, unlabelled pigment jars, ceramic samples; populated shelving where approved | Pottery 8 records, all with normalized ceramics/stock presence; art/craft 11 records, art supplies 10/11. Do not import machinery or all the stockroom props |
| Printer / Home | Dedicated storage-furniture station in a home workspace; substantial cabinet or low credenza, plus the required other support families | Neutral output papers or document box at a safe side; art, curtains, plant or lamp elsewhere | Home 13 records; cabinet/console 7/13; lamps 8/13; wall art 7/13; plants 6/13. Room presence does not put lamps/plants on the device support |
| Printer / Office | Wall-related equipment station; dedicated table, cabinet, credenza or fitted cabinetry under current rules | Output tray, plain papers or document box; populated storage, room lighting or glazing | Office 8 records, desk/worktable 7/8. Adapt room context without copying occupied workstation arrangements |
| Printer / Education or Creative Studio | Suitable library equipment station or separate studio output station | Approved storage and neutral output items; task props only in a clearly separate declared area | Library 2 records and art/craft 1 record are sparse. Retain as optional compatible extensions; do not copy the plastic-crate support |

For laptop Home/Office/Cafe, this is mainly selection guidance using already approved props. Pottery is a specific ordinary Creative Studio subsetting with stronger direct evidence than arbitrary decorative novelty. Do not silently map warehouses, hospitals, outdoor nature scenes or industrial printing into our six labels.

### 2. Make object roles explicit without adding a quota

**PROPOSAL:** tighten the existing printer/support and prop-allocation wording with one relationship rule:

> Keep primary support, neutral output items, separate task areas and background furnishings distinct. A surrounding object in a reference is not automatically on the main support. For printer scenes, retain clear standing access and a dedicated equipment surface; place unrelated activity materials only in a separate, approved and declared background arrangement. Describe useful relationships, not an inventory checklist.

This reinforces existing V6.2 behavior rather than reversing it. It introduces no numeric prop limit and does not require distant furniture in close-ups.

### 3. Keep corpus fit separate from source relevance and style scores

**PROPOSAL:** add one sentence to the scoring instructions:

> HP association evidence guides plausible scene construction only; it is not evidence from this request's Smart Brief or source messaging and cannot earn source-relevance points.

Keep the 18 C-Tech references and their existing score semantics. The new caption statistics support content choices, not a newly calibrated C-Tech or image-quality score. Gaming has no directly labeled environment group in this report; retain its existing C-Tech guidance rather than deleting it or inventing new empirical support.

## Props: reuse first, then a small approval list

**VERIFIED catalogue comparison:** the current catalogue has 260 environment-specific entries. It already covers ordinary notebooks/papers, writing tools, chairs, plants, lamps, shelves, storage furniture, art, curtains, drinkware, pastry plates, cafe vases and creative materials. Examples include `V61-CAF-001` (drinkware), `V61-CAF-005` (pastry plate), `V61-CAF-011` (flower vase), `V61-OFF-007` (document box), `V61-STU-003` (palette/brush alternatives) and `V61-STU-018` (closed pigment jars). Do not relist these as new approvals.

| Original candidate, now approved in the scoped form above | Why it is useful | Environment and conditions |
| --- | --- | --- |
| Plain closed bag or backpack | Missing from the catalogue; 17 laptop-containing records, including 10 Cafe and 2 library/study records | First propose Cafe and Education. Keep it closed, unbranded, beside seating or hanging safely from a chair; no visible devices, contents or obstructed access. One global bag family across variants. Office extension has only one direct report record and is lower priority |
| Plain handmade ceramic bowls, cups or plates as studio work/stock | All 8 pottery-studio records include normalized ceramic/stock context; literal rows 14, 48, 49 and 133 describe pottery vessels. Existing Studio entries mainly cover test tiles, glaze samples and pigment jars rather than this vessel stock | Creative Studio only, selecting a concrete form, not an unresolved list. Separate environment approval required. Use existing broad cup/drinkware, bowl and plate families as appropriate; populated shelving additionally reserves its own family. Do not create a "pottery cup" family to evade the existing cup rule |
| Simple unnumbered analog clock, optional lower priority | Three Office records explicitly name a clock: source rows 56, 379 and 415 | Office only initially, wall- or shelf/desk-mounted as appropriate, no readable numerals/brand. All clock forms share one family. This is a safe adaptation, not the exact caption wording; do not call the combined 8-record clock/calendar count eight clocks |

Do **not** add calendars now: five of the combined clock/calendar records are calendars, and exact captions include readable dates and a figurative image. Bags and studio vessels provide more useful new context with fewer text risks.

The ceramics/stock aggregate is not an approval category: outside pottery it includes cardboard boxes and other stock. Entries must name concrete ordinary objects. The three original candidate categories above became six environment-specific executable entries only after the user's explicit approval.

## What not to import

- No new monitors, keyboards, mice, phones, headphones, docks, chargers or other excluded hardware, despite their observed co-occurrence.
- No extra human faces, portraits, readable menus, screen contents, brand names, product states, device-hand interactions or product descriptions.
- No sofa/pillow/lap/crate/fragile shelf as a new primary support permission. Preserve the authorized support policy and fixed product geometry.
- No numerical clearance/height claims: the report contains no measured support capacity, safety dimensions or generation success rates.
- No raw camera, wide-angle, recentering, blue/teal grade or repeated SCAP phrase instructions. They can conflict with fixed view, separate blue control and phrase diversity.
- No forced corpus percentages, automatic approval from co-occurrence, or copying a whole reference bundle into multiple prompts.

**ASSUMED benefit, not demonstrated:** relevant scene associations and a few missing objects could make scene choices less arbitrary. They may also increase prompt complexity or cause repeated bundles. No new-model or image evidence establishes improvement yet. Existing global family uniqueness means, for example, that a cafe mug may reserve the same family that a pottery cup would need; the planner must choose rather than relax diversity.

## Reproduction and next gate

All paths below are absolute:

- Canonical proposal: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_3/SUMMARY.md`
- Preserved report: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_3/data/ctech_report.html`
- Supplied source index: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_3/data/source_manifest.json`
- Downloaded source evidence: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_3/data/upstream`
- Recomputed counts, row IDs, catalogue inventory and file hashes: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_3/data/evidence.json`
- Offline reproduction: `python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_3/analyze_reference.py`

**NEXT EXACT STEP:** run a separately requested fresh text evaluation on the same 16 input banks, preserving V6.3 runtime/assets, inputs, initial responses, one-repair/failure outcomes and final unchanged model prose. Compare useful scene associations without treating corpus-frequency matching as success. No evaluation or image generation is active. Images require their own requested scope and preserved generation lineage.
