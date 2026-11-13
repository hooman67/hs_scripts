# Paste this into Claude Code on the remote machine

```
I need you to resume a bulk download of Coca-Cola images from their AEM DAM to S3. Everything is already set up in this directory. Here's the context:

## What this project does
- Downloads ~14,709 Coca-Cola product images (bottles, cans) and soccer/FIFA 2026 campaign images from TCCC's AEM as a Cloud Service DAM
- Streams them directly to S3 (no local disk) at: s3://foundry-tccc-enterprise-adobe-assets/dam_assets_downloaded_by_hs/
- AEM author instance: https://author-p64403-e609778.adobeaemcloud.com
- Auth: JWT service account → bearer token (auto-generated)

## What's already done
- The image_manifest.json has 14,709 image paths already crawled from the DAM
- About 54 images were already uploaded to S3 before we stopped
- The script, token generator, and credentials are all here and working

## What I need you to do

1. First, update aws_creds.env if I give you new credentials (the session token may have expired)
2. Generate a fresh AEM bearer token: `npm run token`
3. Run the download using the cached manifest: `npm run download:skip-crawl`
4. Monitor progress and handle any issues

The script has:
- 15 concurrent upload workers
- 30s idle timeout on streams (aborts stalled downloads)
- 3 min hard timeout per asset
- Progress logging every 30s

Key files:
- src/bulk_download.js - main download script
- src/get_token.js - AEM token generator
- creds/service_account.json - AEM service account
- image_manifest.json - cached list of 14,709 image DAM paths
- aws_creds.env - AWS credentials (may need refreshing)

Run it and let me know how it goes. If uploads stall, check if the AEM token or AWS creds expired.
```
