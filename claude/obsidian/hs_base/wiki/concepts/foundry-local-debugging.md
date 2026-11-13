---
type: concept
title: Local debugging of a Foundry app (VS Code)
tags: [foundry, debugging, vscode, debugpy, vault, thd]
created: 2026-09-14
updated: 2026-09-14
sources: ["[[raw/thd-seedance-video-pipeline-learnings-2026-09]]"]
---

# Local debugging of a Foundry app (VS Code)

Bring a Foundry standalone app (e.g. [[wiki/entities/thd-video|THD Video]]) up locally and step through
the real pipeline in the VS Code debugger. The app's `DEBUGGING.md` holds the runbook; here's the
durable how/why.

## Two ways in
- **One-step (F5):** a `debugpy` **launch** config that runs `scripts/serve.py local-simple --port 8000`
  under the debugger via the app's own venv python. Starts and debugs in one step.
- **Attach:** `make debug` launches under `debugpy --listen 5678 --wait-for-client`, then attach with the
  "Attach (debugpy 5678)" config. Better for the interactive Vault flow (runs in a real terminal).

## The editable-install / breakpoint gotcha
The editable install **symlinks the app into the venv**, so at runtime a module's `__file__` reports the
**site-packages** path (not the workspace source) — even though edits are live through the symlink. So the
launch configs need **`pathMappings`** (site-packages → workspace) for breakpoints to bind. Set
`justMyCode:false` to step into framework/libs. If the venv's Python minor version changes, update the
`python3.12` segment in the mapping. Open the **`managed_services`** folder as the workspace so
`${workspaceFolder}` resolves.

## Vault auth
`VaultClient` authenticates **on demand** (OIDC) — do **not** pre-run `vault login`. On first start it
prints an Okta URL; on Pluto, open it on your laptop and `curl '<full callback URL>'` from another
terminal, and startup continues to bind `:8000`. Config (fal key, OpenAI, SAM3 IMS creds) is fetched
from Vault by `scripts/serve.py get_default_config`.

## Driving requests / breakpoints
- Trigger with the bundled smoke (no auth locally): `make smoke HOST=http://127.0.0.1:8000 IMAGE=…`
  (variants `smoke-rewrite`, `smoke-motion-bank`, `smoke-video-ref`).
- Good breakpoint spots: `ThdVideoPipeline.execute`, `seedance_rewriter/{orchestrator,compiler}.py`,
  `image_preprocessing/anonymize.py`, `seedance/provider.py::_fal_payload`.
- Local preprocessing default is `remove` (paint-out); to hit SAM3 anonymize run with
  `--image-preprocessing` + a config whose `default_method="anonymize"`.

## Related
- [[wiki/entities/thd-video]] · [[wiki/concepts/foundry-standalone-app-pipeline]]
- [[wiki/concepts/foundry-dev-deploy]] — shipping instead of local
- [[wiki/concepts/pluto-secrets]] · [[wiki/entities/pluto]]
