---
type: concept
title: Colligo models catalog
tags: [colligo, models, inference, firefly, catalog, models-directory]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/colligo/models/AGENTS.md]]", "[[raw/colligo/models/firefly/README.md]]", "[[raw/colligo/models/di_imaging/README.md]]", "[[raw/colligo/models/af_spur/README.md]]", "[[raw/colligo/models/foundry/workers/AGENTS.md]]", "[[raw/colligo/models/_provenance.md]]"]
---

# Colligo models catalog

The catalog/index of `models/` — the directory in the [[wiki/entities/colligo|Colligo]] monorepo
where the concrete **model workers and pipelines** served by Colligo inference live. Every generative
Firefly capability (image, video, audio, 3D, text/LLM) plus the eval, safety, and gateway workers
that support them is a package here. As of commit `8f0cef36dc` there are **~52 top-level packages**
holding **602 `colligo.yaml` sub-packages**.

## What `models/` is

`models/` is **tenant/user code**, not platform code. It sits on top of the platform primitives
described in [[wiki/concepts/colligo-inference]] (Rhode workers, apps, GPU sharing) and
[[wiki/concepts/colligo-inference-sdk]]. The platform team owns the framework; ~200 developers across
squads own the packages here. The root guidance
([[raw/colligo/models/AGENTS.md]]) is explicit: **treat `models/` as many independent package roots,
not one uniform subsystem.**

Actual source path: `models/colligo/models/<package>/...` (the outer `models/` is the package root
declaring the `colligo` namespace; everything ships under the `colligo.models.*` import path).

## How a model package is structured

A package is a tree of **sub-packages**, each defined by a `colligo.yaml`. The `colligo.yaml` is
**dependency + visibility metadata** (see [[wiki/concepts/colligo-architecture]]), not an endpoint
declaration:

```yaml
visibility: public
public:            # the public sub-package other packages may import
  files: [types]
  deps: [colligo.base, pydantic, ...]
deps:              # private runtime deps of this sub-package
- colligo.fastapi
- colligo.image
exclude: [scripts]
```

The recurring internal shape of a model package:

- **`types/` (public)** — request/response pydantic schemas + a worker/endpoint **enum**. The public
  surface other packages import.
- **`worker/` (or `models/`)** — the `ColligoMLModel` implementation(s) that load weights and run on GPU.
- **`build.py`** — deployment config: which workers, GPU/VRAM per worker, the Rhode **app** they register into.
- **`pipelines/`** — multi-worker orchestration (e.g. text encoder → DiT → VAE decoder → NSFW → upscaler).
- **co-located `tests/`**, and often a `README.md`/`AGENTS.md`.

Endpoints are declared in code (`types.py` enums + `build.py`/app registration), so the HTTP surface
(`POST /v1/<area>/<op>`, sync or `-async`) is not visible in `colligo.yaml`. Many packages pin a
`custom_pyenv:` in `colligo.yaml` (e.g. `af_spur`, `sglang_0_5_9`, `vllm_0_18_0`, `foundry_mesh3d`)
so the Rhode supervisor launches the worker with a dedicated venv — always check this before touching deps.

### Relationship to inference workers

Each leaf package becomes one or more **Rhode workers** (a model loaded on GPU) grouped into **apps**.
Multiple workers share a GPU; a **pipeline** worker calls other workers (locally or remotely) to
compose an endpoint. See [[wiki/concepts/colligo-inference]] for the worker/app/GPU-sharing model and
[[wiki/concepts/colligo-inference-sdk]] for how callers invoke them (`HttpClient` vs `NativeClient`).
The `compare/` package is a large **public API/endpoint layer** (v1/v2/v3) that maps stable customer
endpoints (`images/generate`, `fill`, `expand`, `masking/*`, `models3d/*`, `videos`, `vllm/*`) onto
the underlying model workers.

## Model taxonomy (packages grouped by modality/family)

### Image generation (Firefly / diffusion)
- **firefly** — the flagship. The Firefly image model family: [[wiki/entities/firefly-clio|Clio/CM]]
  diffusion (`clio`, `diffusion/clio1..4`, `gen45`, `gr6`, `image5`, `cm5`), T5/gen45 text encoders,
  VAEs (`imcoding/*`), priors, and the [[wiki/entities/firefly-clineto|Clineto]] video pipelines. Also
  hosts `clio_tyom` (Custom Models / "Train Your Own Model"), `minimal_inference` (dev prototyping
  harness), `sglang_diffusion` (serves OSS DiTs — FLUX.1-dev, Qwen-Image — via SGLang), and `brewmaster`
  (model eval portal).
