# CM5 Components — Foundation Exploration Lineage

CM5 is the Qwen3-VL-based analyze flow for Custom Model preprocessing.
Each CM5 component was ported from the ML team's **foundation_exploration** captioning pipeline at `contrib/Mori/collections/foundation_exploration/scripts/cm/captioning/`.

This file documents the lineage so that coding agents can understand which ML-side implementation each services-side component derives from, what was changed during the port, and what constraints govern prompt evolution.

---

## Reference Architecture

### ML Side (foundation_exploration)

Config-driven sequential pipeline: **Loader → Captioner → Formatter → Writer**.

Key files:
- `captioning_pipeline.py` — Orchestrator; builds requests from YAML config
- `blocks/captioner.py` — Model-agnostic captioning via `CaptionerProtocol`; dispatches request types (`media_type`, `superclass`, `background_consistency`, `backing_shape_consistency`, `caption_scap`, `classify`)
- `workers/qwen_remote.py` — `RemoteQwenVLRunner`: HTTP-based Qwen3-VL runner; contains the original prompt implementations for media type, superclass terms, background consistency, and backing shape consistency
- `workers/qwen_local_enhanced.py` — `EnhancedQwenVLRunner`: local vLLM runner with guided JSON decoding for SCAP captions
- `configs/scap_v2_system_prompts.py` — `SystemPrompts` class with SCAP v2 system prompts, Pydantic output schemas (`SubjectOutputSchema`, `StyleOutputSchema`, `IconographyOutputSchema`), SCAP XML formatting utilities (`format_single_scap`, `normalize_scap_output`)

### Services Side (CM5)

Async component pipeline orchestrated by `TaskTracker` (see parent `v3/AGENTS.md`).

Key files:
- `media_type_detection.py` — `MediaTypeDetectionComponent` (not registered in CM5 pipeline; kept for reference)
- `background_consistency.py` — `BackgroundConsistencyComponent`
- `backing_shape_consistency.py` — `BackingShapeConsistencyComponent`
- `class_descriptor_generation.py` — `ClassDescriptorGenerationComponent`
- `caption_generation.py` — `CaptionGenerationComponent`
- `caption_validation.py` — `CaptionValidationComponent`
- `aggregate_library_changes.py` — `AggregateLibraryChangesComponent`

Shared prompt constants and the `SystemPrompts` class live in:
- `clio_tyom/utils/qwen3_prompting_utils.py`

VLM abstraction:
- `v3/resources/qwen3_resource.py` — `Qwen3Resource.generate()` wraps the hosted vLLM endpoint (replaces `RemoteQwenVLRunner._make_request()` and image-to-base64 conversion)

---

## Component Mapping

### 1. Media Type Detection (not registered in CM5 pipeline)

The `MediaTypeDetectionComponent` exists in `media_type_detection.py` but is **not registered** in the CM5 pipeline. Its output (`MediaTypeDetectionOutput`) was never consumed by any downstream CM5 component. In the CM4 pipeline, it was used to prepend the media type to class descriptors, but the CM5 `ClassDescriptorGenerationComponent` does not use it.

The component file is kept for reference but is not wired into the pipeline.

---

### 2. Background Consistency

| | ML Side | Services Side |
|---|---|---|
| **File** | `workers/qwen_remote.py` `RemoteQwenVLRunner.check_background_consistency()` | `background_consistency.py` `BackgroundConsistencyComponent` |
| **Prompt constants** | Inline in method (two separate prompts) | `qwen3_prompting_utils.BACKGROUND_CONSISTENCY_PROMPT` |
| **System prompt** | `"You are an expert image analysis agent."` | `BACKGROUND_CONSISTENCY_SYSTEM_PROMPT` — identical |
| **Sample size** | Configurable via pipeline YAML (default 4) | `BACKGROUND_CONSISTENCY_SAMPLE_SIZE = 4` |
| **Image resize** | 1024 | `analysis_max_resolution = 1024` (via `TrainingImageV3.pil_image()`) |

**Key structural difference — two-step vs single-step:**

The ML implementation uses a **two-step** process:
1. **Step 1 (per-image):** Sends each image individually with a prompt asking to describe the background. Used for logging and context. `max_tokens=150`.
2. **Step 2 (multi-image):** Sends all images at once to assess background consistency. `max_tokens=200`.

