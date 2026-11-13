# Foundation Exploration Config System

Practical guidance for editing and validating training configs safely, with a focus on Gen6-style runs.

## Quick Reference

```bash
# 1) Structural + shard-cache validation (recommended before launch)
python scripts/misc/validate_config.py -c configs/genrender6/prod/<config>.yaml

# 2) Structural-only validation (skip shard cache checks)
python scripts/misc/validate_config.py -c configs/genrender6/prod/<config>.yaml --skip-cache

# 3) Local sanity run with automatic config mutation for local hardware
morictl local_run --mutate-config configs/genrender6/prod/<config>.yaml

# 4) Launch after validation
morictl launch configs/genrender6/prod/<config>.yaml
```

## When To Use This Workflow

- You are editing `configs/genrender6/...` training configs.
- You changed `data.params`, `data.layout`, `inference.datasets`, or mapping sections.
- You added/removed inference datasets or renamed dataloaders.
- You want to catch config coupling errors before spending cluster GPUs.

## Config Coupling Rules (Most Common Failures)

1. **`data.layout` names must exist in `data.params`.**
   - Every `layout` entry name must exactly match a dataloader `name` in `data.params`.

2. **`validation_mapping` dataloader names must exist in `data.params`.**
   - If you remove a shard from `data.params`, remove it from `validation_mapping` too.

3. **Inference dataset `output_type` must be resolvable.**
   - Each dataset should set `params.output_type`, or
   - Provide a resolvable `params.system_prompt_key_override`.

4. **Minimum GPU constraints must remain valid.**
   - Do not reduce total GPUs below `sharding_gpus` / `balance_gpu_count` expectations for the model.

5. **Training config must be tuned to avoid performance issues.**
   - See [Training Config Setup](../../docs/training_config_setup.md) for guidance on how to do this.

## Recommended Edit Sequence

1. Edit the target config (usually a debug copy, not prod-in-place).
2. Run `validate_config.py` first.
3. Run local sanity with `morictl local_run --mutate-config`.
4. Only then launch remotely.

## Troubleshooting

- **`Training dataloader X not found`**
  - A mapping references a removed or renamed dataloader.
  - Fix name alignment across `data.params`, `data.layout`, and `validation_mapping`.

- **Validation warns about unresolved `output_type`**
  - Add explicit `output_type`, or set a valid `system_prompt_key_override`.

- **`Cannot expand layout... Need N splittable sources, found M`**
  - Not enough data sources can be split to balance layout for world_size.
  - The training system automatically splits sources with `n_gpus=1` and `batch_size >= min_splitting_batch_size` (default: 4).
  - Fix: Add more single-GPU sources, increase batch sizes, or adjust `num_nodes` to make world_size divisible by layout size.
  - See [Automatic data source splitting](finetuning_with_custom_data.md#automatic-data-source-splitting) for details.

- **`world_size` / balance constraints fail locally**
  - Re-run with `--mutate-config`, then inspect nested balance/sharding sections in the config.

## Notes for Gen6 Experiments

For Gen6-related config work, run:

```bash
python scripts/misc/validate_config.py -c configs/genrender6/prod/<config>.yaml
```

This catches cross-section config mismatches and missing shard cache early, before launch.

