# Group composition with corrected inputs

As of 2026-10-20. Status: nine bounded outputs and nine independent critiques complete, validated and published.

## Contents

- [Question and bound](#question-and-bound)
- [Inputs and mapping](#inputs-and-mapping)
- [Method](#method)
- [Results](#results)
- [Evidence limits](#evidence-limits)
- [Durable artifacts](#durable-artifacts)
- [Next exact step](#next-exact-step)

## Question and bound

USER-CONFIRMED: regenerate only the nine active cases in the existing Group composition tab with `/mnt/localssd/mixology/ref_input_originals`, publish them in a separate tab titled **Group composition corrected inputs**, and preserve every existing output. The source set is intended to use the same cup. This bounded batch is exactly one new output for each active composition case: two pairs, three trios, and four five-drink V1/V2 cases. No refractions, speculative prompt revisions, repeats or extra controls are authorized.

## Inputs and mapping

The five PNGs were directly inspected and copied byte-for-byte into the new durable namespace `/home/colligo/mixology_data/refraction_research_2026-10-19/assets/ref_input_originals`; `.DS_Store` was excluded. Existing `/home/colligo/mixology_data/refraction_research_2026-10-19/assets/ref_inputs` was not changed.

| Identity | New file | Original composition index |
| --- | --- | --- |
| cola | `TCCC – Crafted Sept 2026-1.png` | 4 |
| clear | `TCCC – Crafted Sept 2026-2.png` | 1 |
| red | `TCCC – Crafted Sept 2026-3.png` | 2 |
| orange | `TCCC – Crafted Sept 2026-4.png` | 5 |
| amber | `TCCC – Crafted Sept 2026-5.png` | 3 |

The per-case ordered input identities are frozen in `cases.json`. They reproduce the actual image order recorded in each old request. The clear drink is used only in the five-drink cases; no empty cup or cap is present in the supplied folder.

## Method

For each case, the harness verifies the completed original record, reuses its exact system version and user arrangement, sends the corrected drink images in the same semantic order to direct `gpt-6-astra` with `reasoning={"effort":"high"}`, and saves the exact rewritten prompt plus returned metadata. The unchanged bundled image-generation CLI then calls exact `gpt-image-2.5-sunburst` at high quality, 1536×1024, PNG, one image, with prompt augmentation disabled. Each completed output receives one independent Astra-high critique and one direct visual review.

Runs live under `/home/colligo/mixology_data/refraction_research_2026-10-19/composition-corrected-inputs/runs`. Complete IDs are immutable and skipped; uncertain image POSTs are never blindly retried. The initial generation ceiling is exactly nine.

## Results

VERIFIED: exactly nine bounded unchanged-CLI invocations/submissions started and nine 1536×1024 PNG outputs completed. The CLI/OpenAI SDK's default retry behavior is not exposed by these records, so the wire-level image POST count is unknown; no failed or uncertain invocation was manually retried. Each run preserves the full Astra-high rewrite request/response metadata, exact image prompt, ordered input hashes, image request/submission/available response metadata, one Astra-high independent critique and one direct visual review. Execution validation passed at `/home/colligo/mixology_data/refraction_research_2026-10-19/_review/corrected_composition_execution_validation.json`.

OBSERVED: all nine outputs read as a visibly tighter common cup family than their original-input/FAL counterparts, especially in rim spans, body taper and repeated molded base structure. Pair and trio front/back scale changes are mostly modest and compatible with shallow perspective. Small residual geometry differences remain: some rendered bodies are broader or shorter relative to their rims, the amber drink can read slightly slender or squat depending on the case, and foreground cups in the five-drink V2 stagger are mildly wide relative to height.

Eight cases preserve their requested slots. `corrected_v1fal_staggered` contains all five identities and coherent cup geometry but swaps red and cola between the saved V1 back/front slots, producing a layout closer to V2. It is retained as the one authorized sample; no prompt revision or replacement was generated.

Contents, syrup patterns and cream identities remain recognizable but are regenerated rather than pixel-exact. All cups are upright with identifiable bases on a white product surface. No conspicuous projected refractions, patterned caustics or colored light pools were added; a few critiques note faint local warmth immediately under colored bases, which is ordinary contact spill rather than a distinct projection.

## Evidence limits

The same-cup statement is USER-CONFIRMED source intent. Manual projected landmarks show a tight visible source range, but they are approximate 2D observations, not physical measurements. The old outputs used fal.ai and an unexposed Astra effort/backend snapshot; new outputs use Foundry-vended direct OpenAI credentials and fixed Astra high effort. Provider, reasoning and stochastic changes are therefore confounds, so this batch cannot prove that source replacement alone caused any change.

Arrangement examples remain internally generated comparison-only guides and are not inputs or customer-approved geometry. The source pixels—not those examples—govern the corrected-input evaluation.

## Durable artifacts

- `data/input_manifest.json` — source/durable hashes, bytes and dimensions.
- `data/source_geometry.json` — approximate projected landmarks and uncertainty.
- `cases.json` — nine one-to-one counterpart and input-order mappings.
- `prompts/judge.md` — independent critique contract.

## Next exact step

Hooman reviews https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/mixology/refraction_research_2026-10-19/gallery/index.html#composition-corrected-inputs . Do not generate replacements or prompt revisions without a new request. Publication preserved all 35 pre-existing output hashes; authenticated S3 readback matched all 775 published objects and all nine corrected outputs. Local browser validation passed the tab/deep link, 233 images, 1,127 relative links, prompts/critiques, lightbox and mobile layout. A live signed-in gateway browser session was not exercised.