The services side **only implements Step 2** — the consistency assessment prompt sent with all images at once. Step 1 was omitted because it served a diagnostic/logging purpose in the ML pipeline and its output was not consumed by subsequent stages.

The Step 2 prompt text (`BACKGROUND_CONSISTENCY_PROMPT`) is a verbatim copy of the ML side's consistency assessment prompt.

**Other differences:**
- Services side runs for all training modes (no mode gate).
- Services side adds session storage caching and `validation_assert` for minimum image count.

---

### 3. Backing Shape Consistency

| | ML Side | Services Side |
|---|---|---|
| **File** | `workers/qwen_remote.py` `RemoteQwenVLRunner.check_backing_shape_consistency()` | `backing_shape_consistency.py` `BackingShapeConsistencyComponent` |
| **Prompt constants** | Inline in method (two separate prompts) | `qwen3_prompting_utils.BACKING_SHAPE_CONSISTENCY_PROMPT` |
| **System prompt** | `"You are an expert icon design analysis agent."` | `BACKING_SHAPE_CONSISTENCY_SYSTEM_PROMPT` — identical |
| **Sample size** | Configurable via pipeline YAML (default 4) | `BACKING_SHAPE_CONSISTENCY_SAMPLE_SIZE = 4` |
| **Image resize** | 1024 | `analysis_max_resolution = 1024` (via `TrainingImageV3.pil_image()`) |

**Key structural difference — same as background consistency:**

The ML implementation uses a **two-step** process:
1. **Step 1 (per-icon):** Describes each icon's backing shape individually. `max_tokens=100`.
2. **Step 2 (multi-image):** Sends all images to assess backing shape consistency. `max_tokens=150`.

The services side **only implements Step 2**. The Step 2 prompt text is a verbatim copy.

**Other differences:**
- Services side gates on `TYOMTrainingMode.ICONOGRAPHY` — returns empty output for non-iconography modes. The ML side relied on the pipeline config (YAML) to decide whether to include backing shape in the request list.
- Services side adds session storage caching.

---

### 4. Class Descriptor Generation (Superclass Terms)

| | ML Side | Services Side |
|---|---|---|
| **File** | `workers/qwen_remote.py` `RemoteQwenVLRunner.get_superclass_terms()` | `class_descriptor_generation.py` `ClassDescriptorGenerationComponent` |
| **Prompt constants** | Inline in method (long prompt with focus guidance blocks) | `qwen3_prompting_utils.SuperclassPrompts` class |
| **System prompt** | `"You are an expert image captioning agent."` | `SuperclassPrompts.SYSTEM_PROMPT` — identical |
| **Sample size** | Configurable (default 4) | `SuperclassPrompts.TRAINING_SET_SIZE = 4` |
| **Terms range** | `min_terms=10, max_terms=15` | `SuperclassPrompts.MIN_TERM=10, MAX_TERM=15` |
| **Image resize** | 1024 | `analysis_max_resolution = 1024` (via `TrainingImageV3.pil_image()`) |

**Prompt structure mapping:**

The ML side builds the prompt inline in `get_superclass_terms()` as: header + focus guidance (varies by type/sub-type) + no-negation rules + verification check + output format + dimensionality suffix.

The services side refactors this into `SuperclassPrompts`:
- `SuperclassPrompts.PROMPT` — template with `{num_images}`, `{focus_guidance}`, `{min_terms}`, `{max_terms}` placeholders; contains the header, no-negation rules, verification check, and output format
- `SuperclassPrompts.SUBJECT_PHOTOREALISTIC_PROMPT` — focus guidance block (verbatim from ML)
- `SuperclassPrompts.SUBJECT_ILLUSTRATION_PROMPT` — focus guidance block (verbatim from ML)
- `SuperclassPrompts.STYLE_PHOTOREALISTIC_PROMPT` — focus guidance block (verbatim from ML)
- `SuperclassPrompts.STYLE_ILLUSTRATION_PROMPT` — focus guidance block (verbatim from ML)
- `SuperclassPrompts.ICON_PROMPT` — focus guidance block (verbatim from ML)
- `SuperclassPrompts.SUBJECT_PHOTOREALISTIC_SUFFIX` — no dimensionality required (matches ML)
- `SuperclassPrompts.SUFFIX_PROMPT` — dimensionality required as first term (matches ML)

