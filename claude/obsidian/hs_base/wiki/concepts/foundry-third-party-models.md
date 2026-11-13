---
type: concept
title: Foundry third-party models process
tags: [foundry, modeling, process, third-party-models, access-control, security]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/foundry/modeling/processes/third-party-models/README.md]]", "[[raw/foundry/docs/third-party-models.md]]"]
---

# Foundry third-party models process

`modeling/processes/third-party-models/` is the **engineering process** for handling Adobe's approved use of **third-party (3P) model source code and weights** (Runway, Black Forest Labs Flux, LTX-2, etc.). These assets carry contractual and security constraints stricter than normal Foundry project data, so access is tightly controlled.

**Policy boundary:** PgM/legal decide *whether* access is approved (via a separate wiki/Jira process). This package only implements the **engineering controls** for approved access — it never grants access itself.

## The engineering controls (five layers)

1. **Model-specific IAM-backed GitHub access group** — slug `3rdparty-model-access-<model>` (e.g. `3rdparty-model-access-runway`). Members added only through IAM access requests, never manual GitHub membership.
2. **Restricted GitHub repo** under `Adobe-Firefly` — vendor source only. Uses a specific branch pattern:
   - `disclaimer` (default branch, holds the process/disclaimer README from a template)
   - `main` (upstream vendor source only)
   - `adobe/<team>` (approved team's stable branch)
   - `<user>/<work>` (dev branches)
3. **Private S3 bucket** (model-specific) — created via Terraform under `modeling/terraform/foundry-prd/third_party_models/` (kept in that child module so 3P buckets stay visually separate from normal deal storage). Holds base vendor weights **and** all derived artifacts (checkpoints, LoRA adapters, embeddings, distilled/fine-tuned variants). Git repos must never contain weights.
4. **Foundry AWS gateway bucket access** — programmatic access via the `foundry_aws_gateway` client library (vends short-lived, bucket-scoped creds). Gateway deploy config wired in Colligo managed_services (`services/firefly/foundry/deploys/aws_gateway/<env>/values.yaml`, key `third_party_model_access`). Pluto jobs get access out-of-the-box when the user/team is in the right group.
5. **Ethos private-bucket access** — for inference services that consume the weights; IAM added in `modeling/terraform/foundry-prd/ethos/iam_user.tf`.

## Inventory (as of ingest)

| Model | Repo | Bucket | Status |
|---|---|---|---|
| Runway | `Adobe-Firefly/rungen` | `foundry-runway-enterprise-adobe-assets` | Active (repo normalization pending) |
| BFL/Werft (Flux 2 Flex) | `Adobe-Firefly/werft` | `foundry-bfl-werft-adobe-assets` | Active |
| LTX-2 | `Adobe-Firefly/LTX-2` | Unknown | Restricted; do NOT remediate until confirmed |

Test fixtures (`foundry-imaginary-corp-dev-adobe-assets`, `3rdparty-model-access-testing`) are **not** real inventory.

## Automation

A **nested Claude skill** (`.claude/skills/third-party-models/SKILL.md`, topic-local — open Claude from that folder) turns each process section (user onboarding, new-model/repo setup, existing-model audit) into a checklist and runs **read-only** audits. It does not grant access or mutate systems unless explicitly asked.

## Related
- [[wiki/concepts/foundry-modeling]]
- [[wiki/concepts/foundry-terraform]] — where the 3P buckets are provisioned
- [[wiki/entities/foundry]]
- [[wiki/entities/flux]] — BFL Flux is one of the 3P models
- [[wiki/sources/foundry-modeling-docs]]
