---
type: concept
title: Mori Parallelism (MoriX strategies)
tags: [mori, morix, parallelism, fsdp, fsdp2, context-parallelism, attention]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/mori-docs.md]]", "[[raw/colligo/mori/README.md]]"]
---

# Mori Parallelism (MoriX strategies)

The distributed-training strategies exposed by **MoriX**, the accelerator inside [[wiki/entities/mori|Mori]]. All strategies plug in via the **Strategy Pattern** — a new scheme = a new `Plugin` (see [[wiki/concepts/mori-architecture]]).

## Sharding

- **FSDP2 — primary/recommended.** Shards the model's parameters and gradients across devices to cut communication overhead (evolution of FSDP v1, which is deprecated). Configured via `FSDP2ShardingConfig`; implementation `mori.training._dev.plugin.fsdp2_plugin.FSDP2Plugin`. MoriX currently supports both FSDP and FSDP2.

## Sequence / context parallelism

- **Context Parallelism (aka sequence parallelism).** Partitions inputs across devices so each GPU processes a portion — valuable for very long inputs (high-resolution images, video). Enable with `sp_size` (parallelism degree) and `token_budget` (max sequence length).
- **Distributed Attention (in-house).** Evenly shards the input across all GPUs *within a single node* so each GPU processes an equal-length input. Supported, still evolving.
- Optimized attention backends available: **FA2, FA3**, Context Parallelism, and Distributed Attention. For very large layouts (256+ data sources) or very long sequences (1080p video), a **Ring+Ulysses** hybrid breaks the pure-Ulysses ceiling (SP degree ≤ #attention heads) — see the sequence-balancer detail in [[wiki/concepts/mori-config]].

## Not yet available

- **Pipeline parallelism:** not supported.
- **Tensor parallelism:** in progress.

## Relationship to the sequence balancer

Parallelism degree interacts with the **KnapFormer sequence balancer** (`balance_gpu_specs`, e.g. `ring=none,ulysses=8,bags=8,inner=ulysses`), which distributes variable-length sequences across GPUs. That configuration is covered in [[wiki/concepts/mori-config]].

## Related
- [[wiki/entities/mori]]
- [[wiki/concepts/mori-architecture]]
- [[wiki/concepts/mori-config]]
- [[wiki/concepts/mori-training-workflow]]
