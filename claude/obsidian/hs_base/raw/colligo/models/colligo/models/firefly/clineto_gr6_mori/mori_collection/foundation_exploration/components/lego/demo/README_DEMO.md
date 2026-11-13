# Firefly Image 5 Demo

A complete demonstration of the Firefly Image 5 diffusion model system with text-to-image generation, instruct-based image editing, and model comparison capabilities.

## 🚀 Quick Start

### Installation

Run the installation script to set up the demo environment:

```bash
src/foundation_exploration/components/lego/demo/install_demo.sh
```

This script will:
- Create a dedicated virtual environment (`mori-venv-vllm`)
- Install vLLM and required dependencies
- Set up Flask and Streamlit packages

### Starting the Demo

**Option 1: Single Model (Default)**

Run the startup script to launch with one model server:

```bash
src/foundation_exploration/components/lego/demo/start_servers.sh
```

This will start:
- Model 1 server on port 8002
- VLM server (remote) for prompt enhancement

**Option 2: Model Comparison**

To enable side-by-side model comparison (e.g., student vs teacher, different checkpoints):

```bash
src/foundation_exploration/components/lego/demo/start_servers.sh --with-model2
```

This will start:
- Model 1 server on port 8002
- Model 2 server on port 8003
- VLM server (remote) for prompt enhancement

**Note:** When starting both servers, they are launched in parallel to speed up initialization. The script waits for both to be ready before completing.

To use different checkpoints for Model 2, set environment variables before running:

```bash
export MODEL2_CKPT_PATH="s3://path/to/your/checkpoint/"
export MODEL2_CONFIG_PATH="configs/your/config.yaml"
./start_servers.sh --with-model2
```

The demo will be available at: **http://localhost:8501**

## 🎯 How the Demo Works

The demo consists of interconnected components that work together to provide an advanced text-to-image generation experience:

• **Model Server(s) (Ports 8002, 8003)**: The core text-to-image generation engine powered by the Lego diffusion model, running in distributed mode across 4 GPUs using PyTorch's `torchrun`. Provides REST API endpoints for image generation and instruct-based editing. Can run two servers simultaneously for model comparison.

• **VLM Server (Remote)**: An intelligent prompt enhancement service using Qwen3-VL that automatically analyzes images and generates detailed, structured instructions and captions optimized for image editing, including scene descriptions, lighting, and composition details.

• **Streamlit Web Interface**: The user-facing application that orchestrates requests between services, featuring multiple pages:
  - **T2I Generation**: Generate images from text prompts
  - **Instruct Editing**: Edit images with natural language instructions
  - **Batch Editing**: Process multiple images in batch
  - **Model Comparison**: Side-by-side comparison of two model checkpoints
  - **T2I Multistep VLM**: Advanced multi-stage prompt refinement

## ⚖️ Model Comparison Feature

The comparison page allows you to run the same editing task on two different models simultaneously:

**Use Cases:**
- Compare student vs teacher checkpoints
- Evaluate different training iterations
- A/B test model configurations
- Quality assurance across model versions

**How to Use:**
1. Start both servers: `./start_servers.sh --with-model2`
2. Navigate to "Model Comparison" page in Streamlit
3. Upload an image and provide an edit instruction
4. View results side-by-side: Model 1 on the left, Model 2 on the right

**Requirements:**
- 8 GPUs total (GPUs 0-3 for Model 1, GPUs 4-7 for Model 2)
- Both models receive identical inputs for fair comparison
- Results include timing metrics for performance comparison
- GPU allocation is automatic - no manual configuration needed

## 🛠️ Manual Server Management

If you need to start servers individually:

