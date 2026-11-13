---
type: concept
title: Colligo Inference SDK
tags: [colligo, inference, sdk, python, jupyter]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/colligo/pylibs/colligo/sdk/aidoc/index.md]]"]
---

# Colligo Inference SDK

A Python package (`pylibs/colligo/sdk/`) that lets you **call or run [[wiki/entities/colligo|Colligo]] inference workers without the full monorepo dev environment** — e.g. from a Jupyter notebook or any Python script. Distinct from the [[wiki/concepts/colligo-pluto-sdk|Pluto SDK]] (which manages compute jobs); this SDK invokes served models.

## Two ways to install/use

- **Inside the monorepo dev env** — readily available, no install.
- **As a pip package** (no monorepo setup):
  ```bash
  pip install -U torch "adobe-aip[inference]" \
    --extra-index-url=https://:$ARTIFACTORY_UW2_API_TOKEN@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple
  ```
  `adobe-aip[inference]` for calling **remote** workers; `adobe-aip[inference-workers]` to also run workers **locally**. Torch is installed separately.

The SDK is the concrete "short-lived code" delivery vehicle from Colligo's [[wiki/concepts/colligo-philosophy|philosophy]] — though the docs note it is "far from stable, published software" yet.

## Two client modes

- **`HttpClient`** — call models served **remotely** over HTTP. Set the registry with `set_worker_registery(HttpClient(HTTP_ENDPOINT[, AUTH_TOKEN]))`, then `await SomeExecutor.call(request, ...)`. Corp endpoints are VPN-only; auth is an IMS token (starts with `ey`, findable in the Debug UI via "Copy access token").
- **`NativeClient`** — run models **locally** in-process (e.g. notebook): `registery = await NativeClient.create([CLIO_V2]); set_worker_registery(registery)`. Can also delegate specific workers to remote endpoints via `colligo.dev.yaml` config.

Typical call flow: import the worker's types + `Executor` (e.g. `T5Executor`, `ClioExecutor`), build a request pydantic model, `await Executor.call(...)`, then decode outputs (image tensors → PIL/encoded images).

## V3 note

In [[wiki/concepts/colligo-managed-services|Managed Services (V3)]] the Inference SDK is **no longer part of the monorepo** — it becomes an external, independently versioned dependency defined inside `managed_services/`.

## Related

- [[wiki/concepts/colligo-inference]]
- [[wiki/entities/colligo]]
- [[wiki/concepts/colligo-pluto-sdk]]
- [[wiki/concepts/colligo-managed-services]]
