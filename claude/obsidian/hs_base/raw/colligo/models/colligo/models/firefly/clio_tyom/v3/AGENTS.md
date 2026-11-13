# CM4 Preprocessor V3 (Analyze V3) - Architecture Guidelines

## Core Abstractions

### VLMResource
- Abstract base for Vision-Language Models (InternVL, GPT-4o, Dentro, Qwen, etc.)
- Resources are created per-request via `context.get_resource(ResourceType)`
- Each resource defines its own typed API methods
- Resources share `ImageCache` from context for format-based caching
- Supports caching of different preprocessed formats (tensors for local VLMs, base64 strings for API-based VLMs)
- Implements `create()` classmethod for factory pattern

```python
class InternVL25Resource(VLMResource):
    CACHE_FORMAT = "internvl"  # Shared with Dentro for cache reuse
    
    def __init__(self, image_cache: ImageCache):
        super().__init__(self.CACHE_FORMAT, image_cache)
    
    @classmethod
    def create(cls, image_cache: ImageCache, deps: ResourceDependencies) -> Self:
        return cls(image_cache)
    
    async def generate(self, prompt: str, images: list[PILImage], ...) -> tuple[str, ConversationHistory | None]:
        """Typed API - each resource has its own methods."""
        ...
```

### ResourceDependencies
- Container for long-lived external service clients (Dentro, GPT client)
- Created once at pipeline initialization, passed to each request context
- Resources access these via the `create()` factory method

```python
class ResourceDependencies:
    def __init__(
        self,
        dentro_component: Clio4DentroComponent | None = None,
        openai_client: GPTClient | None = None,
    ):
        self.dentro_component = dentro_component
        self.openai_client = openai_client
```

### Components
- Inherit from `CMPreprocessorComponent`
- Single responsibility - one analysis task per component
- Read pipeline inputs directly from context (`training_images`, `library_metadata`, `request`, `config`)
- Read other components' outputs via `context.get_output(OutputType)` for typed access
- Write outputs via `self.set_output(context, output)` with typed output models
- Use `context.get_resource(ResourceType)` to get typed resources
- **Never mutate pipeline inputs or shared objects**

```python
class CategoryDetectionComponent(CMPreprocessorComponent):
    async def process(self, context: CMPreprocessorContext) -> None:
        # Read typed output from another component
        class_descriptors = context.get_output(ClassDescriptorGenerationOutput)
        
        # ... do work ...
        
        # Write typed output
        self.set_output(context, CategoryDetectionOutput(category="object"))
```

### Pipeline
- Orchestrates component execution order
- Uses `context.task_tracker` for parallel execution with dependency management
- Handles parallelization decisions
- Uses `context.clear_cache()` between phases to free memory

## Patterns

### Resource Usage
```python
# ✅ Correct - get typed resource from context
vlm = context.get_resource(InternVL25Resource)
answer, history = await vlm.generate(
    prompt="Describe this image",
    images=pil_images,
    image_hashes=hashes,
)

# ✅ Correct - different resources have different APIs
dentro = context.get_resource(DentroVLMResource)
result = await dentro.check_safety(image, policy="default", image_hash=hash)

gpt4o = context.get_resource(GPT4oResource)
data = await gpt4o.call(content=user_content, system_prompt="...")

# ❌ Wrong - don't instantiate resources directly
resource = InternVL25Resource(image_cache)
```

### Image Caching
- Context owns per-request `ImageCache`
- Pass `image_hashes` to resource methods for caching benefits
- Use `training_image.hash()` (sync, ID-based) for cache keys
- Resources with same `cache_format` share cached data automatically
- Supports both tensor formats (for local VLMs) and string formats (base64 for API-based VLMs)

### Batching
- Use `context.config.batch_config` for batch sizes
- Process in batches to manage memory
- Call `context.clear_cache()` between pipeline phases

### Task Tracking
- Context owns per-request `TaskTracker` for async component execution
- Use `tracker.start(name, coro)` to start a component without blocking
- Use `await tracker.await_all(*names)` to wait for specific dependencies
- Pass no arguments to `await_all()` to wait for all started tasks

```python
tracker = context.task_tracker

# Start independent components in parallel
tracker.start("category_detection", registry.run_component("category_detection", context))
tracker.start("media_type_detection", registry.run_component("media_type_detection", context))
tracker.start("safety_validation", registry.run_component("safety_validation", context))

# Wait only for what's needed before starting dependent work
await tracker.await_all("category_detection", "media_type_detection")
tracker.start("class_descriptor_generation", registry.run_component("class_descriptor_generation", context))

# Wait for all remaining tasks at the end
await tracker.await_all()
```

