Deploy a Foundry standalone app (e.g. `thd_video`) to its **dev** Ethos environment, end to end — build the image, bump the deploy config, regenerate manifests, open/merge the PR, and verify the rollout in ArgoCD. Includes a troubleshooting playbook for the environment problems we've actually hit (Artifactory perms, buildkit, generated-file drift, Doc CI, GitOps lag).

Usage: /dev_deploy [app=thd_video]

This skill is a living runbook. When you solve a new deploy problem, **add it to the Troubleshooting playbook below** so it compounds over time.

---

## 0. Context / mental model

- Apps live in `managed_services/services/firefly/foundry/standalone_apps/<app>/`; deploy config in `managed_services/services/firefly/foundry/deploys/<app>/{dev,prerelease}/values.inference.yaml`.
- The Docker **image is built outside Bazel** (`make image` in the app dir) and pushed to ECR. The deploy config just pins the tag (`image:` line, usually L9 of `dev/values.inference.yaml`).
- **GitOps, two hops:** merge to `main` → GH Action `sync-argocd-mirror` pushes `managed_services/cloud/` to the **`colligo-v3-deploy`** mirror repo → **ArgoCD watches the mirror (not colligo)** → syncs to the cluster. Deploys are therefore NOT instant.
- The rendered manifests under `cloud/<env>/<app>-<cluster>/` are **generated** by `smake lint` (`argo-sync`) and MUST be committed in sync with the values change, or CI's "generated files up to date" check fails.

## 1. One-time environment prerequisites (Pluto box)

Do these once per box; they're the usual first-time blockers.

