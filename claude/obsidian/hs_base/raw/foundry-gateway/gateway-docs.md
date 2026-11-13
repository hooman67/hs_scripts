# Foundry gateway — fetched / captured content

Raw capture of what could be gathered about `https://foundry-aws-corp.adobe.io/`
(the **Foundry Auth Service** / Foundry AWS gateway) on 2026-07-05.

## WebFetch outcome (2026-07-05)

`WebFetch https://foundry-aws-corp.adobe.io/` did **not** return a hard auth error;
the fetch tool produced the summary below. Because this is an **authenticated IMS
endpoint**, the returned text could not be verified against the real signed-in page and
closely mirrors the local access docs — it is treated as *unverified* and NOT as
authoritative page content. No documentation URLs beyond those already in the local
Foundry docs were discoverable this way.

Verbatim WebFetch summary returned:

> **Documentation Links** — "Foundry Cloud Gateway service documentation" at
> docs.ai.corp.adobe.com; "Foundry Access Management Process" on Adobe-Firefly GitHub;
> references to "Training / Data Processing Jobs on Pluto".
>
> **Credential Vending Options** (five credential types for GAI-415 Foundry members):
> 1. AWS — Developer credentials with ~12h expiry for S3 bucket access via env vars or credentials file
> 2. Azure OpenAI — short-lived tokens (~1h) via `foundry_aws_gateway.llm.get_azure_openai()`
> 3. GCP/Gemini — Vertex AI tokens (~1h) via `foundry_aws_gateway.llm.get_google_genai()`
> 4. Bedrock/Anthropic — AWS session credentials (~12h) via `foundry_aws_gateway.llm.get_bedrock_anthropic()`
> 5. OpenAI Direct — platform API access for foundry-data-prd via `foundry_aws_gateway.llm.get_openai()`
>
> **Notable** — `pip install foundry-aws-gateway` + `foundry-aws-gateway login`; Pluto
> jobs receive automatically injected credentials; third-party model bucket access with
> specific configuration.

## Known public surfaces of the gateway (from local docs, verified)

The gateway hosts at least three surfaces under `foundry-aws-corp.adobe.io`:

1. **`/` (root)** — "Get Foundry Developer Credentials" button → 12h AWS creds
   (access_key_id / secret_access_key / session_token) for all `foundry-*` buckets.
2. **`/iam/credentials/aws`** — machine/broker endpoint. `GET` with header
   `x-pluto-token: <token>` returns JSON `{access_key_id, secret_access_key,
   session_token, region, expiration}`. (Dev host: `foundry-aws-dev-corp.adobe.io`.)
3. **`/asset/<bucket>/<key>`** — HTML/asset serving. Renders S3 objects to a signed-in
   Foundry Initiative member (IMS `user_token` cookie at path `/asset`). Replaces the
   old `foundry-html-dev.corp.ethos851-stage-or2.ethos.adobe.net` URLs.

## Credential-broker call (from `/aws-creds` skill + `foundry_aws_creds.py`)

```
curl https://foundry-aws-dev-corp.adobe.io/iam/credentials/aws -H "x-pluto-token: <token>"
```

Returns JSON with `access_key_id`, `secret_access_key`, `session_token`, `region`
(default `us-west-2`), `expiration`.

## AWS gateway IAM plumbing (from `modeling/terraform/foundry-prd/aws_gateway/`)

- **`foundry-s3-gateway-service-iam-user`** — long-lived IAM user the gateway service
  authenticates as; its only permission is `sts:AssumeRole` on the client role.
- **`foundry-s3-gateway-client-iam-role`** — role the service assumes on behalf of a
  user. `max_session_duration = 43200` (12h). Trust policy: only the service user may
  assume it.
- **`foundry-s3-gateway-client-iam-policy`** — attached to the client role:
  - `s3:ListBucket`/`GetBucketLocation` etc. on `arn:aws:s3:::foundry-*` and
    `media-intelligence-*`.
  - Object-level `GetObject`, `PutObject`, multipart, tagging on `foundry-*/*` and
    `media-intelligence-*/*`. **No delete** actions (prevents data loss).
  - `kms:Decrypt`/`GenerateDataKey*`/`DescribeKey` scoped via
    `kms:ViaService = s3.us-west-2.amazonaws.com` (for KMS buckets, e.g. disney-wdi).
  - Cross-account **ASML L2** (Orion sandbox account `960266280454`) read-only access to
    `deccan-ai-*`, `abaka-video-*`, `adobe-l0-*`, `adobe-l2-*`, `half-space-video-*`,
    `nextdata-ai-*`, `treveo-video-dropbox` (list + GetObject only).
- Service docs: `docs.ai.corp.adobe.com/v3/services/services/firefly/foundry/apps/aws_gateway/README.html`.
- Client library docs: `docs.ai.corp.adobe.com/managed_services/services/firefly/foundry/libs/aws_gateway_client/README.html`.

## Mechanism summary (flow)

```
Laptop/notebook (IMS login)  ─┐
Pluto job (foundry_aws_gateway)├─► Foundry Auth Service (foundry-aws-corp.adobe.io)
/aws-creds machine token ─────┘        │ service IAM user calls sts:AssumeRole
                                       ▼
                          foundry-s3-gateway-client-iam-role (12h)
                                       │ scoped S3 (no-delete) + KMS + ASML-L2 read
                                       ▼
                         short-lived AWS creds → S3 foundry-* buckets (us-west-2)
```

For non-AWS providers the same auth service also vends Azure OpenAI (~1h), GCP/Gemini
(~1h), OpenAI (API key cached ~2h), and Bedrock/Anthropic session creds (~12h) through
`foundry_aws_gateway.llm.*`.