**Type system mapping:**

| ML Side (strings) | Services Side (enums) |
|---|---|
| `dataset_type="Icon"` | `TYOMTrainingMode.ICONOGRAPHY` |
| `dataset_type="Subject"` | `TYOMTrainingMode.SUBJECT` |
| `dataset_type="Style"` | `TYOMTrainingMode.STYLE` |
| `dataset_sub_type="Photorealistic"` | `ContentType.photo` |
| `dataset_sub_type="Illustration"` | `ContentType.illustration` |

**Other differences:**
- Services side post-processes: lowercases, splits by comma, deduplicates, and sorts.
- Services side requires `ContentTypeDetectionOutput` to be present (asserted).
- Services side adds session storage caching.

---

### 5. SCAP Caption Generation

| | ML Side | Services Side |
|---|---|---|
| **Files** | `configs/scap_v2_system_prompts.py` `SystemPrompts` class + `blocks/captioner.py` `_caption_with_scap_prompt()` + `workers/qwen_local_enhanced.py` for guided decoding | `caption_generation.py` `CaptionGenerationComponent` |
| **System prompts** | `SystemPrompts.get_subject_prompt(sub_type)`, `get_style_prompt(sub_type)`, `get_iconography_prompt()` | `qwen3_prompting_utils.SystemPrompts` — identical methods |
| **User prompt** | `"Please analyze this image and provide a structured caption in JSON format."` | `SCAP_CAPTION_USER_PROMPT` — identical |
| **Image resize** | 1024 | `analysis_max_resolution = 1024` (via `TrainingImageV3.pil_image()`) |

**System prompt methods are identical** — the `SystemPrompts` class in `qwen3_prompting_utils.py` is a direct copy of `configs/scap_v2_system_prompts.py.SystemPrompts`, with one adaptation: the `sub_type` parameter type changed from `str` (e.g., `"Photorealistic"`) to `ContentType` enum (e.g., `ContentType.photo`).

**Schema / guided decoding:**

The ML side defines three Pydantic schemas with optional fields for each mode:
- `SubjectOutputSchema` (camera is optional, art_style is optional)
- `StyleOutputSchema` (camera is optional for photo style)
- `IconographyOutputSchema` (iconography-specific fields like shape, stroke weights)

The services side defines **five** separate Pydantic models (no optional fields, one per variant):
- `SubjectPhotoSCAPCaption` — lighting, camera, background, composition
- `SubjectIllustrationSCAPCaption` — background, composition, art_style, color_palette
- `StylePhotoSCAPCaption` — lighting, camera, background, composition
- `StyleIllustrationSCAPCaption` — background, composition, art_style, color_palette
- `IconographySCAPCaption` — shape, stroke weights, backing_shape, color_palette, background, composition

All inherit from `SCAPCaption` (scene, type, entities, details).

**Iconography background hardcode:** Both sides set `background = "plain white background"` for iconography mode.

**Other differences:**
- Services side uses `vlm.generate(..., schema=...)` for guided JSON decoding via vLLM's `guided_decoding` parameter.
- Services side processes images in parallel via `asyncio.gather`.
- Services side skips images previously flagged unsafe (`previous_caption_error == image_not_safe`). Safety gating for newly-unsafe images is handled at aggregation time — captions are generated speculatively and discarded if the image fails safety validation.
- Services side has session storage caching and best-effort partial result saving.

---

### 6. Caption Validation

| | ML Side | Services Side |
|---|---|---|
| **File** | `blocks/formatter.py` `SCAPv2ValidatedFormatter` + `configs/scap_v2_system_prompts.py` `normalize_scap_output()` | `caption_validation.py` `CaptionValidationComponent` |

**Different validation approach:** The ML side uses **Pydantic schema validation** (`normalize_scap_output()` → Pydantic model validation → `format_single_scap()` for XML output). The services side uses **PromptyAnalyzer** — an external prompt analysis service that validates caption safety and quality.

The services side also handles `$concept` token substitution: replaces `CONCEPT_ID_PLACEHOLDER` with `CME_CONCEPT_TOKEN`.

Caption validation is **not a direct port** from foundation_exploration. It is services-specific functionality that was developed independently.

---

### 7. Aggregate Library Changes

