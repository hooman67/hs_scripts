# 1. Reproducing and inspecting the experiment

## 2. Environment

Use Python 3.12 or newer. The dependency files record the versions used for this handoff:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Paid generation also requires authorized access to Adobe's `platforms.dev_tools.vault`, AWS CLI credentials for the HP asset bucket, and the configured model IDs. The Adobe integration is supplied by the internal Colligo development environment, not a public package named `platforms`. No tokens are included.

The image model is `gpt-image-2.5-sunburst-2026-09-08`; text rewriting uses `gpt-6-astra`. Availability may change after this snapshot.

## 3. Offline validation

From the experiment directory:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m pytest tests -q -p no:cacheprovider
ruff check --select F,E9,I hp3p tests
git diff --check
```

The tests use synthetic fixtures and require no downloaded evaluation/reference data. Run the explicit `tests/` directory, not historical test snapshots downloaded from S3. The source baseline contained 82 passing tests at export time.

## 4. Fetch runtime inputs from S3

Authenticate using the normal internal AWS process. Do not copy credentials from another user's shell or put them in configuration files.

Fetch only the four inputs needed by the CLI; no experiment outputs are required for this step:

```bash
aws s3 sync \
  s3://foundry-hp-enterprise-adobe-assets/adarabi/hp-3p-gpt25/handoff-20261027/ \
  . --exclude "*" \
  --include "foundry_subset_48_pr35902_gemini.json" \
  --include "baseline_compare.json" \
  --include "hp3p/data/ref_captions.json" \
  --include "assets/styles.json" \
  --only-show-errors
```

These paths are ignored by Git. The original source catalog has 343 entries; `load_catalog` byte-deduplicates it to 341. The exact S3 locations follow the same relative paths as the code's inputs. Section 7 explains the original catalog-path override.

## 5. Inspect the complete snapshot and verify integrity

The [README](../README.md#2-start-here) links directly to the saved HTML, exact prompts, and manifests. The HTML uses absolute corporate asset URLs, so it can be opened without downloading all images. Corporate asset access is still required.

To inspect every archived experiment locally, restore to a separate ignored directory rather than adding the records back beside the source:

```bash
aws s3 sync \
  s3://foundry-hp-enterprise-adobe-assets/adarabi/hp-3p-gpt25/handoff-20261027/ \
  .artifacts/handoff-20261027/ --only-show-errors
```

This is a large download (over 1.6 GB), including images, reference data, historical records, and generated results. Verify both the original binary/reference-catalog inventory and every relocated text/data artifact:

```bash
python - <<'PY'
import hashlib
import json
from pathlib import Path
root = Path(".artifacts/handoff-20261027")
for name in ("artifact_manifest.json", "text_transfer_manifest.json"):
    manifest = json.loads((root / "results" / name).read_text())
    for entry in manifest["artifacts"]:
        path = root / entry["path"]
        assert path.stat().st_size == entry["size"], path
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"], path
    print(f'{name}: verified {len(manifest["artifacts"])} artifacts')
PY
```

The original export manifest describes the earlier copied source/text snapshot, not the current code-only Git layout.

## 6. Rebuild reports without generating

After fetching the runtime inputs in section 4, restore just the run you want to inspect. The source CLI can render it without loading the model client:

```bash
aws s3 sync \
  s3://foundry-hp-enterprise-adobe-assets/adarabi/hp-3p-gpt25/handoff-20261027/runs/full-single-ref-nearest-grade-20261027/ \
  runs/full-single-ref-nearest-grade-20261027/ --only-show-errors
python -m hp3p.cli report --run-id full-single-ref-nearest-grade-20261027 --refs 1
```

This renders the diagnostic `viewer.html`, not the specially curated team page.

For the team page, `hp3p.report.render_comparison` accepts `graded_output_urls` and `prompt_overrides`. A replacement image requires its own exact final prompt. Use the snapshot's `results/prompts.json`; case 43 points to the source-camera-fit-v2 pilot. Never rebuild it from the previous case-43 metadata alone.

The snapshot's `archive/helpers/regenerate_team_with_model_prompts.py` records the exact procedure and verification used. It is a historical, machine-bound driver with overwrite guards, not a portable command to run blindly.

## 7. Paid generation, only after explicit approval

The source CLI's `CATALOG` constant preserves the original machine path for provenance. After section 4, use the downloaded catalog without modifying the source:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -c \
  'from hp3p import cli; cli.CATALOG = "assets/styles.json"; cli.main()' \
  run --run-id NEW_APPROVED_RUN_ID --ids 0043 --refs 1 --workers 1
```

That command makes paid text/image API calls. It uses the unified original-request
pipeline directly; there is no legacy or rewriter switch. Do not execute it just
to validate the handoff. Select a genuinely new run ID and review the intended
scope first. Same-policy cached results, including errors, are returned without
retry. Historical/earlier-policy caches, changed original requests, sizes or reference counts are
rejected rather than silently mixed. Use the `report` command in §6 to inspect
old runs without generating.

