# Product-position flexibility experiment

This folder records the controlled PR #4349 experiment that allows the scene model to translate a digital-twin product while preserving its exact orientation/view for downstream product-pixel reuse.

## Source lineage

- Repository: `git@github.com:Adobe-Firefly/foundry.git`
- PR: `https://github.com/Adobe-Firefly/foundry/pull/4349`
- Isolated durable checkout: `/home/colligo/foundry-pr4349-position-exp`
- Local branch: `hshariati/hp-position-flex-exp`
- PR head inspected on 2026-11-05: `8c358bc7989cb0e137e89db0fd325168249e2a22`
- Pipeline: `/home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25`

The deployed 8016 demo identifies itself as PR #4349 and uses the same guide-only/no-mask policy. Its FastAPI/UI wrapper is not present in PR #4349; that source remains a separate provenance gap.

The deployed status records identify its private run directory as `/mnt/localssd/hp_image/hp16_3p/runs/...` on the remote owner's Pluto pod. That volatile directory is not mounted on this machine. The public OpenAPI surface exposes catalog, scene-only generation, job polling, and artifact routes, but no source route. The four-fixture smoke therefore uses a durable CLI harness that imports and invokes PR #4349's `run_row` directly. It replays each frozen control selection and Stage-A geometry and injects the byte-identical control guide so the treatment changes only Stage-B/final prompt policy. The missing deployed wrapper remains a visible provenance limitation. A later 160-row treatment must not be described as using that wrapper unless its source becomes available.

An earlier `70620ce...` observation came from `Adobe-Firefly/colligo` PR #4349 because that checkout's `origin` pointed at the Colligo repository. It is unrelated. The canonical `Adobe-Firefly/foundry` PR #4349 head, a fresh `git ls-remote`, and the deployed endpoint's `rewriterVersion` all agree on `8c358bc7989c...`.

## Experiment boundary

Allow only x-y translation when this improves usable placement, support geometry, or composition. Preserve scale and exact 3D orientation/view: yaw, pitch, roll, visible faces, camera-facing surfaces, perspective, foreshortening, silhouette, open/closed state, finish, and product details. Preserve contact, full visibility, and no occlusion.

The prompt delta passed offline tests and a four-fixture laptop/printer smoke test. The full frozen V6.1 160-row treatment is now running.

## Implemented prompt delta

The isolated worktree keeps Stage A and guide-renderer coordinates unchanged. The revised prompt permits one optional common x-y image-plane translation of the product and its planned support/contact relationship. Scale, yaw/pitch/roll, visible faces, projection/foreshortening, silhouette proportions, state and details remain fixed. Movement is allowed only for plausible access, support geometry, furniture alignment or composition, never to center or enlarge the product.

Changed source files in the isolated checkout:

- `/home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25/hp3p/prompts/system_3p.txt`
- `/home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py`
- `/home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25/hp3p/geometry.py`
- `/home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25/hp3p/reference_blue.py`

No mask, pixel repair, retry, renderer-math, schema or image-call change is part of the experiment.

## Durable artifacts

- `astra/prompt.md`: complete Astra product-integration request.
- `astra/output.md`: raw Astra response.
- `logs/astra.stdout.log`, `logs/astra.stderr.log`, `logs/astra.exit`: detached call evidence.
- `run_smoke.py`: controlled exact-PR-code smoke harness.
- `run_smoke.sh`: persistent Direct OpenAI gateway launcher.
- `smoke/baseline/`: four frozen control records, guides, product/reference inputs and outputs.
- `smoke/treatment/`: treatment pipeline records, images, prompts and per-fixture provenance.
- `logs/smoke.stdout.log`, `logs/smoke.stderr.log`, `logs/smoke.exit`: detached smoke evidence.
- `smoke/treatment/MECHANICAL_AUDIT.md`: frozen contract and visual smoke assessment.
- `local_endpoint.py`: thin local job API that imports exact PR4349 pipeline code.
- `run_local_endpoint.sh`: persistent local API launcher; tmux name `hp-position-endpoint`.
- `run_full160.py`: frozen-input-validated, resumable serial 160-row submitter.
- `run_full160.sh`: persistent runner launcher; tmux name `hp-position-full160`.
- `full160/run/jobs/`: per-row status, exact guide, result, output and call trace.
- `full160/progress.json`: durable completion checkpoint.
- `prompt_diff.patch`: frozen uncommitted isolated-worktree delta.
- `PROJECT_STATE.md`: live checkpoint and next exact step.
