# 1. HP product scenes with GPT Image 2.5

Owner: **adarabi**. Experimental handoff captured on **2026-10-27**.

Generate HP-branded environments around supplied product images using third-party image editing and HP photographic references, without training a model.

> [!IMPORTANT]
> The current pipeline plans directly from the **original user request**.
> HP12 rewritten prompts remain comparison provenance, not generation inputs.
> The published historical 42-case review below predates this change.

## 2. Start here

| Resource | Purpose |
|---|---|
| [CONTEXT.md](CONTEXT.md) | Decisions, chronology, current state, and unresolved issues |
| [Reproduction guide](docs/REPRODUCING.md) | Dependencies, asset restore, tests, and generation precautions |
| [Results guide](docs/RESULTS.md) | Run history, published comparisons, and interpretation |
| [Saved prompts (S3)](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/adarabi/hp-3p-gpt25/handoff-20261027/results/prompts.json) | Original user request, HP12 rewritten input, and exact final GPT2.5 prompt for all 42 displayed cases |
| [Team HTML snapshot (S3)](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/adarabi/hp-3p-gpt25/handoff-20261027/results/team_comparison.html) | The shareable comparison, including the corrected case-43 selection and both model prompts |
| [Binary artifact manifest (S3)](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/adarabi/hp-3p-gpt25/handoff-20261027/results/artifact_manifest.json) | 3,198 binary/reference-catalog artifacts: SHA256, size, and S3 location |
| [Text/data transfer manifest (S3)](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/adarabi/hp-3p-gpt25/handoff-20261027/results/text_transfer_manifest.json) | All 1,169 files moved out of Git, with download-verified SHA256s |
| [Original export manifest (S3)](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/adarabi/hp-3p-gpt25/handoff-20261027/results/export_manifest.json) | SHA256s of the original source/text snapshot, before this layout cleanup |
| [Historical archive (S3)](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/adarabi/hp-3p-gpt25/handoff-20261027/archive/README.md) | Run records, source snapshots, helpers, and verification evidence |
| [Full-histogram comparison (41/42)](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp-data-artifacts/hp-3p-gpt25/hp-style-exact-full42-20261029T002354Z-d04de1a4-comparison-v1/viewer.html) | Latest authorized evaluation: tag-driven references, reference-blue furnishings, full exact histogram |
| [Tagged reference catalog](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp-data-artifacts/hp-3p-gpt25/reference-catalogs/human-tagged-20261028T233122Z/viewer.html) | 573 entries /571 distinct photos; existing human/no-human labels |

## 3. Historical team review

https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/adarabi/hp-3p-gpt25/full-single-ref-nearest-grade-20261027/team_comparison.html

The page contains 42 cases, original products and user prompts, four HP12 outputs, the generation style reference immediately beside our graded image, and expandable HP12/GPT2.5 input prompts. These historical GPT2.5 results used HP12 rewritten briefs. All 294 image URLs were preserved when the 84 model prompts were added; they have not been regenerated with the current pipeline.

## 4. Current pipeline

1. Prepare product Image 1 and its mask at **1216x912** by default, or **2368x1776** with `--size 2368x1776`. Remove isolated protected mask pixels before deriving product bounds/contact.
2. Select reference tone/content and deterministically choose one or four deduplicated HP photographs.
3. Give **GPT-6 Astra** only the original user request, product, references, bounds/contact, captions and palette statistics. Stage A returns only geometry and product category. There is no upstream scene-rewrite dependency or legacy mode.
4. Build a geometry-only guide and a numeric geometry summary from the estimated camera/support plan. Stage B Astra then sees the drawn guide and summary and writes `layout`, camera, composition and editing text in plain visual words (sizes, distances and positions relative to the product, frame and nearby objects; no metres, degrees, pixels or percentages), with product first, fixed geometry second and the user request third. Stage B is also told that a printer's back stands right against the wall (when the geometry has one); geometry does not encode this. `layout` leads the final prompt as its GEOMETRY section and a final geometry check ends it; the numeric summary stays a stage B input only. The support is placed around the product base from the planner's user side, user-edge gap and lateral offset, with the user-facing edge marked; it is not centered on the contact point. The user request supplies room, support type, objects, materials and lighting; its layout or extent wording is dropped where it conflicts with the geometry.
5. Send the final per-case prompt to **GPT Image 2.5** (`gpt-image-2.5-sunburst-2026-09-08`), high quality, with only the guide (whose product pixels are the real product) and no mask, so the product pixels are not protected. The style reference and product render reach Astra only; the image prompt describes style in words and fails before the call if it still names another image or the reference. Astra A defaults printer supports to stand against a wall unless the request places them elsewhere.
6. Make exactly one image call; save its untouched bytes as `gpt_1.png` and `ours.png`.
7. Where requested, save a separate whole-image Lab grade as `ours_graded.png`. The published historical regrade chose the nearest global tone among all 341 references without making new model calls.

