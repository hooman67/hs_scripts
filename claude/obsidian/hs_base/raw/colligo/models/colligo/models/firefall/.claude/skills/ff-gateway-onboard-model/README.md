# ff-gateway-onboard-model

A Claude Code skill that automates onboarding a new third-party model or model provider into the Firefall FF Gateway (gen3p) pipeline.

---

## What it does

Given an API spec and a few inputs, the skill guides Claude through every step needed to wire a new provider into the FF Gateway pipeline:

1. Analyzes the provider's API spec (auth, endpoints, payload format, error codes)
2. Decides whether to extend an existing provider or create a new one
3. Writes the YAML config entry in `default_3p_model_configs.yaml`
4. Creates the provider schema class in `provider_schemas/<provider_name>.py` (Pydantic-based, drives both discovery and validation)
5. Implements the provider Python class (headers, payload, response parsing, polling, content filtering, metering)
6. Identifies and proposes any changes to `Gen3PPipelineRequest` types
7. Verifies discovery API schema exposure
8. Generates a test file with all required test cases
9. Runs lint and tests to confirm everything is wired correctly

Before making any file changes the skill presents a full plan for user approval.

---

## Installation

The skill is already installed at the project level:

```
.claude/skills/ff-gateway-onboard-model/
├── SKILL.md
├── README.md
└── references/
    ├── provider_image.py.tmpl
    ├── provider_video.py.tmpl
    ├── provider_audio.py.tmpl
    ├── provider_schema.py.tmpl
    └── test_provider.py.tmpl
```

No additional setup is required. Claude Code automatically discovers skills under `.claude/skills/` when it starts in this repo.

---

## How to trigger

Just describe what you want to do in natural language. The skill activates on keywords like:

- `onboard model`
- `new model provider`
- `3p model` / `third-party model`
- `add model version`
- `gen3p pipeline` / `ff gateway` / `firefall gateway`
- `integrate model`

You can also invoke it explicitly:

```
/ff-gateway-onboard-model
```

---

## Examples

### Example 1 — Onboard a new image provider (Ideogram-style)

```
Onboard a new image model provider. The API spec is at https://ideogram.ai/docs/api.
Provider name: acme-image, model ID: acme, version: 1.0.
```

Claude will:
- Fetch and parse the API spec
- Detect it uses a Bearer token auth and JSON payloads
- Present a plan listing every file to be created/modified
- After approval: add a YAML entry under `default_3p_model_configs.yaml`, create
  `provider_schemas/acme_image.py` (Pydantic `ImageProviderSchema` subclass),
  create `model_providers/AcmeImageProvider.py` (extending `ImageThirdPartyModelProvider`),
  and write `tests/test_acme_image_provider.py`

---

### Example 2 — Add a new version to an existing video provider

```
Add model version "ray-4" (internal: "ray-4-0") to the existing Luma provider.
API spec: https://docs.lumalabs.ai/reference
```

Claude will:
- Confirm the `luma` provider already exists in both the YAML config and `LumaProvider.py`
- Present a plan: only two files change — a new model entry in the YAML, a new version
  branch in `LumaProvider.py`, and a new schema class in `provider_schemas/luma.py`
- Leave all other Luma versions untouched

---

### Example 3 — Onboard an async video provider with polling

```
Onboard Runway's new video API. Spec: https://docs.runwayml.com/reference/intro
Provider: runway-new, model: runway-new, version: gen5, modality: video
```

Claude will:
- Detect the API uses async submission + a polling endpoint
- Set `async_api: true` in the YAML with appropriate timeout and polling pause values
- Implement `_get_polling_reference()` and `_polling_response_ready()` in the provider class
- Map `reference_images` (first/last frame) and `reference_videos` from the request

---

### Example 4 — Onboard an audio provider with speech-to-speech

```
Onboard a new TTS/STS audio provider. Spec: https://api.speechprovider.com/docs
Name: speech-provider, model: speech, versions: tts-v1 and sts-v1, modality: audio
```

Claude will:
- Detect TTS uses JSON payload but STS uses `multipart/form-data` with a binary audio field
- Implement conditional payload construction in `_request_payload()`
- Remove `Content-Type` from headers for the FormData path (aiohttp sets it automatically)
- Implement `_is_response_raw_bytes()` → True and `_parse_successful_raw_response()`
- Stub `handle_voice_list_request()` with Redis caching pattern

---

### Example 5 — Provider that supports both image and video

```
Onboard FAL.AI's new provider that generates both images and videos.
Spec: https://fal.ai/docs/api
Provider: fal-new, modality: image+video
```

