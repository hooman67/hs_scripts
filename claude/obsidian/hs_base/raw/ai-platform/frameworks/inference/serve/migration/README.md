The `migration/` folder contains **platform-owned libraries** for external Adobe services (CAI, IMS, BKS, temp storage, etc.). These are services that the inference platform team owns and maintains for consumers of the framework.

# Stability and lifecycle

The migration API is **unstable** — the shape of these APIs may change between releases. However, we maintain **backwards compatibility**.

These libraries are explicitly **temporary**. The goal is:
1. Make the services available now under `frameworks.inference.migration.*` so teams can start migrating
2. Iterate on the API based on real usage
3. Once an API is stable and well-understood, graduate it to the main `frameworks.inference.*` API (removing the `migration` prefix)

# Why it exists

Colligo v2 had direct access to services like BKS, CAI, IMS, and temp storage via global config and internal APIs. In v3, we don't want to expose those internals directly. Instead, the migration layer wraps them with a clean v3-style API while the underlying implementation is still colligo v2 code.

# Where the implementation lives

The actual service implementations still live in the **colligo monorepo**, not here. The migration modules re-export symbols from the vendored colligo folders under `_private/colligo/`. This means:

- **To use a service**: import from `frameworks.inference.migration.*` — this is the stable interface
- **To contribute or fix a bug**: the source of truth is still in colligo. Changes made there do **not** automatically propagate to ai-platform. A manual sync is required to pull updates from colligo into the vendored `_private/colligo/` tree.
- **Long-term**: as each service is fully ported to ai-platform, it will be removed from colligo and implemented natively here, then promoted to `frameworks.inference.*`

# Installation

```bash
pip install frameworks.inference[migration]
```

# Libraries

All libraries share a single `MigrationConfig` registered via `RegisterDefaultConfig` at `frameworks.inference.migration.default_config`. Each library section below shows how to configure it.

````{admonition} MigrationConfig
:class: note

### MigrationConfig

Unified configuration for all migration services.

This configuration is registered to maintain backward compatibility
with colligo v2 code and provides a single configuration point for
all external services being migrated to ai-platform v3.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `cai` | `CAIConfig` | `CAIConfig()` |  |
| `ims` | `IMSConfig` | `IMSConfig()` |  |
| `business_kit` | `BusinessKitConfig` | `BusinessKitConfig()` |  |
| `object_store` | `ObjectStoreConfig` | `ObjectStoreConfig()` |  |
| `temp_storage` | `TempStorageConfig` | `TempStorageConfig()` |  |
| `acp` | `ACPConfig` | `ACPConfig()` |  |

````

## CAI (`migration/cai`)

Content Authenticity Initiative — C2PA signing for digital assets.

- Signs images/videos with a C2PA manifest (chain of custody, provenance, AI generation metadata)
- Uses IMS service-to-service auth (`CAIConfig.ims_credentials`) to call the signing service
- **Linux-only**: the `adobe_c2pa` native library only supports Linux. On macOS calls will fail at runtime.
- Entry points: `cai_sign_image()`, `get_ims_provider()`, `CAIManifest`, `EncodedImage`

```python
from frameworks.inference.migration import cai

token_provider = cai.get_ims_provider()
manifest = cai.CAIManifest(...)
signed = cai.cai_sign_image(image, manifest, token_provider)
```

### Configuration

CAI requires IMS credentials for the signing service. In production, these come from Vault at `dme_spl/services/firefly/{env}/common/FIREFLY_CAI_HIGH_SECURITY` (fields `client-code` and `client-secret`):

```python
inference.initialize(configs={
    "frameworks.inference.migration.default_config": {
        "cai": {
            "ims_credentials": {
                "client_id": "firefly-cai-signing",
                "client_code": {_env: "HIGH_SECURITY_CAI_SIGNING_CODE"},
                "client_secret": {_env: "HIGH_SECURITY_CAI_SIGNING_SECRET"},
            }
        },
    }
})
```

### API Reference

````{admonition} CAI API
:class: note

### CAIConfig

Configuration for CAI (Content Authenticity Initiative) service.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `ims_credentials` | `IMSCredentials` | `IMSCredentials()` |  |

````

## IMS (`migration/ims`)

Identity Management Services — Adobe's authentication system.

- Used internally by CAI and BKS to obtain service tokens for service-to-service calls
- Can also be used directly to validate user tokens or create IMS service instances
- Configured via `IMSConfig` (env, enabled, host)

