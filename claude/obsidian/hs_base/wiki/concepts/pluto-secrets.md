---
type: concept
title: Pluto secrets
tags: [adobe-infra, compute, pluto, secrets, vault, security]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/pluto-docs-extras]]"]
---

# Pluto secrets

[[wiki/entities/pluto|Pluto]] secrets are backed by Adobe's **HashiCorp Vault** and injected into jobs as **environment variables only** — never stored on disk.

## Scopes

| Scope | Who can see it | Where it lives |
|---|---|---|
| **User** | Just you | Managed via Avatar → User Profile → "Available Secrets" |
| **Project** | Project team | `dme_colligo/services/pluto/projects/<team-or-project-folder>` in Vault; access via an IAM group |
| **Role** | Multiple projects (org-level) | Vault |

## Creating secrets

- **User (self-service):** User Profile > Secrets Available → Edit → **+ Add New Entry** → simple string key-value pair (no nested objects) → Save. Requires enabling "Enable secret management" in the **Debug Panel**.
- **Project (requires setup):** create an IAM group → create a folder in Vault's project directory → file a Jira ticket asking **SRE** to associate the IAM group with the folder → SREs whitelist the path.

## Injecting into jobs

Job details → **Execution Specs** → Edit → **+ Expose New Secret** → choose Source (User/Project/Role), Path, Key, and target Environment Variable name → Save. The secret is then available as an env var in **init and main scripts**. To convert Vault's CLI path format: remove `-mount=`, strip quotes, replace spaces with `/`.

> [!warning] Never persist secrets
> "Never store secrets in persistent file systems, including Sensei FS, S3, or root file system." "Never hard-code secrets in job code." Use Vault exclusively.

## Related
- [[wiki/entities/pluto]]
- [[wiki/concepts/pluto-storage]]
- [[wiki/concepts/pluto-job-lifecycle]]
- [[wiki/sources/pluto-docs-extras]]