Claude will:
- Use `ImageVideoThirdPartyModelProvider[Gen3PVisualPipelineRequest]` as the base class
- Define a `_determine_workflow()` method routing to t2i / t2v / edit workflows
- Use `WORKFLOW_FIELDS` + `WORKFLOW_CONSTRAINTS` on the schema class for per-workflow validation

---

## Files touched per onboarding

| File | Always? | Notes |
|---|---|---|
| `configs/default_3p_model_configs.yaml` | Yes | New provider entry or new model version |
| `provider_schemas/<provider_name>.py` | Yes | New file — Pydantic schema class, source of truth for discovery and validation |
| `model_providers/<Name>Provider.py` | Yes | New file (new provider) or extended (new version) |
| `pipelines/gen_3p/types.py` | Only if needed | New request property — proposed and approved first |
| `tests/test_<name>_provider.py` | Yes | New file with ≥ 10 test cases |
| `pylibs/colligo/external_services/business_kit/business_kit_service_types.py` | Only if needed | New `GenerationModel` enum member when `bks_generation_model` value is new |

---

## Key conventions enforced by the skill

| Convention | Detail |
|---|---|
| `hidden: true` + `allow_usage_despite_hidden: true` | Always set for new models |
| `bks_generation_model` | Pattern: `firefall_3p:external:<code>`; must also have a matching `GenerationModel` enum member in `business_kit_service_types.py` |
| `reference_blob_with_meta_defaults` | Only defined when reference media has `min_items >= 1` |
| Circuit breaker | `circuit_breaker_enabled: true`; specific tuning values are optional (defaults apply) |
| FormData headers | Do NOT set `Content-Type` manually — aiohttp sets it with the boundary |
| New request properties | Generalized first; added to the broadest applicable type in the hierarchy |
| Provider registration | Automatic via `pkgutil.walk_packages` — no manual step needed |
| No `allowed_schema_properties` in YAML | Schema class controls discovery output directly |
| No `schema:` block under `model_specific_config` | Validation lives in the Pydantic schema class |
| `model_specific_config` | Only for runtime-consumed values (e.g. `prompt_max_length`, size bounds) |

---

## Provider schema system

The skill uses a Pydantic-based schema class (subclass of `ImageProviderSchema`, `VideoProviderSchema`, or `AudioProviderSchema`) as the **single source of truth** for both client-facing discovery and server-side validation. Key features:

- `REFERENCE_USAGE_CAPS` and `MAX_FILE_SIZE_BYTES` ClassVars drive the caps/discovery endpoint automatically
- `WORKFLOW_FIELDS`, `WORKFLOW_CONSTRAINTS`, and `WORKFLOW_FIELDS_NONMODEL_KEYS` ClassVars support multi-workflow providers (e.g. t2v + i2v); declare outbound-only keys (renames, flattened fields) in `WORKFLOW_FIELDS_NONMODEL_KEYS` so the schema-registry invariants gate can distinguish them from typos
- Import-time guard (`__pydantic_init_subclass__`) raises `TypeError` at boot if any schema field is absent from or incompatible with the pipeline request type

---

## Reference templates

The skill uses templates in `references/` as starting skeletons. Claude reads the
appropriate template, substitutes all `{PLACEHOLDER}` values, and fills in the
provider-specific logic based on the API spec.

| Template | Used for |
|---|---|
| `provider_image.py.tmpl` | Image-only providers |
| `provider_video.py.tmpl` | Video-only providers |
| `provider_audio.py.tmpl` | Audio providers (TTS / STS) |
| `provider_schema.py.tmpl` | All modalities — Pydantic schema class skeleton |
| `test_provider.py.tmpl` | All modalities — 10 test cases stubbed |

---

## Verification

After onboarding, the skill runs:

```bash
# YAML syntax check
python -c "import yaml; yaml.safe_load(open('models/colligo/models/firefall/firefall_router/configs/default_3p_model_configs.yaml'))"

# Schema import check (import-time guard fires here)
python -c "from colligo.models.firefall.firefall_router.provider_schemas.<provider_name> import <SchemaClass>"

# Lint (mypy + ruff)
./m lint --paths \
  models/colligo/models/firefall/firefall_router/model_providers/<Name>Provider.py \
  models/colligo/models/firefall/firefall_router/provider_schemas/<provider_name>.py \
  models/colligo/models/firefall/firefall_router/tests/test_<name>_provider.py

# Unit tests
pytest models/colligo/models/firefall/firefall_router/tests/test_<name>_provider.py -v
```
