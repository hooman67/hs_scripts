# HCM — Horizontal Concerns Module

In-process phase machine for custom-model inference. Owns BKS authorization (P1), ACP persistence (P4), model core (P5), BKS settlement (P7), and telemetry (P8) through a table-driven orchestrator and port facades — so pipeline classes contain only model-specific logic.

---

## Table of contents

- [Architecture overview](#architecture-overview)
- [hcm_spec.yaml field reference](#hcm_specyaml-field-reference)
  - [generation_model](#generation_model)
  - [generation_model_by_tier](#generation_model_by_tier)
  - [get_k12_info](#get_k12_info)
  - [authorization_policies](#authorization_policies)
  - [units](#units)
  - [metering_payload](#metering_payload)
  - [charges_withheld](#charges_withheld)
  - [acp_persistence](#acp_persistence)
  - [metrics](#metrics)
  - [safety](#safety)
- [Implementing a new pipeline](#implementing-a-new-pipeline)
  - [Step 1 — Add a YAML port spec row](#step-1--add-a-yaml-port-spec-row)
  - [Step 2 — Create the pipeline class](#step-2--create-the-pipeline-class)
  - [Step 3 — Wire the worker](#step-3--wire-the-worker)
  - [Step 4 — Tests](#step-4--tests)
- [Phase reference](#phase-reference)

---

## Architecture overview

```
handle_request_validation          handle_request
        │                                 │
  StashedHcmMixin                  StashedHcmMixin
  hcm_handle_request_validation    hcm_handle_request
        │                                 │
   HCMOrchestrator                  HCMOrchestrator
   validation_profile               inference_profile
   ┌─────────────┐                  ┌──────────────────────┐
   │  P1  BKS    │                  │  P4  ACP persist     │
   │  authorize  │                  │  P5  model core      │
   └─────────────┘                  │  P6  safety out      │
                                    │  P7  BKS settle      │
                                    │  P8  telemetry       │
                                    └──────────────────────┘
```

Key files:

| File | Purpose |
|---|---|
| `hcm_spec.yaml` | Declarative per-SKU BKS + safety + metrics config |
| `hcm_spec_schema.py` | Pydantic schema + YAML loader + P8 runtime drivers |
| `stashed_hcm_mixin.py` | Mixin that pipelines inherit; implements the two-pass stash pattern |
| `orchestrator.py` | Table-driven P0–P8 loop |
| `port_bundle.py` | `HorizontalPorts` — typed bundle of all port instances |
| `port_wiring.py` | `build_hcm_ports` factory |
| `binding.py` | `HCMBinding` (product × modality) + `new_hcm_request_context` |
| `stash.py` | Rhode cross-worker stash (carries P1 state to the inference worker) |
| `bks_p1_authorize.py` | P1 hook pair builder |
| `bks_p7_settle.py` | P7 BKS settlement |
| `profiles.py` | `validation_profile`, `inference_profile`, `model_core_only_profile` |
| `adapters/bks.py` | `ConfigDrivenBksPort` — YAML-backed BKS port |
| `adapters/safety.py` | `ConfigDrivenSafetyPort` — YAML-backed P6 output safety; `model_core_context_from_hcm_context` |
| `adapters/acp_cme.py` | `DefaultAcpCmePort` — image persistence |
| `adapters/telemetry.py` | `LoggingTelemetryPort` + P8 helpers |

---

## hcm_spec.yaml field reference

The file has a single top-level key `port_specs` containing named rows. Each row name (e.g. `cm5_inference`) is the value set as `HCM_PORT_SPEC` on the pipeline class.

```yaml
port_specs:
  <row_name>:
    generation_model: ...
    authorization_policies: ...
    units: ...
    # all other fields are optional
```

---

### generation_model

**Required.** The `GenerationModel` enum member name used as the BKS billing model for P7 metering.

| Type | Example values |
|---|---|
| `string` (enum name) | `CLIO_V5_CM_LORA_DIFFUSION`, `CLIO_V4_CM_DIFFUSION`, `CLIO_V4_CM_LORA_DIFFUSION` |

```yaml
generation_model: CLIO_V5_CM_LORA_DIFFUSION
```

The full list of valid names comes from `colligo.external_services.business_kit.business_kit_service_types.GenerationModel`.

---

### generation_model_by_tier

**Optional.** Overrides `generation_model` at P7 based on a request enum attribute. Use when different product tiers bill under different `GenerationModel` values (e.g. BASIC vs standard).

| Field | Type | Description |
|---|---|---|
| `attribute` | string | Request attribute name to read (must be an enum or string) |
| `mapping` | map of string→string | Enum `.name` → `GenerationModel` name override |

```yaml
generation_model_by_tier:
  attribute: custom_model_tier
  mapping:
    BASIC: CLIO_V5_CM_LORA_DIFFUSION_BASIC
```

If the request attribute is absent or its name is not in `mapping`, `generation_model` is used unchanged.

---

### get_k12_info

**Optional, default `false`.** When `true`, P1 `validate_entitlements` requests the BKS k12 (family-friendly) flag and stores it at `HCMMetadataKey.BKS_USER_IS_K12` on the context. The model core can then apply age-appropriate content guardrails.

```yaml
get_k12_info: true
```

---

### authorization_policies

**Required.** Declares how P1 builds the list of `AuthorizationPolicies` attribute names passed to Business Kit.

#### kind: static

Fixed policy list — same for every request regardless of CM lifecycle state.

| Field | Type | Description |
|---|---|---|
| `kind` | `"static"` | Discriminator |
| `names` | list of strings | `AuthorizationPolicies` attribute names (at least one required) |

```yaml
authorization_policies:
  kind: static
  names:
    - FIREFLY_MANDATORY_CHECKS
    - FIREFLY_CREDITS_METERING_CHECKS
```

#### kind: cm_lifecycle

Policy list selected by custom-model publish state. Published models use the full metering list; unpublished / unknown models use a reduced list (no credit deduction).

| Field | Type | Description |
|---|---|---|
| `kind` | `"cm_lifecycle"` | Discriminator |
| `published` | list of strings | Policies when CM state is `PUBLISHED` |
| `preview` | list of strings | Policies when CM state is not published or unknown |

```yaml
authorization_policies:
  kind: cm_lifecycle
  published:
    - FIREFLY_MANDATORY_CHECKS
    - FIREFLY_CREDITS_METERING_CHECKS
  preview:
    - FIREFLY_MANDATORY_CHECKS
```

Valid `AuthorizationPolicies` attribute names are validated at startup. An unknown name raises `ValueError` on first YAML load.

---

### units

**Required.** How many BKS units to report for this request.

#### kind: request_int

Reads an integer attribute directly from the request object.

| Field | Type | Description |
|---|---|---|
| `kind` | `"request_int"` | Discriminator |
| `attribute` | string | Request attribute name |
| `default_if_absent` | int (≥0, default `1`) | Value when attribute is absent or `None` |

```yaml
units:
  kind: request_int
  attribute: n
  default_if_absent: 1
```

#### kind: len_or_default

Uses the length of a sequence attribute (e.g. `seeds` list).

| Field | Type | Description |
|---|---|---|
| `kind` | `"len_or_default"` | Discriminator |
| `attribute` | string | Request attribute name |
| `default_if_absent` | int (≥0, default `1`) | Value when attribute is `None` |

```yaml
units:
  kind: len_or_default
  attribute: seeds
  default_if_absent: 1
```

---

### metering_payload

**Optional.** Declarative P7 Business Kit metering payload. Omit only for SKUs that do not call Business Kit metering (unusual).

```yaml
metering_payload:
  fields:
    - ...  # one or more field specs
  cm_metadata:           # optional
    base_model_version: "5.0.0"
```

#### metering_payload.fields

Each entry in `fields` is a typed field spec:

##### kind: request_attribute

Reads a single attribute from the request object.

| Field | Type | Description |
|---|---|---|
| `kind` | `"request_attribute"` | Discriminator |
| `key` | string | BKS payload key name |
| `attribute` | string | Request attribute name |
| `default` | any (default `null`) | Value when attribute is absent. Use `[]` for list fields. |

```yaml
- kind: request_attribute
  key: seeds
  attribute: seeds
  default: []
```

##### kind: worker_application_version

Injects the worker's deployed application version string (from `WorkerContext`).

| Field | Type | Description |
|---|---|---|
| `kind` | `"worker_application_version"` | Discriminator |
| `key` | string (default `sourceVersion`) | BKS payload key name |

```yaml
- kind: worker_application_version
  key: sourceVersion
```

##### kind: nested_size_wh_star

Resolves image resolution as `"width*height"` from a nested `.size` object. Prefers the response value; falls back to the request.

| Field | Type | Description |
|---|---|---|
| `kind` | `"nested_size_wh_star"` | Discriminator |
| `key` | string (default `imageResolution`) | BKS payload key name |
| `response_size_attr` | string (default `size`) | Nested size attribute on the response |
| `request_size_attr` | string (default `size`) | Nested size attribute on the request |

```yaml
- kind: nested_size_wh_star
  key: imageResolution
  response_size_attr: size
  request_size_attr: size
```

Use this when size lives in `response.size.width` / `response.size.height`.

##### kind: flat_wh_star

Resolves image resolution as `"width*height"` from flat `width`/`height` attributes. Prefers the response; falls back to the request.

| Field | Type | Description |
|---|---|---|
| `kind` | `"flat_wh_star"` | Discriminator |
| `key` | string (default `imageResolution`) | BKS payload key name |
| `response_width_attr` | string (default `width`) | Width attribute on the response |
| `response_height_attr` | string (default `height`) | Height attribute on the response |
| `request_width_attr` | string (default `width`) | Width attribute on the request |
| `request_height_attr` | string (default `height`) | Height attribute on the request |

```yaml
- kind: flat_wh_star
  key: imageResolution
```

Use this when size lives in `response.width` / `response.height` (flat, not nested).

##### kind: response_or_request_attr

Reads an attribute from the response if available, otherwise from the request.

| Field | Type | Description |
|---|---|---|
| `kind` | `"response_or_request_attr"` | Discriminator |
| `key` | string | BKS payload key name |
| `response_attr` | string | Attribute name on the response object |
| `request_attr` | string | Attribute name on the request object |

```yaml
- kind: response_or_request_attr
  key: contentType
  response_attr: predicted_content_type
  request_attr: content_type
```

#### metering_payload.cm_metadata

Optional block that appends standard CM lifecycle fields (`cm_id`, `cm_status`, `base_model_version`) to the metering payload. CM id and state are read from `HCMMetadataKey` values stashed during P1.

| Field | Type | Description |
|---|---|---|
| `base_model_version` | string | Model version string sent to BKS (e.g. `"5.0.0"`) |

```yaml
cm_metadata:
  base_model_version: "5.0.0"
```

---

### charges_withheld

**Optional.** Declarative `chargesWithheld` records for P7 — used to withhold credits for unpublished / preview custom models.

#### kind: none

No `chargesWithheld` records. Credits are always deducted.

```yaml
charges_withheld:
  kind: none
```

#### kind: cm_preview_unpublished

Withholds credits when the custom model is not published. Can be skipped for specific tiers.

| Field | Type | Description |
|---|---|---|
| `kind` | `"cm_preview_unpublished"` | Discriminator |
| `skip_tier_attribute` | string \| null | Request attribute to check for tier-based skip |
| `skip_tier_values` | list of strings | Tier enum names that bypass withholding (credits always deducted for these tiers) |
| `feature_from` | `"generation_model"` \| `"fixed"` | Where to read the `feature` value for the withheld record |
| `feature` | string \| null | `GenerationModel` name when `feature_from` is `"fixed"` |
| `reason` | string (default `"preview"`) | Reason string in the withheld record |
| `message` | string (required) | Human-readable message in the withheld record |

```yaml
# Withhold for unpublished CMs; BASIC tier is always billed (no withholding)
charges_withheld:
  kind: cm_preview_unpublished
  skip_tier_attribute: custom_model_tier
  skip_tier_values:
    - BASIC
  feature_from: fixed
  feature: CLIO_V5_CM_LORA_DIFFUSION
  reason: preview
  message: "No credit deduction for inference request on CM which is not yet published."

# Withhold for unpublished CMs; feature taken from the resolved generation_model
charges_withheld:
  kind: cm_preview_unpublished
  feature_from: generation_model
  reason: preview
  message: "No credit deduction for inference request on CM which is not yet published."
```

---

### acp_persistence

**Optional.** Controls P4 ACP image persistence behaviour.

#### Inline model_name (no `kind` key)

Persist via `v1/images` when the response has `store_inputs = true`.

| Field | Type | Description |
|---|---|---|
| `model_name` | string | ACP model name passed to the persistence endpoint |

```yaml
acp_persistence:
  model_name: image5_custom
```

#### kind: nop

Skip orchestrator P4 persistence entirely. Use when the endpoint owns persistence independently.

```yaml
acp_persistence:
  kind: nop
```

When `acp_persistence` is absent from the spec row, P4 is also skipped.

---

### metrics

**Optional.** P8 workflow label seeding and completion metrics driver.

#### kind: custom_model_inference

Uses `record_custom_model_inference_metrics` for P8 completion callbacks.

| Field | Type | Description |
|---|---|---|
| `kind` | `"custom_model_inference"` | Discriminator |
| `workflow` | workflow spec | See [workflow specs](#workflow-specs) below |
| `detail_level` | string (default `"full"`) | Passed to `record_custom_model_inference_metrics` |
| `seeds_attr` | string (default `"seeds"`) | Request attribute to read seed list from for metrics |

```yaml
metrics:
  kind: custom_model_inference
  workflow:
    kind: request_predicate
    when_attribute: reference_blobs
    when_present: instruct_edit
    default: text_to_image
  detail_level: full
  seeds_attr: seeds
```

#### kind: image4_inference

Uses `ClioV4Utils.record_metrics` for P8 completion callbacks.

| Field | Type | Description |
|---|---|---|
| `kind` | `"image4_inference"` | Discriminator |
| `workflow` | workflow spec | See [workflow specs](#workflow-specs) below |

```yaml
metrics:
  kind: image4_inference
  workflow:
    kind: ordered_predicates
    predicates:
      - kind: attribute_truthy
        attribute: similarity_reference_image
        workflow: show_similar
    default: text_to_image
```

#### Workflow specs

Workflow specs resolve a string workflow label from the request at P8 startup. The resolved value is stored at `HCMMetadataKey.WORKFLOW`.

##### kind: request_predicate

Returns `when_present` if a request attribute is truthy, otherwise `default`.

```yaml
workflow:
  kind: request_predicate
  when_attribute: reference_blobs
  when_present: instruct_edit
  default: text_to_image
```

##### kind: ordered_predicates

Evaluates a list of rules in order; returns the first match or `default`.

```yaml
workflow:
  kind: ordered_predicates
  predicates:
    - kind: attribute_truthy       # matches when attribute is truthy
      attribute: similarity_reference_image
      workflow: show_similar
    - kind: attribute_equals       # matches when attribute equals value (string or enum name/value)
      attribute: content_class
      value: VECTOR
      workflow: text_to_vector
  default: text_to_image
```

---

### safety

**Optional.** P6 output-safety scan mechanism. Selects the `SafetyPort` implementation for the SKU via `ConfigDrivenSafetyPort`. When absent or `kind: nop`, the orchestrator falls through to `NopSafety` (no scan).

#### kind: nop

Explicit no-op — orchestrator P6 runs but performs no scan.

```yaml
safety:
  kind: nop
```

#### kind: cm5_nsfw_adobeone

P6 output safety using CM5's `NSFWAdobeOneComponent` on the stashed `CM5InferenceContext`. The pipeline's model core must store its context under `FlowModalityKeys.MODEL_CORE_CONTEXT` at P5 for the scanner to read decoded images.

| Field | Type | Description |
|---|---|---|
| `kind` | `"cm5_nsfw_adobeone"` | Discriminator |
| `safety_level_2_tree.default` | string | Dentro level-2 tree name used by default |
| `safety_level_2_tree.by_tier` | map of string→string | Per-tier overrides (request tier enum name → tree name) |

```yaml
safety:
  kind: cm5_nsfw_adobeone
  safety_level_2_tree:
    default: lego_level_2_v7
    by_tier:
      BASIC: cm5_cci_cct_training_safety
```

The tree config is passed to the component via `CM5InferenceContext.debug_data` under the key `hcm.cm5.safety_level_2_tree` — see `adapters/safety.py`.

---

## Implementing a new pipeline

### Step 1 — Add a YAML port spec row

Add a named row to `hcm_spec.yaml`. Choose a snake_case name that identifies the SKU and flow (e.g. `cm6_inference`).

```yaml
port_specs:
  cm6_inference:
    generation_model: CLIO_V6_CM_DIFFUSION        # required
    authorization_policies:
      kind: cm_lifecycle
      published:
        - FIREFLY_MANDATORY_CHECKS
        - FIREFLY_CREDITS_METERING_CHECKS
      preview:
        - FIREFLY_MANDATORY_CHECKS
    units:
      kind: len_or_default
      attribute: seeds
      default_if_absent: 1
    metering_payload:
      fields:
        - kind: request_attribute
          key: seeds
          attribute: seeds
          default: []
        - kind: worker_application_version
          key: sourceVersion
        - kind: flat_wh_star
          key: imageResolution
      cm_metadata:
        base_model_version: "6.0.0"
    charges_withheld:
      kind: cm_preview_unpublished
      feature_from: generation_model
      reason: preview
      message: "No credit deduction for inference on unpublished CM6 model."
    acp_persistence:
      model_name: image6_custom
    metrics:
      kind: custom_model_inference
      workflow:
        kind: request_predicate
        when_attribute: reference_blobs
        when_present: instruct_edit
        default: text_to_image
      detail_level: full
      seeds_attr: seeds
    safety:                           # optional — omit when no P6 scan is needed
      kind: nop
```

The YAML is validated against the Pydantic schema in `hcm_spec_schema.py` at process startup. An invalid row (unknown policy name, unknown `GenerationModel`, missing required field) raises immediately.

---

### Step 2 — Create the pipeline class

Subclass the worker's inference base and `StashedHcmMixin`. Set the two required class attributes and implement the four hook methods.

```python
from colligo.base.types.worker import ColligoPipeline
from colligo.models.firefly.hcm.binding import HCMBinding
from colligo.models.firefly.hcm.context import HCMRequestContext
from colligo.models.firefly.hcm.persistence import validate_store_inputs_prerequisites
from colligo.models.firefly.hcm.phases import Modality, ProductFlow
from colligo.models.firefly.hcm.stashed_hcm_mixin import StashedHcmMixin
from colligo.models.firefly.pipelines.cm6.CM6Pipeline import CM6InferencePipelineBase
from colligo.models.firefly.pipelines.cm6.types import CM6Config
from colligo.models.firefly.pipelines.cm6.types.request_types import CM6Request, CM6Response


class CM6PipelineHcm(
    CM6InferencePipelineBase,
    StashedHcmMixin[CM6Request, CM6Response],
    ColligoPipeline[CM6Config],  # explicit for WorkerLoader config-type introspection
):
    """CM6 inference worker — stashed HCM (P1 on validation, P4/P5/P7/P8 on handle_request)."""

    HCM_BINDING = HCMBinding(product=ProductFlow.INFERENCE, modality=Modality.IMAGE)
    HCM_PORT_SPEC = "cm6_inference"

    async def hcm_run_model_core(self, ctx: HCMRequestContext[CM6Request]) -> CM6Response:
        """P5 — delegate to the pipeline's model-specific request handler."""
        return await self._handle_cm6_request(ctx.request)

    async def hcm_validate_prerequisites(self, request: CM6Request) -> None:
        """Called before P1 on handle_request_validation. Validate ACP store inputs."""
        await validate_store_inputs_prerequisites(request)

    async def handle_request_validation(self, request: CM6Request) -> None:
        """Rhode validation worker entry point — runs HCM P1 (BKS authorize + rate limit)."""
        await self.hcm_handle_request_validation(request)

    async def handle_request(self, request: CM6Request) -> CM6Response:
        """Rhode inference worker entry point — runs HCM P4/P5/P7/P8 via orchestrator."""
        return await self.hcm_handle_request(request)
```

**Class attributes:**

| Attribute | Type | Description |
|---|---|---|
| `HCM_BINDING` | `HCMBinding` | Product flow × modality for this worker |
| `HCM_PORT_SPEC` | `str` | Row name in `hcm_spec.yaml` |
| `HCM_PORT_SPEC_FOR_CONTEXT` | `Callable \| None` | Optional per-request spec selector (multi-spec SKUs, e.g. Image4 diffusion vs LoRA) |

**Hook methods to implement:**

| Method | When called | What to implement |
|---|---|---|
| `hcm_run_model_core(ctx)` | P5, inside `handle_request` | Delegate to the pipeline's internal request handler. Read `ctx.request` for the DTO. |
| `hcm_validate_prerequisites(request)` | Before P1, inside `handle_request_validation` | **Required.** Validate ACP store-inputs eligibility, or any pre-P1 check that should block the poll URL. Raises `NotImplementedError` if not overridden. |
| `handle_request_validation(request)` | Rhode validation worker | Call `await self.hcm_handle_request_validation(request)`. Add any pre-HCM checks first (e.g. feature flags). |
| `handle_request(request)` | Rhode inference worker | Call `return await self.hcm_handle_request(request)`. |

**Optional overrides:**

| Method | Use case |
|---|---|
| `hcm_stash_enabled(request) → bool` | Return `False` for non-HCM requests to fall back to a legacy path (Image4 pattern). Defaults to `bool(worker_config.use_hcm)`. |
| `hcm_acp_cme_port(*, port_spec) → AcpCmePort \| None` | Override P4 port wiring. Default returns `DefaultAcpCmePort` when the YAML spec has `acp_persistence`; `None` otherwise. |
| `hcm_safety_port(*, port_spec) → SafetyPort \| None` | Override P6 port wiring. Default returns `ConfigDrivenSafetyPort` when the YAML spec has a `safety` block; `None` (no-op) otherwise. |
| `hcm_telemetry_port(*, port_spec) → TelemetryPort` | Override P8 port. Default returns `LoggingTelemetryPort` wired with the YAML `metrics` driver. |
| `hcm_validation_profile() → HorizontalsProfile` | Override validation-pass profile. Default is `validation_profile(profile_id=f"{binding.product.value}_validation")`. |
| `hcm_profile() → HorizontalsProfile` | Override inference-pass profile. Default is `inference_profile(profile_id=binding.product.value)`. |
| `hcm_request_timeout() → float \| None` | Optional timeout for the `handle_request` orchestrator run. Reads `worker_config.handle_request_timeout`; returns `None` if absent. |
| `hcm_workflow_parser(request) → Any` | Fallback workflow label resolver when the YAML spec has no `metrics.workflow` block. |
| `hcm_build_ports(validation, port_spec) → HorizontalPorts` | Full port bundle override (rarely needed; prefer YAML config or the per-port overrides above). |
| `hcm_on_request_finally(request)` | Runs in a `finally` block after `hcm_handle_request`. Use for inflight counter decrements or cleanup. |

---

### Step 3 — Wire the worker

Update `build.py` to point `worker_type` at the new class:

```python
build.deploy_worker(
    name=CM6_PIPELINE,
    worker_type="colligo.models.firefly.pipelines.cm6.CM6PipelineHcm.CM6PipelineHcm",
    request_type=CM6Request,
    response_type=CM6Response,
    ...
)
```

Add the `hcm` package to `colligo.yaml` deps if not already present:

```yaml
deps:
  - colligo.models.firefly.hcm
```

---

### Step 4 — Tests

Minimum test coverage for a new HCM pipeline:

**1. YAML spec row loads correctly:**

```python
from colligo.models.firefly.hcm.hcm_spec_schema import get_port_spec

def test_cm6_inference_spec_loads() -> None:
    spec = get_port_spec("cm6_inference")
    assert spec.generation_model.name == "CLIO_V6_CM_DIFFUSION"
```

**2. Stashed mixin wiring (model core runs, no MeteringUtils):**

```python
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from colligo.models.firefly.hcm.tests.conftest import make_stashed_hcm_worker

@pytest.mark.asyncio
async def test_cm6_hcm_handle_request_runs_orchestrator() -> None:
    worker = CM6PipelineHcm(...)
    request = MagicMock(spec=CM6Request)
    response = MagicMock(spec=CM6Response)

    with patch.object(worker, "_handle_cm6_request", new=AsyncMock(return_value=response)):
        result = await worker.hcm_handle_request(request)

    assert result is response
```

**3. BKS P1 / P7 (via `test_bks_p1_authorize.py` pattern):**

```python
from colligo.models.firefly.hcm.bks_p1_authorize import build_bks_p1_hooks_for_profile
from colligo.models.firefly.hcm.hcm_spec_schema import get_port_spec

@pytest.mark.asyncio
async def test_cm6_p1_validates_entitlements(mock_bks_entitlement) -> None:
    spec = get_port_spec("cm6_inference")
    _, validate = build_bks_p1_hooks_for_profile("cm6_inference", profile=spec)
    ctx = HCMRequestContext(request=MagicMock(), product=ProductFlow.INFERENCE)
    ctx.metadata[BKS_POLICIES_METADATA_KEY] = ["FIREFLY_MANDATORY_CHECKS"]
    await validate(ctx)
    mock_bks_entitlement.assert_awaited_once()
```

---

## Phase reference

| Phase | Name | Profile | What runs |
|---|---|---|---|
| P0 | Identity / route | both | Resolve org segment, populate identity metadata |
| P1 | BKS authorize | validation | `resolve_authorization_policies` → `validate_entitlements` via `BksPort` |
| P2 | Safety in | — | Input safety (not yet wired; no-op today) |
| P3 | Policy / moderation | — | Content policy (not yet wired; no-op today) |
| P4 | Data plane (ACP) | inference | `persist_result` via `AcpCmePort` when `store_inputs` is set; driven by `acp_persistence` YAML |
| P5 | Model core | inference | `hcm_run_model_core` via `ModelCorePort` |
| P6 | Safety out | inference | `scan_output` via `SafetyPort`; YAML `safety` block selects scanner (CM5: `NSFWAdobeOneComponent`) |
| P7 | BKS settle | inference | `settle(success/error)` via `BksPort` — replaces `*MeteringUtils` on HCM paths |
| P8 | Telemetry | inference | `emit_event(hcm.request.complete)` via `TelemetryPort`; triggers completion metrics |

`validation_profile` enables P1 only. `inference_profile` enables P4 + P5 + P6 + P7 + P8.
