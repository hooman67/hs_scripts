# Select Subject Vector Pipeline (v0.11.6.1)

Vector-optimized Select Subject pipeline using MFM v0.11.6.1 architecture.

## Why Separate Implementation?

To avoid disrupting the standard pipeline while supporting vector-specific requirements:
- Different model architecture (v0.11.6.1 vs v0.11.7.0)
- BGR channel ordering for MFM compatibility
- Full-image refinement strategy

## Key Differences

### 1. BGR Channel Ordering
MFM models were trained with BGR images (OpenCV/mmcv default). Two BGR conversions:
- **Backbone** (`backbone_component.py` line 81): RGB→BGR before feature extraction
- **Refine Bundle** (`rb_task_component.py` line 112): RGB→BGR before mask refinement (the onnx/trt model expected BGR )

### 2. Architecture (v0.11.6.1)
- **5 TRT models**: backbone, neck, pixel_decoder, task, refine_bundle
- **No pixel_decoder_adapter** (unlike v0.11.7.0 which has 6 models)
- Direct connection: pixel_decoder → task_head

### 3. Full-Image Refinement
Uses single full-image bounding box instead of region-based processing for better vectorization results.

## Pipeline Flow

```
RGB Image → Backbone (BGR) → Features → Task → Base Masks → Refine (BGR) → Final Masks
```

## Usage

Deployed as `select_subject_vector_ssv5` worker. Shares API adapters with standard pipeline from `../endpoints/`.