- **[[wiki/entities/flux|flux]]** — Black Forest Labs FLUX image DiT support (types/weights); FLUX.1-dev
  also served via `firefly/sglang_diffusion` and `adobe_research/flux2_klein`.
- **lego_designs** — "Lego" layered/vector design generation (diffusion + VAE + text encoder +
  Qwen prompt expansion); paired with `firefly/lego_*` MLLM backends (`lego_mllm`, `lego_sglang_v1`,
  `lego_vllm_v4`) and the `pipelines/lego_v1` pipeline.
- **spatial_generation** — gen6 spatial/IBL/panorama/3D image generation pipelines (LDM, TTT-LRM, VLM caption).

### Image editing & Digital Imaging (DI)
- **[[wiki/entities/di-imaging|di_imaging]]** — the Digital Imaging suite (owned by co-di): MultiEdit
  (generative erase/expand/fill, object stitch, envirofill), gen_upscaler, GR6 relighting/lightshop,
  harmonization, matting/trimap, SAM2, masking (select-subject, material selection, segformers), depth,
  ESRGAN, CMGAN, NSFW.
- **ffent** — Firefly Enterprise MultiEdit (enterprise variant of the DI multiedit stack:
  pixelperfect, objectcomposite, objectstitch + NSFW).
- **ff_image_ops** — Firefly image operations utilities.
- **recolor** — object recolor (detection + segmentation + tagging + business logic).
- **masking** — standalone select-subject v1 masking worker.
- **text_effects** — text/typography effects generation.
- **af_spur** — async OCR + text-in-image detection & editing (uses Azure OCR + 3P image generate;
  `custom_pyenv: af_spur`).
- **ai_vector** — AI vectorization pipelines (imagetrace, matrix/mosaic agentic pipelines, rotate/select-subject vector).

### Video
- **[[wiki/entities/firefly-clineto|firefly/clineto]]** — the production Firefly **text-to-video /
  image-to-video / video-to-video** pipeline (Filix2 DiT + T5 + AdobeOne image encoder + spatial/edge
  encoders + dual VAE + SSR + Dentro/NSFW guards); model versions like `filix2_t2v_prod1_9_540p`.
- **filix3** — Filix3 generation stack (images/video/img23d/mirai/rgbx/upscalegs; DiT, dual-VAE, T5, BLIP2 workers).
- **video** — video ops: avatar (ffmpeg), lipsync pipeline, background removal, mask propagation,
  uprez (2x/3x/4x super-res), frame extraction; shared `video/common` profiling backends.
- **firefly/mori_lipsync**, **video/lipsync** — lip-sync generation.
- **foundry** workers **wan22** — WAN 2.2 video generation (base, distilled for Foundry Studio depth
  control, NBCU VACE upsampler); plus `video_composition`, `video_concat`, `lyra2`.

### 3D / Substance
- **substance3d** — Substance 3D: MeshLRM/MinLRM mesh reconstruction, Materia Carbon texture gen,
  material super-resolution, IBL post-process, Lagrange meshing.
- **foundry** 3D workers/pipelines — gen6 image-to-multiview (`im2mv`), multiview-to-mesh (`mv2mesh`,
  TripoSG), mesh-to-texture (`mesh2tex`), depth-anything-v3, depth/edge.
- **filix3/img23d** — image-to-3D via Filix3.

### Audio
- **audio** — the audio suite: text-to-speech (tts/ttsv2), speech enhancement (enhance_speech, soundlift),
  transcription (transcribe, whispurr), music generation (genmusic/generate_music), sound-effect
  generation (gensoundfx), auto-dub, beat tracking, tempo, audio tagging.
- **music_recommendations** — music recommendation (feature extractor + video transformer).

### Text / LLM / prompt / agentic
- **firefall** — the Firefly LLM/3P layer: `firefall_router`, 3P gen/LLM pipelines (`gen_3p`, `llm_3p`),
  `auto_model_selector` (leaderboard-driven best-model recommendation), entity service, CAI, notifications.
- **firefly_gateway**, **firefly/ff_gateway_oss** — Firefly model gateway.
- **dentro** / **dentro_v2** — VLM/LLM model zoo used as pre/post processors and eval judges
  (Gemma3, InternVL, Phi, LLaVA, image-reward, VQAScore, face quality, text-rendering, vbench).
