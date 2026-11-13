---
type: concept
title: Pluto JupyterLab
tags: [adobe-infra, compute, pluto, jupyter, notebooks, interactive]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/pluto-docs-extras]]"]
---

# Pluto JupyterLab

JupyterLab runs as a background process inside a [[wiki/concepts/pluto-job-lifecycle|Pluto interactive session]], reached through VS Code Web or a direct URL.

## Launching

- **Recommended (VS Code):** open VS Code Web via "Open VS Code" in job details (Run Details > Pods > Links), install Microsoft's Python extension, then the Jupyter extension.
- **Custom install:**
  ```
  pip install jupyterlab ipykernel
  python -m ipykernel install --user
  jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
  ```
  Or automate startup via a job init script.

## Access & networking

Default port **8888**; URL pattern `https://host-name-8888.<CLUSTER>.colligo.dev/lab/tree/<file.ipynb>`. For remote access set `ServerApp.allow_websocket_origin='*'`.

> [!warning] Auth can be disabled
> "Setting both token and password to empty strings disables authentication, so anyone with network access can access your JupyterLab instance without a password."

## Kernels, environment & persistence

Conda env at `/opt/conda/bin/activate`; register kernels via `ipykernel install --user`; install packages in-notebook with `!pip install` / `!conda install`. Notebooks auto-save; all job-mounted volumes are visible in the file browser. Files persist across sessions only if saved to designated volumes (see [[wiki/concepts/pluto-storage]]). Git works via terminal or VS Code.

## Related
- [[wiki/entities/pluto]]
- [[wiki/concepts/pluto-job-lifecycle]]
- [[wiki/concepts/pluto-console]]
- [[wiki/concepts/pluto-storage]]
- [[wiki/sources/pluto-docs-extras]]
