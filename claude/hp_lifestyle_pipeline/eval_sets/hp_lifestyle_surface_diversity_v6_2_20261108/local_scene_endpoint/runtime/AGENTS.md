# 1. Experiment-specific guidance

- Start with README.md and CONTEXT.md. Experiment records, data, and generated results belong in the linked S3 snapshot, not Git.
- Run all offline checks from this directory: `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m pytest tests -q -p no:cacheprovider` and `ruff check --select F,E9,I hp3p tests`.
- Never start paid model calls, regenerate images, republish assets, or overwrite run records unless explicitly requested.
- Preserve the one-image-call contract, untouched raw bytes at the selected 1216x912 or 2368x1776 canvas, and separate grading outputs. Do not reintroduce alignment, product pasting, outpainting, or automatic retries.
- A successful API response is not visual acceptance. Camera estimates and masks do not guarantee product fidelity.
- Historical helper scripts in S3 contain machine-bound paths and guard assumptions. Read the linked archive README before using them.
- When a displayed result is overridden, its final prompt must come from the same generation. Case 43 uses the source-camera-fit-v2 pilot, not its previous full-run prompt.
- Generate directly from the original user request; never feed HP12 rewritten fields to Astra or use them as a fallback. There is no legacy mode.
- Require one large physical blue surface/furnishing or multiple substantial visible blue elements by default, not token props, thin frames, screens, sky or casts. Explicit minimal-blue, amount/carrier or exclusion requests override it; preserve product framing/finish and avoid a universal cobalt hex or coverage percentage.
- Bump `PIPELINE_VERSION` when generation policy changes; do not silently reuse historical or incompatible caches.
- Prefer user-supplied dimensions with verbatim source quotes; otherwise use explicitly assumed category-level dimensions, not verified SKU specifications. Propagate size provenance and axis assumptions to the image prompt.
- Historical prompts retain the restrictive cobalt rule. Do not rewrite them or present earlier outputs as visual validation of the current policy.
- `--blue-histogram` enables the reference-anchored single-reference policy; conditional physical-scale planning applies in both modes. Keep both policy versions/cache guards consistent. Use the full tagged catalog, not a permanently no-human subset.
- Human eligibility follows the original request and existing `human`/`no_humans` tags, with no cross-tag fallback or human reannotation. Do not inherit old people-containing captions onto removal variants.
- Blue is text-only: everyday blue color names, no histogram HEX substitution, `blue_elements` or claimed reference match. Avoid orange or global blue casts. The histogram only gates the mode and cache identity.
