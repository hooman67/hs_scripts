# KDP Scraped Dataset Assessment

## Table of contents

- [Scope](#scope)
- [Inventory](#inventory)
- [Data quality](#data-quality)
- [Ticket SKU assessment](#ticket-sku-assessment)
- [Candidate SKU ranking](#candidate-sku-ranking)
- [Blind-test recommendation](#blind-test-recommendation)
- [Contradictions and limitations](#contradictions-and-limitations)
- [Sources](#sources)
- [Next validation step](#next-validation-step)

## Scope

As of 2026-10-07, assess scraped public Keurig imagery for an internal engineering POC that generates
lifestyle hero images from product references. This file is the canonical human-readable dataset synthesis.

## Executive synthesis

- **`VERIFIED` — The scrape is useful for a POC, but its labels are not an eval set.** It contains strong
  product references and some genuine lifestyle images, yet many “lifestyle” and even “high-confidence pair”
  files are text-heavy feature cards, studio composites, or infographics.
- **`VERIFIED` — Best first consumer candidates:** K-Express Black (`5000358267`) and Keurig Mini Mate Plus
  Warm Stone (`5000390177`). Together they cover an ordinary kitchen hero and a human-interaction case.
- **`VERIFIED` — Useful secondary stress case:** K-2550 Plumbed (`5000380341`) has the richest delivered
  interaction/context coverage, but it is a commercial brewer rather than the consumer-ticket target.
- **`VERIFIED` — Ticket SKU feasibility differs:** K-Supreme Gen 2 Black has two clean references and three
  exact-SKU studio lifestyle baselines; K-Duo Gen 2 Moonlight Gray has one clean exact-SKU reference and no
  genuine exact-color public lifestyle baseline.
- **`RESEARCHER DECISION` — Start generation with GPT Image 2.5 Sunburst at max quality.** Official OpenAI
  documentation positions Sunburst as the precision-oriented generation/editing variant, and an existing
  Foundry app already uses ordered references through `AsyncOpenAI.images.edit` with this exact model.

## Inventory

Initial S3 object-level inventory:

| Prefix | Objects | Bytes | Status |
|---|---:|---:|---|
| `1_lifestyle/` | 3,139 | 447,064,702 | `VERIFIED`; includes non-image artifacts |
| `2_reference/` | 86 | 19,530,089 | `VERIFIED`; requires role/quality audit |
| `3_pairs/` | 170 | 50,971,292 | `VERIFIED`; pair confidence not yet reconciled |
| `4_index/` | 914 | 7,234,949 | `VERIFIED`; includes HTML and thumbnails |
| `focus_skus/` | 204 | 187,310,217 | `VERIFIED`; expanded content requires classification |

Normalized findings:

| Measure | Result | Interpretation |
|---|---:|---|
| Indexed records | 11,883 | 7,685 YouTube; 3,323 Keurig; 875 Pinterest |
| Delivered lifestyle images | 3,136 | 2,080 hero + 1,056 secondary |
| Delivered lifestyle by source | 2,639 / 342 / 155 | YouTube / Pinterest / Keurig |
| Reference files in S3 | 86 | 74 unique basenames across 21 products and 48 SKU/color variants |
| Byte-distinct reference files | 72 | Some references are duplicated across color/variant folders |
| Pair rows | 161 | 133 high-confidence + 28 color-ambiguous |
| Pair assets | 170 | 81 distinct references + 89 distinct lifestyle-side files |
| Paired product/color variants | 44 | Coverage breadth, not proof of image usability |

The eight delivered lifestyle buckets reconcile exactly to 3,136 images:

- hero: 875 no-cup/no-human; 848 cup/no-human; 266 no-cup/human; 91 cup/human;
- secondary: 502 no-cup/no-human; 301 no-cup/human; 209 cup/no-human; 44 cup/human.

## Data quality

- **`VERIFIED` — Role-label inflation:** many `life_H` assets in `3_pairs/` are infographics or feature
  callouts. Pair confidence indicates product/variant match, not clean-lifestyle suitability.
- **`VERIFIED` — Most delivered lifestyle volume is weakly SKU-grounded:** 2,639 of 3,136 delivered files
  are YouTube frames and 342 are Pinterest images. The supplied report says these sources are not SKU-labeled;
  automatic visual matching would be required before using them as exact-SKU evidence.
- **`VERIFIED` — Official Keurig lifestyle evidence is scarce:** only 155 delivered lifestyle images are
  from keurig.com. This is the preferred pool for a blind baseline because provenance and product association
  are stronger.
- **`VERIFIED` — Scraped reference quality is adequate for POC conditioning:** most curated reference files
  are 1,500×1,500 or 2,000×2,000. Some “reference” views contain callout text, cups, or feature badges and
  should be excluded or cropped before model input.
- **`ASSUMED` — Public scrape rights are sufficient for internal technical validation only.** The PDF itself
  labels the corpus “Internal POC tech validation only”; production usage requires authoritative KDP assets
  and legal/data-governance confirmation.

## Ticket SKU assessment

### K-Duo Gen 2, Moonlight Gray (`5000396548`)

**Verdict:** viable as a hard generation-fidelity test; unsuitable for an exact-SKU real-vs-generated blind
comparison with the current scrape.

- `VERIFIED`: three files are placed under `reference/`, but only the primary product shot is clean enough
  to use directly; the other two contain feature-callout design.
- `VERIFIED`: five additional exact-color files are infographics.
- `VERIFIED`: zero genuine exact-color lifestyle images and zero exact-color videos are present.
- `VERIFIED`: the same-body Black variant (`5000389055`) has nine PDP gallery images, four videos, and 153
  deduplicated frames with the whole brewer visible. These can inform interaction/composition, but they are
  color-mismatched proxies and must not be presented as Moonlight Gray ground truth.
- Risk: the dual single-serve/carafe layout, reservoir, control panel, and simultaneous vessel geometry make
  this a stronger identity/physics stress test than a simple single-serve brewer.

### K-Supreme Gen 2, Black (`5000393168`)

**Verdict:** viable ticket-SKU generation candidate and limited studio-style blind baseline.

- `VERIFIED`: two clean exact-SKU references.
- `VERIFIED`: three exact-SKU red-set studio lifestyle compositions, including one with a cup.
- `VERIFIED`: one model/human image contains no brewer and cannot serve as product evidence.
- `VERIFIED`: eight additional exact-SKU infographics; no exact-SKU video.
- Limitation: the real baseline lacks an authentic kitchen scene and human interaction with the brewer, so
  it tests polished studio realism more than the complete ticket use case.

## Candidate SKU ranking

| Rank | SKU | Role | Verified clean references | Verified useful lifestyle | Main limitation |
|---:|---|---|---:|---:|---|
| 1 | K-Express Black `5000358267` | Primary consumer POC | 2 | 2 | No delivered human-interaction baseline |
| 2 | Mini Mate Plus Warm Stone `5000390177` | Primary human-interaction POC | 1 | 1 exact + 1 multi-color proxy | Sparse exact-SKU real baseline |
| 3 | K-Supreme Gen 2 Black `5000393168` | Ticket-SKU POC | 2 | 3 studio | No real-world/human baseline |
| 4 | K-2550 Plumbed `5000380341` | Interaction stress case | 1 clean + 1 badged | 4 | Commercial brewer; some 600px assets |
| 5 | K-Duo Gen 2 Moonlight Gray `5000396548` | Ticket hard case | 1 clean + 2 callout views | 0 exact-color | Cannot support exact-SKU blind baseline |

Alternatives rejected for the first pass:

- K-Slim White has three pair references but only one genuine contextual lifestyle; the other two
  pair-labeled lifestyle files are feature graphics.
- K-Cafe Barista Bar Black has three useful references, but both pair-labeled lifestyle files are infographics.
- K-Express Black is preferred over apparently higher-count variants because its accepted files are cleaner;
  raw pair count alone rewards repeated reference×lifestyle combinations and text-heavy assets.

The local candidate gallery shows every reviewed file, its exact S3 URI, and its accepted/excluded role:
`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/dataset/artifacts/s3_candidate_gallery/index.html`.

Published gallery:
https://foundry-aws-corp.adobe.io/asset/foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/kdp_candidate_review/gallery/index.html

## Blind-test recommendation

Do not make “can you spot the fake?” the only question. A visually convincing image can still be unusable
because the brewer identity, controls, reservoir, carafe, logo, or interaction physics are wrong.

Recommended two-stage protocol:

1. **Blinded single-image judgment:** show one normalized image at a time; ask `real`, `generated`, or
   `unsure`, confidence 1–5, and marketing usability 1–5. Single-image presentation avoids making the task an
   artificial side-by-side difference hunt.
2. **Post-reveal defect audit:** ask whether product silhouette, controls, logo/text, cup/carafe placement,
   human anatomy/contact, and lighting/reflections are correct. This identifies why an output passed or failed.

Controls:

- Balance real/generated counts within each SKU and scene archetype; randomize order per evaluator.
- Normalize resolution, crop policy, file format, and metadata so compression or dimensions do not reveal origin.
- Hold real evaluation images out of prompt development and never use them as generation references.
- Treat repeated ratings as repeated judgments, not additional unique images.
- Keep K-Duo Moonlight Gray out of an exact-SKU origin test until real Moonlight Gray lifestyle assets exist;
  use it for a product-fidelity panel instead.
- For a directional internal test, target 24–32 stimuli with at least 10 judgments per stimulus. Label results
  exploratory rather than statistically conclusive if the C-Tech pool is smaller.

Primary metric: source-classification accuracy against the 50% chance baseline, with `unsure` reported
separately. Secondary metrics: marketing usability and product-fidelity defect rates. The cheapest validation
is an eight-image pilot that verifies instructions, randomization, and scoring before generating the full set.

## GPT Image 2.5 fit

- `VERIFIED` (OpenAI Docs, retrieved 2026-10-07): GPT Image 2.5 has two explicit variants. Sunburst is the
  precision-oriented image generation/editing model; Flare is the faster everyday-generation model. Both
  accept text and image inputs and support image edits, multiple references, custom dimensions, and quality
  levels through `max`.
- `VERIFIED` (local Foundry source, 2026-10-07): NAOU already calls
  `AsyncOpenAI.images.edit(model="gpt-image-2.5-sunburst")` with ordered image inputs, `quality="max"`, PNG
  output, and native-fit dimensions. This is the closest reusable transport pattern for the POC.
- `RESEARCHER DECISION`: Use Sunburst/max first to measure the best attainable product fidelity. Add Flare
  only as a speed/cost comparison after the prompt/reference protocol is stable.
- `UNVERIFIED`: the Adobe Foundry web documentation root supplied by Hooman timed out from this host, so the
  exact Adobe-hosted credential/base-URL contract remains to be verified before the first model call.

## Contradictions and limitations

- The PDF reports 74 references while the S3 folder has 86 JPG instances. These reconcile as 74 unique
  basenames copied across 48 SKU/color folders; there are 72 byte-distinct files.
- The pair table has 161 relationship rows, while `3_pairs/` has 170 assets; these reconcile as 81 distinct
  reference files plus 89 distinct lifestyle-side files.
- The K-Duo pair table contains two rows labeled lifestyle, but visual inspection shows feature-card/
  infographic content. The supplied PDF's “0 exact-SKU lifestyle” statement is the accurate operational view.
- Scraped imagery is POC evidence, not authoritative client-provided production data.
- A blind “real or generated?” test can be confounded by obvious production style, resolution, text overlays,
  or scene archetype. Only visually clean real images should enter it, and sources must be balanced within SKU
  and scene type.

## Sources

- `s3://foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/`
- User-provided ticket and scrape summary, received 2026-10-07 (`USER-CONFIRMED`).
- `/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/dataset/data/raw/KDP_Keurig_data_index.pdf`
- `/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/dataset/data/raw/all_images.csv`
- `/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/dataset/data/raw/brewer_skus.csv`
- `/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/dataset/data/raw/3_pairs.csv`
- OpenAI Docs, “Image generation,” retrieved 2026-10-07:
  https://developers.openai.com/api/docs/guides/image-generation
- OpenAI Docs, “GPT-Image-2.5 Sunburst,” retrieved 2026-10-07:
  https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst
- `/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/naou_image/utils/openai_image.py`

## Next validation step

Confirm the Adobe-hosted GPT Image credential/base-URL path, then run a small Sunburst/max smoke matrix using
the accepted K-Express, Mini Mate Plus Warm Stone, K-Supreme Gen 2 Black, and K-Duo Gen 2 Moonlight Gray
references. Preserve every input, prompt, parameter, output, and provider request identifier.
