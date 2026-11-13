# Download Coke Assets (AEM → S3)

Downloads Coca-Cola bottle/can product images + soccer 2026 campaign images from TCCC's AEM DAM and streams them directly to S3.

## What it downloads

1. **Product images** (bottles, cans) for Coca-Cola brand variants across 30 countries
   - DAM path: `/content/dam/tccc/products/{country}/{brand}/...`
   - Brands: coca-cola, coca-cola-energy, coca-cola-zero, diet-coke, etc.

2. **Soccer/FIFA 2026 campaign images**
   - DAM path: `/content/dam/tccc/marketing/coca-cola/{campaign}/...`
   - Campaigns: soccer-na-2026, road-to-fifa-2025, fifa-worldcup2026, football-always-on, etc.

**Only image files**: jpg, png, tiff, gif, webp, psd, ai, eps, heic, svg, bmp

Last crawl found **~14,709 images** across 4,726 folders.

## Setup on a new machine

```bash
# 1. Copy this entire folder to the remote machine
scp -r download_coke_assets/ user@remote:~/

# 2. Requires Node.js >= 18
node --version

# 3. Install deps
cd download_coke_assets
npm install

# 4. Update AWS credentials in aws_creds.env
#    (the session token expires — get fresh ones)

# 5. Run
chmod +x run.sh
./run.sh
```

## Files

| File | Description |
|------|-------------|
| `run.sh` | One-command runner: generates token → downloads → uploads |
| `src/get_token.js` | Generates AEM bearer token from service account |
| `src/bulk_download.js` | Crawls DAM folders + streams images to S3 |
| `creds/service_account.json` | AEM service account (private key + client secret) |
| `aws_creds.env` | AWS session credentials (update before running) |
| `image_manifest.json` | Cached list of 14,709 image paths (skip re-crawl) |
| `bearer_token.txt` | Generated AEM bearer token (auto-created by get_token.js) |

## Usage

```bash
# Full run (generates token, crawls DAM, uploads to S3)
./run.sh

# Fresh crawl (ignore cached manifest)
FRESH_CRAWL=1 ./run.sh

# Just generate a new token
npm run token

# Just upload using cached manifest
source aws_creds.env
npm run download:skip-crawl
```

## Environment overrides

| Var | Default | Description |
|-----|---------|-------------|
| `S3_BUCKET` | `foundry-tccc-enterprise-adobe-assets` | Target S3 bucket |
| `S3_PREFIX` | `dam_assets_downloaded_by_hs` | S3 key prefix |
| `AWS_REGION` | `us-west-2` | AWS region |
| `UPLOAD_CONCURRENCY` | `15` | Parallel upload streams |
| `LIST_TIMEOUT_MS` | `15000` | Folder listing timeout |
| `AEM_BASE_URL` | `https://author-p64403-e609778.adobeaemcloud.com` | AEM instance |

## Notes

- The AEM bearer token expires in **24 hours** — `run.sh` regenerates it each time.
- AWS session tokens expire too — update `aws_creds.env` with fresh ones.
- The service account certificate expires **2026-12-22**.
- Some DAM folders timeout (known issue with TCCC's AEM) — the script skips them and continues.
- Images stream directly AEM → S3, no local disk usage.
- Target: `s3://foundry-tccc-enterprise-adobe-assets/dam_assets_downloaded_by_hs/`
