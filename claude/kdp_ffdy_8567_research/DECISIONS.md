# Decisions

## 2026-10-07 — Use stock fe-html for the one-reviewer blind pilot

**Status:** `[CONFIRMED BY USER]`

Use the unmodified stock `fe-html` viewer. A fork is unnecessary because the pilot has one reviewer and the
questions do not need to be locked. Present one opaque normalized candidate per row with the clean product
reference image(s) beside it. Pre-shuffle rows, keep the truth map private, and ask the reviewer to classify the
candidate as `Real` or `Generated`.

Pilot title: `KDP Lifestyle Image — Real vs Generated Pilot`.

## 2026-10-07 — Replace the synthetic black-reference experiment with genuine-reference generations

**Status:** `[CONFIRMED BY USER]`

Remove the Mini Mate synthetic Matte Black reference experiment from the published HTML because a genuine clean
Matte Black reference was found for SKU `5000390176`. Generate additional Matte Black lifestyle variants using
only that genuine clean reference. Match the broad lavender and yellow/cobalt compositions of the scraped
exact-SKU lifestyles through text prompts, as done for K-Supreme; do not supply lifestyle pixels to the model.

The original synthetic artifact may remain archived locally and in S3 but is not part of the displayed POC set.

## 2026-10-07 — Broaden environments, interactions, and Mini Mate color coverage

**Status:** `[CONFIRMED BY USER]`

Add materially different environments and interaction types for every active POC SKU. For K-Supreme Gen 2 Black
and Mini Mate Plus Warm Stone, include one or two compositions that approximate the scraped red/pink studio setting
through text-only scene descriptions; do not supply those lifestyle images to the model.

Create a separate Mini Mate Plus synthetic-black-reference experiment by supplying the clean Warm Stone product
reference for geometry and a black-version lifestyle image only for color evidence. The result must remain labeled
as generated and cannot become ground truth or a real baseline.

Live-data correction: the scrape already contains a genuine clean Mini Mate Plus Matte Black reference for SKU
`5000390176`. The synthetic color-transfer result will therefore be evaluated against that real reference and must
not replace it.

Generate several new K-Express human-interaction variants because the first hand/button result appears visibly
AI-generated to Hooman.

Remaining uncertainty: using observations from the real red/pink images to author scene prompts exposes those
images during prompt development. They may support a labeled scene-matching comparison but are not pristine
holdouts for an unbiased final blind test.

## 2026-10-07 — Expand the POC in one comparison gallery

**Status:** `[CONFIRMED BY USER]`

Extend the successful smoke test with additional scene variations, human interaction, verified non-generated
lifestyle comparisons, and additional high-ranked SKUs. Reuse the existing GPT Image 2.5 HTML gallery and publish
it to Foundry S3.

Generation inputs remain clean product references only. Genuine lifestyle images are held out and displayed as
comparisons rather than supplied to the model, preserving their usefulness for later evaluation.

## 2026-10-07 — Foundry-managed OpenAI authentication

**Status:** `[RESEARCHER DECISION]`

Use `foundry-aws-gateway 2.0.0` in an isolated Python 3.12 environment with the Pluto-injected authentication
token. Do not request or persist an OpenAI key from Hooman. Version 1.6.0 is inadequate because it omits the
required FFDY-8502 policy-acknowledgement header.

## 2026-10-07 — Candidate selection policy

**Status:** `[CONFIRMED BY USER]`

Select initial POC SKUs by the strength and diversity of their available clean references and genuine
lifestyle comparisons. Assess the two ticket SKUs separately even if stronger candidates are selected.

Rationale: the engineering POC should establish achievable quality while still answering ticket-specific
feasibility.

Revisit trigger: client supplies authoritative KDP assets or requires exclusive use of the two ticket SKUs.

## 2026-10-07 — Discovery deliverables

**Status:** `[CONFIRMED BY USER]`

Produce a written dataset assessment and a visual gallery of candidate SKUs with their reference and
lifestyle images.

## 2026-10-07 — Blind-test baseline

**Status:** `[CONFIRMED BY USER]`

Use balanced real and generated images per SKU as the initial C-Tech evaluation design. Alternatives and
improvements will be proposed before executing the evaluation.

## 2026-10-07 — Local data handling

**Status:** `[CONFIRMED BY USER]`

Local downloading or streamed inspection are both acceptable; choose whichever is operationally simpler.

## 2026-10-07 — Initial model variant

**Status:** `[RESEARCHER DECISION — IMPLEMENTATION ADJUSTED]`

Use `gpt-image-2.5-sunburst` for the first fidelity benchmark. Sunburst is documented as the precision-oriented
2.5 model, and the existing NAOU Foundry app provides a tested transport pattern. The first CLI smoke test used
`quality="high"`; `quality="max"` remains a later API-path comparison rather than a description of completed work.

Alternative: benchmark `gpt-image-2.5-flare` after the prompt/reference protocol is stable to quantify the
speed/cost tradeoff. Revisit immediately if the Adobe-hosted deployment exposes a different approved alias.
