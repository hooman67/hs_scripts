---
type: source
title: Foundry gateway — skills & access docs (source)
tags: [foundry, gateway, source, skills, access]
created: 2026-07-05
updated: 2026-07-05
raw: "[[raw/foundry-gateway/_provenance.md]]"
sources: ["[[raw/foundry-gateway/_provenance.md]]", "[[raw/foundry-gateway/gateway-docs.md]]"]
---

# Foundry gateway — skills & access docs (source)

Distilled summary of the sources ingested for the [[wiki/entities/foundry-gateway|Foundry gateway]] ingest (2026-07-05). Full provenance and auth-blocked notes: [[raw/foundry-gateway/_provenance.md]].

## What was ingested

- **7 access-related skills** (`raw/foundry-gateway/skills/`): `aws-creds`, `generate-from-endpoint`, `render-s3-gallery`, `eval_hub_upload`, `html-to-appen-csv-for-humain`, `vendor-generate`, `gcp-gemini` — plus their backing scripts read from `~/.claude/scripts/`. Cataloged in [[wiki/concepts/foundry-gateway-skills]].
- **Foundry repo docs** (read-only): `docs/project-setup-and-access.md` (the canonical access doc) and `docs/gen-foundry-auth-allowlisting.md` (two-layer endpoint auth).
- **Terraform**: `modeling/terraform/foundry-prd/aws_gateway/` — the STS/IAM plumbing behind the gateway (service user → assume 12h no-delete S3 client role).
- **Gateway fetch**: `WebFetch https://foundry-aws-corp.adobe.io/` — see fetch note below.

## Key facts distilled

- `foundry-aws-corp.adobe.io` = the **Foundry Auth Service**, one hostname fronting: developer-credential UI (`/`), AWS broker (`/iam/credentials/aws`, `x-pluto-token`), and asset serving (`/asset/<bucket>/<key>`).
- Credentials are **12h, S3-scoped, no-delete**, `us-west-2`, vended via `sts:AssumeRole`.
- `/aws-creds` uses a **permanent Pluto machine token** (broker path, no IMS sign-in); other skills use the `~/Downloads/creds.txt` UI export.
- Non-AWS providers (Azure OpenAI, Gemini, OpenAI, Bedrock) go through `foundry_aws_gateway.llm.*` off the same auth service.
- gen-foundry model endpoints (`gen-foundry.ff.adobe.io`) use a **separate** two-layer allowlist, not the credential broker.

## Gateway fetch note

`WebFetch` of the gateway root returned an **unverified** summary (no hard auth error) that mirrors the local docs; it was NOT treated as authoritative because the endpoint is IMS-authenticated. Verbatim capture in [[raw/foundry-gateway/gateway-docs.md]]. The signed-in UI and `credential-vending-service.md` (referenced but absent locally) remain uncovered.

## Related
- [[wiki/entities/foundry-gateway]]
- [[wiki/concepts/foundry-aws-access]]
- [[wiki/concepts/foundry-gateway-skills]]
- [[wiki/entities/foundry]] · [[wiki/entities/pluto]]
