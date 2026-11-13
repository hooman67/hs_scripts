# Brewmaster Evaluation System

Automated evaluation for GenAI models with comprehensive metric support for text-to-image, text-to-video, image-to-video, and video-to-video tasks.

**Status**: Production Ready ✅  
**Latest Update**: Enhanced with 6 new temporal consistency metrics (Nov 2025)

---

## Quick Start

### Run Evaluation from Master JSON (Recommended)

```python
from colligo.models.firefly.brewmaster.eval_metrics.runner import EvaluationRunner
from colligo.models.firefly.brewmaster.backend.services.master_json_manager import MasterJSONManager

# Load Master JSON
manager = MasterJSONManager(task_type="t2v")
master_json_data = manager.load_or_create("t2v_demo_v1.0")

# Run evaluation
runner = EvaluationRunner()
asset_metrics = runner.run_from_master_json(
    master_json_data=master_json_data,
    model_ids=["58b51c52-2a98-4039-b202-f6ae530f68f7"],
    dataset_id="4de06df3-9769-4433-aa78-75dccd69f490",
    task_type="t2v",  # or "v2v", "i2v", "t2i"
    device="cuda"
)

# Results: {asset_id: {metric_name: [scores], ...}, ...}
print(asset_metrics)
# {
#   1: {"temporal_consistency": [0.9106], "motion_smoothness": [0.9709]},
#   2: {"temporal_consistency": [0.9723], "motion_smoothness": [0.9423]},
#   ...
# }
```

**What happens:**
- ✅ Videos downloaded from S3 automatically
- ✅ Reference videos loaded for V2V/I2V tasks
- ✅ Prompts matched via `content_id`
- ✅ Metrics calculated for each asset
- ✅ Results ready to write back to Master JSON

### Run Video Evaluation (Traditional)

```bash
cd /Users/jasondong/colligo
PYTHONPATH=/Users/jasondong/colligo python models/colligo/models/firefly/brewmaster/eval_metrics/examples/run_evaluation.py
```

This will evaluate your models and generate:
- JSON report with all metric scores
- Markdown report with interpretations and comparison
- Progress tracking and warnings for dimension mismatches
- Per-model results organized by task type

### Example Structure

```
outputs/
├── text_to_video_generic/     # Task name (no hash)
│   ├── dataset_001/
│   │   ├── model_1_results.json
│   │   └── model_2_results.json
│   └── dataset_002/
│       ├── model_1_results.json
│       └── model_2_results.json
└── image_to_video_generic/
    ├── dataset_003/
    │   └── model_3_results.json
    └── dataset_004/
        └── model_3_results.json
```

---

## Available Metrics

### Text-to-Video (T2V) Metrics

**Deterministic Temporal Metrics (9 metrics)** - No external models required:
- ✅ **Temporal Consistency** - Frame-to-frame stability measurement
- ✅ **Temporal SSIM** - Structural similarity index across time
- ✅ **Motion Smoothness** - Optical flow jitter analysis
- ✅ **Motion Magnitude** - Amount of motion detection
- ✅ **Warping Error** - Optical flow consistency (NEW)
- ✅ **Frame Interpolation Quality** - Motion smoothness via interpolation (NEW)
- ✅ **Flickering Score** - Temporal brightness artifact detection (NEW)
- ✅ **Scene Cut Detection** - Abrupt transition detection (NEW)
- ✅ **Color Consistency** - Temporal color stability (NEW)

**Model-based Metrics (2 metrics)** - Require PyTorch models (free):
- ✅ FVD (Fréchet Video Distance) - Video quality and diversity
- ✅ LPIPS (Learned Perceptual Image Patch Similarity) - Perceptual quality

**Total: 11 metrics for T2V** ✅

### Image-to-Video (I2V) Metrics

**First-Frame Consistency (6 metrics)** - Measure fidelity to input image:
- ✅ PSNR - Peak signal-to-noise ratio
- ✅ SSIM - Structural similarity
- ✅ LPIPS - Learned perceptual similarity
- ✅ Histogram KL Divergence - Distribution similarity
- ✅ Histogram Chi-Square - Statistical distance
- ✅ Histogram Wasserstein - Earth mover's distance

