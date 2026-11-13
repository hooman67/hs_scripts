---
type: source
title: "Source: Pluto docs — extras (storage/secrets/docker/jupyter/policy/troubleshooting)"
tags: [adobe-infra, compute, pluto, source, docs]
created: 2026-07-04
updated: 2026-07-04
raw: "[[raw/pluto-docs-extras]]"
ingested: 2026-07-04
sources: ["[[raw/pluto-docs-extras]]"]
---

# Source: Pluto docs — extras

Ten operational pages from the Pluto aidoc site (`docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/`), fetched 2026-07-04, covering storage, secrets, Docker, Jupyter, policies, and troubleshooting. Full capture in [[raw/pluto-docs-extras]].

## Pages ingested (all succeeded, no 404s)

| Page | Distilled into |
|---|---|
| `file-system.html` | [[wiki/concepts/pluto-storage]] |
| `s3-access.html` | [[wiki/concepts/pluto-storage]] |
| `secrets.html` | [[wiki/concepts/pluto-secrets]] |
| `docker.html` | [[wiki/concepts/pluto-docker-images]] |
| `using-docker.html` | [[wiki/concepts/pluto-docker-images]] |
| `jupyter-user-guide.html` | [[wiki/concepts/pluto-jupyter]] |
| `troubleshooting.html` | [[wiki/concepts/pluto-troubleshooting]] |
| `policy/global-config.html` | [[wiki/concepts/pluto-policy]] |
| `policy/project-init-policy.html` | [[wiki/concepts/pluto-policy]] |
| `blogs/snapshot_announcement.html` | folded into [[wiki/concepts/pluto-job-lifecycle#snapshots]] |

## Key takeaways

- **Four storage tiers, different persistence:** local SSD (dies with job), root `/home/colligo` (needs snapshot), Sensei FS (indefinite, 500 GB, S3-replicated), and S3 (indefinite). See [[wiki/concepts/pluto-storage]].
- **S3 must be in us-west-2**, accessed via IAM Roles/Resources that jobs inherit from their project.
- **Secrets** live in HashiCorp Vault (user/project/role scopes), inject as env vars only — never persisted to disk.
- **Docker:** certified base-image allowlist; custom builds via build-image workflow; and Docker-in-Containerd (DinC) to build/run containers inside a running job.
- **Policies:** low-GPU-utilization, quota-overuse (with automatic preemption), and two-week archival; initiatives/projects can only tighten, never loosen.

## Nav pages noted but not yet ingested
`logs.html`, `ssh.html`, `preflight-checks.html`, `custom-job-telemetry.html`, `scheduler.html`, `network-access.html`, `support.html`, `cli-using.html`, `python-sdk.html`.

## Related
- [[wiki/entities/pluto]]
- [[wiki/concepts/pluto-storage]]
- [[wiki/concepts/pluto-secrets]]
- [[wiki/concepts/pluto-docker-images]]
- [[wiki/concepts/pluto-jupyter]]
- [[wiki/concepts/pluto-troubleshooting]]
- [[wiki/concepts/pluto-policy]]
- [[wiki/sources/pluto-docs]]
- [[wiki/sources/pluto-docs-operations]]
- [[raw/pluto-docs-extras]]