The default input/output canvas remains `1216x912`. Add `--size 2368x1776` to the
approved command for native high-resolution generation. Source products are
uniformly prepared at that size; masks, geometry guides and output validation
use it too. A wrong-size model response is preserved as an error, never upscaled
or repaired.

The original user request is required. HP12 rewritten fields are not supplied
to Astra, even as a fallback. With no explicit blue preference, Astra is
instructed to include one large physical blue surface/furnishing or multiple
clearly visible blue elements with substantial combined area. Tiny props, thin
partition frames, screens, sky and lighting casts alone do not qualify. Minimal
blue, explicit amounts/carriers or exclusions override this default. Planner
input, system instructions and final assembly preserve that priority without a
universal cobalt hex or coverage percentage. The `unified-blue-scale-v17-plain-geometry` policy
keeps V8 composition with concise scale instructions and a planner-placed
support (laptops near the user-facing desk edge; printers square to the support
edges). Astra plans geometry first,
then writes the prompt in plain visual words after seeing the drawn guide; its
`layout` field replaces the numeric geometry summary in the image prompt. It rejects earlier v3-v16,
`unified-blue-v2` and local `unified-blue-scale-v2` caches. Use a fresh run ID
rather than relabeling old results.

Supply physical product dimensions in the original request, for example
`Product dimensions: 15.7" x 15.7" x 13.4".` No separate CLI flag is needed.
Labelled triplets support inches, mm, cm and m; code preserves dimension order
without assigning axes and passes the normalized triplet to the geometry planner.
Other wording is interpreted by the same planner. Without product dimensions,
Astra sizes the geometry from the visible form factor and common knowledge.
No separate scale record is returned or validated.
The source footprint stays fixed; surrounding furniture is sized to it.
This also applies in histogram mode (§9), without an extra model call.
It is not a calibrated camera reconstruction or a product-fidelity guarantee.

`--grade` saves a separate whole-image grade to the sole generation reference. It does **not** enable full-catalog nearest-tone target selection. The latter is provided by `reference_statistics`, `nearest_reference`, and `grade_row(..., catalog=..., reference_stats=...)`; see the archived `regrade_nearest_references.py` for the actual experiment.

## 8. Safety and interpretation

- Do not run `caption`, `run`, or the archived generation drivers without approval.
- Do not republish or overwrite an existing comparison accidentally.
- Do not infer visual acceptance from passing unit tests or successful model responses.
- Do not treat the estimated camera, guide, or mask as a guarantee of generated geometry.
- Full source snapshots and request metadata live in the S3 archive; review them before changing the pipeline.
- Keep generated outputs, restored inputs, and historical experiment records out of Git.

## 9. Reference-anchored full-histogram mode

This mode is explicit; without it the default prominent-blue/scale workflow is used. Fetch the
tagged full catalog and original histogram into ignored local storage:

```bash
mkdir -p .artifacts/reference-blue
aws s3 cp \
  s3://foundry-hp-enterprise-adobe-assets/hp-data-artifacts/hp-3p-gpt25/reference-catalogs/human-tagged-20261028T233122Z/styles.json \
  .artifacts/reference-blue/styles.json --only-show-errors
aws s3 cp \
  s3://foundry-hp-enterprise-adobe-assets/hp-data-artifacts/hp-3p-gpt25/hp-style-exact-full42-20261029T002354Z-d04de1a4-comparison-v1/inputs/full_element_histogram.csv.gz \
  .artifacts/reference-blue/full_element_histogram.csv.gz --only-show-errors
```

The histogram SHA256 is
`24bc14c239b0754ba13881d99a1cddc0eea5d83cfa6c14e36f2ef37049f67099`.
It contains13,623,353 category/HEX pairs across80 categories;78 named elements
remain after excluding unassigned/generic regions. The catalog contains573
entries /571 distinct images, with existing user-provided human/no-human tags.
Do not substitute the no-human-only subset if prompts may request people.

> [!CAUTION]
> The following command makes paid calls. Run only after explicit approval.

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m hp3p.cli run \
  --run-id NEW_APPROVED_REFERENCE_BLUE_RUN \
  --catalog .artifacts/reference-blue/styles.json \
  --blue-histogram .artifacts/reference-blue/full_element_histogram.csv.gz \
  --refs 1 --size 2368x1776 --workers 2 --grade
```

The histogram identity is part of the cache key, but blue is text-only: Astra
receives no histogram inventory and code substitutes no HEX codes. Old captions
are automatically omitted.
`selection_request/response/result.json`, `geometry_request/response.json`,
`geometry_text.txt`, `planning_request/response.json`,
`derived_rewrite.json` and `image_request.json` retain
provenance without credentials. Raw output and grading remain separate.

This mode uses `unified-blue-v21-text-blue-twin-camera-guide-only.1`.
Changed original requests, catalog or histogram identities require a fresh run
ID; earlier v5-v20 results cannot be reused for this policy.
The archived all42 evaluation predates physical-scale integration and is not
visual validation of the combined mode. It
held23 already-selected references fixed and freshly selected19 others. The CLI
normally selects afresh per case; consult the archived exact requests/helpers
for historical input replay, not an expectation of pixel-identical regeneration.