**Temporal Quality Metrics (9 metrics)** - Same as T2V temporal metrics above

**Model-based Metrics (1 metric)**:
- ✅ FVD - Video generation quality

**Total: 16 metrics for I2V** ✅

### Video-to-Video (V2V) Metrics

**Frame-Level Quality (3 metrics)**:
- ✅ PSNR - Frame reconstruction quality
- ✅ SSIM - Structural similarity per frame
- ✅ LPIPS - Perceptual similarity per frame

**Temporal Quality (9 metrics)** - Same as T2V temporal metrics

**Model-based (1 metric)**:
- ✅ FVD - Video transformation quality

**Total: 13 metrics for V2V** ✅

### Text-to-Image (T2I) Metrics

**Image Quality (12 metrics)** - Deterministic:
- ✅ RMS Contrast - Local contrast measurement
- ✅ Color Entropy - Color diversity
- ✅ PSNR, SSIM - Quality and similarity
- ✅ Histogram metrics (KL, Chi-Square, Wasserstein)
- ✅ Edge Density, Sharpness, Gradient Magnitude
- ✅ Local Binary Pattern, GLCM Texture

**Model-based (2 metrics)**:
- ✅ FID (Fréchet Inception Distance)
- ✅ LPIPS (Perceptual similarity)

**Total: 14 metrics for T2I** ✅

---

## Task Types

### Text-to-Video (T2V)
- **Input**: Text prompts + generated videos
- **Reference**: No reference videos needed
- **Metrics**: 9 deterministic temporal + 2 model-based
- **Use case**: Evaluating text-to-video generation models
- **Task ID**: `text_to_video_generic`

### Image-to-Video (I2V)
- **Input**: Input images + generated videos
- **Reference**: Input images for first-frame consistency
- **Metrics**: 6 first-frame + 9 temporal + 1 model-based
- **Use case**: Animating still images, motion generation
- **Task ID**: `image_to_video_generic`

### Video-to-Video (V2V)
- **Input**: Reference videos + generated videos
- **Reference**: Reference videos required
- **Metrics**: 3 frame-level + 9 temporal + 1 model-based
- **Use case**: Video editing, style transfer, super-resolution, enhancement
- **Task ID**: `video_to_video_generic`

### Text-to-Image (T2I)
- **Input**: Text prompts + generated images
- **Reference**: Optional reference images
- **Metrics**: 12 deterministic + 2 model-based
- **Use case**: Evaluating text-to-image generation models
- **Task ID**: `text_to_image_generic`

---

## Dependencies & Installation

### Minimal Environment (23 Deterministic Metrics)
**No GPU required, works on CPU**

```bash
pip install numpy pillow scipy opencv-python
```

Provides all deterministic metrics for comprehensive evaluation without any external models.

### Standard Environment (25 Total Metrics)
**Recommended for complete evaluation**

```bash
pip install numpy pillow scipy opencv-python torch torchvision
```

Adds model-based metrics:
- FID (Fréchet Inception Distance)
- LPIPS (Learned Perceptual Similarity)
- FVD (Fréchet Video Distance)

### Full Environment
Same as standard - all metrics available with free, open-source dependencies.

**Note**: No API keys or paid services required! All metrics use freely available models.

---

## Reporting Features

### Per-Metric Details
- Mean, Std, Min, Max, Median for each model
- Range and "better" direction (higher/lower)
- Scientific notation for very small values

### Summary Table
- Side-by-side model comparison
- Best model per metric
- "Tie" when models perform similarly

### Warnings
- Dimension mismatches (resolution, FPS, duration)
- Failed metrics (non-halting evaluation)
- All warnings logged in report

---

## Integration with Brewmaster Master JSON

### New Interface: `run_from_master_json()`

**Status**: ✅ Production Ready (Dec 2025)

The evaluation system now provides a **direct Master JSON interface** for seamless integration with Brewmaster workflows. This eliminates the need for symlinks and manual file management.

### Quick Example

