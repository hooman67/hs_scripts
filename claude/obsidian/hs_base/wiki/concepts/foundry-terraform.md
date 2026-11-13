---
type: concept
title: Foundry Terraform infrastructure
tags: [foundry, terraform, infrastructure, aws, azure, gcp, s3, iam]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/foundry/modeling/terraform/README.md]]", "[[raw/foundry/docs/project-setup-and-access.md]]"]
---

# Foundry Terraform infrastructure

`modeling/terraform/` is the Terraform for Foundry's cloud resources. **Each subdirectory is an isolated Terraform root** with its own remote state backend. The bulk of it provisions **per-customer S3 storage**; the rest is IAM, cloud gateways, and legacy cleanup. Lint via `make lint` / `make fix` (`terraform fmt`). **There is no CI** — only **admins** (Foundry-Developer-Admin) can `terraform apply`; developers submit a PR and an admin reviews, applies, then merges.

## The roots

| Root | Cloud / account | What it provisions |
|---|---|---|
| `foundry-prd/` | AWS `foundry-prd` (324037283113) | The real production infra. Per-customer **storage** (`storage.tf`), the **aws_gateway** IAM role/user for the credential-vending gateway service, **ethos** IAM user for Ethos pod access to private buckets, and **third_party_models** (child module for 3P model buckets). |
| `foundry-stg/` | AWS `foundry-stg` (457335975320) | Stage account — "we don't use this for anything meaningful." For testing Terraform/AWS interactions only. |
| `azure/` | Azure `AZR14080` | `cloud_gateway` — Azure OpenAI / GPT access (evals, prompt rewriting, LLM-as-judge). State in Azure Blob (`foundryplatformtf`). |
| `gcp/` | GCP `GCP-0805` (`gcp-ml-platform-poc`) | `cloud_gateway` — Gemini via Vertex AI (same eval/rewrite use cases). State in GCS (`foundry-platform-tf`). |
| `adhoc/<year>-<month>-<use-case>/` | usually `foundry-prd` | One-off resources that don't fit the standard storage pipeline — each fully isolated with its own state. Examples in-repo: humain-appen, humain-data-exploration, tccc-sftp, tccc-image-api, thd-image-api, tesco-sftp, foundry-orchestrator-dev. |
| `sensei-asml/` (asml-stage) | AWS `asml-stage` (760168217311, CAMP SenseiDataTreasureChest / AWS1521) | **FROZEN.** Legacy NBCU dropbox/adobe-assets buckets + IAM. Retirement target 2026-Q3; only drift fixes / migration allowed. Uses a dedicated IAM user `aws-sensei-asml-tf-admin` (creds in Vault). |

## Storage model — the common task

The most common change is **adding storage for a new customer/deal** by adding a `module "<company>_storage"` block in `foundry-prd/storage.tf` using the shared **`company-storage`** module.

Each new deal = **one company, one franchise**, with two buckets (us-west-2 only):

| Bucket type | Pattern | Example |
|---|---|---|
| **Dropbox** (customer interface) | `foundry-dropbox-<company>-<franchise>` | `foundry-dropbox-thd-enterprise` |
| **Adobe Assets** (internal only) | `foundry-<company>-<franchise>-adobe-assets` | `foundry-thd-enterprise-adobe-assets` |

Key rules:
- **Dropbox buckets** are the customer boundary — Foundry does **not** create IAM users for customers; instead the customer supplies their IAM role ARN, which is allow-listed via `dropbox_custom_role_permissions`. The customer assumes their own role; no credentials are exchanged.
- **Adobe-assets buckets** are internal, `us-west-2` only. Old `us-east-2` buckets (e.g. THD, from a short-lived training cluster) are **legacy — do not use**.
- Some early deals (Disney) have multiple franchises (`wdi`, `mickey-mouse`); the deal squad owns which is active. New deals: single franchise only.
- **Tech debt:** there are both `company-storage` and `franchise-storage` modules; per-franchise granularity is unnecessary — always use `company-storage` with a single franchise.

There is a matching **`/new-customer-storage` skill** that automates provisioning this Terraform for a new customer.

## Cloud accounts & auth (summary)

- **AWS:** IDP roles → `~/.aws/credentials` profiles (`foundry-prd`, `foundry-stg`, `sensei-asml-admin`).
- **Azure:** `az login` (Adobe SSO); membership in `AZURE-DME-FOUNDRY-STG-ADMIN`.
- **GCP:** `gcloud auth login` + `gcloud auth application-default login`; membership in `GRP-GCP-0805-ADMIN`.

> The `aws_gateway`/`ethos` IAM plumbing here backs the **Foundry Auth Service** (`foundry-aws-corp.adobe.io`) that vends short-lived scoped credentials — that gateway itself is documented separately.

## Related
- [[wiki/concepts/foundry-modeling]]
- [[wiki/entities/foundry]]
- [[wiki/concepts/foundry-third-party-models]] — 3P model buckets live in the `third_party_models` child module
- [[wiki/entities/pluto]] · [[wiki/concepts/pluto-storage]]
- [[wiki/sources/foundry-modeling-docs]]
