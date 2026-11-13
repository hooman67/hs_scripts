# Modeling Terraform

Terraform infrastructure for Foundry's cloud resources. Each subdirectory is an isolated Terraform root with its own S3 backend state.

```sh
# This is where we use to deploy our real things we need. Connected to foundry-prd
# account.
foundry-prd/
  aws_gateway/   # IAM role + user for the credential-vending gateway service
  ethos/         # IAM user for ethos pod access to private S3 buckets

# Azure resources for the AZR14080 account. Foundry uses Azure for OpenAI / GPT
# endpoints — model evals, prompt rewriting, and other LLM-as-judge workflows.
azure/

# GCP resources for the GCP-0805 account. Foundry uses GCP for Gemini via
# Vertex AI — same use cases as Azure (evals, prompt rewriting) but with
# Google models.
gcp/

adhoc/
  # Individual terraform module for an adhoc resource for unforseen usecases.
  # Ideally there should be only a few of these.
  <timestamp>-<use-case>/

# This is for foundry stage account. We don't really use this for anything meaninful.
# Use this for testing terraform and AWS interactions only. Do not make a resource
# here that you need to actually use else-where.
foundry-stg/

# historically NBCU buckets live here. This is froze, we don't add anything new
# here.
asml-stage/
```

## 1. Prerequisites

For background on Foundry's cloud accounts, access tiers, and credential vending, see [Cloud Resources and Access Management](../../docs/project-setup-and-access.md).

