# KDP FFDY-8567 lifestyle-image POC notes

Last updated: 2026-10-07

## Objective

Validate whether GPT Image 2.5 can turn clean Keurig hero/reference assets into convincing, on-brand lifestyle
hero images for KDP digital-shelf, PDP, banner, social, and paid-media use. The POC uses scraped public imagery for
internal engineering validation; it does not establish production rights or replace authoritative client assets.

The eventual C-Tech study should blind image origin and ask reviewers to classify each stimulus as real,
generated, or unsure. Product fidelity and marketing usability must be evaluated separately from visual realism.

## Source dataset

S3 root:

`s3://foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/`

Canonical local dataset assessment:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/dataset/SUMMARY.md`

Normalized/local data root:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/dataset/data/`

Verified scrape layers: `1_lifestyle/`, `2_reference/`, `3_pairs/`, `4_index/`, and `focus_skus/`. Pair confidence
means product/variant association, not that the lifestyle-side image is suitable for a realism evaluation; many
pair-labeled files are infographics or feature cards.

## Published HTML artifacts

Candidate/reference dataset review:

https://foundry-aws-corp.adobe.io/asset/foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/kdp_candidate_review/gallery/index.html

Local source:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/dataset/artifacts/s3_candidate_gallery/index.html`

Current GPT Image 2.5 input/prompt/output comparison gallery:

https://foundry-aws-corp.adobe.io/asset/foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/kdp_poc/gpt_image_2_5_smoke/gallery/index.html

Local source and builder:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/generation/smoke_2026-10-07/gallery/index.html`

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/generation/smoke_2026-10-07/build_gallery.py`

The published comparison gallery is an IMS-authenticated, view-only review artifact. It contains 22 displayed
generations, all 22 full prompts, every clean reference used, real comparison imagery, and explicit evidence-role
labels. All 37 unique image references were confirmed reachable on S3. The synthetic black-reference experiment
was removed from the displayed HTML after a genuine clean Matte Black reference was found.

## Current generation set

| Product | SKU | Displayed generations | Coverage |
|---|---|---:|---|
| K-Express Black | `5000358267` | 7 | Kitchen, breakfast, button press, mug placement, top-close gesture, wide human scene |
| Mini Mate Plus Warm Stone | `5000390177` | 5 | Button press, small kitchen, red/pink studio, mug placement, cool evening |
| Mini Mate Plus Matte Black | `5000390176` | 5 | Botanical sunroom, lavender studio, yellow/cobalt tabletop, mug placement, button press |
| K-Supreme Gen 2 Black | `5000393168` | 5 | Kitchen, two red/pink studio scenes, button press, cool office |

All 22 displayed outputs are 1536×1024 RGB PNGs.

Canonical generation summary:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/generation/smoke_2026-10-07/SUMMARY.md`

Prompts:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/generation/smoke_2026-10-07/prompts/`

Outputs:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/generation/smoke_2026-10-07/outputs/`

Supporting expansion reviews:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/generation/expansion_2026-10-07/k_express_human_variations_review.md`

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/generation/expansion_2026-10-07/k_supreme_batch_notes.md`

## Generation procedure

Model and parameters:

- Model: `gpt-image-2.5-sunburst`
- Endpoint behavior: image edit with one or more clean product references
- Quality: `high`
- Displayed output size: `1536x1024`
- Format: PNG
- Prompt augmentation: disabled because prompts were fully authored
- `input_fidelity`: omitted because Sunburst rejects that legacy parameter
- Seed/request ID: not exposed by the bundled CLI, so exact pixel reproduction is not guaranteed

Bundled CLI:

`/home/colligo/.codex/skills/.system/imagegen/scripts/image_gen.py`

Python environment:

`/mnt/localssd/kdp_imagegen_venv/bin/python`

The environment contains `foundry-aws-gateway==2.0.0`. It obtains an OpenAI client and short-lived key using the
Pluto-injected machine token. Version 1.5/1.6 fails with HTTP 403 because it does not send the FFDY-8502 policy
acknowledgement. No user-supplied OpenAI key is required or stored in the project.

Representative invocation pattern, with the key remaining only in the process environment:

```bash
PY=/mnt/localssd/kdp_imagegen_venv/bin/python
CLI=/home/colligo/.codex/skills/.system/imagegen/scripts/image_gen.py
export OPENAI_API_KEY="$($PY -c 'from foundry_aws_gateway import llm; print(llm.get_openai().api_key)')"
$PY "$CLI" edit \
  --model gpt-image-2.5-sunburst \
  --image /absolute/path/to/clean_reference.jpg \
  --prompt-file /absolute/path/to/prompt.txt \
  --quality high \
  --size 1536x1024 \
  --output-format png \
  --out /absolute/path/to/output.png \
  --no-augment
unset OPENAI_API_KEY
```

S3 publication uses short-lived Foundry AWS credentials and the same-shell sourcing rule. The current untracked
credential file is:

`/mnt/localssd/tmp_creds.txt`

If unavailable or expired, use the global `/aws-creds` workflow rather than asking Hooman to paste credentials.
Gallery assets are uploaded with explicit `text/html`, `text/css`, or `application/javascript` content types and
served from `https://foundry-aws-corp.adobe.io/asset/...` with IMS authentication.

## Exact clean references used

K-Express Black:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/dataset/data/pairs/K-Express-Single-Serve-Coffee-Maker__Black/ref__K-Express-Single-Serve-Coffee-Maker_5000358267.jpg`

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/dataset/data/pairs/K-Express-Single-Serve-Coffee-Maker__Black/ref__K-Express-Single-Serve-Coffee-Maker_en_general.jpg`

