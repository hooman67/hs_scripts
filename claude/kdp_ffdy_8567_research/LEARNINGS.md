# Learnings

## 2026-10-07 — Existing THD image service closely matches the KDP task

**Confidence:** `VERIFIED`

**Source:** `/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/thd_img_l2a/`

The existing THD `singleref` path already defines a clean product/catalog image as the input for generating
a fresh lifestyle scene around that product. Its reusable concepts include product-vs-scene classification,
reference fidelity, brand/text handling, scene-oriented prompt rewriting, reference conditioning, CAI, and
asynchronous image delivery.

Limitation: its generator is Flux2-Dev-L2 and its API is not automatically the GPT Image 2.5 contract.

## 2026-10-07 — Supplied scrape has five functional layers

**Confidence:** `VERIFIED`

**Source:** `s3://foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/`

The scrape separates lifestyle images, clean references, curated reference/lifestyle pairs, a browsable site
index, and expanded focus-SKU folders. Counts include metadata and operating-system artifacts and therefore
require normalization.

## 2026-10-07 — Pair confidence is not image-usability confidence

**Confidence:** `VERIFIED`

**Sources:** the local 161-row pair CSV and manual review of all 170 pair assets.

The 133 “high-confidence” rows describe product/variant association. Numerous lifestyle-side assets are
feature cards or infographics, so high-confidence pairs cannot be placed directly into a realism evaluation.

## 2026-10-07 — Ticket SKUs have asymmetric evidence

**Confidence:** `VERIFIED`

K-Supreme Gen 2 Black has two clean exact-SKU references and three studio lifestyle baselines. K-Duo Gen 2
Moonlight Gray has one clean direct reference and no genuine exact-color lifestyle baseline; Black same-body
video frames are only cross-color interaction proxies.

## 2026-10-07 — GPT Image 2.5 Sunburst has an existing Foundry transport pattern

**Confidence:** `VERIFIED`

**Sources:** official OpenAI documentation and
`/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/naou_image/utils/openai_image.py`.

Sunburst accepts reference images through the image-edit endpoint. The Foundry NAOU app already sends ordered
references using `AsyncOpenAI.images.edit`, `quality="max"`, PNG output, and requested native-fit dimensions.

The 2026-10-07 local credential preflight through `foundry_aws_gateway` failed with HTTP 403 while requesting
OpenAI credentials from `https://foundry-aws-pluto.adobe.io/iam/credentials/openai`. The supplied
`/mnt/localssd/tmp_creds.txt` file is sufficient for read-only KDP S3 inspection, but contains AWS variables
only and cannot authorize image generation.

The 403 was version-specific: gateway client 1.6.0 lacked the acknowledgement required by FFDY-8502. In an
isolated Python 3.12 environment, `foundry-aws-gateway 2.0.0` successfully used the Pluto-injected token and
returned a direct OpenAI client without user-supplied credentials. Relevant upstream documentation:

- https://github.com/Adobe-Firefly/foundry/blob/c6eadff8cc5704281315b3043e4f23ea67f7ed41/docs/project-setup-and-access.md#L233-L249
- https://github.com/Adobe-Firefly/colligo/blob/b6faf123f86feab06132925822de6eb571f2b75e/managed_services/services/firefly/foundry/libs/aws_gateway_client/README.md#L71-L88

The first Sunburst edit also established that `gpt-image-2.5-sunburst` rejects the legacy `input_fidelity`
parameter. Retrying without it succeeded. Direct reference-to-output review found strong preservation of the
K-Express brewer and included cup while generating a new photorealistic kitchen scene. Subtle SKU fidelity still
requires expert review; product fidelity must remain a separate metric from realism.

## 2026-10-07 — Bounded three-SKU Sunburst batch

**Confidence:** `VERIFIED` for visual observations; `UNVERIFIED` for exact SKU correctness pending C-Tech review

**Source:**
`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/generation/smoke_2026-10-07/SUMMARY.md`