- **gemma_text_encoder**, **qwen_vlm_encoder**, **firefly/gen45_text_encoder**, **firefly/t5** — text/VLM
  encoders feeding diffusion pipelines.
- **prompt_forge** / **prompt_forge_llm** — prompt moderation + diversity injection + NSFW pre-check
  (PromptForge V2 and its Qwen3.5-27B LLM replacement).
- **prompt_suggestions**, **autocomplete** — prompt suggestion & autocomplete workers.
- **generative_presentations** (+ **_kg_inferrer**) — PDF/Doc → Express presentation (GPT-driven
  outline/content + stock/Firefly imagery).
- **agentic_design** — agentic design pipeline (graphical processor, text extraction/grouping/backing-shape detection).
- **firefly/vllm_omni**, **cm_vllm**, **internvl**, **prompty** — misc LLM/VLM serving.

### Eval, classifiers & safety
- **eval_classifiers** — eval model zoo (image-reward, VQAScore, vbench, face detection/quality,
  hydranet, text-rendering, extendibility, LLaVA classifier).
- **firefly/brewmaster** — self-contained model-evaluation portal (T2V/I2V/V2V/T2I/I2I; 50+ metrics).
- **cai** / **foundry/cai** — Content Authenticity (C2PA / content credentials).
- **content_guard**, **ip_guard** — content & IP safety/guarding (retrieval-based IP detection).
- **content_type_classifier**, **aesthetiq**, **stylized_text_detector**,
  **typography_pattern_recognition**, **deepfontserver**, **exif_content_predictor**, **apollo_mae** —
  specialized classifiers/detectors (aesthetics, fonts/typography, EXIF, MAE backbone).

### Providers, gateways & external services
- **image_providers** — obtain images for generative designs (Adobe Stock search + Firefly generation).
- **external_services** — thin wrappers for CME, job registry, Melville, OpenAI, prompt-suggestion, vectorize.

### Infrastructure, templates & test
- **common** — shared model utilities (adapter_utils, diffusion, metrics, ocreval, eval-sci utils).
- **build** — deployment/build helpers, apps, and the `hf_hub` S3 model-staging stubs.
- **compare** — the large public v1/v2/v3 **endpoint layer** mapping stable API paths to workers.
- **foundry** — Foundry Studio tenant workers + `authz`, `safety`, `metrics`, `media_composition`, `smoke_t`.
- **adobe_research** — research-contributed workers (flux2_klein, metashadow_detect, parametric_color_grading,
  shot_matching, text2rgba).
- **template** — scaffolding for new model packages (see [[wiki/concepts/colligo-inference]] tutorials).
- **test** — framework test fixtures (echo, sleepy, sse, stream, faulty, storage_test, etc.).

## Notable cross-cutting conventions
- **Custom pyenvs are common** — image/video/LLM workers frequently need conflicting torch/transformers/
  numpy/CUDA combos, isolated via `custom_pyenv:` + `envs/<name>` lock files.
- **OSS weights are S3-staged**, not pulled from HuggingFace at runtime: `hf_hub` stubs pin
  `version_id` + SHA-256 for deterministic, rate-limit-free, license-once cold starts (see
  `firefly/sglang_diffusion`).
- **ACP generation metadata** — Foundry generative pipelines must attach `FoundryGenerationMetadata`
  (prompt/seed/model/version) on ACP upload so Creative Cloud users see generation context.
- **Minimal Inference** — a linear, PyTorch-native prototyping harness with 100% component parity to the
  production pipeline, the recommended hand-off path for researchers integrating models.

## Related
- [[wiki/entities/colligo]] — the parent monorepo.
- [[wiki/concepts/colligo-inference]] · [[wiki/concepts/colligo-inference-sdk]] — how these workers are served & called.
- [[wiki/concepts/colligo-architecture]] — the `colligo.yaml` deps/visibility model.
- [[wiki/concepts/colligo-managed-services]] — Inference V3 (separate Bazel workspace).
- [[wiki/concepts/colligo-training]] — Mori, where many of these models are trained.
- [[wiki/entities/firefly-clio]] · [[wiki/entities/firefly-clineto]] · [[wiki/entities/di-imaging]] · [[wiki/entities/flux]] · [[wiki/entities/firefly-substance3d]] · [[wiki/entities/firefly-firefall]]
- [[wiki/sources/colligo-models-ingest]] — ingest summary.
