---
type: concept
title: Foundry gateway / AWS-access skills
tags: [foundry, gateway, skills, slash-commands, aws, s3, tooling]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/foundry-gateway/skills/aws-creds.md]]", "[[raw/foundry-gateway/skills/generate-from-endpoint.md]]", "[[raw/foundry-gateway/skills/render-s3-gallery.md]]", "[[raw/foundry-gateway/skills/eval_hub_upload.md]]", "[[raw/foundry-gateway/skills/html-to-appen-csv-for-humain.md]]", "[[raw/foundry-gateway/skills/vendor-generate.md]]", "[[raw/foundry-gateway/skills/gcp-gemini.md]]"]
---

# Foundry gateway / AWS-access skills

Catalog of Hooman's Claude slash-command skills that touch the [[wiki/entities/foundry-gateway|Foundry gateway]] / Foundry buckets. Nearly all follow the same pattern: **get short-lived creds → read/write `foundry-*` S3 → publish an asset viewable at `foundry-aws-corp.adobe.io/asset/...`**. Backing scripts live in `~/.claude/scripts/` (PEP 723 `uv run --script`). See the access mechanism in [[wiki/concepts/foundry-aws-access]].

## The credential foundation

| Skill | What it does / how it uses the gateway |
|---|---|
| **`/aws-creds`** | The core. Exchanges the permanent [[wiki/entities/pluto|Pluto]] machine token for 12h AWS creds via the broker (`GET /iam/credentials/aws`, header `x-pluto-token`). Writes `~/.claude/hshariati/aws_creds.env` (600) to `source` before any `aws`/S3 call. Re-run on `ExpiredToken`. Script: `foundry_aws_creds.py`. |

> [!NOTE]
> The older skills below still expect creds in **`~/Downloads/creds.txt`** (exported from the gateway "Get Foundry Developer Credentials" UI); newer ones use `/aws-creds` → `aws_creds.env`. Same underlying gateway, two credential file conventions.

## Generation + publishing

| Skill | What it does / how it uses the gateway |
|---|---|
| **`/generate-from-endpoint`** | Runs a customer's **gen-foundry** generate endpoint over a prompt set (IMS bearer token at `/tmp/auth_token.txt`), uploads images to `s3://<customer-bucket>/hs_results/...`, and builds a 5-file **IMS-auth gallery** (`imsauth.js`) viewable at `foundry-aws-corp.adobe.io/asset/.../gallery/index.html`. Script: `generate_from_endpoint/runner.py`. |
| **`/render-s3-gallery`** | Builds an HTML gallery over an existing S3 prefix, uploaded to `<prefix>/gallery/`. Assets use **relative paths** (no presigned URLs); `imsauth.js` sets the IMS `user_token` cookie at `/asset` so the gateway authorizes image requests for signed-in Foundry Initiative members. |
| **`/vendor-generate`** | Submits each row of a Foundry viz HTML to the Deccan Media Studio API. Reads the source from S3, **presigns** it (vendor can't read `foundry-aws-corp` URLs), writes outputs back to `foundry-*` S3, and emits a new viz HTML at a `foundry-aws-corp.adobe.io/asset/...` URL. |
| **`/html-to-appen-csv-for-humain`** | Turns a viz HTML into an Appen/Humain annotation CSV, copying referenced assets into `s3://foundry-appen-humain-enterprise/to_annotate/...` and writing `annotations.csv`. Pure S3-to-S3 via gateway creds. |

## Eval / LLM

| Skill | What it does / how it uses the gateway |
|---|---|
| **`/eval_hub_upload`** | Uploads a generation (prompts + images) to the Adobe Evaluation Hub. Reads source images from `foundry-*` S3 using `/aws-creds` creds (`source aws_creds.env`, `--creds /dev/null`); the Eval Hub upload itself uses its own API key. Returns a run ID + asset-viewer URL. |
| **`/gcp-gemini`** | Ad-hoc Gemini calls on Vertex AI (Foundry `GCP-0805`) with a short-lived bearer token. The lightweight twin of the official `foundry_aws_gateway.llm.get_google_genai()` path — **no** machine-token broker (unlike `/aws-creds`); refresh via `gcloud auth print-access-token`. Internal use only per access §2.6. |

## Related
- [[wiki/entities/foundry-gateway]] — the gateway these skills target
- [[wiki/concepts/foundry-aws-access]] — the credential/access model
- [[wiki/entities/pluto]] — source of the machine token
- [[wiki/sources/foundry-gateway-ingest]] — source summary
- [[wiki/entities/foundry]]