```python
from frameworks.inference.migration import ims

service = ims.create_ims_service_with_credentials("my-service", credentials)
```

### API Reference

````{admonition} IMS API
:class: note

### IMSConfig

Configuration for IMS (Identity Management Services) service.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `env` | `ImsEnv` | `'stage'` |  |
| `enabled` | `bool` | `False` |  |
| `host` | `HttpUrl` | `HttpUrl('https://ims-na1-stg1.adobelogin.com/')` |  |

````

## Business Kit (`migration/business_kit`)

Authorization and credit metering — controls whether a user can perform an operation and charges credits.

### Authorization

Check if the user is entitled to perform an operation:

```python
from frameworks.inference.migration import business_kit

tier = await business_kit.perform_business_kit_authorization(
    business_kit.BusinessKitAuthorizationInput(
        features={"firefly:internal:image5_generate": 1},
        policies=["metering_enforcement", "firefly_mandatory_checks"],
        get_user_tier_info=True,
    )
)
```

`BusinessKitAuthorizationInput` fields:
- `features`: dict mapping model/feature names to counts (how many units to authorize)
- `policies`: list of authorization policies to check (e.g. `"metering_enforcement"`, `"firefly_mandatory_checks"`, `"firefly_geoip_blocking"`)
- `get_user_tier_info`: if `True`, returns the user's tier string (e.g. `"free"`, `"premium"`)
- `metadata`: optional dict of additional context for the authorization check

### Metering

After successful generation, deduct credits from the user's balance:

```python
business_kit.perform_business_kit_metering(
    metering_data={"num_images": 1, "resolution": "1024x1024"},
    model_name=business_kit.GenerationModel.FIREFLY_IMAGE5_GENERATE,
)
```

Parameters:
- `metering_data`: dict with generation details for the metering payload
- `model_name`: `GenerationModel` enum value identifying the model used
- `error`: optional `MeteringError(type=..., message=...)` — if the generation failed, pass this so credits are not deducted
- `chargesWithheld`: if provided, credits won't be deducted (dry-run metering)

To revert a credit deduction (e.g. if post-processing fails after metering):

```python
business_kit.perform_credit_return(
    metering_data={"num_images": 1},
    model_name=business_kit.GenerationModel.FIREFLY_IMAGE5_GENERATE,
)
```

**IMS token propagation**: BKS uses the user's IMS token (from the incoming HTTP request) to authorize on behalf of the user. In v3 the token is always available via `get_request_ctx().ims_token` — no `store_credentials=True` is needed (that was a v2 opt-in that is always-on in v3).

### Configuration

BKS is disabled by default. To enable it, set `client_id` explicitly. The standard platform credential is `colligov2_platform`. In production, `client_code` and `client_secret` come from Vault at `dme_spl/services/firefly/{env}/common/colligo_ims_credentials` (fields `ims_code` and `ims_secret`):

```python
inference.initialize(configs={
    "frameworks.inference.migration.default_config": {
        "business_kit": {
            "ims_credentials": {
                "client_id": "colligov2_platform",
                "client_code": {_env: "BKS_IMS_CODE"},
                "client_secret": {_env: "BKS_IMS_SECRET"},
            }
        },
    }
})
```

### API Reference

````{admonition} Business Kit API
:class: note

### BusinessKitConfig

Configuration for Business Kit Service (authorization and metering).

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `host` | `HttpUrl` | `HttpUrl('https://bks-stage.adobe.io/')` |  |
| `ims_credentials` | `IMSCredentials` | `IMSCredentials()` |  |
| `max_retries` | `int` | `3` |  |

````

## Object Store (`migration/object_store`)

Session-scoped distributed key-value store backed by Redis (MEMORY durability) or S3 (DURABLE durability).

Used for storing intermediate results or state that needs to survive worker handoffs within a single request session.

```python
from frameworks.inference.migration.object_store import session_support

await session_support.set_data("key", value)
data = await session_support.get_data("key")
```

### Data ping-pong avoidance

In a typical pipeline flow (`pipeline → worker A → pipeline → worker B`), data returned by worker A transits through the pipeline pod before being forwarded to worker B. For large tensors this wastes memory on the pipeline pod and adds serialization overhead for data the pipeline doesn't need.

Workers can use the object store to pass data directly to each other — the pipeline only sees a small key string:

```
                    object store
                    ┌─────────────┐
          set_data  │   tensor    │  get_data
        ┌──────────►│             ├──────────────┐
        │           └─────────────┘              │
        │                                        ▼
   ┌────┴─────┐     key (string)          ┌──────────┐
   │ Worker A ├──────────────────►        │ Worker B │
   └──────────┘     via pipeline          └──────────┘
```