The [Astra system prompt](hp3p/prompts/system_3p.txt) requires one large physical
blue surface/furnishing or multiple clearly visible blue elements with substantial
combined area when the user does not specify a blue preference. Tiny props, thin
partition frames, screen graphics, sky and lighting casts alone do not qualify.
This adapts the prominence policy from
[Colligo #35902](https://github.com/Adobe-Firefly/colligo/pull/35902) to the unified
planner and final image request, without copying its SCAP output schema.
Explicit minimal-blue requests use small accents; explicit blue amounts or
carriers and exclusions take priority. Blue is text-only:
Astra names each carrier with an everyday blue color name plus material,
placement and extent, without hex codes, a claimed reference match, universal
cobalt or coverage percentage. Desk props stay neutral by default, warm wood,
cream and daylight can coexist with blue furnishings, and the lighting rule
forbids orange or global blue casts.

When the original request supplies physical product dimensions, code normalizes
supported inch/mm/cm/m triplets and gives them to the geometry planner, which
links them and source pixel occupancy to camera geometry and nearby object sizes.
Without product dimensions, the planner sizes geometry from the visible form
factor and common knowledge. No separate scale record is returned or validated.
Camera estimates remain
uncalibrated, and the product footprint is not resized. The default generation
policy is `unified-blue-scale-v17-plain-geometry` (V8 composition, concise scale instructions,
a planner-placed support with laptops near the user-facing desk edge, printers
square to the support edges, and two-stage geometry-first planning where the
prompt writer sees the drawn guide, including a gray wall when the support's back
edge is planned against one, and a plain-words GEOMETRY section in the image prompt).
Earlier `unified-blue-scale-v3` through `v16`, `unified-blue-v2` and
local `unified-blue-scale-v2` caches are rejected, as are changed original user
inputs. Use a fresh run ID; historical reports remain readable.
See [reproduction §7](docs/REPRODUCING.md#7-paid-generation-only-after-explicit-approval)
for invocation and [context §13](CONTEXT.md#13-current-unified-pipeline) for lineage
and limitations.

The opt-in **reference-anchored mode** adds `--blue-histogram FULL.csv.gz` and
requires `--refs 1` plus a tagged `--catalog`. It selects references visually with
request-driven human tags and a room-brightness gate. Blue follows the same
text-only policy as the default flow: Stage B returns no `blue_elements`, and
code no longer measures reference material or substitutes histogram HEX codes.
The histogram now only enters the cache identity. Old captions are not inherited.
User-supplied product dimensions reach the planner in this mode too. It uses
`unified-blue-v21-text-blue-twin-camera-guide-only.1` and checks original
user input plus catalog/histogram identity before cache reuse. Earlier v5-v20 caches
are rejected.
See [reproduction §9](docs/REPRODUCING.md#9-reference-anchored-full-histogram-mode).

There is no separate GPT2.5 system-message parameter in this image-edit call: the custom system instructions belong to Astra. HP12 generated result images are comparison outputs, not generation inputs.

## 5. Scope and limitations

- The evalset filename says 48, but contains **42** cases (`baseline-0007` through `baseline-0048`).
- The original catalog has343 entries /341 distinct images. The expanded tagged catalog has573 entries /571 distinct images:341 human and230 no-human photos after byte deduplication. Tags are user assignments, not new model annotations.
- The displayed case 43 comes from `pilot-0043-source-camera-fit-v2-20261027`; the other 41 GPT results come from the single-reference full run followed by nearest-reference grading.
- Product preservation remains best-effort. No mask/prompt provides a hard pixel lock; geometry and details can change.
- Global grading changes product colors and does not selectively match blue surface hues.
- The historical team-review prompts over-constrain blue:41/42 specify `#103FB2`. Those prompts/results remain unchanged; later authorized comparisons are linked separately.
- The latest full-histogram evaluation returned41/42 images; `baseline-0024` had no blue bindings and was rejected before an image call, without retry. API completion is not blanket visual acceptance.
- The package integration uses offline tests; it does not start new paid calls. Actual experiment requests, prompts, reference choices, outputs and helper snapshots remain in S3.
- The combined scale/text-blue/twin-camera policy has not been visually accepted. Linked earlier experiments are provenance, not validation of the combined policy.

## 6. Code in Git, experiments and results in S3

This Git folder contains only active source, tests, prompt templates, dependencies, and maintained context/docs. Evaluation inputs, reference captions, all 23 experiment histories, generated HTML, saved per-case prompts, manifests, historical helpers/designs, and images live in:

`s3://foundry-hp-enterprise-adobe-assets/adarabi/hp-3p-gpt25/handoff-20261027/`

| S3 path below that prefix | Contents |
|---|---|
| `archive/` | Historical text records for all runs, helper scripts, original source history, verification records |
| `results/` | Team HTML, exact displayed prompts, manifests, and integrity evidence |
| `runs/` | Full runtime run directories, including images and request/result metadata |
| `assets/styles.json`, `hp3p/data/ref_captions.json` | Original reference catalog and generated captions |
| `foundry_subset_48_pr35902_gemini.json`, `baseline_compare.json` | Evaluation inputs and HP12 comparison data |
| `docs/` | Historical design, report, and implementation plan |
| `review-media/` | Visual review sheets |

Both the original 3,198 binary/reference-catalog assets and the 1,169 relocated files were downloaded and SHA256-verified. No environments, credentials, private logs, or raw assistant transcripts are included. Corporate asset access or authorized AWS credentials are required.

See the [reproduction guide](docs/REPRODUCING.md) to fetch only the runtime inputs, restore selected runs, or inspect the complete snapshot without adding artifacts back to Git.