### Model 1 Server
```bash
# Activate environment first
source /mnt/localssd/mori-venv/bin/activate

# Start Model 1 server on GPUs 0-3
CUDA_VISIBLE_DEVICES=0,1,2,3 torchrun \
  --nproc_per_node=4 \
  --master_port=29500 \
  --rdzv_backend=c10d \
  --rdzv_endpoint=localhost:29400 \
  --rdzv_id=model1_$(date +%s) \
  src/foundation_exploration/components/lego/demo/model_server.py \
  --config_path configs/lego/diffusion/glow_worm/beta/glow_worm_gen45_11b_prod.yaml \
  --ckpt_path s3://path/to/checkpoint/ \
  --t2i_inference_config_name glow_worm_MEIE_2k_testset_non_ema \
  --edit_inference_config_name glow_worm_MEIE_2k_testset_non_ema \
  --port 8002
```

### Model 2 Server (For Comparison)
```bash
# Activate environment first
source /mnt/localssd/mori-venv/bin/activate

# Start Model 2 server on GPUs 4-7
CUDA_VISIBLE_DEVICES=4,5,6,7 torchrun \
  --nproc_per_node=4 \
  --master_port=29501 \
  --rdzv_backend=c10d \
  --rdzv_endpoint=localhost:29401 \
  --rdzv_id=model2_$(date +%s) \
  src/foundation_exploration/components/lego/demo/model_server.py \
  --config_path configs/lego/diffusion/glow_worm/beta/mmd_8step_inference.yaml \
  --ckpt_path s3://path/to/different/checkpoint/ \
  --t2i_inference_config_name glow_worm_image_reference_scap_ema_1024px \
  --edit_inference_config_name glow_worm_image_reference_scap_ema_1024px \
  --port 8003
```

**Important Notes:**
- Use `CUDA_VISIBLE_DEVICES` to assign specific GPUs to each server
- Use different `--master_port` values for each server (29500 vs 29501)
- Use different `--rdzv_endpoint` ports for each server (29400 vs 29401) to avoid rendezvous conflicts
- Each server needs a unique `--rdzv_id` for proper torchrun coordination
- Model 1 uses GPUs 0-3, Model 2 uses GPUs 4-7 (configurable via `MODEL1_GPUS`/`MODEL2_GPUS` in script)
- `--t2i_inference_config_name` specifies which inference config to use for text-to-image generation
- `--edit_inference_config_name` specifies which inference config to use for image editing
- The config names must match a `name` field in the `inference:` section of the YAML config file

### Streamlit App
```bash
# Open a tmux session
tmux new -s streamlit_demo

# Activate environment first
source /mnt/localssd/mori-venv/bin/activate

# Start Streamlit interface
streamlit run src/foundation_exploration/components/lego/demo/streamlit_client_app.py \
  --server.port 8501 \
  --server.baseUrlPath / \
  --server.enableXsrfProtection=false \
  --server.enableCORS=false
```

## 📝 Notes

- **Single model mode**: Requires 4 GPUs (GPUs 0-3 by default)
- **Comparison mode**: Requires 8 GPUs (GPUs 0-3 for Model 1, GPUs 4-7 for Model 2)
- GPU allocation is handled automatically via `CUDA_VISIBLE_DEVICES`
- VLM inference uses a remote server at `pluto-prod-skatakol-colligo-vllm-c-0:8000`
- Server logs are saved to `model1_server.log` and `model2_server.log` (if enabled)
- **Torchrun isolation**: Each server uses separate coordination ports to avoid conflicts:
  - Model 1: `--master_port=29500`, `--rdzv_endpoint=localhost:29400`
  - Model 2: `--master_port=29501`, `--rdzv_endpoint=localhost:29401`
- Use Ctrl+C to stop the demo when running with `start_servers.sh`
- To customize GPU allocation, edit `MODEL1_GPUS` and `MODEL2_GPUS` variables in `start_servers.sh`
- When Model 1 is already running, running `./start_servers.sh --with-model2` will only start Model 2 (no-op for Model 1)
- **Parallel startup**: When starting multiple servers, they launch simultaneously for faster initialization (~50% time reduction)
