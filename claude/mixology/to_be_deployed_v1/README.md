# Mixology deployment handoff V1

This directory packages the evidence-backed prompts and fixed visual asset needed to implement the first deployment pipeline. The intended flow is:

```text
recipe text or beverage appearance reference
                    |
                    v
    A. generate one uniform single drink
                    |
                    v
      B. combine selected drinks into a group
                    |
                    v
         C. add the refraction treatment
```

The files copied from research are byte-for-byte snapshots. Do not edit them in place. If deployment needs a prompt change, create a separately versioned file and retain these V1 files for regression testing.

## Package contents

| Phase | Packaged files | Purpose |
| --- | --- | --- |
| A — single drink | `01_single_drink/system_v1.txt` | Fixed cup, camera, framing and clean-studio contract. |
| A — single drink | `01_single_drink/neutral_master_v1.png` | Image 1 for every single-drink edit. This is the “cleaned-up model” image from the recipe research. |
| A — single drink | `01_single_drink/recipe_mode_clause.txt` | Exact fixed-master conditioning clause validated in recipe experiments. |
| A — single drink | `01_single_drink/reference_image_mode_clause.txt` | Deployment extension for transferring beverage appearance from Image 2 while retaining Image 1 geometry. This mode was not directly validated in the research batch. |
| B — group composition | `02_group_composition/system_v1.md` | GPT-6 Astra system prompt that writes the multi-image composition prompt. |
| C — refractions | `03_add_refractions/system_v3_frozen.md` | GPT-6 Astra system prompt that writes the final GPT Image relighting prompt. It is byte-identical to Refractions V3. |
| C — refractions | `03_add_refractions/style_reference_image_027.jpg` | Default Image 2 lighting-style reference used by strict two-stage iteration 2. |
| Examples | `SAMPLE_USER_PROMPTS.md` | Copy-ready user prompts for each phase and both Phase A input modes. |
| Audit | `manifest.json` | Source paths, hashes, research status and recommended inference settings. |

All package-relative paths above resolve under:

`/home/colligo/hs_scripts/claude/mixology/to_be_deployed_v1`

## Important distinction: direct image prompt versus prompt rewriter

Phase A's `system_v1.txt` is compiled directly into the single prompt sent to the GPT Image edit operation. The Image API does not receive it as a separate system-role message.

Phases B and C use their system files as system instructions for GPT-6 Astra. Astra receives the user request and the ordered reference images and returns one concise image-editing prompt. Send that returned prompt, with the same ordered images, to GPT Image 2.5 Sunburst. Do not send Astra's reasoning or explanatory text to the image model.

## Shared inference settings

- Image model: `gpt-image-2.5-sunburst`
- Quality: `high`
- Output: PNG, one image
- Phase A canvas: `1024x1536`
- Phases B and C canvas: `1536x1024` for the tested landscape group workflow
- Prompt augmentation: disabled
- Rewriter for Phases B and C: `gpt-6-astra` with high reasoning effort
- Prefer the Foundry-vended direct OpenAI route used in the final research, not an unrecorded provider substitution.

## Phase A — generate one uniform single drink

Always call the GPT Image **edit** operation and always provide `01_single_drink/neutral_master_v1.png` as Image 1. Image 1 controls the cup, rim, base, topping silhouette, size, viewpoint, framing, grounding and white studio scene. Do not use prompt-only generation when cup consistency matters.

### Recipe mode — research validated

Build the image prompt in this order, separated by blank lines:

1. Entire contents of `01_single_drink/system_v1.txt`.
2. Entire contents of `01_single_drink/recipe_mode_clause.txt`.
3. Optional house appearance convention. This describes visible layering or syrup placement; it must not invent ingredients.
4. `Recipe request:` followed by the user's normalized recipe.

Ordered image inputs:

1. `01_single_drink/neutral_master_v1.png` — fixed edit target.

Example user content:

```text
Make Fresh Breeze: 400 ml Sprite, 5 ml strawberry syrup,
10 ml mojito mint syrup, one-third cup ice, vanilla soft-serve float.
```

Do not infer visual layering from quantities alone when a house appearance rule exists. For example, mint syrup does not automatically mean green liquid or visible mint leaves.

### Appearance-reference mode — deployment extension

This mode is included because the application needs to accept another drink photograph, but the research batch did not directly test it. It requires a deployment eval before any reliability claim.

Build the prompt in this order:

1. Entire contents of `01_single_drink/system_v1.txt`.
2. Entire contents of `01_single_drink/reference_image_mode_clause.txt`.
3. The user's requested beverage details and any explicit conflict resolution.

Ordered image inputs:

1. `01_single_drink/neutral_master_v1.png` — fixed edit target and geometry authority.
2. User-provided drink image — beverage appearance only.

Never reverse these images. If the user's image becomes Image 1, the model may adopt its cup shape, camera, lean and crop, defeating the purpose of the neutral master. Initially allow one appearance reference only; define precedence and evaluate explicitly before accepting multiple appearance references.

### Phase A output contract

