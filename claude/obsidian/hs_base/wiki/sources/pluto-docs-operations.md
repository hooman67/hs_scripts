---
type: source
title: "Pluto documentation — operational sub-pages"
raw: "[[raw/pluto-docs-operations]]"
created: 2026-07-04
updated: 2026-07-04
ingested: 2026-07-04
tags: [adobe-infra, compute, pluto]
sources: ["[[raw/pluto-docs-operations]]"]
---

# Pluto documentation — operational sub-pages

The operational sub-pages of the official [[wiki/entities/pluto|Pluto]] docs (job lifecycle, submit flows, editing, projects, scheduler, clusters, CLI/SDK, compute capacity) — beyond the index/concepts pages covered by [[wiki/sources/pluto-docs]]. Source: [[raw/pluto-docs-operations]] (base `https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/`).

## Pages ingested

`getting-started.html` · `jobs.html` · `editing-a-job.html` · `projects.html` · `clusters.html` · `scheduler.html` · `cli-using.html` · `cli.html` · `cli-jobs.html` · `python-sdk.html` · `compute-cap.html`.

## Key claims

- **Two job types:** *Interactive Session* (VS Code / Bash, persists until stopped) and *Training Job* (batch, ends when scripts exit). See [[wiki/concepts/pluto-job-lifecycle]].
- **Job states:** Draft → Pending → Starting → Queued → Running → Running Unstable → Failed / Succeeded → Stopping → Stopped. Terminal jobs archived after ~2 weeks.
- **Submit flow:** Jobs page → *+ Create Job*; interactive = Create & Start, training = Create (Draft) then edit + Start. Scripts are Bash; init-script failure blocks all later scripts; SIGTERM handling ≤30 s for preemption.
- **Snapshots** capture `/home/colligo` (exclude `/mnt/localssd` + GitHub code); ~1.5–2 s/GB save, ~2–3 s/GB restore.
- **Editing:** name/tags/notifications/roles editable live; scheduling/content/runtime/auto-recovery need the job stopped; job type/status/project are fixed forever. See [[wiki/concepts/pluto-console]].
- **Projects:** admin ops (create/edit/members/delete), quota view & transfer ("immediately once you click Confirm Transfer"), resource-access roles. Capacity is set by initiative admins via quarterly prioritization — "The AI Platform support team cannot get you any additional capacity."
- **Scheduler:** strict P0>P1>P2 priority; P2 randomized + re-checked ~every second; P0 never preempted; project-based quota by default, initiative-based opt-in.
- **Clusters:** SRE-only; EKS node groups (homogeneous; a job runs on one node group); node cordoning; docs marked "MORE DETAILS TBD".
- **CLI/SDK:** `aip` CLI (`adobe-aip-cli`) and async `adobe-aip-sdk`, both via UW2 Artifactory; full `aip job ...` command set. See [[wiki/concepts/pluto-cli-sdk]].

## Notes
- Condensed/paraphrased from rendered HTML via WebFetch, not byte-verbatim; quoted strings are reproduced as-is. Fetched 2026-07-04.
- Priority-tier wording matches the docs' guaranteed/reclaimable/spare semantics; the label mismatch across docs/skill/MCP is already flagged in [[wiki/concepts/allocation-priority-tiers]].

## Related
- [[wiki/entities/pluto]]
- [[wiki/sources/pluto-docs]]
- [[wiki/sources/pluto-skill]]
- [[wiki/concepts/pluto-job-lifecycle]]
- [[wiki/concepts/pluto-console]]
- [[wiki/concepts/pluto-cli-sdk]]
