# Caption Monitoring Scripts

This directory contains scripts to help you monitor and analyze the captions being generated and stored in your S3 bucket.

## Scripts Available

### 1. `list_recent_captions.py` - Basic Python Script
A comprehensive Python script for listing and retrieving recent captions.

**Usage:**
```bash
# List 10 most recent captions
python list_recent_captions.py

# List 20 most recent captions
python list_recent_captions.py --limit 20

# Show caption content
python list_recent_captions.py --show-content

# Use different bucket
python list_recent_captions.py --bucket your-bucket-name

# Download a specific caption
python list_recent_captions.py --download "4guvu/vvk0ra8g5ajj917e/70a1f20ca2b351cbca9fd75f9d049c7e.json"
```

### 2. `list_recent_captions_simple.sh` - Simple Shell Script
A lightweight shell script using AWS CLI.

**Usage:**
```bash
# List 10 most recent captions (default)
./list_recent_captions_simple.sh

# List 20 most recent captions
./list_recent_captions_simple.sh 20

# Use different bucket
./list_recent_captions_simple.sh 10 "your-bucket-name"
```

### 3. `caption_monitor.py` - Advanced Monitoring Script
An enhanced script with filtering, analysis, and monitoring capabilities.

**Usage:**
```bash
# Basic listing
python caption_monitor.py

# Show only captions from last 2 hours
python caption_monitor.py --hours 2

# Filter by pattern (e.g., only captions with "4guvu" in the path)
python caption_monitor.py --filter "4guvu"

# Show content and limit to 5 results
python caption_monitor.py --limit 5 --show-content

# Run analysis on recent captions
python caption_monitor.py --analyze

# Download specific caption
python caption_monitor.py --download "4guvu/vvk0ra8g5ajj917e/70a1f20ca2b351cbca9fd75f9d049c7e.json"
```

## Quick Commands for Daily Use

### Check Recent Captions (Simple)
```bash
# Quick check of last 5 captions
./list_recent_captions_simple.sh 5
```

### Monitor Caption Quality
```bash
# Check last 10 captions with content
python caption_monitor.py --limit 10 --show-content
```

### Check Recent Activity
```bash
# See captions from last hour
python caption_monitor.py --hours 1
```

### Download for Local Review
```bash
# Download a specific caption
python caption_monitor.py --download "4guvu/vvk0ra8g5ajj917e/70a1f20ca2b351cbca9fd75f9d049c7e.json" --save-to "caption_review.json"
```

## Prerequisites

1. **AWS CLI configured** with appropriate permissions to access your S3 bucket
2. **Python 3.6+** with boto3 installed:
   ```bash
   pip install boto3
   ```
3. **jq** (optional, for JSON formatting in shell script):
   ```bash
   brew install jq  # macOS
   # or
   sudo apt-get install jq  # Ubuntu/Debian
   ```

## S3 Bucket Structure

Your captions are stored with this structure:
```
s3://genie-qwen2dot5-32b-instruct-fp8-image-structured-captions/
├── 4guvu/
│   └── vvk0ra8g5ajj917e/
│       └── 70a1f20ca2b351cbca9fd75f9d049c7e.json
├── [random_string]/
│   └── [random_folder]/
│       └── [hash].json
└── ...
```

## Tips for Quality Monitoring

1. **Regular Checks**: Run the scripts periodically to monitor caption quality
2. **Filter by Time**: Use `--hours` to check recent activity
3. **Content Review**: Use `--show-content` to see actual caption text
4. **Pattern Analysis**: Use `--analyze` to understand generation patterns
5. **Download Samples**: Download specific captions for detailed review

## Troubleshooting

- **Permission Errors**: Ensure your AWS credentials have S3 read permissions
- **Empty Results**: Check if the bucket name is correct and contains .json files
- **Slow Performance**: The scripts fetch all objects first, then filter. For very large buckets, consider using S3 inventory or other AWS tools for better performance.
