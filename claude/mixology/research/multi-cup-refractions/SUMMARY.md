# Multi-cup refraction refinement

As of 2026-10-20. This topic tests why the user-approved corrected V3 three-cup result has a stronger focal hierarchy than the later joint composition/refraction outputs, and refines the treatment on both a three-cup and a five-cup arrangement. No result is customer approval.

## Contents

- [Decision and scope](#decision-and-scope)
- [Standalone three-cup selection gallery](#standalone-three-cup-selection-gallery)
- [Visual rubric and stopping rule](#visual-rubric-and-stopping-rule)
- [Competing hypotheses and controlled design](#competing-hypotheses-and-controlled-design)
- [Execution checkpoint](#execution-checkpoint)
- [Evidence and limitations](#evidence-and-limitations)

## Standalone three-cup selection gallery

Published a separate review page for choosing among the strict two-stage three-cup outputs. The eligible selection set is exactly `i02_trio_two_stage_origstyle`, `i05_trio_two_stage_benchmark`, and `i07_trio_two_stage_focusclause`. The page shows their shared neutral target, exact style reference, generated output, complete system/user/image prompts, generation settings, hashes, and independent critique. A browser-local picker lets Hooman mark and copy a choice.

`i09_trio_floor_correction` is shown in a clearly separated three-stage follow-up section because it passed the research gates but is not a strict two-stage result. `i01_trio_one_stage_origstyle` is collapsed context only and is not selectable.

Standalone review URL: `https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/mixology/refraction_research_2026-10-19/trio-two-stage-selection/gallery/index.html`.

VERIFIED publication: a new, previously empty S3 prefix received 47 objects / 20,507,569 bytes with no deletion or overwrite. Every uploaded object passed authenticated byte-for-byte SHA-256 readback with explicit MIME types. Local Chromium rendered all 20 review images, exercised the picker and lightbox, and passed desktop/mobile overflow checks with no JavaScript errors or failed requests. IMS was mocked only for local rendering; a live signed-in gateway-browser session remains unverified because direct HTTP access to the corporate gateway timed out from this host.

Durable package: `/home/colligo/mixology_data/refraction_research_2026-10-19/trio-two-stage-selection`. Publication receipt: `/home/colligo/mixology_data/refraction_research_2026-10-19/trio-two-stage-selection/_review/publication.json`. Local browser validation: `/home/colligo/mixology_data/refraction_research_2026-10-19/trio-two-stage-selection/_review/local_validation.json`. Reproducible builder, validator and publisher are under `/home/colligo/hs_scripts/claude/mixology/research/multi-cup-refractions/scripts`.

## Decision and scope

USER-CONFIRMED benchmark: `/home/colligo/mixology_data/refraction_research_2026-10-19/runs/v3corrected_group_clean/output.png` (SHA-256 `1a9d467398531b35f24dda74c281e5a872a77ce2b4a167aee7f8ef94efd22d60`). The desired morphology is a concentrated bright central area that branches outward irregularly, with the visual energy of a lightning impact but rendered as photographic transmitted light, never literal electrical bolts.

USER-CONFIRMED failures: `/home/colligo/mixology_data/refraction_research_2026-10-19/combined/runs/v1_trio_orange_front/output.png` and `/home/colligo/mixology_data/refraction_research_2026-10-19/combined/runs/v1_five_staggered/output.png`. Veins, spiderwebs, mesh, waves, uniform cellular coverage, regular starbursts and global glow are failures even when drink colors are correct.

The experiment may spend at most 20 candidate image generations total. Every attempted image POST counts conservatively; critiques and prompt rewrites do not. All attempts will remain visible in the new `multi-cup-refractions` gallery tab. Stop early only when direct visual inspection and an independent fresh-context `gpt-6-astra` judge with `reasoning={"effort":"high"}` support every essential gate for both a three-cup and five-cup arrangement.

## Visual rubric and stopping rule

Essential gates for each arrangement:

1. **Dominant focal hierarchy:** each important cup-derived field has a clearly dominant compact bright concentration; the eye is not pulled equally across the whole pattern.
2. **Irregular outward branching:** a small number of primary branches leave the focal concentration, split irregularly, taper and lose energy; secondary detail is sparse and subordinate.
3. **Photographic optics:** the effect reads as focused transmitted light grounded on the receiving plane, not drawn lightning, a decorative starburst, white fog, or generic glow.
4. **No dominant network:** uniform cellular mesh, waves, veins or spiderweb coverage cannot be the main morphology. Fine secondary texture may exist only when visibly subordinate to the focal hierarchy, as in the benchmark.
5. **Subject fidelity:** preserve cup count, arrangement, upright grounding, source proportions/contents and opaque cream; do not solve the lighting by redesigning drinks.
6. **Color attribution:** each field inherits its transmitting drink's hue and opacity; dark/opaque drinks transmit less; colors mix only at plausible overlaps.
7. **One coherent setup:** one shared key and compatible downstream projection direction; fields remain attached to their cups and the support plane; no invented wall projections.

The Astra scores are advisory. `overall_pass` is accepted only when its concrete evidence agrees with direct image inspection. A result may be retained as best-so-far without passing.

## Competing hypotheses and controlled design

OBSERVED, 2026-10-20 direct inspection:

- The benchmark has hot focal concentrations below the magenta, cyan and coral cups, with bright unequal trunks and outward branches. It also contains fine mesh; user approval therefore distinguishes **hierarchical branching with subordinate mesh** from a blanket absence of all small lines.
- The two failed combined outputs spread similarly weighted cellular/ripple lines through most colored footprints. They lack a strong compact-to-tapering energy hierarchy. The five-cup failure also repeats comparable caustic density across several fields.
- The existing neutral composition outputs preserve the requested arrangements without committing the relighting model to reconstructing cup identities and lighting simultaneously.

ASSUMED hypotheses, tested without claiming causation from one stochastic output:

1. **Task-load hypothesis:** one-stage composition plus relighting asks Sunburst to synthesize identity, arrangement, scale, direction, color and morphology at once; the longer combined prompt may satisfy “caustics” with a generic repeated texture. A two-stage edit of an already composed neutral target reduces that load. Test: same direct route, Astra-high rewriter, model/quality/size and style reference; compare one-stage and two-stage pipelines on both arrangements.
2. **Style-evidence hypothesis:** prior combined runs used customer image 027 as style input, not the exact now-endorsed V3 output. The benchmark carries the requested focal hierarchy more explicitly. Test: in the two-stage pipeline, change only the style input from customer 027 to the exact benchmark.
3. **Prompt-density hypothesis:** the combined rewrite is roughly twice the length of V3 and balances many constraints; morphology language may lose salience. If needed, add one compact morphology clause to the exact V3-derived relighting workflow, leaving target, style, route and settings fixed.
4. **Stochastic alternative:** any single difference may be sampling variation. Paired results narrow plausible causes but do not prove them; repeat only where the next sample has high information value within the 20-image ceiling.

Planned wave 1 is four direct-route candidates: one-stage and two-stage for the trio, then one-stage and two-stage for the five-cup scene, all using customer 027 as the unchanged style reference. Planned wave 2 changes only the two-stage style reference to the exact approved benchmark for both arrangements. Later candidates are chosen from the independent judgments and direct reviews, one prompt factor at a time.

## Execution checkpoint

Status: waves 1–2 complete. Generation count: **6 / 20 attempted and completed**. Every candidate has a fresh-context Astra-high judgment with returned model `gpt-6-astra`, completed status and request metadata. No essential-gate pass yet.

OBSERVED wave 1: the two-stage candidates preserve the neutral arrangement and coherent projection direction better than the one-stage candidates on both three and five cups. All four still fail focal hierarchy, irregular tapering branches and no-dominant-network. Therefore the controlled results support joint task load as a contributor to composition/direction drift, but not as a sufficient explanation of the mesh morphology. Single stochastic samples prevent stronger causal wording.

OBSERVED wave 2: changing only the two-stage style input from customer image 027 to the exact user-endorsed V3 output did not remove the mesh on either arrangement. The trio gained a small bright base concentration and the five-cup result retained several local knots, but similarly weighted closed-cell connections still dominate most footprints. The style-reference mismatch is therefore not sufficient by itself; copying the benchmark can also copy its subordinate mesh without reproducing its hierarchy.

Actual Astra-high prompt consultation returned one smallest-delta clause: require one compact dominant concentration per existing field, only a few unequal open-ended branches, broad low-intensity gaps, and explicit rejection of starburst/bolt/glow/fog/wave/vein/cellular mesh. Wave 3 appended only this two-sentence clause to the byte-frozen V3 copy, while retaining the same neutral targets, exact benchmark style input, direct route and image settings. The original V3 remains byte-identical.

OBSERVED wave 3: the clause reduced some peripheral density and produced local bright knots, but fresh Astra-high judgments still failed focal hierarchy, irregular branching and no-dominant-network on both arrangements. Exposed fields retained repeated closed cells and competing intersections. Generation count: **8 / 20 attempted and completed**.

Wave 4 is explicitly a three-stage pipeline test: use each wave-3 result as a new edit target and change only its projected-light layer. The correction prompt preserves every cup, field hue, shadow axis and projection direction; removes closed loops; requests one compact core plus two to four unequal branches that may split once but never reconnect. The exact benchmark is morphology-only guidance. This is not represented as the original two-stage V3 pipeline. Next exact step: run and judge `i09_trio_floor_correction`, then `i10_five_floor_correction`.

## Final outcome at the generation ceiling

Generation stopped at **20 / 20 candidate image-generation CLI jobs**, all of which completed and produced one retained image. This count is a job/invocation count, not a claim about exact wire-level POST count: the unchanged bundled CLI uses OpenAI SDK defaults, whose internal retry behavior was not inspected. No orchestration-level image retry occurred under an existing candidate ID.

Every candidate received an independent fresh-context direct Responses judgment. VERIFIED returned metadata: 20/20 report model `gpt-6-astra`, status `completed`, unique response/request IDs and `reasoning={"effort":"high"}` in each saved request; combined returned usage reports 27,277 reasoning tokens. This proves the requested Astra-high route was used, not that its subjective scores are calibrated.

Best three-cup result: `i09_trio_floor_correction`. Direct inspection agrees with the independent judgment's `overall_pass=true`: compact bright concentrations dominate; a limited set of unequal branches taper outward; the optical effect is grounded and photographic; remaining fine crossings are subordinate; drink identity, colors, shared lower-left projection direction and clean background pass. Advisory scores: morphology 4/5, fidelity 5/5, color 5/5, direction 5/5. This is a researcher stop-criterion pass, not customer approval.

Best five-cup result: `i12_five_global_focus_nostyle`. It is the strongest compromise, not a pass. Direct inspection and Astra-high agree that it clears focal hierarchy, no-dominant-network, photographic grounding, subject fidelity, color attribution and coherent direction. It fails the required irregular-branch gate: the dominant core resolves into broad X-like crossing bands with little local splitting or progressive narrowing. Advisory scores: morphology 3/5, fidelity 4/5, color 4/5, direction 5/5. Later attempts either restored network/veins, produced smooth glowing ribbons, or became thin electrical-looking streaks.

The user-specified early stop condition was therefore **not met on both arrangements**. The ceiling, not success, ended generation.

## Diagnosis

SUPPORTED with moderate confidence inside this purposive sample:

- The one-stage joint task contributes to composition and direction drift. Matched direct-route controls preserved the neutral arrangement and one projection direction more reliably when relighting was separated from composition.
- Joint task load is not sufficient to explain the morphology regression. Both one-stage and two-stage V3-style candidates retained dominant mesh in wave 1.
- Supplying the exact approved V3 output as style input is not sufficient and can reinforce its subordinate fine network without transferring the desired brightness hierarchy.
- The most reliable route for the trio was explicitly three-stage: neutral composition, V3-derived relight, then a floor-light-only topology correction. It must be labeled that way rather than promoted as a one-stage or frozen-V3 result.
- Five simultaneous cup fields create a crowding problem in this sample: per-cup foci overlap into networks, while consolidating to one global focus often collapses into an X/star or smooth glowing ribbons. Removing the benchmark input suppressed mesh but weakened photographic irregularity.

NOT PROVEN: a single causal root, provider-wide behavior, generalization to other arrangements, or a robust production recipe. Every condition remains one stochastic output except two exact-prompt five-cup repeats; those repeats varied visibly and neither passed all gates. Different products, geometry and exposed receiving-surface area remain confounds.

## Remaining blocker and next validation

The unresolved five-cup blocker is topology: keep `i12`'s compact dominant focus and quiet fields while replacing its smooth X-like bands with a few photographic, locally splitting, rapidly tapering branches—without restoring mesh or creating electrical cracks/ribbons. Further generation is prohibited by the current 20-image ceiling. Any future work requires a new user-authorized budget and should start from `i12`, not rerun completed IDs.

Publication completed under the shared gallery lock. The new `multi-cup-refractions` tab contains all 20 ordered attempts, complete generator prompts and ordered inputs, outputs, hashes, and fresh-context Astra-high requests/critiques. The locked pre-merge baseline was 888 objects / 199,627,863 bytes. The final live package is 1,133 objects / 246,259,802 bytes: 245 new objects, four expected changed shared files, and zero removals. All 1,133 objects passed authenticated S3 byte readback; all 55 pre-existing output images remained byte-identical. Local browser validation checked 1,813 relative links, tab/deep-link/keyboard/lightbox behavior, desktop and mobile layout, and no JavaScript errors. IMS was mocked only for the local browser test; no live signed-in gateway-browser claim is made.

Published URL: `https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/mixology/refraction_research_2026-10-19/gallery/index.html#multi-cup-refractions`.

Canonical plan: `/home/colligo/hs_scripts/claude/mixology/research/multi-cup-refractions/cases.json`. Reproducible runner: `/home/colligo/hs_scripts/claude/mixology/research/multi-cup-refractions/scripts/run_refinement.py`. Machine-readable journal: `/home/colligo/hs_scripts/claude/mixology/research/multi-cup-refractions/iteration_journal.json`. Durable run root: `/home/colligo/mixology_data/refraction_research_2026-10-19/multi-cup-refractions/runs`.

## Evidence and limitations

VERIFIED storage scope: repository real path `/home/colligo/hs_scripts`; durable data root `/home/colligo/mixology_data/refraction_research_2026-10-19`; both are physically under backed-up `/home/colligo`. `/mnt/localssd` is not the sole location of any needed artifact.

VERIFIED model route before this batch: Foundry-vended direct OpenAI credentials, backend `https://api.openai.com/v1/`, exact `gpt-image-2.5-sunburst` synthetic edit success. Current batch must re-record actual response metadata for every Astra-high call and use the unchanged bundled imagegen CLI for image POSTs. The CLI does not expose the image response request ID or returned snapshot; this limitation remains explicit and no uncertain POST is automatically duplicated.

Source quality limitation: supplied arrangement examples and neutral compositions are internally generated, not customer-approved outputs. The benchmark is user-approved for positive visual comparison in this task, but the experiment does not establish general optical accuracy, production robustness or customer acceptance.
