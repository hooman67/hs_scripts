# v22.1 density-conditioned eight-fixture smoke

All eight frozen fixtures completed with one live Stage-B call and one unmasked image call, no retries, best-of selection, or manual repair. Stage A, product/style inputs, camera metadata, and guide bytes were frozen from the V6.1 controls.

SIFT/RANSAC affine estimates are product-landmark diagnostics, not pixel-perfect masks.

| Fixture | Mode | Class | Scale | Rotation | Translation x,y | Finding |
|---|---|---|---:|---:|---:|---|
| Laptop close | neutral | High-fill | 0.9987 | +0.032° | +2, 0 px | Pass: exact-position default worked |
| Laptop close | relocation | High-fill | 0.8729 | +0.277° | -268, +4 px | Fail: shrank 12.7% to obey conflicting relocation |
| Laptop wide | neutral | Lower-fill | 1.0029 | +0.125° | -1, -5 px | Pass: retained initial placement |
| Laptop wide | relocation | Lower-fill | 0.9019 | +0.343° | +815, +49 px | Fail exact-scale contract; useful relocation but shrank 9.8% |
| Printer close | neutral | High-fill | 1.0003 | +0.011° | 0, -1 px | Pass: exact-position default worked |
| Printer close | relocation | High-fill | 0.9954 | -0.022° | +425, 0 px | Product size/view held, but movement conflicts with intended conservative high-fill behavior |
| Printer wide | neutral | Lower-fill | 0.9989 | +0.066° | +3, -1 px | Pass: retained initial placement |
| Printer wide | relocation | Lower-fill | 0.9932 | +0.583° | +949, -153 px | Pass diagnostic: actual relocation with near-unit scale; visually inspect orientation/contact |

The evidence supports a hard high-fill branch rather than a conditional permission: keep initial x-y exactly and ignore conflicting relocation/layout language, while independently recomposing support/room. Lower-fill remains free to translate. The laptop lower-fill relocation was stochastic regression versus v22's successful scale-preserving result; v22.2 should not change or over-tune that branch.