The output should contain exactly one complete, upright drink in the fixed portrait view. It must have no dramatic refractions, long colored shadows, props, logo, label, straw or lid. Preserve the output at native resolution; do not crop or rescale it before Phase B.

## Phase B — combine multiple cups into a group

Use the outputs from Phase A as the ordered drink references. If the user supplies existing drink images instead, geometry consistency is less reliable because Phase B cannot fully repair mismatched source viewpoints or cup proportions.

### Rewriter call

- System instruction: exact contents of `02_group_composition/system_v1.md`.
- User request: identify the desired spatial arrangement in plain language.
- Images: each finished drink once, in the exact order used by the request.
- Ask Astra to return only the image-editing prompt.

Example user request:

```text
Arrange Image 2 front-center, Image 1 back-left and Image 3 back-right
in a compact shallow staggered group.
```

### Image call

Send Astra's returned prompt and the same ordered drink images to the GPT Image edit operation. The generated group must remain a neutral product photograph: white background, neutral contact shadows and no projected refractions. The composition prompt explicitly reserves refractions for Phase C.

For a straight lineup, request one row, one baseline, small gaps and no overlap. For a staggered group, request shallow front/back offsets and identify every slot. Keep the whole group inside the frame.

Composition V1 was selected for this handoff because it is the simpler validated starting point. Composition V2 added an anti-equalization sentence but did not show a clear overall improvement.

## Phase C — add refractions

Phase C edits the already composed group. It must not rebuild the group from the original single-drink references.

### Rewriter call

- System instruction: exact contents of `03_add_refractions/system_v3_frozen.md`.
- Image 1: Phase B group output. It is authoritative for cup count, identity, arrangement, camera and crop.
- Image 2: `03_add_refractions/style_reference_image_027.jpg`. It is a lighting-style reference only and must never control objects, drink colors, framing or placement. This is the exact default used in strict two-stage iteration 2.
- Recommended user request:

```text
Add refractions. Keep the existing cup arrangement exactly.
```

### Image call

Send Astra's returned prompt and the same ordered images to GPT Image edit. The expected change is directional light transmitted through the cups and ice, producing drink-colored projected fields. The cups, contents, camera and crop should remain unchanged except for lighting-dependent highlights.

Do not omit or reorder the style reference in the deployment reproduction of iteration 2. The style image controls only caustic texture, focal intensity, branching scale variation and falloff. Image 1 remains authoritative for the actual drinks and composition.

The frozen prompt is exactly the Refractions-tab V3 prompt. Its source and packaged copies share SHA-256:

`652fd8895c132e7cf6d311052f55a823dbe7ea09b749077a32d82faa6948eb9e`

## Quality gates and known limitations

Do not translate “keeps the cup uniform” into a pixel-exact guarantee.

- Recipe + neutral-master mode achieved approximately one-to-two-pixel maximum displacement at six sampled cup-edge heights across the validated anchored examples. This is strong projected consistency, not identical pixels or identical 3D geometry.
- Appearance-reference mode is a new deployment extension and needs a bounded eval against the master before release.
- Group composition is generative. One of nine corrected-input composition cases swapped requested depth/identity slots, and small proportion differences remained.
- V3 refraction edits preserved group composition better when run after composition, but the strict two-stage trio results still produced too much mesh or vein-like caustic texture.
- The best three-cup research result required an additional floor-light-only correction after V3. That third correction is intentionally not represented as part of this V1 package. If the deployed quality bar rejects mesh, add an automated or human morphology gate rather than claiming V3 always passes.
- The neutral master is researcher-selected and derived from the supplied amber cup family. It is not a customer-approved production camera.
- All customer-facing outputs require review for cup identity, requested arrangement, unexpected ingredients, refraction topology and background contamination.

## Minimum implementation tests

Before deployment, the pipeline agent should add tests for:

1. Prompt assembly order and exact prompt-file hashes.
2. Image ordering and role labels at every phase.
3. Recipe mode with at least one clear, red/orange and dark beverage.
4. Appearance-reference mode with a deliberately mismatched source cup to verify that Image 1 still controls geometry.
5. Two-cup lineup and three-cup staggered composition, including identity-slot checks.
6. Phase C preservation of the Phase B cup count, crop and arrangement.
7. Refraction morphology rejection for dominant mesh, veins, waves or spiderwebs.
8. Immutable run IDs and no blind retry after an uncertain image POST.

## Research provenance

- Recipe research: `/home/colligo/hs_scripts/claude/mixology/research/recipe-to-image/SUMMARY.md`
- Group-composition research: `/home/colligo/hs_scripts/claude/mixology/research/group-composition-corrected-inputs/SUMMARY.md`
- Multi-cup refraction research: `/home/colligo/hs_scripts/claude/mixology/research/multi-cup-refractions/SUMMARY.md`
- Master source run: `/home/colligo/mixology_data/refraction_research_2026-10-19/recipe-to-image/runs/master_neutral_v1`

Use `manifest.json` to verify that a deployment checkout contains the exact reviewed V1 artifacts.
