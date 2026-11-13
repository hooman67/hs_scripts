# GPT Image 2.5 Sunburst expanded POC — 2026-10-07

## Scope

This bounded engineering POC tests whether GPT Image 2.5 Sunburst can turn clean Keurig product references into
photorealistic lifestyle hero images while retaining high-level product identity. The displayed set contains 22
1536×1024 lifestyle PNGs across three product families. It is purposively selected and visually reviewed, not a
blinded benchmark or proof of exact SKU correctness.

Every displayed generation used only clean product-reference images. No scraped lifestyle pixels were sent to the
model for any output shown in the gallery.

## Run matrix

All runs used the OpenAI image-edit endpoint, model `gpt-image-2.5-sunburst`, `quality="high"`, 1536×1024
dimensions, and PNG output.

| Product / SKU | Count | Scenario coverage |
|---|---:|---|
| K-Express Black `5000358267` | 7 | Kitchen, apartment breakfast, two button presses, mug placement, top-close gesture, wide candid human scene |
| Mini Mate Plus Warm Stone `5000390177` | 5 | Button press, small-space kitchen, red/pink studio, mug placement, cool evening |
| Mini Mate Plus Matte Black `5000390176` | 5 | Botanical sunroom, lavender studio, yellow/cobalt tabletop, mug placement, button press |
| K-Supreme Gen 2 Black `5000393168` | 5 | Residential kitchen, two red/pink studio variants, human press, cool office |
| **Total** | **22** | **Environment, interaction, and text-only scene-match coverage** |

Exact prompts are preserved in:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/generation/smoke_2026-10-07/prompts/`

All generated PNGs are preserved in:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/generation/smoke_2026-10-07/outputs/`

## Visual findings

- **`VERIFIED` — the requested diversity increased materially.** The new set includes red/pink studio,
  botanical sunroom, cool office/evening, apartment, kitchen, and wider human-present compositions.
- **`VERIFIED` — K-Express hand quality improved.** The mug-placement result is the strongest hand/contact
  example; the relaxed button press is also more natural than the user-flagged first press. The top-close gesture
  is visually plausible but does not prove exact handle-mechanism correctness.
- **`VERIFIED` — text-only scene matching works at the visual-world level.** K-Supreme and Mini Mate red/pink
  outputs reproduce the saturated studio vocabulary without receiving real lifestyle pixels. Those real images
  were observed to write the prompts, so they are not pristine holdouts for these scene-match outputs.
- **`VERIFIED` — genuine-reference Matte Black generation succeeds at high level.** All five Matte Black outputs
  used only the genuine clean reference for SKU `5000390176`. The lavender and yellow/cobalt results closely match
  the broad composition of the scraped lifestyles through text prompting alone; the botanical scene adds a
  distinct environment.
- **`VERIFIED` — Matte Black interaction anatomy is promising.** The lavender mug-placement grip and yellow/cobalt
  top-button press are visually plausible at gallery scale, with clear product contact.
- **`VERIFIED` prompt-compliance miss.** The Mini Mate cool-evening output includes a coffee stream despite an
  instruction to avoid one, consistent with action/prop leakage from its reference.
- **`UNVERIFIED` — exact SKU correctness.** C-Tech review is still required for control labels/layout, seams,
  reservoir geometry, scale, wordmark accuracy, human contact, and interaction mechanics. The K-Supreme human
  output's simplified blue-ring control layout deserves specific scrutiny.

## Comparison evidence

The gallery contains every clean input, all 22 full prompts, all 22 generated assets, eight exact-SKU real
lifestyle comparisons, and one cross-color proxy. Evidence roles are color-coded and described in the gallery.

The three K-Supreme red/pink images and two Mini Mate Matte Black lifestyle images are marked **prompt
inspiration**, because they informed textual scene descriptions but their pixels were not model inputs for any
displayed output.

Local gallery source:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/generation/smoke_2026-10-07/gallery/index.html`

## Transport and reproducibility

- `foundry-aws-gateway==2.0.0` retrieved a direct OpenAI client using the Pluto-injected token. No user-supplied
  OpenAI credential was requested or persisted.
- The bundled CLI used for generation is:
  `/home/colligo/.codex/skills/.system/imagegen/scripts/image_gen.py`
- Sunburst rejected legacy `input_fidelity`; successful calls omitted it.
- All 22 displayed output files are 1536×1024 RGB PNGs. The API path does not expose a seed, so exact pixel
  reproduction is not guaranteed.

## Recommended C-Tech review

Use a two-stage evaluation:

1. Run a non-blind technical defect audit on all 22 assets using separate fields for silhouette, controls,
   branding/text, reservoir, vessel placement, interaction/contact, anatomy, scale, and lighting/reflections.
2. Build a balanced blind real-vs-generated test only from images not exposed during prompt development. Match
   scene archetype and crop where possible, randomize order and filenames, separate realism from SKU fidelity,
   and include an explicit “unsure” response.

The red/pink K-Supreme and lavender/yellow Matte Black source images should be excluded from the pristine blind
pool for their corresponding scene-match generations.