**Worker A** — serialize and store the tensor, return only the key:

```python
import io, uuid
import torch
from frameworks.inference.migration.object_store import session_support

key = f"embeddings_{uuid.uuid4().hex[:8]}"
buf = io.BytesIO()
torch.save(tensor, buf)
await session_support.set_data(key, buf.getvalue())
# return the key to the pipeline (small string, not the tensor)
```

**Worker B** — pull the tensor using the key:

```python
import io
import torch
from frameworks.inference.migration.object_store import session_support

data = await session_support.get_data(key)
tensor = torch.load(io.BytesIO(data), weights_only=True)
```

All workers in the same request share a `session_id` (propagated via `RequestContext`), so `set_data` in one worker is readable by `get_data` in another.

### Durability settings

By default the store uses `MEMORY` durability — data lives in the worker pod's memory with a routing pointer in Redis, and other pods fetch via direct RPC. For data that must survive pod restarts, use `DURABLE` (S3-backed):

```python
from frameworks.inference.migration.object_store import session_support
from frameworks.inference.migration.object_store.session_support import (
    SessionStorageDurability,
    SessionStorageOptions,
)

await session_support.set_data(
    key,
    buf.getvalue(),
    options=SessionStorageOptions(
        durability=SessionStorageDurability.DURABLE,
        ttl_s=300,  # optional: expire after 5 minutes
    ),
)
```

### API Reference

````{admonition} Object Store API
:class: note

### ObjectStoreConfig

Configuration for Object Store (session support).

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `durability` | `StorageDurability` | `'memory'` |  |
| `ttl_s` | int \| None | `None` |  |

````

## ACP (`migration/acp`)

Adobe Creative Platform — upload, download, and manage file assets in Creative Cloud.

Used for reading user-supplied `creativeCloudFileId` inputs (images, videos) and uploading generated results back into a user's Creative Cloud folder.

### Downloads

Download a file or component from ACP by its asset ID:

```python
from frameworks.inference.migration import acp

context = acp.ACPContext(api_key="colligo_acp", user_token=ims_user_token)
async with acp.AsyncClientWithStats() as client:
    binary = await acp.get_data_from_acp_file_asset(asset_id, context)
    # binary.to_bytes() -> raw file content
```

For Photoshop-style composites (a component within an asset):

```python
binary = await acp.get_data_from_acp_component(asset_id, component_id, context)
```

### Uploads

Upload a generated file into a user's Creative Cloud folder:

```python
from frameworks.inference.migration import acp

context = acp.ACPContext(api_key="colligo_acp", user_token=ims_user_token)
asset = acp.Binary(value=video_bytes, metadata={"mime_type": "video/mp4"})

async with acp.AsyncClientWithStats() as client:
    new_asset_id = await acp.upload_acp_file_asset(
        folder_asset_id=target_folder_urn,
        asset=asset,
        upload_size=len(video_bytes),
        file_name="output.mp4",
        acp_context=context,
        http_client=client,
    )
```

### Metadata

Patch application metadata on an uploaded asset (e.g. to tag it with generation provenance):

```python
await acp.patch_acp_application_metadata(
    asset_id=new_asset_id,
    namespace="firefly",
    metadata={"prompt": "a viking ship", "model": "gen6"},
    acp_context=context,
    http_client=client,
)
```

### Configuration

ACP downloads are gated by `ACPConfig.enable_inputs` (for `creativeCloudFileId`) and `ACPConfig.enable_components_inputs` (for `creativeCloudComponentId`). Uploads are gated by `ACPConfig.enable_outputs`. All default to `True`.

```python
inference.initialize(configs={
    "frameworks.inference.migration.default_config": {
        "acp": {
            "enable_inputs": True,
            "enable_components_inputs": True,
            "enable_outputs": True,
            "api_key": "colligo_acp",
        }
    }
})
```

### API Reference

````{admonition} ACP API
:class: note

### ACPConfig

Configuration for Adobe Creative Platform (ACP) file storage.

Controls whether the framework allows downloading/uploading assets
via creativeCloudFileId and creativeCloudComponentId inputs/outputs.
Maps to v2's ``CreateCloudStorageConfig``.

