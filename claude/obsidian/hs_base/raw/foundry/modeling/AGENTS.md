# Agent Guidelines - Modeling

**Applicable for all files within `modeling/`.**

See root `AGENTS.md` for repo-wide conventions.

---

## Overview

Infrastructure and tooling for shared model training and serving — the parts that don't have a dedicated home in Colligo or Genie.

> **Note:** The actual training code (foundation_exploration) and Glimmer live in the `colligo` and `genie` repos respectively. This folder holds only the supporting infrastructure in the foundry repo.

## What Lives Here

- `compute/job_agent/` — MCP server + browser dashboard for Foundry GPU job visibility and management. See `compute/job_agent/CLAUDE.md` for details.
- `processes/` — modeling-related operational process packages with templates and local skills. Use this for process/tooling bundles that are more than a live reference doc but do not belong in Colligo or Genie.
- `terraform/` — AWS S3 storage for modeling workloads (customer data buckets, dropbox buckets). See `terraform/AGENTS.md` for details.

## Related Repos

| Repo | What Is There |
|---|---|
| `colligo/contrib/Mori/collections/foundation_exploration` | Training code (model configs, training scripts) |
| `genie/glimmer/modules/foundry` | Glimmer data processing pipelines for foundry |

See `docs/training.md`, `docs/data-processing.md`, and `docs/compute-jobs.md` for overview docs.
