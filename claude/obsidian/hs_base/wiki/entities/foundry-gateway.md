---
type: entity
title: Foundry Gateway (Foundry Auth Service)
tags: [foundry, gateway, auth, ims, aws, s3, access-control]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/foundry-gateway/gateway-docs.md]]", "[[raw/foundry-gateway/skills/aws-creds.md]]", "[[raw/foundry/docs/project-setup-and-access.md]]"]
---

# Foundry Gateway (Foundry Auth Service)

**`foundry-aws-corp.adobe.io`** is the [[wiki/entities/foundry|Foundry]] team's single **access gateway** — the **Foundry Auth Service** that vends short-lived, scoped credentials so developers and jobs can reach AWS/S3, cloud LLM endpoints, and view S3-hosted assets, without holding long-lived keys.

It exists to solve one problem: Foundry engineers need **more than read-only** access (they write to S3, call LLM APIs) but admin-level access is too broad. The gateway hands out **12-hour, write-scoped** credentials for exactly what developers need. See the full flow in [[wiki/concepts/foundry-aws-access]].

## What it fronts

The one hostname exposes (at least) three surfaces:

| Surface | Path | What it does |
|---|---|---|
| **Developer credentials UI** | `/` | "Get Foundry Developer Credentials" button → 12h AWS creds (key/secret/session) for all `foundry-*` buckets. |
| **AWS credential broker** | `/iam/credentials/aws` | `GET` with header `x-pluto-token: <token>` → JSON creds. The machine path behind [[wiki/concepts/foundry-gateway-skills|/aws-creds]]. Dev host: `foundry-aws-dev-corp.adobe.io`. |
| **HTML / asset serving** | `/asset/<bucket>/<key>` | Renders S3 objects to a signed-in Foundry Initiative member (IMS `user_token` cookie at path `/asset`). Replaces old `foundry-html-dev...ethos.adobe.net` URLs. |

Beyond AWS, the same auth service also vends **Azure OpenAI**, **GCP/Gemini**, **OpenAI (direct)**, and **AWS Bedrock/Anthropic** credentials, consumed through the `foundry_aws_gateway` client library (`foundry_aws_gateway.llm.*`).

## Auth model (summary)

- **Identity = IMS.** Interactive users sign in with Adobe SSO (IMS); the browser gallery flow sets a `user_token` cookie for `/asset`. Programmatic callers use the `foundry_aws_gateway` client (one-time `foundry-aws-gateway login`) or a **Pluto machine token** on the broker endpoint.
- **Gating = Foundry Initiative / GAI-415 membership** plus the `Foundry-Developer` IAM tier. [[wiki/entities/pluto|Pluto]] jobs under the Foundry Initiative get credentials injected out-of-the-box.
- **Vending = STS AssumeRole.** A long-lived service IAM user assumes a **12h, no-delete, S3-scoped** client role and returns the temporary creds. IAM plumbing lives in [[wiki/concepts/foundry-terraform|modeling/terraform]] (`foundry-prd/aws_gateway/`).
- **Distinct from gen-foundry inference auth.** The gateway vends *resource* creds (S3/LLM). Calling a Foundry *model endpoint* (`gen-foundry.ff.adobe.io`) is a separate two-layer allowlist — see [[wiki/concepts/foundry-aws-access#gen-foundry-endpoint-auth]].

## Related
- [[wiki/concepts/foundry-aws-access]] — the credential/access model in detail
- [[wiki/concepts/foundry-gateway-skills]] — Hooman's skills that use this gateway
- [[wiki/entities/foundry]] · [[wiki/entities/pluto]]
- [[wiki/concepts/foundry-terraform]] — the `aws_gateway` IAM plumbing
- [[wiki/concepts/foundry-third-party-models]] — 3P buckets add extra controls on top
- [[wiki/concepts/foundry-endpoint-email-allowlist]] — the *customer* gateway (endpoint email allowlist) — a different gateway
- [[wiki/sources/foundry-gateway-ingest]]