Six 1536×1024 Sunburst/high generations across K-Express Black, Mini Mate Plus Warm Stone, and K-Supreme Gen 2
Black showed strong scene realism and high-level product preservation. Both hand/button interactions were
anatomically and contact-plausible at gallery scale. The generated scenes are too homogeneous—mostly warm,
sunlit neutral kitchens—and K-Supreme closely retained the red Keurig mug from its product reference despite a
prompt for an understated mug. This reference-prop leakage is distinct from desired product-identity retention.

Exact labels, seams, control layouts, reservoir scale, and branding remain `UNVERIFIED` until domain-expert review.

## 2026-10-07 — Expanded environment, interaction, and color-transfer batch

**Confidence:** `VERIFIED` for direct visual observations; `UNVERIFIED` for exact SKU correctness

**Source:**
`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/generation/smoke_2026-10-07/SUMMARY.md`

The 19-asset expanded set materially increased scene and interaction diversity. K-Express mug placement and the
new relaxed button press improved on the first user-flagged hand. K-Supreme and Mini Mate red/pink studio scenes
were reproduced from text descriptions without supplying real lifestyle pixels, demonstrating visual-world
matching while also exposing those real images during prompt design and disqualifying them as pristine holdouts.

A genuine clean Mini Mate Plus Matte Black reference for SKU `5000390176` already exists. A requested synthetic
black-reference color-transfer experiment remains useful only as a controlled artifact, not ground truth. A
separate botanical-sunroom lifestyle made only from the genuine black reference provides the proper control.

Observed limitations include a coffee stream in the Mini Mate cool-evening output despite an avoid instruction,
and a simplified blue-ring control layout in the K-Supreme human-press output. These support evaluating prompt
compliance, human realism, and exact product fidelity as separate dimensions.

## 2026-10-07 — Matte Black scene matching from a genuine reference

**Confidence:** `VERIFIED` for direct visual observations; `UNVERIFIED` for exact SKU details pending C-Tech review

Five Matte Black Mini Mate Plus outputs were generated from the genuine clean SKU `5000390176` reference only.
Text prompts reproduced the broad lavender and yellow/cobalt composition families of the scraped lifestyles
without supplying those lifestyle pixels. Both non-human scene matches are visually coherent, and the mug-placement
and top-button-press interactions have plausible anatomy and contact at gallery scale.

The prior synthetic-reference artifact is no longer displayed because it is unnecessary once the genuine clean
black reference is available. The two observed lifestyle images are prompt inspiration rather than pristine blind
holdouts for these scene-matched outputs.

## 2026-10-07 — fe-html supports the core blind-classification workflow but is not blind by default

**Confidence:** `VERIFIED` from the local wrapper and viewer source

`fe-html` supports one image per row, arbitrary custom answer rubrics, shareable question configuration,
reviewer-attributed publishing, CSV export, and multi-reviewer summaries. Therefore it can collect a
`Real / Generated / Unsure` judgment without a new UI.

The default folder/S3 wrapper leaks filenames and relative paths through row IDs, tile labels, metadata, and URLs;
it also sorts inputs and has no shuffle control. A valid blind pilot requires opaque staged filenames/URLs, neutral
labels, a pre-shuffled manifest, normalized media, and a truth map kept outside the report. A viewer fork is only
needed for locked questions or per-reviewer randomization from one shared link.

Detailed assessment:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/evaluation/FE_HTML_BLIND_EVAL_ASSESSMENT.md`

## 2026-10-07 — First blind C-Tech pilot construction

**Confidence:** `VERIFIED`

The published stock `fe-html` pilot contains 14 candidate rows balanced 7 real / 7 generated and balanced within
each included SKU. Each candidate is a metadata-free 1024×1024 RGB PNG with an opaque filename and row ID. Clean
product references appear beside the candidate under neutral labels. The uploaded report contains no truth/source
fields; the answer key remains local and Git-ignored.

The two Matte Black and two K-Supreme scene-matched real images informed prompt wording, so this pilot measures
human distinguishability in deliberately matched scenes rather than unbiased generalization to unseen lifestyle
compositions.
