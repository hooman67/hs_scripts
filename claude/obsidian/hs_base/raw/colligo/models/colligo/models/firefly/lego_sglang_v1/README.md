# Lego SGLang v1

SGLang 0.5.9-based inference worker for Qwen3.5-27B-FP8 model (MLLM backend for the `lego_v1` pipeline).

## Overview

Drop-in alternative to `lego_vllm_v4` using SGLang's in-process Engine instead of vLLM. Uses:

- **SGLang 0.5.9** for efficient LLM inference with structured generation
- **Qwen3.5-27B-FP8** hybrid linear-attention model
- **FlashInfer 0.6.3** attention backend (Triton backend enabled)
- **PyTorch 2.9.1+cu128** with CUDA 12.8
- **Python 3.12+** with numpy 2.x
- **Custom env**: `sglang_0_5_9` (separate from `dev`/`dev2_0`/`vllm_*` due to numpy 2.x and torch ABI conflicts)

## Architecture

```
lego_sglang_v1/
├── LegoSGLang.py          # Main worker implementation
├── build.py               # Deployment configuration
├── types.py               # Type definitions and endpoint registration
├── colligo.yaml           # Package metadata (custom_pyenv: sglang_0_5_9)
├── configs/
│   └── prompt_set/        # System prompts (shared with vLLM workers)
└── scripts/
    └── batch_optimizer.py # Performance benchmarking tool
```

## Key Features

1. **Three Inference Workflows**
   - **T2I (Text-to-Image)**: Generate image descriptions from text prompts
   - **IE (Instruct Edit)**: Generate editing instructions for images
   - **Layers**: Generate layered scene descriptions

2. **Same Prompts as vLLM**: Uses identical system prompts for direct performance comparison

3. **Batch Optimization**: Benchmarking script measuring throughput, latency (p50/p95/p99), TTFT, and cache efficiency

## Environment Setup

```bash
./m deps.enable sglang_0_5_9
./m deps.lock --env sglang_0_5_9
./m package.rhode --spec lego_v1
```

## Deployment Configuration

- Model: `Qwen/Qwen3.5-27B-FP8` (27B parameters, FP8 quantized)
- GPU: 72GB VRAM, single GPU (TP=1)
- Max concurrent requests: 32
- Context length: 16384 tokens
- Memory allocation: 85% static reservation

## API Endpoint

```
POST http://<host>/v1/lego_sglang_v1
Content-Type: application/json

{
  "workflow": "t2i",
  "request": {
    "t2i_workflow_prompt": "An astronaut riding a camel on Mars",
    "seed": 0,
    "sampling_params": {"temperature": 1.0, "max_tokens": 512, "seed": 0}
  }
}
```
