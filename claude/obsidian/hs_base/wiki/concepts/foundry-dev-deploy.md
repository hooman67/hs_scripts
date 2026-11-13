---
type: concept
title: Deploying a Foundry standalone app to dev
tags: [foundry, deployment, argocd, ethos, buildkit, artifactory, gitops, v3]
created: 2026-09-14
updated: 2026-09-14
sources: ["[[raw/thd-seedance-video-pipeline-learnings-2026-09]]"]
---

# Deploying a Foundry standalone app to dev

End-to-end dev deploy of a Foundry standalone app (e.g. [[wiki/entities/thd-video|THD Video]]), with the
environment gotchas we actually hit. Captured as the **`/dev_deploy`** Claude Code skill; complements
[[wiki/concepts/v3-deployment|the V3 Bazel→ArgoCD→Ethos deploy machinery]] and
[[wiki/concepts/foundry-dev-workflow|the Foundry dev workflow]].

## The flow
1. Make the code/config change and **commit it** (`make image` refuses a dirty tree; the image identity
   is the git sha).
2. `smake lint` (from `managed_services/`) — formats, regenerates BUILD/lock, and (`argo-sync`)
   regenerates `cloud/`.
3. `make image` (in the app dir) — builds + pushes the ECR image; copy the printed tag
   `…colligo-dev:fdry-<app>-<sha>-inf<fw>-b<docker>.rc`.
4. Bump the `image:` line in `deploys/<app>/dev/values.inference.yaml` to the new tag.
5. `smake lint` again — regenerates `cloud/<env>/<app>-<cluster>/` with the tag embedded.
6. Commit **only your app's files** — the values change AND the regenerated
   `cloud/dev/<app>-<cluster>/{debug.yaml,templates/k8s_manifest.yaml}`. Nothing stray.
7. PR to `main` (JIRA prefix, fill the template), get review, merge.

## GitOps: it's two hops, not instant
merge to `main` → GH Action **`sync-argocd-mirror`** pushes `managed_services/cloud/` to the
**`colligo-v3-deploy`** mirror repo → **ArgoCD watches the mirror, not colligo** → syncs to the cluster.
So: confirm the mirror got your commit, then in ArgoCD (`argocd.ethos.corp.adobe.com`, needs
`GRP-FIREFLY-READONLY`) **Refresh** to skip the poll; **Sync** only if it's stuck `OutOfSync`. The real
"it's live" check: the `http_server` pod rolled to your new image tag. Runtime skills:
`/foundry-watch-deploy`, `/foundry-ethos`.

## One-time environment prereqs (Pluto box)
- **Artifactory read for `docker-colligo-release`** (needed by `smake` argo-sync's chart download): IAM
  group **`GRP-NEURAL-FILTERS-DEV`** (bundled in the Colligo Developer role; self-serve sync at
  devhome.corp.adobe.com/artifacts → Sync Groups → Cloud). Put YOUR identity token (from
  `artifactory-uw2.adobeitc.com` → Edit Profile → Generate Identity Token) in `~/.netrc` for
  `artifacts.adobeitc.com`. Symptom of missing perm: chart download 401/404 while `api/system/ping` is
  200. See [[wiki/concepts/foundry-aws-access]].
- **buildkit for `make image`** (rootless `buildkitd` behind the `pluto-builder` buildx builder). If
  `no builder "pluto-builder" found` / socket missing: the s6 buildkit service **parked at boot because
  `newuidmap` (the `uidmap` package) was missing** (check `/opt/job-logs/system/buildkit/current`). Fix:
  `sudo apt-get update && sudo apt-get install -y uidmap`, then restart the supervised service
  `sudo /opt/cis/command/s6-svc -d /opt/cis/scandir/buildkit && sudo … -u …`; socket appears at
  `/mnt/localssd/.buildkit/buildkit.sock`. It's **daemonless** (buildx pushes straight to ECR), so
  `dockerd` being down doesn't matter.

## Troubleshooting playbook
- **`smake` argo-sync fails on ANOTHER app's chart** (e.g. an ephemeral `0.dev…` pin that's been GC'd):
  not your fault — the global argo-sync builds every deploy. Ping that owner, or temporarily neutralize
  that chart pin, `smake lint`, then `git checkout` the other app's changes so only yours remain.
- **CI "generated files up to date" fails** → you didn't commit the regenerated `cloud/`. Re-run
  `smake lint`, add the `cloud/dev/<app>-<cluster>/` diff, commit.
- **Doc CI `toc.not_included` SphinxError** → a markdown file under an `aidoc/` folder isn't in a
  toctree. Add `orphan: true` topmatter (the repo convention for non-nav design docs).
- **`make image` "dirty tree"** → commit first. **`Makefile` "missing separator"** → check for stray
  `git stash`/merge conflict markers.

## Dev-specific behaviour to know
- `default_method` is `remove` (paint-out), not SAM3 `anonymize` — no request field selects it; set it
  in the dev values to change. `pickMotionVideo` is gated by `allow_motion_video_debug` (False in dev) →
  request 403; motion bank attaches as a grid.

## Related
- [[wiki/entities/thd-video]] · [[wiki/concepts/foundry-standalone-app-pipeline]]
- [[wiki/concepts/v3-deployment]] · [[wiki/concepts/foundry-dev-workflow]]
- [[wiki/concepts/foundry-aws-access]] · [[wiki/concepts/pluto-docker-images]]
- [[wiki/concepts/foundry-local-debugging]] — running it locally instead