Mini Mate Plus Warm Stone:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/dataset/data/pairs/Keurig-Mini-Mate-Plus__Warm_Stone/ref__Keurig-Mini-Mate-Plus_5000390177.jpg`

Mini Mate Plus Matte Black:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/dataset/data/pairs/Keurig-Mini-Mate-Plus__Matte_Black/ref__Keurig-Mini-Mate-Plus_en_general.jpg`

K-Supreme Gen 2 Black:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/dataset/data/focus_skus/02_K-Supreme-Gen2_Black_5000393168/reference/00_Keurig-K-Supreme-Gen2_5000393168.jpg`

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/dataset/data/focus_skus/02_K-Supreme-Gen2_Black_5000393168/reference/01_Keurig-K-Supreme-Gen2_5000393168_alt1.jpg`

## Generation findings

- Scene realism and high-level product identity are strong across this bounded set.
- K-Express mug placement and the second, relaxed button press have the strongest hands. The first button-press
  result remains in the gallery as a user-identified failure example. The top-close gesture looks plausible but
  does not prove exact mechanism correctness.
- K-Supreme red/pink studio compositions were matched from text descriptions without sending lifestyle pixels.
  The human variant's simplified blue-ring controls require C-Tech scrutiny.
- Mini Mate Warm Stone has a prompt-compliance miss: the cool-evening result contains a coffee stream despite an
  instruction to avoid one.
- A genuine clean Mini Mate Plus Matte Black reference exists for SKU `5000390176`. The earlier synthetic-reference
  premise was incorrect, so that experiment is excluded from the displayed gallery.
- Five Matte Black outputs use only the genuine clean black reference. Lavender and yellow/cobalt scene matches
  reproduce the high-level campaign compositions from text alone; mug-placement and button-press anatomy/contact
  look plausible at gallery scale.
- Exact SKU correctness remains unverified until C-Tech reviews controls, labels, wordmark, seams, reservoir
  geometry, scale, vessel placement, and interaction mechanics.

## Evaluation provenance and blind-test rules

- K-Supreme red/pink real images and Mini Mate Matte Black lavender/yellow images were visually observed while
  authoring text prompts. Their pixels were not model inputs, but they are not pristine holdouts for the matched
  generated scenes.
- The old Mini Mate synthetic-reference output may remain archived locally/S3, but it must not appear in the active
  gallery or evaluation set.
- A fair origin test should show one normalized image at a time, balance real/generated counts within SKU and scene
  archetype, randomize order, hide filenames/URLs/source metadata, and offer `real`, `generated`, and `unsure`.
- Collect confidence and marketing usability independently. Follow with a post-reveal defect audit for silhouette,
  controls, text/logo, reservoir, cup placement, anatomy/contact, scale, and lighting/reflections.
- Normalize dimensions, crop policy, encoding, and metadata so file characteristics do not reveal origin.
- Use a small pilot before the full study. The current recommendation is 24–32 stimuli with at least 10 judgments
  per stimulus when feasible; smaller C-Tech samples are exploratory.

## fe-html assessment

The stock `fe-html` viewer supports the required core workflow: one image per row, custom
`Real / Generated / Unsure` answers, additional confidence/usability questions, reviewer-attributed S3 publishing,
CSV export, and aggregate summaries. A new UI is not necessary for the first pilot.

It is not automatically blind. The default wrapper exposes filename/path-derived row IDs and tile labels, retains
asset URLs in `data.json`, and lexicographically sorts inputs. It also does not lock the questionnaire. Use an
opaque pre-shuffled manifest/staging prefix, neutral labels, normalized images, no provenance metadata, and an
admin-only truth map. Build a viewer fork only if per-reviewer randomization or protocol locking is required.

Detailed source-backed assessment:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/evaluation/FE_HTML_BLIND_EVAL_ASSESSMENT.md`

## Published blind pilot

Title: `KDP Lifestyle Image — Real vs Generated Pilot`

Preconfigured reviewer URL (`Real / Generated`, one row per page):

https://foundry-aws-corp.adobe.io/asset/foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/kdp_poc/blind_real_vs_generated_pilot_2026-10-07/report/viewer.html?q=W3sidGV4dCI6IklzIHRoZSBjYW5kaWRhdGUgaW1hZ2UgcmVhbCBvciBBSS1nZW5lcmF0ZWQ%2FIiwiaGFyZF9jaGVjayI6ZmFsc2UsInJ1YnJpYyI6eyJrZXkiOiJjdXN0b20iLCJuYW1lIjoiUmVhbCB2cyBHZW5lcmF0ZWQiLCJvcHRpb25zIjpbeyJ2YWx1ZSI6InJlYWwiLCJsYWJlbCI6IlJlYWwiLCJ0b25lIjoibmV1dHJhbCJ9LHsidmFsdWUiOiJnZW5lcmF0ZWQiLCJsYWJlbCI6IkdlbmVyYXRlZCIsInRvbmUiOiJhbHQifV19fV0%3D&hide=item_id&per=1

The pilot contains 14 normalized opaque candidates, balanced 7 real / 7 generated and balanced within each SKU.
Every row includes the corresponding clean product reference image(s). The private truth map is local-only and
Git-ignored; neither it nor the source parquet was uploaded.

Pilot documentation:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/evaluation/blind_pilot_2026-10-07/README.md`

Private truth map:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/evaluation/blind_pilot_2026-10-07/private/truth_map.csv`

## Canonical project records

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/PROJECT_STATE.md`

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/DECISIONS.md`

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/LEARNINGS.md`

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/LONG_TERM_PLANS.md`

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research-plan.md`
