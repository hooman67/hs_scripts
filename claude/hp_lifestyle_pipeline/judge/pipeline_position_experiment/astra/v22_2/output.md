## A. Replacement central policy block

```text
Determine density from the existing product guide bounds on the current canvas. HIGH-FILL/CLOSE applies when product width or height is at least 45% of the corresponding canvas dimension. LOWER-FILL/MEDIUM-WIDE applies only when both are below 45%.

In both branches, preserve product identity, exact pixel width and height, yaw/pitch/roll, visible faces, camera-facing surfaces, projection, perspective, foreshortening, silhouette proportions, state, finish, details, and full visibility.

HIGH-FILL/CLOSE: Preserve the product's exact initial x-y coordinates from the supplied guide. This is unconditional: do not test relocation feasibility and do not move the product even if exact size and all other invariants could be preserved. Drop any user relocation, centering, layout, emphasis, support-edge, or composition request that conflicts with this fixed product position. Independently recompose support and room around the fixed product.

LOWER-FILL/MEDIUM-WIDE: Choose product x-y freely for usable composition, using rigid image-plane translation only. Movement is optional. Independently recompose support and room beneath/around the product; product and support need not move together. Preserve every product invariant.

The final executable prompt must retain the product invariants and include verbatim the density-selected active-branch message and the universal exact-size fallback. Planning text alone is insufficient. For HIGH-FILL/CLOSE, omit conflicting product-position instructions from the executable prompt.
```

## B. Deterministic messages

Inject only the density-selected message, verbatim, into both Stage B and the final executable prompt.

**HIGH-FILL/CLOSE**
```text
ACTIVE BRANCH: HIGH-FILL/CLOSE. Keep the product at its exact initial x-y coordinates in the supplied guide, preserving exact pixel width and height and every other product invariant. Do not test whether relocation is feasible; do not move the product even if exact size could be preserved. This rule overrides any conflicting user relocation, centering, layout, emphasis, support-edge, or composition instruction. Independently recompose support and room around the fixed product position.
```

**LOWER-FILL/MEDIUM-WIDE**
```text
ACTIVE BRANCH: LOWER-FILL/MEDIUM-WIDE. Choose product x-y freely for usable composition using rigid image-plane translation only; movement is optional. Preserve exact pixel width and height and every other product invariant. Never resize, reorient, reproject, or crop the product. Independently recompose support and room beneath/around the product; product and support need not move together.
```

## C. Final-check wording

```text
Before emitting the final executable prompt, verify that it contains the unchanged product invariants, exactly one density-selected active-branch message, and the universal exact-size fallback verbatim. For HIGH-FILL/CLOSE, remove conflicting product-position instructions and any conditional permission to move. For LOWER-FILL/MEDIUM-WIDE, retain optional rigid image-plane translation and independent support composition.
```

**Universal exact-size fallback — include verbatim in the executable prompt:**
```text
Preserve exact product pixel width and height and every other product invariant. Never shrink, enlarge, zoom, reframe, rotate, reproject, or crop the product to make a move feasible. Where translation is allowed, if a move cannot preserve every invariant, retain the initial x-y coordinates instead.
```

## D. Contradiction audit

- Remove HIGH-FILL qualifiers such as **“by default,” “prefer,” “unless needed,”** and **“may move if exact size holds.”**
- Scope **“choose x-y freely”** and relocation-feasibility language to LOWER-FILL only.
- Remove conflicting HIGH-FILL relocation instructions from the executable prompt; do not merely append a competing instruction.
- Remove any common product+support translation requirement.
- Scope mandatory initial x-y retention to HIGH-FILL and the infeasible-move fallback; do not impose it unconditionally on LOWER-FILL.

## E. Focused rerun assertions

For all six reruns, verify deterministic branch selection from the unchanged guide bounds and presence of the active branch, product invariants, and fallback in the executable prompt.

| Fixtures | Assertions |
|---|---|
| Laptop + printer close neutral | HIGH-FILL; exact initial x-y and pixel dimensions; all other invariants preserved. |
| Laptop close adversarial relocation | HIGH-FILL; conflicting relocation language removed; neither translation nor shrinking permitted. |
| Printer close adversarial relocation | HIGH-FILL; no translation, even when exact size could be maintained. |
| Laptop + printer lower-fill wide relocation | LOWER-FILL; optional rigid x-y translation remains permitted; support may be independently recomposed; exact dimensions and all other invariants remain mandatory. An infeasible move retains initial x-y. |

Record transform metrics without changing acceptance criteria: lower-fill scale drift remains an invariant failure, but does not justify restricting lower-fill translation in this delta.
