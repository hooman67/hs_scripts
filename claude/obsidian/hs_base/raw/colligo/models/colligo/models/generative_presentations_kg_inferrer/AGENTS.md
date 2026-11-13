# Generative Presentations KG Inferrer

Semantic Inference Service for the **Bring Your Own Template** (BYOT) flow in Generate Presentation. It analyses PPTX files to classify slides, annotate element roles (title, subtitle, decoration, numbering, etc.), and detect copy space -- producing information that the downstream Content Fitting Engine can use to synthesise a template with attached knowledge graph.

See `[docs/](docs/)` for detailed documentation: [ARCHITECTURE](docs/PPTX_ARCHITECTURE.md)

## Architecture: PPTX workflow

### Core idea: property graph as a low-tech ML pipeline

The PPTX analysis pipeline is built on a directed graph of **properties** and their **extractor functions**. Each extractor is a function that computes a single feature from the PPTX structure (position, font size, placeholder type, element count, etc.). Higher-level extractors -- slide category, element category -- consume lower-level properties, forming a dependency graph that is lazily evaluated and cached inside `PPTXPresentation`.

Properties are split into two tiers:

- **`BASE_*`** — direct PPTX reads and trivial heuristics (e.g. `BASE_ELEMENT_POSITION`, `BASE_CHILDREN`). These live in `pptx_semantics/base_features/` and never depend on ML predictions.
- **`ML_*`** — richer features intended as inputs to trained classifiers (e.g. `ML_FONT_SIZE_RANK`, `ML_IS_IMAGE`), plus the two top-level predictions: `ML_SLIDE_CATEGORY` and `ML_ELEMENT_CATEGORY`. These live in `pptx_semantics/ml_features/`.

This design intentionally emulates a feature-engineering pipeline. Individual extractors can be replaced by trained ML models once enough labelled data is available. The extractor/property/cache pattern is the architectural backbone of the entire PPTX workflow.

### Pipeline phases

1. **Initialise** `PPTXPresentation` -- parse PPTX, index slide + layout + master shapes.
2. **Select** -- `SlidesSelector` groups slides by `ML_SLIDE_CATEGORY` and picks the best candidate per archetype using penalty scoring.
3. **Pre-warm** -- `PPTXPipeline._ensure_required_features_loaded()` caches all `PREREQUISITE_SLIDE_FEATURES + ML_SLIDE_CATEGORY` for each selected slide, and all `PREREQUISITE_ELEMENT_FEATURES + ML_ELEMENT_CATEGORY` for every shape on those slides, so the compiler operates in strict readonly mode.
4. **Normalise and convert** -- fill empty placeholders, then convert PPTX to PDF to Express to GDR via CPF services.
5. **Compile** -- `AnnotationCompiler.compile()` matches PPTX shape semantics to GDR entities, producing `AnnotatedSlide` output.

## Architecture: PDF workflow

TODO -- document the GPT-based slide classification and annotation pipeline for PDF inputs (`slide_classifier/`, `slide_annotator/`).

## Architecture: Style extraction

GPT-based style parameter extraction used by both PPTX and PDF workflows (`style_extractor/`).

### Schema versioning

Style contracts are versioned via `BYOTStyleContract` (`style_extractor/byot_style_contracts.py`).

| Version | Key | Description |
|---------|-----|-------------|
| **v1** (default) | `prod_style_schema_version=1` | Flat style dict extracted from a single representative content slide per archetype. |
| **v2** (draft) | `draft_style_schema_version=2` | Per-slide style extraction from up to 3 content slides. Output has one top-level key: `contentSlideStyles` — an array with one full `ExtractedStyleValues`-compatible block per observed content slide. Matches hz's `ExtractedMultiContentSlideStyles` type. Enabled via `use_experimental_style_schema=True` on the request. |

### v2 schema: `contentSlideStyles`

The v2 output shape matches hz's `ExtractedMultiContentSlideStyles`:

```json
{
  "contentSlideStyles": [
    { "slideId": "<gdr-uuid>", "styles": { ...ExtractedStyleValues... } }
  ]
}
```

Each `styles` block is a full v1-compatible `ExtractedStyleValues` payload extracted independently for each content slide. All fields are per-slide — there is no deck-wide propagation.

**Per-slide fields:**