No ML-side equivalent. This component is services-specific: it collects outputs from all other CM5 components and merges them into `CMELibraryMetadata` (library-level), `CMEImageMetadata` (per-image), and UX response data.

---

### 8. SCAP XML Formatting (ML-only, not ported)

The ML side has `format_single_scap()` and `normalize_scap_output()` in `configs/scap_v2_system_prompts.py`. These produce XML-like SCAP v2 strings (e.g., `<scene> ... <type> ... <background> ...`). This formatting was **not ported** to the services side — the services side stores SCAP captions as structured JSON via the typed Pydantic models.

The ML side's `normalize_scap_output()` handles edge cases from unguided decoding (entities as dicts, camera as strings, etc.). The services side avoids these issues by using guided JSON decoding with explicit schemas.

---

## Dataset Type Taxonomy

Both sides use the same five-way taxonomy. The ML side uses string pairs; the services side uses enum pairs.

| ML Side | Services Side | Captioning Mode | Superclass Focus |
|---|---|---|---|
| `Icon` / `None` | `ICONOGRAPHY` / any | `get_iconography_prompt()` | Icon system design characteristics |
| `Subject` / `Photorealistic` | `SUBJECT` / `photo` | `get_subject_prompt(photo)` | Persistent physical traits (no dimensionality) |
| `Subject` / `Illustration` | `SUBJECT` / `illustration` | `get_subject_prompt(illustration)` | Persistent physical traits (with dimensionality) |
| `Style` / `Photorealistic` | `STYLE` / `photo` | `get_style_prompt(photo)` | Photographic style characteristics |
| `Style` / `Illustration` | `STYLE` / `illustration` | `get_style_prompt(illustration)` | Artistic style characteristics |

---

## Prompt Evolution Rules

When modifying prompts in CM5 components:

1. **Prompts live in `qwen3_prompting_utils.py`**, not in the component files. Components import and assemble them.
2. **The ML team's foundation_exploration pipeline is the design reference.** Prompt changes should generally be validated in the ML pipeline first, then ported to the services side.
3. **The no-negation rule is critical** — both superclass prompts and SCAP system prompts enforce "never use negations" in model outputs. Maintain this rule in any new prompts.
4. **Iconography background is always hardcoded** to `"plain white background"` in the `parse_scap_caption` method. This is intentional behavior inherited from the ML pipeline.
5. **Guided decoding schemas must match prompts** — when adding SCAP output fields, update both the `SystemPrompts.get_*_prompt()` methods and the corresponding Pydantic models in `types/scap_caption_generation.py`.

---

## VLM Interface Differences

| Concern | ML Side (`RemoteQwenVLRunner`) | Services Side (`Qwen3Resource`) |
|---|---|---|
| Transport | Direct HTTP (`httpx`) to vLLM endpoint | `BaseExecutor` → hosted vLLM via `QwenVLLM.call()` |
| Image encoding | `_convert_image_to_png()` + base64 | Same functions (copied) |
| Image resize | `PIL.thumbnail((size, size))` | `TrainingImageV3.pil_image()` via `scale_down_image(analysis_max_resolution)` — applied once at image load |
| Retry | Manual exponential backoff (inline) | `tenacity` decorator: 3 attempts, exponential wait 2-5s |
| Guided decoding | Local vLLM only (`outlines` JSON schema) | `VLLMServeGuidedDecodingParams(json_schema=schema)` |
| Batch processing | Sequential per-image | `asyncio.gather` for parallel per-image |
| Auth | IMS token in headers | Handled by `BaseExecutor` infrastructure |

---

## Session Storage Caching

All CM5 components cache their outputs in session storage via `get_tyom_metadata()` / `set_tyom_metadata()`. Cache keys:

| Component | Cache Key | Value Type |
|---|---|---|
| Background Consistency | `TYOM_BACKGROUND_CONSISTENCY_KEY` | `str` |
| Backing Shape Consistency | `TYOM_BACKING_SHAPE_KEY` | `str` |
| Class Descriptor Generation | `TYOM_CLASS_DESCRIPTORS_KEY` | `list[str]` |
| Caption Generation | `TYOM_CAPTION_KEY` | `dict[str, str]` |

This caching pattern does not exist in the ML side. It was added to avoid redundant VLM calls during retries or re-analysis of the same library.
