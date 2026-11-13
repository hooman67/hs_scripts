# V22.4.1 alpha-mask fallback calibration report

As of 2026-11-06, this work is a bounded development candidate. No full-eight or full-160 generation and no S3 upload has been run.

## Result

The affine guard remains authoritative whenever it can fit a transform. The new fallback runs only when the affine result is `no_descriptors` or `too_few_matches`, only for `fixed_position=true`, and only when the persisted RGBA product alpha mask is available. Lower-fill products remain affine-only because there is no labeled textureless lower-fill calibration set.

The fallback searches integer translation in `[-8,+8]` pixels and requires all of:

- alpha silhouette boundary edge coverage within 2 pixels: at least **0.80**;
- internal edge coverage floor: at least **0.20**;
- either internal edge coverage at least **0.80** or masked high-pass NCC at least **0.80**;
- at least **100** internal edge samples.

The internal-edge floor prevents a uniformly dark region from passing based only on product color and silhouette.

## Calibration evidence

The independent calibration excludes the later V22.4 fresh retry.

- 31 preserved real attempts: 23 affine passes, 6 affine failures, 2 prior `too_few_matches` attempts held out from threshold selection.
- 55 deterministic synthetic attempts on five distinct real product/camera silhouettes.
- Synthetic negatives include 12-pixel translation; 0.975 and 1.025 scale; +/-1.1-degree rotation; 0.025 shear; 1.025x0.975 anisotropic scaling; and a solid dark product fill.
- Synthetic positives include identity, exactly 8-pixel translation, and a strong brightness shift.

At the frozen 0.80 boundary threshold:

- synthetic false accepts: **0**;
- synthetic false rejects: **0**;
- known fixed-position affine failures that the fallback would falsely accept: **0**.

The maximum synthetic-negative boundary coverage among samples that satisfy the other gates is 0.7493 (0.025 shear), leaving about 0.05 absolute margin.

## Preserved V22.3.3 failed row replay

The source row is `cashmere__laptop_BackRightCloseUp__p1`.

- Original attempt 1: primary affine `too_few_matches`; fallback boundary 0.9097, internal 0.8663, high-pass NCC 0.4707, translation (+1,-1); **pass**.
- Original attempt 2: primary affine `too_few_matches`; fallback boundary 0.7935, internal 0.9627, high-pass NCC 0.4507, translation (+1,-1); **fail** on boundary.

## Fresh first-row development retry

V22.4 initially used a 0.85 boundary threshold. The fresh generation produced two raw attempts and selected none:

- Fresh attempt 1: primary affine `too_few_matches`; boundary 0.8323, internal 0.8891, high-pass NCC 0.5023, translation (+1,-1). It looked faithful in the contact sheet but failed the 0.85 boundary rule.
- Fresh attempt 2: primary affine `too_few_matches`; boundary 0.6553, internal 0.9565, high-pass NCC 0.4032, translation (0,0). It was visually degraded and failed the boundary rule.

The fresh retry was then treated as development evidence, not added to calibration. An independent recomputation at 0.80 retained zero calibration false accepts/rejects and retained a 0.05 margin over the hardest synthetic negative. V22.4.1 therefore froze 0.80. Deterministic replay, without a new model call, selects fresh attempt 1 and rejects fresh attempt 2.

## Verification

- Package tests: **168 passed**.
- Focused invariant tests cover bounded translation acceptance and rejection of scale, rotation, shear, and a featureless dark fill.
- The V22.3.3 failed-row artifact tree was SHA-verified before the fresh retry and remains preserved.
- V22.4's failed fresh retry is frozen separately before the V22.4.1 threshold change.

## Gate decision

V22.4.1 is ready for review and, if approved, the remaining full-eight smoke. It is not yet approved for full-160 generation.
