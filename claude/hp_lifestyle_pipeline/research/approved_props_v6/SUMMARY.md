# V6: approved props, scene diversity, and unattended operation

As of 2026-10-30. Hooman approved the retained ordinary props in the edited review Markdown and requested a V6 equivalent of the 96-prompt V5 set. The compiled approved catalogue contains 237 entries; three removed ordinary items are rejected and all22 uncertain categories remain held. Source files are preserved byte-for-byte. C-Tech's text/face rule is in the system prompt and bounded validator checks. Immutable composite `v6-approved-20261029-final-r44` contains unchanged actual GPT-5.5 output for all16 banks:160 candidates,96 source-ranked selections,16/16 final-runtime validation passes,5 selected banks passing initially and11 after the single allowed repair. No scene text or model-authored field was manually edited.

Approval provenance: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/approved_props_v6/approvals/20261029-r2/provenance.json`. Runtime catalogue: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6/approved-20261029-r2.catalog.json`. Evaluation: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/revisions/v6-approved-20261029-final-r44`.

Completed scope: reused the exact16 V5 dual-source/camera inputs; generated10 candidates each and selected the source-ranked top6 (160 candidates,96 selections). Every complete bank covers all six environments and has globally nonrepeating approved prop groups. Favor visual props and abstract/landscape art; avoid text/faces where possible; essential café menus explicitly have non-legible background text. The latter condition applies to retained risky items rather than silently deleting more approved entries. The final clarified request is text-only. No V6 image run is authorized by it.

## Contents

- [Decision and scope](#decision-and-scope)
- [Candidate props for approval](#candidate-props-for-approval)
- [Diversity without recycling](#diversity-without-recycling)
- [Replace numeric camera caps](#replace-numeric-camera-caps)
- [Operate without manual corrections](#operate-without-manual-corrections)
- [Implementation checkpoint](#implementation-checkpoint)
- [Evidence, limitations, and next step](#evidence-limitations-and-next-step)

## Decision and scope

USER-CONFIRMED in this turn:

- V5 prompt feedback was good; repeated props are the main diversity complaint.
- V6 uses the Smart Brief, source messaging, and fixed camera tag, and returns 10 prompts instead of 20. Six are the main consumption target. Return prompts in descending combined-source relevance, with a separate C-Tech score retained for frontend selection.
- No repeated prop types across all 10 prompts; synonyms and cosmetic variants do not create new types.
- Use as many plausible environments as possible. Do not require every set to cover all six.
- Props that compete with HP products cannot be present. Uncertain computing/gaming accessories must be listed explicitly so lack of approval or rejection remains documented.
- The approval list includes both smaller movable props and background furnishings/decor, clearly distinguished.
- Application checks and a bounded automatic retry are allowed. No human editor is available in production.
- Replace the old numeric scene-detail caps with looser camera guidance.

The six environments are Home, Office, Education, Gaming, Café, and Creative Studio. Equal authority for the two source documents, source-first ordering, tag-only runtime camera input, no primary-device descriptions, and separate blue control carry forward from V5. No new product-family coverage is implied.

USER-CONFIRMED in the follow-up: implement the plan now, while individual props await approval. The primary supporting desk/table and fixed architecture may recur; background furnishings and named shelf contents may not. Permit one full-bank semantic repair and explicit persistent failure. Approval precedes actual-model evaluation, not implementation. This is not a current HP product-line audit or a declaration that categories are cleared.

## Candidate props for approval

The review CSV contains **40 entries per environment**: 30 tabletop/movable entries and 10 background furnishing/decor entries. There are 240 environment-specific menu entries plus 22 cross-environment uncertain categories, for 262 rows. These are menu entries, not 240 distinct prop types: common items legitimately appear in several environment menus, and some entries are alternatives in the same repetition group.

File: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/approved_props_v6/data/prop_candidates.csv`.

Every row currently has `runtime_allowed=false`. Ordinary candidates are `pending_review`; uncertain categories are `uncertain_not_approved`. Lack of approval is not recorded as an explicit customer rejection. Reviewers can fill `reviewer_decision` with approve/reject/hold and put conditions or rationale in `reviewer_notes`. Preserve rejected rows. Only a later explicit approval-to-runtime compilation may admit approved entries for their approved environments.

