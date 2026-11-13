# WAN 2.2 Video Generation Pipelines

Video generation models based on WAN (Wan AI Network) 2.2 architecture.

## Pipelines

### `wan_22_lucy_pipeline.py` - Base WAN 2.2
**Endpoint:** `v1/wan/v22`

Full WAN 2.2 model with timeline composition, keyframes, and reference images.

### `wan_22_lucy_pipeline_distill.py` - Distilled WAN 2.2
**Endpoint:** `v1/wan/v22_distill`

Distilled (faster) version of WAN 2.2 for **Foundry Studio depth control**.
- Lightning-merged weights for faster inference
- Optimized for timeline-based video editing workflows

### `wan_22_lucy_pipeline_upsample.py` - NBCU Upsampler
**Endpoint:** `v1/wan/v22_nbcu_upsampler`

Video resizing pipeline with **NBCU-trained VACE adapters** for quality enhancement.

**Workflow:**
1. Load input video → auto-detect fps and frame count
2. Resize each frame to target size (LANCZOS interpolation)
3. Apply VACE refinement for quality enhancement
4. Output video with same fps and frame count as input

**API Input:**
```json
{
  "inputVideo": {"id": "uploaded-video-id"},
  "prompt": "upsample",
  "widthPx": 1280,
  "heightPx": 720,
  "seed": 42,
  "output": {}
}
```

**Fields:**
- `inputVideo` (required) - Video to resize
- `prompt` (optional) - Text or structured dict, defaults to `"upsample"`
- `widthPx`, `heightPx` (required) - Target dimensions (16-2048, multiple of 16)
- `seed` (optional) - Random seed
- `output` (optional) - Output settings (ACP upload, etc.)

**Use cases:**
- Upsampling: 480p → 720p (primary training target)
- Downsampling: 1080p → 720p (works but not optimized)

**Lightning mode (optional):**
- Set `USE_LIGHTNING=true` environment variable to use distilled (faster) DIT weights
- Reduces inference time by ~50% with similar quality
- Enabled via: `export USE_LIGHTNING=true` before starting worker

**Performance:**
- Standard: ~180s per 15 frames
- 720p, 81 frames: 1404s (~23 minutes)
- 720p, 113 frames: 2337s (~39 minutes)
- Lightning (estimated): faster
- 720p, 113 frames: 176s

upsampler weights:
<checkpoint_dir>/                                                                                                                                         
  ├── PAI/                                                                                                                                                  
  │   └── Wan2.2-VACE-Fun-A14B/                                                                                                                             
  │       ├── Wan2.1_VAE.pth                                                                                                                                
  │       ├── models_t5_umt5-xxl-enc-bf16.pth                                                                                                               
  │       ├── high_noise_model/                                                                                                                             
  │       │   └── diffusion_pytorch_model.safetensors                                                                                                       
  │       └── low_noise_model/                                                                                                                              
  │           └── diffusion_pytorch_model.safetensors                                                                                                       
  ├── Wan-AI/                                                                                                                                               
  │   ├── Wan2.1-T2V-1.3B/                                                                                                                                  
  │   │   └── google/                                                                                                                                       
  │   │       └── umt5-xxl/                                                                                                                                 
  │   │           ├── special_tokens_map.json                                                                                                               
  │   │           ├── spiece.model                                                                                                                          
  │   │           ├── tokenizer.json                                                                                                                        
  │   │           └── tokenizer_config.json                                                                                                                 
  │   └── Wan2.2-I2V-A14B/                                                                                                                                  
  │       ├── high_noise_model/                                                                                                                             
  │       │   ├── diffusion_pytorch_model-00001-of-00006.safetensors                                                                                        
  │       │   ├── diffusion_pytorch_model-00002-of-00006.safetensors                                                                                        
  │       │   ├── diffusion_pytorch_model-00003-of-00006.safetensors                                                                                        
  │       │   ├── diffusion_pytorch_model-00004-of-00006.safetensors                                                                                        
  │       │   ├── diffusion_pytorch_model-00005-of-00006.safetensors                                                                                        
  │       │   └── diffusion_pytorch_model-00006-of-00006.safetensors                                                                                        
  │       └── low_noise_model/                                                                                                                              
  │           ├── diffusion_pytorch_model-00001-of-00006.safetensors                                                                                        
  │           ├── diffusion_pytorch_model-00002-of-00006.safetensors                                                                                        
  │           ├── diffusion_pytorch_model-00003-of-00006.safetensors                                                                                        
  │           ├── diffusion_pytorch_model-00004-of-00006.safetensors                                                                                        
  │           ├── diffusion_pytorch_model-00005-of-00006.safetensors                                                                                        
  │           └── diffusion_pytorch_model-00006-of-00006.safetensors                                                                                        
  ├── lightning_merged/                                                                                                                                     
  │   ├── high_noise_model.safetensors                                                                                                                      
  │   └── low_noise_model.safetensors                                                                                                                       
  └── vace_upsampler/                                                                                                                                       
      ├── high_noise.safetensors                                                                                                                            
      └── low_noise.safetensors                                                                                                                             
                  
## Checkpoints

- `wan_distill_v1.json` - Base DiT + distilled weights
- `wan_nbcu_upsampler_v1.json` - Base DiT + NBCU VACE adapters (in `vace_upsampler/`)

## FSDP Variant

`wan_22_lucy_pipeline_fsdp.py` - Multi-GPU FSDP (Fully Sharded Data Parallel) version for 4-GPU setups.
