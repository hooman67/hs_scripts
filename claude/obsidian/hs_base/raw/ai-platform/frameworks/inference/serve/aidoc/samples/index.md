---
children:
  - [../../samples/a_basic/README.md, "1. Basic worker"]
  - [../../samples/b_async/README.md, "2. Async patterns"]
  - [../../samples/c_background/README.md, "3. Background jobs"]
  - [../../samples/flux/README.md, "4. Multi-GPU pipeline (FLUX)"]
---

# Samples

```{note}
For the full learning path (samples 1-10, spanning both the framework and managed services),
see the [Inference Platform overview](/platforms/inference/aidoc/index.md#sample-progression).
```

These are the framework-only samples (1-4). They work with any deployment path.

- **[1. Basic worker](../../samples/a_basic/README.md)** — Minimal all-sync example. Start here to learn the fundamentals: compute workers, pipeline workers, web apps, and how to run them locally or in the cloud.

- **[2. Async patterns](../../samples/b_async/README.md)** — Demonstrates using `async def` for `Worker.execute`, `Worker.load`, and WebApp endpoints. Exercises the full sync/async calling matrix.

- **[3. Background jobs](../../samples/c_background/README.md)** — Demonstrates the background (resilient async) API for asynchronous job execution with status tracking and cancellation.

- **[4. Multi-GPU pipeline (FLUX)](../../samples/flux/README.md)** — Full FLUX.1-schnell image generation pipeline decomposed into separate GPU workers. Demonstrates multi-GPU allocation, `num_processes` for replicas, pipeline orchestration, and `params.devices`.

Samples 5-10 are in the [managed services ecosystem](https://docs.ai.corp.adobe.com/managed_services/services/samples/README.html) and add Bazel builds, CI/CD, and Kubernetes deployment.
