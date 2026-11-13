---
name: reference_github_thd_proj
description: How to access the private Adobe-Firefly/THD_Proj GitHub repo (rewriter code) — SSH key location
metadata: 
  node_type: memory
  type: reference
  originSessionId: d24f6783-62e3-43e4-9386-81e8e1cd0c68
  modified: 2026-08-29T07:00:34.714Z
---

The team's video-rewriter production code lives in the **private** GitHub repo
`github.com/Adobe-Firefly/THD_Proj` (the rewriter is the `videogen/` package; PR 145 = "sentence→
script→video on GPT-5.6 Terra + Seedance 2.5"). `gh` is NOT installed and there's no GitHub token in
credentials — API returns 404 unauthenticated.

**Access via Hooman's SSH key:** `/sensei-fs/users/hshariati/doc_dont-delete/id_ed25519` authenticates
to github.com as `hshariati_adobe`. Perms on the file are 0644, so copy it somewhere and `chmod 600`
first, then:
`GIT_SSH_COMMAND="ssh -i <key> -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new" git clone git@github.com:Adobe-Firefly/THD_Proj.git`
(fetch a PR: `git fetch origin pull/145/head:pr145`). Related: [[project_thd_video_rewriter]].
