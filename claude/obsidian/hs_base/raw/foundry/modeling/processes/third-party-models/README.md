# Third-Party Model Assets

Engineering process for Adobe third-party model source code, base weights, derived model artifacts, and access controls.

> [!IMPORTANT]
> PgM/legal approval policy remains the source of truth for whether a person or team may access a third-party model. This package documents the engineering controls that implement approved access.

> [!TIP]
> **Related docs:**
> | When you need... | See |
> |---|---|
> | Approval policy and access request form | [PgM/legal process](https://wiki.corp.adobe.com/x/gQpJ6Q) |
> | Storing weights for inference services | [Private bucket weights guide](https://docs.ai.corp.adobe.com/managed_services/services/firefly/foundry/aidoc/private-bucket-weights.html) |
> | Repo README/disclaimer template | [Repo Template](repo-template.md) |
>
> **Automation:** Open Claude Code from this folder and use the nested `third-party-models` skill to walk through the new-model and existing-model process steps, generate checklists, run read-only audits, and identify follow-up changes. The skill does not grant access or mutate external systems unless explicitly asked.

<!--TOC-->

- [1. Purpose](#1-purpose)
- [2. Current Inventory](#2-current-inventory)
  - [2.1 Test Fixtures](#21-test-fixtures)
- [3. User Process](#3-user-process)
  - [3.1 Onboard Team](#31-onboard-team)
  - [3.2 Request Individual Access](#32-request-individual-access)
  - [3.3 Access Weights](#33-access-weights)
  - [3.4 Offboard Access](#34-offboard-access)
- [4. Shared Conventions](#4-shared-conventions)
  - [4.1 Repo Pattern](#41-repo-pattern)
  - [4.2 Storage Rules](#42-storage-rules)
- [5. Admin Process](#5-admin-process)
  - [5.1 New Model / Repo Setup](#51-new-model--repo-setup)
    - [5.1.1 Confirm Approval](#511-confirm-approval)
    - [5.1.2 Create Access Group](#512-create-access-group)
    - [5.1.3 Create Restricted Repo](#513-create-restricted-repo)
    - [5.1.4 Create Storage](#514-create-storage)
    - [5.1.5 Wire Runtime Access](#515-wire-runtime-access)
    - [5.1.6 Update Documentation](#516-update-documentation)
  - [5.2 Existing Model / Repo Maintenance](#52-existing-model--repo-maintenance)
    - [5.2.1 Audit Existing Model](#521-audit-existing-model)
    - [5.2.2 Record Drift](#522-record-drift)
- [6. Policy Boundary](#6-policy-boundary)
- [7. Skill Usage](#7-skill-usage)

<!--TOC-->

---

## 1. Purpose

Adobe uses third-party model source code and weights for approved product-development work. These assets can have contractual and security constraints that are stricter than normal Foundry project assets.

This process explains how Foundry engineering administers the current engineering controls:

- model-specific access groups,
- restricted GitHub repos,
- private S3 buckets,
- Foundry auth gateway bucket access,
- Ethos private-bucket access for inference services,
- repo branch and README/disclaimer conventions,
- team onboarding and offboarding,
- drift audits.

## 2. Current Inventory

| Model | Repo | Bucket | Model Access Team | Policy Source | Status |
|---|---|---|---|---|---|
| Runway | [`Adobe-Firefly/rungen`](https://github.com/Adobe-Firefly/rungen) | `s3://foundry-runway-enterprise-adobe-assets` | [`3rdparty-model-access-runway`](https://github.com/orgs/Adobe-Firefly/teams/3rdparty-model-access-runway) | [PgM/legal process](https://wiki.corp.adobe.com/x/gQpJ6Q) | Active current example; repo normalization still needs audit |
| BFL/Werft (Flux 2 Flex) | [`Adobe-Firefly/werft`](https://github.com/Adobe-Firefly/werft) | `s3://foundry-bfl-werft-adobe-assets` | [`3rdparty-model-access-bfl-werft`](https://github.com/orgs/Adobe-Firefly/teams/3rdparty-model-access-bfl-werft) | [PgM/legal process](https://wiki.corp.adobe.com/x/gQpJ6Q) | Active |
| LTX-2 | [`Adobe-Firefly/LTX-2`](https://github.com/Adobe-Firefly/LTX-2) | Unknown | Unknown | Unknown | Restricted repo; do not remediate until confirmed |

### 2.1 Test Fixtures

| Fixture | Purpose | Status |
|---|---|---|
| `foundry-imaginary-corp-dev-adobe-assets` | Validates private-bucket support in development/test paths | Not real model inventory |
| `3rdparty-model-access-testing` | Validates model-specific GitHub-team-backed access | Not real model inventory |

## 3. User Process

Use this process when an approved Adobe team or individual needs third-party model access.

### 3.1 Onboard Team

1. Verify the team's access approval in the [PgM/legal process](https://wiki.corp.adobe.com/x/gQpJ6Q).
2. The process admin will set up the repo branch, ownership controls, and team-owned S3 prefix for you. Going forward, use `<team>` as the team's prefix in the model-specific bucket.

### 3.2 Request Individual Access

After a team is onboarded, approved individuals can be added to the model-specific group through [IAM access requests](https://iam.corp.adobe.com/access/request). Search for the model-specific group name, such as `3rdparty-model-access-runway`, and include the approval ticket or policy artifact in the request.

| Start the request | Submit the request |
|---|---|
| ![IAM access request page](https://github.com/user-attachments/assets/ecf2f9e2-1214-40fd-a73d-8177bfd4e724) | ![IAM access request details](https://github.com/user-attachments/assets/26ec7ee8-39ab-4334-9160-df6b5fafa356) |

### 3.3 Access Weights

Access is granted by the model-specific access group and bucket/gateway configuration. As long as a person or job is approved for the model and is in the right access group, the same model-specific bucket can be used for source-adjacent weights, base weights, derived weights, checkpoints, LoRA adapters, embeddings, distilled models, and fine-tuned variants.

For programmatic access, use the [`foundry_aws_gateway` client library](https://docs.ai.corp.adobe.com/managed_services/services/firefly/foundry/libs/aws_gateway_client/README.html). It vends short-lived, bucket-scoped credentials instead of requiring long-lived AWS keys.

```python
import foundry_aws_gateway

s3 = foundry_aws_gateway.maybe_s3_client("foundry-runway-enterprise-adobe-assets")
```

- **Pluto jobs:** access works out of the box when the job runs in an approved Adobe context and the user/team is in the right model access group. Do not add static `AWS_*` environment variables.
- **Laptops and notebooks:** install the client and run `foundry-aws-gateway login` once to authenticate through Adobe SSO; then `foundry_aws_gateway` calls use the cached login.
- **Browser credential access:** sign in at [foundry-aws-corp.adobe.io](https://foundry-aws-corp.adobe.io/) to get bucket-scoped credentials for approved buckets.
- **Browser asset viewing:** if an object has been uploaded to `s3://<bucket>/<key>`, authenticated users can view or download it at `https://foundry-aws-corp.adobe.io/asset/<bucket>/<key>`.

### 3.4 Offboard Access

Follow the [PgM/legal process](https://wiki.corp.adobe.com/x/gQpJ6Q) to request individual or project offboarding. Process admins handle IAM, GitHub, bucket, gateway, Terraform, and Ethos cleanup after the offboarding request is approved.

## 4. Shared Conventions

### 4.1 Repo Pattern

| Branch | Purpose | Controls |
|---|---|---|
| `disclaimer` | Default branch containing the process/disclaimer README | PR required; Foundry admin-controlled merge; squash only |
| `main` | Upstream vendor source code only | PR required; Foundry admin-controlled merge |
| `adobe/<team>` | Approved team's stable branch, for example `adobe/foundry` or `adobe/dva` | PR required; team owner review |
| `<user>/<work>` | User development branch, for example `hoshyari/test-harness` | Normal development branch; merge through PR |

Use GitHub repository rulesets as the first-choice mechanism. `adobe/*` covers one-segment team branches such as `adobe/team`; use per-team rulesets or CODEOWNERS only when a team needs stricter ownership.

### 4.2 Storage Rules

- Base vendor weights live only in the model-specific S3 bucket.
- Derived weights, checkpoints, LoRA adapters, embeddings, distilled models, and fine-tuned variants live in the same model-specific S3 bucket.
- Training jobs should write under team-scoped prefixes such as `<team_name>/<subpath>`.
- Inference services consume weights through the binary manager and private-bucket manifest flow documented in the Colligo [private bucket weights guide](https://docs.ai.corp.adobe.com/managed_services/services/firefly/foundry/aidoc/private-bucket-weights.html).
- Git repos must not contain model weights or other binary artifacts.

## 5. Admin Process

Use the admin process for creating model harnesses, maintaining existing repos and buckets, and recording drift.

### 5.1 New Model / Repo Setup

Use this process when Adobe starts using a new third-party model source repo, base-weight bucket, or derived-artifact bucket.

#### 5.1.1 Confirm Approval

1. Confirm the policy source, approval criteria, and offboarding contacts in the [PgM/legal process](https://wiki.corp.adobe.com/x/gQpJ6Q).
2. Confirm the requester has an approval ticket or equivalent policy artifact before changing IAM, GitHub, S3, gateway, or Ethos configuration.
3. Record the policy source in the [inventory](#2-current-inventory).

#### 5.1.2 Create Access Group

1. Create the IAM-backed GitHub group definition in [`OneAdobe/create-idp-teams`](https://github.com/OneAdobe/create-idp-teams).
2. Create the Adobe-Firefly GitHub team in the [`Adobe-Firefly` GitHub org](https://github.com/orgs/Adobe-Firefly/teams) with slug `3rdparty-model-access-<model>` (for example, [`3rdparty-model-access-runway`](https://github.com/orgs/Adobe-Firefly/teams/3rdparty-model-access-runway)).
3. Add approved named users through [IAM access requests](https://iam.corp.adobe.com/access/request), not by manual GitHub membership.

#### 5.1.3 Create Restricted Repo

1. Create or normalize the restricted repo under [`Adobe-Firefly`](https://github.com/Adobe-Firefly).
2. In the repo's GitHub settings, add [`foundry-github-admin`](https://github.com/orgs/Adobe-Firefly/teams/foundry-github-admin) as Admin.
3. In the repo's GitHub settings, add [`foundry-github-contributors`](https://github.com/orgs/Adobe-Firefly/teams/foundry-github-contributors) as the Foundry engineering access group.
4. In the repo's GitHub settings, add the model-specific team with the permission required for approved users.
5. Create the repo `disclaimer` branch from [Repo Template](repo-template.md) and set `disclaimer` as the default branch. Keep `main` as upstream vendor source code only; do not change vendor source docs for this README.
6. If the Adobe enterprise default-branch ruleset blocks the default-branch change, set the repo custom property `branch_protection_exception=true`, change the default branch to `disclaimer`, then restore the property unless the repo has an approved ongoing exception.
7. In the repo's GitHub rulesets, protect `disclaimer`, `main`, and `adobe/*`.

#### 5.1.4 Create Storage

1. Create the model-specific S3 bucket through Terraform under `modeling/terraform/foundry-prd/third_party_models/`.
2. Keep third-party model buckets in that child module so they remain visually separate from normal deal storage.
3. Keep base vendor weights, derived weights, checkpoints, LoRA adapters, embeddings, distilled models, and fine-tuned variants in that model-specific S3 bucket.
4. Use team-scoped prefixes such as `<team_name>/<subpath>` for training outputs.

#### 5.1.5 Wire Runtime Access

1. Wire bucket-scoped credentials in the Colligo managed services Foundry gateway deploy config using `third_party_model_access`: `services/firefly/foundry/deploys/aws_gateway/<env>/values.yaml` in the Colligo repo. Use `services/firefly/foundry/standalone_apps/aws_gateway/config.example.yaml` as the schema/example.
2. If Ethos inference services consume weights, add the bucket to private-bucket IAM in `modeling/terraform/foundry-prd/ethos/iam_user.tf`.
3. For V3 service implementation, use the Colligo [private bucket weights guide](https://docs.ai.corp.adobe.com/managed_services/services/firefly/foundry/aidoc/private-bucket-weights.html).

#### 5.1.6 Update Documentation

1. Update the [inventory](#2-current-inventory).
2. Update the restricted repo's `disclaimer` branch README from [Repo Template](repo-template.md).
3. Run the nested `third-party-models` skill from this folder to audit the new model state.

### 5.2 Existing Model / Repo Maintenance

Use this process for any model already in the [inventory](#2-current-inventory).

#### 5.2.1 Audit Existing Model

For each model, audit:

- repo exists and is private in [`Adobe-Firefly`](https://github.com/Adobe-Firefly),
- expected GitHub teams are attached in the repo's GitHub settings,
- model-specific team exists in the [`Adobe-Firefly` GitHub org](https://github.com/orgs/Adobe-Firefly/teams),
- approved named users are managed through [IAM access requests](https://iam.corp.adobe.com/access/request),
- bucket exists in Terraform under `modeling/terraform/foundry-prd/`,
- Colligo managed services gateway deploy config includes `third_party_model_access` in `services/firefly/foundry/deploys/aws_gateway/<env>/values.yaml`,
- Ethos private-bucket IAM in `modeling/terraform/foundry-prd/ethos/iam_user.tf` includes the bucket when needed,
- default branch is `disclaimer`, with `main` kept as upstream vendor source code only,
- `README.md`/`disclaimer` branch matches [Repo Template](repo-template.md),
- branch rulesets match the [repo pattern](#41-repo-pattern),
- `branch_protection_exception` is restored unless the repo has an approved ongoing exception,
- inventory row matches the observed state.

#### 5.2.2 Record Drift

1. Record observed drift as Jira follow-up work.
2. Update the [inventory](#2-current-inventory) only when the observed source of truth has changed.
3. Do not remediate LTX-2 until a human confirms it belongs under this process.

## 6. Policy Boundary

The PgM/legal process decides whether access is approved. Engineering must not grant access until the approval ticket/process is complete.

Engineering owns the implementation of approved access:

1. Create or verify the model-specific IAM-backed GitHub group.
2. Wire the group to the model source repo and S3 credential vending.
3. Keep source code in the restricted repo.
4. Keep base weights and derived artifacts in the model-specific S3 bucket.
5. Audit the repo, bucket, gateway, and documentation state for drift.

## 7. Skill Usage

Open Claude Code from this folder or point Claude at this folder, then ask for the third-party model skill. Use it while following [User Process](#3-user-process), [New Model / Repo Setup](#51-new-model--repo-setup), or [Existing Model / Repo Maintenance](#52-existing-model--repo-maintenance) to turn each section into an actionable checklist, run read-only repo/config audits, and summarize remaining manual or PR-based changes.

Supported workflows:

- user process,
- admin process / new model / repo setup,
- admin process / existing model / repo maintenance.
