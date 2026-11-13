# Four-fixture mechanical smoke audit

Frozen: 2026-11-06. This audit covers the fresh treatment run after the
model-facing `reference` wording fix. It does not reuse the failed pre-contract
fixture.

## Contract evidence

- Four of four rows completed: Cashmere laptop close and wide, Magic printer
  close and wide.
- Every row used the exact frozen control product, style image, and byte-identical
  geometry guide.
- Every row recorded exactly `selection_replay`, `geometry_replay`, one live
  `astra_write`, and one live unmasked `image_edit` call.
- Every row returned `status=ok`, `image_calls=1`, and `masked=false`.
- The final prompt for every row passed the unseen-image-reference contract; no
  manual prompt repair or image retry was used.
- Source was pinned to Adobe-Firefly/foundry PR 4349 commit
  `8c358bc7989cb0e137e89db0fd325168249e2a22` and the five hashes stored in
  `manifest.json`.

## Prompt-policy behavior

All four Stage-B compositions retained the baseline product location. The
translation exception remained optional and was constrained to a common
image-plane translation of the product and its support relationship. The writer
preserved scale, orientation/view, visible faces, perspective, and access/contact
requirements in each assembled prompt.

## Visual review

Side-by-side review found no obvious product rotation/view drift, mirror,
clipping, support/contact break, or scale change in the treatment images. Product
movement was minimal or absent, which means the smoke establishes mechanical
coherence but does not establish that allowing translation improves placement.
The full 160-row run is needed to measure whether difficult compositions exercise
the exception and improve the placement judge without increasing orientation
failures.

## Reproducible artifacts

- `manifest.json`: row inputs, hashes, models, call trace, and output hashes.
- `control_vs_treatment.jpg`: visual comparison sheet.
- `<row>/run/rows/<row>/result.json`: assembled prompt and pipeline metadata.
- `<row>/run/rows/<row>/ours.png`: treatment output.

