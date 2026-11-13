# Tooling

Offline developer utilities for the PPTX Semantics pipeline.

---

## `batch_pptx_semantics.py`

Batch-processes a folder of PPTX files through the semantics pipeline and
produces one of three output types. Run from the repo root with the dev
environment active (`./m`).

```bash
python models/colligo/models/generative_presentations_kg_inferrer/tooling/batch_pptx_semantics.py <folder> [options]
```

### Processing modes (`--mode`)


| Mode                 | Description                                                                                                                       |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `server` *(default)* | Uploads each file to a running Colligo instance, calls `POST /v2/byot/pptx-semantics`, polls for the result.                      |
| `local`              | Runs `PPTXPipeline` fully in-process. ONNX classifiers are auto-loaded from `checkpoints/` (see below). No running server needed. |


### Output modes (`--output`)


| Output                 | Mode                | Token      | Results dir  | Description                                                                                                                  |
| ---------------------- | ------------------- | ---------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| `template` *(default)* | `server` or `local` | required   | optional     | Full pipeline → Express → GDR → CFE `createGenPresoTemplate`. Prints a Project X template URL per file.                      |
| `express-annotation`   | `server` or `local` | required   | optional     | Full pipeline → Express → GDR, stops before CFE. Writes `result.json` with `{document_id, annotated_slides}` per file.       |
| `pptx-annotation`      | `local` only        | not needed | **required** | ML annotation + slide selection only. No Express/network calls. Writes a self-contained interactive HTML inspector per file. |


### Examples

All commands are run from the **repo root**.  Input PPTX files live in
`dev-tests*/` folders (git-ignored); results are written to the git-ignored
`results/` directory under the package root.

```bash
# ── server mode ──────────────────────────────────────────────────────────

# Default: full pipeline → Project X template URL (stage)
python models/colligo/models/generative_presentations_kg_inferrer/tooling/batch_pptx_semantics.py \
    models/colligo/models/generative_presentations_kg_inferrer/dev-tests-regular \
    --mode server --token "$TOKEN"

# Annotation JSON only, no CFE call
python models/colligo/models/generative_presentations_kg_inferrer/tooling/batch_pptx_semantics.py \
    models/colligo/models/generative_presentations_kg_inferrer/dev-tests-regular \
    --mode server --token "$TOKEN" --output express-annotation \
    --results-dir models/colligo/models/generative_presentations_kg_inferrer/results

# Point at a local Colligo dev server
python models/colligo/models/generative_presentations_kg_inferrer/tooling/batch_pptx_semantics.py \
    models/colligo/models/generative_presentations_kg_inferrer/dev-tests-regular \
    --mode server --token "$TOKEN" \
    --base-url http://localhost:8000

# Use production endpoints
python models/colligo/models/generative_presentations_kg_inferrer/tooling/batch_pptx_semantics.py \
    models/colligo/models/generative_presentations_kg_inferrer/dev-tests-regular \
    --mode server --token "$TOKEN" --prod

# ── local mode ───────────────────────────────────────────────────────────

# Full pipeline in-process → template URL (stage)
python models/colligo/models/generative_presentations_kg_inferrer/tooling/batch_pptx_semantics.py \
    models/colligo/models/generative_presentations_kg_inferrer/dev-tests-regular \
    --mode local --token "$TOKEN"

# Annotation JSON only
python models/colligo/models/generative_presentations_kg_inferrer/tooling/batch_pptx_semantics.py \
    models/colligo/models/generative_presentations_kg_inferrer/dev-tests-regular \
    --mode local --token "$TOKEN" --output express-annotation \
    --results-dir models/colligo/models/generative_presentations_kg_inferrer/results

# Interactive HTML inspector — no token, no network calls
python models/colligo/models/generative_presentations_kg_inferrer/tooling/batch_pptx_semantics.py \
    models/colligo/models/generative_presentations_kg_inferrer/dev-tests-regular \
    --mode local --output pptx-annotation \
    --results-dir models/colligo/models/generative_presentations_kg_inferrer/results \
    --parallelism 1

# Override the checkpoints directory (e.g. a custom training run)
python models/colligo/models/generative_presentations_kg_inferrer/tooling/batch_pptx_semantics.py \
    models/colligo/models/generative_presentations_kg_inferrer/dev-tests-regular \
    --mode local --output pptx-annotation \
    --results-dir models/colligo/models/generative_presentations_kg_inferrer/results \
    --checkpoints-dir models/colligo/models/generative_presentations_kg_inferrer/checkpoints
```