**Only admins can run `terraform apply`.** Most developers are in the **Foundry-Developer** (readonly) group and do not have write access to the cloud accounts. If you need a Terraform change applied, submit a PR and ask an admin to review and apply it. See [project-setup-and-access.md §3.1](../../docs/project-setup-and-access.md#31-access-groups) for the admin groups.

> We are in progress of fixing auth so only a few people have admin, and others can just use readonly to do the plan part only. [FFP-77156](https://jira.corp.adobe.com/browse/FFP-77156).

### 1.1 AWS

| AWS Account | CAMP / Alias | IDP Role | `~/.aws/credentials` Profile |
|---|---|---|---|
| foundry-prd (324037283113) | | `AWS_AWS3570_PRD_ADMINISTRATOR` | `foundry-prd` |
| foundry-stg (457335975320) | | `AWS_AWS3651_STG_ADMINISTRATOR` | `foundry-stg` |
| asml-stage (760168217311) | SenseiDataTreasureChest / AWS1521 | `AWS_AWS1521_STG_ADMINISTRATOR` | `sensei-asml-admin` (see [sensei-asml/README.md](sensei-asml/README.md)) |

### 1.2 Azure

| Account | CAMP Name | Subscription ID |
|---|---|---|
| Foundry | `AZR14080` | `250ff47a-2418-4e1b-aaa2-65d28dcba127` |

**Auth:** Log in with your Adobe LDAP account via the Azure CLI:

```bash
brew install azure-cli   # one-time
az login                 # opens browser, sign in with Adobe SSO
```

You must be a member of `AZURE-DME-FOUNDRY-STG-ADMIN` (see [project-setup-and-access.md §3.1](../../docs/project-setup-and-access.md#31-access-groups)).

### 1.3 GCP

| Account | CAMP Name |
|---|---|
| `gcp-ml-platform-poc` | `adbe-gcp0805` |

**Auth:** Log in with your Adobe LDAP account via the gcloud CLI:

```bash
brew install google-cloud-sdk                # one-time
gcloud auth login                            # opens browser, sign in with Adobe SSO
gcloud auth application-default login        # separate credential used by Terraform
```

You must be a member of `GRP-GCP-0805-ADMIN` (see [project-setup-and-access.md §3.1](../../docs/project-setup-and-access.md#31-access-groups)).

## 3. When to Do What

### 3.1 Add Storage for a New Company/Franchise

This is the most common task.

1. **Edit** `foundry-prd/storage.tf` — add a new `module "<company>_storage"` block following the template of existing entries.
2. Run `terraform plan -target=module.<company>_storage` to verify.
3. Send a PR. An admin (@hoshyari_adobe for now) will review, `apply`, and merge.

#### Bucket Naming Conventions

| Bucket Type | Pattern | Example (company=`psky`, franchise=`enterprise`) |
|-------------|---------|--------------------------------------------------|
| Dropbox | `foundry-dropbox-<company>-<franchise>` | `foundry-dropbox-psky-enterprise` |
| Adobe Assets | `foundry-<company>-<franchise>-adobe-assets` | `foundry-psky-enterprise-adobe-assets` |

#### Data Flow Notes

- **Adobe-asset buckets** are for internal use by Adobe only. Only create them in `us-west-2`. Some older companies have a `us-east-2` bucket — this was temporary when we had a cluster there; new modules should not create it (set `asset_storage_regions = ["us-west-2"]` only).
- **Dropbox buckets** are the interface with the customer. We do not create IAM users for customers. Instead, ask the customer to provide their IAM role ARN and use `dropbox_custom_role_permissions` to allow-list it with specific S3 permissions. The customer assumes their own role to access the bucket directly — no credentials are exchanged.
- **Pulling data from a company** (no dropbox bucket involved): Ask the company to allow-list our role on their bucket. We can create ad-hoc roles for this — see [`adhoc/2025-12-humain-data-exploration/`](adhoc/2025-12-humain-data-exploration/) for an example.

**There is no CI that runs Terraform.** An admin reviews the PR, runs `apply`, and then merges.

> **⚠️ WARNING: Follow these guidelines. Making ad-hoc AWS changes without committing Terraform code, or creating resources outside the documented patterns, causes confusion, drift, overhead, and wastes time for everyone.**

> **Do NOT make changes in AWS (console or CLI) without a corresponding Terraform commit.** All infrastructure must be code-managed.

For any out-of-convention need, please first contact @ebrodsky or @hoshyari. Depending on the need we can create ad-hoc resources in the [`adhoc/`](adhoc/) folder — but do not go ahead and do it before discussing.

### 3.2 Add a One-Off (Adhoc) Resource

For resources that don't fit the standard company-storage pipeline (e.g. a temporary IAM role, a bucket for a specific experiment):

1. Create a new folder under `adhoc/<year>-<month>-<use-case>/`.
2. Add `providers.tf` with a **unique** S3 backend key (`terraform/adhoc/<use-case>/terraform.tfstate`).
3. Add your resource definitions in `main.tf` (or split as needed).
4. `terraform init` → `terraform plan` to verify.
5. Send a PR. An admin will review, `apply`, and merge.

Each adhoc folder is completely isolated — it has its own state and does not share state with any other root.

### 3.3 Modify Existing Resources

1. Edit the `.tf` files in the appropriate root (`foundry-prd/`, `foundry-stg/`, `sensei-asml/`, or `adhoc/<use-case>/`).
2. Run `terraform plan` to verify.
3. Send a PR. An admin will review, `apply`, and merge.

### 3.4 Modify `sensei-asml` Resources

**This root is frozen.** Only drift fixes and migration work are allowed. See [sensei-asml/README.md](sensei-asml/README.md) for credentials and run guidance.

## 4. Running Terraform

### 4.1 AWS Roots

```sh
# One-time init (per root)
cd modeling/terraform/<root>
AWS_PROFILE=<profile> terraform init

# Verify your changes
AWS_PROFILE=<profile> terraform plan

# To plan only a specific module (avoids touching other resources)
AWS_PROFILE=<profile> terraform plan -target=module.<company_slug>_storage
```

| Root | `AWS_PROFILE` |
|---|---|
| `foundry-prd/` | `foundry-prd` |
| `adhoc/*` | `foundry-prd` |
| `foundry-stg/` | `foundry-stg` |
| `sensei-asml/` | `sensei-asml-admin` |

### 4.2 Azure

```sh
cd modeling/terraform/azure
az login
terraform init
terraform plan
terraform apply
```

> **State:** Azure Blob Storage (`foundryplatformtf` storage account, `tfstate` container, versioning enabled).

### 4.3 GCP

```sh
cd modeling/terraform/gcp
gcloud auth application-default login
terraform init
terraform plan
terraform apply
```

> **State:** GCS (`foundry-platform-tf` bucket, versioning enabled, public access enforced off).

**There is no CI that runs Terraform.** An admin reviews the PR, runs `apply`, and then merges.

## 5. Linting

```sh
# From modeling/terraform/
make lint   # check formatting
make fix    # auto-format
```

## 6. Modules

- **[company-storage](modules/company-storage/)** — Creates a company-level Pluto IAM user and invokes `franchise-storage` for each franchise.
- **[franchise-storage](modules/franchise-storage/)** — Creates per-franchise S3 buckets (dropbox + adobe-assets) and IAM users.

> **Tech debt:** Having both a per-company and per-franchise module is unnecessary — we don't actually need the per-franchise granularity. For now, always use `company-storage` with a single franchise. Do not use `franchise-storage` directly or create multiple franchises per company. We will consolidate this eventually.
