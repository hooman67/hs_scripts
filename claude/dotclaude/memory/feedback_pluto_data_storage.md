---
name: feedback_pluto_data_storage
description: Keep bulk data off home-backed source checkouts on every Pluto project.
metadata:
  type: feedback
---

Hooman's explicit policy: **"All my Pluto projects: code in home, bulk data in /mnt/localssd".**

- Keep source and Git metadata under `/home/colligo`.
- Store datasets, media, generated outputs, raw traces, dependency environments and caches
  under `/mnt/localssd`, not physically inside `colligo` or `hs_scripts`.
- Small prompts, schemas and provenance manifests may stay with the source.
- For cleanup, copy and verify before removing originals; leave symlinks for compatible old
  paths. Skip data and environments currently used by running jobs.
- `/mnt/localssd` is volatile. Preserve irreplaceable work in remote storage, not a second bulk
  copy under home.

This supersedes earlier practices of keeping large experiment evidence in the home checkout.
