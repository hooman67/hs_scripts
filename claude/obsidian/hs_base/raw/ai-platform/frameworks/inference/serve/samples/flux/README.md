# FLUX Image Generation Pipeline

A full end-to-end sample that decomposes [FLUX.1-schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell) image generation into separate inference workers.

```{note}
**Managed services version:** To deploy this pipeline in the managed services ecosystem
(with CI/CD, Bazel builds, BKS authorization, CAI signing, and k8s deployment), see
[Sample E](https://docs.ai.corp.adobe.com/managed_services/services/samples/E/README.html).
```

![](./images/demo.png)

> **Why decompose?** FLUX can run perfectly well on a single GPU — you do *not*
> need to split it into separate workers to generate images. This sample
> deliberately breaks the pipeline apart to demonstrate the inference framework's
> multi-GPU and pipeline capabilities. In real production scenarios this
> decomposition becomes valuable when the components have **different resource
> profiles and throughput characteristics**: T5-XXL is slow and needs ~10 GB,
> the VAE is fast and needs < 1 GB, and the denoiser sits somewhere in between.
> Splitting lets you:
>
> - **Scale independently** — give the T5 encoder `num_processes=2` while keeping
>   the lightweight VAE at 1 replica.
> - **Place on appropriately-sized GPUs** — put the denoiser on a large GPU and
>   the CLIP encoder on a small one.
> - **Avoid one bottleneck blocking everything** — a slow encoder doesn't hold up
>   the VAE from processing already-denoised requests.


---

## Architecture

```
                        ┌──────────────────┐
            ┌──────────►│  CLIP Encoder    │──────┐
            │           │  (1 GB GPU)      │      │
            │           └──────────────────┘      │
 prompt ──► Pipeline                               ──► Denoiser ──► VAE ──► image
            │           ┌──────────────────┐      │    (25 GB)      (1 GB)
            └──────────►│  T5 Encoder      │──────┘
                        │  (10 GB GPU, ×2) │
                        └──────────────────┘
```

| Worker | Model | GPU Memory | `num_processes` |
|---|---|---|---|
| CLIP encoder | CLIP-L text encoder (from FLUX.1-schnell checkpoint) | ~1 GB | 1 |
| T5 encoder | T5-XXL (via FLUX checkpoint) | ~10 GB | 2 |
| Denoiser | `FluxTransformer2DModel` + `FlowMatchEulerDiscreteScheduler` | ~25 GB | 1 |
| VAE decoder | FLUX `AutoencoderKL` | ~1 GB | 1 |
| Pipeline | CPU orchestrator — no model | — | 1 |

The **pipeline worker** calls CLIP and T5 in parallel (via `asyncio.gather` +
`submit_from_el`), feeds both embeddings to the denoiser, then sends the
resulting latents to the VAE for decoding. The full denoising loop runs
inside the denoiser worker to avoid per-step round-trips over Redis.

---

## Background (Resilient Async) Mode

In addition to immediate (synchronous) generation, the sample supports background
job submission. This is useful when generation takes a long time and the caller
does not want to hold a connection open.

Three endpoint patterns are demonstrated:

- **Background-only** (`POST /generate/background`): always submits in
  background mode, returns a job ID with status/cancel URLs.
- **Completion callback** (`POST /generate/with-callback`): background submission
  with a module-level callback invoked when the job reaches a terminal state.
- **Custom query** (`GET /my-jobs/{job_id}`): builds a custom response shape,
  caching the generated image and returning a `presignedUrl` on completion.

The builtin Jobs webapp (`GET /v3/jobs/{job_id}`, `DELETE /v3/jobs/{job_id}`) is
also mounted for standard job lifecycle management.

---

## Running

### Local (prototyping)

```bash
uv run python scripts/run_local.py
```

All workers load in-process. Good for debugging, but requires all models to fit
in memory at once.

### Distributed (multi-GPU)

```bash
uv run python scripts/run_distributed.py
```

Each worker runs in its own subprocess with isolated `CUDA_VISIBLE_DEVICES`.
Opens the interactive dashboard; use curl or the Swagger UI at
`http://localhost:8000/docs` to generate images:

```bash
# Immediate mode (default): returns JSON {"presignedUrl": "/images/<id>"}
curl http://localhost:8000/generate \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "A cat sitting on a windowsill"}'

# Then fetch the image:
curl http://localhost:8000/images/<id> --output image.png

# Background mode: returns 202 with {"job_id": "...", "links": {"cancel": {...}, "result": {...}}}
curl http://localhost:8000/generate/background \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "A cat sitting on a windowsill"}'

# Poll job status:
curl http://localhost:8000/v3/jobs/<job_id>
```

### Testing (end-to-end)

`__manual_test__.py` runs a full end-to-end test of the distributed pipeline:
starts `inference.serve()`, waits for the readiness probe, sends a `/generate`
request, verifies the response, and tears everything down. It requires multiple
GPUs and is **not** picked up by pytest — run it manually:

```{colligo_list_files} ./__manual_test__.py
:use_docstring: true
:show_code:
```

---

## Source code

Workers and web app:

```{colligo_list_files} ./src/ai/flux_sample/*.py
:use_docstring: true
:show_code:
```

Run scripts:

```{colligo_list_files}  ./scripts/*.py
:use_docstring: true
:show_code:
```

Manual test:

```{colligo_list_files} ./__manual_test__.py
:use_docstring: true
:show_code:
```
