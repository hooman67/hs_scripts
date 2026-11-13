# Research Plan

## Question

Can a reference-conditioned third-party image model generate convincing, on-brand Keurig lifestyle hero
imagery from scraped product assets, and which SKUs provide the strongest POC validation set?

## Competing hypotheses

- **H1:** Clean multi-view product references are sufficient for realistic lifestyle compositions with
  recognizable SKU identity.
- **H2:** Product geometry, controls, logos, carafe/cup relationships, and human interaction drift enough that
  generated images are distinguishable or unsuitable for digital-shelf use.
- **H3:** Results are SKU-dependent; simpler single-serve brewers outperform dual-system brewers.

## Stage 1 — Dataset normalization

1. Inspect CSV schemas and supplied report/index.
2. Remove non-image artifacts from counts.
3. Normalize source, product, SKU/variant, image role, dimensions, and pair confidence.
4. Reconcile the ticket summary against object-level records.

## Stage 2 — Candidate verification

Score each SKU on:

- clean reference count and view diversity;
- visible product fidelity cues;
- real lifestyle count and composition diversity;
- verified reference-to-lifestyle pairing confidence;
- absence of watermarks, text overlays, competitor products, and composited-ad structure;
- suitability for human interaction and product-in-focus hero scenes.

Folder labels and automated fields are not accepted without visual spot-checking.

## Stage 3 — POC generation

Use a bounded prompt matrix covering product-only hero, cup-under-brewer, and human-interaction scenes.
Preserve all inputs, prompts, parameters, model/version identifiers, and outputs in the review artifact.

## Stage 4 — Human evaluation

Randomize real and generated images, balance counts within each SKU and scene archetype, hide origin, and
collect both forced-choice origin judgments and independent quality/fidelity ratings.

## Quality gates

- Every selected SKU has at least one visually verified clean reference.
- Every real baseline is verified as lifestyle imagery of the same product/variant or explicitly labeled otherwise.
- No watermarked or text-overlaid image enters the blind baseline.
- Product/variant uncertainty remains visible.
- Generation cannot begin until the model contract and allowed input handling are verified.

## Stopping rules

- Discovery stops when candidate rankings stabilize after visual verification of the leading SKU set.
- Generation stops or changes model when repeated outputs fail the same identity-critical geometry despite
  controlled prompt/reference changes.
- Blind evaluation is not interpreted as portfolio-wide evidence if sample size or evaluator count is too small.

## Outputs

- `research/dataset/SUMMARY.md`
- candidate-SKU gallery under `research/dataset/artifacts/`
- normalized data under `research/dataset/data/`
- later generation and evaluation summaries in their own topic directories.
