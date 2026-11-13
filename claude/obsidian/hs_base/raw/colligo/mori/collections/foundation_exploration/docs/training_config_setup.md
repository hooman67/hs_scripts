# Training Config Setup

Tips for setting up GR6 training configs effectively. Focuses on settings that reduce manual work and common pitfalls.

---

## Glossary

| Term | Definition |
|------|------------|
| **world_size** | Total number of GPUs in the training job. Calculated as `num_nodes × num_gpus` (e.g., 32 nodes × 8 GPUs = 256). |
| **layout_size** | Total GPU slots defined in `data.layout`. Each entry is `[source_name, n_gpus]`, and layout_size is the sum of all n_gpus values. |

---

## Sequence Balancer Setup

To get good performance, it is **critical to configure the sequence balancer correctly**. Otherwise there can be OOM errors, and efficiency bottlenecks.

### Replication: When world_size > layout_size

When your total GPU count (world_size) is a multiple of your data layout size, the system creates **replicas**. Each replica runs all data sources in the layout, processing different random samples.

Example with layout_size=32 and world_size=1024:
- 1024 / 32 = 32 replicas
- Replica 0: GPUs 0-31 (all 32 data sources)
- Replica 1: GPUs 32-63 (same data sources, different samples)
- ... and so on

The sequence balancer also creates its own replicas based on `balance_gpu_specs`.

### How it works

The sequence balancer is based on the **KnapFormer** algorithm. It redistributes sequences across GPUs to minimize workload imbalance using a three-pass approach:

1. **Assign sequences to bags**: Estimate workload per sequence, then use a greedy knapsack algorithm to assign sequences to bags while minimizing per-GPU variance.
2. **Chunk within bags**: For multi-GPU bags, divide each assigned sequence into chunks across the GPUs in that bag.
3. **Route chunks**: Execute an all-to-all collective to move chunks to their target GPUs.

The `balance_gpu_specs` config controls this - e.g. `ring=none,ulysses=8,bags=8,inner=ulysses`.
`ulysses` sets GPUs per bag, and `bags` sets how many independent groups there are.

### Guidelines

**When to use single-GPU bags (`ulysses=1`):**
- Efficient for training on **homogeneous** workloads (e.g., uniform resolution like 512p images only).
- The knapsack algorithm can fully balance workloads without sequence parallelism overhead.

**When to use multi-GPU bags (e.g. `ulysses=8`):**
- Better for **heterogeneous** workloads with long sequences mixed with shorter ones (e.g., joint image+video, mixed resolutions like 240p-720p). Sequence parallelism helps here since the knapsack alone can't fully balance due to variations in sequence lengths.
- `ulysses=8` is a common choice because it groups all 8 GPUs within a node, leveraging high-bandwidth NVLink for the all-to-all communication. Cross-node communication (EFA) is slower. It also keeps chunks sizes reasonable.

**General guidelines:**
- Set `ulysses` depending on type of workload (homogeneous vs heterogeneous, see above).
- Set `bags` in a way that `ulysses × bags` equals your layout_size (not the full world_size, otherwise communication overhead will be too high at large scales). The system automatically creates sequence balancer replicas when required.
- If `world_size % layout_size != 0`, the system will auto-split data sources to expand the layout_size to **smallest divisor of world_size that is >= layout_size**. In this case, make `ulysses × bags` equal to this value. For example: layout_size=28, world_size=1024 → use bags=4 and ulysses=8 (since 1024 % 32 == 0 and 32 >= 28).

Examples (assuming heterogeneous workload):
- layout_size=32, world_size=32: `balance_gpu_specs: "ring=none,ulysses=8,bags=4,inner=ulysses"` (32 GPUs)
- layout_size=32, world_size=1024: same spec works - creates 32 balance replicas automatically
- layout_size=28, world_size=1024: same spec works
- layout_size=64, world_size=1024: `balance_gpu_specs: "ring=none,ulysses=8,bags=8,inner=ulysses"` (64 GPUs, 16 replicas)

### Ring+Ulysses

Pure Ulysses has a ceiling: the sequence parallel degree cannot exceed the number of attention heads. For very large data layouts (256+ sources) or very long sequences (1080p videos), use Ring+Ulysses hybrid to break this ceiling:

```yaml
balance_gpu_specs: "ring=4,ulysses=16,bags=4,inner=ring"
```

This creates a 2D GPU grid where ring attention handles one dimension and Ulysses handles the other, achieving 4x16=64-way sequence parallelism. See `docs/extended_knapformer.md` for details.

---

## Other Config parameters to set

**vae_balance_gpu_count:** Set equal to layout_size (not world_size) for efficient balancing. The VAE balancer redistributes encoding/decoding work across GPUs to minimize per-GPU latency. VAE work varies significantly across data sources (video chunks vs images), so maximum group size gives the best load distribution. Communication overhead is small relative to VAE compute.

**balance_gpu_count (VLM encoder):** Set to layout_size or layout_size/2 (not world_size). Controls VLM text encoder prompt balancing when `auto_balance_prompts: true`.

Like before, if `world_size % layout_size != 0`, you should use the **smallest divisor of world_size that is >= layout_size** instead of the layout_size for both these parameters.

---

## Data Layout

### Setting Data Sources and GPUs

Data sources can be listed in any order in the layout, because the sequence balancer splits compute across all GPUs efficiently.

### Data Layout Doesn't Need to Divide World Size

The training system has automatic data source splitting that handles cases where your layout doesn't evenly divide the world size. The system identifies splittable sources, then splits them to reach the closest valid layout size.

For example, 14 data sources on 64 GPUs would be auto-expanded to 16 sources by splitting the 2 highest-workload sources. This does NOT change the existing data mix.

You can configure the minimum batch size for splitting, though the default should work well in almost all cases:
```yaml
data:
  min_splitting_batch_size: 4  # sources with batch_size < 4 won't be split
```

See "Automatic data source splitting" in `scripts/agent/finetuning_with_custom_data.md` for the full algorithm.

---

## Quick Runs with --limit-samples

All debugging, validation and profiling runs should be started with the `--limit-samples` flag to save time.

```bash
morictl local_run <config> --limit-samples 3
morictl launch <config> --limit-samples 3
```

This limits each SQL data source to load only N samples by adding a `LIMIT` clause to sql queries. It also disables data downloads from S3 and reduces worker threads for faster startup.

Use 2-3 samples - single-sample runs may hit invalid rows and fail.