```python
from colligo.models.firefly.brewmaster.eval_metrics.runner import EvaluationRunner

# Initialize runner
runner = EvaluationRunner()

# Run evaluation directly from Master JSON
asset_metrics = runner.run_from_master_json(
    master_json_data=master_json_data,  # Master JSON dict
    model_ids=["58b51c52-2a98-4039-b202-f6ae530f68f7"],
    dataset_id="4de06df3-9769-4433-aa78-75dccd69f490",
    task_type="t2v",  # Determines evaluation mode
    bypass_metrics=["clip_score", "fvd"],  # Optional: skip expensive metrics
    device="cuda",
)

# Returns: {asset_id: {metric_name: [scores], ...}, ...}
# {
#   1: {"temporal_consistency": [0.9106], "motion_smoothness": [0.9709]},
#   2: {"temporal_consistency": [0.9723], "motion_smoothness": [0.9423]},
#   ...
# }
```

### What It Does

1. **Filters assets** by `model_ids` and `dataset_id`
2. **Downloads videos** from S3 URLs in Master JSON (`assets[].path`)
3. **Loads reference videos/images** for V2V/I2V tasks (from `contents[].ref_paths`)
4. **Matches prompts** using `content_id` (from `contents[].prompt`)
5. **Calculates metrics** for each asset
6. **Returns organized results** mapping `asset_id` to metric scores

### Task Type Handling

The interface automatically detects **no-reference vs with-reference** evaluation:

#### T2V/T2I (No-Reference)
```python
# Master JSON structure
{
  "contents": [{"content_id": 1, "prompt": "...", "ref_paths": {}}],  # Empty ref_paths
  "assets": [{"asset_id": 1, "path": "s3://generated_video.mp4", ...}]
}

# Evaluation behavior
- Uses same video as both prediction and reference
- Extracts absolute quality from metadata (e.g., prediction_smoothness)
- Returns: temporal_consistency: 0.9106 (absolute quality score)
```

#### V2V/I2V (With-Reference)
```python
# Master JSON structure
{
  "contents": [
    {
      "content_id": 1,
      "prompt": "...",
      "ref_paths": {"videos": ["s3://reference_video.mp4"]}  # Has reference
    }
  ],
  "assets": [{"asset_id": 1, "path": "s3://generated_video.mp4", ...}]
}

# Evaluation behavior
- Downloads both generated AND reference videos
- Compares generated to reference
- Returns: temporal_consistency: 0.0523 (difference from reference)
```

### Benefits Over Traditional Interface

**Before (Symlink Approach):**
```python
# ❌ Complex setup
create_symlinks(videos, output_dir)        # Manual file management
write_prompts_txt(prompts, output_dir)     # Sequential index mapping
runner.run(task_name, model_directories, prompts_file)

# Issues:
# - Index mapping bugs (off-by-one errors)
# - Doesn't support reference videos
# - ~200 lines of boilerplate code
```

**After (Master JSON Interface):**
```python
# ✅ Direct integration
asset_metrics = runner.run_from_master_json(
    master_json_data=master_json,
    model_ids=[model_id],
    task_type="t2v"
)

# Benefits:
# - No symlinks, no index mapping
# - Supports all task types (T2V, V2V, I2V, T2I)
# - Handles reference videos/images automatically
# - Cleaner, more reliable
```

### Supported Task Types

| Task Type | Reference Needed | Source | Evaluation Mode |
|-----------|------------------|--------|-----------------|
| **T2V** | No | `ref_paths: {}` | No-reference (absolute quality) |
| **V2V** | Yes | `ref_paths.videos` | With-reference (comparison) |
| **I2V** | Yes | `ref_paths.images` | With-reference (first-frame) |
| **T2I** | No | `ref_paths: {}` | No-reference (absolute quality) |
| **I2I** | Yes | `ref_paths.images` | With-reference (comparison) |

### Master JSON Structure

