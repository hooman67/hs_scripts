# DiT AOTI Export (Generase)

This document describes how to run the Generase DiT AOTI conversion script (`dit_aoti_lazy_erase_fp8_calibrate.py`), which exports the diffusion transformer to an AOTI (Ahead-of-Time Compilation) engine for optimized inference, with optional FP8 quantization.

## Prerequisites

- CUDA-capable GPU (e.g. H100)
- PyTorch with CUDA
- Model checkpoint: the config must point to a directory containing `model.safetensors` (see configuration used by `--config`)
- For FP8 quantization: calibration data in one of the supported formats (see [Calibration data](#calibration-data))

## Basic usage

### Export only (no quantization)

```bash
python /home/colligo/colligo/models/colligo/models/di_imaging/multiedit/models/diffusion/export/dit_aoti_lazy_erase_fp8_calibrate.py \
  --config /home/colligo/colligo/models/colligo/models/di_imaging/multiedit/models/diffusion/export/config_erase_lazy.yaml \
  --output_dir /mnt/localssd/dit \
  --device h100
```

Output: `{output_dir}/dit.so` (e.g. `/mnt/localssd/dit/dit.so`).

### Export with FP8 quantization

1. Prepare calibration data (see [Calibration data](#calibration-data)).
2. Run with `--quantize_fp8`, `--calibration_data_path`, and optionally `--calibration_out_folder`:

```bash
python /home/colligo/colligo/models/colligo/models/di_imaging/multiedit/models/diffusion/export/dit_aoti_lazy_erase_fp8_calibrate.py \
  --config /home/colligo/colligo/models/colligo/models/di_imaging/multiedit/models/diffusion/export/config_erase_lazy.yaml \
  --output_dir /mnt/localssd/dit \
  --device h100 \
  --quantize_fp8 \
  --calibration_data_path /path/to/calibration/data \
  --calibration_out_folder /tmp/aoti_calibration/dit
```

- First run: performs calibration and writes observer state to `--calibration_out_folder` (e.g. `observers_ckpt.pt`).
- Later runs can reuse this by keeping the same `--calibration_out_folder`.
- Use `--save_quantized_checkpoint` to save `quantized_model.pt` for runtime loading.

### Run inference benchmark after export

To compile, export, and then run a short inference benchmark:

```bash
python /home/colligo/colligo/models/colligo/models/di_imaging/multiedit/models/diffusion/export/dit_aoti_lazy_erase_fp8_calibrate.py \
  --config /home/colligo/colligo/models/colligo/models/di_imaging/multiedit/models/diffusion/export/config_erase_lazy.yaml \
  --output_dir /mnt/localssd/dit \
  --device h100 \
  --run_inference_test
```

With quantization, save and use the quantized checkpoint for runtime benchmark:

```bash
python /home/colligo/colligo/models/colligo/models/di_imaging/multiedit/models/diffusion/export/dit_aoti_lazy_erase_fp8_calibrate.py \
  --config /home/colligo/colligo/models/colligo/models/di_imaging/multiedit/models/diffusion/export/config_erase_lazy.yaml \
  --output_dir /mnt/localssd/dit \
  --device h100 \
  --quantize_fp8 \
  --calibration_data_path /path/to/calibration/data \
  --calibration_out_folder /tmp/aoti_calibration/dit \
  --save_quantized_checkpoint \
  --run_inference_test
```

## CLI arguments

- `--config` (default: `config_erase_lazy.yaml`)
- `--output_dir` (default: `/mnt/localssd/dit`)
- `--device` (default: `h100`)
- `--quantize_fp8` (flag)
- `--calibration_data_path` (required for FP8 calibration)
- `--calibration_out_folder` (default: `/tmp/aoti_calibration/dit`)
- `--calibration_num_samples` (default: auto-detect all directory samples)
- `--dtype` (`bfloat16`, `float16`, `float32`; default: `bfloat16`)
- `--save_quantized_checkpoint` (flag)
- `--run_inference_test` (flag)

## Calibration data

When `--quantize_fp8` is set, provide `--calibration_data_path`. The script supports two formats.

### Directory-based (recommended)

- `calibration_data_path` is a directory.
- Each subdirectory is one sample and must contain:
  - `x.pt`  - input tensor `(1, seqlen, 2048)`
  - `x_pe.pt`  - positional encoding `(1, seqlen, 256)`
  - `t_pe.pt`  - time encoding `(1, seqlen, 2048)`
  - `x_out.pt` (optional) - target output

Samples are consumed in sorted subdirectory order. Use `--calibration_num_samples` to limit samples.

### File-based

- Each sample is a single file: `{calibration_data_path}/sample_{idx}.pt`.
- Each file is expected to be a dict with:
  - `args`: tuple `(x, x_pe, t_pe)`
  - `kwargs`: optional dict
  - `output`: optional target tensor

If neither format is available for a requested index, the script falls back to generated dummy samples.

## Quantization behavior

- Quantization target: `torch.nn.Linear` layers via `LinearObserverWrapper` and `QCONFIG_FP8_SYMMETRIC`.
- Included by name filter: layers containing `blocks.`.
- Excluded by name filter:
  - First and last transformer blocks: `tf_block_0.`, `tf_block_27.`
  - In blocks 1 through 26: selected attention and FFN weights (`attention.wq`, `attention.wk`, `attention.wo`, `feed_forward.w2`).
- Observer state is saved to `--calibration_out_folder`:
  - `observers_range_ckpt.pt`
  - `observers_ckpt.pt`

## Outputs

- Export engine: `{output_dir}/dit.so`
- Calibration outputs (when `--quantize_fp8`):
  - `{calibration_out_folder}/observers_range_ckpt.pt`
  - `{calibration_out_folder}/observers_ckpt.pt`
- Optional quantized checkpoint (when `--save_quantized_checkpoint`):
  - `{calibration_out_folder}/quantized_model.pt`

## Runtime test behavior

When `--run_inference_test` is enabled, the script runs a warmup and timed benchmark with random inputs after export.

- Without `--save_quantized_checkpoint`: runtime test loads original `model.safetensors` weights.
- With both `--quantize_fp8` and `--save_quantized_checkpoint`: runtime test loads `{calibration_out_folder}/quantized_model.pt`.
