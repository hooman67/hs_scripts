---
type: concept
title: Pluto storage (file system & S3)
tags: [adobe-infra, compute, pluto, storage, s3, filesystem]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/pluto-docs-extras]]"]
---

# Pluto storage (file system & S3)

Every [[wiki/entities/pluto|Pluto]] job sees four storage tiers with very different persistence guarantees — local SSD, per-job root disk, shared Sensei FS, and S3 — plus a logging FS. Knowing which survives a job stop is the difference between keeping and losing your work.

## Storage tiers

| Location | Purpose | Persistence | Speed |
|---|---|---|---|
| `/mnt/localssd` | Training datasets, model files | **Only until job terminates** | Fastest |
| `/home/colligo` (root/EBS) | Conda envs, code, executables | Lost on termination **unless snapshotted** | Medium |
| `/sensei-fs-3` (a.k.a. `/sensei-fs`) | Shared training data, collaboration | Indefinite | Slower |
| S3 | Checkpoints, dataset/model backups | Indefinite | Slower |
| `/logging-fs` | Job/platform logs only | Ephemeral (auto-deleted) | — |

## Local SSD (`/mnt/localssd`)

Fastest tier, sized per core: CPU x86_64 **25 GB**, A100_40GB / A100_80GB **530 GB**, H100_80GB **478 GB**.

> [!warning] Not backed up
> "Files saved to local SSD are _not_ backed up and do not persist after a job is terminated." Back up to the root filesystem or S3, then save a [[wiki/concepts/pluto-job-lifecycle#snapshots|snapshot]].

## Root file system (`/home/colligo`, EBS)

Per-job, non-shared home directory. Files persist only if you **pause** (which snapshots) or explicitly **save a snapshot** before terminating — nothing is auto-backed-up on termination. Do **not** clone the colligo repo here; use `/mnt/localssd` or GitHub code distribution in training jobs instead.

## Sensei FS (`/sensei-fs-3`, FSx for Lustre)

Shared, collaboration-oriented store. Default quota **500 GB**, automatically replicated to S3. Files not accessed for 7 days are evicted (metadata retained; re-fetch takes seconds). Layout: private `<FS_ROOT>/users/your_username`, team `<FS_ROOT>/tenants` (needs tenant membership + LDAP group). Access: join the Sensei tenant (contact admin) and the corresponding LDAP group via the Adobe IAM portal.

Best practices: keep files here only while actively using them (cost); avoid many small files (tar/zip them); don't store Conda envs, executables, or checkpoints here; share via the tenant directory, not your personal one.

## S3 data access

Pluto brokers S3 access via an IAM **role-based** model across dev/stage/prod — no manual bucket-policy edits.

> [!warning] Region constraint
> S3 buckets must be in **`us-west-2`** only. Other regions are "much slower and more expensive, because data is sent over the open internet."

- **Credentials (interactive/CLI):** use the Adobe **KLAM** tool — select project → environment (dev/sandbox/stage) → generate temporary creds → paste into `~/.aws/credentials` under `[default]`.
- **Register a bucket:** copy its ARN (`arn:aws:s3:::bucket-name`) from the AWS console Properties tab → register as an External **Resource** in Pluto.
- **Access model:** a **Resource** = an external data source; a **Role** = access level (Read-only / Read-write / Admin). Project admins request role access; role owners approve. Per job: Resource Access Roles → select roles → confirm levels. Jobs then **inherit** access from their project's roles — no in-job credentials needed.

## Related
- [[wiki/entities/pluto]]
- [[wiki/concepts/pluto-job-lifecycle]]
- [[wiki/concepts/pluto-secrets]]
- [[wiki/concepts/pluto-resource-hierarchy]]
- [[wiki/sources/pluto-docs-extras]]
