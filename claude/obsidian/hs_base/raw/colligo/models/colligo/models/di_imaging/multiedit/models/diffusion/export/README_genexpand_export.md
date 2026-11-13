# DiT AOTI Export

This document describes how to run the DiT AOTI conversion script (`dit_aoti.py`), which exports the diffusion transformer to an AOTI (Ahead-of-Time Compilation) engine for optimized inference, with optional FP8 quantization.

## Prerequisites

- CUDA-capable GPU (e.g. H100)
- PyTorch with CUDA
- Model checkpoint: the config must point to a directory containing `model.safetensors` (see [Configuration](#configuration))
- For FP8 quantization: calibration data in one of the supported formats (see [Calibration data](#calibration-data))

## Basic usage

### Export only (no quantization)

```bash
python -m colligo.models.di_imaging.multiedit.models.diffusion.export.dit_aoti \
  --config /path/to/config.yaml \
  --output_dir /mnt/localssd/dit \
  --device h100
```

Output: `{output_dir}/dit.so` (e.g. `/mnt/localssd/dit/dit.so`).

### Export with FP8 quantization

1. Prepare calibration data (see [Calibration data](#calibration-data)).
2. Run with `--quantize_fp8`, `--calibration_data_path`, and optionally `--calibration_out_folder`:

```bash
python -m colligo.models.di_imaging.multiedit.models.diffusion.export.dit_aoti \
  --config /path/to/config.yaml \
  --output_dir /mnt/localssd/dit \
  --device h100 \
  --quantize_fp8 \
  --calibration_data_path /path/to/calibration/data \
  --calibration_out_folder /tmp/aoti_calibration/dit
```

- First run: performs calibration and writes observer state to `--calibration_out_folder` (e.g. `observers_ckpt.pt`). Later runs can reuse this by keeping the same `--calibration_out_folder`.
- Use `--save_quantized_checkpoint` to also save a quantized PyTorch checkpoint for loading at runtime (e.g. for `run_aoti`).

### Run inference benchmark after export

To compile, export, and then run a short inference benchmark (e.g. to verify the engine):

```bash
python -m colligo.models.di_imaging.multiedit.models.diffusion.export.dit_aoti \
  --config /path/to/config.yaml \
  --output_dir /mnt/localssd/dit \
  --device h100 \
  --run_inference_test
```

With quantization, use the saved quantized checkpoint for the benchmark:

```bash
python -m colligo.models.di_imaging.multiedit.models.diffusion.export.dit_aoti \
  --config /path/to/config.yaml \
  --output_dir /mnt/localssd/dit \
  --device h100 \
  --quantize_fp8 \
  --calibration_data_path /path/to/calibration/data \
  --calibration_out_folder /tmp/aoti_calibration/dit \
  --save_quantized_checkpoint \
  --run_inference_test
```

### Sample command (FP8 + inference test)

Full example with custom paths:

```bash
python /home/colligo/colligo/models/colligo/models/di_imaging/multiedit/models/diffusion/export/dit_aoti.py \
  --config /home/colligo/colligo/models/colligo/models/di_imaging/multiedit/models/diffusion/export/config_expand.yaml \
  --output_dir /sensei-fs/users/shaychan/multiedit/models/dit/lazy-diff-expand-distilled-aoti/ \
  --quantize_fp8 \
  --calibration_data_path /sensei-fs/users/shaychan/multiedit/dit/calibration_data_lazy/expand_pytorch/ \
  --save_quantized_checkpoint \
  --calibration_out_folder /sensei-fs/users/shaychan/multiedit/dit/calibration_out_lazy/expand/ \
  --run_inference_test
```

(Omitting `--config` uses the default `config.yaml` next to the script.)

## Calibration data

When `--quantize_fp8` is set, you must provide `--calibration_data_path`. The script supports two formats.

### Directory-based (recommended)

- `data_path` is a directory.
- Each **subdirectory** is one sample and must contain:
  - `x_in.pt`  — input tensor `(1, seqlen, 2048)`
  - `x_pe.pt`  — positional encoding `(1, seqlen, 256)`
  - `t_pe.pt`  — time encoding `(1, seqlen, 2048)`
  - `x_out.pt` (optional) — target output

Samples are taken from subdirectories in sorted order. Use `--calibration_num_samples` to limit how many are used.

### File-based

- Each sample is a single `.pt` file: `{data_path}/sample_{idx}.pt`.
- Each file should be a dict with:
  - `"args"`: tuple of `(x, x_pe, t_pe)` with shapes as above
  - `"kwargs"`: optional dict
  - `"output"`: optional target tensor

## Quantization behavior

- **Included:** Linear layers under `blocks.` (transformer blocks) that are not in the exclude list.
- **Excluded:** First and last transformer blocks (`tf_block_0`, `tf_block_27`) and specific attention/FFN weights (e.g. `wq`, `wk`, `wo`, `feed_forward.w2`) in blocks 1–26.
- Observer state is saved in `calibration_out_folder`. Reusing the same folder skips recalibration and loads existing observers.

## Outputs

- **Export:** `{output_dir}/dit.so` — AOTI engine for the transformer forward pass.
- **Calibration (when using FP8):**  
  - `observers_range_ckpt.pt`, `observers_ckpt.pt` in `--calibration_out_folder`.  
  - If `--save_quantized_checkpoint`: `quantized_model.pt` in `--calibration_out_folder`.

Runtime loading (e.g. in `run_aoti`) expects the engine in `output_dir` and, for quantized runs, the quantized checkpoint path (e.g. `{calibration_out_folder}/quantized_model.pt`).
