# Candidate leave-family-out visual calibration

This is an **unfrozen, unevaluated candidate** for V4.1. It does not alter or participate in the frozen V4 development run.

The runtime would prepend at most four small scene-image anchors with concise, comment-grounded calibration guidance. Target images still arrive as the generated scene plus original twin. The target block contains only product type, scene prompt, stage, and images; it never includes the target's comment, expected issue, score, or verdict.

For every target, the builder excludes an anchor when any of these hold:

- exact generated-image SHA-256;
- same twin-image SHA-256;
- exact scene-prompt SHA-256;
- same device + camera + prompt-rank family;
- same product-type + camera + prompt-rank near-duplicate family.

Selection is deterministic and independent of target annotations. Laptops receive one anchor each for chair calibration, support layout, support anatomy, and observation/scope. Printers receive one each for support layout, support anatomy, device position/orientation, and observation/scope. Within a category, the selector prefers the same product type and comparable camera framing. The hard bound is four anchors. Only the 13 cases with explicit human verdicts can be anchors; the two comments without absolute verdicts remain targets but never calibration examples.

`build_anchor_candidate.py` verifies annotation/catalog hashes, source image hashes, thumbnail hashes, the per-target exclusion rules, selection count, and absence of target labels in runtime metadata. It produces `anchor_catalog.json` and `target_anchor_plan.json`. These artifacts are design evidence only; no model call has been made.