**Required Structure:**
```json
{
  "models": [
    {
      "model_id": "58b51c52-2a98-4039-b202-f6ae530f68f7",
      "model_identifier": "t2v_model_1.9"
    }
  ],
  "contents": [
    {
      "content_id": 1,
      "prompt": "A dog running in a field",
      "ref_paths": {
        "videos": ["s3://ref_video.mp4"],  // For V2V/I2V
        "images": ["s3://ref_image.jpg"]   // For I2V/I2I
      },
      "metadata": []
    }
  ],
  "assets": [
    {
      "content_id": 1,
      "asset_id": 1,
      "model_id": "58b51c52-2a98-4039-b202-f6ae530f68f7",
      "path": "s3://clio.../outputs/video.mp4",  // S3 URL or local path
      "error_code": null,
      "metric_scores": {
        "temporal_consistency": [0.9106],  // Populated by evaluation
        "motion_smoothness": [0.9709]
      }
    }
  ]
}
```

### Advanced Features

#### 1. Asset Filtering
```python
# Only evaluate specific models
asset_metrics = runner.run_from_master_json(
    master_json_data=master_json,
    model_ids=["model-A", "model-B"],  # Only these models
    dataset_id=dataset_id,
    task_type="t2v"
)

# Result: Only assets with model-A or model-B are evaluated
```

#### 2. Incremental Evaluation
```python
# Skip expensive metrics (calculated separately)
asset_metrics = runner.run_from_master_json(
    master_json_data=master_json,
    model_ids=[model_id],
    dataset_id=dataset_id,
    task_type="t2v",
    bypass_metrics=["clip_score", "fvd", "lpips"]  # Skip these
)
```

#### 3. Device Selection
```python
# Choose device
asset_metrics = runner.run_from_master_json(
    master_json_data=master_json,
    model_ids=[model_id],
    dataset_id=dataset_id,
    task_type="t2v",
    device="cuda"  # or "cpu" or "auto"
)
```

#### 4. Custom Temp Directory
```python
# Use custom temp directory for downloads
asset_metrics = runner.run_from_master_json(
    master_json_data=master_json,
    model_ids=[model_id],
    dataset_id=dataset_id,
    task_type="t2v",
    temp_dir=Path("/custom/temp/dir")  # Custom location
)
```

### Metric Value Extraction

**For No-Reference Tasks (T2V/T2I):**

Metrics that compute differences (like `motion_smoothness`) store both absolute values:
```python
# Metric returns
result = {
    "value": 0.0,  # Difference (0 when pred==ref)
    "metadata": {
        "prediction_smoothness": 0.9709,  # ← Absolute quality (what we want!)
        "reference_smoothness": 0.9709
    }
}

# Interface extracts
score = result.metadata["prediction_smoothness"]  # 0.9709
```

**For With-Reference Tasks (V2V/I2V):**

Metrics compute actual differences:
```python
# Metric returns
result = {
    "value": 0.0523,  # ← Actual difference (what we want!)
    "metadata": {
        "prediction_smoothness": 0.9709,
        "reference_smoothness": 0.9186
    }
}

# Interface uses
score = result["value"]  # 0.0523
```

### Integration with Brewmaster

The Master JSON interface is fully integrated with Brewmaster's evaluation pipeline:

```python
# backend/services/comparison/main.py

# Run evaluation
eval_results = run_eval_system_evaluation(
    data_dir=data_dir,
    output_dir=output_dir,
    model_ids=model_ids,
    dataset_ids=dataset_ids,
    metric_ids=["temporal_consistency", "motion_smoothness"],
    task_type="t2v",
    master_json_manager=master_json_manager,  # Pass manager
    dataset_names=dataset_names,
    dataset_versions=dataset_versions
)

# Metrics automatically written to Master JSON
# - Assets from S3 downloaded automatically
# - Reference videos handled automatically
# - Results persisted in Master JSON
```

### Error Handling

**Graceful Degradation:**
```python
# Missing video - logs warning, continues with other assets
# Failed download - logs error, skips asset
# Missing prompt - logs warning, skips asset
# Metric failure - logs error, continues with other metrics

# Result: Partial evaluation succeeds, only failed assets skipped
```

### Performance Considerations

**S3 Downloads:**
- Videos downloaded on-demand from S3
- Cached in temporary directory
- Cleaned up after evaluation (optional)

**Memory:**
- Videos loaded one at a time (not all in memory)
- Frames released after metric calculation
- Suitable for large datasets