- `is_started()`, `is_completed()`, `is_failed()` for status checks
- `get_first_failure()` returns the chronologically first failure for re-raising
- Tracker state is per-request (no need to reset between requests)

### Best-Effort Execution

Components follow a best-effort execution model: save partial results before failing so retries only process the delta.

**Principles:**
1. **Save before failing** - Components must call `set_output()` with partial results before re-raising exceptions
2. **Continue on item failure** - Use `asyncio.gather(..., return_exceptions=True)` to let all batch items complete
3. **Aggregation always runs** - Pipeline runs aggregation in `finally` block to collect partial outputs
4. **Storage before re-raise** - Preprocessor saves to storage, then re-raises the first component failure

**Component pattern for batch processing:**
```python
async def process(self, context: CMPreprocessorContext) -> None:
    results: dict[str, str] = {}
    first_exception: BaseException | None = None

    for batch in batches:
        # Use return_exceptions=True to let all items complete
        batch_results = await asyncio.gather(
            *[self._process_item(item) for item in batch],
            return_exceptions=True,
        )
        for result in batch_results:
            if isinstance(result, BaseException):
                if first_exception is None:
                    first_exception = result
            else:
                results[result.key] = result.value

    # Always save partial results before potentially re-raising
    self.set_output(context, MyOutput(results=results))

    if first_exception:
        raise first_exception
```

**Tracking failures:**
- `TaskTracker` captures failed components in `failed` property
- `get_first_failure()` returns `(name, exception)` for the chronologically first failure
- `AggregateLibraryChangesOutput.failed_components` lists all failed component names

### Image Resolution
- Use `pil_image()` to get the image resized to max_resolution (default 2048px)

### Concurrent Image Loading
- Use `asyncio.gather()` for multiple `pil_image()` calls (cached, so zero overhead on repeat calls)
- Use `return_exceptions=True` + check `isinstance(result, BaseException)` for graceful error handling

```python
# ✅ Concurrent
pil_images = list(await asyncio.gather(*[img.pil_image() for img in images]))

# ❌ Sequential
for img in images:
    pil_images.append(await img.pil_image())
```

### State Management

#### Pipeline Inputs (read-only)
Components may read these fields directly from context:
- `context.training_images` - provides `image_id`, `metadata`, `hash()`, `pil_image()`, `_image`
- `context.library_metadata` - library settings (training_mode, class_descriptors, etc.)
- `context.request` - original request parameters
- `context.config` - pipeline configuration
- `context.image_cache` - per-request image cache
- `context.task_tracker` - per-request async task tracker (used by pipeline)
- `context.resource_deps` - long-lived service dependencies

**Never write to these fields** - they are immutable pipeline inputs.

#### Inter-Component Communication
- All derived/computed data flows through `context.results` as typed output models
- Components read via `context.get_output(OutputType)` for typed access
- Components write via `self.set_output(context, output)` with typed models
- Each output type has a `KEY` class variable for storage lookup
- Never mutate shared objects or use utilities that modify passed-in objects

```python
# ✅ Correct - read pipeline inputs
training_mode = context.library_metadata.training_mode
for img in context.training_images:
    metadata = img.metadata  # Original metadata from pipeline input
    pil = await img.pil_image()

# ✅ Correct - read typed output from another component
category_output = context.get_output(CategoryDetectionOutput)
if category_output:
    category = category_output.category  # Type-safe access

# ✅ Correct - write typed output
self.set_output(context, CategoryDetectionOutput(category="object"))

# Note: Metadata aggregation is handled by the pipeline (cm_analyze_v3_impl.py)
# Components write typed outputs, and the pipeline aggregates them into
# CMEImageMetadataUpdate and CMELibraryMetadata before writing to storage.

# ❌ Wrong - writing to pipeline inputs
context.training_images = []  # Never do this
context.library_metadata.training_mode = CMETrainingMode.STYLE  # Never mutate

# ❌ Wrong - mutating internal state of shared objects
training_image._some_field = value
```

## Code Style

### Imports
- **Always use absolute imports** - never use relative imports (e.g., `from ..base import ...`)
- **Never re-export from `__init__.py`** - import directly from the defining module to keep the dependency graph clean
- `__init__.py` files should contain only the copyright header

### Assertions
- Use `validation_assert` for **client errors** (422) - user input validation failures
- Use `runtime_assert` for **server errors** (500) - internal invariant violations / bugs in our code
- **Never** use Python's built-in `assert` statement

```python
from colligo.base.exceptions import runtime_assert, validation_assert

# ✅ Correct - validation_assert for user-facing validation (returns 422)
validation_assert(
    len(images) >= required_count,
    f"Not enough images: got {len(images)}, need {required_count}",
)

# ✅ Correct - runtime_assert for internal invariants (returns 500)
agg_output = ctx.get_output(AggregateLibraryChangesOutput)
runtime_assert(agg_output is not None, "AggregateLibraryChangesOutput must be set by pipeline")

# ✅ Correct - runtime_assert for preconditions that indicate bugs
runtime_assert(len(prompts) == len(images), "prompts and images must have same length")

# ❌ Wrong - don't use plain assert
assert len(images) >= required_count, "Not enough images"
```

