---
type: concept
title: Foundry modeling
tags: [foundry, modeling, infrastructure, compute, terraform, process]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/foundry/modeling/README.md]]", "[[raw/foundry/modeling/AGENTS.md]]", "[[raw/foundry/docs/training.md]]"]
---

# Foundry modeling

`modeling/` is Foundry's home for **shared model-building, training, and serving infrastructure that has no dedicated place elsewhere** (i.e. not in Colligo or Genie). It explicitly does **not** contain the training code itself — that lives in Colligo's `foundation_exploration` and Genie's Glimmer. `modeling/` holds only the *supporting* infrastructure and operational tooling.

## Three sub-areas

| Sub-area | What it is | Wiki page |
|---|---|---|
| `compute/` | Tooling for GPU-job visibility and allocation enforcement on [[wiki/entities/pluto|Pluto]]: **job_agent** (MCP + dashboard) and **job_police** (automated enforcer). | [[wiki/concepts/foundry-compute]] |
| `processes/` | Operational process *packages* (docs + templates + local Claude skills) that are more than a reference doc but don't belong in Colligo/Genie. Currently: `third-party-models/`. | [[wiki/concepts/foundry-third-party-models]] |
| `terraform/` | AWS/Azure/GCP infrastructure-as-code — S3 storage for customer/modeling data, IAM, cloud gateways. | [[wiki/concepts/foundry-terraform]] |

## Where training / data actually live (related repos)

| Repo | What's there |
|---|---|
| `colligo/contrib/Mori/collections/foundation_exploration` | Training code — model configs (`configs/<basemodel>/`, `configs/foundry/<customer>/`), training scripts, `morictl` launcher. Runs the [[wiki/entities/mori|Mori]] framework. |
| `genie/glimmer/modules/foundry` | Glimmer data-processing pipelines for Foundry. |

Training principles (from `docs/training.md`): **"analysis over training"** (diagnosing model behavior matters more than more training) and **no training at scale without a validated PR** (debug run, charts, validation loop, eval sets required first). Jobs are launched with `morictl` (Foundry's training launcher), the Pluto `aip` CLI, or the Pluto UI — always under the Foundry Initiative (GAI-415).

## Related
- [[wiki/entities/foundry]]
- [[wiki/concepts/foundry-compute]]
- [[wiki/concepts/foundry-terraform]]
- [[wiki/concepts/foundry-third-party-models]]
- [[wiki/entities/pluto]] · [[wiki/entities/colligo]] · [[wiki/entities/mori]] · [[wiki/entities/genie]]
- [[wiki/sources/foundry-modeling-docs]]