**Speed:**
- ~2-5 minutes for 10 videos with 5 metrics (GPU)
- ~5-10 minutes on CPU
- Parallel processing within metrics (where applicable)

### Troubleshooting

**Issue: All metrics return 0.0**
```
Cause: Not extracting absolute values for T2V
Fix: Use task_type="t2v" (automatic extraction)
```

**Issue: FileNotFoundError for reference videos**
```
Cause: Invalid S3 URLs in ref_paths
Fix: Validate dataset reference paths before evaluation
```

**Issue: Metrics fail for V2V**
```
Cause: Reference videos not loaded
Fix: Check ref_paths.videos is populated in Master JSON
```

### API Reference

```python
def run_from_master_json(
    self,
    master_json_data: dict[str, Any],
    model_ids: list[str],
    dataset_id: str,
    task_type: str = "t2v",
    bypass_metrics: list[str] | None = None,
    temp_dir: Path | None = None,
    device: str = "auto",
) -> dict[str, Any]:
    """
    Run evaluation directly from Master JSON structure.

    Args:
        master_json_data: Master JSON dict with 'models', 'contents', and 'assets'
        model_ids: List of model IDs to evaluate
        dataset_id: Dataset ID for identification
        task_type: Task type ("t2v", "v2v", "i2v", "t2i", "i2i")
        bypass_metrics: Optional list of metrics to skip
        temp_dir: Temporary directory for downloaded videos
        device: Device to run on ("auto", "cuda", "cpu")

    Returns:
        Dictionary mapping asset_id to metric scores:
        {
            1: {"temporal_consistency": [0.9106], "motion_smoothness": [0.9709]},
            2: {"temporal_consistency": [0.9723], "motion_smoothness": [0.9423]},
            ...
        }
    """
```

### Migration Guide

**From Traditional Interface:**
```python
# OLD
create_model_directories()
create_symlinks()
write_prompts_txt()
runner.run(task_name, model_directories, prompts_file)

# NEW
runner.run_from_master_json(
    master_json_data=master_json,
    model_ids=model_ids,
    dataset_id=dataset_id,
    task_type="t2v"
)

# Changes:
# - Remove all symlink creation code
# - Remove prompts.txt generation
# - Remove index mapping logic
# - Pass Master JSON directly
```

### See Also

- **Complete Flow:** `BREWMASTER_COMPLETE_FLOW.md`
- **Interface Guide:** `MASTER_JSON_EVAL_INTERFACE.md`
- **Architecture:** `KEY_ARCHITECTURE_NOTES.md`

---

## File Structure

```
brewmaster/eval_metrics/
├── README.md                              # This file
├── config/
│   ├── metrics.yaml                       # Metric definitions and requirements
│   ├── tasks.yaml                         # Task configurations
│   └── metrics_registry.py                # Metric catalog
├── metrics/
│   ├── base.py                            # Base metric class
│   ├── video/                             # Video metrics
│   │   ├── temporal_consistency.py        # Temporal stability
│   │   ├── temporal_ssim.py               # Temporal SSIM
│   │   ├── motion_metrics.py              # Motion analysis
│   │   ├── warping_error.py               # 🆕 Optical flow consistency
│   │   ├── temporal_artifacts.py          # 🆕 Flickering & color consistency
│   │   ├── scene_analysis.py              # 🆕 Scene cuts & interpolation
│   │   ├── fvd.py                         # Fréchet Video Distance
│   │   └── lpips_video.py                 # Perceptual similarity
│   └── image/                             # Image metrics (for T2I/I2V)
│       ├── psnr.py                        # Peak signal-to-noise ratio
│       ├── ssim.py                        # Structural similarity
│       ├── lpips.py                       # Perceptual similarity
│       ├── fid.py                         # Fréchet Inception Distance
│       ├── histogram_metrics.py           # Distribution metrics
│       ├── texture_metrics.py             # Texture analysis
│       └── edge_metrics.py                # Edge and sharpness
├── backend/services/eval/
│   ├── brewmaster_job_executor.py         # Main job execution
│   ├── eval_config_manager.py             # Configuration management
│   └── result_processor.py                # Result processing
├── reporting.py                           # Report generation
└── requirements_video_metrics.txt         # Dependencies
```

