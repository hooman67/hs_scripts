<!-- Provenance: distilled from a Claude Code working session on the THD Seedance
reference-to-video Foundry standalone app (managed_services/services/firefly/foundry/
standalone_apps/thd_video), 2026-09-14. Captures operational learnings: prompting Seedance,
the structured rewriter, duration control, image roles, the pipeline architecture, SAM3
anonymize, dev deployment, local debugging, eval methodology, and result HTML generation. -->

# THD Seedance video pipeline — session learnings (2026-09)

Source: interactive engineering session on the `thd_video` app (The Home Depot Seedance
reference-to-video generation, served through Adobe Foundry / Colligo V3).

## Seedance model (via fal.ai)
- The generator is ByteDance **Seedance 2.5** hosted on **fal.ai** (a third-party vendor), endpoint
  `bytedance/seedance-2.5/reference-to-video`. Our pipeline builds the request; fal runs the model.
- `duration` accepts `"auto"` or an int **4–30s**. Per fal docs, `"auto"` = *the model sizes the clip
  to the prompt*. Default `auto`.
- **Seedance 2.0** (`fal-ai/seedance-2/enterprise/reference-to-video`) is used only when the caller
  supplies a reference **video** (laxer policy, caps 15s). Motion-bank **clips** stay on 2.5.
- Strict content policy; on rejection the pipeline retries with a declutter/paint-out edit
  (`DECLUTTER_EDIT_PROMPT`) then surfaces `SeedanceContentPolicyError` (whose `detail` can be a list).

## Structured rewriter / how to prompt Seedance
- A GPT rewriter (`seedance_rewriter/`) turns the raw brief into a structured shot, then a
  deterministic compiler renders the exact Seedance string (parity). Key fields:
  - **Event Script** — a beat timeline tiled across `seconds` (segments like `0-4 seconds: …`).
  - **beats** — ordered *physical* actions (each → one segment). `demeanor` (expression/mood) is a
    separate uncapped 【Performance】 box and does NOT count as a beat.
  - 【Fidelity】 — a standing anti-blur directive (references are anonymized; regenerate clear).
  - **Reference Asset Roles** — a shipped section labelling each `@ImageN` with a role
    (scene / identity / keyframe / motion / storyboard).
- **The rewriter LLM is multimodal** — it receives the image bytes and re-roles each `@ImageN` in its
  output from what it sees. `rewriter.py` hardcodes `role:"scene"` in the manifest it *shows* the LLM,
  but that's only an input hint; the shipped roles are LLM-inferred (verify with a real `used_prompt`
  before claiming "everything is scene").