### Checkpoint auto-loading (`--mode local`)

When running in local mode the script automatically loads the slide and
element ONNX classifiers from the `checkpoints/` directory co-located with
this package. It picks the **alphabetically last** file matching each prefix:


| Classifier       | File pattern               |
| ---------------- | -------------------------- |
| Slide category   | `slide-classifier*.onnx`   |
| Element category | `element-classifier*.onnx` |


Date-stamped files (e.g. `slide-classifier-20260315.onnx`) therefore resolve
to the newest one automatically. Use `--checkpoints-dir` to point at a
different directory.

The training notebooks that produce these files live in
`tooling/training/`.

---

## Training And Deploy Pipeline

Run all commands from the repo root:

```bash
cd /Users/milie/dev/colligo
```

### 1. Search the best slide-classifier config

```bash
python models/colligo/models/generative_presentations_kg_inferrer/tooling/training/search_best_config.py \
    --classifier slide \
    --optuna-trials <SLIDE_TRIALS> \
    --skip-final-report-details
```

Writes:
- config Python module to `models/colligo/models/generative_presentations_kg_inferrer/pptx_semantics/ml_features/slide_model_config.py`
- verbose log to `models/colligo/models/generative_presentations_kg_inferrer/tooling/training/reports/`

### 2. Search the best element-classifier config

```bash
python models/colligo/models/generative_presentations_kg_inferrer/tooling/training/search_best_config.py \
    --classifier element \
    --slide-config models/colligo/models/generative_presentations_kg_inferrer/pptx_semantics/ml_features/slide_model_config.py \
    --optuna-trials <ELEMENT_TRIALS> \
    --skip-final-report-details
```

Writes:
- config Python module to `models/colligo/models/generative_presentations_kg_inferrer/pptx_semantics/ml_features/element_model_config.py`
- verbose log to `models/colligo/models/generative_presentations_kg_inferrer/tooling/training/reports/`

### 3. Train the slide ONNX from the saved config

```bash
python models/colligo/models/generative_presentations_kg_inferrer/tooling/training/slide_classification.py \
    --config models/colligo/models/generative_presentations_kg_inferrer/pptx_semantics/ml_features/slide_model_config.py
```

Writes:
- `models/colligo/models/generative_presentations_kg_inferrer/checkpoints/slide-classifier-<DATE>-vN.onnx`

### 4. Train the element ONNX from the saved config

```bash
python models/colligo/models/generative_presentations_kg_inferrer/tooling/training/element_classification.py \
    --config models/colligo/models/generative_presentations_kg_inferrer/pptx_semantics/ml_features/element_model_config.py
```

Writes:
- `models/colligo/models/generative_presentations_kg_inferrer/checkpoints/element-classifier-<DATE>-vN.onnx`

### 5. Inspect the generated checkpoints

```bash
ls -lt models/colligo/models/generative_presentations_kg_inferrer/checkpoints/*.onnx | head -20
```

### 6. Run the pipeline locally

Interactive HTML inspector:

```bash
python models/colligo/models/generative_presentations_kg_inferrer/tooling/batch_pptx_semantics.py \
    <INPUT_PPTX_DIR> \
    --mode local \
    --output pptx-annotation \
    --results-dir <RESULTS_DIR> \
    --checkpoints-dir models/colligo/models/generative_presentations_kg_inferrer/checkpoints \
    --parallelism 1 \
    -v
```

Express annotation output using local ONNX checkpoints:

```bash
python models/colligo/models/generative_presentations_kg_inferrer/tooling/batch_pptx_semantics.py \
    <INPUT_PPTX_DIR> \
    --mode local \
    --output express-annotation \
    --token "$TOKEN" \
    --results-dir <RESULTS_DIR> \
    --checkpoints-dir models/colligo/models/generative_presentations_kg_inferrer/checkpoints \
    --parallelism 1 \
    -v
```

### 7. Upload the trained ONNX checkpoints to S3

```bash
./m deps.upload_artifact \
    models/colligo/models/generative_presentations_kg_inferrer/checkpoints/slide-classifier-<DATE>-vN.onnx \
    byot_pptx_semantics

./m deps.upload_artifact \
    models/colligo/models/generative_presentations_kg_inferrer/checkpoints/element-classifier-<DATE>-vN.onnx \
    byot_pptx_semantics
```

Keep the returned:
- `key`
- `version_id`
- `sha256`

### 8. Update deploy metadata