| Field | Description |
|-------|-------------|
| `slideId` | GDR page UUID for the content slide. |
| `styles.themeColors.background` | Per-slide dominant background color. |
| `styles.themeColors.backgroundType` | Background classification: `solid`, `gradient`, `composite`, `image`. |
| `styles.contentBacking` | Whether a readability backing overlay is needed. |
| `styles.listStyle` | List decoration style (`decorationKind`: `delimiter` / `background` / `none`). Always present. |
| `styles.tableStyle` | Table decoration. Always present. |
| `styles.sizing.borderThicknessPx` | Table cell border stroke width (0 for non-table). |
| `styles.sizing.segmentThicknessPx` | Timeline connector width (0 for non-timeline). |
| `styles.sizing.markSizePx` | Timeline marker diameter (0 for non-timeline). |
| `styles.sizing.verticalCellDensity` | Table row density 0.0–1.0 (0 for non-table). |

### Offline v2 extraction

```bash
python tooling/batch_pptx_semantics.py /path/to/pptx \
  --mode local --output express-annotation \
  --use-gpt-slide-semantics-pipeline \
  --style-schema-version 2 \
  --token "$TOKEN"
```

## File map

```
pptx_semantics/                     # PPTX workflow (canonical)
  pipeline.py                       #   PPTXPipeline orchestration + PPTXPipelineResponse
  presentation.py                   #   PPTXPresentation: parse, index, cache
  types.py                          #   PPTXPropertyId enum, PPTXProperty model
  extractor.py                      #   PPTXExtractorFn protocol, PPTXExtractorTable
  default_extractors.py             #   Registration of all built-in extractors
  constants.py                      #   Shared XML namespace constants
  annotation_compiler.py            #   PPTX-to-GDR bounding-box matching;
                                    #   PREREQUISITE_SLIDE/ELEMENT_FEATURES declarations
  slides_selector.py                #   Penalty-based best-per-archetype selection
  base_features/                    #   Direct PPTX reads (BASE_* properties)
    element_features.py             #     Position, text, text_style, name, has_text_frame
    slide_features.py               #     Children list
  ml_features/                      #   ML-ready computed features (ML_* properties)
    element_category.py             #     ML_ELEMENT_CATEGORY (placeholder — NotImplementedError)
    slide_category.py               #     ML_SLIDE_CATEGORY   (placeholder — NotImplementedError)
    element_features/               #     Per-element features
      font_features.py              #       Font size, rank, ratio
      paragraph_features.py         #       Paragraph count, bullet, alignment
      position_features.py          #       Normalised position / area
      shape_features.py             #       Rotation, name signals, obstructed area
      structure_features.py         #       PPTX role, type, image, z-order, repeating
      text_features.py              #       Text length, keywords, density
    slide_features/                 #     Per-slide features
      composition_features.py       #       Element counts, data-viz flag
      layout_features.py            #       Layout name keyword flags
      ml_copyspace.py               #       Copy-space detection (ML_COPYSPACE_APPROX_AREA_RATIO)
      position_features.py          #       Slide index, position ratio
      spatial_features.py           #       Text/image area ratios, spread
      text_features.py              #       Biggest font, title length, agenda keyword
    deck_features/                  #     Deck-wide features
      element_percentiles.py        #       ML_DECK_ELEMENT_PERCENTILES
      font_ranks.py                 #       ML_DECK_FONT_RANKS
  utils/
    placeholder_utils.py            #   OXML placeholder-type resolution
utils/                              # CPF clients, geometry helpers, unit conversions
types.py                            # Shared output types (AnnotatedSlide, etc.)
docs/                               # Documentation suite
tooling/
  batch_pptx_semantics.py           # Batch processing script
  generate_pptx_extractor_diagram.py# Property dependency diagram generator
  training/                         # Training pipeline for ML_SLIDE/ELEMENT_CATEGORY
slide_annotator/                    # GPT-based annotator for PDF workflow (WIP)
slide_classifier/                   # GPT-based classifier for PDF workflow (WIP)
style_extractor/                    # GPT-based style extraction for PPTX + PDF (live)
  byot_style_contracts.py           #   Contract registry + BYOTStyleContract class
  byot_style_contracts_v2.py        #   v2 schema params, instructions, validate_v2_extracted_values
  gpt_style_extractor.py            #   GPTStyleExtractor (JSON schema → Pydantic, per-block v2 validation)
  gpt_element_annotator_prompts.py  #   GPT prompts for element annotation
```

## Boundaries (PPTX workflow)

