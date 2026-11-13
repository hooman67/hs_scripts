# Preparation validation

As of 2026-11-05 America/Los_Angeles, this package was tested without launching an endpoint or making model, image, or S3 calls.

- Python compilation: pass.
- Shell syntax (`bash -n`): pass.
- Frozen input verification: pass, 160 rows, 16 banks, ranks 1–10.
- Prompt export: pass, SHA-256 `adcb9edb2643e45acb0cb882cdc4d65b8c256a52d58ad4a44ddd9c235287b3cd`.
- Foundry base commit: pass, `8c358bc7989cb0e137e89db0fd325168249e2a22`.
- Isolated output/collision check: pass.
- FE source/group validation: pass, 16 banks × 10.
- Unit contract tests: 4/4 passed. They cover atomic progress replacement, frozen grouping, exact preflight/report-source validation, and rejection of a guard-selected failed image.

The preparation does not claim that V22.3.3 image quality or placement quality passes the experiment gate. That decision depends on the separate smoke review and must precede launch.