Update the ONNX artifact sources in:
- `models/colligo/models/generative_presentations_kg_inferrer/deploy/types.py`

The deployed code must contain the matching config files in:
- `models/colligo/models/generative_presentations_kg_inferrer/pptx_semantics/ml_features/`

### 9. Deploy and verify

Deploy the same code commit that contains:
- the updated ONNX S3 metadata
- the matching Python config files in `pptx_semantics/ml_features/`

Then run an end-to-end verification against the deployed worker.

### Slide rendition in the HTML inspector

`pptx-annotation` embeds a rendered JPEG of each slide behind the element
overlays. This requires two optional tools:

**1. LibreOffice** (PPTX → PDF)

```bash
brew install --cask libreoffice        # macOS
```

**2. A PDF rasteriser** (PDF → JPEG) — pick one:

```bash
pip install pymupdf                    # recommended (self-contained)

# or:
pip install pdf2image pillow
brew install poppler                   # macOS
```

Without LibreOffice the inspector still works; slide backgrounds are white.

### Other options


| Flag                | Default | Description                                                                     |
| ------------------- | ------- | ------------------------------------------------------------------------------- |
| `--parallelism N`   | `8`     | Maximum concurrent files.                                                       |
| `--results-dir DIR` | —       | Write `result.json` / `inspector.html` per file + `manifest.json`.              |
| `--prod`            | stage   | Use production service endpoints.                                               |
| `--cfe-delay N`     | `5`     | Seconds to wait for Express to settle before calling CFE (`--output template`). |
| `--json`            | off     | Print full JSON to stdout per file (`express-annotation`).                      |
| `-v` / `--verbose`  | off     | Enable DEBUG logging to stderr.                                                 |


---

## `generate_pptx_extractor_diagram.py`

Generates a Graphviz dependency diagram of all `ML_`-prefixed properties
registered in `ppt/default_extractors.py`. Useful for understanding which
features feed into the slide and element classifiers.

```bash
python models/colligo/models/generative_presentations_kg_inferrer/tooling/generate_pptx_extractor_diagram.py [options]
```

Output is written to `docs/` next to this package. The script always writes
a `.dot` file. If the `graphviz` Python package is installed it also renders
directly to PNG or SVG and removes the intermediate `.dot` file.

### Examples

```bash
# Default: render to docs/pptx_ml_feature_dependencies.png
python models/colligo/models/generative_presentations_kg_inferrer/tooling/generate_pptx_extractor_diagram.py

# SVG output
python models/colligo/models/generative_presentations_kg_inferrer/tooling/generate_pptx_extractor_diagram.py \
    --format svg

# Custom output path (extension added automatically)
python models/colligo/models/generative_presentations_kg_inferrer/tooling/generate_pptx_extractor_diagram.py \
    --output /tmp/my_diagram --format svg
```

### Without the `graphviz` Python package

If `graphviz` is not installed the script writes the `.dot` file and prints
the manual rendering command:

```bash
# Install graphviz Python bindings and the system renderer
pip install graphviz
brew install graphviz        # macOS

# Or render the .dot file manually
dot -Tpng models/colligo/models/generative_presentations_kg_inferrer/docs/pptx_ml_feature_dependencies.dot \
    -o models/colligo/models/generative_presentations_kg_inferrer/docs/pptx_ml_feature_dependencies.png
```

### Reading the diagram

The diagram has four clusters:


| Cluster              | Colour | Contents                                                                          |
| -------------------- | ------ | --------------------------------------------------------------------------------- |
| **Deck features**    | grey   | Deck-level `ML_DECK_`* properties (font ranks, element percentiles).              |
| **Slide features**   | yellow | All slide-level `ML_`* properties fed to the slide classifier.                    |
| **Element features** | blue   | All element-level `ML_`* properties fed to the element classifier.                |
| **Legacy (non-ML)**  | dashed | Non-`ML_` properties that some ML extractors depend on (shown with dashed edges). |


Edges point from dependency → consumer (i.e. follow the arrow to see what
uses a given property). The classification and category nodes show transitive
dependencies through the featurizer, so every feature that feeds the trained
model appears as an upstream node.

### Options


| Flag              | Default                        | Description                                                                  |
| ----------------- | ------------------------------ | ---------------------------------------------------------------------------- |
| `-o` / `--output` | `pptx_ml_feature_dependencies` | Output base path (no extension). Relative paths are resolved inside `docs/`. |
| `-f` / `--format` | `png`                          | Render format: `png` or `svg`.                                               |
