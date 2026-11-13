# HP support-top geometry: reviewed runtime candidate

As of 2026-11-09, this directory contains the user-approved isolated runtime and localhost API for
rectangular, round and oval HP primary-support tops. Eight image smoke cases passed the support
integration gate, and the remaining 152 images are running. The Foundry experiment checkout is
unchanged. The live endpoint uses generation enabled; a fresh launcher defaults to disabled.
The canonical live checkpoint is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/PROJECT_STATE.md`.

## Current handoff

- Full clean runtime package:
  `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/local_scene_endpoint/runtime/`
- Complete patch against Foundry commit `8c358bc7989cb0e137e89db0fd325168249e2a22`:
  `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/local_scene_endpoint/runtime_surface_shape_r1.patch`
- Version, hashes, environment, verification and known inconsistencies:
  `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/local_scene_endpoint/runtime_surface_shape_r1_manifest.json`
- Complete endpoint/wrapper/reference/input manifest:
  `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/local_scene_endpoint/deployment_manifest.json`
- Earlier geometry-only source/baseline and its focused patch remain under `base/`, `candidate/` and
  `geometry_shape_candidate.patch` for audit. The runtime patch is the complete handoff.

VERIFIED on 2026-11-09: the source commit exists in the local Foundry Git object database. The dirty
checkout at `/home/colligo/foundry-pr4349-position-exp` was read but not modified. The durable
`hs_scripts` checkout resolves physically to `/home/colligo/hs_scripts`.

## Integrated behavior

- `support_top_shape` is a strict planner field with `rectangular`, `round` and `oval`.
  Direct legacy callers that omit it retain the pinned rectangular behavior.
- Rectangular guide bytes and metadata remain exactly compatible with the pinned implementation.
- Round and oval outlines are built in the physical support plane and projected through the same
  estimated or digital-twin camera. Round diameters must be equal; oval diameters must be unequal.
- The gap reaches the curved rim along the selected user-side axis at the point aligned with the
  product center. All four fixed product-footprint corners must remain inside the ellipse.
- Product source pixels, anchor, footprint, axes, orientation, position and size stay fixed.
- Non-laptop geometry prose remains support-category-neutral, so a cabinet, credenza or fitted
  counter is not relabeled as a table.
- `PIPELINE_VERSION` is `unified-blue-scale-v20-surface-shape-r1`.
- The reviewed Geometry system section and five shape-aware pipeline constants match
  `root_reviewed_policy.json` exactly. The original `_PRINTER_WALL` and
  `_WRITE_PRINTER_WALL` assignment source is byte-identical to the pinned commit. Every other
  system-prompt section is byte-identical to the pinned commit.

## Validation

All offline checks used Python 3.12 and the package's real pinned dependencies through uv. No fake
OpenAI module or other dependency stub was used.

```text
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --python 3.12 --with-requirements requirements-dev.txt python -m pytest tests -q -p no:cacheprovider
157 passed in 33.14s

