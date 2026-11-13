# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# gen_upscaler

Generative image super-resolution service. A Rhode-served HTTP endpoint (`POST /v2/images/generate-sr`) that runs the ZipIR diffusion model in tiled, masked-inpainting mode to produce 2x/4x/8x upscales with synthesized high-frequency detail. This directory is one package root inside the larger `models/` workspace — it has its own `colligo.yaml` per subpackage and its own dependency graph; see `docs/arb.md` for the full design doc.

## Two parallel entry points

The package ships the same ZipIR pipeline in **two** forms. Keep both in mind — they are intentional and serve different purposes:

1. **Service** (`pipelines/upscaler.py` + `models/{tile,t5,clip,caption}/model.py`) — a distributed Rhode deployment with one orchestrator pipeline and four GPU workers.
2. **Reference inference app** (`foundation_exploration/inference/inference_app.py`) — the same math in a single process, used as ground truth when debugging service divergence.

When investigating output bugs, always diff service output against the inference app; the latter is the reference implementation.

## Architecture

```
HTTP POST /v2/images/generate-sr
   ↓  apis/adapters/upscaler.py      (http ↔ pipeline types)
[GenUpscalerPipeline]  pipelines/upscaler.py
   ├─ GenUpscalerEmbeddingsComponent    components/input_embeddings/upscaler.py
   │    ├─ bicubic upscale (CPU)
   │    ├─ CaptionExecutor   → gen_upscaler_caption   (Qwen2.5-VL-7B, 18 GB)   [only if prompt=None]
   │    └─ asyncio.gather(T5Executor, CLIPExecutor)
   │          → gen_upscaler_t5     (T5-Flan, 10 GB)
   │          → gen_upscaler_clip   (AdobeOne ViT-H ONNX, 5 GB)
   └─ GenUpscalerDiffusionComponent    components/diffusion/upscaler.py
        ├─ scanline tiling (utils/tiling.py)
        └─ for each tile: TileExecutor → gen_upscaler_tile  (VAE+DiT, 40 GB)
              vae_encode → EGG/SDE sampling loop → vae_decode
              per-tile color_match_lr (numpy/PIL) + mask compositing
```

Color correction runs per-tile inside `DiffusionComponent` during stitching (matches `inference_app` behavior). There is no separate post-stitching/decoding stage — `diffusion.output_images` is the pipeline response.

Key architecture notes:

