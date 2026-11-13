# 1. Results and run guide

## 2. Latest published pages

| Page | URL |
|---|---|
| Latest full-histogram/reference-carrier comparison:41/42 | https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp-data-artifacts/hp-3p-gpt25/hp-style-exact-full42-20261029T002354Z-d04de1a4-comparison-v1/viewer.html |
| Conditional physical-scale pilot: four cases, no feedback repair | https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp-data-artifacts/hp-3p-gpt25/four-all-scale-v2-no-feedback-20261029T023750Z-1d139dbc/viewer.html |
| PR35902 saved HP12 prompts directly to Image 2.5:42/42, no Astra | https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp-data-artifacts/hp-3p-gpt25/direct-hp12-full42-to-image25-native2368-20261029T045439Z-846de5d8-comparison-v1/viewer.html |
| Team review: 42 cases, corrected case 43, style refs and both prompts | https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/adarabi/hp-3p-gpt25/full-single-ref-nearest-grade-20261027/team_comparison.html |
| Nearest-reference grading diagnostic viewer | https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/adarabi/hp-3p-gpt25/full-single-ref-nearest-grade-20261027/viewer.html |
| Case-43 source-camera pilot and before/after comparison | https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/adarabi/hp-3p-gpt25/pilot-0043-source-camera-fit-v2-20261027/viewer.html |

## 3. Principal experiment stages

| Stage/run | Purpose and outcome |
|---|---|
| `pilot`, `pilot-mask`, `pilot-mask2` | Initial reference-conditioned scenes, then masking/aspect/deduplication changes; product drift persisted |
| `full-20261026`, `full-20261026-contaminated` | Initial full generation; contaminated captures are preserved, not preferred results |
| `pilot-v2`, `full-v2-20261027-stopped` | Early iteration; the full v2 run was stopped |
| `pilot-v3-facing`, `full-v3-20261027` | User-side seating/facing improvements |
| `pilot-v4`, `pilot-v4b`, `pilot-v4c` | Composition, margin canvases, alignment and outpainting; generated artifacts/scene changes motivated abandoning repairs |
| `full-singlecall-w30-20261026` | One-call limit, but still old framing/repair architecture; 42 API successes did not mean acceptable geometry |
| `pilot-direct-native-20261026` | Clean native-frame reset without geometric repairs |
| `row45-product-axis-20261026` | Explicit shared axes; remaining fidelity defects |
| `row45-camera-first-20261026` | Product-driven camera/composition |
| `full-camera-first-w40-20261026` | 42 direct outputs; reported failures in several rows |
| `pilot-geometry-softrefs-20261027` | Five-row guide and softer-light pilot; residual defects documented |
| `full-geometry-softrefs-w40-20261027` | 42 guided four-reference outputs; 589 uploaded files byte-verified |
| `full-single-ref-lens-globalgrade-w40-20261027` | 42 one-reference raw images and separate global grades; 505 uploaded files byte-verified |
| `full-single-ref-nearest-grade-20261027` | Offline regrade of those raw images against nearest of 341 references; zero new model calls; 631 uploaded files byte-verified at initial publication |
| `pilot-0043-source-camera-fit-20261027` | Source-edge measurement and failed structured-output rewrite; zero image calls |
| `pilot-0043-source-camera-fit-v2-20261027` | Corrected schema; one image call, steeper source-constrained camera target, separate grade; selected for team review |

All 23 run directories are preserved in `runs/` under `s3://foundry-hp-enterprise-adobe-assets/adarabi/hp-3p-gpt25/handoff-20261027/`. Historical text-only records are also in that snapshot's `archive/runs/`; nothing is stored in this Git folder. See the [S3 index](../README.md#6-code-in-git-experiments-and-results-in-s3) for direct result/manifest links. The table does not claim that every historical run had a published viewer.

## 4. How to read the saved artifacts

- `hero.png`: original source product.
- `input.png`, `mask.png`: prepared generation input and protection guidance.
- `ref_2.*` and any additional `ref_*`: actual generation style references.
- `geometry_guide.png`: geometry-only guidance, not a style image.
- `gpt_1.png`: untouched first raw generation in the current one-call flow.
- `ours.png`: byte-identical raw output in the current flow; historical early runs used this name differently.
- `ours_graded.png`: separately graded image, with product colors changed too.
- `grade_reference.*`: nearest/reference grading target, not necessarily the generation style reference.
- `result.json`: per-row prompt, selections, status, and diagnostics.
- `image_request.json`, where present: actual prompt and request metadata, without model credentials.
- `manifest.json`, source snapshots and patches: code/provenance captured for particular runs.

## 5. Acceptance versus diagnostics

API status, tests, source-edge angular residuals, and nearest-tone statistics do not prove correct shape, camera, composition, or photographic branding. The case-43 pilot improved the apparent camera but retained visible product-detail drift.

