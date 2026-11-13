# Lyra-2 Foundry Worker

Wraps NVIDIA's [Lyra-2](https://research.nvidia.com/labs/dir/lyra2/) image-to-3D model as a Colligo Foundry worker.
Given a still image and a motion caption it produces a Gaussian Splat PLY, a walkthrough video, and a flythrough video.

## Local inference setup

**Prerequisites:** H100 or H200 GPU (80 GB+ VRAM).

```bash
# 1. Create and sync the custom environment
./m deps.enable foundry_lyra2
./m deps.sync
```

**VS Code (recommended):** use the **inference: rhode debug deploy** run config and select
`foundry`. The `foundry_lyra2` venv is picked up automatically from `colligo.yaml` and
the ~91 GB checkpoint set is downloaded from S3 via the `lyra2_ckpt_files` data item —
no manual checkpoint setup needed.

**worker_e2e.py (smoke test):** the data item is not registered in this path, so you
need the checkpoints pre-downloaded and `LYRA2_CHECKPOINT_DIR` pointing at them:

```bash
source .venvs/foundry_lyra2/bin/activate

python -m colligo.models.foundry.workers.lyra2.scripts.worker_e2e \
    --image /path/to/scene.jpg \
    --caption "A cinematic drone shot through an autumn forest." \
    --ckpt /mnt/localssd/lyra/Lyra-2-weights/checkpoints
```

## Do not deploy yet

Deployment requires a capacity discussion with the infra team first (H200 node
availability, quota, scaling policy). Do not add this worker to any environment's
values.yaml until that is resolved.

## License

The upstream Lyra-2 model and its bundled components (VIPE, Depth Anything 3)
are released under **Apache 2.0** (copyright 2025 NVIDIA Corporation & Affiliates).

Licensing for production use at Adobe is **TBD** — confirm with legal before
enabling this worker in any customer-facing environment.
