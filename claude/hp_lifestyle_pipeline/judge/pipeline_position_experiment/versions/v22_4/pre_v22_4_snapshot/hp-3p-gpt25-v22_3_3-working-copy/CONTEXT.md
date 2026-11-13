# 1. Experiment context and continuation notes

This is a curated technical handoff of the experiment, not a raw conversation transcript. State captured on 2026-10-27.

Sections 2-12 describe that historical handoff. The current generation behavior
is documented in [§13](#13-current-unified-pipeline) and [§14](#14-reference-anchored-full-histogram-policy); historical results and their
actual prompts are preserved, not reinterpreted as outputs of the new code.

## 2. Original task and sources

Evaluate third-party GPT Image 2.5 for HP product-background scenes using HP brand guidance and the existing 343-image reference set instead of training another model.

| Source | Location |
|---|---|
| Evalset | `s3://foundry-hp-enterprise-adobe-assets/eval/foundry_subset_48_pr35902_gemini.json` |
| HP12 new/prominent-blue rewriter | https://github.com/Adobe-Firefly/colligo/pull/35902 |
| HP project wiki | https://wiki.corp.adobe.com/spaces/FOUNDRY/pages/3777530158/Project+Page+HP+Image |
| Baseline results discussion | https://adoberesearch.slack.com/archives/C0AKWLP0MCY/p1792204602567369 |
| Reference/training-set discussion | https://adobesearch.slack.com/archives/C0AK1K5DJ0N/p1785534036112989 |

The initial design also incorporated production HP12 guidance, the prior product-background experiment, and the October HP feedback document. The feedback PDF is not redistributed here.

## 3. Prompt lineage: important clarification

The first design used the original user request. Early composition iterations used `raw_prompt`. **The final pipeline uses `row.baseline_prompt`, loaded from the evalset's `prompt` field, for all 42 cases.** `raw_prompt` is only a fallback in the current code and was not selected for those 42 cases.

The actual flow is:

`original user request + HP12 rewritten scene brief + product/reference images -> custom Astra adaptation -> final GPT2.5 editing prompt`

The custom `system_3p.txt` belongs to the Astra text step. GPT2.5 receives the resulting prompt through `images.edit`, with the guide image only and no mask. We did not port or run the HP12 rewriter implementation for the 3P generation flow. Shared semantic scene briefs explain similarities to the HP12 NEW compositions; this is not an independent user-prompt-only benchmark.

The final HTML and `results/prompts.json` in the [S3 snapshot](README.md#6-code-in-git-experiments-and-results-in-s3) contain both the exact HP12 input and the actual final GPT2.5 prompt per displayed image. Case 43's new camera-fit result is paired with its own new prompt.

## 4. Early repair architecture, now abandoned

The early experiments tried masks, larger canvases, cropping, product location, affine alignment, original-product pasting, repeated generation, outpainting, and scene-only grading. Those stages sometimes repaired coordinates but introduced white rims, soft borders, replacement scenes, camera mismatches, and misleading API-success labels.

Important findings:

- The old locator could report confidence on an image with no product; its scores were not proof of fidelity.
- Mask dilation protected a ring of the original white background, contributing to halos.
- Outpainting could regenerate the whole scene rather than merely fill its border.
- Cropping and compositing changed the requested framing and could worsen photographic consistency.
- A successful `status="ok"` often meant only that the API returned an image.

The dated design/report files are retained in S3 as historical artifacts. In particular, their description of the current multi-call repair pipeline is obsolete, and the old report's row-18 camera conclusion was not reliable.

## 5. Native one-call reset

The user explicitly required one **image-generation** call per case; separate text calls remained allowed.

The approved reset:

- Native 1216x912 input/output with no output resize or crop.
- Corrected mask without an opaque white guard ring.
- Untouched output saved identically as `gpt_1.png` and `ours.png`.
- No retries, alignment, original-product pasting, or outpainting.
- Explicit warnings and errors rather than quietly repairing failures.

The default current pipeline follows this contract. The retained `align.py` and `locate.py` modules are historical utilities, not the active generation path.

## 6. Product-driven camera and geometry guides

Astra must choose camera/composition from the source product's visible faces before arranging the room. Baseline camera/layout text is non-binding when it conflicts with the fixed product; room type, support category, props, and named blue carriers remain semantic requirements.

The guide encodes product bounds/contact, projected support axes, the support polygon with its user-facing edge, and secondary furniture boxes. The planner supplies the product base footprint, user side, user-edge gap and support lateral offset; code anchors the base's nearest point at the mask contact and places the support from those values instead of centering it on the contact. Priority is fixed product, then this geometry, then the user request: requested layout, extent and emphasis are adapted so tabletop objects stay on the drawn support and nothing extends beyond the user-facing edge. It is a geometry diagram, not a style reference or a post-generation transform. Camera dimensions and focal length are estimates, not recovered EXIF or a validated output-camera measurement.

Rows 18, 34, 41, 43, and 44 exposed persistent tabletop-axis, furniture-scale, camera, and product-shape problems. Softer reference lighting was added to counter over-dramatic contrast; it did not guarantee visual compliance.

## 7. Four references versus one

Completed full runs included four-reference geometry/soft-light generation and then one-reference generation. The one-reference experiment retained each row's prior Image 2, added a FOV-derived approximate lens estimate, and saved a separate global grade.

The two variants did use different image counts, and all 42 raw outputs differed. Similar results do not prove references irrelevant: the same strongly constrained scene brief dominated both, the single reference was already among the four, and lens/grading changes confounded a pure reference-count comparison.

## 8. Nearest-reference grading

Matching each image to its original generation reference could impose an unrelated dark or differently colored scene grade. The approved offline revision:

1. Measure/cache Lab statistics for all 341 references.
2. Select the nearest reference in normalized `[L mean, L std, mean a, mean b]` space.
3. Regrade the existing raw output to that target; do not generate again.

All 42 nearest selections were independently checked. Mean target distance decreased from 2.0346 to 0.5143; mean absolute RGB change decreased from 18.008 to 5.084. These metrics describe color statistics, not scene semantics or visual acceptance.

The generation reference and grading target are different concepts. `ref_2.webp` remains the generation reference; `grade_reference.*` records the separately selected grading target. Global grading changes product pixels too.

## 9. Case 43 source-camera pilot

The original camera plan was about 52.70 degrees downward. A source-only Astra measurement annotated two width and two depth chassis edges. A numerical fit under centered-principal-point, square-pixel, zero-roll and orthogonal-edge assumptions gave:

| Quantity | Estimate |
|---|---|
| Downward pitch | 64.25 degrees |
| Vertical FOV | 41.8 degrees |
| Support yaw | -37.6 degrees |
| Maximum annotated-edge residual | 0.139 degrees |

The first rewrite was rejected before generation because a frozen string enum contained embedded double quotes. The failed run is preserved with zero image calls. A corrected v2 reused the measurements, made one successful image call, and saved raw plus nearest-reference grade.

The room became more overhead and the support axes more compatible. The user judged it much better and selected it for team review. Printer silhouette/panel-detail drift still remains; a small source-edge residual is not proof of a physically correct generated camera or exact product preservation.

## 10. Final team-review presentation

The latest page shows all 42 cases with original user request/product, four HP12 outputs, style reference immediately before our image, and expandable HP12/GPT2.5 input prompts. Only case 43 uses the new pilot output. The other 41 GPT outputs and all 168 HP12 output links remain unchanged.

Verification covered 294 image links, 84 verbatim model prompts, and the final uploaded HTML bytes. No generation occurred during the presentation updates.

## 11. Known unresolved blue-palette issue

41 of the 42 displayed historical final prompts explicitly specify cobalt `#103FB2`. The historical system also rejects dusty, gray, or desaturated blues, even though 25 of the row-selected reference captions describe such blues. This over-constrains the reference variation.

The direction identified at handoff was reference-specific hue/saturation/material shading rather than a universal hex. At that time, **no prompt correction or image rerun had been performed**. The saved results deliberately retain the actual instructions used; §13 describes the subsequent code change, not a correction to those historical generations.

## 12. Continuation priorities

- Preserve the original outputs and prompt provenance; do not overwrite historical runs.
- If approved, test the blue-palette correction as a small controlled experiment rather than changing multiple factors simultaneously.
- Judge source product shape/position/viewpoint and room geometry visually, not from API status or color statistics alone.
- Maintain one image call per case and separate raw/graded outputs.
- Do not reintroduce the abandoned repair architecture or describe masks as pixel locks.
- Keep run records, evaluation/reference data, generated results, and historical snapshots in S3. Git retains only the active code, tests, prompt templates, and maintained docs.

## 13. Current unified pipeline

The generation path now consumes only the original `row.user_prompt`, product,
selected references, captions, measured palette and product bounds/contact.
Astra plans in two calls. Stage A returns only `geometry` and
`product_category`; code draws the guide and a numeric geometry summary.
Stage B sees the drawn guide and summary and writes `layout`, `camera`, `composition`
and `prompt` in plain visual words (no metres, degrees, pixels or percentages); `layout`
replaces the numeric summary as the image prompt's GEOMETRY section. This runs under a
strict product > fixed geometry > user request priority. Stage B alone is also told
that a printer's back stands right against the wall when the geometry has one; geometry
and the guide do not encode it. One image call follows.
The two-stage split was piloted on 4 laptops and 6 printers (modest geometry gains;
see the session pages linked from RESULTS). Reference classification stays separate.
There is no legacy mode or rewriter selector; Git history preserves the old
implementation. Empty original requests fail without falling back to
`baseline_prompt` or `raw_prompt`. Those fields remain for historical reporting.

The consolidation adapts fixed-product, natural-support and explicit spatial
placement principles inspected in Colligo commit
[`9ff15fd9da8`](https://github.com/Adobe-Firefly/colligo/commit/9ff15fd9da81136eca7074a61fc122aa04e6a9fa),
which identifies itself as a port of
[Adobe-Firefly/colligo#34442](https://github.com/Adobe-Firefly/colligo/pull/34442).
The original PR diff was not directly accessible. This is not a verbatim port
of its SCAP format: Astra still plans from multiple images and structured
geometry.

The current blue policy distinguishes three situations:

- Blue unspecified: require one large physical blue surface/furnishing or
  multiple clearly visible blue elements with substantial combined area.
  Name consistent materials, visible extent and placement in both composition
  and the final instruction. Small props stay neutral by default. Tiny props,
  thin partition frames, screens, sky and casts alone do not qualify.
- Minimal blue requested: use a few small named accents, not a dominant carrier.
- Explicit amount, carrier or exclusion: follow the request, including no blue.

The default brand-blue requirement is not removed with the upstream brief.
The prominence requirement adapts
[Colligo #35902](https://github.com/Adobe-Firefly/colligo/pull/35902), inspected at
`332c0044c57c4d4963dabbfc08e0ab2bfd9339ba`, to this planner's existing schema.
It removes any single-carrier cap and does not permit omitting blue merely for
a tight crop, studio setting or warm lighting. Product framing and finish stay
fixed; explicit user blue preferences still override the default.
Warm wood, cream and natural daylight can coexist with blue furnishings. Astra
uses plausible ordinary blue color names; no invented reference match, universal
cobalt code or coverage percentage is imposed. Source-product preservation and no-person
restrictions remain fixed constraints; conflicts are recorded in composition.

The default canvas remains 1216x912; `--size 2368x1776` selects native
high-resolution generation. Preparation, masks, guides and validation all use
the selected canvas. Returned raw bytes are never upscaled or repaired.
Mask preparation removes isolated protected pixels using eight-neighbor
connectivity after erosion, without changing RGB preparation. This prevents a
corner speck from expanding bounds or moving the support contact; it is not
semantic segmentation or a guarantee of generated product fidelity.

`pipeline_version="unified-blue-scale-v17-plain-geometry"` combines the prominent-blue default
from #4125 with physical-scale context from local commit `7d341318`. Labelled
user dimensions (inches, mm, cm or m) are normalized by code and given to the
geometry planner, which links them and source pixel occupancy to camera geometry
and surrounding object sizes. Stage A no longer returns or validates a separate
`scale_plan` record; it was not used by stage B or the image prompt.
This is not a calibrated reconstruction or a product resize.
Printers must sit square to the support edges, with yaw read from the bottom edges
at the near base corner; laptops may turn slightly toward the user. The yaw is
still an Astra estimate (printer case 0017 remains visibly misaligned). Stage A
chooses real support furniture with typical dimensions for the room and product,
and sets `back_edge_against_wall` when that furniture normally stands against a
wall; the guide then draws the wall in gray.

Generation rejects historical or earlier-policy caches, including
`unified-blue-v2` and local `unified-blue-scale-v2` through `v15`, and changed canvas,
reference count or original user input; use a fresh run ID. Historical reports remain readable.
Synthetic tests validate request
construction and raw-byte/size behavior, not actual color or product fidelity.
No new paid calls or image generation were performed for this integration.
The combined policy requires a separately authorized visual evaluation; earlier
scale and reference-blue experiments do not establish its visual acceptance.

## 14. Reference-anchored full-histogram policy

The later authorized experiments and their exact sources/results are linked in
[RESULTS.md §6](docs/RESULTS.md#6-reference-and-element-palette-evaluations).
The portable package integration is opt-in via `--blue-histogram` with `--refs 1`.
Without it, the default prominent-blue/scale flow is used.

The full catalog preserves343 old entries and adds230 removal-preferred variants.
Per user instruction, old entries are tagged `human` and new variants `no_humans`;
there was no human reannotation. Byte deduplication yields341 human +230 no-human
photos. The original request determines tag eligibility: explicitly requested
people use human references; explicit no-people/default uses no_humans. Unknown or
opposite tags cannot enter via scene/brightness fallback.

Reference selection visually ranks contact sheets and existing scene/tone tags.
Warm wood/dark finishes are not room illumination. Explicit bright-room requests
gate same-tag, same-scene candidates to their top brightness-score quartile;
dim requests use the bottom quartile. This fixes the old hash picker's blindness
to exposure, but is not a calibrated scene-quality score.

Blue no longer uses the histogram. The earlier mode measured Astra's named
material ROI and substituted the nearest exact histogram HEX code; the merged
policy replaces that with the text-only blue section (§13), so Stage B
returns no `blue_elements` and no `resolved_bindings.json` is written. The
histogram file still gates this mode and enters the cache identity.
`reference_style.resolve_bindings` remains unused library code.
Global blue washes and product recoloring remain forbidden. Explicitly requested
people override only the blanket no-person rule; old captions are never inherited.

The corrected all42 evaluation produced41 images. The failed0024 plan had no blue
bindings and made no image call. The prior run was stopped with22 images retained;
23 completed reference choices were held fixed, with19 new selections,42 fresh
plans and41 image calls. It is not a reference-resampling experiment.
The Git integration preserves the same policy with portable inputs, per-row audit
JSON and input-aware caches; historical machine-bound drivers/viewer updates stay
in the linked S3 snapshots rather than becoming production CLI dependencies.

The combined mode uses
`unified-blue-v21-text-blue-twin-camera-guide-only.1`, rejecting earlier v5-v20
caches.
Final image assembly is shared with the default flow; provided dimensions reach
the geometry planner. Cache reuse
checks the original user request as well as catalog/histogram identity.