These flags gate the common input-resolution path
(``temp_storage.load_data_from_storage_item``) — when disabled, requests
containing the corresponding ACP identifier are rejected with a validation error.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enable_inputs` | `bool` | `True` | Allow downloading assets via creativeCloudFileId. Checked by temp_storage.load_data_from_storage_item; when False, any request containing a creativeCloudFileId is rejected. |
| `enable_components_inputs` | `bool` | `True` | Allow downloading Photoshop-style components via creativeCloudComponentId. Checked by temp_storage.load_data_from_storage_item; when False, any request containing a creativeCloudComponentId is rejected. |
| `enable_outputs` | `bool` | `True` | Allow uploading generated results to a user's Creative Cloud folder (output.targetFolder). When False, upload attempts are rejected. |
| `api_key` | `str` | `'colligo_acp'` | The x-api-key sent on all ACP HTTP calls (download, upload, metadata). |

````

## Temp Storage (`migration/temp_storage`)

Cloud-agnostic blob storage for temporary data (S3 or Azure Blob). Used for uploading generated content and creating presigned download URLs for clients.

```python
from frameworks.inference.migration import temp_storage

# Upload a Binary object (e.g. from a worker output)
obj_id = await temp_storage.upload_binary_to_temp_storage(binary)

# Upload raw bytes
obj_id = await temp_storage.upload_bytes_to_temp_storage(
    content=image_bytes,
    mime_type="image/jpeg",
)

# Download
stored = await temp_storage.download_from_temp_storage(obj_id)
# stored.content      -> bytes
# stored.content_type  -> str (e.g. "image/jpeg")

# Presigned URL — clients download directly from S3/Azure, no proxy
url = await temp_storage.create_presign_url_for_temporary_storage(
    obj_id,
    expires_in=3600,  # seconds, default 1 hour
)

# Check existence
exists = await temp_storage.key_exists_in_temp_storage(obj_id)

# Delete
await temp_storage.delete_object_from_temp_storage(obj_id)
```

Both upload functions return a `uuid.UUID`. You can pass your own `id=` to use a deterministic key.

### Block upload (multipart)

For large files, use block upload to stream chunks:

```python
info = await temp_storage.initiate_block_upload_for_temporary_storage(
    id=obj_id,
    content_type="video/mp4",
    total_size=total_bytes,
    block_size=5 * 1024 * 1024,  # 5 MB chunks
)
# ... upload each block to info.upload_urls[i] ...
result = await temp_storage.complete_block_upload_for_temporary_storage(
    temp_storage.BlockUploadCompleteInfo(
        upload_id=info.upload_id,
        blocks=[{"block_index": i, "etag": etag} for i, etag in enumerate(etags)],
    )
)
```

### Configuration

Temp storage uses the S3/Azure bucket configured in the main `InferenceFrameworkConfig.s3`. To override the bucket:

```python
inference.initialize(configs={
    "frameworks.inference.migration.default_config": {
        "temp_storage": {
            "bucket": "my-bucket",
            "enable_block_upload": True,
        },
    }
})
```

### API Reference

````{admonition} Temp Storage API
:class: note

### TempStorageConfig

Configuration for Temp Storage (blob storage) - consolidated for v3 API.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `backend` | `BlobBackend` | `'S3'` |  |
| `bucket` | `str` | `'pre-signed-firefly-dev'` |  |
| `presigned_url_config` | `PresignedURLSettings` | `PresignedURLSettings()` |  |
| `enable_tagging` | `bool` | `True` |  |
| `enable_block_upload` | `bool` | `True` |  |

````

## Metrics (`migration/metrics`)

Register and emit metrics to Prometheus, NewRelic, and S3.

> Metrics has no `MigrationConfig` entry — backends are controlled by `MetricsConfig` in the main `InferenceFrameworkConfig`.

```python
from frameworks.inference.migration.metrics import METRICS_FACTORY

REQUEST_COUNT = METRICS_FACTORY.create_counter(
    "my_service_requests_total",
    prometheus_options={"documentation": "Total requests", "labelnames": ["status"]},
    newrelic_options={"labelnames": ["status"]},
)
REQUEST_COUNT.labels(status="ok").inc()
```

Pre-registered generation metrics for finance dashboards (must stay identical to v2):

```python
from frameworks.inference.migration.metrics import generations

generations.IMAGE_GENERATIONS.labels(
    workflow="image_gen",
    error_code="",
    client_id="my-client",
    path="/v3/images/generate",
    model_version="v6",
    detail_level="standard",
).inc()
```

See [migration/metrics/aidoc/metrics.md](/frameworks/inference/serve/migration/metrics/aidoc/metrics.md) for full reference.
