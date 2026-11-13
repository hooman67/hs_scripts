# Astra consultation summary

The compact v2 consultation completed successfully and produced usable visible output. The full, unedited answer is in `response.md`.

Its central recommendation is a narrow policy change: remove the high-fill/close exception, use the same translation-only contract for every view, run every first attempt with `fixed_position=False`, and retain one fixed-position recovery attempt after any guard rejection.

The most material guard recommendation is broader than a prompt-only change. Astra advises that a passing affine fit must also pass product-mask appearance verification because affine geometry alone does not establish identity, full visibility, or absence of a duplicate. For low-texture products, it proposes expanding the existing RGBA fallback into a full-canvas, translation-only search using oriented silhouette, internal-edge, high-pass, and direct interior RGB evidence, with ambiguity or inadequate evidence returning `unverifiable`.

Astra explicitly says the available inputs cannot prove literal pixel preservation. Its numerical mask-verification thresholds are proposals, not validated settings. They require synthetic injection tests and real high-fill/close plus medium/wide GPT Image trials before adoption.