- **NEVER** call `get_property` inside `AnnotationCompiler`; use only `get_cached_property` (readonly after the pre-warm phase). All properties the compiler needs are declared in `PREREQUISITE_SLIDE_FEATURES` and `PREREQUISITE_ELEMENT_FEATURES`.
- **NEVER** bypass the extractor/cache pattern by reading python-pptx shape attributes directly in classification or annotation code. All data flows through `PPTXPresentation`.
- **NEVER** mutate `PPTXPresentation` state after `normalize_placeholders` has been called; the cache is frozen for the annotation compiler.
- **NEVER** add a `BASE_*` property that depends on another `ML_*` property. The `BASE_*` tier must remain a strict subset of direct PPTX reads.

## Key patterns and invariants (PPTX workflow)

- **Entity ID format**: `"slide_N"` for slides, `"shape_N_M"` for slide shapes, `"shape_N_LM"` for layout shapes, `"shape_N_MM"` for master shapes, `"deck"` for deck-level properties.
- **Property prefix convention**: `BASE_` for direct reads, `ML_` for ML-ready features and predictions.
- **Master/layout shapes**: non-placeholder shapes from slide layouts and masters are automatically indexed during initialisation. The `showMasterSp` visibility flags are respected.
- **Cache contract**: `get_property(entity_id, prop)` triggers lazy extraction and caches the result; `get_cached_property(entity_id, prop)` is readonly and raises if the property is missing.
- **Pre-warm contract**: before calling `AnnotationCompiler.compile()`, `_ensure_required_features_loaded()` must have been called for every selected slide and all its shapes.
- **Adding a new property**: (1) add a member to `PPTXPropertyId` in `pptx_semantics/types.py` with the appropriate `BASE_` or `ML_` prefix, (2) write an extractor function matching `PPTXExtractorFn(presentation, entity_id) -> PPTXProperty`, (3) register it in `default_extractors.py`, (4) if the compiler needs it, add it to `PREREQUISITE_SLIDE_FEATURES` or `PREREQUISITE_ELEMENT_FEATURES` in `annotation_compiler.py`.

## Principles

When contributing, follow these rules:

1. **Optimise for change** -- good design makes the system easier to change, not just easier to build.
2. **Don't Repeat Yourself** -- eliminate duplicated logic, data, and knowledge. Comment the "why", never the "how".
3. **Maintain orthogonality** -- unrelated components stay independent; a change in one must not break another.
4. **Design by Contract** -- strictly define what functions expect (preconditions) and guarantee (postconditions).
5. **Crash early** -- terminate immediately on impossible states (`runtime_assert`); never mask errors.
6. **Balance resources** -- the component that allocates must also deallocate.
7. **Decouple ruthlessly** -- no global data; tell objects what to do rather than asking for their state.
8. **Embrace events** -- react to events over rigid linear flows.
9. **Think in transformations** -- model code as clean pipelines transforming inputs into outputs.
10. **Avoid inheritance tax** -- prefer interfaces, delegation, and mixins over deep class hierarchies.
11. **Externalise configuration** -- credentials, env vars, and business rules stay out of source code.
12. **Break temporal coupling** -- identify independent tasks that can safely run concurrently.
13. **Eliminate shared state** -- avoid concurrent mutation; use strict mutual exclusion if unavoidable.
14. **Keep code and docs together** -- if you change logic, update docstrings and docs in the same commit.

## Coding conventions

See the root [AGENTS.md](../../../../../../AGENTS.md) for general Python standards (3.10+, strict type annotations, absolute imports, `runtime_assert`/`validation_assert`, Adobe copyright header, Google-style docstrings).

Package-specific additions:

- PEP 8 file names (lowercase, underscores); CamelCase class names with fully capitalised acronyms (e.g. `PPTXPipeline`).
- Extractor functions are module-level, named `extract_<property_name>`.
- All property data flows through the `PPTXPresentation` cache -- no ad-hoc attribute reads on python-pptx objects outside of extractor functions.
- `BASE_*` extractors must not call `get_property` for any `ML_*` property.

## Commands

```bash
pytest models/colligo/models/generative_presentations_kg_inferrer/   # run tests
./m lint --paths models/colligo/models/generative_presentations_kg_inferrer/  # lint
```

## Status

- `pptx_semantics/` -- canonical PPTX implementation; fully operational except for `ML_SLIDE_CATEGORY` and `ML_ELEMENT_CATEGORY`, which are placeholder stubs that raise `NotImplementedError`. Implement via `pptx_semantics/ml_features/slide_category.py` and `element_category.py`.
- `tooling/training/` -- training pipeline for the above ML classifiers; work in progress.
- `slide_annotator/` and `slide_classifier/` -- GPT-based annotator and classifier for the **PDF workflow**; work in progress, needs review.
- `style_extractor/` -- GPT-based style parameter extraction used by **both PPTX and PDF workflows**; live code, needs review.
