# Annotation inventory audit note

As of 2026-11-04, the inventory covers the four requested human-annotated reports and excludes `printer-original-full-guidance-analysis-20261104T222046Z`. Analysis was limited to JSON schemas, metadata, ratings, and full annotation text; no image bytes were downloaded and no paid calls were made.

## Counts

- 4 reports, 5 reviewer submissions, 126 report-row instances, and 158 reviewer-row annotation records.
- 278 structured rating answers.
- 29 nonempty comments, all from `zperkins` in the 30-row V13/V14 laptop+printer report.
- 20 comment rows contain a direct product-placement clause; those yield 20 exact placement-specific quote segments. Only 6 identify one output (2 V13 and 4 V14, including single-output rows); the other 14 do not identify a variant. One additional V14 quote says only “placement issues” and is retained as nonspecific.
- The three HP16 reports reuse the same 32 case IDs, device IDs, cameras, and original V6 prompts exactly. The 30-row report has no exact case-ID or prompt overlap with those 32 cases.

## Label audit

No structured question is placement-specific. `Best of 4` and `Overall preference` are overall preferences. `Product fidelity`, `Scene realism`, `Lighting & integration`, and `Blue elements` are broad or non-placement dimensions. A selected winner is not a placement pass, `both_unusable` is not necessarily a placement failure, and an empty comment is unlabeled rather than a pass.

The only direct placement supervision is in comment clauses about edge/chair distance, product-to-table alignment, floating/contact/weight, and support relationship. Each exact quote in the JSON retains row, reviewer, displayed output(s), normalized stage, target basis, and source JSON pointer. Comments without explicit `v13`/`v14` wording remain assigned to the comparison set. Rows 7–10 displayed only V14, so their comments can be attached to V14; their saved comparative ratings are structurally compromised because V13 was absent.

## Stage and provenance limits

The P0 and two HP16 one-image-call reports are scene-generation outputs despite some assets being named `final`; they contain no downstream relight artifacts. The 30-row report labels outputs `final` and `model_output`. Its V14 lineage points to scene-generator PR #4256, but it has no endpoint stage manifest and V13 provenance is only a run name. Treat that report as provisional for a scene-only judge until the absence of downstream relight is confirmed.

Output hashes are absent from the first three reports, so cross-report byte-identical generations cannot be detected from the supplied JSON. The 30-row report includes hashes. The two reviewers on the HP16 V13/V14 overall-preference report agree exactly on only 5 of 32 rows, reinforcing that those preferences are not stable placement labels.

Canonical extraction:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/data/annotation_inventory.json`

This audit note:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/data/annotation_inventory_notes.md`