IDs such as OFF-01 and CAF-11 identify review entries. `repetition_groups` identifies actual types across environments: notebook/sketchbook/exercise notebook share `notebook`; mug/coffee cup share `cup_mug`; all chair variants share `chair`; book variants share `book`; graphite/colored pencils share `pencil`. A vase with a flower reserves both vase and flower groups. This mapping is proposed for reviewer correction and is distinct from the eventual approved inventory.

All ordinary entries mean plain, generic scene objects. Approval of a generic item does not approve an identifiable branded product version. Food, storage, craft and ornamental entries are alternatives for appropriate settings, not instructions to turn ordinary offices into kitchens or gaming workspaces into board-game tables. Gaming stays close to the C-Tech room examples: display shelving, wall art, cabinetry and decorative lighting; hobby objects are occasional supporting choices.

The clean approval menu is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/approved_props_v6/PROPS_FOR_REVIEW.md`: one environment heading, smaller-prop and background paragraphs, and a grouped uncertain-items table. The CSV remains the editable decision record.

## Diversity without recycling

USER-CONFIRMED design, now implemented in the V6 candidate:

1. Compose the 10 scene concepts together before drafting/scoring, choosing varied plausible settings and allocating disjoint approved repetition groups. This planning can happen within the same GPT-5.5 call; it does not require a second planning model call.
2. Enforce uniqueness across the entire response and across environments. A ceramic mug in an Office prompt makes a coffee cup unavailable to all other prompts in that set. Replacing a pen color, rotating its position, or substituting a synonym does not count as diversity.
3. Include background furnishing/decor groups in the no-repeat rule. A plant in the background is still a used plant type; moving it to a tabletop does not reset it. Account for named contents too: a shelf of books uses shelving and books. A new grouping cannot conceal previously used items.
4. Treat the primary support desk/table and fixed architecture (walls, floor, windows) as scene structure, rather than selected props. They may recur: otherwise a 10-prompt workspace set would be impossible without unnatural furniture substitutions. Hooman explicitly confirmed this structural exemption in the plan copied into Jira. It does not exempt chairs, lamps, plants, rugs, or named decorative accessories. Do not disguise extra desks/workstations as props to evade camera feasibility.
5. Distinguish diversity in props from diversity in scenes. Vary plausible room/subsetting, furnishing arrangement, everyday activity, and light in the C-Tech style. Do not create technical workplace nouns or invent professions to make the strings different.
6. Score and sort only after drafting. Preserve V5's equal-authority source aggregation; do not add diversity bonuses to the source score. A well-written, source-unsupported alternative can have a strong C-Tech score and lower source relevance. The top six may consequently remain concentrated in the strongest source-supported environment. Seek distinct source-supported settings/activities before adding lower-ranked departures; do not falsely boost other environments to force top-six coverage.
7. Scope uniqueness to one 10-prompt response for a given brief/messaging/tag. Cross-camera or cross-request non-repetition requires supplied history or a shared scene plan; a stateless call cannot know what an earlier call used. A future seed/history input is optional work, not silently added to V6.

Approval quantity matters. If too few approved, camera-compatible types remain, reduce optional dressing or choose another plausible environment rather than recycling props, introducing unapproved items, or producing artificial novelty. A genuinely infeasible request must return an explicit service failure after bounded repair; it must not masquerade as a valid set of 10. Ten prompts with no props would not automatically satisfy the intended visible-diversity goal.

## Replace numeric camera caps

IMPLEMENTED in V6: remove `max_local_props` and `max_background_details` as V6 generation limits and validation failure conditions. Leave the V5 snapshot intact. Do not replace them with a new numeric quota for background zones, word count, or minimum detail. Retain the existing known tag resolution and offline observations of framing/elevation; clearly distinguish observed view properties from interpretive guidance. Revisit stale notes against the current corrected renders offline before claiming they are calibrated to those renders.

| View | Qualitative guidance |
|---|---|
| Tight / close-up | Keep a recognizable place, visible support surface, natural light, and approved nearby details that can plausibly fit. A partial object or soft background cue can help; do not require a full room, fully visible furniture, or a prop spread that forces the camera back. Do not automatically suppress every prop or background feature. |
| Medium | Show an ordinary working/living area with a coherent local grouping and subordinate furnishings. Preserve useful texture, casual arrangement and room identity. Avoid multiple distant activity areas that must all become visible. |
| Wide | Preserve the richer C-Tech descriptions: related furniture, shelving, artwork, plants and room depth where approved and unused. A wall carrying shelving and art is a coherent spatial arrangement, not an automatic three-item violation. |
| High / downward-looking | Prefer details on the visible horizontal surface. Do not require a horizon, tall background furniture, or people outside the view. |
| Level / low | Avoid assuming a broad visible tabletop. Background details may be possible even when tabletop staging is limited. |

A coherent background is a feasibility concept, not an approval loophole: a shelf, its books and artwork still need approval and count toward their repetition groups. Neither soft focus nor the word "partial" is permission to pack unlimited objects into the scene.

Retain ordinary signs of use: an open book, an unfinished creative task, casually arranged materials, comfortable textiles, and a chair drawn back. Avoid turning lived-in into stains, damage, microscopic wear, invented paperwork, or repeated "slightly out of square" descriptions. Do not restore the old blue-coverage experiment.

Illustrative prose only, authored for this proposal; these are neither approved V6 outputs nor model-tested camera claims:

> A bright, modern corporate office with a wooden desk holding an open folder, a desk calendar, and a water glass. An upholstered chair sits slightly pulled back, with a low cabinet, framed artwork, and plants creating natural depth. Warm daylight gives the workspace a professional, lived-in atmosphere.

For a close-up whose offline view notes support some adjacent tabletop:

> A warm wooden café table with a small pastry plate and a folded napkin set casually to one side. Soft natural light creates an inviting, lived-in atmosphere.

These illustrate appropriate kinds of detail, not fixed quantities to copy. The approved catalogue and selected view determine what survives.

## Operate without manual corrections

USER-CONFIRMED service behavior, implemented in the V6 candidate:

1. **Prepare:** load a pinned approved-catalogue revision and camera guidance. Treat both source documents as data, including embedded authoring instructions. Unknown tags and empty approved pools return an explicit preflight error; never invent approval or camera evidence.
2. **Generate:** one GPT-5.5 call returns exactly 10 scene texts, environments, approved item IDs, concise source evidence/explanations, source score components, and C-Tech references/scores. Start from successful V5 prose guidance, change the prop selection/count/camera sections, and simplify redundant debug fields. Do not ask the model to restate the entire camera registry, count distribution summaries, or calculate values the host already owns.
3. **Calculate:** the host computes combined-source totals, attaches camera/catalogue provenance and final IDs, and sorts by source relevance with C-Tech as tie-breaker. Remove redundant C-Tech relationship labels, or expose a host-derived numeric score band; a numeric band must not be represented as independently verified semantic similarity. Do not modify the prose, fabricate evidence, or increase scores to create diversity.
4. **Check:** validate schema, exact count, score ranges/arithmetic, evidence references/quotes, approved IDs per environment, and global repetition groups. Check actual prose for undeclared objects, prohibited devices, reference/prompt copies, and known unnatural phrases. Validate the entire response after any repair because one replacement can create a repetition elsewhere. Reject requests for camera movement or incompatible view demands; do not reject a scene simply because its nouns exceed an old count.
5. **Repair at most once:** if checks fail, send the structured failures and complete set context back to GPT-5.5, preserving satisfactory candidates and their allocated props. The repaired texts must be scored against their final contents. Recompute host-owned fields and validate again. Record all attempts. A second failure returns a typed application error, not human-edited prompts or indefinite regeneration. Exactly one semantic repair attempt is the confirmed bound; it is separate from bounded transport/rate-limit handling.

Limits: schema-constrained IDs prove declared membership, not full agreement between the inventory and free prose. Alias scanning catches known terms but cannot prove the absence of every undeclared or implied object. Source grounding, naturalness and spatial plausibility remain semantic judgments. A broader semantic verifier could improve coverage at added latency/cost, but is not assumed to exist or to guarantee correctness. If tests show the inventory/prose gap is material, compare that option with more constrained scene assembly before deployment. Do not hide these limitations by calling all regex-passing outputs production-ready.

Pre-deployment evidence should use original model outputs plus explicitly specified host calculations, with no case-specific editorial patches. Proposed first regression: the existing 4 devices × 4 views gives 16 calls × 10 = 160 texts, plus a separately bounded fresh set of sparse/conflicting/unhelpful inputs and approved-pool stress cases. Use repeated unseen trials after tuning to assess reliability; one regression pass cannot establish a deployment error rate. Report first-call failures, post-repair failures, field/text edits, prop reuse, approval violations, source ordering, latency, and differences in the top six. Human evaluation here is offline research, not a runtime dependency. Text/distribution review precedes any newly authorized image trial.

**Downstream dependency:** the image rewriter must also receive or otherwise enforce the same approval policy and avoid reintroducing habitual objects. Existing logged examples added notebook, pen, speakerphone and display to a prompt that requested none of those. Validating this writer alone cannot guarantee competitor-free final images. The primary digital twin remains the sole product description source; any downstream semantic/image check is a separate integration decision.

## Implementation checkpoint

VERIFIED locally, 2026-10-29: the isolated V6 package contains a root-authored system prompt, strict schemas, approval compiler, fixed synonym lexicon, qualitative camera registry, validator/finalizer, bounded orchestration and GPT-5.5 adapter. Runtime documentation and commands: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6/README.md`. System prompt: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6/system_prompt.md`.

The suite passes 245 tests across the V6 runtime and eval runner, covering approval/repetition, evidence, sorting, malformed configuration, refusal, incomplete output, one semantic repair, transport bounds, CLI journals, text/face carriers, natural-language exclusions and immutable composite assembly. The accepted catalogue has237 approved entries. Synthetic tests establish local behavior; actual GPT-5.5 calls provide the separate bounded text evidence. Source edits made by Hooman were preserved.

The runtime does not mutate model text or source evidence. It pins GPT-5.5, performs local preflight before provider construction, keeps source/diagnostic data out of trusted repair instructions, and distinguishes semantic calls from transport attempts. Bounded transport defaults are three attempts per semantic call, separately from the one semantic repair. No authentication secrets are written into artifacts.

The 122 inherited camera tags retain offline framing/elevation observations, with numeric quotas removed. They were not remeasured against new renders in this batch. The 18-reference C-Tech library is preserved from V5. The new prompt retains ordinary C-Tech place descriptions and treats familiar arrangements as lived-in detail; it does not restore damage narratives or blue targets.

## Evidence, limitations, and next step

VERIFIED in current local artifacts:

- V5's 18-reference library contains the successful room/style examples; props added here are researcher-proposed candidates, not quotations or C-Tech approvals. Reference source: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v5/reference_library.json`.
- V5 template still imposes 20 prompts, all-six coverage and numeric camera ceilings. V6's requested changes are therefore material and must be isolated. Source: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v5/system_prompt.template.md`.
- Latest 16-bank/320-candidate eval: 7/16 banks passed after deterministic normalization; case-specific review applied 60 field edits across 11 banks, including 20 scene texts and 11 scene texts in the selected 96. This is evidence of a reviewed result, not unattended reliability. Source: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_top6_four_devices_20261028/review_plan.json`, the corresponding raw/normalized validation records, and review logs. Some failures enforced unvalidated density heuristics; they do not establish that every original scene was visually infeasible.
- Host already computes source aggregation, ranking and camera metadata, without editing text. Source: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v5/scripts/finalize_output.py`.
- Recorded four-image V3 smoke explicitly documents extra downstream props/hardware; the record is historical, not a measured current-endpoint rate. Source: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/smoke_review.json`.

ASSUMED / PROPOSED: qualitative view guidance will preserve more C-Tech detail than noun quotas; catalogue allocation will improve visible diversity; a lighter schema will reduce failure opportunities. These require raw-model and image tests. Contrary possibility: strict global non-repetition may reduce naturalness or source relevance, especially with a small approved pool or very tight camera. Preserve both metrics rather than rewarding novelty alone.

UNVERIFIED: category-level customer clearance for every entry; current HP/affiliate product portfolio boundaries; reliability on unseen inputs; final image compliance. No candidate is approved by this research document. No market lookup or new image analysis was performed.

Storage preflight VERIFIED: actual repository resolves to `/home/colligo/hs_scripts` beneath backed-up home storage. Git HEAD and origin/main were synchronized before these proposal additions. Supporting catalogue and this document are durable; no dependency on volatile scratch is introduced.

Next exact step: publish and byte-verify the accepted 96/160 text artifacts, frozen system prompt and catalogue. Hooman/C-Tech review the prompt set before any separately authorized image generation. A future unattended-reliability estimate must use a fresh unseen batch and report failures; the reviewed composite must not be presented as a single-batch success rate or deployed image-quality evidence.