---

## Validation

Run validation to check everything works:

```bash
cd /Users/jasondong/colligo
PYTHONPATH=/Users/jasondong/colligo python pylibs/colligo/eval/validation/run_validation.py --comprehensive
```

---

## Metrics Reference

### New Temporal Consistency Metrics (2025)

#### Warping Error
- **What**: Optical flow warping consistency between frames
- **Research**: Lai et al. (2018), Farnebäck (2003)
- **Range**: [0, ∞)
- **Better**: Lower (better temporal consistency)
- **Implementation**: `metrics/video/warping_error.py`

#### Flickering Score
- **What**: Detects temporal brightness flickering artifacts
- **Research**: Bonneel et al. (2015), Lai et al. (2018)
- **Range**: [0, ∞)
- **Better**: Lower (less flickering)
- **Implementation**: `metrics/video/temporal_artifacts.py`

#### Color Consistency
- **What**: Measures color stability across frames
- **Research**: Bonneel et al. (2015), Yao et al. (2020)
- **Range**: [0, 1]
- **Better**: Higher (more stable colors)
- **Implementation**: `metrics/video/temporal_artifacts.py`

#### Scene Cut Detection
- **What**: Detects abrupt scene transitions
- **Research**: Boreczky & Rowe (1996), Lienhart (1999)
- **Range**: [0, 1]
- **Better**: Lower (smoother transitions)
- **Implementation**: `metrics/video/scene_analysis.py`

#### Frame Interpolation Quality
- **What**: Tests motion smoothness via frame interpolation
- **Research**: Jiang et al. (2018) - Super SloMo
- **Range**: [0, 1]
- **Better**: Higher (smoother motion)
- **Implementation**: `metrics/video/scene_analysis.py`

### Core Video Metrics

#### Temporal Consistency
- **What**: Frame-to-frame pixel difference for measuring stability
- **Research**: Liu et al. (2010) - Optical flow spatial statistics
- **Range**: [0, ∞)
- **Better**: Lower (less change between frames)
- **Implementation**: `metrics/video/temporal_consistency.py`

#### Motion Smoothness
- **What**: Optical flow jitter analysis
- **Range**: [0, ∞)
- **Better**: Lower (smoother motion)

#### Temporal SSIM
- **What**: Structural Similarity Index Measure applied temporally across video frames
- **Research**: Wang et al. (2004) - SSIM, Pinson & Wolf (2004) - Video quality assessment
- **Range**: [0, 1]
- **Better**: Higher (better temporal structure preservation)
- **Parameters**: Temporal weight (0.5), grayscale conversion
- **Implementation**: `metrics/video/temporal_ssim.py`

#### Motion Magnitude
- **What**: Amount of motion in video
- **Range**: [0, ∞)
- **Better**: Depends on use case

### Model-Based Metrics

#### FVD (Fréchet Video Distance)
- **What**: Video quality and diversity measurement
- **Research**: Unterthiner et al. (2018)
- **Range**: [0, ∞)
- **Better**: Lower (better quality)
- **Requires**: PyTorch, I3D model

#### LPIPS (Learned Perceptual Similarity)
- **What**: Deep perceptual similarity
- **Research**: Zhang et al. (2018)
- **Range**: [0, 1]
- **Better**: Lower (more similar)
- **Requires**: PyTorch, AlexNet

#### FID (Fréchet Inception Distance)
- **What**: Image quality and diversity
- **Research**: Heusel et al. (2017)
- **Range**: [0, ∞)
- **Better**: Lower (better quality)
- **Requires**: PyTorch, Inception-v3

**For full metric details, see:**
- Video metrics: `metrics/video/`
- Image metrics: `metrics/image/`
- Configuration: `config/metrics.yaml`

---

## Result Storage Structure

Results are organized hierarchically for easy access and comparison:

```
workdir/
└── outputs/
    └── {task_name}/                    # e.g., "text_to_video_generic"
        └── {dataset_id}/               # e.g., "dataset_001"
            ├── {model_id}_results.json # Per-model results
            └── {model_id}_results.json
```

**Key Features:**
- ✅ Clean, readable directory names (no hashes)
- ✅ Easy to locate results by task and dataset
- ✅ Each model's results stored separately
- ✅ Supports incremental evaluation (add more models later)

## Troubleshooting

### "opencv-python is required"
```bash
pip install opencv-python
```

### "torch/torchvision is required"
```bash
pip install torch torchvision
```

### "No module named 'scipy'"
```bash
pip install scipy
```

### Dimension mismatch warnings
This is normal when comparing models with different resolutions/FPS. The system will warn you but continue evaluation.

### Out of memory errors
For model-based metrics (FID, FVD, LPIPS), reduce batch size in metric configuration or use CPU instead of GPU.

---

## Best Practices

1. **Task Selection**: Choose the appropriate task type:
   - `text_to_video_generic` - For T2V generation
   - `image_to_video_generic` - For I2V animation
   - `video_to_video_generic` - For V2V editing/enhancement
   - `text_to_image_generic` - For T2I generation

2. **Metric Selection**:
   - **T2V**: Use temporal metrics + FVD/LPIPS (no reference needed)
   - **I2V**: Use first-frame + temporal metrics
   - **V2V**: Use all frame-level + temporal metrics
   - **T2I**: Use image quality + texture metrics

3. **Model Versioning**: Set model versions in database metadata:
   ```python
   model.meta_data = {"version": "v2.1"}
   ```
   If not set, system uses `v1.0_m` (auto-generated indicator)

4. **Batch Processing**: For large evaluations, adjust batch sizes in metric parameters

5. **Result Organization**: Results are automatically organized by task and dataset for easy comparison

---

## What's New

### Dec 2025: Master JSON Integration ✨
- **🎯 New Interface:** `run_from_master_json()` for direct Master JSON evaluation
- **🚀 No Symlinks:** Eliminates file management complexity and index mapping bugs
- **🌐 All Task Types:** Supports T2V, V2V, I2V, T2I, I2I with automatic mode detection
- **📦 Reference Handling:** Automatic download of reference videos/images for V2V/I2V
- **🔄 S3 Integration:** Downloads generated and reference media from S3 on-demand
- **⚡ Cleaner Code:** ~200 lines removed from integration layer

### Nov 2025: Enhanced Metrics
- **6 new temporal consistency metrics** with scientific research backing
- **Image-to-video (I2V) task support** with 16 specialized metrics
- **Simplified result storage** - clean directory structure without hashes
- **All metrics are free** - no API keys or paid dependencies required

### 🔧 Key Improvements
- Direct Master JSON interface (no intermediate file formats)
- Automatic no-reference vs with-reference detection
- Intelligent value extraction (absolute vs difference)
- Enhanced metric documentation with research citations
- Better organization of deterministic vs model-based metrics
- Comprehensive multi-task support

### 📊 Metric Count
- **T2V**: 11 metrics (9 deterministic + 2 model-based)
- **I2V**: 16 metrics (15 deterministic + 1 model-based)
- **V2V**: 13 metrics (12 deterministic + 1 model-based)
- **T2I**: 14 metrics (12 deterministic + 2 model-based)

---

## Research References

All metrics are based on peer-reviewed research:

- **Optical Flow**: Lucas & Kanade (1981), Horn & Schunck (1981)
- **Temporal Consistency**: Lai et al. (2018), Bonneel et al. (2015)
- **Scene Detection**: Boreczky & Rowe (1996), Lienhart (1999)
- **Interpolation**: Jiang et al. (2018) - Super SloMo
- **Perceptual Metrics**: Zhang et al. (2018) - LPIPS
- **Video Quality**: Unterthiner et al. (2018) - FVD
- **Image Quality**: Heusel et al. (2017) - FID

See `config/metrics.yaml` for complete citations.

---

## Contact & Support

For issues or questions, check:
- Metric implementations in `metrics/video/` and `metrics/image/`
- Configuration files in `config/`
- Job execution in `backend/services/eval/`