- `notesToUser` (clamp/drop/couldn't-honour notes) flows to the response envelope. `must_be_true`
  (checkable facts) is captured, clamped, and validated but **no consumer reads it** — effectively
  write-only.

## Duration control (the 10s cap was ours)
- fal `auto` follows the prompt, so the old ~10s ceiling was **ours**: `seedance_rewriter/schema.py`
  `MAX_SECONDS` clamps the Event-Script timeline. Levers that must move together: `MAX_SECONDS` +
  the system-prompt rule "seconds: an integer 4–N". `MAX_BEATS` caps beats (each is a segment).
- To get longer clips keep sending `duration:"auto"` — it sizes to the now-longer prompt. Explicit
  `durationSeconds` (4–30) also works. We raised `MAX_SECONDS 10→30`, `MAX_BEATS 2→5` and proved a
  **12.04s** clip on bookshelf shot 28 (brief timing to 0:12), still with `auto`.

## Image roles (reference vs storyboard)
- The request contract (`ImageAssetInput`) carries per image only `role: reference | storyboard` —
  there is **no** product/character/scene field. For storyboard-role assets the pipeline appends a
  fixed storyboard directive to the prompt (configurable text + a debug override).
- The eval sets' `ordered_assets.entity/kind` (drill/couch/living-room/storyboard) is an **offline
  digestion artifact**, not a production input. At inference the only per-image signals are the
  request role + the server's product-bank match + the multimodal LLM's own inference. Feeding known
  roles into the rewriter (instead of hardcoded scene) is a deferred follow-up.

## Pipeline architecture
- `ThdVideoPipeline` (CPU orchestrator): SKU search → GPT rewriter → IP Guard → image preprocessing →
  Seedance via fal. Speaks the shared Foundry **unified inference envelope**.
- **Async job model:** submit `POST /v2/video/generate` (or `/v2/video/prompt-rewrite`) → `{jobId,
  links.result.href}` → poll the result href until `succeeded|partial|failed`. Upload references first
  via `POST /v2/storage/image` → use the id as a `tempStorage` source.
- **Product / motion bank:** SKU search resolves products to bank entries; attaches a **grid**
  (Seedance 2.5, `@ImageN`) by default or a **clip** (`@VideoN`) when `pickMotionVideo` is enabled.

## SAM3 anonymize
- `image_preprocessing/anonymize.py::Sam3Anonymizer` calls the deployed `sam2_image` service:
  `POST /v2/storage/image` (upload) + `POST /v1/masking/sam3` (text prompts person/face/hand) → mask
  PNGs → local Gaussian blur composited over the plate.
- **Auth nuance:** use the **ethos-direct** host `https://sam2-image-dev.ethos851-stage-or2.ethos.adobe.net`
  with `x-api-key = foundry-services` (the IMS client_id). The `.private.adobe.io` **edge** rejects
  that; it needs a registered edge key (the reference `naou_image/sam3_client.py` uses
  `clio-playground-web` + a separate IMS identity). Identity via a `foundry-services` IMS bearer.
- Preprocessing has two methods: `remove` (Nano-Banana paint-out, the deploy default) and `anonymize`
  (SAM3 blur). The request cannot select the method; it's the deploy `default_method`.

## Deploying to dev
- Flow: commit → `smake lint` → `make image` (rebuilds only on a new git sha → **commit first**) →
  bump the `image:` tag in `deploys/<app>/dev/values.inference.yaml` → `smake lint` again (regenerates
  `cloud/`) → commit **only your app's** files (values + `cloud/dev/<app>-<cluster>/`) → PR → merge.
- **GitOps two hops:** merge to `main` → GH Action `sync-argocd-mirror` pushes `managed_services/cloud/`
  to the **`colligo-v3-deploy`** mirror → **ArgoCD watches the mirror (not colligo)** → syncs to the
  cluster. So deploys lag; in ArgoCD (`argocd.ethos.corp.adobe.com`) Refresh to skip the poll, Sync
  only if stuck OutOfSync. App = `foundry-thd-video-ethos851-dev-or2`; verify the pod rolled to the
  new image tag.
- **Env prereqs / gotchas we hit:**
  - Artifactory: need IAM group `GRP-NEURAL-FILTERS-DEV` (Colligo Developer role) for
    `docker-colligo-release` read; put your identity token (from `artifactory-uw2.adobeitc.com`) in
    `~/.netrc` for `artifacts.adobeitc.com`. Symptom of missing: `smake` argo-sync chart download 401/404
    while `api/system/ping` is 200.
  - buildkit / `make image` `no builder "pluto-builder" found`: the s6 buildkit service parked at boot
    because `newuidmap` (the `uidmap` package) was missing. Fix: `sudo apt-get update && sudo apt-get
    install -y uidmap`, then restart the supervised service `sudo /opt/cis/command/s6-svc -d/-u
    /opt/cis/scandir/buildkit`; socket appears at `/mnt/localssd/.buildkit/buildkit.sock`. Daemonless
    (buildx pushes straight to ECR) — `dockerd` being down doesn't matter.
  - CI: "generated files up to date" fails if you didn't commit the regenerated `cloud/`. Doc CI fails
    (`toc.not_included`) on a stray `aidoc/**.md` not in a toctree → add `orphan: true` topmatter.
  - Another app's ephemeral `0.dev…` chart pin can break the global `smake argo-sync`; that's not you —
    ping the owner or neutralize+discard to regen just your app.
- Captured as the `/dev_deploy` Claude Code skill; the app's `AGENTS.md` has a Deployment section.

## Local debugging (VS Code)
- `make debug` launches under debugpy on 5678 (`--wait-for-client`); attach with the "THD Video:
  Attach (debugpy 5678)" launch config. Or a one-step "THD Video: Launch + debug" config (F5).
- The editable install **symlinks** the app into the venv, so module `__file__` reports the
  site-packages path → the launch config needs `pathMappings` (site-packages → workspace) for
  breakpoints to bind. `justMyCode:false` to step into libs.
- Vault (`VaultClient`) authenticates **on demand** (OIDC) — don't pre-run `vault login`; complete the
  printed URL (on Pluto: open on laptop, then `curl '<callback>'` from another terminal). Documented in
  the app's `DEBUGGING.md`.
- Gotcha seen: a `git stash pop` left conflict markers in the `Makefile` → `make` "missing separator".

## Eval methodology
- **Fix the eval set, run the UNMODIFIED pipeline.** Feed per-image role via `inference.Binary.metadata`
  (mirrors what the production webapp does) — never hack the pipeline to force behaviour. Clean/typed
  eval sets: strip the inline storyboard directive from prompts, add explicit per-asset `role`, keep
  them reproducible artifacts (`cleaned_prompts_asset_type.json` + an `index_asset_type.html` digest).
- **In-process driver pattern:** instantiate the pipeline directly (`object.__new__` + `load`),
  monkeypatch temp-storage to local files, run shots with `asyncio.wait_for` per-row timeouts.
- **Self-healing supervisor:** detached `setsid` process; kill + relaunch the driver on a >~1050s
  log-mtime stall (handles blocking fal hangs); give up after N; a finisher builds+uploads on DONE.
  Verify liveness by log mtime, not just pgrep.
- **Parallelize across two fal keys** (one set per key) to run eval sets concurrently.
- Always smoke one shot first (video returns, expected behaviour) before launching the full set.

## Result HTMLs
- Every eval set gets a **plain** report AND an **`_fe`** report in the **two-file `/fe_html` form**:
  a vendored `viewer.html` + a separate `data.json`, opened `…_fe.html?src=…_fe.json`. Never ship a
  self-contained card view as the `_fe` version.
- **IMS scaffold** (so IMS-authed S3 assets load): staging imslib + `./imsauth.js` + inline
  `onAuthReady`/`initializeIMS` on DOMContentLoaded; `#ims`/`#loading` before `#content`.
- **All asset URLs absolute** with the full `seedance_video_eval_sets/<set>/` prefix (form
  `https://foundry-aws-corp.adobe.io/asset/<bucket>/<key>`).
- Columns for these runs: input prompt · input images (with reference/storyboard asset-type badge) ·
  processed/anonymized inputs + motion-bank panel · rewritten prompt · output video.

## S3 / gateway access
- Foundry S3 via `foundry_aws_gateway.maybe_s3_client(bucket)` with
  `FOUNDRY_AWS_GATEWAY_HOST=https://foundry-aws-pluto.adobe.io` (works when raw broker creds are
  unavailable). Public asset view URLs: `https://foundry-aws-corp.adobe.io/asset/<bucket>/<key>`.