**When to use which:**
- `validation_assert`: User-provided data is invalid (bad request, missing fields, invalid format)
- `runtime_assert`: Code invariant violated, something that "should never happen" if code is correct

### Docstrings
- **One-liner maximum** for most methods
- Exception: Complex methods with non-obvious behavior may have brief Args/Returns

```python
# ✅ Good
def hash(self) -> str:
    """Get hash based on image ID (fast, no download needed)."""

# ✅ Acceptable for complex methods
async def generate_captions(self, images, ...) -> list[str]:
    """Generate captions using two-phase VLM conversation.
    
    Phase 1: Initial description
    Phase 2: Final caption with history from Phase 1
    """

# ❌ Avoid verbose docstrings
def hash(self) -> str:
    """Get hash based on image ID.
    
    This method computes an MD5 hash of the image ID...
    (unnecessary detail)
    """
```

### Type Hints
- Use precise types, avoid `Any` except where truly needed
- Use `TYPE_CHECKING` guard only for types not used at runtime
- Import types at runtime if they're used in the implementation

### Naming
- `*Output` classes in `components/types/` for typed component outputs (e.g., `CategoryDetectionOutput`)
- `KEY` class variable on output types for storage lookup
- `CACHE_FORMAT` class constant for resource cache formats
- `_private_method` for internal helpers

## File Structure

```
clio_tyom/
├── cm_preprocessor.py         # Unified pipeline entry point (CMPreprocessorPipeline)
├── cm_analyze_v1_impl.py      # Legacy implementation
├── cm_analyze_v3_impl.py      # V3 implementation (handle_request, load_resources)
v3/
├── context.py             # CMPreprocessorContext, ComponentName
├── registry.py            # ComponentRegistry
├── task_tracker.py        # TaskTracker for async component execution
├── types_v3.py            # Pipeline inputs and config types
├── resources/
│   ├── base.py            # VLMResource ABC
│   ├── image_cache.py     # ImageCache (supports tensors and base64 strings)
│   ├── dependencies.py    # ResourceDependencies
│   ├── internvl25_resource.py
│   ├── internvl3_8b_resource.py
│   ├── dentro_resource.py
│   ├── qwen3_resource.py
│   ├── gpt4o_resource.py
│   └── prompty_analyzer_resource.py
├── components/
│   ├── base.py            # CMPreprocessorComponent ABC
│   ├── types/             # Typed output models for each component
│   │   ├── __init__.py    # Copyright header only (no re-exports)
│   │   ├── category_detection.py
│   │   ├── caption_generation.py
│   │   └── ...            # One file per component
│   └── *.py               # Individual components
├── models/
│   └── training_image_v3.py
└── pipelines/
    └── cm4_analysis_pipeline.py
```

## Testing

### Location
Tests live in `tests/v3/components/` (sibling to `v3/`):
```
tests/v3/
└── components/
    └── test_<component_name>.py
```

### Running Tests
**Always run tests for modified files.** Test files mirror source names with `test_` prefix.

```bash
source .venvs/dev/bin/activate

# Run tests for a specific component
pytest models/colligo/models/firefly/clio_tyom/tests/v3/components/test_<component>.py -v

# Run all v3 tests
pytest models/colligo/models/firefly/clio_tyom/tests/v3/ -v
```

### Mocking Pattern
Components require mocking context, resources, and session storage:

```python
from unittest.mock import AsyncMock, MagicMock, patch

def create_mock_context(training_images: list[MagicMock] | None = None) -> MagicMock:
    context = MagicMock()
    context.results = {}
    context.get_images_subset = MagicMock(return_value=training_images or [])
    context.set_result = MagicMock(side_effect=lambda k, v: context.results.update({k: v}))
    return context

def create_mock_training_image(image_id: str) -> MagicMock:
    img = MagicMock()
    img.image_id = image_id
    img.hash.return_value = f"hash-{image_id}"
    img.pil_image = AsyncMock(return_value=PILImage.new("RGB", (100, 100)))
    return img

# Patch session storage functions
with patch("...component.get_tyom_metadata", new_callable=AsyncMock, return_value=None):
    await component.process(context)
```

### Key Assertions
- Verify `set_output()` was called: check `context.results[OutputType.KEY]`
- Verify VLM calls: `mock_vlm.generate.assert_called_once_with(...)`
- Verify caching: check `set_tyom_metadata` was called with expected values
