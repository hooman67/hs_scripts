# AF Spur

Async Endpoints for detection and editing of text within images.

```mermaid
sequenceDiagram
    participant user
    participant v2/images
    participant v1/af_spur_ocr
    participant Azure
    participant v1/af_spur_edit
    participant v2/3p-images/generate-async

    user->>v2/images: Upload image
    v2/images-->>user: Return unique_id

    user->>v1/af_spur_ocr: Request OCR with unique_id
    v1/af_spur_ocr->>Azure: Perform OCR
    Azure-->>v1/af_spur_ocr: Return OCR results (with words)
    v1/af_spur_ocr-->>user: Return OCR results

    user->>v1/af_spur_edit: Request edit with new words
    loop 3 times
        v1/af_spur_edit->>v2/3p-images/generate-async: Perform edit
        v2/3p-images/generate-async-->>v1/af_spur_edit: Return edited image
    end
    v1/af_spur_edit-->>user: Return edited image
```

## Setup

`af_spur` uses a custom Python environment (`af_spur`) due to its dependency on a specific version of `transformers` and `flash-attn` that conflict with the default `dev` env.

### 1. Enable and create the custom environment

```bash
./m deps.enable af_spur
./m deps.create --env af_spur
```

### 2. Lock dependencies (Linux only)

Only needed when changing `envs/af_spur/constraints.txt`. Lock files must be generated on Linux because the environment includes CUDA-dependent wheels (`flash-attn`).

```bash
./m deps.lock --env af_spur
```

On macOS, use the Docker-based locker instead (requires Docker Desktop and `ARTIFACTORY_UW2_API_TOKEN`):

```bash
./m deps.lock.docker --env af_spur
```

After locking, commit the updated `requirements.lock.txt`, `known-packages.txt`, and `linter-roots.txt`.

### 3. Set the Python interpreter for local rhode development

When running rhode locally (VSCode debugger), you must point the Python interpreter at the `af_spur` venv rather than the default `dev` venv:

- **VSCode**: Python: Select Interpreter → Enter interpreter path → `./.venvs/af_spur/bin/python`

This is required because the worker's `colligo.yaml` declares `custom_pyenv: af_spur`, so the rhode supervisor will launch the worker process using `.venvs/af_spur/bin/python`. Mismatching the interpreter causes import errors for packages only present in the `af_spur` env (e.g. `af_spur`, `flash-attn`).

### Linting

Because the package uses a custom env, run the linter with the `--paths` flag to avoid mypy falling back to the wrong environment:

```bash
./m lint --paths "models/colligo/models/af_spur"
```