The team page intentionally mixes the improved case-43 pilot with the previous 41 outputs. It is a curated review, not a new uniformly regenerated 42-row experiment. Its exact image/prompt selection is recorded in the snapshot's `results/prompts.json`, linked from the README.

## 6. Reference and element-palette evaluations

These are separate authorized evaluations, not replacements for the historical
team review. All use original requests, native2368x1776 images, one image call per
successful plan and separate RAW/Lab outputs.

| Comparison | Outcome |
|---|---|
| [Prominent blue](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp-data-artifacts/hp-3p-gpt25/pr4125-full42-prominent-blue-20261028T210900Z-6f75726f-comparison-v1/viewer.html) | 38/42;56 planning attempts including one explicitly authorized14-case recovery |
| [16-code element lookup](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp-data-artifacts/hp-3p-gpt25/hp-element-blue-full42-20261028T221540Z-f7ba49ad-comparison-v1/viewer.html) | 38/42;42 planning attempts,38 image calls |
| [Stopped reference-anchored16-code run](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp-data-artifacts/hp-3p-gpt25/hp-style-anchored-full42-20261028T235737Z-0125c3d4-comparison-v1/viewer.html) | Stopped by user;22 images retained, no automatic recovery |
| [Corrected full-histogram run](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp-data-artifacts/hp-3p-gpt25/hp-style-exact-full42-20261029T002354Z-d04de1a4-comparison-v1/viewer.html) | 41/42;19 new reference selections,42 plans,41 image calls;23 reference choices held fixed |

The latest page preserves four older result columns. Its new generation reference
is second-last and new result last; each exact prompt belongs to that output.
`baseline-0024` returned no blue bindings and was rejected before generation.
There were no automatic model retries.

Under the latest comparison's URL prefix, `run_manifest.json`,
`comparison_rows.json`, `reference_candidates.json`, `exact_lookup/index.json`,
`inputs/`, `code/` and `rows/<case>/` retain inputs, source/helper snapshots, model
requests/responses, selection/anchor evidence, native outputs and offline checks.
The helper snapshots are historical drivers, not portable package entry points.

For0007, the corrected actual material anchor `#3B7B78` maps to wall `#427C78`
(CIELAB76 distance1.65); the earlier16-code run snapped a nearby teal anchor to
gray-blue `#59636D` (distance21.10). For0009, blue reference banquette upholstery
is retained as a banquette, with `#717A87` mapped to `#707B8E` (distance3.55).
These are prompt-binding distances, not measurements of rendered pixels.
Across41 resolved plans, walls occur in17, curtains10, chairs4, sofas3, benches3,
shelves3 and artwork1. Counts are per-case carrier categories.

The [tagged catalog](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp-data-artifacts/hp-3p-gpt25/reference-catalogs/human-tagged-20261028T233122Z/viewer.html)
preserves343 existing entries and230 added removal variants; labels are the
user's group assignments, not inferred human annotations. The [compact palette
demo](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/analysis/hp_lifestyle_t2i_v2.1.0_blue_albedo_20261027/blue-element-palette-demo-20261028T215724Z/index.html)
remains an illustrative lossy summary (78 elements,1,236 entries), not the
corrected run's lookup. Large catalogs, source histograms and generated assets
remain in S3 and are not committed to Git.

## 7. Physical-scale integration and independent direct-prompt comparison

The four-case scale pilot linked in §2 used local `unified-blue-scale-v2`
(`7d341318`): two laptop cases without dimensions (`scale_plan=null`) and two
printer cases with user-supplied dimensions. Outputs are native2368x1776 RAW
without feedback repair; Laptop Wide still shows product-position drift.
That pilot predates the prominent-blue/full-histogram integration.

The local integration combines #4125 at `3d5e0ea1` with that scale patch.
Its default policy is `unified-blue-scale-v3`; histogram mode uses
`unified-blue-v6-full-histogram-reference-carriers-scale`. Both validate supplied
scale plans and propagate them to the final image prompt. Only offline checks
were run for the integration: no combined-policy images have been generated,
and neither source experiment establishes combined visual acceptance.

The separate42-case direct-prompt comparison linked in §2 sends saved
PR35902 evalset prompts verbatim to Image 2.5, with the original prepared product,
photographic reference and mask, but no Astra or geometry guide. It reused two
pilot outputs and generated40 more, without retry or grading. The left output
is a historical unified-blue-v1 comparator, not a scale/histogram control.
This is an independent workflow comparison, not the current pipeline or a
prompt-only ablation. Its source is
[Adobe-Firefly/colligo#35902](https://github.com/Adobe-Firefly/colligo/pull/35902),
not the PR34442 camera6 dataset. Exact prompts, request metadata and untouched
RAWs remain in the linked S3 report; no historical assets were changed.
