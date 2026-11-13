---
type: concept
title: Mori Config & Sequence Balancer
tags: [mori, config, knapformer, sequence-balancer, data-layout, yaml]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/colligo/mori/collections/foundation_exploration/docs/training_config_setup.md]]", "[[raw/colligo/mori/collections/foundation_exploration/scripts/agent/config_system.md]]"]
---

# Mori Config & Sequence Balancer

How [[wiki/entities/mori|Mori]] training runs are configured (YAML), and the **KnapFormer sequence balancer** that makes large heterogeneous runs efficient. (Detail drawn from the active Gen6 / `foundation_exploration` collection.)

## Config validation workflow

Configs are YAML per experiment (e.g. `configs/genrender6/prod/<config>.yaml`). Validate before launch:

```bash
python scripts/misc/validate_config.py -c configs/.../<config>.yaml        # structural + shard-cache
python scripts/misc/validate_config.py -c ... --skip-cache                  # structural only
morictl local_run --mutate-config configs/.../<config>.yaml                  # local sanity (auto-mutates for local HW)
morictl launch configs/.../<config>.yaml
```

**Coupling rules (most common failures):**
1. Every `data.layout` name must exist in `data.params` (as a dataloader `name`).
2. `validation_mapping` dataloader names must exist in `data.params`.
3. Inference dataset `output_type` must be resolvable (explicit `params.output_type` or a valid `system_prompt_key_override`).
4. Don't reduce total GPUs below `sharding_gpus` / `balance_gpu_count` expectations.

## Key terms

- **world_size** = total GPUs = `num_nodes × num_gpus`.
- **layout_size** = sum of `n_gpus` across `data.layout` entries (`[source_name, n_gpus]`).

## Sequence balancer (KnapFormer)

Critical for performance (misconfiguration → OOM / bottlenecks). It redistributes sequences across GPUs to minimize per-GPU workload variance in three passes: **assign** sequences to bags (greedy knapsack), **chunk** within multi-GPU bags, **route** chunks via all-to-all. Controlled by `balance_gpu_specs`, e.g. `ring=none,ulysses=8,bags=8,inner=ulysses` — `ulysses` = GPUs per bag, `bags` = number of independent groups.

- **Single-GPU bags (`ulysses=1`)** — efficient for homogeneous workloads (uniform resolution).
- **Multi-GPU bags (`ulysses=8`)** — better for heterogeneous workloads (mixed image+video / resolutions); `ulysses=8` groups a full node to exploit NVLink for the all-to-all.
- Guideline: make `ulysses × bags == layout_size` (not full world_size). When `world_size % layout_size != 0`, the system auto-splits data sources to the **smallest divisor of world_size ≥ layout_size**; target that value.
- **Ring+Ulysses hybrid** (`ring=4,ulysses=16,bags=4,inner=ring`) builds a 2D GPU grid to exceed the pure-Ulysses ceiling (SP degree ≤ #attention heads) for 256+ sources or 1080p video. See [[wiki/concepts/mori-parallelism]].

## Related balancer knobs

- **`vae_balance_gpu_count`** — set to layout_size (VAE encode/decode balancing).
- **`balance_gpu_count`** (VLM text encoder) — layout_size or layout_size/2 when `auto_balance_prompts: true`.

## Automatic data-source splitting

The data layout need not divide world_size: Mori auto-splits the highest-workload splittable sources to reach the closest valid layout size without changing the data mix (e.g. 14 sources on 64 GPUs → 16). Tunable via `data.min_splitting_batch_size` (default 4; sources below it aren't split).

## Related
- [[wiki/entities/mori]]
- [[wiki/concepts/mori-parallelism]]
- [[wiki/concepts/mori-training-workflow]]
- [[wiki/concepts/mori-architecture]]
