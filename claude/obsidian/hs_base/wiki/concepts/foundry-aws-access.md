---
type: concept
title: Foundry AWS / cloud access model
tags: [foundry, aws, s3, ims, sts, credentials, access-control, security]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/foundry/docs/project-setup-and-access.md]]", "[[raw/foundry-gateway/gateway-docs.md]]", "[[raw/foundry-gateway/skills/aws-creds.md]]", "[[raw/foundry/docs/gen-foundry-auth-allowlisting.md]]"]
---

# Foundry AWS / cloud access model

How the [[wiki/entities/foundry|Foundry]] team gets **short-lived, scoped** access to AWS/S3 and cloud LLM endpoints through the [[wiki/entities/foundry-gateway|Foundry Auth Service]] (`foundry-aws-corp.adobe.io`) — instead of long-lived keys. Goal: **near-zero long-lived credentials**.

## Access tiers (IAM umbrella groups)

- **Foundry-Developer** — all engineers. Read-only on the cloud accounts + write access for S3/Gemini/OpenAI *via the gateway*. Also mirrors into the `foundry-github-contributors` GitHub team.
- **Foundry-Developer-Admin** — capped ~6 (Hooman Shariati, Shayan Hoshyari, Marian Petre, Eugene Brodsky). Full account access; only admins can `terraform apply`.

Getting access = (1) subscribe to Colligo Developer, (2) join `Foundry-Developer` on iam.corp.adobe.com, (3) be added to a **Foundry project** (Foundry Initiative on Pluto, GAI-415 / `d54f60e2-...`). Project membership decides which data you can touch.

## How credentials work

The **Foundry Auth Service** vends credentials **scoped to exactly the write operations developers need**, with **12-hour expiry**. Consumed from two contexts:

1. **Interactive** (laptop/notebook) — the `/` UI ("Get Foundry Developer Credentials") or `foundry_aws_gateway` after a one-time `foundry-aws-gateway login` (Adobe SSO).
2. **Long-running Pluto jobs** — `foundry_aws_gateway` works **out of the box** for jobs under the Foundry Initiative; no login or env vars.

> [!IMPORTANT]
> Recommended programmatic path is the `foundry_aws_gateway` client library (handles vending + refresh, works with boto3 and s5cmd) — **do not use boto3 directly**, and do **not** hard-set `AWS_*` in job env. The library is **not** available in Ethos pods (they use Vault secrets instead).

## The credential-broker / machine-token flow (the `/aws-creds` path)

Hooman's [[wiki/concepts/foundry-gateway-skills|/aws-creds]] skill uses a **permanent [[wiki/entities/pluto|Pluto]] machine token** to hit the broker directly — no interactive IMS sign-in:

1. **Token** resolved (order): `--token` → `PLUTO_TOKEN` env → `credentials.yaml` (`foundry_aws.pluto_token`) → `~/Downloads/creds.txt`. The current token is long-lived (expires 2026-11-27).
2. **Broker call**: `GET https://foundry-aws-dev-corp.adobe.io/iam/credentials/aws` with header `x-pluto-token: <token>`.
3. **Response**: JSON `{access_key_id, secret_access_key, session_token, region, expiration}` (region defaults `us-west-2`).
4. **Env file**: written to `~/.claude/hshariati/aws_creds.env` (mode 600) as `export AWS_*` lines; must be `source`d in the **same** shell command as the `aws` call (env doesn't persist across Bash tool calls).
5. **Refresh**: broker creds are short-lived (~24h in practice); on `ExpiredToken`/`AccessDenied`, re-run the script and re-source. This differs from GCP/Azure ad-hoc paths, which have **no** machine-token broker.

## What the vended AWS creds can do (STS + IAM, from Terraform)

The gateway service does **`sts:AssumeRole`** on a scoped client role. IAM lives in [[wiki/concepts/foundry-terraform|modeling/terraform/foundry-prd/aws_gateway/]]:

- **`foundry-s3-gateway-service-iam-user`** — long-lived service identity; only permission is `sts:AssumeRole` on the client role.
- **`foundry-s3-gateway-client-iam-role`** — assumed on the user's behalf; **`max_session_duration = 43200` (12h)**; trust policy allows only the service user.
- **`foundry-s3-gateway-client-iam-policy`** grants:
  - List/get/**put**/multipart/tagging on `arn:aws:s3:::foundry-*` and `media-intelligence-*` (bucket + object). **No `s3:Delete*`** — deliberately, to prevent data loss.
  - `kms:Decrypt`/`GenerateDataKey*`/`DescribeKey` scoped to `kms:ViaService = s3.us-west-2.amazonaws.com` (for KMS-encrypted buckets, e.g. disney-wdi).
  - **Cross-account ASML L2** (Orion sandbox `960266280454`) **read-only**: `deccan-ai-*`, `abaka-video-*`, `adobe-l0-*`, `adobe-l2-*`, `half-space-video-*`, `nextdata-ai-*`, `treveo-video-dropbox`. Same `foundry_aws_gateway` flow, no extra setup; `foundry-aws-gateway >= 1.2.0`.

Everything is **`us-west-2`**. Old `us-east-2` buckets are legacy — do not use.

## Bucket model: dropbox vs adobe-assets

Per deal (see [[wiki/concepts/foundry-terraform#storage-model]]): a **dropbox** bucket (`foundry-dropbox-<company>-<franchise>`) is the customer boundary (customer assumes their *own* IAM role — Foundry never issues customer keys), and an internal **adobe-assets** bucket (`foundry-<company>-<franchise>-adobe-assets`). The gateway's `foundry-*` wildcard covers both. [[wiki/concepts/foundry-third-party-models|Third-party model buckets]] add repo/access-group/artifact controls on top.

## Other providers via the same auth service

Through `foundry_aws_gateway.llm.*` (all `pip install foundry-aws-gateway[llm]`, **internal use only**, not for production Ethos services):

| Provider | Client call | Token lifetime |
|---|---|---|
| Azure OpenAI (`AZR14080`) | `get_azure_openai()` | ~1h, auto-refresh |
| OpenAI direct (`foundry-data-prd`) | `get_openai()` | API key cached ~2h |
| GCP/Gemini (`GCP-0805`, Vertex AI) | `get_google_genai()` | ~1h, auto-refresh; default `us-west1` |
| AWS Bedrock / Anthropic | `get_bedrock_anthropic()` | ~12h session creds |

Auth-service SP/SA credentials live in Vault under `dme_colligo/services/foundry/cloud-gateway/*`.

## Ethos services (not the gateway)

Ethos-deployed services can't use `foundry_aws_gateway`; they read **Vault secrets** (`dme_colligo/services/foundry/ethos/*`: azure_key, openai_platform_key, s3_private_buckets, bedrock) and use dedicated **IMS clients** (`foundry-services` for service-to-service, `foundry-web`, `foundry-inference-ui`, `colligo-developer`).

## Gen-foundry endpoint auth

Calling a Foundry **model endpoint** (`gen-foundry.ff.adobe.io`) is a *separate* mechanism from resource-credential vending — two independent allowlist layers:

1. **Layer 1 — Colligo Gateway (CGW):** checks the IMS `x-gw-ims-client-id` against `ingress.allowed_client_ids` (prod: `colligo_testing`, `clio-playground-web`, `firefly-service-testing`, `foundry-web`; dev = wildcard).
2. **Layer 2 — per-model allowlist:** the app checks user_id/org_id/email against each model's `foundry_model_authorization_config`. Internal `adobe.com` org passes automatically; external partners need a dedicated **IMS tech account** added to `allowlisted_user_ids` + `allowlisted_emails`.

Note: gen-foundry is **not** `firefly-api.adobe.io` — different service, different auth; Firefly Services creds do not work on gen-foundry. Skills like [[wiki/concepts/foundry-gateway-skills|/generate-from-endpoint]] call these endpoints with an IMS bearer token. For the **token lifecycle** (why the 24h endpoint token is testing-only, and the UI refresh-token / backend S2S paths), see [[wiki/concepts/foundry-inference-auth-tokens]].

## Related
- [[wiki/entities/foundry-gateway]] — the gateway hub
- [[wiki/concepts/foundry-gateway-skills]] — the skills that exercise this model
- [[wiki/entities/pluto]] — the machine token comes from Pluto
- [[wiki/concepts/foundry-terraform]] — where the IAM/STS plumbing is provisioned
- [[wiki/concepts/foundry-third-party-models]] — stricter controls for 3P buckets
- [[wiki/entities/foundry]]
