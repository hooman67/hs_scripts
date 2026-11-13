# Placement judge v2: human-evidence audit

As of 2026-11-04, the complete raw-schema audit covers four reports, five reviewer submissions, 158 reviewer-row records, and 278 structured answers. The machine-readable evidence is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v2/data/human_evidence.json`

A read-only live S3 listing on 2026-11-04 found the same five annotation objects with the same keys and byte sizes as the preserved local snapshots. No additional or newer reviewer object was present under the four report annotation prefixes.

## Strongest labels

The newest user adjudications are exact-variant FAIL labels and remain separate from the older annotation corpus. The short descriptions below are normalized label paraphrases from the task specification, not verbatim user quotations:

| Image | Label paraphrase |
|---|---|
| row 25, V14 printer | `printer/table misaligned` |
| row 12, V13 printer | `printer should wall-align/towardside notmiddle` |
| row 9, V14 laptop | `laptop too far chair + blocked access` |
| row 29, V13 laptop | `laptop too far chair though narrative appealing` |

The JSON contains the full public URL for each label. These are the highest-authority placement judgments in the evidence set. They are useful adjudicated regression cases, but they are not unseen image-level holdouts: rows 9/V14, 12/V13, and 29/V13 were in the v1 held-out pilot, while row 25/V14 was in v1 development.

## Correction to the prior extraction

The earlier inventory counted only 29 nonempty top-level comments. It omitted 63 nonempty per-variant `question_comments` values from the HP16 V13-vs-V14 reviewer submission, including multiline mixed comments such as “Product Placement & Scale\nProduct Lighting & Setting.” The corrected total is 92 nonempty source text annotations before the four newer user labels, split into 135 exact quoted clauses.

Among the 64 clauses that can inform placement or scenario usability, 42 have exact single-variant attribution, one clause explicitly covers both variants, and 21 remain comparison-set ambiguous. Every quote retains report, reviewer, row, variant attribution basis, JSON pointer, and stage confidence. Mixed comments retain their non-placement clauses rather than silently dropping them.

The placement evidence repeatedly covers product-to-furniture alignment, distance to the user-facing edge or chair, blocked access and reach, plausible support/contact/weight, printer location within a room, and whether nearby props face and serve the implied user. The newer row 29 label also establishes that an appealing narrative does not rescue failed placement. Lighting, color, decor, generic hallucinations, and broad preference remain boundary evidence: they are preserved so a later rubric does not accidentally score them as placement defects unless they directly break support, access, orientation, or usability.

## Interpretation limits

The 278 best-of-four, pairwise preference, fidelity, realism, lighting, and blue-element answers are preserved for auditability but are not placement ground truth. A winner is not a placement pass, `both_unusable` is not necessarily a placement failure, “Good” or “OK” is not a placement pass, and an empty comment is unlabeled.

The P0 and both HP16 reports are high-confidence scene-generation outputs. The 30-row laptop/printer report, including the four newly labeled assets, remains medium-confidence for stage because it lacks a complete raw-PNG endpoint stage chain and V13 provenance is only a run name. A later regression manifest labeling these assets `scene_generation` is not independent proof of stage. Separately, `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/data/published_report.json` verifies that each gallery upload has the same SHA-256 as its preserved source-report asset; byte identity does not resolve stage provenance.

Per the v2 split instruction, the former v1 held-out rows 9, 10, 12, 13, 26, and 29 now belong to training evidence. The four latest user labels remain a distinct adjudication set. Because their images overlap prior pilot material, results on them must not be described as unseen generalization.