- **VAE is co-located with DiT** inside `TileModel` (not a separate worker). A request sends a *pixel tile in, pixel tile out* — VAE encode/decode never cross process boundaries.
- **Tile requests are heavy** (~100 MB serialized each): image + masked image + text/image embeddings, and the embeddings are re-sent for every tile. Generate a full smell inventory via the `analyze-codebase` skill (produces `CODEBASE_DIGEST.{md,json}`).
- **Tiles are processed sequentially by design** — `masked_zipir` requires previous tiles to be composited into the mask before the next tile runs.
- **`masked_zipir=True`, `use_compact_condition=True`** are hardcoded; not exposed via the API.
- **foundation_exploration/clio_core/** is a *local fork* of `cliocore`. Production imports would otherwise resolve to `contrib/AdobeDiffusion/cliocore/`; both `inference_app.py` and `models/tile/model.py` patch YAML `target:` strings at runtime to rewrite `clio.*` → `clio_core` and `foundation_playground.*` → `colligo.models.di_imaging.gen_upscaler.foundation_exploration.*`.

## Commands

All Python commands use the repo dev venv: `/home/colligo/colligo/.venvs/dev/bin/python`.

### Lint / build graph regeneration

From the repo root (`/home/colligo/colligo`), since this package participates in the global build graph:

```bash
./m lint --paths models/colligo/models/di_imaging/gen_upscaler
./m lint --check --paths models/colligo/models/di_imaging/gen_upscaler   # no fixes
```

`./m lint` auto-generates `colligo.yaml` manifests from the `build.py` files — do NOT hand-edit `colligo.yaml` entries.

### Running the service (Rhode)

Launch config `"Inference: Rhode Debug Deploy"` in the repo-root `.vscode/launch.json` (`/home/colligo/colligo/.vscode/launch.json`), or equivalently:

```bash
python -m colligo.rhode.commands.dev_supervisor --spec gen_upscaler --locust --log-to-file
```

Service comes up on port 8000. A 404 on the endpoint means workers haven't finished loading — wait and retry, don't change the asset id.

Clean shutdown when orphaned GPU processes are left behind (order matters — supervisor MUST die before workers, otherwise workers respawn):

```bash
pkill -KILL -f "colligo.rhode.commands.dev_supervisor" || true
sleep 2
pkill -KILL -f "colligo.rhode.commands.workers.models" || true
lsof -ti:8000 | xargs -r kill -KILL || true
```

### Running the reference inference app

Uses the full `colligo.models.di_imaging.gen_upscaler.foundation_exploration.*` import path, so `models/` must be on `PYTHONPATH`. All `clio.*` deps have been migrated into `foundation_exploration/clio_core/` — no extra PYTHONPATH entries needed.

```bash
REPO=/home/colligo/colligo
FE=$REPO/models/colligo/models/di_imaging/gen_upscaler/foundation_exploration
OUT=$REPO/models/colligo/models/di_imaging/gen_upscaler/debug_outputs/inference_$(date +%Y%m%d_%H%M%S)
mkdir -p "$OUT"

PYTHONPATH=$REPO/models:$FE/inference \
$REPO/.venvs/dev/bin/python $FE/inference/inference_app.py \
    --config      $FE/configs/f32_config_patch1_8node_mixres_tile_filtered_x8_masked_8k_compact_sr_upscale.yaml \
    --denoiser_pt /sensei-fs/users/abhinavve/zipir/denoiser/denoiser_pkg/denoiser-8k-upscale-non-ema.pt \
    --images      /sensei-fs/users/cobarnes/zipir/input_images/tier1/AdobeStock_119662205.jpg \
    --out_dir     "$OUT/AdobeStock_119662205.jpg" \
    --resize_image --tile_inference --color_correction --steps 8
    # add: --save_intermediates "$OUT"    to dump per-step tensors
```

See `foundation_exploration/inference/README.md` for the full PYTHONPATH / runtime-patching rationale.

### Driving the service

Service accepts `multipart/form-data`: a `request` JSON part + an `input.source=@file` binary part, paired by the JSON's `input.source.name: "input.source"`.

```bash
curl -X POST http://localhost:8000/v2/images/generate-sr \
  -H "Accept: multipart/form-data" \
  -H "x-request-id: manual-$(date +%s)" \
  -F 'request={
        "input": { "source": { "name": "input.source" } },
        "seeds": [0], "scaleFactor": 4, "numSteps": 8, "cfgScale": 5,
        "colorCorrection": true, "tileSize": 4096, "tileOverlap": 256
      };type=application/json' \
  -F 'input.source=@/sensei-fs/users/cobarnes/zipir/input_images/tier1/AdobeStock_119662205.jpg;type=image/jpeg' \
  -o /tmp/service_response.bin
```

The response is a multipart body — the JPEG starts at the first `\xff\xd8\xff` byte sequence. Ground-truth reference outputs for comparison live at `/home/colligo/service_teacher_comparison/tier1-abhinav-genupsampler-inference-outputs/`.

## Code layout

```
apis/
  types/upscaler.py          Pydantic request/response + PublicEndpoint registration
  adapters/upscaler.py       http_request_to_pipeline_request, pipeline_response_to_http_response
components/                   Pure per-phase logic; no direct model calls — use executors
  input_embeddings/upscaler.py
  diffusion/upscaler.py
models/<worker>/              One directory per Rhode worker (tile, t5, clip, caption)
  types.py                    *Executor (client-side handle) + *Request/*Response
  model.py                    *Model (server-side handler) subclassing ColligoModel
  build.py                    build.deploy_worker(...) declaration — registers in build graph
pipelines/
  upscaler.py                GenUpscalerPipeline — orchestrates the three components
  build.py                    build.deploy_worker + deps on all four *Model names + endpoint
utils/tiling.py               scanline_order, mask-aware tile geometry
foundation_exploration/       Vendored research code — ZipIR reference
  inference/inference_app.py    Single-process reference implementation
  clio_core/                    Local fork of cliocore (see note above)
  configs/*.yaml                ZipIR model configs
docs/arb.md, docs/openapi.yaml  Architecture doc + generated OpenAPI spec
scripts/                      Wrapper scripts for the inline commands below
                              (run_inference.sh, send_request.sh, kill_session.sh,
                              compare_tensors.py, parse_trace.py, *_pptx.py).
                              Prefer these wrappers; the snippets in this file are the
                              source of truth they wrap.
.claude/skills/               analyze-codebase (→ CODEBASE_DIGEST.{md,json}),
                              analyze-perf (→ OPTIMIZATION_REPORT*.md), debug-service-diff
```

## When adding or modifying a worker

1. Update `models/<worker>/types.py`, `model.py`, `build.py` together.
2. If dependencies changed, edit `build.py` — not `colligo.yaml`. The yaml is regenerated by `./m lint`.
3. If registering a new endpoint, add the `PublicEndpoint` in `apis/types/upscaler.py` and list it under `public_http_endpoints=[...]` in `pipelines/build.py`.
4. Re-run `./m lint --paths models/colligo/models/di_imaging/gen_upscaler` from the repo root to refresh the build graph and apply formatting/mypy.

## Debugging output divergence

For the full service-vs-inference_app diff workflow (launch, bisect per-step, root-cause report, run-log format), invoke the **`debug-service-diff`** skill — triggered by "run debug", "step debug", "compare intermediate outputs", or "trace the diff". The skill has the commands inlined (no scripts/ dependency).

`agent.md` at the top of this package is an earlier prose version of the same protocol and is **superseded by the skill** — the skill is the source of truth. Ignore `agent.md` unless you're specifically reviewing history.

## Log locations

- Supervisor stdout: `debug_outputs/service.log`
- Worker logs: `_build/rhode-work-dir-gen_upscaler/logs/` — **check these first** for worker errors; the supervisor log only shows orchestration.
- Inference app log: `debug_outputs/inference_<timestamp>.log`

## Request payload (service)

```jsonc
// sent as multipart: a "request" JSON part + an "input.source" binary part
{
  "input":         { "source": { "name": "input.source" } },
  "seeds":         [0],
  "scaleFactor":   4,
  "numSteps":      8,
  "cfgScale":      5,
  "colorCorrection": true,
  "tileSize":      4096,
  "tileOverlap":   256
}
```

Defaults, ranges, and the optional `prompt` / `negPrompt` / `output` fields are defined in `apis/types/upscaler.py:GenUpscalerAPIRequest`.
