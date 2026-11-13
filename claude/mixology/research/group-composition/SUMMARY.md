# Group composition without added refractions

As of 2026-10-20 UTC. Nine active composition outputs are complete through user-authorized FAL. Seven using the rejected leaned-back orange input have now been replaced with the new upright source, retaining their original systems, user prompts, slots and high/1536×1024 settings. The two cola/amber pairs are unchanged. No refractions are added in this tab. Joint composition/refraction now has its own separate third tab and `/home/colligo/hs_scripts/claude/mixology/research/combined-composition/SUMMARY.md`.

LATEST VERIFIED SOURCE REPLACEMENT: the new PNG is `/home/colligo/mixology_data/refraction_research_2026-10-19/assets/ref_inputs/TCCC–Crafted-Sept-2026.png`, SHA-256 `152427247d881087c4e7835408c9f76e28ca40929b0b2dc4e89542137db257da`. Seven group outputs and the same-source single-drink V3 output were replaced; every old run is hash-verified in the recoverable archive `/home/colligo/mixology_data/refraction_research_2026-10-19/_archive/composition_orange_source_replacement_2026-10-20T185455Z` (192 files / 16,060,514 bytes). Full queue IDs, source/output hashes and review evidence: `/home/colligo/mixology_data/refraction_research_2026-10-19/_review/composition_orange_source_replacement_2026-10-20.json`.

OBSERVED on direct review: the replacement orange stands upright and retains its concentrated upper red syrup, cream, taper and simple flat base. All seven keep their previous drink slots/count. Lineups still tend to make cola/orange bodies too slender/tall relative to their own sources; staggered layouts look more faithful but overlap limits contour checks. One Astra rewrite incorrectly called the new orange base a wide flared foot; this was corrected to “simple flat base” before image submission. Raw Astra output and the exact correction are recorded. No extra image or prompt-version revision was used.

USER-CONFIRMED PROVENANCE: supplied arrangement examples were generated internally and are NOT customer-approved outputs. Their spatial slots alone are useful; neither their cup geometry nor their refractions are targets. Two unexecuted old-source plans remain on disk but are hidden from the active gallery.

Review tab: https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/mixology/refraction_research_2026-10-19/gallery/index.html#composition . The gallery build includes all nine outputs, every ordered source input per run, complete system/user/image prompts, advisory critiques and provider request records. The five new entries also show the supplied arrangement example separately from model inputs. The original two unexecuted Foundry-route plans are retained below, clearly labeled. Publication verification is recorded in the project checkpoint.

## Contents

