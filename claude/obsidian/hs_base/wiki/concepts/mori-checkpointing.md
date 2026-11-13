---
type: concept
title: Mori S3 Checkpointing
tags: [mori, checkpointing, s3, experiment-manager, resume]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/mori-docs.md]]"]
---

# Mori S3 Checkpointing

How [[wiki/entities/mori|Mori]] persists and resumes training checkpoints on S3 — the mechanism behind long, resumable large-scale runs.

## Saving

Set env vars in the Pluto job script and enable the **experiment manager**:

```bash
export S3_BUCKET="adobe-ai-platform-video-checkpoint"
export S3_PREFIX="training_logs"
export EXP_MANAGER=true
```

The experiment manager watches the local checkpoint folder and uploads to S3 **periodically** — more robust than direct S3 writes, though a freshly-written checkpoint may lag before it uploads.

## Loading / resuming

```bash
torchrun --nnodes=1 --nproc_per_node=2 train_morix.py \
  --resume s3://clio.corp.adobe.com/<exp>/checkpoints/ckpt_step00000100.pth
```

Auto-recovery: Mori automatically resumes from the latest checkpoint in the user's log directory.

## Tools & access

- **AWS CLI** is the default large-file transfer tool; **s5cmd** is an optional alternative (`export USE_S5CMD=true`).
- Allowlisted buckets like `s3://clio.corp.adobe.com` need **no credentials**. (Compare with [[wiki/concepts/pluto-storage|Pluto storage]] / IAM-role S3 access.)
- Validate integrity: `python -m mori.training.utils.validate_checkpoint_integrity s3://.../path`.

## Handling S3 throttling at scale

For large jobs hitting S3 API throttling:
- **HSDP broadcasting** — only rank 0 downloads; others receive broadcast copies.
- **Pre-partitioned prefixes** — spread load across dedicated partitions.
- **Checkpoint replicas** — keep copies across multiple S3 prefixes for load-balancing.

Support: `#mori-users` Slack (post job URL, error logs, log-dir path).

## Related
- [[wiki/entities/mori]]
- [[wiki/concepts/mori-training-workflow]]
- [[wiki/concepts/pluto-storage]]
- [[wiki/entities/pluto]]
