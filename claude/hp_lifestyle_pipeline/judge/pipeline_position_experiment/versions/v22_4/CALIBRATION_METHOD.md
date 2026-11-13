# V22.4 textureless guard calibration method

As of 2026-11-06, this is an in-progress, fixed-position-only fallback calibration. It does not change or overwrite any V22.3.3 run artifact.

## Evidence set

- 31 preserved real image attempts have an RGBA product mask, geometry guide, raw generated attempt, and affine audit.
- Affine labels: 23 accepted, 6 rejected, and 2 `too_few_matches` attempts from the preserved failed full-160 first row. The two unverified attempts are held out from threshold selection.
- Each distinct fixed-position product/camera silhouette also receives deterministic synthetic checks: identity, allowed 8-pixel translation, brightness shift, forbidden 12-pixel translation, 0.96/1.04 scale, +/-2-degree rotation, 0.04 shear, 1.04x0.96 anisotropic scaling, and a featureless dark product fill.

## Candidate metric

The fallback uses the persisted product alpha mask rather than a dark-pixel detector. It searches integer translations only within +/-8 pixels and measures:

1. alpha-silhouette boundary coverage by output edges within 2 pixels;
2. source-product internal-edge coverage by output edges within 2 pixels;
3. masked high-pass normalized cross-correlation, which is insensitive to mean brightness;
4. a minimum count of source internal-edge samples.

The best translation is selected by a frozen composite ranking before pass thresholds are applied. A conjunction of the four thresholds must separate all labeled fixed-position real attempts and synthetic negatives with zero false accepts and zero false rejects. In particular, a solid dark region may have the right silhouette but must fail the internal-structure and high-pass requirements.

## Scope and stop rule

The two `too_few_matches` attempts do not influence thresholds. They are evaluated only after thresholds are frozen. A lower-fill whole-frame fallback will not be added unless separate labeled textureless lower-fill evidence supports it. No full-160 run or S3 publication is allowed in this work unit.
