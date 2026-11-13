# Recipe-to-image: fixed cup and camera

As of 2026-10-20. Generation and review batch complete: 11 image jobs (one neutral master, three text-only controls, five anchored recipes and two extra cola repeats). Artifact and local browser validation passed. Shared-master conditioning is a promising working approach; prompt-only generation did not preserve the cup/view. Exact geometry remains unproven. Review: https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/mixology/refraction_research_2026-10-19/gallery/index.html#recipe-to-image .

## Contents

- [Question and scope](#question-and-scope)
- [Method and gates](#method-and-gates)
- [Results](#results)
- [System and usage](#system-and-usage)
- [Limitations and alternatives](#limitations-and-alternatives)
- [Sources and evidence](#sources-and-evidence)
- [Checkpoint](#checkpoint)

## Question and scope

USER-CONFIRMED: turn recipe text into clean individual drink images while keeping the exact same cup, camera viewpoint and cup-to-ground orientation. Internal reference images are permitted. Start with the supplied recipe book and five clean originals; new recipes, recipe combinations and added refractions are later work.

ASSUMED: one researcher-selected canonical view from the clean original cup family is a useful initial test, not a user-approved production standard. Test on white, with an upright cup and fixed framing. Ingredients and quantities come from the PDF; amounts do not uniquely determine visible syrup stratification or soft-serve silhouette. Appearance rules inferred from the supplied pictures must be labeled separately from recipe facts.

## Method and gates

Compare recipe-only generation against the same recipe with one fixed geometry-reference image. Use the exact direct Foundry-vended `gpt-image-2.5-sunburst` model through the unchanged imagegen CLI. Do not supply each recipe's target photograph as a generation input. Hold prompt, canvas and quality constant except the reference-role clause. Begin with three contrasting recipes (dark cola, pale Sprite, orange Fanta), then extend the better-supported approach to all five and repeats. Maximum 12 image jobs in this initial research batch, including failed/uncertain jobs and master preparation. Completed 11 and stopped for review; no reason to consume the last slot. No orchestration retries; the unchanged CLI constructs OpenAI with SDK-default internal retries, so exact wire-level POST count is not exposed.

Quality gates: correct recipe identity, one upright complete cup, same projected rim/body/base proportions and baseline, no camera roll or view shift, white clean background, no logos/text/garnishes not in the recipe. Measure projected landmarks and review all actual images. An approximate visual pass is not exact geometry. Text or image conditioning alone cannot establish pixel-exact preservation. If needed, test explicit geometric constraints or deterministic vessel compositing separately and disclose raw versus processed outputs.

Evidence schema: full source recipes, page render and source hash, exact system/user/image prompt, ordered reference roles/hashes, requested model/settings, CLI hash, output hash/dimensions, raw evaluation and limitations. A three-recipe single-sample comparison is a diagnostic, not a statistical estimate of reliability. Different API operations (generate/edit) remain a confound alongside the input image.

## Results

VERIFIED for this batch: the supplied PDF contains five recipes on pages 3–7. Visual checking establishes the mapping below; filenames are not in recipe order. The PDF is preserved byte-for-byte (SHA-256 `3e96805664de7815f62b84f8082eb75e6f64503473c6a6d495097b525490820a`). The master is a one-time neutralization of original -5, placed without rescaling on a white 1024×1536 canvas. It retains the cup family and soft-serve shape while adding a subtle base contact shadow. It is a researcher-selected canonical camera, not a user-approved production view.

| Recipe | Page → clean original suffix | Verified syrup amounts | Text-only max sampled edge shift | Shared-master max sampled edge shift |
|---|---|---|---:|---:|
| Velvet Cherry | 3 → -1 | Vanilla Madagascar 5 ml; cherry 15 ml | 20 px | 1 px; repeats 2 px and 1 px |
| Tropical Sunset | 4 → -3 | Strawberry 5 ml; coconut 5 ml | Not sampled | 1 px |
| Fresh Breeze | 5 → -2 | Strawberry 5 ml; mojito mint 10 ml | 26 px | 1 px |
| Sunset Breeze | 6 → -4 | Vanilla 5 ml; raspberry 10 ml | 19 px | 1 px |
| Sunlit Reverie | 7 → -5 | Watermelon 10 ml | Not sampled | 2 px |

All recipes specify 400 ml base drink, one-third cup ice and vanilla soft serve; soft-serve quantity is unspecified. The measurement is a reproducible high-contrast edge proxy at six fixed image rows, not a silhouette/3D/physical measurement. Results are raw, unregistered 1024×1536 images; no recipe output was rescaled, warped, composited, sharpened or masked. Source and output hashes, formula, coordinates and overlays are under `/home/colligo/mixology_data/refraction_research_2026-10-19/recipe-to-image/analysis/geometry.json` and adjacent guide PNGs.

OBSERVED by direct review: all seven anchored recipe outputs keep the same recognizable rim ellipse, taper, molded base, baseline, cream silhouette and margins. The text-only controls are more strongly tapered, use flatter rim ellipses/different feet, enlarge the product and change soft-serve shapes. Anchored cola repeats vary the syrup/ice arrangement without obvious vessel/view drift. Tea changes the interior ice and removes the soda-like fizz while maintaining its shell. These are finite visual observations, not exact-preservation claims. Two actual direct Astra/high reviews cover all ten recipe outputs: three text controls fail geometry; all seven anchored samples pass approximate geometry, plausible grounding and broad recipe appearance. Full evaluations and their non-blinded input records remain in `analysis`.

Remaining appearance defects are visible: Tropical Sunset is paler pink than the supplied redder image; tea is brighter gold and has more prominent ice; cola repeats reduce some cream/cherry marbling. The judge flags apparent ice load in tea/one cola, but visible cube coverage cannot measure the specified ice volume. These are retained for review rather than hidden behind a broad appearance pass.

## System and usage

The reusable interface is recipe text plus a fixed internal preset. It does **not** need a new photograph of each drink. The five known recipes are normalized in `/home/colligo/hs_scripts/claude/mixology/research/recipe-to-image/data/recipes.json`; source quantities and image-derived appearance conventions are separate fields. Example user request: “Make Fresh Breeze: 400 ml Sprite, 5 ml strawberry syrup, 10 ml mojito mint syrup, one-third cup ice, vanilla soft-serve float.”

The application compiles, in order:

1. `/home/colligo/hs_scripts/claude/mixology/research/recipe-to-image/data/system_v1.txt`: fixed cup/camera/studio contract.
2. Fixed-image role clause: replace the beverage inside Image 1, preserving vessel, cream, view and background.
3. House appearance convention: for Fresh Breeze, mostly clear below localized red syrup, not green mint or a uniformly pink drink.
4. The user's recipe.

Image 1 is always `/home/colligo/mixology_data/refraction_research_2026-10-19/recipe-to-image/runs/master_neutral_v1/output.png` (SHA-256 `3b4602db439efa2814fe1368038591011647c6f6c90980cd071ed6ce66ec0a44`). Send the compiled prompt through the Image API edit operation, exact Sunburst, high, 1024×1536, PNG. The Image API has no separate system-message field: the system contract is compiled into its single prompt. No extra language-model rewrite was used, keeping that variability out of the A/B comparison.

Implementation: `/home/colligo/hs_scripts/claude/mixology/research/recipe-to-image/scripts/run_recipe_tests.py`. It obtains credentials with `llm.get_openai()` on the Pluto gateway and invokes the unchanged imagegen CLI, with secrets only in the child process environment. Unique IDs, a locked submission journal and existing-run checks prevent accidental duplicate jobs. Existing runs are immutable; do not rerun them. CLI response/request IDs, image token usage/cost and exact returned model snapshot are unavailable and explicitly recorded as such. Actual Astra/high judge request IDs, returned model and usage are retained.

## Limitations and alternatives

- ASSUMED recommendation: prefer the fixed-master system for the next user review. It has stronger evidence than text alone here, but seven anchored outputs across five closely related drinks do not establish future reliability. Review the canonical master before adopting it as the production camera.
- Ingredients alone do not uniquely determine the supplied art direction: 5 ml of red syrup can be mixed, drizzled or layered. The house appearance catalog carries that missing direction. These tests therefore evaluate recipe plus a shared preset, not uninformed free-text inference of the original photograph.
- The master descends from the amber original. This is intentional shared conditioning, not an independent or held-out test; the amber result is particularly in-source. All recipes are cream-topped iced beverages in one cup family. New recipes/no-cream drinks require new validation.
- Pixel equality is **not** achieved. Above y430 (mostly topping/background), only about 11–20% of pixels match the master exactly in the anchored samples; mean maximum-channel differences are about 1.3–1.6/255. Close appearance is not pixel identity, and transparent cup reflections may legitimately change with the liquid.
- One-to-two-pixel sampled edge agreement does not cover every contour, rim angle, base contact or hidden 3D surface. The six A/B samples' actual Astra/high judgment agrees with direct review but is non-blinded and advisory; IDs reveal the method.
- A deterministic 3D vessel/camera or fixed-shell compositing pipeline remains an alternative if strict geometry must be guaranteed. Neither was implemented or used to make these outputs appear consistent. Surface optics and edge blending would need separate checks.
- No new recipes, generated group combinations, refractions or production deployment were performed in this branch. The next cheapest validation is Hooman's review of the canonical view and five-drink set, followed by a separately authorized grouping/new-recipe test.

## Sources and evidence

- Customer recipe book: `/mnt/localssd/mixology/TCCC_Crafted_Norway_Pilot_Recipe_Book_260703.pdf` (7 pages, July 2026). Durable copy and page renders are prepared by the script below. Primary source for ingredients, not proof that a generative model preserves geometry.
- Clean originals: `/mnt/localssd/mixology/ref_input_originals`; verified durable copies at `/home/colligo/mixology_data/refraction_research_2026-10-19/assets/ref_input_originals`. Five RGBA PNGs, 851×1265. Source projected proportions are similar, but not perfectly identical.
- Working artifacts: `/home/colligo/mixology_data/refraction_research_2026-10-19/recipe-to-image`.
- Source preparation: `/home/colligo/hs_scripts/claude/mixology/research/recipe-to-image/scripts/prepare_sources.py`.
- Recipe/appearance data: `/home/colligo/hs_scripts/claude/mixology/research/recipe-to-image/data/recipes.json`.
- Generation/provenance runner: `/home/colligo/hs_scripts/claude/mixology/research/recipe-to-image/scripts/run_recipe_tests.py`.
- Geometry checker: `/home/colligo/hs_scripts/claude/mixology/research/recipe-to-image/scripts/analyze_geometry.py`.
- Direct advisory critic: `/home/colligo/hs_scripts/claude/mixology/research/recipe-to-image/scripts/judge_recipe_tests.py`.
- Shared review gallery: https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/mixology/refraction_research_2026-10-19/gallery/index.html#recipe-to-image .
- Artifact validation: `/home/colligo/mixology_data/refraction_research_2026-10-19/recipe-to-image/analysis/artifact_validation.json`.
- Publication/readback and browser evidence: `/home/colligo/mixology_data/refraction_research_2026-10-19/_review/recipe_publication_2026-10-20`.

## Checkpoint

PDF, recipes, master, 10 recipe outputs, two actual Astra/high evaluations and geometry checks are durable and directly inspected. All 11 image jobs completed with no orchestration retry; no recipe image/judge work remains running. The artifact validator passed all prompt/source/output hashes, fixed-reference roles and ten-output judge coverage. Local Chromium verified 11 recipe articles, all five tabs, keyboard/deep-link behavior, full prompts, lightbox and mobile widths, plus all 44 prior output hashes. IMS remains byte-identical; authentication was mocked only locally. Live signed-in gateway browser access is not verified; authenticated S3 readback is recorded separately by the scoped publisher.

Main owns this topic; a separate agent continues multi-cup refraction refinement. Shared gallery writes use the agreed publication lock and fresh baseline; corrected group composition and prior refraction/combined results are preserved. Next: Hooman reviews the canonical master view and five anchored outputs before the separately requested later grouping/new-recipe phase. Do not repeat completed IDs or consume the spare generation slot without a specific unresolved test.