uv run --python 3.12 --with-requirements requirements-dev.txt ruff check --select F,E9,I hp3p tests
All checks passed!
```

The focused geometry suite passed 54 tests. Additional read-only checks verified strict-schema
closure for geometry/twin-plan schemas, exact reviewed constant values, exact system-section
boundaries, pinned printer-wall assignments, and unchanged non-replaced pipeline AST. The complete
patch passed `patch --dry-run -p1`, applied cleanly to a fresh Git archive, and produced a tree
byte-identical to `runtime/`.

## Preserved inconsistencies and limits

The manifest records four boundaries that were not silently edited:

1. The untouched Product-first prompt permits an unspecified printer shelf, side table or credenza,
   while the reviewed Geometry section narrows the default to a substantial cabinet, low credenza,
   fitted counter or dedicated equipment table.
2. A policy change note describes support-level wall anchoring, while the root review rejects that
   change and the preserved wall constants still put the printer chassis against the wall. The
   executable constants and root review take precedence in this integration.
3. Reference-anchored mode still uses its old `ReferenceBlue.VERSION`. If that mode is deployed
   with this prompt, its cache version needs a separate decision. The default-mode cache has the
   requested new `PIPELINE_VERSION`.
4. Pinned package README/CONTEXT prose describes earlier versions and remains unchanged because the
   authorized source scope was geometry, the reviewed prompt section/constants, version and tests.

The ellipse is rasterized as a 128-segment outline. Invalid curved geometry is rejected; the code
never repairs it by moving, rotating or resizing the product. Smoke inference passed on 2026-11-09;
that result is an integration check, not a calibrated image-quality or exact-pixel guarantee.

## Local scene endpoint

The wrapper preserves the V6.2 runner contract:

- `GET /api/credentials` returns the instance CSRF token.
- `GET /api/catalog` returns four devices, exactly four fixed views per device, the same 341
  byte-deduplicated references, and the candidate lineage.
- `POST /api/generate` accepts only `digitalTwinId`, `cameraId` and `prompt`.
- `GET /api/jobs/{job_id}` returns live-style hero/scene stage status and skips all downstream
  relight stages.
- `GET /api/jobs/{job_id}/artifacts/2_scene.png` returns the untouched model PNG after completion.
- `GET /api/jobs/{job_id}/debug` and `GET /api/debug/imports` expose source/import provenance but
  no provider credential values.

The default localhost URL is `http://127.0.0.1:8137`. Start the offline-safe process in a persistent
tmux session:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/local_scene_endpoint
./launch_endpoint.sh hp-v62-shape-endpoint 8137 0
curl -fsS http://127.0.0.1:8137/health
curl -fsS http://127.0.0.1:8137/api/catalog
curl -fsS http://127.0.0.1:8137/api/debug/imports
```

The third launcher argument is the paid-generation gate. The user approved this isolated fix on
2026-11-09, and the live session uses `1`. Do not restart an existing healthy endpoint during its
160-image run. The endpoint still requires its CSRF token and matching localhost origin.

The wrapper uses the pinned package's exact `gpt-6-astra` and
`gpt-image-2.5-sunburst-2026-09-08` IDs. The image request remains one `images.edit` call at
2368x1776, `n=1`, high quality, opaque PNG, using only the generated guide and no mask. The server
uses `foundry-aws-gateway[llm]==2.0.0` for server-managed OpenAI access and stores no credential
value. Startup constructs the real provider client without issuing a model request; health reports
that preflight result. The same check can be run explicitly with `python preflight_provider.py`
inside the pinned endpoint environment.

Rebuild the 16-view bundle, deployment manifest and offline wrapper tests with:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/local_scene_endpoint
python prepare_input_bundle.py
uv run --python 3.12 --with-requirements endpoint-requirements.txt \
  --extra-index-url https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple \
  python build_deployment_manifest.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --python 3.12 \
  --with-requirements runtime/requirements-dev.txt --with fastapi --with 'uvicorn[standard]' \
  --with 'foundry-aws-gateway==2.0.0' \
  --extra-index-url https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple \
  python -m pytest test_endpoint.py -q -p no:cacheprovider
```

`631fe047e7b82c6c690f038effda1155b0ffde5ecdbf8be745164db649a80de5` is explicitly the
41-file candidate code-tree digest. Restored reference files are outside that digest and pinned
separately in `deployment_manifest.json`. The endpoint config SHA-256 is
`9ae1f16c2ace027ad6da157356e5025c1ae06722f6c4cb2955b15f0a959b4b08`; the complete deployment
manifest SHA-256 is `b2a852792ef8029e867fb37c3c21c394d6e47fed7e81dc103fbe726d0ec0604c`.

The first eight-row smoke under deployment manifest `d81b3667...` failed before provider-client
construction because the core gateway package omitted its declared `llm` extra. All eight terminal
jobs remain under `run/jobs`; no image exists and no provider model request was made. Sanitized,
hash-pinned evidence is in `failed_smoke_20261109_manifest.json`.

