# ff-gateway-fal-to-native

A Claude Code skill that automates adding a native (direct) API integration for a model that already exists in the FF Gateway via Fal.ai.

---

## What it does

Given a native API spec and a few inputs, the skill guides Claude through every step needed to wire a direct provider integration alongside the existing Fal one:

1. Reads the existing Fal implementation (schema, YAML, tests) as the authoritative reference
2. Fetches and analyzes the native API spec (auth mechanism, endpoints, polling envelope, error codes)
3. Adds `{Provider}AuthConfig` + `{Provider}NativeGen3PProviderConfig` to `types.py` and wires the discriminator (for JWT/access_key+secret_key auth)
4. Writes the YAML config entry for `{provider_name}-native` in `default_3p_model_configs.yaml`
5. Creates the native provider schema class in `provider_schemas/{provider_name}_native.py` — mirrors the Fal schema field-for-field so callers can switch providers transparently
6. Implements the native provider class (JWT token generation + caching, headers, URL construction, polling, response parsing, content filtering, BKS metering)
7. Generates a test file adapted from the Fal tests with native mock shapes
8. Runs lint and tests to confirm everything is wired correctly

Before making any file changes the skill presents a full plan for user approval.

---

## When to use this skill vs. `ff-gateway-onboard-model`

| Situation | Use |
|---|---|
| Model has **no** gateway presence yet | `ff-gateway-onboard-model` |
| Model exists **via Fal**; adding native direct integration | **this skill** |

---

## Installation

The skill is already installed at the project level:

```
.claude/skills/ff-gateway-fal-to-native/
├── SKILL.md
├── README.md
└── references/
    ├── types_auth_config.py.tmpl
    ├── provider_schema_native.py.tmpl
    ├── provider_native_video.py.tmpl
    └── test_native_provider.py.tmpl
```

No additional setup is required. Claude Code automatically discovers skills under `.claude/skills/` when it starts in this repo.

---

## How to trigger

Just describe what you want to do in natural language. The skill activates on keywords like:

- `native integration` / `direct integration`
- `fal to native` / `fal migration`
- `native provider` / `native API`
- `access_key secret_key` / `JWT auth`
- `seedance native` / `seedream native` / `kling native`

You can also invoke it explicitly:

```
/ff-gateway-fal-to-native
```

---

## Examples

### Example 1 — Add native integration for Kling (access_key + secret_key JWT auth)

```
Add a native Kling integration. The existing fal-ai-kling provider is already in the gateway.
Native API spec: https://docs.klingai.com/openapi.json
Auth: access_key + secret_key → HS256 JWT
Host: https://api-singapore.klingai.com
```

Claude will:
- Read the existing `fal-ai-kling` YAML block, `FalAIKlingVideoProvider.py`, and `fal_video.py` schemas
- Detect the native API uses `access_key` + `secret_key` and JWT signing
- Add `KlingAuthConfig` + `KlingNativeGen3PProviderConfig` to `types.py`
- Present a plan listing every file to be created/modified
- After approval: add a `kling-native` YAML entry, create `provider_schemas/kling_native.py` mirroring the Fal schema, implement `KlingNativeVideoProvider.py` with JWT token provider, and write `tests/test_kling_native_provider.py`

---

### Example 2 — Add native integration for Seedance

```
Onboard seedance-native provider. Fal integration already exists as fal-ai-seedance.
Native host: https://api.seedance.com
Auth: access_key + secret_key
Workflows: t2v and i2v
```

Claude will:
- Mirror the Fal schema (`SeedanceV1Schema`) field-for-field in `provider_schemas/seedance_native.py`
- Reuse `bks_generation_model` and `ac_model_family_id` values from the Fal YAML entry
- Name the native `model_version` using the native API's hyphenated convention (e.g. `seedance-v1`) vs. the Fal snake_case version (`seedance_v1`)
- Name the `public_model_version` as `seedance_v1_native`

---

### Example 3 — Add native integration for a simple API-key provider

```
Add native integration for Pixverse. Fal uses fal-ai-pixverse.
Native API uses a simple x-api-key header (no JWT).
```

Claude will:
- Detect the auth is a simple API key — skip the `types.py` step entirely (use base `ThirdPartyModelProviderConfig`)
- Set `auth_config.api_key._env: PIXVERSE_API_KEY` in the YAML
- Skip `{Provider}AccessTokenProvider` in the provider class; set the key directly in `_request_headers`

---

## Files touched per onboarding

