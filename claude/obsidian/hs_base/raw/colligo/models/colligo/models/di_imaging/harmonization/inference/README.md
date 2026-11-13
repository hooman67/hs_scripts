# GenHarm: Generative Image Harmonization Inference App

GenHarm is an application for harmonizing foreground objects with background images using state-of-the-art diffusion models. This tool can automatically adjust lighting, color, and other visual aspects to create natural-looking composites.

## Setup Instructions

### Prerequisites
- Python 3.8+
- CUDA-compatible GPU
- Adobe Artifactory credentials (for accessing internal packages)
- Colligo dev environment is setup. If not please follow this [doc](https://wiki.corp.adobe.com/display/DISysEng/Set+up+Colligo+Development+Environment#installation-steps)

### Installation

1. Clone the repository and navigate to the project directory.

2. Set up environment variables for Adobe Artifactory access:
   ```bash
   export ARTIFACTORY_UW2_USER="your_username"
   export ARTIFACTORY_UW2_API_TOKEN="your_api_token"
   ```

3. Run the setup script to install all dependencies:
   ```bash
   ./setup.sh
   ```
   This script will:
   - Remove any local copy of the deprecated clio module
   - Install required PyPI packages from Adobe's internal repositories
   - Install all dependencies from requirements.txt
   - Install the current package in editable mode

## Model Serialization

### Converting PyTorch Models to ONNX and TensorRT

PyTorch or ONNX models need to be serialized for optimized inference. The conversion script can be found in the [MFM_mim repository](https://github.com/adobe-masking/MFM_mim), specifically the file [onnx_to_tensorrt.py](https://github.com/adobe-masking/MFM_mim/blob/master/tools/onnx_to_tensorrt.py).

#### ONNX to TensorRT Conversion Process

1. **Prerequisites for TensorRT Conversion:**
   - TensorRT 8.x or higher
   - CUDA 11.x or higher
   - Python packages: `tensorrt`, `onnx`, `onnxruntime-gpu`

2. **Conversion Steps:**
   ```bash
   # Clone the MFM_mim repository
   git clone https://github.com/adobe-masking/MFM_mim.git
   cd MFM_mim/tools
   
   # Convert ONNX model to TensorRT engine
   python onnx_to_tensorrt.py \
     --onnx_model path/to/your/model.onnx \
     --trt_engine path/to/output/engine.trt \
     --precision fp16 \
     --max_batch_size 1 \
     --input_shape "1,6,1536,1536"
   ```

3. **Key Parameters:**
   - `--onnx_model`: Path to the input ONNX model
   - `--trt_engine`: Output path for the TensorRT engine
   - `--precision`: Precision mode (fp16, fp32, int8)
   - `--max_batch_size`: Maximum batch size for the engine
   - `--input_shape`: Input tensor shape (batch, channels, height, width)

## Model Comparison and Validation

### Comparing ONNX vs TensorRT Results

To validate the accuracy of TensorRT conversion and ensure consistency between ONNX and TensorRT models, use the provided comparison scripts.

#### 1. Generate Comparison Results

Refer `refine_vit_compare.py` as a template to generate results from both ONNX and TensorRT models:

```bash
python src/inference/utils/refinement_vit_compare.py \
  --weights path/to/refine_vit_1536.onnx \
  --trt-weights path/to/refine_vit_1536.trt \
  --blur-size 7 \
  --output-directory ./result/onnx_trt_comparison
```

**REMINDER**: Save ONNX and TensorRT results with suffixes as `_onnx.png` and `_trt.png`

#### 2. Analyze Comparison Results

Use `compare_images.py` to analyze the differences between ONNX and TensorRT outputs:

```bash
python src/inference/utils/compare_images.py \
  --results_dir ./result/onnx_trt_comparison \
  --output_dir ./comparison_analysis \
  --index 0  # Optional: compare specific image pair
```


## Running GenHarm

### Basic Usage

Use the `run_gen_harmonize.sh` script to run the inference:

```bash
./run_gen_harmonize.sh
```

### Custom Configuration

You can customize the harmonization by modifying the parameters in `run_gen_harmonize.sh` or providing them directly to the Python script:

```bash
python ./src/inference/apps/inference_gen_harm.py \
  --base_ckpt "path/to/model/checkpoint.ckpt" \
  --prompt "Color, Lighting" \
  --config "./configs/config_inference_192.yaml" \
  --save_to "output_directory/" \
  --sampler "ddim_legacy" \
  --guidance "1" \
  --eta "1" \
  --num_images "1" \
  --timesteps "30" \
  --aspect_ratios "1/1" \
  --img_size "128" \
  --filelist "path/to/filelist.txt"
```

### Key Parameters

- `--base_ckpt`: Path to the model checkpoint
- `--config`: Path to the configuration file
- `--prompt`: Text prompt describing the harmonization (e.g., "Color, Lighting")
- `--save_to`: Directory to save the generated images
- `--num_images`: Number of images to generate per input
- `--timesteps`: Number of diffusion steps (higher = better quality but slower)
- `--guidance`: Classifier-free guidance weight
- `--img_size`: Output image size
- `--filelist`: Path to a file listing input images to process

## Input Format

The input filelist should contain paths to images with corresponding masks and background images. The expected format is one file path per line.

## Output

The harmonized images will be saved to the specified output directory. If the `--upload_to_s3` flag is used, images will also be uploaded to an S3 bucket, and the URL will be saved to the file specified by `--return_file_path`.

## Advanced Options

- `--ness_style`: Noise estimation scaling schedule (options: "accentuated", "smooth", "dreamy", "bold", "x", "y", "z")
- `--neg_prompt_style`: Negative prompt style for guidance (options: "1", "2", "none")
- `--ensemble`: Use model ensemble for better results (but slower inference)
- `--seed`: Set a specific seed for reproducible results

## Examples

### Harmonization
```bash
python ./src/inference/apps/inference_gen_harm.py \
  --base_ckpt "path/to/checkpoint.ckpt" \
  --prompt "Color, Lighting" \
  --config "./configs/config_inference_192.yaml" \
  --save_to "output/" \
  --filelist "input_files.txt"
```

### Model Comparison Workflow
```bash
# Step 1: Generate comparison results
python src/inference/utils/refinement_vit_compare.py \
  --weights models/refine_vit_1536.onnx \
  --trt-weights models/refine_vit_1536.trt \
  --output-directory ./comparison_results

# Step 2: Analyze differences
python src/inference/utils/compare_images.py \
  --results_dir ./comparison_results \
  --output_dir ./analysis_results

# Step 3: Review results
cat ./analysis_results/comparison_report.json
```

