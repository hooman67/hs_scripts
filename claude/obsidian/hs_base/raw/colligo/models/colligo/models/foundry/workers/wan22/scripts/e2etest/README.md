# WAN 2.2 1080p Upsampler E2E Evaluation

End-to-end evaluation script for the WAN 2.2 1080p upsampler model.

## Quick Start

```bash
# Using localhost endpoint (for local development)
# Note: Default output-dir is /mnt/localssd/upsampler_results (local disk usually has limited space)
python run_upsampler_eval.py \
    --csv input.csv \
    --endpoint http://localhost:8000 \
    --limit 5

# Using remote endpoint with S3 upload
python run_upsampler_eval.py \
    --csv input.csv \
    --endpoint https://wan-upsampler.ethos851-stage-or2.ethos.adobe.net/ \
    --s3-bucket foundry-nbcu-adobe-assets \
    --s3-prefix eval/wan22_1080p_upsampler
```

## API Endpoint

**Endpoint:** `POST /v1/wan/v22_nbcu_upsampler_1080`

**Worker:** `wan_22_nbcu_upsampler_1080`

**Example Payload:**
```json
{
  "inputVideo": {"id": "71a4b7e9-57c5-4f71-84f9-91223c4b6c78"},
  "inputImage": {"id": "b8987f12-1dbd-4266-87c4-c9d7082f5492"},
  "prompt": "upsample",
  "widthPx": 1920,
  "heightPx": 1072,
  "seed": 42,
  "output": {}
}
```

## CSV Format

The input CSV should have these columns from the wan-vace-training validation set:

| Column | Required | Description |
|--------|----------|-------------|
| `video` | Yes | S3 URL to input video (480p) |
| `prompt` | Yes | Description text |
| `image` | Yes | S3 URL to input keyframe image |

Example CSV (from `reliable_validation_gr6_kf.csv`):

```csv
video,prompt,image
s3://foundry-nbcu-adobe-assets/training_logs/.../row0_vid2.mp4,"Gabby stands in her whimsical bedroom...",s3://foundry-nbcu-adobe-assets/training_logs/.../row0_img0.jpg
s3://foundry-nbcu-adobe-assets/training_logs/.../row12_vid2.mp4,"Gabby stands in a cozy, striped-wall bedroom...",s3://foundry-nbcu-adobe-assets/training_logs/.../row12_img0.jpg
```

## How It Works

1. **Download inputs:** Downloads video + image from S3 URLs in CSV
2. **Upload to temp storage:** Uploads to endpoint's temp storage to get asset IDs
3. **Call upsampler API:** Sends request with asset IDs to `/v1/wan/v22_nbcu_upsampler_1080`
4. **Download output:** Downloads upsampled 1080p video
5. **Upload to S3:** (Optional) Uploads input/output videos to S3
6. **Generate HTML:** Creates comparison page with side-by-side videos

## Script Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--csv` | `input.csv` | Path to CSV file with video metadata |
| `--endpoint` | `http://localhost:8000` | Upsampler endpoint URL |
| `--output-dir` | `/mnt/localssd/upsampler_results` | Local output directory (uses local SSD by default) |
| `--s3-bucket` | None | S3 bucket for results (optional) |
| `--s3-prefix` | `eval/wan22_1080p_upsampler` | S3 prefix |
| `--width` | `1920` | Output width in pixels |
| `--height` | `1072` | Output height in pixels |
| `--seed` | `42` | Random seed |
| `--aws-profile` | `foundry` | AWS profile name |
| `--limit` | None | Limit number of videos to process |
| `--skip` | `0` | Skip first N videos |

## Output Structure

Local output directory (default: `/mnt/localssd/upsampler_results/`):
```
/mnt/localssd/upsampler_results/
├── index.html              # HTML comparison viewer
├── config.json             # Run configuration
├── results.json            # Detailed results JSON
├── video_000_input.mp4     # Input videos (480p)
├── video_000_input.jpg     # Input keyframe images
├── video_000_output.mp4    # Upsampled output videos (1080p)
├── video_000.json          # Per-video metadata
└── ...
```

S3 output (if configured):
```
s3://bucket/prefix/compare_YYYY-MM-DD_HH-MM-SS/
└── (same structure as local)
```

## Example Usage

### Test with first 3 videos locally

```bash
python run_upsampler_eval.py \
    --csv input.csv \
    --endpoint http://localhost:8000 \
    --limit 3
```

### Full evaluation with S3 upload

```bash
python run_upsampler_eval.py \
    --csv input.csv \
    --endpoint https://wan-upsampler.ethos851-stage-or2.ethos.adobe.net/ \
    --s3-bucket foundry-nbcu-adobe-assets \
    --s3-prefix eval/wan22_1080p_upsampler/v1
```

### Resume from row 10

```bash
python run_upsampler_eval.py \
    --csv input.csv \
    --skip 10
```

## Requirements

- Python 3.10+
- `aiohttp` for async HTTP
- AWS CLI configured with `foundry` profile
- Access to S3 bucket with input videos

Install dependencies:
```bash
pip install aiohttp
```

## Troubleshooting

### S3 download fails
- Check that the S3 URLs in the CSV are accessible
- Verify AWS credentials: `aws --profile foundry sts get-caller-identity`
- Verify S3 access: `aws --profile foundry s3 ls s3://foundry-nbcu-adobe-assets/`

### Endpoint connection fails
- For localhost: ensure the upsampler service is running on port 8000
- For remote: check network connectivity and endpoint URL
- Verify endpoint: `curl <endpoint>/health` (if health endpoint exists)

### Temp storage upload fails
- Check that the endpoint has a temp storage API at `/v1/storage/assets`
- Verify the endpoint accepts multipart form uploads

### Output video download fails
- Check that the API response includes a valid video URL in `outputs[0].video.url`
- Verify presigned URL hasn't expired

## Input CSV

The provided `input.csv` contains 50 validation videos from the wan-vace-training repo:
- **Source:** `https://github.com/Adobe-Firefly/wan-vace-training/blob/idave_v2upsampler/lowres_data/reliable_validation_gr6_kf.csv`
- **Resolution:** 480p inputs → 1080p outputs
- **Content:** Gabby's Dollhouse validation set

## Notes

- The script respects rate limiting with 2-second delays between requests
- All files are downloaded/uploaded sequentially to avoid overwhelming the endpoint
- Failed videos are logged but don't stop the batch processing
- HTML viewer shows side-by-side comparison of input and output videos
