# V23.1 strong low-inlier affine candidate

This read-only candidate evaluates a narrow reliability exception exposed by
the Tassel `printer_FrontWide` pilot. The accepted V23 guard and run-3 evidence
remain unchanged.

The ordinary threshold remains 20 inliers. A fit with 17--19 inliers can avoid
the alpha fallback only when it has at least 0.70 inlier ratio, 0.70/0.60 source
span, four-quadrant coverage, 0.25 hull coverage, and every existing non-count
invariant passes. This includes fixed-translation checks in recovery mode.

No image generation or model calls are performed. The package replays frozen
real/synthetic evidence, the added V23 adversarial suite, prior artifacts, and
the two pilot attempts against a copied candidate module.
