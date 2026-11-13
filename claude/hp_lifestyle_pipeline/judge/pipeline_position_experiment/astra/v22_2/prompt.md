You are reviewing a narrow system-prompt change for Adobe-Firefly/foundry PR 4349's HP image pipeline. Return exact wording for the smallest prompt-only delta. Do not propose code, masks, image retries, coordinate post-repair, Stage-A changes, guide-renderer changes, or unrelated rewrites.

Pipeline context:
- Stage A and the geometry guide remain fixed at the digital twin's supplied baseline coordinates.
- Stage B and GPT Image receive the guide containing real product pixels plus text.
- Downstream stages paste exact digital-twin pixels back, so the product's identity, exact pixel width/height, yaw/pitch/roll, visible faces, camera-facing surfaces, projection, perspective, foreshortening, silhouette proportions, state, finish, details, and full visibility must not change.
- Support and room may be independently recomposed beneath/around the product. No common product+support translation lock.
- For lower-fill views, the product may change x-y by rigid image-plane translation only; scale and all other invariants stay exact.
- Density is deterministic from the existing product guide bounds: HIGH-FILL/CLOSE when width or height is at least 45% of current canvas; LOWER-FILL/MEDIUM-WIDE only when both are below 45%.
- Final image prompt is executable; planning text alone is insufficient.
- Avoid the token `reference` in proposed executable wording because a safety validator rejects unseen-image references.

v22.1 policy:
- High-fill retained initial x-y by default but allowed movement if exact size/invariants held.
- Lower-fill chose x-y freely with independently recomposed support.
- Universal fallback said never shrink/enlarge/zoom/reframe/rotate/reproject to make a move feasible; retain initial x-y instead.

Frozen eight-fixture evidence:
- laptop close neutral: scale .9987, rot .032°, tx +2px — fixed.
- laptop close adversarial relocation: scale .8729, tx -268px — failed by shrinking under conflicting user relocation language.
- printer close neutral: scale 1.0003, rot .011°, near-zero translation — fixed.
- printer close adversarial relocation: scale .9954, tx +425px — size held but moved; high-fill should now remain fixed regardless.
- laptop wide neutral: scale 1.0029, near-zero translation — good.
- laptop wide relocation: scale .9019, tx +815px — stochastic exact-scale failure; do not change/over-tune lower-fill here.
- printer wide neutral: scale .9989, near-zero translation — good.
- printer wide relocation: scale .9932, tx +949px/-153px — useful near-scale-preserving relocation.

Required v22.2 behavior:
1. HIGH-FILL/CLOSE is a hard rule: preserve exact initial x-y coordinates as well as all existing product invariants. Ignore/drop any user relocation, centering, layout, emphasis, support-edge, or composition request that conflicts with fixed product position. Do not test feasibility and do not move even if size could remain exact. Independently recompose support and room around the fixed product position.
2. LOWER-FILL/MEDIUM-WIDE remains exactly as v22.1: choose x-y freely for usable composition, with independently recomposed support; movement optional; never resize/reorient/reproject/crop.
3. Final executable prompt must contain the active branch and a universal exact-size fallback. For high-fill it must unambiguously override conflicting relocation language.
4. Stage A, guide, schemas, masks, product pixel scale, and lower-fill behavior remain unchanged.

Return:
A. The exact replacement central policy block.
B. Exact deterministic HIGH-FILL and LOWER-FILL messages injected into Stage B and the executable prompt.
C. Exact final-check wording, concise and non-contradictory.
D. A short contradiction audit listing phrases to remove or scope.
E. Focused assertions for rerunning laptop+printer close neutral, close adversarial relocation, and lower-fill wide relocation.
