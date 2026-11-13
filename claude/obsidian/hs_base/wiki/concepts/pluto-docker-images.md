---
type: concept
title: Pluto Docker images
tags: [adobe-infra, compute, pluto, docker, images, containers]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/pluto-docs-extras]]"]
---

# Pluto Docker images

Every [[wiki/entities/pluto|Pluto]] job runs a Docker image. The platform ships certified base images and validates jobs against an allowlist; you can also build custom images and even build/run containers **inside** a running job.

## Base & certified images

Platform images run on AMI `ami-001c9106ee1b8910d` (kernel `5.10.223-212.873`, Nvidia driver `550.90.07`, CUDA `12.4`). The certified allowlist lives at `platforms/pluto/utilities/images/certified_images.json`; jobs are validated against it unless you pass `--skip-certified-check`.

- **Default GPU base:** `docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/pluto-training-base:...-CUDA-v12.8.1-...-ubuntu24.04-...-PY-3.12-...`
- **Default CPU base:** `docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/pluto-cpu:...-ubuntu-24.04-py3.12-amd64`
- Also certified: `colligo/colligo-dev:latest` (GPU); a CUDA 13.2.0 Devel variant.

## Building custom images

Two paths: (1) the [build-image](https://github.com/OneAdobe/build-image) workflow (build/push from a Dockerfile), or (2) a Docker-enabled job (`--docker`) built interactively. Docs recommend `uv` for reproducible deps:

```dockerfile
FROM <certified-base-image>
COPY pyproject.toml uv.lock /workspace/
RUN uv sync --frozen --no-dev
COPY src/ /workspace/src/
```

**Do:** use `uv sync`/`uv pip install`; copy scripts/config; set app env vars.
**Do NOT:** replace system Python; modify `/opt/`; change entrypoint/CMD; remove CUDA/NCCL/cuDNN system packages; install a different CUDA version.

Validate before running: `aip images validate <image-url>` and `aip images info <image-url>` (see [[wiki/concepts/pluto-cli-sdk]]).

**Support boundary:** the platform team owns base OS, CUDA/cuDNN/NCCL, Python runtime, and Pluto agent tooling; you own pip packages, training scripts, weights, and data. The platform "does not debug issues caused by user-installed packages or modifications to platform-owned layers." Rebuild custom images when certified bases update.

**Artifactory cache:** since June 2026, images auto-route through `*.af-cache.colligo.dev`.

## Building & running Docker inside a job (DinC)

You can build/run containers within a running job without restarting (tight build-test loop). Enable via **Execution Specs > Content → Enable Docker**, or CLI `--docker`. Requirements: the job must run the platform-selected Docker image and **run on a whole node**; an A10G-1GPU node (`g5.4xlarge`) is recommended.

- Newer images (from `colligo-dev:1.40.4`+) include **BuildKit**: `docker buildx build --no-cache --builder pluto-builder -t something:0.0.1 .`. BuildKit has no Docker daemon, so `--load` fails — use `--push`. Older images use plain `docker build`.
- **Artifactory login:** env vars `${ARTIFACTORY_UW2_USER}` / `${ARTIFACTORY_UW2_API_TOKEN}`.
- **GPU in container:** `docker run -it --gpus all ubuntu /bin/bash`.
- **Mount Sensei FS:** `-v /sensei-fs-3/users/$(cut -d '@' -f 1 <<< ${PLUTO_REMOTE_USER_EMAIL}):/sensei-fs`.
- **Compose & ports:** supported (GPU needs a `deploy.resources.reservations.devices` block); containers reachable at `https://job-name-PORT.<CLUSTER>.colligo.dev/`.
- **How it works:** "Docker-in-Containerd (DinC)" — a Docker daemon inside a platform-managed containerd process (not DinD). Debug logs at `${PLUTO_JOB_LOGS_DIR}/system/dockerd/`.

## Related
- [[wiki/entities/pluto]]
- [[wiki/concepts/pluto-job-lifecycle]]
- [[wiki/concepts/pluto-cli-sdk]]
- [[wiki/concepts/pluto-storage]]
- [[wiki/sources/pluto-docs-extras]]