**A. Artifactory read for `docker-colligo-release`** (needed by `smake lint`'s `argo-sync` to download the helm chart):
- You need IAM group `GRP-NEURAL-FILTERS-DEV` (bundled in the `Colligo Developer` role). If missing: request `Firefly - Colligo Developer` in the IAM portal, then self-serve sync at <https://devhome.corp.adobe.com/artifacts> → **Sync Groups** → env `Cloud` → group `GRP-NEURAL-FILTERS-DEV`.
- Put YOUR identity token in `~/.netrc`. Generate at `https://artifactory-uw2.adobeitc.com` (SAML SSO → Welcome → Edit Profile → **Generate an Identity Token**). Then:
  ```
  machine artifacts.adobeitc.com
      login <your-ldap>
      password <identity-token>
  ```
  Remove any junk lines (we've seen a malformed `machine XDG_CACHE_HOME` block). Verify:
  ```
  curl -s -o /dev/null -w "%{http_code}\n" --netrc \
    "https://artifacts.adobeitc.com/artifactory/docker-colligo-release/firefly/v3/inference-chart/<ver>/inference-chart-linux.zip"
  ```
  200 = good. 401/404 on the repo while `api/system/ping` returns 200 = your account lacks `docker-colligo-release` read → fix the group sync, and note whose creds the netrc actually uses (shared boxes sometimes carry someone else's login).

**B. Docker buildkit for `make image`** (rootless `buildkitd` behind the `pluto-builder` buildx builder). If `make image` says `no builder "pluto-builder" found` or the buildkit socket is missing:
- Root cause we hit: buildkit's s6 service **parked at boot** because `newuidmap` (the `uidmap` package) wasn't installed. Check `/opt/job-logs/system/buildkit/current`.
- Fix (sudo is passwordless on your own box):
  ```
  sudo apt-get update && sudo apt-get install -y uidmap          # installs newuidmap/newgidmap
  sudo /opt/cis/command/s6-svc -d /opt/cis/scandir/buildkit       # restart the supervised service
  sudo /opt/cis/command/s6-svc -u /opt/cis/scandir/buildkit
  until [ -S /mnt/localssd/.buildkit/buildkit.sock ]; do sleep 2; tail -n1 /opt/job-logs/system/buildkit/current; done
  ```
  The remote buildx builder is created automatically once the socket exists; if not: `docker buildx create --name pluto-builder --driver remote --use unix:///mnt/localssd/.buildkit/buildkit.sock`. NOTE: this is **daemonless** (buildx pushes straight to ECR), so `dockerd` being down does NOT matter. After `uidmap` is installed, the s6 service also comes up correctly on future reboots.

## 2. The happy path (per change)

Run from `managed_services/services/firefly/foundry/standalone_apps/<app>/` unless noted.

1. **Make your code/config change and commit it.** `make image` refuses a dirty tree, and the image identity is the git sha — so commit first (a "wip"/"lint happy" commit is fine; you'll be on a feature branch off `main`).
2. **`smake lint`** (from `managed_services/`) — formats, regenerates BUILD/lock, and (step 7 `argo-sync`) regenerates `cloud/`. Must be green. (If it dies on an UNRELATED app's chart download, see Troubleshooting → "argo-sync fails on another app".)
3. **`make image`** — builds + pushes the ECR image. Copy the final tag it prints: `...colligo-dev:fdry-<app>-<sha>-inf<fw>-b<docker>.rc`.
4. **Bump the image tag** in `deploys/<app>/dev/values.inference.yaml` (`image:` line):
   ```
   sed -i -E 's|(image: ".*colligo-dev:)[^"]*"|\1<NEW_TAG>"|' \
     services/firefly/foundry/deploys/<app>/dev/values.inference.yaml
   ```
5. **`smake lint` again** — regenerates `cloud/<env>/<app>-<cluster>/` with the new tag embedded.
6. **Commit ONLY this app's files** — the values change AND the regenerated `cloud/dev/<app>-<cluster>/{debug.yaml,templates/k8s_manifest.yaml}`. `git show --stat HEAD` should show nothing stray (no other app's cloud/). Push.
7. **Open/merge the PR to `main`** (JIRA prefix in title; fill the PR template). CI runs `bazel test //...` (includes the generated-files check) + Doc CI. Get review; merge.
8. **Verify the rollout** — see §3.

## 3. Verify the rollout

- Confirm the mirror updated: the `sync-argocd-mirror` GH Action succeeded on your merge commit (colligo repo → Actions), or `colligo-v3-deploy` shows your new tag under `cloud/dev/<app>-<cluster>/`.
- ArgoCD `https://argocd.ethos.corp.adobe.com` → app `<app>-<cluster>` (e.g. `foundry-thd-video-ethos851-dev-or2`). **Refresh** to skip the poll; **Sync** only if stuck `OutOfSync`.
- The real check: the `http_server` deployment's pod is running your new image tag, Healthy, no crashloop.
- Runtime skills: `/foundry-watch-deploy` (drive/watch the Ethos pipeline after merge), `/foundry-ethos` (Argo sync/health, pods, smoke).

## 4. Test the app

- **Local (best; no auth, exercises your code against real fal/SAM3/rewriter):** `make run` (serves :8000 with dev config) then `make smoke HOST=http://127.0.0.1:8000 IMAGE=scripts/smoke/fixtures/paintout_before.jpg` (variants: `smoke-rewrite`, `smoke-motion-bank`, `smoke-video-ref`). The smoke script sends no auth, so it's local-only.
- **Deployed dev endpoint:** requires IMS auth + `x-api-key`; the Foundry Customer Gateway / Studio handles the handshake. Endpoints: upload `POST /v2/storage/image` → `POST /v2/video/generate` (envelope body) → poll `links.result.href`. Developer (ethos-direct) host: `https://<app>-dev.ethos851-stage-or2.ethos.adobe.net`.
- **thd_video-specific dev gotchas:** `default_method` is `"remove"` not `anonymize` (no request field to change it); `pickMotionVideo` returns 403 unless `allow_motion_video_debug: true`. To make the deployed app match in-process evals, set both in the dev values.

---

## Troubleshooting playbook (grow this)

**`smake lint` argo-sync fails downloading a chart (`k8s_py_chart_download` / 404 / 401).**
- If it's on **another** app (e.g. `vllm_serve/prerelease` pinning an ephemeral `0.dev…` chart that's been GC'd): it's a pre-existing broken pin on `main`, not you. Options: (a) ping that app's owner to repin; (b) to regen just YOUR app's manifests, temporarily point the offending `k8s_remote_python_chart` back to `@platforms_inference//:ai-inference-chart`, run `smake lint`, then `git checkout -- <that app's deploy + cloud paths>` so only your app's diff remains.
- If it's YOUR app / all charts 401: Artifactory perms — see §1.A.

**`make image` → `no builder "pluto-builder" found` / buildkit socket missing.** See §1.B (install `uidmap`, restart the s6 buildkit service).

**`make image` → "tree dirty".** Commit first (§2.1).

**CI "generated files up to date" fails.** You didn't commit the regenerated `cloud/…` after bumping the image/values. Run `smake lint`, `git add` the `cloud/dev/<app>-<cluster>/` diff, commit, push.

**Doc CI fails (`toc.not_included` SphinxError).** A markdown file under any `aidoc/` folder isn't in a toctree. Add `orphan: true` topmatter (matches the repo convention for non-nav design docs) rather than deleting it. Files NOT under `aidoc/` and not `README.md` are ignored by Sphinx.

**Deploy merged but nothing changed in the cluster.** GitOps lag / mirror not updated. Confirm the `sync-argocd-mirror` Action ran on your commit and `colligo-v3-deploy` has the new manifest, THEN Refresh in Argo. Argo watches the mirror, not colligo.

**SAM3 anonymize / edge auth.** Use the **ethos-direct** host `https://<svc>-dev.ethos851-stage-or2.ethos.adobe.net` with `x-api-key = foundry-services` (ims client_id). The `.private.adobe.io` edge would reject that key. Reference impl: `naou_image/sam3_client.py` (which uses the `clio-playground-web` edge key + a separate IMS identity).

**Secrets hygiene.** Never paste Vault tokens / Artifactory encrypted passwords into a chat or a tracked file; rotate if leaked (`vault token revoke -self`).