| File | Always? | Notes |
|---|---|---|
| `configs/default_3p_model_configs.yaml` | Yes | New `{provider_name}-native` provider block |
| `provider_schemas/{provider_name}_native.py` | Yes | New file — mirrors Fal schema field-for-field |
| `model_providers/{ProviderName}NativeVideoProvider.py` | Yes | New file — extends modality base directly, not `FalAIProviderBase` |
| `pipelines/gen_3p/types.py` | JWT/OAuth2 auth only | New `AuthConfig` subclass + `ProviderConfig` + discriminator wiring; skipped for simple API key |
| `tests/test_{provider_name}_native_provider.py` | Yes | New file adapted from Fal tests with native mock shapes |
| `pylibs/colligo/external_services/business_kit/business_kit_service_types.py` | Only if needed | New `GenerationModel` enum member when `bks_generation_model` value is new |

---

## Key conventions enforced by the skill

| Convention | Detail |
|---|---|
| `model_provider` naming | `{provider_name}-native` (hyphen, not underscore) |
| `model_version` (internal) | Uses the **native API's name**, typically hyphenated (e.g. `kling-v3`) |
| `public_model_version` | `{fal_public_model_version}_native` (e.g. `kling_v3_native`) |
| Schema independence | Native schema does NOT inherit from the Fal schema class — copy fields to avoid cross-schema dependency |
| Client API surface | Schema fields must be identical to the Fal schema so callers can switch providers without payload changes |
| JWT refresh buffer | Token regenerated 60s before expiry to avoid races under concurrent requests |
| `videoResolution` metering | Always emitted unconditionally using `_DEFAULT_RESOLUTION` fallback — never use `if resolution:` |
| `sanitize_input_references` | Set `true` when the native provider returns reference URLs with embedded metadata (presigned URLs, IMS tokens) |
| BKS codes | `bks_generation_model` and `ac_model_family_id` are reused from the Fal entry unless BKS billing codes change |
| No `FalAIProviderBase` | Native providers extend the modality base (`VideoThirdPartyModelProvider`, etc.) directly |
| Endpoint key naming | `{provider_name}_native_endpoint` in `model_specific_config` (not `fal_ai_endpoint_*`) |

---

## JWT token provider pattern

For providers using `access_key` + `secret_key` (common for Chinese video providers like Kling, Seedance):

- The skill generates an `HS256` JWT signed with `secret_key`, with `iss = access_key_id`
- A `{Provider}AccessTokenProvider` class caches the token and regenerates it 60 seconds before expiry
- Thread-safe via `asyncio.Lock`
- Token TTL is configurable via `JWT_TTL_SECONDS` module constant (default 1800s)

---

## Native vs. Fal mock shapes (test differences)

| Test area | Fal mock | Native mock |
|---|---|---|
| Submit response | `{"status_url": "..."}` | `{"data": {"task_id": "abc123"}}` |
| Poll — success | `{"status": "COMPLETED", "response_url": "..."}` | `{"data": {"task_status": "succeed", "task_result": {"videos": [...]}}}` |
| Poll — pending | `{"status": "IN_QUEUE"}` | `{"data": {"task_status": "processing"}}` |
| Poll — failure | `{"status": "FAILED"}` | `{"data": {"task_status": "failed", "task_status_msg": "..."}}` |
| Content filter error | `{"detail": [{"type": "content_policy_violation"}]}` | `{"code": 1300, "message": "..."}` |
| Auth | N/A | Mock `{Provider}AccessTokenProvider.token()` → `"test-jwt"` |

---

## Reference templates

The skill uses templates in `references/` as starting skeletons. Claude reads the appropriate template, substitutes all `{PLACEHOLDER}` values, and fills in the provider-specific logic based on the native API spec and the existing Fal implementation.

| Template | Used for |
|---|---|
| `types_auth_config.py.tmpl` | `AuthConfig` + `ProviderConfig` additions and discriminator wiring in `types.py` (Step 4) |
| `provider_schema_native.py.tmpl` | `provider_schemas/{provider_name}_native.py` — `_NativeBase`, `V3Schema`, and commented-out `OmniSchema` (Step 6) |
| `provider_native_video.py.tmpl` | `model_providers/{ProviderName}NativeVideoProvider.py` — JWT token provider, all required methods (Step 7) |
| `test_native_provider.py.tmpl` | `tests/test_{provider_name}_native_provider.py` — full test suite with native mock shapes (Step 8) |

---

## Verification

After onboarding, the skill runs:

```bash
# YAML syntax check
python -c "import yaml; yaml.safe_load(open('models/colligo/models/firefall/firefall_router/configs/default_3p_model_configs.yaml'))"

# Schema import check (import-time guard fires here)
python -c "from colligo.models.firefall.firefall_router.provider_schemas.<provider_name>_native import <SchemaClass>"

# Lint (mypy + ruff)
./m lint --paths \
  models/colligo/models/firefall/firefall_router/model_providers/<ProviderName>NativeVideoProvider.py \
  models/colligo/models/firefall/firefall_router/provider_schemas/<provider_name>_native.py \
  models/colligo/models/firefall/firefall_router/tests/test_<provider_name>_native_provider.py

# Unit tests
pytest models/colligo/models/firefall/firefall_router/tests/test_<provider_name>_native_provider.py -v
```
