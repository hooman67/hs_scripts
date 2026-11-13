---
type: source
title: Colligo models/ ingest
tags: [colligo, models, source, ingest]
created: 2026-07-05
updated: 2026-07-05
raw: "[[raw/colligo/models/_provenance.md]]"
sources: ["[[raw/colligo/models/AGENTS.md]]"]
---

# Colligo models/ ingest

Summary of ingesting the `models/` folder of the [[wiki/entities/colligo|Colligo]] monorepo — the
directory where the concrete model **workers and pipelines** served by Colligo inference live.

## Source
- Repo `/Users/hshariati/colligo`, branch `main`, commit **`8f0cef36dc`**
  (`[FFP-97711] CD ConfigMap StateStore #27861`). Read-only.
- Raw copy: `raw/colligo/models/**` — 707 files (602 `colligo.yaml`, 104 prose docs, 1 pyproject),
  structure preserved. See [[raw/colligo/models/_provenance.md]].

## Scale & taxonomy
- **~52 top-level packages**, 602 `colligo.yaml` sub-packages. Actual path is
  `models/colligo/models/<package>/...` (namespace `colligo.models.*`).
- Grouped by modality in [[wiki/concepts/colligo-models]]: image generation (firefly/Clio, flux,
  lego_designs, spatial_generation), image editing/DI (di_imaging, ffent, recolor, masking, af_spur,
  ai_vector, text_effects, ff_image_ops), video (firefly/clineto, filix3, video, foundry/wan22), 3D
  (substance3d, foundry gen6), audio (audio, music_recommendations), text/LLM/prompt (firefall,
  dentro, prompt_forge, generative_presentations, agentic_design, encoders), eval/safety/classifiers
  (eval_classifiers, brewmaster, cai, ip_guard, content_guard, aesthetiq, deepfontserver, …), and
  infra/template/test/compare.

## Key findings
- A model package = tree of `colligo.yaml`-defined sub-packages (deps + visibility metadata), with a
  public `types/` (schemas + worker enum), a `worker/`/`models/` GPU implementation, a `build.py`
  deployment config, and `pipelines/`. Endpoints are declared **in code**, not in `colligo.yaml`.
- `compare/` is a large public v1/v2/v3 **endpoint layer** mapping stable customer API paths to workers.
- **Custom pyenvs** are pervasive (conflicting torch/transformers/numpy/CUDA); OSS weights are
  **S3-staged** via `hf_hub` stubs (pinned version_id + SHA-256), not fetched from HF at runtime.
- **Minimal Inference** is the sanctioned researcher hand-off path (linear PyTorch harness, 100%
  component parity with production).

## Pages created
- Concept: [[wiki/concepts/colligo-models]] (catalog / key deliverable).
- Entities: [[wiki/entities/firefly-clio]], [[wiki/entities/firefly-clineto]], [[wiki/entities/di-imaging]],
  [[wiki/entities/flux]], [[wiki/entities/firefly-substance3d]], [[wiki/entities/firefly-firefall]].

## Uncovered / future
- Deep per-worker internals (individual `build.py` GPU configs, exact endpoint paths per package).
- Audio, agentic_design, generative_presentations, and eval_classifiers only summarized — each could
  become its own entity page.
- `compare/` endpoint layer mapping and the `build/` apps/hf_hub staging system deserve a dedicated page.

## Related
- [[wiki/entities/colligo]] · [[wiki/concepts/colligo-inference]] · [[wiki/concepts/colligo-inference-sdk]]
- [[wiki/concepts/colligo-architecture]] · [[wiki/concepts/colligo-training]]
