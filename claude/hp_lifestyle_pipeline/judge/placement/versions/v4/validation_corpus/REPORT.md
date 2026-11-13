# Natural Placement Judge V4.1 comment-grounded validation inventory

This is a **development corpus**, not a held-out test set and not an accuracy
estimate. It contains 84 V6 scene-generation rows with non-empty
human comments. The source FE button choices are ignored because the reviewer
said those buttons were used incorrectly.

## Evidence strata

| Evidence class | Rows | Meaning |
|---|---:|---|
| Direct verdict or ambiguity label | 10 | The free-text comment itself says pass, fail, weak/borderline pass/fail, or ambiguous. Qualifiers remain explicit. |
| Issue/assessment only | 15 | The comment identifies a concrete concern or assessment but gives no direct rubric verdict. |
| Relational agreement + concrete comment | 12 | The reviewer agrees with the displayed prior judge and adds concrete evidence. The prior V2 result is preserved as reference provenance, not as an independent human label. |
| Relational agreement only | 47 | Bare agreement is linked to the exact frozen V2 result and never promoted to an independent human verdict. |

The directly stated labels are: 4 pass,
5 fail, and
1 ambiguous. These small,
development-selected counts are unsuitable for estimating production accuracy.

## Inclusion and exclusions

- Included: all 84 persisted rows with non-empty comments.
- Excluded: 5 persisted rows with empty comments; an empty
  comment is not treated as a pass.
- Excluded: 7 report rows
  absent from the saved annotation snapshots; absence is not treated as review.
- Runtime target assets are scene-generation outputs only. The twin remains a
  product reference.

## Integrity checks

- Every generated scene and twin local file was opened and checked against the
  frozen SHA-256, byte size, and dimensions.
- Every annotation snapshot matches its frozen SHA-256.
- Every relational agreement points to a frozen V2 result whose file hash was
  rechecked. Its verdict and explanation are explicitly marked reference-only.
- Asset joins use exact row ID, never row position.

## Files

- Machine-readable inventory: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4/validation_corpus/manifest.json`
- Reproducible builder: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4/validation_corpus/build_validation_corpus.py`
- This report: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4/validation_corpus/REPORT.md`
