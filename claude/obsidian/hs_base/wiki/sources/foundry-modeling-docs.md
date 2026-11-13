---
type: source
title: Foundry modeling docs
tags: [foundry, modeling, source, terraform, third-party-models]
created: 2026-07-05
updated: 2026-07-05
raw: "[[raw/foundry/modeling/README.md]]"
sources: ["[[raw/foundry/modeling/README.md]]", "[[raw/foundry/modeling/AGENTS.md]]", "[[raw/foundry/modeling/terraform/README.md]]", "[[raw/foundry/modeling/processes/third-party-models/README.md]]", "[[raw/foundry/docs/training.md]]"]
---

# Foundry modeling docs

Distilled summary of the `modeling/` documentation set (branch `main`, commit `a2c807d4b`, ingested 2026-07-05):

- `modeling/README.md` + `AGENTS.md` — scope: shared modeling infra not in Colligo/Genie; three sub-areas (compute, processes, terraform).
- `modeling/terraform/README.md` — the isolated-root Terraform layout, cloud accounts (AWS prd/stg, Azure, GCP, frozen sensei-asml), the per-customer S3 storage model + bucket naming, admin-apply / no-CI policy. → [[wiki/concepts/foundry-terraform]].
- `modeling/processes/third-party-models/README.md` — the 3P model access-control process (groups, restricted repos, private buckets, gateway/Ethos wiring, inventory). → [[wiki/concepts/foundry-third-party-models]].
- `docs/training.md` — training work-area overview (code lives in Colligo `foundation_exploration`; "analysis over training"; no scale training without a validated PR).

## Related
- [[wiki/concepts/foundry-modeling]]
- [[wiki/concepts/foundry-terraform]]
- [[wiki/concepts/foundry-third-party-models]]
- [[raw/foundry/_provenance]]