- [Scope and method](#scope-and-method)
- [Source findings](#source-findings)
- [Generated findings](#generated-findings)
- [Two- and three-cup follow-up](#two--and-three-cup-follow-up)
- [Evidence and reproducibility](#evidence-and-reproducibility)
- [Open questions and checkpoint](#open-questions-and-checkpoint)

## Scope and method

USER-CONFIRMED task: develop a reusable Astra system prompt for composing several reference drinks into one shot, with the user prompt choosing side by side or compact staggered. The latest user instruction authorizes fal: requested `openai/gpt-6-astra` through `openrouter/router/vision`, followed by `openai/gpt-image-2.5/sunburst/edit`. This supersedes the original CLI transport only for these new fal runs; the bundled CLI was not modified. No added refractions or integration with refraction V3.

Initial bound (completed): two images, all five finished source drinks in the same order; at most two further images after specific observed defects justify one targeted prompt revision. Latest user-authorized bound (completed): five additional two-/three-cup combinations matching principal supplied layouts, unchanged V1, one output per case and no extra iteration. High quality, 1536 × 1024, no image postprocessing. Full prompts, ordered inputs, hashes, settings, timing and direct visual reviews accompany each output.

ASSUMED: plain white background and support; source drinks belong to a comparable physical cup family; preserve each reference's distinct projected proportions and near-frontal view. Neither image margins nor cream-top height is evidence of cup-body scale. No physical dimensions are provided. The explicit research specification is sufficient to proceed under research-playbook section 2; unresolved choices do not change this bounded method.

Primary question: can a short arrangement request preserve each drink's identity and projected cup geometry while changing layout? Competing hypotheses: explicit body-geometry constraints help; or the model still substitutes a common cup silhouette and needs deterministic compositing or stronger source conditioning. A plausible-looking image alone cannot establish fidelity.

Evaluate the count and identity of all selected drinks, geometry against each drink's own source, scale consistency, arrangement, clipping and overlap, and absence of added refractions. Visual inspection is mandatory. Any reported geometry estimates use topmost visible plastic-rim y to lowest physical-base y for height, outer rim width, and maximum width of the lowest base foot. Normalize height and base width by rim width. These are projected pixel measurements with manual landmark uncertainty, not real-world dimensions; visible-rim perspective and occlusion limit comparability. Cream height is excluded.

## Source findings

VERIFIED by direct visual inspection on 2026-10-19 of the five original source PNGs: each is a complete cream-topped drink on white. Clear/red-layer drink has a broad rounded base, red and amber drinks have stepped narrow bases, cola has a broad nearly flat rim and dark stepped foot, and orange/red-syrup drink has a broad rounded bottom. Cup and topping silhouettes differ. Treating all references as identical cup templates would erase source information.

VERIFIED observations from the supplied comparison corpus: the customer examples contain magenta, blue and pink drinks with straws, photographed at more elevated views. They demonstrate separated versus staggered arrangements but are not source-matched targets for the five cream-topped drinks. The supplied generated examples contain red/orange/amber or cola/amber drinks. Several orange examples have a simple cone-shaped bottom in place of the source's rounded molded base; the foreground orange in `/mnt/localssd/mixology/multi_cup_examples/generated_examples/TCCC – Crafted Sept 2026-3.png` is visibly much larger than its neighbors. Source pairing and the generation procedure are UNVERIFIED; no numeric before/after accuracy claim can be drawn from these examples.

ASSUMED manual source-geometry estimates (see methodology above; rounded, not exact). Orange updated after the upright source replacement; other rows unchanged:

| Input | Drink | Body height / rim width | Base foot / rim width |
| --- | --- | ---: | ---: |
| 1 | Clear/red layer | 1.51 | 0.70 |
| 2 | Red | 1.46 | 0.61 |
| 3 | Amber | 1.47 | 0.61 |
| 4 | Cola/red syrup | 1.36 | 0.64 |
| 5 | Upright orange/red syrup | 1.27 | 0.61 |

These measurements support checking cola and the new orange for elongated bodies, and each cup against its own base shape. The old orange's 1.47/0.70 ratios are superseded; its rounded-foot description must not transfer to the new flat-base input. Ratios are evaluation data, not extra model inputs. Transparent-edge ambiguity and manual coordinate uncertainty are explicit in `/home/colligo/hs_scripts/claude/mixology/research/group-composition/data/source_geometry.json`.

RESEARCHER DECISION: source geometry takes precedence over copying the examples' elevated camera or dramatic light. Use shallow depth and comparable rim widths, preserve each source's body/rim/base ratios, and avoid normalizing total height including cream. This is a testable prompt hypothesis, not a fidelity guarantee.

## Generated findings

Historical pre-replacement findings below describe the earlier old-source outputs, now archived. Current findings appear at the top; canonical run links now show the upright-source replacements.

The following V1/V2 comparison concerns the four original five-cup outputs; the latest smaller groups are a separate sample set below.

VERIFIED execution: `v1fal_side_by_side`, `v1fal_staggered`, `v2fal_side_by_side`, and `v2fal_staggered` each returned one valid 1536 × 1024 PNG at requested high quality. Exact original reference bytes were passed as ordered data URIs. Direct visual reviews are saved in each record; separate Astra advisory critiques are adjacent. Images have not been composited or geometrically postprocessed.

OBSERVED: all four preserve five recognizable identities, cup count, broad cream/ice/syrup patterns and requested arrangement class, without adding refractions. Cup rim widths remain comparable; the staggered results avoid the conspicuously oversized foreground hero seen in the supplied generated examples. This is a visual comparison, not a source-matched benchmark against the customer's prior technology.

OBSERVED LIMITS: the V1 lineup makes the cola body look more slender/tall relative to its source rim; the orange lower silhouette appears narrower. Rear-cup bodies in staggered shots appear somewhat compact, and overlap obscures portions of the silhouette. No new calibrated pixel-landmark measurement of outputs was performed, so these are qualitative geometry findings, not percentage-error claims. High advisory geometry scores do not establish exact preservation.

V2 changes only this system clause: “Do not equalize cup-body heights or simplify base-foot flare to make the group look uniform; unequal rim and cream-peak heights are expected when faithful source proportions require them.” The image prompts include the clause's constraints, but direct inspection shows no clear lineup fidelity improvement. V2's staggered rewrite also changes the drink-to-slot mapping, an allowed arrangement change that confounds direct comparison. One sample per condition cannot isolate a small prompt effect.

RESEARCHER RECOMMENDATION, not user acceptance: keep V1 as the simpler starting system, using the existing short arrangement requests. V2 remains an inspectable experiment, not a promoted winner. Prompt-only synthesis has not demonstrated exact cup preservation. If exact geometry is mandatory, a next separate test should compare constrained cutout/compositing against generative composition; it was not implemented in this batch.

Provider caveats: exact model IDs were requested, but fal response schemas do not return the backend model snapshot. Astra requires `reasoning=true`; effort is not exposed, and the router's default temperature applies. No silent fallback was requested. These are requested controls, not independent proof of backend enforcement.

## Two- and three-cup follow-up

Historical initial batch below. The three orange-containing samples were subsequently replaced as documented above; cola/amber pairs remain unchanged.

USER-CONFIRMED: generate some two- and three-cup combinations, trying to match the supplied examples. VERIFIED source inspection: the cream-topped generated examples show cola + amber pairs and red + orange + amber trios. The earlier PDF customer examples use different straw drinks and are not claimed as exact drink matches.

Five new runs, all unchanged system V1:

| Run ID | Selected drinks / arrangement | Model-input source indices |
| --- | --- | --- |
| `v1small_pair_lineup` | Cola left, amber right; one row | 4, 3 |
| `v1small_pair_staggered` | Cola front-left, amber back-right | 4, 3 |
| `v1small_trio_lineup` | Red, orange, amber; one row | 2, 5, 3 |
| `v1small_trio_orange_front` | Orange front-center, red back-left, amber back-right | 2, 5, 3 |
| `v1small_trio_amber_front` | Amber front-center, red back-left, orange back-right | 2, 3, 5 |

Indices refer to the five-source catalog below, not the model image numbers: each actual request numbers its selected inputs from 1 to N. The exact example path and match limitations are stored per case in `/home/colligo/hs_scripts/claude/mixology/research/group-composition/cases.json`. Five unmodified comparison PNGs are staged at `/home/colligo/mixology_data/refraction_research_2026-10-19/assets/composition_examples`. Examples are displayed for human comparison only, not sent to Astra or Sunburst. The model receives original single-drink sources and a short explicit arrangement request. This matches drink selection and spatial slots, not the examples' refractions, canvas crop, elevated camera, simplified bases or enlarged foreground cup.

VERIFIED execution: all five rewrites, image calls and advisory critiques completed. Each output is an original 1536 × 1024 PNG; input counts are 2, 2, 3, 3, 3. Exact source bytes, model-order indices, V1 text and output hashes are retained. No cropping, source compositing or geometry postprocessing was applied to outputs. The runner and critic now handle selected subsets without altering historical five-input configurations.

OBSERVED by direct inspection: all five have the requested count, recognizable source drinks and correct arrangement slots. Orange's full red syrup loops and rounded molded bottom remain recognizable instead of the simplified lower cone in some supplied examples. The orange-front layout avoids the example's exaggerated foreground scale. The pair lineup and trio lineup show small apparent body/rim changes, most noticeably a slightly compact amber body; the staggered pair's amber looks more slender with a flatter visible rim, but overlap limits certainty. The trio staggers show no obvious gross stretching in visible contours; hidden rear edges cannot be verified. No calibrated output landmark audit or pixel-exact claim was made. Independent advisory geometry scores were 4–5/5, not customer acceptance.

Interpretation: these are useful review candidates using the simpler V1, not proof that prompt-only synthesis guarantees cup geometry. They do not isolate the effect of cup count: source subsets, arrangements and independently rewritten prompts also differ. One sample per case; no repeatability/generalization conclusion. All 23 preexisting output hashes were captured before editing and are checked by the gallery validator. Refraction V3 remains unchanged and all prior images remain available.

Reproduce only if a new sample is explicitly wanted; the existing IDs resume/skip completed requests:

```bash
/home/colligo/.venvs/mixology/bin/python /home/colligo/hs_scripts/claude/mixology/research/model-access/scripts/run_fal_experiments.py generate --kind composition --version v1small --cases pair_lineup pair_staggered trio_lineup trio_orange_front trio_amber_front --workers 2
/home/colligo/.venvs/mixology/bin/python /home/colligo/hs_scripts/claude/mixology/research/model-access/scripts/run_fal_experiments.py judge --kind composition --cases v1small_pair_lineup v1small_pair_staggered v1small_trio_lineup v1small_trio_orange_front v1small_trio_amber_front --workers 2
```

## Evidence and reproducibility

- Original source directory: `/home/colligo/mixology_data/source_restored_2026-10-19/ref_inputs` (durable restored copy); SSD copy inspected at `/mnt/localssd/mixology/ref_inputs`. Exact model-input copies are staged at `/home/colligo/mixology_data/refraction_research_2026-10-19/assets/ref_inputs` so gallery links remain relative; their hashes are checked against the originals before each run.
- Current source order: `315fb11e7cc94ecf8103ee2cf98227ae.png` (clear with red layer), `6b61ea2d3b3f46959c6a0403879f8299.png` (red), `b82dd27cd8c4471ea84aa21f9878e980.png` (amber), `edbf33f823b842df9cd34393caea6cca.png` (cola/red syrup), `TCCC–Crafted-Sept-2026.png` (updated upright orange/red syrup). The old spaced-name orange remains only as historical source provenance; it is excluded from future active input mappings.
- Explicitly excluded: `/home/colligo/mixology_data/source_restored_2026-10-19/ref_inputs/white_cap.png` and `/home/colligo/mixology_data/source_restored_2026-10-19/ref_inputs/empty_cup.png`. No auxiliary reference is sent.
- Comparison directories: `/mnt/localssd/mixology/multi_cup_examples/customer_examples` (all three images inspected) and `/mnt/localssd/mixology/multi_cup_examples/generated_examples` (all eight files inspected; seven distinct files). VERIFIED: the files `/mnt/localssd/mixology/multi_cup_examples/generated_examples/TCCC – Crafted Sept 2026-8.png` and `/mnt/localssd/mixology/multi_cup_examples/generated_examples/TCCC – Crafted Sept 2026-4 copy.png` have identical SHA-256 `1939cc8ecbe6d6e6b4c38c539d92573468ceae933ca6e46fa4b48500458c276e`; they are one independent example.
- Reusable starting system: `/home/colligo/hs_scripts/claude/mixology/research/group-composition/prompts/system_v1.md`. Targeted comparison: `/home/colligo/hs_scripts/claude/mixology/research/group-composition/prompts/system_v2.md`.
- Cases: `/home/colligo/hs_scripts/claude/mixology/research/group-composition/cases.json`.
- Actual fal runner: `/home/colligo/hs_scripts/claude/mixology/research/model-access/scripts/run_fal_experiments.py`, with `/home/colligo/hs_scripts/claude/mixology/research/model-access/scripts/fal_transport.py`. The original Foundry runner `/home/colligo/hs_scripts/claude/mixology/research/group-composition/scripts/run_composition.py` remains unchanged. All original input hashes are retained.
- Run artifacts: `/home/colligo/mixology_data/refraction_research_2026-10-19/composition/runs`.
- Full imagegen skill applied: `/home/colligo/.codex/skills/.system/imagegen/SKILL.md`; explicitly authorized CLI/model path, indexed image roles, repeated invariants, bounded single-change iteration. Bundled CLI remains untouched.

Confidence legend: VERIFIED means directly observed in the cited current local evidence, ASSUMED is a working hypothesis, UNVERIFIED lacks supporting source data, USER-CONFIRMED describes task constraints rather than model performance. This is a purposive five-drink sample and one output per initial arrangement; no repeatability or generalization claim is justified.

## Open questions and checkpoint

Nine outputs have been generated, reaching both the initial two-plus-two bound and the latest five-small-group bound. Important remaining uncertainties are exact physical cup dimensions, customer tolerance for geometric drift, permissible occlusion, whether source microtexture must be pixel-exact, and transfer to unrelated cup families. The bounded test treats source projected ratios as authoritative and makes no claim about those unknowns.

Next exact step: Hooman reviews the updated composition tab and the separate seven-sample combined tab. Publication/browser evidence is in the project checkpoint. No inference remains running. Original prepared plans and superseded runs are retained off-gallery. If exact preservation is requested later, clarify acceptable geometric tolerance or compare a source-pixel-preserving composition method.
